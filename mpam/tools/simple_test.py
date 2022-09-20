from __future__ import annotations

import re
import sys
from typing import Sequence, Final, Optional, cast, Union, Any

from antlr4 import FileStream, CommonTokenStream, ParserRuleContext, InputStream

from antlr4.tree.Tree import ParseTreeWalker, TerminalNode

from langsup.type_supp import Type
from simpleLexer import simpleLexer
from simpleListener import simpleListener
from simpleParser import simpleParser


class Scope:
    parent: Final[Optional[Scope]]
    names: Final[dict[str, ParserRuleContext]]
    
    def __init__(self, parent: Optional[Scope]) -> None:
        self.parent = parent
        self.names = {}
        
    def find_defining_scope(self, name: str) -> Optional[Scope]:
        if name in self.names:
            return self
        parent = self.parent
        return None if parent is None else parent.find_defining_scope(name)
        
    def lookup(self, name: str) -> Optional[ParserRuleContext]:
        scope = self.find_defining_scope(name)
        return None if scope is None else scope.names[name]
    
    def define(self, name: str, val_ctx: ParserRuleContext) -> None:
        self.names[name] = val_ctx
    
    def __getitem__(self, name: str) -> ParserRuleContext:
        ctx = self.lookup(name)
        # TODO: Better error reporting
        assert ctx is not None, f"'{name}' is undefined"
        return ctx
    
    def __setitem__(self, name: str, val_ctx: ParserRuleContext) -> None:
        scope = self.find_defining_scope(name)
        if scope is not None:
            scope.names[name] = val_ctx
        else:
            self.define(name, val_ctx)

