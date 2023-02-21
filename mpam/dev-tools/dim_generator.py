from __future__ import annotations

from _collections import defaultdict
from functools import cached_property
from itertools import product
from typing import TypeVar, Generator, Tuple, List, Final, Mapping, Optional, \
    Sequence, Union, Iterable, Callable

from erk.basic import always, ComputedDefaultDict, ValOrFn, ensure_val
from erk.stringutils import split_camel_case, conj_str


T = TypeVar('T')

def value_range_iterator(value: T, min_value: int, max_value: int) -> Generator[Tuple[T, int], None, None]:
    return ((value, n) for n in range(min_value, max_value + 1))

def combinations_iterator(seq: List[Tuple[T, int, int]]) -> Generator[Tuple[Tuple[T, int], ...], None, None]:
    value_ranges = [value_range_iterator(elem[0], elem[1], elem[2]) for elem in seq]
    for combination in product(*value_ranges):
        yield combination
        # yield (combination[0][0], sum(n for _, n in combination))  # return a tuple with value and sum of all ns

def get_combinations(seq: List[Tuple[T, int, int]]) -> List[Tuple[Tuple[T, int], ...]]:
    return list(combinations_iterator(seq))
        
ExptList = tuple[tuple[str, int], ...]

class Dimensionality:
    exponents: Final[ExptList]
    known: Mapping[ExptList, Dimensionality]
    _name: Optional[str] = None
    restrictions: Final[dict[str, Dimensionality]]
    restriction: Optional[tuple[Dimensionality, str]] = None
    extra_methods: Final[list[str]]
    bounds: Final[dict[str, tuple[int, int]]] = {}
    explicitly_named: bool = False
    derivation: Optional[str] = None
    dependencies: Sequence[Dimensionality]
    aliases: Final[list[str]]
    description: Optional[str] = None
    bases: dict[str, Dimensionality] = {}
    by_name: dict[str, Dimensionality] = {}

    
    @property
    def is_scalar(self) -> bool:
        return len(self.exponents) == 0
    
    @cached_property
    def is_base(self) -> bool:
        expts = self.exponents
        return len(expts) == 1 and expts[0][1] == 1
    
    @cached_property
    def _sort_key(self) -> tuple[bool, str]:
        return (not self.is_base, self.name)
    
    @property
    def name(self) -> str:
        s = self._name
        if s is None:
            if len(self.exponents) == 0:
                s = "Scalar"
            else:
                num = [f"{b}{e}" for b,e in self.exponents if e > 0]
                denom = [f"{b}{-e}" for b,e in self.exponents if e < 0]
                s = "DIM_"
                if len(num) > 0:
                    s += "_".join(num)
                if len(denom) > 0:
                    s += "_".join(denom)
            self._name = s
        return s
    
    @property
    def in_bounds(self) -> bool:
        for b,e in self.exponents:
            bounds = self.bounds[b]
            if e < bounds[0]:
                return False
            elif e > bounds[1]:
                return False
        return True

    def __init__(self, exponents: ExptList) -> None:
        self.exponents = self.normalize(exponents)
        self.aliases = []
        self.dependencies = () if self.is_base else tuple(self.bases[e[0]] for e in exponents)
        self.restrictions = {}
        self.extra_methods = []
        
    def __repr__(self) -> str:
        return self.name
    
    @classmethod    
    def normalize(cls, exponents: Sequence[tuple[str, int]]) -> ExptList:
        as_list = [(b,e) for b,e in exponents if e != 0]
        as_list.sort()
        return tuple(as_list)
    
    def __lt__(self, rhs: Dimensionality) -> bool:
        if rhs is self:
            return False
        return self._sort_key < rhs._sort_key
        
        
    @classmethod
    def find(cls, exponents: ExptList) -> Dimensionality:
        return cls.known[exponents]
    
    def named(self, name: str, *, 
              alias: Union[str, Sequence[str]] = (), 
              description: Optional[str] = None) -> Dimensionality:
        self._name = name
        if isinstance(alias, str):
            alias = (alias,)
        self.aliases.extend(alias)
        if description is None:
            description = self.desc_from_name(name)
        self.description = description
        self.explicitly_named = True
        self.by_name[name] = self
        if hasattr(self, "_sort_key"):
            del self._sort_key
        # print(f"{name}: {self.exponents}")
        for b,e in self.exponents:
            bounds = self.bounds[b]
            if e < bounds[0]:
                self.bounds[b] = (e, bounds[1])
            elif e > bounds[1]:
                self.bounds[b] = (bounds[0], e)
        return self
    
    def extra_code(self, method: ValOrFn[str]) -> Dimensionality:
        self.extra_methods.append(ensure_val(method, str))
        return self
    
    @classmethod
    def base(cls, abbr: str, *, min_expt: int = 0, max_expt: int = 1,
             restr: Optional[tuple[Dimensionality, str]] = None) -> Dimensionality:
        exponents = ((abbr, 1),)
        cls.bounds[abbr] = (min_expt, max_expt)
        dim = cls.find(exponents)
        cls.bases[abbr] = dim
        if restr is not None:
            dim.restriction = restr
            d,r = restr
            dim.dependencies = (d,)
            dim.description = f"{d.name}[{r}]"
        return dim
    
    @classmethod
    def desc_from_name(cls, name: str) -> str:
        words = split_camel_case(name)
        return " ".join(w.lower() for w in words)
    
    @classmethod
    def scalar(cls) -> Dimensionality:
        s = cls.find(())
        if s._name is None:
            s.named("Scalar")
        return s
    
    def __pow__(self, n: int) -> Dimensionality:
        if n == 0:
            return self.scalar()
        if n == 1:
            return self
        exponents = tuple((b,e*n) for b,e in self.exponents)
        return self.find(exponents)
    
    def __mul__(self, rhs: Dimensionality) -> Dimensionality:
        exponents = defaultdict[str, int](always(0))
        for b,e in self.exponents:
            exponents[b] += e
        for b,e in rhs.exponents:
            exponents[b] += e
        return self.find(self.normalize(exponents.items()))
            
    def __truediv__(self, rhs: Dimensionality) -> Dimensionality:
        exponents = defaultdict[str, int](always(0))
        for b,e in self.exponents:
            exponents[b] += e
        for b,e in rhs.exponents:
            exponents[b] -= e
        return self.find(self.normalize(exponents.items()))
    
    _next_restriction: int = 1
    def __getitem__(self, restr: str) -> Dimensionality:
        d = self.restrictions.get(restr, None)
        if d is None:
            abbr = f"_r{self._next_restriction}"
            self._next_restriction += 1
            name = f"{self.name}_of_{restr}"
            descr = f":class:`{self.name}`[:class:`{restr}`]"
            d = Dimensionality.base(abbr, restr=(self, restr)).named(name, description=descr)
            self.restrictions[restr] = d
        return d
        
    
    def derived_power(self, n: int, name: str, *, 
                      alias: Union[str, Sequence[str]] = (),
                      description: Optional[str] = None) -> Dimensionality:
        if description is None:
            description = self.desc_from_name(name)
        description += f" (:class:`{self.name}`\ ``**{n}``)"
        dim = (self**n).named(name, alias=alias, description=description)
        dim.derivation = f"{self.name}**{n}"
        dim.dependencies = (self,)
        return dim
    
    def derived_product(self, rhs: Dimensionality, name: str, *, 
                        alias: Union[str, Sequence[str]] = (),
                        description: Optional[str] = None) -> Dimensionality:
        if description is None:
            description = self.desc_from_name(name)
        description += f" (:class:`{self.name}`\ ``*``:class:`{rhs.name}`)"
        dim = (self * rhs).named(name, alias=alias, description=description)
        dim.derivation = f"{self.name}*{rhs.name}"
        dim.dependencies = (self, rhs)
        return dim

    def derived_quotient(self, rhs: Dimensionality, name: str, *, 
                         alias: Union[str, Sequence[str]] = (),
                         description: Optional[str] = None) -> Dimensionality:
        if description is None:
            description = self.desc_from_name(name)
        if self.is_scalar:
            description += f" (``1/``:class:`{rhs.name}`)"
        else:
            description += f" (:class:`{self.name}`\ ``/``:class:`{rhs.name}`)"
        dim = (self / rhs).named(name, alias=alias, description=description)
        dim.derivation = f"{self.name}/{rhs.name}"
        dim.dependencies = (self, rhs)
        return dim
    
    @classmethod
    def dependency_sort(cls, dims: Iterable[Dimensionality], *,
                        include_scalar: bool = False) -> Sequence[Dimensionality]:
        
        seen = set[Dimensionality]()
        if not include_scalar:
            seen.add(Dimensionality.scalar())
            
        dlist = list[Dimensionality]()
        dset = set(dims)
        def add_to_dlist(d: Dimensionality) -> None:
            for dep in d.dependencies:
                if not dep in seen:
                    seen.add(dep)
                    add_to_dlist(dep)
                    dset.discard(dep)
            dlist.append(d)
        
        while dset:
            d = dset.pop()
            if not d in seen:
                seen.add(d)
                add_to_dlist(d)
        return dlist
    
