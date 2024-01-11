from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
import heapq
import logging
from threading import Thread, Condition, Event, Lock, Timer
import traceback
from types import TracebackType
from typing import (Optional, Literal, Protocol, Any, Sequence,
                    Iterable, Final, Union, Callable, NamedTuple)

from erk.stringutils import match_width
from quantities.SI import sec, ms
from quantities.dimensions import Time
from quantities.ticks import Ticks, TickNumber, ticks
from quantities.timestamp import time_now, time_in, Timestamp


logger = logging.getLogger(__name__)


def _in_secs(t: Time) -> float:
    return t.as_number(sec)

_wait_timeout: float = _in_secs(0.5*sec)

TimerFunc = Callable[[], Optional[Union[Time,Timestamp]]]
ClockCallback = Callable[[], Optional[Ticks]]

_trace_ticks: bool = False

class State(Enum):
    NEW = auto()
    RUNNING = auto()
    SHUTDOWN_REQUESTED = auto()
    ABORT_REQUESTED = auto()
    DEAD = auto()

class Worker:
    idle_barrier: IdleBarrier
    desc: Any

    @property
    def is_idle(self) -> bool:
        return self not in self.idle_barrier.running_components

    def __init__(self, idle_barrier: IdleBarrier, desc: Optional[Any] = None) -> None:
        self.idle_barrier = idle_barrier
        if desc is None:
            desc = f"@{id(self)}"
        self.desc = desc
        
    def __str__(self) -> str:
        return f"{type(self).__name__}[{self.desc}]"

    def not_idle(self) -> None:
        self.idle_barrier.running(self)

    def idle(self) -> None:
        self.idle_barrier.idle(self)

class IdleBarrier:
    event: Event
    lock: Lock
    running_components: set[Worker]

    def __init__(self) -> None:
        self.event = Event()
        self.event.set()
        self.lock = Lock()
        self.running_components = set[Worker]()

    def running(self, component: Worker) -> None:
        with self.lock:
            self.event.clear()
            self.running_components.add(component)
            # logger.debug(f"Running {component} [{map_str(self.running_components)}]")
            # print(f"{component} not idle [{len(self.running_components)}]")

    def idle(self, component: Worker) -> None:
        with self.lock:
            self.running_components.discard(component)
            # logger.debug(f"Idle {component} [{map_str(self.running_components)}]")
            # print(f"{component} idle [{len(self.running_components)}]")
            if len(self.running_components) == 0:
                # print("System is idle")
                self.event.set()

    def wait(self, timeout: Optional[float] = None) -> None:
        # logger.debug(f"wait(): {map_str(self.running_components)}")
        self.event.wait(timeout)
        # logger.debug(f"back from wait(): {map_str(self.running_components)}")

class Updatable(Protocol):
    def update_state(self) -> Any: ...

# class DevCommRequest:
#     component: Optional[Updatable]
#     def __init__(self, component: Optional[Updatable], cb: Callback):
#         self.component = component
#         self.callback: Callback = cb
#     def prepare(self) -> Any:
#         (self.callback)()
#

DevCommRequest = Callable[[], Iterable[Updatable]]
ClockRequest = tuple[Ticks, ClockCallback]
ClockCommRequest = tuple[Ticks, DevCommRequest]
TimerRequest = tuple[Timestamp, TimerFunc, bool]
TimerDeltaRequest = tuple[Time, TimerFunc, bool]

