from __future__ import annotations

from _collections_abc import Iterable
from enum import Enum, auto
from typing import Final, Optional, Sequence, ClassVar, Callable, \
    Any, Mapping, Union

from mpam.types import Delayed
from _collections import defaultdict
from quantities.core import Unit, qstr
import typing
from functools import cached_property
from threading import RLock
import logging
from erk.stringutils import conj_str
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class TypeMismatchError(RuntimeError):
    have: Final[Type]
    want: Final[Type]
    
    def __init__(self, have: Type, want: Type) -> None:
        super().__init__(f"Cannot convert from {have} to {want}")
        self.have = have
        self.want = want
        
ValueConverter = Callable[[Any], Any]

class SpecialValueConverter(Enum):
    NO_CONVERSION = auto()
    IDENTITY = auto()
    
_Converter = Union[ValueConverter, SpecialValueConverter]

_RepTypes = tuple[typing.Type,...]
TypeRepSpec = Union[typing.Type, _RepTypes]

def _trs_to_tuple(trs: TypeRepSpec) -> _RepTypes:
    return trs if isinstance(trs, tuple) else (trs,)

class Type:
    name: Final[str]
    direct_supers: Final[Sequence[Type]]
    all_supers: Final[Sequence[Type]]
    direct_subs: Final[list[Type]]
    all_subs: Final[list[Type]]
    rep_types: _RepTypes
    as_func_type: Final[Optional[CallableType]]
    
    _conversions: Final[dict[Type, _Converter]]
    _maybe: Optional[MaybeType] = None
    
    _class_lock: Final = RLock()
    
    conversions: ClassVar[dict[tuple[Type,Type], Callable[[Any],Any]]] = {}
    compatible: ClassVar[set[tuple[Type,Type]]] = set()
    
    @property
    def maybe(self) -> MaybeType:
        mt = self._maybe
        if mt is None:
            mt = self._maybe = MaybeType(self)
        return mt
    
    ANY: ClassVar[Type]
    NONE: ClassVar[Type]
    IGNORE: ClassVar[Type]
    ERROR: ClassVar[Type]
    NUMBER: ClassVar[Type]
    INT: ClassVar[Type]
    FLOAT: ClassVar[Type]
    WELL: ClassVar[Type]
    ACTION: ClassVar[CallableType]
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
    TEMP_CONTROL: ClassVar[Type]
    HEATER: ClassVar[Type]
    CHILLER: ClassVar[Type]
    MAGNET: ClassVar[Type]
    BOARD: ClassVar[Type]
    POWER_SUPPLY: ClassVar[Type]
    VOLTAGE: ClassVar[Type]
    POWER_MODE: ClassVar[Type]
    FAN: ClassVar[Type]
    
    # @cached_property
    # def as_callable_type(self) -> Optional[CallableType]:
    #     candidates = filter(lambda t: isinstance(t, CallableType), self.all_supers)
    #     funcs = self.upper_bounds(*candidates)
    
    def __init__(self, name: str, supers: Optional[Sequence[Type]] = None, *, 
                 is_root: bool = False,
                 as_func_type: Optional[CallableType] = None,
                 rep_types: TypeRepSpec = ()):
        self.name = name
        if supers is None:
            supers = [] if is_root else  [Type.ANY]
            
        self.direct_supers = supers
        self.direct_subs = []
        self.all_subs = []
        self.rep_types = _trs_to_tuple(rep_types)
        self._conversions = {}
        
        if as_func_type is None:
            super_func_types = set(s.as_func_type for s in supers if s.as_func_type is not None)
            if len(super_func_types) > 0:
                sfts = list(super_func_types)
                as_func_type = sfts[0]
                if len(super_func_types) > 1:
                    logger.warning(f"Multiple function supers for {self}: {conj_str(sfts)}.  Using {as_func_type}.")
        self.as_func_type = as_func_type
        
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
    def __lt__(self, rhs: Type) -> bool:
        return self is not rhs and self.can_convert_to(rhs)
        
        # if self is rhs:
        #     return False
        # if rhs is Type.ANY:
        #     return self is not Type.ANY
        # if isinstance(rhs, MaybeType):
        #     if self is Type.NONE:
        #         return True
        #     elif isinstance(self, MaybeType):
        #         return self.if_there_type < rhs.if_there_type
        #     else:
        #         return self < rhs.if_there_type
        # if self in rhs.all_subs:
        #     return True
        # return self.can_convert_to(rhs)
    def __le__(self, rhs: Type) -> bool:
        return self is rhs or self < rhs
    
    def set_rep_type(self, rep_types: TypeRepSpec) -> None:
        with self._class_lock:
            self.rep_types = _trs_to_tuple(rep_types)
            

    # _warned_multiple_conversions: Final = set[tuple[Type, Type]]()ll      # _warned_no_conversion_to_super: Final = set[tuple[Type, Type]]()
    
    def _rep_compatible(self, other: Type) -> bool:
        # By default, we are implicitly compatible if all of our possible rep
        # types are subclasses of any of their rep types.
        
        other_reps = other.rep_types
        return all(issubclass(r, other_reps) for r in self.rep_types)
    
    def _find_conversion_to(self, other: Type) -> _Converter:
        # Called with _class_lock locked
        if other is Type.ANY:
            return SpecialValueConverter.IDENTITY
        # if other is Type.NONE:
        #     return to_const(None)
        if isinstance(other, MaybeType):
            if self is Type.NONE:
                return SpecialValueConverter.IDENTITY
            if not isinstance(self, MaybeType):
                return self._conversion_to(other.if_there_type)
            # Both sides are maybes
            conv = self.if_there_type._conversion_to(other.if_there_type)
            if conv is SpecialValueConverter.NO_CONVERSION or conv is SpecialValueConverter.IDENTITY:
                return conv
            fn = conv
            return lambda v: None if v is None else fn(v)
        if other in self.direct_supers:
            # There's no explicit conversion and no prohibited conversion,
            # so if it's a direct super, it's okay if the reps are compatible
            rep_compatible = self._rep_compatible(other)
            return SpecialValueConverter.IDENTITY if rep_compatible else SpecialValueConverter.NO_CONVERSION        
        # It isn't a direct super, but maybe we can go through a direct
        # super or somebody we know how to convert to.
            

        def compose(first: _Converter, second: _Converter) -> _Converter:
            if first is SpecialValueConverter.NO_CONVERSION or second is SpecialValueConverter.NO_CONVERSION:
                return SpecialValueConverter.NO_CONVERSION
            if first is SpecialValueConverter.IDENTITY:
                return second
            if second is SpecialValueConverter.IDENTITY:
                return first
            f = first
            s = second
            return lambda v: s(f(v))
        
        middles = dict[Type, _Converter]()
        def check_and_add(middle: Type) -> None:
            if middle is Type.ANY:
                return
            
            # First, we check to see whether we can do the conversion through this type.
            
            to_middle = self._conversion_to(middle)
            if to_middle is SpecialValueConverter.NO_CONVERSION:
                return
            c = compose(to_middle, middle._conversion_to(other))
            if c is SpecialValueConverter.NO_CONVERSION:
                return
            # It's possible.  Now we iterate through the current middles
            # to see if we're below any of them or any of them are below us.
            
            to_delete: list[Type] = []
            
            for m in middles:
                if middle._conversion_to(m) is not SpecialValueConverter.NO_CONVERSION:
                    # We already know how to get past this middle, so we can ignore it.
                    return
                if m._conversion_to(middle) is not SpecialValueConverter.NO_CONVERSION:
                    # We can use this middle to go past the other, so we
                    # flag the other to be deleted.  We can't actually
                    # delete while we're iterating.
                    to_delete.append(m)
                    
            for m in to_delete:
                del middles[m]
                
            middles[middle] = c
            
        candidates = {*self._conversions.keys(), *self.direct_supers}
        for c in candidates:
            check_and_add(c)
            
        if middles:
            # At this point, middles contains all of the best ways to get to
            # the target type.  If there's more than one path, we warn, but
            # only once per pair.
            
            pairs = [*middles.items()]
            logger.info(f"Converting {self} to {other} through {pairs[0][0]}")

            if len(pairs) > 1:
                # This warning will only happen once, because we cache the result.
                options = [p[0] for p in pairs]
                logger.warning(f"Can convert from {self} to {other} through {conj_str(options)}.  Using {options[0]}.")
                
            return pairs[0][1]

        if other in self.all_supers:
        
            # There's no way to get there.  But it's a supertype, so there should
            # be.  We print out a warning and assume that we can just pass the
            # value.
            logger.warning(f"No conversion from {self} to super-type {other}.  Assuming value is compatible.")
            return SpecialValueConverter.IDENTITY
        
        
        # There's no way to get there, and that's okay.
        return SpecialValueConverter.NO_CONVERSION
          
    
    def _conversion_to(self, other: Type) -> _Converter:
        # Called with _class_lock locked
        vc = self._conversions.get(other, None)

        if vc is None:
            # logger.info(f"--> Looking for conversion from {self} to {other}")
            vc = self._find_conversion_to(other)
            # desc = ("ident" if vc is SpecialValueConverter.IDENTITY
            #         else "none" if vc is SpecialValueConverter.NO_CONVERSION
            #         else "complex")
            # logger.info(f"<-- Conversion from {self} to {other}: {desc}")
            self._conversions[other] = vc
        return vc
            
    def converter_to(self, other: Type) -> Optional[ValueConverter]:
        # Nobody gets to change add converters or reps while we're looking
        with self._class_lock:
            vc = self._conversion_to(other)
            if vc is SpecialValueConverter.IDENTITY:
                return lambda v: v
            if vc is SpecialValueConverter.NO_CONVERSION:
                return None
            return vc

    _known_bounds: Final = dict[tuple['Type',...], Sequence['Type']]()
        
    @classmethod
    def upper_bounds(cls, *types: Type) -> Sequence[Type]:
        maybe = any(isinstance(t, MaybeType) for t in types)
        if maybe:
            type_set = set(t.if_there_type if isinstance(t, MaybeType) else t for t in types)
        else:
            type_set = set(types)
        if len(type_set) == 1:
            return (types[0].maybe,) if maybe else (types[0],)
        if len(type_set) == 0:
            return ()

        key = tuple(type_set)
        bounds = cls._known_bounds.get(key, None)
        
        if bounds is None:
            with cls._class_lock:
                candidates = {key[0], *key[0].all_supers}
                candidates.intersection_update(*({t, *t.all_supers} for t in key[1:]))            
                
                remove = set[Type]()
                for c1 in candidates:
                    for c2 in candidates:
                        if c1 < c2:
                            remove.add(c2)
                candidates -= remove
                if maybe:
                    bounds = tuple(c.maybe for c in candidates)
                else:
                    bounds = tuple(candidates)
                cls._known_bounds[key] = bounds
        return bounds
    
    @classmethod
    def upper_bound(cls, *types: Type) -> Type:
        bounds = cls.upper_bounds(*types)
        return Type.NONE if len(bounds) == 0 else bounds[0]
    
    @classmethod
    def register_conversion(cls, have: Type, want: Type, converter: Optional[ValueConverter]) -> None:
        with cls._class_lock:
            have._conversions[want] = SpecialValueConverter.NO_CONVERSION if converter is None else converter 
        
    # @classmethod
    # def value_compatible(cls, have: Union[Type, Sequence[Type]], want: Union[Type, Sequence[Type]]) -> None:
    #     if isinstance(have, Type):
    #         have = (have,)
    #     if isinstance(want, Type):
    #         want = (want,)
    #     cls.compatible |= {(h,w) for h in have for w in want}
        
    def convert_to(self, want: Type, val: Any) -> Any:
        if self is want or self is Type.ANY:
            return val
        converter = self.converter_to(want)
        if converter is None:
            raise TypeMismatchError(self, want)
        return converter(val)
    
    def can_convert_to(self, want: Type) -> bool:
        if self is want or want is Type.ANY:
            return True
        return self._conversion_to(want) is not SpecialValueConverter.NO_CONVERSION
    

