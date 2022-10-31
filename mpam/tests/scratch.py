from __future__ import annotations


from quantities.SI import uL
from quantities.dimensions import Volume

Volume.default_units = uL

for _ in range(5):
    v = Volume.noise(10 *uL)
    print(v)
