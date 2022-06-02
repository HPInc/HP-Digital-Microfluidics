from __future__ import annotations
from langsup.type_supp import Type

def check(lhs: Type, rhs: Type) -> None:
    print(f"{lhs} < {rhs} : {lhs < rhs}")

it = Type.INT
ft = Type.FLOAT
vi = it.lval
vf = ft.lval
lmi = it.maybe.lval
mi = it.maybe

check(it, ft)
check(ft, it)
check(vi, it)
check(vi, ft)
check(vf, it)
check(vf, ft)
check(vf, vi)
check(vi, vf)

check(vi, lmi)
check(lmi, vi)
check(it, mi)
