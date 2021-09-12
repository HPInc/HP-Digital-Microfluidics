from __future__ import annotations

from _collections import defaultdict
from typing import Optional, TypeVar, Generic, Hashable, NamedTuple, Final, \
    Callable, Any, cast, Sequence, Union, Mapping, ClassVar, List

from antlr4 import InputStream, CommonTokenStream, FileStream, ParserRuleContext,\
    Token
from antlr4.tree.Tree import TerminalNode

from DMFLexer import DMFLexer
from DMFParser import DMFParser
from DMFVisitor import DMFVisitor
from langsup.type_supp import Type, CallableType, MacroType, Signature
from mpam.device import Pad, Board, BinaryComponent, WellPad, Well
from mpam.drop import Drop
from mpam.types import unknown_reagent, Liquid, Dir, Delayed, OnOff, Barrier
from abc import ABC, abstractmethod
import typing
from mpam.paths import Path


Name_ = TypeVar("Name_", bound=Hashable)
Val_ = TypeVar("Val_")

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
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
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
    def apply(self, env: Environment, args: Sequence[Any]) -> Delayed[Any]: ... # @UnusedVariable
    
class MotionValue(CallableValue):
    @abstractmethod
    def move(self, env: Environment, drop: Drop) -> Delayed[Drop]: ... # @UnusedVariable
    
    def apply(self, env:Environment, args:Sequence[Any])->Delayed[Drop]:
        assert len(args) == 1
        drop = args[0]
        assert isinstance(drop, Drop)
        return self.move(env, drop)
        
    
class DeltaValue(MotionValue):
    dist: Final[int]
    direction: Final[Dir]
    
    def __init__(self, dist: int, direction: Dir) -> None:
        self.dist = dist
        self.direction = direction
        
    def move(self, env:Environment, drop:Drop)->Delayed[Drop]:
        path = Path.walk(self.direction, steps = self.dist)
        return path.schedule_for(drop)
    
class ToPadValue(MotionValue):
    dest: Final[Pad]
    
    def __init__(self, pad: Pad) -> None:
        self.dest = pad
        
    def move(self, env:Environment, drop:Drop)->Delayed[Drop]:
        path = Path.to_pad(self.dest)
        return path.schedule_for(drop)

class ToRowColValue(MotionValue):
    dest: Final[int]
    verticalp: Final[bool]
    
    def __init__(self, dest: int, verticalp: bool) -> None:
        self.dest = dest
        self.verticalp = verticalp
        
    def move(self, env:Environment, drop:Drop)->Delayed[Drop]:
        if self.verticalp:
            path = Path.to_row(self.dest)
        else:
            path = Path.to_col(self.dest)
        return path.schedule_for(drop)
    
class TwiddlePadValue(CallableValue):
    op: Final[BinaryComponent.ModifyState]
    
    def __init__(self, op: BinaryComponent.ModifyState) -> None:
        self.op = op
        
    def apply(self, env:Environment, args:Sequence[Any])->Delayed[OnOff]:
        assert len(args) == 1
        bc = args[0]
        assert isinstance(bc, BinaryComponent)
        return self.op.schedule_for(bc)

class MacroValue(CallableValue):
    param_names: Final[Sequence[str]]
    body: Final[Executable]
    sig: Final[Signature]
    
    def __init__(self, mt: MacroType, param_names: Sequence[str], body: Executable) -> None:
        self.sig = mt.sig
        self.param_names = param_names
        self.body = body
        
    def apply(self, env:Environment, args:Sequence[Any])->Delayed[Any]:
        bindings = dict(zip(self.param_names, args))
        local_env = env.new_child(bindings)
        return self.body.evaluate(local_env)
    
    def __str__(self) -> str:
        params = ", ".join(f"{n}: {t}" for n,t in zip(self.param_names, self.sig.param_types)) # @UnusedVariable
        return f"macro({params})->{self.sig.return_type}"
        
