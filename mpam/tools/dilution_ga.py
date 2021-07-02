from __future__ import annotations
from argparse import ArgumentParser, Namespace
from typing import Final, Sequence, NamedTuple, Optional
import math
from random import randint
from erk.stringutils import map_str
import random

class Mix:
    drops: Final[tuple[int,int]]
    value: float
    
    def __init__(self, drop1: int, drop2: int, *,
                 value: float = -1) -> None:
        self.drops = (drop1,drop2)
        self.value = value
        
    def __repr__(self) -> str:
        return f"Mix({self.drops[0]}, {self.drops[1]}: {self.value})"
    
    def useful(self, useful_drops: set[int]) -> bool:
        return self.drops[0] in useful_drops or self.drops[1] in useful_drops
    
    
MixSeq = Sequence[Mix]

class Evaluation(NamedTuple):
    miss: float
    drops_used: int
    useful_mixes: int
    error: float
    
class Candidate:
    mixes: Final[MixSeq]
    eval: Final[Evaluation]
    reduced: Final[MixSeq]
    
    
    @staticmethod
    def error_for(val: float, *, folds: float) -> float:
        return math.inf if val == 1 else val*(folds-1)/(1-val)-1

    @staticmethod
    def evaluate(mixes: MixSeq, *,
                 folds: float,
                 tolerance: float,
                 full: bool) -> tuple[Evaluation,MixSeq]:
        current: dict[int,tuple[float, set[int]]] = {0: (1,set())}
        error = Candidate.error_for(1, folds=folds)
        last_step = 0
        n_drops: int = math.ceil(folds)
        
        for mix in mixes:
            d1,d2 = mix.drops
            v1,used1 = current.get(d1, (0,set()))
            v2,used2 = current.get(d2, (0,set()))
            if v1 != v2:
                val = (v1+v2)/2
                used = used1 | used2 | {last_step}
                current[d1] = current[d2] = (val, used)
                mix.value = val
                if full:
                    min_val: float = 1
                    max_val: float = 0
                    assert isinstance(n_drops, int)
                    for d in range(n_drops):
                        val, used = current.get(d,(0,set()))
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
                elif d1 == 0 or d2 == 0:
                    error = Candidate.error_for(val, folds=folds)
                    if error < tolerance:
                        break
            last_step += 1
        if error < 0:
            error = -error
        miss = max(error-tolerance, 0)
        
        
        next_drop = 1
        mapped_drops = {0: 0}
        def remap_drop(drop: int) -> int:
            nonlocal next_drop
            mapped: Optional[int] = mapped_drops.get(drop)
            if mapped is None:
                mapped = next_drop
                next_drop += 1
                mapped_drops[drop] = mapped
            return mapped
        def remap_mix(m: Mix) -> Mix:
            drops = m.drops
            d0 = remap_drop(drops[0])
            d1 = remap_drop(drops[1])
            if d1 < d0:
                d1,d0 = d0,d1
            return Mix(d0, d1, value=m.value)
        
        useful_steps = range(0, last_step+1) if full else current.get(0, (0, set()))[1]
        reduced = [remap_mix(m) for i,m in enumerate(mixes) if i in useful_steps]

        return (Evaluation(miss, next_drop-1, len(reduced), error), reduced)
        

    @classmethod
    def generate(cls, *,
                 seq_len: int, 
                 n_drops: int, 
                 folds: int,
                 tolerance: float,
                 full: bool) -> Candidate:
        def random_mix() -> Mix:
            return Mix(randint(0, n_drops), randint(0,n_drops))
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
              preserve_size: bool) -> Candidate:

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
            print(f"  {map_str(candidate.reduced)}")
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
        max_drops: int,
        candidate_size: int,
        tourney_size: int,
        pop_size: int,
        max_gens: int,
        one_point: bool,
        preserve_size: bool) -> Candidate:
    monitor = Monitor()
    gen: int = 0
    def checked(c: Candidate) -> Candidate:
        monitor.see(c, gen)
        return c
    pop = [checked(Candidate.generate(seq_len = candidate_size,
                                      n_drops = max_drops,
                                      folds=folds,
                                      tolerance=tolerance,
                                      full=full)) for _ in range(pop_size)]
    for gen in range(1, max_gens):
        print(f"*** Generation {gen:,} ***")
        for _ in range(pop_size):
            m,f,worst = tournament(tourney_size, pop)
            new = m.cross(f, one_point=one_point, preserve_size=preserve_size,
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
    parser.add_argument("--preserve_size", action='store_true',
                        help=f"Preserve candidate size during crossover")
    

    args: Namespace = parser.parse_args()
    folds: int = args.folds
    tolerance: float = args.tolerance
    full: bool = args.full
    max_drops: int = math.ceil(folds)-1 if full else args.max_drops
    size: int = args.size
    tourney_size: int = args.tourney_size
    pop_size: int = args.pop_size
    max_gens: int = args.max_gens
    one_point: bool = args.one_point
    preserve_size: bool = args.preserve_size
    
    run(folds=folds, tolerance=tolerance, full=full, max_drops=max_drops, 
        candidate_size=size, tourney_size=tourney_size, pop_size=pop_size,
        max_gens=max_gens, one_point=one_point, preserve_size=preserve_size)
    
    # c = Candidate.generate(seq_len=size, n_drops=max_drops, folds=folds, tolerance=tolerance)
    # print(map_str(c.mixes))
    # print(map_str(c.reduced))
    # print(map_str(c.eval))
