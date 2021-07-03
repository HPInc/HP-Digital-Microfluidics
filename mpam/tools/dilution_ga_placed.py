from __future__ import annotations
from argparse import ArgumentParser, Namespace
from typing import Final, Sequence, NamedTuple, Optional
import math
from random import randint, choice
from erk.stringutils import map_str
import random
from mpam.types import Dir, XYCoord, Orientation

class Mix(NamedTuple):
    drop: XYCoord
    direction: Dir
    
    def __repr__(self) -> str:
        return f"({self.drop.x},{self.drop.y})-{self.direction.name}"
    
class EvaluatedMix(NamedTuple):
    mix: Mix
    value: float

MixSeq = Sequence[Mix]
EvaluatedMixSeq = Sequence[EvaluatedMix]

class NamedMix(NamedTuple):
    step: int
    mix: Mix
    value: float
    d1: str
    d2: str
    
    def __repr__(self) -> str:
        return f"Mix({self.step}: {self.d1}{self.d2}, {self.mix}: {self.value})"


class Evaluation(NamedTuple):
    miss: float
    drops_used: int
    steps: int
    error: float
    useful_mixes: int
    
swap_p = dict[tuple[XYCoord, XYCoord], bool]()
def need_swap(d1: XYCoord, d2: XYCoord) -> bool:
    val = swap_p.get((d1,d2), None)
    if val is None:
        val = math.fabs(d2.x) < math.fabs(d1.x) or math.fabs(d2.y) < math.fabs(d1.y)
        swap_p[(d1,d2)] = val
    return val

