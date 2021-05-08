from typing import Type, Optional, Final, Mapping, Callable, Tuple, Literal,\
    TypeVar
from types import TracebackType
from mpam.types import XYCoord, Dir, OnOff, Delayed
from mpam.engine import Callback, DevCommRequest, TimerFunc, ClockCallback,\
    Engine, ClockThread, _wait_timeout, Worker
from quantities.dimensions import Time
from quantities.timestamp import time_now
from threading import Event

PadArray = Mapping[XYCoord, 'Pad']

T = TypeVar('T')
Modifier = Callable[[T],T]

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
    
    @classmethod
    def _modifier(cls, *, gated:bool=False, immediate:bool=False):
        def fn(self: 'Pad', mod: Modifier[OnOff]) -> Delayed[OnOff]:
            future = Delayed[OnOff]()
            setter = self.set_device_state
            
            def cb() -> Optional[Callback]:
                old = self._state
                new = mod(old)
                print(f"Setting pad at {self.location} to {new}")
                setter(new)
                self._state = new
                finish: Optional[Callback] = None if immediate else (lambda : future.post(old))
                return finish
            
            tag = "[Gated] " if gated else ""
            print(f"{tag}Asking to set pad at {self.location} to {mod(self._state)}")
            if immediate:
                future.post(mod(self._state))
            if gated:
                self._board.on_tick(cb)
            else:
                self._board.communicate(cb)
            return future
        return fn
            
    
    def request_modify_state(self, mod: Modifier[OnOff], *, gated: bool = False) -> OnOff:
        fn = Pad._modifier(gated=gated, immediate = True)
        return fn(self, mod).value()
    def async_modify_state(self, mod: Modifier[OnOff], *, gated: bool = False) -> Delayed[OnOff]:
        fn = Pad._modifier(gated=gated)
        return fn(self, mod)
    def gated_request_modify_state(self, mod: Modifier[OnOff]) -> OnOff:
        return self.request_modify_state(mod, gated=True)
    def modify_state(self, mod: Modifier[OnOff]) -> OnOff:
        return self.async_modify_state(mod).value()
    def gated_modify_state(self, mod: Modifier[OnOff]) -> Delayed[OnOff]:
        return self.async_modify_state(mod, gated=True)
    
    def request_set_state(self, val: OnOff, *, gated: bool = False) -> OnOff:
        return self.request_modify_state(lambda _: val, gated=gated)
    def gated_request_set_state(self, val: OnOff) -> OnOff:
        return self.request_set_state(val, gated=True)
    def async_set_state(self, val: OnOff, *, gated: bool = False) -> Delayed[OnOff]:
        return self.async_modify_state(lambda _: val, gated=gated)
    def set_state(self, val: OnOff) -> OnOff:
        return self.async_set_state(val).value()
    def gated_set_state(self, val: OnOff) -> Delayed[OnOff]:
        return self.async_set_state(val, gated = True)
            
    def request_turn_on(self, *, gated: bool = False) -> OnOff:
        return self.request_set_state(OnOff.ON, gated=gated)
    def async_turn_on(self, *, gated: bool = False) -> Delayed[OnOff]:
        return self.async_set_state(OnOff.ON, gated=gated)
    def gated_request_turn_on(self) -> OnOff:
        return self.request_turn_on(gated=True)
    def gated_turn_on(self) -> Delayed[OnOff]:
        return self.async_turn_on(gated=True)
    def turn_on(self) -> OnOff:
        return self.gated_turn_on().value()

    def request_turn_off(self, *, gated: bool = False) -> OnOff:
        return self.request_set_state(OnOff.OFF, gated=gated)
    def async_turn_off(self, *, gated: bool = False) -> Delayed[OnOff]:
        return self.async_set_state(OnOff.OFF, gated=gated)
    def gated_request_turn_off(self) -> OnOff:
        return self.request_turn_off(gated=True)
    def gated_turn_off(self) -> Delayed[OnOff]:
        return self.async_turn_off(gated=True)
    def turn_off(self) -> OnOff:
        return self.gated_turn_off().value()
    
    def request_toggle(self, *, gated: bool = False) -> OnOff:
        return self.request_modify_state(lambda s : ~s, gated=gated)
    def async_toggle(self, *, gated: bool = False) -> Delayed[OnOff]:
        return self.async_modify_state(lambda s : ~s, gated=gated)
    def gated_request_toggle(self) -> OnOff:
        return self.request_toggle(gated=True)
    def gated_toggle(self) -> Delayed[OnOff]:
        return self.async_toggle(gated=True)
    def toggle(self) -> OnOff:
        return self.async_toggle().value()
    
