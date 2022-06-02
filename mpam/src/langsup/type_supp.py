from __future__ import annotations

from _collections_abc import Iterable
from enum import Enum, auto
from typing import Final, Optional, Sequence, ClassVar, Callable, \
    Any, Mapping, Union, TypeVar, Generic

from mpam.types import Delayed
from _collections import defaultdict
from quantities.core import Unit
import typing
from abc import ABC, abstractmethod

class TypeMismatchError(RuntimeError):
    have: Final[Type]
    want: Final[Type]
    
    def __init__(self, have: Type, want: Type) -> None:
        super().__init__(f"Cannot convert from {have} to {want}")
        self.have = have
        self.want = want

class Type:
    name: Final[str]
    direct_supers: Final[Sequence[Type]]
    all_supers: Final[Sequence[Type]]
    direct_subs: Final[list[Type]]
    all_subs: Final[list[Type]]
    _maybe: Optional[MaybeType] = None
    _lval: Optional[LvalType] = None
    _cached_converters: Final[dict[Type, Callable[[Any], Any]]]
    
    
    rep_types: dict[Type, Union[typing.Type, tuple[typing.Type,...]]] = {}
    conversions: ClassVar[dict[tuple[Type,Type], Callable[[Any],Any]]] = {}
    compatible: ClassVar[set[tuple[Type,Type]]] = set()
    
    @property
    def maybe(self) -> MaybeType:
        mt = self._maybe
        if mt is None:
            mt = self._maybe = MaybeType(self)
        return mt
    
    @property
    def lval(self) -> LvalType:
        lt = self._lval
        if lt is None:
            lt = self._lval = LvalType(self)
        return lt
    
    @property
    def not_maybe(self) -> Type:
        return self
    
    @property
    def rval(self) -> Type:
        return self
    
    def to_rval(self, val: Any) -> Any:
        return val
    
    ANY: ClassVar[Type]
    NONE: ClassVar[Type]
    IGNORE: ClassVar[Type]
    ERROR: ClassVar[Type]
    NUMBER: ClassVar[Type]
    INT: ClassVar[Type]
    FLOAT: ClassVar[Type]
    WELL: ClassVar[Type]
    BINARY_STATE: ClassVar[Type]
    ON: ClassVar[Type]
    OFF: ClassVar[Type]
    BINARY_CPT: ClassVar[Type]
    PAD: ClassVar[Type]
    WELL_PAD: ClassVar[Type]
    WELL_GATE: ClassVar[Type]
    DROP: ClassVar[Type]
    ORIENTED_DROP: ClassVar[Type]
    DIR: ClassVar[Type]
    ORIENTED_DIR: ClassVar[Type]
    MOTION: ClassVar[MotionType]
    DELTA: ClassVar[Type]
    TWIDDLE_OP: ClassVar[TwiddleOpType]
    PAUSE: ClassVar[PauseType]
    ROW: ClassVar[Type]
    COLUMN: ClassVar[Type]
    BARRIER: ClassVar[Type]
    DELAY: ClassVar[Type]
    TIME: ClassVar[Type]
    TICKS: ClassVar[Type]
    BOOL: ClassVar[Type]
    STRING: ClassVar[Type]
    VOLUME: ClassVar[Type]
    SCALED_REAGENT: ClassVar[Type]
    REAGENT: ClassVar[Type]
    LIQUID: ClassVar[Type]
    BUILT_IN: ClassVar[Type]
    # TEMP: ClassVar[Type]
    ABS_TEMP: ClassVar[Type]
    REL_TEMP: ClassVar[Type]
    AMBIG_TEMP: ClassVar[Type]
    HEATER: ClassVar[Type]
    MAGNET: ClassVar[Type]
    BOARD: ClassVar[Type]
    POWER_SUPPLY: ClassVar[Type]
    VOLTAGE: ClassVar[Type]
    POWER_MODE: ClassVar[Type]
    FAN: ClassVar[Type]
    
    def __init__(self, name: str, supers: Optional[Sequence[Type]] = None, *, 
                 is_root: bool = False):
        self.name = name
        if supers is None:
            supers = [] if is_root else  [Type.ANY]
            
        self.direct_supers = supers
        self.direct_subs = []
        self.all_subs = []
        self._cached_converters = {}
        
        ancestors = set[Type](supers) 
        
        for st in supers:
            st.direct_subs.append(self)
            st.all_subs.append(self)
            for anc in st.all_supers:
                ancestors.add(anc)
                if self not in anc.all_subs:
                    anc.all_subs.append(self)
        self.all_supers = list(ancestors) 

    def __repr__(self) -> str:
        return f"Type.{self.name}"
    
    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, rhs: object) -> bool:
        return self is rhs
    
    _cached_lt: Final[dict[tuple[Type, Type], bool]] = {}
    
    def __lt__(self, rhs: Type) -> bool:
        if self is rhs:
            return False
        key = (self, rhs)
        val = self._cached_lt.get(key, None)
        if val is not None:
            return val
        val = self.subsumed_by(rhs)
        self._cached_lt[key] = val
        return val
        
    def subsumed_by(self, rhs: Type) -> bool:
        if isinstance(rhs, MaybeType):
            if self is Type.NONE:
                return True
            elif isinstance(self, MaybeType):
                return self.if_there_type < rhs.if_there_type
            else:
                return self <= rhs.if_there_type
        if self in rhs.all_subs:
            return True
        return self.can_convert_to(rhs)
    
    def __le__(self, rhs: Type) -> bool:
        return self is rhs or self < rhs
    
    @classmethod
    def upper_bounds(cls, *types: Type) -> Sequence[Type]:
        maybe = any(isinstance(t, MaybeType) for t in types)
        if maybe:
            types = tuple(t.if_there_type if isinstance(t, MaybeType) else t for t in types)
        if len(types) == 0:
            return ()
        candidates = {types[0], *types[0].all_supers}
        candidates.intersection_update(*({t, *t.all_supers} for t in types[1:]))
        
        remove = set[Type]()
        for c1 in candidates:
            for c2 in candidates:
                if c1 < c2:
                    remove.add(c2)
        candidates -= remove
        if maybe:
            return tuple(c.maybe for c in candidates)
        return tuple(candidates)
    
    @classmethod
    def upper_bound(cls, *types: Type) -> Type:
        bounds = cls.upper_bounds(*types)
        return Type.NONE if len(bounds) == 0 else bounds[0]
    
    @classmethod
    def register_conversion(cls, have: Type, want: Type, converter: Callable[[Any], Any]) -> None:
        cls.conversions[(have, want)] = converter
        
    @classmethod
    def value_compatible(cls, have: Union[Type, Sequence[Type]], want: Union[Type, Sequence[Type]]) -> None:
        if isinstance(have, Type):
            have = (have,)
        if isinstance(want, Type):
            want = (want,)
        cls.compatible |= {(h,w) for h in have for w in want}
        
    # def converter_to(self, want: Type) -> Callable[[Any], Any]:
    #     if want is self:
    #         return lambda v: v
    #     return lambda v: self.convert_to(want, v)
    
    # @classmethod
    # def cls_make_converter(cls, have: Type, want: Type) -> Optional[Callable[[Any], Any]]:
    #     if isinstance(have, LvalType):
    #         if isinstance(want, LvalType):
    #             return None
    #         rval_type = have.rval_type
    #         def convert_lval(val: Any) -> Any:
    #             assert isinstance(val, LValue), f"{val} has asserted type {have}, not an LValue"
    #             return rval_type.convert_to(want, val.get_value())
    #         return convert_lval
    #     if isinstance(want, MaybeType):
    #         to_type = want.if_there_type
    #         def convert_to_maybe(val: Any) -> Any:
    #             if val is None:
    #                 return val
    #             if isinstance(have, MaybeType):
    #                 from_type = have.if_there_type
    #             else:
    #                 from_type = have
    #             return from_type.convert_to(to_type, val)
    #         return convert_to_maybe
    #     if (have, want) in cls.compatible:
    #         return lambda x: x
    #     fn = cls.conversions.get((have, want), None)
    #     if fn is not None:
    #         return fn
    #     have_rep = cls.rep_types.get(have, None)
    #     want_rep = cls.rep_types.get(want, None)
    #     if have_rep is not None and want_rep is not None:
    #         if not isinstance(have_rep, tuple):
    #             have_rep = (have_rep,)
    #         compatible_reps = all(issubclass(r, want_rep) for r in have_rep)
    #         if compatible_reps:
    #             return lambda x: x
    #     return None

    def make_converter(self, want: Type) -> Optional[Callable[[Any], Any]]:
        if isinstance(want, MaybeType):
            to_type = want.if_there_type
            def convert_to_maybe(val: Any) -> Any:
                if val is None:
                    return val
                return self.not_maybe.convert_to(to_type, val)
            return convert_to_maybe
        if (self, want) in Type.compatible:
            return lambda x: x
        fn = Type.conversions.get((self, want), None)
        if fn is not None:
            return fn
        have_rep = Type.rep_types.get(self, None)
        want_rep = Type.rep_types.get(want, None)
        if have_rep is not None and want_rep is not None:
            if not isinstance(have_rep, tuple):
                have_rep = (have_rep,)
            compatible_reps = all(issubclass(r, want_rep) for r in have_rep)
            if compatible_reps:
                return lambda x: x
        return None
        
    def convert_to(self, want: Type, val: Any) -> Any:
        if self is want:
            return val
        if want is Type.ANY:
            return val
        if want is Type.NONE:
            return None
        converter = self._cached_converters.get(want, None)
        if converter is None:
            converter = self.make_converter(want)
            if converter is None:
                raise TypeMismatchError(self, want)
            self._cached_converters[want] = converter
        return converter(val)

    
    def can_convert_to(self, want: Type) -> bool:
        if self is want or want is Type.ANY or want is Type.NONE:
            return True
        key = (self, want)
        if key in self.compatible or key in self.conversions:
            return True
        if isinstance(want, MaybeType):
            if isinstance(self, MaybeType):
                return self.if_there_type.can_convert_to(want.if_there_type)
            else:
                return self.can_convert_to(want.if_there_type)
        return False
    
