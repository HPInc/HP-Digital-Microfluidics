from __future__ import annotations
import numbers
from typing import Optional, ClassVar, Callable, TypeVar, Generic, \
    overload, Union, cast, MutableMapping, Any, Final, Tuple
from erk.stringutils import split_camel_case, infer_plural
import math

ExptFormatter = Callable[[int],str]

class Exponents:
    mapping = { "0": "\u2070", "1": "\u00B9", "2": "\u00B2",
                "3": "\u00B3", "4": "\u2074", "5": "\u2075",
                "6": "\u2076", "7": "\u2077", "8": "\u2078",
                "9": "\u2079", }

    # superscript() works fine, but the output shows up as
    # block codes in Emacs and is unreadable in mintty, so I'm not
    # going to use it.


    stars: ExptFormatter = lambda n : "" if n == 1 else f"**{n:g}" 
    caret: ExptFormatter = lambda n : "" if n == 1 else f"^{n:g}"
    superscript: ExptFormatter = lambda n : ("" if n == 1
                              else "".join(Exponents.mapping[c] for c in str(n)))
    html: ExptFormatter = lambda n : "" if n == 1 else f"<sup>{n:g}</sup>"

    default_format: ExptFormatter = stars

T = TypeVar('T')
BaseExp = tuple['BaseDimension', int]
BaseExpTuple = Tuple[BaseExp, ...]
DimOpCache = MutableMapping[T, 'Dimensionality']
AbbrExp = tuple[Union[str, tuple[str,str]], int]

D = TypeVar('D', bound='Quantity')
ND = TypeVar('ND', bound='NamedDim')

Quant = Union['UnknownDimQuant', 'NamedDim[ND]']

# def _restriction_name(obj) -> str:
#     return 
        
def _restriction_name(restriction):
    return restriction.__name__ if isinstance(restriction, type) else str(restriction)

