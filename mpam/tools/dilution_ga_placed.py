from __future__ import annotations

from argparse import ArgumentParser, Namespace
import math
from mpam.ga_regression import Candidate, MixSeq, Evaluation, EvaluatedMixSeq, \
    Regression
from mpam.types import XYCoord, Orientation


class DilutionCandidate(Candidate['DilutionCandidate']):    
    def evaluate(self, mixes: MixSeq, *,
                 size: float,
                 tolerance: float,
                 slop: float,
                 full: bool) -> tuple[Evaluation,EvaluatedMixSeq]:

        lead = XYCoord(0,0)

        folds = size        
        CurrentVal = tuple[float, set[int]]
        current: dict[XYCoord,CurrentVal] = { lead: (1, set())}
        last_step = 0
        n_drops: int = math.ceil(folds)
        

        orientation = Orientation.NORTH_POS_EAST_POS
        values: list[float] = [-1] * len(mixes)
        
        def error_for(val: float) -> float:
            return math.inf if val == 1 else val*(folds-1)/(1-val)-1

        error = error_for(1)
        
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
            elif d1 == lead or d2 == lead:
                error = error_for(val)
            if abs(error) < tolerance+slop:
                break
            
        return self.finish_evaluate(error=error,
                                    tolerance=tolerance,
                                    slop=slop,
                                    full=full,
                                    used_steps={loc: cv[1] for loc, cv in current.items()},
                                    lead=lead,
                                    errors=values,
                                    )
    
class DilutionRegression(Regression[DilutionCandidate]):
    def __init__(self) -> None:
        super().__init__(logfile_prefix="dilute", 
                         candidate_type=DilutionCandidate,
                         description="Find optimal dilution sequences")
        
    def add_args_to(self, parser: ArgumentParser):
        parser.add_argument("folds", type=float, 
                            help="""The number of times to dilute (e.g., 8 for an 8x dilution).  
                                    Does not need to be an integer""")
        
        super().add_args_to(parser)
    
    def run_from_args(self, args: Namespace) -> DilutionCandidate:
        folds: float = args.folds
        args.problem_size = folds
        return super().run_from_args(args)

if __name__ == '__main__':
    # mixes = [Mix(XYCoord(0,0), Dir.WEST),
    #          Mix(XYCoord(0,0), Dir.EAST),
    #          Mix(XYCoord(0,0), Dir.WEST),
    #          Mix(XYCoord(0,0), Dir.EAST),
    #          ]
    #
    # c = DilutionCandidate(mixes, size=3, tolerance=0.1, slop=0.000001,full=False)
    #
    # assert False
    
    r = DilutionRegression()
    parser = r.argument_parser()
    args: Namespace = parser.parse_args()
    best = r.run_from_args(args)
    
