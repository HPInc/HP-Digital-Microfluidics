from __future__ import annotations
from mpam.types import Liquid, Dir, Delayed, RunMode, DelayType,\
    Operation, OpScheduler, XYCoord, unknown_reagent, Ticks, tick,\
    StaticOperation, Reagent, Callback
from mpam.device import Pad, Board, Well, WellGroup, WellState
from mpam.exceptions import NoSuchPad, NotAtWell
from typing import Optional, Final, Union, Sequence, Callable
from quantities.SI import uL
from threading import Lock
from quantities.dimensions import Volume

class Drop(OpScheduler['Drop']):
    liquid: Liquid
    pad: Pad
    exists: bool
    
    @property
    def volume(self) -> Volume:
        return self.liquid.volume
    
    @property
    def reagent(self) -> Reagent:
        return self.liquid.reagent
    
    def __init__(self, pad: Pad, liquid: Liquid) -> None:
        assert pad.drop is None, f"Trying to create a second drop at {pad}"
        self.liquid = liquid
        self.pad = pad
        self.exists = True
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
        
    
    class Move(Operation['Drop','Drop']):
        direction: Final[Dir]
        steps: Final[int]
        
        # I originally had an "allow_unsafe_motion" parameter that was used in a test to see whether 
        # a step would be in the neighborhood of a drop, but it was reasoning based on the current state,
        # so it really didn't make any sense.

        # allow_unsafe_motion: Final[bool]
        
        def __repr__(self) -> str:
            return f"<Drop.Move: {self.steps} {self.direction}>"
        
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
         
            
    class DispenseFrom(StaticOperation['Drop']):
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
                pad = self.well.exit_pad
                liquid = well.transfer_out(v)
                drop = Drop(pad=pad, liquid=liquid)
                if post_result:
                    real_future.post(drop)
                
                
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
                          future: Optional[Delayed[None]] = None
                          ) -> Delayed[None]:
            if future is None:
                future = Delayed[None]()
            real_future = future
            if self.well is None:
                if drop.pad.well is None:
                    raise NotAtWell(f"{drop} not at a well")
                well = drop.pad.well
            else:
                well = self.well
            def consume_drop(_) -> None:
                well.transfer_in(drop.liquid)
                drop.exists = False
                drop.pad.drop = None
                if post_result:
                    real_future.post(None)
                
                
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
            from_pad.drop = None
            self.pad = to_pad
            to_pad.drop = self
            # print(f"Drop now at {to_pad}")
        return fn
