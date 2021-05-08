from enum import Enum, auto
from threading import Thread, Condition, Event, Lock, Timer
import heapq
from quantities.SI import sec, ms
from quantities.timestamp import time_now, time_in
from quantities.dimensions import Time
from typing import Optional, Type, Literal, Protocol, Any, Callable, Sequence,\
    Iterable
from types import TracebackType

def _in_secs(t: Time) -> float:
    return t.as_number(sec)

_wait_timeout: float = _in_secs(0.5*sec)

TimerFunc = Callable[[], Optional[Time]]
ClockCallback = Callable[[], Optional[int]]

class  State(Enum):
    NEW = auto()
    RUNNING = auto()
    SHUTDOWN_REQUESTED = auto()
    ABORT_REQUESTED = auto()
    DEAD = auto()
    
class Worker:
    idle_barrier: 'IdleBarrier'
    
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
            
    def idle(self, component: Worker) -> None:
        with self.lock:
            self.running_components.discard(component)
            if len(self.running_components) == 0:
                self.event.set()
                
    def wait(self, timeout: float = None) -> None:
        self.event.wait(timeout)
      
class Updatable(Protocol):
    def update_state(self) -> Any: ...          

Callback = Callable[[], Any]
            
# class DevCommRequest:
#     component: Optional[Updatable]
#     def __init__(self, component: Optional[Updatable], cb: Callback):
#         self.component = component
#         self.callback: Callback = cb    
#     def prepare(self) -> Any:
#         (self.callback)()
#

DevCommRequest = Callable[[], Iterable[Updatable]]

class Engine:
    idle_barrier: IdleBarrier
    dev_comm_thread: 'DevCommThread'
    timer_thread: 'TimerThread'
    clock_thread: 'ClockThread'
    
    def __init__(self) -> None:
        self.idle_barrier = IdleBarrier()
        self.dev_comm_thread = DevCommThread(self)
        self.timer_thread = TimerThread(self)
        self.clock_thread = ClockThread(self)
        
        
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
        
    def __enter__(self) -> 'Engine':
        return self
    
    def __exit__(self, 
                 exc_type: Optional[Type[BaseException]],  # @UnusedVariable
                 exc_val: Optional[BaseException],  # @UnusedVariable
                 exc_tb: Optional[TracebackType]  # @UnusedVariable
                 ) -> Literal[False]:
        self.idle_barrier.wait()
        return False
    
    def communicate(self, req: DevCommRequest):
        self.dev_comm_thread.add_request(req)
        
    def call_at(self, t: Time, fn: TimerFunc):
        self.timer_thread.call_at(t, fn)
        
    def call_after(self, delta: Time, fn: TimerFunc):
        self.timer_thread.call_after(delta, fn)

    def before_tick(self, fn: ClockCallback, *, delta: int=0) -> None:
        self.clock_thread.before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, *, delta: int=0):
        self.clock_thread.after_tick(fn, delta=delta)

    def on_tick(self, req: DevCommRequest, *, delta: int=0):
        self.clock_thread.on_tick(req, delta=delta)
        
        
class WorkerThread(Thread, Worker):
    engine: Engine
    idle_barrier: IdleBarrier
    state: State
    lock: Lock
    
    def __init__(self, engine: Engine, name: str) -> None:
        # super().__init__(*args, **kwdargs)
        super().__init__(name=name, daemon=True)
        self.engine = engine
        self.idle_barrier = engine.idle_barrier
        self.state = State.NEW
        self.lock = Lock()
        
    def wake_up(self) -> None:
        raise NotImplementedError()
    
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

    
class DevCommThread(WorkerThread):
    condition: Condition
    queue: list[DevCommRequest]
    
    def __init__(self, engine: Engine):
        super().__init__(engine, "Device Communication Thread")
        self.condition = Condition(lock=self.lock)
        self.queue = []
        
    # called with lock locked
    def wake_up(self) -> None:
        self.condition.notify()
        
        
    def run(self) -> None:
        try:
            self.state = State.RUNNING
            need_update: set[Updatable] = set()
            queue = self.queue
            condition = self.condition
            while self.state is State.RUNNING:
                queue_copy: list[DevCommRequest]
                with self.lock:
                    while self.state is State.RUNNING and not queue:
                        condition.wait(_wait_timeout)
                    if self.state is State.ABORT_REQUESTED:
                        return
                    # we don't want to be holding the lock when we process the requests,
                    # because they may want to add to the queue.  (Probably shouldn't, 
                    # but they might).  So we'll copy the queue and clear it.
                    queue_copy = queue.copy()
                    queue.clear()
                for req in queue_copy:
                    cpts = req()
                    need_update.update(cpts)
                for c in need_update:
                    c.update_state()
                need_update.clear()
                if not queue:
                    with self.lock:
                        if not queue:
                            self.idle()
        finally:
            print(self.name, "exited")
            self.state = State.DEAD
    
    def add_request(self, req: DevCommRequest) -> None:
        assert self.state is State.RUNNING or self.state is State.NEW
        with self.lock:
            self.queue.append(req)
            self.not_idle()
            self.wake_up()
            
    def add_requests(self, reqs: Sequence[DevCommRequest]) -> None:
        assert self.state is State.RUNNING or self.state is State.NEW
        if len(reqs) > 0:
            with self.condition:
                self.queue.extend(reqs)
                self.not_idle()
                self.wake_up()
            
        
