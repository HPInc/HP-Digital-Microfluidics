from __future__ import annotations
from quantities.dimensions import Time
from quantities.SI import seconds

Time.default_units = (seconds,)

print(Time.INF.is_finite)