Type.ANY = Type("ANY", is_root=True)
Type.NONE = Type("NONE")
Type.IGNORE = Type("IGNORE")
Type.ERROR = Type("ERROR")
Type.WELL = Type("WELL")
Type.NUMBER = Type("NUMBER")
Type.FLOAT = Type("FLOAT", [Type.NUMBER])
Type.INT = Type("INT", [Type.FLOAT])
Type.BINARY_CPT = Type("BINARY_CPT")
Type.BINARY_STATE = Type("BINARY_STATE")
Type.PAD = Type("PAD", [Type.BINARY_CPT])
Type.WELL_PAD = Type("WELL_PAD", [Type.BINARY_CPT])
Type.WELL_GATE = Type("WELL_GATE", [Type.WELL_PAD])
Type.DROP = Type("DROP", [Type.PAD])
Type.ORIENTED_DROP = Type("ORIENTED_DROP", [Type.DROP])
Type.DIR = Type("DIR")
Type.ORIENTED_DIR = Type("ORIENTED_DIR", [Type.DIR])
Type.ROW = Type("ROW")
Type.COLUMN = Type("COLUMN")
Type.BARRIER = Type("BARRIER")
Type.DELAY = Type("DELAY")
Type.TIME = Type("TIME", [Type.DELAY])
Type.TICKS = Type("TICKS", [Type.DELAY])
Type.BOOL = Type("BOOL")
Type.STRING = Type("STRING")
Type.VOLUME = Type("VOLUME")
Type.SCALED_REAGENT = Type("SCALED_REAGENT")
Type.REAGENT = Type("REAGENT", [Type.SCALED_REAGENT])
Type.LIQUID = Type("LIQUID")
Type.BUILT_IN = Type("BUILT_IN")
Type.ABS_TEMP = Type("ABS_TEMP")
Type.REL_TEMP = Type("REL_TEMP")
Type.AMBIG_TEMP = Type("AMBIG_TEMP", [Type.ABS_TEMP, Type.REL_TEMP])
Type.HEATER = Type("HEATER", [Type.BINARY_CPT])
Type.MAGNET = Type("MAGNET", [Type.BINARY_CPT])
Type.BOARD = Type("BOARD")
Type.POWER_SUPPLY = Type("POWER_SUPPLY", [Type.BINARY_CPT])
Type.VOLTAGE = Type("VOLTAGE")
Type.POWER_MODE = Type("POWER_MODE")
Type.FAN = Type("FAN", [Type.BINARY_CPT])