FT = tuple[Time, TimerFunc]

class TimerThread(WorkerThread):
    
    class MyTimer(Timer):
        timer_thread: 'TimerThread'
        target_time: Time
        started: bool
        

        def __init__(self, timer_thread: 'TimerThread', target_time: Time, delay: Time, func: TimerFunc) -> None:
            super().__init__(_in_secs(delay), lambda : self.call_func())
            self.timer_thread = timer_thread
            self.target_time = target_time
            self.func: TimerFunc = func
            self.started = False 
            
        def call_func(self) -> None:
            self.started = True
            next_time: Optional[Time] = (self.func)()
            tt = self.timer_thread
            with tt.lock:
                if next_time:
                    heapq.heappush(tt.queue, (next_time, self.func))
                tt.timer = None
                if not tt.queue:
                    tt.idle()
                tt.wake_up()

    condition: Condition
    queue: list[FT]
    timer: Optional[MyTimer]
                
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, "Timer Thread")
        self.condition = Condition(lock=self.lock)
        self.queue = []
        self.timer = None
        
    def wake_up(self) -> None:
        self.condition.notify()
        
    def run(self) -> None:
        try:
            queue = self.queue
            condition = self.condition
            lock = self.lock
            self.state = State.RUNNING
            while self.state is State.RUNNING or (self.state is State.SHUTDOWN_REQUESTED and queue):
                func = None
                desired_time: Optional[Time] = None
                with lock:
                    while ((self.state is State.RUNNING and (not queue or self.timer is not None))
                            or
                            self.state is State.SHUTDOWN_REQUESTED and self.timer is not None):
                        condition.wait(_wait_timeout)
                    if self.state is State.ABORT_REQUESTED:
                        return
                    assert self.timer is None
                    if not queue:
                        assert self.state is not State.RUNNING
                        return
                    (desired_time, func) = heapq.heappop(queue)
                # we're now not locked, so we can safely either run the function or schedule it
                now: Time = time_now()
                if now >= desired_time:
                    next_time: Optional[Time] = func()
                    if next_time:
                        with condition:
                            heapq.heappush(queue, (next_time, func))
                    elif not queue:
                        self.idle()
                else:
                    with condition:
                        self.timer = self.MyTimer(self, desired_time, desired_time-now, func)
                        self.timer.start()
        finally:
            print(self.name, "exited")
            self.state = State.DEAD
            
    def call_at(self, t: Time, fn: TimerFunc) -> None:
        assert self.state is State.RUNNING or self.state is State.NEW
        with self.condition:
            self.not_idle()
            timer = self.timer
            if timer is not None and t < timer.target_time:
                # We're trying to add something before the one that's (maybe) waiting.  If we
                # can cancel it, we push it back and then ourselves.  If we can't cancel it, it's
                # already started, so we just push ourselves.  (We know it's past time for us to run, so
                # we could just call it here, but I'm not sure how safe that is.)
                timer.cancel()
                if not timer.started:
                    heapq.heappush(self.queue, (timer.target_time, timer.func))
                    self.timer = None
            heapq.heappush(self.queue, (t, fn))  
            self.wake_up()

    def call_after(self, delta: Time, fn: TimerFunc) -> None:
        self.call_at(time_in(delta), fn)

CT = tuple[int, ClockCallback]
                