class Engine:
    idle_barrier: IdleBarrier
    dev_comm_thread: DevCommThread
    timer_thread: TimerThread
    clock_thread: ClockThread

    def __init__(self, *,
                 default_clock_interval: Time) -> None:
        self.idle_barrier = IdleBarrier()
        self.dev_comm_thread = DevCommThread(self)
        self.timer_thread = TimerThread(self)
        self.clock_thread = ClockThread(self, default_clock_interval=default_clock_interval)

    def _join_threads(self) -> None:
        if self.dev_comm_thread.is_alive():
            self.dev_comm_thread.join()
        if self.timer_thread.is_alive():
            self.timer_thread.join()
        if self.clock_thread.is_alive():
            self.clock_thread.join()

    def start(self) -> None:
        pass

    def stop(self) -> None:
        self.dev_comm_thread.request_stop()
        self.timer_thread.request_stop()
        self.clock_thread.request_stop()
        self._join_threads()

    def abort(self) -> None:
        self.dev_comm_thread.request_abort()
        self.timer_thread.request_abort()
        self.clock_thread.request_abort()
        self._join_threads()

    def __enter__(self) -> Engine:
        return self

    def __exit__(self,
                 exc_type: Optional[type[BaseException]],  # @UnusedVariable
                 exc_val: Optional[BaseException],  # @UnusedVariable
                 exc_tb: Optional[TracebackType]  # @UnusedVariable
                 ) -> Literal[False]:
        self.idle_barrier.wait()
        return False

    def communicate(self, reqs: Sequence[DevCommRequest]) -> None:
        self.dev_comm_thread.add_requests(reqs)

    def call_at(self, reqs: Sequence[TimerRequest]) -> None:
        self.timer_thread.call_at(reqs)

    def call_after(self, reqs: Sequence[TimerDeltaRequest]) -> None:
        self.timer_thread.call_after(reqs)

    def before_tick(self, reqs: Sequence[ClockRequest]) -> None:
        self.clock_thread.before_tick(reqs)

    def after_tick(self, reqs: Sequence[ClockRequest]) -> None:
        self.clock_thread.after_tick(reqs)

    def on_tick(self, reqs: Sequence[ClockCommRequest]) -> None:
        self.clock_thread.on_tick(reqs)


class WorkerThread(Thread, Worker, ABC):
    engine: Engine
    state: State
    lock: Lock

    def __init__(self, engine: Engine, name: str) -> None:
        # super().__init__(*args, **kwdargs)
        Thread.__init__(self, name=name, daemon=True)
        Worker.__init__(self, engine.idle_barrier)
        self.engine = engine
        self.state = State.NEW
        self.lock = Lock()

    @abstractmethod
    def wake_up(self) -> None:
        ...

    def request_abort(self) -> None:
        if self.state is State.RUNNING:
            with self.lock:
                self.state = State.ABORT_REQUESTED
                # self.daemon = True
                self.wake_up()

    def request_stop(self) -> None:
        if self.state is State.RUNNING:
            with self.lock:
                self.state = State.SHUTDOWN_REQUESTED
                self.wake_up()

    # If I do this inline, MyPy complains about "non-overlapping identity check"
    def abort_requested(self) -> bool:
        return self.state is State.ABORT_REQUESTED

    # called with lock
    def ensure_running(self) -> None:
        if not self.is_alive():
            self.start()

    # called with lock
    def not_idle(self) -> None:
        super().not_idle()
        # self.idle_barrier.running(self)
        # self.daemon = False
        self.ensure_running()

    # called with lock
    # def idle(self) -> None:
    #     self.idle_barrier.idle(self)
    #     # self.daemon = True
    #
    
    def print_exception(self, ex: Exception) -> None:
        header = f"Exception caught in {self}:"
        print(header)
        print(match_width(header, repeating="-"))
        traceback.print_exception(type(ex), ex, ex.__traceback__)

class DCReqQueue(NamedTuple):
    requests: list[DevCommRequest] = []
    events: list[Event] = []

class DevCommThread(WorkerThread):
    condition: Condition
    requests: Final[list[DevCommRequest]]
    signals: Final[list[Event]]

    def __init__(self, engine: Engine):
        super().__init__(engine, "Device Communication Thread")
        self.condition = Condition(lock=self.lock)
        self.requests = []
        self.signals = []


    # called with lock locked
    def wake_up(self) -> None:
        self.condition.notify()


    def run(self) -> None:
        logger.debug('%s started', self.name)
        try:
            self.state = State.RUNNING
            need_update: set[Updatable] = set()
            condition = self.condition
            while self.state is State.RUNNING:
                with self.lock:
                    while self.state is State.RUNNING and not self.requests:
                        condition.wait(_wait_timeout)
                    if self.abort_requested():
                        return
                    # we don't want to be holding the lock when we process the requests,
                    # because they may want to add to the queue.  (Probably shouldn't,
                    # but they might).  So we'll copy the queue and clear it.
                    requests = self.requests.copy()
                    signals = self.signals.copy()
                    self.requests.clear()
                    self.signals.clear()
                # logger.debug(f"--processing communication queue: length {len(queue_copy)}")
                for req in requests:
                    try:
                        cpts = req()
                        need_update.update(cpts)
                    except RuntimeError as ex:
                        self.print_exception(ex)
                for c in need_update:
                    c.update_state()
                need_update.clear()
                for e in signals:
                    e.set()
                if not self.requests:
                    with self.lock:
                        if not self.requests:
                            self.idle()
        finally:
            logger.info('%s exited', self.name)
            self.state = State.DEAD

    # def add_request(self, req: DevCommRequest) -> None:
    #     assert self.state is State.RUNNING or self.state is State.NEW
    #     with self.lock:
    #         self.queue.append(req)
    #         self.not_idle()
    #         self.wake_up()

    def add_requests(self, reqs: Sequence[DevCommRequest], *,
                     when_done: Optional[Union[Event, Sequence[Event]]] = None) -> None:
        assert self.state is State.RUNNING or self.state is State.NEW
        if len(reqs) > 0 or when_done:
            with self.condition:
                self.requests.extend(reqs)
                if when_done is not None:
                    if isinstance(when_done, Event):
                        self.signals.append(when_done)
                    else:
                        self.signals.extend(when_done)
                self.not_idle()
                self.wake_up()


