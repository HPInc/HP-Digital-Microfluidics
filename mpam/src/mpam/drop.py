from __future__ import annotations
from mpam.types import Liquid, Dir, Delayed, RunMode, DelayType,\
    Operation, OpScheduler, XYCoord, unknown_reagent, Ticks, tick,\
    StaticOperation, Reagent, Callback
from mpam.device import Pad, Board, Well, WellGroup, WellState, ExtractionPoint
from mpam.exceptions import NoSuchPad, NotAtWell
from typing import Optional, Final, Union, Sequence, Callable, \
    Iterator
from quantities.SI import uL
from threading import Lock
from quantities.dimensions import Volume
from enum import Enum, auto
from abc import ABC, abstractmethod

# if TYPE_CHECKING:
    # from mpam.processes import MultiDropProcessType

class DropStatus(Enum):
    ON_BOARD = auto()
    IN_WELL = auto()
    IN_MIX = auto()
    OFF_BOARD = auto()
    
class MotionOp(Operation['Drop', 'Drop'], ABC):
    allow_unsafe: Final[bool]
    
    def __init__(self, *, allow_unsafe: bool):
        self.allow_unsafe = allow_unsafe
    
    @abstractmethod
    def dirAndSteps(self, drop: Drop) -> tuple[Dir, int]: ...  # @UnusedVariable
    def _schedule_for(self, drop: Drop, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      ) -> Delayed[Drop]:
        board = drop.pad.board
        system = board.in_system()
        
        direction, steps = self.dirAndSteps(drop)
        # allow_unsafe_motion = self.allow_unsafe_motion
        future = Delayed[Drop]()
        
        if steps == 0:
            future.post(drop)
            return future
            
        one_tick: Ticks = 1*tick
        allow_unsafe = self.allow_unsafe
        assert mode.is_gated
        def before_tick() -> Iterator[Optional[Ticks]]:
            last_pad = drop.pad
            for i in range(steps):
                next_pad = last_pad.neighbor(direction)
                if next_pad is None or next_pad.broken:
                    raise NoSuchPad(board.orientation.neighbor(direction, last_pad.location))
                if not allow_unsafe:
                    while not next_pad.safe_except(last_pad):
                        # print(f"unsafe: {i} of {steps}, {drop}, lp = {last_pad}, np = {next_pad}")
                        yield one_tick
                while not next_pad.reserve():
                    if allow_unsafe:
                        break
                    yield one_tick
                with system.batched():
                    # print(f"Tick number {system.clock.next_tick}")
                    # print(f"Moving drop from {last_pad} to {next_pad}")
                    assert last_pad == drop.pad, f"{i} of {steps}, {drop}, lp = {last_pad}, np = {next_pad}"
                    next_pad.schedule(Pad.TurnOn, mode=mode, post_result=False)
                    last_pad.schedule(Pad.TurnOff, mode=mode, post_result=False)
                    board.after_tick(drop._update_pad_fn(last_pad, next_pad))
                    # print(f"i = {i}, steps = {steps}, drop = {drop}, lp = {last_pad}, np = {next_pad}")
                    if post_result and i == steps-1:
                        board.after_tick(lambda : future.post(drop))
                last_pad = next_pad
                if i < steps-1:
                    yield one_tick
            yield None
        iterator = before_tick()
        board.before_tick(lambda: next(iterator), delta=mode.gated_delay(after))
        return future
    
    
    
    

