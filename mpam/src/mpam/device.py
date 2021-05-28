from __future__ import annotations
from typing import Optional, Final, Mapping, Callable, Literal,\
    TypeVar, Sequence, TYPE_CHECKING, Union, ClassVar, Generic, Hashable
from types import TracebackType
from quantities.dimensions import Time, Volume, Temperature
from quantities.timestamp import time_now, Timestamp
from threading import Event, Lock, Thread

from mpam.types import XYCoord, Dir, OnOff, Delayed, Liquid, RunMode, DelayType,\
    Operation, OpScheduler, Orientation, TickNumber, tick, Ticks,\
    unknown_reagent, waste_reagent, Reagent, ChangeCallbackList, ChangeCallback,\
    Callback
from mpam.engine import DevCommRequest, TimerFunc, ClockCallback,\
    Engine, ClockThread, _wait_timeout, Worker, TimerRequest, ClockRequest,\
    ClockCommRequest, TimerDeltaRequest
from mpam.exceptions import PadBrokenError
from enum import Enum, auto
import itertools
from erk.errors import ErrorHandler, PRINT
from matplotlib import pyplot
from quantities.temperature import TemperaturePoint

if TYPE_CHECKING:
    from mpam.drop import Drop

PadArray = Mapping[XYCoord, 'Pad']

T = TypeVar('T')
Modifier = Callable[[T],T]

class BoardComponent:
    board: Final[Board]
    
    def __init__(self, board: Board) -> None:
        self.board = board
        

BC = TypeVar('BC', bound='BinaryComponent')
        
class BinaryComponent(BoardComponent, Generic[BC]):
    _state: OnOff
    broken: bool
    state_change_callbacks: Final[ChangeCallbackList[OnOff]]
    
    
    def __init__(self, board: Board, initial_state: OnOff = OnOff.OFF) -> None:
        super().__init__(board)
        self._state = initial_state
        self.broken = False
        self.set_device_state: Callable[[OnOff], None]
        self.state_change_callbacks = ChangeCallbackList[OnOff]()
        
    @property
    def current_state(self) -> OnOff:
        return self._state

    @current_state.setter
    def current_state(self, val: OnOff) -> None:
        old = self._state
        self._state = val
        self.state_change_callbacks.process(old, val)
        
    def on_state_change(self, cb: ChangeCallback[OnOff], *, key: Optional[Hashable] = None):
        self.state_change_callbacks.add(cb, key=key)
        
    class ModifyState(Operation[BC, OnOff]):
        def _schedule_for(self, obj: BC, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,
                          future: Optional[Delayed[OnOff]] = None
                          ) -> Delayed[OnOff]:
            
            if obj.broken:
                raise PadBrokenError
            mod = self.mod
            if future is None:
                future = Delayed[OnOff]()
            real_future = future
            setter = obj.set_device_state
            
            def cb() -> Optional[Callback]:
                old = obj.current_state
                new = mod(old)
                # print(f"Setting {obj} to {new}")
                setter(new)
                obj.current_state= new
                # print(f"Back from setting {obj} val = {obj._state}")
                finish: Optional[Callback] = None if not post_result else (lambda : real_future.post(old))
                return finish
            
            obj.board.schedule(cb, mode, after=after)
            return future
        
        def __init__(self, mod: Modifier[OnOff]) -> None:
            self.mod: Final[Modifier[OnOff]] = mod
    
    @staticmethod        
    def SetState(val: OnOff) -> ModifyState:
        return BinaryComponent[BC].ModifyState(lambda _ : val)
            
 
    TurnOn: ClassVar[ModifyState]
    TurnOff: ClassVar[ModifyState]
    Toggle: ClassVar[ModifyState]
    
    ...
    
BinaryComponent[BC].TurnOn = BinaryComponent.SetState(OnOff.ON)
BinaryComponent[BC].TurnOff = BinaryComponent.SetState(OnOff.OFF)
BinaryComponent[BC].Toggle = BinaryComponent.ModifyState(lambda s: ~s)
    
    
    
