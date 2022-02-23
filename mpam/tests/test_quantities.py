from quantities.SI import sec, ml, m, mol, ul, meter
from quantities.US import ft
from quantities.dimensions import Volume, Substance
from quantities.core import CountDim


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
Volume.default_units = ml
print(v, v2)


print(v2/v)

print(ml.quantity)

print((m**2).quantity)
print(m**2)

print((2*mol/(1*ml)).__class__)

print((2*ul.of(Substance)/(10*ml)).in_units(ml.of(Substance)/ml))

print(2*ul[Substance]/ml)

class Tick(CountDim): ...
tick = ticks = Tick.base_unit("tick")
t = 1*tick
print(t)
t += 2
print(t)
print((1/(2*ticks)).in_units(ticks**-1))
print(1/(2*ticks))

print((1*meter/(1*ticks)).in_units(meter/ticks))
print(1*meter/(1*ticks))

print((t**2).in_units(ticks**2))
print(t**2)

x2 = 2*ticks.of("Test")
# reveal_type(x2)
print(x2)


