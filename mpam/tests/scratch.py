from quantities.SI import uL, mL, L, nL, cc, hours, days, minutes, seconds,\
    meters, liters, m, s
from quantities.dimensions import Volume
from quantities.US import pint, qt, acre, ft, fl_oz, gallons, pints, quarts,\
    cups


# v : Volume = 25*uL
#
# Volume.default_units([mL, cc, uL, pint, qt])
#
# print(25*uL)
# print(1*L)
# print(20*nL)
#
# Volume.default_units((acre*ft).a(Volume))
#
# print(25*uL)
# print(1*L)
# print(20*nL)
#
# print((24*hours).in_units([days]))
#
duration = 540*minutes+52.24*seconds
print(duration.decomposed([seconds, hours, days, minutes], required=[minutes, seconds]))
# print(duration.decomposed([days, hours, minutes, seconds], required="all"))
# print(duration.decomposed([days, hours, minutes, seconds]))
#
# print(f"|{(meters**2)/seconds:.^20}|")
# print("------------")

v = 3*liters
# Volume.default_units([mL, cc, uL, pint, qt])
# # Volume.default_units((m**3).a(Volume))
# Volume.default_units(mL)
#
# print(f"|{v:20,f}|")
# print(f"|{v:<20,f}|")
# print(f"|{v:20,.2f}|")
# print(f"|{v:<20,.2f}|")
# print(f"|{v:<20,f;>5}|")
# print(f"|{v:20,f;>5}|")
# print(f"|{v:20,.3f;.>5}|")
# print(f"|{v:*<20,.3f;.>5}|")
#
# d = (5*L).decomposed([gallons, quarts, pints, cups, fl_oz])
# print(d)
#
# print(f"|{d:40f}|")
# print(f"|{d:.>40f}|")
# print(f"|{d:.<40f}|")
# print(f"|{d:.<40.2f}|")
# print(f"|{d:.<40}|")
# print(f"|{d:.<40.2}|")

Volume.default_units((m**3).a(Volume))
print(f"{v}")
print(f"{v:;h}")
print(f"{m**3:h}")
print(f"{m**3:s}")
print(f"{m**3:c}")
print(f"{(m**3)/seconds:c}")



print(f"{v/(2*s):.4f;c}")
print(f"{m**3:h}")
print(f"{v:.3f;p-}")