class Pad(OpScheduler['Pad'], BinaryComponent['Pad']):
    location: Final[XYCoord]
    exists: Final[bool]
    # broken: bool
    
    _pads: Final[PadArray]
    _drop: Optional[Drop]
    _dried_liquid: Optional[Drop]
    _neighbors: Optional[Sequence[Pad]]
    _well: Optional[Well] = None
    _magnet: Optional[Magnet] = None
    _heater: Optional[Heater] = None
    
    _drop_change_callbacks: Final[ChangeCallbackList[Optional[Drop]]]
        
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
    def magnet(self) -> Optional[Magnet]:
        return self._magnet
    
    @property
    def heater(self) -> Optional[Heater]:
        return self._heater
    
    @property
    def drop(self) -> Optional[Drop]:
        return self._drop
    
    @drop.setter
    def drop(self, drop: Optional[Drop]):
        old = self._drop
        self._drop = drop
        self._drop_change_callbacks.process(old, drop)
    
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
        BinaryComponent.__init__(self, board, initial_state=OnOff.OFF)
        self.location = loc
        self.exists = exists
        # self.broken = False
        self._pads = board.pad_array
        self._drop = None
        self._dried_liquid = None
        self._drop_change_callbacks = ChangeCallbackList()
        
    def __repr__(self) -> str:
        return f"Pad({self.column},{self.row})"
        
    def neighbor(self, d: Dir) -> Optional[Pad]:
        n = self.board.orientation.neighbor(d, self.location)
        p = self._pads.get(n, None)
        if p is None or not p.exists:
            return None
        return p
    
    def empty(self) -> bool:
        return self.drop is None
    
    def safe(self) -> bool:
        return self.empty and all(map(lambda n : n.empty, self.neighbors))
    
    def on_drop_change(self, cb: ChangeCallback[Optional[Drop]], *, key: Optional[Hashable] = None):
        self._drop_change_callbacks.add(cb, key=key)
    
WellPadLoc = Union[tuple['WellGroup', int], 'Well']

class WellPad(OpScheduler['WellPad'], BinaryComponent['WellPad']):
        loc: WellPadLoc
        
        def __repr__(self) -> str:
            loc = getattr(self, 'loc', None)
            if loc is None:
                return f"WellPad(unassigned, {id(self)})"
            elif isinstance(loc, Well):
                return f"WellPad({loc}[gate])"
            else:
                return f"WellPad({loc[0]}[{loc[1]}]"
            
        def set_location(self, loc: WellPadLoc) -> None:
            self.loc = loc

class WellState(Enum):
    EXTRACTABLE = auto()
    READY = auto()
    DISPENSED = auto()
    ABSORBED = auto()
    
# -1 is the well's gate pad.  Others are indexes into the shared_pads list
WellOpStep = Sequence[int]
WellOpStepSeq = Sequence[WellOpStep]
WellOpSeqDict = Mapping[tuple[WellState,WellState], WellOpStepSeq]

