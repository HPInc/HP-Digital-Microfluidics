from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
import itertools
import random
from threading import Event, Lock, Thread
from types import TracebackType
from typing import Optional, Final, Mapping, Callable, Literal, \
    TypeVar, Sequence, TYPE_CHECKING, Union, ClassVar, Hashable, Any, Iterator,\
    NamedTuple, Iterable

from matplotlib.gridspec import SubplotSpec

from erk.basic import not_None
from erk.errors import ErrorHandler, PRINT
from mpam.engine import DevCommRequest, TimerFunc, ClockCallback, \
    Engine, ClockThread, _wait_timeout, Worker, TimerRequest, ClockRequest, \
    ClockCommRequest, TimerDeltaRequest, IdleBarrier
from mpam.exceptions import PadBrokenError
from mpam.types import XYCoord, Dir, OnOff, Delayed, Liquid, RunMode, DelayType, \
    Operation, OpScheduler, Orientation, TickNumber, tick, Ticks, \
    unknown_reagent, waste_reagent, Reagent, ChangeCallbackList, ChangeCallback, \
    Callback, MixResult, State, CommunicationScheduler
from quantities.SI import sec, ms
from quantities.core import Unit
from quantities.dimensions import Time, Volume, Frequency
from quantities.temperature import TemperaturePoint, abs_F
from quantities.timestamp import time_now, Timestamp
from _collections import defaultdict


if TYPE_CHECKING:
    from mpam.drop import Drop, Blob
    from mpam.monitor import BoardMonitor
    from mpam.pipettor import Pipettor

PadArray = Mapping[XYCoord, 'Pad']

T = TypeVar('T')
Modifier = Callable[[T],T]

class BoardComponent:
    board: Final[Board]
    
    def __init__(self, board: Board) -> None:
        self.board = board
    def schedule_communication(self, cb: Callable[[], Optional[Callback]], mode: RunMode, *,  
                               after: Optional[DelayType] = None) -> None:  
        return self.board.schedule(cb, mode=mode, after=after)
    
    def delayed(self, function: Callable[[], T], *,
                after: Optional[DelayType]) -> Delayed[T]:
        return self.board.delayed(function, after=after)
 
    def user_operation(self) -> UserOperation:
        return UserOperation(self.board.in_system().engine.idle_barrier)

BC = TypeVar('BC', bound='BinaryComponent')
        
class BinaryComponent(BoardComponent, OpScheduler[BC]):
    _state: Final[State[OnOff]]
    broken: bool
    live: bool
    
    def __init__(self, board: Board, *,
                 state: State[OnOff],
                 live: bool = True) -> None:
        super().__init__(board)
        self._state = state
        self.broken = False
        self.live = live
        
    @property
    def current_state(self) -> OnOff:
        return self._state.current_state

    @current_state.setter
    def current_state(self, val: OnOff) -> None:
        self._state.current_state = val
        
    def on_state_change(self, cb: ChangeCallback[OnOff], *, key: Optional[Hashable] = None):
        self._state.on_state_change(cb, key=key)
        
    class ModifyState(Operation[BC, OnOff]):
        def _schedule_for(self, obj: BC, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,
                          ) -> Delayed[OnOff]:
            
            if obj.broken:
                raise PadBrokenError(obj)
            mod = self.mod
            future = Delayed[OnOff]()
            # state_obj = obj._state
            
            def cb() -> Optional[Callback]:
                old = obj.current_state
                new = mod(old)
                # print(f"Setting {obj} to {new}")
                obj._state.realize_state(new)
                obj.current_state = new
                # print(f"Back from setting {obj} val = {obj._state}")
                finish: Optional[Callback] = None if not post_result else (lambda : future.post(old))
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
    
class PipettingTarget:
    
    @property
    @abstractmethod
    def contents(self) -> Optional[Liquid]: ...
    
    @property
    def pipettor(self) -> Optional[Pipettor]:
        return None

    @abstractmethod
    def prepare_for_add(self) -> None: # @UnusedVariable
        ...

    @abstractmethod
    def prepare_for_remove(self) -> None: 
        ...
    
    @abstractmethod
    def pipettor_added(self, reagent: Reagent, volume: Volume, *, # @UnusedVariable
                       mix_result: Optional[MixResult],
                       last: bool) -> None: # @UnusedVariable
        ...
    
    @abstractmethod
    def pipettor_removed(self, reagent: Reagent, volume: Volume, *,
                         last: bool) -> None: # @UnusedVariable
        ...
        
class DropLoc(ABC, CommunicationScheduler):
    blob: Optional[Blob] = None
    _drop: Optional[Drop] = None
    _neighbors_for_blob: Optional[Sequence[DropLoc]] = None
    _drop_change_callbacks: Final[ChangeCallbackList[Optional[Drop]]]
    
    @property
    def drop(self) -> Optional[Drop]:
        return self._drop
    
    @drop.setter
    def drop(self, drop: Optional[Drop]):
        old = self._drop
        self._drop = drop
        self._drop_change_callbacks.process(old, drop)
        
    @property
    def checked_drop(self) -> Drop:
        if self._drop is not None:
            return self._drop
        print(f"Drop at {self}: {self._drop}")
        raise TypeError(f"{self} has no drop")
    
    
    @property
    def neighbors_for_blob(self) -> Sequence[DropLoc]:
        ns = self._neighbors_for_blob
        if ns is None:
            ns = self._neighbors_for_blob = self.compute_neighbors_for_blob()
        return ns
    
    def __init__(self) -> None:
        self._drop_change_callbacks = ChangeCallbackList()
        
    def on_drop_change(self, cb: ChangeCallback[Optional[Drop]], *, key: Optional[Hashable] = None):
        self._drop_change_callbacks.add(cb, key=key)
        
    
    @abstractmethod
    def compute_neighbors_for_blob(self) -> Sequence[DropLoc]: ...
    
    
    
class LocatedPad:
    location: Final[XYCoord]
    
    @property
    def row(self) -> int:
        return self.location.y 
    @property
    def column(self) -> int:
        return self.location.x
    
    
    def __init__(self, loc: XYCoord) -> None:
        self.location = loc
    
    
