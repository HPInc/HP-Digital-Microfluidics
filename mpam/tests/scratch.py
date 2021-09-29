from __future__ import annotations
from quantities.core import qstr
from erk.stringutils import noun
from quantities.SI import uL

print(qstr(2000, 'file'))
print(f"{qstr(2, 'sheep')}")
print(f"{qstr(2, 'fix')}")
print(f"{qstr(2, 'monkey')}")
print(f"{qstr(2, 'lady')}")

print(f"{qstr(2000, 'FILE'):,}")
print(f"{qstr(2, 'FIX')}")
print(f"{qstr(2, 'MONKEY')}")
print(f"{qstr(2, 'LADY')}")

print(f"{noun(2, 'file')}")

print(f"{(2*uL).in_units(uL)}")