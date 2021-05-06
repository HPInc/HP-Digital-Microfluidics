from typing import Type, Optional, Final, Mapping, Callable, Tuple, Literal
from types import TracebackType
from mpam.types import XYCoord, Dir, OnOff, Delayed
from mpam.engine import Callback, DevCommRequest, TimerFunc, ClockCallback,\
    Engine, ClockThread, _wait_timeout, Worker
from quantities.dimensions import Time
from quantities.timestamp import time_now
from threading import Event

PadArray = Mapping[XYCoord, 'Pad']

class Pad:
    location: Final[XYCoord]
    exists: Final[bool]
    _board: Final['Board']
    _pads: Final[PadArray]
    _state: OnOff
    
    
    
    @property
    def row(self) -> int:
        return self.location.y 
    @property
    def column(self) -> int:
        return self.location.x
    
    @property
    def current_state(self) -> OnOff:
        return self._state
    
    def __init__(self, loc: XYCoord, board: 'Board', *, exists: bool = True) -> None:
        self.location = loc
        self.exists = exists
        self._board = board
        self._state = OnOff.OFF
        self._pads = board.pad_array()
        self.set_device_state: Callable[[OnOff], None]
        
    def neighbor(self, d: Dir) -> Optional['Pad']:
        p = self._pads[self.location+d]
        if p is None or not p.exists:
            return None
        return p
    
    def request_set_state(self, val: OnOff) -> OnOff:
        print("Setting pad @", self.location, "to", val)
        old = self._state
        setter = self.set_device_state
        self._board.communicate(lambda : setter(val))
        self._state = val
        return old
    
    def request_turn_on(self) -> OnOff:
        return self.request_set_state(OnOff.ON)

    def request_turn_off(self) -> OnOff:
        return self.request_set_state(OnOff.OFF)
    
    def request_toggle(self) -> OnOff:
        return self.request_set_state(~self._state)
    
    def async_set_state(self, val: OnOff) -> Delayed[OnOff]:
        print("Asking to set pad @", self.location, "to", val)
        future = Delayed[OnOff]()
        setter = self.set_device_state
        def cb():
            print("Setting pad @", self.location, "to", val)
            old = self._state
            setter(val)
            future.post(old)
        self._board.communicate(cb)
        return future
    
    def set_state(self, val: OnOff) -> OnOff:
        return self.async_set_state(val).value()
    
    def gated_request_set_state(self, val: OnOff) -> OnOff:
        print("[Gated] Asking to set pad @", self.location, "to", val)
        setter = self.set_device_state
        old = self._state
        def cb():
            print("Setting pad @", self.location, "to", val)
            setter(val)
        self._board.on_tick(cb)
        return old
            
    def gated_set_state(self, val: OnOff) -> Delayed[OnOff]:
        print("[Gated] Asking to set pad @", self.location, "to", val)
        future = Delayed[OnOff]()
        setter = self.set_device_state
        def cb():
            print("Setting pad @", self.location, "to", val)
            old = self._state
            setter(val)
            future.post(old)
        self._board.on_tick(cb)
        return future
            
    
class SystemComponent:
    system: Optional['System'] = None
    
    def __init__(self) -> None:
        ...
        
    def join_system(self, system: 'System') -> None:
        self.system = system
        
    def in_system(self) -> 'System':
        system = self.system
        assert system is not None
        return system
    
    def update_state(self) -> None:
        raise NotImplementedError("{}.update_state() not defined".format(self.__class__))
            
    def communicate(self, cb: Callback):
        def req() -> Tuple[SystemComponent]:
            cb()
            return (self,)
        self.in_system().communicate(req)
        
    def call_at(self, t: Time, fn: Callback):
        self.in_system().call_at(t, fn)
        
    def call_after(self, delta: Time, fn: Callback):
        self.in_system().call_after(delta, fn)
        
    def before_tick(self, fn: ClockCallback, *, delta: int=0) -> None:
        self.in_system().before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, *, delta: int=0):
        self.in_system().after_tick(fn, delta=delta)

    def on_tick(self, cb: Callback, *, delta: int=0):
        def req() -> Tuple[SystemComponent]:
            cb()
            return (self,)
        self.in_system().on_tick(req, delta=delta)
 