Type.ANY = Type("ANY", is_root = True)
Type.NONE = Type("NONE")
Type.IGNORE = Type("IGNORE")
Type.ERROR = Type("ERROR")
Type.WELL = Type("WELL")
Type.NUMBER = Type("NUMBER")
Type.FLOAT = Type("FLOAT", [Type.NUMBER])
Type.INT = Type("INT", [Type.FLOAT, Type.NUMBER])
Type.BINARY_CPT = Type("BINARY_CPT")
Type.BINARY_STATE = Type("BINARY_STATE")
Type.PAD = Type("PAD", [Type.BINARY_CPT])
Type.WELL_PAD = Type("WELL_PAD", [Type.BINARY_CPT])
Type.WELL_GATE = Type("WELL_GATE", [Type.WELL_PAD])
Type.DROP = Type("DROP", [Type.PAD])
Type.ORIENTED_DROP = Type("ORIENTED_DROP", [Type.DROP])
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
Type.TEMP_CONTROL = Type("TEMP_CONTROL", [Type.BINARY_CPT])
Type.HEATER = Type("HEATER", [Type.TEMP_CONTROL])
Type.CHILLER = Type("CHILLER", [Type.TEMP_CONTROL])
Type.MAGNET = Type("MAGNET", [Type.BINARY_CPT])
Type.BOARD = Type("BOARD")
Type.POWER_SUPPLY = Type("POWER_SUPPLY", [Type.BINARY_CPT])
Type.VOLTAGE = Type("VOLTAGE")
Type.POWER_MODE = Type("POWER_MODE")
Type.FAN = Type("FAN", [Type.BINARY_CPT])

