from quantities import dimensions, prefixes
import math

# angle
rad = radian = dimensions.Angle(1).as_unit("rad")
sr = steradian = dimensions.SolidAngle(1).as_unit("sr")
deg = degree = (math.pi/180)*rad

# mass
g = gramme = gram = dimensions.Mass.base_unit("g")
µg = ug = microgramme = microgram = prefixes.micro(gram)
mg = milligramme = milligram = prefixes.milli(gram)
kg = kilogramme = kilogram = prefixes.kilo(gram)
tonne = metric_tonne = metric_ton = (1000*kg).as_unit("tonne")

# distance
m = metre = meter = dimensions.Distance.base_unit("m")
dm = decimetre = decimeter = prefixes.deci(meter)
cm = centimetre = centimeter = prefixes.centi(meter)
mm = millimetre = millimeter = prefixes.milli(meter)
µm = um = micron = micrometre = micrometer = prefixes.micro(meter)
nm = nanometre = nanometer = prefixes.nano(meter)
km = kilometre = kilometer = prefixes.kilo(meter)

# area
ha = hectare = (m**2).a(dimensions.Area).as_unit("ha")

# volume
l = L = litre = liter = (dm**3).a(dimensions.Volume).as_unit("l")
dl = dL = decilitre = deciliter = prefixes.deci(liter)
cl = cL = centilitre = centiliter = prefixes.centi(liter)
ml = mL = millilitre = milliliter = prefixes.milli(liter)
µl = µL = ul = uL = micorlitre = microliter = prefixes.micro(liter)
st = stere = (m**3).a(dimensions.Volume).as_unit("st")

# time
s = sec = second = dimensions.Time.base_unit("s")
ms = msec = millisec = millisecond = prefixes.milli(second)
µs = us = µsec = usec = microsec = microsecond = prefixes.micro(second)
ns = nsec = nanosec = nanosecond = prefixes.nano(second)
mins = minute = (60*second).as_unit("min")
hr = hour = (60*minute).as_unit("hr")
day = (24*hour).as_unit("day")

# frequency
Hz = hertz = (1/s).a(dimensions.Frequency).as_unit("Hz")

# force
N = newton = (kg*m/s**2).a(dimensions.Force).as_unit("N")

# work
J = joule = (N*m).a(dimensions.Work).as_unit("J")

# pressure
Pa = pascal = (N/m**2).a(dimensions.Pressure).as_unit("Pa")

# power
W = watt = (J/s).a(dimensions.Power).as_unit("W")

# temperature
K = kelvin = dimensions.Temperature.base_unit("K")
deg_K = kelvin
deg_C = kelvin.as_unit("°C")

# luminous intensity
cd = candela = dimensions.LumInt.base_unit("cd")

# luminous flux
lm = lumen = (cd*sr).a(dimensions.LumFlux).as_unit("lm")

# illuminance
lx = lux = (lm/m**2).a(dimensions.Illuminance).as_unit("lux")

# current
A = ampere = dimensions.Current.base_unit("A")

# charge
C = coulomb = (A*s).a(dimensions.Charge).as_unit("C")
faraday = (96485.33212310084*C).as_unit("F")

# voltage, electric potential, emf
V = volt = (J/C).a(dimensions.Voltage).as_unit("V")

# magnetic flux
Wb = weber = (V*s).a(dimensions.MagneticFlux).as_unit("Wb")

# magnetic induction, flux density
T = tesla = (Wb/m**2).a(dimensions.MagneticInduction).as_unit("T")

# capacitance
F = farad = (C/V).a(dimensions.Capacitance).as_unit("F")

# resistance
Ω = ohm = (V/A).a(dimensions.Resistance).as_unit("Ω")

# conductance
S = siemens = (A/V).a(dimensions.Conductance).as_unit("S")
mho = S.as_unit("mho")

# inductance
H = henry = (V*s/A).a(dimensions.Inductance).as_unit("H")

# radioactivity
Bq = becquerel = (1/s).a(dimensions.Radioactivity).as_unit("Bq")

# ionizing radiation dose
Gy = gray = (J/kg).a(dimensions.IonizingRadDose).as_unit("Gy")
Sv = sievert = (J/kg).a(dimensions.IonizingRadDose).as_unit("Sv")

if __name__ == '__main__':
    ...
