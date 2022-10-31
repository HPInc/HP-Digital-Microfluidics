from __future__ import annotations

from mpam.types import deg_C_per_sec
from quantities.SI import sec, deg_C
from quantities.temperature import abs_C
from quantities.dimensions import Temperature

Temperature.default_units = deg_C
hr = 10*deg_C_per_sec
print(hr)
print(hr.for_time(10*sec))
print(20*abs_C+hr.for_time(2*sec))