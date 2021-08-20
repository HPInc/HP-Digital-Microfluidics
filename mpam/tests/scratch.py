from __future__ import annotations

from mpam.types import Liquid, unknown_reagent, Reagent
from quantities.SI import uL
from erk.numutils import farey




v = 0.5*uL

l1 = Liquid(Reagent("r1"), v)
l2 = Liquid(Reagent("r2"), v)
l3 = Liquid(Reagent("r3"), v)

# m = Liquid.mix_together([l1, (l2, 0.5)])
m = Liquid.mix_together([l1, l2, l3])

print(m)

a = 2.0

print(farey(a/(a+1)))