from __future__ import annotations
from typing import Optional, Final, Mapping, Callable, Literal,\
    TypeVar, Sequence, TYPE_CHECKING, Union, ClassVar
from types import TracebackType
from quantities.dimensions import Time, Volume
from quantities.timestamp import time_now, Timestamp
from threading import Event, Lock

from mpam.types import XYCoord, Dir, OnOff, Delayed, Liquid, RunMode, DelayType,\
    Operation, OpScheduler
from mpam.engine import Callback, DevCommRequest, TimerFunc, ClockCallback,\
    Engine, ClockThread, _wait_timeout, Worker, TimerRequest, ClockRequest,\
    ClockCommRequest, TimerDeltaRequest
from mpam.exceptions import PadBrokenError

if TYPE_CHECKING:
    from mpam.drop import Drop

PadArray = Mapping[XYCoord, 'Pad']

T = TypeVar('T')
Modifier = Callable[[T],T]


class Pad(OpScheduler['Pad']):
    location: Final[XYCoord]
    exists: Final[bool]
    broken: bool
    
    _board: Final[Board]
    _pads: Final[PadArray]
    _state: OnOff
    _drop: Optional[Drop]
    _dried_liquid: Optional[Drop]
    _neighbors: Optional[Sequence[Pad]]
    _well: Optional[Well]
        
    @property
    def row(self) -> int:
        return self.location.y 
    @property
    def column(self) -> int:
        return self.location.x
    
    @property
    def well(self) -> Optional[Well]:
        return self._well
    
    @property
    def current_state(self) -> OnOff:
        return self._state
    
    @property
    def drop(self) -> Optional[Drop]:
        return self._drop
    
    @property
    def dried_liquid(self) -> Optional[Drop]:
        return self._dried_liquid
    
    @property
    def neighbors(self) -> Sequence[Pad]:
        ns = getattr(self, '_neighbors', None)
        if ns is None:
            ns = [self.neighbor(d) for d in Dir if self.neighbor(d)]
            self._neighbors = ns
        return ns
    
    def __init__(self, loc: XYCoord, board: Board, *, exists: bool = True) -> None:
        self.location = loc
        self.exists = exists
        self.broken = False
        self._board = board
        self._state = OnOff.OFF
        self._pads = board.pad_array()
        self.set_device_state: Callable[[OnOff], None]
        self._drop = None
        self._dried_liquid = None
        
    def __repr__(self) -> str:
        return f"Pad[{self.column},{self.row}]"
        
    def neighbor(self, d: Dir) -> Optional[Pad]:
        p = self._pads.get(self.location+d, None)
        if p is None or not p.exists:
            return None
        return p
    
    def empty(self) -> bool:
        return self.drop is None
    
    def safe(self) -> bool:
        return self.empty and all(map(lambda n : n.empty, self.neighbors))
    
    class ModifyState(Operation['Pad', OnOff]):
        def guess_value(self, pad: Pad) -> OnOff:
            return self.mod(pad._state)
        
        def _schedule_for(self, pad: Pad, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          guess_only: bool = False,
                          future: Optional[Delayed[OnOff]] = None
                          ) -> Delayed[OnOff]:
            
            if pad.broken:
                raise PadBrokenError
            current = pad._state
            mod = self.mod
            if future is None:
                future = Delayed[OnOff](guess=mod(current), immediate=guess_only)
            real_future = future
            setter = pad.set_device_state
            
            def cb() -> Optional[Callback]:
                old = pad._state
                new = mod(old)
                print(f"Setting pad at {pad.location} to {new}")
                setter(new)
                self._state = new
                finish: Optional[Callback] = None if guess_only else (lambda : real_future.post(old))
                return finish
            
            tag = "[Gated] " if mode.is_gated else ""
            print(f"{tag}Asking to set pad at {pad.location} to {mod(pad._state)}")
            pad._board.schedule(cb, mode, after=after)
            return future
        
        def __init__(self, mod: Modifier[OnOff]) -> None:
            self.mod: Final[Modifier[OnOff]] = mod
    
    @staticmethod        
    def SetState(val: OnOff) -> ModifyState:
        return Pad.ModifyState(lambda _ : val)
            
 
    TurnOn: ClassVar[ModifyState]
    TurnOff: ClassVar[ModifyState]
    Toggle: ClassVar[ModifyState]

    def schedule_modify_state(self, mod: Modifier[OnOff], *, 
                              mode: RunMode=RunMode.GATED, 
                              after:Optional[DelayType] = None,
                              guess_only: bool = False) -> Delayed[OnOff]:
        if self.broken:
            raise PadBrokenError
        current = self._state
        future = Delayed[OnOff](guess=mod(current), immediate=guess_only)
        setter = self.set_device_state
        
        def cb() -> Optional[Callback]:
            old = self._state
            new = mod(old)
            print(f"Setting pad at {self.location} to {new}")
            setter(new)
            self._state = new
            finish: Optional[Callback] = None if guess_only else (lambda : future.post(old))
            return finish
        
        tag = "[Gated] " if mode.is_gated else ""
        print(f"{tag}Asking to set pad at {self.location} to {mod(self._state)}")
        self._board.schedule(cb, mode, after=after)
        return future

    def modify_state(self, mod: Modifier[OnOff], *, 
                     mode: RunMode=RunMode.GATED, 
                     after:Optional[DelayType] = None,
                     guess_only: bool = False) -> OnOff:
        return self.schedule_modify_state(mod, mode=mode, after=after, guess_only=guess_only).value
   
    def schedule_set_state(self, val: OnOff, *,
                           mode: RunMode=RunMode.GATED, 
                           after:Optional[DelayType] = None,
                           guess_only: bool = False) -> Delayed[OnOff]:
        return self.schedule_modify_state(lambda _: val, mode=mode, after=after, guess_only=guess_only)
                  
    def set_state(self, val: OnOff, *, 
                  mode: RunMode=RunMode.GATED, 
                  after:Optional[DelayType] = None,
                  guess_only: bool = False) -> OnOff:
        return self.schedule_set_state(val, mode=mode, after=after, guess_only=guess_only).value
    
    def schedule_turn_on(self, *,
                         mode: RunMode=RunMode.GATED, 
                         after:Optional[DelayType] = None,
                         guess_only: bool = False) -> Delayed[OnOff]:
        return self.schedule_set_state(OnOff.ON, mode=mode, after=after, guess_only=guess_only)
            
    def turn_on(self, *, 
                mode: RunMode=RunMode.GATED, 
                after:Optional[DelayType] = None,
                guess_only: bool = False) -> OnOff:
        return self.schedule_turn_on(mode=mode, after=after, guess_only=guess_only).value
   
    def schedule_turn_off(self, *,
                          mode: RunMode=RunMode.GATED, 
                          after:Optional[DelayType] = None,
                          guess_only: bool = False) -> Delayed[OnOff]:
        return self.schedule_set_state(OnOff.OFF, mode=mode, after=after, guess_only=guess_only)
            
    def turn_off(self, *, 
                 mode: RunMode=RunMode.GATED, 
                 after:Optional[DelayType] = None,
                 guess_only: bool = False) -> OnOff:
        return self.schedule_turn_off(mode=mode, after=after, guess_only=guess_only).value
   
    def schedule_toggle(self, *,
                        mode: RunMode=RunMode.GATED, 
                        after:Optional[DelayType] = None,
                        guess_only: bool = False) -> Delayed[OnOff]:
        return self.schedule_modify_state(lambda s: ~s, mode=mode, after=after, guess_only=guess_only)
            
    def toggle(self, *, 
               mode: RunMode=RunMode.GATED, 
               after:Optional[DelayType] = None,
               guess_only: bool = False) -> OnOff:
        return self.schedule_toggle(mode=mode, after=after, guess_only=guess_only).value
 
