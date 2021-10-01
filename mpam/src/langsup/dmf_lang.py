from __future__ import annotations

from _collections import defaultdict
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic, Hashable, NamedTuple, Final, \
    Callable, Any, cast, Sequence, Union, Mapping, ClassVar, List
import typing

from antlr4 import InputStream, CommonTokenStream, FileStream, ParserRuleContext, \
    Token
from antlr4.tree.Tree import TerminalNode

from DMFLexer import DMFLexer
from DMFParser import DMFParser
from DMFVisitor import DMFVisitor
from langsup.type_supp import Type, CallableType, MacroType, Signature, Attr,\
    Rel, MaybeType
from mpam.device import Pad, Board, BinaryComponent, WellPad, Well
from mpam.drop import Drop, DropStatus
from mpam.paths import Path
from mpam.types import unknown_reagent, Liquid, Dir, Delayed, OnOff, Barrier, \
    ticks, Ticks, DelayType, Turn, EHSpec, ErrorHandler
from quantities.core import Unit
from quantities.dimensions import Time
from erk.stringutils import map_str



Name_ = TypeVar("Name_", bound=Hashable)
Val_ = TypeVar("Val_")

class EvaluationError(RuntimeError): ...

class MaybeNotSatisfiedError(EvaluationError): ...
        


class Scope(Generic[Name_, Val_]):
    parent: Optional[Scope[Name_,Val_]]
    mapping: dict[Name_, Val_]
    
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
    
    def __init__(self,
                 initial: Optional[Scope[Name_,Val_]] = None):
        self.current = Scope(None) if initial is None else initial
        
    def lookup(self, name: Name_) -> Optional[Val_]:
        return self.current.lookup(name)
    
    def define(self, name: Name_, val: Val_) -> None:
        return self.current.define(name, val)
    
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
    
    @abstractmethod
    def apply(self, args: Sequence[Any]) -> Delayed[Any]: ... # @UnusedVariable
    
class MotionValue(CallableValue):
    @abstractmethod
    def move(self, drop: Drop) -> Delayed[Drop]: ... # @UnusedVariable
    
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
    
    def __init__(self, op: BinaryComponent.ModifyState) -> None:
        self.op = op
        
    def apply(self, args:Sequence[Any])->Delayed[OnOff]: 
        assert len(args) == 1
        bc = args[0]
        assert isinstance(bc, BinaryComponent)
        return self.op.schedule_for(bc)
    
class PauseValue(CallableValue):
    duration: Final[DelayType]
    board: Final[Board]
    
    def __init__(self, duration: DelayType, board: Board) -> None:
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
    sig: Final[Signature]
    static_env: Final[Environment]
    
    def __init__(self, mt: MacroType, env: Environment, param_names: Sequence[str], body: Executable) -> None:
        self.sig = mt.sig
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
    
class WellPadValue(NamedTuple):
    pad: WellPad
    well: Well
    
    def __str__(self) -> str:
        pad = self.pad
        if isinstance(pad.loc, Well):
            return str(pad)
        else:
            return f"({pad}, {self.well})"
    
Attr.GATE.register(Type.WELL, Type.WELL_PAD, lambda well: WellPadValue(well.gate, well))
Attr.EXIT_PAD.register(Type.WELL, Type.PAD, lambda well: well.exit_pad)
Attr.STATE.register(Type.BINARY_CPT, Type.BINARY_STATE, lambda cpt: cpt.current_state)
Attr.DISTANCE.register(Type.DELTA, Type.INT, lambda delta: delta.dist)
Attr.DURATION.register(Type.PAUSE, Type.DELAY, lambda pause: pause.duration)
Attr.PAD.register(Type.DROP, Type.PAD, lambda drop: drop.pad)
Attr.ROW.register(Type.PAD, Type.INT, lambda pad: pad.row)
Attr.COLUMN.register(Type.PAD, Type.INT, lambda pad: pad.column)
Attr.EXIT_DIR.register(Type.WELL, Type.DIR, lambda well: well.exit_dir)
Attr.WELL.register(Type.PAD, Type.WELL.maybe, lambda p: p.well)
Attr.WELL.register(Type.WELL_PAD, Type.WELL, lambda wp: wp.well)
Attr.DROP.register(Type.PAD, Type.DROP.maybe, lambda p: p.drop)