class MaybeType(Type):
    if_there_type: Final[Type]
    
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
    

class Signature:
    param_types: Final[tuple[Type,...]]
    return_type: Final[Type]
    arity: Final[int]
    _known: ClassVar[dict[tuple[tuple[Type,...], Type], Signature]] = {}
    
    
    def __init__(self, param_types: tuple[Type, ...], return_type: Type) -> None:
        self.param_types = param_types
        self.return_type = return_type
        self.arity = len(param_types)
    
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
        ptypes = self.param_types
        pdesc = "()" if self.arity == 0 else ' x '.join(t.name for t in ptypes)
        return f"{pdesc} -> {self.return_type}"
    
    def __hash__(self) -> int:
        return id(self)
    
    def __eq__(self, rhs: object) -> bool:
        return self is rhs
    
    def callable_using(self, arg_types: Sequence[Type]) -> bool:
        return (len(arg_types) == self.arity
                and all(theirs <= mine 
                        for mine,theirs in zip(self.param_types, arg_types)))
        
    def covariant_to(self, other: Signature) -> bool:
        params_ok = self.callable_using(other.param_types)
        their_return = other.return_type
        return_ok = their_return is Type.NONE or self.return_type <= their_return
        return params_ok and return_ok
    
    def narrower_than(self, other: Signature) -> bool:
        if self.arity != other.arity:
            return False
        val = False
        for mine,theirs in zip(self.param_types, other.param_types):
            if theirs < mine:
                # They have a narrower parameter, so we're not narrower.
                return False
            if mine < theirs:
                # We have a narrower parameter, so we might be 
                val = True
            elif mine is not theirs:
                # If neither one is narrower and they're not the same, they're
                # incompatible, so we're not narrower.
                return False
        # if val is False, the params are identical.  In that case, I'm narrower
        # if I return something narrower.  In the case where I take narrower
        # params, I treat myself as narrower regardless of the return type.
        return val or self.return_type < other.return_type
            
        
    
    def _converter_to(self, other: Signature) -> _Converter:
        if self is other:
            return SpecialValueConverter.IDENTITY
        if self.arity != other.arity:
            return SpecialValueConverter.NO_CONVERSION
        cv_return = self.return_type._conversion_to(other.return_type)
        if cv_return is SpecialValueConverter.NO_CONVERSION:
            return SpecialValueConverter.NO_CONVERSION
        cv_params = tuple(theirs._conversion_to(mine)
                          for mine,theirs in zip(self.param_types, other.param_types))
        if SpecialValueConverter.NO_CONVERSION in cv_params:
            return SpecialValueConverter.NO_CONVERSION
        if (cv_return is SpecialValueConverter.IDENTITY
            and all(cv is SpecialValueConverter.IDENTITY for cv in cv_params)):
            return SpecialValueConverter.IDENTITY
        # At least something has to convert.
        def converter(cv: _Converter) -> ValueConverter:
            assert cv is not SpecialValueConverter.NO_CONVERSION
            return (lambda v: v) if cv is SpecialValueConverter.IDENTITY else cv
        param_converters = tuple(converter(cv) for cv in cv_params)
        result_converter = converter(cv_return)
        def convert(fn: CallableValue) -> ConvertedCallableValue:
            return ConvertedCallableValue(fn, other, param_converters, result_converter)
        return convert


