from __future__ import annotations

from mypy.types import NoneType

from mpam.types import Liquid, unknown_reagent
from quantities.SI import uL


liquid = Liquid(unknown_reagent, 0.5*uL)
print(liquid)