class Pad(BinaryComponent['Pad'], DropLoc, LocatedPad):
    exists: Final[bool]
    
    reserved: bool = False
    # broken: bool
    
    _pads: Final[PadArray]
    _dried_liquid: Optional[Drop]
    _neighbors: Optional[Sequence[Pad]] = None
    _all_neighbors: Optional[Sequence[Pad]] = None
    _between_pads: Optional[Mapping[Pad,Pad]] = None
    _well: Optional[Well] = None
    _magnet: Optional[Magnet] = None
    _heater: Optional[Heater] = None
    _extraction_point: Optional[ExtractionPoint] = None
    
        
    
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
    def extraction_point(self) -> Optional[ExtractionPoint]:
        return self._extraction_point
    
    
    @property
    def dried_liquid(self) -> Optional[Drop]:
        return self._dried_liquid
    
    @property
    def neighbors(self) -> Sequence[Pad]:
        ns = self._neighbors
        if ns is None:
            ns = [n for d in (Dir.N,Dir.S,Dir.E,Dir.W) if (n := self.neighbor(d)) is not None]
            self._neighbors = ns
        return ns

    @property
    def all_neighbors(self) -> Sequence[Pad]:
        ns = self._all_neighbors
        if ns is None:
            ns = [n for d in Dir if (n := self.neighbor(d)) is not None]
            self._all_neighbors = ns
        return ns
    
    @property
    def corner_neighbors(self) -> Sequence[Pad]:
        ns = self._neighbors
        if ns is None:
            ns = [n for d in (Dir.NE,Dir.SE,Dir.SW,Dir.NW) if (n := self.neighbor(d)) is not None]
            self._neighbors = ns
        return ns

    
    
    @property
    def between_pads(self) -> Mapping[Pad, Pad]:
        bps: Optional[Mapping[Pad,Pad]] = getattr(self, '_between_pads', None)
        if bps is None:
            bps = {p: m for d in Dir.cardinals() 
                   if (m := self.neighbor(d)) is not None 
                        and (p := m.neighbor(d)) is not None}
            self._between_pads = bps
        return bps
    
    def __init__(self, loc: XYCoord, board: Board, 
                 state: State[OnOff], *, exists: bool = True) -> None:
        BinaryComponent.__init__(self, board, state=state, live=exists)
        LocatedPad.__init__(self, loc)
        DropLoc.__init__(self)
        self.exists = exists
        # self.broken = False
        self._pads = board.pad_array
        self._dried_liquid = None
        def journal_change(old: OnOff, new: OnOff) -> None:
            if old is not new:
                board.journal_state_change(self, new)
        self.on_state_change(journal_change, key=f"Journal Change {self}")

        
    def __repr__(self) -> str:
        return f"Pad({self.column},{self.row})"
        
    def neighbor(self, d: Dir) -> Optional[Pad]:
        n = self.board.orientation.neighbor(d, self.location)
        p = self._pads.get(n, None)
        if p is None or not p.exists:
            return None
        return p
    
    @property
    def empty(self) -> bool:
        return self.drop is None
    
    @property
    def safe(self) -> bool:
        w = self.well
        if w is not None and (w.gate_on or w.gate_reserved):
            return False
        return self.empty and all(map(lambda n : n.empty and not n.reserved, self.all_neighbors))
    
    def safe_except(self, padOrWell: Union[Pad, Well]) -> bool:
        if not self.empty:
            return False
        w = self.well
        if w is not None and w is not padOrWell and (w.gate_on or w.gate_reserved):
            return False
        for p in self.all_neighbors:
            if p is not padOrWell and (not p.empty or p.reserved):
                return False
        return True
    
    def reserve(self) -> bool:
        if self.reserved:
            return False
        self.reserved = True
        return True
    
        
    def liquid_added(self, liquid: Liquid, *, mix_result: Optional[MixResult] = None) -> None:
        # I'm treating adding and removing liquid as synchronous
        journal = ChangeJournal()
        journal.note_delivery(self, liquid, mix_result=mix_result)
        journal.process_changes()
        # self.board.change_journal.note_delivery(self, liquid, mix_result=mix_result)

    def liquid_removed(self, volume: Volume) -> None:
        # I'm treating adding and removing liquid as synchronous
        journal = ChangeJournal()
        journal.note_removal(self, volume)
        journal.process_changes()
        # self.board.change_journal.note_removal(self, volume)
        
    def deliver(self, liquid: Liquid, *, 
                journal: Optional[ChangeJournal] = None,
                mix_result: Optional[MixResult] = None) -> None:
        if journal is None:
            journal = self.board.change_journal
        journal.note_delivery(self, liquid, mix_result = mix_result)
    
    def remove(self, volume: Volume, *, journal: Optional[ChangeJournal] = None) -> None:
        if journal is None:
            journal = self.board.change_journal
        journal.note_removal(self, volume)
        
    def compute_neighbors_for_blob(self)->Sequence[DropLoc]:
        if (well := self.well) is None:
            return self.neighbors
        else:
            return [*self.neighbors, well.gate]
        
    
# WellPadLoc = Union[tuple['WellGroup', int], 'Well']

class WellPad(BinaryComponent['WellPad'], DropLoc):
    well: Well
    index: int
    _neighbor_indices: Final[Sequence[int]]
    _neighbors: Optional[Sequence[DropLoc]] = None
    
    @property
    def is_gate(self) -> bool:
        return False
    
    @property
    def has_fluid(self) -> bool:
        return self.current_state is OnOff.ON
    
        
    def __init__(self, board: Board, 
                 state: State[OnOff], *, 
                 live: bool = True,
                 neighbors: Sequence[int]) -> None:
        BinaryComponent.__init__(self, board, state=state, live=live)
        DropLoc.__init__(self)
        self._neighbor_indices = neighbors
        # print(f"{self}.live = {self.live}")
        def journal_change(old: OnOff, new: OnOff) -> None:
            if old is not new:
                board.journal_state_change(self, new)
        self.on_state_change(journal_change, key=f"Journal Change {self}")
        
        
    def __repr__(self) -> str:
        well: Optional[Well] = getattr(self, 'well', None)
        if well is None:
            return f"WellPad(unassigned, {id(self)})"
        elif self.is_gate:
            return f"WellPad({well}[gate])"
        else:
            return f"WellPad({well}[{self.index}]"
            
    def set_location(self, well: Well, index: int) -> None:
        self.well = well
        self.index = index

    def compute_neighbors_for_blob(self)->Sequence[DropLoc]:
        ns = self._neighbors
        if ns is None:
            well = self.well
            ns = tuple(well.gate if n==-1 else well.shared_pads[n] for n in self._neighbor_indices)
            self._neighbors = ns
        return ns
        
class WellGate(WellPad, LocatedPad):
    @property
    def is_gate(self) -> bool:
        return True
    
    def __init__(self, board: Board,
                 exit_pad: Pad,
                 exit_dir: Dir,
                 state: State[OnOff], *,
                 neighbors: tuple[int, ...],
                 live: bool = True) -> None:
        WellPad.__init__(self, board, state, live=live, neighbors=neighbors)
        loc = board.orientation.neighbor(exit_dir.opposite, exit_pad.location)
        LocatedPad.__init__(self, loc)
        
    def __repr__(self) -> str:
        well: Optional[Well] = getattr(self, 'well', None)
        if well is None:
            return f"WellGate(unassigned, {id(self)})"
        else:
            return f"WellGate({well})"
        

    def compute_neighbors_for_blob(self)->Sequence[DropLoc]:
        ns = self._neighbors
        if ns is None:
            ns = (self.well.exit_pad, *super().compute_neighbors_for_blob())
            self._neighbors = ns
        return ns
    
    def deliver(self, liquid: Liquid, *, 
                journal: Optional[ChangeJournal] = None,
                mix_result: Optional[MixResult] = None) -> None:
        if journal is None:
            journal = self.board.change_journal
        journal.note_delivery(self, liquid, mix_result = mix_result)
    
    def remove(self, volume: Volume, *, journal: Optional[ChangeJournal] = None) -> None:
        if journal is None:
            journal = self.board.change_journal
        journal.note_removal(self, volume)
    
    

class WellState(Enum):
    EXTRACTABLE = auto()
    READY = auto()
    DISPENSED = auto()
    ABSORBED = auto()
    
# -1 is the well's gate pad.  Others are indexes into the shared_pads list
WellOpStep = Sequence[int]
WellOpStepSeq = Sequence[WellOpStep]
WellOpSeqDict = Mapping[tuple[WellState,WellState], WellOpStepSeq]

class GateStatus(Enum):
    NOT_YET = auto()
    JUST_ON = auto()
    UNSAFE = auto()

