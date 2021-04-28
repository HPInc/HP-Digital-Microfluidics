from enum import Enum, auto
from threading import Thread, Condition, Event, Lock, Timer
from quantities import SI
import heapq
import time
from aifc import fn

sec = SI.sec
usec = SI.usec
ms = SI.ms

def time_now():
    return time.time()*sec

def time_in(delta):
    return time_now()+delta

def time_since(t):
    return time_now()-t

def _in_secs(t):
    return t.in_units(sec).magnitude

_wait_timeout = _in_secs(0.5*sec)

class  State(Enum):
    NEW = auto()
    RUNNING = auto()
    SHUTDOWN_REQUESTED = auto()
    ABORT_REQUESTED = auto()
    DEAD = auto()
    
class IdleBarrier:
    def __init__(self):
        self.event = Event()
        self.event.set()
        self.lock = Lock()
        self.running = set()
    
    def running(self, component):
        with self.lock:
            self.event.clear()
            self.running.add(component)
            
    def idle(self, component):
        with self.lock:
            self.running.discard(component)
            if len(self.running) == 0:
                self.event.set()
                
    def wait(self, timeout = None):
        self.event.wait(timeout)
                
            

class Engine:
    def __init__(self, board):
        self.the_board = board
        self.idle_barrier = IdleBarrier()
        self.dev_comm_thread = DevCommThread(self)
        self.timer_thread = TimerThread(self)
        
        
    def _join_threads(self):
        self.dev_comm_thread.join()
    
    def start(self):
        pass
        
    def stop(self):
        self.dev_comm_thread.request_stop()
        self._join_threads()
    
    def abort(self):
        self.dev_comm_thread.request_abort()
        self._join_threads()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.idle_barrier.wait()
        return False
    
    def communicate(self, req):
        self.dev_comm_thread.add_request(req)
        
    def call_at(self, t, fn):
        self.timer_thread.call_at(t, fn)
        
    def call_after(self, delta, fn):
        self.timer_thread.call_after(delta, fn)
        
class WorkerThread(Thread):
    def __init__(self, engine, *args, **kwdargs):
        super().__init__(*args, **kwdargs)
        self.idle_barrier = engine.idle_barrier
        self.state = State.NEW
        self.lock = Lock()
        
    def request_abort(self):
        if self.state is State.RUNNING:
            with self.lock:
                self.state = State.ABORT_REQUESTED
                self.daemon = True
                self.wake_up()
            
    def request_stop(self):
        if self.state is State.RUNNING:
            with self.condition:
                self.state = State.SHUTDOWN_REQUESTED
                self.wake_up()
            
    # called with lock
    def ensure_running(self):
        if not self.is_alive():
            self.start()
            
    # called with lock
    def not_idle(self):
        self.idle_barrier.running(self)
        self.daemon = False
        self.ensure_running()
        
    # called with lock
    def idle(self):
        self.idle_barrier.idle(self)
        self.daemon = True
        
    
class DevCommThread(WorkerThread):
    def __init__(self, engine):
        super().__init__(name="Device Communication Thread", daemon=True)
        self.condition = Condition(lock=self.lock)
        self.queue = []
        
    # called with lock locked
    def wake_up(self):
        self.condition.notify()
        
    def run(self):
        try:
            self.state = State.RUNNING
            need_update = set()
            queue = self.queue
            condition = self.condition
            while self.state is State.RUNNING:
                queue_copy = None
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
                    need_update.add(req.component)
                for c in self.need_update:
                    c.updatestate()
                need_update.clear()
                if not queue:
                    with condition:
                        if not queue:
                            self.idle()
        finally:
            self.state = State.DEAD
    
    def add_request(self, req):
        assert self.state is State.RUNNING
        with self.lock:
            self.queue.append(req)
            self.not_idle()
            self.wake_up()
            
    def add_requests(self, reqs):
        assert self.state is State.RUNNING
        if len(reqs) > 0:
            with self.condition:
                self.queue.extend(reqs)
                self.not_idle()
                self.wake_up()
            
        
