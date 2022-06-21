from __future__ import annotations

from devices.dummy_pipettor import DummyPipettor
from mpam.types import unknown_reagent, Reagent
from erk.stringutils import map_str
from mpam.exerciser import Exerciser

Exerciser.setup_logging(levels="info")

p = DummyPipettor()

s = p.source_named("A2")
assert s is not None
s.reagent = unknown_reagent

print(s)

reagents = [Reagent.find(f"R{n+1}") for n in range(8)]
sources = [p.sources_for(r)[0] for r in reagents]

for source in sources:
    print(source)
    
print(map_str(p._sources_by_reagent))