class Dimensionality(Generic[D]):
    
    _instances: ClassVar[dict[BaseExpTuple, Dimensionality]] = {}
    exponents: BaseExpTuple
    name: Optional[str]
    quant_class: type[D]
    _cached_description: str
    _desc_expt_fmt: object           # It's an ExptFormatter, but all I care about is whether it has changed
    _cached_multiplication: DimOpCache[Dimensionality]
    _cached_division: DimOpCache[Dimensionality]
    _cached_power: DimOpCache[int]
    _restrictions: dict[Any, BaseDimension]
    _default_units: Optional[UnitExpr[D]]
    _unrestricted: Optional[Dimensionality[D]] = None
    _restriction: Optional[Any] = None

    def __init__(self, expts: BaseExpTuple, name: Optional[str] = None) -> None:
        self.exponents = expts      # a tuple of sorted base/expt tuples
        self.name = name
        # self.quant_class = UnknownDimQuant
        self._instances[self.exponents] = self
        self._restrictions = dict[Any, BaseDimension]()
        self._default_units = None

    def __repr__(self) -> str:
        return self.name or self.description()

    def named(self, name: str) -> Dimensionality:
        self.name = name
        return self
    
    @property
    def default_units(self) -> Optional[UnitExpr[D]]:
        units = self._default_units
        # print(f"Finding default units for {self}")
        if units is None:
            us: Optional[UnitExpr] = None
            for t in self.exponents:
                # If we're a base and we don't have default, our tuple
                # will be ((self,1),), which would cause an infinite recursion
                if t[0] is self:
                    # but if we're restricted, we can delegate to our unrestricted one
                    if self._unrestricted is None:
                        return None
                    unr_units = self._unrestricted.default_units
                    if unr_units is None:
                        return None
                    if isinstance(unr_units, Unit):
                        return unr_units.of(self._restriction)
                    desc: str = unr_units.description(mag=2)
                    return unr_units.as_unit(f"({desc})").of(self._restriction)
                du = t[0].default_units
                if du is None:
                    return None
                u: UnitExpr = du**t[1]
                us = u if us is None else us*u
            units = us
            self._default_units = units
        return units
    
    @default_units.setter
    def default_units(self, units: UnitExpr[D]):
        self._default_units = units    
    
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
    def _find_or_create(cls, expts: BaseExpTuple) -> Dimensionality:
        d = cls._instances.get(expts)
        if d is None:
            d = Dimensionality(expts)
            d.quant_class = UnknownDimQuant
        return d

    def __mul__(self, other: Dimensionality) -> Dimensionality:
        if not isinstance(other, Dimensionality):
            raise TypeError(f"Not a dimensionality object: {other}")
        cache: Optional[DimOpCache[Dimensionality]] = getattr(self, "_cached_multiplication", None)
        if cache is None:
            self._cached_multiplication = cache = {}
        res: Optional[Dimensionality] = cache.get(other)
        if res is None:
            expts: dict[BaseDimension, int] = dict(self.exponents)
            for (d,e) in other.exponents:
                if d in expts:
                    expts[d] += e
                    if expts[d] == 0:
                        del expts[d]
                else:
                    expts[d] = e
            res = cache[other] = self._find_or_create(tuple(sorted(expts.items())))
        return res
        
    def __truediv__(self, other: Dimensionality) -> Dimensionality:
        if not isinstance(other, Dimensionality):
            raise TypeError(f"Not a dimensionality object: {other}")
        cache: Optional[DimOpCache[Dimensionality]] = getattr(self, "_cached_division", None)
        if cache is None:
            self._cached_division = cache = {}
        res: Optional[Dimensionality] = cache.get(other)
        if res is None:
            expts: dict[BaseDimension, int] = dict(self.exponents)
            for (d,e) in other.exponents:
                if d in expts:
                    expts[d] -= e
                    if expts[d] == 0:
                        del expts[d]
                else:
                    expts[d] = -e
            res = cache[other] = self._find_or_create(tuple(sorted(expts.items())))
        return res

    def __pow__(self, n: int) -> Dimensionality:
        if not isinstance(n, numbers.Integral):
            raise TypeError(f"Exponent not integral: {n}")
        cache: Optional[DimOpCache[int]] = getattr(self, "_cached_power", None)
        if cache is None:
            self._cached_power = cache = {}
        res: Optional[Dimensionality] = cache.get(n)
        if res is None:
            t = tuple(sorted((d,e*n) for (d,e) in self.exponents))
            res = cache[n] = self._find_or_create(t)
        return res
    

    def of(self, restriction: T, *, dim: Optional[str] = None) -> BaseDimension:
        d = self._restrictions.get(restriction, None)
        if d is not None:
            return d
        if issubclass(self.quant_class, NamedDim):
            c = self.quant_class.restricted(restriction)
            d = c._dim
            self._restrictions[restriction] = d
            return d
        name = dim or self.name
        assert name is not None, f"Unnamed dimension {self} cannot be restricted, without 'dim='"
        restr_pname = _restriction_name(restriction)
        pname = f"{name}[{restr_pname}]"
        rname = f"{name}_{restr_pname}"
        # immediate_base = CountDim if issubclass(self.quant_class, CountDim) else BaseDim
        new_dim_class = BaseDimMeta(rname,(BaseDim,), {"_dim_name": pname})
        new_dim: BaseDimension = new_dim_class._dim
        new_dim._unrestricted = self
        new_dim._restriction = restriction
        self._restrictions[restriction] = new_dim
        return new_dim
    
    def __getitem__(self, restriction: T) -> BaseDimension:
        return self.of(restriction)
        
    
class BaseDimension(Dimensionality[ND]):
    _sort_name: str
    
    def __init__(self, name: str) -> None:
        super().__init__(((self,1),), name)
        self._sort_name = name

    def __lt__(self, other: BaseDimension) -> bool:
        return self._sort_name < other._sort_name
    
    def description(self, *, exponent_fmt: ExptFormatter = None) -> str:  # @UnusedVariable
        return self._sort_name

    def base_unit(self, abbr: str, singular: Optional[str]=None) -> Unit[ND]:
        unit = Unit[ND](abbr, cast(ND, self.make_quantity(1)), singular=singular)
        self.default_units = unit
        return unit
    

