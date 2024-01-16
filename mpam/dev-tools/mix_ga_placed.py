from __future__ import annotations

from argparse import ArgumentParser, Namespace
import math
from typing import Optional, Sequence

from sifu.grid import XYCoord, Orientation, Dir
from dmf.ga_regression import Candidate, MixSeq, Evaluation, EvaluatedMixSeq, \
    Regression


Mixture = Sequence[float]


class MixCandidate(Candidate['MixCandidate']):    
    def evaluate(self, mixes: MixSeq, *,
                 size: float,
                 tolerance: float,
                 slop: float,
                 full: bool) -> tuple[Evaluation,EvaluatedMixSeq]:

        lead = XYCoord(0,0)
        allowed = { lead }
        orientation = Orientation.NORTH_POS_EAST_POS
        
        n_drops = math.floor(size)
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
            
        return self.finish_evaluate(error=error,
                                    tolerance=tolerance,
                                    slop=slop,
                                    full=full,
                                    used_steps={loc: cv[1] for loc, cv in current.items()},
                                    lead=lead,
                                    errors=errors,
                                    )
    
class MixRegression(Regression[MixCandidate]):
    def __init__(self) -> None:
        super().__init__(logfile_prefix="mix", 
                         candidate_type=MixCandidate,
                         description="Find optimal mixing sequences")
        
    def add_args_to(self, parser: ArgumentParser) -> None:
        parser.add_argument("n_drops", type=int, 
                            help="""The number of drops to mix""")
        super().add_args_to(parser)
    
    def run_from_args(self, args: Namespace) -> MixCandidate:
        n_drops: int = args.n_drops
        args.problem_size = float(n_drops)
        return super().run_from_args(args)

if __name__ == '__main__':
    r = MixRegression()
    parser = r.argument_parser()
    args: Namespace = parser.parse_args()
    best = r.run_from_args(args)
    
