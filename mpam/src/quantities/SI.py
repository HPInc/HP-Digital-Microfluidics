from quantities import dimensions, prefixes
import math

# angle
radians = dimensions.Angle(1).as_unit("rad")
"""
Base :class:`~quantities.core.Unit` (``rad``) of
:class:`~quantities.dimensions.Angle`

Aliases include :attr:`rad` and :attr:`radian`.

""" 
radian = radians    #: alias of :attr:`radians`
rad = radians       #: alias of :attr:`radians`
steradians = dimensions.SolidAngle(1).as_unit("sr")
"""
Base :class:`~quantities.core.Unit` (``wr``) of
:class:`~quantities.dimensions.SolidAngle`

Aliases include :attr:`sr` :attr:`steradian`.
"""
steradian = steradians  #: alias of :attr:`steradians` 
sr = steradians         #: alias of :attr:`steradians` 
degrees = ((math.pi/180)*rad).as_unit("deg")
"""
:class:`~quantities.core.Unit` (``deg = π/180 rad``) of
:class:`~quantities.dimensions.Angle`

Aliases include :attr:`deg` and :attr:`degree`.
"""
degree = degrees    #: alias of :attr:`degrees`
deg = degrees       #: alias of :attr:`degrees`

# mass
grams = dimensions.Mass.base_unit("g")
"""
Base :class:`~quantities.core.Unit` (``g``) of
:class:`~quantities.dimensions.Mass`

Aliases include :attr:`g`, :attr:`gram`, :attr:`grammes`,
and :attr:`gramme`
""" 
gram = grams    #: alias of :attr:`grams`
grammes = grams #: alias of :attr:`grams`
gramme = grams  #: alias of :attr:`grams`
g = grams  # alias of :attr:`grams`

micrograms = prefixes.micro(gram)
"""
Prefixed :class:`~quantities.core.Unit` (``µg``) of
:attr:`grams`

Aliases include :attr:`µg`, :attr:`ug`, :attr:`microgram`,
:attr:`microgrammes`, and :attr:`microgramme`.
"""
microgram = micrograms      #: alias of :attr:`micrograms`
microgrammes = micrograms   #: alias of :attr:`micrograms`
microgramme = micrograms    #: alias of :attr:`micrograms`
µg = micrograms             #: alias of :attr:`micrograms`
ug = micrograms             #: alias of :attr:`micrograms`
milligrams = prefixes.milli(gram)
"""
Prefixed :class:`~quantities.core.Unit` (``mg``) of
:attr:`grams`

Aliases include :attr:`mg`, :attr:`milligram`,
:attr:`milligrammes`, and :attr:`milligramme`
"""
milligram = milligrams      #: alias of :attr:`milligrams`
milligrammes = milligrams   #: alias of :attr:`milligrams`
milligramme = milligrams    #: alias of :attr:`milligrams`
mg = milligrams             #: alias of :attr:`milligrams`
kilograms = prefixes.kilo(gram)
"""
Prefixed :class:`~quantities.core.Unit` (``kg``) of
:attr:`grams`

Aliases include :attr:`kg`, :attr:`kilogram`,
:attr:`kilogrammes`, and :attr:`kilogramme`.
"""
kilogram = kilograms      #: alias of :attr:`kilograms`
kilogrammes = kilograms   #: alias of :attr:`kilograms`
kilogramme = kilograms    #: alias of :attr:`kilograms`
kg = kilograms             #: alias of :attr:`kilograms`

tonnes = (1000*kg).as_unit("tonne")
"""
:class:`~quantities.core.Unit` (``tonne = 1000 kg``) of
:class:`~quantities.dimensions.Mass`

Aliases include :attr:`tonne`, :attr:`metric_tons`,
:attr:`metric_ton`, :attr:`metric_tonnes`, and
:attr:`metric_tonne`.
"""
tonne = tonnes    #: alias of :attr:`tonnes`
metric_tons = tonnes    #: alias of :attr:`tonnes`
metric_ton = tonnes    #: alias of :attr:`tonnes`
metric_tonnes = tonnes    #: alias of :attr:`tonnes`
metric_tonne = tonnes    #: alias of :attr:`tonnes`

