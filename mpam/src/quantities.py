# -*- coding: utf-8 -*-

import numbers
#from functools import cached_property

class Exponents:
    mapping = { "0": "\u2070", "1": "\u00B9", "2": "\u00B2",
                "3": "\u00B3", "4": "\u2074", "5": "\u2075",
                "6": "\u2076", "7": "\u2077", "8": "\u2078",
                "9": "\u2079", }

    # superscript() works fine, but the output shows up as
    # block codes in Emacs and is unreadable in mintty, so I'm not
    # going to use it.


    stars = lambda n : "" if n == 1 else "**%g" % n
    caret = lambda n : "" if n == 1 else "^%g" % n
    superscript = lambda n : ("" if n == 1
                              else "".join(Exponents.mapping[c] for c in str(n)))
    html = lambda n : "" if n == 1 else "<sup>%g</sup>" %n

    default_format = stars

class Dimensionality:
    
    _instances = {}

    def __init__(self, expts, name=None):
        self.exponents = expts      # a tuple of sorted base/expt tuples
        self.name = name
        self._instances[self.exponents] = self

    def __repr__(self):
        return self.name or self.description()

    def named(self, name):
        self.name = name
        return self

    def description(self, *, exponent_fmt = None):
        if exponent_fmt is None: exponent_fmt = Exponents.default_format
        cd = getattr(self, "_cached_description", None)
        if cd is None or self._desc_expt_fmt is not exponent_fmt: 
            self._desc_expt_fmt = exponent_fmt

            num = [str(d)+exponent_fmt(e)
                   for (d,e) in self.exponents
                   if e > 0]

            n = "*".join(num) if num else "1"

            denom = [str(d)+exponent_fmt(-e)
                     for (d,e) in self.exponents
                     if e < 0]


            if denom:
                n += "/"
                if len(denom) > 1: n += "("
                n += "*".join(denom)
                if len(denom) > 1: n += ")"

            cd = self._cached_description = n

        return cd

    @classmethod
    def _find_or_create(cls, expts):
        d = cls._instances.get(expts)
        return d or Dimensionality(expts)

    def __mul__(self, other):
        if not isinstance(other, Dimensionality):
            raise TypeError("Not a dimensionality object: %s" % other)
        cache = getattr(self, "_cached_multiplication", None)
        if cache is None:
            self._cached_multiplication = cache = {}
        res = cache.get(other)
        if res is None:
            expts = dict(self.exponents)
            for (d,e) in other.exponents:
                if d in expts:
                    expts[d] += e
                    if expts[d] == 0:
                        del expts[d]
                else:
                    expts[d] = e
            res = cache[other] = self._find_or_create(tuple(sorted(expts.items())))
        return res
        
    def __truediv__(self, other):
        if not isinstance(other, Dimensionality):
            raise TypeError("Not a dimensionality object: %s" % other)
        cache = getattr(self, "_cached_division", None)
        if cache is None:
            self._cached_division = cache = {}
        res = cache.get(other)
        if res is None:
            expts = dict(self.exponents)
            for (d,e) in other.exponents:
                if d in expts:
                    expts[d] -= e
                    if expts[d] == 0:
                        del expts[d]
                else:
                    expts[d] = -e
            res = cache[other] = self._find_or_create(tuple(sorted(expts.items())))
        return res

    def __pow__(self, n):
        if not isinstance(n, numbers.Integral):
            raise TypeError("Exponent not integral: %s" % n)
        cache = getattr(self, "_cached_power", None)
        if cache is None:
            self._cached_power = cache = {}
        res = cache.get(n)
        if res is None:
            t = tuple(sorted((d,e*n) for (d,e) in self.exponents))
            res = cache[n] = self._find_or_create(t)
        return res
        

class BaseDimension(Dimensionality):
    def __init__(self, name):
        super().__init__(((self,1),), name)

    def __lt__(self, other):
        return self.name < other.name

    def description(self, *, exponent_fmt = None):
        return self.name

    def base_unit(self, abbr):
        return Unit(abbr, Quantity(1, self))

scalar = Dimensionality((), "scalar")

class DimensionalityError(Exception):
    def __init__(self, expected, got):
        super().__init__("Expected {0}; got {1}".format(expected, got))

class DimMismatchError(Exception):
    def __init__(self, lhs, op, rhs):
        super().__init__("{0} {1} {2}".format(lhs, op, rhs))

