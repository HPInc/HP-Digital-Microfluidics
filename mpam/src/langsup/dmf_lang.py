from __future__ import annotations

from _collections import defaultdict
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic, Hashable, NamedTuple, Final, \
    Callable, Any, cast, Sequence, Union, Mapping, ClassVar, List, Tuple,\
    TYPE_CHECKING
import typing

from antlr4 import InputStream, CommonTokenStream, FileStream, ParserRuleContext, \
    Token
from antlr4.tree.Tree import TerminalNode

from DMFLexer import DMFLexer
from DMFParser import DMFParser
from DMFVisitor import DMFVisitor
from langsup.type_supp import Type, CallableType, MacroType, Signature, Attr,\
    Rel, MaybeType, Func, CompositionType, PhysUnit, EnvRelativeUnit
from mpam.device import Pad, Board, BinaryComponent, Well,\
    WellGate, WellPad
from mpam.drop import Drop, DropStatus
from mpam.paths import Path
from mpam.types import unknown_reagent, Liquid, Dir, Delayed, OnOff, Barrier, \
    Ticks, DelayType, Turn, Reagent, Mixture, Postable
from quantities.core import Unit, Dimensionality
from quantities.dimensions import Time, Volume
from erk.stringutils import map_str, conj_str
import math
from functools import reduce
from erk.basic import LazyPattern, not_None
from re import Match

if TYPE_CHECKING:
    from mpam.monitor import BoardMonitor


Name_ = TypeVar("Name_", bound=Hashable)
Val_ = TypeVar("Val_")

class EvaluationError(RuntimeError): ...

class CompilationError(RuntimeError): ...

class MaybeNotSatisfiedError(EvaluationError): ...

class AlreadyDropError(EvaluationError): ...
        
class UnknownUnitDimensionError(CompilationError):
    unit: Final[Unit]
    dimensionality: Final[Dimensionality]
    
    def __init__(self, unit: Unit) -> None:
        dim = unit.dimensionality()
        super().__init__(f"Unit {unit} has unknown dimensionality {dim}")
        self.unit = unit
        self.dimensionality = dim

class Scope(Generic[Name_, Val_]):
    parent: Optional[Scope[Name_,Val_]]
    mapping: dict[Name_, Val_]
    
    @property
    def is_top_level(self) -> bool:
        return self.parent is None
    
    def __init__(self, parent: Optional[Scope[Name_, Val_]], 
                 *, 
                 initial: Optional[dict[Name_,Val_]] = None) -> None:
        self.parent = parent
        self.mapping = initial if initial is not None else {}
        
    def new_child(self, initial: Optional[dict[Name_,Val_]] = None) -> Scope[Name_,Val_]:
        return Scope(parent=self, initial=initial)
    
    def find_scope(self, name: Name_) -> Optional[Scope[Name_,Val_]]:
        if name in self.mapping:
            return self
        parent = self.parent
        return None if parent is None else parent.find_scope(name)
    
    def lookup(self, name: Name_) -> Optional[Val_]:
        scope = self.find_scope(name)
        return None if scope is None else scope.mapping[name]
    
    def define(self, name: Name_, val: Val_) -> None:
        self.mapping[name] = val
        
    def defined_locally(self, name: Name_) -> bool:
        return name in self.mapping
    
    def __getitem__(self, name: Name_) -> Val_:
        val = self.lookup(name)
        if val is None:
            scope: Optional[Scope[Name_, Val_]] = self
            defined: List[Sequence[Name_]] = []
            while scope is not None:
                defined.append(tuple(scope.mapping.keys()))
                scope = scope.parent
            raise KeyError(f"'{name}' is undefined.  Defined: {defined}")
        return val
    
    def __setitem__(self, name: Name_, val: Val_) -> None:
        scope = self.find_scope(name)
        if scope is None:
            scope = self
        scope.mapping[name] = val
        
class ScopeStack(Generic[Name_, Val_]):
    current: Scope[Name_, Val_]
    
    @property
    def is_top_level(self) -> bool:
        return self.current.is_top_level
    
    def __init__(self,
                 initial: Optional[Scope[Name_,Val_]] = None):
        self.current = Scope(None) if initial is None else initial
        
    def lookup(self, name: Name_) -> Optional[Val_]:
        return self.current.lookup(name)
    
    def define(self, name: Name_, val: Val_) -> None:
        return self.current.define(name, val)
    
    def defined_locally(self, name: Name_) -> bool:
        return self.current.defined_locally(name)
    
    def __getitem__(self, name: Name_) -> Val_:
        return self.current[name]
    
    def __setitem__(self, name: Name_, val: Val_) -> None:
        self.current[name] = val
        
    def push(self, initial: Optional[dict[Name_,Val_]] = None):
        return StackPush(self, initial)

class StackPush(Generic[Name_, Val_]):
    stack: ScopeStack[Name_, Val_]
    scope: Scope[Name_, Val_]
    old: Scope[Name_, Val_]
    def __init__(self, stack: ScopeStack[Name_, Val_], initial: Optional[dict[Name_,Val_]] = None) -> None:
        self.stack = stack
        self.scope = stack.current.new_child(initial)
        
    def __enter__(self) -> StackPush[Name_, Val_]:
        stack = self.stack
        self.old = stack.current
        stack.current = self.scope
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: # @UnusedVariable
        self.stack.current = self.old

class Value(NamedTuple):
    val_type: Type
    value: object
        
        
class Environment(Scope[str, Any]):
    board: Final[Board]
    
    @property
    def monitor(self) -> Optional[BoardMonitor]:
        system = self.board.system
        if system is None:
            return None
        return system.monitor
    
    def __init__(self, parent: Optional[Scope[str, Any]], 
                 *,
                 board: Board, 
                 initial: Optional[dict[str, Any]] = None) -> None:
        super().__init__(parent, initial=initial)
        self.board = board
    def new_child(self, initial: Optional[dict[str,Any]] = None) -> Environment:
        return Environment(parent=self, board=self.board, initial=initial)
    
    
TypeMap = Scope[str, Type]

class CallableValue(ABC):
    sig: Final[Signature]
    
    def __init__(self, sig: Signature) -> None:
        self.sig = sig
    
    @abstractmethod
    def apply(self, args: Sequence[Any]) -> Delayed[Any]: ... # @UnusedVariable
    
    
class ComposedCallable(CallableValue):
    first: Final[CallableValue]
    second: Final[CallableValue]
    pass_first_arg: Final[bool]
    
    def __init__(self, 
                 ct: CompositionType,
                 first: CallableValue, 
                 second: CallableValue, 
                 pass_first_arg: bool) -> None:
        super().__init__(ct.sig)
        self.first=first
        self.second=second
        self.pass_first_arg = pass_first_arg
        
    
    def apply(self, args:Sequence[Any])->Delayed[Any]:
        return (self.first.apply(args)
                    .chain(lambda v: self.second.apply((args[0] if self.pass_first_arg else v,))))
    
    
        
    def __str__(self) -> str:
        return f"({self.first} : {self.second})"
    
class MotionValue(CallableValue):
    @abstractmethod
    def move(self, drop: Drop) -> Delayed[Drop]: ... # @UnusedVariable
    
    _sig: ClassVar[Signature] = Signature.of((Type.DROP,), Type.DROP)
    
    def __init__(self) -> None:
        super().__init__(self._sig)
    
    def apply(self, args:Sequence[Any])->Delayed[Drop]:
        assert len(args) == 1
        drop = args[0]
        assert isinstance(drop, Drop)
        return self.move(drop)
        
    
class DeltaValue(MotionValue):
    dist: Final[int]
    direction: Final[Dir]
    
    def __init__(self, dist: int, direction: Dir) -> None:
        self.dist = dist
        self.direction = direction
        
    def __str__(self) -> str:
        return f"Delta({self.dist}, {self.direction})"
        
    def move(self, drop:Drop)->Delayed[Drop]:
        path = Path.walk(self.direction, steps = self.dist)
        return path.schedule_for(drop)
    
    def turned(self, turn: Turn) -> DeltaValue:
        return DeltaValue(self.dist, self.direction.turned(turn))
    
    def __eq__(self, rhs: object) -> bool:
        if rhs is self:
            return True
        if not isinstance(rhs, DeltaValue):
            return False
        return self.dist == rhs.dist and self.direction is rhs.direction
    
    def __hash__(self) -> int:
        return hash((self.dist, self.direction))
        
    
class UnsafeWalkValue(MotionValue):
    delta: Final[DeltaValue]
    
    def __init__(self, delta: DeltaValue) -> None:
        self.delta = delta
    
    def __str__(self) -> str:
        return f"UnsafeWalk({self.delta.dist}, {self.delta.direction})"
    
    def move(self, drop:Drop)->Delayed[Drop]:
        delta = self.delta
        path = Path.walk(delta.direction, steps = delta.dist, allow_unsafe = True)
        return path.schedule_for(drop)
    
    
    
class RemoveDropValue(MotionValue):
    def move(self, drop:Drop)->Delayed[Drop]:
        if drop.status is not DropStatus.ON_BOARD:
            print(f"{drop} is not on board.  Cannot remove")
        else:
            if drop.status is DropStatus.ON_BOARD:
                drop.pad.drop = None
            drop.status = DropStatus.OFF_BOARD
        return Delayed.complete(drop)
    
class ToPadValue(MotionValue):
    dest: Final[Pad]
    
    def __init__(self, pad: Pad) -> None:
        self.dest = pad
        
    def move(self, drop:Drop)->Delayed[Drop]:
        path = Path.to_pad(self.dest)
        return path.schedule_for(drop)

class ToRowColValue(MotionValue):
    dest: Final[int]
    verticalp: Final[bool]
    
    def __init__(self, dest: int, verticalp: bool) -> None:
        self.dest = dest
        self.verticalp = verticalp
        
    def move(self, drop:Drop)->Delayed[Drop]:
        if self.verticalp:
            path = Path.to_row(self.dest)
        else:
            path = Path.to_col(self.dest)
        return path.schedule_for(drop)
    
class TwiddlePadValue(CallableValue):
    op: Final[BinaryComponent.ModifyState]
    
    ON: ClassVar[TwiddlePadValue]
    OFF: ClassVar[TwiddlePadValue]
    TOGGLE: ClassVar[TwiddlePadValue]
    
    _sig: ClassVar[Signature] = Signature.of((Type.BINARY_CPT,), Type.BINARY_STATE)
    
    def __init__(self, op: BinaryComponent.ModifyState) -> None:
        super().__init__(self._sig)
        self.op = op
        
    def apply(self, args:Sequence[Any])->Delayed[OnOff]: 
        assert len(args) == 1
        bc = args[0]
        assert isinstance(bc, BinaryComponent)
        return self.op.schedule_for(bc)
    

TwiddlePadValue.ON = TwiddlePadValue(BinaryComponent.TurnOn)
TwiddlePadValue.OFF= TwiddlePadValue(BinaryComponent.TurnOff)
TwiddlePadValue.TOGGLE = TwiddlePadValue(BinaryComponent.Toggle)
    