class Emitter:
    dims: Final[set[Dimensionality]]
    restrictions: Final[Sequence[str]]
    indent = "    "
    
    def __init__(self, *,
                 extras: Iterable[Dimensionality] = (),
                 restrictions: Sequence[str] = ()
                 ) -> None:
        self.dims = {*Dimensionality.by_name.values(), *extras}
        self.restrictions = tuple(restrictions)

    def emit(self) -> None:
        self.emit_header()
        self.emit_aliases(Dimensionality.scalar())
        for r in self.restrictions:
            self.emit_restriction(r)
        dims = Dimensionality.dependency_sort(self.dims)
        self.dims.update(dims)
        
        for d in dims:
            self.emit_dim(d)
        

    def emit_header(self) -> None:
        print(f'''
from __future__ import annotations

from quantities.core import BaseDim, DerivedDim, Scalar,\
    Quantity, UnitExpr, Unit, AbbrExp, ScalarUnitExpr
from typing import overload, Union, Literal, Optional, cast

###########################################
# This is a generated file. Do not edit it.
#
# To regenerate the file, edit and run
# tools/gen_dims.py
###########################################
        ''')
        
    def emit_aliases(self, d: Dimensionality) -> None:
        if d.aliases:
            for alias in d.aliases:
                print(f"{alias} = {d.name}")
            print()
        
    def emit_restriction(self, restr: str) -> None:
        print(f'''
class {restr}:
    """
    A restriction base class.  
    """
    ... 
        ''')
        
    def powers_of(self, d: Dimensionality, *,
                  min_power: int = -4,
                  max_power: int = 4) -> Sequence[tuple[int, Dimensionality]]:
        result: list[tuple[int, Dimensionality]] = []
        for e in range(min_power, max_power+1):
            d2 = d**e
            if d2 in self.dims:
                result.append((e, d2))
        return result
    
    def op_of(self, d: Dimensionality, 
              op: Callable[[Dimensionality, Dimensionality], Dimensionality]
              ) -> Sequence[tuple[Dimensionality, Dimensionality]]:
        result: list[tuple[Dimensionality, Dimensionality]] = []
        for d2 in self.dims:
            d3 = op(d, d2)
            if d3 in self.dims:
                result.append((d2, d3))
        return result

    def emit_dim_header(self, d: Dimensionality) -> None:
        parent = "BaseDim" if d.is_base else "DerivedDim"
        indent = self.indent
        name = d.name
        print(f"class {name}({parent}):")
        if d.description is not None:
            print(f'{indent}"""')   
            print(f'{indent}A :class`.Quantity` representing {d.description}')
            if len(d.aliases) > 0:
                alias_desc = conj_str([f":class:`{a}`" for a in d.aliases])
                follow = "is an alias" if len(d.aliases) == 1 else "are aliases"
                print()
                print(f"{indent}{alias_desc} {follow}.")
            print(f'{indent}"""')
        
        if not d.is_base:
            expr = d.derivation
            if expr is None:
                if len(d.exponents) == 1:
                    b,e = d.exponents[0]
                    expr = f"{Dimensionality.bases[b].name}**{e}"
                else: 
                    def base_expr(bd: Dimensionality, e: int) -> str:
                        return bd.name if e==1 else f"({bd.name}**{e})"
                    expr = "*".join(base_expr(Dimensionality.bases[b], e) for b,e in d.exponents)
            print(f"{indent}derived = {expr}")
            print()
        elif d.restriction:
            d2,r = d.restriction
            print(f'{indent}_dim_name = "{d2.name}[{r}]"')
            print()
            
    def unit_expr_name(self, d: Dimensionality) -> str:
        return d.name+"UnitExpr"
            
    def unit_name(self, d: Dimensionality) -> str:
        return d.name+"Unit"
            
    def emit_powers(self, powers: Sequence[tuple[int, Dimensionality]], *,
                    is_ue: bool = False) -> None:
        indent=self.indent
        if len(powers) > 2:
            rtd: Optional[Dimensionality] = None
            default_return = "UnitExpr" if is_ue else "Quantity"
            ignore = f"{indent}# type: ignore[override]"
            for e,d2 in powers:
                if e == -1:
                    rtd = d2
                print(f"{indent}@overload{ignore}")
                ignore = ""
                d2_name = self.unit_expr_name(d2) if is_ue else d2.name
                print(f"{indent}def __pow__(self, _rhs: Literal[{e}]) -> {d2_name}: ...")
            print(f"{indent}@overload")
            print(f"{indent}def __pow__(self, _rhs: int) -> {default_return}: ...")
            print(f"{indent}def __pow__(self, rhs: int) -> {default_return}:")
            print(f"{indent}{indent}return super().__pow__(rhs)")
            print()
            if rtd is not None:
                print(f'''
    def __rtruediv__(self, n: float) -> {rtd.name}:
        return cast({rtd.name}, super().__rtruediv__(n))
                ''')
    def emit_op(self, name: str,
                op: str, mapping: Sequence[tuple[Dimensionality, Dimensionality]], *,
                is_ue: bool = False) -> None:
        indent = self.indent
        if len(mapping) > 0:
            print(f"{indent}@overload{indent}# type: ignore[override]")
            print(f"{indent}def {op}(self, _rhs: float) -> {name}: ...")
            for d2,d3 in mapping:
                print(f"{indent}@overload")
                # d2_ue = self.unit_expr_name(d2)
                d2_ue = f"UnitExpr[{d2.name}]"
                arg = d2_ue if is_ue else f"Union[{d2.name}, {d2_ue}]"
                d3_name = self.unit_expr_name(d3) if is_ue else d3.name
                print(f"{indent}def {op}(self, _rhs: {arg}) -> {d3_name}: ...")
            if is_ue:
                print(f"{indent}@overload")
                print(f"{indent}def {op}(self, _rhs: UnitExpr) -> UnitExpr: ...")
                print(f"{indent}def {op}(self, rhs: Union[float, UnitExpr]) -> Union[{name}, UnitExpr]:")
            else:
                print(f"{indent}@overload")
                print(f"{indent}def {op}(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...")
                print(f"{indent}def {op}(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[{name}, Quantity]:")
            print(f"{indent}{indent}return super().{op}(rhs)")
            print()
            
    def emit_unit_ops(self, d: Dimensionality) -> None:
        ue_name = self.unit_expr_name(d)
        u_name = self.unit_name(d)
        print(f'''
    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> {ue_name}:
        return {ue_name}(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> {u_name}:
        return {u_name}(abbr, self, singular=singular)
        ''')
        if d.is_base:
            print(f'''
    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> {u_name}:
        return cls._base_unit({u_name}, abbr, singular=singular)
            ''')
            
    def emit_unit_expr(self, d: Dimensionality,
                       powers: Sequence[tuple[int, Dimensionality]],
                       products: Sequence[tuple[Dimensionality, Dimensionality]],
                       quotients: Sequence[tuple[Dimensionality, Dimensionality]],
                       ) -> None:
        name = d.name
        ue_name = self.unit_expr_name(d)
        u_name = self.unit_name(d)
        print(f'''
class {ue_name}(UnitExpr[{name}]):
    """
    A :class:`.UnitExpr`[:class:`{name}`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[{name}]] = None, 
                singular: Optional[str] = None) -> {u_name}:
        return cast({u_name}, super().as_unit(abbr, check=check, singular=singular))
        ''')
        if powers or products or quotients:
            self.emit_powers(powers, is_ue=True)
            self.emit_op(d.name, "__mul__", products,is_ue=True)
            self.emit_op(d.name, "__truediv__", quotients, is_ue=True)
    
    def emit_unit(self, d: Dimensionality) -> None:
        name = d.name
        ue_name = self.unit_expr_name(d)
        u_name = self.unit_name(d)
        print(f'''
class {u_name}(Unit[{name}], {ue_name}):
    """
    A :class:`.Unit`[:class:`{name}`] and a :class:`{ue_name}`
    """
    ...
        ''')
    
    def emit_dim(self, d: Dimensionality) -> None:
        self.emit_dim_header(d)
        powers = self.powers_of(d)
        products = self.op_of(d, lambda x,y: x*y)
        quotients = self.op_of(d, lambda x,y: x/y)
        self.emit_powers(powers)
        self.emit_op(d.name, "__mul__", products)
        self.emit_op(d.name, "__truediv__", quotients)
        self.emit_unit_ops(d)
        for code in d.extra_methods:
            print(code)
            
        self.emit_aliases(d)
        if d.restriction:
            d2,r = d.restriction
            print(f"{d2.name}.note_restriction({r}, {d.name})")
        self.emit_unit_expr(d, powers, products, quotients)
        self.emit_unit(d)
        print()
        
            
Dimensionality.known = ComputedDefaultDict(Dimensionality)