class WellMotion:
    group: Final[WellGroup]
    target: Final[WellState]
    future: Final[Delayed[WellGroup]]
    post_result: Final[bool]
    well_gates: Final[set[WellPad]]
    pad_states: Final[dict[Pad, OnOff]]
    next_step: int
    one_tick: Final[ClassVar[Ticks]] = 1*tick
    sequence: WellOpStepSeq
    used_gate: bool
    
    def __init__(self, group: WellGroup, target: WellState, *,
                 future: Optional[Delayed[WellGroup]] = None,
                 post_result: bool = True) -> None:
        self.group = group
        self.target = target
        self.future = future or Delayed[WellGroup]()
        self.post_result = post_result
        self.well_gates = set[WellPad]()
        self.pad_states = {}
        self.next_step = 0
        self.callback: ClockCallback = lambda : self.do_step()
        self.used_gate = False
        
    def do_step(self) -> Optional[Ticks]:
        group = self.group
        # On the first step, we need to see if this is really necessary or if we 
        # can piggyback onto another motion (or just return) 
        if self.next_step == 0:
            with group.lock:
                current = group.motion
                if current is not None:
                    if current.target == self.target and not current.used_gate:
                        # The current one is already going the same place we are and
                        # it hasn't twiddled a gate yet, so we can piggyback.
                        # (Strictly speaking, we could do that if it's *just* twiddled
                        # the gates for the first time and it hasn't taken place yet, 
                        # but that's probably more bookkeeping than is worthwhile.)
                        current.well_gates.update(self.well_gates)
                        current.pad_states.update(self.pad_states)
                        current.future.when_value(lambda g : self.future.post(g))
                        return None
                    else:
                        # Otherwise, we'll try again next time.  (I was going to reschedule 
                        # when the current one was done, but it's almost certainly cheaper to
                        # just check each tick.
                        return self.one_tick
                if group.state is self.target:
                    # There's no motion, and we're already where we want to be.
                    # If this is EXTRACTABLE or READY, we're fine, otherwise, we got here
                    # without using our gates, so we need to go through READY again
                    if self.target is WellState.READY or self.target is WellState.EXTRACTABLE:
                        self.future.post(group)
                        return None
                if group.state is WellState.READY or self.target is WellState.READY:
                    self.sequence = group.sequences[(group.state, self.target)]
                else:
                    self.sequence = list(group.sequences[(group.state, WellState.READY)])
                    self.sequence += group.sequences[(WellState.READY, self.target)]
                assert len(self.sequence) > 0
                group.motion = self
        shared_pads = group.shared_pads
        states = list(itertools.repeat(OnOff.OFF, len(shared_pads)))
        gate_state = OnOff.OFF
        for pad_index in self.sequence[self.next_step]:
            if pad_index == -1:
                gate_state = OnOff.ON
                self.used_gate = True
            else:
                states[pad_index] = OnOff.ON
        for (i, shared) in enumerate(shared_pads):
            shared.schedule(WellPad.SetState(states[i]), post_result=False)
        for gate in self.well_gates:
            gate.schedule(WellPad.SetState(gate_state), post_result=False)
        self.next_step += 1
        if self.next_step == len(self.sequence):
            # we're done.  If there are any (exit) pads to twiddle, we do it now.
            for (pad, state) in self.pad_states.items():
                pad.schedule(Pad.SetState(state), post_result=False)
            # And on the other side, we clean up
            def cb() -> None:
                # Any gates we turned on, we turn off at the next tick
                for gate in self.well_gates:
                    gate.schedule(WellPad.TurnOff, post_result=False)
                with group.lock:
                    group.motion = None
                    group.state = self.target
                    if self.post_result:
                        self.future.post(group)
            group.board.after_tick(cb)
            return None
        else:
            # Otherwise we do the next step the next time around
            return self.one_tick
            
                    
    
class WellGroup(BoardComponent, OpScheduler['WellGroup']):
    name: Final[str]
    shared_pads: Final[Sequence[WellPad]]
    wells: list[Well]
    sequences: Final[WellOpSeqDict]
    
    lock: Final[Lock]
    
    state: WellState
    motion: Optional[WellMotion]
    
    
    def __init__(self, name: str, 
                 board: Board,
                 pads: Sequence[WellPad],
                 sequences: WellOpSeqDict) -> None:
        BoardComponent.__init__(self, board)
        self.name = name
        self.shared_pads = pads
        for (index, pad) in enumerate(pads):
            pad.set_location((self, index))
        self.sequences = sequences
        self.wells = []
        
        self.state = WellState.EXTRACTABLE
        self.motion = None
        self.lock = Lock()
        
    def __repr__(self) -> str:
        return f"WellGroup[{self.name}]"
        
    def add_well(self, well: Well) -> None:
        self.wells.append(well)
        
    class TransitionTo(Operation['WellGroup','WellGroup']):
        target: Final[WellState]
        well: Final[Optional[Well]]
        
        def __init__(self, target: WellState, *,
                     well: Optional[Well] = None) -> None:
            self.target = target
            self.well = well
            
        def _schedule_for(self, group: WellGroup, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,
                          future: Optional[Delayed[WellGroup]] = None
                          )-> Delayed[WellGroup]:
            board = group.board
            motion = WellMotion(group, self.target, future=future, post_result=post_result)
            well = self.well
            if well is not None:
                motion.well_gates.add(well.gate)
                target = self.target
                # assert target is WellState.DISPENSED or target is WellState.ABSORBED, \
                    # f"Well provided on transition to {target}"
                motion.pad_states[well.exit_pad] = OnOff.ON if target is WellState.DISPENSED else OnOff.OFF
            board.before_tick(motion.callback, delta=mode.gated_delay(after))
            return motion.future
    
PadBounds = Sequence[tuple[float,float]]

