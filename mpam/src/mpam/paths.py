from __future__ import annotations

from typing import Final, Optional, Callable, Any

from mpam.device import Well, ExtractionPoint
from mpam.drop import Drop
from mpam.types import StaticOperation, Operation, Ticks, Delayed, RunMode, \
    DelayType, schedule, Dir, Reagent, Liquid, ComputeOp
from mpam.processes import StartProcess, JoinProcess, MultiDropProcessType


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
            
    
            
    class Start(StaticOperation[Drop]):
        first_step: Final[Path.StartStep]
        middle_steps: Final[tuple[Path.MiddleStep, ...]]
        
        def __init__(self, start: Path.StartStep, 
                     middle: tuple[Path.MiddleStep,...]) -> None:
            self.first_step = start
            self.middle_steps = middle
            
        def _extend(self, step: Path.MiddleStep) -> Path.Start:
            return Path.Start(start=self.first_step, middle = self.middle_steps+(step,))
    
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED,     
                      after: Optional[DelayType] = None, 
                      post_result: bool = True,          
                      ) -> Delayed[Drop]:
            middle = self.middle_steps
            last = len(middle) - 1
            future = schedule(self.first_step.op, mode=mode, after=after,
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
        
        def start(self, process_type: MultiDropProcessType, *,
                  after: Optional[Ticks] = None) -> Path.Start:
            return self._extend(Path.StartProcessStep(process_type, after=after))
        
        
        # def mix(self, mix_type: MixingType, *,
        #         result: Optional[Reagent] = None,
        #         tolerance: float = 0.1,
        #         n_shuttles: int = 0, 
        #         fully_mix: Union[bool, Sequence[int]] = False,
        #         after: Optional[Ticks] = None) -> Path.Start:
        #     return self._extend(Path.MixStep(mix_type, result=result,
        #                                      tolerance=tolerance, n_shuttles=n_shuttles,
        #                                      fully_mix=fully_mix,
        #                                      after=after))
        def join(self, *,
                 after: Optional[Ticks] = None) -> Path.Start:
            return self._extend(Path.JoinProcessStep(after=after))
        
        in_mix = join
        
        def then_process(self, fn: Callable[[Drop], Any]) -> Path.Start:
            return self._extend(Path.CallStep(fn))
        
        def enter_well(self, *,
                       after: Optional[Ticks] = None) -> Path.Full:
            return Path.Full(self.first_step, self.middle_steps, Path.EnterWellStep(after=after))
        
            
    class Middle(Operation[Drop,Drop]):
        middle_steps: Final[tuple[Path.MiddleStep, ...]]
        
        def __init__(self, middle: tuple[Path.MiddleStep, ...]) -> None:
            self.middle_steps =  middle
            
        def _extend(self, step: Path.MiddleStep) -> Path.Middle:
            return Path.Middle(self.middle_steps+(step,))

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
            
            middle = self.middle_steps
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
        
        def start(self, process_type: MultiDropProcessType, *,
                  after: Optional[Ticks] = None) -> Path.Middle:
            return self._extend(Path.StartProcessStep(process_type, after=after))
        
        # def mix(self, mix_type: MixingType, *,
        #         result: Optional[Reagent] = None,
        #         tolerance: float = 0.1,
        #         n_shuttles: int = 0, 
        #         fully_mix: Union[bool, Sequence[int]] = True,
        #         after: Optional[Ticks] = None) -> Path.Middle:
        #     return self._extend(Path.MixStep(mix_type, result=result,
        #                                      tolerance=tolerance, n_shuttles=n_shuttles,
        #                                      fully_mix=fully_mix,
        #                                      after=after))
        #

        def join(self, *,
                 after: Optional[Ticks] = None) -> Path.Middle:
            return self._extend(Path.JoinProcessStep(after=after))
        
        in_mix = join
        
        def then_process(self, fn: Callable[[Drop], Any]) -> Path.Middle:
            return self._extend(Path.CallStep(fn))
        
        def enter_well(self, *,
                       after: Optional[Ticks] = None) -> Path.End:
            return Path.End(self.middle_steps, Path.EnterWellStep(after=after))

        
    class End(Operation[Drop, None]):
        middle_steps: Final[tuple[Path.MiddleStep,...]]
        last_step: Final[Path.EndStep]
        
        def __init__(self, 
                     middle: tuple[Path.MiddleStep,...],
                     end: Path.EndStep) -> None:
            self.middle_steps = middle
            self.last_step = end
            
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
            
            middle = self.middle_steps
            for step in middle:
                future = step._schedule_after(future, post_result=True, is_last = False)
            return self.last_step._schedule_after(future, post_result=post_result)
        
    class Full(StaticOperation[None]):
        first_step: Final[Path.StartStep]
        middle_steps: Final[tuple[Path.MiddleStep, ...]]
        last_step: Final[Path.EndStep]
        
        def __init__(self, 
                     start: Path.StartStep,
                     middle: tuple[Path.MiddleStep,...],
                     end: Path.EndStep) -> None:
            self.first_step = start
            self.middle_steps = middle
            self.last_step = end
            
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED,     
                      after: Optional[DelayType] = None, 
                      post_result: bool = True,          
                      ) -> Delayed[None]:
            middle = self.middle_steps
            future = schedule(self.first_step.op, mode=mode, after=after,
                              post_result = True)
            for step in middle:
                future = step._schedule_after(future, post_result=True, is_last = False)
            return self.last_step._schedule_after(future, post_result=post_result)
        
    @classmethod
    def dispense_from(cls, well: Well) -> Path.Start:
        return Path.Start(Path.DispenseStep(well), ())
    
    @classmethod
    def teleport_into(cls, extraction_point: ExtractionPoint, *,
                      liquid: Optional[Liquid] = None,
                      reagent: Optional[Reagent] = None) -> Path.Start:
        return Path.Start(Path.TeleportInStep(extraction_point, liquid=liquid, reagent=reagent), ())

    @classmethod
    def walk(cls, direction: Dir, *,
             steps: int = 1,
             allow_unsafe: bool = False,
             after: Optional[Ticks] = None) -> Path.Middle:
        return Path.Middle((Path.WalkStep(direction, steps, allow_unsafe, after),))
    
    @classmethod
    def to_col(cls, col: int, *,
               allow_unsafe: bool = False,
               after: Optional[Ticks] = None) -> Path.Middle:
        return Path.Middle((Path.ToColStep(col, allow_unsafe, after),))
    @classmethod
    def to_row(cls, row: int, *,
               allow_unsafe: bool = False,
               after: Optional[Ticks] = None) -> Path.Middle:
        return Path.Middle((Path.ToRowStep(row, allow_unsafe, after),))
    
    @classmethod
    def start(cls, process_type: MultiDropProcessType, *,
              after: Optional[Ticks] = None) -> Path.Middle:
        return Path.Middle((Path.StartProcessStep(process_type, after=after),))
        
    @classmethod
    def join(cls, *,
             after: Optional[Ticks] = None) -> Path.Middle:
        return Path.Middle((Path.JoinProcessStep(after=after),))
    
    in_mix = join
    
    @classmethod
    def then_process(cls, fn: Callable[[Drop], Any]) -> Path.Middle:
        return Path.Middle((Path.CallStep(fn),))
    
    @classmethod
    def enter_well(cls, *,
                   after: Optional[Ticks] = None) -> Path.End:
        return Path.End((), Path.EnterWellStep(after=after))

    
        
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
            
    class StartProcessStep(MiddleStep):
        def __init__(self, process_type: MultiDropProcessType,
                     after: Optional[Ticks] = None) -> None:
            super().__init__(StartProcess(process_type), after)
    # class MixStep(StartProcessStep):
    #     def __init__(self, mix_type: MixingType,
    #                  result: Optional[Reagent] = None,
    #                  tolerance: float = 0.1,
    #                  n_shuttles: int = 0, 
    #                  fully_mix: Union[bool, Sequence[int]] = False,
    #                  after: Optional[Ticks] = None) -> None:
    #         super().__init__(MixProcess(mix_type, result=result,
    #                                     tolerance=tolerance,
    #                                     n_shuttles=n_shuttles,
    #                                     fully_mix=fully_mix), 
    #                                     after)
    class JoinProcessStep(MiddleStep):
        def __init__(self, 
                     after: Optional[Ticks] = None) -> None:
            super().__init__(JoinProcess(), after)
        
            
    class CallStep(MiddleStep):
        def __init__(self, fn: Callable[[Drop], Any],
                     after: Optional[Ticks] = None) -> None:
            def fn2(drop: Drop) -> Delayed[Drop]:
                future = Delayed[Drop]()
                fn(drop)
                future.post(drop)
                return future
            super().__init__(ComputeOp[Drop,Drop](fn2), after)

