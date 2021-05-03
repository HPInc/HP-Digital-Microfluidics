import numbers
from typing import Tuple, Optional, ClassVar, Callable, TypeVar, Generic, \
    overload, Union, NewType, cast, Type, Mapping, MutableMapping
from erk.stringutils import split_camel_case

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
DimOpCache = MutableMapping[T, 'Dimensionality']
AbbrExp = tuple[str, int]

D = TypeVar('D', bound='Quantity')
ND = TypeVar('ND', bound='NamedDim')

Quant = Union['UnknownDimQuant', 'NamedDim[ND]']
        
class Dimensionality(Generic[D]):
    
    _instances: ClassVar[dict[BaseExpTuple, 'Dimensionality']] = {}
    exponents: BaseExpTuple
    name: Optional[str]
    quant_class: Type[D]
    _cached_description: str
    _desc_expt_fmt: object           # It's an ExptFormatter, but all I care about is whether it has changed
    _cached_multiplication: DimOpCache['Dimensionality']
    _cached_division: DimOpCache['Dimensionality']
    _cached_power: DimOpCache[int]

    def __init__(self, expts: BaseExpTuple, name: Optional[str] = None) -> None:
        self.exponents = expts      # a tuple of sorted base/expt tuples
        self.name = name
        # self.quant_class = UnknownDimQuant
        self._instances[self.exponents] = self

    def __repr__(self) -> str:
        return self.name or self.description()

    def named(self, name: str) -> 'Dimensionality':
        self.name = name
        return self
    
    def make_quantity(self, mag: float) -> D:
        return self.quant_class(mag, self)

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
        if d is None:
            d = Dimensionality(expts)
            d.quant_class = UnknownDimQuant
        return d

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

class BaseDimension(Dimensionality[ND]):
    _sort_name: str
    
    def __init__(self, name: str) -> None:
        super().__init__(((self,1),), name)
        self._sort_name = name

    def __lt__(self, other: 'BaseDimension') -> bool:
        return self._sort_name < other._sort_name
    
    def description(self, *, exponent_fmt: ExptFormatter = None) -> str:  # @UnusedVariable
        return self._sort_name

    def base_unit(self, abbr: str) -> 'Unit[ND]':
        return Unit[ND](abbr, cast(ND, self.make_quantity(1)))
    

class DimensionalityError(Exception):
    def __init__(self, expected: Dimensionality, got: Dimensionality) -> None:
        super().__init__("Expected {} ({}) got {}".format(expected, expected.description(), got))

class DimMismatchError(Exception):
    def __init__(self, lhs, op, rhs) -> None:
        super().__init__("{0} {1} {2}".format(lhs, op, rhs))

