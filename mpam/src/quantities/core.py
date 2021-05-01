import numbers

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
            raise TypeError("RHS of %s is not a Quantity: %s" % (op, rhs))
        if not rhs.has_dimensionality(self.dimensionality):
            raise TypeError("%s %s %s is ill-formed" % (self.dimensionality, op, rhs.dimensionality))

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
            raise DimMismatchError(self.dimensionality, " in ", "{0} ({1})".format(units, units.dimensionality()))
        return _BoundQuantity(self, units)
    
    def as_number(self, units):
        return self.in_units(units).magnitude

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

    def _index_in(self, abbr, lst):
        for (i, pair) in enumerate(lst):
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
