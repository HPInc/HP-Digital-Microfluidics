from __future__ import annotations

from _collections import defaultdict
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic, Hashable, NamedTuple, Final, \
    Callable, Any, cast, Sequence, Union, Mapping, ClassVar, List, Tuple,\
    TYPE_CHECKING, overload, Iterator, NoReturn
import typing

from antlr4 import InputStream, CommonTokenStream, FileStream, ParserRuleContext, \
    Token
from antlr4.tree.Tree import TerminalNode

from DMFLexer import DMFLexer
from DMFParser import DMFParser
from DMFVisitor import DMFVisitor
from langsup.type_supp import Type, CallableType, Signature, Attr,\
    Rel, MaybeType, Func, PhysUnit, EnvRelativeUnit,\
    NumberedItem, CallableTypeKind, CallableValue, EvaluationError, MaybeError,\
    Val_, LoopExitType, ByNameCache, ExtraArgFunc, ExtraArgDelayedFunc
from mpam.device import Pad, Board, BinaryComponent, Well,\
    WellGate, WellPad, TemperatureControl, PowerSupply, PowerMode, Chiller,\
    Heater, System, DropLoc, ExtractionPoint, EC, Magnet, Fan
from mpam.drop import Drop, DropStatus
from mpam.paths import Path
from mpam.types import unknown_reagent, Liquid, Dir, Delayed, OnOff, Barrier, \
    Ticks, DelayType, Turn, Reagent, Mixture, Postable, MISSING, MissingOr,\
    not_Missing
from quantities.core import Unit, Dimensionality
from quantities.dimensions import Time, Volume, Temperature, Voltage
from erk.stringutils import map_str, conj_str
import math
from functools import reduce
from erk.basic import LazyPattern, not_None, assert_never, to_const
from re import Match
from threading import RLock
import re
from quantities.temperature import TemperaturePoint, abs_C
from quantities.SI import deg_C
from quantities.timestamp import Timestamp, time_in, time_now
import io
import logging

if TYPE_CHECKING:
    from mpam.monitor import BoardMonitor

logger = logging.getLogger(__name__)

Name_ = TypeVar("Name_", bound=Hashable)

T_ = TypeVar("T_")


class CompilationError(RuntimeError): ...

class MaybeNotSatisfiedError(EvaluationError): ...

class AlreadyDropError(EvaluationError): ...

class UninitializedVariableError(EvaluationError): ...

class NoSuchComponentError(EvaluationError):
    def __init__(self, kind: str, which: int, max_val: int) -> None:
        super().__init__(f"{kind} #{which} does not exist.  Max is {max_val}.")
        
class NoSuchPadError(EvaluationError):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(f"No pad at ({x}, {y}).")
        
class UnknownUnitDimensionError(CompilationError):
    unit: Final[Unit]
    dimensionality: Final[Dimensionality]
    
    def __init__(self, unit: Unit) -> None:
        dim = unit.dimensionality()
        super().__init__(f"Unit {unit} has unknown dimensionality {dim}.")
        self.unit = unit
        self.dimensionality = dim
        
class ErrorToPropagate(CompilationError):
    error: Final[Executable]
    
    def __init__(self, error: Executable) -> None:
        self.error = error
        
def error_check(fn: Callable[..., Val_]) -> Callable[..., MaybeError[Val_]]:
    def check(*args: Sequence[Any]) -> MaybeError[Val_]:
        first = args[0]
        if isinstance(first, EvaluationError):
            return first
        return fn(*args)
    return check

def error_check_delayed(fn: Callable[..., Delayed[Val_]]) -> Callable[..., Delayed[MaybeError[Val_]]]:
    def check(*args: Sequence[Any]) -> Delayed[MaybeError[Val_]]:
        first = args[0]
        if isinstance(first, EvaluationError):
            return Delayed.complete(first)
        # Well, *that's* a kludge
        return fn(*args).transformed(lambda x: x)
    return check

class ControlTransfer(EvaluationError): ...

class LoopExit(ControlTransfer):
    name: Final[Optional[str]]
    
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name
        
class MacroReturn(ControlTransfer):
    value: Final[Any]
    
    def __init__(self, value: Any) -> None:
        self.value = value
            

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
    
    def lookup(self, name: Name_) -> MissingOr[Val_]:
        scope = self.find_scope(name)
        return MISSING if scope is None else scope.mapping[name]
    
    def define(self, name: Name_, val: Val_) -> None:
        self.mapping[name] = val
        
    def defined_locally(self, name: Name_) -> bool:
        return name in self.mapping
    
    def __getitem__(self, name: Name_) -> Val_:
        val = self.lookup(name)
        if val is MISSING:
            scope: Optional[Scope[Name_, Val_]] = self
            defined: List[Name_] = []
            while scope is not None:
                defined.extend(scope.mapping.keys())
                scope = scope.parent
            defined.sort()
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
        
    def lookup(self, name: Name_) -> MissingOr[Val_]:
        return self.current.lookup(name)
    
    def define(self, name: Name_, val: Val_) -> None:
        return self.current.define(name, val)
    
    def defined_locally(self, name: Name_) -> bool:
        return self.current.defined_locally(name)
    
    def __getitem__(self, name: Name_) -> Val_:
        return self.current[name]
    
    def __setitem__(self, name: Name_, val: Val_) -> None:
        self.current[name] = val
        
    def push(self, initial: Optional[dict[Name_,Val_]] = None) -> StackPush:
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
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: # @UnusedVariable
        self.stack.current = self.old

class Value(NamedTuple):
    val_type: Type
    value: object
        
        
class Environment(Scope[str, Any]):
    board: Final[Board]

    @property
    def monitor(self) -> Optional[BoardMonitor]:
        system = self.board.system
        print(f"Monitor used is {system.monitor}")
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

class ControlScope:
    parent: Final[Optional[ControlScope]]
    visible_loops: Final[Sequence[str]]
    return_type: Final[Optional[Type]]
    
    @property
    def in_loop(self) -> bool:
        return len(self.visible_loops) > 0
    
    def __init__(self, *,
                 parent: Optional[ControlScope] = None,
                 return_type: Optional[Type] = None,
                 loop_name: Optional[str] = None) -> None:
        self.parent = parent
        self.return_type = (return_type if return_type is not None else 
                            parent.return_type if parent is not None
                            else None)
        parent_loops = () if parent is None else parent.visible_loops
        self.visible_loops = (() if return_type is not None 
                              else parent_loops if loop_name is None 
                              else (loop_name, *parent_loops))
        
    def in_named_loop(self, name: str) -> bool:
        return name in self.visible_loops
    
    def named_loop_level(self, name: str) -> int:
        return self.visible_loops.index(name)
        
    
class ControlScopeStack:
    top: ControlScope
    
    @property
    def return_ok(self) -> bool:
        return self.top.return_type is not None
    
    @property
    def return_type(self) -> Optional[Type]:
        return self.top.return_type
    
    @property
    def in_loop(self) -> bool:
        return self.top.in_loop
    
    def __init__(self) -> None:
        self.top = ControlScope()
        
    def in_named_loop(self, name: str) -> bool:
        return self.top.in_named_loop(name)
    
    def named_loop_index(self, name: str) -> int:
        return self.top.named_loop_level(name)
    
    def enter_macro(self, return_type: Type) -> CSPush:
        return CSPush(self, return_type=return_type)
    
    def enter_loop(self, *, name: Optional[str] = None) -> CSPush:
        if name is None:
            name = ""
        return CSPush(self, loop_name=name)
    
class CSPush:
    stack: Final[ControlScopeStack]
    scope: Final[ControlScope]
    old: Final[ControlScope]
    
    def __init__(self, stack: ControlScopeStack, *, 
                 return_type: Optional[Type] = None, loop_name: Optional[str] = None) -> None:
        self.stack = stack
        self.old = stack.top 
        self.scope = ControlScope(parent=stack.top, return_type=return_type, loop_name=loop_name)
        
    def __enter__(self) -> CSPush:
        self.stack.top = self.scope
        return self
        
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: # @UnusedVariable
        self.stack.top = self.old

    
class ComposedCallable(CallableValue):
    first: Final[CallableValue]
    second: Final[CallableValue]
    
    def __init__(self, 
                 first: CallableValue, 
                 second: CallableValue, *,
                 sig: Optional[Signature] = None) -> None:
        first_sig = first.sig
        second_sig = second.sig
        first_kind = CallableTypeKind.for_sig(first_sig)
        second_kind = CallableTypeKind.for_sig(second_sig)
        if sig is None:
            param_types = second_sig.param_types if first_kind is CallableTypeKind.ACTION else first_sig.param_types
            return_type = second_sig.return_type if second_kind is CallableTypeKind.TRANSFORM else first_sig.return_type
            sig = Signature.of(param_types, return_type)
        super().__init__(sig)
        self.first = first
        self.second = second
        assert second_kind is not CallableTypeKind.GENERAL, f"Injection target cannot be of GENERAL kind: {second}"
        required_type = Type.ANY if second_kind is CallableTypeKind.ACTION else second_sig.param_types[0]
        provided_type = (sig.param_types[0] if (sig.arity > 0
                                                and first_kind in (CallableTypeKind.ACTION, CallableTypeKind.MONITOR))
                         else first_sig.return_type)
        
        if first_kind is CallableTypeKind.ACTION:
            def provide(args: Sequence[Any]) -> Delayed[MaybeError[Any]]:
                val = None if provided_type is Type.NO_VALUE else args[0]
                return first.apply(()).transformed(error_check(to_const(val)))
        elif first_kind is CallableTypeKind.MONITOR:
            def provide(args: Sequence[Any]) -> Delayed[MaybeError[Any]]:
                assert(len(args) == 1)
                val = args[0]
                return first.apply((val,)).transformed(error_check(to_const(val)))
        else:
            def provide(args: Sequence[Any]) -> Delayed[MaybeError[Any]]:
                return first.apply(args)
        self.provide: Callable[[Sequence[Any]], Delayed[MaybeError[Any]]] = provide

        
        if second_kind is CallableTypeKind.ACTION:
            def inject(v: Any) -> Delayed[MaybeError[Any]]:
                return second.apply(()).transformed(error_check(to_const(v)))
        elif second_kind is CallableTypeKind.MONITOR:
            def inject(v: Any) -> Delayed[MaybeError[Any]]:
                injected = provided_type.checked_convert_to(required_type, v)
                return (error_check_delayed(lambda i: second.apply((i,)))(injected)
                        .transformed(error_check(to_const(v))))
                # return second.apply((injected,)).transformed(error_check(to_const(v)))
        elif second_kind is CallableTypeKind.TRANSFORM:
            def inject(v: Any) -> Delayed[MaybeError[Any]]:
                injected = provided_type.checked_convert_to(required_type, v)
                return error_check_delayed(lambda i: second.apply((i,)))(injected)                
                # return second.apply((injected,))
        else:
            assert_never(second_kind)
        self.inject: Callable[[Any], Delayed[MaybeError[Any]]] = inject
        
    
    def apply(self, args:Sequence[Any])->Delayed[MaybeError[Any]]:
        return self.provide(args).chain(error_check_delayed(self.inject))
        
    def __str__(self) -> str:
        return f"({self.first} : {self.second})"
    
    @classmethod
    def composed_type(cls, first: CallableType, second: CallableType) -> CallableType:
        first_kind = first.kind
        if first_kind is CallableTypeKind.ACTION:
            return second 
        second_kind = second.kind
        assert second_kind is not CallableTypeKind.GENERAL
        param_types = first.param_types
        return_type = second.return_type if second_kind is CallableTypeKind.TRANSFORM else first.return_type
        return CallableType.find(param_types, return_type)

    
class MotionValue(CallableValue):
    @abstractmethod
    def move(self, drop: Drop) -> Delayed[Drop]: ... # @UnusedVariable
    
    _sig: ClassVar[Signature] = Signature.of((Type.DROP,), Type.DROP)
    
    def __init__(self) -> None:
        super().__init__(self._sig)
    
    def apply(self, args:Sequence[Any])->Delayed[Drop]:
        self.check_arity(args)
        drop = args[0]
        assert isinstance(drop, Drop)
        return self.move(drop)
        
    
class DeltaValue(MotionValue):
    dist: Final[int]
    direction: Final[Dir]
    
    def __init__(self, dist: int, direction: Dir) -> None:
        super().__init__()
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
        super().__init__()
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
        super().__init__()
        self.dest = pad
        
    def move(self, drop:Drop)->Delayed[Drop]:
        path = Path.to_pad(self.dest)
        return path.schedule_for(drop)

class ToRowColValue(MotionValue):
    dest: Final[int]
    verticalp: Final[bool]
    
    def __init__(self, dest: int, verticalp: bool) -> None:
        super().__init__()
        self.dest = dest
        self.verticalp = verticalp
        
    def move(self, drop:Drop)->Delayed[Drop]:
        if self.verticalp:
            path = Path.to_row(self.dest)
        else:
            path = Path.to_col(self.dest)
        return path.schedule_for(drop)
    
class TwiddleBinaryValue(CallableValue):
    op: Final[BinaryComponent.ModifyState]
    
    ON: ClassVar[TwiddleBinaryValue]
    OFF: ClassVar[TwiddleBinaryValue]
    TOGGLE: ClassVar[TwiddleBinaryValue]
    
    _sig: ClassVar[Signature] = Signature.of((Type.BINARY_CPT,), Type.BINARY_STATE)
    
    def __init__(self, op: BinaryComponent.ModifyState) -> None:
        super().__init__(self._sig)
        self.op = op
        
    def apply(self, args:Sequence[Any])->Delayed[None]: 
        self.check_arity(args)
        bc = args[0]
        assert isinstance(bc, BinaryComponent)
        return self.op.schedule_for(bc).transformed(to_const(None))
    
    def __str__(self) -> str:
        if self is TwiddleBinaryValue.ON:
            return "ON"
        elif self is TwiddleBinaryValue.OFF:
            return "OFF"
        elif self is TwiddleBinaryValue.TOGGLE:
            return "TOGGLE"
        else:
            return f"Twiddle({self.op})"
    

TwiddleBinaryValue.ON = TwiddleBinaryValue(BinaryComponent.TurnOn)
TwiddleBinaryValue.OFF= TwiddleBinaryValue(BinaryComponent.TurnOff)
TwiddleBinaryValue.TOGGLE = TwiddleBinaryValue(BinaryComponent.Toggle)