class CallableTypeKind(Enum):
    GENERAL = auto()
    ACTION = auto()
    MONITOR = auto()
    TRANSFORM = auto()
    
    @classmethod
    def for_sig(cls, sig: Signature) -> CallableTypeKind:
        n_args = sig.arity
        if sig.return_type is Type.NONE:
            if n_args == 0:
                return CallableTypeKind.ACTION
            elif n_args == 1:
                return CallableTypeKind.MONITOR
        return CallableTypeKind.TRANSFORM if n_args == 1 else CallableTypeKind.GENERAL
    
class CallableValue(ABC):
    sig: Final[Signature]
    
    def __init__(self, sig: Signature) -> None:
        self.sig = sig
    
    @abstractmethod
    def apply(self, args: Sequence[Any]) -> Delayed[Any]: ... # @UnusedVariable
    
    def check_arity(self, args: Sequence[Any]) -> None:
        want = self.sig.arity
        got = len(args)
        assert want == got, f"Functional object expected {qstr(want, 'argument')}, got {got}., "
    
class ConvertedCallableValue(CallableValue):
    cv: Final[CallableValue]
    param_converters: Final[Sequence[ValueConverter]]
    
    def __init__(self, cv: CallableValue, sig: Signature,
                 param_converters: Sequence[ValueConverter],
                 result_converter: ValueConverter) -> None:
        super().__init__(sig)
        self.cv = cv
        self.param_converters = param_converters
        self.result_converter: Final[ValueConverter] = result_converter
        
    def apply(self, args: Sequence[Any]) -> Delayed[Any]:
        converted_args = [fn(a) for fn,a in zip(self.param_converters, args)]
        future = self.cv.apply(converted_args)
        return future.transformed(self.result_converter)