class WellMotion:
    group: Final[DispenseGroup]
    board: Final[Board]
    target: Final[WellState]
    initial_future: Final[Delayed[Well]]
    futures: Final[list[tuple[Well, Delayed[Well]]]]
    # post_result: Final[bool]
    well_gates: Final[set[WellGate]]
    shared_pads: Final[Sequence[WellPad]]
    guard: Final[Optional[Iterator[bool]]]
    # next_step: int
    turned_gates_on: bool = False
    turned_gates_off: bool = False
    # on_last_step: bool = False
    one_tick: Final[Ticks] = 1*tick
    # sequence: WellOpStepSeq
    gate_status: GateStatus
    
    def __init__(self, well: Well, target: WellState, *,
                 guard: Optional[Iterator[bool]] = None,
                 post_result: bool = True) -> None:
        self.group = well.group
        self.board = well.board
        self.initial_future = Delayed[Well]()
        self.futures = [(well, self.initial_future)] if post_result else []
        self.target = target
        # self.post_result = post_result
        self.well_gates = { well.gate }
        self.shared_pads = well.shared_pads
        self.guard = guard
        # self.next_step = 0
        self.gate_status = GateStatus.NOT_YET
        
    def try_adopt(self, other: WellMotion) -> bool:
        # This is called from other.do_step(), with the group locked.
        if self.target is not other.target or self.gate_status is GateStatus.UNSAFE:
            return False
        # The other one wants to go to the same place we are, and either we haven't turned 
        # any gates on yet or we just did in this tick.
        
        # If we're dispensing and we already have any of that motion's gates in our set,
        # it'll have to wait until we're done with this one.
        if self.target is WellState.DISPENSED and (self.well_gates & other.well_gates):
            return False
        
        # print(f"Piggybacking")
        self.well_gates.update(other.well_gates)
        # we don't have to add the shared pads.  Changing the ones we have will suffice.
        if self.gate_status is GateStatus.JUST_ON:
            for gate in other.well_gates:
                gate.schedule(WellPad.TurnOn, post_result = False)

        self.futures.extend(other.futures)             
        return True
    
    def post_futures(self) -> None:
        for w,f in self.futures:
            f.post(w)
        
    # Returns True if it should keep going
    def iterator(self) -> Iterator[bool]:
        target = self.target
        # On the first step, we need to see if this is really necessary or if we 
        # can piggyback onto another motion (or just return) 
        
        # print(f"New motion to {self.target}, gates = {self.well_gates}: {self}")
        group = self.group
        
        def with_lock() -> Optional[bool]:
            with group.lock:
                current = group.motion
                if current is not None:
                    # print(f"There already is a motion going to {current.target} (gate_status = {current.gate_status}): {current}")
                    if current.try_adopt(self):
                        # If we can piggyback, we do.
                        return False
                    else:
                        # Otherwise, we'll try again next time.  (I was going to reschedule 
                        # when the current one was done, but it's almost certainly cheaper to
                        # just check each tick.
                        # print(f"Deferring")
                        return True
                # print(f"We're the first")
                if group.state is target:
                    # There's no motion, and we're already where we want to be.
                    # If this is EXTRACTABLE or READY, we're fine, otherwise, we got here
                    # without using our gates, so we need to go through READY again
                    if target is WellState.READY or target is WellState.EXTRACTABLE:
                        self.post_futures()
                        # print(f"Already at {target}")
                        return False
                # if group.state is WellState.READY or target is WellState.READY:
                #     self.sequence = group.sequences[(group.state, target)]
                # else:
                #     self.sequence = list(group.sequences[(group.state, WellState.READY)])
                #     self.sequence += group.sequences[(WellState.READY, target)]
                # # print(f"Switching from {group.state} to {target}: {self.sequence}")
                # assert len(self.sequence) > 0
                group.motion = self            
                return None

        # Even before we try to be adopted, if we're trying to dispense, we need to reserve the exit pad 
        # (which means we won't have to later) and refill the well, if necessary.  If we're trying to absorb,
        # we wait until there's a drop there.  This is encapsulated in the object's guard
        
        guard = self.guard
        if guard is not None:
            while (next(guard)):
                yield True
                
        # This needs to be done as a separate call, because we need to release 
        # the lock each time.

        # last_yield: Optional[bool] = None
        while (val := with_lock()) is not None:
            # print(f"Yielding {val}")
            # last_yield = val
            yield val
            
        # print(f"After loop ({val})")
        # assert last_yield != False
            
        shared_pads = self.shared_pads
        # turned_gates_on = self.turned_gates_on
        # turned_gates_off = self.turned_gates_off
        for on_last_step, step in group.transition_func(group.state, target):
            # We squirrel it away so that it can be used in try_adopt()
            # self.on_last_step = on_last_step
            states = list(itertools.repeat(OnOff.OFF, len(shared_pads)))
            gate_state = OnOff.OFF
            for pad_index in step:
                if pad_index == -1:
                    gate_state = OnOff.ON
                    # If we're turning the gates on to dispense, we need to make sure that the 
                    # corresponding exit pads aren't occupied (or we'll slurp the drop back).  
                    # If any are, we just return and try again next time.
                    if target is WellState.DISPENSED:
                        for g in self.well_gates:
                            assert(g.index == -1)
                            w = g.well
                            assert isinstance(w, Well)
                            while not w.exit_pad.empty:
                                yield True
                else:
                    states[pad_index] = OnOff.ON

            gs = self.gate_status
            
            if gs is GateStatus.JUST_ON and gate_state is OnOff.OFF:
                self.gate_status = GateStatus.UNSAFE
                # If we're dispensing, and we've turned the gate on and we're about
                # to turn it off for the first time, we need to make sure that the
                # exit pads are safe and reserved.
                if target is WellState.DISPENSED:
                    for g in self.well_gates:
                        well = g.well
                        pad = well.exit_pad
                        # The pad should already be reserved.
                        assert pad.reserved
                        # while not pad.safe_except(well):
                        #     yield True
                        # while not pad.reserve():
                        #     yield True
                        pad.schedule(Pad.TurnOn, post_result=False)
            elif gs is GateStatus.NOT_YET and gate_state is OnOff.ON:
                self.gate_status = GateStatus.JUST_ON
                # If we're abosrbing, and we're about to turn on the gate for the
                # first time, we need to turn off any pads in the blob at the exit pad
                if target is WellState.ABSORBED:
                    for g in self.well_gates:
                        well = g.well
                        pad = well.exit_pad
                        pads: Sequence[DropLoc] = (pad,)
                        if (blob := pad.blob) is not None:
                            pads = blob.pads
                        for p in pads:
                            assert isinstance(p, Pad)
                            p.schedule(Pad.TurnOff, post_result=False)
            for (i, shared) in enumerate(shared_pads):
                shared.schedule(WellPad.SetState(states[i]), post_result=False)
            for gate in self.well_gates:
                gate.schedule(WellPad.SetState(gate_state), post_result=False)
            # gs = self.gate_status
            # if gate_state is OnOff.ON and gs is GateStatus.NOT_YET:
            #     self.gate_status = GateStatus.JUST_ON
            # elif gs is GateStatus.JUST_ON and gate_state is OnOff.OFF:
            #     self.gate_status = GateStatus.UNSAFE
            #

            if not on_last_step:
                # We do the next step the next time around
                yield True
        # And on the other side, we clean up
        def cb() -> None:
            # # Any gates we turned on, we turn off at the next tick
            # for gate in self.well_gates:
            #     gate.schedule(WellPad.TurnOff, post_result=False)
            with group.lock:
                group.motion = None
                group.state = self.target
                self.post_futures()
        self.board.after_tick(cb)
        yield False

            
                    
    
class WellGroupDead(BoardComponent, OpScheduler['WellGroupDead']):
    name: Final[str]
    shared_states: Final[Sequence[State[OnOff]]]
    wells: list[Well]
    sequences: Final[WellOpSeqDict]
    
    lock: Final[Lock]
    
    state: WellState
    motion: Optional[WellMotion]
    
    
    def __init__(self, name: str, 
                 board: Board,
                 states: Sequence[State[OnOff]],
                 sequences: WellOpSeqDict) -> None:
        BoardComponent.__init__(self, board)
        self.name = name
        self.shared_states = states
        self.sequences = sequences
        self.wells = []
        
        self.state = WellState.EXTRACTABLE
        self.motion = None
        self.lock = Lock()
        
    def __repr__(self) -> str:
        return f"WellGroup[{self.name}]"
        
    def add_well(self, well: Well) -> None:
        self.wells.append(well)
        
    
PadBounds = Sequence[tuple[float,float]]

class WellShape:
    gate_pad_bounds: Final[PadBounds]
    shared_pad_bounds: Final[Sequence[Union[PadBounds, Sequence[PadBounds]]]]
    reagent_id_circle_center: tuple[float,float]
    reagent_id_circle_radius: float
    
    def __init__(self, *, 
                 gate_pad_bounds: PadBounds,
                 shared_pad_bounds: Sequence[Union[PadBounds, Sequence[PadBounds]]],
                 reagent_id_circle_center: tuple[float, float],
                 reagent_id_circle_radius: float = 1):
        self.gate_pad_bounds = gate_pad_bounds
        self.shared_pad_bounds = shared_pad_bounds
        self.reagent_id_circle_center = reagent_id_circle_center
        self.reagent_id_circle_radius = reagent_id_circle_radius
        
