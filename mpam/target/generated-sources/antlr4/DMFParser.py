# Generated from DMF.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


from mpam.types import Dir, OnOff
from langsup.type_supp import Type


from mpam.types import Dir 


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\64")
        buf.write("\u00fc\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\3\2\7\2$\n\2\f\2\16")
        buf.write("\2\'\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\5\3\67\n\3\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3")
        buf.write("\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6I\n\6\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7")
        buf.write("Z\n\7\3\b\3\b\7\b^\n\b\f\b\16\ba\13\b\3\b\3\b\3\b\7\b")
        buf.write("f\n\b\f\b\16\bi\13\b\3\b\5\bl\n\b\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3")
        buf.write("\t\5\t\u0081\n\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3")
        buf.write("\t\5\t\u008d\n\t\3\t\3\t\3\t\3\t\3\t\7\t\u0094\n\t\f\t")
        buf.write("\16\t\u0097\13\t\3\t\3\t\3\t\3\t\5\t\u009d\n\t\3\t\3\t")
        buf.write("\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3")
        buf.write("\t\3\t\3\t\3\t\7\t\u00b2\n\t\f\t\16\t\u00b5\13\t\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u00c3\n")
        buf.write("\n\3\13\3\13\3\13\3\13\5\13\u00c9\n\13\3\f\3\f\3\f\5\f")
        buf.write("\u00ce\n\f\3\r\3\r\3\r\3\r\3\r\7\r\u00d5\n\r\f\r\16\r")
        buf.write("\u00d8\13\r\5\r\u00da\n\r\3\r\3\r\3\16\3\16\3\16\3\16")
        buf.write("\5\16\u00e2\n\16\3\16\3\16\3\16\3\16\3\16\3\16\5\16\u00ea")
        buf.write("\n\16\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\5\17\u00f4")
        buf.write("\n\17\3\20\3\20\5\20\u00f8\n\20\3\21\3\21\3\21\2\3\20")
        buf.write("\22\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \2\13\3\2)")
        buf.write("*\3\2\21\22\4\2&&((\4\2##++\3\2\24\25\3\2\26\27\3\2\30")
        buf.write("\31\3\2\32\33\3\2\35\36\2\u0119\2%\3\2\2\2\4\66\3\2\2")
        buf.write("\2\68\3\2\2\2\b;\3\2\2\2\nH\3\2\2\2\fY\3\2\2\2\16k\3\2")
        buf.write("\2\2\20\u009c\3\2\2\2\22\u00c2\3\2\2\2\24\u00c8\3\2\2")
        buf.write("\2\26\u00ca\3\2\2\2\30\u00cf\3\2\2\2\32\u00e9\3\2\2\2")
        buf.write("\34\u00f3\3\2\2\2\36\u00f7\3\2\2\2 \u00f9\3\2\2\2\"$\5")
        buf.write("\6\4\2#\"\3\2\2\2$\'\3\2\2\2%#\3\2\2\2%&\3\2\2\2&(\3\2")
        buf.write("\2\2\'%\3\2\2\2()\7\2\2\3)\3\3\2\2\2*+\5\16\b\2+,\7\2")
        buf.write("\2\3,\67\3\2\2\2-.\5\b\5\2./\7\2\2\3/\67\3\2\2\2\60\61")
        buf.write("\5\20\t\2\61\62\7\2\2\3\62\67\3\2\2\2\63\64\5\n\6\2\64")
        buf.write("\65\7\2\2\3\65\67\3\2\2\2\66*\3\2\2\2\66-\3\2\2\2\66\60")
        buf.write("\3\2\2\2\66\63\3\2\2\2\67\5\3\2\2\289\5\b\5\29:\7,\2\2")
        buf.write(":\7\3\2\2\2;<\5\36\20\2<=\7$\2\2=>\5\20\t\2>\t\3\2\2\2")
        buf.write("?@\7\3\2\2@A\5\20\t\2AB\t\2\2\2BI\3\2\2\2CD\7\3\2\2DE")
        buf.write("\t\2\2\2EI\5\20\t\2FG\7-\2\2GI\5\20\t\2H?\3\2\2\2HC\3")
        buf.write("\2\2\2HF\3\2\2\2I\13\3\2\2\2JK\5\b\5\2KL\7,\2\2LZ\3\2")
        buf.write("\2\2MN\5\36\20\2NO\7$\2\2OP\5\30\r\2PQ\5\16\b\2QZ\3\2")
        buf.write("\2\2RS\5\n\6\2ST\7,\2\2TZ\3\2\2\2UV\5\20\t\2VW\7,\2\2")
        buf.write("WZ\3\2\2\2XZ\5\16\b\2YJ\3\2\2\2YM\3\2\2\2YR\3\2\2\2YU")
        buf.write("\3\2\2\2YX\3\2\2\2Z\r\3\2\2\2[_\7\4\2\2\\^\5\f\7\2]\\")
        buf.write("\3\2\2\2^a\3\2\2\2_]\3\2\2\2_`\3\2\2\2`b\3\2\2\2a_\3\2")
        buf.write("\2\2bl\7\5\2\2cg\7\6\2\2df\5\f\7\2ed\3\2\2\2fi\3\2\2\2")
        buf.write("ge\3\2\2\2gh\3\2\2\2hj\3\2\2\2ig\3\2\2\2jl\7\7\2\2k[\3")
        buf.write("\2\2\2kc\3\2\2\2l\17\3\2\2\2mn\b\t\1\2no\7\b\2\2op\5\20")
        buf.write("\t\2pq\7\t\2\2qr\b\t\1\2r\u009d\3\2\2\2st\7\b\2\2tu\5")
        buf.write("\20\t\2uv\7\n\2\2vw\5\20\t\2wx\7\t\2\2x\u009d\3\2\2\2")
        buf.write("yz\7+\2\2z\u009d\5\20\t\22{|\5\22\n\2|}\5\20\t\r}\u009d")
        buf.write("\3\2\2\2~\u0080\7\r\2\2\177\u0081\5\24\13\2\u0080\177")
        buf.write("\3\2\2\2\u0080\u0081\3\2\2\2\u0081\u0082\3\2\2\2\u0082")
        buf.write("\u009d\5\20\t\f\u0083\u0084\7\16\2\2\u0084\u0085\7\17")
        buf.write("\2\2\u0085\u009d\5\20\t\13\u0086\u0087\7\20\2\2\u0087")
        buf.write("\u0088\t\3\2\2\u0088\u009d\5\20\t\n\u0089\u009d\5\26\f")
        buf.write("\2\u008a\u008c\5\34\17\2\u008b\u008d\7/\2\2\u008c\u008b")
        buf.write("\3\2\2\2\u008c\u008d\3\2\2\2\u008d\u009d\3\2\2\2\u008e")
        buf.write("\u008f\5\36\20\2\u008f\u0090\7\b\2\2\u0090\u0095\5\20")
        buf.write("\t\2\u0091\u0092\7\n\2\2\u0092\u0094\5\20\t\2\u0093\u0091")
        buf.write("\3\2\2\2\u0094\u0097\3\2\2\2\u0095\u0093\3\2\2\2\u0095")
        buf.write("\u0096\3\2\2\2\u0096\u0098\3\2\2\2\u0097\u0095\3\2\2\2")
        buf.write("\u0098\u0099\7\t\2\2\u0099\u009d\3\2\2\2\u009a\u009d\5")
        buf.write("\36\20\2\u009b\u009d\7/\2\2\u009cm\3\2\2\2\u009cs\3\2")
        buf.write("\2\2\u009cy\3\2\2\2\u009c{\3\2\2\2\u009c~\3\2\2\2\u009c")
        buf.write("\u0083\3\2\2\2\u009c\u0086\3\2\2\2\u009c\u0089\3\2\2\2")
        buf.write("\u009c\u008a\3\2\2\2\u009c\u008e\3\2\2\2\u009c\u009a\3")
        buf.write("\2\2\2\u009c\u009b\3\2\2\2\u009d\u00b3\3\2\2\2\u009e\u009f")
        buf.write("\f\17\2\2\u009f\u00a0\t\4\2\2\u00a0\u00b2\5\20\t\20\u00a1")
        buf.write("\u00a2\f\16\2\2\u00a2\u00a3\t\5\2\2\u00a3\u00b2\5\20\t")
        buf.write("\17\u00a4\u00a5\f\b\2\2\u00a5\u00a6\7\'\2\2\u00a6\u00b2")
        buf.write("\5\20\t\t\u00a7\u00a8\f\21\2\2\u00a8\u00a9\7\13\2\2\u00a9")
        buf.write("\u00aa\5\20\t\2\u00aa\u00ab\7\f\2\2\u00ab\u00b2\3\2\2")
        buf.write("\2\u00ac\u00ad\f\20\2\2\u00ad\u00b2\5\22\n\2\u00ae\u00af")
        buf.write("\f\t\2\2\u00af\u00b0\7%\2\2\u00b0\u00b2\7\23\2\2\u00b1")
        buf.write("\u009e\3\2\2\2\u00b1\u00a1\3\2\2\2\u00b1\u00a4\3\2\2\2")
        buf.write("\u00b1\u00a7\3\2\2\2\u00b1\u00ac\3\2\2\2\u00b1\u00ae\3")
        buf.write("\2\2\2\u00b2\u00b5\3\2\2\2\u00b3\u00b1\3\2\2\2\u00b3\u00b4")
        buf.write("\3\2\2\2\u00b4\21\3\2\2\2\u00b5\u00b3\3\2\2\2\u00b6\u00b7")
        buf.write("\t\6\2\2\u00b7\u00b8\b\n\1\2\u00b8\u00c3\b\n\1\2\u00b9")
        buf.write("\u00ba\t\7\2\2\u00ba\u00bb\b\n\1\2\u00bb\u00c3\b\n\1\2")
        buf.write("\u00bc\u00bd\t\b\2\2\u00bd\u00be\b\n\1\2\u00be\u00c3\b")
        buf.write("\n\1\2\u00bf\u00c0\t\t\2\2\u00c0\u00c1\b\n\1\2\u00c1\u00c3")
        buf.write("\b\n\1\2\u00c2\u00b6\3\2\2\2\u00c2\u00b9\3\2\2\2\u00c2")
        buf.write("\u00bc\3\2\2\2\u00c2\u00bf\3\2\2\2\u00c3\23\3\2\2\2\u00c4")
        buf.write("\u00c5\7\34\2\2\u00c5\u00c9\b\13\1\2\u00c6\u00c7\t\n\2")
        buf.write("\2\u00c7\u00c9\b\13\1\2\u00c8\u00c4\3\2\2\2\u00c8\u00c6")
        buf.write("\3\2\2\2\u00c9\25\3\2\2\2\u00ca\u00cd\5\30\r\2\u00cb\u00ce")
        buf.write("\5\16\b\2\u00cc\u00ce\5\20\t\2\u00cd\u00cb\3\2\2\2\u00cd")
        buf.write("\u00cc\3\2\2\2\u00ce\27\3\2\2\2\u00cf\u00d0\7\37\2\2\u00d0")
        buf.write("\u00d9\7\b\2\2\u00d1\u00d6\5\32\16\2\u00d2\u00d3\7\n\2")
        buf.write("\2\u00d3\u00d5\5\32\16\2\u00d4\u00d2\3\2\2\2\u00d5\u00d8")
        buf.write("\3\2\2\2\u00d6\u00d4\3\2\2\2\u00d6\u00d7\3\2\2\2\u00d7")
        buf.write("\u00da\3\2\2\2\u00d8\u00d6\3\2\2\2\u00d9\u00d1\3\2\2\2")
        buf.write("\u00d9\u00da\3\2\2\2\u00da\u00db\3\2\2\2\u00db\u00dc\7")
        buf.write("\t\2\2\u00dc\31\3\2\2\2\u00dd\u00de\5\34\17\2\u00de\u00e1")
        buf.write("\b\16\1\2\u00df\u00e0\7/\2\2\u00e0\u00e2\b\16\1\2\u00e1")
        buf.write("\u00df\3\2\2\2\u00e1\u00e2\3\2\2\2\u00e2\u00ea\3\2\2\2")
        buf.write("\u00e3\u00e4\5\36\20\2\u00e4\u00e5\7\'\2\2\u00e5\u00e6")
        buf.write("\5\34\17\2\u00e6\u00e7\b\16\1\2\u00e7\u00e8\b\16\1\2\u00e8")
        buf.write("\u00ea\3\2\2\2\u00e9\u00dd\3\2\2\2\u00e9\u00e3\3\2\2\2")
        buf.write("\u00ea\33\3\2\2\2\u00eb\u00ec\7\20\2\2\u00ec\u00f4\b\17")
        buf.write("\1\2\u00ed\u00ee\7 \2\2\u00ee\u00f4\b\17\1\2\u00ef\u00f0")
        buf.write("\7\16\2\2\u00f0\u00f4\b\17\1\2\u00f1\u00f2\7!\2\2\u00f2")
        buf.write("\u00f4\b\17\1\2\u00f3\u00eb\3\2\2\2\u00f3\u00ed\3\2\2")
        buf.write("\2\u00f3\u00ef\3\2\2\2\u00f3\u00f1\3\2\2\2\u00f4\35\3")
        buf.write("\2\2\2\u00f5\u00f8\7.\2\2\u00f6\u00f8\5 \21\2\u00f7\u00f5")
        buf.write("\3\2\2\2\u00f7\u00f6\3\2\2\2\u00f8\37\3\2\2\2\u00f9\u00fa")
        buf.write("\7\"\2\2\u00fa!\3\2\2\2\30%\66HY_gk\u0080\u008c\u0095")
        buf.write("\u009c\u00b1\u00b3\u00c2\u00c8\u00cd\u00d6\u00d9\u00e1")
        buf.write("\u00e9\u00f3\u00f7")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'turn'", "'{'", "'}'", "'[['", "']]'", 
                     "'('", "')'", "','", "'['", "']'", "'to'", "'well'", 
                     "'#'", "'drop'", "'@'", "'at'", "'gate'", "'up'", "'north'", 
                     "'down'", "'south'", "'left'", "'west'", "'right'", 
                     "'east'", "'row'", "'col'", "'column'", "'macro'", 
                     "'pad'", "'int'", "'**__**'", "'+'", "'='", "''s'", 
                     "'/'", "':'", "'*'", "'off'", "'on'", "'-'", "';'", 
                     "'toggle'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "ADD", "ASSIGN", "ATTR", "DIV", "INJECT", 
                      "MUL", "OFF", "ON", "SUB", "TERMINATOR", "TOGGLE", 
                      "ID", "INT", "FLOAT", "STRING", "EOL_COMMENT", "COMMENT", 
                      "WS" ]

    RULE_macro_file = 0
    RULE_interactive = 1
    RULE_top_level_stat = 2
    RULE_assignment = 3
    RULE_pad_op = 4
    RULE_stat = 5
    RULE_compound = 6
    RULE_expr = 7
    RULE_direction = 8
    RULE_axis = 9
    RULE_macro_def = 10
    RULE_macro_header = 11
    RULE_param = 12
    RULE_param_type = 13
    RULE_name = 14
    RULE_kwd_names = 15

    ruleNames =  [ "macro_file", "interactive", "top_level_stat", "assignment", 
                   "pad_op", "stat", "compound", "expr", "direction", "axis", 
                   "macro_def", "macro_header", "param", "param_type", "name", 
                   "kwd_names" ]

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
    T__30=31
    T__31=32
    ADD=33
    ASSIGN=34
    ATTR=35
    DIV=36
    INJECT=37
    MUL=38
    OFF=39
    ON=40
    SUB=41
    TERMINATOR=42
    TOGGLE=43
    ID=44
    INT=45
    FLOAT=46
    STRING=47
    EOL_COMMENT=48
    COMMENT=49
    WS=50

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
            return self.getToken(DMFParser.EOF, 0)

        def top_level_stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.Top_level_statContext)
            else:
                return self.getTypedRuleContext(DMFParser.Top_level_statContext,i)


        def getRuleIndex(self):
            return DMFParser.RULE_macro_file

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

        localctx = DMFParser.Macro_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_macro_file)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DMFParser.T__31 or _la==DMFParser.ID:
                self.state = 32
                self.top_level_stat()
                self.state = 37
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 38
            self.match(DMFParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InteractiveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return DMFParser.RULE_interactive

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Compound_interactiveContext(InteractiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.InteractiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def compound(self):
            return self.getTypedRuleContext(DMFParser.CompoundContext,0)

        def EOF(self):
            return self.getToken(DMFParser.EOF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompound_interactive" ):
                listener.enterCompound_interactive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompound_interactive" ):
                listener.exitCompound_interactive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompound_interactive" ):
                return visitor.visitCompound_interactive(self)
            else:
                return visitor.visitChildren(self)


    class Assignment_interactiveContext(InteractiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.InteractiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def assignment(self):
            return self.getTypedRuleContext(DMFParser.AssignmentContext,0)

        def EOF(self):
            return self.getToken(DMFParser.EOF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment_interactive" ):
                listener.enterAssignment_interactive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment_interactive" ):
                listener.exitAssignment_interactive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment_interactive" ):
                return visitor.visitAssignment_interactive(self)
            else:
                return visitor.visitChildren(self)


    class Expr_interactiveContext(InteractiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.InteractiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)

        def EOF(self):
            return self.getToken(DMFParser.EOF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr_interactive" ):
                listener.enterExpr_interactive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr_interactive" ):
                listener.exitExpr_interactive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr_interactive" ):
                return visitor.visitExpr_interactive(self)
            else:
                return visitor.visitChildren(self)


    class Pad_op_interactiveContext(InteractiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.InteractiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def pad_op(self):
            return self.getTypedRuleContext(DMFParser.Pad_opContext,0)

        def EOF(self):
            return self.getToken(DMFParser.EOF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPad_op_interactive" ):
                listener.enterPad_op_interactive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPad_op_interactive" ):
                listener.exitPad_op_interactive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPad_op_interactive" ):
                return visitor.visitPad_op_interactive(self)
            else:
                return visitor.visitChildren(self)



    def interactive(self):

        localctx = DMFParser.InteractiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_interactive)
        try:
            self.state = 52
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 40
                self.compound()
                self.state = 41
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Assignment_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 43
                self.assignment()
                self.state = 44
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 46
                self.expr(0)
                self.state = 47
                self.match(DMFParser.EOF)
                pass

            elif la_ == 4:
                localctx = DMFParser.Pad_op_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 49
                self.pad_op()
                self.state = 50
                self.match(DMFParser.EOF)
                pass


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

        def assignment(self):
            return self.getTypedRuleContext(DMFParser.AssignmentContext,0)


        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_top_level_stat

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTop_level_stat" ):
                listener.enterTop_level_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTop_level_stat" ):
                listener.exitTop_level_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTop_level_stat" ):
                return visitor.visitTop_level_stat(self)
            else:
                return visitor.visitChildren(self)




    def top_level_stat(self):

        localctx = DMFParser.Top_level_statContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_top_level_stat)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.assignment()
            self.state = 55
            self.match(DMFParser.TERMINATOR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.which = None # NameContext
            self.what = None # ExprContext

        def ASSIGN(self):
            return self.getToken(DMFParser.ASSIGN, 0)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)


        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def getRuleIndex(self):
            return DMFParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = DMFParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            localctx.which = self.name()
            self.state = 58
            self.match(DMFParser.ASSIGN)
            self.state = 59
            localctx.what = self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pad_opContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.which = None # ExprContext

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def ON(self):
            return self.getToken(DMFParser.ON, 0)

        def OFF(self):
            return self.getToken(DMFParser.OFF, 0)

        def TOGGLE(self):
            return self.getToken(DMFParser.TOGGLE, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_pad_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPad_op" ):
                listener.enterPad_op(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPad_op" ):
                listener.exitPad_op(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPad_op" ):
                return visitor.visitPad_op(self)
            else:
                return visitor.visitChildren(self)




    def pad_op(self):

        localctx = DMFParser.Pad_opContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_pad_op)
        self._la = 0 # Token type
        try:
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 61
                self.match(DMFParser.T__0)
                self.state = 62
                localctx.which = self.expr(0)
                self.state = 63
                _la = self._input.LA(1)
                if not(_la==DMFParser.OFF or _la==DMFParser.ON):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 65
                self.match(DMFParser.T__0)
                self.state = 66
                _la = self._input.LA(1)
                if not(_la==DMFParser.OFF or _la==DMFParser.ON):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 67
                localctx.which = self.expr(0)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 68
                self.match(DMFParser.TOGGLE)
                self.state = 69
                localctx.which = self.expr(0)
                pass


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


        def getRuleIndex(self):
            return DMFParser.RULE_stat

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Expr_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)

        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr_stat" ):
                listener.enterExpr_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr_stat" ):
                listener.exitExpr_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr_stat" ):
                return visitor.visitExpr_stat(self)
            else:
                return visitor.visitChildren(self)


    class Assign_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def assignment(self):
            return self.getTypedRuleContext(DMFParser.AssignmentContext,0)

        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

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


    class Compound_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def compound(self):
            return self.getTypedRuleContext(DMFParser.CompoundContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompound_stat" ):
                listener.enterCompound_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompound_stat" ):
                listener.exitCompound_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompound_stat" ):
                return visitor.visitCompound_stat(self)
            else:
                return visitor.visitChildren(self)


    class Pad_op_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def pad_op(self):
            return self.getTypedRuleContext(DMFParser.Pad_opContext,0)

        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPad_op_stat" ):
                listener.enterPad_op_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPad_op_stat" ):
                listener.exitPad_op_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPad_op_stat" ):
                return visitor.visitPad_op_stat(self)
            else:
                return visitor.visitChildren(self)


    class Macro_def_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.which = None # NameContext
            self.body = None # CompoundContext
            self.copyFrom(ctx)

        def ASSIGN(self):
            return self.getToken(DMFParser.ASSIGN, 0)
        def macro_header(self):
            return self.getTypedRuleContext(DMFParser.Macro_headerContext,0)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)

        def compound(self):
            return self.getTypedRuleContext(DMFParser.CompoundContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacro_def_stat" ):
                listener.enterMacro_def_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacro_def_stat" ):
                listener.exitMacro_def_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacro_def_stat" ):
                return visitor.visitMacro_def_stat(self)
            else:
                return visitor.visitChildren(self)



    def stat(self):

        localctx = DMFParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_stat)
        try:
            self.state = 87
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Assign_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 72
                self.assignment()
                self.state = 73
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Macro_def_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 75
                localctx.which = self.name()
                self.state = 76
                self.match(DMFParser.ASSIGN)
                self.state = 77
                self.macro_header()
                self.state = 78
                localctx.body = self.compound()
                pass

            elif la_ == 3:
                localctx = DMFParser.Pad_op_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 80
                self.pad_op()
                self.state = 81
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 4:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 83
                self.expr(0)
                self.state = 84
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 5:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 86
                self.compound()
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
            return DMFParser.RULE_compound

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Par_blockContext(CompoundContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.CompoundContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.StatContext)
            else:
                return self.getTypedRuleContext(DMFParser.StatContext,i)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.CompoundContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.StatContext)
            else:
                return self.getTypedRuleContext(DMFParser.StatContext,i)


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

        localctx = DMFParser.CompoundContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_compound)
        self._la = 0 # Token type
        try:
            self.state = 105
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__1]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 89
                self.match(DMFParser.T__1)
                self.state = 93
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__10) | (1 << DMFParser.T__11) | (1 << DMFParser.T__13) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__19) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                    self.state = 90
                    self.stat()
                    self.state = 95
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 96
                self.match(DMFParser.T__2)
                pass
            elif token in [DMFParser.T__3]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 97
                self.match(DMFParser.T__3)
                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__10) | (1 << DMFParser.T__11) | (1 << DMFParser.T__13) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__19) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                    self.state = 98
                    self.stat()
                    self.state = 103
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 104
                self.match(DMFParser.T__4)
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
            self.has_side_effect = False


        def getRuleIndex(self):
            return DMFParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)
            self.has_side_effect = ctx.has_side_effect


    class Paren_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.rhs = None # ExprContext
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def SUB(self):
            return self.getToken(DMFParser.SUB, 0)
        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(DMFParser.INT, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.n = None # Token
            self.copyFrom(ctx)

        def param_type(self):
            return self.getTypedRuleContext(DMFParser.Param_typeContext,0)

        def INT(self):
            return self.getToken(DMFParser.INT, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.who = None # ExprContext
            self.which = None # ExprContext
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def macro_def(self):
            return self.getTypedRuleContext(DMFParser.Macro_defContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.lhs = None # ExprContext
            self.rhs = None # ExprContext
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)

        def ADD(self):
            return self.getToken(DMFParser.ADD, 0)
        def SUB(self):
            return self.getToken(DMFParser.SUB, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.dist = None # ExprContext
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def direction(self):
            return self.getTypedRuleContext(DMFParser.DirectionContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.x = None # ExprContext
            self._expr = None # ExprContext
            self.y = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.who = None # ExprContext
            self.what = None # ExprContext
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def INJECT(self):
            return self.getToken(DMFParser.INJECT, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.well = None # ExprContext
            self.copyFrom(ctx)

        def ATTR(self):
            return self.getToken(DMFParser.ATTR, 0)
        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.which = None # ExprContext
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.loc = None # ExprContext
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self._expr = None # ExprContext
            self.args = list() # of ExprContexts
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.which = None # ExprContext
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)

        def axis(self):
            return self.getTypedRuleContext(DMFParser.AxisContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.lhs = None # ExprContext
            self.rhs = None # ExprContext
            self._expr = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)

        def MUL(self):
            return self.getToken(DMFParser.MUL, 0)
        def DIV(self):
            return self.getToken(DMFParser.DIV, 0)

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
        localctx = DMFParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 14
        self.enterRecursionRule(localctx, 14, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 108
                self.match(DMFParser.T__5)
                self.state = 109
                localctx._expr = self.expr(0)
                self.state = 110
                self.match(DMFParser.T__6)
                localctx.has_side_effect=localctx._expr.has_side_effect
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 113
                self.match(DMFParser.T__5)
                self.state = 114
                localctx.x = localctx._expr = self.expr(0)
                self.state = 115
                self.match(DMFParser.T__7)
                self.state = 116
                localctx.y = localctx._expr = self.expr(0)
                self.state = 117
                self.match(DMFParser.T__6)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 119
                self.match(DMFParser.SUB)
                self.state = 120
                localctx.rhs = localctx._expr = self.expr(16)
                pass

            elif la_ == 4:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 121
                self.direction()
                self.state = 122
                localctx.dist = localctx._expr = self.expr(11)
                pass

            elif la_ == 5:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 124
                self.match(DMFParser.T__10)
                self.state = 126
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27))) != 0):
                    self.state = 125
                    self.axis()


                self.state = 128
                localctx.which = localctx._expr = self.expr(10)
                pass

            elif la_ == 6:
                localctx = DMFParser.Well_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 129
                self.match(DMFParser.T__11)
                self.state = 130
                self.match(DMFParser.T__12)
                self.state = 131
                localctx.which = localctx._expr = self.expr(9)
                pass

            elif la_ == 7:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 132
                self.match(DMFParser.T__13)
                self.state = 133
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__14 or _la==DMFParser.T__15):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 134
                localctx.loc = localctx._expr = self.expr(8)
                pass

            elif la_ == 8:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 135
                self.macro_def()
                pass

            elif la_ == 9:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 136
                self.param_type()
                self.state = 138
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                if la_ == 1:
                    self.state = 137
                    localctx.n = self.match(DMFParser.INT)


                pass

            elif la_ == 10:
                localctx = DMFParser.Function_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 140
                self.name()
                self.state = 141
                self.match(DMFParser.T__5)
                self.state = 142
                localctx._expr = localctx._expr = self.expr(0)
                localctx.args.append(localctx._expr)
                self.state = 147
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__7:
                    self.state = 143
                    self.match(DMFParser.T__7)
                    self.state = 144
                    localctx._expr = localctx._expr = self.expr(0)
                    localctx.args.append(localctx._expr)
                    self.state = 149
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 150
                self.match(DMFParser.T__6)
                pass

            elif la_ == 11:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 152
                self.name()
                pass

            elif la_ == 12:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 153
                self.match(DMFParser.INT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 177
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 175
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 156
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 157
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 158
                        localctx.rhs = localctx._expr = self.expr(14)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 159
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 160
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 161
                        localctx.rhs = localctx._expr = self.expr(13)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 162
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 163
                        self.match(DMFParser.INJECT)
                        self.state = 164
                        localctx.what = localctx._expr = self.expr(7)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 165
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 166
                        self.match(DMFParser.T__8)
                        self.state = 167
                        localctx.which = localctx._expr = self.expr(0)
                        self.state = 168
                        self.match(DMFParser.T__9)
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 170
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 171
                        self.direction()
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Gate_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.well = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 172
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 173
                        self.match(DMFParser.ATTR)
                        self.state = 174
                        self.match(DMFParser.T__16)
                        pass

             
                self.state = 179
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

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
            return DMFParser.RULE_direction

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

        localctx = DMFParser.DirectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_direction)
        self._la = 0 # Token type
        try:
            self.state = 192
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__17, DMFParser.T__18]:
                self.enterOuterAlt(localctx, 1)
                self.state = 180
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__17 or _la==DMFParser.T__18):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__19, DMFParser.T__20]:
                self.enterOuterAlt(localctx, 2)
                self.state = 183
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__19 or _la==DMFParser.T__20):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__21, DMFParser.T__22]:
                self.enterOuterAlt(localctx, 3)
                self.state = 186
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__21 or _la==DMFParser.T__22):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__23, DMFParser.T__24]:
                self.enterOuterAlt(localctx, 4)
                self.state = 189
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__23 or _la==DMFParser.T__24):
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
            return DMFParser.RULE_axis

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

        localctx = DMFParser.AxisContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_axis)
        self._la = 0 # Token type
        try:
            self.state = 198
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__25]:
                self.enterOuterAlt(localctx, 1)
                self.state = 194
                self.match(DMFParser.T__25)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__26, DMFParser.T__27]:
                self.enterOuterAlt(localctx, 2)
                self.state = 196
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__26 or _la==DMFParser.T__27):
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

        def macro_header(self):
            return self.getTypedRuleContext(DMFParser.Macro_headerContext,0)


        def compound(self):
            return self.getTypedRuleContext(DMFParser.CompoundContext,0)


        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def getRuleIndex(self):
            return DMFParser.RULE_macro_def

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

        localctx = DMFParser.Macro_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_macro_def)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            self.macro_header()
            self.state = 203
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__1, DMFParser.T__3]:
                self.state = 201
                self.compound()
                pass
            elif token in [DMFParser.T__5, DMFParser.T__10, DMFParser.T__11, DMFParser.T__13, DMFParser.T__17, DMFParser.T__18, DMFParser.T__19, DMFParser.T__20, DMFParser.T__21, DMFParser.T__22, DMFParser.T__23, DMFParser.T__24, DMFParser.T__28, DMFParser.T__29, DMFParser.T__30, DMFParser.T__31, DMFParser.SUB, DMFParser.ID, DMFParser.INT]:
                self.state = 202
                self.expr(0)
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


    class Macro_headerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ParamContext)
            else:
                return self.getTypedRuleContext(DMFParser.ParamContext,i)


        def getRuleIndex(self):
            return DMFParser.RULE_macro_header

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMacro_header" ):
                listener.enterMacro_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMacro_header" ):
                listener.exitMacro_header(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMacro_header" ):
                return visitor.visitMacro_header(self)
            else:
                return visitor.visitChildren(self)




    def macro_header(self):

        localctx = DMFParser.Macro_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_macro_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 205
            self.match(DMFParser.T__28)
            self.state = 206
            self.match(DMFParser.T__5)
            self.state = 215
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__11) | (1 << DMFParser.T__13) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.ID))) != 0):
                self.state = 207
                self.param()
                self.state = 212
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__7:
                    self.state = 208
                    self.match(DMFParser.T__7)
                    self.state = 209
                    self.param()
                    self.state = 214
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 217
            self.match(DMFParser.T__6)
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
            return self.getTypedRuleContext(DMFParser.Param_typeContext,0)


        def INT(self):
            return self.getToken(DMFParser.INT, 0)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)


        def INJECT(self):
            return self.getToken(DMFParser.INJECT, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_param

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

        localctx = DMFParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.state = 231
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__11, DMFParser.T__13, DMFParser.T__29, DMFParser.T__30]:
                self.enterOuterAlt(localctx, 1)
                self.state = 219
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 223
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.INT:
                    self.state = 221
                    localctx._INT = self.match(DMFParser.INT)
                    localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))


                pass
            elif token in [DMFParser.T__31, DMFParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 225
                localctx._name = self.name()
                self.state = 226
                self.match(DMFParser.INJECT)
                self.state = 227
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
            return DMFParser.RULE_param_type

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

        localctx = DMFParser.Param_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_param_type)
        try:
            self.state = 241
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__13]:
                self.enterOuterAlt(localctx, 1)
                self.state = 233
                self.match(DMFParser.T__13)
                localctx.type=Type.DROP
                pass
            elif token in [DMFParser.T__29]:
                self.enterOuterAlt(localctx, 2)
                self.state = 235
                self.match(DMFParser.T__29)
                localctx.type=Type.PAD
                pass
            elif token in [DMFParser.T__11]:
                self.enterOuterAlt(localctx, 3)
                self.state = 237
                self.match(DMFParser.T__11)
                localctx.type=Type.WELL
                pass
            elif token in [DMFParser.T__30]:
                self.enterOuterAlt(localctx, 4)
                self.state = 239
                self.match(DMFParser.T__30)
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
            return self.getToken(DMFParser.ID, 0)

        def kwd_names(self):
            return self.getTypedRuleContext(DMFParser.Kwd_namesContext,0)


        def getRuleIndex(self):
            return DMFParser.RULE_name

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

        localctx = DMFParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 245
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.ID]:
                self.state = 243
                self.match(DMFParser.ID)
                pass
            elif token in [DMFParser.T__31]:
                self.state = 244
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
            return DMFParser.RULE_kwd_names

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

        localctx = DMFParser.Kwd_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_kwd_names)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 247
            self.match(DMFParser.T__31)
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
        self._predicates[7] = self.expr_sempred
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
         




