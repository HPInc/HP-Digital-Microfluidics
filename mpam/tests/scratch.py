from __future__ import annotations
from math import floor

def tobin(d: float, max_places=20) -> str:
    intpart = floor(d)
    val = f"{intpart:b}."
    
    d -= intpart
    places = 0
    while d>0 and places < max_places:
        if d >= 0.5:
            val += "1"
            d -= 0.5
        else:
            val += "0"
        d *= 2
        places += 1
    return val

print(tobin(1/3))
print(tobin(1/4))
print(tobin(1/5))
print(tobin(1/7))
print(tobin(1/10))