class SystemComponent:
    system: Optional['System'] = None
    _after_update: Final[list[Callback]]
    
    def __init__(self) -> None:
        self._after_update = []
        
    def join_system(self, system: 'System') -> None:
        self.system = system
        
    def in_system(self) -> 'System':
        system = self.system
        assert system is not None
        return system
    
    def update_state(self) -> None:
        raise NotImplementedError(f"{self.__class__}.update_state() not defined")
    
    def finish_update(self) -> None:
        # This is assumed to only be called in the DevComm thread, so
        # no locking is necessary.
        for cb in self._after_update:
            cb()
        self._after_update.clear()
        
    def make_request(self, cb: Callable[[], Optional[Callback]]) -> DevCommRequest:
        def req() -> Tuple[SystemComponent]:
            new_cb = cb()
            if new_cb is not None:
                self._after_update.append(new_cb)
            return (self,)
        return req
    
    def communicate(self, cb: Callable[[], Optional[Callback]]):
        req = self.make_request(cb)
        self.in_system().communicate(req)
        
    def call_at(self, t: Time, fn: Callback):
        self.in_system().call_at(t, fn)
        
    def call_after(self, delta: Time, fn: Callback):
        self.in_system().call_after(delta, fn)
        
    def before_tick(self, fn: ClockCallback, *, delta: int=0) -> None:
        self.in_system().before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, *, delta: int=0):
        self.in_system().after_tick(fn, delta=delta)

    def on_tick(self, cb: Callable[[], Optional[Callback]], *, delta: int=0):
        req = self.make_request(cb)
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
                 exc_type: Optional[Type[BaseException]],  # @UnusedVariable
                 exc_val: Optional[BaseException],  # @UnusedVariable
                 exc_tb: Optional[TracebackType]) -> Literal[False]:  # @UnusedVariable
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
    
    @update_interval.setter
    def update_interval(self, interval: Time) -> None:
        self.clock_thread.update_interval = interval
    
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
                return
        ct.wake_up()
        
    def start(self, interval: Optional[Time] = None) -> None:
        assert not self.running, "Clock.start() called while clock is running"
        self.clock_thread.start_clock(interval)
        
    def pause(self) -> None:
        assert self.running, "Clock.pause() called while clock is running"
        self.clock_thread.pause_clock()
        
        
                
                

class System:
    board: Board
    engine: Engine
    clock: Clock
    
    def __init__(self, *, board: Board):
        self.board = board
        self.engine = Engine()
        self.clock = Clock(self)
        board.join_system(self)

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
        
    def call_at(self, t: Time, fn: TimerFunc, *, daemon: bool = False) -> None:
        self.engine.call_at(t, fn, daemon = daemon)
        
    def call_after(self, delta: Time, fn: TimerFunc, *, daemon: bool = False) -> None:
        self.engine.call_after(delta, fn, daemon = daemon)
        
    def before_tick(self, fn: ClockCallback, *, delta: int=0) -> None:
        self.engine.before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, *, delta: int=0):
        self.engine.after_tick(fn, delta=delta)

    def on_tick(self, req: DevCommRequest, *, delta: int=0):
        self.engine.on_tick(req, delta=delta)
        