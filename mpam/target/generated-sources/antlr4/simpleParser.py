# Generated from simple.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


from mpam.types import Dir 
from langsup.type_supp import Type


from mpam.types import Dir 


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3/")
        buf.write("\u00c7\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2")
        buf.write("\7\2\34\n\2\f\2\16\2\37\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\4\3\4\3\4\3\4\5\4,\n\4\3\5\3\5\7\5\60\n\5\f\5\16")
        buf.write("\5\63\13\5\3\5\3\5\3\5\7\58\n\5\f\5\16\5;\13\5\3\5\5\5")
        buf.write(">\n\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\5\6R\n\6\3\6\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\5\6^\n\6\3\6\3\6\3\6\3\6\3\6\7\6")
        buf.write("e\n\6\f\6\16\6h\13\6\3\6\3\6\3\6\3\6\5\6n\n\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3")
        buf.write("\6\3\6\3\6\3\6\7\6\u0083\n\6\f\6\16\6\u0086\13\6\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7\u0094\n")
        buf.write("\7\3\b\3\b\3\b\3\b\5\b\u009a\n\b\3\t\3\t\3\t\3\t\3\t\7")
        buf.write("\t\u00a1\n\t\f\t\16\t\u00a4\13\t\5\t\u00a6\n\t\3\t\3\t")
        buf.write("\3\t\3\n\3\n\3\n\3\n\5\n\u00af\n\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\5\n\u00b7\n\n\3\13\3\13\3\13\3\13\3\13\3\13\5\13")
        buf.write("\u00bf\n\13\3\f\3\f\5\f\u00c3\n\f\3\r\3\r\3\r\2\3\n\16")
        buf.write("\2\4\6\b\n\f\16\20\22\24\26\30\2\n\3\2\20\21\4\2$$&&\4")
        buf.write("\2!!\'\'\3\2\23\24\3\2\25\26\3\2\27\30\3\2\31\32\3\2\34")
        buf.write("\35\2\u00de\2\35\3\2\2\2\4\"\3\2\2\2\6+\3\2\2\2\b=\3\2")
        buf.write("\2\2\nm\3\2\2\2\f\u0093\3\2\2\2\16\u0099\3\2\2\2\20\u009b")
        buf.write("\3\2\2\2\22\u00b6\3\2\2\2\24\u00be\3\2\2\2\26\u00c2\3")
        buf.write("\2\2\2\30\u00c4\3\2\2\2\32\34\5\4\3\2\33\32\3\2\2\2\34")
        buf.write("\37\3\2\2\2\35\33\3\2\2\2\35\36\3\2\2\2\36 \3\2\2\2\37")
        buf.write("\35\3\2\2\2 !\7\2\2\3!\3\3\2\2\2\"#\5\26\f\2#$\7\"\2\2")
        buf.write("$%\5\n\6\2%&\7(\2\2&\5\3\2\2\2\',\5\4\3\2()\5\n\6\2)*")
        buf.write("\7(\2\2*,\3\2\2\2+\'\3\2\2\2+(\3\2\2\2,\7\3\2\2\2-\61")
        buf.write("\7\3\2\2.\60\5\6\4\2/.\3\2\2\2\60\63\3\2\2\2\61/\3\2\2")
        buf.write("\2\61\62\3\2\2\2\62\64\3\2\2\2\63\61\3\2\2\2\64>\7\4\2")
        buf.write("\2\659\7\5\2\2\668\5\6\4\2\67\66\3\2\2\28;\3\2\2\29\67")
        buf.write("\3\2\2\29:\3\2\2\2:<\3\2\2\2;9\3\2\2\2<>\7\6\2\2=-\3\2")
        buf.write("\2\2=\65\3\2\2\2>\t\3\2\2\2?@\b\6\1\2@A\7\7\2\2AB\5\n")
        buf.write("\6\2BC\7\b\2\2Cn\3\2\2\2DE\7\7\2\2EF\5\n\6\2FG\7\t\2\2")
        buf.write("GH\5\n\6\2HI\7\b\2\2In\3\2\2\2JK\7\'\2\2Kn\5\n\6\22LM")
        buf.write("\5\f\7\2MN\5\n\6\rNn\3\2\2\2OQ\7\f\2\2PR\5\16\b\2QP\3")
        buf.write("\2\2\2QR\3\2\2\2RS\3\2\2\2Sn\5\n\6\fTU\7\r\2\2UV\7\16")
        buf.write("\2\2Vn\5\n\6\13WX\7\17\2\2XY\t\2\2\2Yn\5\n\6\nZn\5\20")
        buf.write("\t\2[]\5\24\13\2\\^\7*\2\2]\\\3\2\2\2]^\3\2\2\2^n\3\2")
        buf.write("\2\2_`\5\26\f\2`a\7\7\2\2af\5\n\6\2bc\7\t\2\2ce\5\n\6")
        buf.write("\2db\3\2\2\2eh\3\2\2\2fd\3\2\2\2fg\3\2\2\2gi\3\2\2\2h")
        buf.write("f\3\2\2\2ij\7\b\2\2jn\3\2\2\2kn\5\26\f\2ln\7*\2\2m?\3")
        buf.write("\2\2\2mD\3\2\2\2mJ\3\2\2\2mL\3\2\2\2mO\3\2\2\2mT\3\2\2")
        buf.write("\2mW\3\2\2\2mZ\3\2\2\2m[\3\2\2\2m_\3\2\2\2mk\3\2\2\2m")
        buf.write("l\3\2\2\2n\u0084\3\2\2\2op\f\17\2\2pq\t\3\2\2q\u0083\5")
        buf.write("\n\6\20rs\f\16\2\2st\t\4\2\2t\u0083\5\n\6\17uv\f\b\2\2")
        buf.write("vw\7%\2\2w\u0083\5\n\6\txy\f\21\2\2yz\7\n\2\2z{\5\n\6")
        buf.write("\2{|\7\13\2\2|\u0083\3\2\2\2}~\f\20\2\2~\u0083\5\f\7\2")
        buf.write("\177\u0080\f\t\2\2\u0080\u0081\7#\2\2\u0081\u0083\7\22")
        buf.write("\2\2\u0082o\3\2\2\2\u0082r\3\2\2\2\u0082u\3\2\2\2\u0082")
        buf.write("x\3\2\2\2\u0082}\3\2\2\2\u0082\177\3\2\2\2\u0083\u0086")
        buf.write("\3\2\2\2\u0084\u0082\3\2\2\2\u0084\u0085\3\2\2\2\u0085")
        buf.write("\13\3\2\2\2\u0086\u0084\3\2\2\2\u0087\u0088\t\5\2\2\u0088")
        buf.write("\u0089\b\7\1\2\u0089\u0094\b\7\1\2\u008a\u008b\t\6\2\2")
        buf.write("\u008b\u008c\b\7\1\2\u008c\u0094\b\7\1\2\u008d\u008e\t")
        buf.write("\7\2\2\u008e\u008f\b\7\1\2\u008f\u0094\b\7\1\2\u0090\u0091")
        buf.write("\t\b\2\2\u0091\u0092\b\7\1\2\u0092\u0094\b\7\1\2\u0093")
        buf.write("\u0087\3\2\2\2\u0093\u008a\3\2\2\2\u0093\u008d\3\2\2\2")
        buf.write("\u0093\u0090\3\2\2\2\u0094\r\3\2\2\2\u0095\u0096\7\33")
        buf.write("\2\2\u0096\u009a\b\b\1\2\u0097\u0098\t\t\2\2\u0098\u009a")
        buf.write("\b\b\1\2\u0099\u0095\3\2\2\2\u0099\u0097\3\2\2\2\u009a")
        buf.write("\17\3\2\2\2\u009b\u009c\7\36\2\2\u009c\u00a5\7\7\2\2\u009d")
        buf.write("\u00a2\5\22\n\2\u009e\u009f\7\t\2\2\u009f\u00a1\5\22\n")
        buf.write("\2\u00a0\u009e\3\2\2\2\u00a1\u00a4\3\2\2\2\u00a2\u00a0")
        buf.write("\3\2\2\2\u00a2\u00a3\3\2\2\2\u00a3\u00a6\3\2\2\2\u00a4")
        buf.write("\u00a2\3\2\2\2\u00a5\u009d\3\2\2\2\u00a5\u00a6\3\2\2\2")
        buf.write("\u00a6\u00a7\3\2\2\2\u00a7\u00a8\7\b\2\2\u00a8\u00a9\5")
        buf.write("\b\5\2\u00a9\21\3\2\2\2\u00aa\u00ab\5\24\13\2\u00ab\u00ae")
        buf.write("\b\n\1\2\u00ac\u00ad\7*\2\2\u00ad\u00af\b\n\1\2\u00ae")
        buf.write("\u00ac\3\2\2\2\u00ae\u00af\3\2\2\2\u00af\u00b7\3\2\2\2")
        buf.write("\u00b0\u00b1\5\26\f\2\u00b1\u00b2\7%\2\2\u00b2\u00b3\5")
        buf.write("\24\13\2\u00b3\u00b4\b\n\1\2\u00b4\u00b5\b\n\1\2\u00b5")
        buf.write("\u00b7\3\2\2\2\u00b6\u00aa\3\2\2\2\u00b6\u00b0\3\2\2\2")
        buf.write("\u00b7\23\3\2\2\2\u00b8\u00b9\7\17\2\2\u00b9\u00bf\b\13")
        buf.write("\1\2\u00ba\u00bb\7\r\2\2\u00bb\u00bf\b\13\1\2\u00bc\u00bd")
        buf.write("\7\37\2\2\u00bd\u00bf\b\13\1\2\u00be\u00b8\3\2\2\2\u00be")
        buf.write("\u00ba\3\2\2\2\u00be\u00bc\3\2\2\2\u00bf\25\3\2\2\2\u00c0")
        buf.write("\u00c3\7)\2\2\u00c1\u00c3\5\30\r\2\u00c2\u00c0\3\2\2\2")
        buf.write("\u00c2\u00c1\3\2\2\2\u00c3\27\3\2\2\2\u00c4\u00c5\7 \2")
        buf.write("\2\u00c5\31\3\2\2\2\25\35+\619=Q]fm\u0082\u0084\u0093")
        buf.write("\u0099\u00a2\u00a5\u00ae\u00b6\u00be\u00c2")
        return buf.getvalue()


