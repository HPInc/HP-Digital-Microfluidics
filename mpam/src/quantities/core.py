import numbers
from typing import Tuple, Optional, ClassVar, Callable, TypeVar, Generic, \
    overload, Union, NewType


ExptFormatter = Callable[[int],str]

class Exponents:
    mapping = { "0": "\u2070", "1": "\u00B9", "2": "\u00B2",
                "3": "\u00B3", "4": "\u2074", "5": "\u2075",
                "6": "\u2076", "7": "\u2077", "8": "\u2078",
                "9": "\u2079", }

    # superscript() works fine, but the output shows up as
    # block codes in Emacs and is unreadable in mintty, so I'm not
    # going to use it.


    stars: ExptFormatter = lambda n : "" if n == 1 else "**%g" % n
    caret: ExptFormatter = lambda n : "" if n == 1 else "^%g" % n
    superscript: ExptFormatter = lambda n : ("" if n == 1
                              else "".join(Exponents.mapping[c] for c in str(n)))
    html: ExptFormatter = lambda n : "" if n == 1 else "<sup>%g</sup>" %n

    default_format: ExptFormatter = stars

T = TypeVar('T')
BaseExp = tuple['BaseDimension', int]
BaseExpTuple = Tuple[BaseExp, ...]
DimOpCache = dict[T, 'Dimensionality']
AbbrExp = tuple[str, int]

class Dimensionality:
    
    _instances: ClassVar[dict[BaseExpTuple, 'Dimensionality']] = {}
    exponents: BaseExpTuple
    name: Optional[str]
    _cached_description: str
    _desc_expt_fmt: object           # It's an ExptFormatter, but all I care about is whether it has changed
    _cached_multiplication: DimOpCache['Dimensionality']
    _cached_division: DimOpCache['Dimensionality']
    _cached_power = DimOpCache[int]

    def __init__(self, expts: BaseExpTuple, name: Optional[str] = None) -> None:
        self.exponents = expts      # a tuple of sorted base/expt tuples
        self.name = name
        self._instances[self.exponents] = self

    def __repr__(self) -> str:
        return self.name or self.description()

    def named(self, name: str) -> 'Dimensionality':
        self.name = name
        return self

    def description(self, *, exponent_fmt: Optional[ExptFormatter] = None) -> str:
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
    def _find_or_create(cls, expts: BaseExpTuple) -> 'Dimensionality':
        d = cls._instances.get(expts)
        return d or Dimensionality(expts)

    def __mul__(self, other: 'Dimensionality') -> 'Dimensionality':
        if not isinstance(other, Dimensionality):
            raise TypeError("Not a dimensionality object: %s" % other)
        cache: Optional[DimOpCache['Dimensionality']] = getattr(self, "_cached_multiplication", None)
        if cache is None:
            self._cached_multiplication = cache = {}
        res: Optional['Dimensionality'] = cache.get(other)
        if res is None:
            expts: dict['BaseDimension', int] = dict(self.exponents)
            for (d,e) in other.exponents:
                if d in expts:
                    expts[d] += e
                    if expts[d] == 0:
                        del expts[d]
                else:
                    expts[d] = e
            res = cache[other] = self._find_or_create(tuple(sorted(expts.items())))
        return res
        
    def __truediv__(self, other: 'Dimensionality') -> 'Dimensionality':
        if not isinstance(other, Dimensionality):
            raise TypeError("Not a dimensionality object: %s" % other)
        cache: Optional[DimOpCache['Dimensionality']] = getattr(self, "_cached_division", None)
        if cache is None:
            self._cached_division = cache = {}
        res: Optional['Dimensionality'] = cache.get(other)
        if res is None:
            expts: dict['BaseDimension', int] = dict(self.exponents)
            for (d,e) in other.exponents:
                if d in expts:
                    expts[d] -= e
                    if expts[d] == 0:
                        del expts[d]
                else:
                    expts[d] = -e
            res = cache[other] = self._find_or_create(tuple(sorted(expts.items())))
        return res

    def __pow__(self, n: int) -> 'Dimensionality':
        if not isinstance(n, numbers.Integral):
            raise TypeError("Exponent not integral: %s" % n)
        cache: Optional[DimOpCache[int]] = getattr(self, "_cached_power", None)
        if cache is None:
            self._cached_power = cache = {}
        res: Optional['Dimensionality'] = cache.get(n)
        if res is None:
            t = tuple(sorted((d,e*n) for (d,e) in self.exponents))
            res = cache[n] = self._find_or_create(t)
        return res
    
