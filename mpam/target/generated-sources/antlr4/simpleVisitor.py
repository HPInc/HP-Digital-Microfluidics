# Generated from simple.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .simpleParser import simpleParser
else:
    from simpleParser import simpleParser

from mpam.types import Dir 
from langsup.type_supp import Type


from mpam.types import Dir 


# This class defines a complete generic visitor for a parse tree produced by simpleParser.

class simpleVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by simpleParser#macro_file.
    def visitMacro_file(self, ctx:simpleParser.Macro_fileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#assign_stat.
    def visitAssign_stat(self, ctx:simpleParser.Assign_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#stat.
    def visitStat(self, ctx:simpleParser.StatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#block.
    def visitBlock(self, ctx:simpleParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#par_block.
    def visitPar_block(self, ctx:simpleParser.Par_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#paren_expr.
    def visitParen_expr(self, ctx:simpleParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#neg_expr.
    def visitNeg_expr(self, ctx:simpleParser.Neg_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#int_expr.
    def visitInt_expr(self, ctx:simpleParser.Int_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#type_name_expr.
    def visitType_name_expr(self, ctx:simpleParser.Type_name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#index_expr.
    def visitIndex_expr(self, ctx:simpleParser.Index_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#macro_expr.
    def visitMacro_expr(self, ctx:simpleParser.Macro_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#name_expr.
    def visitName_expr(self, ctx:simpleParser.Name_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#addsub_expr.
    def visitAddsub_expr(self, ctx:simpleParser.Addsub_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#delta_expr.
    def visitDelta_expr(self, ctx:simpleParser.Delta_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#coord_expr.
    def visitCoord_expr(self, ctx:simpleParser.Coord_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#injection_expr.
    def visitInjection_expr(self, ctx:simpleParser.Injection_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#gate_expr.
    def visitGate_expr(self, ctx:simpleParser.Gate_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#well_expr.
    def visitWell_expr(self, ctx:simpleParser.Well_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#drop_expr.
    def visitDrop_expr(self, ctx:simpleParser.Drop_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#function_expr.
    def visitFunction_expr(self, ctx:simpleParser.Function_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#to_expr.
    def visitTo_expr(self, ctx:simpleParser.To_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#muldiv_expr.
    def visitMuldiv_expr(self, ctx:simpleParser.Muldiv_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#direction.
    def visitDirection(self, ctx:simpleParser.DirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#axis.
    def visitAxis(self, ctx:simpleParser.AxisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#macro_def.
    def visitMacro_def(self, ctx:simpleParser.Macro_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#param.
    def visitParam(self, ctx:simpleParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#param_type.
    def visitParam_type(self, ctx:simpleParser.Param_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#name.
    def visitName(self, ctx:simpleParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by simpleParser#kwd_names.
    def visitKwd_names(self, ctx:simpleParser.Kwd_namesContext):
        return self.visitChildren(ctx)



del simpleParser