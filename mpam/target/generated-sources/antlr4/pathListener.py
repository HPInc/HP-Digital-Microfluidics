# Generated from path.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pathParser import pathParser
else:
    from pathParser import pathParser

from mpam.types import Dir 


# This class defines a complete listener for a parse tree produced by pathParser.
class pathListener(ParseTreeListener):

    # Enter a parse tree produced by pathParser#paren_expr.
    def enterParen_expr(self, ctx:pathParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by pathParser#paren_expr.
    def exitParen_expr(self, ctx:pathParser.Paren_exprContext):
        pass


    # Enter a parse tree produced by pathParser#int_expr.
    def enterInt_expr(self, ctx:pathParser.Int_exprContext):
        pass

    # Exit a parse tree produced by pathParser#int_expr.
    def exitInt_expr(self, ctx:pathParser.Int_exprContext):
        pass


    # Enter a parse tree produced by pathParser#coord_expr.
    def enterCoord_expr(self, ctx:pathParser.Coord_exprContext):
        pass

    # Exit a parse tree produced by pathParser#coord_expr.
    def exitCoord_expr(self, ctx:pathParser.Coord_exprContext):
        pass


    # Enter a parse tree produced by pathParser#horiz_dist.
    def enterHoriz_dist(self, ctx:pathParser.Horiz_distContext):
        pass

    # Exit a parse tree produced by pathParser#horiz_dist.
    def exitHoriz_dist(self, ctx:pathParser.Horiz_distContext):
        pass


    # Enter a parse tree produced by pathParser#injection_expr.
    def enterInjection_expr(self, ctx:pathParser.Injection_exprContext):
        pass

    # Exit a parse tree produced by pathParser#injection_expr.
    def exitInjection_expr(self, ctx:pathParser.Injection_exprContext):
        pass


    # Enter a parse tree produced by pathParser#drop_expr.
    def enterDrop_expr(self, ctx:pathParser.Drop_exprContext):
        pass

    # Exit a parse tree produced by pathParser#drop_expr.
    def exitDrop_expr(self, ctx:pathParser.Drop_exprContext):
        pass


    # Enter a parse tree produced by pathParser#function_expr.
    def enterFunction_expr(self, ctx:pathParser.Function_exprContext):
        pass

    # Exit a parse tree produced by pathParser#function_expr.
    def exitFunction_expr(self, ctx:pathParser.Function_exprContext):
        pass


    # Enter a parse tree produced by pathParser#name_expr.
    def enterName_expr(self, ctx:pathParser.Name_exprContext):
        pass

    # Exit a parse tree produced by pathParser#name_expr.
    def exitName_expr(self, ctx:pathParser.Name_exprContext):
        pass


    # Enter a parse tree produced by pathParser#addsub_expr.
    def enterAddsub_expr(self, ctx:pathParser.Addsub_exprContext):
        pass

    # Exit a parse tree produced by pathParser#addsub_expr.
    def exitAddsub_expr(self, ctx:pathParser.Addsub_exprContext):
        pass


    # Enter a parse tree produced by pathParser#muldiv_expr.
    def enterMuldiv_expr(self, ctx:pathParser.Muldiv_exprContext):
        pass

    # Exit a parse tree produced by pathParser#muldiv_expr.
    def exitMuldiv_expr(self, ctx:pathParser.Muldiv_exprContext):
        pass


    # Enter a parse tree produced by pathParser#attr_expr.
    def enterAttr_expr(self, ctx:pathParser.Attr_exprContext):
        pass

    # Exit a parse tree produced by pathParser#attr_expr.
    def exitAttr_expr(self, ctx:pathParser.Attr_exprContext):
        pass


    # Enter a parse tree produced by pathParser#horiz_unit.
    def enterHoriz_unit(self, ctx:pathParser.Horiz_unitContext):
        pass

    # Exit a parse tree produced by pathParser#horiz_unit.
    def exitHoriz_unit(self, ctx:pathParser.Horiz_unitContext):
        pass


    # Enter a parse tree produced by pathParser#vert_unit.
    def enterVert_unit(self, ctx:pathParser.Vert_unitContext):
        pass

    # Exit a parse tree produced by pathParser#vert_unit.
    def exitVert_unit(self, ctx:pathParser.Vert_unitContext):
        pass


    # Enter a parse tree produced by pathParser#undirected_unit.
    def enterUndirected_unit(self, ctx:pathParser.Undirected_unitContext):
        pass

    # Exit a parse tree produced by pathParser#undirected_unit.
    def exitUndirected_unit(self, ctx:pathParser.Undirected_unitContext):
        pass


    # Enter a parse tree produced by pathParser#horiz_dir.
    def enterHoriz_dir(self, ctx:pathParser.Horiz_dirContext):
        pass

    # Exit a parse tree produced by pathParser#horiz_dir.
    def exitHoriz_dir(self, ctx:pathParser.Horiz_dirContext):
        pass


    # Enter a parse tree produced by pathParser#vertical_dir.
    def enterVertical_dir(self, ctx:pathParser.Vertical_dirContext):
        pass

    # Exit a parse tree produced by pathParser#vertical_dir.
    def exitVertical_dir(self, ctx:pathParser.Vertical_dirContext):
        pass


    # Enter a parse tree produced by pathParser#name.
    def enterName(self, ctx:pathParser.NameContext):
        pass

    # Exit a parse tree produced by pathParser#name.
    def exitName(self, ctx:pathParser.NameContext):
        pass


    # Enter a parse tree produced by pathParser#kwd_names.
    def enterKwd_names(self, ctx:pathParser.Kwd_namesContext):
        pass

    # Exit a parse tree produced by pathParser#kwd_names.
    def exitKwd_names(self, ctx:pathParser.Kwd_namesContext):
        pass



del pathParser