WellVolumeSpec = Union[Volume, Callable[[], Volume]]

TransitionStep = tuple[bool,WellOpStep]
TransitionFunc = Callable[[WellState,WellState], Iterator[TransitionStep]]

def transitions_from(sd: WellOpSeqDict) -> TransitionFunc:
    def fn(start: WellState, end: WellState) -> Iterator[TransitionStep]:
        ready = WellState.READY
        if start is ready or end is ready:
            seq = sd[(start, end)]
        else:
            seq = [*sd[(start, ready)], *sd[(ready, end)]]
        last = len(seq)-1
        return ((i==last, s) for i,s in enumerate(seq))
    return fn
        

class DispenseGroup:
    key: Final[Any]
    lock: Final[Lock]
    motion: Optional[WellMotion]
    state: WellState
    
    def __init__(self, key: Any, transition_func: TransitionFunc) -> None:
        self.key = key
        self.transition_func: Final[TransitionFunc] = transition_func
        self.lock = Lock()
        self.motion = None
        self.state = WellState.EXTRACTABLE
        
    def __repr__(self) -> str:
        if isinstance(self.key, Well):
            return str(self.key)
        return f"DispenseGroup({self.key})"
    
    
class Well(OpScheduler['Well'], BoardComponent, PipettingTarget):
    number: Final[int]
    group: Final[DispenseGroup]
    capacity: Final[Volume]
    dispensed_volume: Final[Volume]
    is_voidable: Final[bool]
    exit_pad: Final[Pad]
    shared_pads: Final[Sequence[WellPad]]
    gate: Final[WellGate]
    exit_dir: Final[Dir]
    gate_reserved: bool = False
    _contents: Optional[Liquid]
    _shape: Final[Optional[WellShape]]
    
    required: Optional[Volume] = None
    
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
            return Volume.ZERO
        else:
            return c.volume
        
    @property
    def reagent(self) -> Reagent:
        c = self._contents
        if c is None:
            return unknown_reagent
        else:
            return c.reagent

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
    
    @property
    def gate_on(self) -> bool:
        return self.gate.current_state is OnOff.ON
    
    # refill if dispensing would take you to this level
    _min_fill: Optional[WellVolumeSpec] = None
    
    @property
    def min_fill(self) -> Volume:
        return self.volume_from_spec(self._min_fill, lambda: Volume.ZERO)
    
    @min_fill.setter
    def min_fill(self, volume: Optional[WellVolumeSpec]) -> None:
        self._min_fill = volume
        
    # The compute_V() functions are there because currently, MyPy will complain if you try to
    # assign a value of a type that doesn't match the *getter*. (MyPy issue #3004.  They agree 
    # that it should be fixed, but it still isn't as of 8/2/21.)
    
    def compute_min_fill(self, volume: Optional[WellVolumeSpec]) -> None:
        self._min_fill = volume
    
    # empty if absorbing would take you above this level
    _max_fill: Optional[WellVolumeSpec] = None

    @property
    def max_fill(self) -> Volume:
        return self.volume_from_spec(self._max_fill, lambda: self.capacity)
    
    @max_fill.setter
    def max_fill(self, volume: Optional[WellVolumeSpec]) -> None:
        self._max_fill = volume

    def compute_max_fill(self, volume: Optional[WellVolumeSpec]) -> None:
        self._max_fill = volume
    
    # when refilling, fill to this level
    _fill_to: Optional[WellVolumeSpec] = None
    

    @property
    def fill_to(self) -> Volume:
        def default_fill_line() -> Volume:
            if self.required is None:
                return self.capacity
            return min(self.capacity, self.required)
        return self.volume_from_spec(self._fill_to, default_fill_line)
    
    @fill_to.setter
    def fill_to(self, volume: Optional[WellVolumeSpec]) -> None:
        self._fill_to = volume

    def compute_fill_to(self, volume: Optional[WellVolumeSpec]) -> None:
        self._fill_to = volume
        
        
    # when emptying, empty to this level
    _empty_to: Optional[WellVolumeSpec] = None
    
    @property
    def empty_to(self) -> Volume:
        return self.volume_from_spec(self._empty_to, lambda: Volume.ZERO)
    
    @empty_to.setter
    def empty_to(self, volume: Optional[WellVolumeSpec]) -> None:
        self._empty_to = volume
    
    def compute_empty_to(self, volume: Optional[WellVolumeSpec]) -> None:
        self._empty_to = volume
    
    def __init__(self, *,
                 board: Board,
                 number: int,
                 group: Union[DispenseGroup, TransitionFunc],
                 exit_pad: Pad,
                 gate: WellGate,
                 shared_pads: Sequence[WellPad],
                 capacity: Volume,
                 dispensed_volume: Volume,
                 exit_dir: Dir,
                 is_voidable: bool = False,
                 shape: Optional[WellShape] = None,
                 ) -> None:
        BoardComponent.__init__(self, board)
        self.number = number
        if not isinstance(group, DispenseGroup):
            group = DispenseGroup(self, group)
        self.group = group
        self.exit_pad = exit_pad
        self.gate = gate
        self.shared_pads = shared_pads
        self.capacity = capacity
        self.dispensed_volume = dispensed_volume
        self.exit_dir = exit_dir
        self.is_voidable = is_voidable
        self._contents = None
        self._shape = shape
        self._liquid_change_callbacks = ChangeCallbackList()
        

        assert exit_pad._well is None, f"{exit_pad} is already associated with {exit_pad.well}"
        exit_pad._well = self
        gate.set_location(self, -1)
        for i,wp in enumerate(shared_pads):
            wp.set_location(self, i)
        
    def prepare_for_add(self) -> None: 
        pass

    def prepare_for_remove(self) -> None: 
        pass
    
    def pipettor_added(self, reagent: Reagent, volume: Volume, *,
                       mix_result: Optional[MixResult],
                       last: bool) -> None:
        got = Liquid(reagent, volume)
        self.transfer_in(got, mix_result=mix_result)
    
    def pipettor_removed(self, reagent: Reagent, volume: Volume, *,
                         last: bool) -> None: # @UnusedVariable
        self.transfer_out(volume)
    
        
    def volume_from_spec(self, spec: Optional[WellVolumeSpec], default_fn: Callable[[], Volume]) -> Volume:
        if spec is None:
            return default_fn()
        if isinstance(spec, Volume):
            return spec
        return spec()
        
    def __repr__(self) -> str:
        return f"Well[{self.number} <> {self.exit_pad}]"
    
    def _can_accept(self, reagent: Reagent) -> bool:
        if self.available: return True
        my_r = self.reagent
        return (my_r == reagent
                or my_r == unknown_reagent 
                or reagent == unknown_reagent
                or my_r == waste_reagent) 
        
    def _can_provide(self, reagent: Reagent) -> bool:
        # If we're empty, there's no mismatch, but ensure_conent() will refil.  Otherwise, we can
        # do it if we don't know or care what we want or we don't know what we have  
        if self.available: return True
        my_r = self.reagent
        return (my_r == reagent
                or my_r == unknown_reagent 
                or reagent == unknown_reagent
                or reagent == waste_reagent) 
        
    def transfer_in(self, liquid: Liquid, *,
                    volume: Optional[Volume] = None, 
                    on_overflow: ErrorHandler = PRINT,
                    on_reagent_mismatch: ErrorHandler = PRINT,
                    mix_result: Optional[MixResult] = None) -> None:
        if volume is None:
            volume = liquid.volume
        on_overflow.expect_true(self.remaining_capacity >= volume,
                    lambda : f"Tried to add {volume} to {self}.  Remaining capacity only {self.remaining_capacity}")
        # available implies _contents is not None, but MyPy can't do the inference for the else
        # clause if I don't check it here.
        if self._contents is None or self.available:
            self.contents = Liquid(liquid.reagent, Volume.ZERO)
        else:
            r = self._contents.reagent
            on_reagent_mismatch.expect_true(self._can_accept(liquid.reagent),
                                            lambda : f"Adding {liquid.reagent} to {self} containing {r}")
        assert self._contents is not None
        self._contents.mix_in(liquid, result=mix_result)
        self._liquid_change_callbacks.process(self._contents, self._contents)
        # print(f"{self} now contains {self.contents}")
            
    def transfer_out(self, volume: Volume, *,
                     on_empty: ErrorHandler = PRINT) -> Liquid:
        on_empty.expect_true(self.volume>= 0.99*volume,
                    lambda : f"Tried to draw {volume} from {self}, which only has {self.volume}")
        v = min(self.volume, volume)
        reagent: Reagent
        if self._contents is None:
            reagent = unknown_reagent
        else:
            reagent = self._contents.reagent
            # print(f"Removing {v} from {self._contents}")
            self._contents -= v
        if self.required is not None:
            if self.required <= v:
                self.required = None
            else:
                self.required -= v
        self._liquid_change_callbacks.process(self._contents, self._contents)
        # print(f"{self} now contains {self.contents}")
        return Liquid(reagent, v)

    def contains(self, content: Union[Liquid, Reagent],
                 *, on_overflow: ErrorHandler = PRINT) -> None:
        if isinstance(content, Reagent):
            liquid = Liquid(content, Volume.ZERO)
        else:
            liquid = content
        on_overflow.expect_true(liquid.volume <= self.capacity,
                                lambda : f"Asserted {self} contains {liquid}. Capacity only {self.capacity}")
        self._contents = None
        self.transfer_in(liquid, volume=min(liquid.volume, self.capacity))
        # print(f"Volume is now {self.volume}")
        
    def reserve_gate(self) -> bool:
        if self.gate_reserved:
            return False
        self.gate_reserved = True
        return True
    
    def add(self, liquid: Liquid, *,
            mix_result: Optional[MixResult] = None,
            on_insufficient: ErrorHandler = PRINT,
            on_no_source: ErrorHandler = PRINT
            ) -> Delayed[Well]:
        pipettor = self.pipettor
        assert pipettor is not None, f"{self} has no pipettor and add() was not overridden"
        
        p_future = pipettor.schedule(pipettor.Supply(liquid, self,
                                                     mix_result=mix_result,
                                                     on_insufficient=on_insufficient,
                                                     on_no_source=on_no_source))
        return p_future.triggering(value=self)
    
    def remove(self, volume: Volume, *,
               on_no_sink: ErrorHandler = PRINT
               ) -> Delayed[Well]:
        pipettor = self.pipettor
        assert pipettor is not None, f"{self} has no pipettor and remove() was not overridden"
        
        p_future = pipettor.schedule(pipettor.Extract(volume, self,
                                                      on_no_sink=on_no_sink))
        return p_future.triggering(value=self)
    
    def refill(self, *, reagent: Optional[Reagent] = None) -> Delayed[Well]:
        volume = self.fill_to - self.volume
        # print(f"Fill line is {self.fill_to}.  Adding {volume}.")
        assert volume > Volume.ZERO, f"refill(volume={volume}) called on {self}"
        if reagent is None:
            reagent = self.reagent
        return self.add(Liquid(reagent, volume))
    
    def empty_well(self) -> Delayed[Well]:
        volume = self.volume - self.empty_to
        assert volume > Volume.ZERO, f"empty_well(volume={volume}) called on {self}"
        return self.remove(volume)
    

    def ensure_content(self, 
                       volume: Optional[Volume] = None,
                       reagent: Optional[Reagent] = None,
                       *, on_reagent_mismatch: ErrorHandler = PRINT
                       # slop
                       ) -> Delayed[Well]:
        if volume is None:
            volume = self.dispensed_volume
        if reagent is not None:
            on_reagent_mismatch.expect_true(self._can_provide(reagent),
                                            lambda : f"{self} contains {self.reagent}.  Expected {reagent}")
        current_volume = self.volume
        resulting_volume = current_volume - volume
        if resulting_volume >= self.min_fill or resulting_volume.is_close_to(self.min_fill, 
                                                                             abs_tol=0.05*self.dispensed_volume):
            return Delayed.complete(self)
        # print(f"Require {volume} of {reagent}.  Only have {current_volume}.  Refilling")
        return self.refill(reagent=reagent)
    
    def ensure_space(self, 
                     volume: Volume,
                     reagent: Optional[Reagent] = None,
                     *, on_reagent_mismatch: ErrorHandler = PRINT
                     ) -> Delayed[Well]:
        if reagent is not None:
            on_reagent_mismatch.expect_true(self._can_provide(reagent),
                                            lambda : f"{self} contains {self.reagent}.  Expected {reagent}")
        current_volume = self.volume
        resulting_volume = current_volume + volume
        if resulting_volume <= self.max_fill or resulting_volume.is_close_to(self.max_fill, 
                                                                             abs_tol=0.05*self.dispensed_volume):
            # print(f"{resulting_volume:g} <= {self.max_fill:g}")
            return Delayed.complete(self)
        # print(f"Need to empty well ({resulting_volume:g} > {self.max_fill:g}")
        return self.empty_well()
    

                    
    def on_liquid_change(self, cb: ChangeCallback[Optional[Liquid]], *, key: Optional[Hashable] = None) -> None:
        self._liquid_change_callbacks.add(cb, key=key)
        
        
    class TransitionTo(Operation['Well','Well']):
        target: Final[WellState]
        guard: Final[Optional[Iterator[bool]]]
        
        def __init__(self, target: WellState, *,
                     guard: Optional[Iterator[bool]] = None
                     ) -> None:
            self.target = target
            self.guard = guard
            
        def _schedule_for(self, well: Well, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,
                          )-> Delayed[Well]:
            board = well.board
            motion = WellMotion(well, self.target, post_result=post_result, guard=self.guard)
            # target = self.target
            # assert target is WellState.DISPENSED or target is WellState.ABSORBED, \
                # f"Well provided on transition to {target}"
            # if target is WellState.DISPENSED:
            #     motion.pad_states[well.exit_pad] = OnOff.ON
            # motion.pad_states[well.exit_pad] = OnOff.ON if target is WellState.DISPENSED else OnOff.OFF
            
            def before_tick() -> Iterator[Optional[Ticks]]:
                iterator = motion.iterator()
                one_tick = 1*tick
                while next(iterator):
                    yield one_tick
                yield None
            iterator = before_tick()
            board.before_tick(lambda: next(iterator), delta=mode.gated_delay(after))
            return motion.initial_future