D = TypeVar('D', bound=Dimensionality)
        

class BaseDimension(Dimensionality, Generic[D]):
    _sort_name: str
    
    def __init__(self, name: str) -> None:
        super().__init__(((self,1),), name)
        self._sort_name = name

    def __lt__(self, other: 'BaseDimension') -> bool:
        return self._sort_name < other._sort_name
    
    def description(self, *, exponent_fmt: ExptFormatter = None) -> str:
        return self._sort_name

    def base_unit(self: D, abbr: str) -> 'Unit[D]':
        return Unit(abbr, Quantity(1, self))

scalar = Dimensionality((), "scalar")

class DimensionalityError(Exception):
    def __init__(self, expected: Dimensionality, got: Dimensionality) -> None:
        super().__init__("Expected {0}; got {1}".format(expected, got))

class DimMismatchError(Exception):
    def __init__(self, lhs, op, rhs) -> None:
        super().__init__("{0} {1} {2}".format(lhs, op, rhs))

class Quantity(Generic[D]):
    dimensionality: D
    magnitude: float
    
    def __init__(self, mag: float, dim: D) -> None:
        self.dimensionality = dim
        self.magnitude = mag

    def __repr__(self) -> str:
        return "Quantity({0}, {1})".format(self.magnitude, self.dimensionality)

    def has_dimensionality(self, dim: Dimensionality) -> bool:
        if not isinstance(dim, Dimensionality):
            raise TypeError("Not a Dimensionaluty: %s" % dim)
        return self.dimensionality is dim

    def check_dimensionality(self, dim: Dimensionality) -> 'Quantity[D]':
        if not self.has_dimensionality(dim):
            raise DimensionalityError(dim, self.dimensionality)
        return self
        
    def _ensure_dim_match(self, rhs: 'Quantity[D]', op: str) -> None:
        if not isinstance(rhs, Quantity):
            raise TypeError("RHS of %s is not a Quantity: %s" % (op, rhs))
        if not rhs.has_dimensionality(self.dimensionality):
            raise TypeError("%s %s %s is ill-formed" % (self.dimensionality, op, rhs.dimensionality))

    def __add__(self, rhs: 'Quantity[D]') -> 'Quantity[D]':
        self._ensure_dim_match(rhs, "+")
        return Quantity(self.magnitude+rhs.magnitude, self.dimensionality)

    def __sub__(self, rhs: 'Quantity[D]') -> 'Quantity[D]':
        self._ensure_dim_match(rhs, "-")
        return Quantity(self.magnitude-rhs.magnitude, self.dimensionality)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Quantity): 
            return False
        self._ensure_dim_match(rhs, "==")
        return self.magnitude == rhs.magnitude
    
    def __lt__(self, rhs: 'Quantity[D]') -> bool:
        self._ensure_dim_match(rhs, "<")
        return self.magnitude < rhs.magnitude
    
    def __le__(self, rhs: 'Quantity[D]') -> bool:
        self._ensure_dim_match(rhs, "<=")
        return self.magnitude <= rhs.magnitude

    @overload
    def __mul__(self, rhs: float) -> 'Quantity[D]': ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: 'Quantity') -> 'Quantity': ...  # @UnusedVariable
    def __mul__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return Quantity(self.magnitude*rhs, self.dimensionality)
        if not isinstance(rhs, Quantity):
            raise TypeError("RHS not a Quantity: %s" % rhs)
        return Quantity(self.magnitude*rhs.magnitude,
                        self.dimensionality*rhs.dimensionality)

    def __rmul__(self, lhs: float) -> 'Quantity[D]':
        if not isinstance(lhs, numbers.Real):
            raise TypeError("LHS not a real number: %s" % lhs)
        return Quantity(lhs*self.magnitude, self.dimensionality)

    @overload
    def __truediv__(self, rhs: float) -> 'Quantity[D]': ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: 'Quantity') -> 'Quantity': ...  # @UnusedVariable
    def __truediv__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return Quantity(self.magnitude/rhs, self.dimensionality)
        if not isinstance(rhs, Quantity):
            raise TypeError("RHS not a Quantity: %s" % rhs)
        return Quantity(self.magnitude/rhs.magnitude,
                        self.dimensionality/rhs.dimensionality)

    def __rtruediv__(self, lhs: float) -> 'Quantity':
        if not isinstance(lhs, numbers.Real):
            raise TypeError("LHS not a real number: %s" % lhs)
        return Quantity(lhs/self.magnitude, scalar/self.dimensionality)

    def __pow__(self, rhs: int) -> 'Quantity':
        if not isinstance(rhs, numbers.Integral):
            raise TypeError("LHS not an integer: %s" % rhs)
        return Quantity(self.magnitude**rhs, self.dimensionality**rhs)

    def in_units(self, units: 'UnitExpr[D]') -> '_BoundQuantity[D]':
        if not isinstance(units, UnitExpr):
            raise TypeError("Not a UnitExpr: %s" % units)
        if units.dimensionality() is not self.dimensionality:
            raise DimMismatchError(self.dimensionality, " in ", "{0} ({1})".format(units, units.dimensionality()))
        return _BoundQuantity(self, units)
    
    def as_number(self, units: 'UnitExpr[D]') -> float:
        return self.in_units(units).magnitude

