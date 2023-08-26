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


# This class defines a complete listener for a parse tree produced by dmlParser.
class dmlListener(ParseTreeListener):

    # Enter a parse tree produced by dmlParser#macro_file.
    def enterMacro_file(self, ctx:dmlParser.Macro_fileContext):
        pass

    # Exit a parse tree produced by dmlParser#macro_file.
    def exitMacro_file(self, ctx:dmlParser.Macro_fileContext):
        pass


    # Enter a parse tree produced by dmlParser#compound_interactive.
    def enterCompound_interactive(self, ctx:dmlParser.Compound_interactiveContext):
        pass

    # Exit a parse tree produced by dmlParser#compound_interactive.
    def exitCompound_interactive(self, ctx:dmlParser.Compound_interactiveContext):
        pass


    # Enter a parse tree produced by dmlParser#loop_interactive.
    def enterLoop_interactive(self, ctx:dmlParser.Loop_interactiveContext):
        pass

    # Exit a parse tree produced by dmlParser#loop_interactive.
    def exitLoop_interactive(self, ctx:dmlParser.Loop_interactiveContext):
        pass


    # Enter a parse tree produced by dmlParser#decl_interactive.
    def enterDecl_interactive(self, ctx:dmlParser.Decl_interactiveContext):
        pass

    # Exit a parse tree produced by dmlParser#decl_interactive.
    def exitDecl_interactive(self, ctx:dmlParser.Decl_interactiveContext):
        pass


    # Enter a parse tree produced by dmlParser#macro_def_interactive.
    def enterMacro_def_interactive(self, ctx:dmlParser.Macro_def_interactiveContext):
        pass

    # Exit a parse tree produced by dmlParser#macro_def_interactive.
    def exitMacro_def_interactive(self, ctx:dmlParser.Macro_def_interactiveContext):
        pass


    # Enter a parse tree produced by dmlParser#expr_interactive.
    def enterExpr_interactive(self, ctx:dmlParser.Expr_interactiveContext):
        pass

    # Exit a parse tree produced by dmlParser#expr_interactive.
    def exitExpr_interactive(self, ctx:dmlParser.Expr_interactiveContext):
        pass


    # Enter a parse tree produced by dmlParser#empty_interactive.
    def enterEmpty_interactive(self, ctx:dmlParser.Empty_interactiveContext):
        pass

    # Exit a parse tree produced by dmlParser#empty_interactive.
    def exitEmpty_interactive(self, ctx:dmlParser.Empty_interactiveContext):
        pass


    # Enter a parse tree produced by dmlParser#declaration.
    def enterDeclaration(self, ctx:dmlParser.DeclarationContext):
        pass

    # Exit a parse tree produced by dmlParser#declaration.
    def exitDeclaration(self, ctx:dmlParser.DeclarationContext):
        pass


    # Enter a parse tree produced by dmlParser#decl_stat.
    def enterDecl_stat(self, ctx:dmlParser.Decl_statContext):
        pass

    # Exit a parse tree produced by dmlParser#decl_stat.
    def exitDecl_stat(self, ctx:dmlParser.Decl_statContext):
        pass


    # Enter a parse tree produced by dmlParser#macro_def_stat.
    def enterMacro_def_stat(self, ctx:dmlParser.Macro_def_statContext):
        pass

    # Exit a parse tree produced by dmlParser#macro_def_stat.
    def exitMacro_def_stat(self, ctx:dmlParser.Macro_def_statContext):
        pass


    # Enter a parse tree produced by dmlParser#if_stat.
    def enterIf_stat(self, ctx:dmlParser.If_statContext):
        pass

    # Exit a parse tree produced by dmlParser#if_stat.
    def exitIf_stat(self, ctx:dmlParser.If_statContext):
        pass


    # Enter a parse tree produced by dmlParser#expr_stat.
    def enterExpr_stat(self, ctx:dmlParser.Expr_statContext):
        pass

    # Exit a parse tree produced by dmlParser#expr_stat.
    def exitExpr_stat(self, ctx:dmlParser.Expr_statContext):
        pass


    # Enter a parse tree produced by dmlParser#loop_stat.
    def enterLoop_stat(self, ctx:dmlParser.Loop_statContext):
        pass

    # Exit a parse tree produced by dmlParser#loop_stat.
    def exitLoop_stat(self, ctx:dmlParser.Loop_statContext):
        pass


    # Enter a parse tree produced by dmlParser#exit_stat.
    def enterExit_stat(self, ctx:dmlParser.Exit_statContext):
        pass

    # Exit a parse tree produced by dmlParser#exit_stat.
    def exitExit_stat(self, ctx:dmlParser.Exit_statContext):
        pass


    # Enter a parse tree produced by dmlParser#return_stat.
    def enterReturn_stat(self, ctx:dmlParser.Return_statContext):
        pass

    # Exit a parse tree produced by dmlParser#return_stat.
    def exitReturn_stat(self, ctx:dmlParser.Return_statContext):
        pass


    # Enter a parse tree produced by dmlParser#compound_stat.
    def enterCompound_stat(self, ctx:dmlParser.Compound_statContext):
        pass

    # Exit a parse tree produced by dmlParser#compound_stat.
    def exitCompound_stat(self, ctx:dmlParser.Compound_statContext):
        pass


    # Enter a parse tree produced by dmlParser#block.
    def enterBlock(self, ctx:dmlParser.BlockContext):
        pass

    # Exit a parse tree produced by dmlParser#block.
    def exitBlock(self, ctx:dmlParser.BlockContext):
        pass


    # Enter a parse tree produced by dmlParser#par_block.
    def enterPar_block(self, ctx:dmlParser.Par_blockContext):
        pass

    # Exit a parse tree produced by dmlParser#par_block.
    def exitPar_block(self, ctx:dmlParser.Par_blockContext):
        pass


    # Enter a parse tree produced by dmlParser#n_times_loop_header.
    def enterN_times_loop_header(self, ctx:dmlParser.N_times_loop_headerContext):
        pass

    # Exit a parse tree produced by dmlParser#n_times_loop_header.
    def exitN_times_loop_header(self, ctx:dmlParser.N_times_loop_headerContext):
        pass


    # Enter a parse tree produced by dmlParser#duration_loop_header.
    def enterDuration_loop_header(self, ctx:dmlParser.Duration_loop_headerContext):
        pass

    # Exit a parse tree produced by dmlParser#duration_loop_header.
    def exitDuration_loop_header(self, ctx:dmlParser.Duration_loop_headerContext):
        pass


    # Enter a parse tree produced by dmlParser#test_loop_header.
    def enterTest_loop_header(self, ctx:dmlParser.Test_loop_headerContext):
        pass

    # Exit a parse tree produced by dmlParser#test_loop_header.
    def exitTest_loop_header(self, ctx:dmlParser.Test_loop_headerContext):
        pass


    # Enter a parse tree produced by dmlParser#seq_iter_loop_header.
    def enterSeq_iter_loop_header(self, ctx:dmlParser.Seq_iter_loop_headerContext):
        pass

    # Exit a parse tree produced by dmlParser#seq_iter_loop_header.
    def exitSeq_iter_loop_header(self, ctx:dmlParser.Seq_iter_loop_headerContext):
        pass


    # Enter a parse tree produced by dmlParser#step_iter_loop_header.
    def enterStep_iter_loop_header(self, ctx:dmlParser.Step_iter_loop_headerContext):
        pass

    # Exit a parse tree produced by dmlParser#step_iter_loop_header.
    def exitStep_iter_loop_header(self, ctx:dmlParser.Step_iter_loop_headerContext):
        pass


    # Enter a parse tree produced by dmlParser#step_first_and_dir.
    def enterStep_first_and_dir(self, ctx:dmlParser.Step_first_and_dirContext):
        pass

    # Exit a parse tree produced by dmlParser#step_first_and_dir.
    def exitStep_first_and_dir(self, ctx:dmlParser.Step_first_and_dirContext):
        pass


    # Enter a parse tree produced by dmlParser#loop.
    def enterLoop(self, ctx:dmlParser.LoopContext):
        pass

    # Exit a parse tree produced by dmlParser#loop.
    def exitLoop(self, ctx:dmlParser.LoopContext):
        pass


    # Enter a parse tree produced by dmlParser#exit.
    def enterExit(self, ctx:dmlParser.ExitContext):
        pass

    # Exit a parse tree produced by dmlParser#exit.
    def exitExit(self, ctx:dmlParser.ExitContext):
        pass


    # Enter a parse tree produced by dmlParser#ret.
    def enterRet(self, ctx:dmlParser.RetContext):
        pass

    # Exit a parse tree produced by dmlParser#ret.
    def exitRet(self, ctx:dmlParser.RetContext):
        pass


    # Enter a parse tree produced by dmlParser#term_punct.
    def enterTerm_punct(self, ctx:dmlParser.Term_punctContext):
        pass

    # Exit a parse tree produced by dmlParser#term_punct.
    def exitTerm_punct(self, ctx:dmlParser.Term_punctContext):
        pass


    # Enter a parse tree produced by dmlParser#neg_expr.
    def enterNeg_expr(self, ctx:dmlParser.Neg_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#neg_expr.
    def exitNeg_expr(self, ctx:dmlParser.Neg_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#const_rc_expr.
    def enterConst_rc_expr(self, ctx:dmlParser.Const_rc_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#const_rc_expr.
    def exitConst_rc_expr(self, ctx:dmlParser.Const_rc_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#unit_string_expr.
    def enterUnit_string_expr(self, ctx:dmlParser.Unit_string_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#unit_string_expr.
    def exitUnit_string_expr(self, ctx:dmlParser.Unit_string_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#action_expr.
    def enterAction_expr(self, ctx:dmlParser.Action_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#action_expr.
    def exitAction_expr(self, ctx:dmlParser.Action_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#attr_assign_expr.
    def enterAttr_assign_expr(self, ctx:dmlParser.Attr_assign_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#attr_assign_expr.
    def exitAttr_assign_expr(self, ctx:dmlParser.Attr_assign_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#unit_expr.
    def enterUnit_expr(self, ctx:dmlParser.Unit_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#unit_expr.
    def exitUnit_expr(self, ctx:dmlParser.Unit_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#temperature_expr.
    def enterTemperature_expr(self, ctx:dmlParser.Temperature_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#temperature_expr.
    def exitTemperature_expr(self, ctx:dmlParser.Temperature_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#mix_expr.
    def enterMix_expr(self, ctx:dmlParser.Mix_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#mix_expr.
    def exitMix_expr(self, ctx:dmlParser.Mix_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#print_expr.
    def enterPrint_expr(self, ctx:dmlParser.Print_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#print_expr.
    def exitPrint_expr(self, ctx:dmlParser.Print_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#become_expr.
    def enterBecome_expr(self, ctx:dmlParser.Become_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#become_expr.
    def exitBecome_expr(self, ctx:dmlParser.Become_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#numbered_expr.
    def enterNumbered_expr(self, ctx:dmlParser.Numbered_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#numbered_expr.
    def exitNumbered_expr(self, ctx:dmlParser.Numbered_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#rel_expr.
    def enterRel_expr(self, ctx:dmlParser.Rel_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#rel_expr.
    def exitRel_expr(self, ctx:dmlParser.Rel_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#existence_expr.
    def enterExistence_expr(self, ctx:dmlParser.Existence_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#existence_expr.
    def exitExistence_expr(self, ctx:dmlParser.Existence_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#not_expr.
    def enterNot_expr(self, ctx:dmlParser.Not_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#not_expr.
    def exitNot_expr(self, ctx:dmlParser.Not_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#reagent_lit_expr.
    def enterReagent_lit_expr(self, ctx:dmlParser.Reagent_lit_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#reagent_lit_expr.
    def exitReagent_lit_expr(self, ctx:dmlParser.Reagent_lit_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#and_expr.
    def enterAnd_expr(self, ctx:dmlParser.And_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#and_expr.
    def exitAnd_expr(self, ctx:dmlParser.And_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#prompt_expr.
    def enterPrompt_expr(self, ctx:dmlParser.Prompt_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#prompt_expr.
    def exitPrompt_expr(self, ctx:dmlParser.Prompt_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#or_expr.
    def enterOr_expr(self, ctx:dmlParser.Or_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#or_expr.
    def exitOr_expr(self, ctx:dmlParser.Or_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#injection_expr.
    def enterInjection_expr(self, ctx:dmlParser.Injection_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#injection_expr.
    def exitInjection_expr(self, ctx:dmlParser.Injection_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#drop_expr.
    def enterDrop_expr(self, ctx:dmlParser.Drop_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#drop_expr.
    def exitDrop_expr(self, ctx:dmlParser.Drop_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#function_expr.
    def enterFunction_expr(self, ctx:dmlParser.Function_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#function_expr.
    def exitFunction_expr(self, ctx:dmlParser.Function_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#to_expr.
    def enterTo_expr(self, ctx:dmlParser.To_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#to_expr.
    def exitTo_expr(self, ctx:dmlParser.To_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#bool_const_expr.
    def enterBool_const_expr(self, ctx:dmlParser.Bool_const_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#bool_const_expr.
    def exitBool_const_expr(self, ctx:dmlParser.Bool_const_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#has_expr.
    def enterHas_expr(self, ctx:dmlParser.Has_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#has_expr.
    def exitHas_expr(self, ctx:dmlParser.Has_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#float_expr.
    def enterFloat_expr(self, ctx:dmlParser.Float_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#float_expr.
    def exitFloat_expr(self, ctx:dmlParser.Float_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#n_rc_expr.
    def enterN_rc_expr(self, ctx:dmlParser.N_rc_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#n_rc_expr.
    def exitN_rc_expr(self, ctx:dmlParser.N_rc_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#macro_expr.
    def enterMacro_expr(self, ctx:dmlParser.Macro_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#macro_expr.
    def exitMacro_expr(self, ctx:dmlParser.Macro_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#name_expr.
    def enterName_expr(self, ctx:dmlParser.Name_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#name_expr.
    def exitName_expr(self, ctx:dmlParser.Name_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#addsub_expr.
    def enterAddsub_expr(self, ctx:dmlParser.Addsub_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#addsub_expr.
    def exitAddsub_expr(self, ctx:dmlParser.Addsub_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#liquid_expr.
    def enterLiquid_expr(self, ctx:dmlParser.Liquid_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#liquid_expr.
    def exitLiquid_expr(self, ctx:dmlParser.Liquid_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#reagent_expr.
    def enterReagent_expr(self, ctx:dmlParser.Reagent_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#reagent_expr.
    def exitReagent_expr(self, ctx:dmlParser.Reagent_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#dir_expr.
    def enterDir_expr(self, ctx:dmlParser.Dir_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#dir_expr.
    def exitDir_expr(self, ctx:dmlParser.Dir_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#coord_expr.
    def enterCoord_expr(self, ctx:dmlParser.Coord_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#coord_expr.
    def exitCoord_expr(self, ctx:dmlParser.Coord_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#pause_expr.
    def enterPause_expr(self, ctx:dmlParser.Pause_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#pause_expr.
    def exitPause_expr(self, ctx:dmlParser.Pause_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#accept_expr.
    def enterAccept_expr(self, ctx:dmlParser.Accept_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#accept_expr.
    def exitAccept_expr(self, ctx:dmlParser.Accept_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#attr_expr.
    def enterAttr_expr(self, ctx:dmlParser.Attr_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#attr_expr.
    def exitAttr_expr(self, ctx:dmlParser.Attr_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#paren_expr.
    def enterParen_expr(self, ctx:dmlParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#paren_expr.
    def exitParen_expr(self, ctx:dmlParser.Paren_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#split_expr.
    def enterSplit_expr(self, ctx:dmlParser.Split_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#split_expr.
    def exitSplit_expr(self, ctx:dmlParser.Split_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#type_name_expr.
    def enterType_name_expr(self, ctx:dmlParser.Type_name_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#type_name_expr.
    def exitType_name_expr(self, ctx:dmlParser.Type_name_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#index_expr.
    def enterIndex_expr(self, ctx:dmlParser.Index_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#index_expr.
    def exitIndex_expr(self, ctx:dmlParser.Index_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#name_assign_expr.
    def enterName_assign_expr(self, ctx:dmlParser.Name_assign_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#name_assign_expr.
    def exitName_assign_expr(self, ctx:dmlParser.Name_assign_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#string_lit_expr.
    def enterString_lit_expr(self, ctx:dmlParser.String_lit_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#string_lit_expr.
    def exitString_lit_expr(self, ctx:dmlParser.String_lit_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#magnitude_expr.
    def enterMagnitude_expr(self, ctx:dmlParser.Magnitude_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#magnitude_expr.
    def exitMagnitude_expr(self, ctx:dmlParser.Magnitude_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#in_dir_expr.
    def enterIn_dir_expr(self, ctx:dmlParser.In_dir_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#in_dir_expr.
    def exitIn_dir_expr(self, ctx:dmlParser.In_dir_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#pause_until_expr.
    def enterPause_until_expr(self, ctx:dmlParser.Pause_until_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#pause_until_expr.
    def exitPause_until_expr(self, ctx:dmlParser.Pause_until_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#muldiv_expr.
    def enterMuldiv_expr(self, ctx:dmlParser.Muldiv_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#muldiv_expr.
    def exitMuldiv_expr(self, ctx:dmlParser.Muldiv_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#int_expr.
    def enterInt_expr(self, ctx:dmlParser.Int_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#int_expr.
    def exitInt_expr(self, ctx:dmlParser.Int_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#turn_expr.
    def enterTurn_expr(self, ctx:dmlParser.Turn_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#turn_expr.
    def exitTurn_expr(self, ctx:dmlParser.Turn_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#cond_expr.
    def enterCond_expr(self, ctx:dmlParser.Cond_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#cond_expr.
    def exitCond_expr(self, ctx:dmlParser.Cond_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#merge_expr.
    def enterMerge_expr(self, ctx:dmlParser.Merge_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#merge_expr.
    def exitMerge_expr(self, ctx:dmlParser.Merge_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#delta_expr.
    def enterDelta_expr(self, ctx:dmlParser.Delta_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#delta_expr.
    def exitDelta_expr(self, ctx:dmlParser.Delta_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#sample_expr.
    def enterSample_expr(self, ctx:dmlParser.Sample_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#sample_expr.
    def exitSample_expr(self, ctx:dmlParser.Sample_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#unit_recip_expr.
    def enterUnit_recip_expr(self, ctx:dmlParser.Unit_recip_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#unit_recip_expr.
    def exitUnit_recip_expr(self, ctx:dmlParser.Unit_recip_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#is_expr.
    def enterIs_expr(self, ctx:dmlParser.Is_exprContext):
        pass

    # Exit a parse tree produced by dmlParser#is_expr.
    def exitIs_expr(self, ctx:dmlParser.Is_exprContext):
        pass


    # Enter a parse tree produced by dmlParser#existence.
    def enterExistence(self, ctx:dmlParser.ExistenceContext):
        pass

    # Exit a parse tree produced by dmlParser#existence.
    def exitExistence(self, ctx:dmlParser.ExistenceContext):
        pass


    # Enter a parse tree produced by dmlParser#possession.
    def enterPossession(self, ctx:dmlParser.PossessionContext):
        pass

    # Exit a parse tree produced by dmlParser#possession.
    def exitPossession(self, ctx:dmlParser.PossessionContext):
        pass


    # Enter a parse tree produced by dmlParser#reagent.
    def enterReagent(self, ctx:dmlParser.ReagentContext):
        pass

    # Exit a parse tree produced by dmlParser#reagent.
    def exitReagent(self, ctx:dmlParser.ReagentContext):
        pass


    # Enter a parse tree produced by dmlParser#direction.
    def enterDirection(self, ctx:dmlParser.DirectionContext):
        pass

    # Exit a parse tree produced by dmlParser#direction.
    def exitDirection(self, ctx:dmlParser.DirectionContext):
        pass


    # Enter a parse tree produced by dmlParser#turn.
    def enterTurn(self, ctx:dmlParser.TurnContext):
        pass

    # Exit a parse tree produced by dmlParser#turn.
    def exitTurn(self, ctx:dmlParser.TurnContext):
        pass


    # Enter a parse tree produced by dmlParser#rc.
    def enterRc(self, ctx:dmlParser.RcContext):
        pass

    # Exit a parse tree produced by dmlParser#rc.
    def exitRc(self, ctx:dmlParser.RcContext):
        pass


    # Enter a parse tree produced by dmlParser#axis.
    def enterAxis(self, ctx:dmlParser.AxisContext):
        pass

    # Exit a parse tree produced by dmlParser#axis.
    def exitAxis(self, ctx:dmlParser.AxisContext):
        pass


    # Enter a parse tree produced by dmlParser#macro_declaration.
    def enterMacro_declaration(self, ctx:dmlParser.Macro_declarationContext):
        pass

    # Exit a parse tree produced by dmlParser#macro_declaration.
    def exitMacro_declaration(self, ctx:dmlParser.Macro_declarationContext):
        pass


    # Enter a parse tree produced by dmlParser#macro_def.
    def enterMacro_def(self, ctx:dmlParser.Macro_defContext):
        pass

    # Exit a parse tree produced by dmlParser#macro_def.
    def exitMacro_def(self, ctx:dmlParser.Macro_defContext):
        pass


    # Enter a parse tree produced by dmlParser#macro_header.
    def enterMacro_header(self, ctx:dmlParser.Macro_headerContext):
        pass

    # Exit a parse tree produced by dmlParser#macro_header.
    def exitMacro_header(self, ctx:dmlParser.Macro_headerContext):
        pass


    # Enter a parse tree produced by dmlParser#param.
    def enterParam(self, ctx:dmlParser.ParamContext):
        pass

    # Exit a parse tree produced by dmlParser#param.
    def exitParam(self, ctx:dmlParser.ParamContext):
        pass


    # Enter a parse tree produced by dmlParser#no_arg_action.
    def enterNo_arg_action(self, ctx:dmlParser.No_arg_actionContext):
        pass

    # Exit a parse tree produced by dmlParser#no_arg_action.
    def exitNo_arg_action(self, ctx:dmlParser.No_arg_actionContext):
        pass


    # Enter a parse tree produced by dmlParser#value_type.
    def enterValue_type(self, ctx:dmlParser.Value_typeContext):
        pass

    # Exit a parse tree produced by dmlParser#value_type.
    def exitValue_type(self, ctx:dmlParser.Value_typeContext):
        pass


    # Enter a parse tree produced by dmlParser#not_future_type.
    def enterNot_future_type(self, ctx:dmlParser.Not_future_typeContext):
        pass

    # Exit a parse tree produced by dmlParser#not_future_type.
    def exitNot_future_type(self, ctx:dmlParser.Not_future_typeContext):
        pass


    # Enter a parse tree produced by dmlParser#not_maybe_type.
    def enterNot_maybe_type(self, ctx:dmlParser.Not_maybe_typeContext):
        pass

    # Exit a parse tree produced by dmlParser#not_maybe_type.
    def exitNot_maybe_type(self, ctx:dmlParser.Not_maybe_typeContext):
        pass


    # Enter a parse tree produced by dmlParser#sample_type.
    def enterSample_type(self, ctx:dmlParser.Sample_typeContext):
        pass

    # Exit a parse tree produced by dmlParser#sample_type.
    def exitSample_type(self, ctx:dmlParser.Sample_typeContext):
        pass


    # Enter a parse tree produced by dmlParser#atomic_type.
    def enterAtomic_type(self, ctx:dmlParser.Atomic_typeContext):
        pass

    # Exit a parse tree produced by dmlParser#atomic_type.
    def exitAtomic_type(self, ctx:dmlParser.Atomic_typeContext):
        pass


    # Enter a parse tree produced by dmlParser#sampleable_type.
    def enterSampleable_type(self, ctx:dmlParser.Sampleable_typeContext):
        pass

    # Exit a parse tree produced by dmlParser#sampleable_type.
    def exitSampleable_type(self, ctx:dmlParser.Sampleable_typeContext):
        pass


    # Enter a parse tree produced by dmlParser#quantity_type.
    def enterQuantity_type(self, ctx:dmlParser.Quantity_typeContext):
        pass

    # Exit a parse tree produced by dmlParser#quantity_type.
    def exitQuantity_type(self, ctx:dmlParser.Quantity_typeContext):
        pass


    # Enter a parse tree produced by dmlParser#component_type.
    def enterComponent_type(self, ctx:dmlParser.Component_typeContext):
        pass

    # Exit a parse tree produced by dmlParser#component_type.
    def exitComponent_type(self, ctx:dmlParser.Component_typeContext):
        pass


    # Enter a parse tree produced by dmlParser#dim_unit.
    def enterDim_unit(self, ctx:dmlParser.Dim_unitContext):
        pass

    # Exit a parse tree produced by dmlParser#dim_unit.
    def exitDim_unit(self, ctx:dmlParser.Dim_unitContext):
        pass


    # Enter a parse tree produced by dmlParser#numbered_type.
    def enterNumbered_type(self, ctx:dmlParser.Numbered_typeContext):
        pass

    # Exit a parse tree produced by dmlParser#numbered_type.
    def exitNumbered_type(self, ctx:dmlParser.Numbered_typeContext):
        pass


    # Enter a parse tree produced by dmlParser#minimum.
    def enterMinimum(self, ctx:dmlParser.MinimumContext):
        pass

    # Exit a parse tree produced by dmlParser#minimum.
    def exitMinimum(self, ctx:dmlParser.MinimumContext):
        pass


    # Enter a parse tree produced by dmlParser#maximum.
    def enterMaximum(self, ctx:dmlParser.MaximumContext):
        pass

    # Exit a parse tree produced by dmlParser#maximum.
    def exitMaximum(self, ctx:dmlParser.MaximumContext):
        pass


    # Enter a parse tree produced by dmlParser#min_max.
    def enterMin_max(self, ctx:dmlParser.Min_maxContext):
        pass

    # Exit a parse tree produced by dmlParser#min_max.
    def exitMin_max(self, ctx:dmlParser.Min_maxContext):
        pass


    # Enter a parse tree produced by dmlParser#attr.
    def enterAttr(self, ctx:dmlParser.AttrContext):
        pass

    # Exit a parse tree produced by dmlParser#attr.
    def exitAttr(self, ctx:dmlParser.AttrContext):
        pass


    # Enter a parse tree produced by dmlParser#rel.
    def enterRel(self, ctx:dmlParser.RelContext):
        pass

    # Exit a parse tree produced by dmlParser#rel.
    def exitRel(self, ctx:dmlParser.RelContext):
        pass


    # Enter a parse tree produced by dmlParser#bool_val.
    def enterBool_val(self, ctx:dmlParser.Bool_valContext):
        pass

    # Exit a parse tree produced by dmlParser#bool_val.
    def exitBool_val(self, ctx:dmlParser.Bool_valContext):
        pass


    # Enter a parse tree produced by dmlParser#name.
    def enterName(self, ctx:dmlParser.NameContext):
        pass

    # Exit a parse tree produced by dmlParser#name.
    def exitName(self, ctx:dmlParser.NameContext):
        pass


    # Enter a parse tree produced by dmlParser#multi_word_name.
    def enterMulti_word_name(self, ctx:dmlParser.Multi_word_nameContext):
        pass

    # Exit a parse tree produced by dmlParser#multi_word_name.
    def exitMulti_word_name(self, ctx:dmlParser.Multi_word_nameContext):
        pass


    # Enter a parse tree produced by dmlParser#kwd_names.
    def enterKwd_names(self, ctx:dmlParser.Kwd_namesContext):
        pass

    # Exit a parse tree produced by dmlParser#kwd_names.
    def exitKwd_names(self, ctx:dmlParser.Kwd_namesContext):
        pass


    # Enter a parse tree produced by dmlParser#string.
    def enterString(self, ctx:dmlParser.StringContext):
        pass

    # Exit a parse tree produced by dmlParser#string.
    def exitString(self, ctx:dmlParser.StringContext):
        pass


    # Enter a parse tree produced by dmlParser#old_attr.
    def enterOld_attr(self, ctx:dmlParser.Old_attrContext):
        pass

    # Exit a parse tree produced by dmlParser#old_attr.
    def exitOld_attr(self, ctx:dmlParser.Old_attrContext):
        pass


    # Enter a parse tree produced by dmlParser#attr_sep.
    def enterAttr_sep(self, ctx:dmlParser.Attr_sepContext):
        pass

    # Exit a parse tree produced by dmlParser#attr_sep.
    def exitAttr_sep(self, ctx:dmlParser.Attr_sepContext):
        pass


    # Enter a parse tree produced by dmlParser#inject_sep.
    def enterInject_sep(self, ctx:dmlParser.Inject_sepContext):
        pass

    # Exit a parse tree produced by dmlParser#inject_sep.
    def exitInject_sep(self, ctx:dmlParser.Inject_sepContext):
        pass



del dmlParser