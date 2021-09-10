from __future__ import annotations

from _collections import defaultdict
from typing import Optional, TypeVar, Generic, Hashable, NamedTuple, Final, \
    Callable, Any, cast, Sequence, Union, Mapping, ClassVar

from antlr4 import InputStream, CommonTokenStream, FileStream, ParserRuleContext
from antlr4.tree.Tree import TerminalNode

from DMFLexer import DMFLexer
from DMFParser import DMFParser
from DMFVisitor import DMFVisitor
from langsup.type_supp import Type, CallableType
from mpam.device import Pad, Board
from mpam.drop import Drop
from mpam.types import unknown_reagent, Liquid, Dir
from abc import ABC, abstractmethod
import typing


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
            raise KeyError(f"'{name}' is undefined")
        return val
    
    def __setitem__(self, name: Name_, val: Val_) -> None:
        scope = self.find_scope(name)
        if scope is None:
            scope = self
        scope.mapping[name] = val
        
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
    def apply(self, env: Environment, args: Sequence[Any]) -> Any: ... # @UnusedVariable
    
class MotionValue(CallableValue):
    @abstractmethod
    def move(self, env: Environment, drop: Drop) -> None: ... # @UnusedVariable
    
    def apply(self, env:Environment, args:Sequence[Any])->Drop:
        assert len(args) == 1
        drop = args[0]
        assert isinstance(drop, Drop)
        self.move(env, drop)
        return drop
        
    
class DeltaValue(MotionValue):
    dist: Final[int]
    direction: Final[Dir]
    
    def __init__(self, dist: int, direction: Dir) -> None:
        self.dist = dist
        self.direction = direction
        
    def move(self, env:Environment, drop:Drop)->None:
        # TODO: Do the motion
        ...
    
class ToPadValue(MotionValue):
    dest: Final[Pad]
    
    def __init__(self, pad: Pad) -> None:
        self.dest = pad
        
    def move(self, env:Environment, drop:Drop)->None:
        # TODO: Do the motion
        ...

class ToRowColValue(MotionValue):
    dest: Final[int]
    verticalp: Final[bool]
    
    def __init__(self, dest: int, verticalp: bool) -> None:
        self.dest = dest
        self.verticalp = verticalp
        
    def move(self, env:Environment, drop:Drop)->None:
        # TODO: Do the motion
        ...

        
        
