# Generated from DMF.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DMFParser import DMFParser
else:
    from DMFParser import DMFParser

from mpam.types import Dir, OnOff, Turn, ticks, unknown_reagent, waste_reagent
from langsup.type_supp import Type, Rel, PhysUnit, EnvRelativeUnit, NumberedItem
from quantities import SI


from mpam.types import Dir 


# This class defines a complete generic visitor for a parse tree produced by DMFParser.

class DMFVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DMFParser#macro_file.
    def visitMacro_file(self, ctx:DMFParser.Macro_fileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#compound_interactive.
    def visitCompound_interactive(self, ctx:DMFParser.Compound_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#decl_interactive.
    def visitDecl_interactive(self, ctx:DMFParser.Decl_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#print_interactive.
    def visitPrint_interactive(self, ctx:DMFParser.Print_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#expr_interactive.
    def visitExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#empty_interactive.
    def visitEmpty_interactive(self, ctx:DMFParser.Empty_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#declaration.
    def visitDeclaration(self, ctx:DMFParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#printing.
    def visitPrinting(self, ctx:DMFParser.PrintingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#decl_stat.
    def visitDecl_stat(self, ctx:DMFParser.Decl_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#pause_stat.
    def visitPause_stat(self, ctx:DMFParser.Pause_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#print_stat.
    def visitPrint_stat(self, ctx:DMFParser.Print_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#if_stat.
    def visitIf_stat(self, ctx:DMFParser.If_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#expr_stat.
    def visitExpr_stat(self, ctx:DMFParser.Expr_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#loop_stat.
    def visitLoop_stat(self, ctx:DMFParser.Loop_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#compound_stat.
    def visitCompound_stat(self, ctx:DMFParser.Compound_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#block.
    def visitBlock(self, ctx:DMFParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#par_block.
    def visitPar_block(self, ctx:DMFParser.Par_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#repeat_loop.
    def visitRepeat_loop(self, ctx:DMFParser.Repeat_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#for_loop.
    def visitFor_loop(self, ctx:DMFParser.For_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#term_punct.
    def visitTerm_punct(self, ctx:DMFParser.Term_punctContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#paren_expr.
    def visitParen_expr(self, ctx:DMFParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#neg_expr.
    def visitNeg_expr(self, ctx:DMFParser.Neg_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#const_rc_expr.
    def visitConst_rc_expr(self, ctx:DMFParser.Const_rc_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#unit_string_expr.
    def visitUnit_string_expr(self, ctx:DMFParser.Unit_string_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#action_expr.
    def visitAction_expr(self, ctx:DMFParser.Action_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#attr_assign_expr.
    def visitAttr_assign_expr(self, ctx:DMFParser.Attr_assign_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#type_name_expr.
    def visitType_name_expr(self, ctx:DMFParser.Type_name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#unit_expr.
    def visitUnit_expr(self, ctx:DMFParser.Unit_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#temperature_expr.
    def visitTemperature_expr(self, ctx:DMFParser.Temperature_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#index_expr.
    def visitIndex_expr(self, ctx:DMFParser.Index_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#numbered_expr.
    def visitNumbered_expr(self, ctx:DMFParser.Numbered_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#rel_expr.
    def visitRel_expr(self, ctx:DMFParser.Rel_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#name_assign_expr.
    def visitName_assign_expr(self, ctx:DMFParser.Name_assign_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#string_lit_expr.
    def visitString_lit_expr(self, ctx:DMFParser.String_lit_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#not_expr.
    def visitNot_expr(self, ctx:DMFParser.Not_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#reagent_lit_expr.
    def visitReagent_lit_expr(self, ctx:DMFParser.Reagent_lit_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#and_expr.
    def visitAnd_expr(self, ctx:DMFParser.And_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#magnitude_expr.
    def visitMagnitude_expr(self, ctx:DMFParser.Magnitude_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#in_dir_expr.
    def visitIn_dir_expr(self, ctx:DMFParser.In_dir_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#or_expr.
    def visitOr_expr(self, ctx:DMFParser.Or_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#injection_expr.
    def visitInjection_expr(self, ctx:DMFParser.Injection_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#drop_expr.
    def visitDrop_expr(self, ctx:DMFParser.Drop_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#function_expr.
    def visitFunction_expr(self, ctx:DMFParser.Function_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#to_expr.
    def visitTo_expr(self, ctx:DMFParser.To_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#muldiv_expr.
    def visitMuldiv_expr(self, ctx:DMFParser.Muldiv_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#bool_const_expr.
    def visitBool_const_expr(self, ctx:DMFParser.Bool_const_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#int_expr.
    def visitInt_expr(self, ctx:DMFParser.Int_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#has_expr.
    def visitHas_expr(self, ctx:DMFParser.Has_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#float_expr.
    def visitFloat_expr(self, ctx:DMFParser.Float_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#n_rc_expr.
    def visitN_rc_expr(self, ctx:DMFParser.N_rc_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#turn_expr.
    def visitTurn_expr(self, ctx:DMFParser.Turn_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#cond_expr.
    def visitCond_expr(self, ctx:DMFParser.Cond_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#macro_expr.
    def visitMacro_expr(self, ctx:DMFParser.Macro_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#mw_name_expr.
    def visitMw_name_expr(self, ctx:DMFParser.Mw_name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#name_expr.
    def visitName_expr(self, ctx:DMFParser.Name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#addsub_expr.
    def visitAddsub_expr(self, ctx:DMFParser.Addsub_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#delta_expr.
    def visitDelta_expr(self, ctx:DMFParser.Delta_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#liquid_expr.
    def visitLiquid_expr(self, ctx:DMFParser.Liquid_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#reagent_expr.
    def visitReagent_expr(self, ctx:DMFParser.Reagent_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#dir_expr.
    def visitDir_expr(self, ctx:DMFParser.Dir_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#coord_expr.
    def visitCoord_expr(self, ctx:DMFParser.Coord_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#pause_expr.
    def visitPause_expr(self, ctx:DMFParser.Pause_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#is_expr.
    def visitIs_expr(self, ctx:DMFParser.Is_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#attr_expr.
    def visitAttr_expr(self, ctx:DMFParser.Attr_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#reagent.
    def visitReagent(self, ctx:DMFParser.ReagentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#direction.
    def visitDirection(self, ctx:DMFParser.DirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#turn.
    def visitTurn(self, ctx:DMFParser.TurnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#rc.
    def visitRc(self, ctx:DMFParser.RcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#axis.
    def visitAxis(self, ctx:DMFParser.AxisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#macro_def.
    def visitMacro_def(self, ctx:DMFParser.Macro_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#macro_header.
    def visitMacro_header(self, ctx:DMFParser.Macro_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#param.
    def visitParam(self, ctx:DMFParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#no_arg_action.
    def visitNo_arg_action(self, ctx:DMFParser.No_arg_actionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#param_type.
    def visitParam_type(self, ctx:DMFParser.Param_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#dim_unit.
    def visitDim_unit(self, ctx:DMFParser.Dim_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#numbered_type.
    def visitNumbered_type(self, ctx:DMFParser.Numbered_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#attr.
    def visitAttr(self, ctx:DMFParser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#rel.
    def visitRel(self, ctx:DMFParser.RelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#assign_op.
    def visitAssign_op(self, ctx:DMFParser.Assign_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#bool_val.
    def visitBool_val(self, ctx:DMFParser.Bool_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#name.
    def visitName(self, ctx:DMFParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#multi_word_name.
    def visitMulti_word_name(self, ctx:DMFParser.Multi_word_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#kwd_names.
    def visitKwd_names(self, ctx:DMFParser.Kwd_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#string.
    def visitString(self, ctx:DMFParser.StringContext):
        return self.visitChildren(ctx)



del DMFParser