class Quantity:
    def __init__(self, mag, dim):
        self.dimensionality = dim
        self.magnitude = mag

    def __repr__(self):
        return "Quantity({0}, {1})".format(self.magnitude, self.dimensionality)

    def has_dimensionality(self, dim):
        if not isinstance(dim, Dimensionality):
            raise TypeError("Not a Dimensionaluty: %s" % dim)
        return self.dimensionality is dim

    def check_dimensionality(self, dim):
        if not self.has_dimensionality(dim):
            raise DimensionalityError(dim, self.dimensionality)
        return self
        
    def _ensure_dim_match(self, rhs, op):
        if not isinstance(rhs, Quantity):
            raise TypeError("RHS not a Quantity: %s" % rhs)
        rhs.check_dimensionality(self.dimensionality)

    def __add__(self, rhs):
        self._ensure_dim_match(rhs, "+")
        return Quantity(self.magnitude+rhs.magnitude, self.dimensionality)

    def __sub__(self, rhs):
        self._ensure_dim_match(rhs, "-")
        return Quantity(self.magnitude-rhs.magnitude, self.dimensionality)

    def __eq__(self, rhs):
        self._ensure_dim_match(rhs, "==")
        return self.magnitude == rhs.magnitude
    
    def __lt__(self, rhs):
        self._ensure_dim_match(rhs, "<")
        return self.magnitude < rhs.magnitude
    
    def __le__(self, rhs):
        self._ensure_dim_match(rhs, "<=")
        return self.magnitude <= rhs.magnitude

    def __mul__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return Quantity(self.magnitude*rhs, self.dimensionality)
        if not isinstance(rhs, Quantity):
            raise TypeError("RHS not a Quantity: %s" % rhs)
        return Quantity(self.magnitude*rhs.magnitude,
                        self.dimensionality*rhs.dimensionality)

    def __rmul__(self, lhs):
        if not isinstance(lhs, numbers.Real):
            raise TypeError("LHS not a real number: %s" % lhs)
        return Quantity(lhs*self.magnitude, self.dimensionality)

    def __truediv__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return Quantity(self.magnitude/rhs, self.dimensionality)
        if not isinstance(rhs, Quantity):
            raise TypeError("RHS not a Quantity: %s" % rhs)
        return Quantity(self.magnitude/rhs.magnitude,
                        self.dimensionality/rhs.dimensionality)

    def __rtruediv__(self, lhs):
        if not isinstance(lhs, numbers.Real):
            raise TypeError("LHS not a real number: %s" % lhs)
        return Quantity(lhs/self.magnitude, scalar/self.dimensionality)

    def __pow__(self, rhs):
        if not isinstance(rhs, numbers.Integral):
            raise TypeError("LHS not an integer: %s" % rhs)
        return Quantity(self.magnitude**rhs, self.dimensionality**rhs)

    def in_units(self, units):
        if not isinstance(units, UnitExpr):
            raise TypeError("Not a UnitExpr: %s" % units)
        if units.dimensionality() is not self.dimensionality:
            raise DimMismatchError(self.dimensionality, " in ", units.dimensionality)
        return _BoundQuantity(self, units)

class _BoundQuantity:
    def __init__(self, quant, units):
        self.magnitude = quant.magnitude/units.quantity.magnitude
        self.units = units

    def description(self, *, exponent_fmt = None):
        return "%g %s" % (self.magnitude, self.units.description(exponent_fmt = exponent_fmt))

    def __repr__(self):
        return self.description()