class CallableType(Type):
    instances = dict[Signature, 'CallableType']()
    
    sig: Final[Signature]
    with_self_sig: Final[Signature]
    
    @property
    def param_types(self) -> Sequence[Type]:
        return self.sig.param_types
    
    @property
    def return_type(self) -> Type:
        return self.sig.return_type
    
    @cached_property
    def kind(self) -> CallableTypeKind:
        return CallableTypeKind.for_sig(self.sig)
    
    def __init__(self,
                 name: str,  
                 param_types: Sequence[Type],
                 return_type: Type,
                 *,
                 supers: Optional[Sequence[Type]] = None,
                 rep_types: TypeRepSpec=(CallableValue,)):
        super().__init__(name, supers, as_func_type = self, rep_types = rep_types)
        self.sig = Signature.of(param_types, return_type)
        self.with_self_sig = Signature.of((self, *param_types), return_type)
        
    def set_rep_type(self, rep_types:TypeRepSpec)->None:
        rep_types = _trs_to_tuple(rep_types)
        non_cv_types = [t for t in rep_types if not issubclass(t, CallableValue)]
        if non_cv_types:
            logger.error(f"set_rep_type({self}, ...) has types not derived from CallableValue, ignoring {conj_str(non_cv_types)}.")
            rep_types = tuple(t for t in rep_types if issubclass(t, CallableValue))
        if len(rep_types) == 0:
            rep_types = (CallableValue,)
        super().set_rep_type(rep_types)
        
    def _rep_compatible(self, other: Type) -> bool:
        # For CallableTypes, not only do the rep types have to be type-
        # compatible for Python, but if the other is a CallableType, the
        # signatures need to match.
        if not super()._rep_compatible(other):
            return False
        if isinstance(other, CallableType):
            return self.sig is other.sig
        return True
        
    @classmethod
    def find(cls, param_types: Sequence[Type], return_type: Type, *, name: Optional[str] = None) -> CallableType:
        sig = Signature.of(param_types, return_type)
        ct = cls.instances.get(sig, None)
        if ct is None:
            if name is None:
                name = f"Macro[({','.join(t.name for t in param_types)}),{return_type.name}]"
            ct = CallableType(name, param_types, return_type)
            cls.instances[sig] = ct
        return ct
    
    def _find_conversion_to(self, other: Type) -> _Converter:
        # If we can find a conversion by normal means, we use it
        cv = super()._find_conversion_to(other)
        if cv is SpecialValueConverter.NO_CONVERSION:
            # If not and the the other is a CallableType that can use a (straight)
            # CallableValue, we try to create a converter.
            if isinstance(other, CallableType) and CallableValue in other.rep_types:
                cv = self.sig._converter_to(other.sig)
        return cv
    
    # # I'm not sure if it's really correct to put this here, but
    # # it will probably do the right thing.
    # def __lt__(self, rhs:Type)->bool:
    #     if isinstance(rhs, CallableType):
    #         return self.sig.narrower_than(rhs.sig)
    #     return Type.__lt__(self, rhs)
    
    # def __eq__(self, rhs:object)->bool:
    #     if isinstance(rhs, MacroType):
    #         return self.sig == rhs.sig
    #     return CallableType.__eq__(self, rhs)
    
    def __hash__(self)->int:
        return hash(self.sig)
    
