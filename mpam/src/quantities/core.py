from __future__ import annotations
from typing import Optional, ClassVar, Callable, TypeVar, Generic, \
    overload, Union, cast, MutableMapping, Any, Final, Tuple, Sequence, Iterable,\
    Literal, Mapping, Type
from erk.stringutils import split_camel_case, infer_plural
import logging
import math
from erk.basic import LazyPattern, Lazy
import re
from abc import abstractmethod, ABC
from _collections import defaultdict
import random
from random import Random

logger = logging.getLogger(__name__)

ExptFormatter = Callable[[int],str] 
"""
A :class:`.Callable` that maps integers to strings representing that integer as
an exponent
"""

class Exponents:
    """
    A collection of :class:`ExptFormatter`\s
    
    :attr:`Exponents.default_format` can be set to the default
    :class:`ExptFormatter` to use.  It defaults to :attr:`stars`
    """
    _superscript_chars = { "0": "\u2070", "1": "\u00B9", "2": "\u00B2",
                          "3": "\u00B3", "4": "\u2074", "5": "\u2075",
                          "6": "\u2076", "7": "\u2077", "8": "\u2078",
                          "9": "\u2079", }

    # superscript() works fine, but the output shows up as
    # block codes in Emacs and is unreadable in mintty, so I'm not
    # going to use it.


    stars: ExptFormatter = lambda n : "" if n == 1 else f"**{n:g}"
    """
    An :class:`ExptFormatter` that uses ``**``.  For example ``2`` maps onto
    ``**2``.
    """ 
    caret: ExptFormatter = lambda n : "" if n == 1 else f"^{n:g}"
    """
    An :class:`ExptFormatter` that uses ``^``.  For example ``2`` maps onto
    ``^2``.
    """ 
    superscript: ExptFormatter = lambda n : ("" if n == 1
                              else "".join(Exponents._superscript_chars[c] for c in str(n)))
    """
    An :class:`ExptFormatter` that uses Unicode superscript characters.  For
    example ``2`` maps onto ``²``.
    """ 
    html: ExptFormatter = lambda n : "" if n == 1 else f"<sup>{n:g}</sup>"
    """
    An :class:`ExptFormatter` that HTML superscript formatting.  For example
    ``2`` maps onto ``<sup>2</sup>``.
    """ 

    default_format: ExptFormatter = stars
    """
    The default :class:`ExptFormatter` to use.  It defaults to :attr:`stars`,
    but can be modified.
    """

T = TypeVar('T')
BaseExp = tuple['BaseDimension', int]
BaseExpTuple = Tuple[BaseExp, ...]
DimOpCache = MutableMapping[T, 'Dimensionality']
AbbrExp = tuple[Union[str, tuple[str,str]], int]

D = TypeVar('D', bound='Quantity')
Dco = TypeVar('Dco', bound='Quantity', covariant=True)
Dctr = TypeVar('Dctr', bound='Quantity', contravariant=True)
D2 = TypeVar('D2', bound='Quantity')
ND = TypeVar('ND', bound='NamedDim')
BD = TypeVar('BD', bound='BaseDim')
CD = TypeVar('CD', bound='CountDim')
U = TypeVar('U', bound='Unit')
UE = TypeVar('UE', bound='UnitExpr')

D_co = TypeVar('D_co', bound='Quantity', covariant=True)
D_ca = TypeVar('D_ca', bound='Quantity', contravariant=True)

# Quant = Union['UnknownDimQuant', 'NamedDim']
# QuantOrUnit = Union[D, 'UnitExpr[D]']

# def _restriction_name(obj) -> str:
#     return

ZeroOr = Union[Literal[0], D] 
        
def _restriction_name(restriction: Any) -> str:
    return restriction.__name__ if isinstance(restriction, type) else str(restriction)

class DimLike(ABC):
    @abstractmethod
    def as_dimensionality(self) -> Dimensionality: ...

class Dimensionality(Generic[D], DimLike):
    
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
    _default_units: Optional[Tuple[UnitExpr[D], ...]]
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

    def named(self, name: str) -> Dimensionality[D]:
        self.name = name
        return self
    
    def as_dimensionality(self) -> Dimensionality[D]:
        return self
    
    @property
    def default_units(self) -> Optional[Tuple[UnitExpr[D], ...]]:
        units = self._default_units
        # print(f"Finding default units for {self}")
        if units is None:
            # print(f"Creating default units for {self}")
            us: Optional[UnitExpr] = None
            for t in self.exponents:
                # If we're a base and we don't have default, our tuple
                # will be ((self,1),), which would cause an infinite recursion
                if t[0] is self:
                    # but if we're restricted, we can delegate to our unrestricted one
                    if self._unrestricted is None:
                        return None
                    unr_units_set = self._unrestricted.default_units
                    if unr_units_set is None:
                        return None
                    def map_to_restriction(u: UnitExpr[D]) -> Unit[D]:
                        if isinstance(u, Unit):
                            return u.of(self._restriction)
                        else:
                            desc: str = u.description(mag=2)
                            return u.as_unit(f"({desc})").of(self._restriction)
                    return tuple( map_to_restriction(u) for u in unr_units_set )
                du = t[0].default_units
                if du is None:
                    return None
                u: UnitExpr = du[0]**t[1]
                # print(f"Includes {du[0]}**{t[1]} = {u}: ({u.quantity.dimensionality})")
                us = u if us is None else us*u
            units = None if us is None else (us,)
            self._default_units = units
        return units
    
    @default_units.setter
    def default_units(self, units: Optional[Tuple[UnitExpr[D], ...]]) -> None:
        # print(f"Setting default units of {self} to {units}")
        if units is not None:
            assert units[0].quantity.dimensionality is self
        self._default_units = units
        
    def format_quantity(self, quant: D, format_spec: str = "") -> str:
        units = self.default_units
        if units is None or len(units) == 0:
            return quant.__repr__()
        assert units[0].quantity.dimensionality is self
        return quant.in_units(units).__format__(format_spec) 
        
    
    def make_quantity(self, mag: float) -> D:
        return self.quant_class(mag, self) # type: ignore[arg-type]

    def description(self, *, exponent_fmt: Optional[ExptFormatter] = None) -> str:
        if exponent_fmt is None: exponent_fmt = Exponents.default_format
        cd: Optional[str] = getattr(self, "_cached_description", None)
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

    def __mul__(self, other: DimLike) -> Dimensionality[Quantity]:
        other = other.as_dimensionality()
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
        
    def __truediv__(self, other: DimLike) -> Dimensionality[Quantity]:
        other = other.as_dimensionality()
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

    def __pow__(self, n: int) -> Dimensionality[Quantity]:
        # if not isinstance(n, numbers.Integral):
            # raise TypeError(f"Exponent not integral: {n}")
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
            c: type[BaseDim] = self.quant_class.restricted(restriction)
            d = c.dim()
            self._restrictions[restriction] = d
            return d
        name = dim or self.name
        assert name is not None, f"Unnamed dimension {self} cannot be restricted, without 'dim='"
        restr_pname = _restriction_name(restriction)
        pname = f"{name}[{restr_pname}]"
        rname = f"{name}_{restr_pname}"

        # I'm not sure I understand why, but new_dim_class is inferred to be of
        # type BaseDimMeta, and I can't get MyPy to understand that it's a
        # BaseDim (so that I can invoke the class method dim()) without the cast.
        new_dim_class = cast(Type[BaseDim], BaseDimMeta(rname,(BaseDim,), {"_dim_name": pname}))
        new_dim: BaseDimension = new_dim_class.dim()
        new_dim._unrestricted = self
        new_dim._restriction = restriction
        self._restrictions[restriction] = new_dim
        return new_dim
    
    def __getitem__(self, restriction: T) -> BaseDimension:
        return self.of(restriction)
        
    
