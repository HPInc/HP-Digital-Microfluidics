from __future__ import annotations

from quantities.SI import mm, uL
from quantities.US import mil
from quantities.dimensions import Volume


drop_size = (0.3*mm*(1.5*mm-3*mil)**2).a(Volume)

print(drop_size.in_units(uL))