# distance
meters = dimensions.Distance.base_unit("m")
"""
Base :class:`~quantities.core.Unit` (``m``) of
:class:`~quantities.dimensions.Distance`

Aliases inclde :attr:`m`, :attr:`meter`,
:attr:`metres`, and :attr:`metre`.
""" 
meter = meters  #: alias of :attr:`meters`
metres = meters #: alias of :attr:`meters`
metre = meters  #: alias of :attr:`meters`
m = meters      #: alias of :attr:`meters`
decimeters = prefixes.deci(meter)
"""
Prefixed :class:`~quantities.core.Unit` (``dm``) of
:attr:`meters`

Aliases include :attr:`dm`, :attr:`decimeter`,
:attr:`decimetres`, and :attr:`decimetre`.
"""
decimeter = decimeters  #: alias of :attr:`decimeters`
decimetres = decimeters  #: alias of :attr:`decimeters`
decimetre = decimeters  #: alias of :attr:`decimeters`
dm = decimeters  #: alias of :attr:`decimeters`
centimeters = prefixes.centi(meter)
"""
Prefixed :class:`~quantities.core.Unit` (``cm``) of
:attr:`meters`

Aliases include :attr:`cm`, :attr:`centimeter`,
:attr:`centimetres`, and :attr:`centimetre`.
"""
centimeter = centimeters  #: alias of :attr:`centimeters`
centimetres = centimeters  #: alias of :attr:`centimeters`
centimetre = centimeters  #: alias of :attr:`centimeters`
cm = centimeters  #: alias of :attr:`centimeters`
millimeters = prefixes.milli(meter)
"""
Prefixed :class:`~quantities.core.Unit` (``mm``) of
:attr:`meters`

Aliases include :attr:`mm`, :attr:`millimeter`,
:attr:`millimetres`, and :attr:`millimetre`.
"""
millimeter = millimeters  #: alias of :attr:`millimeters`
millimetres = millimeters  #: alias of :attr:`millimeters`
millimetre = millimeters  #: alias of :attr:`millimeters`
mm = millimeters  #: alias of :attr:`millimeters`

microns = prefixes.micro(meter)
"""
Prefixed :class:`~quantities.core.Unit` (``µm``) of
:attr:`meters`

Aliases include :attr:`µm`, :attr:`um`,
:attr:`micrometers`, :attr:`micrometer`,
:attr:`micrometres`, and :attr:`micrometre`.
"""
micrometers = microns #: alias of :attr:`microns`
micrometer = microns #: alias of :attr:`microns`
micrometres = microns  #: alias of :attr:`microns`
micrometre = microns  #: alias of :attr:`microns`
µm = microns  #: alias of :attr:`microns`
um = microns  #: alias of :attr:`microns`

nanometers = prefixes.nano(meter)
"""
Prefixed :class:`~quantities.core.Unit` (``nm``) of
:attr:`meters`

Aliases include :attr:`nm`, :attr:`nanometer`,
:attr:`nanometres`, and :attr:`nanometre`.
"""
nanometer = nanometers  #: alias of :attr:`nanometers`
nanometres = nanometers  #: alias of :attr:`nanometers`
nanometre = nanometers  #: alias of :attr:`nanometers`
nm = nanometers  #: alias of :attr:`nanometers`

kilometers = prefixes.kilo(meter)
"""
Prefixed :class:`~quantities.core.Unit` (``km``) of
:attr:`meters`

Aliases include :attr:`km`, :attr:`kilometer`,
:attr:`kilometres`, and :attr:`kilometre`.
"""
kilometer = kilometers  #: alias of :attr:`kilometers`
kilometres = kilometers  #: alias of :attr:`kilometers`
kilometre = kilometers  #: alias of :attr:`kilometers`
km = kilometers  #: alias of :attr:`kilometers`

# area
hectares = (10000*(m**2)).as_unit("ha")
"""
:class:`~quantities.core.Unit` (``ha = 10,000 m**2``) of
:class:`~quantities.dimensions.Area`

Aliases include :attr:`ha` and :attr:`hectare`.
"""
hectare = hectares   #: alias of :attr:`hectares`
ha  = hectares   #: alias of :attr:`hectares`

# volume
liters = (dm**3).as_unit("l")
"""
:class:`~quantities.core.Unit` (``L = dm**3``) of
:class:`~quantities.dimensions.Volume`

Aliases include :attr:`L`, :attr:`l`, :attr:`liter`,
:attr:`litres`, and :attr:`litre`.
""" 
liter = liters  #: alias of :attr:`liter`
litres = liters #: alias of :attr:`liter`
litre = liters  #: alias of :attr:`liter`
L = liters      #: alias of :attr:`liter`
l = liters      #: alias of :attr:`liter`

