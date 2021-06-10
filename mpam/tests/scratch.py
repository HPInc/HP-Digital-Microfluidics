from quantities.SI import uL, mL, L, nL, cc, hours, days, minutes, seconds
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
print(duration.decomposed([seconds, hours, days, minutes], required=[minutes, seconds]))
print(duration.decomposed([days, hours, minutes, seconds], required="all"))
print(duration.decomposed([days, hours, minutes, seconds]))