Pad.TurnOn = Pad.SetState(OnOff.ON)
Pad.TurnOff = Pad.SetState(OnOff.OFF)
Pad.Toggle = Pad.ModifyState(lambda s: ~s)

    
class Well:
    class Section:
        index: Final[int] 
        well: Final[Well]
        def __init__(self, index: int, well: Well) -> None:
            self.index = index
            self.well = well
            
        def __repr__(self) -> str:
            return f"Section[{self.index}, {self.well}]"
        
    class DispensingSequence: ...
    
    number: Final[int]
    _board: Final[Board]
    capacity: Final[Volume]
    exit_pad: Final[Pad]
    dispensed_volume: Final[Volume]
    dispensing_ticks: Final[int]
    absorbing_ticks: Final[int]
    is_voidable: Final[bool]
    gate: Final[Section]
    sections: Final[Sequence[Section]]
    dispensing_sequences: Final[Sequence[DispensingSequence]]
    _contents: Optional[Liquid]
    
    @property
    def contents(self) -> Optional[Liquid]:
        return self._contents
    
    @property
    def volume(self) -> Volume:
        c = self._contents
        if c is None:
            return Volume.ZERO()
        else:
            return c.volume

    @property    
    def remaining_capacity(self) -> Volume:
        return self.capacity-self.volume
        
    @property
    def drop_availability(self) -> float:
        return self.volume.ratio(self.dispensed_volume)
    
    @property
    def empty(self) -> bool:
        return self.drop_availability < 1
    
    @property
    def available(self) -> bool:
        c = self._contents
        return c is None or c.volume==Volume.ZERO and not c.inexact
        
    def __init__(self, board: Board, *,
                 number: int, 
                 capacity: Volume,
                 exit_pad: Pad,
                 dispensed_volume: Volume,
                 dispensing_ticks: int,
                 absorbing_ticks: int,
                 is_voidable: bool = False,
                 gate: Section,
                 sections: Sequence[Section],
                 dispensing_sequences: Sequence[DispensingSequence]
                 ) -> None:
        self._board = board
        self.number = number
        self.capacity = capacity
        self.exit_pad = exit_pad
        assert not exit_pad._well, f"{exit_pad} is already associated with {exit_pad.well}"
        exit_pad._well = self
        self.dispensed_volume = dispensed_volume
        self.dispensing_ticks = dispensing_ticks
        self.absorbing_ticks = absorbing_ticks
        self.is_voidable = is_voidable
        self.gate = gate
        self.sections = sections
        self.dispensing_sequences = dispensing_sequences
        assert len(dispensing_sequences) > 0, "At least one dispensing sequence must be provided"
        self._contents = None
        

    
