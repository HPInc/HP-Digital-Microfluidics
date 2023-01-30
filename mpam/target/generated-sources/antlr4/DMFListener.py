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


    # Enter a parse tree produced by DMFParser#loop_interactive.
    def enterLoop_interactive(self, ctx:DMFParser.Loop_interactiveContext):
        pass

    # Exit a parse tree produced by DMFParser#loop_interactive.
    def exitLoop_interactive(self, ctx:DMFParser.Loop_interactiveContext):
        pass


    # Enter a parse tree produced by DMFParser#decl_interactive.
    def enterDecl_interactive(self, ctx:DMFParser.Decl_interactiveContext):
        pass

    # Exit a parse tree produced by DMFParser#decl_interactive.
    def exitDecl_interactive(self, ctx:DMFParser.Decl_interactiveContext):
        pass


    # Enter a parse tree produced by DMFParser#expr_interactive.
    def enterExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext):
        pass

    # Exit a parse tree produced by DMFParser#expr_interactive.
    def exitExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext):
        pass


    # Enter a parse tree produced by DMFParser#empty_interactive.
    def enterEmpty_interactive(self, ctx:DMFParser.Empty_interactiveContext):
        pass

    # Exit a parse tree produced by DMFParser#empty_interactive.
    def exitEmpty_interactive(self, ctx:DMFParser.Empty_interactiveContext):
        pass


    # Enter a parse tree produced by DMFParser#declaration.
    def enterDeclaration(self, ctx:DMFParser.DeclarationContext):
        pass

    # Exit a parse tree produced by DMFParser#declaration.
    def exitDeclaration(self, ctx:DMFParser.DeclarationContext):
        pass


    # Enter a parse tree produced by DMFParser#decl_stat.
    def enterDecl_stat(self, ctx:DMFParser.Decl_statContext):
        pass

    # Exit a parse tree produced by DMFParser#decl_stat.
    def exitDecl_stat(self, ctx:DMFParser.Decl_statContext):
        pass


    # Enter a parse tree produced by DMFParser#if_stat.
    def enterIf_stat(self, ctx:DMFParser.If_statContext):
        pass

    # Exit a parse tree produced by DMFParser#if_stat.
    def exitIf_stat(self, ctx:DMFParser.If_statContext):
        pass


    # Enter a parse tree produced by DMFParser#expr_stat.
    def enterExpr_stat(self, ctx:DMFParser.Expr_statContext):
        pass

    # Exit a parse tree produced by DMFParser#expr_stat.
    def exitExpr_stat(self, ctx:DMFParser.Expr_statContext):
        pass


    # Enter a parse tree produced by DMFParser#loop_stat.
    def enterLoop_stat(self, ctx:DMFParser.Loop_statContext):
        pass

    # Exit a parse tree produced by DMFParser#loop_stat.
    def exitLoop_stat(self, ctx:DMFParser.Loop_statContext):
        pass


    # Enter a parse tree produced by DMFParser#exit_stat.
    def enterExit_stat(self, ctx:DMFParser.Exit_statContext):
        pass

    # Exit a parse tree produced by DMFParser#exit_stat.
    def exitExit_stat(self, ctx:DMFParser.Exit_statContext):
        pass


    # Enter a parse tree produced by DMFParser#return_stat.
    def enterReturn_stat(self, ctx:DMFParser.Return_statContext):
        pass

    # Exit a parse tree produced by DMFParser#return_stat.
    def exitReturn_stat(self, ctx:DMFParser.Return_statContext):
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


    # Enter a parse tree produced by DMFParser#n_times_loop_header.
    def enterN_times_loop_header(self, ctx:DMFParser.N_times_loop_headerContext):
        pass

    # Exit a parse tree produced by DMFParser#n_times_loop_header.
    def exitN_times_loop_header(self, ctx:DMFParser.N_times_loop_headerContext):
        pass


    # Enter a parse tree produced by DMFParser#duration_loop_header.
    def enterDuration_loop_header(self, ctx:DMFParser.Duration_loop_headerContext):
        pass

    # Exit a parse tree produced by DMFParser#duration_loop_header.
    def exitDuration_loop_header(self, ctx:DMFParser.Duration_loop_headerContext):
        pass


    # Enter a parse tree produced by DMFParser#test_loop_header.
    def enterTest_loop_header(self, ctx:DMFParser.Test_loop_headerContext):
        pass

    # Exit a parse tree produced by DMFParser#test_loop_header.
    def exitTest_loop_header(self, ctx:DMFParser.Test_loop_headerContext):
        pass


    # Enter a parse tree produced by DMFParser#seq_iter_loop_header.
    def enterSeq_iter_loop_header(self, ctx:DMFParser.Seq_iter_loop_headerContext):
        pass

    # Exit a parse tree produced by DMFParser#seq_iter_loop_header.
    def exitSeq_iter_loop_header(self, ctx:DMFParser.Seq_iter_loop_headerContext):
        pass


    # Enter a parse tree produced by DMFParser#step_iter_loop_header.
    def enterStep_iter_loop_header(self, ctx:DMFParser.Step_iter_loop_headerContext):
        pass

    # Exit a parse tree produced by DMFParser#step_iter_loop_header.
    def exitStep_iter_loop_header(self, ctx:DMFParser.Step_iter_loop_headerContext):
        pass


    # Enter a parse tree produced by DMFParser#step_first_and_dir.
    def enterStep_first_and_dir(self, ctx:DMFParser.Step_first_and_dirContext):
        pass

    # Exit a parse tree produced by DMFParser#step_first_and_dir.
    def exitStep_first_and_dir(self, ctx:DMFParser.Step_first_and_dirContext):
        pass


    # Enter a parse tree produced by DMFParser#loop.
    def enterLoop(self, ctx:DMFParser.LoopContext):
        pass

    # Exit a parse tree produced by DMFParser#loop.
    def exitLoop(self, ctx:DMFParser.LoopContext):
        pass


    # Enter a parse tree produced by DMFParser#exit.
    def enterExit(self, ctx:DMFParser.ExitContext):
        pass

    # Exit a parse tree produced by DMFParser#exit.
    def exitExit(self, ctx:DMFParser.ExitContext):
        pass


    # Enter a parse tree produced by DMFParser#ret.
    def enterRet(self, ctx:DMFParser.RetContext):
        pass

    # Exit a parse tree produced by DMFParser#ret.
    def exitRet(self, ctx:DMFParser.RetContext):
        pass


    # Enter a parse tree produced by DMFParser#term_punct.
    def enterTerm_punct(self, ctx:DMFParser.Term_punctContext):
        pass

    # Exit a parse tree produced by DMFParser#term_punct.
    def exitTerm_punct(self, ctx:DMFParser.Term_punctContext):
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


    # Enter a parse tree produced by DMFParser#const_rc_expr.
    def enterConst_rc_expr(self, ctx:DMFParser.Const_rc_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#const_rc_expr.
    def exitConst_rc_expr(self, ctx:DMFParser.Const_rc_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#unit_string_expr.
    def enterUnit_string_expr(self, ctx:DMFParser.Unit_string_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#unit_string_expr.
    def exitUnit_string_expr(self, ctx:DMFParser.Unit_string_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#action_expr.
    def enterAction_expr(self, ctx:DMFParser.Action_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#action_expr.
    def exitAction_expr(self, ctx:DMFParser.Action_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#attr_assign_expr.
    def enterAttr_assign_expr(self, ctx:DMFParser.Attr_assign_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#attr_assign_expr.
    def exitAttr_assign_expr(self, ctx:DMFParser.Attr_assign_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#type_name_expr.
    def enterType_name_expr(self, ctx:DMFParser.Type_name_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#type_name_expr.
    def exitType_name_expr(self, ctx:DMFParser.Type_name_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#unit_expr.
    def enterUnit_expr(self, ctx:DMFParser.Unit_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#unit_expr.
    def exitUnit_expr(self, ctx:DMFParser.Unit_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#temperature_expr.
    def enterTemperature_expr(self, ctx:DMFParser.Temperature_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#temperature_expr.
    def exitTemperature_expr(self, ctx:DMFParser.Temperature_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#index_expr.
    def enterIndex_expr(self, ctx:DMFParser.Index_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#index_expr.
    def exitIndex_expr(self, ctx:DMFParser.Index_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#print_expr.
    def enterPrint_expr(self, ctx:DMFParser.Print_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#print_expr.
    def exitPrint_expr(self, ctx:DMFParser.Print_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#numbered_expr.
    def enterNumbered_expr(self, ctx:DMFParser.Numbered_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#numbered_expr.
    def exitNumbered_expr(self, ctx:DMFParser.Numbered_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#rel_expr.
    def enterRel_expr(self, ctx:DMFParser.Rel_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#rel_expr.
    def exitRel_expr(self, ctx:DMFParser.Rel_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#existence_expr.
    def enterExistence_expr(self, ctx:DMFParser.Existence_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#existence_expr.
    def exitExistence_expr(self, ctx:DMFParser.Existence_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#name_assign_expr.
    def enterName_assign_expr(self, ctx:DMFParser.Name_assign_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#name_assign_expr.
    def exitName_assign_expr(self, ctx:DMFParser.Name_assign_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#string_lit_expr.
    def enterString_lit_expr(self, ctx:DMFParser.String_lit_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#string_lit_expr.
    def exitString_lit_expr(self, ctx:DMFParser.String_lit_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#not_expr.
    def enterNot_expr(self, ctx:DMFParser.Not_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#not_expr.
    def exitNot_expr(self, ctx:DMFParser.Not_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#reagent_lit_expr.
    def enterReagent_lit_expr(self, ctx:DMFParser.Reagent_lit_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#reagent_lit_expr.
    def exitReagent_lit_expr(self, ctx:DMFParser.Reagent_lit_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#and_expr.
    def enterAnd_expr(self, ctx:DMFParser.And_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#and_expr.
    def exitAnd_expr(self, ctx:DMFParser.And_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#magnitude_expr.
    def enterMagnitude_expr(self, ctx:DMFParser.Magnitude_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#magnitude_expr.
    def exitMagnitude_expr(self, ctx:DMFParser.Magnitude_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#prompt_expr.
    def enterPrompt_expr(self, ctx:DMFParser.Prompt_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#prompt_expr.
    def exitPrompt_expr(self, ctx:DMFParser.Prompt_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#in_dir_expr.
    def enterIn_dir_expr(self, ctx:DMFParser.In_dir_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#in_dir_expr.
    def exitIn_dir_expr(self, ctx:DMFParser.In_dir_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#or_expr.
    def enterOr_expr(self, ctx:DMFParser.Or_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#or_expr.
    def exitOr_expr(self, ctx:DMFParser.Or_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#injection_expr.
    def enterInjection_expr(self, ctx:DMFParser.Injection_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#injection_expr.
    def exitInjection_expr(self, ctx:DMFParser.Injection_exprContext):
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


    # Enter a parse tree produced by DMFParser#bool_const_expr.
    def enterBool_const_expr(self, ctx:DMFParser.Bool_const_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#bool_const_expr.
    def exitBool_const_expr(self, ctx:DMFParser.Bool_const_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#int_expr.
    def enterInt_expr(self, ctx:DMFParser.Int_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#int_expr.
    def exitInt_expr(self, ctx:DMFParser.Int_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#has_expr.
    def enterHas_expr(self, ctx:DMFParser.Has_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#has_expr.
    def exitHas_expr(self, ctx:DMFParser.Has_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#float_expr.
    def enterFloat_expr(self, ctx:DMFParser.Float_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#float_expr.
    def exitFloat_expr(self, ctx:DMFParser.Float_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#n_rc_expr.
    def enterN_rc_expr(self, ctx:DMFParser.N_rc_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#n_rc_expr.
    def exitN_rc_expr(self, ctx:DMFParser.N_rc_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#turn_expr.
    def enterTurn_expr(self, ctx:DMFParser.Turn_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#turn_expr.
    def exitTurn_expr(self, ctx:DMFParser.Turn_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#cond_expr.
    def enterCond_expr(self, ctx:DMFParser.Cond_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#cond_expr.
    def exitCond_expr(self, ctx:DMFParser.Cond_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#macro_expr.
    def enterMacro_expr(self, ctx:DMFParser.Macro_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#macro_expr.
    def exitMacro_expr(self, ctx:DMFParser.Macro_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#mw_name_expr.
    def enterMw_name_expr(self, ctx:DMFParser.Mw_name_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#mw_name_expr.
    def exitMw_name_expr(self, ctx:DMFParser.Mw_name_exprContext):
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


    # Enter a parse tree produced by DMFParser#liquid_expr.
    def enterLiquid_expr(self, ctx:DMFParser.Liquid_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#liquid_expr.
    def exitLiquid_expr(self, ctx:DMFParser.Liquid_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#reagent_expr.
    def enterReagent_expr(self, ctx:DMFParser.Reagent_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#reagent_expr.
    def exitReagent_expr(self, ctx:DMFParser.Reagent_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#dir_expr.
    def enterDir_expr(self, ctx:DMFParser.Dir_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#dir_expr.
    def exitDir_expr(self, ctx:DMFParser.Dir_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#coord_expr.
    def enterCoord_expr(self, ctx:DMFParser.Coord_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#coord_expr.
    def exitCoord_expr(self, ctx:DMFParser.Coord_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#pause_expr.
    def enterPause_expr(self, ctx:DMFParser.Pause_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#pause_expr.
    def exitPause_expr(self, ctx:DMFParser.Pause_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#is_expr.
    def enterIs_expr(self, ctx:DMFParser.Is_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#is_expr.
    def exitIs_expr(self, ctx:DMFParser.Is_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#attr_expr.
    def enterAttr_expr(self, ctx:DMFParser.Attr_exprContext):
        pass

    # Exit a parse tree produced by DMFParser#attr_expr.
    def exitAttr_expr(self, ctx:DMFParser.Attr_exprContext):
        pass


    # Enter a parse tree produced by DMFParser#existence.
    def enterExistence(self, ctx:DMFParser.ExistenceContext):
        pass

    # Exit a parse tree produced by DMFParser#existence.
    def exitExistence(self, ctx:DMFParser.ExistenceContext):
        pass


    # Enter a parse tree produced by DMFParser#possession.
    def enterPossession(self, ctx:DMFParser.PossessionContext):
        pass

    # Exit a parse tree produced by DMFParser#possession.
    def exitPossession(self, ctx:DMFParser.PossessionContext):
        pass


    # Enter a parse tree produced by DMFParser#reagent.
    def enterReagent(self, ctx:DMFParser.ReagentContext):
        pass

    # Exit a parse tree produced by DMFParser#reagent.
    def exitReagent(self, ctx:DMFParser.ReagentContext):
        pass


    # Enter a parse tree produced by DMFParser#direction.
    def enterDirection(self, ctx:DMFParser.DirectionContext):
        pass

    # Exit a parse tree produced by DMFParser#direction.
    def exitDirection(self, ctx:DMFParser.DirectionContext):
        pass


    # Enter a parse tree produced by DMFParser#turn.
    def enterTurn(self, ctx:DMFParser.TurnContext):
        pass

    # Exit a parse tree produced by DMFParser#turn.
    def exitTurn(self, ctx:DMFParser.TurnContext):
        pass


    # Enter a parse tree produced by DMFParser#rc.
    def enterRc(self, ctx:DMFParser.RcContext):
        pass

    # Exit a parse tree produced by DMFParser#rc.
    def exitRc(self, ctx:DMFParser.RcContext):
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


    # Enter a parse tree produced by DMFParser#no_arg_action.
    def enterNo_arg_action(self, ctx:DMFParser.No_arg_actionContext):
        pass

    # Exit a parse tree produced by DMFParser#no_arg_action.
    def exitNo_arg_action(self, ctx:DMFParser.No_arg_actionContext):
        pass


    # Enter a parse tree produced by DMFParser#param_type.
    def enterParam_type(self, ctx:DMFParser.Param_typeContext):
        pass

    # Exit a parse tree produced by DMFParser#param_type.
    def exitParam_type(self, ctx:DMFParser.Param_typeContext):
        pass


    # Enter a parse tree produced by DMFParser#base_param_type.
    def enterBase_param_type(self, ctx:DMFParser.Base_param_typeContext):
        pass

    # Exit a parse tree produced by DMFParser#base_param_type.
    def exitBase_param_type(self, ctx:DMFParser.Base_param_typeContext):
        pass


    # Enter a parse tree produced by DMFParser#dim_unit.
    def enterDim_unit(self, ctx:DMFParser.Dim_unitContext):
        pass

    # Exit a parse tree produced by DMFParser#dim_unit.
    def exitDim_unit(self, ctx:DMFParser.Dim_unitContext):
        pass


    # Enter a parse tree produced by DMFParser#numbered_type.
    def enterNumbered_type(self, ctx:DMFParser.Numbered_typeContext):
        pass

    # Exit a parse tree produced by DMFParser#numbered_type.
    def exitNumbered_type(self, ctx:DMFParser.Numbered_typeContext):
        pass


    # Enter a parse tree produced by DMFParser#attr.
    def enterAttr(self, ctx:DMFParser.AttrContext):
        pass

    # Exit a parse tree produced by DMFParser#attr.
    def exitAttr(self, ctx:DMFParser.AttrContext):
        pass


    # Enter a parse tree produced by DMFParser#rel.
    def enterRel(self, ctx:DMFParser.RelContext):
        pass

    # Exit a parse tree produced by DMFParser#rel.
    def exitRel(self, ctx:DMFParser.RelContext):
        pass


    # Enter a parse tree produced by DMFParser#bool_val.
    def enterBool_val(self, ctx:DMFParser.Bool_valContext):
        pass

    # Exit a parse tree produced by DMFParser#bool_val.
    def exitBool_val(self, ctx:DMFParser.Bool_valContext):
        pass


    # Enter a parse tree produced by DMFParser#name.
    def enterName(self, ctx:DMFParser.NameContext):
        pass

    # Exit a parse tree produced by DMFParser#name.
    def exitName(self, ctx:DMFParser.NameContext):
        pass


    # Enter a parse tree produced by DMFParser#multi_word_name.
    def enterMulti_word_name(self, ctx:DMFParser.Multi_word_nameContext):
        pass

    # Exit a parse tree produced by DMFParser#multi_word_name.
    def exitMulti_word_name(self, ctx:DMFParser.Multi_word_nameContext):
        pass


    # Enter a parse tree produced by DMFParser#kwd_names.
    def enterKwd_names(self, ctx:DMFParser.Kwd_namesContext):
        pass

    # Exit a parse tree produced by DMFParser#kwd_names.
    def exitKwd_names(self, ctx:DMFParser.Kwd_namesContext):
        pass


    # Enter a parse tree produced by DMFParser#string.
    def enterString(self, ctx:DMFParser.StringContext):
        pass

    # Exit a parse tree produced by DMFParser#string.
    def exitString(self, ctx:DMFParser.StringContext):
        pass



del DMFParser