rep_types: Mapping[Type, typing.Type] = {
        Type.DROP: Drop,
        Type.INT: int,
        Type.BINARY_STATE: OnOff,
        Type.BINARY_CPT: BinaryComponent,
        Type.PAD: Pad,
        Type.WELL_PAD: WellPadValue,
        Type.WELL: Well,
        Type.DELTA: DeltaValue,
        Type.MOTION: MotionValue,
        Type.TIME: Time,
        Type.TICKS: Ticks,
        Type.PAUSE: PauseValue,
        Type.DIR: Dir,
        Type.BOOL: bool,
    }

class Conversions:
    known: ClassVar[dict[tuple[Type,Type], Callable[[Any], Any]]] = {}
    known_ok: ClassVar[set[tuple[Type,Type]]] = set()
    
    @classmethod
    def register(cls, have: Type, want: Type, converter: Callable[[Any], Any]) -> None:
        cls.known[(have, want)] = converter
        
    @classmethod
    def ok(cls, have: Type, want: Type) -> None:
        cls.known_ok.add((have,want))
        
    @classmethod
    def convert(cls, have: Type, want: Type, val: Any) -> Any:
        if have is want:
            return val
        if want is Type.ANY:
            return val
        if want is Type.NONE:
            return None
        if isinstance(want, MaybeType):
            if val is None:
                return val
            elif isinstance(have, MaybeType):
                return cls.convert(have.if_there_type, want.if_there_type, val)
            else:
                return cls.convert(have, want.if_there_type, val)
        if (have,want) in cls.known_ok:
            return val
        converter = cls.known.get((have, want), None)
        if converter is not None:
            return converter(val)
        rep = rep_types.get(want, None)
        if rep is not None and isinstance(val, rep):
            return val
        assert False, f"Don't know how to convert from {have} to {want}: {val}"
    
Conversions.register(Type.DROP, Type.PAD,
                     lambda drop: drop.pad)
Conversions.register(Type.DROP, Type.BINARY_CPT,
                     lambda drop: drop.pad)
Conversions.ok(Type.TIME, Type.DELAY)
Conversions.ok(Type.TICKS, Type.DELAY)
Conversions.register(Type.WELL_PAD, Type.BINARY_CPT,
                     lambda wp: wp.pad)



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
                return Conversions.convert(have=self.return_type, want=req_type, val=val)
            future = future.transformed(convert)
        # if required is not None: 
        #     check = rep_types.get(required, None)
        #     if check is not None:
        #         assert isinstance(val, check), f"Expected {check}, got {val}"
        return future
    
    
    
    