class MaybeType(Type):
    if_there_type: Final[Type]
    
    @property
    def not_maybe(self) -> Type:
        return self.if_there_type

    def __init__(self, if_there_type: Type) -> None:
        super().__init__(f"MAYBE({if_there_type.name})")
        self.if_there_type = if_there_type
        
    @property
    def maybe(self)->MaybeType:
        return self
        
    def __repr__(self) -> str:
        return f"Maybe({self.if_there_type})"
    
    # def __lt__(self, rhs: Type) -> bool:
    #     if isinstance(rhs, MaybeType):
    #         return self.if_there_type < rhs.if_there_type
    #     return super().__lt__(rhs)
    
class LvalType(Type):
    rval_type: Final[Type]
    
    @property
    def maybe(self) -> MaybeType:
        return self.rval_type.maybe
    
    @property
    def lval(self) -> LvalType:
        return self
    
    @property
    def rval(self) -> Type:
        return self.rval_type
    
    def to_rval(self, val: Any) -> Any:
        return self._val_as_LValue(val).get_value()
    
    def __init__(self, rval_type: Type) -> None:
        super().__init__(f"Lval({rval_type.name})", (rval_type,))
        self.rval_type = rval_type
        
    def __repr__(self) -> str:
        return f"LVal({self.rval_type})"
    
    def _val_as_LValue(self, val: Any) -> LValue:
        assert isinstance(val, LValue), f"{val} has asserted type {self}, not an LValue"
        return val
    
    def make_converter(self, want:Type)->Optional[Callable[[Any], Any]]:
        if isinstance(want, LvalType):
            return None
        def convert_lval(val: Any) -> Any:
            val = self._val_as_LValue(val)
            return self.rval_type.convert_to(want, val.get_value())
        return convert_lval

    
    