class Board(SystemComponent):
    pads: Final[PadArray]
    
    def __init__(self, pads: PadArray) -> None:
        super().__init__()
        self.pads = pads

    def stop(self) -> None:
        pass    
    def abort(self) -> None:
        pass
    
    def pad_array(self) -> PadArray:
        return self.pads
    
    def pad_at(self, x: int, y: int) -> Pad:
        return self.pads[XYCoord(x,y)]
    
class Operation(Worker):
    def __enter__(self) -> 'Operation':
        self.not_idle()
        return self
    
    def __exit__(self, 
                 exc_type: Optional[Type[BaseException]], 
                 exc_val: Optional[BaseException], 
                 exc_tb: Optional[TracebackType]) -> Literal[False]:
        self.idle()
        return False

class Clock:
    system: Final['System']
    engine: Final[Engine]
    clock_thread: Final[ClockThread]
    def __init__(self, system: 'System') -> None:
        self.system = system
        self.engine = system.engine
        self.clock_thread = system.engine.clock_thread
        
    @property
    def update_interval(self) -> Time:
        return self.clock_thread.update_interval
    
    @property
    def next_tick(self) -> int:
        return self.clock_thread.next_tick
    
    @property
    def last_tick(self) -> int:
        return self.next_tick-1
    
    @property
    def running(self) -> bool:
        return self.clock_thread.running
    
    def before_tick(self, fn: ClockCallback, tick: Optional[int] = None, delta: Optional[int] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.before_tick() called with both tick and delta specified"
            delta = max(0, tick-self.next_tick)
        elif delta is None:
            delta = 0
        self.clock_thread.before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, tick: Optional[int] = None, delta: Optional[int] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.after_tick() called with both tick and delta specified"
            delta = max(0, tick-self.next_tick)
        elif delta is None:
            delta = 0
        self.clock_thread.after_tick(fn, delta=delta)
    
    def await_tick(self, tick: Optional[int] = None, delta: Optional[int] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.await_tick() called with both tick and delta specified"
            delta = tick-self.next_tick
        elif delta is None:
            delta = 0
        if delta >= 0:
            e = Event()
            def cb():
                e.signal()
            self.clock_thread.after_tick(cb, delta=delta)
            while not e.is_set():
                e.wait(_wait_timeout)

    def advance_clock(self, min_delay: Optional[Time] = None) -> None:
        assert not self.running, "Clock.advance_clock() called while clock is running"
        ct = self.clock_thread
        if min_delay is not None:
            next_allowed = ct.last_tick_time+min_delay
            if next_allowed > time_now():
                def do_advance():
                    ct.wake_up()
                self.system.call_at(next_allowed, do_advance)
            else:
                ct.wake_up()
                
                

class System:
    board: Board
    engine: Engine
    
    def __init__(self, *, board: Board):
        self.board = board
        self.engine = Engine()
        board.system = self

    def __enter__(self) -> 'System':
        self.engine.__enter__()
        return self
    
    def __exit__(self, 
                 exc_type: Optional[Type[BaseException]], 
                 exc_val: Optional[BaseException], 
                 exc_tb: Optional[TracebackType]) -> bool:
        return self.engine.__exit__(exc_type, exc_val, exc_tb)
    
    def stop(self) -> None:
        self.engine.stop()
        self.board.stop()
        
    def abort(self) -> None:
        self.engine.abort()
        self.board.abort()
        
    def communicate(self, req: DevCommRequest) -> None:
        self.engine.communicate(req)
        
    def call_at(self, t: Time, fn: TimerFunc) -> None:
        self.engine.call_at(t, fn)
        
    def call_after(self, delta: Time, fn: TimerFunc) -> None:
        self.engine.call_after(delta, fn)
        
    def before_tick(self, fn: ClockCallback, *, delta: int=0) -> None:
        self.engine.before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, *, delta: int=0):
        self.engine.after_tick(fn, delta=delta)

    def on_tick(self, req: DevCommRequest, *, delta: int=0):
        self.engine.on_tick(req, delta=delta)
        