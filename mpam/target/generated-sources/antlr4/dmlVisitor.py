# Generated from dml.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .dmlParser import dmlParser
else:
    from dmlParser import dmlParser

from mpam.types import Dir, OnOff, Turn, ticks, unknown_reagent, waste_reagent
from langsup.type_supp import Type, Rel, PhysUnit, EnvRelativeUnit, NumberedItem
from quantities import SI


from mpam.types import Dir 


# This class defines a complete generic visitor for a parse tree produced by dmlParser.

class dmlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by dmlParser#macro_file.
    def visitMacro_file(self, ctx:dmlParser.Macro_fileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#compound_interactive.
    def visitCompound_interactive(self, ctx:dmlParser.Compound_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#loop_interactive.
    def visitLoop_interactive(self, ctx:dmlParser.Loop_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#decl_interactive.
    def visitDecl_interactive(self, ctx:dmlParser.Decl_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#macro_def_interactive.
    def visitMacro_def_interactive(self, ctx:dmlParser.Macro_def_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#expr_interactive.
    def visitExpr_interactive(self, ctx:dmlParser.Expr_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#empty_interactive.
    def visitEmpty_interactive(self, ctx:dmlParser.Empty_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#declaration.
    def visitDeclaration(self, ctx:dmlParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#decl_stat.
    def visitDecl_stat(self, ctx:dmlParser.Decl_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#macro_def_stat.
    def visitMacro_def_stat(self, ctx:dmlParser.Macro_def_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#if_stat.
    def visitIf_stat(self, ctx:dmlParser.If_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#expr_stat.
    def visitExpr_stat(self, ctx:dmlParser.Expr_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#loop_stat.
    def visitLoop_stat(self, ctx:dmlParser.Loop_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#exit_stat.
    def visitExit_stat(self, ctx:dmlParser.Exit_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#return_stat.
    def visitReturn_stat(self, ctx:dmlParser.Return_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#compound_stat.
    def visitCompound_stat(self, ctx:dmlParser.Compound_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#block.
    def visitBlock(self, ctx:dmlParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#par_block.
    def visitPar_block(self, ctx:dmlParser.Par_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#n_times_loop_header.
    def visitN_times_loop_header(self, ctx:dmlParser.N_times_loop_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#duration_loop_header.
    def visitDuration_loop_header(self, ctx:dmlParser.Duration_loop_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#test_loop_header.
    def visitTest_loop_header(self, ctx:dmlParser.Test_loop_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#seq_iter_loop_header.
    def visitSeq_iter_loop_header(self, ctx:dmlParser.Seq_iter_loop_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#step_iter_loop_header.
    def visitStep_iter_loop_header(self, ctx:dmlParser.Step_iter_loop_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#step_first_and_dir.
    def visitStep_first_and_dir(self, ctx:dmlParser.Step_first_and_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#loop.
    def visitLoop(self, ctx:dmlParser.LoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#exit.
    def visitExit(self, ctx:dmlParser.ExitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#ret.
    def visitRet(self, ctx:dmlParser.RetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#term_punct.
    def visitTerm_punct(self, ctx:dmlParser.Term_punctContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#neg_expr.
    def visitNeg_expr(self, ctx:dmlParser.Neg_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#const_rc_expr.
    def visitConst_rc_expr(self, ctx:dmlParser.Const_rc_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#unit_string_expr.
    def visitUnit_string_expr(self, ctx:dmlParser.Unit_string_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#action_expr.
    def visitAction_expr(self, ctx:dmlParser.Action_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#attr_assign_expr.
    def visitAttr_assign_expr(self, ctx:dmlParser.Attr_assign_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#unit_expr.
    def visitUnit_expr(self, ctx:dmlParser.Unit_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#mix_expr.
    def visitMix_expr(self, ctx:dmlParser.Mix_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#print_expr.
    def visitPrint_expr(self, ctx:dmlParser.Print_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#become_expr.
    def visitBecome_expr(self, ctx:dmlParser.Become_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#numbered_expr.
    def visitNumbered_expr(self, ctx:dmlParser.Numbered_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#rel_expr.
    def visitRel_expr(self, ctx:dmlParser.Rel_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#existence_expr.
    def visitExistence_expr(self, ctx:dmlParser.Existence_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#not_expr.
    def visitNot_expr(self, ctx:dmlParser.Not_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#reagent_lit_expr.
    def visitReagent_lit_expr(self, ctx:dmlParser.Reagent_lit_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#and_expr.
    def visitAnd_expr(self, ctx:dmlParser.And_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#prompt_expr.
    def visitPrompt_expr(self, ctx:dmlParser.Prompt_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#or_expr.
    def visitOr_expr(self, ctx:dmlParser.Or_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#injection_expr.
    def visitInjection_expr(self, ctx:dmlParser.Injection_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#drop_expr.
    def visitDrop_expr(self, ctx:dmlParser.Drop_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#function_expr.
    def visitFunction_expr(self, ctx:dmlParser.Function_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#to_expr.
    def visitTo_expr(self, ctx:dmlParser.To_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#bool_const_expr.
    def visitBool_const_expr(self, ctx:dmlParser.Bool_const_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#has_expr.
    def visitHas_expr(self, ctx:dmlParser.Has_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#float_expr.
    def visitFloat_expr(self, ctx:dmlParser.Float_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#n_rc_expr.
    def visitN_rc_expr(self, ctx:dmlParser.N_rc_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#macro_expr.
    def visitMacro_expr(self, ctx:dmlParser.Macro_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#name_expr.
    def visitName_expr(self, ctx:dmlParser.Name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#addsub_expr.
    def visitAddsub_expr(self, ctx:dmlParser.Addsub_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#liquid_expr.
    def visitLiquid_expr(self, ctx:dmlParser.Liquid_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#reagent_expr.
    def visitReagent_expr(self, ctx:dmlParser.Reagent_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#dir_expr.
    def visitDir_expr(self, ctx:dmlParser.Dir_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#coord_expr.
    def visitCoord_expr(self, ctx:dmlParser.Coord_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#pause_expr.
    def visitPause_expr(self, ctx:dmlParser.Pause_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#accept_expr.
    def visitAccept_expr(self, ctx:dmlParser.Accept_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#attr_expr.
    def visitAttr_expr(self, ctx:dmlParser.Attr_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#paren_expr.
    def visitParen_expr(self, ctx:dmlParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#split_expr.
    def visitSplit_expr(self, ctx:dmlParser.Split_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#type_name_expr.
    def visitType_name_expr(self, ctx:dmlParser.Type_name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#index_expr.
    def visitIndex_expr(self, ctx:dmlParser.Index_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#name_assign_expr.
    def visitName_assign_expr(self, ctx:dmlParser.Name_assign_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#string_lit_expr.
    def visitString_lit_expr(self, ctx:dmlParser.String_lit_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#magnitude_expr.
    def visitMagnitude_expr(self, ctx:dmlParser.Magnitude_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#in_dir_expr.
    def visitIn_dir_expr(self, ctx:dmlParser.In_dir_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#pause_until_expr.
    def visitPause_until_expr(self, ctx:dmlParser.Pause_until_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#temperature_expr_C.
    def visitTemperature_expr_C(self, ctx:dmlParser.Temperature_expr_CContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#temperature_expr_F.
    def visitTemperature_expr_F(self, ctx:dmlParser.Temperature_expr_FContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#muldiv_expr.
    def visitMuldiv_expr(self, ctx:dmlParser.Muldiv_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#int_expr.
    def visitInt_expr(self, ctx:dmlParser.Int_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#turn_expr.
    def visitTurn_expr(self, ctx:dmlParser.Turn_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#cond_expr.
    def visitCond_expr(self, ctx:dmlParser.Cond_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#merge_expr.
    def visitMerge_expr(self, ctx:dmlParser.Merge_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#delta_expr.
    def visitDelta_expr(self, ctx:dmlParser.Delta_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#sample_expr.
    def visitSample_expr(self, ctx:dmlParser.Sample_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#unit_recip_expr.
    def visitUnit_recip_expr(self, ctx:dmlParser.Unit_recip_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#is_expr.
    def visitIs_expr(self, ctx:dmlParser.Is_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#existence.
    def visitExistence(self, ctx:dmlParser.ExistenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#possession.
    def visitPossession(self, ctx:dmlParser.PossessionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#reagent.
    def visitReagent(self, ctx:dmlParser.ReagentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#direction.
    def visitDirection(self, ctx:dmlParser.DirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#turn.
    def visitTurn(self, ctx:dmlParser.TurnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#rc.
    def visitRc(self, ctx:dmlParser.RcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#axis.
    def visitAxis(self, ctx:dmlParser.AxisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#macro_declaration.
    def visitMacro_declaration(self, ctx:dmlParser.Macro_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#macro_def.
    def visitMacro_def(self, ctx:dmlParser.Macro_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#macro_header.
    def visitMacro_header(self, ctx:dmlParser.Macro_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#param.
    def visitParam(self, ctx:dmlParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#no_arg_action.
    def visitNo_arg_action(self, ctx:dmlParser.No_arg_actionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#value_type.
    def visitValue_type(self, ctx:dmlParser.Value_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#not_future_type.
    def visitNot_future_type(self, ctx:dmlParser.Not_future_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#not_maybe_type.
    def visitNot_maybe_type(self, ctx:dmlParser.Not_maybe_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#sample_type.
    def visitSample_type(self, ctx:dmlParser.Sample_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#atomic_type.
    def visitAtomic_type(self, ctx:dmlParser.Atomic_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#sampleable_type.
    def visitSampleable_type(self, ctx:dmlParser.Sampleable_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#quantity_type.
    def visitQuantity_type(self, ctx:dmlParser.Quantity_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#component_type.
    def visitComponent_type(self, ctx:dmlParser.Component_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#dim_unit.
    def visitDim_unit(self, ctx:dmlParser.Dim_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#numbered_type.
    def visitNumbered_type(self, ctx:dmlParser.Numbered_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#minimum.
    def visitMinimum(self, ctx:dmlParser.MinimumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#maximum.
    def visitMaximum(self, ctx:dmlParser.MaximumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#min_max.
    def visitMin_max(self, ctx:dmlParser.Min_maxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#attr.
    def visitAttr(self, ctx:dmlParser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#rel.
    def visitRel(self, ctx:dmlParser.RelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#bool_val.
    def visitBool_val(self, ctx:dmlParser.Bool_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#future.
    def visitFuture(self, ctx:dmlParser.FutureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#name.
    def visitName(self, ctx:dmlParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#multi_word_name.
    def visitMulti_word_name(self, ctx:dmlParser.Multi_word_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#kwd_names.
    def visitKwd_names(self, ctx:dmlParser.Kwd_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#string.
    def visitString(self, ctx:dmlParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#old_attr.
    def visitOld_attr(self, ctx:dmlParser.Old_attrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#attr_sep.
    def visitAttr_sep(self, ctx:dmlParser.Attr_sepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dmlParser#inject_sep.
    def visitInject_sep(self, ctx:dmlParser.Inject_sepContext):
        return self.visitChildren(ctx)



del dmlParser