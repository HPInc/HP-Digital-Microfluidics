from __future__ import annotations
from mpam.types import Liquid, Dir, Delayed, RunMode, DelayType,\
    Operation, OpScheduler, XYCoord, unknown_reagent, Ticks, tick,\
    StaticOperation, Reagent, Callback, waste_reagent, schedule, ComputeOp
from mpam.device import Pad, Board, Well, WellGroup, WellState, ExtractionPoint
from mpam.exceptions import NoSuchPad, NotAtWell, MPAMError
from typing import Optional, Final, Union, Sequence, Callable, Mapping, ClassVar,\
    Iterator, Any
from quantities.SI import uL
from threading import Lock
from quantities.dimensions import Volume
from enum import Enum, auto
import math
from abc import ABC, abstractmethod

class DropStatus(Enum):
    ON_BOARD = auto()
    IN_WELL = auto()
    IN_MIX = auto()
    
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
    
class Path:
    class StartStep:
        op: Final[StaticOperation[Drop]]
    
        def __init__(self, op: StaticOperation[Drop]):
            self.op = op
            
    class MiddleStep:
        op: Final[Operation[Drop, Drop]]
        after: Final[Optional[Ticks]]
    
        def __init__(self, op: Operation[Drop,Drop], after: Optional[Ticks]) -> None:
            self.op = op
            self.after = after
            
        def _schedule_after(self, future: Delayed[Drop], *,
                            is_last: bool, post_result: bool) -> Delayed[Drop]:
            return future.then_schedule(self.op, mode=RunMode.GATED, after=self.after,
                                        post_result=post_result if is_last else True)
            
    class EndStep:
        op: Final[Operation[Drop, None]]
        after: Final[Optional[Ticks]]
    
        def __init__(self, op: Operation[Drop,None], after: Optional[Ticks]) -> None:
            self.op = op
            self.after = after
            
        def _schedule_after(self, future: Delayed[Drop], *,
                            post_result: bool) -> Delayed[None]:
            return future.then_schedule(self.op, mode=RunMode.GATED, after=self.after,
                                        post_result=post_result)
            
    
            
    class Start(StaticOperation['Drop']):
        start: Final[Path.StartStep]
        middle: Final[tuple[Path.MiddleStep, ...]]
        
        def __init__(self, start: Path.StartStep, 
                     middle: tuple[Path.MiddleStep,...]) -> None:
            self.start = start
            self.middle = middle
            
        def _extend(self, step: Path.MiddleStep) -> Path.Start:
            return Path.Start(start=self.start, middle = self.middle+(step,))
    
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED,     
                      after: Optional[DelayType] = None, 
                      post_result: bool = True,          
                      ) -> Delayed[Drop]:
            middle = self.middle
            last = len(middle) - 1
            future = schedule(self.start.op, mode=mode, after=after,
                              post_result = post_result if last == -1 else True)
            for i,step in enumerate(middle):
                future = step._schedule_after(future, post_result=post_result, is_last = i==last)
            return future
        
            
        def walk(self, direction: Dir, *,
                 steps: int = 1,
                 allow_unsafe: bool = False,
                 after: Optional[Ticks] = None) -> Path.Start:
            return self._extend(Path.WalkStep(direction, steps, allow_unsafe, after))
        def to_col(self, col: int, *,
                   allow_unsafe: bool = False,
                   after: Optional[Ticks] = None) -> Path.Start:
            return self._extend(Path.ToColStep(col, allow_unsafe, after))
        def to_row(self, row: int, *,
                   allow_unsafe: bool = False,
                   after: Optional[Ticks] = None) -> Path.Start:
            return self._extend(Path.ToRowStep(row, allow_unsafe, after))
        def mix(self, mix_type: MixingType, *,
                result: Optional[Reagent] = None,
                tolerance: float = 0.1,
                n_shuttles: int = 0, 
                fully_mix: Union[bool, Sequence[int]] = False,
                after: Optional[Ticks] = None) -> Path.Start:
            return self._extend(Path.MixStep(mix_type, result=result,
                                             tolerance=tolerance, n_shuttles=n_shuttles,
                                             fully_mix=fully_mix,
                                             after=after))
        def in_mix(self, *,
                   after: Optional[Ticks] = None) -> Path.Start:
            return self._extend(Path.InMixStep(after=after))
        
        def then_process(self, fn: Callable[[Drop], Any]) -> Path.Start:
            return self._extend(Path.CallStep(fn))
        
        def enter_well(self, *,
                       after: Optional[Ticks] = None) -> Path.Full:
            return Path.Full(self.start, self.middle, Path.EnterWellStep(after=after))
        
            
    class Middle(Operation['Drop','Drop']):
        middle: Final[tuple[Path.MiddleStep, ...]]
        
        def __init__(self, middle: tuple[Path.MiddleStep, ...]) -> None:
            self.middle =  middle
            
        def _extend(self, step: Path.MiddleStep) -> Path.Middle:
            return Path.Middle(self.middle+(step,))

        def _schedule_for(self, obj: Drop, *,
                          mode: RunMode = RunMode.GATED,     
                          after: Optional[DelayType] = None, 
                          post_result: bool = True,          
                          ) -> Delayed[Drop]:
            assert mode is RunMode.GATED
            future = Delayed[Drop]()
            if after is None:
                future.post(obj)
            else:
                obj.pad.board.before_tick(lambda: future.post(obj), delta=mode.gated_delay(after))
            
            middle = self.middle
            last = len(middle) - 1
            for i,step in enumerate(middle):
                future = step._schedule_after(future, post_result=post_result, is_last = i==last)
            return future

        def walk(self, direction: Dir, *,
                 steps: int = 1,
                 allow_unsafe: bool = False,
                 after: Optional[Ticks] = None) -> Path.Middle:
            return self._extend(Path.WalkStep(direction, steps, allow_unsafe, after))
        def to_col(self, col: int, *,
                   allow_unsafe: bool = False,
                   after: Optional[Ticks] = None) -> Path.Middle:
            return self._extend(Path.ToColStep(col, allow_unsafe, after))
        def to_row(self, row: int, *,
                   allow_unsafe: bool = False,
                   after: Optional[Ticks] = None) -> Path.Middle:
            return self._extend(Path.ToRowStep(row, allow_unsafe, after))
        def mix(self, mix_type: MixingType, *,
                result: Optional[Reagent] = None,
                tolerance: float = 0.1,
                n_shuttles: int = 0, 
                fully_mix: Union[bool, Sequence[int]] = True,
                after: Optional[Ticks] = None) -> Path.Middle:
            return self._extend(Path.MixStep(mix_type, result=result,
                                             tolerance=tolerance, n_shuttles=n_shuttles,
                                             fully_mix=fully_mix,
                                             after=after))
        def in_mix(self, *,
                   after: Optional[Ticks] = None) -> Path.Middle:
            return self._extend(Path.InMixStep(after=after))
        
        def then_process(self, fn: Callable[[Drop], Any]) -> Path.Middle:
            return self._extend(Path.CallStep(fn))
        
        def enter_well(self, *,
                       after: Optional[Ticks] = None) -> Path.End:
            return Path.End(self.middle, Path.EnterWellStep(after=after))

        
    class End(Operation['Drop', None]):
        middle: Final[tuple[Path.MiddleStep,...]]
        end: Final[Path.EndStep]
        
        def __init__(self, 
                     middle: tuple[Path.MiddleStep,...],
                     end: Path.EndStep) -> None:
            self.middle = middle
            self.end = end
            
        def _schedule_for(self, obj: Drop, *,
                          mode: RunMode = RunMode.GATED,     
                          after: Optional[DelayType] = None, 
                          post_result: bool = True,          
                          ) -> Delayed[None]:
            assert mode is RunMode.GATED
            future = Delayed[Drop]()
            if after is None:
                future.post(obj)
            else:
                obj.pad.board.before_tick(lambda: future.post(obj), delta=mode.gated_delay(after))
            
            middle = self.middle
            for step in middle:
                future = step._schedule_after(future, post_result=True, is_last = False)
            return self.end._schedule_after(future, post_result=post_result)
        
    class Full(StaticOperation[None]):
        start: Final[Path.StartStep]
        middle: Final[tuple[Path.MiddleStep, ...]]
        end: Final[Path.EndStep]
        
        def __init__(self, 
                     start: Path.StartStep,
                     middle: tuple[Path.MiddleStep,...],
                     end: Path.EndStep) -> None:
            self.start = start
            self.middle = middle
            self.end = end
            
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED,     
                      after: Optional[DelayType] = None, 
                      post_result: bool = True,          
                      ) -> Delayed[None]:
            middle = self.middle
            future = schedule(self.start.op, mode=mode, after=after,
                              post_result = True)
            for step in middle:
                future = step._schedule_after(future, post_result=True, is_last = False)
            return self.end._schedule_after(future, post_result=post_result)
        
    @classmethod
    def dispense_from(cls, well: Well) -> Path.Start:
        return Path.Start(Path.DispenseStep(well), ())
    
    @classmethod
    def teleport_into(cls, extraction_point: ExtractionPoint, *,
                      liquid: Optional[Liquid] = None,
                      reagent: Optional[Reagent] = None) -> Path.Start:
        return Path.Start(Path.TeleportInStep(extraction_point, liquid=liquid, reagent=reagent), ())

        
    class DispenseStep(StartStep):
        def __init__(self, well: Well) -> None:
            super().__init__(Drop.DispenseFrom(well))
    class TeleportInStep(StartStep):
        def __init__(self, extraction_point: ExtractionPoint, *,
                     liquid: Optional[Liquid] = None,
                     reagent: Optional[Reagent] = None
                     ) -> None:
            super().__init__(Drop.TeleportInTo(extraction_point, liquid=liquid, reagent=reagent))
            
    class EnterWellStep(EndStep):
        def __init__(self, *, 
                     after: Optional[Ticks]) -> None:
            super().__init__(Drop.EnterWell(), after)
        

    class WalkStep(MiddleStep):
        def __init__(self, direction: Dir, steps: int, allow_unsafe: bool, 
                     after: Optional[Ticks]) -> None:
            super().__init__(Drop.Move(direction, steps=steps, allow_unsafe=allow_unsafe), after)
            
    class ToColStep(MiddleStep):
        def __init__(self, col: int, allow_unsafe: bool, 
                     after: Optional[Ticks]) -> None:
            super().__init__(Drop.ToCol(col, allow_unsafe=allow_unsafe), after)
            
    class ToRowStep(MiddleStep):
        def __init__(self, row: int, allow_unsafe: bool, 
                     after: Optional[Ticks]) -> None:
            super().__init__(Drop.ToRow(row, allow_unsafe=allow_unsafe), after)
            
    class MixStep(MiddleStep):
        def __init__(self, mix_type: MixingType,
                     result: Optional[Reagent] = None,
                     tolerance: float = 0.1,
                     n_shuttles: int = 0, 
                     fully_mix: Union[bool, Sequence[int]] = False,
                     after: Optional[Ticks] = None) -> None:
            super().__init__(Drop.Start(MixProcess(mix_type, result=result,
                                                   tolerance=tolerance,
                                                   n_shuttles=n_shuttles,
                                                   fully_mix=fully_mix)), 
                                        after)
    class InMixStep(MiddleStep):
        def __init__(self, 
                     after: Optional[Ticks] = None) -> None:
            super().__init__(Drop.Join(), after)
        
            
    class CallStep(MiddleStep):
        def __init__(self, fn: Callable[[Drop], Any],
                     after: Optional[Ticks] = None) -> None:
            def fn2(drop: Drop) -> Delayed[Drop]:
                future = Delayed[Drop]()
                fn(drop)
                future.post(drop)
                return future
            super().__init__(ComputeOp['Drop','Drop'](fn2), after)

    