class UnitExpr:
    def __init__(self, quant, num, denom):
        self.quantity = quant
        self.num = num
        self.denom = denom

    def __repr__(self):
        return self.description()
        return "Unit('{0}', {1})".format(self.abbreviation, self.quantity)

    def dimensionality(self):
        return self.quantity.dimensionality

    def _index_in(self, abbr, list):
        for (i, pair) in enumerate(list):
            if abbr == pair[0]:
                return (i, pair[1])
        return (None, None)

    def _add_expts(self, new_n, new_d, expts):
        for (a,e) in expts:
            (i, old_e) = self._index_in(a, new_n)
            if i is not None:
                # if it's in the numerator, we just add
                new_n[i] = (a,old_e+e)
                continue

            (i, old_e) = self._index_in(a, new_d)
            if i is None:
                # if it's in neither, we add to the numerator.
                new_n.append((a, e))
                continue

            # it's in the denominator.  If the values are the same, we
            # can get rid of it.
            if e == old_e:
                del new_d[i]
                continue

            # if the old denom (expt) is greater than the new one, we
            # leave it in the denominator, but lower the magnitude.
            if e < old_e:
                new_d[i] = (a, old_e-e)
                continue

            # otherwise, we take it out of the denominator and put the
            # difference in the numerator.
            del new_d[i]
            new_n.append((a,e-old_e))
            
    def description(self, *, exponent_fmt = None):
        if exponent_fmt is None: exponent_fmt = Exponents.default_format
        cd = getattr(self, "_cached_description", None)
        if cd is None or self._desc_expt_fmt is not exponent_fmt: 
            self._desc_expt_fmt = exponent_fmt
            num = [a+exponent_fmt(e) for (a, e) in self.num]
            n = "*".join(num)
            denom = [a+exponent_fmt(e) for (a, e) in self.denom]
            if denom:
                n += "/"+"*".join(denom)
            cd = self._cached_description = n
        return cd


    def _combine_with(self, num, denom):
        new_n = self.num[:]
        new_d = self.denom[:]

        self._add_expts(new_n, new_d, num)
        # We swap the numerator and denominator lists when processing the denominator
        self._add_expts(new_d, new_n, denom)

        return (new_n, new_d)

        

    def __mul__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return self.quantity*rhs

        if not isinstance(rhs, UnitExpr):
            raise TypeError("RHS is not a number or UnitExpr: %s" % rhs)

        cache = getattr(self, "_cached_multiplication", None)
        if cache is None:
            self._cached_multiplication = cache = {}
        res = cache.get(rhs)
        if res is None:
            (new_num, new_denom) = self._combine_with(rhs.num, rhs.denom)
            res = UnitExpr(self.quantity*rhs.quantity, new_num, new_denom)
            cache[rhs] = res
        return res

    def __rmul__(self, n):
        if not isinstance(n, numbers.Real):
            raise TypeError("LHS is not a real number: %s" % n)
        return n*self.quantity

    def __truediv__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return self.quantity/rhs

        if not isinstance(rhs, UnitExpr):
            raise TypeError("RHS is not a number or UnitExpr: %s" % rhs)

        cache = getattr(self, "_cached_division", None)
        if cache is None:
            self._cached_multiplication = cache = {}
        res = cache.get(rhs)
        if res is None:
            (new_num, new_denom) = self._combine_with(rhs.denom, rhs.num)
            res = UnitExpr(self.quantity/rhs.quantity, new_num, new_denom)
            cache[rhs] = res
        return res


    def __rtruediv__(self, n):
        if not isinstance(n, numbers.Real):
            raise TypeError("LHS is not a real number: %s" % n)
        return n/self.quantity
        

    def __pow__(self, rhs):
        if not isinstance(rhs, numbers.Integral):
            raise TypeError("LHS not an integer: %s" % rhs)
        q = self.quantity**rhs
        num = [(a, e*rhs) for (a,e) in self.num]
        denom = [(a, e*rhs) for (a,e) in self.denom]
        return UnitExpr(q, num, denom)

    def format(self, q):
        return q.in_units(self)

    def __mod__(self, q):
        return self.format(q)

class Unit(UnitExpr):
    def __init__(self, abbr, quant, check = None):
        if isinstance(quant, UnitExpr):
            quant = 1*quant
        if not isinstance(quant, Quantity):
            raise TypeError("Creating Unit from non-Quantity: %s" % quant)
        if check is not None and quant.dimensionality is not check:
            raise DimMismatchError(quant.dimensionality, "!=", check)
        super().__init__(quant, [(abbr, 1)], [])
        self.abbreviation = abbr

    def description(self, *, exponent_fmt = None):
        return self.abbreviation

class Prefix:
    def __init__(self, prefix, mult):
        if not isinstance(mult, numbers.Real):
            raise TypeError("Multipler is not a real number: %s" % mult)
        self.prefix = prefix
        self.multiplier = mult

    def __rep__(self):
        return "Prefix(%s, %s)" % (self.prefix, self.multiplier)

    def __call__(self, unit):
        if not isinstance(unit, Unit):
            raise TypeError("Prefix %s applied to non-Unit %s" % (self, unit))
        return Unit(self.prefix+unit.abbreviation, self.multiplier*unit.quantity)