rep_types: Mapping[Type, typing.Type] = {
        Type.DROP: Drop,
        Type.INT: int,
        Type.PAD: Pad,
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
        converter = cls.known[(have, want)]
        return converter(val)
    
Conversions.register(Type.DROP, Type.PAD,
                     lambda drop: drop.pad)

class Executable(NamedTuple):
    return_type: Type
    func: Callable[[Environment], Any]
    
    def evaluate(self, env: Environment, required: Optional[Type] = None) -> Any:
        fn = self.func
        val = fn(env)
        if required is not None and required is not self.return_type:
            val = Conversions.convert(have=self.return_type, want=required, val=val)
        if required is not None: 
            check = rep_types.get(required, None)
            if check is not None:
                assert isinstance(val, check), f"Expected {check}, got {val}"
        return val
    
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
        executable.evaluate(self.globals)
        
    def evaluate(self, expr: str, required: Optional[Type] = None) -> Any:
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
    current_types: TypeMap
    
    default_creators = defaultdict[Type,Callable[[Environment],Any]](lambda: (lambda _: None),
                                                          {Type.INT: lambda _: 0,
                                                           Type.PAD: lambda env: env.board.pad_at(0,0) 
                                                          })
    
    def __init__(self, *,
                 global_types: Optional[TypeMap] = None) -> None:
        self.global_types = global_types if global_types is not None else TypeMap(None)
        self.current_types = self.global_types
        
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

        
        
    def visit(self, tree) -> Executable:
        return cast(Executable, DMFVisitor.visit(self, tree))

    def visitMacro_file(self, ctx:DMFParser.Macro_fileContext) -> Executable:
        stats: Sequence[Executable] = [self.visit(tls) for tls in ctx.top_level_stat()] 
        def run(env: Environment) -> None:
            for stat in stats:
                stat.evaluate(env)
        return Executable(Type.NONE, run)


    def visitCompound_interactive(self, ctx:DMFParser.Compound_interactiveContext):
        return DMFVisitor.visitCompound_interactive(self, ctx)


    def visitAssignment_interactive(self, ctx:DMFParser.Assignment_interactiveContext):
        return DMFVisitor.visitAssignment_interactive(self, ctx)


    def visitExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext):
        return DMFVisitor.visitExpr_interactive(self, ctx)


    def visitTop_level_stat(self, ctx:DMFParser.Top_level_statContext) -> Executable:
        return self.visit(ctx.assignment())


    def visitAssignment(self, ctx:DMFParser.AssignmentContext) -> Executable:
        name_ctx = cast(DMFParser.NameContext, ctx.which)
        name = self.text_of(name_ctx)
        value = self.visit(ctx.what)
        required_type = self.current_types.lookup(name)
        if required_type is not None and not required_type <= value.return_type:
            return self.error(ctx, required_type,
                              f"variable '{name}' has type {required_type.name}.  Expr has type {value.return_type.name}")
        returned_type = required_type if required_type is not None else value.return_type
        if required_type is None:
            self.current_types[name] = returned_type
        def run(env: Environment):
            val = value.evaluate(env, required_type)
            env[name] = val
            print(f"Assigned {name} := {val}")
            return val
        return Executable(returned_type, run)


    def visitAssign_stat(self, ctx:DMFParser.Assign_statContext) -> Executable:
        return self.visit(ctx.assignment())


    def visitMacro_def_stat(self, ctx:DMFParser.Macro_def_statContext):
        return DMFVisitor.visitMacro_def_stat(self, ctx)


    def visitExpr_stat(self, ctx:DMFParser.Expr_statContext):
        return DMFVisitor.visitExpr_stat(self, ctx)


    def visitCompound_stat(self, ctx:DMFParser.Compound_statContext):
        return DMFVisitor.visitCompound_stat(self, ctx)


    def visitBlock(self, ctx:DMFParser.BlockContext):
        return DMFVisitor.visitBlock(self, ctx)


    def visitPar_block(self, ctx:DMFParser.Par_blockContext):
        return DMFVisitor.visitPar_block(self, ctx)


    def visitParen_expr(self, ctx:DMFParser.Paren_exprContext):
        return DMFVisitor.visitParen_expr(self, ctx)


    def visitNeg_expr(self, ctx:DMFParser.Neg_exprContext):
        return DMFVisitor.visitNeg_expr(self, ctx)


    def visitInt_expr(self, ctx:DMFParser.Int_exprContext):
        val: int = int(ctx.INT().getText())
        return Executable(Type.INT, lambda _: val)


    def visitType_name_expr(self, ctx:DMFParser.Type_name_exprContext):
        return DMFVisitor.visitType_name_expr(self, ctx)


    def visitIndex_expr(self, ctx:DMFParser.Index_exprContext):
        return DMFVisitor.visitIndex_expr(self, ctx)


    def visitMacro_expr(self, ctx:DMFParser.Macro_exprContext):
        return DMFVisitor.visitMacro_expr(self, ctx)


    def visitName_expr(self, ctx:DMFParser.Name_exprContext) -> Executable:
        name = self.text_of(ctx.name())
        var_type = self.current_types.lookup(name)
        if var_type is None:
            return self.error(ctx.name(), Type.NONE, f"Undefined variable: {name}")
        def run(env: Environment) -> Any:
            return env[name]
        return Executable(var_type, run)


    def visitAddsub_expr(self, ctx:DMFParser.Addsub_exprContext) -> Executable:
        lhs = self.visit(ctx.lhs)
        rhs = self.visit(ctx.rhs)
        addp = ctx.ADD() is not None
        if lhs.return_type <= Type.INT and rhs.return_type <= Type.INT:
            def run_int(env: Environment) -> int:
                x: int = lhs.evaluate(env, Type.INT)
                y: int = rhs.evaluate(env, Type.INT)
                return x+y if addp else x-y
            return Executable(Type.INT, run_int)
        elif lhs.return_type <= Type.PAD and rhs.return_type <= Type.DELTA:
            def run_delta(env: Environment) -> Pad:
                p: Pad = lhs.evaluate(env, Type.PAD)
                d: DeltaValue = rhs.evaluate(env, Type.DELTA)
                n = d.dist if addp else -d.dist
                board = env.board
                loc = board.orientation.neighbor(d.direction, p.location, steps=n)
                return board.pads[loc]
            return Executable(Type.PAD, run_delta)
        if addp:
            return self.error(ctx, Type.NONE,
                              f"Can't add {lhs.return_type.name} and {rhs.return_type.name}: {self.text_of(ctx)}")
        else:
            return self.error(ctx, Type.NONE,
                              f"Can't add {lhs.return_type.name} and {rhs.return_type.name}: {self.text_of(ctx)}")
            


    def visitDelta_expr(self, ctx:DMFParser.Delta_exprContext) -> Executable:
        dist = self.visit(ctx.dist)
        direction: Dir = ctx.direction().d
        if not dist.return_type <= Type.INT:
            return self.error(ctx.dist, Type.INT, f"Not an integer: {self.text_of(ctx.dist)}")
        def run(env: Environment) -> DeltaValue:
            n: int = dist.evaluate(env, Type.INT)
            return DeltaValue(n, direction)
        return Executable(Type.DELTA, run)


    def visitCoord_expr(self, ctx:DMFParser.Coord_exprContext) -> Executable:
        x = self.visit(ctx.x)
        y = self.visit(ctx.y)
        if not x.return_type <= Type.INT:
            return self.error(ctx.x, Type.PAD, f"x coordinate not an integer: {self.text_of(ctx.x)}")
        if not y.return_type <= Type.INT:
            return self.error(ctx.y, Type.PAD, f"y coordinate not an integer: {self.text_of(ctx.x)}")
        def run(env: Environment) -> Pad:
            xc: int = x.evaluate(env, Type.INT)
            yc: int = y.evaluate(env, Type.INT)
            return env.board.pad_at(xc, yc)
        return Executable(Type.PAD, run)



    def visitInjection_expr(self, ctx:DMFParser.Injection_exprContext) -> Executable:
        who = self.visit(ctx.who)
        what = self.visit(ctx.what)
        inj_type = what.return_type
        if not isinstance(inj_type, CallableType) or len(inj_type.param_types) == 0:
            return self.error(ctx.what, Type.NONE, 
                              f"Not an injection target ({what.return_type.name}): {self.text_of(ctx.what)}")
        first_arg_type = inj_type.param_types[0]
        if not who.return_type <= first_arg_type:
            return self.error(ctx.who, Type.NONE, 
                              f"Injected value ({who.return_type.name}) '{self.text_of(ctx.who)}' not compatible with "
                              +f"{first_arg_type.name}: {self.text_of(ctx.what)}")
        def run(env: Environment) -> Any:
            func = what.evaluate(env)
            obj = who.evaluate(env, first_arg_type)
            assert isinstance(func, CallableValue)
            res = func.apply(env, (obj,))
            return res
        return Executable(inj_type.return_type, run)
            
        


    def visitGate_expr(self, ctx:DMFParser.Gate_exprContext):
        return DMFVisitor.visitGate_expr(self, ctx)


    def visitWell_expr(self, ctx:DMFParser.Well_exprContext):
        return DMFVisitor.visitWell_expr(self, ctx)


    def visitDrop_expr(self, ctx:DMFParser.Drop_exprContext) -> Executable:
        loc_exec = self.visit(ctx.loc)
        if not loc_exec.return_type <= Type.PAD:
            self.error(ctx.loc, Type.DROP, 
                       f"Not a pad: {self.text_of(ctx.loc)}")
        def run(env: Environment) -> Drop:
            pad: Pad = loc_exec.evaluate(env, Type.PAD)
            drop = pad.drop
            if drop is None:
                liquid = Liquid(unknown_reagent, env.board.drop_size)
                drop = Drop(pad, liquid)
            return drop
        return Executable(Type.DROP, run)


    def visitFunction_expr(self, ctx:DMFParser.Function_exprContext):
        return DMFVisitor.visitFunction_expr(self, ctx)


    def visitTo_expr(self, ctx:DMFParser.To_exprContext) -> Executable:
        axis: Optional[DMFParser.AxisContext] = ctx.axis()
        which = self.visit(ctx.which)
        if axis is None:
            # This is a to-pad motion
            if not which.return_type <= Type.PAD:
                if which.return_type <= Type.INT:
                    return self.error(ctx, Type.MOTION, f"Did you forget 'row' or 'column'?: {self.text_of(ctx)}")
                return self.error(ctx, Type.MOTION, f"'to' expr without 'row' or 'column' takes a PAD: {self.text_of(ctx)}")
            def run(env: Environment) -> MotionValue:
                pad: Pad = which.evaluate(env, Type.PAD)
                return ToPadValue(pad)
        else:
            if not which.return_type <= Type.INT:
                return self.error(ctx.which, Type.MOTION, 
                                  f"Row or column name not an int ({which.return_type.name}): {self.text_of(ctx.which)}")
            verticalp = cast(bool, axis.verticalp)
            def run(env: Environment) -> MotionValue:
                n: int = which.evaluate(env, Type.INT)
                return ToRowColValue(n, verticalp)
        return Executable(Type.MOTION, run)


    def visitMuldiv_expr(self, ctx:DMFParser.Muldiv_exprContext):
        return DMFVisitor.visitMuldiv_expr(self, ctx)


    def visitDirection(self, ctx:DMFParser.DirectionContext):
        return DMFVisitor.visitDirection(self, ctx)


    def visitAxis(self, ctx:DMFParser.AxisContext):
        return DMFVisitor.visitAxis(self, ctx)


    def visitMacro_def(self, ctx:DMFParser.Macro_defContext):
        return DMFVisitor.visitMacro_def(self, ctx)


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