class DimensionalityError(Exception):
    def __init__(self, expected: Dimensionality, got: Dimensionality) -> None:
        super().__init__(f"Expected {expected} ({expected.description()}) got {got}")

class DimMismatchError(Exception):
    def __init__(self, lhs, op, rhs) -> None:
        super().__init__(f"{lhs} {op} {rhs}")

class Quantity(Generic[D]):
    dimensionality: Dimensionality
    magnitude: float

    # def __init__(self, mag: float, dim: Dimensionality[D]) -> None:
    def __init__(self, mag: float, dim: Dimensionality) -> None:
        self.dimensionality = dim
        self.magnitude = mag

    def __repr__(self) -> str:
        return f"Quantity({self.magnitude}, {self.dimensionality})"
    
    def __str__(self) -> str:
        units = self.dimensionality.default_units
        return self.__repr__() if units is None else self.in_units(units).__str__() 
    
    def __bool__(self) -> bool:
        return self.magnitude != 0

    def cast(self: D) -> D:
        return self
    

    def has_dimensionality(self, dim: Dimensionality) -> bool:
        if not isinstance(dim, Dimensionality):
            raise TypeError(f"Not a Dimensionaluty: {dim}")
        my_dim = self.dimensionality
        return my_dim is dim or my_dim._unrestricted is dim

    def check_dimensionality(self: D, dim: Dimensionality) -> D:
        if not self.has_dimensionality(dim):
            raise DimensionalityError(dim, self.dimensionality)
        return self
        
    def a(self, expected: type[ND]) -> ND:
        return cast(ND, self.check_dimensionality(expected.dim()))
    
    an = a

    def _ensure_dim_match(self, rhs: Quantity, op: str) -> None:
        if not isinstance(rhs, Quantity):
            raise TypeError(f"RHS of {op} is not a Quantity: {rhs}")
        if not rhs.has_dimensionality(self.dimensionality):
            raise TypeError(f"{self.dimensionality} {op} {rhs.dimensionality} is ill-formed")

    def __add__(self: D, rhs: D) -> D:
        self._ensure_dim_match(rhs, "+")
        return cast(D, self.dimensionality.make_quantity(self.magnitude+rhs.magnitude))

    def __sub__(self: D, rhs: D) -> D:
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
    
    def multiply_by(self, rhs: Quant) -> Quant:
        if not isinstance(rhs, Quantity):
            raise TypeError(f"RHS not a Quantity: {rhs}")
        new_dim = self.dimensionality*rhs.dimensionality
        return new_dim.make_quantity(self.magnitude*rhs.magnitude)
                        
    def divide_by(self, rhs: Quant) -> Quant:
        if not isinstance(rhs, Quantity):
            raise TypeError(f"RHS not a Quantity: {rhs}")
        new_dim = self.dimensionality/rhs.dimensionality
        return new_dim.make_quantity(self.magnitude/rhs.magnitude)
    def in_denom(self, lhs: float) -> Quant:
        if not isinstance(lhs, numbers.Real):
            raise TypeError(f"LHS not a Quantity: {lhs}")
        new_dim = self.dimensionality**(-1)
        return new_dim.make_quantity(lhs/self.magnitude)
    
    def to_power(self, rhs: int) -> Quant:
        if not isinstance(rhs, numbers.Integral):
            raise TypeError(f"RHS not an integer: {rhs}")
        new_dim = self.dimensionality**rhs
        return new_dim.make_quantity(self.magnitude**rhs)

    @overload
    def __mul__(self, rhs: float) -> D: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: Quant) -> Quant: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: UnitExpr) -> Quant: ...  # @UnusedVariable
    def __mul__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return self.dimensionality.make_quantity(self.magnitude*rhs)
        if isinstance(rhs, UnitExpr):
            return self.multiply_by(rhs.quantity)
        return self.multiply_by(rhs)

    def __rmul__(self, lhs: float) -> D:
        if not isinstance(lhs, numbers.Real):
            raise TypeError(f"LHS not a real number: {lhs}")
        return self.dimensionality.make_quantity(lhs*self.magnitude)

    @overload
    def __truediv__(self, rhs: float) -> D: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: Quant) -> Quant: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: UnitExpr) -> Quant: ...  # @UnusedVariable
    def __truediv__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return self.dimensionality.make_quantity(self.magnitude/rhs)
        if isinstance(rhs, UnitExpr):
            return self.divide_by(rhs.quantity)
        return self.divide_by(rhs)

    def __rtruediv__(self, lhs: float) -> Quant:
        return self.in_denom(lhs)

    def __pow__(self, rhs: int) -> Quant:
        return self.to_power(rhs)
    
    def ratio(self, base: D) -> float:
        return self.magnitude/base.magnitude

    def in_units(self: D, units: UnitExpr[D]) -> _BoundQuantity[D]:
        if not isinstance(units, UnitExpr):
            raise TypeError(f"Not a UnitExpr: {units}")
        if units.dimensionality() is not self.dimensionality:
            raise DimMismatchError(self.dimensionality, "in", f"{units} ({units.dimensionality()})")
        return _BoundQuantity(self, units)
    
    def as_number(self, units: UnitExpr[D]) -> float:
        return self.in_units(units).magnitude
    
    def as_unit(self: D, abbr: str) -> Unit[D]:
        return Unit[D](abbr, self)
    
    def as_unit_expr(self: D, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> UnitExpr[D]:
        return UnitExpr[D](self, num, denom)
    
    def of(self, restriction: T, *, dim: Optional[str] = None) -> BaseDim:
        d = self.dimensionality.of(restriction, dim=dim)
        return d.make_quantity(self.magnitude)
    
    def __getitem__(self, restriction: T) -> BaseDim:
        return self.of(restriction)
    

class UnknownDimQuant(Quantity['UnknownDimQuant']):
    def __repr__(self) -> str:
        return f"UnknownDimQuant[{self.magnitude},{self.dimensionality}]"
    
class _BoundQuantity(Generic[D]):
    magnitude: float
    units: UnitExpr[D]
    def __init__(self, quant: D, units: UnitExpr[D]) -> None:
        self.magnitude = quant.magnitude/units.quantity.magnitude
        self.units = units

    def description(self, *, exponent_fmt: Optional[ExptFormatter] = None) -> str:
        desc = self.units.description(exponent_fmt=exponent_fmt, mag=self.magnitude)
        return f"{self.magnitude:g} {desc}"

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
        return self.description(mag=0)
        # return f"Unit('{self.abbreviation}', {self.quantity})"

    def dimensionality(self) -> Dimensionality[D]:
        return self.quantity.dimensionality

    def _index_in(self, abbr: Union[str,tuple[str,str]], lst: list[AbbrExp]) -> Union[tuple[None,None], tuple[int,int]]:
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
            
    @staticmethod
    def choose_abbr(mag: float, abbrs: Union[str, tuple[str,str]]) -> str:
        # print(f"mag={mag}, abbrs={abbrs}")
        if (isinstance(abbrs, tuple)):
            return abbrs[0] if mag==1 else abbrs[1]
        else:
            return abbrs
            
    def description(self, *, mag: float, exponent_fmt: Optional[ExptFormatter] = None) -> str:
        if exponent_fmt is None: exponent_fmt = Exponents.default_format
        cd = getattr(self, "_cached_description", None)
        if cd is None or self._desc_expt_fmt is not exponent_fmt: 
            self._desc_expt_fmt = exponent_fmt
            num = [self.choose_abbr(mag, a)+exponent_fmt(e) for (a, e) in self.num]
            n = "*".join(num)
            # we always pick the singular form in the denominator
            denom = [self.choose_abbr(1, a)+exponent_fmt(e) for (a, e) in self.denom]
            if denom:
                n += "/"+"*".join(denom)
            cd = self._cached_description = n
        return cd


    def _combine_with(self, num: list[AbbrExp], denom: list[AbbrExp]) -> tuple[tuple[AbbrExp,...], tuple[AbbrExp,...]]: 
        new_n = list(self.num)
        new_d = list(self.denom)

        self._add_expts(new_n, new_d, num)
        # We swap the numerator and denominator lists when processing the denominator
        self._add_expts(new_d, new_n, denom)

        return (tuple(new_n), tuple(new_d))

        
    @overload
    def __mul__(self, rhs: float) -> D: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: UnitExpr) -> UnitExpr[UnknownDimQuant]: ...  # @UnusedVariable
    def __mul__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return self.quantity*rhs

        if not isinstance(rhs, UnitExpr):
            raise TypeError(f"RHS is not a number or UnitExpr: {rhs}")

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
            raise TypeError(f"LHS is not a real number: {n}")
        return n*self.quantity
    
    @overload
    def __truediv__(self, rhs: float) -> D: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: UnitExpr) -> UnitExpr[UnknownDimQuant]: ...  # @UnusedVariable
    def __truediv__(self, rhs):
        if isinstance(rhs, numbers.Real):
            return self.quantity/rhs

        if not isinstance(rhs, UnitExpr):
            raise TypeError(f"RHS is not a number or UnitExpr: {rhs}")

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
            raise TypeError(f"LHS is not a real number: {n}")
        return n/self.quantity
        
    # def qpow(self, rhs: int) -> UnknownDimQuant:
        # return cast(UnknownDimQuant, self.quantity**rhs)

    def __pow__(self, rhs: int) -> UnitExpr[UnknownDimQuant]:
        if not isinstance(rhs, numbers.Integral):
            raise TypeError(f"LHS not an integer: {rhs}")
        if rhs == 1:
            return self
        if rhs == 0:
            return UnitExpr(Scalar(1),(),())
        q = self.quantity**rhs
        n = self.num
        d = self.denom
        if rhs < 0:
            rhs = -rhs
            (n,d) = (d,n)
        num = ((a, e*rhs) for (a,e) in n)
        denom = ((a, e*rhs) for (a,e) in d)
        return q.as_unit_expr(num, denom)

    def format(self, q: D) -> _BoundQuantity[D]:
        return q.in_units(self)

    def __mod__(self, q: D) -> _BoundQuantity[D]:
        return self.format(q)
    
    def a(self, expected: type[ND]) -> UnitExpr[ND]:
        self.quantity.check_dimensionality(expected.dim())
        return cast(UnitExpr[ND], self)
    an = a
    
    def as_unit(self, abbr: str, check: type[D] = None) -> Unit[D]:  # @UnusedVariable
        return Unit[D](abbr, self)
    