class Magnet(BinaryComponent['Magnet']): 
    pads: Final[Sequence[Pad]]
    
    def __init__(self, board: Board, *, state: State[OnOff], pads: Sequence[Pad]) -> None:
        BinaryComponent.__init__(self, board, state=state)
        self.pads = pads
        for pad in pads:
            pad._magnet = self
            
    def __repr__(self) -> str:
        return f"Magnet({', '.join(str(self.pads))})"
    
class HeatingMode(Enum):
    OFF = auto()
    MAINTAINING = auto()
    HEATING = auto()
    COOLING = auto()
    
    
class Heater(OpScheduler['Heater'], BoardComponent):
    num: Final[int]
    pads: Final[Sequence[Pad]]
    mode: HeatingMode
    _last_reading: Optional[TemperaturePoint]
    _target: Optional[TemperaturePoint]
    polling_interval: Final[Time]
    _temperature_change_callbacks: Final[ChangeCallbackList[Optional[TemperaturePoint]]]
    _target_change_callbacks: Final[ChangeCallbackList[Optional[TemperaturePoint]]]
    _lock: Final[Lock]
    _current_op_key: Any
    _polling: bool = False
    
    
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
        self.mode = HeatingMode.OFF
        self.polling_interval = polling_interval
        self._last_reading = None
        self._target = None
        self._temperature_change_callbacks = ChangeCallbackList()
        self._target_change_callbacks = ChangeCallbackList()
        self._lock = Lock()
        self._current_op_key = None
        for pad in pads:
            pad._heater = self
            
    def start_polling(self) -> None:
        if self._polling:
            return
        self._polling = True
        def do_poll() -> Optional[Time]:
            self.poll()
            return self.polling_interval if self._polling else None
        self.board.call_after(Time.ZERO, do_poll, daemon=True)
        
    def stop_polling(self) -> None:
        self._polling = False
            
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
        
    class SetTemperature(Operation['Heater','Heater']):
        target: Final[Optional[TemperaturePoint]]
        
        def _schedule_for(self, heater: Heater, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,
                          ) -> Delayed[Heater]:
            future = Delayed[Heater]()
            target = self.target
            
            def do_it() -> None:
                ambient_threshold = 80*abs_F
                with heater._lock:
                    if heater._current_op_key is not None:
                        heater._temperature_change_callbacks.remove(heater._current_op_key)
                    heater.target = target
                    temp = heater.current_temperature
                    
                    mode: HeatingMode
                    if temp is None:
                        mode = HeatingMode.OFF if target is None else HeatingMode.HEATING
                        if post_result:
                            future.post(heater)
                        return
                    elif temp == target:
                        mode = HeatingMode.MAINTAINING
                        if post_result:
                            future.post(heater)
                        return
                    elif target is None and temp < ambient_threshold:
                        mode = HeatingMode.OFF
                        if post_result:
                            future.post(heater)
                        return
                    elif target is None or temp > target:
                        mode = HeatingMode.COOLING
                    else:
                        mode = HeatingMode.HEATING
                    heater.mode = mode
                    key = (heater, f"Temp->{target}", random.random())
                    
                    user_op = heater.user_operation()
                    
                    user_op.__enter__()
                
                    def check(old: Optional[TemperaturePoint], new: Optional[TemperaturePoint]):  # @UnusedVariable
                        assert mode is HeatingMode.HEATING or mode is HeatingMode.COOLING
                        if new is None:
                            # Not much we can do if we don't get a reading
                            return
                        if mode is HeatingMode.HEATING:
                            assert target is not None
                            done = new >= target
                        elif target is None:
                            done = new < ambient_threshold
                        else:
                            done = new <= target
                        
                        if done:
                            with heater._lock:
                                user_op.__exit__(None, None, None)
                                heater.mode = HeatingMode.OFF if target is None else HeatingMode.MAINTAINING
                                heater._temperature_change_callbacks.remove(key)
                            if post_result:
                                future.post(heater)
                    heater.on_temperature_change(check, key=key)
            heater.board.schedule(do_it, mode, after=after)
            return future
            
        
        def __init__(self, target: Optional[TemperaturePoint]) -> None:
            self.target = target
            