deciliters = prefixes.deci(liter)
"""
Prefixed :class:`~quantities.core.Unit` (``dL``) of
:attr:`liters`

Aliases include :attr:`dL`, :attr:`dl`, :attr:`deciliter`,
:attr:`decilitres`, and :attr:`decilitre`.
"""
deciliter = deciliters  #: alias of :attr:`deciliters`
decilitres = deciliters  #: alias of :attr:`deciliters`
decilitre = deciliters  #: alias of :attr:`deciliters`
dL = deciliters  #: alias of :attr:`deciliters`
dl = deciliters  #: alias of :attr:`deciliters`

centiliters = prefixes.centi(liter)
"""
Prefixed :class:`~quantities.core.Unit` (``cL``) of
:attr:`liters`

Aliases include :attr:`cL`, :attr:`cl`, :attr:`centiliter`,
:attr:`centilitres`, and :attr:`centilitre`.
"""
centiliter = centiliters  #: alias of :attr:`centiliters`
centilitres = centiliters  #: alias of :attr:`centiliters`
centilitre = centiliters  #: alias of :attr:`centiliters`
cL = centiliters  #: alias of :attr:`centiliters`
cl = centiliters  #: alias of :attr:`centiliters`

milliliters = prefixes.milli(liter)
"""
Prefixed :class:`~quantities.core.Unit` (``mL``) of
:attr:`liters`

Aliases include :attr:`mL`, :attr:`ml`, :attr:`milliliter`,
:attr:`millilitres`, and :attr:`millilitre`.
"""
milliliter = milliliters  #: alias of :attr:`milliliters`
millilitres = milliliters  #: alias of :attr:`milliliters`
millilitre = milliliters  #: alias of :attr:`milliliters`
mL = milliliters  #: alias of :attr:`milliliters`
ml = milliliters  #: alias of :attr:`milliliters`

microliters = prefixes.micro(liter)
"""
Prefixed :class:`~quantities.core.Unit` (``µL``) of
:attr:`liters`

Aliases include :attr:`µL`, :attr:`µL`, :attr:`uL`,
:attr:`ul`, :attr:`microliter`, :attr:`microlitres`,
and :attr:`microlitre`.
"""
microliter = microliters  #: alias of :attr:`microliters`
microlitres = microliters  #: alias of :attr:`microliters`
microlitre = microliters  #: alias of :attr:`microliters`
µL = microliters  #: alias of :attr:`microliters`
µl = microliters  #: alias of :attr:`microliters`
uL = microliters  #: alias of :attr:`microliters`
ul = microliters  #: alias of :attr:`microliters`

nanoliters = prefixes.nano(liter)
"""
Prefixed :class:`~quantities.core.Unit` (``nL``) of
:attr:`liters`

Aliases include :attr:`nL`, :attr:`nl`, :attr:`nanoliter`,
:attr:`nanolitres`, and :attr:`nanolitre`.
"""
nanoliter = nanoliters  #: alias of :attr:`nanoliters`
nanolitres = nanoliters  #: alias of :attr:`nanoliters`
nanolitre = nanoliters  #: alias of :attr:`nanoliters`
nL = nanoliters  #: alias of :attr:`nanoliters`
nl = nanoliters  #: alias of :attr:`nanoliters`

picoliters = prefixes.pico(liter)
"""
Prefixed :class:`~quantities.core.Unit` (``pL``) of
:attr:`liters`

Aliases include :attr:`pL`, :attr:`pl`, :attr:`picoliter`,
:attr:`picolitres`, and :attr:`picolitre`.
"""
picoliter = picoliters  #: alias of :attr:`picoliters`
picolitres = picoliters  #: alias of :attr:`picoliters`
picolitre = picoliters  #: alias of :attr:`picoliters`
pL = picoliters  #: alias of :attr:`picoliters`
pl = picoliters  #: alias of :attr:`picoliters`

cc = (cm**3).as_unit("cc")
"""
:class:`~quantities.core.Unit` (``cc = cm**3``) of
:class:`~quantities.dimensions.Volume`
""" 
steres = (m**3).as_unit("st")
"""
:class:`~quantities.core.Unit` (``st = m**3``) of
:class:`~quantities.dimensions.Volume`

Aliases include :attr:`st` and :attr:`stere`.
""" 
stere = steres  #: alias of :attr:`steres`
st = steres     #: alias of :attr:`steres`