class SystemComponent:
    system: Optional[System] = None
    _after_update: Final[list[Callback]]
    
    def __init__(self) -> None:
        self._after_update = []
        
    def join_system(self, system: System) -> None:
        self.system = system
        
    def in_system(self) -> System:
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
        def req() -> tuple[SystemComponent]:
            new_cb = cb()
            if new_cb is not None:
                self._after_update.append(new_cb)
            return (self,)
        return req
    
    def communicate(self, cb: Callable[[], Optional[Callback]], delta: Time=Time.ZERO()):
        req = self.make_request(cb)
        sys = self.in_system()
        if delta > Time.ZERO():
            self.call_after(delta, lambda : sys.communicate(req))
        else:
            sys.communicate(req)
        
    def call_at(self, t: Timestamp, fn: Callback):
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
 
    def schedule(self, cb: Callable[[], Optional[Callback]], mode: RunMode, *, 
                 after: Optional[DelayType] = None) -> None:
        if mode.is_gated:
            self.on_tick(cb, delta=mode.gated_delay(after).count)
        else:
            self.communicate(cb, delta=mode.asynchronous_delay(after))
       
    # def schedule_before(self, cb: C):

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
    
class UserOperation(Worker):
    def __enter__(self) -> UserOperation:
        self.not_idle()
        return self
    
    def __exit__(self, 
                 exc_type: Optional[type[BaseException]],  # @UnusedVariable
                 exc_val: Optional[BaseException],  # @UnusedVariable
                 exc_tb: Optional[TracebackType]) -> Literal[False]:  # @UnusedVariable
        self.idle()
        return False

class Clock:
    system: Final[System]
    engine: Final[Engine]
    clock_thread: Final[ClockThread]
    def __init__(self, system: System) -> None:
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
        self.system.before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, tick: Optional[int] = None, delta: Optional[int] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.after_tick() called with both tick and delta specified"
            delta = max(0, tick-self.next_tick)
        elif delta is None:
            delta = 0
        self.system.after_tick(fn, delta=delta)
    
    # Calling await_tick() when the clock isn't running only works if there is another thread that
    # will advance it.  
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
            self.clock_thread.after_tick([(delta, cb)])
            while not e.is_set():
                e.wait(_wait_timeout)

    def advance(self, min_delay: Optional[Time] = None) -> None:
        assert not self.running, "Clock.advance_clock() called while clock is running"
        ct = self.clock_thread
        if min_delay is not None:
            next_allowed = ct.last_tick_time+min_delay
            if next_allowed > time_now():
                def do_advance():
                    ct.wake_up()
                self.system.engine.call_at([(next_allowed, do_advance, False)])
                return
        ct.wake_up()
        
    def start(self, interval: Optional[Time] = None) -> None:
        assert not self.running, "Clock.start() called while clock is running"
        self.clock_thread.start_clock(interval)
        
    def pause(self) -> None:
        assert self.running, "Clock.pause() called while clock is running"
        self.clock_thread.pause_clock()