class BaseDimension(Dimensionality[BD]):
    _sort_name: str
    
    def __init__(self, name: str) -> None:
        super().__init__(((self,1),), name)
        self._sort_name = name

    def __lt__(self, other: BaseDimension) -> bool:
        return self._sort_name < other._sort_name
    
    def description(self, *, exponent_fmt: Optional[ExptFormatter] = None) -> str:  # @UnusedVariable
        return self._sort_name

    def base_unit(self, abbr: str, *, singular: Optional[str]=None) -> Unit[BD]:
        q = self.make_quantity(1)
        unit: Unit[BD] = q.as_unit(abbr, singular=singular)
        # unit = Unit[BD](abbr, self.make_quantity(1), singular=singular)
        if self._default_units is None: 
            self.default_units = (unit,)
        return unit
    

class DimensionalityError(Exception):
    def __init__(self, expected: Dimensionality, got: Dimensionality) -> None:
        super().__init__(f"Expected {expected} ({expected.description()}) got {got}")

class DimMismatchError(Exception):
    def __init__(self, lhs: Dimensionality, op: str, rhs: Union[Dimensionality, str]) -> None:
        super().__init__(f"{lhs} {op} {rhs}")

class Quantity:
    '''
    A dimensioned quantity
    '''
    _dimensionality: Final[Dimensionality]
    magnitude: float
    
    @property
    def dimensionality(self: D) -> Dimensionality[D]:
        return self._dimensionality

    @property
    def is_positive(self) -> bool:
        return self.magnitude > 0
    
    @property
    def is_negative(self) -> bool:
        return self.magnitude < 0
    
    @property
    def is_zero(self) -> bool:
        return self.magnitude == 0
    
    @property
    def is_finite(self) -> bool:
        return self.magnitude < math.inf and self.magnitude > -math.inf
    
    # def __init__(self, mag: float, dim: Dimensionality[D]) -> None:
    def __init__(self: D, mag: float, dim: Dimensionality[D]) -> None:
        self._dimensionality = dim
        self.magnitude = mag

    def __repr__(self) -> str:
        return f"Quantity({self.magnitude}, {self.dimensionality})"
    
    def __str__(self) -> str:
        return self.dimensionality.format_quantity(self)
    
    def __format__(self, format_spec: str) -> str:
        return self.dimensionality.format_quantity(self, format_spec)
    
    def __bool__(self) -> bool:
        return self.magnitude != 0

    def cast(self: D) -> D:
        return self
    
    # It's tempting to overload this so that if the argument is 
    # Dimensionality[D] the return type is hinted Literal[True] and 
    # otherwise it's hinted Literal[False] (or maybe just bool).  
    # But I think that would break restricted types, which have the
    # same D, regardless of restriction.
    def has_dimensionality(self, dim: Dimensionality) -> bool: 
        if not isinstance(dim, Dimensionality):
            raise TypeError(f"Not a Dimensionaluty: {dim}")
        my_dim = self.dimensionality
        return my_dim is dim or my_dim._unrestricted is dim

    def check_dimensionality(self: D, dim: Dimensionality[D]) -> D:
        if not self.has_dimensionality(dim):
            raise DimensionalityError(dim, self.dimensionality)
        return self
        
    def a(self: D, expected: type[ND]) -> ND:
        edim = cast(Dimensionality[D], expected.dim())
        return cast(ND, self.check_dimensionality(edim))
    
    an = a

    def _ensure_dim_match(self, rhs: Quantity, op: str) -> None:
        if not isinstance(rhs, Quantity):
            raise TypeError(f"RHS of {op} is not a Quantity: {rhs}")
        if not rhs.has_dimensionality(self.dimensionality):
            raise TypeError(f"{self.dimensionality} {op} {rhs.dimensionality} is ill-formed")

    def same_dim(self: D, magnitude: float) -> D:
        return self.dimensionality.make_quantity(magnitude)        

    def __neg__(self: D) -> D:
        return self.same_dim(-self.magnitude)
    
    def __add__(self: D, rhs: D) -> D:
        self._ensure_dim_match(rhs, "+")
        return self.same_dim(self.magnitude+rhs.magnitude)

    def __sub__(self: D, rhs: D) -> D:
        self._ensure_dim_match(rhs, "-")
        return self.same_dim(self.magnitude-rhs.magnitude)

    def __eq__(self, rhs: object) -> bool:
        if isinstance(rhs, int) and rhs == 0:
            return self.magnitude == 0.0
        if not isinstance(rhs, Quantity): 
            return False
        self._ensure_dim_match(rhs, "==")
        return self.magnitude == rhs.magnitude
    
    def __hash__(self) -> int:
        return hash((self.magnitude, self.dimensionality))
    
    def _magnitude_of(self: D, other: ZeroOr[D], op: str) -> float:
        if other == 0:
            return 0
        self._ensure_dim_match(other, op)
        return other.magnitude
    
    # Some dimensions (e.g., money) may change self.magnitude during the call to
    # _ensure_dim_match(), so we have to make sure it's called before we read
    # it.
    
    def __lt__(self: D, rhs: ZeroOr[D]) -> bool:
        their_mag = self._magnitude_of(rhs, "<")
        return self.magnitude < their_mag
    
    def __le__(self:D , rhs: ZeroOr[D]) -> bool:
        their_mag = self._magnitude_of(rhs, "<=")
        return self.magnitude <= their_mag
    
    def __gt__(self: D, rhs: ZeroOr[D]) -> bool:
        their_mag = self._magnitude_of(rhs, ">")
        return self.magnitude > their_mag
    
    def __ge__(self:D , rhs: ZeroOr[D]) -> bool:
        their_mag = self._magnitude_of(rhs, ">=")
        return self.magnitude >= their_mag
    
    def is_close_to(self, other: ZeroOr[D], *, 
                    rel_tol: float = 1e-09, 
                    abs_tol: Optional[ZeroOr[D]] = None,
                    ) -> bool:
        their_mag = self._magnitude_of(other, "is_close_to")
        my_mag = self.magnitude
        if my_mag == their_mag:
            return True
        tol = self._magnitude_of(abs_tol, "is_close_to.abs_tol") if abs_tol is not None else 1e-9 if their_mag==0 else 0
        if abs(my_mag-their_mag) < tol:
            return True
        return math.isclose(self.magnitude, their_mag, rel_tol=rel_tol)
    
    @classmethod
    def noise(cls: Type[D], sd: D, *, rng: Optional[Random] = None) -> D:
        if sd.is_zero:
            return sd
        if rng is None:
            mag = random.normalvariate(mu = 0.0, sigma = sd.magnitude)
        else:
            mag = rng.gauss(mu = 0.0, sigma = sd.magnitude)
        q = sd.dimensionality.make_quantity(mag)
        return q

    
    def multiply_by(self, rhs: Quantity) -> Quantity:
        if not isinstance(rhs, Quantity):
            raise TypeError(f"RHS not a Quantity: {rhs}")
        new_dim = self.dimensionality*rhs.dimensionality
        return new_dim.make_quantity(self.magnitude*rhs.magnitude)
                        
    def divide_by(self, rhs: Quantity) -> Quantity:
        if not isinstance(rhs, Quantity):
            raise TypeError(f"RHS not a Quantity: {rhs}")
        new_dim = self.dimensionality/rhs.dimensionality
        return new_dim.make_quantity(self.magnitude/rhs.magnitude)
    
    def in_denom(self, lhs: float) -> Quantity:
        # if not isinstance(lhs, numbers.Real):
            # raise TypeError(f"LHS not a Quantity: {lhs}")
        new_dim = self.dimensionality**(-1)
        return new_dim.make_quantity(lhs/self.magnitude)
    
    def to_power(self, rhs: int) -> Quantity:
        # if not isinstance(rhs, numbers.Integral):
            # raise TypeError(f"RHS not an integer: {rhs}")
        if rhs == 1:
            return self
        if rhs == 0:
            return Scalar.from_float(1)
        new_dim = self.dimensionality**rhs
        return new_dim.make_quantity(self.magnitude**rhs)
    
    @overload
    def __mul__(self: D, _rhs: Union[float, Scalar]) -> D: ...  
    @overload
    def __mul__(self: D, _rhs: Quantity) -> Quantity: ...  
    @overload
    def __mul__(self: D, _rhs: UnitExpr) -> Quantity: ...  
    def __mul__(self: D, rhs: Union[float, Quantity, UnitExpr]) ->  Union[D, Quantity]:
        if isinstance(rhs, (float, int)):
            return self.same_dim(self.magnitude*rhs)
        if isinstance(rhs, UnitExpr):
            return self.multiply_by(rhs.quantity)
        return self.multiply_by(rhs)

    def __rmul__(self: D, lhs: float) -> D:
        # if not isinstance(lhs, numbers.Real):
            # raise TypeError(f"LHS not a real number: {lhs}")
        return self.same_dim(lhs*self.magnitude)

    @overload
    def __truediv__(self: D, _rhs: Union[float, Scalar]) -> D: ...  
    @overload
    def __truediv__(self: D, _rhs: Union[D, UnitExpr[D]]) -> Scalar: ...
    @overload
    def __truediv__(self: D, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self: D, rhs: Union[float, Quantity, UnitExpr]) -> Union[D, Quantity]:
        if isinstance(rhs, (float, int)):
            return self.same_dim(self.magnitude/rhs)
        if isinstance(rhs, UnitExpr):
            return self.divide_by(rhs.quantity)
        return self.divide_by(rhs)

    def __rtruediv__(self, lhs: float) -> Quantity:
        return self.in_denom(lhs)

    @overload
    def __pow__(self: D, _rhs: Literal[0]) -> Scalar: ...
    @overload
    def __pow__(self: D, _rhs: Literal[1]) -> D: ...
    @overload
    def __pow__(self: D, _rhs: int) -> Quantity: ...
    def __pow__(self, rhs: int) -> Quantity:
        return self.to_power(rhs)
    
    def ratio(self: D, base: D) -> float:
        return self.magnitude/base.magnitude
    
    def _in_units(self: D, units: UnitExpr[D]) -> _BoundQuantity[D]:
        if units.dimensionality() is not self.dimensionality:
            raise DimMismatchError(self.dimensionality, "in", f"{units} ({units.dimensionality()})")
        return _BoundQuantity(self, units)
        

    def in_units(self: D, units: Union[UnitExpr[D], Sequence[UnitExpr[D]]]) -> _BoundQuantity[D]:
        if isinstance(units, UnitExpr):
            return self._in_units(units)
        assert len(units) > 0, f"Empty units list passed to ({self}).in_units()"
        if len(units) == 1:
            return self._in_units(units[0])
        
        best = units[0]
        best_mag = self.as_number(best)
        if best_mag == 0:
            return self._in_units(best)
        for u in units[1:]:
            m = self.as_number(u)
            if (m >= 1 and (best_mag < 1 or m < best_mag)) or (m < 1 and m > best_mag):
                best = u
                best_mag = m
        return self._in_units(best)
    
    def as_number(self: D, units: UnitExpr[D]) -> float:
        return self.in_units(units).magnitude
    
    def as_unit(self: D, abbr: str, *, singular: Optional[str]=None) -> Unit[D]:
        return Unit[D](abbr, self, singular=singular)
    
    def as_unit_expr(self: D, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> UnitExpr[D]:
        return UnitExpr[D](self, num, denom)
    
    def of(self, restriction: T, *, dim: Optional[str] = None) -> BaseDim:
        d = self.dimensionality.of(restriction, dim=dim)
        return cast(BaseDim, d.make_quantity(self.magnitude))
    
    
    def decomposed(self: D, units: Iterable[UnitExpr[D]], *, 
                   required: Optional[Union[Iterable[UnitExpr[D]],
                                            Literal["all"]]] = None) -> _DecomposedQuantity[D]:
        if self.magnitude < 0:
            raise ValueError(f"decompose() not defined for negative {self}")
        biggest_first = list(units)
        biggest_first.sort(reverse = True)
        if required is not None:
            reqd = set(biggest_first if required == "all" else required)
        else:
            reqd = set()
        used: list[tuple[UnitExpr[D], int]] = []
        q = self
        last = biggest_first[-1]
        for u in biggest_first:
            m = q.as_number(u)
            whole = math.floor(m)
            if math.isclose(m, whole+1):
                whole=whole+1
            if whole >= 1:
                if math.isclose(m, whole):
                    remainder = 0.0
                else:
                    remainder = m - whole
                used.append((u, whole))
                q = remainder*u
                last = u
            elif u in reqd:
                used.append((u, 0))
                last = u
        if len(used) == 0:
            used.append((last, 0))
        return _DecomposedQuantity[D](used, q)
    

class UnknownDimQuant(Quantity):
    def __repr__(self) -> str:
        return f"UnknownDimQuant[{self.magnitude},{self.dimensionality}]"
    
class _DecomposedQuantity(Generic[D]):
    tuples: Sequence[tuple[UnitExpr[D], int]]
    remainder: D
    
    def __init__(self, 
                 tuples: Sequence[tuple[UnitExpr[D], int]],
                 remainder: D) -> None:
        self.tuples = tuples
        self.remainder = remainder
        
    def __repr__(self) -> str:
        last = self.tuples[-1][0]
        def fmt(u: UnitExpr[D], mag: int) -> str:
            f: float = mag+self.remainder.as_number(u) if u is last else mag
            return (f*u).in_units(u).__str__()
        return ", ".join(fmt(u, mag) for u,mag in self.tuples)
    
#            (?P<mid>\\#?0?)
    _nspec_re: ClassVar[LazyPattern] = LazyPattern("""
            (?:(?P<fill>.)?
                (?P<align>[<>^])
            )?
            (?P<mid>\\#?0?)
            (?P<width>[0-9]+)?
            (?P<grouping>[,_]?)
            (?P<prec>\\.[0-9]+)?
            (?P<type>t?.)?
        """, re.VERBOSE)
    
    def _fmt_specs(self, format_spec: str) -> tuple[str, str, str]:
        nspec, _, uspec = format_spec.partition(";")
        
        if uspec:
            uspec = ";"+uspec
        
        pat = _DecomposedQuantity._nspec_re.value
        m = pat.fullmatch(nspec)
        if m is None:
            raise ValueError(f"_DecomposedQuantity can't parse number format specification '{nspec}'")
        d = m.groupdict(default = "")
        align = d["align"]
        most_spec = d["mid"]+d["grouping"]+".0f"+uspec
        last_spec = d["mid"]+d["grouping"]+d["prec"]+d["type"]+uspec
        sspec = d["fill"]+align+d["width"]
        
        return (most_spec, last_spec, sspec)
    
    def __format__(self, format_spec: str) -> str:
        most_spec, last_spec, sspec = self._fmt_specs(format_spec)
        
        last = self.tuples[-1][0]
        def fmt(u: UnitExpr[D], mag: int) -> str:
            f: float = mag+self.remainder.as_number(u) if u is last else mag
            return (f*u).in_units(u).__format__(last_spec if u is last else most_spec)
        s = ", ".join(fmt(u, mag) for u,mag in self.tuples)
        return s.__format__(sspec)
    
    class Joined:
        decomposed: Final[_DecomposedQuantity]
        sep: Final[str]
        digits: Final[int]
        
        def __init__(self, decomposed: _DecomposedQuantity, sep: str, digits: int) -> None:
            self.decomposed = decomposed
            self.sep = sep
            self.digits = digits
            
        def __str__(self) -> str:
            return self.__format__("f")
            
            
        def __format__(self, format_spec: str) -> str:
            pat = _DecomposedQuantity._nspec_re.value
            m = pat.fullmatch(format_spec)
            if m is None:
                raise ValueError(f"_DecomposedQuantity can't parse number format specification '{format_spec}'")
            d = m.groupdict(default = "")
            align = d["align"]
            w = str(self.digits)
            unpadded_spec = d["mid"]+d["grouping"]+".0f"
            padded_spec = d["mid"]+d["grouping"]+"0"+w+".0f"
            remainder_spec = d["prec"]+"f"
            sspec = d["fill"]+align+d["width"]
            
            decomposed = self.decomposed
            last = decomposed.tuples[-1][0]
            spec = unpadded_spec
            def fmt(mag: int) -> str:
                nonlocal spec
                val = mag.__format__(spec)
                spec = padded_spec
                return val
            s = self.sep.join(fmt(t[1]) for t in decomposed.tuples)
            r = decomposed.remainder.as_number(last).__format__(remainder_spec)[1:]
            s += r
            return s.__format__(sspec)
            
    
    def joined(self, sep: str, digits: int) -> Joined:
        return _DecomposedQuantity.Joined(self, sep, digits)

    
    
class _BoundQuantity(Generic[D]):
    magnitude: Final[float]
    units: UnitExpr[D]
    is_count: Final[bool]
    
    def __init__(self, quant: D, units: UnitExpr[D]) -> None:
        self.magnitude = quant.magnitude/units.quantity.magnitude
        self.units = units
        self.is_count = isinstance(quant, CountDim) and self.magnitude.is_integer()

    def description(self, *, exponent_fmt: Optional[ExptFormatter] = None) -> str:
        desc = self.units.description(exponent_fmt=exponent_fmt, mag=self.magnitude)
        if self.is_count:
            return f"{int(self.magnitude):,d} {desc}"
        else:
            return f"{self.magnitude:g} {desc}"

    def __repr__(self) -> str:
        return self.description()
    
    def split(self) -> tuple[float, UnitExpr[D]]:
        return (self.magnitude, self.units)
    
    _uspec_re: ClassVar[LazyPattern] = LazyPattern("""
                (?:(?P<fill>.)?
                   (?P<align>[<>^])
                )?
                (?P<min>[0-9]+)?
                (?:\\.(?P<max>[0-9]+))?
                (?P<exp>[hsc*])?
                (?P<brackets>[pb])?
                (?P<sep>[- =_])?
            """, re.VERBOSE
        )
    _nspec_re: ClassVar[LazyPattern] = LazyPattern("""
                (?:(?P<fill>.)?
                   (?P<align>[<>^])
                )?
                (?P<mid>\\#?0?)
                (?P<width>[0-9]+)?
                (?P<rest>.*)
            """, re.VERBOSE
        )
    def __format__(self, format_spec: str) -> str:
        nspec, _, uspec = format_spec.partition(";")

        pat = _BoundQuantity._uspec_re.value
        m = pat.fullmatch(uspec)
        if m is None:
            raise ValueError(f"UnitExpr can't parse unit format specification '{uspec}'")
        d = m.groupdict(default = "")
        sep = d["sep"] or " "
        if sep == "=":
            sep = ""
        alt = "#" if math.isclose(self.magnitude, 1) else ""
        maxw = ("."+d["max"]) if d["max"] else ""
        uspec = d["fill"]+d["align"]+alt+d["min"]+maxw+d["exp"]
        formatted_unit  = self.units.__format__(uspec)
        if d["brackets"] == "p":
            formatted_unit = "(" + formatted_unit + ")"
        elif d["brackets"] == "b":
            formatted_unit = "[" + formatted_unit + "]"
        # print(f"u: '{formatted_unit}'")
        pat = _BoundQuantity._nspec_re.value
        m = pat.fullmatch(nspec)
        if m is None:
            raise ValueError(f"UnitExpr can't parse number format specification '{nspec}'")
        d = m.groupdict(default = "")
        sspec = ""
        align = d["align"]
        if align == "<" or align == "^":
            sspec = d["fill"]+align+d["width"]
            nspec = d["mid"]+d["rest"]
        elif d["width"]:
            width = int(d["width"])-len(formatted_unit)-len(sep)
            wspec = "" if width < 1 else str(width)
            nspec = d["fill"]+d["align"]+d["mid"]+wspec+d["rest"]
        as_float = nspec.endswith("f") or nspec.endswith("g")
        if not as_float and self.is_count:
            formatted_number = int(self.magnitude).__format__(nspec)
        else:
            if (trim := nspec.endswith("tf")):
                nspec = nspec[:-2]+"f"
            formatted_number = self.magnitude.__format__(nspec)
            if trim:
                formatted_number = formatted_number.rstrip("0").rstrip(".")
        res = (formatted_number+sep+formatted_unit).__format__(sspec)
        return res

        
        
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

    def _add_expts(self, new_n: list[AbbrExp], new_d: list[AbbrExp], expts: Sequence[AbbrExp]) -> None:
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
        cd: Optional[str] = getattr(self, "_cached_description", None)
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
    
    # _fmt_re: ClassVar[Optional[Pattern]] = None
    
    _fmt_re: ClassVar[LazyPattern] = LazyPattern("(?P<pre>.*?)(?P<exp>[hs*c])?")
    
    _expt_fmts: ClassVar[Lazy[Mapping[str, ExptFormatter]]] = Lazy(
        lambda: {
            '': Exponents.default_format,
            '*': Exponents.stars,
            's': Exponents.superscript,
            'c': Exponents.caret,
            'h': Exponents.html
            }
        )
    
    def __format__(self, format_spec: str) -> str:
        # pat = UnitExpr._fmt_re
        # if pat is None:
        #     pat = re.compile("(?P<bracket>[[(])?(?:(?P<fill>.)?(?P<align>[<>^]))?(?P<sing>#)?(?P<min>[0-9]+)?(?:\\.(?P<max>[0-9]+))?")
        #     UnitExpr._fmt_re = pat
        # m = pat.fullmatch(format_spec)
        # if m is None:
        #     raise ValueError(f"UnitExpr can't parse format specification '{format_spec}'")
        # d = m.groupdict()
        # print(d)
        m = UnitExpr._fmt_re.value.fullmatch(format_spec)
        if m is None:
            raise ValueError(f"UnitExpr can't parse format specification '{format_spec}'")
        d = m.groupdict(default = "")
        e = d["exp"]
        # print(f"exp: '{e}' in '{format_spec}' {repr(self)}")
        expt = UnitExpr._expt_fmts.value[e]
        pre, match, post = d["pre"].partition("#")
        desc = self.description(mag = 1 if match else 2, exponent_fmt = expt)
        # print(f"desc: '{desc}'")
        return desc.__format__(pre+post)


    def _combine_with(self, num: Sequence[AbbrExp], denom: Sequence[AbbrExp]) -> tuple[tuple[AbbrExp,...], tuple[AbbrExp,...]]: 
        new_n = list(self.num)
        new_d = list(self.denom)

        self._add_expts(new_n, new_d, num)
        # We swap the numerator and denominator lists when processing the denominator
        self._add_expts(new_d, new_n, denom)

        return (tuple(new_n), tuple(new_d))
    
    def _multiply_by(self, q: Quantity, 
                     num: tuple[AbbrExp,...], 
                     denom: tuple[AbbrExp,...]) -> UnitExpr:
        Tpair = tuple[tuple[AbbrExp,...], tuple[AbbrExp, ...]]
        Cache = dict[Tpair, Tpair]
        cache: Optional[Cache] = getattr(self, "_cached_multiplication", None)
        if cache is None:
            self._cached_multiplication = cache = {}
        cached_num_denom = cache.get((num, denom))
        if cached_num_denom is None:
            cached_num_denom = self._combine_with(num, denom)
            cache[(num, denom)] = cached_num_denom
        # t: tuple[list[AbbrExp], list[AbbrExp]] = cached_num_denom
        (new_num, new_denom) = cached_num_denom
        new_q = self.quantity*q
        def desc(q: Quantity) -> str:
            return f"{q.dimensionality}[{q.dimensionality.description()}]"
        # print(f"({desc(self.quantity)})*({desc(q)}) = {desc(new_q)}")
        res = new_q.as_unit_expr(new_num, new_denom)
        return res
        

        
    @overload
    def __mul__(self, _rhs: float) -> D: ...  
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...  
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[D, UnitExpr]:
        if isinstance(rhs, (float, int)):
            return self.quantity*rhs

        if not isinstance(rhs, UnitExpr):
            raise TypeError(f"RHS is not a number or UnitExpr: {rhs}")
        return self._multiply_by(rhs.quantity, rhs.num, rhs.denom)

    def __rmul__(self, n: float) -> D:
        # if not isinstance(n, numbers.Real):
        #     raise TypeError(f"LHS is not a real number: {n}")
        q: D = self.quantity
        return n*q
    
    @overload
    def __truediv__(self, _rhs: float) -> D: ...  
    @overload
    def __truediv__(self, _rhs: UnitExpr[D]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...  
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[D, UnitExpr]:
        if isinstance(rhs, (float, int, Scalar)):
            return self.quantity/rhs

        if not isinstance(rhs, UnitExpr):
            raise TypeError(f"RHS is not a number or UnitExpr: {rhs}")
        return self._multiply_by(1/rhs.quantity, rhs.denom, rhs.num)


    def __rtruediv__(self, n: float) -> Quantity:
        # if not isinstance(n, numbers.Real):
        #     raise TypeError(f"LHS is not a real number: {n}")
        return n/self.quantity
        
    # def qpow(self, rhs: int) -> UnknownDimQuant:
        # return cast(UnknownDimQuant, self.quantity**rhs)

    @overload
    def __pow__(self, _rhs: Literal[0]) -> ScalarUnitExpr: ... 
    @overload
    def __pow__(self: UE, _rhs: Literal[1]) -> UE: ... 
    @overload
    def __pow__(self, _rhs: int) -> UnitExpr: ...
    def __pow__(self, rhs: int) -> UnitExpr:
        # if not isinstance(rhs, numbers.Integral):
        #     raise TypeError(f"LHS not an integer: {rhs}")
        if rhs == 1:
            return self
        if rhs == 0:
            return Scalar.unit_expr
        Tpair = tuple[tuple[AbbrExp,...], tuple[AbbrExp, ...]]
        Cache = dict[int, Tpair]
        cache: Optional[Cache] = getattr(self, "_cached_power", None)
        if cache is None:
            self._cached_power = cache = {}
        cached_num_denom = cache.get(rhs)
        if cached_num_denom is None:
            abs_rhs = rhs
            n = self.num
            d = self.denom
            if rhs < 0:
                abs_rhs = -rhs
                (n,d) = (d,n)
            num = tuple((a, e*abs_rhs) for (a,e) in n)
            denom = tuple((a, e*abs_rhs) for (a,e) in d)
            cached_num_denom = (num, denom)
            cache[rhs] = cached_num_denom
        # t: tuple[list[AbbrExp], list[AbbrExp]] = cached_num_denom
        (new_num, new_denom) = cached_num_denom
        new_q = self.quantity**rhs
        res = new_q.as_unit_expr(new_num, new_denom)
        return res

    def format(self, q: D) -> _BoundQuantity[D]:
        return q.in_units(self)
    
    def __mod__(self, q: D) -> _BoundQuantity[D]:
        return self.format(q)
    
    def a(self, expected: type[ND]) -> UnitExpr[ND]:
        # TODO: Is this kosher?  Should Dimensionality take a contravariant type param?
        edim = cast(Dimensionality[D], expected.dim())
        self.quantity.check_dimensionality(edim)
        return cast(UnitExpr[ND], self)
    an = a
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[D]] = None, # @UnusedVariable
                singular: Optional[str]=None) -> Unit[D]: 
        return self.quantity.as_unit(abbr, singular=singular)
        # return Unit[D](abbr, self, singular=singular)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UnitExpr): 
            return False
        q: D = self.quantity
        val: bool = q == other.quantity
        return val
    def __hash__(self) -> int:
        return hash(self.quantity)
    def __lt__(self, other: UnitExpr[D]) -> bool:
        return self.quantity < other.quantity
    def __le__(self, other: UnitExpr[D]) -> bool:
        return self.quantity <= other.quantity
    
