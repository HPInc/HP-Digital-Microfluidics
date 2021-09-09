# Generated from simple.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .simpleParser import simpleParser
else:
    from simpleParser import simpleParser

from mpam.types import Dir 
from langsup.type_supp import Type


from mpam.types import Dir 


# This class defines a complete listener for a parse tree produced by simpleParser.
class simpleListener(ParseTreeListener):

    # Enter a parse tree produced by simpleParser#macro_file.
    def enterMacro_file(self, ctx:simpleParser.Macro_fileContext):
        pass

    # Exit a parse tree produced by simpleParser#macro_file.
    def exitMacro_file(self, ctx:simpleParser.Macro_fileContext):
        pass


    # Enter a parse tree produced by simpleParser#assign_stat.
    def enterAssign_stat(self, ctx:simpleParser.Assign_statContext):
        pass

    # Exit a parse tree produced by simpleParser#assign_stat.
    def exitAssign_stat(self, ctx:simpleParser.Assign_statContext):
        pass


    # Enter a parse tree produced by simpleParser#stat.
    def enterStat(self, ctx:simpleParser.StatContext):
        pass

    # Exit a parse tree produced by simpleParser#stat.
    def exitStat(self, ctx:simpleParser.StatContext):
        pass


    # Enter a parse tree produced by simpleParser#block.
    def enterBlock(self, ctx:simpleParser.BlockContext):
        pass

    # Exit a parse tree produced by simpleParser#block.
    def exitBlock(self, ctx:simpleParser.BlockContext):
        pass


    # Enter a parse tree produced by simpleParser#par_block.
    def enterPar_block(self, ctx:simpleParser.Par_blockContext):
        pass

    # Exit a parse tree produced by simpleParser#par_block.
    def exitPar_block(self, ctx:simpleParser.Par_blockContext):
        pass


    # Enter a parse tree produced by simpleParser#paren_expr.
    def enterParen_expr(self, ctx:simpleParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#paren_expr.
    def exitParen_expr(self, ctx:simpleParser.Paren_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#neg_expr.
    def enterNeg_expr(self, ctx:simpleParser.Neg_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#neg_expr.
    def exitNeg_expr(self, ctx:simpleParser.Neg_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#int_expr.
    def enterInt_expr(self, ctx:simpleParser.Int_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#int_expr.
    def exitInt_expr(self, ctx:simpleParser.Int_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#type_name_expr.
    def enterType_name_expr(self, ctx:simpleParser.Type_name_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#type_name_expr.
    def exitType_name_expr(self, ctx:simpleParser.Type_name_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#index_expr.
    def enterIndex_expr(self, ctx:simpleParser.Index_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#index_expr.
    def exitIndex_expr(self, ctx:simpleParser.Index_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#macro_expr.
    def enterMacro_expr(self, ctx:simpleParser.Macro_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#macro_expr.
    def exitMacro_expr(self, ctx:simpleParser.Macro_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#name_expr.
    def enterName_expr(self, ctx:simpleParser.Name_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#name_expr.
    def exitName_expr(self, ctx:simpleParser.Name_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#addsub_expr.
    def enterAddsub_expr(self, ctx:simpleParser.Addsub_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#addsub_expr.
    def exitAddsub_expr(self, ctx:simpleParser.Addsub_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#delta_expr.
    def enterDelta_expr(self, ctx:simpleParser.Delta_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#delta_expr.
    def exitDelta_expr(self, ctx:simpleParser.Delta_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#coord_expr.
    def enterCoord_expr(self, ctx:simpleParser.Coord_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#coord_expr.
    def exitCoord_expr(self, ctx:simpleParser.Coord_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#injection_expr.
    def enterInjection_expr(self, ctx:simpleParser.Injection_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#injection_expr.
    def exitInjection_expr(self, ctx:simpleParser.Injection_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#gate_expr.
    def enterGate_expr(self, ctx:simpleParser.Gate_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#gate_expr.
    def exitGate_expr(self, ctx:simpleParser.Gate_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#well_expr.
    def enterWell_expr(self, ctx:simpleParser.Well_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#well_expr.
    def exitWell_expr(self, ctx:simpleParser.Well_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#drop_expr.
    def enterDrop_expr(self, ctx:simpleParser.Drop_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#drop_expr.
    def exitDrop_expr(self, ctx:simpleParser.Drop_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#function_expr.
    def enterFunction_expr(self, ctx:simpleParser.Function_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#function_expr.
    def exitFunction_expr(self, ctx:simpleParser.Function_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#to_expr.
    def enterTo_expr(self, ctx:simpleParser.To_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#to_expr.
    def exitTo_expr(self, ctx:simpleParser.To_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#muldiv_expr.
    def enterMuldiv_expr(self, ctx:simpleParser.Muldiv_exprContext):
        pass

    # Exit a parse tree produced by simpleParser#muldiv_expr.
    def exitMuldiv_expr(self, ctx:simpleParser.Muldiv_exprContext):
        pass


    # Enter a parse tree produced by simpleParser#direction.
    def enterDirection(self, ctx:simpleParser.DirectionContext):
        pass

    # Exit a parse tree produced by simpleParser#direction.
    def exitDirection(self, ctx:simpleParser.DirectionContext):
        pass


    # Enter a parse tree produced by simpleParser#axis.
    def enterAxis(self, ctx:simpleParser.AxisContext):
        pass

    # Exit a parse tree produced by simpleParser#axis.
    def exitAxis(self, ctx:simpleParser.AxisContext):
        pass


    # Enter a parse tree produced by simpleParser#macro_def.
    def enterMacro_def(self, ctx:simpleParser.Macro_defContext):
        pass

    # Exit a parse tree produced by simpleParser#macro_def.
    def exitMacro_def(self, ctx:simpleParser.Macro_defContext):
        pass


    # Enter a parse tree produced by simpleParser#param.
    def enterParam(self, ctx:simpleParser.ParamContext):
        pass

    # Exit a parse tree produced by simpleParser#param.
    def exitParam(self, ctx:simpleParser.ParamContext):
        pass


    # Enter a parse tree produced by simpleParser#param_type.
    def enterParam_type(self, ctx:simpleParser.Param_typeContext):
        pass

    # Exit a parse tree produced by simpleParser#param_type.
    def exitParam_type(self, ctx:simpleParser.Param_typeContext):
        pass


    # Enter a parse tree produced by simpleParser#name.
    def enterName(self, ctx:simpleParser.NameContext):
        pass

    # Exit a parse tree produced by simpleParser#name.
    def exitName(self, ctx:simpleParser.NameContext):
        pass


    # Enter a parse tree produced by simpleParser#kwd_names.
    def enterKwd_names(self, ctx:simpleParser.Kwd_namesContext):
        pass

    # Exit a parse tree produced by simpleParser#kwd_names.
    def exitKwd_names(self, ctx:simpleParser.Kwd_namesContext):
        pass



del simpleParser