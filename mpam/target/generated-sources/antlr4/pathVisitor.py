# Generated from path.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pathParser import pathParser
else:
    from pathParser import pathParser

from mpam.types import Dir 


# This class defines a complete generic visitor for a parse tree produced by pathParser.

class pathVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by pathParser#paren_expr.
    def visitParen_expr(self, ctx:pathParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#int_expr.
    def visitInt_expr(self, ctx:pathParser.Int_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#coord_expr.
    def visitCoord_expr(self, ctx:pathParser.Coord_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#horiz_dist.
    def visitHoriz_dist(self, ctx:pathParser.Horiz_distContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#injection_expr.
    def visitInjection_expr(self, ctx:pathParser.Injection_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#drop_expr.
    def visitDrop_expr(self, ctx:pathParser.Drop_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#function_expr.
    def visitFunction_expr(self, ctx:pathParser.Function_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#name_expr.
    def visitName_expr(self, ctx:pathParser.Name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#addsub_expr.
    def visitAddsub_expr(self, ctx:pathParser.Addsub_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#muldiv_expr.
    def visitMuldiv_expr(self, ctx:pathParser.Muldiv_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#attr_expr.
    def visitAttr_expr(self, ctx:pathParser.Attr_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#horiz_unit.
    def visitHoriz_unit(self, ctx:pathParser.Horiz_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#vert_unit.
    def visitVert_unit(self, ctx:pathParser.Vert_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#undirected_unit.
    def visitUndirected_unit(self, ctx:pathParser.Undirected_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#horiz_dir.
    def visitHoriz_dir(self, ctx:pathParser.Horiz_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#vertical_dir.
    def visitVertical_dir(self, ctx:pathParser.Vertical_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#name.
    def visitName(self, ctx:pathParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pathParser#kwd_names.
    def visitKwd_names(self, ctx:pathParser.Kwd_namesContext):
        return self.visitChildren(ctx)



del pathParser