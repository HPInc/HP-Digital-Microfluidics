from enum import Enum, auto
from threading import Thread, Condition, Event, Lock, Timer
import heapq
from quantities.SI import sec, ms
from quantities.timestamp import time_now, time_in
from quantities.dimensions import Time
from typing import Optional, Type, Literal, Protocol, Any, Callable, Sequence,\
    Iterable
from types import TracebackType
import time

def _in_secs(t: Time) -> float:
    return t.as_number(sec)

_wait_timeout: float = _in_secs(0.5*sec)

class  State(Enum):
    NEW = auto()
    RUNNING = auto()
    SHUTDOWN_REQUESTED = auto()
    ABORT_REQUESTED = auto()
    DEAD = auto()
    
class IdleBarrier:
    event: Event
    lock: Lock
    running_components: set['WorkerThread'] 
    
    def __init__(self) -> None:
        self.event = Event()
        self.event.set()
        self.lock = Lock()
        self.running_components = set['WorkerThread']()
    
    def running(self, component: 'WorkerThread') -> None:
        with self.lock:
            self.event.clear()
            self.running_components.add(component)
            
    def idle(self, component: 'WorkerThread') -> None:
        with self.lock:
            self.running_components.discard(component)
            if len(self.running_components) == 0:
                self.event.set()
                
    def wait(self, timeout: float = None) -> None:
        self.event.wait(timeout)
      
class Updatable(Protocol):
    def updatestate(self) -> Any: ...          
            
class Request(Protocol):
    def prepare(self) -> Any: ...
    component: Optional[Updatable]
    
Callback = Callable[[], Any]


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
        self.dev_comm_thread.join()
    
    def start(self) -> None:
        pass
        
    def stop(self) -> None:
        self.dev_comm_thread.request_stop()
        self._join_threads()
    
    def abort(self) -> None:
        self.dev_comm_thread.request_abort()
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
    
    def communicate(self, req: Request):
        self.dev_comm_thread.add_request(req)
        
    def call_at(self, t: Time, fn: Callback):
        self.timer_thread.call_at(t, fn)
        
    def call_after(self, delta: Time, fn: Callback):
        self.timer_thread.call_after(delta, fn)
        
class WorkerThread(Thread):
    engine: Engine
    idle_barrier: IdleBarrier
    state: State
    lock: Lock
    
    def __init__(self, engine: Engine, *args, **kwdargs) -> None:
        super().__init__(*args, **kwdargs)
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
                self.daemon = True
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
        self.idle_barrier.running(self)
        self.daemon = False
        self.ensure_running()
        
    # called with lock
    def idle(self) -> None:
        self.idle_barrier.idle(self)
        self.daemon = True
        
    
class DevCommThread(WorkerThread):
    condition: Condition
    queue: list[Request]
    
    def __init__(self, engine: Engine):
        super().__init__(engine, name="Device Communication Thread", daemon=True)
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
                queue_copy: list[Request]
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
                    req.prepare()
                    if req.component:
                        need_update.add(req.component)
                for c in need_update:
                    c.updatestate()
                need_update.clear()
                if not queue:
                    with self.lock:
                        if not queue:
                            self.idle()
        finally:
            self.state = State.DEAD
    
    def add_request(self, req: Request) -> None:
        assert self.state is State.RUNNING
        with self.lock:
            self.queue.append(req)
            self.not_idle()
            self.wake_up()
            
    def add_requests(self, reqs: Sequence[Request]) -> None:
        assert self.state is State.RUNNING
        if len(reqs) > 0:
            with self.condition:
                self.queue.extend(reqs)
                self.not_idle()
                self.wake_up()
            
        
TimerFunc = Callable[[], Optional[Time]]
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
        super().__init__(engine, name="Timer Thread", daemon=True)
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
            self.state = State.DEAD
            
    def call_at(self, t: Time, fn: TimerFunc) -> None:
        assert self.state is State.RUNNING
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

ClockCallback = Callable[[], Optional[int]]
CT = tuple[int, ClockCallback]
                
class ClockThread(WorkerThread):
    class TickRequest:
        cancelled: bool
        clock: 'ClockThread'
        
        def __init__(self, clock: 'ClockThread') -> None:
            self.cancelled = False
            self.clock = clock
            
        def __call__(self) -> Optional[Time]:
            if not self.cancelled:
                self.clock.tick_event.set()
                return time_in(self.clock.update_interval)
            return None
                
        def cancel(self) -> None:
            self.cancelled = True
            if self.clock.outstanding_tick_request is self:
                self.clock.outstanding_tick_request = None
        
    running: bool
    tick_event: Event
    update_finished: Event
    pre_tick_queue: list[CT]
    post_tick_queue: list[CT]
    on_tick_queue: list[tuple[int, Request]]
    work: int
    next_tick: int
    outstanding_tick_request: Optional[TickRequest]
    
    def __init__(self, engine):
        super().__init__(engine, name="Clock Thread", daemon = True)
        self.running = False
        self.tick_event = Event()
        self.update_finished = Event()
        self.pre_tick_queue = []
        self.post_tick_queue = []
        self.on_tick_queue = []
        self.update_interval = 100*ms
        self.work = 0
        self.next_tick = 0
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

    class note_done:
        event: Event
        component: Optional[Updatable] = None
        def __init__(self, e: Event) -> None:
            self.event = e
        def prepare(self) -> None:
            self.event.set()
        
    def run(self) -> None:
        lock = self.lock
        update_finished = self.update_finished 
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
                queue: list[CT]
                with lock:
                    queue = self.pre_tick_queue
                    self.pre_tick_queue = []
                    self.work -= len(queue)
                new_queue: list[CT] = self._process_queue(queue)
                rqueue: list[Request]
                with lock:
                    self.pre_tick_queue.extend(new_queue)
                    self.work += len(new_queue)
                    rqueue = [req for (delta, req) in self.on_tick_queue if delta == 0]
                    self.on_tick_queue = [(delta-1, req) for (delta, req) in self.on_tick_queue if delta > 0]
                    self.work -= len(rqueue)
                    if rqueue:
                        rqueue.append(self.note_done(update_finished))
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
            self.state = State.DEAD
            
    def before_tick(self, fn: ClockCallback, *, delta: int=0) -> None:
        with self.lock:
            self.pre_tick_queue.append((delta, fn))
            self.not_idle()
            self.work += 1

    def after_tick(self, fn: ClockCallback, *, delta: int=0):
        with self.lock:
            self.post_tick_queue.append((delta, fn))
            self.not_idle()
            self.work += 1

    def on_tick(self, req: Request, *, delta: int=0):
        with self.lock:
            self.on_tick_queue.append((delta, req))
            self.not_idle()
            self.work += 1

    