class PauseValue(CallableValue):
    duration: Final[DelayType]
    board: Final[Board]
    
    _sig: ClassVar[Signature] = Signature.of((Type.DELAY,), Type.NONE)
    
    def __init__(self, duration: DelayType, board: Board) -> None:
        super().__init__(self._sig)
        self.duration = duration
        self.board = board
        
    def __str__(self) -> str:
        return f"Pause({self.duration})"
        
    def apply(self, args: Sequence[Any])->Delayed[None]:
        assert len(args) == 1
        return self.board.delayed(lambda : None, after=self.duration)
    
    

class MacroValue(CallableValue):
    param_names: Final[Sequence[str]]
    body: Final[Executable]
    static_env: Final[Environment]
    
    def __init__(self, mt: MacroType, env: Environment, param_names: Sequence[str], body: Executable) -> None:
        super().__init__(mt.sig)
        self.static_env = env
        self.param_names = param_names
        self.body = body
        
    def apply(self, args:Sequence[Any])->Delayed[Any]:
        bindings = dict(zip(self.param_names, args))
        local_env = self.static_env.new_child(bindings)
        return self.body.evaluate(local_env)
    
    def __str__(self) -> str:
        params = ", ".join(f"{n}: {t}" for n,t in zip(self.param_names, self.sig.param_types)) # @UnusedVariable
        return f"macro({params})->{self.sig.return_type}"
    
class WellGateValue(NamedTuple):
    pad: WellGate
    well: Well
    
    def __str__(self) -> str:
        return str(self.pad)
        # if isinstance(pad.loc, Well):
        #     return str(pad)
        # else:
        #     return f"({pad}, {self.well})"
        
class ScaledReagent(NamedTuple):
    mult: float
    reagent: Reagent
    
    def __str__(self) -> str:
        return f"Scaled[{self.mult}, {self.reagent}]"
    
    def mix_with(self, rhs: ScaledReagent) -> Reagent:
        ratio = self.mult/rhs.mult
        return Mixture.find_or_compute(self.reagent, rhs.reagent, ratio=ratio)

K_ = TypeVar("K_")
V_ = TypeVar("V_")
T_ = TypeVar("T_")
class ByNameCache(dict[K_,V_]):
    def __init__(self, factory: Callable[[K_], V_]):
        self.factory = factory
    def __missing__(self, key: K_) -> V_:
        ret: V_ = self.factory(key)
        self[key] = ret
        return ret

Functions = ByNameCache[str, Func](lambda name: Func(name))
Attributes = ByNameCache[str, Attr](lambda name: Attr(Functions[f"{name} attribute"]))

ERUnitLookup: dict[EnvRelativeUnit, tuple[Type, Type, Callable[[Environment], Unit]]] = {
        EnvRelativeUnit.DROP: (Type.VOLUME, Type.FLOAT, lambda env: env.board.drop_unit),
    } 

def unit_adaptor(unit: PhysUnit,
                 op_name: str, 
                 types_fn: Callable[[Type, Type], tuple[Sequence[Type], Type]],
                 fn: Callable[[Unit], Callable[[Any], Any]]) -> Func:
    func = Func(str(unit))
    func.postfix_op(op_name)
    
    if isinstance(unit, EnvRelativeUnit):
        qtype, ntype, unit_finder = ERUnitLookup[unit]
        arg_types, ret_type = types_fn(qtype, ntype)
        func.register(arg_types, ret_type, WithEnv(lambda env, n: fn(unit_finder(env))(n)))
    else:
        dim = unit.dimensionality()
        try:
            qtype, ntype = DimensionToType[dim]
        except KeyError:
            raise UnknownUnitDimensionError(unit)
        arg_types, ret_type = types_fn(qtype, ntype)
        func.register_immediate(arg_types, ret_type, fn(unit))
    return func

def unit_func(unit: PhysUnit) -> Func:
    return unit_adaptor(unit, str(unit), 
                        lambda qt,nt: ((nt,), qt),
                        lambda unit: lambda n: n*unit)

UnitFuncs = ByNameCache[PhysUnit, Func](unit_func)

def unit_mag_func(unit: PhysUnit) -> Func:
    return unit_adaptor(unit, f"'s magnitude in {unit}",
                        lambda qt,nt: ((qt,), Type.FLOAT), # @UnusedVariable
                        lambda unit: lambda d: d.as_number(unit))

UnitMagFuncs = ByNameCache[PhysUnit, Func](unit_mag_func)

def unit_string_func(unit: PhysUnit) -> Func:
    return unit_adaptor(unit, f"as string in {unit}",
                        lambda qt,nt: ((qt,), Type.STRING), # @UnusedVariable
                        lambda unit: lambda d: f"{d.in_units(unit):g}") 

UnitStringFuncs = ByNameCache[PhysUnit, Func](unit_string_func)

Attributes["gate"].register(Type.WELL, Type.WELL_GATE, lambda well: well.gate)
Attributes["#exit_pad"].register(Type.WELL, Type.PAD, lambda well: well.exit_pad)
Attributes["state"].register(Type.BINARY_CPT, Type.BINARY_STATE, lambda cpt: cpt.current_state)
Attributes["distance"].register(Type.DELTA, Type.INT, lambda delta: delta.dist)
Attributes["direction"].register(Type.DELTA, Type.DIR, lambda delta: delta.direction)
Attributes["duration"].register(Type.PAUSE, Type.DELAY, lambda pause: pause.duration)
def _set_pad(d: Drop, p: Pad):
    d.pad = p
    d.status = DropStatus.ON_BOARD
Attributes["pad"].register(Type.DROP, Type.PAD, lambda drop: drop.pad, setter=_set_pad)
Attributes["row"].register(Type.PAD, Type.INT, lambda pad: pad.row)
Attributes["column"].register(Type.PAD, Type.INT, lambda pad: pad.column)
Attributes["#exit_dir"].register(Type.WELL, Type.DIR, lambda well: well.exit_dir)
Attributes["well"].register(Type.PAD, Type.WELL.maybe, lambda p: p.well)
Attributes["well"].register(Type.WELL_PAD, Type.WELL, lambda wp: wp.well)
Attributes["drop"].register(Type.PAD, Type.DROP.maybe, lambda p: p.drop) 
# Attributes["magnitude"].register((Type.TIME, Type.VOLUME), Type.FLOAT, lambda q: q.magnitude)
Attributes["magnitude"].register(Type.TICKS, Type.INT, lambda q: q.magnitude)
Attributes["length"].register(Type.STRING, Type.INT, lambda s: len(s))
Attributes["number"].register(Type.WELL, Type.INT, lambda w : w.number)

Attributes["volume"].register([Type.LIQUID, Type.WELL], Type.VOLUME, lambda d: d.volume)
Attributes["volume"].register(Type.DROP, Type.VOLUME, lambda d: d.blob_volume)
def _set_drop_volume(d: Drop, v: Volume):
    d.blob_volume = v
Attributes["volume"].register_setter(Type.DROP, Type.VOLUME, _set_drop_volume)
def _set_well_volume(w: Well, v: Volume):
    w.contains(Liquid(w.reagent, v))
Attributes["volume"].register_setter(Type.WELL, Type.VOLUME, _set_well_volume)

Attributes["reagent"].register([Type.DROP, Type.LIQUID, Type.WELL], Type.REAGENT, lambda d: d.reagent)
def _set_drop_reagent(d: Drop, r: Reagent):
    d.reagent= r
Attributes["reagent"].register_setter(Type.DROP, Type.REAGENT, _set_drop_reagent)
def _set_well_reagent(w: Well, r: Reagent):
    w.contains(Liquid(r, w.volume))
Attributes["reagent"].register_setter(Type.WELL, Type.REAGENT, _set_well_reagent)

def _set_drop_liquid(d: Drop, liq: Liquid):
    d.blob_volume = liq.volume
    d.reagent= liq.reagent
Attributes["contents"].register(Type.DROP, Type.LIQUID, lambda d: Liquid(d.reagent, d.volume),
                                setter=_set_drop_liquid)

def _set_well_contents(w: Well, liq: Liquid):
    w.contains(liq)
Attributes["contents"].register(Type.WELL, Type.LIQUID.maybe, lambda w: Liquid(w.reagent, w.volume),
                                setter=_set_well_contents)

Attributes["capacity"].register(Type.WELL, Type.VOLUME, lambda w: w.capacity)
Attributes["#remaining_capacity"].register(Type.WELL, Type.VOLUME, lambda w: w.remaining_capacity)


Functions["ROUND"].register_immediate((Type.FLOAT,), Type.INT, lambda x: round(x))
Functions["FLOOR"].register_immediate((Type.FLOAT,), Type.INT, lambda x: math.floor(x))
Functions["CEILING"].register_immediate((Type.FLOAT,), Type.INT, lambda x: math.ceil(x))
Functions["UNSAFE"].register_immediate((Type.DELTA,), Type.MOTION, lambda d: UnsafeWalkValue(d))
Functions["UNSAFE"].register_immediate((Type.DIR,), Type.MOTION, lambda d: UnsafeWalkValue(DeltaValue(1,d)))
Functions["PRINT"].register_all_immediate([((Type.ANY,) * 10, Type.NONE) for n in range(1, 8)],
                                          print)
Functions["STRING"].register_immediate((Type.ANY,), Type.STRING, str)
# Functions["ON_BOARD"].register_immediate((Type.PAD,), Type.BOOL,
#                                          )

BuiltIns = {
    "ceil": Functions["CEILING"],
    "floor": Functions["FLOOR"],
    "round": Functions["ROUND"],
    "unsafe_walk": Functions["UNSAFE"],
    "on board": Functions["ON_BOARD"],
    # "print": Functions["PRINT"],
    "str": Functions["STRING"],
    "mixture": Functions["MIX"]
    }

class SpecialVariable:
    var_type: Final[Type]
    
    @property
    def is_settable(self) -> bool:
        return self._setter is not None
    
    def __init__(self, var_type: Type, *,
                 getter: Callable[[Environment], Any],
                 setter: Optional[Callable[[Environment, Any], None]] = None) -> None:
        self.var_type = var_type
        self._getter = getter
        self._setter = setter
    
    def get(self, env: Environment) -> Any:
        return (self._getter)(env)
    
    def set(self, env: Environment, val: Any) -> None:
        assert self._setter is not None
        (self._setter)(env, val)
        
class MonitorVariable(SpecialVariable):
    def __init__(self, name: str, var_type: Type, *,
                 getter: Callable[[BoardMonitor], Any],
                 setter: Optional[Callable[[BoardMonitor, Any], None]] = None) -> None:
        def adapted_getter(env: Environment) -> Any:
            monitor = env.monitor
            if monitor is None:
                raise EvaluationError(f"Evaluating {name} only works in a monitored run")
            return getter(monitor)
        
        def adapted_setter(env: Environment, val: Any) -> None:
            monitor = env.monitor
            if monitor is None:
                raise EvaluationError(f"Setting {name} only works in a monitored run")
            assert setter is not None
            setter(monitor, val)
            
        super().__init__(var_type, getter=adapted_getter, setter = setter and adapted_setter)
        
    ...
    
