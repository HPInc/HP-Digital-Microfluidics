from __future__ import  annotations

from re import Pattern, Match
import re
from typing import Final, Optional, Callable, Any, Union, Iterable, Sequence, \
    overload

from mpam.device import Well, ExtractionPoint, Pad, System, Board, \
    ProductLocation, BoardComponent
from mpam.drop import Drop, DropComputeOp
from mpam.processes import StartProcess, JoinProcess, MultiDropProcessType
from mpam.types import StaticOperation, Operation, Delayed, \
    DelayType, schedule, Dir, Reagent, Liquid, XYCoord, Barrier, T, \
    WaitableType, Callback, Postable, WaitableType, NO_WAIT, CSOperation
from quantities.dimensions import Volume


Schedulable = Union['Path.Start', 'Path.Full',
                    tuple[Union[Drop, Delayed[Drop]],
                          Union['Path.Middle', 'Path.End']]]


class Path:
    class Step:
        after: Final[WaitableType]

        def __init__(self, after: WaitableType) -> None:
            self.after = after

    class StartStep(Step):
        op: Final[StaticOperation[Drop]]

        def __init__(self, op: StaticOperation[Drop], after: WaitableType) -> None:
            super().__init__(after=after)
            self.op = op

    class MiddleStep(Step):
        op: Final[Operation[Drop, Drop]]

        def __init__(self, op: Operation[Drop, Drop], after: WaitableType) -> None:
            super().__init__(after=after)
            self.op = op

        def _schedule_after(self, future: Delayed[Drop], *,
                            is_last: bool, post_result: bool) -> Delayed[Drop]:
            return future.then_schedule(self.op, after=self.after,
                                        post_result=post_result if is_last else True)

    class EndStep(Step):
        op: Final[CSOperation[Drop, None]]

        def __init__(self, op: CSOperation[Drop, None], after: WaitableType) -> None:
            super().__init__(after=after)
            self.op = op

        def _schedule_after(self, future: Delayed[Drop], *,
                            post_result: bool) -> Delayed[None]:
            return future.then_schedule(self.op, after=self.after,
                                        post_result=post_result)


    class Start(StaticOperation[Drop]):
        first_step: Final[Path.StartStep]
        middle_steps: Final[tuple[Path.MiddleStep, ...]]

        def __init__(self, start: Path.StartStep,
                     middle: tuple[Path.MiddleStep,...]) -> None:
            super().__init__(scheduler=start.op.scheduler)
            self.first_step = start
            self.middle_steps = middle

        @overload
        def __add__(self, other: Union[Path.MiddleStep, Path.Middle]) -> Path.Start: ... # @UnusedVariable
        @overload
        def __add__(self, other: Union[Path.EndStep, Path.End]) -> Path.Full: ... # @UnusedVariable
        def __add__(self, other: Union[Path.MiddleStep,
                                       Path.EndStep,
                                       Path.Middle,
                                       Path.End]):
            if isinstance(other, Path.MiddleStep):
                return Path.Start(self.first_step, self.middle_steps+(other,))
            if isinstance(other, Path.Middle):
                return Path.Start(self.first_step, self.middle_steps+other.middle_steps)
            if isinstance(other, Path.EndStep):
                return Path.Full(self.first_step, self.middle_steps, other)
            return Path.Full(self.first_step, self.middle_steps+other.middle_steps, other.last_step)

        # def _extend(self, step: Path.MiddleStep) -> Path.Start:
        #     return Path.Start(start=self.first_step, middle = self.middle_steps+(step,))

        def _schedule(self, *, post_result: bool = True) -> Delayed[Drop]:
            middle = self.middle_steps
            last = len(middle) - 1
            future = schedule(self.first_step.op,
                              after=self.first_step.after,
                              post_result=post_result if last == -1 else True)
            for i,step in enumerate(middle):
                future = step._schedule_after(future, post_result=post_result, is_last = i==last)
            return future

        def walk(self, direction: Dir, *,
                 steps: int = 1,
                 allow_unsafe: bool = False,
                 after: WaitableType = NO_WAIT) -> Path.Start:
            return self+Path.WalkStep(
                direction, steps=steps, allow_unsafe=allow_unsafe, after=after)
        def to_col(self, col: int, *,
                   allow_unsafe: bool = False,
                   after: WaitableType = NO_WAIT) -> Path.Start:
            return self+Path.ToColStep(col, allow_unsafe=allow_unsafe, after=after)
        def to_row(self, row: int, *,
                   allow_unsafe: bool = False,
                   after: WaitableType = NO_WAIT) -> Path.Start:
            return self+Path.ToRowStep(row, allow_unsafe=allow_unsafe, after=after)

        def to_pad(self, target: Union[Pad, XYCoord, tuple[int, int]],
                   *,
                   row_first: bool = True,
                   allow_unsafe: bool = False,
                   after: WaitableType = NO_WAIT) -> Path.Start:
            r: int
            c: int
            if isinstance(target, Pad):
                r,c = target.row, target.column
            elif isinstance(target, XYCoord):
                r,c = target.row, target.col
            else:
                c,r = target
            if row_first:
                return self.to_row(r, allow_unsafe=allow_unsafe, after=after).to_col(c)
            else:
                return self.to_col(c, allow_unsafe=allow_unsafe, after=after).to_row(r)


        def start(self, process_type: MultiDropProcessType, *,
                  after: WaitableType = NO_WAIT) -> Path.Start:
            return self+Path.StartProcessStep(process_type, after=after)

        # def mix(self, mix_type: MixingType, *,
        #         result: Optional[Reagent] = None,
        #         tolerance: float = 0.1,
        #         n_shuttles: int = 0,
        #         fully_mix: Union[bool, Sequence[int]] = False,
        #         after: WaitableType = NO_WAIT) -> Path.Start:
        #     return self._extend(Path.MixStep(mix_type, result=result,
        #                                      tolerance=tolerance, n_shuttles=n_shuttles,
        #                                      fully_mix=fully_mix,
        #                                      after=after))
        def join(self, *,
                 after: WaitableType = NO_WAIT) -> Path.Start:
            return self+Path.JoinProcessStep(after=after)

        in_mix = join

        def then_process(self, fn: Callable[[Drop], Any], *,
                         after: WaitableType = NO_WAIT) -> Path.Start:
            return self+Path.CallStep(fn, after=after)

        def then_do(self, fn: Callable[[Drop], Delayed[T]], *,
                    after: WaitableType = NO_WAIT) -> Path.Start:
            return self+Path.CallAndWaitStep(fn, after=after)

        def enter_well(self, *,
                       after: WaitableType = NO_WAIT) -> Path.Full:
            return self+Path.EnterWellStep(after=after)

        def teleport_out(self, *,
                         volume: Optional[Volume] = None,
                         product_loc: Optional[Postable[ProductLocation]] = None,
                         after: WaitableType = NO_WAIT) -> Path.Full:
            return self+Path.TeleportOutStep(volume=volume, after=after, product_loc=product_loc)

        def reach(self, barrier: Barrier, *, wait: bool = True,
                  after: WaitableType = NO_WAIT) -> Path.Start:
            return self+Path.BarrierStep(barrier, wait=wait, after=after)

        def wait_for(self, waitable: WaitableType, *,
                     after: WaitableType = NO_WAIT) -> Path.Start:
            return self+Path.PauseStep(waitable, after=after)

        def extended(self, path: Path.Middle) -> Path.Start:
            return self+path

    class Middle(CSOperation[Drop, Drop]):
        middle_steps: Final[tuple[Path.MiddleStep, ...]]

        def __init__(self, middle: tuple[Path.MiddleStep, ...]) -> None:
            self.middle_steps =  middle

        @overload
        def __add__(self, other: Union[Path.MiddleStep, Path.Middle]) -> Path.Middle: ... # @UnusedVariable
        @overload
        def __add__(self, other: Union[Path.EndStep, Path.End]) -> Path.End: ... # @UnusedVariable
        def __add__(self, other: Union[Path.MiddleStep,
                                       Path.EndStep,
                                       Path.Middle,
                                       Path.End]):
            if isinstance(other, Path.MiddleStep):
                return Path.Middle(self.middle_steps+(other,))
            if isinstance(other, Path.Middle):
                return Path.Middle(self.middle_steps+other.middle_steps)
            if isinstance(other, Path.EndStep):
                return Path.End(self.middle_steps, other)
            return Path.End(self.middle_steps+other.middle_steps, other.last_step)

        # def _extend(self, step: Path.MiddleStep) -> Path.Middle:
            # return Path.Middle(self.middle_steps+(step,))

        def _schedule_for(self, obj: Drop, *,
                          post_result: bool = True,
                          ) -> Delayed[Drop]:
            future = Delayed.complete(obj)
            middle = self.middle_steps
            last = len(middle) - 1
            for i,step in enumerate(middle):
                future = step._schedule_after(future, post_result=post_result, is_last = i==last)
            return future

        def walk(self, direction: Dir, *,
                 steps: int = 1,
                 allow_unsafe: bool = False,
                 after: WaitableType = NO_WAIT) -> Path.Middle:
            return self+Path.WalkStep(
                direction, steps=steps, allow_unsafe=allow_unsafe, after=after)
        def to_col(self, col: int, *,
                   allow_unsafe: bool = False,
                   after: WaitableType = NO_WAIT) -> Path.Middle:
            return self+Path.ToColStep(col, allow_unsafe=allow_unsafe, after=after)
        def to_row(self, row: int, *,
                   allow_unsafe: bool = False,
                   after: WaitableType = NO_WAIT) -> Path.Middle:
            return self+Path.ToRowStep(row, allow_unsafe=allow_unsafe, after=after)

        def to_pad(self, target: Union[Pad, XYCoord, tuple[int, int]],
                   *,
                   row_first: bool = True,
                   allow_unsafe: bool = False,
                   after: WaitableType = NO_WAIT) -> Path.Middle:
            r: int
            c: int
            if isinstance(target, Pad):
                r,c = target.row, target.column
            elif isinstance(target, XYCoord):
                r,c = target.row, target.col
            else:
                c,r = target
            if row_first:
                return self.to_row(r, allow_unsafe=allow_unsafe, after=after).to_col(c)
            else:
                return self.to_col(c, allow_unsafe=allow_unsafe, after=after).to_row(r)

        def start(self, process_type: MultiDropProcessType, *,
                  after: WaitableType = NO_WAIT) -> Path.Middle:
            return self+Path.StartProcessStep(process_type, after=after)

        # def mix(self, mix_type: MixingType, *,
        #         result: Optional[Reagent] = None,
        #         tolerance: float = 0.1,
        #         n_shuttles: int = 0,
        #         fully_mix: Union[bool, Sequence[int]] = True,
        #         after: WaitableType = NO_WAIT) -> Path.Middle:
        #     return self._extend(Path.MixStep(mix_type, result=result,
        #                                      tolerance=tolerance, n_shuttles=n_shuttles,
        #                                      fully_mix=fully_mix,
        #                                      after=after))
        #

        def join(self, *,
                 after: WaitableType = NO_WAIT) -> Path.Middle:
            return self+Path.JoinProcessStep(after=after)

        in_mix = join

        def then_process(self, fn: Callable[[Drop], Any], *,
                         after: WaitableType = NO_WAIT) -> Path.Middle:
            return self+Path.CallStep(fn, after=after)

        def then_do(self, fn: Callable[[Drop], Delayed[T]],
                    after: WaitableType = NO_WAIT) -> Path.Middle:
            return self+Path.CallAndWaitStep(fn, after=after)

        def enter_well(self, *,
                       after: WaitableType = NO_WAIT) -> Path.End:
            return self+Path.EnterWellStep(after=after)

        def teleport_out(self, *,
                         volume: Optional[Volume] = None,
                         product_loc: Optional[Postable[ProductLocation]] = None,
                         after: WaitableType = NO_WAIT) -> Path.End:
            return self+Path.TeleportOutStep(volume=volume, after=after, product_loc=product_loc)

        def reach(self, barrier: Barrier, *,
                  wait: bool = True, after: WaitableType = NO_WAIT) -> Path.Middle:
            return self+Path.BarrierStep(barrier, wait=wait, after=after)

        def wait_for(self, waitable: WaitableType, *,
                     after: WaitableType = NO_WAIT) -> Path.Middle:
            return self+Path.PauseStep(waitable, after=after)

        def extended(self, path: Path.Middle) -> Path.Middle:
            return self+path

    class End(CSOperation[Drop, None]):
        middle_steps: Final[tuple[Path.MiddleStep,...]]
        last_step: Final[Path.EndStep]

        def __init__(self,
                     middle: tuple[Path.MiddleStep,...],
                     end: Path.EndStep) -> None:
            self.middle_steps = middle
            self.last_step = end

        def _schedule_for(self, obj: Drop, *,
                          post_result: bool = True,
                          ) -> Delayed[None]:
            future = Delayed.complete(obj)
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
            super().__init__(scheduler=start.op.scheduler)
            self.first_step = start
            self.middle_steps = middle
            self.last_step = end

        def _schedule(self, *,
                      post_result: bool = True,
                      ) -> Delayed[None]:
            middle = self.middle_steps
            future = schedule(self.first_step.op, post_result = True)
            for step in middle:
                future = step._schedule_after(future, post_result=True, is_last = False)
            return self.last_step._schedule_after(future, post_result=post_result)


    @classmethod
    def empty(cls) -> Path.Middle:
        return Path.Middle(())

    @classmethod
    def dispense_from(cls, well: Well, *,
                      after_reservation: Optional[Callback] = None,
                      before_release: Optional[Callback] = None,
                      after: WaitableType = NO_WAIT) -> Path.Start:
        return Path.Start(Path.DispenseStep(well, after_reservation=after_reservation,
                                            before_release=before_release,
                                            after=after), ())

    @classmethod
    def teleport_into(cls, extraction_point: ExtractionPoint, *,
                      liquid: Optional[Liquid] = None,
                      reagent: Optional[Reagent] = None,
                      after: WaitableType = NO_WAIT) -> Path.Start:
        return Path.Start(
            Path.TeleportInStep(
                extraction_point, liquid=liquid, reagent=reagent, after=after),
            ())

    @classmethod
    def appear_at(cls, pad: Union[Pad, XYCoord, tuple[int, int]], *,
                  board: Board,
                  after: WaitableType = NO_WAIT,
                  liquid: Optional[Liquid] = None) -> Path.Start:
        return Path.Start(Path.AppearStep(pad, board=board, after=after, liquid=liquid), ())

    @classmethod
    def walk(cls, direction: Dir, *,
             steps: int = 1,
             allow_unsafe: bool = False,
             after: WaitableType = NO_WAIT) -> Path.Middle:
        return Path.Middle((Path.WalkStep(
            direction, steps=steps, allow_unsafe=allow_unsafe, after=after),))

    @classmethod
    def to_col(cls, col: int, *,
               allow_unsafe: bool = False,
               after: WaitableType = NO_WAIT) -> Path.Middle:
        return Path.Middle((Path.ToColStep(
            col, allow_unsafe=allow_unsafe, after=after),))
    @classmethod
    def to_row(cls, row: int, *,
               allow_unsafe: bool = False,
               after: WaitableType = NO_WAIT) -> Path.Middle:
        return Path.Middle((Path.ToRowStep(
            row, allow_unsafe=allow_unsafe, after=after),))

    @classmethod
    def to_pad(cls, target: Union[Pad, XYCoord, tuple[int, int]],
               *,
               row_first: bool = True,
               allow_unsafe: bool = False,
               after: WaitableType = NO_WAIT) -> Path.Middle:
        r: int
        c: int
        if isinstance(target, Pad):
            r,c = target.row, target.column
        elif isinstance(target, XYCoord):
            r,c = target.row, target.col
        else:
            c,r = target
        if row_first:
            return Path.to_row(r, allow_unsafe=allow_unsafe, after=after).to_col(c)
        else:
            return Path.to_col(c, allow_unsafe=allow_unsafe, after=after).to_row(r)

    @classmethod
    def start(cls, process_type: MultiDropProcessType, *,
              after: WaitableType = NO_WAIT) -> Path.Middle:
        return Path.Middle((Path.StartProcessStep(process_type, after=after),))

    @classmethod
    def join(cls, *,
             after: WaitableType = NO_WAIT) -> Path.Middle:
        return Path.Middle((Path.JoinProcessStep(after=after),))

    in_mix = join

    @classmethod
    def then_process(cls, fn: Callable[[Drop], Any], *,
                     after: WaitableType = NO_WAIT) -> Path.Middle:
        return Path.Middle((Path.CallStep(fn, after=after),))

    @classmethod
    def enter_well(cls, *,
                   after: WaitableType = NO_WAIT) -> Path.End:
        return Path.End((), Path.EnterWellStep(after=after))

    @classmethod
    def schedule_paths(cls, paths: Iterable[Schedulable], *,
                       system: System,
                       after: WaitableType = NO_WAIT,
                       ) -> Sequence[Union[Delayed[Drop], Delayed[None]]]:
        def scheduled(path: Schedulable) -> Union[Delayed[Drop], Delayed[None]]:
            if isinstance(path, Path.Start) or isinstance(path, Path.Full):
                return path.schedule(after=after)
            else:
                return path[1].schedule_for(path[0], after=after)
        with system.batched():
            return [scheduled(p) for p in paths]

    @classmethod
    def run_paths(cls, paths: Iterable[Schedulable], *,
                  system: System,
                  after: WaitableType = NO_WAIT,
                  ) -> Sequence[Drop]:
        values = (f.value for f in cls.schedule_paths(
            paths, system=system, after=after))
        return [d for d in values if d is not None]

    @classmethod
    def from_spec(cls, spec: str, *, start: Union[Well, Pad]) -> tuple[Middle, Pad, int]:
        current_pad = start.exit_pad if isinstance(start, Well) else start
        step_re: Pattern = re.compile(' *(\\d*)([UDLRNSEW]) *')
        spec = spec.upper()
        full_spec = spec

        path = cls.empty()
        steps = 0

        dirs = {
            'U': Dir.UP, 'N': Dir.UP,
            'D': Dir.DOWN, 'S': Dir.DOWN,
            'R': Dir.RIGHT, 'E': Dir.RIGHT,
            'L': Dir.LEFT, 'W': Dir.WEST,
            }

        while spec:
            m: Optional[Match[str]] = step_re.match(spec)
            if m is None:
                raise ValueError(f"Couldn't parse '{spec}' in '{full_spec}'")
            spec = spec[m.end():]
            n = int(m.group(1)) if len(m.group(1)) else 1
            d = m.group(2)

            steps += n
            direction = dirs[d]

            path = path.walk(direction, steps=n)
            for i in range(n):  # @UnusedVariable
                p = current_pad.neighbor(direction)
                if p is None:
                    raise ValueError(f"Can't walk {d} ({direction}) from {current_pad} in '{full_spec}'")
                current_pad = p

        return (path, current_pad, steps)


    class DispenseStep(StartStep):
        def __init__(self, well: Well, *,
                     after: WaitableType,
                     after_reservation: Optional[Callback] = None,
                     before_release: Optional[Callback] = None) -> None:
            super().__init__(
                Drop.DispenseFrom(well, after_reservation=after_reservation, before_release=before_release),
                after=after)
    class TeleportInStep(StartStep):
        def __init__(self, extraction_point: ExtractionPoint, *,
                     after: WaitableType,
                     liquid: Optional[Liquid] = None,
                     reagent: Optional[Reagent] = None
                     ) -> None:
            super().__init__(
                Drop.TeleportInTo(
                    extraction_point, liquid=liquid, reagent=reagent),
                after=after)
    class AppearStep(StartStep):
        def __init__(self, pad: Union[Pad, XYCoord, tuple[int, int]], *,
                     board: Board,
                     after: WaitableType,
                     liquid: Optional[Liquid] = None
                     ) -> None:
            super().__init__(Drop.AppearAt(pad, board=board, liquid=liquid),
                             after=after)

    class TeleportOutStep(EndStep):
        def __init__(self, *,
                     after: WaitableType,
                     volume: Optional[Volume] = None,
                     product_loc: Optional[Postable[ProductLocation]] = None,
                     ) -> None:
            super().__init__(Drop.TeleportOut(volume=volume, product_loc=product_loc), after)
    class EnterWellStep(EndStep):
        def __init__(self, *,
                     after: WaitableType) -> None:
            super().__init__(Drop.EnterWell(), after)


    class WalkStep(MiddleStep):
        def __init__(self, direction: Dir, *,
                     steps: int, allow_unsafe: bool, after: WaitableType) -> None:
            super().__init__(Drop.Move(direction, steps=steps, allow_unsafe=allow_unsafe), after)

    class ToColStep(MiddleStep):
        def __init__(self, col: int, *,
                     allow_unsafe: bool, after: WaitableType) -> None:
            super().__init__(Drop.ToCol(col, allow_unsafe=allow_unsafe), after)

    class ToRowStep(MiddleStep):
        def __init__(self, row: int, *,
                     allow_unsafe: bool, after: WaitableType) -> None:
            super().__init__(Drop.ToRow(row, allow_unsafe=allow_unsafe), after)

    class StartProcessStep(MiddleStep):
        def __init__(self, process_type: MultiDropProcessType, *,
                     after: WaitableType) -> None:
            super().__init__(StartProcess(process_type), after)
    # class MixStep(StartProcessStep):
    #     def __init__(self, mix_type: MixingType,
    #                  result: Optional[Reagent] = None,
    #                  tolerance: float = 0.1,
    #                  n_shuttles: int = 0,
    #                  fully_mix: Union[bool, Sequence[int]] = False,
    #                  after: WaitableType = NO_WAIT) -> None:
    #         super().__init__(MixProcess(mix_type, result=result,
    #                                     tolerance=tolerance,
    #                                     n_shuttles=n_shuttles,
    #                                     fully_mix=fully_mix),
    #                                     after)
    class JoinProcessStep(MiddleStep):
        def __init__(self, *,
                     after: WaitableType) -> None:
            super().__init__(JoinProcess(), after)


    class CallStep(MiddleStep):
        def __init__(self, fn: Callable[[Drop], Any], *,
                     after: WaitableType) -> None:
            def fn2(drop: Drop) -> Delayed[Drop]:
                future = Postable[Drop]()
                fn(drop)
                future.post(drop)
                return future
            super().__init__(DropComputeOp(fn2), after)

    class CallAndWaitStep(MiddleStep):
        def __init__(self, fn: Callable[[Drop], Delayed[Any]], *,
                     after: WaitableType) -> None:
            def fn2(drop: Drop) -> Delayed[Drop]:
                future = Postable[Drop]()
                fn(drop).then_call(lambda _: future.post(drop))
                return future
            super().__init__(DropComputeOp(fn2), after)

    class BarrierStep(MiddleStep):
        def __init__(self, barrier: Barrier, *,
                     wait: bool = True,
                     after: WaitableType) -> None:
            def pass_through(drop: Drop) -> Delayed[Drop]:
                future = Postable[Drop]()
                barrier.pass_through(drop)
                future.post(drop)
                return future
            op: Operation[Drop, Drop] = Drop.WaitAt(barrier) if wait else DropComputeOp(pass_through)
            super().__init__(op, after)

    class PauseStep(MiddleStep):
        def __init__(self, waitable: WaitableType, *,
                     after: WaitableType) -> None:
            super().__init__(Drop.WaitFor(waitable), after)