class Well(OpScheduler['Well'], BoardComponent):
    number: Final[int]
    group: Final[WellGroup]
    capacity: Final[Volume]
    dispensed_volume: Final[Volume]
    is_voidable: Final[bool]
    exit_pad: Final[Pad]
    gate: Final[WellPad]
    _contents: Optional[Liquid]
    gate_pad_bounds: Final[Optional[PadBounds]]
    shared_pad_bounds: Final[Optional[Sequence[Union[PadBounds, Sequence[PadBounds]]]]]
    
    _liquid_change_callbacks: Final[ChangeCallbackList[Optional[Liquid]]]
    
    @property
    def contents(self) -> Optional[Liquid]:
        return self._contents
    
    @contents.setter
    def contents(self, liquid: Optional[Liquid]):
        old = self._contents
        self._contents = liquid
        self._liquid_change_callbacks.process(old, liquid)
    
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
    
    def __init__(self, *,
                 board: Board,
                 number: int,
                 group: WellGroup,
                 exit_pad: Pad,
                 gate: WellPad,
                 capacity: Volume,
                 dispensed_volume: Volume,
                 is_voidable: bool = False,
                 gate_pad_bounds: Optional[PadBounds] = None,
                 shared_pad_bounds: Optional[Sequence[Union[PadBounds, Sequence[PadBounds]]]] = None
                 ) -> None:
        BoardComponent.__init__(self, board)
        self.number = number
        self.group = group
        self.exit_pad = exit_pad
        self.gate = gate
        self.capacity = capacity
        self.dispensed_volume = dispensed_volume
        self.is_voidable = is_voidable
        self._contents = None
        self.gate_pad_bounds = gate_pad_bounds
        self.shared_pad_bounds = shared_pad_bounds
        self._liquid_change_callbacks = ChangeCallbackList()

        group.add_well(self)
        assert exit_pad._well is None, f"{exit_pad} is already associated with {exit_pad.well}"
        exit_pad._well = self
        gate.set_location(self)
        
    def __repr__(self) -> str:
        return f"Well[{self.number} <> {self.exit_pad}]"
    
    def _can_accept(self, liquid: Liquid) -> bool:
        c = self._contents
        if c is None: return True
        my_r = c.reagent
        their_r = liquid.reagent
        return (my_r == their_r 
                or my_r == unknown_reagent 
                or their_r == unknown_reagent
                or my_r == waste_reagent) 
    
    def transfer_in(self, liquid: Liquid, *,
                    volume: Optional[Volume] = None, 
                    on_overflow: ErrorHandler = PRINT,
                    on_reagent_mismatch: ErrorHandler = PRINT) -> None:
        if volume is None:
            volume = liquid.volume
        on_overflow.expect_true(self.remaining_capacity >= volume,
                    lambda : f"Tried to add {volume} to {self}.  Remaining capacity only {self.remaining_capacity}")
        if self._contents is None:
            self.contents = Liquid(liquid.reagent, volume)
        else:
            r = self._contents.reagent
            on_reagent_mismatch.expect_true(self._can_accept(liquid),
                                            lambda : f"Adding {liquid.reagent} to {self} containing {r}")
            self._contents += volume
            liquid -= volume
        print(f"{self} now contains {self.contents}")
            
    def transfer_out(self, volume: Volume, *,
                     on_empty: ErrorHandler = PRINT) -> Liquid:
        on_empty.expect_true(self.volume>= volume,
                    lambda : f"Tried to draw {volume} from {self}, which only has {self.volume}")
        reagent: Reagent
        if self._contents is None:
            reagent = unknown_reagent
        else:
            reagent = self._contents.reagent
            print(f"Removing {volume} from {self._contents}")
            self._contents -= volume
        print(f"{self} now contains {self.contents}")
        return Liquid(reagent, volume)

    def contains(self, liquid: Liquid,
                 *, on_overflow: ErrorHandler = PRINT) -> None:
        on_overflow.expect_true(liquid.volume <= self.capacity,
                                lambda : f"Asserted {self} contains {liquid}. capacity only {self.capacity}")
        self._contents = None
        self.transfer_in(liquid, volume=min(liquid.volume, self.capacity))
        print(f"Volume is now {self.volume}")
        
    def on_liquid_change(self, cb: ChangeCallback[Optional[Liquid]], *, key: Optional[Hashable] = None) -> None:
        self._liquid_change_callbacks.add(cb, key=key)
        
        
class Magnet(OpScheduler['Magnet'], BinaryComponent['Magnet']): 
    pads: Final[Sequence[Pad]]
    
    def __init__(self, board: Board, *, pads: Sequence[Pad]) -> None:
        BinaryComponent.__init__(self, board)
        self.pads = pads
        for pad in pads:
            pad._magnet = self
            
    def __repr__(self) -> str:
        return f"Magnet({', '.join(str(self.pads))})"
    
