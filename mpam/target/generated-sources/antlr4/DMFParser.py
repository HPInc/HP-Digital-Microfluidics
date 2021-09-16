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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3:")
        buf.write("\u0106\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\3\2\7\2\"\n\2\f\2\16\2%\13\2")
        buf.write("\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3\63")
        buf.write("\n\3\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5@")
        buf.write("\n\5\3\6\3\6\7\6D\n\6\f\6\16\6G\13\6\3\6\3\6\3\6\7\6L")
        buf.write("\n\6\f\6\16\6O\13\6\3\6\5\6R\n\6\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\5\7h\n\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7")
        buf.write("s\n\7\3\7\3\7\3\7\5\7x\n\7\3\7\5\7{\n\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\7\7\u0086\n\7\f\7\16\7\u0089\13")
        buf.write("\7\5\7\u008b\n\7\3\7\3\7\3\7\3\7\5\7\u0091\n\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\7\7\u00ac\n\7\f")
        buf.write("\7\16\7\u00af\13\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b")
        buf.write("\3\b\3\b\3\b\5\b\u00bd\n\b\3\t\3\t\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\t\3\t\3\t\3\t\3\t\3\t\3\t\5\t\u00cd\n\t\3\n\3\n\3\n")
        buf.write("\3\n\5\n\u00d3\n\n\3\13\3\13\3\13\5\13\u00d8\n\13\3\f")
        buf.write("\3\f\3\f\3\f\3\f\7\f\u00df\n\f\f\f\16\f\u00e2\13\f\5\f")
        buf.write("\u00e4\n\f\3\f\3\f\3\r\3\r\3\r\3\r\5\r\u00ec\n\r\3\r\3")
        buf.write("\r\3\r\3\r\3\r\3\r\5\r\u00f4\n\r\3\16\3\16\3\16\3\16\3")
        buf.write("\16\3\16\3\16\3\16\5\16\u00fe\n\16\3\17\3\17\5\17\u0102")
        buf.write("\n\17\3\20\3\20\3\20\2\3\f\21\2\4\6\b\n\f\16\20\22\24")
        buf.write("\26\30\32\34\36\2\f\3\2\23\24\3\2/\60\4\2,,..\4\2))\61")
        buf.write("\61\3\2\30\31\3\2\32\33\3\2\34\35\3\2\36\37\3\2\"#\3\2")
        buf.write("$%\2\u012c\2#\3\2\2\2\4\62\3\2\2\2\6\64\3\2\2\2\b?\3\2")
        buf.write("\2\2\nQ\3\2\2\2\f\u0090\3\2\2\2\16\u00bc\3\2\2\2\20\u00cc")
        buf.write("\3\2\2\2\22\u00d2\3\2\2\2\24\u00d4\3\2\2\2\26\u00d9\3")
        buf.write("\2\2\2\30\u00f3\3\2\2\2\32\u00fd\3\2\2\2\34\u0101\3\2")
        buf.write("\2\2\36\u0103\3\2\2\2 \"\5\b\5\2! \3\2\2\2\"%\3\2\2\2")
        buf.write("#!\3\2\2\2#$\3\2\2\2$&\3\2\2\2%#\3\2\2\2&\'\7\2\2\3\'")
        buf.write("\3\3\2\2\2()\5\n\6\2)*\7\2\2\3*\63\3\2\2\2+,\5\6\4\2,")
        buf.write("-\7\2\2\3-\63\3\2\2\2./\5\f\7\2/\60\7\2\2\3\60\63\3\2")
        buf.write("\2\2\61\63\7\2\2\3\62(\3\2\2\2\62+\3\2\2\2\62.\3\2\2\2")
        buf.write("\62\61\3\2\2\2\63\5\3\2\2\2\64\65\5\34\17\2\65\66\7*\2")
        buf.write("\2\66\67\5\f\7\2\67\7\3\2\2\289\5\6\4\29:\7\62\2\2:@\3")
        buf.write("\2\2\2;<\5\f\7\2<=\7\62\2\2=@\3\2\2\2>@\5\n\6\2?8\3\2")
        buf.write("\2\2?;\3\2\2\2?>\3\2\2\2@\t\3\2\2\2AE\7\3\2\2BD\5\b\5")
        buf.write("\2CB\3\2\2\2DG\3\2\2\2EC\3\2\2\2EF\3\2\2\2FH\3\2\2\2G")
        buf.write("E\3\2\2\2HR\7\4\2\2IM\7\5\2\2JL\5\b\5\2KJ\3\2\2\2LO\3")
        buf.write("\2\2\2MK\3\2\2\2MN\3\2\2\2NP\3\2\2\2OM\3\2\2\2PR\7\6\2")
        buf.write("\2QA\3\2\2\2QI\3\2\2\2R\13\3\2\2\2ST\b\7\1\2TU\7\7\2\2")
        buf.write("UV\5\f\7\2VW\7\b\2\2W\u0091\3\2\2\2XY\7\7\2\2YZ\5\f\7")
        buf.write("\2Z[\7\t\2\2[\\\5\f\7\2\\]\7\b\2\2]\u0091\3\2\2\2^_\7")
        buf.write("\61\2\2_\u0091\5\f\7\30`a\7\65\2\2a\u0091\5\20\t\2bc\5")
        buf.write("\16\b\2cd\5\f\7\22d\u0091\3\2\2\2eg\7\n\2\2fh\5\22\n\2")
        buf.write("gf\3\2\2\2gh\3\2\2\2hi\3\2\2\2i\u0091\5\f\7\21jk\7\13")
        buf.write("\2\2kl\7\f\2\2l\u0091\5\f\7\20mn\7\22\2\2no\t\2\2\2o\u0091")
        buf.write("\5\f\7\fp\u0091\5\24\13\2qs\7\25\2\2rq\3\2\2\2rs\3\2\2")
        buf.write("\2st\3\2\2\2t\u0091\t\3\2\2uw\7\63\2\2vx\7\26\2\2wv\3")
        buf.write("\2\2\2wx\3\2\2\2x\u0091\3\2\2\2y{\7\27\2\2zy\3\2\2\2z")
        buf.write("{\3\2\2\2{|\3\2\2\2|\u0091\5\32\16\2}~\5\32\16\2~\177")
        buf.write("\7\65\2\2\177\u0091\3\2\2\2\u0080\u0081\5\34\17\2\u0081")
        buf.write("\u008a\7\7\2\2\u0082\u0087\5\f\7\2\u0083\u0084\7\t\2\2")
        buf.write("\u0084\u0086\5\f\7\2\u0085\u0083\3\2\2\2\u0086\u0089\3")
        buf.write("\2\2\2\u0087\u0085\3\2\2\2\u0087\u0088\3\2\2\2\u0088\u008b")
        buf.write("\3\2\2\2\u0089\u0087\3\2\2\2\u008a\u0082\3\2\2\2\u008a")
        buf.write("\u008b\3\2\2\2\u008b\u008c\3\2\2\2\u008c\u008d\7\b\2\2")
        buf.write("\u008d\u0091\3\2\2\2\u008e\u0091\5\34\17\2\u008f\u0091")
        buf.write("\7\65\2\2\u0090S\3\2\2\2\u0090X\3\2\2\2\u0090^\3\2\2\2")
        buf.write("\u0090`\3\2\2\2\u0090b\3\2\2\2\u0090e\3\2\2\2\u0090j\3")
        buf.write("\2\2\2\u0090m\3\2\2\2\u0090p\3\2\2\2\u0090r\3\2\2\2\u0090")
        buf.write("u\3\2\2\2\u0090z\3\2\2\2\u0090}\3\2\2\2\u0090\u0080\3")
        buf.write("\2\2\2\u0090\u008e\3\2\2\2\u0090\u008f\3\2\2\2\u0091\u00ad")
        buf.write("\3\2\2\2\u0092\u0093\f\24\2\2\u0093\u0094\t\4\2\2\u0094")
        buf.write("\u00ac\5\f\7\25\u0095\u0096\f\23\2\2\u0096\u0097\t\5\2")
        buf.write("\2\u0097\u00ac\5\f\7\24\u0098\u0099\f\13\2\2\u0099\u009a")
        buf.write("\7-\2\2\u009a\u00ac\5\f\7\f\u009b\u009c\f\27\2\2\u009c")
        buf.write("\u00ac\5\16\b\2\u009d\u009e\f\25\2\2\u009e\u00ac\5\20")
        buf.write("\t\2\u009f\u00a0\f\17\2\2\u00a0\u00a1\7\r\2\2\u00a1\u00a2")
        buf.write("\5\f\7\2\u00a2\u00a3\7\16\2\2\u00a3\u00ac\3\2\2\2\u00a4")
        buf.write("\u00a5\f\16\2\2\u00a5\u00a6\7+\2\2\u00a6\u00ac\7\17\2")
        buf.write("\2\u00a7\u00a8\f\r\2\2\u00a8\u00a9\7+\2\2\u00a9\u00aa")
        buf.write("\7\20\2\2\u00aa\u00ac\7\21\2\2\u00ab\u0092\3\2\2\2\u00ab")
        buf.write("\u0095\3\2\2\2\u00ab\u0098\3\2\2\2\u00ab\u009b\3\2\2\2")
        buf.write("\u00ab\u009d\3\2\2\2\u00ab\u009f\3\2\2\2\u00ab\u00a4\3")
        buf.write("\2\2\2\u00ab\u00a7\3\2\2\2\u00ac\u00af\3\2\2\2\u00ad\u00ab")
        buf.write("\3\2\2\2\u00ad\u00ae\3\2\2\2\u00ae\r\3\2\2\2\u00af\u00ad")
        buf.write("\3\2\2\2\u00b0\u00b1\t\6\2\2\u00b1\u00b2\b\b\1\2\u00b2")
        buf.write("\u00bd\b\b\1\2\u00b3\u00b4\t\7\2\2\u00b4\u00b5\b\b\1\2")
        buf.write("\u00b5\u00bd\b\b\1\2\u00b6\u00b7\t\b\2\2\u00b7\u00b8\b")
        buf.write("\b\1\2\u00b8\u00bd\b\b\1\2\u00b9\u00ba\t\t\2\2\u00ba\u00bb")
        buf.write("\b\b\1\2\u00bb\u00bd\b\b\1\2\u00bc\u00b0\3\2\2\2\u00bc")
        buf.write("\u00b3\3\2\2\2\u00bc\u00b6\3\2\2\2\u00bc\u00b9\3\2\2\2")
        buf.write("\u00bd\17\3\2\2\2\u00be\u00bf\6\t\n\3\u00bf\u00c0\7 \2")
        buf.write("\2\u00c0\u00c1\b\t\1\2\u00c1\u00cd\b\t\1\2\u00c2\u00c3")
        buf.write("\7!\2\2\u00c3\u00c4\b\t\1\2\u00c4\u00cd\b\t\1\2\u00c5")
        buf.write("\u00c6\6\t\13\3\u00c6\u00c7\t\n\2\2\u00c7\u00c8\b\t\1")
        buf.write("\2\u00c8\u00cd\b\t\1\2\u00c9\u00ca\t\13\2\2\u00ca\u00cb")
        buf.write("\b\t\1\2\u00cb\u00cd\b\t\1\2\u00cc\u00be\3\2\2\2\u00cc")
        buf.write("\u00c2\3\2\2\2\u00cc\u00c5\3\2\2\2\u00cc\u00c9\3\2\2\2")
        buf.write("\u00cd\21\3\2\2\2\u00ce\u00cf\7 \2\2\u00cf\u00d3\b\n\1")
        buf.write("\2\u00d0\u00d1\t\n\2\2\u00d1\u00d3\b\n\1\2\u00d2\u00ce")
        buf.write("\3\2\2\2\u00d2\u00d0\3\2\2\2\u00d3\23\3\2\2\2\u00d4\u00d7")
        buf.write("\5\26\f\2\u00d5\u00d8\5\n\6\2\u00d6\u00d8\5\f\7\2\u00d7")
        buf.write("\u00d5\3\2\2\2\u00d7\u00d6\3\2\2\2\u00d8\25\3\2\2\2\u00d9")
        buf.write("\u00da\7&\2\2\u00da\u00e3\7\7\2\2\u00db\u00e0\5\30\r\2")
        buf.write("\u00dc\u00dd\7\t\2\2\u00dd\u00df\5\30\r\2\u00de\u00dc")
        buf.write("\3\2\2\2\u00df\u00e2\3\2\2\2\u00e0\u00de\3\2\2\2\u00e0")
        buf.write("\u00e1\3\2\2\2\u00e1\u00e4\3\2\2\2\u00e2\u00e0\3\2\2\2")
        buf.write("\u00e3\u00db\3\2\2\2\u00e3\u00e4\3\2\2\2\u00e4\u00e5\3")
        buf.write("\2\2\2\u00e5\u00e6\7\b\2\2\u00e6\27\3\2\2\2\u00e7\u00e8")
        buf.write("\5\32\16\2\u00e8\u00eb\b\r\1\2\u00e9\u00ea\7\65\2\2\u00ea")
        buf.write("\u00ec\b\r\1\2\u00eb\u00e9\3\2\2\2\u00eb\u00ec\3\2\2\2")
        buf.write("\u00ec\u00f4\3\2\2\2\u00ed\u00ee\5\34\17\2\u00ee\u00ef")
        buf.write("\7-\2\2\u00ef\u00f0\5\32\16\2\u00f0\u00f1\b\r\1\2\u00f1")
        buf.write("\u00f2\b\r\1\2\u00f2\u00f4\3\2\2\2\u00f3\u00e7\3\2\2\2")
        buf.write("\u00f3\u00ed\3\2\2\2\u00f4\31\3\2\2\2\u00f5\u00f6\7\22")
        buf.write("\2\2\u00f6\u00fe\b\16\1\2\u00f7\u00f8\7\21\2\2\u00f8\u00fe")
        buf.write("\b\16\1\2\u00f9\u00fa\7\13\2\2\u00fa\u00fe\b\16\1\2\u00fb")
        buf.write("\u00fc\7\'\2\2\u00fc\u00fe\b\16\1\2\u00fd\u00f5\3\2\2")
        buf.write("\2\u00fd\u00f7\3\2\2\2\u00fd\u00f9\3\2\2\2\u00fd\u00fb")
        buf.write("\3\2\2\2\u00fe\33\3\2\2\2\u00ff\u0102\7\64\2\2\u0100\u0102")
        buf.write("\5\36\20\2\u0101\u00ff\3\2\2\2\u0101\u0100\3\2\2\2\u0102")
        buf.write("\35\3\2\2\2\u0103\u0104\7(\2\2\u0104\37\3\2\2\2\33#\62")
        buf.write("?EMQgrwz\u0087\u008a\u0090\u00ab\u00ad\u00bc\u00cc\u00d2")
        buf.write("\u00d7\u00e0\u00e3\u00eb\u00f3\u00fd\u0101")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "'}'", "'[['", "']]'", "'('", "')'", 
                     "','", "'to'", "'well'", "'#'", "'['", "']'", "'gate'", 
                     "'exit'", "'pad'", "'drop'", "'@'", "'at'", "'turn'", 
                     "'state'", "'the'", "'up'", "'north'", "'down'", "'south'", 
                     "'left'", "'west'", "'right'", "'east'", "'row'", "'rows'", 
                     "'col'", "'column'", "'cols'", "'columns'", "'macro'", 
                     "'int'", "'**__**'", "'+'", "'='", "''s'", "'/'", "':'", 
                     "'*'", "'off'", "'on'", "'-'", "';'", "'toggle'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "ADD", "ASSIGN", 
                      "ATTR", "DIV", "INJECT", "MUL", "OFF", "ON", "SUB", 
                      "TERMINATOR", "TOGGLE", "ID", "INT", "FLOAT", "STRING", 
                      "EOL_COMMENT", "COMMENT", "WS" ]

    RULE_macro_file = 0
    RULE_interactive = 1
    RULE_assignment = 2
    RULE_stat = 3
    RULE_compound = 4
    RULE_expr = 5
    RULE_direction = 6
    RULE_rc = 7
    RULE_axis = 8
    RULE_macro_def = 9
    RULE_macro_header = 10
    RULE_param = 11
    RULE_param_type = 12
    RULE_name = 13
    RULE_kwd_names = 14

    ruleNames =  [ "macro_file", "interactive", "assignment", "stat", "compound", 
                   "expr", "direction", "rc", "axis", "macro_def", "macro_header", 
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
    T__35=36
    T__36=37
    T__37=38
    ADD=39
    ASSIGN=40
    ATTR=41
    DIV=42
    INJECT=43
    MUL=44
    OFF=45
    ON=46
    SUB=47
    TERMINATOR=48
    TOGGLE=49
    ID=50
    INT=51
    FLOAT=52
    STRING=53
    EOL_COMMENT=54
    COMMENT=55
    WS=56

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
            self.state = 33
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__4) | (1 << DMFParser.T__7) | (1 << DMFParser.T__8) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__18) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                self.state = 30
                self.stat()
                self.state = 35
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 36
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


    class Empty_interactiveContext(InteractiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.InteractiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def EOF(self):
            return self.getToken(DMFParser.EOF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmpty_interactive" ):
                listener.enterEmpty_interactive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmpty_interactive" ):
                listener.exitEmpty_interactive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmpty_interactive" ):
                return visitor.visitEmpty_interactive(self)
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
            self.state = 48
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 38
                self.compound()
                self.state = 39
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Assignment_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 41
                self.assignment()
                self.state = 42
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 44
                self.expr(0)
                self.state = 45
                self.match(DMFParser.EOF)
                pass

            elif la_ == 4:
                localctx = DMFParser.Empty_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 47
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
            self.state = 50
            localctx.which = self.name()
            self.state = 51
            self.match(DMFParser.ASSIGN)
            self.state = 52
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
            self.state = 61
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Assign_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 54
                self.assignment()
                self.state = 55
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 57
                self.expr(0)
                self.state = 58
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 3:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 60
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
            self.state = 79
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__0]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 63
                self.match(DMFParser.T__0)
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__4) | (1 << DMFParser.T__7) | (1 << DMFParser.T__8) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__18) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                    self.state = 64
                    self.stat()
                    self.state = 69
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 70
                self.match(DMFParser.T__1)
                pass
            elif token in [DMFParser.T__2]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 71
                self.match(DMFParser.T__2)
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__4) | (1 << DMFParser.T__7) | (1 << DMFParser.T__8) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__18) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                    self.state = 72
                    self.stat()
                    self.state = 77
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 78
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


    class Const_rc_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self._INT = None # Token
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(DMFParser.INT, 0)
        def rc(self):
            return self.getTypedRuleContext(DMFParser.RcContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConst_rc_expr" ):
                listener.enterConst_rc_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConst_rc_expr" ):
                listener.exitConst_rc_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConst_rc_expr" ):
                return visitor.visitConst_rc_expr(self)
            else:
                return visitor.visitChildren(self)


    class Int_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self._INT = None # Token
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


    class N_rc_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.dist = None # ExprContext
            self.copyFrom(ctx)

        def rc(self):
            return self.getTypedRuleContext(DMFParser.RcContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterN_rc_expr" ):
                listener.enterN_rc_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitN_rc_expr" ):
                listener.exitN_rc_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitN_rc_expr" ):
                return visitor.visitN_rc_expr(self)
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
            self.state = 142
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 82
                self.match(DMFParser.T__4)
                self.state = 83
                self.expr(0)
                self.state = 84
                self.match(DMFParser.T__5)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 86
                self.match(DMFParser.T__4)
                self.state = 87
                localctx.x = self.expr(0)
                self.state = 88
                self.match(DMFParser.T__6)
                self.state = 89
                localctx.y = self.expr(0)
                self.state = 90
                self.match(DMFParser.T__5)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 92
                self.match(DMFParser.SUB)
                self.state = 93
                localctx.rhs = self.expr(22)
                pass

            elif la_ == 4:
                localctx = DMFParser.Const_rc_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 94
                localctx._INT = self.match(DMFParser.INT)
                self.state = 95
                self.rc((0 if localctx._INT is None else int(localctx._INT.text)))
                pass

            elif la_ == 5:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 96
                self.direction()
                self.state = 97
                localctx.dist = self.expr(16)
                pass

            elif la_ == 6:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 99
                self.match(DMFParser.T__7)
                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__29) | (1 << DMFParser.T__31) | (1 << DMFParser.T__32))) != 0):
                    self.state = 100
                    self.axis()


                self.state = 103
                localctx.which = self.expr(15)
                pass

            elif la_ == 7:
                localctx = DMFParser.Well_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 104
                self.match(DMFParser.T__8)
                self.state = 105
                self.match(DMFParser.T__9)
                self.state = 106
                localctx.which = self.expr(14)
                pass

            elif la_ == 8:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 107
                self.match(DMFParser.T__15)
                self.state = 108
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__16 or _la==DMFParser.T__17):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 109
                localctx.loc = self.expr(10)
                pass

            elif la_ == 9:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 110
                self.macro_def()
                pass

            elif la_ == 10:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__18:
                    self.state = 111
                    self.match(DMFParser.T__18)


                self.state = 114
                _la = self._input.LA(1)
                if not(_la==DMFParser.OFF or _la==DMFParser.ON):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 11:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 115
                self.match(DMFParser.TOGGLE)
                self.state = 117
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                if la_ == 1:
                    self.state = 116
                    self.match(DMFParser.T__19)


                pass

            elif la_ == 12:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__20:
                    self.state = 119
                    self.match(DMFParser.T__20)


                self.state = 122
                self.param_type()
                pass

            elif la_ == 13:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 123
                self.param_type()
                self.state = 124
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 14:
                localctx = DMFParser.Function_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 126
                self.name()
                self.state = 127
                self.match(DMFParser.T__4)
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__4) | (1 << DMFParser.T__7) | (1 << DMFParser.T__8) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__18) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB) | (1 << DMFParser.TOGGLE) | (1 << DMFParser.ID) | (1 << DMFParser.INT))) != 0):
                    self.state = 128
                    localctx._expr = self.expr(0)
                    localctx.args.append(localctx._expr)
                    self.state = 133
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==DMFParser.T__6:
                        self.state = 129
                        self.match(DMFParser.T__6)
                        self.state = 130
                        localctx._expr = self.expr(0)
                        localctx.args.append(localctx._expr)
                        self.state = 135
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 138
                self.match(DMFParser.T__5)
                pass

            elif la_ == 15:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 140
                self.name()
                pass

            elif la_ == 16:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 141
                localctx._INT = self.match(DMFParser.INT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 171
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 169
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 144
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 145
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 146
                        localctx.rhs = self.expr(19)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 147
                        if not self.precpred(self._ctx, 17):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 17)")
                        self.state = 148
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 149
                        localctx.rhs = self.expr(18)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 150
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 151
                        self.match(DMFParser.INJECT)
                        self.state = 152
                        localctx.what = self.expr(10)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 153
                        if not self.precpred(self._ctx, 21):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 21)")
                        self.state = 154
                        self.direction()
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.N_rc_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 155
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 156
                        self.rc(0)
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 157
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 158
                        self.match(DMFParser.T__10)
                        self.state = 159
                        localctx.which = self.expr(0)
                        self.state = 160
                        self.match(DMFParser.T__11)
                        pass

                    elif la_ == 7:
                        localctx = DMFParser.Gate_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.well = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 162
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 163
                        self.match(DMFParser.ATTR)
                        self.state = 164
                        self.match(DMFParser.T__12)
                        pass

                    elif la_ == 8:
                        localctx = DMFParser.Exit_pad_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.well = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 165
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 166
                        self.match(DMFParser.ATTR)
                        self.state = 167
                        self.match(DMFParser.T__13)
                        self.state = 168
                        self.match(DMFParser.T__14)
                        pass

             
                self.state = 173
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
            self.state = 186
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__21, DMFParser.T__22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 174
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
                self.state = 177
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
                self.state = 180
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
                self.state = 183
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


    class RcContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1, n:int=None):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.n = None
            self.d = None
            self.verticalp = None
            self.n = n


        def getRuleIndex(self):
            return DMFParser.RULE_rc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRc" ):
                listener.enterRc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRc" ):
                listener.exitRc(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRc" ):
                return visitor.visitRc(self)
            else:
                return visitor.visitChildren(self)




    def rc(self, n:int):

        localctx = DMFParser.RcContext(self, self._ctx, self.state, n)
        self.enterRule(localctx, 14, self.RULE_rc)
        self._la = 0 # Token type
        try:
            self.state = 202
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 188
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 189
                self.match(DMFParser.T__29)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 192
                self.match(DMFParser.T__30)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 195
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 196
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__31 or _la==DMFParser.T__32):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 199
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__33 or _la==DMFParser.T__34):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass


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
        self.enterRule(localctx, 16, self.RULE_axis)
        self._la = 0 # Token type
        try:
            self.state = 208
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__29]:
                self.enterOuterAlt(localctx, 1)
                self.state = 204
                self.match(DMFParser.T__29)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__31, DMFParser.T__32]:
                self.enterOuterAlt(localctx, 2)
                self.state = 206
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__31 or _la==DMFParser.T__32):
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
        self.enterRule(localctx, 18, self.RULE_macro_def)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            self.macro_header()
            self.state = 213
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__0, DMFParser.T__2]:
                self.state = 211
                self.compound()
                pass
            elif token in [DMFParser.T__4, DMFParser.T__7, DMFParser.T__8, DMFParser.T__14, DMFParser.T__15, DMFParser.T__18, DMFParser.T__20, DMFParser.T__21, DMFParser.T__22, DMFParser.T__23, DMFParser.T__24, DMFParser.T__25, DMFParser.T__26, DMFParser.T__27, DMFParser.T__28, DMFParser.T__35, DMFParser.T__36, DMFParser.T__37, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT]:
                self.state = 212
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
        self.enterRule(localctx, 20, self.RULE_macro_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 215
            self.match(DMFParser.T__35)
            self.state = 216
            self.match(DMFParser.T__4)
            self.state = 225
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__8) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.ID))) != 0):
                self.state = 217
                self.param()
                self.state = 222
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__6:
                    self.state = 218
                    self.match(DMFParser.T__6)
                    self.state = 219
                    self.param()
                    self.state = 224
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 227
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
        self.enterRule(localctx, 22, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.state = 241
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__8, DMFParser.T__14, DMFParser.T__15, DMFParser.T__36]:
                self.enterOuterAlt(localctx, 1)
                self.state = 229
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 233
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.INT:
                    self.state = 231
                    localctx._INT = self.match(DMFParser.INT)
                    localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))


                pass
            elif token in [DMFParser.T__37, DMFParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 235
                localctx._name = self.name()
                self.state = 236
                self.match(DMFParser.INJECT)
                self.state = 237
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
        self.enterRule(localctx, 24, self.RULE_param_type)
        try:
            self.state = 251
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__15]:
                self.enterOuterAlt(localctx, 1)
                self.state = 243
                self.match(DMFParser.T__15)
                localctx.type=Type.DROP
                pass
            elif token in [DMFParser.T__14]:
                self.enterOuterAlt(localctx, 2)
                self.state = 245
                self.match(DMFParser.T__14)
                localctx.type=Type.PAD
                pass
            elif token in [DMFParser.T__8]:
                self.enterOuterAlt(localctx, 3)
                self.state = 247
                self.match(DMFParser.T__8)
                localctx.type=Type.WELL
                pass
            elif token in [DMFParser.T__36]:
                self.enterOuterAlt(localctx, 4)
                self.state = 249
                self.match(DMFParser.T__36)
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
        self.enterRule(localctx, 26, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 255
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.ID]:
                self.state = 253
                self.match(DMFParser.ID)
                pass
            elif token in [DMFParser.T__37]:
                self.state = 254
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
        self.enterRule(localctx, 28, self.RULE_kwd_names)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            self.match(DMFParser.T__37)
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
        self._predicates[7] = self.rc_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 17)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 21)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 19)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 11)
         

    def rc_sempred(self, localctx:RcContext, predIndex:int):
            if predIndex == 8:
                return localctx.n==1
         

            if predIndex == 9:
                return localctx.n==1
         