# FT = tuple[Timestamp, TimerFunc, bool]

class TimerThread(WorkerThread):
    class Entry:
        desired_time: Final[Timestamp]
        is_daemon: Final[bool]

        def __init__(self, desired_time: Timestamp, func: TimerFunc, is_daemon: bool):
            self.desired_time = desired_time
            self.func: Final[TimerFunc] = func
            self.is_daemon = is_daemon

        def __lt__(self, other: TimerThread.Entry) -> bool:
            my_time = self.desired_time
            their_time = other.desired_time
            if my_time < their_time:
                return True
            elif their_time < my_time:
                return False
            else:
                return id(self.func) < id(other.func)

        def __repr__(self) -> str:
            return f"Entry({self.desired_time}, {self.func}{', daemon' if self.is_daemon else ''})@{id(self)}"

    class MyTimer(Timer):
        timer_thread: TimerThread
        target_time: Timestamp
        started: bool
        daemon_task: Final[bool]


        def __init__(self, timer_thread: TimerThread, target_time: Timestamp, delay: Time,
                     func: TimerFunc, daemon: bool) -> None:
            super().__init__(_in_secs(delay), lambda : self.call_func())
            self.name=f"MyTimer ({target_time})"
            self.timer_thread = timer_thread
            self.target_time = target_time
            self.func: TimerFunc = func
            self.started = False
            self.daemon_task = daemon
            # print(f"Pausing for {delay} until {target_time} for {func}")

        def call_func(self) -> None:
            self.started = True
            next_time: Optional[Union[Timestamp, Time]] = (self.func)()
            tt = self.timer_thread
            with tt.lock:
                if next_time:
                    if isinstance(next_time, Time):
                        next_time = time_in(next_time)
                    heapq.heappush(tt.queue, TimerThread.Entry(next_time, self.func, self.daemon_task))
                elif self.daemon_task:
                    tt.n_daemons -= 1
                tt.timer = None
                if len(tt.queue) == tt.n_daemons:
                    tt.idle()
                tt.wake_up()

    condition: Condition
    queue: list[Entry]
    timer: Optional[MyTimer]
    n_daemons: int

    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, "Timer Thread")
        self.condition = Condition(lock=self.lock)
        self.queue = []
        self.timer = None
        self.n_daemons = 0

    def wake_up(self) -> None:
        self.condition.notify()

    def run(self) -> None:
        logger.debug('%s started', self.name)
        try:
            queue = self.queue
            condition = self.condition
            lock = self.lock
            self.state = State.RUNNING
            while self.state is State.RUNNING or (self.state is State.SHUTDOWN_REQUESTED and not self.is_idle):
                # desired_time: Timestamp
                with lock:
                    while ((self.state is State.RUNNING and (not queue or self.timer is not None))
                            or
                            self.state is State.SHUTDOWN_REQUESTED and self.timer is not None):
                        condition.wait(_wait_timeout)
                    if self.abort_requested():
                        return
                    if self.state is State.SHUTDOWN_REQUESTED and self.is_idle:
                        return
                    assert self.timer is None
                    if not queue:
                        assert self.state is not State.RUNNING
                        return
                    entry = heapq.heappop(queue)
                # we're now not locked, so we can safely either run the function or schedule it
                now: Timestamp = time_now()
                if now >= entry.desired_time:
                    try:
                        next_time: Optional[Union[Time,Timestamp]] = entry.func()
                        if next_time:
                            if isinstance(next_time, Time):
                                next_time = time_in(next_time)
                            with condition:
                                heapq.heappush(queue, TimerThread.Entry(next_time, entry.func, entry.is_daemon))
                    except RuntimeError as ex:
                        self.print_exception(ex)
                    if len(queue) == self.n_daemons:
                        self.idle()
                else:
                    with condition:
                        self.timer = self.MyTimer(self, entry.desired_time, entry.desired_time-now, entry.func, entry.is_daemon)
                        self.timer.start()
        finally:
            logger.info('%s exited', self.name)
            self.state = State.DEAD

    def call_at(self, reqs: Sequence[TimerRequest]) -> None:
        assert self.state is State.RUNNING or self.state is State.NEW
        with self.condition:
            self.not_idle()
            timer = self.timer
            for (t, fn, daemon) in reqs:
                if timer is not None and t < timer.target_time:
                    # We're trying to add something before the one that's (maybe) waiting.  If we
                    # can cancel it, we push it back and then ourselves.  If we can't cancel it, it's
                    # already started, so we just push ourselves.  (We know it's past time for us to run, so
                    # we could just call it here, but I'm not sure how safe that is.)
                    timer.cancel()
                    if not timer.started:
                        heapq.heappush(self.queue, TimerThread.Entry(timer.target_time, timer.func, timer.daemon_task))
                        self.timer = None
                heapq.heappush(self.queue, TimerThread.Entry(t, fn, daemon))
                if daemon:
                    self.n_daemons += 1
                if len(self.queue) == self.n_daemons:
                    self.idle()
            self.wake_up()

    def call_after(self, reqs: Sequence[TimerDeltaRequest]) -> None:
        now = time_now()
        self.call_at([(now+delta, fn, daemon) for (delta, fn, daemon) in reqs])