class LValue(ABC):
    val_type: Final[Type]
    
    def __init__(self, val_type: Type):
        self.val_type = val_type.lval
        
    def describe(self) -> str:
        return type(self).__name__
    
    def __str__(self):
        return f"Lval[{self.describe()}: {self.get_value()}"

    @abstractmethod
    def get_value(self) -> Any:
        ...
        
    @abstractmethod
    def _set(self, val: Any) -> Any: # @UnusedVariable
        ...
        
    def set_value(self, val: Any) -> Any:
        if self.is_short_circuit_val(val):
            return val
        return self._set(val)
    
    def is_short_circuit_val(self, val: Any) -> bool: # @UnusedVariable
        return False

    def modify(self, *, delta: Callable[[], Delayed[Any]],
               modifier: Callable[[Any, Any], Delayed[Any]]) -> Delayed[Any]:
        
        old = self.get_value()
        if self.is_short_circuit_val(old):
            return Delayed.complete(old)

        def with_delta(d: Any) -> Delayed[Any]:
            if self.is_short_circuit_val(d):
                return Delayed.complete(d)

            return (modifier(old, d)
                    .transformed(lambda new: self.set_value(new)))
        return (delta()
                .chain(with_delta))
                    

class Signature:
    param_types: Final[tuple[Type,...]]
    return_type: Final[Type]
    _known: ClassVar[dict[tuple[tuple[Type,...], Type], Signature]] = {}
    
    def __init__(self, param_types: tuple[Type, ...], return_type: Type) -> None:
        self.param_types = param_types
        self.return_type = return_type
    
    @classmethod
    def of(cls, param_types: Sequence[Type], return_type: Type) -> Signature:
        if not isinstance(param_types, tuple):
            param_types = tuple(param_types)
        key = param_types, return_type
        sig = cls._known.get(key, None)
        if sig is None:
            sig = Signature(param_types, return_type)
            cls._known[key] = sig
        return sig
    
    def __repr__(self) -> str:
        return f"Signature({self.param_types}, {self.return_type})"
    
    def __str__(self) -> str:
        return f"{' x '.join(t.name for t in self.param_types)} -> {self.return_type}"
    
    def __hash__(self) -> int:
        return id(self)
    
    def __eq__(self, rhs: object) -> bool:
        return self is rhs
    
    def callable_using(self, arg_types: Sequence[Type]) -> bool:
        return (len(arg_types) == len(self.param_types)
                and all(theirs <= mine 
                        for mine,theirs in zip(self.param_types, arg_types)))
    
    def narrower_than(self, other: Signature) -> bool:
        val = False
        for mine,theirs in zip(self.param_types, other.param_types):
            if theirs < mine:
                return False
            if mine < theirs:
                val = True
        # I'm going covariant on both sides deliberately, but I'm not sure that's right.
        return val or self.return_type < other.return_type


