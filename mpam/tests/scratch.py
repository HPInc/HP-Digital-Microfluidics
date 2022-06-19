from __future__ import annotations

from quantities.SI import volts, m, s, Hz, sec
from quantities.US import mph
from quantities.core import default_units, set_default_units
from quantities.prefixes import milli, kilo


v = 20*volts

speed = 20*m/s
freq = 100*Hz

set_default_units(milli(volts), mph)

print(v, speed, freq)
with default_units(volts, m/s, kilo(Hz), Hz):
    print(v, speed, freq, 0/sec)
    
print(v, speed, freq)