class _BoundQuantity(Generic[D]):
    magnitude: float
    units: 'UnitExpr[D]'
    def __init__(self, quant: Quantity[D], units: 'UnitExpr[D]') -> None:
        self.magnitude = quant.magnitude/units.quantity.magnitude
        self.units = units

    def description(self, *, exponent_fmt: Optional[ExptFormatter] = None) -> str:
        return "%g %s" % (self.magnitude, self.units.description(exponent_fmt = exponent_fmt))

    def __repr__(self) -> str:
        return self.description()

class UnitExpr(Generic[D]):
    quantity: Quantity[D]
    num: list[AbbrExp]
    denom: list[AbbrExp]
    
    _cached_description: str
    _desc_expt_fmt: object           # It's an ExptFormatter, but all I care about is whether it has changed
  
    def __init__(self, quant: Quantity[D], num: list[AbbrExp], denom: list[AbbrExp]) -> None:
        self.quantity = quant
        self.num = num
        self.denom = denom

    def __repr__(self) -> str:
        return self.description()
        return "Unit('{0}', {1})".format(self.abbreviation, self.quantity)

    def dimensionality(self) -> D:
        return self.quantity.dimensionality

    def _index_in(self, abbr: str, lst: list[AbbrExp]) -> Union[Tuple[None,None], Tuple[int,int]]:
        for (i, pair) in enumerate(lst):
            if abbr == pair[0]:
                return (i, pair[1])
        return (None, None)

    def _add_expts(self, new_n: list[AbbrExp], new_d: list[AbbrExp], expts: list[AbbrExp]) -> None:
        for (a,e) in expts:
            (i, old_e) = self._index_in(a, new_n)
            if i is not None:
                assert old_e is not None
                # if it's in the numerator, we just add
                new_n[i] = (a,old_e+e)
                continue

            (i, old_e) = self._index_in(a, new_d)
            if i is None:
                # if it's in neither, we add to the numerator.
                new_n.append((a, e))
                continue
            assert old_e is not None
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
            
    def description(self, *, exponent_fmt: Optional[ExptFormatter] = None) -> str:
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


    def _combine_with(self, num: list[AbbrExp], denom: list[AbbrExp]) -> Tuple[list[AbbrExp], list[AbbrExp]]: 
        new_n = self.num[:]
        new_d = self.denom[:]

        self._add_expts(new_n, new_d, num)
        # We swap the numerator and denominator lists when processing the denominator
        self._add_expts(new_d, new_n, denom)

        return (new_n, new_d)

        
    @overload
    def __mul__(self, rhs: float) -> Quantity[D]: ...
    @overload
    def __mul__(self, rhs: 'UnitExpr') -> 'UnitExpr': ...
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

    def __rmul__(self, n: float) -> Quantity[D]:
        if not isinstance(n, numbers.Real):
            raise TypeError("LHS is not a real number: %s" % n)
        return n*self.quantity
    
    @overload
    def __truediv__(self, rhs: float) -> Quantity[D]: ...
    @overload
    def __truediv__(self, rhs: 'UnitExpr') -> 'UnitExpr': ...
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


    def __rtruediv__(self, n: float) -> 'UnitExpr':
        if not isinstance(n, numbers.Real):
            raise TypeError("LHS is not a real number: %s" % n)
        return n/self.quantity
        

    def __pow__(self, rhs: int) -> 'UnitExpr':
        if not isinstance(rhs, numbers.Integral):
            raise TypeError("LHS not an integer: %s" % rhs)
        q = self.quantity**rhs
        num = [(a, e*rhs) for (a,e) in self.num]
        denom = [(a, e*rhs) for (a,e) in self.denom]
        return UnitExpr(q, num, denom)

    def format(self, q: Quantity[D]) -> _BoundQuantity[D]:
        return q.in_units(self)

    def __mod__(self, q: Quantity[D]) -> _BoundQuantity[D]:
        return self.format(q)

