from __future__ import annotations
from mpam.types import Reagent, Mixture

r1 = Reagent("r1")
r2 = Reagent("r2")

print(Mixture.find_or_compute(r1, r2, ratio = 0.4))