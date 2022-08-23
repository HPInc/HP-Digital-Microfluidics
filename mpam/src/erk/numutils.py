from __future__ import annotations

from fractions import Fraction
from math import floor, isclose


def farey(n: float, *,
          max_denom: int = 10000,
          rel_tol=1e-09,
          abs_tol=0.0,
          ) -> Fraction:
    if n < 0:
        return -farey(-n)
    if n > 1:
        i = floor(n)
        return i+farey(n-i)
    if n > 0.5:
        return 1-farey(1-n)

    hi_n, hi_d = 1, floor(1/n)
    lo_n, lo_d = 1, hi_d+1
    
    hi_dev = hi_n/hi_d-n
    if hi_dev == 0:
        return Fraction(hi_n, hi_d)
    lo_dev = n-lo_n/lo_d
    
    while True:
        # print(f"bounds: {lo_n}/{lo_d} = {lo_n/lo_d} ({lo_dev}) : {n} : ({hi_dev}) {hi_n/hi_d} = {hi_n}/{hi_d}")
        new_n = lo_n+hi_n
        new_d = lo_d+hi_d
        if new_d > max_denom:
            break;
        new = new_n/new_d
        if isclose(new, n, rel_tol=rel_tol, abs_tol=abs_tol):
            return Fraction(new_n, new_d)
        
        if new > n:
            hi_dev = new-n
            hi_n = new_n
            hi_d = new_d
        else:
            lo_dev = n-new
            lo_n = new_n
            lo_d = new_d
        
    if hi_dev < lo_dev:
        return Fraction(hi_n, hi_d)
    else:
        return Fraction(lo_n, lo_d)
    
