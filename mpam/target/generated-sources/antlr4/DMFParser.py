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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\67")
        buf.write("\u00ef\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\3\2\7\2 \n\2\f\2\16\2#\13\2\3\2\3\2\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3\60\n\3\3\4\3\4")
        buf.write("\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5=\n\5\3\6\3\6")
        buf.write("\7\6A\n\6\f\6\16\6D\13\6\3\6\3\6\3\6\7\6I\n\6\f\6\16\6")
        buf.write("L\13\6\3\6\5\6O\n\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7c\n\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7n\n\7\3\7\3\7\3\7\5")
        buf.write("\7s\n\7\3\7\5\7v\n\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\7\7\u0081\n\7\f\7\16\7\u0084\13\7\5\7\u0086\n\7\3\7")
        buf.write("\3\7\3\7\3\7\5\7\u008c\n\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\7\7\u00a5\n\7\f\7\16\7\u00a8\13\7\3\b\3\b\3")
        buf.write("\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\b\u00b6\n\b\3")
        buf.write("\t\3\t\3\t\3\t\5\t\u00bc\n\t\3\n\3\n\3\n\5\n\u00c1\n\n")
        buf.write("\3\13\3\13\3\13\3\13\3\13\7\13\u00c8\n\13\f\13\16\13\u00cb")
        buf.write("\13\13\5\13\u00cd\n\13\3\13\3\13\3\f\3\f\3\f\3\f\5\f\u00d5")
        buf.write("\n\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f\u00dd\n\f\3\r\3\r\3\r")
        buf.write("\3\r\3\r\3\r\3\r\3\r\5\r\u00e7\n\r\3\16\3\16\5\16\u00eb")
        buf.write("\n\16\3\17\3\17\3\17\2\3\f\20\2\4\6\b\n\f\16\20\22\24")
        buf.write("\26\30\32\34\2\13\3\2\20\21\3\2,-\4\2))++\4\2&&..\3\2")
        buf.write("\30\31\3\2\32\33\3\2\34\35\3\2\36\37\3\2!\"\2\u0110\2")
        buf.write("!\3\2\2\2\4/\3\2\2\2\6\61\3\2\2\2\b<\3\2\2\2\nN\3\2\2")
        buf.write("\2\f\u008b\3\2\2\2\16\u00b5\3\2\2\2\20\u00bb\3\2\2\2\22")
        buf.write("\u00bd\3\2\2\2\24\u00c2\3\2\2\2\26\u00dc\3\2\2\2\30\u00e6")
        buf.write("\3\2\2\2\32\u00ea\3\2\2\2\34\u00ec\3\2\2\2\36 \5\b\5\2")
        buf.write("\37\36\3\2\2\2 #\3\2\2\2!\37\3\2\2\2!\"\3\2\2\2\"$\3\2")
        buf.write("\2\2#!\3\2\2\2$%\7\2\2\3%\3\3\2\2\2&\'\5\n\6\2\'(\7\2")
        buf.write("\2\3(\60\3\2\2\2)*\5\6\4\2*+\7\2\2\3+\60\3\2\2\2,-\5\f")
        buf.write("\7\2-.\7\2\2\3.\60\3\2\2\2/&\3\2\2\2/)\3\2\2\2/,\3\2\2")
        buf.write("\2\60\5\3\2\2\2\61\62\5\32\16\2\62\63\7\'\2\2\63\64\5")
        buf.write("\f\7\2\64\7\3\2\2\2\65\66\5\6\4\2\66\67\7/\2\2\67=\3\2")
        buf.write("\2\289\5\f\7\29:\7/\2\2:=\3\2\2\2;=\5\n\6\2<\65\3\2\2")
        buf.write("\2<8\3\2\2\2<;\3\2\2\2=\t\3\2\2\2>B\7\3\2\2?A\5\b\5\2")
        buf.write("@?\3\2\2\2AD\3\2\2\2B@\3\2\2\2BC\3\2\2\2CE\3\2\2\2DB\3")
        buf.write("\2\2\2EO\7\4\2\2FJ\7\5\2\2GI\5\b\5\2HG\3\2\2\2IL\3\2\2")
        buf.write("\2JH\3\2\2\2JK\3\2\2\2KM\3\2\2\2LJ\3\2\2\2MO\7\6\2\2N")
        buf.write(">\3\2\2\2NF\3\2\2\2O\13\3\2\2\2PQ\b\7\1\2QR\7\7\2\2RS")
        buf.write("\5\f\7\2ST\7\b\2\2T\u008c\3\2\2\2UV\7\7\2\2VW\5\f\7\2")
        buf.write("WX\7\t\2\2XY\5\f\7\2YZ\7\b\2\2Z\u008c\3\2\2\2[\\\7.\2")
        buf.write("\2\\\u008c\5\f\7\26]^\5\16\b\2^_\5\f\7\21_\u008c\3\2\2")
        buf.write("\2`b\7\f\2\2ac\5\20\t\2ba\3\2\2\2bc\3\2\2\2cd\3\2\2\2")
        buf.write("d\u008c\5\f\7\20ef\7\r\2\2fg\7\16\2\2g\u008c\5\f\7\17")
        buf.write("hi\7\17\2\2ij\t\2\2\2j\u008c\5\f\7\16k\u008c\5\22\n\2")
        buf.write("ln\7\25\2\2ml\3\2\2\2mn\3\2\2\2no\3\2\2\2o\u008c\t\3\2")
        buf.write("\2pr\7\60\2\2qs\7\26\2\2rq\3\2\2\2rs\3\2\2\2s\u008c\3")
        buf.write("\2\2\2tv\7\27\2\2ut\3\2\2\2uv\3\2\2\2vw\3\2\2\2w\u008c")
        buf.write("\5\30\r\2xy\5\30\r\2yz\7\62\2\2z\u008c\3\2\2\2{|\5\32")
        buf.write("\16\2|\u0085\7\7\2\2}\u0082\5\f\7\2~\177\7\t\2\2\177\u0081")
        buf.write("\5\f\7\2\u0080~\3\2\2\2\u0081\u0084\3\2\2\2\u0082\u0080")
        buf.write("\3\2\2\2\u0082\u0083\3\2\2\2\u0083\u0086\3\2\2\2\u0084")
        buf.write("\u0082\3\2\2\2\u0085}\3\2\2\2\u0085\u0086\3\2\2\2\u0086")
        buf.write("\u0087\3\2\2\2\u0087\u0088\7\b\2\2\u0088\u008c\3\2\2\2")
        buf.write("\u0089\u008c\5\32\16\2\u008a\u008c\7\62\2\2\u008bP\3\2")
        buf.write("\2\2\u008bU\3\2\2\2\u008b[\3\2\2\2\u008b]\3\2\2\2\u008b")
        buf.write("`\3\2\2\2\u008be\3\2\2\2\u008bh\3\2\2\2\u008bk\3\2\2\2")
        buf.write("\u008bm\3\2\2\2\u008bp\3\2\2\2\u008bu\3\2\2\2\u008bx\3")
        buf.write("\2\2\2\u008b{\3\2\2\2\u008b\u0089\3\2\2\2\u008b\u008a")
        buf.write("\3\2\2\2\u008c\u00a6\3\2\2\2\u008d\u008e\f\23\2\2\u008e")
        buf.write("\u008f\t\4\2\2\u008f\u00a5\5\f\7\24\u0090\u0091\f\22\2")
        buf.write("\2\u0091\u0092\t\5\2\2\u0092\u00a5\5\f\7\23\u0093\u0094")
        buf.write("\f\13\2\2\u0094\u0095\7*\2\2\u0095\u00a5\5\f\7\f\u0096")
        buf.write("\u0097\f\25\2\2\u0097\u0098\7\n\2\2\u0098\u0099\5\f\7")
        buf.write("\2\u0099\u009a\7\13\2\2\u009a\u00a5\3\2\2\2\u009b\u009c")
        buf.write("\f\24\2\2\u009c\u00a5\5\16\b\2\u009d\u009e\f\r\2\2\u009e")
        buf.write("\u009f\7(\2\2\u009f\u00a5\7\22\2\2\u00a0\u00a1\f\f\2\2")
        buf.write("\u00a1\u00a2\7(\2\2\u00a2\u00a3\7\23\2\2\u00a3\u00a5\7")
        buf.write("\24\2\2\u00a4\u008d\3\2\2\2\u00a4\u0090\3\2\2\2\u00a4")
        buf.write("\u0093\3\2\2\2\u00a4\u0096\3\2\2\2\u00a4\u009b\3\2\2\2")
        buf.write("\u00a4\u009d\3\2\2\2\u00a4\u00a0\3\2\2\2\u00a5\u00a8\3")
        buf.write("\2\2\2\u00a6\u00a4\3\2\2\2\u00a6\u00a7\3\2\2\2\u00a7\r")
        buf.write("\3\2\2\2\u00a8\u00a6\3\2\2\2\u00a9\u00aa\t\6\2\2\u00aa")
        buf.write("\u00ab\b\b\1\2\u00ab\u00b6\b\b\1\2\u00ac\u00ad\t\7\2\2")
        buf.write("\u00ad\u00ae\b\b\1\2\u00ae\u00b6\b\b\1\2\u00af\u00b0\t")
        buf.write("\b\2\2\u00b0\u00b1\b\b\1\2\u00b1\u00b6\b\b\1\2\u00b2\u00b3")
        buf.write("\t\t\2\2\u00b3\u00b4\b\b\1\2\u00b4\u00b6\b\b\1\2\u00b5")
        buf.write("\u00a9\3\2\2\2\u00b5\u00ac\3\2\2\2\u00b5\u00af\3\2\2\2")
        buf.write("\u00b5\u00b2\3\2\2\2\u00b6\17\3\2\2\2\u00b7\u00b8\7 \2")
        buf.write("\2\u00b8\u00bc\b\t\1\2\u00b9\u00ba\t\n\2\2\u00ba\u00bc")
        buf.write("\b\t\1\2\u00bb\u00b7\3\2\2\2\u00bb\u00b9\3\2\2\2\u00bc")
        buf.write("\21\3\2\2\2\u00bd\u00c0\5\24\13\2\u00be\u00c1\5\n\6\2")
        buf.write("\u00bf\u00c1\5\f\7\2\u00c0\u00be\3\2\2\2\u00c0\u00bf\3")
        buf.write("\2\2\2\u00c1\23\3\2\2\2\u00c2\u00c3\7#\2\2\u00c3\u00cc")
        buf.write("\7\7\2\2\u00c4\u00c9\5\26\f\2\u00c5\u00c6\7\t\2\2\u00c6")
        buf.write("\u00c8\5\26\f\2\u00c7\u00c5\3\2\2\2\u00c8\u00cb\3\2\2")
        buf.write("\2\u00c9\u00c7\3\2\2\2\u00c9\u00ca\3\2\2\2\u00ca\u00cd")
        buf.write("\3\2\2\2\u00cb\u00c9\3\2\2\2\u00cc\u00c4\3\2\2\2\u00cc")
        buf.write("\u00cd\3\2\2\2\u00cd\u00ce\3\2\2\2\u00ce\u00cf\7\b\2\2")
        buf.write("\u00cf\25\3\2\2\2\u00d0\u00d1\5\30\r\2\u00d1\u00d4\b\f")
        buf.write("\1\2\u00d2\u00d3\7\62\2\2\u00d3\u00d5\b\f\1\2\u00d4\u00d2")
        buf.write("\3\2\2\2\u00d4\u00d5\3\2\2\2\u00d5\u00dd\3\2\2\2\u00d6")
        buf.write("\u00d7\5\32\16\2\u00d7\u00d8\7*\2\2\u00d8\u00d9\5\30\r")
        buf.write("\2\u00d9\u00da\b\f\1\2\u00da\u00db\b\f\1\2\u00db\u00dd")
        buf.write("\3\2\2\2\u00dc\u00d0\3\2\2\2\u00dc\u00d6\3\2\2\2\u00dd")
        buf.write("\27\3\2\2\2\u00de\u00df\7\17\2\2\u00df\u00e7\b\r\1\2\u00e0")
        buf.write("\u00e1\7\24\2\2\u00e1\u00e7\b\r\1\2\u00e2\u00e3\7\r\2")
        buf.write("\2\u00e3\u00e7\b\r\1\2\u00e4\u00e5\7$\2\2\u00e5\u00e7")
        buf.write("\b\r\1\2\u00e6\u00de\3\2\2\2\u00e6\u00e0\3\2\2\2\u00e6")
        buf.write("\u00e2\3\2\2\2\u00e6\u00e4\3\2\2\2\u00e7\31\3\2\2\2\u00e8")
        buf.write("\u00eb\7\61\2\2\u00e9\u00eb\5\34\17\2\u00ea\u00e8\3\2")
        buf.write("\2\2\u00ea\u00e9\3\2\2\2\u00eb\33\3\2\2\2\u00ec\u00ed")
        buf.write("\7%\2\2\u00ed\35\3\2\2\2\32!/<BJNbmru\u0082\u0085\u008b")
        buf.write("\u00a4\u00a6\u00b5\u00bb\u00c0\u00c9\u00cc\u00d4\u00dc")
        buf.write("\u00e6\u00ea")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "'}'", "'[['", "']]'", "'('", "')'", 
                     "','", "'['", "']'", "'to'", "'well'", "'#'", "'drop'", 
                     "'@'", "'at'", "'gate'", "'exit'", "'pad'", "'turn'", 
                     "'state'", "'the'", "'up'", "'north'", "'down'", "'south'", 
                     "'left'", "'west'", "'right'", "'east'", "'row'", "'col'", 
                     "'column'", "'macro'", "'int'", "'**__**'", "'+'", 
                     "'='", "''s'", "'/'", "':'", "'*'", "'off'", "'on'", 
                     "'-'", "';'", "'toggle'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "ADD", "ASSIGN", "ATTR", "DIV", "INJECT", "MUL", "OFF", 
                      "ON", "SUB", "TERMINATOR", "TOGGLE", "ID", "INT", 
                      "FLOAT", "STRING", "EOL_COMMENT", "COMMENT", "WS" ]

    RULE_macro_file = 0
    RULE_interactive = 1
    RULE_assignment = 2
    RULE_stat = 3
    RULE_compound = 4
    RULE_expr = 5
    RULE_direction = 6
    RULE_axis = 7
    RULE_macro_def = 8
    RULE_macro_header = 9
    RULE_param = 10
    RULE_param_type = 11
    RULE_name = 12
    RULE_kwd_names = 13

    ruleNames =  [ "macro_file", "interactive", "assignment", "stat", "compound", 
                   "expr", "direction", "axis", "macro_def", "macro_header", 
                   "param", "param_type", "name", "kwd_names" ]

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
    T__32=33
    T__33=34
    T__34=35
    ADD=36
    ASSIGN=37
    ATTR=38
    DIV=39
    INJECT=40
    MUL=41
    OFF=42
    ON=43
    SUB=44
    TERMINATOR=45
    TOGGLE=46
    ID=47
    INT=48
    FLOAT=49
    STRING=50
    EOL_COMMENT=51
    COMMENT=52
    WS=53

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

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.StatContext)
            else:
                return self.getTypedRuleContext(DMFParser.StatContext,i)


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
            self.state = 31
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__4) | (1 << DMFParser.T__9) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__34) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                self.state = 28
                self.stat()
                self.state = 33
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 34
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



    def interactive(self):

        localctx = DMFParser.InteractiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_interactive)
        try:
            self.state = 45
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 36
                self.compound()
                self.state = 37
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Assignment_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 39
                self.assignment()
                self.state = 40
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 42
                self.expr(0)
                self.state = 43
                self.match(DMFParser.EOF)
                pass


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
        self.enterRule(localctx, 4, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            localctx.which = self.name()
            self.state = 48
            self.match(DMFParser.ASSIGN)
            self.state = 49
            localctx.what = self.expr(0)
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



    def stat(self):

        localctx = DMFParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_stat)
        try:
            self.state = 58
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Assign_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 51
                self.assignment()
                self.state = 52
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 54
                self.expr(0)
                self.state = 55
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 3:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 57
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
        self.enterRule(localctx, 8, self.RULE_compound)
        self._la = 0 # Token type
        try:
            self.state = 76
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__0]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 60
                self.match(DMFParser.T__0)
                self.state = 64
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__4) | (1 << DMFParser.T__9) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__34) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                    self.state = 61
                    self.stat()
                    self.state = 66
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 67
                self.match(DMFParser.T__1)
                pass
            elif token in [DMFParser.T__2]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 68
                self.match(DMFParser.T__2)
                self.state = 72
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__4) | (1 << DMFParser.T__9) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__34) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                    self.state = 69
                    self.stat()
                    self.state = 74
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 75
                self.match(DMFParser.T__3)
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
            return DMFParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class Paren_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
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


    class Exit_pad_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.well = None # ExprContext
            self.copyFrom(ctx)

        def ATTR(self):
            return self.getToken(DMFParser.ATTR, 0)
        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExit_pad_expr" ):
                listener.enterExit_pad_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExit_pad_expr" ):
                listener.exitExit_pad_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExit_pad_expr" ):
                return visitor.visitExit_pad_expr(self)
            else:
                return visitor.visitChildren(self)


    class Index_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.who = None # ExprContext
            self.which = None # ExprContext
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


    class Twiddle_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ON(self):
            return self.getToken(DMFParser.ON, 0)
        def OFF(self):
            return self.getToken(DMFParser.OFF, 0)
        def TOGGLE(self):
            return self.getToken(DMFParser.TOGGLE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTwiddle_expr" ):
                listener.enterTwiddle_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTwiddle_expr" ):
                listener.exitTwiddle_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTwiddle_expr" ):
                return visitor.visitTwiddle_expr(self)
            else:
                return visitor.visitChildren(self)


    class Injection_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.who = None # ExprContext
            self.what = None # ExprContext
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
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 79
                self.match(DMFParser.T__4)
                self.state = 80
                self.expr(0)
                self.state = 81
                self.match(DMFParser.T__5)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 83
                self.match(DMFParser.T__4)
                self.state = 84
                localctx.x = self.expr(0)
                self.state = 85
                self.match(DMFParser.T__6)
                self.state = 86
                localctx.y = self.expr(0)
                self.state = 87
                self.match(DMFParser.T__5)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 89
                self.match(DMFParser.SUB)
                self.state = 90
                localctx.rhs = self.expr(20)
                pass

            elif la_ == 4:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 91
                self.direction()
                self.state = 92
                localctx.dist = self.expr(15)
                pass

            elif la_ == 5:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 94
                self.match(DMFParser.T__9)
                self.state = 96
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31))) != 0):
                    self.state = 95
                    self.axis()


                self.state = 98
                localctx.which = self.expr(14)
                pass

            elif la_ == 6:
                localctx = DMFParser.Well_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 99
                self.match(DMFParser.T__10)
                self.state = 100
                self.match(DMFParser.T__11)
                self.state = 101
                localctx.which = self.expr(13)
                pass

            elif la_ == 7:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 102
                self.match(DMFParser.T__12)
                self.state = 103
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__13 or _la==DMFParser.T__14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 104
                localctx.loc = self.expr(12)
                pass

            elif la_ == 8:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 105
                self.macro_def()
                pass

            elif la_ == 9:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 107
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__18:
                    self.state = 106
                    self.match(DMFParser.T__18)


                self.state = 109
                _la = self._input.LA(1)
                if not(_la==DMFParser.OFF or _la==DMFParser.ON):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 10:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 110
                self.match(DMFParser.TOGGLE)
                self.state = 112
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                if la_ == 1:
                    self.state = 111
                    self.match(DMFParser.T__19)


                pass

            elif la_ == 11:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 115
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__20:
                    self.state = 114
                    self.match(DMFParser.T__20)


                self.state = 117
                self.param_type()
                pass

            elif la_ == 12:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 118
                self.param_type()
                self.state = 119
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 13:
                localctx = DMFParser.Function_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 121
                self.name()
                self.state = 122
                self.match(DMFParser.T__4)
                self.state = 131
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__4) | (1 << DMFParser.T__9) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__34) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                    self.state = 123
                    localctx._expr = self.expr(0)
                    localctx.args.append(localctx._expr)
                    self.state = 128
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==DMFParser.T__6:
                        self.state = 124
                        self.match(DMFParser.T__6)
                        self.state = 125
                        localctx._expr = self.expr(0)
                        localctx.args.append(localctx._expr)
                        self.state = 130
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 133
                self.match(DMFParser.T__5)
                pass

            elif la_ == 14:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 135
                self.name()
                pass

            elif la_ == 15:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 136
                self.match(DMFParser.INT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 164
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 162
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 139
                        if not self.precpred(self._ctx, 17):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 17)")
                        self.state = 140
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 141
                        localctx.rhs = self.expr(18)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 142
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 143
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 144
                        localctx.rhs = self.expr(17)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 145
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 146
                        self.match(DMFParser.INJECT)
                        self.state = 147
                        localctx.what = self.expr(10)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 148
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 149
                        self.match(DMFParser.T__7)
                        self.state = 150
                        localctx.which = self.expr(0)
                        self.state = 151
                        self.match(DMFParser.T__8)
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 153
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 154
                        self.direction()
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Gate_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.well = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 155
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 156
                        self.match(DMFParser.ATTR)
                        self.state = 157
                        self.match(DMFParser.T__15)
                        pass

                    elif la_ == 7:
                        localctx = DMFParser.Exit_pad_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.well = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 158
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 159
                        self.match(DMFParser.ATTR)
                        self.state = 160
                        self.match(DMFParser.T__16)
                        self.state = 161
                        self.match(DMFParser.T__17)
                        pass

             
                self.state = 166
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

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
        self.enterRule(localctx, 12, self.RULE_direction)
        self._la = 0 # Token type
        try:
            self.state = 179
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__21, DMFParser.T__22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 167
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__21 or _la==DMFParser.T__22):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__23, DMFParser.T__24]:
                self.enterOuterAlt(localctx, 2)
                self.state = 170
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__23 or _la==DMFParser.T__24):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__25, DMFParser.T__26]:
                self.enterOuterAlt(localctx, 3)
                self.state = 173
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__25 or _la==DMFParser.T__26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__27, DMFParser.T__28]:
                self.enterOuterAlt(localctx, 4)
                self.state = 176
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__27 or _la==DMFParser.T__28):
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
        self.enterRule(localctx, 14, self.RULE_axis)
        self._la = 0 # Token type
        try:
            self.state = 185
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__29]:
                self.enterOuterAlt(localctx, 1)
                self.state = 181
                self.match(DMFParser.T__29)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__30, DMFParser.T__31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 183
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__30 or _la==DMFParser.T__31):
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
        self.enterRule(localctx, 16, self.RULE_macro_def)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 187
            self.macro_header()
            self.state = 190
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__0, DMFParser.T__2]:
                self.state = 188
                self.compound()
                pass
            elif token in [DMFParser.T__4, DMFParser.T__9, DMFParser.T__10, DMFParser.T__12, DMFParser.T__17, DMFParser.T__18, DMFParser.T__20, DMFParser.T__21, DMFParser.T__22, DMFParser.T__23, DMFParser.T__24, DMFParser.T__25, DMFParser.T__26, DMFParser.T__27, DMFParser.T__28, DMFParser.T__32, DMFParser.T__33, DMFParser.T__34, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT]:
                self.state = 189
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
        self.enterRule(localctx, 18, self.RULE_macro_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.match(DMFParser.T__32)
            self.state = 193
            self.match(DMFParser.T__4)
            self.state = 202
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__17) | (1 << DMFParser.T__33) | (1 << DMFParser.T__34) | (1 << DMFParser.ID))) != 0):
                self.state = 194
                self.param()
                self.state = 199
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__6:
                    self.state = 195
                    self.match(DMFParser.T__6)
                    self.state = 196
                    self.param()
                    self.state = 201
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 204
            self.match(DMFParser.T__5)
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
        self.enterRule(localctx, 20, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.state = 218
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__10, DMFParser.T__12, DMFParser.T__17, DMFParser.T__33]:
                self.enterOuterAlt(localctx, 1)
                self.state = 206
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 210
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.INT:
                    self.state = 208
                    localctx._INT = self.match(DMFParser.INT)
                    localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))


                pass
            elif token in [DMFParser.T__34, DMFParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 212
                localctx._name = self.name()
                self.state = 213
                self.match(DMFParser.INJECT)
                self.state = 214
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
        self.enterRule(localctx, 22, self.RULE_param_type)
        try:
            self.state = 228
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__12]:
                self.enterOuterAlt(localctx, 1)
                self.state = 220
                self.match(DMFParser.T__12)
                localctx.type=Type.DROP
                pass
            elif token in [DMFParser.T__17]:
                self.enterOuterAlt(localctx, 2)
                self.state = 222
                self.match(DMFParser.T__17)
                localctx.type=Type.PAD
                pass
            elif token in [DMFParser.T__10]:
                self.enterOuterAlt(localctx, 3)
                self.state = 224
                self.match(DMFParser.T__10)
                localctx.type=Type.WELL
                pass
            elif token in [DMFParser.T__33]:
                self.enterOuterAlt(localctx, 4)
                self.state = 226
                self.match(DMFParser.T__33)
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
        self.enterRule(localctx, 24, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 232
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.ID]:
                self.state = 230
                self.match(DMFParser.ID)
                pass
            elif token in [DMFParser.T__34]:
                self.state = 231
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
        self.enterRule(localctx, 26, self.RULE_kwd_names)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 234
            self.match(DMFParser.T__34)
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
        self._predicates[5] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 17)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 16)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 19)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 10)
         