class TimerThread(WorkerThread):
    class MyTimer(Timer):
        def __init__(self, timer_thread, target_time, delay, func):
            super().__init__(_in_secs(delay), lambda : self.call_func())
            self.timer_thread = timer_thread
            self.target_time = target_time
            self.func = func
            
        def call_func(self):
            next_time = self.func()
            tt = self.timer_thread
            with tt.lock:
                if next_time:
                    heapq.heappush(tt.queue, (next_time, self.func))
                tt.timer = None
                if not tt.queue:
                    tt.idle()
                tt.wake_up()
                
    def __init__(self, engine):
        super().__init__(name="Timer Thread", daemon=True)
        self.condition = Condition(lock=self.lock)
        self.queue = []
        self.timer = None
        
    def wake_up(self):
        self.condition.notify()
        
    def run(self):
        try:
            queue = self.queue
            condition = self.condition
            lock = self.lock
            self.state = State.RUNNING
            while self.state is State.RUNNING or (self.state is State.SHUTDOWN_REQUESTED and queue):
                func = None
                desired_time = None
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
                now = time_now()
                next_time = None
                if now >= desired_time:
                    next_time = func()
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
            
    def call_at(self, t, fn):
        assert self.state is State.RUNNING
        with self.condition:
            self.not_idle()
            timer = self.timer
            if timer is not None and t < timer.target_time:
                # We're trying to add something before the one that's (maybe) waiting.  If we
                # can cancel it, we push it back and then ourselves.  If we can't cancel it, it's
                # already started, so we just push ourselves.  (We know it's past time for us to run, so
                # we could just call it here, but I'm not sure how safe that is.)
                if timer.cancel():
                    heapq.heappush(self.queue, (timer.target_time, timer.func))
                    self.timer = None
            heapq.heappush(self.queue, (t, fn))  
            self.wake_up()

    def call_after(self, delta, fn):
        self.call_at(time_in(delta), fn)
            
                
class ClockThread(WorkerThread):
    class TickRequest:
        def __init__(self, clock):
            self.cancelled = False
            self.clock = clock
            
        def __call__(self):
            if not self.cancelled:
                self.clock.tick_event.set()
                return time_in(self.clock.update_interval)
                
        def cancel(self):
            self.cancelled = True
            if self.clock.outstanding_tick_request is self:
                self.clock.outstanding_tick_request = None
        
    
    def __init__(self, engine):
        super().__init__(name="Clock Thread", daemon = True)
        self.engine = engine
        self.running = False
        self.tick_event = Event()
        self.update_finished = Event()
        self.pre_tick_queue = []
        self.post_tick_queue = []
        self.on_tick_queue = []
        self.update_interval = 100*ms
        self.state = State.NEW
        self.work = 0
        self.next_tick = 0
        self.outstanding_tick_request = None
        self.lock = Lock()
        
    def _process_queue(self, queue):
        new_queue = []
        for (delay, fn) in queue:
            if delay > 0:
                new_queue.append((delay-1, fn))
            else:
                new_delay = fn()
                if new_delay is not None:
                    new_queue.append((new_delay, fn))
        return new_queue
    
    def wake_up(self):
        self.tick_event.set()
        
    def run(self):
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
                queue = None
                with lock:
                    queue = self.pre_tick_queue
                    self.pre_tick_queue = []
                    self.work -= len(queue)
                new_queue = self._process_queue(queue)
                with lock:
                    self.pre_tick_queue.extend(new_queue)
                    self.work += len(new_queue)
                    queue = self.on_tick_queue
                    self.on_tick_queue = []
                    self.work -= len(queue)
                    if queue:
                        queue.append(lambda : update_finished.set())
                        comm_thread.add_requests(queue)
                    self.next_tick += 1
                if queue:
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
            
    def before_tick(self, fn, *, delta=0):
        with self.lock:
            self.pre_tick_queue.append((delta, fn))
            self.not_idle()
            self.work += 1

    def after_tick(self, fn, *, delta=0):
        with self.lock:
            self.post_tick_queue.append((delta, fn))
            self.not_idle()
            self.work += 1

    def on_tick(self, req, *, delta=0):
        with self.lock:
            self.on_tick_queue.append((delta, req))
            self.not_idle()
            self.work += 1

    