class Candidate:
    mixes: Final[MixSeq]
    eval: Final[Evaluation]
    reduced: Final[EvaluatedMixSeq]
    
    
    @staticmethod
    def error_for(val: float, *, folds: float) -> float:
        return math.inf if val == 1 else val*(folds-1)/(1-val)-1

    @staticmethod
    def evaluate(mixes: MixSeq, *,
                 folds: float,
                 tolerance: float,
                 full: bool) -> tuple[Evaluation,EvaluatedMixSeq]:

        lead = XYCoord(0,0)
        
        current: dict[XYCoord,tuple[float, set[int]]] = {lead: (1,set())}
        error = Candidate.error_for(1, folds=folds)
        last_step = 0
        n_drops: int = math.ceil(folds)

        orientation = Orientation.NORTH_POS_EAST_POS
        values: list[float] = [-1] * len(mixes)
        
        
        for i,mix in enumerate(mixes):
            this_step = last_step
            last_step = last_step + 1
            d1 = mix.drop
            d2 = orientation.neighbor(mix.direction, d1)
            v1,used1 = current.get(d1, (0,set()))
            v2,used2 = current.get(d2, (0,set()))
            if v1 == v2:
                continue
            if full and len(current) == n_drops and (v1 == 0 or v2 == 0):
                continue
            val = (v1+v2)/2
            used = used1 | used2 | {this_step}
            current[d1] = current[d2] = (val, used)
            values[i] = val
            if full:
                if len(current) == n_drops:
                    min_val: float = 1
                    max_val: float = 0
                    assert isinstance(n_drops, int)
                    for val,used in current.values():
                        if val < min_val:
                            min_val = val
                        if val > max_val:
                            max_val = val
                    error = math.inf if min_val == 0 else max_val/min_val-1
                    if error < tolerance:
                        # print(f"drops: {n_drops}, max: {max_val}, min: {min_val}, error: {error}")
                        # print(current)
                        # assert False
                        break
            elif d1 == lead or d2 == lead:
                error = Candidate.error_for(val, folds=folds)
                if error < tolerance:
                    break
        if error < 0:
            error = -error
        miss = max(error-tolerance, 0)
        
        
        
        if full:
            useful_steps = set[int]()
            for s in current.values():
                useful_steps |= s[1] 
        else:
            useful_steps = current.get(XYCoord(0,0), (0, set()))[1]
        sorted_steps = list(useful_steps)
        sorted_steps.sort()
        # reduced = [remap_mix(m) for i,m in enumerate(mixes) if i in useful_steps]
        reduced = [EvaluatedMix(m, values[i]) for i,m in enumerate(mixes) if i in useful_steps]
        # if reduced and not reduced[0].value == 0.5:
            # assert False
            
        # used_drops = { XYCoord(0,0)}
        step_used = { XYCoord(0,0): 0 }
        max_step = 0
        for em in reduced:
            mix = em.mix
            d1 = mix.drop
            d2 = orientation.neighbor(mix.direction, d1)
            step_no = max(step_used.get(d1, 0), step_used.get(d2, 0)) + 1
            step_used[d1] = step_used[d2] = step_no
            if step_no > max_step:
                max_step = step_no
            # used_drops.add(d1)
            # used_drops.add(d2)

        return (Evaluation(miss, len(step_used)-1, max_step, error, len(reduced)), reduced)
    
    def reduced_mixes(self) -> Sequence[NamedMix]:
        next_drop = 1
        mapped_drops = {XYCoord(0,0): "A"}
        orientation = Orientation.NORTH_POS_EAST_POS
        
        last_set = dict[str, int]()
        
        def remap_drop(drop: XYCoord) -> str:
            nonlocal next_drop
            mapped: Optional[str] = mapped_drops.get(drop, None)
            if mapped is None:
                if next_drop < 26:
                    mapped = chr(ord("A")+next_drop)
                else:
                    mapped = f"<{next_drop}>"
                next_drop += 1
                mapped_drops[drop] = mapped
            return mapped
        def remap_mix(m: EvaluatedMix) -> NamedMix:
            mix = m.mix
            d1 = mix.drop
            d2 = orientation.neighbor(mix.direction, d1)
            s1 = remap_drop(d1)
            s2 = remap_drop(d2)
            step = max(last_set.get(s1, 0), last_set.get(s2, 0)) + 1
            last_set[s1] = last_set[s2] = step
            if need_swap(d1, d2):
                return NamedMix(step, Mix(d2, mix.direction.opposite), m.value, s2, s1)
            else:
                return NamedMix(step, mix, m.value, s1, s2)
            
        mixes = [remap_mix(m) for m in self.reduced]
        mixes.sort(key=lambda nm: (nm.step, nm.d1))
            
        return mixes
        
    
    @classmethod
    def generate(cls, *,
                 seq_len: int, 
                 radius: int, 
                 folds: int,
                 tolerance: float,
                 full: bool) -> Candidate:
        def random_mix() -> Mix:
            return Mix(XYCoord(randint(-radius, radius), 
                               randint(-radius, radius)),
                        choice(Dir.cardinals()))
        mixes = [random_mix() for _ in range(seq_len)]
        return Candidate(mixes, folds=folds, tolerance=tolerance, full=full)
        
    
    
    def __init__(self, mixes: MixSeq, *,
                 folds: int,
                 tolerance: float,
                 full: bool) -> None:
        self.mixes = mixes
        self.eval, self.reduced = self.evaluate(mixes, folds=folds, tolerance=tolerance, full=full)

    def cross(self, other: Candidate, *,
              folds: int,
              tolerance: float,
              full: bool,
              one_point: bool,
              preserve_size: bool,
              max_size: int) -> Candidate:

        def pick_point(c: Candidate) -> int:
            return randint(0, len(c.mixes))
        def pick_two(c: Candidate) -> tuple[int,int]:
            a = pick_point(c)
            b = pick_point(c)
            return (a,b) if a<=b else (b,a)
        
        mixes: list[Mix] = []
        if one_point:
            my_point = pick_point(self)
            their_point = my_point if preserve_size else pick_point(other)
            mixes.extend(self.mixes[:my_point])
            mixes.extend(other.mixes[:their_point])
        else:
            my_a, my_b = pick_two(self)
            their_a, their_b = (my_a,my_b) if preserve_size else pick_two(other)
            mixes.extend(self.mixes[:my_a])
            mixes.extend(other.mixes[their_a:their_b])
            mixes.extend(self.mixes[my_b:])
        if len(mixes) > max_size:
            mixes = mixes[:max_size]
        return Candidate(mixes, folds=folds, tolerance=tolerance, full=full)
            
            

class Monitor:
    best: Optional[Candidate] = None
    best_gen: int = 0
    def see(self, candidate: Candidate, gen: int) -> bool:
        best = self.best
        if best is None or candidate.eval < best.eval:
            self.best = candidate
            self.best_gen = gen
            print("---------")
            print(f"New best in generation {gen}: {candidate.eval}")
            print(f"  {map_str(candidate.reduced_mixes())}")
            return True
        return False
    
    
def tournament(size: int, pop: Sequence[Candidate]) -> tuple[Candidate,Candidate,int]:
    psize = len(pop)
    indexes = [random.randrange(psize) for _ in range(size)]
    indexes.sort(key = lambda i: pop[i].eval)
    return (pop[indexes[0]], pop[indexes[1]], indexes[-1])