SpecialVars: dict[str, SpecialVariable] = {}
    
DimensionToType: dict[Dimensionality, tuple[Type, Type]] = {
    Time.dim(): (Type.TIME, Type.FLOAT),
    Volume.dim(): (Type.VOLUME, Type.FLOAT),
    Ticks.dim(): (Type.TICKS, Type.INT),
    }

rep_types: Mapping[Type, Union[typing.Type, Tuple[typing.Type,...]]] = {
        Type.DROP: Drop,
        Type.INT: int,
        Type.FLOAT: float,
        Type.NUMBER: (float, int),
        Type.BINARY_STATE: OnOff,
        Type.BINARY_CPT: BinaryComponent,
        Type.PAD: Pad,
        Type.WELL_PAD: WellPad,
        Type.WELL_GATE: WellGate,
        Type.WELL: Well,
        Type.DELTA: DeltaValue,
        Type.MOTION: MotionValue,
        Type.TIME: Time,
        Type.TICKS: Ticks,
        Type.DELAY: (Time, Ticks),
        Type.PAUSE: PauseValue,
        Type.DIR: Dir,
        Type.BOOL: bool,
        Type.BUILT_IN: Func,
        Type.VOLUME: Volume,
        Type.LIQUID: Liquid,
        Type.STRING: str,
        Type.REAGENT: Reagent,
        Type.SCALED_REAGENT: ScaledReagent,
    }

# class Conversions:
#     known: ClassVar[dict[tuple[Type,Type], Callable[[Any], Any]]] = {}
#     known_ok: ClassVar[set[tuple[Type,Type]]] = set()
#
#     @classmethod
#     def register(cls, have: Type, want: Type, converter: Callable[[Any], Any]) -> None:
#         cls.known[(have, want)] = converter
#
#     @classmethod
#     def ok(cls, have: Union[Type, Sequence[Type]], want: Union[Type,Sequence[Type]]) -> None:
#         if isinstance(have, Type):
#             have = (have,)
#         if isinstance(want, Type):
#             want = (want,)
#         cls.known_ok |= {(h,w) for h in have for w in want}
#
#     @classmethod
#     def convert(cls, have: Type, want: Type, val: Any) -> Any:
#         if have is want:
#             return val
#         if want is Type.ANY:
#             return val
#         if want is Type.NONE:
#             return None
#         if isinstance(want, MaybeType):
#             if val is None:
#                 return val
#             elif isinstance(have, MaybeType):
#                 return cls.convert(have.if_there_type, want.if_there_type, val)
#             else:
#                 return cls.convert(have, want.if_there_type, val)
#         if (have,want) in cls.known_ok:
#             return val
#         converter = cls.known.get((have, want), None)
#         if converter is not None:
#             return converter(val)
#         rep = rep_types.get(want, None)
#         if rep is not None and isinstance(val, rep):
#             return val
#         assert False, f"Don't know how to convert from {have} to {want}: {val}"
#
#     @classmethod
#     def can_convert(cls, have: Type, want: Type) -> bool:
#         if have is want or want is Type.ANY or want is Type.NONE:
#             return True
#         key = (have, want)
#         if key in cls.known or key in cls.known_ok:
#             return True
#         if isinstance(want, MaybeType):
#             if isinstance(have, MaybeType):
#                 return cls.can_convert(have.if_there_type, want.if_there_type)
#             else:
#                 return cls.can_convert(have, want.if_there_type)
#         return False

    
Type.value_compatible((Type.TIME, Type.TICKS), Type.DELAY)
Type.value_compatible((Type.INT, Type.FLOAT), Type.NUMBER)

Type.register_conversion(Type.DROP, Type.PAD, lambda drop: drop.pad)
Type.register_conversion(Type.DROP, Type.BINARY_CPT, lambda drop: drop.pad)
Type.register_conversion(Type.INT, Type.FLOAT, float)
Type.register_conversion(Type.REAGENT, Type.SCALED_REAGENT, lambda r: ScaledReagent(1, r))
Type.register_conversion(Type.DIR, Type.DELTA, lambda d: DeltaValue(1, d))
Type.register_conversion(Type.DIR, Type.MOTION, lambda d: DeltaValue(1, d))



class Executable:
    return_type: Final[Type]
    contains_error: Final[bool]
    
    def __init__(self, return_type: Type, func: Callable[[Environment], Delayed[Any]],
                 based_on: Sequence[Executable] = (),
                 *,
                 is_error: bool = False,
                 ) -> None:
        self.return_type = return_type
        self.func: Final[Callable[[Environment], Delayed[Any]]] = func
        self.contains_error = is_error or any(e.contains_error for e in based_on)
        
    @classmethod
    def constant(cls, return_type: Type, val: Any, based_on: Sequence[Executable] = (), *,
                 is_error: bool = False) -> Executable:
        return Executable(return_type, lambda _: Delayed.complete(val), based_on, is_error=is_error)
        
    def __str__(self) -> str:
        e = "ERROR, " if self.contains_error else ""
        return f"Executable({e}{self.return_type}, {self.func}"
    
    
    def evaluate(self, env: Environment, required: Optional[Type] = None) -> Delayed[Any]:
        assert not self.contains_error, f"attempting to evaluate {self}"
        fn = self.func
        future = fn(env)
        if required is not None and required is not self.return_type:
            req_type = required
            def convert(val) -> Any:
                return self.return_type.convert_to(req_type, val=val, rep_types=rep_types)
                # return Conversions.convert(have=self.return_type, want=req_type, val=val)
            future = future.transformed(convert)
        # if required is not None: 
        #     check = rep_types.get(required, None)
        #     if check is not None:
        #         assert isinstance(val, check), f"Expected {check}, got {val}"
        return future
    
class LazyEval:
    Definition = Callable[[Environment, Sequence[Executable]], Delayed[Any]]
    def __init__(self, 
                 func: Definition) -> None:
        self.func = func
    
    def __call__(self, env: Environment, arg_execs: Sequence[Executable]) -> Delayed[Any]:
        fn = self.func
        return fn(env, arg_execs)

class WithEnv:
    def __init__(self, func: Callable):
        self.func = func
    def __call__(self, env: Environment, *args) -> Delayed[Any]:
        return Delayed.complete(self.func(env, *args))    
    
class DMFInterpreter:
    globals: Final[Environment]
    namespace: Final[TypeMap]
    
    def __init__(self, file_name: Optional[str], *, board: Board, encoding: str='ascii', errors: str='strict') -> None:
        self.globals = Environment(None, board=board)
        self.namespace = TypeMap(None)
        if file_name is not None:
            parser = self.get_parser(FileStream(file_name, encoding, errors))
            tree = parser.macro_file()
            assert isinstance(tree, DMFParser.Macro_fileContext)
            compiler = DMFCompiler(global_types = self.namespace, interactive = False)
            executable = compiler.visit(tree)
            assert isinstance(executable, Executable)
            if executable.contains_error:
                print(f"Macro file '{file_name}' contained error, not loading.")
            else:
                executable.evaluate(self.globals).wait()
        
    def set_global(self, name: str, val: Any, vtype: Type):
        self.namespace[name] = vtype
        self.globals[name] = val
        
    def evaluate(self, expr: str, required: Optional[Type] = None, *, 
                 cache_as: Optional[str] = None) -> Delayed[tuple[Type, Any]]:
        parser = self.get_parser(InputStream(expr))
        tree = parser.interactive()
        assert isinstance(tree, DMFParser.InteractiveContext)
        compiler = DMFCompiler(global_types = self.namespace, interactive=True)
        executable = compiler.visit(tree)
        assert isinstance(executable, Executable)
        if executable.contains_error:
            print("Expression contained error, not evaluating.")
            return Delayed.complete((executable.return_type, None))
        future = executable.evaluate(self.globals, required=required)
        if cache_as is not None and executable.return_type is not Type.IGNORE:
            cvar = cache_as
            future.then_call(lambda val: self.set_global(cvar, val, executable.return_type))
        return future.transformed(lambda val: (executable.return_type, val))
    
    def get_parser(self, input_stream: InputStream) -> DMFParser:
        lexer = DMFLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DMFParser(stream)
        return parser
    