class Heater(OpScheduler['Heater'], BoardComponent):
    num: Final[int]
    pads: Final[Sequence[Pad]]
    _last_reading: Optional[TemperaturePoint]
    _target: Optional[TemperaturePoint]
    polling_interval: Final[Time]
    _temperature_change_callbacks: Final[ChangeCallbackList[Optional[TemperaturePoint]]]
    _target_change_callbacks: Final[ChangeCallbackList[Optional[TemperaturePoint]]]
    
    @property
    def current_temperature(self) -> Optional[TemperaturePoint]:
        return self._last_reading
    
    @current_temperature.setter
    def current_temperature(self, new: Optional[TemperaturePoint]) -> None:
        old = self._last_reading
        self._last_reading = new
        self._temperature_change_callbacks.process(old, new)
        
    @property
    def target(self) -> Optional[TemperaturePoint]:
        return self._target
    
    @target.setter
    def target(self, new: Optional[TemperaturePoint]) -> None:
        old = self._target
        self._target = new
        self._target_change_callbacks.process(old, new)
        
    def __init__(self, num: int, board: Board, *, 
                 pads: Sequence[Pad],
                 polling_interval: Time) -> None:
        BoardComponent.__init__(self, board)
        self.num = num
        self.pads = pads
        self.polling_interval = polling_interval
        self._last_reading = None
        self._target = None
        self._temperature_change_callbacks = ChangeCallbackList()
        self._target_change_callbacks = ChangeCallbackList()
        for pad in pads:
            pad._heater = self
            
    def __repr__(self) -> str:
        return f"Heater({self.num})"
    
    # If the implementation doesn't override, then we always get back None (immediately)
    def poll(self) -> Delayed[Optional[TemperaturePoint]]:
        future = Delayed[Optional[TemperaturePoint]]()
        future.post(None)
        return future
        
        
    def on_temperature_change(self, cb: ChangeCallback[Optional[TemperaturePoint]], *, key: Optional[Hashable] = None):
        self._temperature_change_callbacks.add(cb, key=key)

    def on_target_change(self, cb: ChangeCallback[Optional[TemperaturePoint]], *, key: Optional[Hashable] = None):
        self._target_change_callbacks.add(cb, key=key)
    

    
class SystemComponent:
    system: Optional[System] = None
    _after_update: Final[list[Callback]]
    _monitor_callbacks: Final[list[Callback]]
    
    def __init__(self) -> None:
        self._after_update = []
        self._monitor_callbacks = []
        
    def join_system(self, system: System) -> None:
        self.system = system
        
    def in_system(self) -> System:
        system = self.system
        assert system is not None
        return system
    
    def update_state(self) -> None:
        raise NotImplementedError(f"{self.__class__}.update_state() not defined")
    
    def add_monitor(self, cb: Callback) -> None:
        self._monitor_callbacks.append(cb)
    
    def finish_update(self) -> None:
        # This is assumed to only be called in the DevComm thread, so
        # no locking is necessary.
        for cb in self._after_update:
            cb()
        self._after_update.clear()
        for cb in self._monitor_callbacks:
            cb()
        
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
        
    def call_at(self, t: Timestamp, fn: Callback, *, daemon: bool = False):
        self.in_system().call_at(t, fn, daemon=daemon)
        
    def call_after(self, delta: Time, fn: Callback, *, daemon: bool = False):
        self.in_system().call_after(delta, fn, daemon=daemon)
        
    def before_tick(self, fn: ClockCallback, *, delta: Ticks = Ticks.ZERO()) -> None:
        self.in_system().before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, *, delta: Ticks = Ticks.ZERO()):
        self.in_system().after_tick(fn, delta=delta)

    def on_tick(self, cb: Callable[[], Optional[Callback]], *, delta: Ticks = Ticks.ZERO()):
        req = self.make_request(cb)
        self.in_system().on_tick(req, delta=delta)
 
    def schedule(self, cb: Callable[[], Optional[Callback]], mode: RunMode, *, 
                 after: Optional[DelayType] = None) -> None:
        if mode.is_gated:
            self.on_tick(cb, delta=mode.gated_delay(after))
        else:
            self.communicate(cb, delta=mode.asynchronous_delay(after))
       
    # def schedule_before(self, cb: C):