def run(*, 
        folds: int,
        tolerance: float,
        full: bool,
        max_drops: int,  # @UnusedVariable
        radius: int,
        candidate_size: int,
        tourney_size: int,
        pop_size: int,
        max_gens: int,
        max_size: int,
        one_point: bool,
        preserve_size: bool) -> Candidate:
    monitor = Monitor()
    gen: int = 0
    def checked(c: Candidate) -> Candidate:
        monitor.see(c, gen)
        return c
    pop = [checked(Candidate.generate(seq_len = candidate_size,
                                      radius = radius,
                                      folds=folds,
                                      tolerance=tolerance,
                                      full=full)) for _ in range(pop_size)]
    for gen in range(1, max_gens):
        print(f"*** Generation {gen:,} ***")
        for _ in range(pop_size):
            m,f,worst = tournament(tourney_size, pop)
            new = m.cross(f, one_point=one_point, preserve_size=preserve_size,
                          max_size=max_size,
                          folds=folds, tolerance=tolerance, full=full)
            if new.eval < pop[worst].eval:
                pop[worst] = checked(new)
    
    best = monitor.best
    assert best is not None
    return best


if __name__ == '__main__':
    parser = ArgumentParser(description="Find optimal dilution sequences")
    parser.add_argument("folds", type=float, 
                        help="""The number of times to dilute (e.g., 8 for an 8x dilution).  
                                Does not need to be an integer""")
    default_radius = 5
    parser.add_argument("-r", "--radius", type=int, default=default_radius, metavar="INT",
                        help = f"The maximum deviation from the lead drop.  Default is {default_radius}")
    default_tolerance = 0.1
    parser.add_argument("-t", "--tolerance", type=float, default=default_tolerance, metavar="FLOAT",
                        help=f"The required tolerance.  Default it {default_tolerance:g} ({100*default_tolerance:g}%%)")
    default_drops = 20
    drops_group = parser.add_mutually_exclusive_group()
    drops_group.add_argument("-d", "--max-drops", type=int, default=default_drops, metavar="INT",
                             help=f"The maximum number of drops to use.  Default is {default_drops}.")
    drops_group.add_argument("-f", "--full", action="store_true",
                             help=f"Find sequence that evenly mixes all drops")
    default_size = 50
    parser.add_argument("-s", "--size", type=int, default=default_size, metavar="INT",
                        help=f"The initial length of candidate sequences.  Default is {default_size}.")
    default_ts = 7
    parser.add_argument("-ts", "--tourney-size", type=int, default=default_ts, metavar="INT",
                        help=f"The tournament size.  Default is {default_ts}.")
    default_ps = 20000
    parser.add_argument("-ps", "--pop-size", type=int, default=default_ps, metavar="INT",
                        help=f"The population size.  Default is {default_ps:,}.")
    default_mg = 100
    parser.add_argument("-mg", "--max-gens", type=int, default=default_mg, metavar="INT",
                        help=f"""The maximum number of generation equivalents to run.
                                 Default is {default_mg:,}.""")
    
    parser.add_argument("--one_point", action='store_true',
                        help=f"Use one-point crossover rather than two-point crossover")
    size_group = parser.add_mutually_exclusive_group()
    size_group.add_argument("--preserve_size", action='store_true',
                        help=f"Preserve candidate size during crossover")
    default_ms = 500
    size_group.add_argument("-ms", "--max-size", type=int, default=default_ms, metavar="INT",
                        help=f"""The maximum length of a candidate mixing sequence.
                                 Default is {default_ms:,}.""")
    

    args: Namespace = parser.parse_args()
    folds: int = args.folds
    tolerance: float = args.tolerance
    full: bool = args.full
    max_drops: int = math.ceil(folds)-1 if full else args.max_drops
    radius: int = args.radius
    size: int = args.size
    tourney_size: int = args.tourney_size
    pop_size: int = args.pop_size
    max_gens: int = args.max_gens
    max_size: int = args.max_size
    one_point: bool = args.one_point
    preserve_size: bool = args.preserve_size
    
    run(folds=folds, tolerance=tolerance, full=full, max_drops=max_drops, radius=radius,
        candidate_size=size, tourney_size=tourney_size, pop_size=pop_size,
        max_gens=max_gens, max_size=max_size, 
        one_point=one_point, preserve_size=preserve_size)
    
    # c = Candidate.generate(seq_len=size, n_drops=max_drops, folds=folds, tolerance=tolerance)
    # print(map_str(c.mixes))
    # print(map_str(c.reduced))
    # print(map_str(c.eval))
