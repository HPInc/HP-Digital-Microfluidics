from quantities.SI import sec, ml, m, mol, ul
from quantities.US import ft
from quantities.dimensions import Volume, Substance


a = 5*sec
b = 10*ft


# print(a+b)


print(Volume.dim())
x = Volume.dim().of("substance")
y = Volume.dim()["substance"]

print(x, y, x is y)

class Reagent: ...
z = Volume.dim().of(Reagent)
print(z)

v = 1*ml
v2 = (1*ml).of(Reagent)

print(v, v2)

print(v2/v)

print(ml.quantity)

print((m**2).quantity)
print(m**2)

print((2*mol/(1*ml)).__class__)

print((2*ul.of(Substance)/(10*ml)).in_units(ml.of(Substance)/ml))

print(2*ul[Substance]/ml)