rep_types: Mapping[Type, typing.Type] = {
        Type.DROP: Drop,
        Type.INT: int,
        Type.BINARY_STATE: OnOff,
        Type.BINARY_CPT: BinaryComponent,
        Type.PAD: Pad,
        Type.WELL_PAD: WellPad,
        Type.WELL: Well,
        Type.DELTA: DeltaValue,
        Type.MOTION: MotionValue
    }

class Conversions:
    known: ClassVar[dict[tuple[Type,Type], Callable[[Any], Any]]] = {}
    
    @classmethod
    def register(self, have: Type, want: Type, converter: Callable[[Any], Any]) -> None:
        self.known[(have, want)] = converter
        
    @classmethod
    def convert(cls, have: Type, want: Type, val: Any) -> Any:
        if have is want:
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

class Executable(NamedTuple):
    return_type: Type
    func: Callable[[Environment], Delayed[Any]]
    
    def evaluate(self, env: Environment, required: Optional[Type] = None) -> Delayed[Any]:
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
    
    def __init__(self, file_name: str, *, board: Board, encoding: str='ascii', errors: str='strict') -> None:
        self.globals = Environment(None, board=board)
        parser = self.get_parser(FileStream(file_name, encoding, errors))
        tree = parser.macro_file()
        assert isinstance(tree, DMFParser.Macro_fileContext)
        compiler = DMFCompiler()
        self.namespace = compiler.global_types
        executable = compiler.visit(tree)
        assert isinstance(executable, Executable)
        executable.evaluate(self.globals).wait()
        
    def evaluate(self, expr: str, required: Optional[Type] = None) -> Delayed[Any]:
        parser = self.get_parser(InputStream(expr))
        tree = parser.interactive()
        assert isinstance(tree, DMFParser.InteractiveContext)
        compiler = DMFCompiler(global_types = self.namespace)
        executable = compiler.visit(tree)
        assert isinstance(executable, Executable)
        return executable.evaluate(self.globals, required=required)
    
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
        
    def defaultResult(self):
        assert False, "Undefined visitor method"
    
        
    def error(self, ctx:ParserRuleContext, return_type: Type, msg:str) -> Executable:
        print(f"line {ctx.start.line}:{ctx.start.column} {msg}")
        return Executable(return_type, self.default_creators[return_type])
        
    def text_of(self, ctx_or_token: Union[ParserRuleContext, TerminalNode]) -> str:
        if isinstance(ctx_or_token, TerminalNode):
            t: str = ctx_or_token.getText()
            return t
        return " ".join(self.text_of(child) for child in ctx_or_token.getChildren())

    def type_name_var(self, ctx: DMFParser.Param_typeContext, n: Optional[int] = None):
        t: Type = cast(Type, ctx.type)
        index = "" if n is None else f"_{n}"
        return f"**{t.name}{index}**"
        
        
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
        return Executable(Type.NONE, run)


    def visitCompound_interactive(self, ctx:DMFParser.Compound_interactiveContext):
        return DMFVisitor.visitCompound_interactive(self, ctx)


    def visitAssignment_interactive(self, ctx:DMFParser.Assignment_interactiveContext):
        return DMFVisitor.visitAssignment_interactive(self, ctx)


    def visitExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext):
        return DMFVisitor.visitExpr_interactive(self, ctx)

    
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
        if required_type is not None and not required_type <= value.return_type:
            return self.error(ctx, required_type,
                              f"variable '{name}' has type {required_type.name}.  Expr has type {value.return_type.name}")
        returned_type = required_type if required_type is not None else value.return_type
        # print(f"Compiling assignment: {name} : {returned_type}")
        if required_type is None:
            self.current_types[name] = returned_type
        def run(env: Environment) -> Delayed[Any]:
            def do_assignment(val) -> Any:
                env[name] = val
                print(f"Assigned {name} := {val}")
                return val
            return value.evaluate(env, required_type).transformed(do_assignment)
        return Executable(returned_type, run)


    def visitAssign_stat(self, ctx:DMFParser.Assign_statContext) -> Executable:
        return self.visit(ctx.assignment())



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
        return Executable(ret_type, run)



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
        return Executable(ret_type, run)


    def visitParen_expr(self, ctx:DMFParser.Paren_exprContext) -> Executable:
        return self.visit(ctx.expr())


    def visitNeg_expr(self, ctx:DMFParser.Neg_exprContext):
        return DMFVisitor.visitNeg_expr(self, ctx)


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
        if not well.return_type <= Type.WELL:
            self.error(ctx.who, Type.WELL_PAD, f"Not a well ({well.return_type.name}): {self.text_of(ctx.who)}")
        if not which.return_type <= Type.INT:
            self.error(ctx.which, Type.WELL_PAD, f"Not an integer ({which.return_type.name}): {self.text_of(ctx.which)}")
        def run(env: Environment) -> Delayed[WellPad]:
            f: Delayed[Well] = well.evaluate(env, Type.WELL)
            return f.chain(lambda w: (which.evaluate(env, Type.INT)
                                            .transformed(lambda n: w.group.shared_pads[cast(int, n)]))
                )
        return Executable(Type.WELL_PAD, run)
    


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
            return Executable(Type.INT, run_int)
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
            return Executable(Type.PAD, run_delta)
        if addp:
            return self.error(ctx, Type.NONE,
                              f"Can't add {lhs.return_type.name} and {rhs.return_type.name}: {self.text_of(ctx)}")
        else:
            return self.error(ctx, Type.NONE,
                              f"Can't subtract {rhs.return_type.name} from {lhs.return_type.name}: {self.text_of(ctx)}")
            


    def visitDelta_expr(self, ctx:DMFParser.Delta_exprContext) -> Executable:
        dist = self.visit(ctx.dist)
        direction: Dir = ctx.direction().d
        if not dist.return_type <= Type.INT:
            return self.error(ctx.dist, Type.INT, f"Not an integer: {self.text_of(ctx.dist)}")
        def run(env: Environment) -> Delayed[DeltaValue]:
            return (dist.evaluate(env, Type.INT)
                    .transformed(lambda n: DeltaValue(n, direction))
                    )
        return Executable(Type.DELTA, run)


    def visitCoord_expr(self, ctx:DMFParser.Coord_exprContext) -> Executable:
        x = self.visit(ctx.x)
        y = self.visit(ctx.y)
        if not x.return_type <= Type.INT:
            return self.error(ctx.x, Type.PAD, f"x coordinate not an integer: {self.text_of(ctx.x)}")
        if not y.return_type <= Type.INT:
            return self.error(ctx.y, Type.PAD, f"y coordinate not an integer: {self.text_of(ctx.x)}")
        def run(env: Environment) -> Delayed[Pad]:
            return (x.evaluate(env, Type.INT)
                    .chain(lambda xc: (y.evaluate(env, Type.INT)
                                       .transformed(lambda yc: env.board.pad_at(xc, yc))))
                    )
        return Executable(Type.PAD, run)



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
        if not who.return_type <= first_arg_type:
            return self.error(ctx.who, Type.NONE, 
                              f"Injected value ({who.return_type.name}) '{self.text_of(ctx.who)}' not compatible with "
                              +f"{first_arg_type.name}: {self.text_of(ctx.what)}")
        
        return_first_arg = inj_type.return_type is Type.NONE
        
        def run(env: Environment) -> Delayed[Any]:
            def inject(obj, func) -> Delayed[Any]:
                assert isinstance(func, CallableValue)
                future = func.apply(env, (obj,))
                return future if not return_first_arg else future.transformed(lambda _: obj)
            return (who.evaluate(env, first_arg_type)
                    .chain(lambda obj: (what.evaluate(env)
                                        .chain(lambda func: inject(obj, func)))))
        # print(f"Injection returns {inj_type.return_type}: {self.text_of(ctx)}")
        return Executable(first_arg_type if return_first_arg else inj_type.return_type, run)
            
        


    def visitGate_expr(self, ctx:DMFParser.Gate_exprContext) -> Executable:
        well = self.visit(ctx.well)
        if not well.return_type <= Type.WELL:
            self.error(ctx.well, Type.WELL_PAD, f"Not a well: {self.text_of(ctx.well)}")
        def run(env: Environment) -> Delayed[WellPad]:
            f: Delayed[Well] = well.evaluate(env, Type.WELL)
            return f.transformed(lambda w: w.gate)
        return Executable(Type.WELL_PAD, run)
    
    def visitExit_pad_expr(self, ctx:DMFParser.Exit_pad_exprContext) -> Executable:
        well = self.visit(ctx.well)
        if not well.return_type <= Type.WELL:
            self.error(ctx.well, Type.WELL_PAD, f"Not a well: {self.text_of(ctx.well)}")
        def run(env: Environment) -> Delayed[Pad]:
            f: Delayed[Well] = well.evaluate(env, Type.WELL)
            return f.transformed(lambda w: w.exit_pad)
        return Executable(Type.PAD, run)


    def visitWell_expr(self, ctx:DMFParser.Well_exprContext) -> Executable:
        which = self.visit(ctx.which)
        if not which.return_type <= Type.INT:
            self.error(ctx.which, Type.WELL, f"Not an integer: {self.text_of(ctx.which)}")
        def run(env: Environment) -> Delayed[Well]:
            f: Delayed[int] = which.evaluate(env, Type.INT)
            return f.transformed(lambda n: env.board.wells[n])
        return Executable(Type.WELL, run)



    def visitDrop_expr(self, ctx:DMFParser.Drop_exprContext) -> Executable:
        loc_exec = self.visit(ctx.loc)
        if not loc_exec.return_type <= Type.PAD:
            self.error(ctx.loc, Type.DROP, 
                       f"Not a pad: {self.text_of(ctx.loc)}")
        def run(env: Environment) -> Delayed[Drop]:
            def get_drop(pad: Pad) -> Drop:
                drop = pad.drop
                if drop is None:
                    liquid = Liquid(unknown_reagent, env.board.drop_size)
                    drop = Drop(pad, liquid)
                return drop
            return loc_exec.evaluate(env, Type.PAD).transformed(get_drop)
        return Executable(Type.DROP, run)


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
            future = future.chain(lambda _: cast(Delayed[Any], func.apply(env, args)))
            return future
        
        return Executable(ret_type, run)


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
        return Executable(Type.MOTION, run)


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
            return Executable(Type.INT, run_int)
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
        param_type: Type = cast(Type, ctx.type)
        name_ctx: Optional[str] = ctx.name()
        if name_ctx is None:
            name = self.type_name_var(ctx.param_type(), ctx.n)
        else:
            name = self.text_of(name_ctx)
        return (name, param_type)

    def visitMacro_def(self, ctx:DMFParser.Macro_defContext) -> Executable:
        header: DMFParser.Macro_defContext = ctx.macro_header()
        param_contexts: Sequence[DMFParser.ParamContext] = header.param()
        
        param_defs = tuple(self.param_def(pc) for pc in param_contexts)
        param_names = tuple(pdef[0] for pdef in param_defs)
        param_types = tuple(pdef[1] for pdef in param_defs)
        
        with self.current_types.push(dict(param_defs)): 
            body: Executable
            if ctx.compound() is not None:
                body = self.visit(ctx.compound())
            else:
                body = self.visit(ctx.expr())
            macro_type = MacroType(param_types, body.return_type)
        
        macro = MacroValue(macro_type, param_names, body)
            
        def run(env: Environment) -> Delayed[MacroValue]:
            return Delayed.complete(macro)
        return Executable(macro_type, run)
        


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