class Unit(UnitExpr[D]):
    abbreviation: Final[str]
    singular: Final[str]
    _restrictions: Final[dict[Any, Unit]]
    
    def __init__(self, abbr: str, quant: Union[D,UnitExpr[D]], 
                 *, check: Optional[Dimensionality] = None,
                 singular: Optional[str] = None):
        if isinstance(quant, UnitExpr):
            quant = 1*quant
        if not isinstance(quant, Quantity):
            raise TypeError(f"Creating Unit from non-Quantity: {quant}")
        if check is not None and quant.dimensionality is not check:
            raise DimMismatchError(quant.dimensionality, "!=", check)
        real_abbr: Union[str, tuple[str,str]] = abbr if singular is None else (singular, abbr)
        super().__init__(quant, ((real_abbr, 1),), ())
        self.abbreviation = abbr
        self.singular = singular or abbr
        self._restrictions = dict[Any, Unit]()

    def description(self, *, mag: float, exponent_fmt: Optional[ExptFormatter] = None) -> str:  # @UnusedVariable
        return self.singular if mag == 1 else self.abbreviation
            
    def of(self, restriction: T, *, dim: Optional[str] = None) -> Unit[D]:
        u = self._restrictions.get(restriction, None)
        if u is None:
            q = self.quantity.of(restriction, dim=dim)
            a = f"{self.abbreviation}[{_restriction_name(restriction)}]"
            u = Unit(a, q)
            self._restrictions[restriction] = u
        return u
    
    def __getitem__(self, restriction: T) -> Unit:
        return self.of(restriction)