class Quantity(Generic[D]):
    dimensionality: Dimensionality
    magnitude: float

    # def __init__(self, mag: float, dim: Dimensionality[D]) -> None:
    def __init__(self, mag: float, dim: Dimensionality) -> None:
        self.dimensionality = dim
        self.magnitude = mag

    def __repr__(self) -> str:
        return "Quantity({0}, {1})".format(self.magnitude, self.dimensionality)
    

    def cast(self: D) -> D:
        return self

    def has_dimensionality(self, dim: Dimensionality) -> bool:
        if not isinstance(dim, Dimensionality):
            raise TypeError("Not a Dimensionaluty: %s" % dim)
        return self.dimensionality is dim

    def check_dimensionality(self: D, dim: Dimensionality) -> D:
        if not self.has_dimensionality(dim):
            raise DimensionalityError(dim, self.dimensionality)
        return self
        
    def a(self, expected: Type[ND]) -> ND:
        return cast(ND, self.check_dimensionality(expected.dim()))
    
    an = a

    def _ensure_dim_match(self, rhs: 'Quantity', op: str) -> None:
        if not isinstance(rhs, Quantity):
            raise TypeError("RHS of %s is not a Quantity: %s" % (op, rhs))
        if not rhs.has_dimensionality(self.dimensionality):
            raise TypeError("%s %s %s is ill-formed" % (self.dimensionality, op, rhs.dimensionality))

    def __add__(self: D, rhs: 'Quant') -> D:
        self._ensure_dim_match(rhs, "+")
        return cast(D, self.dimensionality.make_quantity(self.magnitude+rhs.magnitude))

    def __sub__(self: D, rhs: Union[D, 'Quantity[D]']) -> D:
        self._ensure_dim_match(rhs, "-")
        return cast(D, self.dimensionality.make_quantity(self.magnitude-rhs.magnitude))

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Quantity): 
            return False
        self._ensure_dim_match(rhs, "==")
        return self.magnitude == rhs.magnitude
    
    def __lt__(self, rhs: D) -> bool:
        self._ensure_dim_match(rhs, "<")
        return self.magnitude < rhs.magnitude
    
    def __le__(self, rhs: D) -> bool:
        self._ensure_dim_match(rhs, "<=")
        return self.magnitude <= rhs.magnitude
    
    def multiply_by(self, rhs: 'Quant') -> 'Quant':
        if not isinstance(rhs, Quantity):
            raise TypeError("RHS not a Quantity: %s" % rhs)
        new_dim = self.dimensionality*rhs.dimensionality
        return new_dim.make_quantity(self.magnitude*rhs.magnitude)
                        
    def divide_by(self, rhs: 'Quant') -> 'Quant':
        if not isinstance(rhs, Quantity):
            raise TypeError("RHS not a Quantity: %s" % rhs)
        new_dim = self.dimensionality/rhs.dimensionality
        return new_dim.make_quantity(self.magnitude/rhs.magnitude)
    def in_denom(self, lhs: float) -> 'Quant':
        if not isinstance(lhs, numbers.Real):
            raise TypeError("LHS not a real number: %s" % lhs)
        new_dim = self.dimensionality**(-1)
        return new_dim.make_quantity(lhs/self.magnitude)
    
    def to_power(self, rhs: int) -> 'Quant':
        if not isinstance(rhs, numbers.Integral):
            raise TypeError("RHS not an integer: %s" % rhs)
        new_dim = self.dimensionality**rhs
        return new_dim.make_quantity(self.magnitude**rhs)

    @overload
    def __mul__(self, rhs: float) -> D: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: 'Quant') -> 'Quant': ...  # @UnusedVariable
    def __mul__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return self.dimensionality.make_quantity(self.magnitude*rhs)
        return self.multiply_by(rhs)

    def __rmul__(self, lhs: float) -> D:
        if not isinstance(lhs, numbers.Real):
            raise TypeError("LHS not a real number: %s" % lhs)
        return self.dimensionality.make_quantity(lhs*self.magnitude)

    @overload
    def __truediv__(self, rhs: float) -> D: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: 'Quant') -> 'Quant': ...  # @UnusedVariable
    def __truediv__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return self.dimensionality.make_quantity(self.magnitude/rhs)
        return self.divide_by(rhs)

    def __rtruediv__(self, lhs: float) -> 'Quant':
        return self.in_denom(lhs)

    def __pow__(self, rhs: int) -> 'Quant':
        return self.to_power(rhs)

    def in_units(self: D, units: 'UnitExpr[D]') -> '_BoundQuantity[D]':
        if not isinstance(units, UnitExpr):
            raise TypeError("Not a UnitExpr: %s" % units)
        if units.dimensionality() is not self.dimensionality:
            raise DimMismatchError(self.dimensionality, " in ", "{0} ({1})".format(units, units.dimensionality()))
        return _BoundQuantity(self, units)
    
    def as_number(self, units: 'UnitExpr[D]') -> float:
        return self.in_units(units).magnitude
    
    def as_unit(self: D, abbr: str) -> 'Unit[D]':
        return Unit[D](abbr, self)
    
    def as_unit_expr(self: D, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> 'UnitExpr[D]':
        return UnitExpr[D](self, num, denom)

class UnknownDimQuant(Quantity['UnknownDimQuant']):
    def __repr__(self) -> str:
        return "UnknownDimQuant[{0},{1}]".format(self.magnitude, self.dimensionality)
    
class _BoundQuantity(Generic[D]):
    magnitude: float
    units: 'UnitExpr[D]'
    def __init__(self, quant: D, units: 'UnitExpr[D]') -> None:
        self.magnitude = quant.magnitude/units.quantity.magnitude
        self.units = units

    def description(self, *, exponent_fmt: Optional[ExptFormatter] = None) -> str:
        return "%g %s" % (self.magnitude, self.units.description(exponent_fmt = exponent_fmt))

    def __repr__(self) -> str:
        return self.description()

class UnitExpr(Generic[D]):
    quantity: D
    num: tuple[AbbrExp, ...]
    denom: tuple[AbbrExp, ...]
    
    _cached_description: str
    _desc_expt_fmt: object           # It's an ExptFormatter, but all I care about is whether it has changed
  
    def __init__(self, quant: D, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> None:
        self.quantity = quant
        self.num = num
        self.denom = denom

    def __repr__(self) -> str:
        return self.description()
        return "Unit('{0}', {1})".format(self.abbreviation, self.quantity)

    def dimensionality(self) -> Dimensionality[D]:
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


    def _combine_with(self, num: list[AbbrExp], denom: list[AbbrExp]) -> Tuple[tuple[AbbrExp,...], tuple[AbbrExp,...]]: 
        new_n = list(self.num)
        new_d = list(self.denom)

        self._add_expts(new_n, new_d, num)
        # We swap the numerator and denominator lists when processing the denominator
        self._add_expts(new_d, new_n, denom)

        return (tuple(new_n), tuple(new_d))

        
    @overload
    def __mul__(self, rhs: float) -> D: ...
    @overload
    def __mul__(self, rhs: 'UnitExpr') -> 'UnitExpr[UnknownDimQuant]': ...
    def __mul__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return self.quantity*rhs

        if not isinstance(rhs, UnitExpr):
            raise TypeError("RHS is not a number or UnitExpr: %s" % rhs)

        cache = getattr(self, "_cached_multiplication", None)
        if cache is None:
            self._cached_multiplication = cache = {}
        cached_num_denom = cache.get((rhs.num, rhs.denom))
        if cached_num_denom is None:
            cached_num_denom = self._combine_with(rhs.num, rhs.denom)
            cache[(rhs.num, rhs.denom)] = cached_num_denom
        
        t: tuple[list[AbbrExp], list[AbbrExp]] = cached_num_denom
        (new_num, new_denom) = t
        new_q = self.quantity*rhs.quantity
        res = new_q.as_unit_expr(new_num, new_denom)
        return res

    def __rmul__(self, n: float) -> D:
        if not isinstance(n, numbers.Real):
            raise TypeError("LHS is not a real number: %s" % n)
        return n*self.quantity
    
    @overload
    def __truediv__(self, rhs: float) -> D: ...
    @overload
    def __truediv__(self, rhs: 'UnitExpr') -> 'UnitExpr[UnknownDimQuant]': ...
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


    def __rtruediv__(self, n: float) -> D:
        if not isinstance(n, numbers.Real):
            raise TypeError("LHS is not a real number: %s" % n)
        return n/self.quantity
        
    # def qpow(self, rhs: int) -> UnknownDimQuant:
        # return cast(UnknownDimQuant, self.quantity**rhs)

    def __pow__(self, rhs: int) -> 'UnitExpr[UnknownDimQuant]':
        if not isinstance(rhs, numbers.Integral):
            raise TypeError("LHS not an integer: %s" % rhs)
        q = self.quantity**rhs
        num = [(a, e*rhs) for (a,e) in self.num]
        denom = [(a, e*rhs) for (a,e) in self.denom]
        return q.as_unit_expr(num, denom)

    def format(self, q: D) -> _BoundQuantity[D]:
        return q.in_units(self)

    def __mod__(self, q: D) -> _BoundQuantity[D]:
        return self.format(q)
    
    def a(self, expected: Type[ND]) -> 'UnitExpr[ND]':
        self.quantity.check_dimensionality(expected.dim())
        return cast(UnitExpr[ND], self)
    an = a
    
    def as_unit(self, abbr: str, check: Type[D] = None) -> 'Unit[D]':  # @UnusedVariable
        return Unit[D](abbr, self)
    

class Unit(UnitExpr[D]):
    abbreviation: str
    
    def __init__(self, abbr: str, quant: Union[D,UnitExpr[D]], check: Optional[Dimensionality] = None):
        if isinstance(quant, UnitExpr):
            quant = 1*quant
        if not isinstance(quant, Quantity):
            raise TypeError("Creating Unit from non-Quantity: %s" % quant)
        if check is not None and quant.dimensionality is not check:
            raise DimMismatchError(quant.dimensionality, "!=", check)
        super().__init__(quant, ((abbr, 1),), ())
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
    

class NamedDim(Quantity[ND]): 
    _dim: ClassVar[Dimensionality[ND]]
    _this_class: ClassVar[Type[ND]]
    
    def __init__(self, mag: float, dim: Dimensionality[ND] = None) -> None:
        if dim is None:
            dim = self._dim
        super().__init__(mag, dim)
        
    def __repr__(self) -> str:
        return "{0}[{1}]".format(self._this_class.__name__, self.magnitude)
    
    @classmethod
    def dim(cls: Type[ND]) -> Dimensionality[ND]:
        return cls._dim
    
    @classmethod
    def unit(cls: Type[ND], abbr: str, quant: Union[ND, 'UnitExpr[ND]']) -> 'Unit[ND]':
        return Unit[ND](abbr, quant, cls._dim)

class Scalar(NamedDim['Scalar']):
    _dim = Dimensionality['Scalar']((), 'scalar')
    
Scalar._dim.quant_class = Scalar
    
    
    
    
class DerivedDimMeta(type):
    def __new__(cls, name, base, dct):
        return super().__new__(cls, name, base, dct)
    
    def __init__(cls, name: str, base, dct) -> None:  # @UnusedVariable
        if name == "DerivedDim":
            return
        cls._this_class = cls
        d: Optional[Dimensionality] = getattr(cls, "derived", None)
        if d is None:
            raise NameError("DerivedDim {0} does not define 'derived'".format(name))
        if not isinstance(d, Dimensionality):
            raise TypeError("{0}.derived not a Dimensionality".format(name))
        if d.name is None:
            n:str = "_".join(split_camel_case(name)).lower()
            d.name = n
            d.quant_class = cast(Type[DerivedDim], cls)
        cls._dim = d
        
class DerivedDim(NamedDim[ND], metaclass=DerivedDimMeta): 
    derived: ClassVar[Dimensionality]

class BaseDimMeta(type):
    def __new__(cls, name, base, dct):
        return super().__new__(cls, name, base, dct)
    
    def __init__(cls, name: str, base, dct):  # @UnusedVariable
        if name == "BaseDim":
            return
        cls._this_class = cls
        d = getattr(cls, "_dim", None)
        if d is not None:
            raise NameError("BaseDim {0} does already define 'dim'".format(name))
        n:str = "_".join(split_camel_case(name)).lower()
        d = BaseDimension[ND](n)
        d.quant_class = cast(Type[DerivedDim], cls)
        cls._dim = d

class BaseDim(NamedDim[ND], metaclass=BaseDimMeta): 
    _dim: ClassVar[BaseDimension[ND]]
    
    @classmethod
    def base_unit(cls: Type['BaseDim[ND]'], abbr: str) -> Unit[ND]:
        return cls._dim.base_unit(abbr)


if __name__ == '__main__':
    
    ...

    # class Distance(BaseDim['Distance']): ... 
    # dist = BaseDimension[Distance]("distance")
    #
    # class Time(BaseDim['Time']): ...
    # time = BaseDimension[Time]("time")
    #
    # class Mass(BaseDim['Mass']): ...
    # mass = BaseDimension[Mass]("mass")
    #
    # m = Quantity[Mass](5, mass)
    # m2 = Quantity[Mass](3, mass)
    # t = Time(5, time)
    # seconds = time.base_unit("s")
    #
    # minutes = Unit("min", 60*seconds)
    # # meters = dist.base_unit("m")
    