class ProductLocation(NamedTuple):
    reagent: Reagent
    location: Any
    
class ExtractionPoint(OpScheduler['ExtractionPoint'], BoardComponent, PipettingTarget):
    pad: Final[Pad]
    removed: Optional[Volume] = None
    
    @property
    def contents(self) -> Optional[Liquid]:
        drop = self.pad.drop
        if drop is None:
            return None
        return drop.blob.contents
    
    def __init__(self, pad: Pad) -> None:
        BoardComponent.__init__(self, pad.board)
        self.pad = pad
        pad._extraction_point = self
        
    def __repr__(self) -> str:
        return f"ExtractionPoint[{self.pad.location}]"
        
    def prepare_for_add(self) -> None:
        expect_drop = self.pad.drop is not None 
        self.reserve_pad(expect_drop=expect_drop).wait()
        self.pad.schedule(Pad.TurnOn).wait()
        
    def pipettor_added(self, reagent: Reagent, volume: Volume, *,
                       last: bool,
                       mix_result: Optional[MixResult]) -> None:
        if volume > Volume.ZERO:
            got = Liquid(reagent, volume)
            self.pad.liquid_added(got, mix_result=mix_result)
        if last:
            self.pad.reserved = False
    
    def prepare_for_remove(self) -> None:
        self.ensure_drop().wait()
        
    def pipettor_removed(self, reagent: Reagent, volume: Volume, # @UnusedVariable
                         *, last: bool) -> None: # @UnusedVariable
        pad = self.pad
        if volume > Volume.ZERO:
            pad.liquid_removed(volume)
        blob = not_None(pad.blob, desc=lambda: f"{self} has no blob after extraction")
        # If the blob is now empty, we turn off all of its pads.

        # TODO: Should this be a property of the operation that called this?
        if blob.total_volume.is_zero:
            for p in blob.pads:
                assert isinstance(p, Pad)
                # TODO: Do I need to wait on this somewhere?
                p.schedule(Pad.TurnOff, post_result=False)
            
        
        

    def transfer_out(self, *,
                     liquid: Optional[Liquid] = None,
                     on_no_sink: ErrorHandler = PRINT,
                     is_product: bool = True,
                     product_loc: Optional[Delayed[ProductLocation]] = None
                     ) -> Delayed[Liquid]:
        pipettor = self.pipettor
        assert pipettor is not None, f"{self} has no pipettor and transfer_out() not overridden"
        if liquid is None:
            drop = not_None(self.pad.drop)
            liquid = drop.blob.contents
        p_future = pipettor.schedule(pipettor.Extract(liquid.volume, self,
                                                      is_product = is_product,
                                                      product_loc = product_loc, 
                                                      on_no_sink = on_no_sink))
        return p_future
    
    def transfer_in_result(self) -> Drop:
        return not_None(self.pad.drop)

    def transfer_in(self, liquid: Liquid, *,                           
                     mix_result: Optional[Union[Reagent, str]]=None,   
                     on_insufficient: ErrorHandler=PRINT,              
                     on_no_source: ErrorHandler=PRINT                  
                     ) -> Delayed[Drop]:
        from mpam.drop import Drop # @Reimport
        pipettor = self.pipettor
        assert pipettor is not None, f"{self} has no pipettor and transfer_in() not overridden"
        p_future = pipettor.schedule(pipettor.Supply(liquid, self,
                                                     mix_result = mix_result,
                                                     on_insufficient = on_insufficient,
                                                     on_no_source = on_no_source))
        future = Delayed[Drop]()
        p_future.post_transformed_to(future, lambda _: not_None(self.transfer_in_result()))
        return future
       
    def reserve_pad(self, *, expect_drop: bool = False) -> Delayed[None]:
        pad = self.pad
        return pad.board.on_condition(lambda: expect_drop == (pad.drop is not None) 
                                                and pad.reserve(),
                                      lambda: None)
        
    def ensure_drop(self) -> Delayed[None]:
        pad = self.pad
        return pad.board.on_condition(lambda: pad.drop is not None, lambda: None)

    class TransferIn(Operation['ExtractionPoint', 'Drop']):
        reagent: Final[Reagent]
        volume: Final[Optional[Volume]]
        mix_result: Final[Optional[Union[Reagent, str]]]
        on_insufficient: Final[ErrorHandler]
        on_no_source: Final[ErrorHandler]
        
        def __init__(self, reagent: Reagent, volume: Optional[Volume] = None, *,
                     mix_result: Optional[Union[Reagent, str]] = None,
                     on_insufficient: ErrorHandler = PRINT,
                     on_no_source: ErrorHandler = PRINT
                     ) -> None:
            self.reagent = reagent
            self.volume = volume
            self.mix_result = mix_result
            self.on_insufficient = on_insufficient
            self.on_no_source = on_no_source
            
        def _schedule_for(self, extraction_point: ExtractionPoint, *,
                          mode: RunMode = RunMode.GATED, # @UnusedVariable
                          after: Optional[DelayType] = None,
                          post_result: bool = True, # @UnusedVariable
                          ) -> Delayed[Drop]:
            from mpam.drop import Drop # @Reimport
            liquid = Liquid(self.reagent, 
                            extraction_point.board.drop_size if self.volume is None else self.volume)
            future = Delayed[Drop]()
            def do_it() -> None:
                extraction_point.transfer_in(liquid,
                                             mix_result = self.mix_result,
                                             on_insufficient = self.on_insufficient,
                                             on_no_source = self.on_no_source
                                             ).post_to(future)

            extraction_point.delayed(do_it, after=after)
            return future

    class TransferOut(Operation['ExtractionPoint', 'Liquid']):
        volume: Final[Optional[Volume]]
        on_no_sink: Final[ErrorHandler]
        product_loc: Final[Optional[Delayed[ProductLocation]]]

        def __init__(self, volume: Optional[Volume] = None, *,
                     on_no_sink: ErrorHandler = PRINT,
                     product_loc: Optional[Delayed[ProductLocation]] = None
                     ) -> None:
            self.volume = volume
            self.on_no_sink = on_no_sink
            self.product_loc = product_loc

        def _schedule_for(self, extraction_point: ExtractionPoint, *,
                          mode: RunMode = RunMode.GATED, # @UnusedVariable
                          after: Optional[DelayType] = None,
                          post_result: bool = True, # @UnusedVariable
                          ) -> Delayed[Liquid]:
            future = Delayed[Liquid]()
            def finish(liquid: Liquid) -> None:
                future.post(liquid)
            def do_it() -> None:
                drop = not_None(extraction_point.pad.drop)
                liquid = Liquid(drop.reagent,
                                drop.blob_volume if self.volume is None else self.volume)
                extraction_point.transfer_out(liquid = liquid,
                                              on_no_sink = self.on_no_sink,
                                              product_loc = self.product_loc
                                             ).post_to(future)

            extraction_point.delayed(do_it, after=after)
            return future
        
    