CT = tuple[Ticks, ClockCallback]

class ClockThread(WorkerThread):
    class TickRequest:
        cancelled: bool
        clock: ClockThread

        def __init__(self, clock: ClockThread) -> None:
            self.cancelled = False
            self.clock = clock

        def __repr__(self) -> str:
            return "<Tick Request>"

        def __call__(self) -> Optional[Time]:
            # next_tick = time_in(self.clock.update_interval)
            if not self.cancelled:
                self.clock.tick_event.set()
                # return next_tick
                return self.clock.update_interval
            return None

        def cancel(self) -> None:
            self.cancelled = True
            if self.clock.outstanding_tick_request is self:
                self.clock.outstanding_tick_request = None

    running: bool
    tick_event: Event
    pre_tick_queue: list[CT]
    post_tick_queue: list[CT]
    on_tick_queue: list[tuple[Ticks, DevCommRequest]]
    update_interval: Time
    work: int
    next_tick: TickNumber
    last_tick_time: Timestamp
    outstanding_tick_request: Optional[TickRequest]

    def __init__(self, engine: Engine, *, default_clock_interval: Time) -> None:
        super().__init__(engine, "Clock Thread")
        self.running = False
        self.tick_event = Event()
        self.pre_tick_queue = []
        self.post_tick_queue = []
        self.on_tick_queue = []
        self.work = 0
        self.next_tick = TickNumber.ZERO()
        self.last_tick_time = Timestamp.never()
        self.outstanding_tick_request = None
        self.update_interval = default_clock_interval

    def _process_queue(self, queue: Sequence[CT], *, tag: Optional[str]=None) -> list[CT]:
        new_queue: list[CT] = []
        if _trace_ticks and len(queue) > 0:
            print(f">> processing {tag} queue")
        for (delay, fn) in queue:
            if delay > 0:
                new_queue.append((delay-1, fn))
            else:
                if _trace_ticks:
                    print(f"-- calling {fn}")
                try:
                    new_delay: Optional[Ticks] = fn()
                    if new_delay is not None:
                        assert new_delay >= 0, f"Delay returned by before/after tick callback ({new_delay}) cannot be negative"
                        assert new_delay > 0, (f"Delay returned by before/after tick callback ({new_delay}) "
                                               + "is relative to current tick number, and so cannot be zero")
                        # The least astonishing return value for something that should happen on relative to the next tick
                        # is 1*tick, not 0*ticks
                        new_queue.append((new_delay-1, fn))
                except RuntimeError as ex:
                    self.print_exception(ex)
                
        if _trace_ticks and len(queue) > 0:
            deferred = len(new_queue)
            processed = len(queue)-deferred
            print(f"<< processed {tag} queue: processed {processed}, deferred {deferred}")
        return new_queue

    def wake_up(self) -> None:
        self.tick_event.set()

    def run(self) -> None:
        logger.debug('%s started', self.name)
        lock = self.lock
        update_finished = Event()
        tick_event = self.tick_event
        comm_thread = self.engine.dev_comm_thread
        last_time: Timestamp = time_now()
        try:
            self.state = State.RUNNING
            while self.state is State.RUNNING or self.state is State.SHUTDOWN_REQUESTED and self.work > 0:
                while not tick_event.wait(_wait_timeout):
                    pass
                tick_event.clear()
                if self.abort_requested():
                    return
                now = time_now()
                elapsed = now-last_time
                last_time = now
                if _trace_ticks:
                    print(f"** Processing tick #{self.next_tick.number} time is {now} ({elapsed.as_number(ms):.2f} ms since last)")
                self.last_tick_time = now
                queue: list[CT]
                with lock:
                    queue = self.pre_tick_queue
                    self.pre_tick_queue = []
                    self.work -= len(queue)
                new_queue: list[CT] = self._process_queue(queue, tag = "pre-tick")
                rqueue: list[DevCommRequest]
                with lock:
                    self.pre_tick_queue.extend(new_queue)
                    self.work += len(new_queue)
                    rqueue = [req for (delta, req) in self.on_tick_queue if delta <= 0]
                    self.on_tick_queue = [(delta-1, req) for (delta, req) in self.on_tick_queue if delta > 0]
                    self.work -= len(rqueue)
                    if rqueue:
                        if _trace_ticks:
                            print(f"-- processing on-tick queue: length {len(rqueue)}")
                        # def note_finished():
                        #     update_finished.set()
                        #     return ()
                        # rqueue.append(note_finished)
                        comm_thread.add_requests(rqueue, when_done=update_finished)
                    self.next_tick += 1*ticks
                if rqueue:
                    while not update_finished.wait(_wait_timeout):
                        pass
                update_finished.clear()
                with lock:
                    queue = self.post_tick_queue
                    self.post_tick_queue = []
                    self.work -= len(queue)
                new_queue = self._process_queue(queue, tag = "post-tick")
                if new_queue:
                    with lock:
                        self.post_tick_queue.extend(new_queue)
                        self.work += len(new_queue)
                if self.work == 0 or not self.running:
                    self.idle()
        finally:
            logger.info('%s exited', self.name)
            self.state = State.DEAD

    def before_tick(self, reqs: Sequence[ClockRequest]) -> None:
        assert self.state is State.RUNNING or self.state is State.NEW
        with self.lock:
            self.pre_tick_queue.extend(reqs)
            if self.running:
                self.not_idle()
            else:
                self.ensure_running()
            self.work += len(reqs)

    def after_tick(self, reqs: Sequence[ClockRequest]) -> None:
        assert self.state is State.RUNNING or self.state is State.NEW
        with self.lock:
            self.post_tick_queue.extend(reqs)
            if self.running:
                self.not_idle()
            else:
                self.ensure_running()
            self.work += len(reqs)

    def on_tick(self, reqs: Sequence[ClockCommRequest]) -> None:
        assert self.state is State.RUNNING or self.state is State.NEW, f"{self.state}"
        with self.lock:
            self.on_tick_queue.extend(reqs)
            if self.running:
                self.not_idle()
            else:
                self.ensure_running()
            self.work += len(reqs)


    def start_clock(self, interval: Optional[Time] = None) -> None:
        with self.lock:
            assert not self.running
            assert not self.outstanding_tick_request
            if interval is not None:
                self.update_interval = interval
            self.running = True
            tr = self.outstanding_tick_request = self.TickRequest(self)
            self.engine.call_after([(self.update_interval, tr, True)])
            self.ensure_running()
            self.wake_up()

    def pause_clock(self) -> None:
        with self.lock:
            assert self.running
            assert self.outstanding_tick_request
            self.running = False
            self.outstanding_tick_request.cancel()