class InjectableStatementValue(CallableValue):
    _default_sig: ClassVar[Signature] = Type.ACTION.sig
    
    def __init__(self, sig: Optional[Signature] = None) -> None:
        super().__init__(sig or self._default_sig)
    
    @abstractmethod
    def invoke(self) -> Delayed[MaybeError[None]]: ...

    def apply(self, args: Sequence[Any])->Delayed[MaybeError[None]]:
        self.check_arity(args)
        return self.invoke()
    
class BoundDelayedAction(InjectableStatementValue):
    name: Final[str]
    def __init__(self, fn: Callable[[], Delayed[MaybeError[Any]]], *, 
                 name: Optional[str] = None) -> None:
        super().__init__()
        self.fn = fn
        if name is None:
            name = f"BoundDelayedAction[{fn}]"
        self.name = name
        
    def invoke(self)->Delayed[MaybeError[None]]:
        return self.fn().transformed(error_check(to_const(None)))
    
    def __str__(self) -> str:
        return self.name
    
class BoundImmediateAction(BoundDelayedAction):
    def __init__(self, fn: Callable[[], Any], *,
                 name: Optional[str] = None):
        if name is None:
            name = f"BoundImmediateAction[{fn}]"
        super().__init__(lambda: Delayed.complete(fn()), name=name)
        
class PauseValue(InjectableStatementValue):
    duration: Final[DelayType]
    board: Final[Board]
    
    def __init__(self, duration: DelayType, board: Board) -> None:
        super().__init__()
        self.duration = duration
        self.board = board
        
    def __str__(self) -> str:
        return f"Pause({self.duration})"
        
    def invoke(self)->Delayed[None]:
        print(f"Pausing for {self.duration}")
        return self.board.delayed(lambda : None, after=self.duration)
    
class PromptValue(InjectableStatementValue):
    prompt: Final[Optional[str]]
    system: Final[System]
    
    def __init__(self, vals: Sequence[Any], board: Board) -> None:
        super().__init__()
        self.system = board.system
        prompt: Optional[str] = None
        if len(vals) > 0:
            output = io.StringIO()
            print(*vals, file=output, end="")
            prompt = output.getvalue()
            output.close()
        self.prompt = prompt
        
    def __str__(self) -> str:
        return f"Prompt({self.prompt})"
        
    def invoke(self)->Delayed[None]:
        future = Postable[None]()
        self.system.prompt_and_wait(future, prompt=self.prompt)
        return future
    
    

class MacroValue(CallableValue):
    param_names: Final[Sequence[str]]
    body: Final[Executable]
    static_env: Final[Environment]
    
    def __init__(self, mt: CallableType, env: Environment, param_names: Sequence[str], body: Executable) -> None:
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


Functions = ByNameCache[str, Func](lambda name: Func(name))
Attributes = ByNameCache[str, Attr](lambda name: Attr(Functions[f"'{name}' attribute"]))

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



BuiltIns = {
    "ceil": Functions["CEILING"],
    "floor": Functions["FLOOR"],
    "round": Functions["ROUND"],
    "unsafe_walk": Functions["UNSAFE"],
    "str": Functions["STRING"],
    "mixture": Functions["MIX"],
    "dispense drop": Functions["#dispense drop"],
    "enter well": Functions["#enter well"],
    "transfer in": Functions["#transfer in"],
    "transfer out": Functions["#transfer out"],
    "remove": Functions["#remove liquid"],
    "fill": Functions["fill"],
    "prepare to dispense": Functions["#prepare to dispense"]
    }

class SpecialVariable(Generic[T_]):
    var_type: Final[Type]
    
    @property
    def is_settable(self) -> bool:
        return self._setter is not None
    
    def __init__(self, var_type: Type, *,
                 getter: Callable[[Environment], T_],
                 setter: Optional[Callable[[Environment, T_], None]] = None,
                 allowed_vals: Optional[tuple[T_,...]] = None
                 ) -> None:
        
        self.var_type = var_type
        self._getter = getter
        self._setter = setter
        self.allowed_vals: Final = allowed_vals
    
    def get(self, env: Environment) -> T_:
        return (self._getter)(env)
    
    def set(self, env: Environment, val: T_) -> None:
        assert self._setter is not None
        (self._setter)(env, val)
        
class Constant(SpecialVariable[T_]):
    val: Final[Any]
    def __init__(self, var_type: Type, val: T_) -> None:
        super().__init__(var_type, getter = to_const(val))
        self.val = val
        
class MonitorVariable(SpecialVariable[T_]):
    def __init__(self, name: str, var_type: Type, *,
                 getter: Callable[[BoardMonitor], T_],
                 setter: Optional[Callable[[BoardMonitor, T_], None]] = None,
                 unmonitored_getter: Optional[Callable[[Environment], T_]] = None,
                 unmonitored_setter: Optional[Callable[[Environment, T_], None]] = None) -> None:
        def adapted_getter(env: Environment) -> Any:
            monitor = env.monitor
            if monitor is not None:
                return getter(monitor)
            if unmonitored_getter is not None:
                return unmonitored_getter(env)
            raise EvaluationError(f"Evaluating {name} only works in a monitored run")
        
        def adapted_setter(env: Environment, val: T_) -> None:
            monitor = env.monitor
            if setter is None:
                raise EvaluationError(f"Attempted to set immutable variable {name}")
            elif monitor is not None:
                setter(monitor, val)
            elif unmonitored_setter is not None:
                unmonitored_setter(env, val)  
            else:
                raise EvaluationError(f"Setting {name} only works in a monitored run")
        super().__init__(var_type, getter=adapted_getter, setter = setter and adapted_setter)
        
    
SpecialVars: dict[str, SpecialVariable] = {}
    
DimensionToType: dict[Dimensionality, tuple[Type, Type]] = {
    Time.dim(): (Type.TIME, Type.FLOAT),
    Volume.dim(): (Type.VOLUME, Type.FLOAT),
    Ticks.dim(): (Type.TICKS, Type.INT),
    Voltage.dim(): (Type.VOLTAGE, Type.FLOAT),
    }

AnyTemp = Union[Temperature, TemperaturePoint, "AmbiguousTemp"]
class AmbiguousTemp:
    absolute: Final[TemperaturePoint]
    relative: Final[Temperature]
    
    def __init__(self, absolute: TemperaturePoint, relative: Temperature) -> None:
        self.absolute = absolute
        self.relative = relative
    
    def __str__(self) -> str:
        return (f"Ambiguous[abs: {self.absolute}, rel: {self.relative}]")
    
    @overload
    def __add__(self, rhs: Union[Temperature, AmbiguousTemp]) -> AmbiguousTemp: ... # @UnusedVariable
    @overload
    def __add__(self, rhs: TemperaturePoint) -> TemperaturePoint: ... # @UnusedVariable
    def __add__(self, rhs: AnyTemp) -> AnyTemp:
        if isinstance(rhs, TemperaturePoint):
            return rhs+self.relative
        if not isinstance(rhs, Temperature):
            rhs = rhs.relative
        return AmbiguousTemp(self.absolute+rhs, self.relative+rhs)
    
    @overload
    def __radd__(self, lhs: Temperature) -> AmbiguousTemp: ... # @UnusedVariable
    @overload
    def __radd__(self, lhs: TemperaturePoint) -> TemperaturePoint: ... # @UnusedVariable
    def __radd__(self, lhs: Union[Temperature, TemperaturePoint]) -> AnyTemp:
        return self+lhs
        
        
    @overload
    def __sub__(self, rhs: TemperaturePoint) -> Temperature: ... # @UnusedVariable
    @overload
    def __sub__(self, rhs: Union[Temperature, AmbiguousTemp]) -> AmbiguousTemp: ... # @UnusedVariable
    def __sub__(self, rhs: AnyTemp) -> Union[Temperature, AmbiguousTemp]:
        if isinstance(rhs, TemperaturePoint):
            return self.absolute-rhs
        if not isinstance(rhs, Temperature):
            rhs = rhs.relative
        return AmbiguousTemp(self.absolute-rhs, self.relative-rhs)
    
    @overload
    def __rsub__(self, lhs: Temperature) -> Temperature: ... # @UnusedVariable
    @overload
    def __rsub__(self, lhs: TemperaturePoint) -> AmbiguousTemp: ... # @UnusedVariable
    def __rsub__(self, lhs: Union[Temperature, TemperaturePoint]) -> Union[Temperature, AmbiguousTemp]:
        if isinstance(lhs, Temperature):
            return lhs-self.relative
        return AmbiguousTemp(lhs-self.relative, lhs-self.absolute)
    
    
rep_types: Mapping[Type, Union[typing.Type, Tuple[typing.Type,...]]] = {
        Type.DROP: Drop,
        Type.INT: int,
        Type.FLOAT: float,
        Type.NUMBER: (float, int),
        Type.BINARY_STATE: OnOff,
        Type.ON: OnOff,
        Type.OFF: OnOff,
        Type.BINARY_CPT: BinaryComponent,
        Type.PAD: Pad,
        Type.WELL_PAD: WellPad,
        Type.WELL_GATE: WellGate,
        Type.PIPETTING_TARGET: (Well, ExtractionPoint),
        Type.WELL: Well,
        Type.EXTRACTION_POINT: ExtractionPoint,
        Type.DELTA: DeltaValue,
        Type.MOTION: MotionValue,
        Type.TIME: Time,
        Type.TICKS: Ticks,
        Type.DELAY: (Time, Ticks),
        Type.DIR: Dir,
        Type.BOOL: bool,
        Type.BUILT_IN: Func,
        Type.VOLUME: Volume,
        Type.LIQUID: Liquid,
        Type.STRING: str,
        Type.REAGENT: Reagent,
        Type.SCALED_REAGENT: ScaledReagent,
        Type.ABS_TEMP: TemperaturePoint,
        Type.REL_TEMP: Temperature,
        Type.AMBIG_TEMP: AmbiguousTemp,
        Type.TEMP_CONTROL: TemperatureControl,
        Type.HEATER: Heater,
        Type.CHILLER: Chiller,
        Type.BOARD: Board, 
        Type.POWER_SUPPLY: PowerSupply,
        Type.VOLTAGE: Voltage,
        Type.POWER_MODE: PowerMode,
        Type.MISSING: type(None),
   }

for t,reps in rep_types.items():
    t.set_rep_type(reps)

    
# Type.value_compatible((Type.TIME, Type.TICKS), Type.DELAY)
# Type.value_compatible((Type.INT, Type.FLOAT), Type.NUMBER)

Type.register_conversion(Type.DROP, Type.PAD, lambda drop: drop.pad)
Type.register_conversion(Type.EXTRACTION_POINT, Type.PAD, lambda ep: ep.pad)
# Type.register_conversion(Type.DROP, Type.BINARY_CPT, lambda drop: drop.pad)
Type.register_conversion(Type.INT, Type.FLOAT, float)
Type.register_conversion(Type.REAGENT, Type.SCALED_REAGENT, lambda r: ScaledReagent(1, r))
Type.register_conversion(Type.DIR, Type.DELTA, lambda d: DeltaValue(1, d))
# Type.register_conversion(Type.DIR, Type.MOTION, lambda d: DeltaValue(1, d))
Type.register_conversion(Type.AMBIG_TEMP, Type.ABS_TEMP, lambda t: t.absolute)
Type.register_conversion(Type.AMBIG_TEMP, Type.REL_TEMP, lambda t: t.relative)
Type.register_conversion(Type.ON, Type.TWIDDLE_OP, to_const(TwiddleBinaryValue.ON))
Type.register_conversion(Type.OFF, Type.TWIDDLE_OP, to_const(TwiddleBinaryValue.OFF))


class Executable:
    return_type: Final[Type]
    contains_error: Final[bool]
    const_val: Final[Any]
    
    def __init__(self, return_type: Type, func: Callable[[Environment], Delayed[Any]],
                 based_on: Sequence[Executable] = (),
                 *,
                 is_error: bool = False,
                 const_val: Any = MISSING,
                 ) -> None:
        self.return_type = return_type
        self.func: Final[Callable[[Environment], Delayed[Any]]] = func
        self.contains_error = is_error or any(e.contains_error for e in based_on)
        self.const_val = const_val
        
    @classmethod
    def constant(cls, return_type: Type, val: Any, based_on: Sequence[Executable] = (), *,
                 is_error: bool = False) -> Executable:
        return Executable(return_type, to_const(Delayed.complete(val)), 
                          based_on, is_error=is_error, const_val=val)
        
    def __str__(self) -> str:
        e = "ERROR, " if self.contains_error else ""
        c_or_f = f", {self.func}" if self.const_val is MISSING else f"= {self.const_val}"
        return f"Executable({e}{self.return_type}{c_or_f}"
    
    
    def evaluate(self, env: Environment, required: Optional[Type] = None) -> Delayed[Any]:
        if self.contains_error:
            raise EvaluationError(f"attempting to evaluate {self}")
        future: Delayed[Any]
        if self.const_val is not MISSING:
            future = Delayed.complete(self.const_val)
        else:
            fn = self.func
            future = fn(env)
        if required is not None and required is not self.return_type:
            req_type = required
            def convert(val: Any) -> Any:
                return self.return_type.checked_convert_to(req_type, val=val)
                # return Conversions.convert(have=self.return_type, want=req_type, val=val)
            future = future.transformed(convert)
        # if required is not None: 
        #     check = rep_types.get(required, None)
        #     if check is not None:
        #         assert isinstance(val, check), f"Expected {check}, got {val}"
        return future
    
    def check_and_eval(self, maybe_error: MaybeError, 
                       env: Environment, required: Optional[Type] = None) -> Delayed[Any]:
        if isinstance(maybe_error, EvaluationError):
            return Delayed.complete(maybe_error)
        return self.evaluate(env, required)
    
class LazyEval:
    Definition = Callable[[Environment, Sequence[Executable]], Delayed[Any]]
    def __init__(self, 
                 func: Definition) -> None:
        self.func = func
    
    def __call__(self, env: Environment, arg_execs: Sequence[Executable]) -> Delayed[Any]:
        fn = self.func
        return fn(env, arg_execs)

WithEnv = ExtraArgFunc[Environment]
WithEnvDelayed = ExtraArgDelayedFunc[Environment]