class simpleParser ( Parser ):

    grammarFileName = "simple.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "'}'", "'[['", "']]'", "'('", "')'", 
                     "','", "'['", "']'", "'to'", "'well'", "'#'", "'drop'", 
                     "'@'", "'at'", "'gate'", "'up'", "'north'", "'down'", 
                     "'south'", "'left'", "'west'", "'right'", "'east'", 
                     "'row'", "'col'", "'column'", "'macro'", "'int'", "'**__**'", 
                     "'+'", "'='", "''s'", "'/'", "':'", "'*'", "'-'", "';'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "ADD", "ASSIGN", 
                      "ATTR", "DIV", "INJECT", "MUL", "SUB", "TERMINATOR", 
                      "ID", "INT", "FLOAT", "STRING", "EOL_COMMENT", "COMMENT", 
                      "WS" ]

    RULE_macro_file = 0
    RULE_top_level_stat = 1
    RULE_stat = 2
    RULE_compound = 3
    RULE_expr = 4
    RULE_direction = 5
    RULE_axis = 6
    RULE_macro_def = 7
    RULE_param = 8
    RULE_param_type = 9
    RULE_name = 10
    RULE_kwd_names = 11

    ruleNames =  [ "macro_file", "top_level_stat", "stat", "compound", "expr", 
                   "direction", "axis", "macro_def", "param", "param_type", 
                   "name", "kwd_names" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    ADD=31
    ASSIGN=32
    ATTR=33
    DIV=34
    INJECT=35
    MUL=36
    SUB=37
    TERMINATOR=38
    ID=39
    INT=40
    FLOAT=41
    STRING=42
    EOL_COMMENT=43
    COMMENT=44
    WS=45

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Macro_fileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(simpleParser.EOF, 0)

        def top_level_stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.Top_level_statContext)
            else:
                return self.getTypedRuleContext(simpleParser.Top_level_statContext,i)


        def getRuleIndex(self):
            return simpleParser.RULE_macro_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacro_file" ):
                listener.enterMacro_file(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacro_file" ):
                listener.exitMacro_file(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacro_file" ):
                return visitor.visitMacro_file(self)
            else:
                return visitor.visitChildren(self)




    def macro_file(self):

        localctx = simpleParser.Macro_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_macro_file)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==simpleParser.T__29 or _la==simpleParser.ID:
                self.state = 24
                self.top_level_stat()
                self.state = 29
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 30
            self.match(simpleParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Top_level_statContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return simpleParser.RULE_top_level_stat

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Assign_statContext(Top_level_statContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.Top_level_statContext
            super().__init__(parser)
            self.which = None # NameContext
            self.what = None # ExprContext
            self.copyFrom(ctx)

        def ASSIGN(self):
            return self.getToken(simpleParser.ASSIGN, 0)
        def TERMINATOR(self):
            return self.getToken(simpleParser.TERMINATOR, 0)
        def name(self):
            return self.getTypedRuleContext(simpleParser.NameContext,0)

        def expr(self):
            return self.getTypedRuleContext(simpleParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssign_stat" ):
                listener.enterAssign_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssign_stat" ):
                listener.exitAssign_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssign_stat" ):
                return visitor.visitAssign_stat(self)
            else:
                return visitor.visitChildren(self)



    def top_level_stat(self):

        localctx = simpleParser.Top_level_statContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_top_level_stat)
        try:
            localctx = simpleParser.Assign_statContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            localctx.which = self.name()
            self.state = 33
            self.match(simpleParser.ASSIGN)
            self.state = 34
            localctx.what = self.expr(0)
            self.state = 35
            self.match(simpleParser.TERMINATOR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def top_level_stat(self):
            return self.getTypedRuleContext(simpleParser.Top_level_statContext,0)


        def expr(self):
            return self.getTypedRuleContext(simpleParser.ExprContext,0)


        def TERMINATOR(self):
            return self.getToken(simpleParser.TERMINATOR, 0)

        def getRuleIndex(self):
            return simpleParser.RULE_stat

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStat" ):
                listener.enterStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStat" ):
                listener.exitStat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStat" ):
                return visitor.visitStat(self)
            else:
                return visitor.visitChildren(self)




    def stat(self):

        localctx = simpleParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stat)
        try:
            self.state = 41
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 37
                self.top_level_stat()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 38
                self.expr(0)
                self.state = 39
                self.match(simpleParser.TERMINATOR)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompoundContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return simpleParser.RULE_compound

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Par_blockContext(CompoundContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.CompoundContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.StatContext)
            else:
                return self.getTypedRuleContext(simpleParser.StatContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPar_block" ):
                listener.enterPar_block(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPar_block" ):
                listener.exitPar_block(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPar_block" ):
                return visitor.visitPar_block(self)
            else:
                return visitor.visitChildren(self)


    class BlockContext(CompoundContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.CompoundContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.StatContext)
            else:
                return self.getTypedRuleContext(simpleParser.StatContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)



    def compound(self):

        localctx = simpleParser.CompoundContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_compound)
        self._la = 0 # Token type
        try:
            self.state = 59
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [simpleParser.T__0]:
                localctx = simpleParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 43
                self.match(simpleParser.T__0)
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << simpleParser.T__4) | (1 << simpleParser.T__9) | (1 << simpleParser.T__10) | (1 << simpleParser.T__12) | (1 << simpleParser.T__16) | (1 << simpleParser.T__17) | (1 << simpleParser.T__18) | (1 << simpleParser.T__19) | (1 << simpleParser.T__20) | (1 << simpleParser.T__21) | (1 << simpleParser.T__22) | (1 << simpleParser.T__23) | (1 << simpleParser.T__27) | (1 << simpleParser.T__28) | (1 << simpleParser.T__29) | (1 << simpleParser.SUB) | (1 << simpleParser.ID) | (1 << simpleParser.INT))) != 0):
                    self.state = 44
                    self.stat()
                    self.state = 49
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 50
                self.match(simpleParser.T__1)
                pass
            elif token in [simpleParser.T__2]:
                localctx = simpleParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 51
                self.match(simpleParser.T__2)
                self.state = 55
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << simpleParser.T__4) | (1 << simpleParser.T__9) | (1 << simpleParser.T__10) | (1 << simpleParser.T__12) | (1 << simpleParser.T__16) | (1 << simpleParser.T__17) | (1 << simpleParser.T__18) | (1 << simpleParser.T__19) | (1 << simpleParser.T__20) | (1 << simpleParser.T__21) | (1 << simpleParser.T__22) | (1 << simpleParser.T__23) | (1 << simpleParser.T__27) | (1 << simpleParser.T__28) | (1 << simpleParser.T__29) | (1 << simpleParser.SUB) | (1 << simpleParser.ID) | (1 << simpleParser.INT))) != 0):
                    self.state = 52
                    self.stat()
                    self.state = 57
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 58
                self.match(simpleParser.T__3)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return simpleParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class Paren_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(simpleParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParen_expr" ):
                listener.enterParen_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParen_expr" ):
                listener.exitParen_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParen_expr" ):
                return visitor.visitParen_expr(self)
            else:
                return visitor.visitChildren(self)


    class Neg_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.rhs = None # ExprContext
            self.copyFrom(ctx)

        def SUB(self):
            return self.getToken(simpleParser.SUB, 0)
        def expr(self):
            return self.getTypedRuleContext(simpleParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNeg_expr" ):
                listener.enterNeg_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNeg_expr" ):
                listener.exitNeg_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNeg_expr" ):
                return visitor.visitNeg_expr(self)
            else:
                return visitor.visitChildren(self)


    class Int_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(simpleParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInt_expr" ):
                listener.enterInt_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInt_expr" ):
                listener.exitInt_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInt_expr" ):
                return visitor.visitInt_expr(self)
            else:
                return visitor.visitChildren(self)


    class Type_name_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.n = None # Token
            self.copyFrom(ctx)

        def param_type(self):
            return self.getTypedRuleContext(simpleParser.Param_typeContext,0)

        def INT(self):
            return self.getToken(simpleParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType_name_expr" ):
                listener.enterType_name_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType_name_expr" ):
                listener.exitType_name_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType_name_expr" ):
                return visitor.visitType_name_expr(self)
            else:
                return visitor.visitChildren(self)


    class Index_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.who = None # ExprContext
            self.which = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.ExprContext)
            else:
                return self.getTypedRuleContext(simpleParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIndex_expr" ):
                listener.enterIndex_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIndex_expr" ):
                listener.exitIndex_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIndex_expr" ):
                return visitor.visitIndex_expr(self)
            else:
                return visitor.visitChildren(self)


    class Macro_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def macro_def(self):
            return self.getTypedRuleContext(simpleParser.Macro_defContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacro_expr" ):
                listener.enterMacro_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacro_expr" ):
                listener.exitMacro_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacro_expr" ):
                return visitor.visitMacro_expr(self)
            else:
                return visitor.visitChildren(self)


    class Name_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(simpleParser.NameContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterName_expr" ):
                listener.enterName_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitName_expr" ):
                listener.exitName_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitName_expr" ):
                return visitor.visitName_expr(self)
            else:
                return visitor.visitChildren(self)


    class Addsub_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.lhs = None # ExprContext
            self.rhs = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.ExprContext)
            else:
                return self.getTypedRuleContext(simpleParser.ExprContext,i)

        def ADD(self):
            return self.getToken(simpleParser.ADD, 0)
        def SUB(self):
            return self.getToken(simpleParser.SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddsub_expr" ):
                listener.enterAddsub_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddsub_expr" ):
                listener.exitAddsub_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddsub_expr" ):
                return visitor.visitAddsub_expr(self)
            else:
                return visitor.visitChildren(self)


    class Delta_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.dist = None # ExprContext
            self.copyFrom(ctx)

        def direction(self):
            return self.getTypedRuleContext(simpleParser.DirectionContext,0)

        def expr(self):
            return self.getTypedRuleContext(simpleParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDelta_expr" ):
                listener.enterDelta_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDelta_expr" ):
                listener.exitDelta_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDelta_expr" ):
                return visitor.visitDelta_expr(self)
            else:
                return visitor.visitChildren(self)


    class Coord_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.x = None # ExprContext
            self.y = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.ExprContext)
            else:
                return self.getTypedRuleContext(simpleParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCoord_expr" ):
                listener.enterCoord_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCoord_expr" ):
                listener.exitCoord_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCoord_expr" ):
                return visitor.visitCoord_expr(self)
            else:
                return visitor.visitChildren(self)


    class Injection_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.who = None # ExprContext
            self.what = None # ExprContext
            self.copyFrom(ctx)

        def INJECT(self):
            return self.getToken(simpleParser.INJECT, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.ExprContext)
            else:
                return self.getTypedRuleContext(simpleParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInjection_expr" ):
                listener.enterInjection_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInjection_expr" ):
                listener.exitInjection_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInjection_expr" ):
                return visitor.visitInjection_expr(self)
            else:
                return visitor.visitChildren(self)


    class Gate_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.well = None # ExprContext
            self.copyFrom(ctx)

        def ATTR(self):
            return self.getToken(simpleParser.ATTR, 0)
        def expr(self):
            return self.getTypedRuleContext(simpleParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGate_expr" ):
                listener.enterGate_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGate_expr" ):
                listener.exitGate_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGate_expr" ):
                return visitor.visitGate_expr(self)
            else:
                return visitor.visitChildren(self)


    class Well_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.which = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(simpleParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWell_expr" ):
                listener.enterWell_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWell_expr" ):
                listener.exitWell_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWell_expr" ):
                return visitor.visitWell_expr(self)
            else:
                return visitor.visitChildren(self)


    class Drop_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.loc = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(simpleParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDrop_expr" ):
                listener.enterDrop_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDrop_expr" ):
                listener.exitDrop_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDrop_expr" ):
                return visitor.visitDrop_expr(self)
            else:
                return visitor.visitChildren(self)


    class Function_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self._expr = None # ExprContext
            self.args = list() # of ExprContexts
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(simpleParser.NameContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.ExprContext)
            else:
                return self.getTypedRuleContext(simpleParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_expr" ):
                listener.enterFunction_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_expr" ):
                listener.exitFunction_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction_expr" ):
                return visitor.visitFunction_expr(self)
            else:
                return visitor.visitChildren(self)


    class To_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.which = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(simpleParser.ExprContext,0)

        def axis(self):
            return self.getTypedRuleContext(simpleParser.AxisContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTo_expr" ):
                listener.enterTo_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTo_expr" ):
                listener.exitTo_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTo_expr" ):
                return visitor.visitTo_expr(self)
            else:
                return visitor.visitChildren(self)


    class Muldiv_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a simpleParser.ExprContext
            super().__init__(parser)
            self.lhs = None # ExprContext
            self.rhs = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.ExprContext)
            else:
                return self.getTypedRuleContext(simpleParser.ExprContext,i)

        def MUL(self):
            return self.getToken(simpleParser.MUL, 0)
        def DIV(self):
            return self.getToken(simpleParser.DIV, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMuldiv_expr" ):
                listener.enterMuldiv_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMuldiv_expr" ):
                listener.exitMuldiv_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMuldiv_expr" ):
                return visitor.visitMuldiv_expr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = simpleParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                localctx = simpleParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 62
                self.match(simpleParser.T__4)
                self.state = 63
                self.expr(0)
                self.state = 64
                self.match(simpleParser.T__5)
                pass

            elif la_ == 2:
                localctx = simpleParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 66
                self.match(simpleParser.T__4)
                self.state = 67
                localctx.x = self.expr(0)
                self.state = 68
                self.match(simpleParser.T__6)
                self.state = 69
                localctx.y = self.expr(0)
                self.state = 70
                self.match(simpleParser.T__5)
                pass

            elif la_ == 3:
                localctx = simpleParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 72
                self.match(simpleParser.SUB)
                self.state = 73
                localctx.rhs = self.expr(16)
                pass

            elif la_ == 4:
                localctx = simpleParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 74
                self.direction()
                self.state = 75
                localctx.dist = self.expr(11)
                pass

            elif la_ == 5:
                localctx = simpleParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 77
                self.match(simpleParser.T__9)
                self.state = 79
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << simpleParser.T__24) | (1 << simpleParser.T__25) | (1 << simpleParser.T__26))) != 0):
                    self.state = 78
                    self.axis()


                self.state = 81
                localctx.which = self.expr(10)
                pass

            elif la_ == 6:
                localctx = simpleParser.Well_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 82
                self.match(simpleParser.T__10)
                self.state = 83
                self.match(simpleParser.T__11)
                self.state = 84
                localctx.which = self.expr(9)
                pass

            elif la_ == 7:
                localctx = simpleParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 85
                self.match(simpleParser.T__12)
                self.state = 86
                _la = self._input.LA(1)
                if not(_la==simpleParser.T__13 or _la==simpleParser.T__14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 87
                localctx.loc = self.expr(8)
                pass

            elif la_ == 8:
                localctx = simpleParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 88
                self.macro_def()
                pass

            elif la_ == 9:
                localctx = simpleParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 89
                self.param_type()
                self.state = 91
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
                if la_ == 1:
                    self.state = 90
                    localctx.n = self.match(simpleParser.INT)


                pass

            elif la_ == 10:
                localctx = simpleParser.Function_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 93
                self.name()
                self.state = 94
                self.match(simpleParser.T__4)
                self.state = 95
                localctx._expr = self.expr(0)
                localctx.args.append(localctx._expr)
                self.state = 100
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==simpleParser.T__6:
                    self.state = 96
                    self.match(simpleParser.T__6)
                    self.state = 97
                    localctx._expr = self.expr(0)
                    localctx.args.append(localctx._expr)
                    self.state = 102
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 103
                self.match(simpleParser.T__5)
                pass

            elif la_ == 11:
                localctx = simpleParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 105
                self.name()
                pass

            elif la_ == 12:
                localctx = simpleParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 106
                self.match(simpleParser.INT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 130
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 128
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
                    if la_ == 1:
                        localctx = simpleParser.Muldiv_exprContext(self, simpleParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 109
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 110
                        _la = self._input.LA(1)
                        if not(_la==simpleParser.DIV or _la==simpleParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 111
                        localctx.rhs = self.expr(14)
                        pass

                    elif la_ == 2:
                        localctx = simpleParser.Addsub_exprContext(self, simpleParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 112
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 113
                        _la = self._input.LA(1)
                        if not(_la==simpleParser.ADD or _la==simpleParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 114
                        localctx.rhs = self.expr(13)
                        pass

                    elif la_ == 3:
                        localctx = simpleParser.Injection_exprContext(self, simpleParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 115
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 116
                        self.match(simpleParser.INJECT)
                        self.state = 117
                        localctx.what = self.expr(7)
                        pass

                    elif la_ == 4:
                        localctx = simpleParser.Index_exprContext(self, simpleParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 118
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 119
                        self.match(simpleParser.T__7)
                        self.state = 120
                        localctx.which = self.expr(0)
                        self.state = 121
                        self.match(simpleParser.T__8)
                        pass

                    elif la_ == 5:
                        localctx = simpleParser.Delta_exprContext(self, simpleParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 123
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 124
                        self.direction()
                        pass

                    elif la_ == 6:
                        localctx = simpleParser.Gate_exprContext(self, simpleParser.ExprContext(self, _parentctx, _parentState))
                        localctx.well = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 125
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 126
                        self.match(simpleParser.ATTR)
                        self.state = 127
                        self.match(simpleParser.T__15)
                        pass

             
                self.state = 132
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class DirectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.d = None
            self.verticalp = None


        def getRuleIndex(self):
            return simpleParser.RULE_direction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirection" ):
                listener.enterDirection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirection" ):
                listener.exitDirection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDirection" ):
                return visitor.visitDirection(self)
            else:
                return visitor.visitChildren(self)




    def direction(self):

        localctx = simpleParser.DirectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_direction)
        self._la = 0 # Token type
        try:
            self.state = 145
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [simpleParser.T__16, simpleParser.T__17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 133
                _la = self._input.LA(1)
                if not(_la==simpleParser.T__16 or _la==simpleParser.T__17):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [simpleParser.T__18, simpleParser.T__19]:
                self.enterOuterAlt(localctx, 2)
                self.state = 136
                _la = self._input.LA(1)
                if not(_la==simpleParser.T__18 or _la==simpleParser.T__19):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [simpleParser.T__20, simpleParser.T__21]:
                self.enterOuterAlt(localctx, 3)
                self.state = 139
                _la = self._input.LA(1)
                if not(_la==simpleParser.T__20 or _la==simpleParser.T__21):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [simpleParser.T__22, simpleParser.T__23]:
                self.enterOuterAlt(localctx, 4)
                self.state = 142
                _la = self._input.LA(1)
                if not(_la==simpleParser.T__22 or _la==simpleParser.T__23):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AxisContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.verticalp = None


        def getRuleIndex(self):
            return simpleParser.RULE_axis

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAxis" ):
                listener.enterAxis(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAxis" ):
                listener.exitAxis(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAxis" ):
                return visitor.visitAxis(self)
            else:
                return visitor.visitChildren(self)




    def axis(self):

        localctx = simpleParser.AxisContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_axis)
        self._la = 0 # Token type
        try:
            self.state = 151
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [simpleParser.T__24]:
                self.enterOuterAlt(localctx, 1)
                self.state = 147
                self.match(simpleParser.T__24)
                localctx.verticalp=True
                pass
            elif token in [simpleParser.T__25, simpleParser.T__26]:
                self.enterOuterAlt(localctx, 2)
                self.state = 149
                _la = self._input.LA(1)
                if not(_la==simpleParser.T__25 or _la==simpleParser.T__26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.verticalp=False
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Macro_defContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def compound(self):
            return self.getTypedRuleContext(simpleParser.CompoundContext,0)


        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simpleParser.ParamContext)
            else:
                return self.getTypedRuleContext(simpleParser.ParamContext,i)


        def getRuleIndex(self):
            return simpleParser.RULE_macro_def

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacro_def" ):
                listener.enterMacro_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacro_def" ):
                listener.exitMacro_def(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacro_def" ):
                return visitor.visitMacro_def(self)
            else:
                return visitor.visitChildren(self)




    def macro_def(self):

        localctx = simpleParser.Macro_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_macro_def)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153
            self.match(simpleParser.T__27)
            self.state = 154
            self.match(simpleParser.T__4)
            self.state = 163
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << simpleParser.T__10) | (1 << simpleParser.T__12) | (1 << simpleParser.T__28) | (1 << simpleParser.T__29) | (1 << simpleParser.ID))) != 0):
                self.state = 155
                self.param()
                self.state = 160
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==simpleParser.T__6:
                    self.state = 156
                    self.match(simpleParser.T__6)
                    self.state = 157
                    self.param()
                    self.state = 162
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 165
            self.match(simpleParser.T__5)
            self.state = 166
            self.compound()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.type = None
            self.pname = None
            self.n = None
            self._param_type = None # Param_typeContext
            self._INT = None # Token
            self._name = None # NameContext

        def param_type(self):
            return self.getTypedRuleContext(simpleParser.Param_typeContext,0)


        def INT(self):
            return self.getToken(simpleParser.INT, 0)

        def name(self):
            return self.getTypedRuleContext(simpleParser.NameContext,0)


        def INJECT(self):
            return self.getToken(simpleParser.INJECT, 0)

        def getRuleIndex(self):
            return simpleParser.RULE_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam" ):
                listener.enterParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam" ):
                listener.exitParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = simpleParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.state = 180
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [simpleParser.T__10, simpleParser.T__12, simpleParser.T__28]:
                self.enterOuterAlt(localctx, 1)
                self.state = 168
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 172
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==simpleParser.INT:
                    self.state = 170
                    localctx._INT = self.match(simpleParser.INT)
                    localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))


                pass
            elif token in [simpleParser.T__29, simpleParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 174
                localctx._name = self.name()
                self.state = 175
                self.match(simpleParser.INJECT)
                self.state = 176
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Param_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.type = None


        def getRuleIndex(self):
            return simpleParser.RULE_param_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam_type" ):
                listener.enterParam_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam_type" ):
                listener.exitParam_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam_type" ):
                return visitor.visitParam_type(self)
            else:
                return visitor.visitChildren(self)




    def param_type(self):

        localctx = simpleParser.Param_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_param_type)
        try:
            self.state = 188
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [simpleParser.T__12]:
                self.enterOuterAlt(localctx, 1)
                self.state = 182
                self.match(simpleParser.T__12)
                localctx.type=Type.DROP
                pass
            elif token in [simpleParser.T__10]:
                self.enterOuterAlt(localctx, 2)
                self.state = 184
                self.match(simpleParser.T__10)
                localctx.type=Type.WELL
                pass
            elif token in [simpleParser.T__28]:
                self.enterOuterAlt(localctx, 3)
                self.state = 186
                self.match(simpleParser.T__28)
                localctx.type=Type.INT
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(simpleParser.ID, 0)

        def kwd_names(self):
            return self.getTypedRuleContext(simpleParser.Kwd_namesContext,0)


        def getRuleIndex(self):
            return simpleParser.RULE_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterName" ):
                listener.enterName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitName" ):
                listener.exitName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitName" ):
                return visitor.visitName(self)
            else:
                return visitor.visitChildren(self)




    def name(self):

        localctx = simpleParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [simpleParser.ID]:
                self.state = 190
                self.match(simpleParser.ID)
                pass
            elif token in [simpleParser.T__29]:
                self.state = 191
                self.kwd_names()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Kwd_namesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return simpleParser.RULE_kwd_names

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKwd_names" ):
                listener.enterKwd_names(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKwd_names" ):
                listener.exitKwd_names(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKwd_names" ):
                return visitor.visitKwd_names(self)
            else:
                return visitor.visitChildren(self)




    def kwd_names(self):

        localctx = simpleParser.Kwd_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_kwd_names)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self.match(simpleParser.T__29)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[4] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 7)
         