class Prefix:
    prefix: str
    multiplier: float
    
    def __init__(self, prefix: str, mult: float) -> None:
        if not isinstance(mult, numbers.Real):
            raise TypeError(f"Multipler is not a real number: {mult}")
        self.prefix = prefix
        self.multiplier = mult

    def __rep__(self) -> str:
        return f"Prefix({self.prefix}, {self.multiplier})"

    def __call__(self, unit: Unit[D]) -> Unit[D]:
        if not isinstance(unit, Unit):
            raise TypeError(f"Prefix {self} applied to non-Unit {unit}")
        return Unit(self.prefix+unit.abbreviation, self.multiplier*unit.quantity)
    

class NamedDim(Quantity[ND]): 
    _dim: ClassVar[Dimensionality[ND]]
    _this_class: ClassVar[type[ND]]
    
    def __init__(self, mag: float, dim: Dimensionality[ND] = None) -> None:
        if dim is None:
            dim = self._dim
        super().__init__(mag, dim)
        
    def __repr__(self) -> str:
        return f"{self._this_class.__name__}[{self.magnitude}]"
    
    
    @classmethod
    def dim(cls: type[ND]) -> Dimensionality[ND]:
        return cls._dim
    
    @classmethod
    def unit(cls: type[ND], abbr: str, quant: Union[ND, UnitExpr[ND]]) -> Unit[ND]:
        return Unit[ND](abbr, quant, check=cls._dim)
    
    @classmethod
    def ZERO(cls) -> ND:
        # This is created in the metaclasses for the subclasses.  If I try to add
        # @property here, mypy complains that it has method type.  If I make it
        # a propery in the metaclasses (the correct approach), I can't type it 
        # properly, because the metaclasses can't get the ND parameter.
        return getattr(cls, "_zero")
    
    @classmethod
    def default_units(cls, units: UnitExpr[ND]) -> None:
        cls.dim().default_units = units
        
    _restriction_classes: ClassVar[dict[Any, type[BaseDim[ND]]]]
    @classmethod
    def restricted(cls, restriction: T) -> type[BaseDim[ND]]:
        c = cls._restriction_classes.get(restriction, None)
        if c is not None:
            return c
        restr_pname = _restriction_name(restriction)
        pname = f"{cls._dim.name}[{restr_pname}]"
        rname = f"{cls.__name__}_{restr_pname}"
        # immediate_base = CountDim if issubclass(self.quant_class, CountDim) else BaseDim
        immediate_base = cls if issubclass(cls, BaseDim) else BaseDim
        new_dim_class = cast(type[BaseDim], BaseDimMeta(rname,(immediate_base,), {"_dim_name": pname}))
        new_dim: BaseDimension = new_dim_class._dim
        cls._restriction_classes[restriction] = new_dim_class
        new_dim._unrestricted = cls._dim
        new_dim._restriction = restriction
        return new_dim_class
    
    