Prefix.yotta = Prefix("Y", 1e24)
Prefix.zetta = Prefix("Z", 1e21)
Prefix.exa   = Prefix("E", 1e18)
Prefix.peta  = Prefix("P",  1e15)
Prefix.tera  = Prefix("T",  1e12)
Prefix.giga  = Prefix("G",  1e9)
Prefix.mega  = Prefix("M",  1e6)
Prefix.kilo  = Prefix("k",  1e3)
Prefix.hecto = Prefix("h", 1e2)
Prefix.deka  = Prefix("da", 1e1)
Prefix.deci  = Prefix("d",  1e-1)
Prefix.centi = Prefix("c", 1e-2)
Prefix.milli = Prefix("m", 1e-3)
Prefix.micro = Prefix("μ", 1e-6)
Prefix.nano  = Prefix("n",  1e-9)
Prefix.pico  = Prefix("p",  1e-12)
Prefix.femto = Prefix("f", 1e-15)
Prefix.atto  = Prefix("a",  1e-9)
Prefix.zepto = Prefix("z", 1e-9)
Prefix.yocto = Prefix("y", 1e-9)

# def UnitSet(name, dimensionality = None, *, attr_name = None):
#     def decorate(Class):
#         d = BaseDimension(name) if dimensionality is None else dimensionality.named(name)
#         setattr(Class, attr_name or name, d)

#         old_getattr = getattr(Class, "__getattr__", None)

#         def new_getattr(self, name):
#             print("Looking up ", name)
#             lazy = getattr(self, "_lazy_"+name, None)
#             if lazy is None:
#                 if old_getattr is not None:
#                     return old_getattr(self, name)
#                 else:
#                     raise AttributeError(name)
#             print("Instantiating ", name)
#             res = lazy(self)
#             setattr(self, name, res)
#             return res
                
#         setattr(Class, "__getattr__", new_getattr)
#         return Class
#     return decorate

# @UnitSet("distance")
# class Distance:
#     @staticmethod
#     @cached_property
#     def foo(dist):
#         return dist.distance.base_unit("m")
#     _lazy_meter = lambda dist: dist.distance.base_unit("m")
#     _lazy_m = lambda dist: dist.meter


# @UnitSet("area", Distance.distance**2)
# class Area:
#     ...

# class UnitSetMeta(type):
#     def __getattr__(self, name):
#         print("Looking up ", name)
#         lazy = getattr(self, "_lazy_"+name, None)
#         if lazy is None:
#             return super().__getattr__(self, name)
#         print("Instantiating ", name)
#         res = lazy(self)
#         setattr(self, name, res)
#         return res

#     def test():
#         return 10

#     ...

# class lazy_unit:
#     def __init__(self, func):
#         self.func = func

#     def __set_name__(self, owner, name):
#         print("Assigned to ", name)
#         self.name = name

#     def __get__(self, instance, owner=None):
#         res = self.func(owner)
#         print("Computed ", res)
#         setattr(owner, self.name, res)
#         return res

# def lazy_base_unit(abbr):
#     return LazyUnit(lambda cls: cls.base_unit(abbr))

# #class UnitSetBase(metaclass = UnitSetMeta):
# class UnitSetBase:
#     def __init_subclass__(cls, *, name, dimensionality = None, attr_name = None, **kwargs):
#         super().__init_subclass__(**kwargs)
#         d = BaseDimension(name) if dimensionality is None else dimensionality.named(name)
#         cls.dim = d
#         setattr(cls, attr_name or name, d)

#     @classmethod
#     def base_unit(cls, name):
#         return cls.dim.base_unit(name)

#     @classmethod
#     def alias(cls, name):
#         print("An alias for ", name)
        
#     @staticmethod
#     def lazy_base_unit(name):
#         return lazy_unit(lambda cls: cls.base_unit(name))

# class Dist(UnitSetBase, name="distance"):
#     meter = lazy_base_unit("m")
#     m = meter


mass = BaseDimension("mass")
distance = BaseDimension("distance")
time = BaseDimension("time")
temperature = BaseDimension("temperature")
lum_int = BaseDimension("lum_int")
current = BaseDimension("current")
storage = BaseDimension("storage")