# time
seconds = dimensions.Time.base_unit("s")
"""
Base :class:`~quantities.core.Unit` (``s``) of
:class:`~quantities.dimensions.Time`

Aliases include :attr:`s`, :attr:`second`,
:attr:`secs`, and :attr:`sec`.
""" 
second = seconds    #: alias of :attr:`seconds`
secs = seconds    #: alias of :attr:`seconds`
sec = seconds    #: alias of :attr:`seconds`
s = seconds    #: alias of :attr:`seconds`

milliseconds = prefixes.milli(second)
"""
Prefixed :class:`~quantities.core.Unit` (``ms``) of
:attr:`seconds`

Aliases include :attr:`ms`, :attr:`millisecond`,
:attr:`millisecs`, :attr:`millisec`, :attr:`msecs`,
and :attr:`msec`.
"""
millisecond = milliseconds  #: alias of :attr:`milliseconds`
millisecs = milliseconds  #: alias of :attr:`milliseconds`
millisec = milliseconds  #: alias of :attr:`milliseconds`
msecs = milliseconds  #: alias of :attr:`milliseconds`
msec = milliseconds  #: alias of :attr:`milliseconds`
ms = milliseconds  #: alias of :attr:`milliseconds`

microseconds = prefixes.micro(second)
"""
Prefixed :class:`~quantities.core.Unit` (``µs``) of
:attr:`seconds`

Aliases include :attr:`µs`, :attr:`us`, :attr:`microsecond`,
:attr:`microsecs`, :attr:`microsec`, :attr:`µsecs`,
:attr:`µsec`, :attr:`usecs`, and :attr:`usec`.

"""
microsecond = microseconds  #: alias of :attr:`microseconds`
microsecs = microseconds  #: alias of :attr:`microseconds`
microsec = microseconds  #: alias of :attr:`microseconds`
usecs = microseconds  #: alias of :attr:`microseconds`
usec = microseconds  #: alias of :attr:`microseconds`
µsecs = microseconds  #: alias of :attr:`microseconds`
µsec = microseconds  #: alias of :attr:`microseconds`
µs = microseconds  #: alias of :attr:`microseconds`
us = microseconds  #: alias of :attr:`microseconds`

nanoseconds = prefixes.nano(second)
"""
Prefixed :class:`~quantities.core.Unit` (``ns``) of
:attr:`seconds`

Aliases include :attr:`ns`, :attr:`nanosecond`,
:attr:`nanosecs`, :attr:`nanosec`, :attr:`nsecs`,
and :attr:`nsec`.
"""
nanosecond = nanoseconds  #: alias of :attr:`nanoseconds`
nanosecs = nanoseconds  #: alias of :attr:`nanoseconds`
nanosec = nanoseconds  #: alias of :attr:`nanoseconds`
nsecs = nanoseconds  #: alias of :attr:`nanoseconds`
nsec = nanoseconds  #: alias of :attr:`nanoseconds`
ns = nanoseconds  #: alias of :attr:`nanoseconds`

minutes = (60*second).as_unit("min")
"""
:class:`~quantities.core.Unit` (``min = 60 s``) of
:class:`~quantities.dimensions.Time`

Aliases include :attr:`minute` and :attr:`mins`.

Note:
   ``min`` is a reserved word in Python.
""" 
minute = minutes    #: alias of :attr:`minutes`
mins = minutes    #: alias of :attr:`minutes`

hours = (60*minute).as_unit("hr")
"""
:class:`~quantities.core.Unit` (``hr = 60 min``) of
:class:`~quantities.dimensions.Time`

Aliases include :attr:`hr` and :attr:`hour`.
""" 
hour = hours    #: alias of :attr:`hours`
hr = hours    #: alias of :attr:`hours`

days = (24*hour).as_unit("days", singular="day")
"""
:class:`~quantities.core.Unit` (``days = 24 hr``) of
:class:`~quantities.dimensions.Time`

Aliases include :attr:`day`.
""" 
day = days  #: alias of :attr:`days`

weeks = (7*day).as_unit("wk")
"""
:class:`~quantities.core.Unit` (``wk = 7 days``) of
:class:`~quantities.dimensions.Time`

Aliases include :attr:`wk` and :attr:`week`.
""" 
week = weeks    #: alias of :attr:`weeks`
wk = weeks    #: alias of :attr:`weeks`

# frequency

hertz = (1/s).as_unit("Hz")

"""
:class:`~quantities.core.Unit` (``Hz = 1/s``) of
:class:`~quantities.dimensions.Frequency`

Aliases include :attr:`Hz`.
"""
Hz = hertz  #: alias of :attr:`hertz` 

