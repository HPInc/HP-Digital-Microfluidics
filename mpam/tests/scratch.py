from __future__ import annotations
from quantities.dimensions import Time, Volume
from quantities.SI import seconds

t = 5*seconds*seconds

a = Time.ZERO
b = Time.ZERO
c = Volume.ZERO

print(a, b, c)
print(a is b)
print(a is c)
print(a is 10*seconds - 10*seconds)
print(t+0)
print(t-0)
print(0+t)
print(0-t)

