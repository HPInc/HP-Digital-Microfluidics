from __future__ import annotations
from argparse import ArgumentParser, Namespace, ArgumentTypeError
from typing import Final, Sequence, NamedTuple, Optional, TextIO
import math
from random import randint, choice
from erk.stringutils import map_str
import random
from mpam.types import Dir, XYCoord, Orientation
from sys import stdout
from contextlib import redirect_stdout
import os.path
from quantities.timestamp import time_now

class Mix(NamedTuple):
    drop: XYCoord
    direction: Dir
    
    def __repr__(self) -> str:
        return f"({self.drop.x},{self.drop.y})-{self.direction.name}"
    
class EvaluatedMix(NamedTuple):
    mix: Mix
    error: float

MixSeq = Sequence[Mix]
EvaluatedMixSeq = Sequence[EvaluatedMix]
Mixture = Sequence[float]

class NamedMix(NamedTuple):
    step: int
    mix: Mix
    error: float
    d1: int
    d2: int
    
    def __repr__(self) -> str:
        def tag(i: int) -> str:
            return chr(ord("A")+i) if i < 26 else f"<{i}>"
        return f"Mix({self.step}: {tag(self.d1)}{tag(self.d2)}, {self.mix}: {self.error})"
    
        

    

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


def log_mixes(mixes: Sequence[NamedMix], *,
              evaluation: Evaluation,
              file: TextIO = stdout) -> None:
    orientation = Orientation.NORTH_POS_EAST_POS
    loc = dict[int, XYCoord]()
    steps = dict[int, list[NamedMix]]()
    for m in mixes:
        mix = m.mix
        loc[m.d1] = mix.drop
        loc[m.d2] = orientation.neighbor(mix.direction, mix.drop)
        s = steps.get(m.step, None)
        if s is None:
            s = steps[m.step] = []
        s.append(m)
    locs = "("+" ".join(f"({xy.x},{xy.y})," for _,xy in sorted(loc.items()))+")"

    with redirect_stdout(file):
        print() 
        print(f"# {evaluation}")
        print(f"MixingSeq({evaluation.error},")
        print(f"  {locs},")
        print(f"  (")
        for _, step_mixes in sorted(steps.items()):
            print("   (" 
                  + " ".join(f"PM({m.d1},{m.d2})," for m in step_mixes)
                  +"),")
        print("  ))")
        for m in mixes:
            print(f"# {m}") 