class SystemComponent(ABC):
    system: Optional[System] = None
    _after_update: Final[list[Callback]]
    _monitor_callbacks: Final[list[Callback]]
    
    def __init__(self) -> None:
        self._after_update = []
        self._monitor_callbacks = []
        
    def join_system(self, system: System) -> None:
        self.system = system
        system.component_joined(self)
        
    def system_shutdown(self) -> None:
        pass
        
    def in_system(self) -> System:
        return not_None(self.system)

    @abstractmethod    
    def update_state(self) -> None:
        self.finish_update()
    
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
    
    def communicate(self, cb: Callable[[], Optional[Callback]], delta: Time=Time.ZERO):
        req = self.make_request(cb)
        sys = self.in_system()
        if delta > Time.ZERO:
            self.call_after(delta, lambda : sys.communicate(req))
        else:
            sys.communicate(req)
        
    def call_at(self, t: Timestamp, fn: TimerFunc, *, daemon: bool = False):
        self.in_system().call_at(t, fn, daemon=daemon)
        
    def call_after(self, delta: Time, fn: TimerFunc, *, daemon: bool = False):
        self.in_system().call_after(delta, fn, daemon=daemon)
        
    def before_tick(self, fn: ClockCallback, *, delta: Ticks = Ticks.ZERO) -> None:
        self.in_system().before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, *, delta: Ticks = Ticks.ZERO):
        self.in_system().after_tick(fn, delta=delta)
        

    def on_tick(self, cb: Callable[[], Optional[Callback]], *, delta: Ticks = Ticks.ZERO):
        req = self.make_request(cb)
        self.in_system().on_tick(req, delta=delta)
        
    def delayed(self, function: Callable[[], T], *,
                after: Optional[DelayType]) -> Delayed[T]:
        return self.in_system().delayed(function, after=after)
 
    def schedule(self, cb: Callable[[], Optional[Callback]], mode: RunMode, *, 
                 after: Optional[DelayType] = None) -> None:
        if mode.is_gated:
            self.on_tick(cb, delta=mode.gated_delay(after))
        else:
            self.communicate(cb, delta=mode.asynchronous_delay(after))
      
    def user_operation(self) -> UserOperation:
        return UserOperation(not_None(self.system).engine.idle_barrier)
    
    def on_condition(self, pred: Callable[[], bool],
                     val_fn: Callable[[], T]) -> Delayed[T]:
        if pred():
            return Delayed.complete(val_fn())
        future = Delayed[T]()
        one_tick = 1 * tick
        def keep_trying() -> Iterator[Optional[Ticks]]:
            while not pred():
                yield one_tick
            future.post(val_fn())
            yield None
            
        iterator = keep_trying()
        self.before_tick(lambda: next(iterator))
        return future
       
    # def schedule_before(self, cb: C):
    
    
class ChangeJournal:
    turned_on: Final[set[DropLoc]]
    turned_off: Final[set[DropLoc]]
    delivered: Final[dict[DropLoc, list[Liquid]]]
    removed: Final[dict[DropLoc, Volume]]
    mix_result: Final[dict[DropLoc, MixResult]]
    
    @property
    def has_transfer(self) -> bool:
        return bool(self.delivered) or bool(self.removed)
    
    def __init__(self) -> None:
        self.turned_on = set()
        self.turned_off = set()
        self.delivered = defaultdict(list)
        self.removed = defaultdict(lambda: Volume.ZERO)
        self.mix_result = {}
        
    def change_to(self, pad: DropLoc, new_state: OnOff) -> None:
        wrong,right = (self.turned_off,self.turned_on) if new_state else (self.turned_on, self.turned_off)
        if pad in wrong:
            wrong.remove(pad)
        else:
            right.add(pad)
            
    def note_removal(self, pad: DropLoc, volume: Volume) -> None:
        self.removed[pad] += volume
        
    def note_delivery(self, pad: DropLoc, liquid: Liquid, *, mix_result: Optional[MixResult] = None) -> None:
        self.delivered[pad].append(liquid)
        if mix_result:
            self.mix_result[pad] = mix_result
            
    def process_changes(self) -> None:
        from mpam.drop import Blob # @Reimport
        Blob.process_changes(self)
            

class Board(SystemComponent):
    pads: Final[PadArray]
    wells: Final[Sequence[Well]]
    magnets: Final[Sequence[Magnet]]
    heaters: Final[Sequence[Heater]]
    extraction_points: Final[Sequence[ExtractionPoint]]
    # _well_groups: Mapping[str, WellGroup]
    orientation: Final[Orientation]
    drop_motion_time: Final[Time]
    _drop_size: Volume
    _reserved_well_gates: list[Well]
    _lock: Final[Lock]
    _drop_unit: Unit[Volume]
    # _drops: Final[list[Drop]]
    # _to_appear: Final[list[tuple[Pad, Liquid]]]
    _change_journal: ChangeJournal
    trace_blobs: ClassVar[bool] = False
    
    
    @property
    def change_journal(self) -> ChangeJournal:
        with self._lock:
            return self._change_journal
    
    def __init__(self, *, 
                 pads: PadArray,
                 wells: Sequence[Well],
                 magnets: Optional[Sequence[Magnet]] = None,
                 heaters: Optional[Sequence[Heater]] = None,
                 extraction_points: Optional[Sequence[ExtractionPoint]] = None,
                 orientation: Orientation,
                 drop_motion_time: Time) -> None:
        super().__init__()
        self._change_journal = ChangeJournal()
        self.pads = pads
        self.wells = wells
        self.magnets = [] if magnets is None else magnets
        self.heaters = [] if heaters is None else heaters
        self.extraction_points = [] if extraction_points is None else extraction_points
        self.orientation = orientation
        self.drop_motion_time = drop_motion_time
        self._lock = Lock()
        self._reserved_well_gates = []
        # self._drops = []
        # self._to_appear = []
        
    def replace_change_journal(self) -> ChangeJournal:
        with self._lock:
            old = self._change_journal
            self._change_journal = ChangeJournal()
            return old

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
    
    # @property
    # def well_groups(self) -> Mapping[str, WellGroup]:
    #     cache: Optional[Mapping[str, WellGroup]] = getattr(self, '_well_groups', None)
    #     if cache is None:
    #         cache = {well.group.name: well.group for well in self.wells}
    #         self._well_groups = cache
    #     return cache
    
    @property
    def drop_size(self) -> Volume:
        cache: Optional[Volume] = getattr(self, '_drop_size', None)
        if cache is None:
            cache = self.wells[0].dispensed_volume
            assert all(w.dispensed_volume==cache for w in self.wells), "Not all wells dispense the same volume"
            self._drop_size = cache
        return cache
    
    @property
    def drop_unit(self) -> Unit[Volume]:
        cache: Optional[Unit[Volume]] = getattr(self, '_drop_unit', None)
        if cache is None:
            cache = self.drop_size.as_unit("drops", singular="drop")
            self._drop_unit = cache
        return cache
    
    def finish_update(self) -> None:
        self.infer_drop_motion()
        super().finish_update()
        
    def join_system(self, system: System)->None:
        super().join_system(system)
        for h in self.heaters:
            h.start_polling()
    

    def print_blobs(self):
        from mpam.drop import Blob # @Reimport
        print("--------------")
        print("Blobs on board")
        print("--------------")
        blobs = set[Blob]()
        
        def check_pads(pads: Iterable[DropLoc]) -> None:
            nonlocal blobs
            for pad in pads:
                if pad is not None and pad.blob is not None:
                    if not pad in pad.blob.pads:
                        print(f"{pad} not in {pad.blob}")
                    blobs.add(pad.blob)
                    
        check_pads(self.pads.values())
        for well in self.wells:
            check_pads(well.shared_pads)
            check_pads((well.gate,))
        
        for blob in blobs:
            print(blob)

    def infer_drop_motion(self) -> None:
        self.replace_change_journal().process_changes()
        if self.trace_blobs:
            self.print_blobs()
        
    def journal_state_change(self, pad: DropLoc, new_state: OnOff) -> None:
        self.change_journal.change_to(pad, new_state)
        
    def journal_removal(self, pad: DropLoc, volume: Volume) -> None:
        self.change_journal.note_removal(pad, volume)
        
    def journal_delivery(self, pad: DropLoc, liquid: Liquid, *,
                         mix_result: Optional[MixResult] = None):
        self.change_journal.note_delivery(pad, liquid, mix_result=mix_result)
    