Type.ACTION = CallableType.find((), Type.NONE, name="Action")        


class MotionType(CallableType):
    def __init__(self, name: str = "MOTION", *,
                 supers: Optional[Sequence[Type]] = None) -> None:
        super().__init__(name, (Type.DROP,), Type.DROP, supers=supers)
        
Type.MOTION = MotionType()


class DeltaType(MotionType):
    def __init__(self) -> None:
        super().__init__("DELTA", supers=(Type.MOTION,))

Type.DELTA = DeltaType()
Type.DIR = Type("DIR", [Type.DELTA])
Type.ORIENTED_DIR = Type("ORIENTED_DIR", [Type.DIR])

class TwiddleOpType(CallableType):
    def __init__(self) -> None:
        super().__init__("TWIDDLE_OP", (Type.BINARY_CPT,), Type.NONE)
        
Type.TWIDDLE_OP = TwiddleOpType()
Type.ON = Type("ON", [Type.BINARY_STATE, Type.TWIDDLE_OP])
Type.OFF = Type("OFF", [Type.BINARY_STATE, Type.TWIDDLE_OP])


# class CompositionType(CallableType):
#     instances = dict[tuple[bool, Signature], 'CompositionType']()
#
#     def __init__(self, 
#                  param_types: Sequence[Type],
#                  return_type: Type):
#         kind = "ComposedAction" if is_action else "Composition"
#         super().__init__(f"{kind}[({','.join(t.name for t in param_types)}),{return_type.name}]", 
#                          param_types, return_type)
#
#     @classmethod
#     def find(cls, param_types: Sequence[Type], return_type: Type, *, is_action: bool) -> CompositionType:
#         sig = Signature.of(param_types, return_type)
#         mt = cls.instances.get((is_action, sig), None)
#         if mt is None:
#             mt = CompositionType(param_types, return_type, is_action=is_action)
#             cls.instances[(is_action, sig)] = mt
#         return mt

# class MacroType(CallableType):
#     instances = dict[Signature, 'MacroType']()
#
#     def __init__(self, 
#                  param_types: Sequence[Type],
#                  return_type: Type):
#         super().__init__(f"Macro[({','.join(t.name for t in param_types)}),{return_type.name}]", 
#                          param_types, return_type)
#
#     @classmethod
#     def find(cls, param_types: Sequence[Type], return_type: Type) -> MacroType:
#         sig = Signature.of(param_types, return_type)
#         mt = cls.instances.get(sig, None)
#         if mt is None:
#             mt = MacroType(param_types, return_type)
#             cls.instances[sig] = mt
#         return mt
#
#     # I'm not sure if it's really correct to put this here, but
#     # it will probably do the right thing.
#     def __lt__(self, rhs:Type)->bool:
#         if isinstance(rhs, MacroType):
#             return self.sig.narrower_than(rhs.sig)
#         return Type.__lt__(self, rhs)
#
#     # def __eq__(self, rhs:object)->bool:
#     #     if isinstance(rhs, MacroType):
#     #         return self.sig == rhs.sig
#     #     return CallableType.__eq__(self, rhs)
#
#     def __hash__(self)->int:
#         return hash(self.sig)
    

