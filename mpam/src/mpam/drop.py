from __future__ import annotations
from mpam.types import Liquid, Dir, Delayed, RunMode, DelayType,\
    Operation, OpScheduler, XYCoord, unknown_reagent, Ticks, tick,\
    StaticOperation, Reagent, Callback, waste_reagent
from mpam.device import Pad, Board, Well, WellGroup, WellState
from mpam.exceptions import NoSuchPad, NotAtWell
from typing import Optional, Final, Union, Sequence, Callable, Mapping
from quantities.SI import uL
from threading import Lock
from quantities.dimensions import Volume
from enum import Enum, auto
from mpam.engine import ClockCallback

class DropStatus(Enum):
    ON_BOARD = auto()
    IN_WELL = auto()
    IN_MIX = auto()

class Drop(OpScheduler['Drop']):
    liquid: Liquid
    pad: Pad
    status: DropStatus
    
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
        self.pad = pad
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
                      future: Optional[Delayed[Drop]] = None
                      ) -> Delayed[Drop]:
            if future is None:
                future = Delayed[Drop]()
            real_future = future
            assert mode.is_gated
            pad = self.pad
            def make_drop(_) -> None:
                drop = Drop(pad=pad, liquid=self.liquid)
                if post_result:
                    real_future.post(drop)
            pad.schedule(Pad.TurnOn, mode=mode, after=after) \
                .then_call(make_drop)
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
                    # print(f"Moving drop from {last_pad} to {next_pad}")
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
                drop.status = DropStatus.IN_WELL
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
        
            
    class Mix(Operation['Drop','Drop']):
        mix_type: Final[MixingType]
        result: Final[Optional[Reagent]]
        tolerance: Final[float]
        n_shuttles: Final[int]
        
        def __repr__(self) -> str:
            return f"<Drop.Mix: {self.mix_type}, result={self.result}, tol={self.tolerance:%}, shuttles:{self.n_shuttles}>"
        
        def __init__(self, mix_type: MixingType, *,
                     result: Optional[Reagent] = None,
                     tolerance: float = 0.1,
                     n_shuttles: int = 0) -> None:
            self.mix_type = mix_type
            self.result = result
            self.tolerance = tolerance
            self.n_shuttles = n_shuttles

        def _schedule_for(self, drop: Drop, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,  # @UnusedVariable
                          future: Optional[Delayed[Drop]] = None
                          ) -> Delayed[Drop]:
            board = drop.pad.board
            if future is None:
                future = Delayed[Drop]()
                
            real_future: Delayed[Drop] = future
            assert mode.is_gated
            def before_tick() -> None:
                # If all the other drops are waiting, this will install a callback on the next tick and then
                # call it immediately to do the first step.  Otherwise, that will happen when the last 
                # drop shows up.
                self.mix_type.start_mix(self, drop, real_future)
            board.before_tick(before_tick, delta=mode.gated_delay(after))
            return future
        
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
    
    class InMix(Operation['Drop','Drop']):
        fully_mixed: Final[bool]
        
        def __repr__(self) -> str:
            return f"<Drop.InMix: fully_mixed={self.fully_mixed}>"
        
        def __init__(self, *, fully_mixed = False) -> None:
            self.fully_mixed = fully_mixed

        def _schedule_for(self, drop: Drop, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,  # @UnusedVariable
                          future: Optional[Delayed[Drop]] = None
                          ) -> Delayed[Drop]:
            board = drop.pad.board
            if future is None:
                future = Delayed[Drop]()
                
            real_future: Delayed[Drop] = future
            assert mode.is_gated
            def before_tick() -> None:
                MixInstance.join_mix(drop, real_future, self.fully_mixed)
            board.before_tick(before_tick, delta=mode.gated_delay(after))
            return future