class Board(SystemComponent):
    pads: Final[PadArray]
    wells: Final[Sequence[Well]]
    magnets: Final[Sequence[Magnet]]
    heaters: Final[Sequence[Heater]]
    _well_groups: Mapping[str, WellGroup]
    orientation: Final[Orientation]
    drop_motion_time: Final[Time]
    _drop_size: Volume
    
    def __init__(self, *, 
                 pads: PadArray,
                 wells: Sequence[Well],
                 magnets: Optional[Sequence[Magnet]] = None,
                 heaters: Optional[Sequence[Heater]] = None,
                 orientation: Orientation,
                 drop_motion_time: Time) -> None:
        super().__init__()
        self.pads = pads
        self.wells = wells
        self.magnets = [] if magnets is None else magnets
        self.heaters = [] if heaters is None else heaters
        self.orientation = orientation
        self.drop_motion_time = drop_motion_time

    def stop(self) -> None:
        pass    
    def abort(self) -> None:
        pass
    
    @property
    def pad_array(self) -> PadArray:
        return self.pads
    
    def pad_at(self, x: int, y: int) -> Pad:
        return self.pads[XYCoord(x,y)]
    
    @property
    def max_row(self) -> int:
        return max(coord.y for coord in self.pads)

    @property
    def min_row(self) -> int:
        return min(coord.y for coord in self.pads)

    @property
    def max_column(self) -> int:
        return max(coord.x for coord in self.pads)

    @property
    def min_column(self) -> int:
        return min(coord.x for coord in self.pads)
    
    @property
    def well_groups(self) -> Mapping[str, WellGroup]:
        cache = getattr(self, '_well_groups', None)
        if cache is None:
            cache = {well.group.name: well.group for well in self.wells}
            self._well_groups = cache
        return cache
    
    @property
    def drop_size(self) -> Volume:
        cache = getattr(self, '_drop_size', None)
        if cache is None:
            cache = self.wells[0].dispensed_volume
            assert all(w.dispensed_volume==cache for w in self.wells), "Not all wells dispense the same volume"
            self._drop_size = cache
        return cache
        
        
    
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
    def next_tick(self) -> TickNumber:
        return self.clock_thread.next_tick
    
    @property
    def last_tick(self) -> TickNumber:
        return self.next_tick-1*tick
    
    @property
    def running(self) -> bool:
        return self.clock_thread.running
    
    def before_tick(self, fn: ClockCallback, tick: Optional[TickNumber] = None, delta: Optional[Ticks] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.before_tick() called with both tick and delta specified"
            delta = max(Ticks.ZERO(), tick-self.next_tick)
        elif delta is None:
            delta = Ticks.ZERO()
        self.system.before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, tick: Optional[TickNumber] = None, delta: Optional[Ticks] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.after_tick() called with both tick and delta specified"
            delta = max(Ticks.ZERO(), tick-self.next_tick)
        elif delta is None:
            delta = Ticks.ZERO()
        self.system.after_tick(fn, delta=delta)
    
    # Calling await_tick() when the clock isn't running only works if there is another thread that
    # will advance it.  
    def await_tick(self, tick: Optional[TickNumber] = None, delta: Optional[Ticks] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.await_tick() called with both tick and delta specified"
            delta = tick-self.next_tick
        elif delta is None:
            delta = Ticks.ZERO()
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
        self.engine = Engine(default_clock_interval=board.drop_motion_time)
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
        
    def before_tick(self, fn: ClockCallback, *, delta: Ticks=Ticks.ZERO()) -> None:
        self._channel().before_tick([(delta, fn)])

    def after_tick(self, fn: ClockCallback, *, delta: Ticks = Ticks.ZERO()):
        self._channel().after_tick([(delta, fn)])
        

    def on_tick(self, req: DevCommRequest, *, delta: Ticks = Ticks.ZERO()):
        self._channel().on_tick([(delta, req)])
        
    def batched(self) -> Batch:
        with self._batch_lock:
            self._batch = Batch(self, nested=self._batch)
            return self._batch
        
        
    def run_monitored(self, fn: Callable[[System],T]) -> T:
        from mpam.monitor import BoardMonitor
        val: T
        
        done = Event()
        def run_it() -> None:
            nonlocal val
            with self:
                val = fn(self)  # @UnusedVariable
            done.set()

        thread = Thread(target=run_it)
        monitor = BoardMonitor(self.board)
        thread.start()
        while not done.is_set():
            monitor.process_display_updates()
            monitor.figure.canvas.draw_idle()
            pyplot.pause(0.02)
            
        pyplot.pause(100)
        return val
    