class DMFInterpreter:
    globals: Final[Environment]
    namespace: Final[TypeMap]
    
    def __init__(self, file_name: Optional[str], *, board: Board, encoding: str='ascii', errors: str='strict') -> None:
        self.globals = Environment(None, board=board)
        if file_name is not None:
            parser = self.get_parser(FileStream(file_name, encoding, errors))
            tree = parser.macro_file()
            assert isinstance(tree, DMFParser.Macro_fileContext)
            compiler = DMFCompiler()
            ns = compiler.global_types
            executable = compiler.visit(tree)
            assert isinstance(executable, Executable)
            if executable.contains_error:
                print(f"Macro file '{file_name}' contained error, not loading.")
            else:
                executable.evaluate(self.globals).wait()
        else:
            ns = TypeMap(None)
        self.namespace = ns
        
    def set_global(self, name: str, val: Any, vtype: Type):
        self.namespace[name] = vtype
        self.globals[name] = val
        
        
    def evaluate(self, expr: str, required: Optional[Type] = None, *, 
                 cache_as: Optional[str] = None,
                 on_error: Optional[EHSpec] = None
                 ) -> Delayed[tuple[Type, Any]]:
        parser = self.get_parser(InputStream(expr))
        tree = parser.interactive()
        assert isinstance(tree, DMFParser.InteractiveContext)
        compiler = DMFCompiler(global_types = self.namespace)
        executable = compiler.visit(tree)
        assert isinstance(executable, Executable)
        if executable.contains_error:
            print("Expression contained error, not evaluating.")
            return Delayed.complete((executable.return_type, None))
        future = Delayed.computed(lambda :executable.evaluate(self.globals, required=required),
                                  on_error=on_error)
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
    
    default_creators = defaultdict[Type,Callable[[Environment],Any]](lambda: (lambda _: None),
                                                          {Type.INT: lambda _: 0,
                                                           Type.PAD: lambda env: env.board.pad_at(0,0) 
                                                          })
    
    def __init__(self, *,
                 global_types: Optional[TypeMap] = None) -> None:
        self.global_types = global_types if global_types is not None else TypeMap(None)
        self.current_types = ScopeStack(self.global_types)
        
    def defaultResult(self) -> Executable:
        print("Unhandled tree")
        return Executable(Type.ERROR, lambda _: Delayed.complete(None), is_error=True)
        # assert False, "Undefined visitor method"
        
    def visitChildren(self, node):
        print(f"Unhandled tree: {type(node).__name__}")
        return Executable(Type.ERROR, lambda _: Delayed.complete(None), is_error=True)
    
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
        
    def text_of(self, ctx_or_token: Union[ParserRuleContext, TerminalNode]) -> str:
        if isinstance(ctx_or_token, TerminalNode):
            t: str = ctx_or_token.getText()
            return t
        return " ".join(self.text_of(child) for child in ctx_or_token.getChildren())

    def type_name_var(self, ctx: DMFParser.Param_typeContext, n: Optional[int] = None):
        t: Type = cast(Type, ctx.type)
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
            if have <= want:
                return None
            else:
                wname = want.name
        else:
            if any(have <= w for w in want):
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


    def visitAssignment_interactive(self, ctx:DMFParser.Assignment_interactiveContext) -> Executable:
        return self.visit(ctx.assignment())


    def visitExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext) -> Executable:
        return self.visit(ctx.expr())
    
    def visitEmpty_interactive(self, ctx:DMFParser.Empty_interactiveContext) -> Executable: # @UnusedVariable
        return Executable(Type.IGNORE, lambda env: Delayed.complete(None)) # @UnusedVariable

    
    # def visitAssignment_tls(self, ctx:DMFParser.Assignment_tlsContext) -> Executable:
    #     return self.visit(ctx.assignment())
    #
    # def visitMacro_def_tls(self, ctx:DMFParser.Macro_def_tlsContext) -> Executable:
    #     return 0



    def visitAssignment(self, ctx:DMFParser.AssignmentContext) -> Executable:
        name_ctx = cast(DMFParser.NameContext, ctx.which)
        name = self.text_of(name_ctx)
        value = self.visit(ctx.what)
        required_type = self.current_types.lookup(name)
        if required_type is not None:
            if e := self.type_check(required_type, value.return_type, ctx, 
                                    lambda want,have,text: # @UnusedVariable
                                        f"variable '{name}' has type {have}.  Expr has type {want}",
                                    return_type=required_type):
                return e
        returned_type = required_type if required_type is not None else value.return_type
        # print(f"Compiling assignment: {name} : {returned_type}")
        if required_type is None and not value.contains_error:
            self.current_types[name] = returned_type
        def run(env: Environment) -> Delayed[Any]:
            def do_assignment(val) -> Any:
                env[name] = val
                # print(f"Assigned {name} := {val}")
                return val
            return value.evaluate(env, required_type).transformed(do_assignment)
        return Executable(returned_type, run, (value,))


    def visitAssign_stat(self, ctx:DMFParser.Assign_statContext) -> Executable:
        return self.visit(ctx.assignment())

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
            future = Delayed[None]()
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
            if result_type is None or result_type <= t:
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
    

    def visitParen_expr(self, ctx:DMFParser.Paren_exprContext) -> Executable:
        return self.visit(ctx.expr())


    def visitNeg_expr(self, ctx:DMFParser.Neg_exprContext) -> Executable:
        rhs = self.visit(ctx.rhs)
        if e := self.type_check(Type.INT, rhs, ctx,
                                lambda w,h,t: # @UnusedVariable
                                    f"Can't negate {h}: {t}",
                                return_type = Type.INT):
            return e

        def run(env: Environment) -> Delayed[int]:
            def compute(x: int):
                return -x
            return rhs.evaluate(env, Type.INT).transformed(compute)
        return Executable(Type.INT, run, (rhs,))



    def visitInt_expr(self, ctx:DMFParser.Int_exprContext):
        val: int = int(ctx.INT().getText())
        return Executable(Type.INT, lambda _: Delayed.complete(val))


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
        well = self.visit(ctx.who)
        which = self.visit(ctx.which)
        if (e:=self.type_check(Type.WELL, well, ctx.who,
                               lambda want,have,text:               # @UnusedVariable
                                    f"Not a well ({have}): {text}",
                               return_type=Type.WELL_PAD)):
            return e
        if (e:=self.type_check(Type.INT, which, ctx.which,
                               lambda want,have,text:               # @UnusedVariable
                                    f"Not an integer ({have}): {text}",
                               return_type=Type.WELL_PAD)):
            return e
                               
        def run(env: Environment) -> Delayed[WellPadValue]:
            f: Delayed[Well] = well.evaluate(env, Type.WELL)
            return f.chain(lambda w: (which.evaluate(env, Type.INT)
                                            .transformed(lambda n: WellPadValue(w.group.shared_pads[cast(int, n)],
                                                                                w)))
                )
        return Executable(Type.WELL_PAD, run, (well, which))
    


    def visitMacro_expr(self, ctx:DMFParser.Macro_exprContext) -> Executable:
        return self.visit(ctx.macro_def())

    def visitTwiddle_expr(self, ctx:DMFParser.Twiddle_exprContext) -> Executable:
        op = (BinaryComponent.Toggle if ctx.TOGGLE() is not None
              else BinaryComponent.TurnOn if ctx.ON() is not None
              else BinaryComponent.TurnOff)
        val = TwiddlePadValue(op)
        return Executable(Type.TWIDDLE_OP, lambda _ : Delayed.complete(val))

    def visitName_expr(self, ctx:DMFParser.Name_exprContext) -> Executable:
        name = self.text_of(ctx.name())
        var_type = self.current_types.lookup(name)
        if var_type is None:
            return self.error(ctx.name(), Type.NONE, f"Undefined variable: {name}")
        def run(env: Environment) -> Delayed[Any]:
            return Delayed.complete(env[name])
        return Executable(var_type, run)

    def visitBool_const_expr(self, ctx:DMFParser.Bool_const_exprContext) -> Executable:
        val = ctx.bool_val().val
        return Executable(Type.BOOL, lambda _: Delayed.complete(val))

    def visitAddsub_expr(self, ctx:DMFParser.Addsub_exprContext) -> Executable:
        lhs = self.visit(ctx.lhs)
        rhs = self.visit(ctx.rhs)
        addp = ctx.ADD() is not None
        if lhs.return_type <= Type.INT and rhs.return_type <= Type.INT:
            def run_int(env: Environment) -> Delayed[int]:
                def combine(x: int, y: int) -> int:
                    return x+y if addp else x-y
                future: Delayed[int] = lhs.evaluate(env, Type.INT)
                return future.chain(lambda x: (rhs.evaluate(env, Type.INT)
                                               .transformed(lambda y: combine(x,y))))
            return Executable(Type.INT, run_int, (lhs,rhs))
        elif lhs.return_type <= Type.PAD and rhs.return_type <= Type.DELTA:
            def run_delta(env: Environment) -> Delayed[Pad]:
                def combine(p: Pad, d: DeltaValue) -> Pad:
                    n = d.dist if addp else -d.dist
                    board = env.board
                    loc = board.orientation.neighbor(d.direction, p.location, steps=n)
                    return board.pads[loc]
                return (lhs.evaluate(env, Type.PAD)
                        .chain(lambda p: (rhs.evaluate(env, Type.DELTA)
                                          .transformed(lambda d: combine(p,d)))))
            return Executable(Type.PAD, run_delta, (lhs, rhs))
        elif lhs.return_type <= Type.TIME and rhs.return_type <= Type.TIME:
            def run_time(env: Environment) -> Delayed[Time]:
                def combine(x: Time, y: Time) -> Time:
                    return x+y if addp else x-y
                future: Delayed[Time] = lhs.evaluate(env, Type.TIME)
                return future.chain(lambda x: (rhs.evaluate(env, Type.TIME)
                                               .transformed(lambda y: combine(x,y))))
            return Executable(Type.TIME, run_time, (lhs,rhs))
        elif lhs.return_type <= Type.TICKS and rhs.return_type <= Type.TICKS:
            def run_ticks(env: Environment) -> Delayed[Ticks]:
                def combine(x: Ticks, y: Ticks) -> Ticks:
                    return x+y if addp else x-y
                future: Delayed[Ticks] = lhs.evaluate(env, Type.TICKS)
                return future.chain(lambda x: (rhs.evaluate(env, Type.TICKS)
                                               .transformed(lambda y: combine(x,y))))
            return Executable(Type.TICKS, run_ticks, (lhs,rhs))
            
        if addp:
            return self.error(ctx, Type.NONE,
                              f"Can't add {lhs.return_type.name} and {rhs.return_type.name}: {self.text_of(ctx)}")
        else:
            return self.error(ctx, Type.NONE,
                              f"Can't subtract {rhs.return_type.name} from {lhs.return_type.name}: {self.text_of(ctx)}")
            


    def visitRel_expr(self, ctx:DMFParser.Rel_exprContext) -> Executable:
        lhs = self.visit(ctx.lhs)
        rhs = self.visit(ctx.rhs)
        rel: Rel = ctx.rel().which
        ok_types = (Type.INT, Type.TIME, Type.TICKS)
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
        attr: Attr = ctx.attr().which
        desc = attr[obj.return_type]
        if desc is not None:
            ot, rt, extractor = desc
            if not isinstance(rt, MaybeType):
                self.error(ctx.attr(), Type.BOOL,
                           lambda txt:  f"{txt} is not a 'maybe' attribute. 'has' will always return True.")
                return Executable(Type.BOOL, (lambda _: Delayed.complete(True)), (obj,))
            def run(env: Environment) -> Delayed[Any]:
                f: Delayed = obj.evaluate(env, ot)
                return f.transformed(lambda o: extractor(o) is not None)
            return Executable(Type.BOOL, run, (obj,))
        types = attr.known_types
        if len(types) == 0:
            return self.error(ctx.attr(), Type.NONE,
                              lambda txt: f"{txt} is an attribute, but I don't know what to do with it")
        if len(types) == 1:
            e = self.type_check(types[0], obj.return_type, ctx.obj)
            assert e is not None
            return e
        
        a = self.text_of(ctx.attr())
        otn = obj.return_type.name
        tns = map_str(tuple(t.name for t in types))
        
        def emessage(text: str) -> str:
            return f"{otn}.{a} not defined, requires one of {tns}: {text}"
        return self.error(ctx.obj, Type.NONE, emessage)

    def visitNot_expr(self, ctx:DMFParser.Not_exprContext) -> Executable:
        arg = self.visit(ctx.expr())
        if e := self.type_check(Type.BOOL, arg.return_type, ctx.expr(), return_type=Type.BOOL):
            return e
        def run(env: Environment) -> Delayed[bool]:
            return arg.evaluate(env, Type.BOOL).transformed(lambda v: not v)
        return Executable(Type.BOOL, run, (arg,))
    
    def visitAnd_expr(self, ctx:DMFParser.And_exprContext) -> Executable:
        lhs = self.visit(ctx.lhs)
        rhs = self.visit(ctx.rhs)
        if e := self.type_check(Type.BOOL, lhs.return_type, ctx.lhs, return_type=Type.BOOL):
            return e
        if e := self.type_check(Type.BOOL, rhs.return_type, ctx.rhs, return_type=Type.BOOL):
            return e
        def run(env: Environment) -> Delayed[bool]:
            def combine(x: bool, y: bool) -> bool:
                return x and y
            future: Delayed = lhs.evaluate(env, Type.BOOL)
            return future.chain(lambda x: (rhs.evaluate(env, Type.BOOL)
                                            .transformed(lambda y: combine(x,y))))
        return Executable(Type.BOOL, run, (lhs,rhs))
    
    def visitOr_expr(self, ctx:DMFParser.Or_exprContext) -> Executable:
        lhs = self.visit(ctx.lhs)
        rhs = self.visit(ctx.rhs)
        if e := self.type_check(Type.BOOL, lhs.return_type, ctx.lhs, return_type=Type.BOOL):
            return e
        if e := self.type_check(Type.BOOL, rhs.return_type, ctx.rhs, return_type=Type.BOOL):
            return e
        def run(env: Environment) -> Delayed[bool]:
            def combine(x: bool, y: bool) -> bool:
                return x or y
            future: Delayed = lhs.evaluate(env, Type.BOOL)
            return future.chain(lambda x: (rhs.evaluate(env, Type.BOOL)
                                            .transformed(lambda y: combine(x,y))))
        return Executable(Type.BOOL, run, (lhs,rhs))
    
    def visitCond_expr(self, ctx:DMFParser.Cond_exprContext) -> Executable:
        first = self.visit(ctx.first)
        cond = self.visit(ctx.cond)
        second = self.visit(ctx.second)
        if e := self.type_check(Type.BOOL, cond, ctx.cond):
            return e
        if first.return_type <= second.return_type:
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
        return Executable(Type.DIR, lambda _: Delayed.complete(direction))
    
    def visitTurn_expr(self, ctx:DMFParser.Turn_exprContext) -> Executable:
        start = self.visit(ctx.start_dir) 
        if e:=self.type_check(Type.DIR, start, ctx.start_dir, return_type=Type.DIR):
            return e
        t: Turn = ctx.turn().t
        def run(env: Environment) -> Delayed[Dir]:
            return (start.evaluate(env, Type.DIR)
                    .transformed(lambda d: cast(Dir, d).turned(t))
                    )
        return Executable(Type.DIR, run, (start,))
    
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
        def run(env: Environment) -> Delayed[DeltaValue]: # @UnusedVariable
            return (Delayed.complete(DeltaValue(n, direction)))
        return Executable(Type.DELTA, run)

    
    def visitCoord_expr(self, ctx:DMFParser.Coord_exprContext) -> Executable:
        x = self.visit(ctx.x)
        y = self.visit(ctx.y)
        if e:=self.type_check(Type.INT, x, ctx.x,
                              lambda want,have,text: f"x coordinate ({have}) must be {want}: {text}",
                              return_type=Type.PAD):
            return e
        if e:=self.type_check(Type.INT, y, ctx.y,
                              lambda want,have,text: f"y coordinate ({have}) must be {want}: {text}",
                              return_type=Type.PAD):
            return e
        def run(env: Environment) -> Delayed[Pad]:
            return (x.evaluate(env, Type.INT)
                    .chain(lambda xc: (y.evaluate(env, Type.INT)
                                       .transformed(lambda yc: env.board.pad_at(xc, yc))))
                    )
        return Executable(Type.PAD, run, (x,y))



    def visitInjection_expr(self, ctx:DMFParser.Injection_exprContext) -> Executable:
        who = self.visit(ctx.who)
        what = self.visit(ctx.what)
        inj_type = what.return_type
        if inj_type <= Type.MOTION:
            inj_type = Type.MOTION
        if not isinstance(inj_type, CallableType) or len(inj_type.param_types) != 1:
            return self.error(ctx.what, Type.NONE, 
                              f"Not an injection target ({what.return_type.name}): {self.text_of(ctx.what)}")
        first_arg_type = inj_type.param_types[0]
        return_first_arg = inj_type.return_type is Type.NONE
        return_type = who.return_type if return_first_arg else inj_type.return_type
        if e:=self.type_check(first_arg_type, who, ctx.who,
                              lambda want,have,text:
                                f"Injected value ({have}) '{text}' not compatible with "
                                +f"{want}: {self.text_of(ctx.what)}",
                              return_type=return_type):
            return e
        
        def run(env: Environment) -> Delayed[Any]:
            dc = ErrorHandler.get_prevailing() is ErrorHandler.default_handler
            print(f"Prevailing is default (injection): {dc}")
            def inject(obj, func) -> Delayed[Any]:
                assert isinstance(func, CallableValue)
                future = func.apply((obj,))
                return future if not return_first_arg else future.transformed(lambda _: obj)
            return (who.evaluate(env, first_arg_type)
                    .chain(lambda obj: (what.evaluate(env)
                                        .chain(lambda func: inject(obj, func)))))
        # print(f"Injection returns {inj_type.return_type}: {self.text_of(ctx)}")
        return Executable(return_type, run, (who, what))
            
    
    def visitAttr_expr(self, ctx:DMFParser.Attr_exprContext) -> Executable:
        obj = self.visit(ctx.obj)
        attr: Attr = ctx.attr().which
        desc = attr[obj.return_type]
        if desc is not None:
            ot, rt, extractor = desc
            if isinstance(rt, MaybeType):
                real_extractor = extractor
                def extractor(obj):
                    v = real_extractor(obj)
                    if v is None:
                        raise MaybeNotSatisfiedError(f"{obj} does not have {attr}")
                    return v
                rt = rt.if_there_type
            def run(env: Environment) -> Delayed[Any]:
                f: Delayed = obj.evaluate(env, ot)
                return f.transformed(extractor)
            return Executable(rt, run, (obj,))
        types = attr.known_types
        if len(types) == 0:
            return self.error(ctx.attr(), Type.NONE,
                              lambda txt: f"{txt} is an attribute, but I don't know what to do with it")
        if len(types) == 1:
            e = self.type_check(types[0], obj.return_type, ctx.obj)
            assert e is not None
            return e
        
        a = self.text_of(ctx.attr())
        otn = obj.return_type.name
        tns = map_str(tuple(t.name for t in types))
        
        def emessage(text: str) -> str:
            return f"{otn}.{a} not defined, requires one of {tns}: {text}"
        return self.error(ctx.obj, Type.NONE, emessage)


    # def visitGate_expr(self, ctx:DMFParser.Gate_exprContext) -> Executable:
    #     well = self.visit(ctx.well)
    #     if e:=self.type_check(Type.WELL, well, ctx.well, return_type=Type.WELL_PAD):
    #         return e
    #     def run(env: Environment) -> Delayed[WellPad]:
    #         f: Delayed[Well] = well.evaluate(env, Type.WELL)
    #         return f.transformed(lambda w: w.gate)
    #     return Executable(Type.WELL_PAD, run, (well,))
    #
    # def visitExit_pad_expr(self, ctx:DMFParser.Exit_pad_exprContext) -> Executable:
    #     well = self.visit(ctx.well)
    #     if e:=self.type_check(Type.WELL, well, ctx.well, return_type=Type.PAD):
    #         return e
    #     def run(env: Environment) -> Delayed[Pad]:
    #         f: Delayed[Well] = well.evaluate(env, Type.WELL)
    #         return f.transformed(lambda w: w.exit_pad)
    #     return Executable(Type.PAD, run, (well,))


    def visitWell_expr(self, ctx:DMFParser.Well_exprContext) -> Executable:
        which = self.visit(ctx.which)
        if e:=self.type_check(Type.INT, which, ctx.which, return_type=Type.WELL):
            return e
        def run(env: Environment) -> Delayed[Well]:
            f: Delayed[int] = which.evaluate(env, Type.INT)
            return f.transformed(lambda n: env.board.wells[n])
        return Executable(Type.WELL, run, (which,))



    def visitDrop_expr(self, ctx:DMFParser.Drop_exprContext) -> Executable:
        loc_exec = self.visit(ctx.loc)
        if e:=self.type_check(Type.PAD, loc_exec, ctx.loc, return_type=Type.DROP):
            return e
        def run(env: Environment) -> Delayed[Drop]:
            def get_drop(pad: Pad) -> Drop:
                drop = pad.drop
                if drop is None:
                    liquid = Liquid(unknown_reagent, env.board.drop_size)
                    drop = Drop(pad, liquid)
                return drop
            return loc_exec.evaluate(env, Type.PAD).transformed(get_drop)
        return Executable(Type.DROP, run, (loc_exec,))


    def visitFunction_expr(self, ctx:DMFParser.Function_exprContext) -> Executable:
        f_name = self.text_of(ctx.name())
        arg_execs = tuple(self.visit(arg) for arg in ctx.args)
        f_type = self.current_types.lookup(f_name)
        if f_type is None:
            return self.error(ctx.name(), Type.NONE, f"Undefined macro: {f_name}")
        if not isinstance(f_type, CallableType):
            return self.error(ctx.name(), Type.NONE, f"Not a macro ({f_type.name}): {f_name}")
        ret_type = f_type.return_type
        param_types = f_type.param_types
        for i in range(len(param_types)):
            if not arg_execs[i].return_type <= param_types[i]:
                ac = ctx.args[i]
                ae = arg_execs[i]
                pt = param_types[i]
                return self.error(ac, ret_type, f"Argument {i+1} not {pt.name} ({ae.return_type.name}): {self.text_of(ac)}")
        
        def run(env: Environment) -> Delayed[Any]:
            func = env[f_name]
            assert isinstance(func, CallableValue)
            args: List[Any] = []
            future: Optional[Delayed[Any]] = None
            for ae,pt in zip(arg_execs, param_types):
                if future is None:
                    future = ae.evaluate(env, pt)
                else:
                    future = future.chain(lambda _: ae.evaluate(env, pt))
                future = future.transformed(lambda arg: args.append(arg))
            if future is None:
                future = Delayed.complete(None)
            future = future.chain(lambda _: cast(Delayed[Any], func.apply(args)))
            return future
        
        return Executable(ret_type, run, arg_execs)


    def visitTo_expr(self, ctx:DMFParser.To_exprContext) -> Executable:
        axis: Optional[DMFParser.AxisContext] = ctx.axis()
        which = self.visit(ctx.which)
        if axis is None:
            # This is a to-pad motion
            if not which.return_type <= Type.PAD:
                if which.return_type <= Type.INT:
                    return self.error(ctx, Type.MOTION, f"Did you forget 'row' or 'column'?: {self.text_of(ctx)}")
                return self.error(ctx, Type.MOTION, f"'to' expr without 'row' or 'column' takes a PAD: {self.text_of(ctx)}")
            def run(env: Environment) -> Delayed[MotionValue]:
                return which.evaluate(env, Type.PAD).transformed(lambda pad: ToPadValue(pad))
        else:
            if not which.return_type <= Type.INT:
                return self.error(ctx.which, Type.MOTION, 
                                  f"Row or column name not an int ({which.return_type.name}): {self.text_of(ctx.which)}")
            verticalp = cast(bool, axis.verticalp)
            def run(env: Environment) -> Delayed[MotionValue]:
                return which.evaluate(env, Type.PAD).transformed(lambda n: ToRowColValue(n, verticalp))
        return Executable(Type.MOTION, run, (which,))
    
    def visitRemove_expr(self, ctx:DMFParser.Remove_exprContext) -> Executable: # @UnusedVariable
        def run(env: Environment) -> Delayed[MotionValue]: # @UnusedVariable
            return Delayed.complete(RemoveDropValue())
        return Executable(Type.MOTION, run, ())


    def visitMuldiv_expr(self, ctx:DMFParser.Muldiv_exprContext)->Executable:
        lhs = self.visit(ctx.lhs)
        rhs = self.visit(ctx.rhs)
        mulp = ctx.MUL() is not None
        if lhs.return_type <= Type.INT and rhs.return_type <= Type.INT:
            def run_int(env: Environment) -> Delayed[int]:
                def combine(x: int, y: int) -> int:
                    return x*y if mulp else int(x/y)
                future: Delayed[int] = lhs.evaluate(env, Type.INT)
                return future.chain(lambda x: (rhs.evaluate(env, Type.INT)
                                               .transformed(lambda y: combine(x,y))))
            return Executable(Type.INT, run_int, (lhs, rhs))
        if mulp and lhs.return_type <= Type.INT and rhs.return_type <= Type.TIME:
            def run_int_time(env: Environment) -> Delayed[Time]:
                def combine(x: int, y: Time) -> Time:
                    return x*y
                future: Delayed[int] = lhs.evaluate(env, Type.INT)
                return future.chain(lambda x: (rhs.evaluate(env, Type.TIME)
                                               .transformed(lambda y: combine(x,y))))
            return Executable(Type.TIME, run_int_time, (lhs, rhs))
        if lhs.return_type <= Type.TIME and rhs.return_type <= Type.INT:
            def run_time_int(env: Environment) -> Delayed[Time]:
                def combine(x: Time, y: int) -> Time:
                    return x*y if mulp else x/y
                future: Delayed[Time] = lhs.evaluate(env, Type.TIME)
                return future.chain(lambda x: (rhs.evaluate(env, Type.INT)
                                               .transformed(lambda y: combine(x,y))))
            return Executable(Type.TIME, run_time_int, (lhs, rhs))
        if mulp and lhs.return_type <= Type.INT and rhs.return_type <= Type.TICKS:
            def run_int_ticks(env: Environment) -> Delayed[Ticks]:
                def combine(x: int, y: Ticks) -> Ticks:
                    return x*y
                future: Delayed[int] = lhs.evaluate(env, Type.INT)
                return future.chain(lambda x: (rhs.evaluate(env, Type.TICKS)
                                               .transformed(lambda y: combine(x,y))))
            return Executable(Type.TICKS, run_int_ticks, (lhs, rhs))
        if lhs.return_type <= Type.TICKS and rhs.return_type <= Type.INT:
            def run_ticks_int(env: Environment) -> Delayed[Ticks]:
                def combine(x: Ticks, y: int) -> Ticks:
                    return x*y if mulp else x/y
                future: Delayed[Ticks] = lhs.evaluate(env, Type.TICKS)
                return future.chain(lambda x: (rhs.evaluate(env, Type.INT)
                                               .transformed(lambda y: combine(x,y))))
            return Executable(Type.TIME, run_ticks_int, (lhs, rhs))
            
        if mulp:
            return self.error(ctx, Type.NONE,
                              f"Can't multiply {lhs.return_type.name} and {rhs.return_type.name}: {self.text_of(ctx)}")
        else:
            return self.error(ctx, Type.NONE,
                              f"Can't divide {lhs.return_type.name} by {rhs.return_type.name}: {self.text_of(ctx)}")


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
        

    def visitTime_expr(self, ctx:DMFParser.Time_exprContext) -> Executable:
        duration = self.visit(ctx.duration)
        unit_ctx: DMFParser.Time_unitContext = ctx.time_unit()
        unit = cast(Unit[Time], unit_ctx.unit)
        if e:=self.type_check(Type.INT, duration, ctx.duration, return_type = Type.TIME):
            return e
        def run(env: Environment) -> Delayed[Time]:
            return duration.evaluate(env, Type.INT).transformed(lambda n: cast(int,n)*unit)
        return Executable(Type.TIME, run, (duration,))
    
    def visitTicks_expr(self, ctx:DMFParser.Ticks_exprContext) -> Executable:
        duration = self.visit(ctx.duration)
        if e:=self.type_check(Type.INT, duration, ctx.duration, return_type = Type.TICKS):
            return e
        def run(env: Environment) -> Delayed[Ticks]:
            return duration.evaluate(env, Type.INT).transformed(lambda n: cast(int,n)*ticks)
        return Executable(Type.TICKS, run, (duration,))
    
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

