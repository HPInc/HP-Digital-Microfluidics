from __future__ import annotations

from mpam.types import Sample
from quantities.SI import volts
from quantities.dimensions import Voltage
from quantities.timestamp import Timestamp, time_now


Voltage.default_units=volts

vs = [20*volts, 30*volts, 40*volts, 2*volts, 50*volts]

s = Sample.for_type(Voltage, vs)

atts = ("count", "values", *Sample._cached_properies)

for a in sorted(atts):
    print(f"{a}: {getattr(s, a)}")
    
print("------------")
s.add(5*volts)

for a in sorted(atts):
    print(f"{a}: {getattr(s, a)}")
    
s2 = Sample.for_type(Timestamp, (time_now(), time_now(), time_now()))
print("------------")
for a in sorted(atts):
    print(f"{a}: {getattr(s2, a)}")
