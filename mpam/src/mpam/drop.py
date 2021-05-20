from __future__ import annotations
from mpam.types import Liquid, Dir, Delayed, RunMode, DelayType,\
    Operation, OpScheduler, XYCoord, unknown_reagent, Ticks, tick,\
    StaticOperation, Reagent
from mpam.device import Pad, Board, Well, WellGroup, WellState
from mpam.exceptions import NoSuchPad
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
        
        # I originally had an "allow_unsafe_motion" parameter that was used in a test to see whether 
        # a step would be in the neighborhood of a drop, but it was reasoning based on the current state,
        # so it really didn't make any sense.

        # allow_unsafe_motion: Final[bool]
        
        def _schedule_for(self, drop: Drop, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,
                          future: Optional[Delayed[Drop]] = None
                          ) -> Delayed[Drop]:
            board = drop.pad.board
            system = board.in_system()
            direction = self.direction
            steps = self.steps
            # allow_unsafe_motion = self.allow_unsafe_motion
            if future is None:
                future = Delayed[Drop]()
                
            one_tick: Ticks = 1*tick
            real_future: Delayed[Drop] = future
            assert mode.is_gated
            def before_tick() -> Optional[Ticks]:
                nonlocal steps
                last_pad = drop.pad
                with system.batched():
                    next_pad = last_pad.neighbor(direction)
                    # print(f"Moving from {last_pad} to {next_pad}")
                    if next_pad is None or next_pad.broken:
                        raise NoSuchPad(board.orientation.neighbor(direction, last_pad.location))
                    next_pad.schedule(Pad.TurnOn, mode=mode, post_result=False)
                    last_pad.schedule(Pad.TurnOff, mode=mode, post_result=False)
                    board.after_tick(drop._update_pad_fn(last_pad, next_pad))
                    steps -= 1
                    # print(f"steps is now {steps}")
                    if steps > 0:
                        return one_tick
                    if post_result:
                        board.after_tick(lambda : real_future.post(drop))
                return None
            board.before_tick(before_tick, delta=mode.gated_delay(after))
            return future
        
        def __init__(self, direction: Dir, *, steps: int = 1) -> None:
            self.direction = direction
            self.steps = steps
         
            
    class Dispense(StaticOperation['Drop']):
        well: Well
        
        
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      future: Optional[Delayed[Drop]] = None
                      ) -> Delayed[Drop]:
            if future is None:
                future = Delayed[Drop]()
            real_future = future
            well = self.well
            def make_drop(_) -> None:
                v = well.dispensed_volume
                in_well = well.contents
                r: Reagent  # @UnusedVariable
                r = in_well.reagent if in_well else unknown_reagent
                if in_well is None:
                    print(f"Dispensing from empty well {well}")
                    r = unknown_reagent
                else:
                    r = in_well.reagent
                    if in_well.volume < v:
                        print(f"Attempting to draw {v} from {well}, which only has {in_well.volume}")
                    in_well -= v
                drop = Drop(pad=self.well.exit_pad, liquid=Liquid(r, v))
                real_future.post(drop)
                
                
            # Note, we post the drop as soon as we get to the DISPENSED state, even theough
            # we continue on to READY
            group = self.well.group
            group.schedule(WellGroup.TransitionTo(WellState.DISPENSED, well = self.well), after=after) \
                .then_call(make_drop) \
                .then_schedule(WellGroup.TransitionTo(WellState.READY))
            return future
            
        
        def __init__(self, well: Well) -> None:
            self.well = well
            
    def _update_pad_fn(self, from_pad: Pad, to_pad: Pad):
        def fn() -> None:
            assert from_pad._drop is self, f"Moved {self}, but thought it was at {from_pad}"
            assert to_pad._drop is None, f"Moving {self} to non-empty {to_pad}"
            # print(f"Moved drop from {from_pad} to {to_pad}")
            from_pad._drop = None
            self.pad = to_pad
            to_pad._drop = self
            # print(f"Drop now at {to_pad}")
        return fn
