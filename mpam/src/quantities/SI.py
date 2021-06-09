from quantities import dimensions, prefixes
import math

# angle
rad = radian = radians = dimensions.Angle(1).as_unit("rad")
sr = steradian = steradians = dimensions.SolidAngle(1).as_unit("sr")
deg = degree = degrees = (math.pi/180)*rad

# mass
g = gramme = gram = dimensions.Mass.base_unit("g")
grammes = grams = g
µg = ug = microgramme = microgram = prefixes.micro(gram)
microgrammes = micrograms = ug
mg = milligramme = milligram = prefixes.milli(gram)
milligrammes = milligrams = mg
kg = kilogramme = kilogram = prefixes.kilo(gram)
kilogrammes = kilograms = kg
tonne = metric_tonne = metric_ton = (1000*kg).as_unit("tonne")
tonnes = metric_tonnes = metric_tons = tonne

# distance
m = metre = meter = dimensions.Distance.base_unit("m")
metres = meters = m
dm = decimetre = decimeter = prefixes.deci(meter)
decimetres = decimeters = dm
cm = centimetre = centimeter = prefixes.centi(meter)
centimetres = centimeters = cm
mm = millimetre = millimeter = prefixes.milli(meter)
millimetres = millimeters = mm
µm = um = micron = micrometre = micrometer = prefixes.micro(meter)
microns = micrometres = micrometers = um
nm = nanometre = nanometer = prefixes.nano(meter)
nanometres = nanometers = nm
km = kilometre = kilometer = prefixes.kilo(meter)
kilometres = kilometers = km

# area
ha = hectares = hectare = (m**2).a(dimensions.Area).as_unit("ha")

# volume
l = L = litre = liter = (dm**3).a(dimensions.Volume).as_unit("l")
litres = liters = L
dl = dL = decilitre = deciliter = prefixes.deci(liter)
decilitres = deciliters = dL
cl = cL = centilitre = centiliter = prefixes.centi(liter)
centilitres = centiliters = cL
ml = mL = millilitre = milliliter = prefixes.milli(liter)
millilitres = milliliters = mL
µl = µL = ul = uL = micorlitre = microliter = prefixes.micro(liter)
microlitres = microliters = uL
nl = nL = nanolitre = nanoliter = prefixes.nano(liter)
nanolitres = nanoliters = nL
pl = pL = picolitre = picoliter = prefixes.pico(liter)
picolitres = picoliters = pL
cc = (cm**3).a(dimensions.Volume).as_unit("cc")
st = steres = stere = (m**3).a(dimensions.Volume).as_unit("st")

# time
s = sec = second = dimensions.Time.base_unit("s")
secs = seconds = s
ms = msec = millisec = millisecond = prefixes.milli(second)
millisecs = milliseconds = ms
µs = us = µsec = usec = microsec = microsecond = prefixes.micro(second)
µsecs = usecs = microsecs = microseconds = us
ns = nsec = nanosec = nanosecond = prefixes.nano(second)
nsecs = nanosecs = nanoseconds = ns
mins = minutes = minute = (60*second).as_unit("min")
hr = hours = hour = (60*minute).as_unit("hr")
days = day = (24*hour).as_unit("days", singular="day")
wk = weeks = week = (7*day).as_unit("wk")

# frequency
Hz = hertz = (1/s).a(dimensions.Frequency).as_unit("Hz")

# force
N = newtons = newton = (kg*m/s**2).a(dimensions.Force).as_unit("N")

# work
J = joules = joule = (N*m).a(dimensions.Work).as_unit("J")

# pressure
Pa = pascals = pascal = (N/m**2).a(dimensions.Pressure).as_unit("Pa")

# power
W = watts = watt = (J/s).a(dimensions.Power).as_unit("W")

# temperature
K = kelvins = kelvin = dimensions.Temperature.base_unit("K")
deg_K = degrees_K = degree_K = degrees_Kelvin = degree_Kelvin = kelvin
deg_C = degrees_C = degree_C = kelvin.as_unit("°C")
degrees_Celsius = degree_Celcius = deg_C
degrees_centigrade = degree_centigrade = deg_C


# luminous intensity
cd = candelas = candela = dimensions.LumInt.base_unit("cd")

# luminous flux
lm = lumens = lumen = (cd*sr).a(dimensions.LumFlux).as_unit("lm")

# illuminance
lx = lux = (lm/m**2).a(dimensions.Illuminance).as_unit("lux")

# current
A = amperes = ampere = dimensions.Current.base_unit("A")

# charge
C = coulombs = coulomb = (A*s).a(dimensions.Charge).as_unit("C")
faradays = faraday = (96485.33212310084*C).as_unit("F")

# voltage, electric potential, emf
V = volts = volt = (J/C).a(dimensions.Voltage).as_unit("V")

# magnetic flux
Wb = webers = weber = (V*s).a(dimensions.MagneticFlux).as_unit("Wb")

# magnetic induction, flux density
T = teslas = tesla = (Wb/m**2).a(dimensions.MagneticInduction).as_unit("T")

# capacitance
F = farads = farad = (C/V).a(dimensions.Capacitance).as_unit("F")

# resistance
Ω = ohms = ohm = (V/A).a(dimensions.Resistance).as_unit("Ω")

# conductance
S = siemens = (A/V).a(dimensions.Conductance).as_unit("S")
mhos = mho = S.as_unit("mho")

# inductance
H = henrys = henry = (V*s/A).a(dimensions.Inductance).as_unit("H")

# radioactivity
Bq = becquerels = becquerel = (1/s).a(dimensions.Radioactivity).as_unit("Bq")

# ionizing radiation dose
Gy = grays = gray = (J/kg).a(dimensions.IonizingRadDose).as_unit("Gy")
Sv = sieverts = sievert = (J/kg).a(dimensions.IonizingRadDose).as_unit("Sv")

# amount
mol = moles = mole = dimensions.Amount.base_unit("mol")
mmol = millimoles = millimole = prefixes.milli(mole)
µmol = umol = micromoles = micromole = prefixes.micro(mole)


# molar concentration
M = molar = (mmol/L).a(dimensions.MolarConcentration).as_unit("M")
mM = millimolar = prefixes.milli(molar)
µM = micromolar = prefixes.micro(molar)
nM = nanomolar = prefixes.nano(molar)


