from __future__ import annotations
from mpam.types import Liquid, Dir, Delayed, RunMode, DelayType,\
    Operation, OpScheduler, XYCoord, unknown_reagent, Ticks, tick,\
    StaticOperation, Reagent, Callback, waste_reagent
from mpam.device import Pad, Board, Well, WellGroup, WellState
from mpam.exceptions import NoSuchPad, NotAtWell, MPAMError
from typing import Optional, Final, Union, Sequence, Callable, Mapping, ClassVar,\
    Iterator
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
                          ) -> Delayed[Drop]:
            board = drop.pad.board
            system = board.in_system()
            direction = self.direction
            steps = self.steps
            # allow_unsafe_motion = self.allow_unsafe_motion
            future = Delayed[Drop]()
            
            if steps == 0:
                future.post(drop)
                return future
                
            one_tick: Ticks = 1*tick
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
                        board.after_tick(lambda : future.post(drop))
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
                          ) -> Delayed[Drop]:
            board = drop.pad.board
            future = Delayed[Drop]()
                
            assert mode.is_gated
            def before_tick() -> None:
                # If all the other drops are waiting, this will install a callback on the next tick and then
                # call it immediately to do the first step.  Otherwise, that will happen when the last 
                # drop shows up.
                self.mix_type.start_mix(self, drop, future)
            board.before_tick(before_tick, delta=mode.gated_delay(after))
            return future
        
    def _update_pad_fn(self, from_pad: Pad, to_pad: Pad):
        def fn() -> None:
            assert from_pad.drop is self, f"Moved {self}, but thought it was at {from_pad}"
            assert to_pad.drop is None, f"Moving {self} to non-empty {to_pad}"
            # print(f"Moved drop from {from_pad} to {to_pad}")
            self.pad = to_pad
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
                          ) -> Delayed[Drop]:
            board = drop.pad.board
            future = Delayed[Drop]()
                
            assert mode.is_gated
            def before_tick() -> None:
                MixInstance.join_mix(drop, future, self.fully_mixed)
            board.before_tick(before_tick, delta=mode.gated_delay(after))
            return future

class MixSequenceStep(ABC):
    @abstractmethod
    def schedule(self, shuttle_no: int, mergep: bool,           # @UnusedVariable
                 drops: Sequence[Drop],                         # @UnusedVariable
                 pads: Sequence[Pad]) -> Mapping[Drop, float]:  # @UnusedVariable
        ...
    

class MixInstance:
    mix_type: Final[MixingType]
    tolerance: Final[float]
    result: Final[Optional[Reagent]]
    n_shuttles: Final[int]
    drops: Final[list[Optional[Drop]]]
    pad_indices: Final[Mapping[Pad, int]]
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
                 secondary_locs: Sequence[Pad],
                 ) -> None:
        self.mix_type = op.mix_type
        self.tolerance = op.tolerance
        self.result = op.result
        self.n_shuttles = op.n_shuttles
        self.futures = {lead_drop: lead_future}
        self.full_mix = { lead_drop }
        self.secondary_locs = secondary_locs
        self.board = lead_drop.pad.board
        self.drops = [None] * (len(secondary_locs)+1)
        self.drops[0] = lead_drop
        self.pad_indices = { p: i+1 for i,p in enumerate(secondary_locs)}
        # print(map_str(self.pad_indices))
        
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
                    self.drops[self.pad_indices[p]] = d
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
                inst.drops[inst.pad_indices[p]] = drop
                if fully_mixed:
                    inst.full_mix.add(drop)
                inst.pending_drops -= 1
                ready = inst.pending_drops == 0
        if ready:
            inst.run()
            
    def play_script(self) -> Iterator[Optional[Ticks]]:
        def checked(d: Optional[Drop]) -> Drop:
            assert d is not None
            return d
        drops = tuple(checked(d) for d in self.drops)
        i = self.mix_type.perform(full_mix = self.full_mix,
                                  tolerance = self.tolerance,
                                  drops = drops,
                                  n_shuttles = self.n_shuttles
                                  )
        one_tick = 1*tick
        while next(i):
            yield one_tick
        self.schedule_post()
        yield None
        
    def run(self) -> None: 
        iterator = self.play_script()
        
        # We're inside a before_tick, so we run the first step here.  Then we install
        # the callback before the next tick to do the rest
        after_first = next(iterator)
        assert after_first is not None
        self.board.before_tick(lambda: next(iterator))

               
        
    
    def schedule_post(self) -> None:
        def do_post() -> None:
            result = self.result
            for drop, future in self.futures.items():
                if drop in self.full_mix:
                    print(f"result is {drop.liquid}")
                    if result is not None:
                        drop.reagent = result
                else:
                    drop.reagent = waste_reagent
                future.post(drop)
        self.board.after_tick(do_post)
        
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
                print(f"Merging: now {l1.reagent}.  Error is {self.error}")
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
                 
class MixingBase(ABC):
    is_approximate: Final[bool]
    
    def __init__(self, *, is_approximate: bool) -> None:
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
    
    def start_mix(self, op: Drop.Mix, lead_drop: Drop, future: Delayed[Drop]) -> None:
        secondary = self.secondary_pads(lead_drop) 
        inst = MixInstance(op, lead_drop, future, secondary)
        if inst.install():
            inst.run()

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
    
    def __init__(self, script: MixSequence, *, is_approximate: bool):
        super().__init__(is_approximate = is_approximate)
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
        super().__init__(is_approximate = mix_type.is_approximate)
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
    
    def __init__(self, phases: MixPhases):
        approximate_phases = 0
        for phase in phases:
            if any(submix.is_approximate for submix in phase):
                approximate_phases += 1
        self.n_approximate = approximate_phases
        
        super().__init__(is_approximate = approximate_phases > 0)
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
            print(f"Adjusted tolerance is {tolerance}")
        
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
        super().__init__(Mix2.the_script, is_approximate = False)
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
        super().__init__(Mix3.the_script, is_approximate = True)
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
        super().__init__(phases)
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
        super().__init__(phases)
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
        super().__init__(phases)
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


