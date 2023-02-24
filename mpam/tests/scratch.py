from __future__ import annotations
from quantities.currency.pre_decimal_GBP import shillings, sixpence, farthings,\
    pence, pounds
from typing import Protocol, Optional

x = 2*shillings+2*farthings+3*pence+5*pounds
print(x.in_units((pounds, shillings, pence)))
print(x.as_currency())

class Foo(Protocol):
    def __call__(self, x: int, *, k: Optional[str] = None) -> int: ...
    
def bar(_x: int, y: float=1, *, k: Optional[str] = "Hi", b: bool=True) -> int:
    print(k)
    return _x+1

v: Foo = bar

v(8)