# class TiedUnitExpr(UnitExpr[D], Generic[D, U]):
#     def as_unit(self, abbr:str, check:Optional[type[D]]=None, singular:Optional[str]=None)->U:
#         return cast(U, super().as_unit(abbr, check=check, singular=singular))
#
#     # I should be able to override a() to return something typed to the type of self, but
#     # I can't figure out how to get it by the compiler.

UEorSeq = Union[UnitExpr[D], Sequence[UnitExpr[D]]]

class Unit(UnitExpr[D]):
    """
    A dimensional unit.  When a number is multiplied by a :class:`Unit`, a
    :class:`Quantity` of the appropriate :class:`Dimensionality` is produced.
    
    Args:
        D: The subclass of :class:`Quantity` that this :class:`Unit` produces
           when a number is multiplied by.
    """
    abbreviation: Final[str]
    singular: Final[str]
    _restrictions: Final[dict[Any, Unit]]
    
    def __init__(self, abbr: str, quant: Union[D,UnitExpr[D]], 
                 *, check: Optional[Dimensionality[D]] = None,
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
        # return self.singular if mag == 1 else self.abbreviation
        return self.singular if math.isclose(mag, 1) else self.abbreviation
    
    def of(self, restriction: T, *, dim: Optional[str] = None) -> Unit[D]:
        u = self._restrictions.get(restriction, None)
        if u is None:
            q = self.quantity.of(restriction, dim=dim)
            a = f"{self.abbreviation}[{_restriction_name(restriction)}]"
            u = Unit(a, q)
            # u = q.as_unit(a)
            self._restrictions[restriction] = u
        return u
    
    def __getitem__(self, restriction: T) -> Unit:
        return self.of(restriction)

class Prefix:
    prefix: str
    multiplier: float
    
    def __init__(self, prefix: str, mult: float) -> None:
        # if not isinstance(mult, numbers.Real):
        #     raise TypeError(f"Multipler is not a real number: {mult}")
        self.prefix = prefix
        self.multiplier = mult

    def __rep__(self) -> str:
        return f"Prefix({self.prefix}, {self.multiplier})"

    def __call__(self, unit: U) -> U:
        if not isinstance(unit, Unit):
            raise TypeError(f"Prefix {self} applied to non-Unit {unit}")
        magnitude = self.multiplier * unit.quantity
        abbr = self.prefix + unit.abbreviation
        return cast(U, magnitude.as_unit(abbr))
    
    def __mul__(self, rhs: float) -> float:
        return self.multiplier*rhs
    def __rmul__(self, lhs: float) -> float:
        return lhs*self.multiplier
    def __truediv__(self, rhs: float) -> float:
        return self.multiplier/rhs
    
    def scale(self, prefix: str, mult: float) -> Prefix:
        return Prefix(prefix, self.multiplier*mult)
    
class NamedDimMeta(type, DimLike):
    @property
    def ZERO(self: Type[T]) -> T:
        val: T = getattr(self, "_zero")
        return val
    
    @property
    def INF(self: Type[T]) -> T:
        val: T = getattr(self, "_infinity")
        return val
    
    def __init__(self, name: str, base: tuple[Type, ...], dct: Mapping) -> None:  # @UnusedVariable 
        self._zero = self(0.0)
        self._infinity = self(math.inf)
        self._restriction_classes: dict[Any, type[BaseDim]] = {}

    def as_dimensionality(self: type[ND]) -> Dimensionality[ND]: # type: ignore[misc]
        raise NotImplementedError()

    def __mul__(self: type[ND], other: DimLike) -> Dimensionality[Quantity]: # type: ignore[misc]
        return self.as_dimensionality()*other
    def __truediv__(self: type[ND], other: DimLike) -> Dimensionality[Quantity]: # type: ignore[misc]
        return self.as_dimensionality()/other
    def __pow__(self: type[ND], n: int) -> Dimensionality[Quantity]: # type: ignore[misc]
        return self.as_dimensionality()**n
    
    def __getitem__(self: type[ND], restriction: T) -> BaseDimension:  # type: ignore[misc]
        return self.as_dimensionality().of(restriction)
    
    @property
    def default_units(self: type[ND]) -> Optional[Union[UnitExpr[ND], Sequence[UnitExpr[ND]]]]: # type: ignore[misc]
        units = self.as_dimensionality().default_units
        if units is not None and len(units) == 1:
            return units[0]
        else:
            return units
    
    @default_units.setter
    def default_units(self: type[ND], units: Optional[Union[UnitExpr[ND], Sequence[UnitExpr[ND]]]]) -> None: # type: ignore[misc]
        if units is not None:
            if isinstance(units, UnitExpr):
                units = (units,)
            elif not isinstance(units, tuple):
                units = tuple(units)
        self.as_dimensionality().default_units = units
        
                                                  

class NamedDim(Quantity, metaclass=NamedDimMeta):
    # In earlier code, I had _dim defined as ClassVar[Dimensionality[ND]] (and
    # as ClassVar[Dimensionality[BD]] in BaseDim).  MyPy 0.931 complains about
    # this, saying that ClassVar attributes can't have type variables.  Which
    # makes sense, except that here I'm actually setting it (via the metaclass)
    # in the subclass, where it does make sense.  So I'm currently doing an explicit
    # lookup and set using get/setattr
    _dim_key: Final = "_dim" 
    
    def __init__(self: ND, mag: float, dim: Optional[Dimensionality[ND]] = None) -> None:
        if dim is None:
            dim = type(self).dim()
        super().__init__(mag, dim)
        
    def __repr__(self) -> str:
        return f"{type(self).__name__}[{self.magnitude}]"
    
    
    @classmethod
    @abstractmethod
    def dim(cls: type[ND]) -> Dimensionality[ND]:
        ...
        
    @classmethod
    def as_dimensionality(cls: type[ND]) -> Dimensionality[ND]:
        return cls.dim()
        
    # @classmethod
    # def default_units(cls: type[ND], units: Union[UnitExpr[ND], Sequence[UnitExpr[ND]]]) -> None:
    #     if isinstance(units, UnitExpr):
    #         units = (units,)
    #     elif not isinstance(units, tuple):
    #         units = tuple(units)
    #     cls.dim().default_units = units
    
    @classmethod
    def unit(cls: type[ND], abbr: str, quant: Union[ND, UnitExpr[ND]]) -> Unit[ND]:
        if isinstance(quant, UnitExpr):
            return quant.as_unit(abbr, check=cls)
        else:
            quant.check_dimensionality(cls.dim())
            return quant.as_unit(abbr)
        
    _restriction_classes: ClassVar[dict[Any, type[BaseDim]]]
    
    @classmethod
    def note_restriction(cls, restriction: T, rclass: type[BaseDim]) -> None:
        cls._restriction_classes[restriction] = rclass
        new_dim: BaseDimension = rclass.dim()
        new_dim._unrestricted = cls.dim()
        new_dim._restriction = restriction
        
    @classmethod
    def restricted(cls, restriction: T) -> type[BaseDim]:
        c = cls._restriction_classes.get(restriction, None)
        if c is not None:
            return c
        restr_pname = _restriction_name(restriction)
        pname = f"{cls.dim().name}[{restr_pname}]"
        rname = f"{cls.__name__}_{restr_pname}"
        # immediate_base = CountDim if issubclass(self.quant_class, CountDim) else BaseDim
        immediate_base: Union[Type[NamedDim], Type[BaseDim]] = cls if issubclass(cls, BaseDim) else BaseDim
        new_dim_class = cast(type[BaseDim], BaseDimMeta(rname,(immediate_base,), {"_dim_name": pname}))
        cls.note_restriction(restriction, new_dim_class)
        return new_dim_class
    
    
    
    
    
class DerivedDimMeta(NamedDimMeta):
    
    def __new__(cls, name: str, base: tuple[Type,...], dct: dict[str, Any]) -> DerivedDimMeta:
        return super().__new__(cls, name, base, dct)
    
    def __init__(cls, name: str, base: tuple[Type,...], dct: dict[str, Any]) -> None:  # @UnusedVariable @NoSelf
        if name == "DerivedDim":
            return
        # cls._this_class = cls
        d: Optional[Dimensionality] = getattr(cls, "derived", None)
        if d is None:
            raise NameError(f"DerivedDim {name} does not define 'derived'")
        if not isinstance(d, Dimensionality):
            raise TypeError(f"{name}.derived not a Dimensionality")
        if d.name is None:
            n:str = "_".join(split_camel_case(name)).lower()
            d.name = n
            d.quant_class = cast(type[DerivedDim], cls)
        real_d = d
        def my_dim() -> Dimensionality:
            return real_d
        cls.dim = my_dim
        super().__init__(name, base, dct)

        

class DerivedDim(NamedDim, metaclass=DerivedDimMeta): 
    @classmethod
    def dim(cls:type[ND])->Dimensionality[ND]:
        assert False, f"{cls}.dim() not defined by BaseDimMeta"


class BaseDimMeta(NamedDimMeta):
    
    def __new__(cls, name: str, base: tuple[Type,...], dct: dict[str, Any]) -> BaseDimMeta:
        return super().__new__(cls, name, base, dct)
    
    def __init__(self, name: str, base: tuple[Type,...], dct: dict[str, Any]) -> None:  # @UnusedVariable
        if name == "BaseDim" or name == "TiedBaseDim":
            return
        # cls._this_class = cls
        # d = getattr(cls, "_dim", None)
        # if d is not None:
            # raise NameError(f"BaseDim {name} already defines '_dim'")
        # if d is None:
        n: str
        explicit_name = getattr(self, "_dim_name", None)
        if explicit_name is not None:
            assert isinstance(explicit_name, str), f"{name}._dim_name not a str"
            n = explicit_name
        else:
            n = "_".join(split_camel_case(name)).lower()
        
        d: BaseDimension[Any] = BaseDimension(n)
        d.quant_class = cast(type[BaseDim], self)
        def my_dim() -> BaseDimension:
            return d
        self.dim = my_dim
        super().__init__(name, base, dct)

# class UnitFunc(Protocol[U]):
#     def __call__(self, abbr: str, quant: Union[D,UnitExpr[D]], 
#                  *, check: Optional[Dimensionality[D]] = None,
#                  singular: Optional[str] = None) -> U:
        ...    

class BaseDim(NamedDim, metaclass=BaseDimMeta): 
    # _dim: ClassVar[BaseDimension[BD]]
    
    @classmethod
    def dim(cls:type[BD])->BaseDimension[BD]:
        assert False, f"{cls}.dim() not defined by BaseDimMeta"
        
    @staticmethod
    def use_unit(unit: type[U]) -> Callable[[ND, str], U]:
        return unit
    
    @classmethod
    def _base_unit(cls: type[BD],
                   unit: type[U], # @UnusedVariable
                   abbr: str, *, singular: Optional[str]=None,
                   ) -> U:
        return cast(U, cls.dim().base_unit(abbr, singular=singular))
    
    
    @classmethod
    def base_unit(cls: type[BD], abbr: str, *, singular: Optional[str]=None) -> Unit[BD]:
        return cls._base_unit(Unit[BD], abbr, singular=singular)
    
    
    
# class TiedBaseDim(Generic[UE, U], BaseDim):
#     @property
#     @abstractmethod
#     def unit_expr_class(self) -> type[UE]: 
#         ...
#
#     @property
#     @abstractmethod
#     def unit_class(self) -> type[U]:
#         ...
#
#     def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> UE:
#         return (self.unit_expr_class)(self, num, denom)
#
#     def as_unit(self, abbr:str, *, singular: Optional[str] = None) -> U:
#         return (self.unit_class)(abbr, self, singular=singular)
#
#     @classmethod
#     def base_unit(cls, abbr:str, *, singular:Optional[str]=None)->U:
#         return cast(U, super(TiedBaseDim, cls).base_unit(abbr, singular=singular))
    
    
class CountDim(BaseDim):
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
    
    # ERK: I have no idea why this is necessary, but if I don't include it, count dim objects are 
    # unhashable. (10/7/21) 
    def __hash__(self) -> int:
        return super().__hash__()
    
    def __add__(self: CD, rhs: Union[float,CD]) -> CD:
        rmag: float = rhs if isinstance(rhs, (float, int)) else rhs.magnitude
        return self.same_dim(self.magnitude+rmag)
    
    def __radd__(self: CD, lhs: float) -> CD:
        return self.same_dim(lhs+self.magnitude)
    
    # I'm getting rid of the in-place operations because it's maddeningly frustrating to 
    # track down errors due to ZERO() changing because it was used in a context in
    # which somebody thought it was okay to increment.
    
    # def __iadd__(self, rhs: Union[float,ND]) -> ND:
    #     rmag: float = rhs if isinstance(rhs, (float, int)) else rhs.magnitude
    #     self.magnitude += rmag
    #     return self.cast()
    
    def __sub__(self: CD, rhs: Union[float,BD]) -> CD:
        rmag: float = rhs if isinstance(rhs, (float, int)) else rhs.magnitude
        return self.same_dim(self.magnitude-rmag)
    
    def __rsub__(self: CD, lhs: float) -> CD:
        return self.same_dim(lhs-self.magnitude)
        
    # def __isub__(self, rhs: Union[float,ND]) -> ND:
    #     rmag: float = rhs if isinstance(rhs, (float, int)) else rhs.magnitude
    #     self.magnitude -= rmag
    #     return self.cast()

    def __eq__(self, rhs: object) -> bool:
        if isinstance(rhs, (int, float)):
            return self.magnitude == rhs
        if not isinstance(rhs, Quantity): 
            return False
        self._ensure_dim_match(rhs, "==")
        return self.magnitude == rhs.magnitude
    
    def __lt__(self: CD, rhs: Union[float,CD]) -> bool:
        if isinstance(rhs, (int, float)):
            return self.magnitude < rhs
        self._ensure_dim_match(rhs, "<")
        return self.magnitude < rhs.magnitude
    def __gt__(self: CD, rhs: Union[float,CD]) -> bool:
        if isinstance(rhs, (int, float)):
            return self.magnitude > rhs
        self._ensure_dim_match(rhs, ">")
        return self.magnitude > rhs.magnitude
    
    def __le__(self: CD, rhs: Union[float,CD]) -> bool:
        if isinstance(rhs, (int, float)):
            return self.magnitude <= rhs
        self._ensure_dim_match(rhs, "<=")
        return self.magnitude <= rhs.magnitude
    def __ge__(self: CD, rhs: Union[float,CD]) -> bool:
        if isinstance(rhs, (int, float)):
            return self.magnitude >= rhs
        self._ensure_dim_match(rhs, ">=")
        return self.magnitude >= rhs.magnitude

    @classmethod
    def base_unit(cls: type[CD], abbr: str, *, 
                  plural: Optional[str] = None, 
                  singular: Optional[str] = None) -> Unit[CD]:
        assert plural is None or singular is None, f"Both singular ({singular}) and plural ({plural}) specified for {abbr}"
        if singular is None:
            singular = abbr
        if plural is None:
            plural = infer_plural(singular)
        return cls.dim().base_unit(plural, singular=singular)
    
    noun_units: dict[str, Unit] = {}
    
    @classmethod
    def for_noun(cls, singular: str, *, plural: Optional[str] = None) -> Unit:
        unit = cls.noun_units.get(singular, None)
        if unit is None:
            cname = f"count_of_{singular}"
            c: Type[CountDim] = type(cname, (CountDim,), {}) 
            unit = c.base_unit(singular, plural=plural)
            cls.noun_units[singular] = unit
        return unit
    
def qstr(n: float, singular: str, *, plural: Optional[str] = None) -> Quantity:
    q: Quantity = n*CountDim.for_noun(singular, plural=plural)
    return q

class Scalar(NamedDim):
    _dim = Dimensionality['Scalar']((), 'scalar')
    unit_expr: ScalarUnitExpr
    def __float__(self) -> float:
        return float(self.magnitude)
    
    def __pow__(self:D, _rhs: int) -> Scalar:
        return Scalar(self.magnitude**_rhs)
    
    @overload   
    def __mul__(self, _rhs: Union[float, Scalar]) -> Scalar: ...
    @overload
    def __mul__(self, _rhs: Union[D, UnitExpr[D]]) -> D: ...
    def __mul__(self, rhs: Union[float, D, UnitExpr[D]]) ->  Quantity:
        return super().__mul__(rhs)
    
    def __rtruediv__(self, lhs: float) -> Scalar:
        return cast(Scalar, self.in_denom(lhs))

    @classmethod
    def dim(cls)->Dimensionality[Scalar]:
        return cls._dim
    
    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> ScalarUnitExpr:
        return ScalarUnitExpr(self, num, denom)
    
    def as_unit(self, abbr:str, *, singular: Optional[str] = None) -> ScalarUnit:
        return ScalarUnit(abbr, self, singular=singular)
    
    @classmethod
    def from_float(cls, magnitude: float) -> Scalar:
        return Scalar(magnitude, cls.dim())
    
Scalar.dim().quant_class = Scalar

class ScalarUnitExpr(UnitExpr[Scalar]):
    def __pow__(self, rhs: int) -> ScalarUnitExpr:
        return cast(ScalarUnitExpr, super().__pow__(rhs))
    
    @overload
    def __mul__(self, _rhs: float) -> Scalar: ...  
    @overload
    def __mul__(self, _rhs: UE) -> UE: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Scalar, UnitExpr]:
        return super().__mul__(rhs)
    