angle = scalar
solid_angle = scalar
area = (distance**2).named("area")
volume = (distance**3).named("volume")
frequency = (scalar/time).named("frequency")
radioactivity = frequency
velocity = (distance/time).named("velocity")
acceleration = (velocity/time).named("acceleration")
force = (mass*acceleration).named("force")
work = (force*distance).named("work")
pressure = (force/area).named("pressure")
power = (work/time).named("power")
lum_flux = lum_int
charge = (current*time).named("charge")
voltage = (work/charge).named("voltage")
emf = elec_potential = voltage
flux = (voltage*time).named("flux")
magnetic_flux = flux
flux_density = (flux/area).named("flux_density")
magnetic_induction = flux_density
capacitance = (charge/voltage).named("capacitance")
resistance = (voltage/current).named("resistance")
conductance = (current/voltage).named("conductance")
inductance = (resistance*time).named("inductance")
ionizing_rad_dose = (work/mass).named("ionizing_rad_dose")


class SI:
    # angle
    rad = radian = Unit("rad", Quantity(1, scalar))
    sr = steraian = Unit("sr", Quantity(1, scalar))

    # mass
    g = gramme = gram = mass.base_unit("g")
    µg = ug = microgramme = microgram = Prefix.micro(gram)
    mg = milligramme = milligram = Prefix.milli(gram)
    kg = kilogramme = kilogram = Prefix.kilo(gram)
    tonne = metric_tonne = metric_ton = Unit("tonne", 1000*kg)

    # distance
    m = metre = meter = distance.base_unit("m")
    dm = decimetre = decimeter = Prefix.deci(meter)
    cm = centimetre = centimeter = Prefix.centi(meter)
    mm = millimetre = millimeter = Prefix.milli(meter)
    µm = um = micron = micrometre = micrometer = Prefix.micro(meter)
    nm = nanometre = nanometer = Prefix.nano(meter)
    km = kilometre = kilometer = Prefix.kilo(meter)

    # area
    ha = hectare = Unit("ha", m**2)
    
    # volume
    l = L = litre = liter = Unit("l", dm**3)
    dl = dL = decilitre = deciliter = Prefix.deci(liter)
    cl = cL = centilitre = centiliter = Prefix.centi(liter)
    ml = mL = millilitre = milliliter = Prefix.milli(liter)
    µl = µL = ul = uL = micorlitre = microliter = Prefix.micro(liter)
    st = stere = Unit("st", m**3)

    # time
    s = sec = second = time.base_unit("s")
    ms = msec = millisec = millisecond = Prefix.milli(second)
    µs = us = µsec = usec = microsec = microsecond = Prefix.micro(second)
    ns = nsec = nanosec = nanosecond = Prefix.nano(second)
    min = minute = Unit("min", 60*second)
    hr = hour = Unit("hr", 60*minute)
    day = Unit("day", 24*hour)

    # frequency
    Hz = hertz = Unit("Hz", 1/s)

    # force
    N = newton = Unit("N", kg*m/s**2)

    # work
    J = joule = Unit("J", N*m)

    # pressure
    Pa = pascal = Unit("Pa", N/m**2)

    # power
    W = watt = Unit("W", J/s)

    # temperature
    K = kelvin = temperature.base_unit("K")
    deg_K = kelvin
    deg_C = Unit("°C", kelvin)

    # luminous intensity
    cd = candela = lum_int.base_unit("cd")

    # luminous flux
    lm = lumen = Unit("lm", cd*sr)

    # illuminance
    lx = lux = Unit("lux", lm/m**2)

    # current
    A = ampere = current.base_unit("A")

    # charge
    C = coulomb = Unit("C", A*s)
    faraday = Unit("F", 96485.33212310084*C)

    # voltage, electric potential, emf
    V = volt = Unit("V", J/C)

    # magnetic flux
    Wb = weber = Unit("Wb", V*s)

    # magnetic induction, flux density
    T = tesla = Unit("T", Wb/m**2)

    # capacitance
    F = farad = Unit("F", C/V)

    # resistance
    Ω = ohm = Unit("Ω", V/A)

    # conductance
    S = siemens = Unit("S", A/V)
    mho = Unit("mho", S)

    # inductance
    H = henry = Unit("H", V*s/A)

    # radioactivity
    Bq = becquerel = Unit("Bq", 1/s)

    # ionizing radiation dose
    Gy = gray = Unit("Gy", J/kg)
    Sv = sievert = Unit("Sv", J/kg)
    
    

class Force:
    ...

