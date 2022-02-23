from __future__ import annotations

from quantities.SI import mL
from quantities.dimensions import Volume
from quantities.US import gal

v = 3*gal
print(Volume.default_units)
print(f"{v:,g}")

Volume.default_units = mL
print(Volume.default_units)
print(f"{v:,g}")

