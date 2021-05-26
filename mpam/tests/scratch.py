from mpam.types import Reagent, Liquid, Mixture, Chemical, waste_reagent
from quantities.SI import uL, mM, L, mg, ml
from quantities.dimensions import MassConcentration, Substance,\
    VolumeConcentration, Molarity
from typing import Mapping
from erk.stringutils import map_str
from mypyc import rt_subtype

c1 = Chemical.find("C1")
c2 = Chemical.find("C2")
c3 = Chemical.find("C3")
c4 = Chemical.find("C4")

mg_per_L = (mg/L).a(MassConcentration)
ml_per_L = (ml.of(Substance)/L).a(VolumeConcentration)

Molarity.default_units(mM)
MassConcentration.default_units(mg_per_L)
VolumeConcentration.default_units(ml_per_L)

r1 = Reagent("R1", composition={c1: 1*mM, c2: 3*mg_per_L})
r2 = Reagent("R2", composition={c1: 2*mM, c3: 2*ml_per_L})
r3 = Reagent("R3", composition={c3: 2*mg_per_L})

l1 = r1.liquid(volume=2*uL)
l2 = r2.liquid(volume=2*uL)
l3 = r3.liquid(volume=2*uL)

m1 = l1.mix_with(l2)
m2 = l1.mix_with(l3)
m = m1.mix_with(m2)

n1 = l2.mix_with(l3)
n = n1.mix_with(l1).mix_with(l1)

def fmt_dict(d: Mapping) -> str:
    return f"{{{', '.join(f'{k}: {v}' for k,v in d.items())}}}"

print(m)
print(Mixture._known_mixtures)
print(Mixture._instances)
print(n)
print(n.reagent is m.reagent)
print(map_str(r1.composition))
print(map_str(r2.composition))
print(map_str(r3.composition))
print(map_str(m1.reagent.composition))
print(map_str(m2.reagent.composition))
print(map_str(m.reagent.composition))
print(m1.reagent.composition[c1])
print(m1.reagent.composition[c2])

n2 = l2.mix_with(waste_reagent.liquid(2*uL))
print(n2)

rt = r2.processed("thermocycled", Reagent.LoseComposition)
print(rt)
print(map_str(rt.composition))
print(l1.processed("frozen"))