class DMFCompiler(DMFVisitor):
    global_types: Final[TypeMap]
    current_types: ScopeStack[str, Type]
    interactive: Final[bool]
    
    default_creators = defaultdict[Type,Callable[[Environment],Any]](lambda: (lambda _: None),
                                                          {Type.INT: lambda _: 0,
                                                           Type.FLOAT: lambda _: 0.0,
                                                           Type.PAD: lambda env: env.board.pad_at(0,0),
                                                           Type.TIME: lambda _: Time.ZERO,
                                                           Type.VOLUME: lambda _: Volume.ZERO,
                                                           Type.TICKS: lambda _: Ticks.ZERO,
                                                          })
    
    def __init__(self, *,
                 interactive: bool,
                 global_types: Optional[TypeMap] = None) -> None:
        self.interactive = interactive
        self.global_types = global_types if global_types is not None else TypeMap(None)
        self.current_types = ScopeStack(self.global_types)
        
    def defaultResult(self) -> Executable:
        print("Unhandled tree")
        return Executable.constant(Type.ERROR, None, is_error=True)
        # assert False, "Undefined visitor method"
        
    def visitChildren(self, node):
        print(f"Unhandled tree: {type(node).__name__}")
        return Executable.constant(Type.ERROR, None, is_error=True)
    
    def compatible(self, have: Type, want: Type) -> bool:
        return have <= want # or Conversions.can_convert(have, want)
    
    def error_val(self, return_type: Type, 
                  value: Optional[Callable[[Environment], Any]] = None) -> Executable:
        vfn = value if value is not None else lambda env: self.default_creators[return_type](env)
        return Executable(return_type, lambda env: Delayed.complete(vfn(env)), is_error=True)
    
    def error(self, 
              ctx: ParserRuleContext, 
              return_type: Type, 
              msg: Union[str, Callable[[str], str]],
              *,
              value: Optional[Callable[[Environment], Any]] = None) -> Executable:
        if not isinstance(msg, str):
            msg = msg(self.text_of(ctx))
        print(f"line {ctx.start.line}:{ctx.start.column} {msg}")
        return self.error_val(return_type, value)
    
    def args_error(self, args: Sequence[Union[Executable, Type]], 
                   arg_ctxts: Sequence[ParserRuleContext], 
                   whole: ParserRuleContext,
                   return_type: Type, 
                   *,
                   verb: Optional[str] = None,
                   value: Optional[Callable[[Environment], Any]] = None,
                   msg: Optional[Union[str, Callable[[Sequence[Type], 
                                                      Sequence[str],
                                                      str], str]]] = None) -> Executable:
        
        arg_types = [arg.return_type if isinstance(arg, Executable) else arg for arg in args]
        if msg is None:
            if verb is None:
                verb = "combine"
            msg = f"Cannot {verb} {conj_str(arg_types)}: {self.text_of(whole)}"
        if not isinstance(msg, str):
            msg = msg(arg_types, [self.text_of(a) for a in arg_ctxts], self.text_of(whole))
        return self.error(whole, return_type, msg, value=value)
    


        
    def text_of(self, ctx_or_token: Union[ParserRuleContext, TerminalNode]) -> str:
        if isinstance(ctx_or_token, TerminalNode):
            t: str = ctx_or_token.getText()
            return t
        return " ".join(self.text_of(child) for child in ctx_or_token.getChildren())
    
    def string_text(self, token: TerminalNode) -> str:
        with_quotes: str = token.getText()
        val = with_quotes[1:-1]
        # print(f"With Quotes: <{with_quotes}>, without: <{val}>")
        def repl_escape(m: Match) -> str:
            seq = m.group(1)
            if seq.startswith("u"):
                hexdigits = m.group(2)
                return chr(int(hexdigits, 16))
                # Handle unicode
                ...
            repl = self.escape_replacement.get(seq, None)
            return  repl or seq
        val = self.escape_re.value.sub(repl_escape, val)
        return val

    def type_name_var(self, t_or_ctx: Union[DMFParser.Param_typeContext, Type], n: Optional[int] = None) -> str:
        t = t_or_ctx if isinstance(t_or_ctx, Type) else cast(Type, t_or_ctx.type)
        # t: Type = cast(Type, ctx.type)
        index = "" if n is None else f"_{n}"
        return f"**{t.name}{index}**"
        

    def type_check(self, 
                   want: Union[Type,Sequence[Type]],
                   have: Union[Type,Executable],
                   ctx: ParserRuleContext, 
                   msg: Optional[Union[str, Callable[[str, str, str], str]]] = None,
                   *,
                   return_type: Type = Type.NONE,
                   value: Optional[Callable[[Environment], Any]] = None
                   ) -> Optional[Executable]:
        if isinstance(have, Executable):
            have = have.return_type
        if isinstance(want, Type):
            if self.compatible(have, want):
                return None
            else:
                wname = want.name
        else:
            if any(self.compatible(have, w) for w in want):
                return None
            else:
                wname = map_str(tuple(w.name for w in want))
        # if what we have is Type.NONE, we've already found something we can't recover from,
        # so we don't bother with a message
        if have is Type.NONE:
            return self.error_val(return_type, value)
        m: Union[str, Callable[[str], str]]
        if isinstance(msg, str):
            m = msg
        else:
            if msg is None:
                msg = lambda want,have,text: f"Expected {want}, got {have}: {text}"
            msg_fn = msg
            h = have
            def msg_factory(text) -> str:
                return msg_fn(wname, h.name, text)
            m = msg_factory
        return self.error(ctx, return_type, m, value=value)
    
    def arg_dispatch(self, args: Sequence[Executable],
                     param_types: Sequence[Type],
                     ret_type: Type,
                     func: Callable[[Environment], Delayed[Any]]
                     ) -> Optional[Executable]:
        if not all(self.compatible(arg.return_type, pt) 
                   for arg, pt in zip(args, param_types)):
            return None
        return Executable(ret_type, func, args)
    
    def inapplicable_attr_error(self, 
                                attr: Attr,
                                obj_type: Type,
                                *,
                                attr_ctx: ParserRuleContext,
                                obj_ctx: ParserRuleContext,
                                ret_type: Optional[Type] = None
                                ) -> Executable:
        types = attr.applies_to
        if len(types) == 0:
            return self.error(attr_ctx, ret_type or Type.NONE,
                              lambda txt: f"{txt} is an attribute, but I don't know what to do with it")
        if ret_type is None:
            ret_type = Type.upper_bound(*attr.returns)
        if len(types) == 1:
            e = self.type_check(types[0], obj_type, obj_ctx, return_type=ret_type)
            assert e is not None
            return e
        
        a = self.text_of(attr_ctx)
        otn = obj_type.name
        tns = map_str(tuple(t.name for t in types))
        
        def emessage(text: str) -> str:
            return f"{otn}'s {a} not defined, requires one of {tns}: {text}"
        return self.error(obj_ctx, ret_type, emessage)
    
    def not_an_attr_error(self,
                          ctx: ParserRuleContext, 
                          attr_ctx: DMFParser.AttrContext) -> Executable:
        attr_name = attr_ctx.which
        attr_text = self.text_of(attr_ctx)
        type_spec = "" if (attr_text == attr_name) else f" ({attr_name})"
        return self.error(ctx, Type.NONE,
                          lambda text: f"'{attr_text}'{type_spec} is not an attribute: {text})")
        
    
    def use_callable(self, fn: Callable[..., Delayed[Any]],
                     arg_execs: Sequence[Executable],
                     sig: Signature, 
                     *,
                     extra_args: Sequence[Any] = ()) -> Executable:
        if isinstance(fn, LazyEval):
            def run(env: Environment) -> Delayed[Any]:
                return fn(env, arg_execs, *extra_args)
        else:
            def run(env: Environment) -> Delayed[Any]:
                args: List[Any] = []
                def make_lambda(ae: Executable, pt: Type) -> Callable[[Any], Delayed]:
                    return lambda _: ae.evaluate(env,pt).transformed(lambda arg: args.append(arg))
                lambdas = [make_lambda(ae,pt) for ae,pt in zip(arg_execs, sig.param_types)]
                if len(lambdas) == 0:
                    return fn()
                first = lambdas[0](None)
                future = (Delayed.complete(None) if len(arg_execs) == 0
                          else reduce(lambda fut,fn: fut.chain(fn),
                                      lambdas[1:],
                                      first))
                if isinstance(fn, WithEnv):
                    future = future.chain(lambda _: fn(env, *args, *extra_args))
                else:
                    future = future.chain(lambda _: fn(*args, *extra_args))
                return future            
        return Executable(sig.return_type, run, arg_execs)
    
    def use_function(self, func: Union[Func, str],
                     ctx: ParserRuleContext,
                     arg_ctxts: Sequence[ParserRuleContext],
                     *,
                     extra_args: Sequence[Any] = ()) -> Executable:
        if isinstance(func, str):
            if func not in Functions:
                raise KeyError(f"Compiler has no implementation for function '{func}'")
            func = Functions[func]
        arg_execs = [self.visit(arg) for arg in arg_ctxts]
        arg_types = [ae.return_type for ae in arg_execs]
        desc = func[arg_types]
        if desc is None:
            rt = func.error_type(arg_types)
            # Don't bother to report an error if an arg already did and we don't know
            # what type it would have returned.
            real_func = func
            for ae in arg_execs:
                if ae.return_type is Type.NONE and ae.contains_error:
                    return self.error_val(rt)
            return self.error(ctx, rt, lambda txt: real_func.type_error(arg_types, txt))
        sig, fn = desc
        return self.use_callable(fn, arg_execs, sig, extra_args=extra_args)
    
    def unit_exec(self, unit: PhysUnit, ctx: ParserRuleContext, size_ctx: ParserRuleContext) -> Executable:
        func = UnitFuncs[unit]
        return self.use_function(func, ctx, (size_ctx,))
    
    def unit_mag_exec(self, unit: PhysUnit, ctx: ParserRuleContext, quant_ctx: ParserRuleContext) -> Executable:
        func = UnitMagFuncs[unit]
        return self.use_function(func, ctx, (quant_ctx,))
    
    def unit_string_exec(self, unit: PhysUnit, ctx: ParserRuleContext, quant_ctx: ParserRuleContext) -> Executable:
        func = UnitStringFuncs[unit]
        return self.use_function(func, ctx, (quant_ctx,))
    
    def visit(self, tree) -> Executable:
        return cast(Executable, DMFVisitor.visit(self, tree))

    def visitMacro_file(self, ctx:DMFParser.Macro_fileContext) -> Executable:
        stats: Sequence[Executable] = [self.visit(tls) for tls in ctx.stat()] 
        def run(env: Environment) -> Delayed[None]:
            if len(stats) == 0:
                return Delayed.complete(None)
            future: Delayed[Any] = stats[0].evaluate(env)
            for stat in stats[1:]:
                def evaluator(s: Executable):
                    return lambda _: s.evaluate(env)
                future = future.chain(evaluator(stat))
            return future
        return Executable(Type.NONE, run, stats)


    def visitCompound_interactive(self, ctx:DMFParser.Compound_interactiveContext) -> Executable:
        return self.visit(ctx.compound())


    # def visitAssignment_interactive(self, ctx:DMFParser.Assignment_interactiveContext) -> Executable:
    #     return self.visit(ctx.assignment())

    def visitDecl_interactive(self, ctx:DMFParser.Decl_interactiveContext) -> Executable:
        return self.visit(ctx.declaration())


    def visitExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext) -> Executable:
        return self.visit(ctx.expr())
    
    def visitEmpty_interactive(self, ctx:DMFParser.Empty_interactiveContext) -> Executable: # @UnusedVariable
        return Executable.constant(Type.IGNORE, None)

    
    # def visitAssignment_tls(self, ctx:DMFParser.Assignment_tlsContext) -> Executable:
    #     return self.visit(ctx.assignment())
    #
    # def visitMacro_def_tls(self, ctx:DMFParser.Macro_def_tlsContext) -> Executable:
    #     return 0



    def visitName_assign_expr(self, ctx:DMFParser.Name_assign_exprContext) -> Executable:
        name_ctx = cast(DMFParser.NameContext, ctx.which)
        type_ctx = cast(Optional[DMFParser.Param_typeContext], ctx.param_type())
        n = None if ctx.n is None else int(cast(Token, ctx.n).text)

        if type_ctx is None:
            name: str = cast(str, name_ctx.val)
            # name = self.text_of(name_ctx)
        else:
            name = self.type_name_var(type_ctx, n)
        value = self.visit(ctx.what)
        builtin = BuiltIns.get(name, None)
        setter: Callable[[Environment, Any], None]
        var_type: Type
        if builtin is not None:
            return self.error(ctx, value.return_type, 
                              f"Can't assign to built-in '{name}'")
            
        if (special := SpecialVars.get(name)) is not None:
            if not special.is_settable:
                return self.error(ctx, value.return_type,
                                  f"Can't assign to special variable '{name}'")
            var_type = special.var_type
            spec = special
            setter = lambda env,val: spec.set(env, val)
            new_decl = False
        else:
            vt = self.current_types.lookup(name)
            if vt is None:
                new_decl = True
                var_type = value.return_type
                if not self.current_types.is_top_level:
                    self.error(ctx, var_type,
                               lambda text: f"Undeclared variable '{name}' assigned to in local scope: {text}"
                               )
            else:
                var_type = vt
                new_decl = False
            def do_assignment(env: Environment, val) -> None:
                if new_decl:
                    env.define(name, val)
                else:
                    env[name] = val
            setter = do_assignment
        if e := self.type_check(var_type, value.return_type, ctx, 
                                lambda want,have,text: 
                                    f"variable '{name}' has type {have}.  Expression has type {want}: {text}",
                                return_type=var_type):
                return e
        returned_type = var_type
        # print(f"Compiling assignment: {name} : {returned_type}")
        if new_decl and not value.contains_error:
            self.current_types.define(name, returned_type)
        def run(env: Environment) -> Delayed[Any]:
            def do_assignment(val) -> Any:
                setter(env, val)
                return val
            return value.evaluate(env, var_type).transformed(do_assignment)
        return Executable(returned_type, run, (value,))
    
    def visitAttr_assign_expr(self, ctx:DMFParser.Attr_assign_exprContext) -> Executable:
        obj = self.visit(ctx.obj)
        value = self.visit(ctx.what)
        attr_name: str = ctx.attr().which
        attr = Attributes.get(attr_name, None)
        if attr is None:
            return self.not_an_attr_error(ctx, ctx.attr())
        desc = attr.setter(obj.return_type, value.return_type)
        if desc is None:
            a = self.text_of(ctx.attr())
            allowed = attr.accepts_for(obj.return_type)
            if len(allowed) == 0:
                if obj.return_type not in attr.applies_to:
                    return self.inapplicable_attr_error(attr, obj.return_type,
                                                        attr_ctx = ctx.attr,
                                                        obj_ctx = ctx.obj,
                                                        ret_type = value.return_type)
                else:
                    otn = obj.return_type.name
                    def emessage(text: str) -> str:
                        return f"{otn}'s {a} is not mutable: {text}"
                    return self.error(ctx, value.return_type, emessage)
            else:
                def emessage(text: str) -> str:
                    if len(allowed) == 1:
                        req = allowed[0].name
                    else:
                        tns = map_str(tuple(t.name for t in allowed))
                        req = f"one of {tns}"
                    return f"{otn}'s {a} can only be set to {req}: {text}"
                return self.error(ctx, value.return_type, emessage)
        sig, setter = desc 
        ot, vt = sig.param_types
        def run(env: Environment) -> Delayed[Any]:
            def do_assignment(o,v) -> Any:
                setter(o,v)
                return v
            
            return (obj.evaluate(env, ot) 
                        .chain(lambda o: value.evaluate(env, vt)
                                .transformed(lambda v: do_assignment(o,v))))
        return Executable(value.return_type, run, (obj, value))


    # def visitAssign_stat(self, ctx:DMFParser.Assign_statContext) -> Executable:
    #     return self.visit(ctx.assignment())
    
    def visitDeclaration(self, ctx:DMFParser.DeclarationContext) -> Executable:
        name_ctx : Optional[DMFParser.NameContext] = ctx.name()
        var_type: Optional[Type] = ctx.type
        n: Optional[int] = ctx.n
        init_ctx: Optional[DMFParser.ExprContext] = ctx.init
        has_local_kwd = ctx.LOCAL() is not None
        
        if name_ctx is None:
            assert var_type is not None
            assert n is not None
            name = self.type_name_var(var_type, n)
        else:
            name = cast(str, name_ctx.val)
            # name = self.text_of(name_ctx)

        assert init_ctx is not None or var_type is not None
        value = self.visit(init_ctx) if init_ctx is not None else None
            
        # if we have a "type n = init" form and "type n" already defined, we just assign rather than
        # shadowing
        just_assign = not has_local_kwd and value is not None and self.current_types.lookup(name) is not None

        if var_type is None:
            assert value is not None
            var_type = value.return_type        
        builtin = BuiltIns.get(name, None)
        if builtin is not None:
            return self.error(ctx, var_type, 
                              lambda text: f"Can't declare variable shadowing built-in '{name}': {text}")
        if name in SpecialVars:
            return self.error(ctx, var_type, 
                              lambda text: f"Can't declare variable shadowing special variable '{name}': {text}")
        if not just_assign and self.current_types.defined_locally(name):
            old_type = not_None(self.current_types.lookup(name)).name
            new_type = var_type.name
            if old_type is not new_type:
                return self.error(ctx, var_type, 
                                  lambda text: f"{name} redeclared as {new_type}, was {old_type}: {text}")
            self.error(ctx, var_type,
                       lambda text: f"{name} already declared in scope: {text}")
            just_assign = True
        if (value is None or not value.contains_error) and not just_assign:
            self.current_types.define(name, var_type)            

        if value is None:
            # Declaration only
            def do_decl(env: Environment) -> Delayed[None]:
                env.define(name, None)
                return Delayed.complete(None)
            return Executable(Type.NONE, do_decl)
            
        if e := self.type_check(var_type, value.return_type, ctx, 
                                lambda want,have,text: 
                                    f"variable '{name}' has type {have}.  Expression has type {want}: {text}",
                                return_type=var_type):
            return e
        
        real_val = value
        def run(env: Environment) -> Delayed[Any]:
            def do_assignment(val) -> Any:
                if just_assign:
                    env[name] = val
                else:
                    env.define(name, val)
                return val
            return real_val.evaluate(env, var_type).transformed(do_assignment)
        return Executable(var_type, run, (value,))

    def visitDecl_stat(self, ctx:DMFParser.Decl_statContext) -> Executable:
        return self.visit(ctx.declaration())
    
    def visitPrinting(self, ctx:DMFParser.PrintingContext) -> Executable:
        def print_vals(*vals):
            print(*vals)
            return Delayed.complete(None)
        vals = tuple(self.visit(c) for c in ctx.vals)
        sig = Signature.of(tuple(v.return_type for v in vals), Type.NONE)
        return self.use_callable(print_vals, vals, sig)
        
    def visitPrint_stat(self, ctx:DMFParser.Print_statContext):
        return self.visit(ctx.printing())

    def visitPrint_interactive(self, ctx:DMFParser.Print_statContext):
        return self.visit(ctx.printing())

    def visitPause_stat(self, ctx:DMFParser.Pause_statContext) -> Executable:
        duration = self.visit(ctx.duration)
        if e:=self.type_check(Type.DELAY, duration, ctx.duration,
                              lambda want,have,text: # @UnusedVariable
                                f"Delay ({have} must be time or ticks: {text}",
                              return_type=Type.PAUSE):
            return e
        def run(env: Environment) -> Delayed[None]:
            def pause(d: DelayType, env: Environment) -> Delayed[None]:
                print(f"Delaying for {d}")
                return env.board.delayed(lambda: None, after=d)
            return (duration.evaluate(env, Type.DELAY)
                    .chain(lambda d: pause(d, env)))
        return Executable(Type.PAUSE, run, (duration,))

    def visitExpr_stat(self, ctx:DMFParser.Expr_statContext) -> Executable:
        return self.visit(ctx.expr())

    

    def visitCompound_stat(self, ctx:DMFParser.Compound_statContext) -> Executable:
        return self.visit(ctx.compound())


    def visitBlock(self, ctx:DMFParser.BlockContext) -> Executable:
        stat_contexts: Sequence[DMFParser.StatContext] = ctx.stat()
        with self.current_types.push():
            stat_execs = tuple(self.visit(sc) for sc in stat_contexts)
            
        ret_type = Type.NONE if len(stat_execs) == 0 else stat_execs[-1].return_type

        def run(env: Environment) -> Delayed[None]:
            local_env = env.new_child()
            if len(stat_execs) == 0:
                return Delayed.complete(None)
            
            def execute(i: int) -> Delayed[None]:
                # print(f"***Executing {self.text_of(stat_contexts[i])}")
                return stat_execs[i].evaluate(local_env)
            
            future = execute(0)
            for i in range(1, len(stat_execs)):
                # We have to do something like this to ensure that each lambda gets a different i
                def executor(j: int) -> Callable[[Any], Delayed[None]]:
                    return lambda _: execute(j)
                # print(f"Scheduling {self.text_of(stat_contexts[i])}")
                future = future.chain(executor(i))
            return future
        return Executable(ret_type, run, stat_execs)



    def visitPar_block(self, ctx:DMFParser.Par_blockContext) -> Executable:
        stat_contexts: Sequence[DMFParser.StatContext] = ctx.stat()
        with self.current_types.push():
            stat_execs = tuple(self.visit(sc) for sc in stat_contexts)
            
        ret_type = Type.NONE
        
        def run(env: Environment) -> Delayed[None]:
            local_env = env.new_child()
            if len(stat_execs) == 0:
                return Delayed.complete(None)
            barrier = Barrier[Any](required = len(stat_execs))
            future = Postable[None]()
            barrier.wait(None, future)
            with env.board.in_system().batched():
                for se in stat_execs:
                    se.evaluate(local_env).then_call(lambda v: barrier.reach(v))
            return future
        return Executable(ret_type, run, stat_execs)
    
    def visitIf_stat(self, ctx:DMFParser.If_statContext) -> Executable:
        test_ctxts: Sequence[DMFParser.ExprContext] = ctx.tests
        tests = [self.visit(ctx) for ctx in test_ctxts]
        body_ctxts: Sequence[DMFParser.CompoundContext] = ctx.bodies
        bodies = [self.visit(ctx) for ctx in body_ctxts]
        else_ctxt = cast(Optional[DMFParser.CompoundContext], ctx.else_body)
        else_body = self.visit(else_ctxt) if else_ctxt is not None else None
        
        for t,c in zip(tests, test_ctxts):
            if e := self.type_check(Type.BOOL, t, c):
                return e

        result_type: Optional[Type] = None
        def check_result_type(t: Type) -> bool:
            nonlocal result_type
            if result_type is None or self.compatible(result_type, t):
                result_type = t
                return False
            result_type = Type.NONE
            return True
        
        if else_body is None:
            result_type = Type.NONE
            children = (*tests, *bodies)
        else:
            result_type = else_body.return_type
            children = (*tests, *bodies, else_body)
            
            for b in bodies:
                if check_result_type(b.return_type):
                    break
        
        def run(env: Environment) -> Delayed:
            n_tests = len(tests)
            def check(i: int) -> Delayed:
                if i == n_tests:
                    if else_body is None:
                        return Delayed.complete(None)
                    else:
                        return else_body.evaluate(env, result_type)
                return (tests[i].evaluate(env, Type.BOOL)
                        .chain(lambda v: (bodies[i].evaluate(env, result_type)
                                          if v else check(i+1))))
            return check(0)
        
        
        return Executable(result_type, run, children)
    
    def visitLoop_stat(self, ctx:DMFParser.Loop_statContext) -> Executable:
        return self.visit(ctx.loop())
    
    def visitRepeat_loop(self, ctx:DMFParser.Repeat_loopContext) -> Executable:
        n_exec = self.visit(ctx.n)
        assert False
        # if e := self.type_check(Type.INT, n_exec, ctx,
        #                         lambda text: 
        #                         )
        ...
    

    def visitParen_expr(self, ctx:DMFParser.Paren_exprContext) -> Executable:
        return self.visit(ctx.expr())


    def visitNeg_expr(self, ctx:DMFParser.Neg_exprContext) -> Executable:
        return self.use_function("NEGATE", ctx, (ctx.rhs,))


    def visitInt_expr(self, ctx:DMFParser.Int_exprContext):
        val: int = int(ctx.INT().getText())
        return Executable.constant(Type.INT, val)

    def visitFloat_expr(self, ctx:DMFParser.Float_exprContext):
        val: float = float(ctx.FLOAT().getText())
        return Executable.constant(Type.FLOAT, val)

    def visitType_name_expr(self, ctx:DMFParser.Type_name_exprContext):
        n = None if ctx.n is None else int(cast(Token, ctx.n).text)
        name = self.type_name_var(ctx.param_type(), n)
        var_type = self.current_types.lookup(name)
        if var_type is None:
            return self.error(ctx.param_type(), Type.NONE, f"Undefined variable: {name}")
        def run(env: Environment) -> Delayed[Any]:
            return Delayed.complete(env[name])
        return Executable(var_type, run)
    
    
    def visitIndex_expr(self, ctx:DMFParser.Index_exprContext) -> Executable:
        return self.use_function("INDEX", ctx, (ctx.who, ctx.which))

    def visitMacro_expr(self, ctx:DMFParser.Macro_exprContext) -> Executable:
        return self.visit(ctx.macro_def())

    def visitAction_expr(self, ctx:DMFParser.Action_exprContext) -> Executable:
        which: str = ctx.no_arg_action().which
        return self.use_function(which, ctx, ())

    def visitName_expr(self, ctx:DMFParser.Name_exprContext) -> Executable:
        name: str = ctx.name().val
        builtin = BuiltIns.get(name, None)
        if builtin is not None:
            return Executable.constant(Type.BUILT_IN, builtin)
        if (special := SpecialVars.get(name)) is not None:
            real_special = special
            return Executable(special.var_type, lambda env: Delayed.complete(real_special.get(env)))
        var_type = self.current_types.lookup(name)
        if var_type is None:
            return self.error(ctx.name(), Type.NONE, f"Undefined variable: {name}")
        def run(env: Environment) -> Delayed[Any]:
            return Delayed.complete(env[name])
        return Executable(var_type, run)

    def visitBool_const_expr(self, ctx:DMFParser.Bool_const_exprContext) -> Executable:
        val = ctx.bool_val().val
        return Executable.constant(Type.BOOL, val)
    
    escape_re = LazyPattern("\\\\([rnt]|u([a-fA-F0-9]{4})|.)")
    escape_replacement = { 
        "r": "\r",
        "n": "\n",
        "t": "\t",
        }
    
    def visitString_lit_expr(self, ctx:DMFParser.String_lit_exprContext) -> Executable:
        val = self.string_text(ctx.string())
        return Executable.constant(Type.STRING, val)
        

    def visitAddsub_expr(self, ctx:DMFParser.Addsub_exprContext) -> Executable:
        addp = ctx.ADD() is not None
        func = "ADD" if addp else "SUBTRACT"
        return self.use_function(func, ctx, (ctx.lhs, ctx.rhs))
            

    def visitRel_expr(self, ctx:DMFParser.Rel_exprContext) -> Executable:
        lhs = self.visit(ctx.lhs)
        rhs = self.visit(ctx.rhs)
        rel: Rel = ctx.rel().which
        ok_types = (Type.INT, Type.FLOAT, Type.TIME, Type.TICKS, Type.VOLUME)
        if rel is not Rel.EQ and rel is not Rel.NE:
            if e:=self.type_check(ok_types, lhs.return_type, ctx.lhs, return_type=Type.BOOL):
                return e
        if lhs.return_type is not rhs.return_type:
            return self.error(ctx, Type.BOOL,
                              f"Can't compare {lhs.return_type.name} and {rhs.return_type.name}: {self.text_of(ctx)}")
        def run(env: Environment) -> Delayed[bool]:
            def combine(x, y) -> bool:
                return rel.test(x, y) 
            future: Delayed = lhs.evaluate(env)
            return future.chain(lambda x: (rhs.evaluate(env)
                                            .transformed(lambda y: combine(x,y))))
        return Executable(Type.BOOL, run, (lhs,rhs))
    
    
    def visitHas_expr(self, ctx:DMFParser.Has_exprContext) -> Executable:
        obj = self.visit(ctx.obj)
        attr_name: str = ctx.attr().which
        attr = Attributes.get(attr_name, None)
        if attr is None:
            return self.not_an_attr_error(ctx, ctx.attr())
        desc = attr.getter(obj.return_type)
        if desc is None:
            return self.inapplicable_attr_error(attr, obj.return_type,
                                                attr_ctx = ctx.attr(),
                                                obj_ctx = ctx.obj,
                                                ret_type = Type.BOOL)
        sig, extractor = desc
        rt = sig.return_type
        ot = sig.param_types[0] 
        if not isinstance(rt, MaybeType):
            self.error(ctx.attr(), Type.BOOL,
                       lambda txt:  f"{txt} is not a 'maybe' attribute. 'has' will always return True.")
            return Executable(Type.BOOL, (lambda _: Delayed.complete(True)), (obj,))
        def run(env: Environment) -> Delayed[Any]:
            f: Delayed = obj.evaluate(env, ot)
            return f.chain(extractor).transformed(lambda v: v is not None)
        return Executable(Type.BOOL, run, (obj,))
    
    

    def visitNot_expr(self, ctx:DMFParser.Not_exprContext) -> Executable:
        return self.use_function("NOT", ctx, (ctx.expr(),))
    
    def visitAnd_expr(self, ctx:DMFParser.And_exprContext) -> Executable:
        return self.use_function("AND", ctx, (ctx.lhs, ctx.rhs))
    
    def visitOr_expr(self, ctx:DMFParser.Or_exprContext) -> Executable:
        return self.use_function("OR", ctx, (ctx.lhs, ctx.rhs))
    
    def visitCond_expr(self, ctx:DMFParser.Cond_exprContext) -> Executable:
        first = self.visit(ctx.first)
        cond = self.visit(ctx.cond)
        second = self.visit(ctx.second)
        if e := self.type_check(Type.BOOL, cond, ctx.cond):
            return e
        if self.compatible(first.return_type, second.return_type):
            result_type = second.return_type
        elif second.return_type < first.return_type:
            result_type = first.return_type
        else:
            t1 = first.return_type.name
            t2 = second.return_type.name
            return self.error(ctx, Type.ANY, 
                              lambda txt: f"Conditional expression branches incompatible ({t1} and {t2}): {txt}")
        def run(env: Environment) -> Delayed:
            def branch(c: bool) -> Delayed:
                if c:
                    return first.evaluate(env, result_type)
                else:
                    return second.evaluate(env, result_type)
            return cond.evaluate(env, Type.BOOL).chain(lambda v: branch(v))
        return Executable(result_type, run, (first, cond, second))

    def visitDelta_expr(self, ctx:DMFParser.Delta_exprContext) -> Executable:
        dist = self.visit(ctx.dist)
        direction: Dir = ctx.direction().d
        if e:=self.type_check(Type.INT, dist, ctx.dist, return_type=Type.DELTA):
            return e
        def run(env: Environment) -> Delayed[DeltaValue]:
            return (dist.evaluate(env, Type.INT)
                    .transformed(lambda n: DeltaValue(n, direction))
                    )
        return Executable(Type.DELTA, run, (dist,))

    def visitIn_dir_expr(self, ctx:DMFParser.In_dir_exprContext) -> Executable: 
        dist = self.visit(ctx.dist)
        direction = self.visit(ctx.d)
        if e:=self.type_check(Type.INT, dist, ctx.dist, return_type=Type.DELTA):
            return e
        if e:=self.type_check(Type.DIR, direction, ctx.d, return_type=Type.DELTA):
            return e
        def run(env: Environment) -> Delayed[DeltaValue]:
                def combine(n: int, d: Dir) -> DeltaValue:
                    return DeltaValue(n, d)
                future: Delayed[int] = dist.evaluate(env, Type.INT)
                return future.chain(lambda n: (direction.evaluate(env, Type.DIR)
                                               .transformed(lambda d: combine(n,d))))
        return Executable(Type.DELTA, run, (dist, direction))


    
    def visitDir_expr(self, ctx:DMFParser.Dir_exprContext) -> Executable:
        direction: Dir = ctx.direction().d
        return Executable.constant(Type.DIR, direction)
    
    def visitTurn_expr(self, ctx:DMFParser.Turn_exprContext) -> Executable:
        return self.use_function("TURNED", ctx, (ctx.start_dir,), extra_args=(ctx.turn().t,))
    
    def visitN_rc_expr(self, ctx:DMFParser.N_rc_exprContext) -> Executable:
        dist = self.visit(ctx.dist)
        direction: Dir = ctx.rc().d
        if e:=self.type_check(Type.INT, dist, ctx.dist, return_type=Type.DELTA):
            return e
        def run(env: Environment) -> Delayed[DeltaValue]:
            return (dist.evaluate(env, Type.INT)
                    .transformed(lambda n: DeltaValue(n, direction))
                    )
        return Executable(Type.DELTA, run, (dist,))

    def visitConst_rc_expr(self, ctx:DMFParser.N_rc_exprContext) -> Executable:
        direction: Dir = ctx.rc().d
        n = int(cast(Token, ctx.INT()).getText())
        return Executable.constant(Type.DELTA, DeltaValue(n, direction))

    
    def visitCoord_expr(self, ctx:DMFParser.Coord_exprContext) -> Executable:
        return self.use_function("COORD", ctx, (ctx.x, ctx.y))

    def visitInjection_expr(self, ctx:DMFParser.Injection_exprContext) -> Executable:
        who = self.visit(ctx.who)
        what = self.visit(ctx.what)
        inj_type = what.return_type
        if inj_type is Type.DIR or inj_type <= Type.MOTION:
            inj_type = Type.MOTION
        injected_type = who.return_type
        if injected_type <= Type.MOTION:
            injected_type = Type.MOTION
        if not isinstance(inj_type, CallableType) or len(inj_type.param_types) != 1:
            return self.error(ctx.what, Type.NONE, 
                              f"Not an injection target ({what.return_type.name}): {self.text_of(ctx.what)}")
        first_arg_type = inj_type.param_types[0]
        return_first_arg = inj_type.return_type is Type.NONE
        return_type = who.return_type if return_first_arg else inj_type.return_type
        if self.compatible(who.return_type, first_arg_type):
            def run(env: Environment) -> Delayed[Any]:
                def inject(obj, func) -> Delayed[Any]:
                    assert isinstance(func, CallableValue)
                    future = func.apply((obj,))
                    return future if not return_first_arg else future.transformed(lambda _: obj)
                return (who.evaluate(env, first_arg_type)
                        .chain(lambda obj: (what.evaluate(env, inj_type)
                                            .chain(lambda func: inject(obj, func)))))
            # print(f"Injection returns {inj_type.return_type}: {self.text_of(ctx)}")
            return Executable(return_type, run, (who, what))
        elif injected_type is Type.DIR or isinstance(injected_type, CallableType):
            if injected_type is Type.DIR:
                injected_type = Type.MOTION
            assert isinstance(injected_type, CallableType)
            pass_first_arg = len(injected_type.param_types) == 1 and injected_type.return_type is Type.NONE
            pass_arg_type = injected_type.param_types[0] if pass_first_arg else injected_type.return_type
            if e:=self.type_check(first_arg_type, pass_arg_type, ctx.who,
                                  lambda want,have,text:
                                    f"Injecting form '{text}' returns {have}, not compatible with "
                                    +f"{want}: {self.text_of(ctx.what)}"):
                return e
            chain_return_type = pass_arg_type if return_first_arg else inj_type.return_type
            chain_type = CompositionType.find(injected_type.param_types, chain_return_type)
            
            def chain(env: Environment) -> Delayed[Any]:
                def combine(first: CallableValue, second: CallableValue) -> Delayed[Any]:
                    comp = ComposedCallable(chain_type, first, second, pass_first_arg)
                    return Delayed.complete(comp)
                return (who.evaluate(env, injected_type)
                        .chain(lambda first: (what.evaluate(env, inj_type)
                                              .chain(lambda second: combine(first, second)))))
            return Executable(chain_type, chain, (who, what))
        e = self.type_check(first_arg_type, who, ctx.who,
                            (lambda want,have,text:
                                f"Injected value ({have}) '{text}' not compatible with "
                                +f"{want}: {self.text_of(ctx.what)}"),
                            return_type=return_type)
        return not_None(e)
        
            
    
    def visitAttr_expr(self, ctx:DMFParser.Attr_exprContext) -> Executable:
        obj = self.visit(ctx.obj)
        attr_name: str = ctx.attr().which
        attr = Attributes.get(attr_name, None)
        if attr is None:
            return self.not_an_attr_error(ctx, ctx.attr())
        getter = attr.getter(obj.return_type)
        if getter is None:
            return self.inapplicable_attr_error(attr, obj.return_type,
                                                attr_ctx = ctx.attr(),
                                                obj_ctx = ctx.obj)
        
        sig, extractor = getter
        rt = sig.return_type
        ot = sig.param_types[0]
        check: Optional[Callable[[Any], Any]] = None
        if isinstance(rt, MaybeType):
            real_extractor = extractor
            def extractor(obj):
                def check(val):
                    if val is None:
                        raise MaybeNotSatisfiedError(f"{obj} does not have {attr}")
                    return val
                return real_extractor(obj).transformed(check)
            rt = rt.if_there_type
        def run(env: Environment) -> Delayed[Any]:
            f: Delayed = obj.evaluate(env, ot)
            return f.chain(extractor)
        return Executable(rt, run, (obj,))



    def visitWell_expr(self, ctx:DMFParser.Well_exprContext) -> Executable:
        which = self.visit(ctx.which)
        if e:=self.type_check(Type.INT, which, ctx.which, return_type=Type.WELL):
            return e
        def run(env: Environment) -> Delayed[Well]:
            f: Delayed[int] = which.evaluate(env, Type.INT)
            return f.transformed(lambda n: env.board.wells[n])
        return Executable(Type.WELL, run, (which,))



    def visitDrop_expr(self, ctx:DMFParser.Drop_exprContext) -> Executable:
        # loc_exec = self.visit(ctx.loc)
        vol: Optional[DMFParser.ExprContext] = ctx.vol
        
        if vol is None:
            return self.use_function("FIND_DROP", ctx, (ctx.loc,))
        else:
            return self.use_function("NEW_DROP", ctx, (ctx.vol, ctx.loc))
        
    def visitReagent_lit_expr(self, ctx:DMFParser.Reagent_lit_exprContext) -> Executable:
        reagent = ctx.reagent().r
        return Executable.constant(Type.REAGENT, reagent)
        
    def visitReagent_expr(self, ctx:DMFParser.Reagent_exprContext) -> Executable:
        return self.use_function("FIND_REAGENT", ctx, (ctx.which,))
    
    def visitLiquid_expr(self, ctx:DMFParser.Liquid_exprContext) -> Executable:
        return self.use_function("LIQUID", ctx, (ctx.vol, ctx.which))


    def visitFunction_expr(self, ctx:DMFParser.Function_exprContext) -> Executable:
        arg_execs = tuple(self.visit(arg) for arg in ctx.args)
        fc = cast(DMFParser.ExprContext, ctx.func)
        if isinstance(fc, DMFParser.Name_exprContext):
            func_name = self.text_of(fc.name())
            builtin = BuiltIns.get(func_name, None)
            if builtin is not None:
                return self.use_function(builtin, ctx, ctx.args)
        func_exec = self.visit(fc)
        f_type = func_exec.return_type
        if f_type is Type.DIR:
            f_type = Type.DELTA
        if not isinstance(f_type, CallableType):
            return self.error(fc, Type.NONE, lambda text: f"Not callable ({f_type.name}): {text}")
        ret_type = f_type.return_type
        param_types = f_type.param_types
        if len(param_types) != len(arg_execs):
            np = len(param_types)
            na = len(arg_execs)
            return self.error(ctx, ret_type, 
                              lambda text: f"Wrong number of arguments to macro.  Expected {np}, got {na}: {text}")
        for i in range(len(param_types)):
            if not self.compatible(arg_execs[i].return_type, param_types[i]):
                ac = ctx.args[i]
                ae = arg_execs[i]
                pt = param_types[i]
                return self.error(ac, ret_type, f"Argument {i+1} not {pt.name} ({ae.return_type.name}): {self.text_of(ac)}")
        
        def dispatch(fn: CallableValue, *args) -> Delayed[Any]:
            return fn.apply(args)
        
        # fn_exec = Executable(f_type, lambda env: Delayed.complete(env[f_name]), ())
        
        return self.use_callable(dispatch, [func_exec, *arg_execs], f_type.with_self_sig)
        


    def visitTo_expr(self, ctx:DMFParser.To_exprContext) -> Executable:
        axis: Optional[DMFParser.AxisContext] = ctx.axis()
        which = self.visit(ctx.which)
        if axis is None:
            # This is a to-pad motion
            if not self.compatible(which.return_type, Type.PAD):
                if self.compatible(which.return_type, Type.INT):
                    return self.error(ctx, Type.MOTION, f"Did you forget 'row' or 'column'?: {self.text_of(ctx)}")
                return self.error(ctx, Type.MOTION, f"'to' expr without 'row' or 'column' takes a PAD: {self.text_of(ctx)}")
            def run(env: Environment) -> Delayed[MotionValue]:
                return which.evaluate(env, Type.PAD).transformed(lambda pad: ToPadValue(pad))
        else:
            if not self.compatible(which.return_type, Type.INT):
                return self.error(ctx.which, Type.MOTION, 
                                  f"Row or column name not an int ({which.return_type.name}): {self.text_of(ctx.which)}")
            verticalp = cast(bool, axis.verticalp)
            def run(env: Environment) -> Delayed[MotionValue]:
                return which.evaluate(env, Type.INT).transformed(lambda n: ToRowColValue(n, verticalp))
        return Executable(Type.MOTION, run, (which,))
    
    def visitMuldiv_expr(self, ctx:DMFParser.Muldiv_exprContext)->Executable:
        mulp = ctx.MUL() is not None
        func = "MULTIPLY" if mulp else "DIVIDE"
        return self.use_function(func, ctx, (ctx.lhs, ctx.rhs))

    def visitDirection(self, ctx:DMFParser.DirectionContext):
        return DMFVisitor.visitDirection(self, ctx)


    def visitAxis(self, ctx:DMFParser.AxisContext):
        return DMFVisitor.visitAxis(self, ctx)

    def param_def(self, ctx: DMFParser.ParamContext) -> tuple[str, Type]:
        param_type: Optional[Type] = cast(Optional[Type], ctx.type)
        if param_type is None:
            param_type = Type.ERROR
            self.error(ctx, Type.IGNORE, lambda txt: f"No type specified for parameter '{txt}'")
        name_ctx: Optional[str] = ctx.name()
        if name_ctx is None:
            name = self.type_name_var(ctx.param_type(), ctx.n)
        else:
            name = self.text_of(name_ctx)
        return (name, param_type)
    
    def check_macro_params(self, names: Sequence[str],
                           types: Sequence[Type], 
                           ctxts: Sequence[DMFParser.ParamContext]) -> Optional[Executable]:
        seen = set[str]()
        saw_duplicate = False
        saw_untyped = any(t is Type.ERROR for t in types)
        for i,n in enumerate(names):
            if n in seen:
                self.error(ctxts[i], Type.IGNORE, lambda txt: f"Duplicate parameter: '{txt}'")
                saw_duplicate = True
            else:
                seen.add(n)
        if not saw_duplicate and not saw_untyped:
            return None
        macro_type = MacroType.find(types, Type.NONE)
        return self.error_val(macro_type, lambda env: Delayed.complete(None)) # @UnusedVariable

    def visitMacro_def(self, ctx:DMFParser.Macro_defContext) -> Executable:
        header: DMFParser.Macro_defContext = ctx.macro_header()
        param_contexts: Sequence[DMFParser.ParamContext] = header.param()
        
        for pc in param_contexts:
            if cast(bool, pc.deprecated):
                self.error(pc, cast(Type,pc.type), 
                           lambda text: f"'NAME: TYPE' declarations are deprecated.  Use 'TYPE NAME': {text}")
        
        param_defs = tuple(self.param_def(pc) for pc in param_contexts)
        param_names = tuple(pdef[0] for pdef in param_defs)
        param_types = tuple(pdef[1] for pdef in param_defs)
        
        if e := self.check_macro_params(param_names, param_types, param_contexts):
            return e
        
        with self.current_types.push(dict(param_defs)): 
            body: Executable
            if ctx.compound() is not None:
                body = self.visit(ctx.compound())
            else:
                body = self.visit(ctx.expr())
            macro_type = MacroType.find(param_types, body.return_type)
        
        def run(env: Environment) -> Delayed[MacroValue]: # @UnusedVariable
            return Delayed.complete(MacroValue(macro_type, env, param_names, body))
        return Executable(macro_type, run, (body,))

    def visitUnit_expr(self, ctx:DMFParser.Unit_exprContext) -> Executable:
        return self.unit_exec(ctx.dim_unit().unit, ctx, ctx.amount)
    
    def visitMagnitude_expr(self, ctx:DMFParser.Magnitude_exprContext) -> Executable:
        if ctx.dim_unit() is None:
            return self.error(ctx, Type.FLOAT, lambda text: f"'magnitude' requires 'in <unit>': {text}")
        return self.unit_mag_exec(ctx.dim_unit().unit, ctx, ctx.quant)

    def visitUnit_string_expr(self, ctx:DMFParser.Unit_exprContext) -> Executable:
        return self.unit_string_exec(ctx.dim_unit().unit, ctx, ctx.quant)
    
    # def visitDrop_vol_expr(self, ctx:DMFParser.Drop_vol_exprContext) -> Executable:
    #     return self.use_function("DROP_VOL", ctx, (ctx.amount,))
        
    def visitPause_expr(self, ctx:DMFParser.Pause_exprContext) -> Executable:
        duration = self.visit(ctx.duration)
        if e:=self.type_check(Type.DELAY, duration, ctx.duration,
                              lambda want,have,text: # @UnusedVariable
                                f"Delay ({have} must be time or ticks: {text}",
                              return_type=Type.PAUSE):
            return e
        def run(env: Environment) -> Delayed[PauseValue]:
            return (duration.evaluate(env, Type.DELAY)
                    .transformed(lambda d: PauseValue(d, env.board)))
        return Executable(Type.PAUSE, run, (duration,))
                
    def visitMacro_header(self, ctx:DMFParser.Macro_headerContext):
        return DMFVisitor.visitMacro_header(self, ctx)


    def visitParam(self, ctx:DMFParser.ParamContext):
        return DMFVisitor.visitParam(self, ctx)


    def visitParam_type(self, ctx:DMFParser.Param_typeContext):
        return DMFVisitor.visitParam_type(self, ctx)


    def visitName(self, ctx:DMFParser.NameContext):
        return DMFVisitor.visitName(self, ctx)


    def visitKwd_names(self, ctx:DMFParser.Kwd_namesContext):
        return DMFVisitor.visitKwd_names(self, ctx)
    
    @classmethod
    def setup_function_table(cls) -> None:
        fn = Functions["NEGATE"]
        fn.prefix_op("-")
        fn.register_all_immediate([((Type.INT,), Type.INT),
                                   ((Type.FLOAT,), Type.FLOAT)
                                   ], lambda x: -x)
        
        fn = Functions["INDEX"]
        fn.format_type_expr_using(2, lambda x,y: f"{x}[{y}]")
        fn.register_all_immediate([((Type.WELL, Type.INT), Type.WELL_PAD),
                                   ], lambda w,n: w.shared_pads[cast(int, n)])
        

        def add_delta(p: Pad, dn: Dir, n: int) -> Pad:
            board = p.board
            loc = board.orientation.neighbor(dn, p.location, steps=n)
            return board.pads[loc]

        fn = Functions["ADD"]
        fn.infix_op("+")
        fn.register_all_immediate([((Type.INT,Type.INT), Type.INT),
                                   ((Type.FLOAT,Type.FLOAT), Type.FLOAT),
                                   ((Type.TIME,Type.TIME), Type.TIME),
                                   ((Type.TICKS,Type.TICKS), Type.TICKS),
                                   ((Type.VOLUME,Type.VOLUME), Type.VOLUME),
                                   ((Type.STRING,Type.STRING), Type.STRING)
                                   ], lambda x,y: x+y)
        fn.register_immediate((Type.PAD, Type.DELTA), Type.PAD, lambda p,d: add_delta(p, d.direction, d.dist))
        fn.register_all_immediate([((Type.STRING, Type.NUMBER), Type.STRING),
                                   ], lambda x,y: x+str(y))
        fn.register_immediate((Type.SCALED_REAGENT, Type.SCALED_REAGENT), Type.REAGENT,
                              lambda x,y: x.mix_with(y)
                              )
        fn.register_immediate((Type.LIQUID, Type.LIQUID), Type.LIQUID,
                              lambda x,y: x.mix_with(y)
                              )
        
        
        fn = Functions["SUBTRACT"]
        fn.infix_op("-")
        fn.register_all_immediate([((Type.INT,Type.INT), Type.INT),
                                   ((Type.FLOAT,Type.FLOAT), Type.FLOAT),
                                   ((Type.TIME,Type.TIME), Type.TIME),
                                   ((Type.TICKS,Type.TICKS), Type.TICKS),
                                   ((Type.VOLUME,Type.VOLUME), Type.VOLUME),
                                   ], lambda x,y: x-y)
        
         
        fn.register_immediate((Type.PAD, Type.DELTA), Type.PAD, lambda p,d: add_delta(p, d.direction, -d.dist))
        
        fn = Functions["NOT"]
        fn.prefix_op("not")
        fn.register_all_immediate([((Type.BOOL,), Type.BOOL),
                                   ], lambda x: not x)

    
        fn = Functions["AND"]
        fn.infix_op("and")
        
        def sc_and(env: Environment, arg_execs: Sequence[Executable]) -> Delayed[bool]:
            lhs, rhs = arg_execs
            return (lhs.evaluate(env, Type.BOOL)
                    .chain(lambda x: (Delayed.complete(x) if not x
                                      else rhs.evaluate(env, Type.BOOL)))
                    )
        fn.register((Type.BOOL,Type.BOOL), Type.BOOL, LazyEval(sc_and))

        fn = Functions["OR"]
        fn.infix_op("or")
        
        def sc_or(env: Environment, arg_execs: Sequence[Executable]) -> Delayed[bool]:
            lhs, rhs = arg_execs
            return (lhs.evaluate(env, Type.BOOL)
                    .chain(lambda x: (Delayed.complete(x) if x
                                      else rhs.evaluate(env, Type.BOOL)))
                    )
        fn.register((Type.BOOL,Type.BOOL), Type.BOOL, LazyEval(sc_or))

        fn = Functions["MULTIPLY"]
        fn.infix_op("*")
        fn.register_all_immediate([((Type.INT,Type.INT), Type.INT),
                                   ((Type.FLOAT,Type.FLOAT), Type.FLOAT),
                                   ((Type.FLOAT,Type.TIME), Type.TIME),
                                   ((Type.TIME,Type.FLOAT), Type.TIME),
                                   ((Type.FLOAT,Type.TICKS), Type.TICKS),
                                   ((Type.TICKS,Type.FLOAT), Type.TICKS),
                                   ((Type.FLOAT,Type.VOLUME), Type.VOLUME),
                                   ((Type.VOLUME,Type.FLOAT), Type.VOLUME),
                                   ], lambda x,y: x*y)
        fn.register_immediate((Type.NUMBER, Type.REAGENT), Type.SCALED_REAGENT,
                              lambda n,r: ScaledReagent(n,r))

        fn = Functions["DIVIDE"]
        fn.infix_op("/")
        
        fn.register_all_immediate([((Type.FLOAT,Type.FLOAT), Type.FLOAT),
                                   ((Type.TIME,Type.FLOAT), Type.TIME),
                                   ((Type.TICKS,Type.FLOAT), Type.TICKS),
                                   ((Type.VOLUME,Type.FLOAT), Type.VOLUME),
                                   ], lambda x,y: x/y)
        fn.register_immediate((Type.LIQUID, Type.FLOAT), Type.LIQUID,
                              lambda liquid, split: Liquid(liquid.reagent, liquid.volume/split)
                              )

        # fn = Functions["TICKS"]
        # fn.postfix_op("ticks")
        # fn.register_immediate((Type.INT,), Type.TICKS, lambda n: n*ticks)
        
        fn = Functions["DROP_VOL"]
        fn.postfix_op("drops")
        fn.register((Type.FLOAT,), Type.VOLUME,
                    WithEnv(lambda env,n: n*env.board.drop_unit))

        fn = Functions["TURN-ON"]
        fn.register_immediate((), Type.TWIDDLE_OP, lambda: TwiddlePadValue.ON)
        fn = Functions["TURN-OFF"]
        fn.register_immediate((), Type.TWIDDLE_OP, lambda: TwiddlePadValue.OFF)
        fn = Functions["TOGGLE"]
        fn.register_immediate((), Type.TWIDDLE_OP, lambda: TwiddlePadValue.TOGGLE)
        
        fn = Functions["REMOVE-FROM-BOARD"]
        fn.register_immediate((), Type.MOTION, lambda: RemoveDropValue())
        
        fn = Functions["FIND_DROP"]
        fn.prefix_op("drop @")
        def new_drop(pad: Pad, liquid: Optional[Union[Liquid, Volume]] = None) -> Drop:
            if liquid is None:
                liquid = Liquid(unknown_reagent, pad.board.drop_size)
            elif isinstance(liquid, Volume):
                liquid = Liquid(unknown_reagent, liquid)
            else:
                # We copy the liquid, since the drop will adopt it.
                liquid = Liquid(liquid.reagent, liquid.volume)
            if pad.drop is not None:
                raise AlreadyDropError(f"There is already a drop at {pad}")
            pad.liquid_added(liquid)
            return not_None(pad.drop)
        fn.register_immediate((Type.PAD,), Type.DROP,
                              lambda p: p.drop or new_drop(p))
        
        fn = Functions["NEW_DROP"]
        fn.infix_op("@")
        fn.register_all_immediate([((Type.VOLUME, Type.PAD), Type.DROP),
                                   ((Type.LIQUID, Type.PAD), Type.DROP),
                                  ],
                                  lambda v,p: new_drop(p, v))
        
        fn = Functions["FIND_REAGENT"]
        fn.prefix_op("reagent named")
        fn.register_immediate((Type.STRING,), Type.REAGENT, lambda name: Reagent.find(name))
            
        fn = Functions["LIQUID"]
        fn.infix_op("of")
        fn.register_immediate((Type.VOLUME, Type.REAGENT), Type.LIQUID, lambda v,r: Liquid(r, v))
        
        fn = Functions["TURNED"]
        fn.postfix_op("turned")
        fn.register_immediate((Type.DIR,), Type.DIR, lambda d,t: d.turned(t))
        fn.register_immediate((Type.DELTA,), Type.DELTA, lambda d,t: d.turned(t))
        
        fn = Functions["COORD"]
        fn.format_type_expr_using(2, lambda x,y: f"({x}, {y})")
        def find_pad(env: Environment, x: int, y: int):
            board = env.board
            return board.pad_at(x, y)
        fn.register((Type.INT, Type.INT), Type.PAD, WithEnv(find_pad))
        
        fn = Functions["MIX"]
        def mix_reagent(*reagents: ScaledReagent) -> Reagent:
            parts,res = reagents[0]
            
            for m,r in reagents[1:]:
                ratio = parts/m
                res = Mixture.find_or_compute(res, r, ratio=ratio)
                parts += m
            return res
        fn.register_all_immediate([((Type.SCALED_REAGENT,)*n, Type.REAGENT) for n in range(1,8)], 
                                  mix_reagent)
        
    @classmethod
    def setup_special_vars(cls) -> None:
        name = "interactive reagent"
        def get_reagent(monitor: BoardMonitor) -> Reagent:
            return monitor.interactive_reagent
        def set_reagent(monitor: BoardMonitor, reagent: Reagent):
            monitor.interactive_reagent = reagent
        SpecialVars[name] = MonitorVariable(name, Type.REAGENT, getter=get_reagent, setter=set_reagent)
        
        name = "interactive volume"
        def get_volume(monitor: BoardMonitor) -> Volume:
            return monitor.interactive_volume
        def set_volume(monitor: BoardMonitor, volume: Volume):
            monitor.interactive_volume = volume
        SpecialVars[name] = MonitorVariable(name, Type.VOLUME, getter=get_volume, setter=set_volume)

        
DMFCompiler.setup_function_table()
DMFCompiler.setup_special_vars()