class Scalar(NamedDim['Scalar']):
    _dim = Dimensionality['Scalar']((), 'scalar')
    
Scalar._dim.quant_class = Scalar
    
    
    
    
class DerivedDimMeta(type):
    def __new__(cls, name, base, dct):
        return super().__new__(cls, name, base, dct)
    
    def __init__(cls, name: str, base, dct) -> None:  # @UnusedVariable @NoSelf
        if name == "DerivedDim":
            return
        cls._this_class = cls
        d: Optional[Dimensionality] = getattr(cls, "derived", None)
        if d is None:
            raise NameError(f"DerivedDim {name} does not define 'derived'")
        if not isinstance(d, Dimensionality):
            raise TypeError(f"{name}.derived not a Dimensionality")
        if d.name is None:
            n:str = "_".join(split_camel_case(name)).lower()
            d.name = n
            d.quant_class = cast(type[DerivedDim], cls)
        cls._dim = d
        cls._zero = cls(0)
        cls._restriction_classes: dict[Any, type[BaseDim]] = {}

        

class DerivedDim(NamedDim[ND], metaclass=DerivedDimMeta): 
    derived: ClassVar[Dimensionality]

class BaseDimMeta(type):
    def __new__(cls, name, base, dct):
        return super().__new__(cls, name, base, dct)
    
    def __init__(cls, name: str, base, dct):  # @UnusedVariable
        if name == "BaseDim":
            return
        cls._this_class = cls
        # d = getattr(cls, "_dim", None)
        # if d is not None:
            # raise NameError(f"BaseDim {name} already defines '_dim'")
        # if d is None:
        n: str
        explicit_name = getattr(cls, "_dim_name", None)
        if explicit_name is not None:
            assert isinstance(explicit_name, str), f"{name}._dim_name not a str"
            n = explicit_name
        else:
            n = "_".join(split_camel_case(name)).lower()
        d = BaseDimension[ND](n)
        d.quant_class = cast(type[DerivedDim], cls)
        cls._dim = d
        cls._zero = cls(0)
        cls._restriction_classes: dict[Any, type[BaseDim]] = {}