class TypeAnnotator(simpleListener):
    input_stream: Final[InputStream]
    types: dict[ParserRuleContext, Type]
    global_scope: Final[Scope]
    current_scope: Scope
    _lines: Optional[Sequence[str]] = None
    
    @property
    def lines(self) -> Sequence[str]:
        val = self._lines
        if val is None:
            text = str(self.input_stream)
            val = re.split("\\s*\\r?\\n\\s*", text)
            self._lines = val
        return val
    
    # def input_text(self, ctx: ParserRuleContext) -> str:
        # lines = self.lines
        
        
    
    def __init__(self, input_stream: InputStream) -> None:
        self.input_stream = input_stream
        self.types = {}
        self.global_scope = Scope(None)
        self.current_scope = self.global_scope
        
    def type_of(self, ctx: ParserRuleContext, restr: Optional[Union[Type, Sequence[Type]]] = None) -> Type:
        t = self.types[ctx]
        if restr is not None:
            if isinstance(restr, Type):
                restr = (restr,)
            matches = tuple(t <= r for r in restr)
            assert any(matches), f"Not a {tuple(r.name for r in restr)}: [{t.name}] {self.text_of(ctx)}"
        return t
    
    def note_type(self, ctx: ParserRuleContext, ctx_type: Type) -> None:
        self.types[ctx] = ctx_type

    def exitNeg_expr(self, ctx:simpleParser.Neg_exprContext) -> Any:
        return simpleListener.exitNeg_expr(self, ctx)
    
    def lookup_name(self, name: str) -> ParserRuleContext:
        return self.current_scope.lookup(name)
    
    def define(self, name: str, val: ParserRuleContext) -> None:
        self.current_scope[name] = val
        
    def text_of(self, ctx_or_token: Union[ParserRuleContext, TerminalNode]) -> str:
        if isinstance(ctx_or_token, TerminalNode):
            t: str = ctx_or_token.getText()
            return t
        return " ".join(self.text_of(child) for child in ctx_or_token.getChildren())


    def exitInt_expr(self, ctx:simpleParser.Int_exprContext) -> None:
        self.note_type(ctx, Type.INT)

    def exitType_name_expr(self, ctx:simpleParser.Type_name_exprContext) -> None:
        pass


    def exitIndex_expr(self, ctx:simpleParser.Index_exprContext) -> Any:
        return simpleListener.exitIndex_expr(self, ctx)
    
    def exitInjection_expr(self, ctx:simpleParser.Injection_exprContext) -> None:
        # what_t = self.type_of(ctx.what, Type.CALLABLE)
        ...
        
    def exitMacro_expr(self, ctx:simpleParser.Macro_exprContext) -> Any:
        return simpleListener.exitMacro_expr(self, ctx)


    def exitName_expr(self, ctx:simpleParser.Name_exprContext) -> None:
        name: str = ctx.getText()
        t = self.type_of(self.lookup_name(name))
        self.note_type(ctx, t)


    def exitAddsub_expr(self, ctx:simpleParser.Addsub_exprContext) -> None:
        lhs_t = self.type_of(ctx.lhs, (Type.INT, Type.PAD))
        if lhs_t <= Type.INT:
            rhs_t = self.type_of(ctx.rhs, Type.INT) # @UnusedVariable
            self.note_type(ctx, Type.INT)
        else:
            rhs_t = self.type_of(ctx.rhs, Type.DELTA) # @UnusedVariable
            self.note_type(ctx, Type.PAD)


    def exitDelta_expr(self, ctx:simpleParser.Delta_exprContext) -> None:
        dist_t = self.type_of(ctx.dist, Type.INT) # @UnusedVariable
        dir_t = self.type_of(ctx.direction(), Type.DIR) # @UnusedVariable
        self.note_type(ctx, Type.DELTA)


    def exitCoord_expr(self, ctx:simpleParser.Coord_exprContext) -> None:
        xt = self.type_of(ctx.x, Type.INT) # @UnusedVariable
        yt = self.type_of(ctx.y, Type.INT) # @UnusedVariable
        self.note_type(ctx, Type.PAD)


    def exitGate_expr(self, ctx:simpleParser.Gate_exprContext) -> Any:
        return simpleListener.exitGate_expr(self, ctx)


    def exitWell_expr(self, ctx:simpleParser.Well_exprContext) -> Any:
        return simpleListener.exitWell_expr(self, ctx)


    def exitDrop_expr(self, ctx:simpleParser.Drop_exprContext) -> None:
        dt = self.type_of(ctx.loc, Type.PAD) # @UnusedVariable
        self.note_type(ctx, Type.DROP)


    def exitFunction_expr(self, ctx:simpleParser.Function_exprContext) -> Any:
        return simpleListener.exitFunction_expr(self, ctx)


    def exitTo_expr(self, ctx:simpleParser.To_exprContext) -> Any:
        return simpleListener.exitTo_expr(self, ctx)


    def exitMuldiv_expr(self, ctx:simpleParser.Muldiv_exprContext) -> Any:
        return simpleListener.exitMuldiv_expr(self, ctx)

        
    def trace(self, ctx: ParserRuleContext) -> None:
        assert ctx in self.types, f"No type extablished for '{self.text_of(ctx)}' [{type(ctx).__name__}]"
        t = self.types[ctx]
        print(f"{t.name}: {self.text_of(ctx)}")
    
    def exitParen_expr(self, ctx:simpleParser.Paren_exprContext) -> None:
        self.types[ctx] = self.types[ctx.expr()]
        
    def exitEveryRule(self, ctx:ParserRuleContext) -> None:
        if isinstance(ctx, simpleParser.ExprContext):
            self.trace(ctx)
            
    def exitAssign_stat(self, ctx:simpleParser.Assign_statContext) -> None:
        name = cast(simpleParser.NameContext, ctx.which).getText()
        val = cast(simpleParser.ExprContext, ctx.what)
        val_type = self.type_of(val)
        print(f"Assignment: {name} = {val_type}: {self.text_of(val)}")
        self.define(name, val)
        
    def exitDirection(self, ctx:simpleParser.DirectionContext) -> None:
        self.note_type(ctx, Type.DIR)
        


def main(argv: Sequence[str]) -> None:
    input_stream = FileStream(argv[1])
    lexer = simpleLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = simpleParser(stream)
    parse_tree = parser.macro_file()
    type_annotator = TypeAnnotator(input_stream)
    walker = ParseTreeWalker()
    walker.walk(type_annotator, parse_tree)
    # tree_rep = parse_tree.toStringTree(recog=parser)
    # print(tree_rep)
    
    
    
if __name__ == '__main__':
    main(sys.argv)