Scalar.unit_expr = Scalar(1).as_unit_expr((),())
        
class ScalarUnit(Unit[Scalar], ScalarUnitExpr):
    ...

def set_default_units(*units: UnitExpr) -> Mapping[Dimensionality, Sequence[UnitExpr]]:
    # print(f"Setting default units to {map_str(units)}")
    seen = set[UnitExpr]()
    by_dim: dict[Dimensionality, list[UnitExpr]] = defaultdict(list)
    for unit in units:
        if unit not in seen:
            by_dim[unit.dimensionality()].append(unit)
            seen.add(unit)
    for dim,defaults in by_dim.items():
        # print(f"  Defaults for {dim} = {map_str(defaults)}")
        dim.default_units = tuple(defaults)
    return by_dim 

class default_units:
    to_set: Final[Sequence[UnitExpr]]
    to_reset: dict[Dimensionality, Optional[Tuple[UnitExpr, ...]]]
    
    def __init__(self, *units: UnitExpr) -> None:
        self.to_set = units
        self.to_reset = {}
        
    def __enter__(self) -> default_units:
        units = self.to_set
        self.to_reset.clear()
        dims = {unit.dimensionality() for unit in units}
        for dim in dims:
            self.to_reset[dim] = dim.default_units
        set_default_units(*units)
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Literal[False]: # @UnusedVariable
        for dim,defaults in self.to_reset.items():
            dim.default_units = defaults
        return False
    