class CallableType(Type):
    sig: Final[Signature]
    with_self_sig: Final[Signature]
    
    @property
    def param_types(self) -> Sequence[Type]:
        return self.sig.param_types
    
    @property
    def return_type(self) -> Type:
        return self.sig.return_type
    
    # param_types: Final[Sequence[Type]]
    # return_type: Final[Type]
    
    def __init__(self,
                 name: str,  
                 param_types: Sequence[Type],
                 return_type: Type,
                 *,
                 supers: Optional[Sequence[Type]] = None):
        super().__init__(name, supers)
        self.sig = Signature.of(param_types, return_type)
        self.with_self_sig = Signature.of((self, *param_types), return_type)
        

class MotionType(CallableType):
    def __init__(self, name: str = "MOTION", *,
                 supers: Optional[Sequence[Type]] = None) -> None:
        super().__init__(name, (Type.DROP,), Type.DROP, supers=supers)
        
Type.MOTION = MotionType()

class DeltaType(MotionType):
    def __init__(self) -> None:
        super().__init__("DELTA", supers=(Type.MOTION,))

Type.DELTA = DeltaType()


class TwiddleOpType(CallableType):
    def __init__(self):
        super().__init__("TWIDDLE_OP", (Type.BINARY_CPT,), Type.NONE)
        
Type.TWIDDLE_OP = TwiddleOpType()
Type.ON = Type("ON", [Type.BINARY_STATE, Type.TWIDDLE_OP])
Type.OFF = Type("OFF", [Type.BINARY_STATE, Type.TWIDDLE_OP])

class PauseType(CallableType):
    def __init__(self):
        super().__init__("PAUSE", (Type.ANY,), Type.NONE)
        
Type.PAUSE = PauseType()

class CompositionType(CallableType):
    instances = dict[Signature, 'CompositionType']()
    
    def __init__(self, 
                 param_types: Sequence[Type],
                 return_type: Type):
        super().__init__(f"Composition[({','.join(t.name for t in param_types)}),{return_type.name}]", 
                         param_types, return_type)
        
    @classmethod
    def find(cls, param_types: Sequence[Type], return_type: Type) -> CompositionType:
        sig = Signature.of(param_types, return_type)
        mt = cls.instances.get(sig, None)
        if mt is None:
            mt = CompositionType(param_types, return_type)
            cls.instances[sig] = mt
        return mt