class BaseDim(NamedDim[ND], metaclass=BaseDimMeta): 
    _dim: ClassVar[BaseDimension[ND]]
    
    @classmethod
    def base_unit(cls: type[BaseDim[ND]], abbr: str) -> Unit[ND]:
        return cls._dim.base_unit(abbr)
    
class CountDim(BaseDim[ND]):
    @property
    def count(self) -> int:
        return math.floor(self.magnitude)
    
    @property
    def checked_count(self) -> int:
        m = self.magnitude
        n = math.floor(m)
        if n != m:
            raise ValueError(f"{self} has non-integral magnitude")
        return n
    
    def __add__(self: ND, rhs: Union[float,ND]) -> ND:
        rmag: float = rhs if isinstance(rhs, (float, int)) else rhs.magnitude
        return cast(ND, self.dimensionality.make_quantity(self.magnitude+rmag))
    
    def __radd__(self, lhs: float) -> ND:
        return cast(ND, self.dimensionality.make_quantity(self.magnitude+lhs))
    
    def __sub__(self: ND, rhs: Union[float,ND]) -> ND:
        rmag: float = rhs if isinstance(rhs, (float, int)) else rhs.magnitude
        return cast(ND, self.dimensionality.make_quantity(self.magnitude-rmag))
    
    def __rsub__(self, lhs: float) -> ND:
        return cast(ND, self.dimensionality.make_quantity(lhs-self.magnitude))
        

    def __eq__(self, rhs: object) -> bool:
        if isinstance(rhs, (int, float)):
            return self.magnitude == rhs
        if not isinstance(rhs, Quantity): 
            return False
        self._ensure_dim_match(rhs, "==")
        return self.magnitude == rhs.magnitude
    
    def __lt__(self, rhs: Union[float,ND]) -> bool:
        if isinstance(rhs, (int, float)):
            return self.magnitude < rhs
        self._ensure_dim_match(rhs, "<")
        return self.magnitude < rhs.magnitude
    
    def __le__(self, rhs: D) -> bool:
        if isinstance(rhs, (int, float)):
            return self.magnitude <= rhs
        self._ensure_dim_match(rhs, "<=")
        return self.magnitude <= rhs.magnitude

    @classmethod
    def base_unit(cls: type[CountDim[ND]], singular: str, *, plural: Optional[str] = None) -> Unit[ND]:
        if plural is None:
            plural = infer_plural(singular)
        return cls._dim.base_unit(plural, singular=singular)
