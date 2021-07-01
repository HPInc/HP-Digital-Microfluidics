from __future__ import annotations

from abc import ABC, abstractmethod
import math
from typing import Final, Optional, Union, Sequence, Iterator, ClassVar, Mapping

from mpam.device import Pad
from mpam.drop import Drop, DropStatus
from mpam.exceptions import MPAMError
from mpam.processes import MultiDropProcessType
from mpam.types import Reagent, Delayed, waste_reagent, Dir


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