class ClockThread(WorkerThread):
    class TickRequest:
        cancelled: bool
        clock: 'ClockThread'
        
        def __init__(self, clock: 'ClockThread') -> None:
            self.cancelled = False
            self.clock = clock
            
        def __call__(self) -> Optional[Time]:
            next_tick = time_in(self.clock.update_interval)
            if not self.cancelled:
                self.clock.tick_event.set()
                return next_tick
            return None
                
        def cancel(self) -> None:
            self.cancelled = True
            if self.clock.outstanding_tick_request is self:
                self.clock.outstanding_tick_request = None
                
                
    class note_done:
        event: Event
        component: Optional[Updatable] = None
        def __init__(self, e: Event) -> None:
            self.event = e
        def prepare(self) -> None:
            self.event.set()

    running: bool
    tick_event: Event
    pre_tick_queue: list[CT]
    post_tick_queue: list[CT]
    on_tick_queue: list[tuple[int, DevCommRequest]]
    update_interval: Time = 100*ms
    work: int
    next_tick: int
    last_tick_time: Time
    outstanding_tick_request: Optional[TickRequest]
    
    def __init__(self, engine):
        super().__init__(engine, "Clock Thread")
        self.running = False
        self.tick_event = Event()
        self.pre_tick_queue = []
        self.post_tick_queue = []
        self.on_tick_queue = []
        self.work = 0
        self.next_tick = 0
        self.last_tick_time = 0*sec
        self.outstanding_tick_request = None
        
    def _process_queue(self, queue: Sequence[CT]) -> list[CT]:
        new_queue: list[CT] = []
        for (delay, fn) in queue:
            if delay > 0:
                new_queue.append((delay-1, fn))
            else:
                new_delay: Optional[int] = fn()
                if new_delay is not None:
                    new_queue.append((new_delay, fn))
        return new_queue
    
    def wake_up(self) -> None:
        self.tick_event.set()

        
    def run(self) -> None:
        lock = self.lock
        update_finished = Event()
        tick_event = self.tick_event
        comm_thread = self.engine.dev_comm_thread
        try:
            self.state = State.RUNNING
            while self.state is State.RUNNING or self.state is State.SHUTDOWN_REQUESTED and self.work > 0:
                while not tick_event.wait(_wait_timeout):
                    pass
                tick_event.clear()
                if self.state is State.ABORT_REQUESTED:
                    return
                print("Processing tick ", self.next_tick)
                self.last_tick_time = time_now()
                queue: list[CT]
                with lock:
                    queue = self.pre_tick_queue
                    self.pre_tick_queue = []
                    self.work -= len(queue)
                new_queue: list[CT] = self._process_queue(queue)
                rqueue: list[DevCommRequest]
                with lock:
                    self.pre_tick_queue.extend(new_queue)
                    self.work += len(new_queue)
                    rqueue = [req for (delta, req) in self.on_tick_queue if delta <= 0]
                    self.on_tick_queue = [(delta-1, req) for (delta, req) in self.on_tick_queue if delta > 0]
                    self.work -= len(rqueue)
                    if rqueue:
                        def note_finished():
                            update_finished.set()
                            return ()
                        rqueue.append(note_finished)
                        comm_thread.add_requests(rqueue)
                    self.next_tick += 1
                if rqueue:
                    while not update_finished.wait(_wait_timeout):
                        pass
                update_finished.clear()
                with lock:
                    queue = self.post_tick_queue
                    self.post_tick_queue = []
                    self.work -= len(queue)
                new_queue = self._process_queue(queue)
                if new_queue:
                    with lock:
                        self.post_tick_queue.extend(new_queue)
                        self.work += len(new_queue)
                if self.work == 0 or not self.running:
                    self.idle()
        finally:
            print(self.name, "exited")
            self.state = State.DEAD
            
    def before_tick(self, fn: ClockCallback, *, delta: int=0) -> None:
        assert self.state is State.RUNNING or self.state is State.NEW
        with self.lock:
            self.pre_tick_queue.append((delta, fn))
            self.not_idle()
            self.work += 1

    def after_tick(self, fn: ClockCallback, *, delta: int=0):
        assert self.state is State.RUNNING or self.state is State.NEW
        with self.lock:
            self.post_tick_queue.append((delta, fn))
            self.not_idle()
            self.work += 1

    def on_tick(self, req: DevCommRequest, *, delta: int=0):
        assert self.state is State.RUNNING or self.state is State.NEW
        with self.lock:
            self.on_tick_queue.append((delta, req))
            self.not_idle()
            self.work += 1

    