class UserOperation(Worker):
    def __init__(self, idle_barrier: IdleBarrier) -> None:
        super().__init__(idle_barrier)
    
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
    
    interval_change_callbacks: Final[ChangeCallbackList[Time]]
    state_change_callbacks: Final[ChangeCallbackList[bool]]

    def __init__(self, system: System) -> None:
        self.system = system
        self.engine = system.engine
        self.clock_thread = system.engine.clock_thread
        self.interval_change_callbacks = ChangeCallbackList[Time]()
        self.state_change_callbacks = ChangeCallbackList[bool]()
        
    @property
    def update_interval(self) -> Time:
        return self.clock_thread.update_interval
    
    @update_interval.setter
    def update_interval(self, interval: Time) -> None:
        old = self.clock_thread.update_interval
        if old != interval:
            self.clock_thread.update_interval = interval
            self.interval_change_callbacks.process(old, interval)
        
    def on_interval_change(self, cb: ChangeCallback[Time], *, key: Optional[Hashable] = None):
        self.interval_change_callbacks.add(cb, key=key)
        
    @property
    def update_rate(self) -> Frequency:
        return 1/self.update_interval
    
    @update_rate.setter
    def update_rate(self, rate: Frequency) -> None:
        self.update_interval = 1/rate
    
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
            delta = max(Ticks.ZERO, tick-self.next_tick)
        elif delta is None:
            delta = Ticks.ZERO
        self.system.before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, tick: Optional[TickNumber] = None, delta: Optional[Ticks] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.after_tick() called with both tick and delta specified"
            delta = max(Ticks.ZERO, tick-self.next_tick)
        elif delta is None:
            delta = Ticks.ZERO
        self.system.after_tick(fn, delta=delta)
    
    # Calling await_tick() when the clock isn't running only works if there is another thread that
    # will advance it.  
    def await_tick(self, tick: Optional[TickNumber] = None, delta: Optional[Ticks] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.await_tick() called with both tick and delta specified"
            delta = tick-self.next_tick
        elif delta is None:
            delta = Ticks.ZERO
        if delta >= 0:
            e = Event()
            def cb():
                e.set()
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
        
    def on_state_change(self, cb: ChangeCallback[bool], *, key: Optional[Hashable] = None):
        self.state_change_callbacks.add(cb, key=key)
    
    def start(self, interval: Optional[Union[Time,Frequency]] = None) -> None:
        assert not self.running, "Clock.start() called while clock is running"
        if isinstance(interval, Frequency):
            interval = (1/interval).a(Time)
        if interval is not None:
            self.update_interval = interval
        self.state_change_callbacks.process(False, True)
        self.clock_thread.start_clock(interval)
        
    def pause(self) -> None:
        assert self.running, "Clock.pause() called while clock is running"
        self.state_change_callbacks.process(True, False)
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
    monitor: Optional[BoardMonitor] = None
    _cpts_lock: Final[Lock]
    components: Final[list[SystemComponent]]
    running: bool = True
    
    def __init__(self, *, board: Board):
        self.board = board
        self.engine = Engine(default_clock_interval=board.drop_motion_time)
        self.clock = Clock(self)
        self._batch = None
        self._batch_lock = Lock()
        self._cpts_lock = Lock()
        self.components = []
        board.join_system(self)

    def __enter__(self) -> System:
        self.engine.__enter__()
        return self
    
    def __exit__(self, 
                 exc_type: Optional[type[BaseException]], 
                 exc_val: Optional[BaseException], 
                 exc_tb: Optional[TracebackType]) -> bool:
        return self.engine.__exit__(exc_type, exc_val, exc_tb)
    
    def component_joined(self, component: SystemComponent) -> None:
        with self._cpts_lock:
            assert self.running, f"Tried to add {component} to system after shutdown"
            self.components.append(component)
            
    def shutdown(self) -> None:
        with self._cpts_lock:
            for cpt in self.components:
                cpt.system_shutdown()
    
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
        
    def before_tick(self, fn: ClockCallback, *, delta: Ticks=Ticks.ZERO) -> None:
        self._channel().before_tick([(delta, fn)])

    def after_tick(self, fn: ClockCallback, *, delta: Ticks = Ticks.ZERO):
        self._channel().after_tick([(delta, fn)])
        

    def on_tick(self, req: DevCommRequest, *, delta: Ticks = Ticks.ZERO):
        self._channel().on_tick([(delta, req)])
        
    def delayed(self, function: Callable[[], T], *,
                after: Optional[DelayType]) -> Delayed[T]:
        if after is None:
            return Delayed.complete(function())
        future = Delayed[T]()
        def run_then_post() -> None:
            future.post(function())
        if isinstance(after, Time):
            if after > Time.ZERO:
                self.call_after(after, run_then_post)
            else:
                return Delayed.complete(function())
        else:
            if after > Ticks.ZERO:
                self.before_tick(run_then_post, delta = after)
            else:
                return Delayed.complete(function())
        return future
        
    def batched(self) -> Batch:
        with self._batch_lock:
            self._batch = Batch(self, nested=self._batch)
            return self._batch
        
        
    def run_monitored(self, fn: Callable[[System],T],
                      *, 
                      min_time: Time = 0*sec, 
                      max_time: Optional[Time] = None, 
                      update_interval: Time = 20*ms,
                      control_setup: Optional[Callable[[BoardMonitor, SubplotSpec], Any]] = None,
                      control_fraction: Optional[float] = None,
                      macro_file_name: Optional[str] = None,
                      thread_name: Optional[str] = None,
                      ) -> T:
        from mpam.monitor import BoardMonitor  # @Reimport
        val: T
        
        done = Event()
        def run_it() -> None:
            nonlocal val
            with self:
                val = fn(self)  # @UnusedVariable
            done.set()
            self.shutdown()

        if thread_name is None:
            thread_name = f"Monitored task @ {time_now()}"
        thread = Thread(target=run_it, name=thread_name)
        monitor = BoardMonitor(self.board,
                               control_setup=control_setup,
                               control_fraction=control_fraction,
                               macro_file_name=macro_file_name)
        self.monitor = monitor
        thread.start()
        monitor.keep_alive(sentinel = lambda : done.is_set(),
                           min_time = min_time,
                           max_time = max_time,
                           update_interval = update_interval)

        return val
    