class Unit(UnitExpr[D]):
    abbreviation: str
    
    def __init__(self, abbr: str, quant: Union[Quantity[D],UnitExpr[D]], check: Optional[Dimensionality] = None):
        if isinstance(quant, UnitExpr):
            quant = 1*quant
        if not isinstance(quant, Quantity):
            raise TypeError("Creating Unit from non-Quantity: %s" % quant)
        if check is not None and quant.dimensionality is not check:
            raise DimMismatchError(quant.dimensionality, "!=", check)
        super().__init__(quant, [(abbr, 1)], [])
        self.abbreviation = abbr

    def description(self, *, exponent_fmt: Optional[ExptFormatter] = None) -> str:
        return self.abbreviation

class Prefix:
    prefix: str
    multiplier: float
    
    def __init__(self, prefix: str, mult: float) -> None:
        if not isinstance(mult, numbers.Real):
            raise TypeError("Multipler is not a real number: %s" % mult)
        self.prefix = prefix
        self.multiplier = mult

    def __rep__(self) -> str:
        return "Prefix(%s, %s)" % (self.prefix, self.multiplier)

    def __call__(self, unit: Unit[D]) -> Unit[D]:
        if not isinstance(unit, Unit):
            raise TypeError("Prefix %s applied to non-Unit %s" % (self, unit))
        return Unit(self.prefix+unit.abbreviation, self.multiplier*unit.quantity)


if __name__ == '__main__':

    Distance = NewType('Distance', Dimensionality)
    dist = BaseDimension[Distance]("distance")
    Time = NewType('Time', Dimensionality)
    time = BaseDimension[Time]("time")
    Mass = NewType('Mass', Dimensionality)
    mass = BaseDimension[Mass]("mass")

    m = Quantity(5, mass)
    m2 = Quantity(3, mass)
    t = Quantity(5, time)
    seconds = time.base_unit("s")

    minutes = Unit("min", 60*seconds)
    meters = dist.base_unit("m")