class MacroType(CallableType):
    instances = dict[Signature, 'MacroType']()
    
    def __init__(self, 
                 param_types: Sequence[Type],
                 return_type: Type):
        super().__init__(f"Macro[({','.join(t.name for t in param_types)}),{return_type.name}]", 
                         param_types, return_type)
        
    @classmethod
    def find(cls, param_types: Sequence[Type], return_type: Type) -> MacroType:
        sig = Signature.of(param_types, return_type)
        mt = cls.instances.get(sig, None)
        if mt is None:
            mt = MacroType(param_types, return_type)
            cls.instances[sig] = mt
        return mt
    
    # I'm not sure if it's really correct to put this here, but
    # it will probably do the right thing.
    
    def subsumed_by(self, rhs:Type)->bool:
        if isinstance(rhs, MacroType):
            return self.sig.narrower_than(rhs.sig)
        return super().subsumed_by(rhs)
    
    # def __eq__(self, rhs:object)->bool:
    #     if isinstance(rhs, MacroType):
    #         return self.sig == rhs.sig
    #     return CallableType.__eq__(self, rhs)
    
    def __hash__(self)->int:
        return hash(self.sig)
    
_T = TypeVar("_T")

class BySigDispatch(Generic[_T]):

    @property
    def known_sigs(self) -> Sequence[Signature]:
        return tuple(p[0] for p in self.overloads.values())

    def __init__(self) -> None:
        self.overloads: Final[dict[tuple[Type,...], 
                                   tuple[Signature, _T]]] = {}

    def add(self, param_types: Sequence[Type], 
            return_type: Type, 
            definition: _T) -> None:
        sig = Signature.of(param_types, return_type)
        self.overloads[sig.param_types] = (sig,definition)

    def add_all(self, sigs: Sequence[Union[Signature, tuple[Sequence[Type], Type]]],
                definition: _T) -> None:
        for sig in sigs:
            if isinstance(sig, Signature):
                param_types: Sequence[Type] = sig.param_types
                return_type = sig.return_type
            else:
                param_types, return_type = sig
            self.add(param_types, return_type, definition)
    
    def find_best(self, arg_types: Sequence[Type]) -> Optional[tuple[Signature, _T]]:
        d = self.overloads
        best: Optional[tuple[Signature, _T]] = None
        for sig, defn in d.values():
            if sig.callable_using(arg_types) and (best is None or sig.narrower_than(best[0])):
                best = (sig,defn)
        return best
    