class US:
    # mass
    lb = pound = Unit("lb", 0.45359237*SI.kg)
    oz = ounce = Unit("oz", lb/16)
    dr = dram = Unit("dr", oz/16)
    gr = grain = Unit("gr", lb/7000)
    ct = carat = Unit("ct", 200*SI.mg)
    cwt = hundredweight = Unit("cwt", 100*lb)
    ton = Unit("ton", 2000*lb)
    long_cwt = long_hundredweight = Unit("long_cwt", 112*lb)
    long_ton = Unit("long_ton", 2240*lb)

    dwt = pennyweight = Unit("dwt", 24*gr)
    oz_t = troy_oz = troy_ounce = Unit("oz_t", 20*dwt)
    lb_t = troy_lb = troy_pound = Unit("lb_t", 12*oz_t)

    slug = Unit("slug", 32.1740*lb)

    # distance 

    inch = Unit("in", 2.54*SI.cm)
    ft = foot = Unit("ft", 12*inch)
    yd = yard = Unit("yd", 3*ft)
    mi = mile = Unit("mi", 5280*ft)
    point = Unit("point", inch/72)
    fur = furlong = Unit("fur", 660*ft)
    lea = league = Unit("lea", 3*mi)
    ftm = fathom = Unit("yd", 2*yd)
    nmi = nautical_mile = Unit("nmi", 1.151*mi)
    hand = Unit("hand", 4*inch)
    th = thou = Unit("th", inch/1000)
    ch = chain = Unit("ch", 66*ft)
    cable = Unit("cable", 100*ftm)

    #area

    sq_in = square_inch = Unit("sq_in", inch**2)
    sq_ft = square_foot = Unit("sq_ft", ft**2)
    sq_mi = square_mile = Unit("sq_mi", mi**2)
    acre = Unit("acre", sq_mi/640)
    section = Unit("section", sq_mi)

    # volume
    cu_in = cubic_inch = Unit("cu_in", inch**3)
    gal = gallon = Unit("gal", 231*cu_in)
    fl_oz = fluid_ounce = Unit("fl_oz", gal/128)
    qt = quart = Unit("qt", 32*fl_oz)
    pt = pint = Unit("pt", 16*fl_oz)
    cup = Unit("C", 8*fl_oz)
    Tbsp = tablespoon = Unit("Tbsp", fl_oz/2)
    tsp = teaspoon = Unit("tsp", Tbsp/3)
    fl_dr = fluid_dram = Unit("fl_dr", Tbsp/4)
    minim = Unit("min", tsp/80)
    shot = jig = jigger = Unit("jig", 1.5*fl_oz)
    bbl = barrel = Unit("bbl", 31.5*gal)
    hogshead = Unit("hogshead", 63*gal)
    board_ft = board_foot = Unit("board_ft", ft**2*inch)

    pt_d = dry_pt = dry_pint = Unit("pt_d", 33.6003125*cu_in)
    qt_d = dry_qt = dry_quart = Unit("qt_d", 2*pt_d)
    gal_d = dry_gal = dry_gallon = Unit("gal_d", 4*qt_d)
    pk = peck = Unit("pk", 2*gal_d)
    bu = bushel = Unit("bu", 4*pk)
    bbl_d = dry_bbl = dry_barrel = Unit("bbl_d", 7056*cu_in)

    # time

    s = SI.s
    min = SI.min
    hr = SI.hr

    # velocity
    fps = foot_per_second = Unit("fps", ft/s)
    mph = mile_per_hour = Unit("mph", mi/hr)

    # temperature
    deg_F = Unit("°F", 1.8*SI.deg_C)

    # work
    Btu = Unit("Btu", 1054*Prefix.kilo(SI.J))
    cal = small_cal = small_calorie = Unit("cal", 4.184*SI.J)
    kcal = kilocalorie = Prefix.kilo(small_cal)
    Cal = food_calorie = calorie = Unit("Cal", kcal)

    # force
    pdl = poundal = Unit("pdl", lb*ft/s**2)
    lbf = pound_force = Unit("lbf", slug*ft/s**2)

    # pressure
    psi = Unit("psi", lbf/sq_in)

    # power
    hp = horsepower = Unit("hp", 845.7*SI.W)
    
    
    
    


if __name__ == '__main__':

    dist = BaseDimension("distance")
    time = BaseDimension("time")
    mass = BaseDimension("mass")

    m = Quantity(5, mass)
    m2 = Quantity(3, mass)
    t = Quantity(5, time)
    seconds = time.base_unit("s")

    minutes = Unit("min", 60*seconds)
    meters = dist.base_unit("m")