class LoopType(ABC):
    compiler: Final[DMFCompiler]
    
    def __init__(self, compiler: DMFCompiler) -> None:
        self.compiler = compiler
    
    @classmethod
    def for_context(cls, header: DMFParser.Loop_headerContext, *, compiler: DMFCompiler) -> LoopType:
        def not_implemented(kind: str) -> NoReturn:
            error = compiler.not_yet_implemented(kind, header)
            raise ErrorToPropagate(error)

        if isinstance(header, DMFParser.N_times_loop_headerContext):
            return NTimesLoopType(header, compiler=compiler)
        if isinstance(header, DMFParser.Duration_loop_headerContext):
            return ForDurationLoopType(header, compiler=compiler)
        if isinstance(header, DMFParser.Test_loop_headerContext):
            return BoolTestLoopType(header, compiler=compiler)
        if isinstance(header, DMFParser.Seq_iter_loop_headerContext):
            not_implemented("'With var in' loops")
        if isinstance(header, DMFParser.Step_iter_loop_headerContext):
            return StepIterLoopType(header, compiler=compiler)
        
        assert_never(header)
        
    # Override to push variables into the subcontext
    def compile_body(self, body: DMFParser.CompoundContext) -> Executable:
        return self.compiler.visit(body)
    
    # Override to add a new environment for control variables
    def header_env(self, env: Environment) -> Environment:
        return env
    
    @abstractmethod
    def based_on(self) -> Sequence[Executable]: ...
    
    @abstractmethod
    def test(self, env: Environment) -> Iterator[Delayed[MaybeError[bool]]]: # @UnusedVariable
        ...

class NTimesLoopType(LoopType):
    n_exec: Final[Executable]
    
    def __init__(self, header: DMFParser.N_times_loop_headerContext, *, compiler: DMFCompiler) -> None:
        super().__init__(compiler)
        self.n_exec = self.compiler.visit(header.n)
        if e := compiler.type_check(Type.INT, self.n_exec, header,
                                    lambda want,have,text:
                                      f"Counted loop expression must be of type {want}, was {have}: {text}"
                                      ):
            raise(ErrorToPropagate(e))
        
    def based_on(self)->Sequence[Executable]:
        return (self.n_exec,)
    
    def test(self, env: Environment) -> Iterator[Delayed[MaybeError[bool]]]:
        n_remaining: int
        def set_limit(n: int) -> bool:
            if n < 1:
                return False
            nonlocal n_remaining
            n_remaining = n-1 # @UnusedVariable
            return True
        yield self.n_exec.evaluate(env, Type.INT).transformed(error_check(set_limit))
        while n_remaining > 0:
            n_remaining -= 1
            yield Delayed.complete(True)
        yield Delayed.complete(False)
        
class BoolTestLoopType(LoopType):
    continue_on: Final[bool]
    cond_exec: Final[Executable]
    
    def __init__(self, header: DMFParser.Test_loop_headerContext, *, compiler: DMFCompiler) -> None:
        super().__init__(compiler)
        self.continue_on = header.WHILE() is not None
        cond_ctx = cast(DMFParser.ExprContext, header.cond)
        cond_exec = self.compiler.visit(cond_ctx)
        if e := compiler.type_check(Type.BOOL, cond_exec, header,
                                    lambda want,have,text:
                                      f"While/until loop condition must be of type {want}, was {have}: {text}"
                                      ):
            cond_exec = e
        self.cond_exec = cond_exec
        
    def based_on(self)->Sequence[Executable]:
        return (self.cond_exec,)
    
    def test(self, env: Environment) -> Iterator[Delayed[MaybeError[bool]]]:
        running = True
        
        def check(b: bool) -> bool:
            nonlocal running
            running = b == self.continue_on
            return running
        
        while running:
            yield self.cond_exec.evaluate(env, Type.BOOL).transformed(error_check(check))
        
class ForDurationLoopType(LoopType):
    duration_exec: Final[Executable]
    
    def __init__(self, header: DMFParser.Duration_loop_headerContext, *, compiler: DMFCompiler) -> None:
        super().__init__(compiler)
        duration_exec = self.compiler.visit(header.duration)
        if e := compiler.type_check(Type.TIME, duration_exec, header,
                                    lambda want,have,text:
                                      f"Timed loop expression must be of type {want}, was {have}: {text}"
                                      ):
            duration_exec = e
        self.duration_exec = duration_exec
        
    def based_on(self)->Sequence[Executable]:
        return (self.duration_exec,)
    
    def test(self, env: Environment) -> Iterator[Delayed[MaybeError[bool]]]:
        stop_at: Timestamp
        def set_limit(t: Time) -> bool:
            if t <= 0:
                return False
            nonlocal stop_at
            stop_at = time_in(t) # @UnusedVariable
            return True
        yield self.duration_exec.evaluate(env, Type.TIME).transformed(error_check(set_limit))
        while time_now() < stop_at:
            yield Delayed.complete(True)
        yield Delayed.complete(False)
        
class StepIterLoopType(LoopType):
    start_exec: Final[Optional[Executable]]
    stop_exec: Final[Executable]
    step_exec: Final[Executable]
    var_name: Final[str]
    var_type: Final[Type]
    new_var: Final[bool]
    downp: Final[bool]
    rel: Final[Rel]
    cmp_type: Final[Type]
    inc_sig: Final[Signature]
    
    def __init__(self, header: DMFParser.Step_iter_loop_headerContext, *, compiler: DMFCompiler) -> None:
        super().__init__(compiler)
        
        def raise_error(msg: str, ret_type: Type = Type.NO_VALUE) -> NoReturn:
            raise ErrorToPropagate(compiler.error(header, ret_type, f"{msg}: {compiler.text_of(header)}"))
        
        sfd = cast(DMFParser.Step_first_and_dirContext, header.first)
        self.downp = cast(bool, sfd.is_down)
        start_ctx: Optional[ParserRuleContext] = sfd.expr()
        self.start_exec = None if start_ctx is None else compiler.visit(start_ctx) 
        self.stop_exec = compiler.visit(header.bound)
        step: Optional[Executable] = None
        step_ctx: Optional[DMFParser.ExprContext] = header.step
        if (step_ctx):
            step = compiler.visit(step_ctx)
        else:
            # Needs to be done right
            step = Executable.constant(Type.INT, 1)
        self.step_exec = step
        
        # No idea why one of the mypy tests on GitHub (only on 3.9) is complaining about "Redundant cast to Union[Any,Any]"
        var_ctx = cast(Union[DMFParser.ParamContext, DMFParser.NameContext], header.var) # type: ignore [redundant-cast] 
        
        if isinstance(var_ctx, DMFParser.ParamContext):
            var_name, var_type = compiler.param_def(var_ctx)
            new_var = True
            if cast(bool, var_ctx.deprecated):
                compiler.decl_deprecated(var_ctx)
        elif isinstance(var_ctx, DMFParser.NameContext):
            var_name = cast(str, var_ctx.val)
            vt = compiler.current_types.lookup(var_name)
            if vt is not MISSING:
                var_type = vt
                new_var = False
            else: 
                if self.start_exec is None:
                    raise_error(f"'{var_name} not declared in loop header and not in surrounding context, and no start value was provided")
                var_type = self.start_exec.return_type
                new_var = True
                compiler.error(header, var_type, 
                               (f"'{var_name} not declared in loop header and not in surrounding context."
                                + f"  Assuming type {var_type} based on initial value of '{compiler.text_of(header.first)}'"))
        else:
            assert_never(var_ctx)
        self.var_name = var_name
        self.var_type = var_type
        self.new_var = new_var
        
        if self.start_exec is not None:
            start_type = self.start_exec.return_type
            if not start_type.can_convert_to(var_type):
                raise_error(f"Can't convert initial value ({start_type}) to {var_type}")
        self.rel = Rel.GE if self.downp else Rel.LE
        stop_type = self.stop_exec.return_type 
        cmp_type = self.rel.comparable_type(var_type, stop_type)
        if cmp_type is None:
            raise_error(f"Can't compare {var_name} ({var_type}) and stop value ({stop_type})")
        self.cmp_type = cmp_type
        fn = Functions["SUBTRACT" if self.downp else "ADD"]
        step_type = self.step_exec.return_type
        maybe_sig_inc = fn[(var_type, step_type)]
        if maybe_sig_inc is None:
            verb = "decrement" if self.downp else "increment"
            raise_error(f"Can't {verb} {var_name} ({var_type}) by {step_type}")
            
        sig, inc = maybe_sig_inc
        inc_type = sig.return_type
        if not inc_type.can_convert_to(var_type):
            verbing = "decrementing" if self.downp else "incrementing"
            raise_error(f"Result of {verbing} {var_name} ({var_type}) by {step_type} ({inc_type}) not assignable to variable")
        
        self.inc: Final[Callable[[Any,Any], Delayed[Any]]] = inc
        self.inc_sig = sig
         
    def based_on(self)->Sequence[Executable]:
        if self.start_exec is None:
            return (self.stop_exec, self.step_exec)
        else:
            return (self.start_exec, self.stop_exec, self.step_exec)
    
    def compile_body(self, body:DMFParser.CompoundContext)->Executable:
        if self.new_var:
            with self.compiler.current_types.push({self.var_name: self.var_type}):
                return self.compiler.visit(body)
        return self.compiler.visit(body)
    
    def header_env(self, env:Environment)->Environment:
        return env.new_child()
    
    def test(self, env: Environment) -> Iterator[Delayed[MaybeError[bool]]]:
        stop_val: Any
        step_val: Any
        next_val: Any
        var_name = self.var_name
        var_type = self.var_type
        cmp_type = self.cmp_type
        inc_sig = self.inc_sig
        inc_var_type = inc_sig.param_types[0]
        inc_ret_type = inc_sig.return_type
        inc = self.inc
        running = True
        var_scope = env if self.new_var else not_None(env.find_scope(var_name))
        
        
        def note_next(val: Any, val_type: Type) -> None:
            nonlocal next_val
            next_val = val_type.convert_to(var_type, val) # @UnusedVariable

        def set_stop(val: Any) -> None:
            nonlocal stop_val
            stop_val = val # @UnusedVariable

        def set_step(val: Any) -> None:
            nonlocal step_val
            step_val = val # @UnusedVariable

        def test(ignored: None) -> bool:
            nonlocal running
            if not running:
                return False
            running = self.rel.test(var_type.convert_to(cmp_type, next_val), stop_val)
            if running:
                var_scope.define(var_name, next_val)
            return running
            
        def increment() -> Delayed[MaybeError[None]]:
            return (inc(var_type.convert_to(inc_var_type, var_scope[var_name]), step_val)
                    .transformed(error_check(lambda v: note_next(v, inc_ret_type)))
                    )

        initialize: Delayed[MaybeError[None]]
        if self.start_exec is None:        
            next_val = var_scope.lookup(var_name)
            if next_val is MISSING:
                yield(Delayed.complete(EvaluationError(f"'repeat with' loop has no initial value, and loop variable {var_name} has not yet been assigned.")))
            initialize = Delayed.complete(None)
        else:
            initialize = self.start_exec.evaluate(env, var_type).transformed(error_check(lambda v: note_next(v, var_type)))
        yield (initialize
               .chain(lambda v: self.stop_exec.check_and_eval(v, env, cmp_type)).transformed(error_check(set_stop))
               .chain(lambda v: self.step_exec.check_and_eval(v, env, inc_sig.param_types[1])).transformed(error_check(set_step))
               .transformed(error_check(test))
               )
        
        while running:
            yield (increment().transformed(error_check(test)))

    
class DMFInterpreter:
    globals: Final[Environment]
    namespace: Final[TypeMap]
    
    def __init__(self, file_names: Sequence[str], *, board: Board, encoding: str='ascii', errors: str='strict') -> None:
        self.globals = Environment(None, board=board)
        self.namespace = TypeMap(None)
        for file_name in file_names:
            print(f"Loading macro file '{file_name}'")
            parser = self.get_parser(FileStream(file_name, encoding, errors))
            tree = parser.macro_file()
            assert isinstance(tree, DMFParser.Macro_fileContext)
            compiler = DMFCompiler(global_types = self.namespace, interactive = False)
            executable = compiler.visit(tree)
            assert isinstance(executable, Executable)
            if executable.contains_error:
                print(f"Macro file '{file_name}' contained error, not loading.")
            else:
                val = executable.evaluate(self.globals).value
                if isinstance(val, EvaluationError):
                    print(f"Exception caught while loading '{file_name}': {val}")
        
    def set_global(self, name: str, val: Any, vtype: Type) -> None:
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
        def munge_result(val: Any) -> Tuple[Type, Any]:
            t = Type.ERROR if isinstance(val, EvaluationError) else executable.return_type
            return (t, val)
        return future.transformed(munge_result)
    
    def get_parser(self, input_stream: InputStream) -> DMFParser:
        lexer = DMFLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DMFParser(stream)
        return parser
    

