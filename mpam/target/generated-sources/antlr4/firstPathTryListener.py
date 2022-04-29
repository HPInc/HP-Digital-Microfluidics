# Generated from firstPathTry.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .firstPathTryParser import firstPathTryParser
else:
    from firstPathTryParser import firstPathTryParser

from mpam.types import Dir 


# This class defines a complete listener for a parse tree produced by firstPathTryParser.
class firstPathTryListener(ParseTreeListener):

    # Enter a parse tree produced by firstPathTryParser#paren_expr.
    def enterParen_expr(self, ctx:firstPathTryParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#paren_expr.
    def exitParen_expr(self, ctx:firstPathTryParser.Paren_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#int_expr.
    def enterInt_expr(self, ctx:firstPathTryParser.Int_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#int_expr.
    def exitInt_expr(self, ctx:firstPathTryParser.Int_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#coord_expr.
    def enterCoord_expr(self, ctx:firstPathTryParser.Coord_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#coord_expr.
    def exitCoord_expr(self, ctx:firstPathTryParser.Coord_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#horiz_dist.
    def enterHoriz_dist(self, ctx:firstPathTryParser.Horiz_distContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#horiz_dist.
    def exitHoriz_dist(self, ctx:firstPathTryParser.Horiz_distContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#injection_expr.
    def enterInjection_expr(self, ctx:firstPathTryParser.Injection_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#injection_expr.
    def exitInjection_expr(self, ctx:firstPathTryParser.Injection_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#drop_expr.
    def enterDrop_expr(self, ctx:firstPathTryParser.Drop_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#drop_expr.
    def exitDrop_expr(self, ctx:firstPathTryParser.Drop_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#function_expr.
    def enterFunction_expr(self, ctx:firstPathTryParser.Function_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#function_expr.
    def exitFunction_expr(self, ctx:firstPathTryParser.Function_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#name_expr.
    def enterName_expr(self, ctx:firstPathTryParser.Name_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#name_expr.
    def exitName_expr(self, ctx:firstPathTryParser.Name_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#addsub_expr.
    def enterAddsub_expr(self, ctx:firstPathTryParser.Addsub_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#addsub_expr.
    def exitAddsub_expr(self, ctx:firstPathTryParser.Addsub_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#muldiv_expr.
    def enterMuldiv_expr(self, ctx:firstPathTryParser.Muldiv_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#muldiv_expr.
    def exitMuldiv_expr(self, ctx:firstPathTryParser.Muldiv_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#attr_expr.
    def enterAttr_expr(self, ctx:firstPathTryParser.Attr_exprContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#attr_expr.
    def exitAttr_expr(self, ctx:firstPathTryParser.Attr_exprContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#horiz_unit.
    def enterHoriz_unit(self, ctx:firstPathTryParser.Horiz_unitContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#horiz_unit.
    def exitHoriz_unit(self, ctx:firstPathTryParser.Horiz_unitContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#vert_unit.
    def enterVert_unit(self, ctx:firstPathTryParser.Vert_unitContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#vert_unit.
    def exitVert_unit(self, ctx:firstPathTryParser.Vert_unitContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#undirected_unit.
    def enterUndirected_unit(self, ctx:firstPathTryParser.Undirected_unitContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#undirected_unit.
    def exitUndirected_unit(self, ctx:firstPathTryParser.Undirected_unitContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#horiz_dir.
    def enterHoriz_dir(self, ctx:firstPathTryParser.Horiz_dirContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#horiz_dir.
    def exitHoriz_dir(self, ctx:firstPathTryParser.Horiz_dirContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#vertical_dir.
    def enterVertical_dir(self, ctx:firstPathTryParser.Vertical_dirContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#vertical_dir.
    def exitVertical_dir(self, ctx:firstPathTryParser.Vertical_dirContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#name.
    def enterName(self, ctx:firstPathTryParser.NameContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#name.
    def exitName(self, ctx:firstPathTryParser.NameContext):
        pass


    # Enter a parse tree produced by firstPathTryParser#kwd_names.
    def enterKwd_names(self, ctx:firstPathTryParser.Kwd_namesContext):
        pass

    # Exit a parse tree produced by firstPathTryParser#kwd_names.
    def exitKwd_names(self, ctx:firstPathTryParser.Kwd_namesContext):
        pass



del firstPathTryParser