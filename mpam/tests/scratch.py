from __future__ import annotations

from quantities.SI import mm, uL, seconds, hours, meters, sec, m
from quantities.US import mil, acre, mph
from quantities.prefixes import half, quarter
from quantities.scalar import thousand, dozen
from quantities.core import Unit, UnitExpr
from quantities.dimensions import TimeUnitExpr


drop_size = (0.3*mm*(1.5*mm-3*mil)**2)

print(drop_size.in_units(uL))

x = (3*mm)*(5*mm)
y = x*(5*mm)


z = 10*mm*acre


# reveal_type(10*acre*ft)

# reveal_type(20*acre*ft/(3*ft))

s = (20*mm)**2/(1*mm)**2

print(s)

print(2*thousand*mm)
# reveal_type(micro(seconds))
half_secs = half(seconds)  
# reveal_type(3*dozen*seconds)
print((3*dozen*seconds).in_units(quarter(seconds)))

print((5*mm)**2*(2*hours))

print(meters/mm)
print(type(meters/mm))
# reveal_type(meters/mm) 
reveal_type((2*sec)*(3*mph))
reveal_type(m/sec/sec)
reveal_type(mph/sec*sec)
reveal_type(3*m/sec**2)

class Foo:
    def __init__(self, x: int) -> None: ...
    
class Bar(Foo): ...


class Parent:
    def test(self, n: int) -> Foo: 
        return Foo(n)
    
class Child:
    test = Bar
    
c = Child()

reveal_type(c.test(2))
    
    
    