class Func:
    Definition = Callable[..., Delayed]
    table: Final[BySigDispatch[Definition]]
    TypeExprFormatter = Callable[..., Optional[str]]
    name: Final[str]
    # verb: Final[str]
    type_expr_formatters: Final[dict[Optional[int], list[TypeExprFormatter]]]
    
    def __init__(self, name: str, 
                 # *,
                 # verb: Optional[str] = None,
                 # error_msg_factory: Optional[Callable[[Sequence[Type], str], Optional[str]]] = None,
                 ) -> None:
        self.name = name
        self.table = BySigDispatch()
        # self.verb = verb or name.lower()
        # self.error_msg_factory = error_msg_factory
        self.type_expr_formatters = defaultdict(list)
        
    def __repr__(self) -> str:
        return f"Func.{self.name}"
    
    def register(self, param_types: Sequence[Type], 
                 return_type: Type, 
                 definition: Definition) -> Func:
        self.table.add(param_types, return_type, definition)
        return self
        
    def register_immediate(self, param_types: Sequence[Type], return_type: Type, definition: Callable[..., Any]) -> Func:
        def fn(*args) -> Delayed:
            return Delayed.complete(definition(*args))
        return self.register(param_types, return_type, fn)
    def register_all(self, sigs: Sequence[Union[Signature, tuple[Sequence[Type], Type]]],
                     definition: Definition) -> Func:
        self.table.add_all(sigs, definition)
        return self
        
    def register_all_immediate(self, sigs: Sequence[Union[Signature, tuple[Sequence[Type], Type]]],
                               definition: Callable[..., Any]) -> Func:
        for sig in sigs:
            if isinstance(sig, Signature):
                param_types: Sequence[Type] = sig.param_types
                return_type = sig.return_type
            else:
                param_types, return_type = sig
            self.register_immediate(param_types, return_type, definition)
        return self
    
    def __getitem__(self, arg_types: Sequence[Type]) -> Optional[tuple[Signature, Definition]]:
        return self.table.find_best(arg_types)
    
        
    def format_type_expr_using(self, arity: Optional[int], formatter: Func.TypeExprFormatter, *,
                               override: bool = False) -> Func:
        if override:
            self.type_expr_formatters[arity] = [formatter]
        else:
            self.type_expr_formatters[arity].append(formatter)
        return self
            
    def infix_op(self, op: str, *, override: bool = False) -> Func:
        return self.format_type_expr_using(2, lambda x,y: f"{x} {op} {y}", override=override)
    def prefix_op(self, op: str, *, override: bool = False) -> Func:
        return self.format_type_expr_using(1, lambda x: f"{op} {x}", override=override)
    def postfix_op(self, op: str, *, override: bool = False) -> Func:
        return self.format_type_expr_using(1, lambda x: f"{x} {op}", override=override)

    def format_type_expr(self, types: Sequence[Type]) -> str:
        arity = len(types)
        names = [t.name for t in types]
        for formatter in self.type_expr_formatters[arity]:
            if val := formatter(*names):
                return val
        for formatter in self.type_expr_formatters[None]:
            if val := formatter(names):
                return val
        return f"{self.name}({', '.join(names)})"
    
    def type_error(self, arg_types: Sequence[Type], text: str) -> str:
        error = f"Cannot compute {self.format_type_expr(arg_types)}: {text}"
        sigs = self.table.known_sigs
        if len(sigs) == 0:
            return error
        expectations = [f"{self.format_type_expr(sig.param_types)} -> {sig.return_type.name}" for sig in sigs]
        expectations.sort()
        error += "\n  expected"
        if len(sigs) > 1:
            error += " one of"
        indent = "    "
        error += ":\n" + indent + ("\n"+indent).join(expectations)
        return error
    
    def error_type(self, arg_types: Sequence[Type], *, 
                   default_type: Type = Type.NONE) -> Type:
        penetration: int = 0
        best: Optional[Type] = None
        mismatch = False
        def match_len(pts: Sequence[Type]) -> int:
            for i,pt in enumerate(pts):
                at = arg_types[i]
                if not at<=pt:
                    return i
            return len(pts)
        for sig in self.table.known_sigs:
            rt = sig.return_type
            ml = match_len(sig.param_types)
            if ml > penetration:
                best = rt
                penetration = ml
                mismatch = False
            elif ml == penetration and not mismatch:
                if best is None or best <= rt:
                    best = rt
                elif not rt < best:
                    mismatch = True
        return default_type if mismatch or best is None else best
                
    
