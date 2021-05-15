from __future__ import annotations
from mpam.types import Liquid, Dir, Delayed, RunMode, DelayType,\
    Operation, OpScheduler, XYCoord, unknown_reagent
from mpam.device import Pad, Board
from mpam.exceptions import NoSuchPad, UnsafeMotion
from typing import Optional, Final, Union, Sequence
from quantities.SI import uL
from threading import Lock

class Drop(OpScheduler['Drop']):
    liquid: Liquid
    pad: Pad
    
    def __init__(self, pad: Pad, liquid: Liquid) -> None:
        assert pad.drop is None, f"Trying to create a second drop at {pad}"
        self.liquid = liquid
        self.pad = pad
        pad._drop = self
        
    def __repr__(self) -> str:
        return f"Drop[{self.pad}, {self.liquid}]"
    
    @classmethod
    def appear_at(self, board: Board, locations: Sequence[Union[XYCoord, tuple[int, int]]],
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
            with lock:
                nonlocal outstanding
                outstanding -= 1
                if outstanding == 0:
                    future.post(drops)
        with system.batched():
            for drop in drops:
                drop.pad.schedule(Pad.TurnOn).when_value(join)
        return future
        
    
    class Move(Operation['Drop','Drop']):
        direction: Final[Dir]
        steps: Final[int]
        allow_unsafe_motion: Final[bool]
        
        def _schedule_for(self, drop: Drop, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,
                          future: Optional[Delayed[Drop]] = None
                          ) -> Delayed[Drop]:
            board = drop.pad._board
            system = board.in_system()
            direction = self.direction
            steps = self.steps
            allow_unsafe_motion = self.allow_unsafe_motion
            if future is None:
                future = Delayed[Drop]()
            with system.batched():
                last_pad: Pad = drop.pad
                for step in range(steps):
                    next_pad = last_pad.neighbor(direction)
                    if next_pad is None or next_pad.broken:
                        raise NoSuchPad(last_pad.location+direction)
                    if not allow_unsafe_motion and not next_pad.safe():
                        raise UnsafeMotion(next_pad)
                    delay = mode.step_delay(after, step)
                    next_pad.schedule(Pad.TurnOn, mode=mode, post_result=False, after=delay)
                    last_pad.schedule(Pad.TurnOff, mode=mode, post_result=False, after=delay)
                    ufn = drop._update_pad_fn(last_pad, next_pad)
                    if mode.is_gated:
                        board.before_tick(ufn, delta=mode.gated_delay(after, step=step+1).count)
                    else:
                        delta = mode.asynchronous_delay(after, step=step+1)-0.1*mode.motion_time
                        board.call_after(delta, ufn)
                    last_pad = next_pad
                if post_result:
                    real_future: Delayed[Drop] = future
                    def post() -> None:
                        real_future.post(drop)
                    if mode.is_gated:
                        board.before_tick(post, delta=mode.gated_delay(after, step=steps).count)
                    else:
                        delta = mode.asynchronous_delay(after, step=steps+1)-0.1*mode.motion_time
                        board.call_after(delta, ufn)
                    # board.schedule(post, mode, after=delay)
            return future
        
        def __init__(self, direction: Dir, *, steps: int=1, allow_unsafe_motion: bool = False) -> None:
            self.direction = direction
            self.steps = steps
            self.allow_unsafe_motion = allow_unsafe_motion
            
    def _update_pad_fn(self, from_pad: Pad, to_pad: Pad):
        def fn() -> None:
            assert from_pad._drop is self, f"Moved {self}, but thought it was at {from_pad}"
            assert to_pad._drop is None, f"Moving {self} to non-empty {to_pad}"
            from_pad._drop = None
            self.pad = to_pad
            to_pad._drop = self
            print(f"Drop now at {to_pad}")
        return fn