# force
N = newtons = newton = (kg*m/s**2).as_unit("N")

# work
J = joules = joule = (N*m).as_unit("J")

# pressure
Pa = pascals = pascal = (N/m**2).as_unit("Pa")

# power
W = watts = watt = (J/s).as_unit("W")

# temperature
degrees_Kelvin = dimensions.Temperature.base_unit("K")
"""
Base :class:`~quantities.core.Unit` (``K``) of
:class:`~quantities.dimensions.Temperature`.

Aliases include :attr:`deg_K`, :attr:`K`, :attr:`degree_Kelvin`,
:attr:`degrees_K`, :attr:`degree_K`, :attr:`kelvins`,
and :attr:`kelvin`.

Note:
    This is used for temperature differences.  For absolute temperature, use
    :attr:`~quantities.temperature.abs_K`.
""" 
degree_Kelvin = degrees_Kelvin  #: alias of :attr:`degrees_Kelvin`
degrees_K = degrees_Kelvin  #: alias of :attr:`degrees_Kelvin`
degree_K = degrees_Kelvin  #: alias of :attr:`degrees_Kelvin`
kelvins = degrees_Kelvin  #: alias of :attr:`degrees_Kelvin`
kelvin = degrees_Kelvin  #: alias of :attr:`degrees_Kelvin`
deg_K = degrees_Kelvin  #: alias of :attr:`degrees_Kelvin`
K = degrees_Kelvin  #: alias of :attr:`degrees_Kelvin`

degrees_Celsius = kelvin.as_unit("°C")
"""
:class:`~quantities.core.Unit` (``°C = K``) of
:class:`~quantities.dimensions.Temperature`.

Aliases include :attr:`deg_C`, :attr:`degree_Celsius`,
:attr:`degrees_C`, :attr:`degree_C`,
:attr:`degrees_centigrade`, and :attr:`degree_centigrade`.

Note:
    This is used for temperature differences.  For absolute temperature, use
    :attr:`~quantities.temperature.abs_C`.
""" 
degree_Celsius = degrees_Celsius  #: alias of :attr:`degrees_Celsius`
degrees_C = degrees_Celsius  #: alias of :attr:`degrees_Celsius`
degree_C = degrees_Celsius  #: alias of :attr:`degrees_Celsius`
degrees_centigrade = degrees_Celsius  #: alias of :attr:`degrees_Celsius`
degree_centigrade = degrees_Celsius  #: alias of :attr:`degrees_Celsius`
deg_C = degrees_Celsius  #: alias of :attr:`degrees_Celsius`


# luminous intensity
cd = candelas = candela = dimensions.LumInt.base_unit("cd")

# luminous flux
lm = lumens = lumen = (cd*sr).as_unit("lm")

# illuminance
lx = lux = (lm/m**2).as_unit("lux")

# current
A = amperes = ampere = dimensions.Current.base_unit("A")

# charge
C = coulombs = coulomb = (A*s).as_unit("C")
faradays = faraday = (96485.33212310084*C).as_unit("F")

# voltage, electric potential, emf
V = volts = volt = (J/C).as_unit("V")
mV = millivolts = millivolt = prefixes.milli(volts)
kV = kilovolts = kilovolt = prefixes.kilo(volts)

# magnetic flux
Wb = webers = weber = (V*s).as_unit("Wb")

# magnetic induction, flux density
T = teslas = tesla = (Wb/m**2).as_unit("T")

# capacitance
F = farads = farad = (C/V).as_unit("F")

# resistance
Ω = ohms = ohm = (V/A).as_unit("Ω")

# conductance
S = siemens = (A/V).as_unit("S")
mhos = mho = S.as_unit("mho")

# inductance
H = henrys = henry = (V*s/A).as_unit("H")

# radioactivity
Bq = becquerels = becquerel = (1/s).as_unit("Bq")

# ionizing radiation dose
Gy = grays = gray = (J/kg).as_unit("Gy")
Sv = sieverts = sievert = (J/kg).as_unit("Sv")

# amount
mol = moles = mole = dimensions.Amount.base_unit("mol")
mmol = millimoles = millimole = prefixes.milli(mole)
µmol = umol = micromoles = micromole = prefixes.micro(mole)

# molar concentration
M = molar = (mmol/L).as_unit("M")
mM = millimolar = prefixes.milli(molar)
µM = micromolar = prefixes.micro(molar)
nM = nanomolar = prefixes.nano(molar)