class Candidate:
    mixes: Final[MixSeq]
    eval: Final[Evaluation]
    reduced: Final[EvaluatedMixSeq]
    
    

    @staticmethod
    def evaluate(mixes: MixSeq, *,
                 n_drops: int,
                 tolerance: float,
                 slop: float,
                 full: bool) -> tuple[Evaluation,EvaluatedMixSeq]:

        lead = XYCoord(0,0)
        allowed = { lead }
        orientation = Orientation.NORTH_POS_EAST_POS
        
        def initial_val(n: int) -> Mixture:
            return tuple(1 if i==n else 0 for i in range(n_drops))
        next_drop = 0
        def next_val(d: XYCoord) -> Optional[Mixture]:
            nonlocal next_drop, allowed
            if next_drop == n_drops:
                return None
            val = initial_val(next_drop)
            next_drop += 1
            allowed |= { orientation.neighbor(direction, d) for direction in Dir.cardinals()}
            return val
        
        CurrentVal = tuple[Mixture, set[int], float]
        current: dict[XYCoord,CurrentVal] = {}
        
        last_step = 0

        errors: list[float] = [-1] * len(mixes)
        
        def error_for(val: Mixture) -> float:
            min_val = min(val)
            max_val = max(val)
            return math.inf if min_val == 0 else max_val/min_val-1
        
        error = math.inf
        for i,mix in enumerate(mixes):
            this_step = last_step
            last_step = last_step + 1
            d1 = mix.drop
            d2 = orientation.neighbor(mix.direction, d1)
            if d1 not in allowed and d2 not in allowed:
                continue
            v1,used1,e1 = current.get(d1, (next_val(d1),set[int](), math.inf))  # @UnusedVariable
            if v1 is None:
                continue
            v2,used2,e2 = current.get(d2, (next_val(d2),set[int](), math.inf))  # @UnusedVariable
            if v2 is None:
                continue
            if v1 == v2:
                continue
            val: Mixture = tuple((x+y)/2 for x,y in zip(v1, v2))
            used = used1 | used2 | {this_step}
            e = errors[i] = error_for(val)
            current[d1] = current[d2] = (val, used, e)
            if full:
                if len(current) == n_drops:
                    error = max(e for val, used, e in current.values())
            elif d1 == lead or d2 == lead:
                error = e
            if error < tolerance+slop:
                break
            
        if error < 0:
            error = -error
        miss = max(error-tolerance, 0)
        if miss < slop:
            miss = 0
        
        
        
        if full:
            useful_steps = set[int]()
            for s in current.values():
                useful_steps |= s[1] 
        else:
            if lead in current:
                useful_steps = current[lead][1]
            else:
                useful_steps = set()
        sorted_steps = list(useful_steps)
        sorted_steps.sort()
        # reduced = [remap_mix(m) for i,m in enumerate(mixes) if i in useful_steps]
        reduced = [EvaluatedMix(m, errors[i]) for i,m in enumerate(mixes) if i in useful_steps]
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
        mapped_drops = {XYCoord(0,0): 0}
        orientation = Orientation.NORTH_POS_EAST_POS
        
        last_set = dict[int, int]()
        
        def remap_drop(drop: XYCoord) -> int:
            nonlocal next_drop
            mapped: Optional[int] = mapped_drops.get(drop, None)
            if mapped is None:
                mapped = mapped_drops[drop] = next_drop
                next_drop += 1
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
                return NamedMix(step, Mix(d2, mix.direction.opposite), m.error, s2, s1)
            else:
                return NamedMix(step, mix, m.error, s1, s2)
            
        mixes = [remap_mix(m) for m in self.reduced]
        mixes.sort(key=lambda nm: (nm.step, nm.d1))
            
        return mixes
        
    
    @classmethod
    def generate(cls, *,
                 seq_len: int, 
                 radius: int, 
                 n_drops: int,
                 tolerance: float,
                 slop: float,
                 full: bool) -> Candidate:
        def random_mix() -> Mix:
            return Mix(XYCoord(randint(-radius, radius), 
                               randint(-radius, radius)),
                        choice(Dir.cardinals()))
        mixes = [random_mix() for _ in range(seq_len)]
        return Candidate(mixes, n_drops=n_drops, tolerance=tolerance, full=full, slop=slop)
        
    
    
    def __init__(self, mixes: MixSeq, *,
                 n_drops: int,
                 tolerance: float,
                 slop: float,
                 full: bool) -> None:
        self.mixes = mixes
        self.eval, self.reduced = self.evaluate(mixes, n_drops=n_drops, tolerance=tolerance, slop=slop, 
                                                full=full)

    def cross(self, other: Candidate, *,
              n_drops: int,
              tolerance: float,
              slop: float,
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
        return Candidate(mixes, n_drops=n_drops, tolerance=tolerance, full=full, slop=slop)
            
            

class Monitor:
    best: Optional[Candidate] = None
    best_gen: int = 0
    seen: int = 0
    log_file_name: Final[str]
    log_file: Optional[TextIO] = None
    
    
    def __init__(self, log_file_name: str) -> None:
        self.log_file_name = log_file_name
    
    def see(self, candidate: Candidate, gen: int) -> bool:
        best = self.best
        self.seen += 1
        if best is None or candidate.eval < best.eval:
            self.best = candidate
            self.best_gen = gen
            reduced = candidate.reduced_mixes()
            print("---------")
            print(f"New best in generation {gen} ({self.seen:,}): {candidate.eval}")
            print(f"  {map_str(reduced)}")
            if (candidate.eval.miss == 0):
                if self.log_file is None:
                    self.log_file = open(self.log_file_name, "w").__enter__()
                log_mixes(reduced, evaluation=candidate.eval, file = self.log_file)
                self.log_file.flush()
            return True
        return False
    
    def __enter__(self) -> Monitor:
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> Optional[bool]:
        if self.log_file is not None:
            return self.log_file.__exit__(exc_type, exc_val, exc_tb)
        return False
    
    
def tournament(size: int, pop: Sequence[Candidate]) -> tuple[Candidate,Candidate,int]:
    psize = len(pop)
    indexes = [random.randrange(psize) for _ in range(size)]
    indexes.sort(key = lambda i: pop[i].eval)
    return (pop[indexes[0]], pop[indexes[1]], indexes[-1])

def run(*, 
        n_drops: int,
        tolerance: float,
        full: bool,
        radius: int,
        candidate_size: int,
        tourney_size: int,
        pop_size: int,
        max_gens: int,
        max_size: int,
        one_point: bool,
        preserve_size: bool,
        log_file: str,
        slop: float) -> Candidate:
    with Monitor(log_file) as monitor:
        gen: int = 0
        def checked(c: Candidate) -> Candidate:
            monitor.see(c, gen)
            return c
        pop = [checked(Candidate.generate(seq_len = candidate_size,
                                          radius = radius,
                                          n_drops=n_drops,
                                          tolerance=tolerance,
                                          full=full,
                                          slop=slop)) for _ in range(pop_size)]
        for gen in range(1, max_gens):
            print(f"*** Generation {gen:,} ({monitor.seen:,}) ***")
            for _ in range(pop_size):
                m,f,worst = tournament(tourney_size, pop)
                new = m.cross(f, one_point=one_point, preserve_size=preserve_size,
                              max_size=max_size,
                              n_drops=n_drops, tolerance=tolerance, full=full,
                              slop=slop)
                if new.eval < pop[worst].eval:
                    pop[worst] = checked(new)
                else:
                    monitor.seen += 1
        
        best = monitor.best
        assert best is not None
        return best


if __name__ == '__main__':
    parser = ArgumentParser(description="Find optimal mixing sequences")
    parser.add_argument("n_drops", type=int, 
                        help="""The number of drops to mix""")
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
    default_size = 200
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
    
    def dir_path(d: str) -> str:
        if os.path.isdir(d):
            return d
        else:
            raise ArgumentTypeError(f"Not a directory: '{d}'")
    
    default_logdir = os.path.join(".", "logs")
    parser.add_argument("--log_dir", type=dir_path, default=default_logdir,
                        help=f"The directory for log files.  Default is {default_logdir}.")
    
    default_slop = 0.00001
    parser.add_argument("--slop", type=float, default=default_slop,
                        help=f"""The amount that a solution is allowed to 
                                 exceed the stated tolerance.  This helps with floating-point
                                 rounding inequalities.  Default is {default_slop}
                        """)
    

    args: Namespace = parser.parse_args()
    print(args)
    n_drops: int = args.n_drops
    tolerance: float = args.tolerance
    full: bool = args.full
    radius: int = args.radius
    size: int = args.size
    tourney_size: int = args.tourney_size
    pop_size: int = args.pop_size
    max_gens: int = args.max_gens
    max_size: int = args.max_size
    one_point: bool = args.one_point
    preserve_size: bool = args.preserve_size
    logdir: str = args.log_dir
    slop: float = args.slop
    
    ts = time_now().strftime(fmt="%Y%m%d_%H%M%S")
    logfile = os.path.join(logdir, f"mix-{n_drops}{'-full' if full else ''}-t{tolerance}.{ts}")
    
    run(n_drops=n_drops, tolerance=tolerance, full=full, radius=radius,
        candidate_size=size, tourney_size=tourney_size, pop_size=pop_size,
        max_gens=max_gens, max_size=max_size, 
        one_point=one_point, preserve_size=preserve_size,log_file = logfile,
        slop=slop)
    
    # c = Candidate.generate(seq_len=size, n_drops=max_drops, folds=folds, tolerance=tolerance)
    # print(map_str(c.mixes))
    # print(map_str(c.reduced))
    # print(map_str(c.eval))