class MixInstance:
    mix_type: Final[MixingType]
    tolerance: Final[float]
    result: Final[Optional[Reagent]]
    n_shuttles: Final[int]
    futures: Final[dict[Drop, Delayed[Drop]]]
    full_mix: Final[set[Drop]]
    secondary_locs: Final[Sequence[Pad]]
    board: Final[Board]
    pending_drops: int
    
    global_lock: Final[Lock] = Lock()
    
    def __init__(self, 
                 op: Drop.Mix,
                 lead_drop: Drop,
                 lead_future: Delayed[Drop],
                 secondary_locs: Sequence[Pad]
                 ) -> None:
        self.mix_type = op.mix_type
        self.tolerance = op.tolerance
        self.result = op.result
        self.n_shuttles = op.n_shuttles
        self.futures = {lead_drop: lead_future}
        self.full_mix = { lead_drop }
        self.secondary_locs = secondary_locs
        self.board = lead_drop.pad.board
        
    def install(self) -> bool:
        pending_drops = 0
        with self.global_lock:
            for p in self.secondary_locs:
                t: Optional[tuple[Delayed[Drop], bool]] = getattr(p, "_waiting_for_mix", None)
                if t is None:
                    setattr(p, "_mix_waiting", self)
                    pending_drops += 1
                else:
                    setattr(p, "_waiting_for_mix", None)
                    d = p.drop
                    assert d is not None
                    self.futures[d] = t[0]
                    if t[1]:
                        self.full_mix.add(d)
            if pending_drops > 0:
                self.pending_drops = pending_drops
            return pending_drops == 0
        
    
    @classmethod        
    def join_mix(cls, drop: Drop, future: Delayed[Drop], fully_mixed: bool) -> None:
        ready: bool = False
        with cls.global_lock:
            p = drop.pad
            inst: Optional[MixInstance] = getattr(p, "_mix_waiting", None)
            if inst is None:
                setattr(p, "_waiting_for_mix", (future, fully_mixed))
                return
            else:
                setattr(p, "_mix_waiting", None)
                inst.futures[drop] = future
                if fully_mixed:
                    inst.full_mix.add(drop)
                inst.pending_drops -= 1
                ready = inst.pending_drops == 0
        if ready:
            inst.run()
               
    def stepper(self) -> ClockCallback:
        raise NotImplementedError()
    
    def run(self) -> None: 
        cb = self.stepper()
        # We're inside a before_tick, so we run the first step here.  Then we install
        # the callback before the next tick to do the rest
        after_first = cb()
        assert after_first is not None
        self.board.before_tick(cb)
        
    def pairwise_merge(self, pad1: Pad, middle: Pad, pad2: Pad, *,
                       result: Optional[Reagent] = None) -> None:
        drop1 = pad1.drop
        assert drop1 is not None
        drop2 = pad2.drop
        assert drop2 is not None

        l1 = drop1.liquid
        l2 = drop2.liquid
        real_drop1 = drop1
        real_drop2 = drop2
        def update(_) -> None:
            real_drop2.status = DropStatus.IN_MIX
            l1.mix_in(l2, result=result)
            
            pad1.drop = None
            pad2.drop = None 
            real_drop1.pad = middle 
            middle.drop = real_drop1
            setattr(middle, "_stashed_drop", real_drop2)
        
        pad1.schedule(Pad.TurnOff, post_result=False)
        pad2.schedule(Pad.TurnOff, post_result=False)
        middle.schedule(Pad.TurnOn).then_call(update)
        
    def pairwise_split(self, pad1: Pad, middle: Pad, pad2: Pad) -> None:
        drop1 = middle.drop
        assert drop1 is not None
        drop2 = getattr(middle, "_stashed_drop")
        assert drop2 is not None

        l1 = drop1.liquid
        l2 = drop2.liquid
        real_drop1 = drop1
        real_drop2 = drop2
        def update(_) -> None:
            l1.split_to(l2)
            real_drop2.status = DropStatus.ON_BOARD
            pad1.drop = real_drop1
            real_drop1.pad = pad1
            pad2.drop = real_drop2
            real_drop2.pad = pad2
            middle.drop = None
            setattr(middle, "_stashed_drop", None)
        
        pad1.schedule(Pad.TurnOff, post_result=False)
        pad2.schedule(Pad.TurnOff, post_result=False)
        middle.schedule(Pad.TurnOn).then_call(update)
        
    class Step:
        def run(self, shuttle_no: int, mergep: bool, drops: Sequence[Drop]) -> Mapping[Drop, float]:
            raise NotImplementedError()
        
    class MixStep:
        d1_index: Final[int]
        d2_index: Final[int]
        error: Final[float]
        def __init__(self, drop1: int, drop2: int, error: float) -> None:
            self.d1_index = drop1
            self.d2_index = drop2
            self.error = error
            
                
        def run(self, shuttle_no: int, mergep: bool, drops: Sequence[Drop]) -> Mapping[Drop, float]:  # @UnusedVariable
            drop1 = drops[self.d1_index]
            drop2 = drops[self.d2_index]
            pad1 = drop1.pad
            pad2 = drop2.pad
            middle = pad1.between_pads[pad2]
            l1 = drop1.liquid
            l2 = drop2.liquid
            if mergep:
                def update(_) -> None:
                    drop2.status = DropStatus.IN_MIX
                    l1.mix_in(l2)
                    pad1.drop = None
                    pad2.drop = None
                    drop1.pad = middle
                    middle.drop = drop1
                pad1.schedule(Pad.TurnOff, post_result = False)
                pad2.schedule(Pad.TurnOff, post_result = False)
                middle.schedule(Pad.TurnOn).then_call(update)
            else:
                def update(_) -> None:
                    l1.split_to(l2)
                    drop2.status = DropStatus.ON_BOARD
                    pad1.drop = drop1
                    drop1.pad = pad1
                    pad2.drop = drop2
                    drop2.pad = pad2
                    middle.drop = None
                pad1.schedule(Pad.TurnOn, post_result = False)
                pad2.schedule(Pad.TurnOn, post_result = False)
                middle.schedule(Pad.TurnOff).then_call(update)
            e = self.error
            return {drop1: e, drop2: e}
                
                
        
    def schedule_post(self) -> None:
        def do_post() -> None:
            result = self.result
            for drop, future in self.futures.items():
                if drop in self.full_mix:
                    if result is not None:
                        drop.reagent = result
                else:
                    drop.reagent = waste_reagent
                future.post(drop)
        self.board.after_tick(do_post)