class Attr:
    Getter = Callable[[Any], Any]
    Setter = Callable[[Any,Any], Any]
    # Definition = Callable[..., Any]
    name: Final[str]
    getters: Final[BySigDispatch[Getter]]
    setters: Final[BySigDispatch[Setter]]


    def __init__(self, name: str) -> None:
        self.name = name
        self.getters = BySigDispatch()
        self.setters = BySigDispatch()
        
    def __repr__(self) -> str:
        return f"Attr.{self.name}"
    
    @property
    def applies_to(self) -> Sequence[Type]:
        return [sig.param_types[0] for sig in self.getters.known_sigs if len(sig.param_types) == 1]
    
    @property
    def returns(self) -> Sequence[Type]:
        return [sig.return_type for sig in self.getters.known_sigs if len(sig.param_types) == 1]
    
    def register_setter(self, otype: Union[Type, Sequence[Type]], vtype, 
                        setter: Callable[[Any,Any], Any]) -> None:
        if isinstance(otype, Type):
            self.setters.add((otype, vtype), Type.NONE, setter)
        else:
            for ot in otype:
                self.setters.add((ot, vtype), Type.NONE, setter)
                 
    
    def register(self, otype: Union[Type,Sequence[Type]], rtype: Type, extractor: Callable[[Any], Any],
                 *,
                 setter: Optional[Callable[[Any,Any], Any]] = None) -> None:
        if isinstance(otype, Type):
            self.getters.add((otype,), rtype, extractor)
        else:
            for ot in otype:
                self.getters.add((ot,), rtype, extractor)
        if setter is not None:
            self.register_setter(otype, rtype, setter)
                    
    def getter(self, otype: Type) -> Optional[tuple[Signature, Getter]]:
        return self.getters.find_best((otype,))
        
    def setter(self, otype: Type, vtype: Type) -> Optional[tuple[Signature, Setter]]:
        return self.setters.find_best((otype, vtype))
    
    # def __getitem__(self, otype: Type) -> Optional[tuple[Signature, Callable[..., Delayed]]]:
        # return self.getter(otype)
    
    def accepts_for(self, otype: Type) -> Sequence[Type]:
        return [sig.param_types[1] for sig in self.setters.known_sigs 
                    if len(sig.param_types) == 2 and otype <= sig.param_types[0]]
        
    @classmethod
    def new_instances(cls, names: Iterable[str]) -> None:
        for name in names:
            setattr(cls, name, Attr(name))
                

class Rel(Enum):
    # BUG: MyPy 0.931 (12128).  MyPy is confused because _ignore_ is going to be
    # deleted by Enum's metaclass.  This has been fixed but not released.
    # https://github.com/python/mypy/pull/12128
    _ignore_ = ["_known"] # type: ignore[misc]    
    _known: ClassVar[Mapping[Rel, Callable[[Any,Any], Any]]]
    
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    
    def test(self, x, y) -> bool:
        fn = self._known[self]
        res = fn(x, y)
        assert isinstance(res, bool)
        return res
    
Rel._known = {
    Rel.EQ: lambda x,y: x == y,
    Rel.NE: lambda x,y: x != y,
    Rel.LT: lambda x,y: x < y,
    Rel.LE: lambda x,y: x <= y,
    Rel.GT: lambda x,y: x > y,
    Rel.GE: lambda x,y: x >= y,
    }
    
class EnvRelativeUnit(Enum):
    DROP = auto()
    
PhysUnit = Union[Unit,EnvRelativeUnit]

class NumberedItem(Enum):
    WELL = auto()
    HEATER = auto()
    MAGNET = auto()

if __name__ == '__main__':
    def check(lhs: Type, rhs: Type) -> None:
        print(f"Comparing {lhs} and {rhs}:")
        # print(f"  {lhs}.all_subs = {map_str(lhs.all_subs)}")
        # print(f"  {rhs}.all_subs = {map_str(rhs.all_subs)}")
        print(f"  {lhs} == {rhs}: {lhs == rhs}")
        print(f"  {lhs} != {rhs}: {(lhs != rhs)}")
        print(f"  {lhs} < {rhs}: {lhs < rhs}")
        print(f"  {lhs} <= {rhs}: {lhs <= rhs}")
        print(f"  {lhs} > {rhs}: {lhs > rhs}")
        print(f"  {lhs} >= {rhs}: {lhs >= rhs}")
        
    
    check(Type.WELL, Type.INT)
    check(Type.INT, Type.NUMBER)
    check(Type.WELL, Type.WELL)
    check(Type.WELL, Type.ANY)