class Drop(OpScheduler['Drop']):
    liquid: Liquid
    _pad: Pad
    status: DropStatus
    
    @property
    def pad(self) -> Pad:
        return self._pad
    
    @pad.setter
    def pad(self, pad: Pad) -> None:
        old = self._pad
        # assert?
        if old.drop is self:
            old.drop = None
        self._pad = pad
        pad.drop = self
    
    @property
    def volume(self) -> Volume:
        return self.liquid.volume
    
    @property
    def reagent(self) -> Reagent:
        return self.liquid.reagent
    
    @reagent.setter
    def reagent(self, val: Reagent) -> None:
        self.liquid.reagent = val
    
    def __init__(self, pad: Pad, liquid: Liquid) -> None:
        assert pad.drop is None, f"Trying to create a second drop at {pad}"
        self.liquid = liquid
        self._pad = pad
        self.status = DropStatus.ON_BOARD 
        pad.drop = self
        
    def __repr__(self) -> str:
        return f"Drop[{self.pad}, {self.liquid}]"
    
    def schedule_communication(self, cb: Callable[[], Optional[Callback]], mode: RunMode, *,  
                               after: Optional[DelayType] = None) -> None:  
        self.pad.schedule_communication(cb, mode=mode, after=after)
    
    
    @classmethod
    def appear_at(cls, board: Board, locations: Sequence[Union[XYCoord, tuple[int, int]]],
                 liquid: Liquid = Liquid(unknown_reagent, 0.5*uL) 
                 ) -> Delayed[Sequence[Drop]]:
        locs = ((loc.x, loc.y) if isinstance(loc, XYCoord) else loc for loc in locations)
        drops = tuple(Drop(board.pad_at(x,y), liquid) for (x, y) in locs)
        future = Delayed[Sequence[Drop]]()
        system = board.system
        assert system is not None
        outstanding: int = len(drops)
        lock = Lock()
        def join(_) -> None:
            # print("joining")
            with lock:
                nonlocal outstanding
                outstanding -= 1
                if outstanding == 0:
                    future.post(drops)
        with system.batched():
            for drop in drops:
                drop.pad.schedule(Pad.TurnOn).when_value(join)
        return future
        
    class AppearAt(StaticOperation['Drop']):
        pad: Final[Pad]
        liquid: Final[Liquid]
        
        def __init__(self, pad: Union[Pad, XYCoord, tuple[int, int]], *, 
                     board: Board,
                     liquid: Optional[Liquid] = None,
                     ) -> None:
            if isinstance(pad, XYCoord):
                pad = board.pad_array[pad]
            elif isinstance(pad, tuple):
                pad = board.pad_at(pad[0], pad[1])
            self.pad = pad
            if liquid is None:
                liquid = Liquid(unknown_reagent, board.drop_size)
            self.liquid = liquid
            
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  
                      ) -> Delayed[Drop]:
            future = Delayed[Drop]()
            assert mode.is_gated
            pad = self.pad
            def make_drop(_) -> None:
                drop = Drop(pad=pad, liquid=self.liquid)
                if post_result:
                    future.post(drop)
            pad.schedule(Pad.TurnOn, mode=mode, after=after) \
                .then_call(make_drop)
            return future
            
    class TeleportInTo(StaticOperation['Drop']):
        extraction_point: Final[ExtractionPoint]
        liquid: Final[Liquid]
        
        def __init__(self, extraction_point: ExtractionPoint, *,
                     liquid: Optional[Liquid] = None, 
                     reagent: Optional[Reagent] = None,
                     ) -> None:
            self.extraction_point = extraction_point
            board = extraction_point.pad.board 
            if liquid is None:
                if reagent is None:
                    reagent = unknown_reagent
                liquid = Liquid(reagent, board.drop_size)
            self.liquid = liquid
            
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  
                      ) -> Delayed[Drop]:
            future = Delayed[Drop]()
            assert mode.is_gated
            pad = self.extraction_point.pad
            def make_drop(_) -> None:
                drop = Drop(pad=pad, liquid=self.liquid)
                if post_result:
                    future.post(drop)
            pad.schedule(Pad.TurnOn, mode=mode, after=after) \
                .then_call(make_drop)
            return future
    
    class Move(MotionOp):
        direction: Final[Dir]
        steps: Final[int]
        
        def __repr__(self) -> str:
            return f"<Drop.Move: {self.steps} {self.direction}>"
        
        def __init__(self, direction: Dir, *, steps: int = 1, 
                     allow_unsafe: bool = False) -> None:
            super().__init__(allow_unsafe=allow_unsafe)
            self.direction = direction
            self.steps = steps
            
        def dirAndSteps(self, drop: Drop)->tuple[Dir, int]:  # @UnusedVariable
            return self.direction, self.steps
            
    class ToCol(MotionOp):
        col: Final[int]
        
        def __repr__(self) -> str:
            return f"<Drop.ToCol: {self.col}>"

        def __init__(self, col: int, *, allow_unsafe: bool = False) -> None:
            super().__init__(allow_unsafe=allow_unsafe)
            self.col = col
            
        def dirAndSteps(self, drop: Drop)->tuple[Dir, int]:
            pad = drop.pad
            direction = pad.board.orientation.pos_x
            current = pad.column
            steps = self.col-current
            return (direction, steps) if steps >=0 else (direction.opposite, -steps)
            
    class ToRow(MotionOp):
        row: Final[int]
        
        def __repr__(self) -> str:
            return f"<Drop.ToRow: {self.row}>"

        def __init__(self, row: int, *, allow_unsafe: bool = False) -> None:
            super().__init__(allow_unsafe=allow_unsafe)
            self.row = row
            
        def dirAndSteps(self, drop: Drop)->tuple[Dir, int]:
            pad = drop.pad
            direction = pad.board.orientation.pos_y
            current = pad.row
            steps = self.row-current
            return (direction, steps) if steps >=0 else (direction.opposite, -steps)
            
            
         
            
    class DispenseFrom(StaticOperation['Drop']):
        well: Well
        
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  
                      ) -> Delayed[Drop]:
            future = Delayed[Drop]()
            well = self.well
            def make_drop(_) -> None:
                v = well.dispensed_volume
                pad = self.well.exit_pad
                liquid = well.transfer_out(v)
                drop = Drop(pad=pad, liquid=liquid)
                if post_result:
                    future.post(drop)
                
                
            # Note, we post the drop as soon as we get to the DISPENSED state, even theough
            # we continue on to READY
            group = self.well.group
            group.schedule(WellGroup.TransitionTo(WellState.DISPENSED, well = self.well), mode=mode, after=after) \
                .then_call(make_drop) \
                .then_schedule(WellGroup.TransitionTo(WellState.READY))
            return future
            
        
        def __init__(self, well: Well) -> None:
            self.well = well
            
    class EnterWell(Operation['Drop',None]):
        well: Final[Optional[Well]]
        
        def __repr__(self) -> str:
            return f"<Drop.EnterWell: {self.well}>"
        
        
        def _schedule_for(self, drop: Drop, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,  
                          ) -> Delayed[None]:
            future = Delayed[None]()
            if self.well is None:
                if drop.pad.well is None:
                    raise NotAtWell(f"{drop} not at a well")
                well = drop.pad.well
            else:
                well = self.well
            def consume_drop(_) -> None:
                well.transfer_in(drop.liquid)
                drop.status = DropStatus.IN_WELL
                drop.pad.drop = None
                if post_result:
                    future.post(None)
                
                
            # Note, we post the drop as soon as we get to the DISPENSED state, even theough
            # we continue on to READY
            group = well.group
            group.schedule(WellGroup.TransitionTo(WellState.ABSORBED, well=well), mode=mode, after=after) \
                .then_call(consume_drop) \
                .then_schedule(WellGroup.TransitionTo(WellState.READY, well=well))
            return future
            
        
        def __init__(self, well: Optional[Well] = None) -> None:
            self.well = well
        
            
        
    def _update_pad_fn(self, from_pad: Pad, to_pad: Pad):
        def fn() -> None:
            assert from_pad.drop is self, f"Moved {self}, but thought it was at {from_pad}"
            assert to_pad.drop is None, f"Moving {self} to non-empty {to_pad}"
            # print(f"Moved drop from {from_pad} to {to_pad}")
            self.pad = to_pad
            to_pad.reserved = False
            # print(f"Drop now at {to_pad}")
        return fn
    