class MixingType:
    def start_mix(self, op: Drop.Mix, lead_drop: Drop, future: Delayed[Drop]) -> None:
        inst = self.new_instance(op, lead_drop, future)
        if inst.install():
            inst.run()
    
    def new_instance(self, op: Drop.Mix, lead_drop: Drop, future: Delayed[Drop]) -> MixInstance:
        raise NotImplementedError()

class Mix2(MixingType):
    to_second: Final[Dir]
    
    def __init__(self, to_second: Dir) -> None:
        self.to_second = to_second
        
    def new_instance(self, op: Drop.Mix, lead_drop: Drop, future: Delayed[Drop]) -> MixInstance:
        return self.Inst(op, lead_drop, future, self.to_second)
    

    class Inst(MixInstance):
        lead_pad: Final[Pad]
        other_pad: Final[Pad]
        middle_pad: Final[Pad]
        
        @staticmethod
        def pads_to_use(drop: Drop, direction: Dir) -> tuple[Pad,Pad,Pad]:
            p1 = drop.pad
            p2 = p1.neighbor(direction)
            assert p2 is not None and p2.exists
            p3 = p2.neighbor(direction)
            assert p3 is not None and p3.exists
            return (p1, p2, p3)
        
        def __init__(self, 
                     op: Drop.Mix,
                     lead_drop: Drop,
                     lead_future: Delayed[Drop],
                     to_second: Dir
                     ) -> None:
            pads = self.pads_to_use(lead_drop, to_second)
            super().__init__(op, lead_drop, lead_future, (pads[2],))
            self.lead_pad = pads[0]
            self.middle_pad = pads[1]
            self.other_pad = pads[2]
            
        def stepper(self) -> ClockCallback:
            steps_remaining = 2*(self.n_shuttles+1)
            one_tick = 1*tick
            pad1 = self.lead_pad            
            pad2 = self.other_pad
            middle = self.middle_pad
            def cb() -> Optional[Ticks]:
                nonlocal steps_remaining
                if steps_remaining % 2 == 0:
                    self.pairwise_merge(pad1, middle, pad2)
                else:
                    self.pairwise_split(pad1, middle, pad2)
                steps_remaining -= 1
                if steps_remaining == 0:
                    self.schedule_post()
                    return None
                return one_tick
            return cb
            
        
    

