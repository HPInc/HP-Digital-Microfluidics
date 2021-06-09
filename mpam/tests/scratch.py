from quantities.SI import uL, mL, L, nL, cc, cm, hours, days, minutes, seconds,\
    ms, us
from quantities.dimensions import Volume
from quantities.US import pint, qt, acre, ft


v : Volume = 25*uL

Volume.default_units([mL, cc, uL, pint, qt])

print(25*uL)
print(1*L)
print(20*nL)

Volume.default_units((acre*ft).a(Volume))

print(25*uL)
print(1*L)
print(20*nL)

print((24*hours).in_units([days]))


duration = 540*minutes+52.24*seconds
print(duration.decomposed([days, hours, minutes, seconds], optional=[days, hours]))