MaybeBounded = Union[D, "Bounded[D]"]
        
class Bounded(Generic[D]):
    def __init__(self, min_value: D, max_value: D, *,
                 upper_limit: Optional[D] = None,
                 lower_limit: Optional[D] = None) -> None:
        self.min_value: Final[D] = min_value
        self.max_value: Final[D] = max_value
        self.upper_limit: Final[Optional[D]] = upper_limit
        self.lower_limit: Final[Optional[D]] = lower_limit
        
    def _clip(self, new_min: D, new_max: D) -> MaybeBounded:
        upper_limit = self.upper_limit
        lower_limit = self.lower_limit
        if lower_limit is not None:
            new_min = max(new_min, lower_limit)
        if upper_limit is not None:
            new_max = min(new_max, upper_limit)
        if new_min == new_max:
            return new_min
        return Bounded[D](new_min, new_max, 
                          upper_limit=upper_limit, lower_limit=lower_limit)
        
        
    def __add__(self, rhs: MaybeBounded[D]) -> MaybeBounded[D]:
        my_min = self.min_value
        my_max = self.max_value
        if isinstance(rhs, Bounded):
            their_min = rhs.min_value
            their_max = rhs.max_value
        else:
            their_min = their_max = rhs
        return self._clip(my_min+their_min, my_max+their_max)

    def __sub__(self, rhs: MaybeBounded[D]) -> MaybeBounded[D]:
        my_min = self.min_value
        my_max = self.max_value
        if isinstance(rhs, Bounded):
            their_min = rhs.min_value
            their_max = rhs.max_value
        else:
            their_min = their_max = rhs
        return self._clip(my_min-their_min, my_max-their_max)

