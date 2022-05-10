# Generated from firstPathTry.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .firstPathTryParser import firstPathTryParser
else:
    from firstPathTryParser import firstPathTryParser

from mpam.types import Dir 


# This class defines a complete generic visitor for a parse tree produced by firstPathTryParser.

class firstPathTryVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by firstPathTryParser#paren_expr.
    def visitParen_expr(self, ctx:firstPathTryParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#int_expr.
    def visitInt_expr(self, ctx:firstPathTryParser.Int_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#coord_expr.
    def visitCoord_expr(self, ctx:firstPathTryParser.Coord_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#horiz_dist.
    def visitHoriz_dist(self, ctx:firstPathTryParser.Horiz_distContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#injection_expr.
    def visitInjection_expr(self, ctx:firstPathTryParser.Injection_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#drop_expr.
    def visitDrop_expr(self, ctx:firstPathTryParser.Drop_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#function_expr.
    def visitFunction_expr(self, ctx:firstPathTryParser.Function_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#name_expr.
    def visitName_expr(self, ctx:firstPathTryParser.Name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#addsub_expr.
    def visitAddsub_expr(self, ctx:firstPathTryParser.Addsub_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#muldiv_expr.
    def visitMuldiv_expr(self, ctx:firstPathTryParser.Muldiv_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#attr_expr.
    def visitAttr_expr(self, ctx:firstPathTryParser.Attr_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#horiz_unit.
    def visitHoriz_unit(self, ctx:firstPathTryParser.Horiz_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#vert_unit.
    def visitVert_unit(self, ctx:firstPathTryParser.Vert_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#undirected_unit.
    def visitUndirected_unit(self, ctx:firstPathTryParser.Undirected_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#horiz_dir.
    def visitHoriz_dir(self, ctx:firstPathTryParser.Horiz_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#vertical_dir.
    def visitVertical_dir(self, ctx:firstPathTryParser.Vertical_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#name.
    def visitName(self, ctx:firstPathTryParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by firstPathTryParser#kwd_names.
    def visitKwd_names(self, ctx:firstPathTryParser.Kwd_namesContext):
        return self.visitChildren(ctx)



del firstPathTryParser