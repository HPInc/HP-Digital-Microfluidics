# Generated from DMF.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DMFParser import DMFParser
else:
    from DMFParser import DMFParser

from mpam.types import Dir, OnOff, Turn
from langsup.type_supp import Type, Rel
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


    # Visit a parse tree produced by DMFParser#assignment_interactive.
    def visitAssignment_interactive(self, ctx:DMFParser.Assignment_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#expr_interactive.
    def visitExpr_interactive(self, ctx:DMFParser.Expr_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#empty_interactive.
    def visitEmpty_interactive(self, ctx:DMFParser.Empty_interactiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#assignment.
    def visitAssignment(self, ctx:DMFParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#assign_stat.
    def visitAssign_stat(self, ctx:DMFParser.Assign_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#pause_stat.
    def visitPause_stat(self, ctx:DMFParser.Pause_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#if_stat.
    def visitIf_stat(self, ctx:DMFParser.If_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#expr_stat.
    def visitExpr_stat(self, ctx:DMFParser.Expr_statContext):
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


    # Visit a parse tree produced by DMFParser#paren_expr.
    def visitParen_expr(self, ctx:DMFParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#neg_expr.
    def visitNeg_expr(self, ctx:DMFParser.Neg_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#const_rc_expr.
    def visitConst_rc_expr(self, ctx:DMFParser.Const_rc_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#type_name_expr.
    def visitType_name_expr(self, ctx:DMFParser.Type_name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#index_expr.
    def visitIndex_expr(self, ctx:DMFParser.Index_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#rel_expr.
    def visitRel_expr(self, ctx:DMFParser.Rel_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#time_expr.
    def visitTime_expr(self, ctx:DMFParser.Time_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#not_expr.
    def visitNot_expr(self, ctx:DMFParser.Not_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#ticks_expr.
    def visitTicks_expr(self, ctx:DMFParser.Ticks_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#and_expr.
    def visitAnd_expr(self, ctx:DMFParser.And_exprContext):
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


    # Visit a parse tree produced by DMFParser#remove_expr.
    def visitRemove_expr(self, ctx:DMFParser.Remove_exprContext):
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


    # Visit a parse tree produced by DMFParser#dir_expr.
    def visitDir_expr(self, ctx:DMFParser.Dir_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#coord_expr.
    def visitCoord_expr(self, ctx:DMFParser.Coord_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#vol_expr.
    def visitVol_expr(self, ctx:DMFParser.Vol_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#twiddle_expr.
    def visitTwiddle_expr(self, ctx:DMFParser.Twiddle_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#pause_expr.
    def visitPause_expr(self, ctx:DMFParser.Pause_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#well_expr.
    def visitWell_expr(self, ctx:DMFParser.Well_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#attr_expr.
    def visitAttr_expr(self, ctx:DMFParser.Attr_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#drop_vol_expr.
    def visitDrop_vol_expr(self, ctx:DMFParser.Drop_vol_exprContext):
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


    # Visit a parse tree produced by DMFParser#param_type.
    def visitParam_type(self, ctx:DMFParser.Param_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#time_unit.
    def visitTime_unit(self, ctx:DMFParser.Time_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#vol_unit.
    def visitVol_unit(self, ctx:DMFParser.Vol_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#attr.
    def visitAttr(self, ctx:DMFParser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#rel.
    def visitRel(self, ctx:DMFParser.RelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#bool_val.
    def visitBool_val(self, ctx:DMFParser.Bool_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#name.
    def visitName(self, ctx:DMFParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DMFParser#kwd_names.
    def visitKwd_names(self, ctx:DMFParser.Kwd_namesContext):
        return self.visitChildren(ctx)



del DMFParser