class PathStart:
    _start: Final[StaticOperation[Drop]]
    
    def __init__(self, start: StaticOperation[Drop]):
        self._start = start

    
# class Path:
#     def _walk_op(self, direction: Dir, steps: int, allow_unsafe: bool) -> Drop.Move:
#         return Drop.Move(direction, steps=steps, allow_unsafe=allow_unsafe)
#
# class PathFragment(Path):
#     ...
#
# class ExtensiblePathFragment(Path):
#     op: Final[Operation[Drop, Drop]]
#
#     def __init__(self, op: Operation[Drop, Drop]) -> None:
#         self.op = op
#
#     def _extended(self, op: Operation[Drop,Drop], after: Optional[DelayType]) -> ExtensiblePathFragment:
#         return ExtensiblePathFragment(self.op.then(op,after=after))
#
#     def walk(self, direction: Dir, *,
#              steps: int = 1,
#              allow_unsafe: bool = False,
#              after: Optional[DelayType] = None
#              ) -> ExtensiblePathFragment:
#         return self._extended(self._walk_op(direction, steps, allow_unsafe), after)
#
# class ExtensibleBasedPath(Path):
#     op: Final[StaticOperation[Drop]]
#
#     def __init__(self, op: StaticOperation[Drop]) -> None:
#         self.op = op
#
#     def _extended(self, op: Operation[Drop,Drop], after: Optional[DelayType]) -> ExtensibleBasedPath:
#         return ExtensibleBasedPath(self.op.then(op,after=after))
#
#     def walk(self, direction: Dir, *,
#              steps: int = 1,
#              allow_unsafe: bool = False,
#              after: Optional[DelayType] = None
#              ) -> ExtensibleBasedPath:
#         return self._extended(self._walk_op(direction, steps, allow_unsafe), after)
# class BasedPath(Path):
#     ...
#
#
#
# class TerminatedPathFragment(Path):
#     op: Operation[Drop, None]
#
#
#
#
# class FullPath(Path):
#     op: StaticOperation[None]
    
    

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
    
        
    class Start(Operation['Drop','Drop']):
        process_type: Final[MultiDropProcessType]
        
        def __repr__(self) -> str:
            return f"<Drop.Start: {self.process_type}>"
        
        def __init__(self, process_type: MultiDropProcessType) -> None:
            self.process_type = process_type

        def _schedule_for(self, drop: Drop, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[Drop]:
            board = drop.pad.board
            future = Delayed[Drop]()
                
            assert mode.is_gated
            def before_tick() -> None:
                # If all the other drops are waiting, this will install a callback on the next tick and then
                # call it immediately to do the first step.  Otherwise, that will happen when the last 
                # drop shows up.
                self.process_type.start(drop, future)
            board.before_tick(before_tick, delta=mode.gated_delay(after))
            return future
        
    class Join(Operation['Drop','Drop']):
        
        def __repr__(self) -> str:
            return f"<Drop.Join>"
        
        def _schedule_for(self, drop: Drop, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[Drop]:
            board = drop.pad.board
            future = Delayed[Drop]()
                
            assert mode.is_gated
            def before_tick() -> None:
                MultiDropProcess.join(drop, future)
            board.before_tick(before_tick, delta=mode.gated_delay(after))
            return future

class MultiDropProcessType(ABC):
    n_drops: Final[int]
    
    def __init__(self, n_drops: int) -> None:
        self.n_drops = n_drops
    
    # returns True if the iterator still has work to do
    @abstractmethod
    def iterator(self, drops: tuple[Drop, ...]) -> Iterator[bool]:  # @UnusedVariable
        ...
        
    # returns True if the futures should be posted.
    def finish(self, drops: Sequence[Drop],                  # @UnusedVariable
               futures: dict[Drop, Delayed[Drop]]) -> bool:  # @UnusedVariable
        return True
    
    @abstractmethod
    def secondary_pads(self, lead_drop: Drop) -> Sequence[Pad]:  # @UnusedVariable
        ...
        
    def start(self, lead_drop: Drop, future: Delayed[Drop]) -> None:
        process = MultiDropProcess(self, lead_drop, future)
        process.start()

    
class MultiDropProcess:
    process_type: Final[MultiDropProcessType]
    futures: Final[dict[Drop, Delayed[Drop]]]
    drops: Final[list[Optional[Drop]]]
    
    global_lock: Final[Lock] = Lock()
    
    def __init__(self, process_type: MultiDropProcessType,
                 lead_drop: Drop,
                 lead_future: Delayed[Drop]
                 ) -> None:
        self.process_type = process_type
        self.futures = {lead_drop: lead_future}
        self.drops = [None] * process_type.n_drops
        self.drops[0] = lead_drop
        
    def start(self) -> None:
        drops = self.drops
        lead_drop = drops[0]
        assert lead_drop is not None
        secondary_pads = self.process_type.secondary_pads(lead_drop)
        futures = self.futures
        pending_drops = 0
        lock = self.global_lock
        
        def on_join_factory(i: int) -> Callable[[Drop, Delayed[Drop]],
                                         Optional[Callback]]:
            # Called with global_lock locked.  Returns true if last one.
            def on_join(drop: Drop, future: Delayed[Drop]) -> Optional[Callback]:
                nonlocal pending_drops
                drops[i+1] = drop
                futures[drop] = future
                if pending_drops == 1:
                    return lambda: self.run()
                else:
                    pending_drops -= 1
                    return None
            return on_join
        
        with lock:
            for i,p in enumerate(secondary_pads):
                future: Optional[Delayed[Drop]] = getattr(p, "_waiting_to_join", None)
                if future is None:
                    setattr(p, "_on_join", on_join_factory(i))
                    pending_drops += 1
                else:
                    setattr(p, "_waiting_to_join", None)
                    d = p.drop
                    assert d is not None
                    futures[d] = future
                    drops[i] = d
            ready = (pending_drops == 0)
        if ready:
            self.run()


    @classmethod
    def join(cls, drop: Drop, future: Delayed[Drop]) -> None:
        p = drop.pad
        with cls.global_lock:
            fn: Optional[Callable[[Drop,Delayed[Drop]],
                                  Optional[Callback]]] = getattr(p, "_on_join", None)
            if fn is None:
                setattr(p, "_waiting_to_join", future)
                return
            else:
                setattr(p, "_on_join", None)
                cb = fn(drop, future)
        if cb is not None:
            cb()
            
    def iterator(self, board: Board, drops: Sequence[Drop]) -> Iterator[Optional[Ticks]]:
        process_type = self.process_type
        futures = self.futures
        def checked(d: Optional[Drop]) -> Drop:
            assert d is not None
            return d
        drops = tuple(checked(d) for d in drops)
        i = process_type.iterator(drops = drops)
        one_tick = 1*tick
        while next(i):
            yield one_tick
        def do_post() -> None:
            if process_type.finish(drops, futures):
                for drop, future in futures.items():
                    future.post(drop)
        board.after_tick(do_post)
        yield None
        
            
    def run(self) -> None:
        def checked(d: Optional[Drop]) -> Drop:
            assert d is not None
            return d
        drops = tuple(checked(d) for d in self.drops)
        lead_drop = drops[0]
        assert lead_drop is not None
        board = lead_drop.pad.board
        iterator = self.iterator(board, drops)
        
        # We're inside a before_tick, so we run the first step here.  Then we install
        # the callback before the next tick to do the rest
        after_first = next(iterator)
        if after_first is not None: 
            board.before_tick(lambda: next(iterator))
        
class MixSequenceStep(ABC):
    @abstractmethod
    def schedule(self, shuttle_no: int, mergep: bool,           # @UnusedVariable
                 drops: Sequence[Drop],                         # @UnusedVariable
                 pads: Sequence[Pad]) -> Mapping[Drop, float]:  # @UnusedVariable
        ...
    

class MixStep(MixSequenceStep):
    d1_index: Final[int]
    d2_index: Final[int]
    error: Final[float]
    def __init__(self, drop1: int, drop2: int, error: float) -> None:
        self.d1_index = drop1
        self.d2_index = drop2
        self.error = error
        
            
    def schedule(self, shuttle_no: int,  # @UnusedVariable
                 mergep: bool, 
                 drops: Sequence[Drop],
                 pads: Sequence[Pad]) -> Mapping[Drop, float]:  
        drop1 = drops[self.d1_index]
        drop2 = drops[self.d2_index]
        pad1 = pads[self.d1_index]
        pad2 = pads[self.d2_index]
        middle = pad1.between_pads[pad2]
        l1 = drop1.liquid
        l2 = drop2.liquid
        if mergep:
            def update(_) -> None:
                drop2.status = DropStatus.IN_MIX
                l1.mix_in(l2)
                # print(f"Merging: now {l1.reagent}.  Error is {self.error}")
                pad2.drop = None
                drop1.pad = middle
            pad1.schedule(Pad.TurnOff, post_result = False)
            pad2.schedule(Pad.TurnOff, post_result = False)
            middle.schedule(Pad.TurnOn).then_call(update)
        else:
            def update(_) -> None:
                l1.split_to(l2)
                drop2.status = DropStatus.ON_BOARD
                drop1.pad = pad1
                pad2.drop = drop2
            pad1.schedule(Pad.TurnOn, post_result = False)
            pad2.schedule(Pad.TurnOn, post_result = False)
            middle.schedule(Pad.TurnOff).then_call(update)
        e = self.error
        return {drop1: e, drop2: e}
                 


class MixProcess(MultiDropProcessType):
    mix_type: Final[MixingType]
    result: Final[Optional[Reagent]]
    tolerance: Final[float]
    n_shuttles: Final[int]
    fully_mix: Final[Union[bool, Sequence[int]]]
    def __init__(self, mix_type: MixingType, *,
                 result: Optional[Reagent] = None,
                 tolerance: float = 0.1,
                 n_shuttles: int = 0,
                 fully_mix: Union[bool, Sequence[int]] = False,
                 ) -> None:
        super().__init__(mix_type.n_drops)
        self.mix_type = mix_type
        self.result = result
        self.tolerance = tolerance
        self.n_shuttles = n_shuttles
        self.fully_mix = fully_mix
        
    def __repr__(self) -> str:
        return f"""<MixProcess: {self.mix_type}, 
                        result={self.result}, 
                        tol={self.tolerance:%}, 
                        shuttles={self.n_shuttles}
                        fully_mix={self.fully_mix}>"""
        
        
    def secondary_pads(self, lead_drop: Drop) -> Sequence[Pad]:  # @UnusedVariable
        return self.mix_type.secondary_pads(lead_drop)
    
    # returns True if the iterator still has work to do
    def iterator(self, drops: tuple[Drop, ...]) -> Iterator[bool]:  # @UnusedVariable
        fm = self.fully_mix
        if isinstance(fm, bool):
            fully_mix = set(drops) if fm else {drops[0]}
        else:
            fully_mix = { drops[i] for i in fm }
        return self.mix_type.perform(full_mix = fully_mix,
                                     tolerance = self.tolerance,
                                     drops = drops,
                                     n_shuttles = self.n_shuttles
                                     )

    # returns True if the futures should be posted.
    def finish(self, drops: Sequence[Drop],             
               futures: dict[Drop, Delayed[Drop]]) -> bool:  # @UnusedVariable
        result = self.result
        fm = self.fully_mix
        if isinstance(fm, bool):
            fully_mix = set(drops) if fm else {drops[0]}
        else:
            fully_mix = { drops[i] for i in fm }
        print(f"mix result is {drops[0].liquid}")
        for drop in drops:
            if drop in fully_mix:
                if result is not None:
                    drop.reagent = result
            else:
                drop.reagent = waste_reagent
        return True
                
            
        
        
        
class MixingBase(ABC):
    is_approximate: Final[bool]
    n_drops: Final[int]
    
    def __init__(self, *, n_drops: int, is_approximate: bool) -> None:
        self.n_drops = n_drops
        self.is_approximate = is_approximate

    @abstractmethod    
    def perform(self, *,
                full_mix: set[Drop],        # @UnusedVariable
                tolerance: float,           # @UnusedVariable
                drops: tuple[Drop,...],     # @UnusedVariable
                n_shuttles: int,            # @UnusedVariable
                ) -> Iterator[bool]:
        ...

class MixingType(MixingBase):
    

    @abstractmethod            
    def secondary_pads(self, lead_drop: Drop) -> Sequence[Pad]: ...  # @UnusedVariable

        
    def two_steps_from(self, pad: Pad, direction: Dir) -> Pad:
        m = pad.neighbor(direction)
        assert m is not None
        p = m.neighbor(direction)
        assert p is not None
        return p
    
    
MixSequence = Sequence[Sequence[MixSequenceStep]]
    
class PureMix(MixingType):
    script: Final[MixSequence]
    
    def __init__(self, script: MixSequence, *,
                 n_drops: int, 
                 is_approximate: bool):
        super().__init__(n_drops = n_drops, is_approximate = is_approximate)
        self.script = script
    
    def perform(self, *,
                full_mix: set[Drop], 
                tolerance: float,
                drops: tuple[Drop,...],
                n_shuttles: int,
                ) -> Iterator[bool]:
        unsatisfied = full_mix.intersection(drops)
        if not unsatisfied:
            yield False
        tolerances = {d: tolerance if d in unsatisfied else math.inf for d in drops}
        error = {d: math.inf for d in drops}
        for step in self.script:
            drop_pads = tuple(d.pad for d in drops)
            for shuttle in range(n_shuttles+1):
                for mergep in (True, False):
                    for action in step:
                        e = action.schedule(shuttle, mergep, drops, drop_pads)
                        error.update(e)
                    if not mergep and shuttle == n_shuttles:
                        for d in unsatisfied.copy():
                            if error[d] <= tolerances[d]:
                                unsatisfied.remove(d)
                    if unsatisfied:
                        yield True
                    else:
                        yield False
        min_tolerance = min(tolerances[d] for d in unsatisfied)
        min_error = min(error[d] for d in unsatisfied)
        n = len(drops)
        raise MPAMError(f"""Requested driving error to {min_tolerance} in {n}-way mix.  
                                        Could only get to {min_error} on at least one drop""")
        

class Submix(MixingBase):
    mix_type: Final[MixingType]
    indices: Final[Sequence[int]]
    need_all: Final[bool]

    def __init__(self, mix_type: MixingType, indices: Sequence[int], need_all: bool) -> None:
        super().__init__(n_drops = len(indices), is_approximate = mix_type.is_approximate)
        self.mix_type = mix_type
        self.indices = indices
        self.need_all = need_all
    
    def perform(self, *,
                full_mix: set[Drop], 
                tolerance: float,
                drops: tuple[Drop,...],
                n_shuttles: int,
                ) -> Iterator[bool]:
        used = tuple(drops[i] for i in self.indices)
        return self.mix_type.perform(full_mix = set(used) if self.need_all else full_mix,
                                     tolerance = tolerance,
                                     drops = used,
                                     n_shuttles = n_shuttles)
        
MixPhases = Sequence[Sequence[Submix]]

class CompositeMix(MixingType):
    phases: Final[MixPhases]
    n_approximate: Final[int]
    
    def __init__(self, phases: MixPhases, *, n_drops: int):
        approximate_phases = 0
        for phase in phases:
            if any(submix.is_approximate for submix in phase):
                approximate_phases += 1
        self.n_approximate = approximate_phases
        
        super().__init__(n_drops=n_drops, is_approximate = approximate_phases > 0)
        self.phases = phases
    
    def perform(self, *,
                full_mix: set[Drop], 
                tolerance: float,
                drops: tuple[Drop,...],
                n_shuttles: int,
                ) -> Iterator[bool]:
        # print(drops)
        approximate_phases = self.n_approximate
        if approximate_phases > 1:
            tolerance = (1+tolerance)**(1/approximate_phases)-1
            # print(f"Adjusted tolerance is {tolerance}")
        
        last_phase = len(self.phases)-1
        for p,phase in enumerate(self.phases):
            iters = {i: submix.perform(full_mix=full_mix,
                                       tolerance=tolerance,
                                       drops=drops,
                                       n_shuttles=n_shuttles) 
                        for i,submix in enumerate(phase)}
            while iters:
                current = tuple(iters.items())
                for i,iterator in current:
                    if not next(iterator):
                        del iters[i]
                        
                done = p==last_phase and not iters
                yield not done
        
    
    
class Mix2(PureMix):
    to_second: Final[Dir]
    
    the_script: Final[ClassVar[MixSequence]] = (
        (MixStep(0,1,0.0),)
        ,)

    def __init__(self, to_second: Dir) -> None:
        super().__init__(Mix2.the_script, n_drops=2, is_approximate = False)
        self.to_second = to_second
        
    def secondary_pads(self, lead_drop:Drop)->Sequence[Pad]:
        p1 = lead_drop.pad
        p2 = self.two_steps_from(p1, self.to_second)
        return (p2,)

class Mix3(PureMix):
    to_second: Final[Dir]
    to_third: Final[Dir]
    
    the_script: Final[ClassVar[MixSequence]] = (
        (MixStep(0,1,math.inf),),
        (MixStep(1,2,1/1),),        
        (MixStep(0,1,1/2),),
        (MixStep(1,2,1/5),),
        (MixStep(0,1,1/10),),
        (MixStep(1,2,1/21),),
        (MixStep(0,1,1/42),),
        (MixStep(1,2,1/85),),
        (MixStep(0,1,1/170),),
        (MixStep(1,2,1/341),),
        )

    def __init__(self, to_second: Dir, to_third: Dir) -> None:
        super().__init__(Mix3.the_script, n_drops=3, is_approximate = True)
        self.to_second = to_second
        self.to_third = to_third
        
    def secondary_pads(self, lead_drop:Drop)->Sequence[Pad]:
        p1 = lead_drop.pad
        p2 = self.two_steps_from(p1, self.to_second)
        p3 = self.two_steps_from(p2, self.to_third)
        return (p2,p3)

class Mix4(CompositeMix):
    to_second: Final[Dir]
    to_third: Final[Dir]
    

    def __init__(self, to_second: Dir, to_third: Dir) -> None:
        phases = ((Submix(Mix2(to_second), (0,1), True),
                   Submix(Mix2(to_second), (2,3), True)),
                  (Submix(Mix2(to_third), (0,2), False),
                   Submix(Mix2(to_third), (1,3), False))
                )
        super().__init__(phases, n_drops=4)
        self.to_second = to_second
        self.to_third = to_third
        
    def secondary_pads(self, lead_drop:Drop)->Sequence[Pad]:
        p1 = lead_drop.pad
        p2 = self.two_steps_from(p1, self.to_second)
        p3 = self.two_steps_from(p1, self.to_third)
        p4 = self.two_steps_from(p3, self.to_second)
        return (p2,p3,p4)

class Mix6(CompositeMix):
    major_dir: Final[Dir]
    minor_dir: Final[Dir]
    

    def __init__(self, major_dir: Dir, minor_dir: Dir) -> None:
        phases = ((Submix(Mix2(minor_dir), (0,3), True),
                   Submix(Mix2(minor_dir), (1,4), True),
                   Submix(Mix2(minor_dir), (2,5), True)),
                  (Submix(Mix3(major_dir, major_dir), (0,1,2), False),
                   Submix(Mix3(major_dir, major_dir), (3,4,5), False))
                )
        super().__init__(phases, n_drops=6)
        self.major_dir = major_dir
        self.minor_dir = minor_dir
        
    def secondary_pads(self, lead_drop:Drop)->Sequence[Pad]:
        p1 = lead_drop.pad
        p2 = self.two_steps_from(p1, self.major_dir)
        p3 = self.two_steps_from(p2, self.major_dir)
        p4 = self.two_steps_from(p1, self.minor_dir)
        p5 = self.two_steps_from(p4, self.major_dir)
        p6 = self.two_steps_from(p5, self.major_dir)
        return (p2,p3,p4,p5,p6)

class Mix9(CompositeMix):
    major_dir: Final[Dir]
    minor_dir: Final[Dir]
    

    def __init__(self, major_dir: Dir, minor_dir: Dir) -> None:
        phases = ((Submix(Mix3(minor_dir, minor_dir), (0,3,6), True),
                   Submix(Mix3(minor_dir, minor_dir), (1,4,7), True),
                   Submix(Mix3(minor_dir, minor_dir), (2,5,8), True)),
                  (Submix(Mix3(major_dir, major_dir), (0,1,2), False),
                   Submix(Mix3(major_dir, major_dir), (3,4,5), False),
                   Submix(Mix3(major_dir, major_dir), (6,7,8), False))
                )
        super().__init__(phases, n_drops=9)
        self.major_dir = major_dir
        self.minor_dir = minor_dir
        
    def secondary_pads(self, lead_drop:Drop)->Sequence[Pad]:
        p1 = lead_drop.pad
        p2 = self.two_steps_from(p1, self.major_dir)
        p3 = self.two_steps_from(p2, self.major_dir)
        p4 = self.two_steps_from(p1, self.minor_dir)
        p5 = self.two_steps_from(p4, self.major_dir)
        p6 = self.two_steps_from(p5, self.major_dir)
        p7 = self.two_steps_from(p4, self.minor_dir)
        p8 = self.two_steps_from(p7, self.major_dir)
        p9 = self.two_steps_from(p8, self.major_dir)
        return (p2,p3,p4,p5,p6,p7,p8,p9)