class Func:
    Definition = Callable[..., Delayed]
    TypeExprFormatter = Callable[..., Optional[str]]
    name: Final[str]
    # verb: Final[str]
    overloads: Final[dict[tuple[Type,...], tuple[Signature,Definition]]]
    type_expr_formatters: Final[dict[Optional[int], list[TypeExprFormatter]]]
    
    def __init__(self, name: str, 
                 # *,
                 # verb: Optional[str] = None,
                 # error_msg_factory: Optional[Callable[[Sequence[Type], str], Optional[str]]] = None,
                 ) -> None:
        self.name = name
        # self.verb = verb or name.lower()
        self.overloads = {}
        # self.error_msg_factory = error_msg_factory
        self.type_expr_formatters = defaultdict(list)
        
    def __repr__(self) -> str:
        return f"Func.{self.name}"
    
    @property
    def known_sigs(self) -> Sequence[Signature]:
        return tuple(p[0] for p in self.overloads.values())

    def register(self, param_types: Sequence[Type], return_type: Type, definition: Definition) -> Func:
        sig = Signature.of(param_types, return_type)
        self.overloads[sig.param_types] = (sig,definition)
        return self
        
    def register_immediate(self, param_types: Sequence[Type], return_type: Type, definition: Callable[..., Any]) -> Func:
        def fn(*args: Sequence[Any]) -> Delayed:
            return Delayed.complete(definition(*args))
        return self.register(param_types, return_type, fn)
        
    def register_all(self, sigs: Sequence[Union[Signature, tuple[Sequence[Type], Type]]],
                     definition: Definition) -> Func:
        for sig in sigs:
            if isinstance(sig, Signature):
                param_types: Sequence[Type] = sig.param_types
                return_type = sig.return_type
            else:
                param_types, return_type = sig
            self.register(param_types, return_type, definition)
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
        
    def __getitem__(self, arg_types: Sequence[Type]) -> Optional[tuple[Signature, Func.Definition]]:
        d = self.overloads
        best: Optional[tuple[Signature, Func.Definition]] = None
        for sig, defn in d.values():
            if sig.callable_using(arg_types) and (best is None or sig.narrower_than(best[0])):
                best = (sig,defn)
        return best
    
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
        sigs = [sig for sig,_ in self.overloads.values()]
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
        for sig,_ in self.overloads.values():
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
    func: Final[Func]

    def __init__(self, value: Union[str, Func]) -> None:
        if isinstance(value, str):
            value = Func(value)
        self.func = value
        
    def __repr__(self) -> str:
        return f"Attr.{self.func.name}"
    
    @property
    def applies_to(self) -> Sequence[Type]:
        return [sig.param_types[0] for sig in self.func.known_sigs if sig.arity == 1]
    
    @property
    def returns(self) -> Sequence[Type]:
        return [sig.return_type for sig in self.func.known_sigs if sig.arity == 1]
    
    def register_setter(self, otype: Union[Type, Sequence[Type]], vtype: Type, 
                        setter: Callable[[Any,Any], Any]) -> None:
        if isinstance(otype, Type):
            self.func.register_immediate((otype, vtype), Type.NONE, setter)
        else:
            for ot in otype:
                self.func.register_immediate((ot, vtype), Type.NONE, setter)
                 
    
    def register(self, otype: Union[Type,Sequence[Type]], rtype: Type, extractor: Callable[[Any], Any],
                 *,
                 setter: Optional[Callable[[Any,Any], Any]] = None) -> None:
        if isinstance(otype, Type):
            self.func.register_immediate((otype,), rtype, extractor)
        else:
            for ot in otype:
                self.func.register_immediate((ot,), rtype, extractor)
        if setter is not None:
            self.register_setter(otype, rtype, setter)
                    
    def getter(self, otype: Type) -> Optional[tuple[Signature, Callable[..., Delayed]]]:
        return self.func[(otype,)]
        
    def setter(self, otype: Type, vtype: Type) -> Optional[tuple[Signature, Callable[..., Delayed]]]:
        return self.func[(otype, vtype)]
    
    # def __getitem__(self, otype: Type) -> Optional[tuple[Signature, Callable[..., Delayed]]]:
        # return self.getter(otype)
    
    def accepts_for(self, otype: Type) -> Sequence[Type]:
        return [sig.param_types[1] for sig in self.func.known_sigs 
                    if sig.arity == 2 and sig.param_types[0] is otype]
        
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
    
    def test(self, x: Any, y: Any) -> bool:
        fn = self._known[self]
        res = fn(x, y)
        assert isinstance(res, bool)
        return res
    
    def comparable_type(self, lhs: Type, rhs: Type) -> Optional[Type]:
        candidates = (lhs,) if lhs is rhs else Type.upper_bounds(lhs, rhs)
        if len(candidates) < 1:
            return None
        if self is Rel.EQ or self is Rel.NE:
            return candidates[0]
        ok_types = (Type.INT, Type.FLOAT, Type.TIME, Type.TICKS, Type.VOLUME, 
                    Type.ABS_TEMP, Type.REL_TEMP, Type.VOLTAGE)
        for t in candidates:
            for ok in ok_types:
                if t <= ok:
                    return ok
        return None
        
    
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
    CHILLER = auto()
    TEMP_CONTROL = auto()
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
    
    



