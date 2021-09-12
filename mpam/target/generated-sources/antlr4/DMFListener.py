# Generated from DMF.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DMFParser import DMFParser
else:
    from DMFParser import DMFParser

from mpam.types import Dir, OnOff
from langsup.type_supp import Type


from mpam.types import Dir 


# This class defines a complete listener for a parse tree produced by DMFParser.
class DMFListener(ParseTreeListener):

    # Enter a parse tree produced by DMFParser#macro_file.
    def enterMacro_file(self, ctx:DMFParser.Macro_fileContext):
        pass

    # Exit a parse tree produced by DMFParser#macro_file.
    def exitMacro_file(self, ctx:DMFParser.Macro_fileContext):
        pass


    # Enter a parse tree produced by DMFParser#compound_interactive.
    def enterCompound_interactive(self, ctx:DMFParser.Compound_interactiveContext):
        pass

    # Exit a parse tree produced by DMFParser#compound_interactive.
    def exitCompound_interactive(self, ctx:DMFParser.Compound_interactiveContext):
        pass


    # Enter a parse tree produced by DMFParser#assignment_interactive.
    def enterAssignment_interactive(self, ctx:DMFParser.Assignment_interactiveContext):
        pass

    # Exit a parse tree produced by DMFParser#assignment_interactive.
    def exitAssignment_interactive(self, ctx:DMFParser.Assignment_interactiveContext):
        pass


    # Enter a parse tree produced by DMFParser#expr_interactive.
    def enterExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext):
        pass

    # Exit a parse tree produced by DMFParser#expr_interactive.
    def exitExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext):
        pass


    # Enter a parse tree produced by DMFParser#assignment.
    def enterAssignment(self, ctx:DMFParser.AssignmentContext):
        pass

    # Exit a parse tree produced by DMFParser#assignment.
    def exitAssignment(self, ctx:DMFParser.AssignmentContext):
        pass


    # Enter a parse tree produced by DMFParser#assign_stat.
    def enterAssign_stat(self, ctx:DMFParser.Assign_statContext):
        pass

    # Exit a parse tree produced by DMFParser#assign_stat.
    def exitAssign_stat(self, ctx:DMFParser.Assign_statContext):
        pass


    # Enter a parse tree produced by DMFParser#expr_stat.
    def enterExpr_stat(self, ctx:DMFParser.Expr_statContext):
        pass

    # Exit a parse tree produced by DMFParser#expr_stat.
    def exitExpr_stat(self, ctx:DMFParser.Expr_statContext):
        pass


    # Enter a parse tree produced by DMFParser#compound_stat.
    def enterCompound_stat(self, ctx:DMFParser.Compound_statContext):
        pass

    # Exit a parse tree produced by DMFParser#compound_stat.
    def exitCompound_stat(self, ctx:DMFParser.Compound_statContext):
        pass


    # Enter a parse tree produced by DMFParser#block.
    def enterBlock(self, ctx:DMFParser.BlockContext):
        pass

    # Exit a parse tree produced by DMFParser#block.
    def exitBlock(self, ctx:DMFParser.BlockContext):
        pass


    # Enter a parse tree produced by DMFParser#par_block.
    def enterPar_block(self, ctx:DMFParser.Par_blockContext):
        pass

    # Exit a parse tree produced by DMFParser#par_block.
    def exitPar_block(self, ctx:DMFParser.Par_blockContext):
        pass


    # Enter a parse tree produced by DMFParser#paren_expr.
    def enterParen_expr(self, ctx:DMFParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#paren_expr.
    def exitParen_expr(self, ctx:DMFParser.Paren_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#neg_expr.
    def enterNeg_expr(self, ctx:DMFParser.Neg_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#neg_expr.
    def exitNeg_expr(self, ctx:DMFParser.Neg_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#int_expr.
    def enterInt_expr(self, ctx:DMFParser.Int_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#int_expr.
    def exitInt_expr(self, ctx:DMFParser.Int_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#type_name_expr.
    def enterType_name_expr(self, ctx:DMFParser.Type_name_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#type_name_expr.
    def exitType_name_expr(self, ctx:DMFParser.Type_name_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#exit_pad_expr.
    def enterExit_pad_expr(self, ctx:DMFParser.Exit_pad_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#exit_pad_expr.
    def exitExit_pad_expr(self, ctx:DMFParser.Exit_pad_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#index_expr.
    def enterIndex_expr(self, ctx:DMFParser.Index_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#index_expr.
    def exitIndex_expr(self, ctx:DMFParser.Index_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#macro_expr.
    def enterMacro_expr(self, ctx:DMFParser.Macro_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#macro_expr.
    def exitMacro_expr(self, ctx:DMFParser.Macro_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#name_expr.
    def enterName_expr(self, ctx:DMFParser.Name_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#name_expr.
    def exitName_expr(self, ctx:DMFParser.Name_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#addsub_expr.
    def enterAddsub_expr(self, ctx:DMFParser.Addsub_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#addsub_expr.
    def exitAddsub_expr(self, ctx:DMFParser.Addsub_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#delta_expr.
    def enterDelta_expr(self, ctx:DMFParser.Delta_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#delta_expr.
    def exitDelta_expr(self, ctx:DMFParser.Delta_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#coord_expr.
    def enterCoord_expr(self, ctx:DMFParser.Coord_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#coord_expr.
    def exitCoord_expr(self, ctx:DMFParser.Coord_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#twiddle_expr.
    def enterTwiddle_expr(self, ctx:DMFParser.Twiddle_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#twiddle_expr.
    def exitTwiddle_expr(self, ctx:DMFParser.Twiddle_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#injection_expr.
    def enterInjection_expr(self, ctx:DMFParser.Injection_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#injection_expr.
    def exitInjection_expr(self, ctx:DMFParser.Injection_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#gate_expr.
    def enterGate_expr(self, ctx:DMFParser.Gate_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#gate_expr.
    def exitGate_expr(self, ctx:DMFParser.Gate_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#well_expr.
    def enterWell_expr(self, ctx:DMFParser.Well_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#well_expr.
    def exitWell_expr(self, ctx:DMFParser.Well_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#drop_expr.
    def enterDrop_expr(self, ctx:DMFParser.Drop_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#drop_expr.
    def exitDrop_expr(self, ctx:DMFParser.Drop_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#function_expr.
    def enterFunction_expr(self, ctx:DMFParser.Function_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#function_expr.
    def exitFunction_expr(self, ctx:DMFParser.Function_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#to_expr.
    def enterTo_expr(self, ctx:DMFParser.To_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#to_expr.
    def exitTo_expr(self, ctx:DMFParser.To_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#muldiv_expr.
    def enterMuldiv_expr(self, ctx:DMFParser.Muldiv_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#muldiv_expr.
    def exitMuldiv_expr(self, ctx:DMFParser.Muldiv_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#direction.
    def enterDirection(self, ctx:DMFParser.DirectionContext):
        pass

    # Exit a parse tree produced by DMFParser#direction.
    def exitDirection(self, ctx:DMFParser.DirectionContext):
        pass


    # Enter a parse tree produced by DMFParser#axis.
    def enterAxis(self, ctx:DMFParser.AxisContext):
        pass

    # Exit a parse tree produced by DMFParser#axis.
    def exitAxis(self, ctx:DMFParser.AxisContext):
        pass


    # Enter a parse tree produced by DMFParser#macro_def.
    def enterMacro_def(self, ctx:DMFParser.Macro_defContext):
        pass

    # Exit a parse tree produced by DMFParser#macro_def.
    def exitMacro_def(self, ctx:DMFParser.Macro_defContext):
        pass


    # Enter a parse tree produced by DMFParser#macro_header.
    def enterMacro_header(self, ctx:DMFParser.Macro_headerContext):
        pass

    # Exit a parse tree produced by DMFParser#macro_header.
    def exitMacro_header(self, ctx:DMFParser.Macro_headerContext):
        pass


    # Enter a parse tree produced by DMFParser#param.
    def enterParam(self, ctx:DMFParser.ParamContext):
        pass

    # Exit a parse tree produced by DMFParser#param.
    def exitParam(self, ctx:DMFParser.ParamContext):
        pass


    # Enter a parse tree produced by DMFParser#param_type.
    def enterParam_type(self, ctx:DMFParser.Param_typeContext):
        pass

    # Exit a parse tree produced by DMFParser#param_type.
    def exitParam_type(self, ctx:DMFParser.Param_typeContext):
        pass


    # Enter a parse tree produced by DMFParser#name.
    def enterName(self, ctx:DMFParser.NameContext):
        pass

    # Exit a parse tree produced by DMFParser#name.
    def exitName(self, ctx:DMFParser.NameContext):
        pass


    # Enter a parse tree produced by DMFParser#kwd_names.
    def enterKwd_names(self, ctx:DMFParser.Kwd_namesContext):
        pass

    # Exit a parse tree produced by DMFParser#kwd_names.
    def exitKwd_names(self, ctx:DMFParser.Kwd_namesContext):
        pass



del DMFParser