class DMFCompiler(DMFVisitor):
    global_types: Final[TypeMap]
    current_types: Final[ScopeStack[str, Type]]
    control_stack: Final[ControlScopeStack]
    interactive: Final[bool]
    
    default_creators = defaultdict[Type,Callable[[Environment],Any]](lambda: to_const(None),
                                                          {Type.INT: to_const(0),
                                                           Type.FLOAT: to_const(0.0),
                                                           Type.PAD: lambda env: env.board.pad_at(0,0),
                                                           Type.TIME: to_const(Time.ZERO),
                                                           Type.VOLUME: to_const(Volume.ZERO),
                                                           Type.TICKS: to_const(Ticks.ZERO),
                                                           Type.VOLTAGE: to_const(Voltage.ZERO),
                                                          })
    
    def __init__(self, *,
                 interactive: bool,
                 global_types: Optional[TypeMap] = None) -> None:
        self.interactive = interactive
        self.global_types = global_types if global_types is not None else TypeMap(None)
        self.current_types = ScopeStack(self.global_types)
        self.control_stack = ControlScopeStack()
        
    def defaultResult(self) -> Executable:
        print("Unhandled tree")
        return Executable.constant(Type.ERROR, None, is_error=True)
        # assert False, "Undefined visitor method"
        
    def visitChildren(self, node: Any) -> Executable:
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
        print(f"ERROR: line {ctx.start.line}:{ctx.start.column} {msg}")
        return self.error_val(return_type, value)

    def print_warning(self, 
                      ctx: ParserRuleContext, 
                      msg: Union[str, Callable[[str], str]]) -> None:
        if not isinstance(msg, str):
            msg = msg(self.text_of(ctx))
        print(f"WARNING: line {ctx.start.line}:{ctx.start.column} {msg}")
        
    
    def not_yet_implemented(self,
                            kind: str,
                            ctx: ParserRuleContext,
                            *, 
                            return_type: Type = Type.NO_VALUE,
                            value: Optional[Callable[[Environment], Any]] = None
                            ) -> Executable:
        msg = f"{kind} not yet implemented"
        return self.error(ctx, return_type, msg, value=value)
    
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

    def decl_deprecated(self, pc: DMFParser.ParamContext) -> Executable:
        return self.error(pc, cast(Type,pc.type), 
                          lambda text: f"'NAME: TYPE' declarations are deprecated.  Use 'TYPE NAME': {text}")


        
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
        if isinstance(t, MaybeType):
            t = t.if_there_type
        # t: Type = cast(Type, ctx.type)
        index = "" if n is None else f"_{n}"
        return f"**{t.name}{index}**"
        

    def type_check(self, 
                   want: Union[Type,Sequence[Type]],
                   have: Union[Type,Executable],
                   ctx: ParserRuleContext, 
                   msg: Optional[Union[str, Callable[[str, str, str], str]]] = None,
                   *,
                   return_type: Type = Type.NO_VALUE,
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
        # if what we have is Type.NO_VALUE, we've already found something we can't recover from,
        # so we don't bother with a message
        
        # Should that be Type.ERROR?
        if have is Type.NO_VALUE:
            return self.error_val(return_type, value)
        m: Union[str, Callable[[str], str]]
        if isinstance(msg, str):
            m = msg
        else:
            if msg is None:
                msg = lambda want,have,text: f"Expected {want}, got {have}: {text}"
            msg_fn = msg
            h = have
            def msg_factory(text: str) -> str:
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
            return self.error(attr_ctx, ret_type or Type.NO_VALUE,
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
        return self.error(ctx, Type.NO_VALUE,
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
                def stash_arg(arg: Any) -> Any:
                    args.append(arg)
                    return arg
                def make_lambda(ae: Executable, pt: Type) -> Callable[[Any], Delayed]:
                    return lambda maybe_error: (ae.check_and_eval(maybe_error, env,pt)
                                                .transformed(stash_arg))
                lambdas = [make_lambda(ae,pt) for ae,pt in zip(arg_execs, sig.param_types)]
                future = (Delayed.complete(None) if len(arg_execs) == 0
                          else reduce(lambda fut,fn: fut.chain(fn),
                                      lambdas[1:],
                                      lambdas[0](None)))
                def chain_call(maybe_error: MaybeError) -> Delayed[Any]:
                    if isinstance(maybe_error, EvaluationError):
                        return Delayed.complete(maybe_error)
                    else:
                        try:
                            if isinstance(fn, (ExtraArgFunc, ExtraArgDelayedFunc)):
                                return fn(env, *args, *extra_args)
                            else:
                                return fn(*args, *extra_args)
                        except EvaluationError as ex:
                            return Delayed.complete(ex)
                return future.chain(chain_call)
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
        will_inject = self.get_injected_type_annotation(ctx)
        if will_inject is None:
            desc = func[arg_types]
        else:
            desc = func.for_injection(arg_types, will_inject)
        if desc is None:
            rt = func.error_type(arg_types)
            # Don't bother to report an error if an arg already did and we don't know
            # what type it would have returned.
            real_func = func
            for ae in arg_execs:
                if ae.return_type is Type.NO_VALUE and ae.contains_error:
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
    
    def visit(self, tree: Any) -> Executable:
        return cast(Executable, DMFVisitor.visit(self, tree))

    def visitMacro_file(self, ctx:DMFParser.Macro_fileContext) -> Executable:
        stats: Sequence[Executable] = [self.visit(tls) for tls in ctx.stat()] 
        def run(env: Environment) -> Delayed[None]:
            if len(stats) == 0:
                return Delayed.complete(None)
            future: Delayed[Any] = stats[0].evaluate(env)
            for stat in stats[1:]:
                def evaluator(s: Executable) -> Callable[[MaybeError], Delayed[Any]]:
                    return lambda maybe_error: s.check_and_eval(maybe_error, env)
                future = future.chain(evaluator(stat))
            return future
        return Executable(Type.NO_VALUE, run, stats)


    def visitCompound_interactive(self, ctx:DMFParser.Compound_interactiveContext) -> Executable:
        return self.visit(ctx.compound())
    
    def visitLoop_interactive(self, ctx:DMFParser.LoopContext) -> Executable:
        return self.visit(ctx.loop())


    # def visitAssignment_interactive(self, ctx:DMFParser.Assignment_interactiveContext) -> Executable:
    #     return self.visit(ctx.assignment())

    def visitDecl_interactive(self, ctx:DMFParser.Decl_interactiveContext) -> Executable:
        return self.visit(ctx.declaration())


    def exprAsStatement(self, ctx: DMFParser.ExprContext) -> Executable:
        ex = self.visit(ctx)
        rt = ex.return_type
        if (isinstance(rt, CallableType) 
            and rt.kind is CallableTypeKind.ACTION 
            and not isinstance(ctx, (DMFParser.Name_assign_exprContext,
                                     DMFParser.Attr_assign_exprContext))):
            def doit(fn: InjectableStatementValue) -> Delayed[MaybeError[None]]:
                # logger.info(f"Invoking {ex.return_type}: {fn}")
                return fn.apply(())
                                                              
            def run(env: Environment) -> Delayed[MaybeError[None]]:
                return (ex.evaluate(env)
                        .chain(error_check_delayed(doit)))
            return Executable(Type.NO_VALUE, run, (ex,))
        return ex

    def visitExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext) -> Executable:
        return self.exprAsStatement(ctx.expr())
    
    def visitEmpty_interactive(self, ctx:DMFParser.Empty_interactiveContext) -> Executable: # @UnusedVariable
        return Executable.constant(Type.IGNORE, None)

    
    # def visitAssignment_tls(self, ctx:DMFParser.Assignment_tlsContext) -> Executable:
    #     return self.visit(ctx.assignment())
    #
    # def visitMacro_def_tls(self, ctx:DMFParser.Macro_def_tlsContext) -> Executable:
    #     return 0

    injected_type_annotation: Final = "_injected_type_"
    
    def get_injected_type_annotation(self, ctx: DMFParser.ExprContext) -> Optional[Type]:
        return getattr(ctx, self.injected_type_annotation, None)

    def set_injected_type_annotation(self, ctx: DMFParser.ExprContext, t: Type) -> None:
        setattr(ctx, self.injected_type_annotation, t)
    


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
            allowed = special.allowed_vals
            if allowed is not None:
                const_val = value.const_val
                if len(allowed) == 0:
                    if const_val is MISSING:
                        return self.error(ctx, value.return_type,
                                          f"Value assigned to special variable '{name}' must be a constant")
                elif const_val not in allowed:
                    if len(allowed) == 1: 
                        options = str(allowed[0])
                    else:
                        options = f"one of {conj_str(allowed)}"
                    return self.error(ctx, value.return_type,
                                      f"Value assigned to special variable '{name}' must be {options}")
                    ...
            spec = special
            setter = lambda env,val: spec.set(env, val)
            new_decl = False
        else:
            vt = self.current_types.lookup(name)
            if vt is MISSING:
                new_decl = True
                var_type = value.return_type
                if var_type < Type.BINARY_STATE:
                    var_type = Type.BINARY_STATE
                if not self.current_types.is_top_level:
                    self.print_warning(ctx, lambda text: f"Undeclared variable '{name}' assigned to in local scope: {text}")
            else:
                var_type = vt
                new_decl = False
            def do_assignment(env: Environment, val: Any) -> None:
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
            def do_assignment(val: Any) -> Any:
                if not isinstance(val, EvaluationError):
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
                otn = obj.return_type.name
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
            def do_assignment(o: Any, v: Any) -> Any:
                if not isinstance(v, EvaluationError):
                    setter(o,v)
                return v
            
            return (obj.evaluate(env, ot) 
                        .chain(lambda o: value.check_and_eval(o, env, vt)
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
        just_assign = not has_local_kwd and value is not None and self.current_types.lookup(name) is not MISSING

        if var_type is None:
            assert value is not None
            var_type = value.return_type
            if var_type < Type.BINARY_STATE:
                var_type = Type.BINARY_STATE     
        builtin = BuiltIns.get(name, None)
        if builtin is not None:
            return self.error(ctx, var_type, 
                              lambda text: f"Can't declare variable shadowing built-in '{name}': {text}")
        if name in SpecialVars:
            return self.error(ctx, var_type, 
                              lambda text: f"Can't declare variable shadowing special variable '{name}': {text}")
        if not just_assign and self.current_types.defined_locally(name):
            old_type = not_Missing(self.current_types.lookup(name)).name
            new_type = var_type.name
            if old_type is not new_type:
                return self.error(ctx, var_type, 
                                  lambda text: f"{name} redeclared as {new_type}, was {old_type}: {text}")
            self.print_warning(ctx, lambda text: f"{name} already declared in scope: {text}")
            just_assign = True
        if (value is None or not value.contains_error) and not just_assign:
            self.current_types.define(name, var_type)            

        if value is None:
            # Declaration only
            def do_decl(env: Environment) -> Delayed[None]:
                env.define(name, MISSING)
                return Delayed.complete(None)
            return Executable(Type.NO_VALUE, do_decl)
            
        if e := self.type_check(var_type, value.return_type, ctx, 
                                lambda want,have,text: 
                                    f"variable '{name}' has type {want}.  Expression has type {have}: {text}",
                                return_type=var_type):
            return e
        
        real_val = value
        def run(env: Environment) -> Delayed[Any]:
            def do_assignment(val: Any) -> Any:
                if isinstance(val, EvaluationError):
                    return val
                if just_assign:
                    env[name] = val
                else:
                    env.define(name, val)
                return val
            return real_val.evaluate(env, var_type).transformed(do_assignment)
        return Executable(var_type, run, (value,))

    def visitDecl_stat(self, ctx:DMFParser.Decl_statContext) -> Executable:
        return self.visit(ctx.declaration())
    
    def visitPrint_expr(self, ctx:DMFParser.Print_exprContext) -> Executable:
        arg_text = (self.text_of(c) for c in ctx.vals)
        def print_vals(*vals: Sequence[Any]) -> Delayed[BoundImmediateAction]:
            def do_print() -> None:
                print(*vals)
            name = f"print({', '.join(arg_text)})"
            return Delayed.complete(BoundImmediateAction(do_print, name = name))
        vals = tuple(self.visit(c) for c in ctx.vals)
        sig = Signature.of(tuple(v.return_type for v in vals), Type.ACTION)
        return self.use_callable(print_vals, vals, sig)
        
    # def visitPrint_stat(self, ctx:DMFParser.Print_statContext) -> Executable:
    #     return self.visit(ctx.printing())
    #
    # def visitPrint_interactive(self, ctx:DMFParser.Print_statContext) -> Executable:
    #     return self.visit(ctx.printing())

    # def visitPause_stat(self, ctx:DMFParser.Pause_statContext) -> Executable:
    #     duration = self.visit(ctx.duration)
    #     if e:=self.type_check(Type.DELAY, duration, ctx.duration,
    #                           lambda want,have,text: # @UnusedVariable
    #                             f"Delay ({have} must be time or ticks: {text}",
    #                           return_type=Type.PAUSE):
    #         return e
    #     def run(env: Environment) -> Delayed[MaybeError[None]]:
    #         def pause(d: DelayType, env: Environment) -> Delayed[None]:
    #             print(f"Delaying for {d}")
    #             return env.board.delayed(lambda: None, after=d)
    #         return (duration.evaluate(env, Type.DELAY)
    #                 .chain(lambda d: error_check_delayed(pause)(d, env)))
    #     return Executable(Type.PAUSE, run, (duration,))
    

    def visitExpr_stat(self, ctx:DMFParser.Expr_statContext) -> Executable:
        return self.exprAsStatement(ctx.expr())

    def visitCompound_stat(self, ctx:DMFParser.Compound_statContext) -> Executable:
        return self.visit(ctx.compound())


    def visitBlock(self, ctx:DMFParser.BlockContext) -> Executable:
        stat_contexts: Sequence[DMFParser.StatContext] = ctx.stat()
        with self.current_types.push():
            stat_execs = tuple(self.visit(sc) for sc in stat_contexts)
            
        ret_type = Type.NO_VALUE
        
        for i in range(len(stat_execs)):
            if ret_type.is_control:
                self.print_warning(stat_contexts[i], lambda txt: f"Statement is unreachable, ignoring: {txt}") # @UnusedVariable
                stat_execs = stat_execs[:i]
                break
            rt = stat_execs[i].return_type
            if rt.is_control:
                ret_type = rt

        def run(env: Environment) -> Delayed[MaybeError[None]]:
            if len(stat_execs) == 0:
                return Delayed.complete(None)
            local_env = env.new_child()
            if len(stat_execs) == 1:
                return stat_execs[0].evaluate(local_env)
            def execute(maybe_error: MaybeError, i: int) -> Delayed[MaybeError[None]]:
                # print(f"***Executing {self.text_of(stat_contexts[i])}")
                return stat_execs[i].check_and_eval(maybe_error, local_env)
            
            future = execute(None, 0)
            for i in range(1, len(stat_execs)):
                # We have to do something like this to ensure that each lambda gets a different i
                def executor(j: int) -> Callable[[Any], Delayed[MaybeError[None]]]:
                    return lambda maybe_error: execute(maybe_error, j)
                # print(f"Scheduling {self.text_of(stat_contexts[i])}")
                future = future.chain(executor(i))
            return future
        return Executable(ret_type, run, stat_execs)


    _par_block_error_lock = RLock()

    def visitPar_block(self, ctx:DMFParser.Par_blockContext) -> Executable:
        stat_contexts: Sequence[DMFParser.StatContext] = ctx.stat()
        with self.current_types.push():
            stat_execs = tuple(self.visit(sc) for sc in stat_contexts)
            
        
        rts = [ex.return_type for ex in stat_execs]
        ret_type = (Type.MACRO_RETURN if Type.MACRO_RETURN in rts
                    else Type.UNNAMED_LOOP_EXIT if Type.UNNAMED_LOOP_EXIT in rts
                    else Type.NO_VALUE)
        # If we're NO_VALUE, we may still have named loop exits.  We need to
        # pick the narrowest.
        if ret_type is Type.NO_VALUE:
            named_loop_exits = [t for t in rts if isinstance(t, LoopExitType)]
            if named_loop_exits:
                ret_type = named_loop_exits[0]
                for let in named_loop_exits[1:]:
                    if let.nested_levels < ret_type.nested_levels:
                        ret_type = let
                
        
        def run(env: Environment) -> Delayed[MaybeError[None]]:
            if len(stat_execs) == 0:
                return Delayed.complete(None)
            local_env = env.new_child()
            if len(stat_execs) == 1:
                return stat_execs[0].evaluate(local_env)
            barrier = Barrier[Any](required = len(stat_execs))
            error: MaybeError[None] = None
            trigger_future = Postable[MaybeError[None]]()
            barrier.wait(None, trigger_future)
            future = trigger_future.transformed(lambda _: error)
            def note_error(ex: EvaluationError) -> None: 
                nonlocal error
                first = False
                with self._par_block_error_lock:
                    if error is None:
                        first = True
                        error = ex
                if first:
                    # Firing the barrier will post the trigger_future, which
                    # will cause future to return the error we just set. It
                    # will fire again when all the statements reach it, but
                    # nobody will be waiting.
                    barrier.fire()
                else:
                    if not isinstance(ex, ControlTransfer):
                        print(f"Uncaught error in parallel block ({type(ex).__name__}): {ex}")
            
            with env.board.system.batched():
                def reach_barrier(maybe_error: MaybeError[None]) -> None:
                    if isinstance(maybe_error, EvaluationError):
                        note_error(maybe_error)
                    barrier.reach(maybe_error)
                for se in stat_execs:
                    se.evaluate(local_env).then_call(reach_barrier)
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

        # result_type: Optional[Type] = None
        # def check_result_type(t: Type) -> bool:
        #     nonlocal result_type
        #     if result_type is None or self.compatible(result_type, t):
        #         result_type = t
        #         return False
        #     result_type = Type.NONE
        #     return True
        
        if else_body is None:
            result_type = Type.NO_VALUE
            children = (*tests, *bodies)
        else:
            else_type = else_body.return_type
            children = (*tests, *bodies, else_body)
            result_type = Type.upper_bound(else_type, *(b.return_type for b in bodies))
            
            # for b in bodies:
            #     if check_result_type(b.return_type):
            #         break
                

        def run(env: Environment) -> Delayed:
            n_tests = len(tests)
            def check(i: int) -> Delayed:
                if i == n_tests:
                    if else_body is None:
                        return Delayed.complete(None)
                    else:
                        return else_body.evaluate(env, result_type)
                    
                def next_try(v: bool) -> Delayed:
                    if v:
                        return bodies[i].evaluate(env, result_type)
                    else:
                        return check(i+1)
                return tests[i].evaluate(env, Type.BOOL).chain(error_check_delayed(next_try))
            return check(0)
        
        
        return Executable(result_type, run, children)
    
    
    # def visitN_times_loop_header(self, ctx:DMFParser.N_times_loop_headerContext) -> Executable:
    #     return self.not_yet_implemented("n-times loop", ctx)
    #
    # def visitDuration_loop_header(self, ctx:DMFParser.Duration_loop_headerContext) -> Executable:
    #     return self.not_yet_implemented("duration loop", ctx)
    #
    # def visitWhile_loop_header(self, ctx:DMFParser.While_loop_headerContext) -> Executable:
    #     return self.not_yet_implemented("while loop", ctx)
    #
    # def visitUntil_loop_header(self, ctx:DMFParser.Until_loop_headerContext) -> Executable:
    #     return self.not_yet_implemented("until loop", ctx)
    #
    # def visitSeq_iter_loop_header(self, ctx:DMFParser.Seq_iter_loop_headerContext) -> Executable:
    #     return self.not_yet_implemented("sequence iteration loop", ctx)
    #
    # def visitStep_iter_loop_header(self, ctx:DMFParser.Step_iter_loop_headerContext) -> Executable:
    #     return self.not_yet_implemented("step iteration loop", ctx)
    
    def visitLoop_stat(self, ctx:DMFParser.Loop_statContext) -> Executable:
        return self.visit(ctx.loop())

    def visitLoop(self, ctx:DMFParser.LoopContext) -> Executable:
        header = cast(DMFParser.Loop_headerContext, ctx.header)
        body = cast(DMFParser.CompoundContext, ctx.body)
        try:
            loop_type = LoopType.for_context(header, compiler=self)
        except ErrorToPropagate as ex:
            return ex.error
        name_ctx: Optional[DMFParser.NameContext] = ctx.loop_name
        name = None if name_ctx is None else cast(str, name_ctx.val)
        with self.control_stack.enter_loop(name=name):
            body_exec = loop_type.compile_body(body)
            
        return_type = body_exec.return_type
        # An exit from this loop (unnamed or one that matches our name) turns
        # into a NO_VALUE for the loop as a whole.  Any other exit makes the
        # entire loop be an exit.
        if isinstance(return_type, LoopExitType):
            levels = return_type.nested_levels
            return_type = Type.NO_VALUE if levels == 0 else LoopExitType.for_level(levels-1)
        def run(env: Environment) -> Delayed[MaybeError[None]]:
            env = loop_type.header_env(env)
            test_iter = loop_type.test(env)
            
            
            def do_pass(prev: MaybeError[None]) -> Delayed[MaybeError[None]]:
                if isinstance(prev, LoopExit):
                    exited_loop_name = prev.name
                    # print(f"Exiting loop named '{exited_loop_name}'.  Our name is '{name}'")
                    if exited_loop_name is None or exited_loop_name == name:
                        return Delayed.complete(None)
                # Note: This will catch loop exits for enclosing loops.
                if isinstance(prev, EvaluationError):
                    return Delayed.complete(prev)
                test_val = next(test_iter)
                def check(b: MaybeError[bool]) -> Delayed[MaybeError[None]]:
                    if isinstance(b, EvaluationError):
                        return Delayed.complete(b)
                    if not b:
                        return Delayed.complete(None)
                    return body_exec.evaluate(env).chain(do_pass)
                return test_val.chain(check)
            return do_pass(None)
            
        return Executable(return_type, run, (*loop_type.based_on(), body_exec))
    

    def visitExit_stat(self, ctx:DMFParser.Exit_statContext) -> Executable:
        return self.visit(ctx.exit())
    
    def visitExit(self, ctx:DMFParser.ExitContext) -> Executable:
        name_ctx: Optional[DMFParser.NameContext] = ctx.loop_name
        name = None if name_ctx is None else cast(str, name_ctx.val)
        if not self.control_stack.in_loop:
            return self.error(ctx, Type.NO_VALUE, "Loop exit statement not within loop")
        if name is not None and not self.control_stack.in_named_loop(name):
            return self.error(ctx, Type.UNNAMED_LOOP_EXIT, f"Not within loop named '{name}'")
        if name is None:
            ret_type = Type.UNNAMED_LOOP_EXIT
        else:
            n = self.control_stack.named_loop_index(name)
            ret_type = LoopExitType.for_level(n)
        return Executable.constant(ret_type, LoopExit(name))
        
    def visitReturn_stat(self, ctx:DMFParser.Return_statContext) -> Executable:
        return self.visit(ctx.ret())
    
    def visitRet(self, ctx:DMFParser.RetContext) -> Executable:
        value_ctx: Optional[DMFParser.ExprContext] = ctx.expr()
        return_type = self.control_stack.return_type
        if return_type is None:
            return self.error(ctx, Type.NO_VALUE, "Return statement not within macro")

        if value_ctx is None:
            if return_type is not Type.NO_VALUE:
                return self.error(ctx, Type.NO_VALUE, 
                                  f"No value on return statement.  Expected {return_type.name}.")
            return Executable.constant(Type.NO_VALUE, MacroReturn(None))
        value = self.visit(value_ctx)
        val_type = value.return_type

        if return_type is Type.NO_VALUE:
            return self.error(ctx, Type.MACRO_RETURN, 
                              lambda txt: f"Returning value of type {val_type.name} from macro that does not return a value: {txt}")
            
        if e := self.type_check(return_type, val_type, value_ctx,
                                lambda want,have,text:
                                    f"Returned value must be of type {want}, was {have}: {text}",
                                return_type = Type.MACRO_RETURN):
            return e
        
        def run(env: Environment) -> Delayed[MaybeError[Any]]:
            return value.evaluate(env, return_type).transformed(error_check(MacroReturn))
        return Executable(Type.MACRO_RETURN, run, (value,))
        
    
        
    def visitParen_expr(self, ctx:DMFParser.Paren_exprContext) -> Executable:
        return self.visit(ctx.expr())


    def visitNeg_expr(self, ctx:DMFParser.Neg_exprContext) -> Executable:
        return self.use_function("NEGATE", ctx, (ctx.rhs,))


    def visitInt_expr(self, ctx:DMFParser.Int_exprContext) -> Executable:
        val: int = int(ctx.INT().getText())
        return Executable.constant(Type.INT, val)

    def visitFloat_expr(self, ctx:DMFParser.Float_exprContext) -> Executable:
        val: float = float(ctx.FLOAT().getText())
        return Executable.constant(Type.FLOAT, val)

    def visitType_name_expr(self, ctx:DMFParser.Type_name_exprContext) -> Executable:
        n = None if ctx.n is None else int(cast(Token, ctx.n).text)
        name = self.type_name_var(ctx.param_type(), n)
        var_type = self.current_types.lookup(name)
        if var_type is MISSING:
            return self.error(ctx.param_type(), Type.NO_VALUE, f"Undefined variable: {name}")
        def run(env: Environment) -> Delayed[Any]:
            val = env.lookup(name)
            if val is MISSING:
                return Delayed.complete(UninitializedVariableError(f"Uninitialized variable: {name}"))
            return Delayed.complete(val)
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
            if isinstance(special, Constant):
                return Executable.constant(special.var_type, special.val)
            real_special = special
            return Executable(special.var_type, lambda env: Delayed.complete(real_special.get(env)))
        var_type = self.current_types.lookup(name)
        if var_type is MISSING:
            return self.error(ctx.name(), Type.NO_VALUE, f"Undefined variable: {name}")
        def run(env: Environment) -> Delayed[Any]:
            val = env.lookup(name)
            if val is MISSING:
                return Delayed.complete(UninitializedVariableError(f"Uninitialized variable: {name}"))
            return Delayed.complete(val)
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
        lhs_t = lhs.return_type
        rhs_t = rhs.return_type
        ub_t = rel.comparable_type(lhs_t, rhs_t)
        if ub_t is None:
            return self.error(ctx, Type.BOOL,
                              f"Can't compare {lhs_t.name} and {rhs_t.name}: {self.text_of(ctx)}")
        def run(env: Environment) -> Delayed[MaybeError[bool]]:
            return (lhs.evaluate(env, ub_t)
                    .chain(lambda x: (rhs.check_and_eval(x, env, ub_t)
                                      .transformed(error_check(lambda y: rel.test(x, y))))))
            # return future.chain(second)
        return Executable(Type.BOOL, run, (lhs,rhs))
    
    
    def visitHas_expr(self, ctx:DMFParser.Has_exprContext) -> Executable:
        obj = self.visit(ctx.obj)
        attr_name: str = ctx.attr().which
        attr = Attributes.get(attr_name, None)
        polarity: bool = ctx.possession().polarity
        test = (lambda v: v is not None) if polarity else (lambda v: v is None) 
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
            self.print_warning(ctx.attr(), lambda txt:  f"{txt} is not a 'maybe' attribute. 'has' will always return True.")
            return Executable(Type.BOOL, (to_const(Delayed.complete(True))), (obj,))
        def run(env: Environment) -> Delayed[MaybeError[bool]]:
            def check(v: Any) -> MaybeError[bool]:
                if isinstance(v, EvaluationError):
                    return v
                return v is not None
            return (obj.evaluate(env, ot)
                    .chain(error_check_delayed(extractor))
                    .transformed(error_check(test)))
            # return obj.evaluate(env, ot).chain(extractor).transformed(check)
        return Executable(Type.BOOL, run, (obj,))
    
    def visitExistence_expr(self, ctx:DMFParser.Existence_exprContext) -> Executable:
        val = self.visit(ctx.val)
        polarity: bool = ctx.existence().polarity
        test = (lambda v: v is not None) if polarity else (lambda v: v is None) 
        val_type = val.return_type
        # We can't just return the constant because we can't (yet) prove that there are no side effects.
        if val_type is not Type.MISSING and not isinstance(val_type, MaybeType):
            self.print_warning(ctx, lambda txt: f"Expression doesn't return MAYBE type in '{txt}'")
        def run(env: Environment) -> Delayed[MaybeError[bool]]:
            return val.evaluate(env).transformed(error_check(test))
        return Executable(Type.BOOL, run, (val,))
    
        
    def visitIs_expr(self, ctx:DMFParser.Is_exprContext) -> Executable:
        neg = ctx.NOT() is not None or ctx.ISNT() is not None
        obj = self.visit(ctx.obj)
        pred = self.visit(ctx.pred)
        pred_type = pred.return_type
        if pred_type < Type.BINARY_STATE:
            if (e := self.type_check(Type.BINARY_CPT, obj, ctx,
                                     lambda want, have, text:
                                        f"Left-hand side of 'is <state>' expression needs to be {want}, was {have}: {text}",
                                     return_type = Type.BOOL)):
                return e 
            want_on = pred_type is Type.ON
            if neg:
                want_on = not want_on
            func = "#is on" if want_on else "#is off"
            return self.use_function(func, ctx, (ctx.obj,))
        # if pred_type is Type.MISSING:
        #     if (e := self.type_check(Type.ANY.maybe, obj, ctx,
        #                              lambda want, have, text:
        #                                 f"Left-hand side of 'is missing' expression needs to be {want}, was {have}: {text}",
        #                              return_type = Type.BOOL)):
        #         return e
        #     func = "#exists" if neg else "#does not exist" 
        #     return self.use_function(func, ctx, (ctx.obj,))
        if (not isinstance(pred_type, CallableType)
            or len(pred_type.param_types) != 1
            or pred_type.return_type is not Type.BOOL):
            return self.error(ctx.pred, Type.BOOL,
                              f"Not a predicate ({pred_type}): {self.text_of(ctx.pred)}")
        first_arg_type = pred_type.param_types[0]
        if (e := self.type_check(first_arg_type, obj, ctx,
                                 (lambda want, have, text: 
                                    f"Value ({have}) '{text}' not compatible with "
                                    +f"{want}: {self.text_of(ctx.pred)}"),
                                 return_type = Type.BOOL)):
            return e
        def run(env: Environment) -> Delayed[MaybeError[bool]]:
            def inject(obj: Any, func: Any) -> Delayed[MaybeError[bool]]:
                if isinstance(func, EvaluationError):
                    return Delayed.complete(func)
                assert isinstance(func, CallableValue)
                future: Delayed[MaybeError[bool]] = func.apply((obj,))
                if neg:
                    future = future.transformed(lambda v: v if isinstance(v, EvaluationError) else not v)
                return future
            def after_obj(obj: Any) -> Delayed[Any]:
                if isinstance(obj, EvaluationError):
                    return Delayed.complete(obj)
                return pred.evaluate(env, pred_type).chain(lambda func: inject(obj, func))
            return obj.evaluate(env, first_arg_type).chain(after_obj)
        return Executable(Type.BOOL, run, (obj, pred))

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
        result_type = Type.upper_bound(first.return_type, second.return_type)
        if result_type is Type.NO_VALUE:
            t1 = first.return_type.name
            t2 = second.return_type.name
            return self.error(ctx, Type.ANY, 
                              lambda txt: f"Conditional expression branches incompatible ({t1} and {t2}): {txt}")
        def run(env: Environment) -> Delayed:
            def branch(c: MaybeError[bool]) -> Delayed:
                if isinstance(c, EvaluationError):
                    return Delayed.complete(c)
                if c:
                    return first.evaluate(env, result_type)
                else:
                    return second.evaluate(env, result_type)
            return cond.evaluate(env, Type.BOOL).chain(branch)
        return Executable(result_type, run, (first, cond, second))

    def visitDelta_expr(self, ctx:DMFParser.Delta_exprContext) -> Executable:
        dist = self.visit(ctx.dist)
        direction: Dir = ctx.direction().d
        if e:=self.type_check(Type.INT, dist, ctx.dist, return_type=Type.DELTA):
            return e
        def run(env: Environment) -> Delayed[MaybeError[DeltaValue]]:
            def to_delta(n: MaybeError[int]) -> MaybeError[DeltaValue]:
                if isinstance(n, EvaluationError):
                    return n
                return DeltaValue(n, direction)
            return dist.evaluate(env, Type.INT).transformed(to_delta)
        return Executable(Type.DELTA, run, (dist,))

    def visitIn_dir_expr(self, ctx:DMFParser.In_dir_exprContext) -> Executable: 
        dist = self.visit(ctx.dist)
        direction = self.visit(ctx.d)
        if e:=self.type_check(Type.INT, dist, ctx.dist, return_type=Type.DELTA):
            return e
        if e:=self.type_check(Type.DIR, direction, ctx.d, return_type=Type.DELTA):
            return e
        def run(env: Environment) -> Delayed[MaybeError[DeltaValue]]:
                def combine(n: int, d: MaybeError[Dir]) -> MaybeError[DeltaValue]:
                    if isinstance(d, EvaluationError):
                        return d
                    return DeltaValue(n, d)
                def after_n(n: MaybeError[int]) -> Delayed[MaybeError[DeltaValue]]:
                    if isinstance(n, EvaluationError):
                        return Delayed.complete(n)
                    real_n = n
                    return direction.evaluate(env, Type.DIR).transformed(lambda d: combine(real_n,d))
                future: Delayed[MaybeError[int]] = dist.evaluate(env, Type.INT)
                return future.chain(after_n)
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
        def run(env: Environment) -> Delayed[MaybeError[DeltaValue]]:
            def to_delta(n: MaybeError[int]) -> MaybeError[DeltaValue]:
                if isinstance(n, EvaluationError):
                    return n
                return DeltaValue(n, direction)
            return dist.evaluate(env, Type.INT).transformed(to_delta)

        return Executable(Type.DELTA, run, (dist,))

    def visitConst_rc_expr(self, ctx:DMFParser.N_rc_exprContext) -> Executable:
        direction: Dir = ctx.rc().d
        n = int(cast(Token, ctx.INT()).getText())
        return Executable.constant(Type.DELTA, DeltaValue(n, direction))

    
    def visitCoord_expr(self, ctx:DMFParser.Coord_exprContext) -> Executable:
        return self.use_function("COORD", ctx, (ctx.x, ctx.y))

    def visitInjection_expr(self, ctx:DMFParser.Injection_exprContext) -> Executable:
        who = self.visit(ctx.who)
        self.set_injected_type_annotation(cast(DMFParser.ExprContext, ctx.what), who.return_type)
        what = self.visit(ctx.what)
        # logger.info(f"Injecting {self.text_of(ctx.who)} into {self.text_of(ctx.what)}")
        if what.return_type is Type.BUILT_IN:
            func: MissingOr[Func] = what.const_val
            if func is MISSING:
                return self.error(ctx.what, Type.NO_VALUE, f"Internal error: {self.text_of(ctx.what)} is a built-in, but no Func value")
            return self.use_function(func, ctx, (ctx.who,))
        target_type = what.return_type.as_func_type
        if (target_type is None
            or (target_kind := target_type.kind) is CallableTypeKind.GENERAL):
            return self.error(ctx.what, Type.NO_VALUE, 
                              f"Not an injection target ({what.return_type.name}): {self.text_of(ctx.what)}")
        injected_type = who.return_type
        # if injected_type <= Type.MOTION:
        #     injected_type = Type.MOTION
        # if injected_type <= Type.TWIDDLE_OP:
        #     injected_type = Type.TWIDDLE_OP

        do_injection: Callable[[Any, CallableValue, Type], Delayed[Any]]
        if target_kind is CallableTypeKind.TRANSFORM:
            required_type = target_type.param_types[0]
            do_injection = lambda v, fn, t: error_check_delayed(lambda x: fn.apply((t.checked_convert_to(required_type, x),)))(v)
        elif target_kind is CallableTypeKind.MONITOR:
            required_type = target_type.param_types[0]
            do_injection = (lambda v, fn, t: error_check_delayed(lambda x: fn.apply((t.checked_convert_to(required_type, x),)))(v)
                            .transformed(to_const(v)))
        elif target_kind is CallableTypeKind.ACTION:
            required_type = Type.ANY
            do_injection = lambda v, fn, _: fn.apply(()).transformed(to_const(v)) 
        else:
            assert_never(target_kind)
        
        can_pass = self.compatible(injected_type, required_type)
        lhs_type = injected_type.as_func_type
        can_chain = (lhs_type is not None
                     and self.compatible(lhs_type.return_type, required_type))
        
        if can_pass and not can_chain:
            return_type = target_type.return_type if target_kind is CallableTypeKind.TRANSFORM else injected_type 
            def run(env: Environment) -> Delayed[Any]:
                def after_who(who: Any) -> Delayed[Any]:
                    return what.evaluate(env, target_type).chain(error_check_delayed(lambda func: do_injection(who, func, required_type)))
                return who.evaluate(env).chain(error_check_delayed(after_who))
            # print(f"Injection returns {inj_type.return_type}: {self.text_of(ctx)}")
            return Executable(return_type, run, (who, what))
        elif can_chain:
            assert lhs_type is not None
            chain_type = ComposedCallable.composed_type(lhs_type, target_type)
            
            def chain(env: Environment) -> Delayed[Any]:
                def combine(first: CallableValue, second: CallableValue) -> CallableValue:
                    comp = ComposedCallable(first, second)
                    return comp
                def after_first(first: CallableValue) -> Delayed[MaybeError[CallableValue]]:
                    return what.evaluate(env, target_type).transformed(error_check(lambda second: combine(first, second)))
                return who.evaluate(env, injected_type).chain(error_check_delayed(after_first))
            return Executable(chain_type, chain, (who, what))
        elif lhs_type is not None:
            return_type = target_type.return_type if target_kind is CallableTypeKind.TRANSFORM else lhs_type.return_type
            e = self.type_check(required_type, lhs_type.return_type, ctx.who,
                                (lambda want,have,text:
                                 f"Injecting form '{text}' returns {have}, not compatible with "
                                 +f"{want}: {self.text_of(ctx.what)}"),
                                return_type=return_type)
            return not_None(e)
        else:
            return_type = target_type.return_type if target_kind is CallableTypeKind.TRANSFORM else injected_type 
            e = self.type_check(required_type, injected_type, ctx.who,
                                (lambda want,have,text:
                                 f"Injected value ({have}) '{text}' not compatible with "
                                 +f"{want}: {self.text_of(ctx.what)}"),
                                return_type=return_type)
            return not_None(e)
        
            
    
    def visitAttr_expr(self, ctx:DMFParser.Attr_exprContext) -> Executable:
        obj = self.visit(ctx.obj)
        existence_check = ctx.existence() is not None 
        
        is_maybe = existence_check or (ctx.MAYBE() is not None)
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
        if is_maybe and not isinstance(rt, MaybeType):
            self.print_warning(ctx, lambda text: f"{ot.name}'s {attr_name} is a {rt.name}, not a MAYBE type: {text}")
        if isinstance(rt, MaybeType) and not is_maybe:
            real_extractor = extractor
            real_attr = attr
            attr_text = self.text_of(ctx.attr())
            def extractor(obj: Any) -> Delayed[Any]:
                def check(val: Any) -> MaybeError:
                    if val is None:
                        name = real_attr.func.name
                        if (m := re.fullmatch("'(.*)' attribute", name)) is not None:
                            name = m.group(1)
                        ex = MaybeNotSatisfiedError(f"{obj} has no '{attr_text}'.")
                        return ex
                    return val
                return real_extractor(obj).transformed(error_check(check))
            rt = rt.if_there_type
        elif existence_check:
            polarity = ctx.existence().polarity
            test = (lambda v: v is not None) if polarity else (lambda v: v is None)
            if rt is Type.MISSING:
                return Executable.constant(Type.BOOL, test(None), (obj,))
            elif not isinstance(rt, MaybeType):
                return Executable.constant(Type.BOOL, not test(None), (obj,))
            real_extractor = extractor
            extractor = lambda obj: real_extractor(obj).transformed(error_check(test))
            rt = Type.BOOL
        def run(env: Environment) -> Delayed[Any]:
            return obj.evaluate(env, ot).chain(error_check_delayed(extractor))
        return Executable(rt, run, (obj,))

    
    def visitNumbered_expr(self, ctx:DMFParser.Numbered_exprContext) -> Executable:
        which = self.visit(ctx.which)
        kind_ctx = cast(DMFParser.Numbered_typeContext, ctx.kind)
        kind = cast(NumberedItem, kind_ctx.kind)
        
        def find_component(cpt_type: type[EC],
                           rt: Type,
                           name: str) -> Executable:
            if e:=self.type_check(Type.INT, which, ctx.which, return_type=rt):
                return e
            def run(env: Environment) -> Delayed[MaybeError[EC]]:
                def find(n: int) -> MaybeError[EC]:
                    try:
                        def lookup(board: Board, n: int) -> EC:
                            return board.component_number(n, cpt_type)
                        return lookup(env.board, n)
                    except IndexError:
                        max_val = len(env.board.find_all(cpt_type))
                        return NoSuchComponentError(name, n, max_val)
                return (which.evaluate(env, Type.INT)
                        .transformed(error_check(find)))
            return Executable(rt, run, (which,))
        
        def find_in_list(lookup: Callable[[Board, int], T_],
                         rt: Type,
                         name: str, 
                         *,
                         max_val: Callable[[Board], int]) -> Executable:
            if e:=self.type_check(Type.INT, which, ctx.which, return_type=rt):
                return e
            def run(env: Environment) -> Delayed[MaybeError[T_]]:
                def find(n: int) -> MaybeError[T_]:
                    try:
                        return lookup(env.board, n)
                    except IndexError:
                        return NoSuchComponentError(name, n, max_val(env.board))
                return (which.evaluate(env, Type.INT)
                        .transformed(error_check(find)))
            return Executable(rt, run, (which,))
        
        if kind is NumberedItem.WELL:
            return find_in_list(Board.well_number, Type.WELL, "well", max_val=lambda b: len(b.wells))
        # elif kind is NumberedItem.TEMP_CONTROL:
        #     return figure(lambda b: b.temperature_controls, Type.HEATER, "temperature control")
        elif kind is NumberedItem.HEATER:
            return find_component(Heater, Type.HEATER, "heater")
        elif kind is NumberedItem.CHILLER:
            return find_component(Chiller, Type.CHILLER, "chiller")
        elif kind is NumberedItem.MAGNET:
            return find_component(Magnet, Type.MAGNET, "magnet")
        elif kind is NumberedItem.EXTRACTION_POINT:
            return find_in_list(Board.extraction_point_number, Type.EXTRACTION_POINT, "extraction point",
                                max_val = lambda b: len(b.extraction_points))
        else:
            assert_never(kind)



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
        f_type = func_exec.return_type.as_func_type
        if f_type is None:
            return self.error(fc, Type.NO_VALUE, lambda text: f"Not callable ({func_exec.return_type.name}): {text}")
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
            
        def catch_return(val: MaybeError[Any]) -> Any:
            if isinstance(val, MacroReturn):
                return val.value
            # Either it's a fall-off-the-end value, which should only be allowed
            # if it's okay, or it's some other error, which we should propagate.
            return val
        
        def dispatch(fn: CallableValue, *args: Sequence[Any]) -> Delayed[Any]:
            return fn.apply(args).transformed(catch_return)
        
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
            def run(env: Environment) -> Delayed[MaybeError[MotionValue]]:
                return (which.evaluate(env, Type.PAD)
                        .transformed(error_check(lambda pad: ToPadValue(pad))))
        else:
            if not self.compatible(which.return_type, Type.INT):
                return self.error(ctx.which, Type.MOTION, 
                                  f"Row or column name not an int ({which.return_type.name}): {self.text_of(ctx.which)}")
            verticalp = cast(bool, axis.verticalp)
            def run(env: Environment) -> Delayed[MaybeError[MotionValue]]:
                return (which.evaluate(env, Type.INT)
                        .transformed(error_check(lambda n: ToRowColValue(n, verticalp))))
        return Executable(Type.MOTION, run, (which,))
    
    def visitMuldiv_expr(self, ctx:DMFParser.Muldiv_exprContext)->Executable:
        mulp = ctx.MUL() is not None
        func = "MULTIPLY" if mulp else "DIVIDE"
        return self.use_function(func, ctx, (ctx.lhs, ctx.rhs))

    def visitDirection(self, ctx:DMFParser.DirectionContext) -> Executable:
        return DMFVisitor.visitDirection(self, ctx) # type: ignore [no-any-return]


    def visitAxis(self, ctx:DMFParser.AxisContext) -> Executable:
        return DMFVisitor.visitAxis(self, ctx) # type: ignore [no-any-return]

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
        macro_type = CallableType.find(types, Type.NO_VALUE)
        return self.error_val(macro_type, lambda env: Delayed.complete(None)) # @UnusedVariable

    def visitMacro_def(self, ctx:DMFParser.Macro_defContext) -> Executable:
        header: DMFParser.Macro_headerContext = ctx.macro_header()
        param_contexts: Sequence[DMFParser.ParamContext] = header.param()
        
        for pc in param_contexts:
            if cast(bool, pc.deprecated):
                self.decl_deprecated(pc)
        
        param_defs = tuple(self.param_def(pc) for pc in param_contexts)
        param_names = tuple(pdef[0] for pdef in param_defs)
        param_types = tuple(pdef[1] for pdef in param_defs)
        
        return_type_context: Optional[DMFParser.Param_typeContext] = header.ret_type
        return_type = Type.NO_VALUE if return_type_context is None else cast(Type, return_type_context.type)
        
        if e := self.check_macro_params(param_names, param_types, param_contexts):
            return e
        
        # Unfortunately, you can't put parens around multiple with clauses until
        # Python 3.10.
        with self.current_types.push(dict(param_defs)), \
             self.control_stack.enter_macro(return_type): 
            body: Executable
            if ctx.compound() is not None:
                body = self.visit(ctx.compound())
            else:
                body = self.visit(ctx.expr())
        
        body_type = body.return_type
        macro_type = CallableType.find(param_types, return_type)
        if return_type is not Type.NO_VALUE and body_type is not Type.MACRO_RETURN:
            return self.error(ctx, macro_type, "Macro does not return a value.")
        
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
    
    def visitTemperature_expr(self, ctx:DMFParser.Temperature_exprContext) -> Executable:
        return self.use_function("TEMP_C", ctx, (ctx.amount,))
    
    # def visitDrop_vol_expr(self, ctx:DMFParser.Drop_vol_exprContext) -> Executable:
    #     return self.use_function("DROP_VOL", ctx, (ctx.amount,))
        
    def visitPause_expr(self, ctx:DMFParser.Pause_exprContext) -> Executable:
        duration = self.visit(ctx.duration)
        if e:=self.type_check(Type.DELAY, duration, ctx.duration,
                              lambda want,have,text: # @UnusedVariable
                                f"Delay ({have} must be time or ticks: {text}",
                              return_type=Type.ACTION):
            return e
        def run(env: Environment) -> Delayed[MaybeError[PauseValue]]:
            return (duration.evaluate(env, Type.DELAY)
                    .transformed(error_check(lambda d: PauseValue(d, env.board))))
        return Executable(Type.ACTION, run, (duration,))
    
    def visitPrompt_expr(self, ctx:DMFParser.Prompt_exprContext) -> Executable:
        def run(env: Environment, *vals: Sequence[Any]) -> Delayed[PromptValue]:
            return Delayed.complete(PromptValue(vals, board=env.board))
        vals = tuple(self.visit(c) for c in ctx.vals)
        sig = Signature.of(tuple(v.return_type for v in vals), Type.ACTION)
        return self.use_callable(WithEnvDelayed(run), vals, sig)
            
            
                
    def visitMacro_header(self, ctx:DMFParser.Macro_headerContext) -> Executable:
        return DMFVisitor.visitMacro_header(self, ctx) # type: ignore [no-any-return]


    def visitParam(self, ctx:DMFParser.ParamContext) -> Executable:
        return DMFVisitor.visitParam(self, ctx) # type: ignore [no-any-return]


    def visitParam_type(self, ctx:DMFParser.Param_typeContext) -> Executable:
        return DMFVisitor.visitParam_type(self, ctx) # type: ignore [no-any-return]


    def visitName(self, ctx:DMFParser.NameContext) -> Executable:
        return DMFVisitor.visitName(self, ctx) # type: ignore [no-any-return]


    def visitKwd_names(self, ctx:DMFParser.Kwd_namesContext) -> Executable:
        return DMFVisitor.visitKwd_names(self, ctx) # type: ignore [no-any-return]
    
    @classmethod
    def setup_function_table(cls) -> None:
        fn = Functions["NEGATE"]
        fn.prefix_op("-")
        fn.register_all_immediate([((Type.INT,), Type.INT),
                                   ((Type.FLOAT,), Type.FLOAT),
                                   ((Type.REL_TEMP,), Type.REL_TEMP),
                                   ], lambda x: -x)
        
        fn = Functions["INDEX"]
        fn.format_type_expr_using(2, lambda x,y: f"{x}[{y}]")
        fn.register_all_immediate([((Type.WELL, Type.INT), Type.WELL_PAD),
                                   ], lambda w,n: w.shared_pad_number(cast(int, n)))
        

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
                                   ((Type.STRING,Type.STRING), Type.STRING),
                                   # ((Type.AMBIG_TEMP, Type.AMBIG_TEMP), Type.AMBIG_TEMP),
                                   ((Type.AMBIG_TEMP, Type.REL_TEMP), Type.AMBIG_TEMP),
                                   ((Type.ABS_TEMP, Type.REL_TEMP), Type.ABS_TEMP),
                                   ((Type.REL_TEMP, Type.ABS_TEMP), Type.ABS_TEMP),
                                   ((Type.REL_TEMP, Type.REL_TEMP), Type.REL_TEMP),
                                   ((Type.VOLTAGE, Type.VOLTAGE), Type.VOLTAGE)
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
                                   # ((Type.AMBIG_TEMP, Type.AMBIG_TEMP), Type.AMBIG_TEMP),
                                   ((Type.AMBIG_TEMP, Type.REL_TEMP), Type.AMBIG_TEMP),
                                   ((Type.REL_TEMP, Type.REL_TEMP), Type.REL_TEMP),
                                   ((Type.ABS_TEMP, Type.REL_TEMP), Type.ABS_TEMP),
                                   ((Type.ABS_TEMP, Type.ABS_TEMP), Type.REL_TEMP),
                                   ((Type.VOLTAGE, Type.VOLTAGE), Type.VOLTAGE)
                                   ], lambda x,y: x-y)
        
         
        fn.register_immediate((Type.PAD, Type.DELTA), Type.PAD, lambda p,d: add_delta(p, d.direction, -d.dist))
        
        fn = Functions["NOT"]
        fn.prefix_op("not")
        fn.register_all_immediate([((Type.BOOL,), Type.BOOL),
                                   ], lambda x: not x)

    
        fn = Functions["AND"]
        fn.infix_op("and")
        
        def sc_and(env: Environment, arg_execs: Sequence[Executable]) -> Delayed[MaybeError[bool]]:
            lhs, rhs = arg_execs
            def after_lhs(x: MaybeError[bool]) -> Delayed[MaybeError[bool]]:
                if isinstance(x, EvaluationError) or not x:
                    return Delayed.complete(x)
                else:
                    return rhs.evaluate(env, Type.BOOL)
            return lhs.evaluate(env, Type.BOOL).chain(after_lhs)
        fn.register((Type.BOOL,Type.BOOL), Type.BOOL, LazyEval(sc_and))

        fn = Functions["OR"]
        fn.infix_op("or")
        
        def sc_or(env: Environment, arg_execs: Sequence[Executable]) -> Delayed[MaybeError[bool]]:
            lhs, rhs = arg_execs
            def after_lhs(x: MaybeError[bool]) -> Delayed[MaybeError[bool]]:
                if isinstance(x, EvaluationError) or x:
                    return Delayed.complete(x)
                else:
                    return rhs.evaluate(env, Type.BOOL)
            return lhs.evaluate(env, Type.BOOL).chain(after_lhs)
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
                                   ((Type.REL_TEMP,Type.FLOAT), Type.REL_TEMP),
                                   ((Type.FLOAT,Type.REL_TEMP), Type.REL_TEMP),
                                   # ((Type.AMBIG_TEMP,Type.FLOAT), Type.REL_TEMP),
                                   ((Type.VOLTAGE,Type.FLOAT), Type.VOLTAGE),
                                   ((Type.FLOAT,Type.VOLTAGE), Type.VOLTAGE),
                                   ], lambda x,y: x*y)
        fn.register_immediate((Type.NUMBER, Type.REAGENT), Type.SCALED_REAGENT,
                              lambda n,r: ScaledReagent(n,r))

        fn = Functions["DIVIDE"]
        fn.infix_op("/")
        
        fn.register_all_immediate([((Type.FLOAT,Type.FLOAT), Type.FLOAT),
                                   ((Type.TIME,Type.FLOAT), Type.TIME),
                                   ((Type.TICKS,Type.FLOAT), Type.TICKS),
                                   ((Type.VOLUME,Type.FLOAT), Type.VOLUME),
                                   ((Type.REL_TEMP,Type.FLOAT), Type.REL_TEMP),
                                   # ((Type.AMBIG_TEMP,Type.FLOAT), Type.REL_TEMP),
                                   ((Type.VOLTAGE,Type.FLOAT), Type.VOLTAGE),
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
        fn.register_immediate((), Type.TWIDDLE_OP, lambda: TwiddleBinaryValue.ON)
        fn = Functions["TURN-OFF"]
        fn.register_immediate((), Type.TWIDDLE_OP, lambda: TwiddleBinaryValue.OFF)
        fn = Functions["TOGGLE"]
        fn.register_immediate((), Type.TWIDDLE_OP, lambda: TwiddleBinaryValue.TOGGLE)
        
        fn = Functions["REMOVE-FROM-BOARD"]
        fn.register_immediate((), Type.MOTION, lambda: RemoveDropValue())
        
        fn = Functions["FIND_DROP"]
        fn.prefix_op("drop @")
        def new_drop(pad: Pad, liquid: Optional[Union[Liquid, Volume]] = None) -> MaybeError[Drop]:
            if liquid is None:
                liquid = Liquid(unknown_reagent, pad.board.drop_size)
            elif isinstance(liquid, Volume):
                liquid = Liquid(unknown_reagent, liquid)
            else:
                # We copy the liquid, since the drop will adopt it.
                liquid = Liquid(liquid.reagent, liquid.volume)
            if pad.drop is not None:
                return AlreadyDropError(f"There is already a drop at {pad}")
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
        def find_pad(env: Environment, x: int, y: int) -> MaybeError[Pad]:
            board = env.board
            try:
                return board.pad_at(x, y)
            except KeyError:
                return NoSuchPadError(x, y)
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
        
        fn = Functions["TEMP_C"]
        fn.postfix_op("C")
        fn.register_immediate((Type.NUMBER,), Type.AMBIG_TEMP, 
                              lambda n: AmbiguousTemp(absolute=n*abs_C, relative=n*deg_C))
        
        fn = Functions["RESET PADS"]
        fn.register((), Type.NO_VALUE, WithEnv(lambda env: env.board.reset_pads()))
        fn = Functions["RESET MAGNETS"]
        fn.register((), Type.NO_VALUE, WithEnv(lambda env: env.board.reset_components(Magnet)))
        fn = Functions["RESET HEATERS"]
        fn.register((), Type.NO_VALUE, WithEnv(lambda env: env.board.reset_components(Heater)))
        fn = Functions["RESET CHILLERS"]
        fn.register((), Type.NO_VALUE, WithEnv(lambda env: env.board.reset_components(Chiller)))
        fn = Functions["RESET ALL"]
        fn.register((), Type.NO_VALUE, WithEnv(lambda env: env.board.reset_all()))
        
        fn = Functions["ROUND"]
        fn.register_immediate((Type.FLOAT,), Type.INT, lambda x: round(x))
        fn = Functions["FLOOR"]
        fn.register_immediate((Type.FLOAT,), Type.INT, lambda x: math.floor(x))
        fn = Functions["CEILING"]
        fn.register_immediate((Type.FLOAT,), Type.INT, lambda x: math.ceil(x))
        fn = Functions["UNSAFE"]
        fn.register_immediate((Type.DELTA,), Type.MOTION, lambda d: UnsafeWalkValue(d))
        fn = Functions["UNSAFE"]
        fn.register_immediate((Type.DIR,), Type.MOTION, lambda d: UnsafeWalkValue(DeltaValue(1,d)))
        fn = Functions["PRINT"]
        fn.register_all_immediate([((Type.ANY,) * 10, Type.NO_VALUE) for n in range(1, 8)],
                                                  print)
        fn = Functions["STRING"]
        fn.register_immediate((Type.ANY,), Type.STRING, str)
        fn = Functions["#is on"]
        fn.register_immediate((Type.BINARY_CPT,), Type.BOOL, lambda c: c.current_state is OnOff.ON)
        fn = Functions["#is off"]
        fn.register_immediate((Type.BINARY_CPT,), Type.BOOL, lambda c: c.current_state is OnOff.OFF)
        fn = Functions["#exists"]
        fn.register_immediate((Type.ANY.maybe,), Type.BOOL, lambda v: v is not None)   
        fn = Functions["#does not exist"]
        fn.register_immediate((Type.ANY.maybe,), Type.BOOL, lambda v: v is None)   
        

        fn = Functions["#dispense drop"]
        def dispense(w: Well) -> Delayed[Drop]:
            path = Path.dispense_from(w)
            return path.schedule()
        fn.register((Type.WELL,), Type.DROP, dispense)
        
        fn = Functions["#enter well"]
        def enter_well(d: Drop) -> Delayed[None]:
            path = Path.enter_well()
            return path.schedule_for(d)
        fn.register((Type.DROP,), Type.NO_VALUE, enter_well)        
        
        fn = Functions["#transfer in"]
        # def add_liquid(target: Union[Well,ExtractionPoint], liquid: Liquid, *,
        #                result: Optional[Reagent] = None) -> Delayed[Well]:
        #     if isinstance(target, Well):
        #         return target.add(liquid.reagent, liquid.volume, mix_result=result)
        #     else:
        #         path = Path.teleport_into(target, liquid=liquid, mix_result=result)
        #         return path.schedule()
                
        def add_liquid_to_well(w: Well, liquid: Liquid, *,
                               result: Optional[Reagent] = None) -> Delayed[Well]:
            return w.add(liquid.reagent, liquid.volume, mix_result=result)
        fn.register((Type.WELL, Type.LIQUID), Type.WELL, add_liquid_to_well, curry_at=0)
        fn.register((Type.WELL, Type.LIQUID, Type.REAGENT), Type.WELL,
                    lambda w,l,r: add_liquid_to_well(w, l, result=r), curry_at=0)
        def add_volume_to_well(w: Well, v: Volume) -> Delayed[Well]:
            return w.add(w.reagent, v)
        fn.register((Type.WELL, Type.VOLUME), Type.WELL, add_volume_to_well, curry_at=0)
        def add_liquid_to_ep(ep: ExtractionPoint, liquid: Liquid) -> Delayed[Drop]:
            path = Path.teleport_into(ep, liquid=liquid)
            return path.schedule()
        fn.register((Type.EXTRACTION_POINT, Type.LIQUID), Type.DROP, add_liquid_to_ep, curry_at=0)
        # TODO: To transfer in just based on volume, we need to be able to get
        # our hands on the interactive reagent, which means we need an Environment.
        
        def interactive_reagent(env: Environment) -> Reagent:
            return cast(Reagent, SpecialVars["interactive reagent"].get(env))

        fn.register((Type.EXTRACTION_POINT,Type.VOLUME), Type.DROP,
                    WithEnvDelayed(lambda env, ep, v: add_liquid_to_ep(ep, Liquid(interactive_reagent(env), v))),
                    curry_at=0)

        # fn.register((Type.EXTRACTION_POINT, Type.VOLUME), Type.DROP,
                            # lambda ep,v: add_liquid_to_ep(ep, Liquid(ep, ))
        def add_reagent_to_ep(ep: ExtractionPoint, r: Reagent) -> Delayed[Drop]:
            return Path.teleport_into(ep, reagent=r).schedule()
        fn.register((Type.EXTRACTION_POINT, Type.REAGENT), Type.DROP, add_reagent_to_ep, curry_at=0)
        fn.register((Type.EXTRACTION_POINT,), Type.DROP,
                    WithEnvDelayed(lambda env, ep: add_reagent_to_ep(ep, interactive_reagent(env))))

        fn = Functions["#transfer out"]
        def remove_liquid(source: Union[Well, ExtractionPoint], volume: Optional[Volume] = None) -> Delayed[Liquid]:
            if isinstance(source, Well):
                if volume is None:
                    volume = source.volume
                return source.remove(volume)
            else:
                return source.transfer_out(volume=volume, is_product=True)
        
        fn.register((Type.PIPETTING_TARGET, Type.VOLUME), Type.LIQUID, remove_liquid, curry_at=0)
        fn.register((Type.PIPETTING_TARGET,), Type.LIQUID, remove_liquid)
        
        
        # def remove_volume_from_well(w: Well, v: Volume) -> Delayed[Well]:
        #     return w.remove(v)
        # fn.register((Type.WELL, Type.VOLUME), Type.WELL, remove_volume_from_well, curry_at=0)
        #
        # def remove_liquid_from_ep(ep: ExtractionPoint, v: Optional[Volume] = None) -> Delayed[Liquid]:
        #     # def trace_loc(loc: ProductLocation) -> None:
        #     #     print(f"Removed product {loc.reagent} to {loc.location}")
        #     # prod_loc = Postable[ProductLocation]()
        #     # prod_loc.then_call(trace_loc)
        #     # return ep.transfer_out(volume=v, is_product=True, product_loc=prod_loc)
        #     return ep.transfer_out(volume=v, is_product=True)
        #
        # fn.register((Type.EXTRACTION_POINT,), Type.LIQUID, remove_liquid_from_ep)
        # fn.register((Type.EXTRACTION_POINT, Type.VOLUME), Type.LIQUID, remove_liquid_from_ep, curry_at=0)

        def remove_drop_from_ep(d: Drop) -> Delayed[Liquid]:
            if not isinstance((p:=d.pad), Pad) or (ep:=p.extraction_point) is None:
                raise EvaluationError(f"No extraction point at {p}")
            return remove_liquid(ep)
        fn.register((Type.DROP,), Type.LIQUID, remove_drop_from_ep)
        
            

        fn = Functions["fill"]
        def fill_well(w: Well, r: Optional[Reagent] = None) -> Delayed[Well]:
            return w.refill(reagent=r)
        fn.register((Type.WELL,), Type.WELL, fill_well)
        fn.register((Type.WELL, Type.REAGENT), Type.WELL, fill_well, curry_at=0)


        fn = BuiltIns["empty"] = Functions["empty"]
        def empty_well(w: Well) -> Delayed[Liquid]:
            return w.empty_well()
        fn.register((Type.WELL,), Type.WELL, empty_well)

        fn = Functions["#prepare to dispense"]
        def prepare_to_dispense(w: Well, what: Optional[Union[Volume,Liquid,Reagent]] = None) -> None:
            v = (what if isinstance(what, Volume)
                 else what.volume if isinstance(what, Liquid)
                 else None)
            r = (what if isinstance(what, Reagent)
                 else what.reagent if isinstance(what, Liquid)
                 else None)
            if v is not None:
                w.required = v
            w.ensure_content(v, r)
        fn.register_all_immediate([((Type.WELL, Type.LIQUID), Type.NO_VALUE),
                                   ((Type.WELL, Type.VOLUME), Type.NO_VALUE),
                                   ((Type.WELL, Type.REAGENT), Type.NO_VALUE),
                                   ((Type.WELL,), Type.NO_VALUE)],
                                   prepare_to_dispense,
                                   curry_at=0)
        
    @classmethod
    def setup_special_vars(cls) -> None:
        unmonitored_interactive_reagent = unknown_reagent
        name = "interactive reagent"
        def get_reagent(monitor: BoardMonitor) -> Reagent:
            return monitor.interactive_reagent
        def unmonitored_get_reagent(_env: Environment) -> Reagent:
            return unmonitored_interactive_reagent
        def set_reagent(monitor: BoardMonitor, reagent: Reagent) -> None:
            monitor.interactive_reagent = reagent
        def unmonitored_set_reagent(_env: Environment, reagent: Reagent) -> None:
            nonlocal unmonitored_interactive_reagent
            unmonitored_interactive_reagent = reagent
        SpecialVars[name] = MonitorVariable[Reagent](name, Type.REAGENT, getter=get_reagent, setter=set_reagent,
                                                     unmonitored_getter=unmonitored_get_reagent,
                                                     unmonitored_setter=unmonitored_set_reagent)
        
        unmonitored_interactive_volume: Optional[Volume] = None
        name = "interactive volume"
        def get_volume(monitor: BoardMonitor) -> Volume:
            return monitor.interactive_volume
        def unmonitored_get_volume(env: Environment) -> Volume:
            v = unmonitored_interactive_volume
            if v is None:
                v = env.board.drop_size
            return v
        def set_volume(monitor: BoardMonitor, volume: Volume) -> None:
            monitor.interactive_volume = volume
        def unmonitored_set_volume(_env: Environment, volume: Volume) -> None:
            nonlocal unmonitored_interactive_volume
            unmonitored_interactive_volume = volume
        SpecialVars[name] = MonitorVariable[Volume](name, Type.VOLUME, getter=get_volume, setter=set_volume,
                                                    unmonitored_getter=unmonitored_get_volume,
                                                    unmonitored_setter=unmonitored_set_volume)
        
        name = "clicked pad"
        def get_clicked_pad(monitor: BoardMonitor) -> Optional[Pad]:
            # print(f"Monitor looked in is {monitor}")
            c: Optional[BinaryComponent] = monitor.last_clicked
            # print(f"  Last clicked is {c}")
            return c if c is not None and isinstance(c, Pad) else None
        SpecialVars[name] = MonitorVariable[Optional[Pad]](name, Type.PAD.maybe, getter=get_clicked_pad)
        SpecialVars["clicked"] = SpecialVars[name]
        
        name = "clicked drop"
        def get_clicked_drop(monitor: BoardMonitor) -> Optional[Drop]:
            c: Optional[BinaryComponent] = monitor.last_clicked
            return c.drop if c is not None and isinstance(c, DropLoc) else None
            
        SpecialVars[name] = MonitorVariable[Optional[Drop]](name, Type.DROP.maybe, getter=get_clicked_drop)
        
        
        
        name = "missing"
        def get_none(env: Environment) -> None: # @UnusedVariable
            return None
        SpecialVars["missing"] = Constant(Type.MISSING, None)
        SpecialVars["none"] = Constant(Type.MISSING, None)
        
        name = "the board"
        def get_board(env: Environment) -> Board:
            return env.board
        SpecialVars[name] = SpecialVariable[Board](Type.BOARD, getter=get_board)
        
        SpecialVars["AC"] = Constant(Type.POWER_MODE, PowerMode.AC)
        SpecialVars["DC"] = Constant(Type.POWER_MODE, PowerMode.DC)
        SpecialVars["on"] = Constant(Type.ON, OnOff.ON)
        SpecialVars["off"] = Constant(Type.OFF, OnOff.OFF)
        
        # name="index base"
        # def get_index_base(env: Environment) -> int:
        #     return env.index_base
        # def set_index_base(env: Environment, val: int) -> None:
        #     env.index_base = val
        # SpecialVars[name] = SpecialVariable(Type.INT, getter=get_index_base, setter=set_index_base,
        #                                     allowed_vals=(0,1))    
        
    @classmethod
    def setup_attributes(cls) -> None:
        Attributes["gate"].register(Type.WELL, Type.WELL_GATE, lambda well: well.gate)
        Attributes["#exit_pad"].register(Type.WELL, Type.PAD, lambda well: well.exit_pad)
        def set_state(c: BinaryComponent, s: OnOff) -> None:
            c.current_state = s
        Attributes["state"].register(Type.BINARY_CPT, Type.BINARY_STATE, lambda cpt: cpt.current_state)
        Attributes["state"].register_setter(Type.BINARY_CPT, Type.BINARY_STATE, set_state)
        
        Attributes["state"].register(Type.BINARY_CPT, Type.BINARY_STATE, lambda cpt: cpt.current_state)
        Attributes["distance"].register(Type.DELTA, Type.INT, lambda delta: delta.dist)
        Attributes["direction"].register(Type.DELTA, Type.DIR, lambda delta: delta.direction)
        # Attributes["duration"].register(Type.PAUSE, Type.DELAY, lambda pause: pause.duration)
        def set_pad(d: Drop, p: Pad) -> None:
            d.pad = p
            d.status = DropStatus.ON_BOARD
        Attributes["pad"].register(Type.DROP, Type.PAD, lambda drop: drop.pad, setter=set_pad)
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
        Attributes["number"].register((Type.HEATER, Type.CHILLER), Type.INT, lambda h : h.number)
        
        Attributes["volume"].register([Type.LIQUID, Type.WELL], Type.VOLUME, lambda d: d.volume)
        Attributes["volume"].register(Type.DROP, Type.VOLUME, lambda d: d.blob_volume)
        def set_drop_volume(d: Drop, v: Volume) -> None:
            d.blob_volume = v
        Attributes["volume"].register_setter(Type.DROP, Type.VOLUME, set_drop_volume)
        def set_well_volume(w: Well, v: Volume) -> None:
            w.contains(Liquid(w.reagent, v))
        Attributes["volume"].register_setter(Type.WELL, Type.VOLUME, set_well_volume)
        
        Attributes["reagent"].register([Type.DROP, Type.LIQUID, Type.WELL], Type.REAGENT, lambda d: d.reagent)
        def set_drop_reagent(d: Drop, r: Reagent) -> None:
            d.reagent= r
        Attributes["reagent"].register_setter(Type.DROP, Type.REAGENT, set_drop_reagent)
        def set_well_reagent(w: Well, r: Reagent) -> None:
            w.contains(Liquid(r, w.volume))
        Attributes["reagent"].register_setter(Type.WELL, Type.REAGENT, set_well_reagent)
        
        def set_drop_liquid(d: Drop, liq: Liquid) -> None:
            d.blob_volume = liq.volume
            d.reagent= liq.reagent
        Attributes["contents"].register(Type.DROP, Type.LIQUID, lambda d: Liquid(d.reagent, d.volume),
                                        setter=set_drop_liquid)
        
        def set_well_contents(w: Well, liq: Liquid) -> None:
            w.contains(liq)
        Attributes["contents"].register(Type.WELL, Type.LIQUID.maybe, lambda w: Liquid(w.reagent, w.volume),
                                        setter=set_well_contents)
        
        Attributes["capacity"].register(Type.WELL, Type.VOLUME, lambda w: w.capacity)
        Attributes["#remaining_capacity"].register(Type.WELL, Type.VOLUME, lambda w: w.remaining_capacity)
        
        def set_required(w: Well, v: Optional[Volume]) -> None:
            w.required = v
        Attributes["requirement"].register(Type.WELL, Type.VOLUME.maybe, lambda w: w.required,
                                           setter=set_required)
        
        def set_fill_level(w: Well, v: Optional[Volume]) -> None:
            w.compute_max_fill(v)
        Attributes["#fill_level"].register(Type.WELL, Type.VOLUME.maybe, lambda w: w.max_fill,
                                           setter=set_fill_level)
        
        def set_refill_level(w: Well, v: Optional[Volume]) -> None:
            w.compute_min_fill(v)
        Attributes["#refill_level"].register(Type.WELL, Type.VOLUME.maybe, lambda w: w.min_fill,
                                           setter=set_refill_level)
        
            
        
        Attributes["heater"].register((Type.PAD, Type.WELL), Type.HEATER.maybe, lambda p: p.heater)
        Attributes["chiller"].register((Type.PAD, Type.WELL), Type.CHILLER.maybe, lambda p: p.chiller)
        Attributes["magnet"].register(Type.PAD, Type.MAGNET.maybe, lambda p: p.magnet)
        
        Attributes["#current_temperature"].register(Type.TEMP_CONTROL, Type.ABS_TEMP, lambda h: h.current_temperature)
        def set_tc_target(h: TemperatureControl, t: Optional[TemperaturePoint]) -> None:
            h.target = t
        Attributes["#target_temperature"].register(Type.TEMP_CONTROL, Type.ABS_TEMP.maybe, lambda h: h.target)
        Attributes["#target_temperature"].register_setter(Type.TEMP_CONTROL, Type.ABS_TEMP.maybe, set_tc_target)
        
        Attributes["#max_target"].register(Type.HEATER, Type.ABS_TEMP, lambda h: h.max_target)
        Attributes["#min_target"].register(Type.CHILLER, Type.ABS_TEMP, lambda c: c.min_target)
        
        Attributes["#power_supply"].register(Type.BOARD, Type.POWER_SUPPLY.maybe, lambda b: b.find_one(PowerSupply))
        
        def set_ps_voltage(ps: PowerSupply, v: Voltage) -> None:
            ps.voltage = v
        Attributes["voltage"].register(Type.POWER_SUPPLY, Type.VOLTAGE, lambda ps: ps.voltage)
        Attributes["voltage"].register_setter(Type.POWER_SUPPLY, Type.VOLTAGE, set_ps_voltage)
        
        def set_ps_mode(ps: PowerSupply, m: PowerMode) -> None:
            ps.mode = m
        Attributes["mode"].register(Type.POWER_SUPPLY, Type.POWER_MODE, lambda ps: ps.mode)
        Attributes["mode"].register_setter(Type.POWER_SUPPLY, Type.POWER_MODE, set_ps_mode)
        
        Attributes["#min_voltage"].register(Type.POWER_SUPPLY, Type.VOLTAGE, lambda ps: ps.min_voltage)
        Attributes["#max_voltage"].register(Type.POWER_SUPPLY, Type.VOLTAGE, lambda ps: ps.max_voltage)
        
        Attributes["fan"].register(Type.BOARD, Type.FAN.maybe, lambda b: b.find_one(Fan))

DMFCompiler.setup_attributes()
DMFCompiler.setup_function_table()
DMFCompiler.setup_special_vars()