class Batch:
    system: Final[System]
    nested: Final[Optional[Batch]]
    
    buffer_communicate: list[DevCommRequest]
    buffer_call_at: list[TimerRequest]
    buffer_call_after: list[TimerDeltaRequest]
    buffer_before_tick: list[ClockRequest]
    buffer_after_tick: list[ClockRequest]
    buffer_on_tick: list[ClockCommRequest]
    
    def __init__(self, system: System, *, nested: Optional[Batch]) -> None:
        self.system = system
        self.nested = nested
        self.buffer_communicate = []
        self.buffer_call_at = []
        self.buffer_call_after = []
        self.buffer_before_tick = []
        self.buffer_after_tick = []
        self.buffer_on_tick = []

    def communicate(self, reqs: Sequence[DevCommRequest]) -> None:
        self.buffer_communicate.extend(reqs)
        
    def call_at(self, reqs: Sequence[TimerRequest]) -> None:
        self.buffer_call_at.extend(reqs)
        
    def call_after(self, reqs: Sequence[TimerDeltaRequest]) -> None:
        self.buffer_call_after.extend(reqs)
        
    def before_tick(self, reqs: Sequence[ClockRequest]) -> None:
        self.buffer_before_tick.extend(reqs)

    def after_tick(self, reqs: Sequence[ClockRequest]) -> None:
        self.buffer_after_tick.extend(reqs)

    def on_tick(self, reqs: Sequence[ClockCommRequest]) -> None:
        self.buffer_on_tick.extend(reqs)
                
    def __enter__(self) -> Batch:
        return self

    # I'm currently assuming that if we get an exception,
    # we don't want to try to do the communication.  Instead
    # we just return, clearing ourselves from the system
    # if we're not nested    
    def __exit__(self, 
                 exc_type: Optional[type[BaseException]], 
                 exc_val: Optional[BaseException],  # @UnusedVariable
                 exc_tb: Optional[TracebackType]) -> Literal[False]:  # @UnusedVariable
        if exc_type is None:
            sink: Union[Batch,Engine] = self.nested or self.system.engine
            sink.communicate(self.buffer_communicate)
            sink.call_at(self.buffer_call_at)
            sink.call_after(self.buffer_call_after)
            sink.before_tick(self.buffer_before_tick)
            sink.after_tick(self.buffer_after_tick)
            sink.on_tick(self.buffer_on_tick)
            with self.system._batch_lock:
                self.system._batch = self.nested
        return False
    

class System:
    board: Board
    engine: Engine
    clock: Clock
    _batch_lock: Final[Lock]
    _batch: Optional[Batch]
    
    def __init__(self, *, board: Board):
        self.board = board
        self.engine = Engine()
        self.clock = Clock(self)
        self._batch = None
        self._batch_lock = Lock()
        board.join_system(self)

    def __enter__(self) -> System:
        self.engine.__enter__()
        return self
    
    def __exit__(self, 
                 exc_type: Optional[type[BaseException]], 
                 exc_val: Optional[BaseException], 
                 exc_tb: Optional[TracebackType]) -> bool:
        return self.engine.__exit__(exc_type, exc_val, exc_tb)
    
    def stop(self) -> None:
        self.engine.stop()
        self.board.stop()
        
    def abort(self) -> None:
        self.engine.abort()
        self.board.abort()
        
    def _channel(self) -> Union[Batch, Engine]:
        with self._batch_lock:
            return self._batch or self.engine
    def communicate(self, req: DevCommRequest) -> None:
        self._channel().communicate([req])
        
    def call_at(self, t: Timestamp, fn: TimerFunc, *, daemon: bool = False) -> None:
        self._channel().call_at([(t, fn, daemon)])
        
    def call_after(self, delta: Time, fn: TimerFunc, *, daemon: bool = False) -> None:
        self._channel().call_after([(delta, fn, daemon)])
        
    def before_tick(self, fn: ClockCallback, *, delta: int=0) -> None:
        self._channel().before_tick([(delta, fn)])

    def after_tick(self, fn: ClockCallback, *, delta: int=0):
        self._channel().after_tick([(delta, fn)])
        

    def on_tick(self, req: DevCommRequest, *, delta: int=0):
        self._channel().on_tick([(delta, req)])
        
    def batched(self) -> Batch:
        with self._batch_lock:
            self._batch = Batch(self, nested=self._batch)
            return self._batch
    