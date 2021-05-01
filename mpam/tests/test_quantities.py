from quantities.SI import sec, ms
from quantities.US import ft
a = 5*sec
b = 10*ft

print(a.in_units(ft))
print(a+b)