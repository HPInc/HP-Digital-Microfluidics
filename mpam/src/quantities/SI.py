from . import core, prefixes, dimensions

# angle
rad = radian = core.Unit("rad", core.Quantity(1, dimensions.scalar))
sr = steraian = core.Unit("sr", core.Quantity(1, dimensions.scalar))

# mass
g = gramme = gram = dimensions.mass.base_unit("g")
µg = ug = microgramme = microgram = prefixes.micro(gram)
mg = milligramme = milligram = prefixes.milli(gram)
kg = kilogramme = kilogram = prefixes.kilo(gram)
tonne = metric_tonne = metric_ton = core.Unit("tonne", 1000*kg)

# distance
m = metre = meter = dimensions.distance.base_unit("m")
dm = decimetre = decimeter = prefixes.deci(meter)
cm = centimetre = centimeter = prefixes.centi(meter)
mm = millimetre = millimeter = prefixes.milli(meter)
µm = um = micron = micrometre = micrometer = prefixes.micro(meter)
nm = nanometre = nanometer = prefixes.nano(meter)
km = kilometre = kilometer = prefixes.kilo(meter)

# area
ha = hectare = core.Unit("ha", m**2)

# volume
l = L = litre = liter = core.Unit("l", dm**3)
dl = dL = decilitre = deciliter = prefixes.deci(liter)
cl = cL = centilitre = centiliter = prefixes.centi(liter)
ml = mL = millilitre = milliliter = prefixes.milli(liter)
µl = µL = ul = uL = micorlitre = microliter = prefixes.micro(liter)
st = stere = core.Unit("st", m**3)

# time
s = sec = second = dimensions.time.base_unit("s")
ms = msec = millisec = millisecond = prefixes.milli(second)
µs = us = µsec = usec = microsec = microsecond = prefixes.micro(second)
ns = nsec = nanosec = nanosecond = prefixes.nano(second)
mins = minute = core.Unit("min", 60*second)
hr = hour = core.Unit("hr", 60*minute)
day = core.Unit("day", 24*hour)

# frequency
Hz = hertz = core.Unit("Hz", 1/s)

# force
N = newton = core.Unit("N", kg*m/s**2)

# work
J = joule = core.Unit("J", N*m)

# pressure
Pa = pascal = core.Unit("Pa", N/m**2)

# power
W = watt = core.Unit("W", J/s)

# temperature
K = kelvin = dimensions.temperature.base_unit("K")
deg_K = kelvin
deg_C = core.Unit("°C", kelvin)

# luminous intensity
cd = candela = dimensions.lum_int.base_unit("cd")

# luminous flux
lm = lumen = core.Unit("lm", cd*sr)

# illuminance
lx = lux = core.Unit("lux", lm/m**2)

# current
A = ampere = dimensions.current.base_unit("A")

# charge
C = coulomb = core.Unit("C", A*s)
faraday = core.Unit("F", 96485.33212310084*C)

# voltage, electric potential, emf
V = volt = core.Unit("V", J/C)

# magnetic flux
Wb = weber = core.Unit("Wb", V*s)

# magnetic induction, flux density
T = tesla = core.Unit("T", Wb/m**2)

# capacitance
F = farad = core.Unit("F", C/V)

# resistance
Ω = ohm = core.Unit("Ω", V/A)

# conductance
S = siemens = core.Unit("S", A/V)
mho = core.Unit("mho", S)

# inductance
H = henry = core.Unit("H", V*s/A)

# radioactivity
Bq = becquerel = core.Unit("Bq", 1/s)

# ionizing radiation dose
Gy = gray = core.Unit("Gy", J/kg)
Sv = sievert = core.Unit("Sv", J/kg)
