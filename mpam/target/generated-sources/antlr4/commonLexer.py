# Generated from commonLexer.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from mpam.types import Dir 



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\t")
        buf.write("\u0098\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\3\2\3\2\3\3\3\3\3\4\3\4")
        buf.write("\5\4(\n\4\3\5\3\5\5\5,\n\5\3\6\3\6\3\6\5\6\61\n\6\3\6")
        buf.write("\7\6\64\n\6\f\6\16\6\67\13\6\3\6\5\6:\n\6\3\7\6\7=\n\7")
        buf.write("\r\7\16\7>\3\7\3\7\6\7C\n\7\r\7\16\7D\7\7G\n\7\f\7\16")
        buf.write("\7J\13\7\3\b\3\b\5\bN\n\b\3\b\3\b\3\t\3\t\3\t\3\t\5\t")
        buf.write("V\n\t\3\t\3\t\3\t\5\t[\n\t\3\n\3\n\5\n_\n\n\3\13\3\13")
        buf.write("\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\fl\n\f\3\r\3\r")
        buf.write("\7\rp\n\r\f\r\16\rs\13\r\3\r\3\r\3\16\3\16\3\16\3\16\7")
        buf.write("\16{\n\16\f\16\16\16~\13\16\3\16\5\16\u0081\n\16\3\16")
        buf.write("\3\16\3\16\3\16\3\17\3\17\3\17\3\17\7\17\u008b\n\17\f")
        buf.write("\17\16\17\u008e\13\17\3\17\3\17\3\17\3\17\3\17\3\20\3")
        buf.write("\20\3\20\3\20\4|\u008c\2\21\3\2\5\2\7\2\t\2\13\3\r\4\17")
        buf.write("\2\21\5\23\2\25\2\27\2\31\6\33\7\35\b\37\t\3\2\t\4\2C")
        buf.write("\\c|\3\2\62;\4\2GGgg\6\2\f\f\17\17$$^^\5\2\62;CHch\b\2")
        buf.write("$$))^^ppttvv\5\2\13\f\17\17\"\"\2\u00a0\2\13\3\2\2\2\2")
        buf.write("\r\3\2\2\2\2\21\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35")
        buf.write("\3\2\2\2\2\37\3\2\2\2\3!\3\2\2\2\5#\3\2\2\2\7\'\3\2\2")
        buf.write("\2\t+\3\2\2\2\13\60\3\2\2\2\r<\3\2\2\2\17K\3\2\2\2\21")
        buf.write("Z\3\2\2\2\23^\3\2\2\2\25`\3\2\2\2\27k\3\2\2\2\31m\3\2")
        buf.write("\2\2\33v\3\2\2\2\35\u0086\3\2\2\2\37\u0094\3\2\2\2!\"")
        buf.write("\t\2\2\2\"\4\3\2\2\2#$\t\3\2\2$\6\3\2\2\2%(\5\3\2\2&(")
        buf.write("\5\5\3\2\'%\3\2\2\2\'&\3\2\2\2(\b\3\2\2\2),\5\7\4\2*,")
        buf.write("\7a\2\2+)\3\2\2\2+*\3\2\2\2,\n\3\2\2\2-\61\5\3\2\2./\7")
        buf.write("a\2\2/\61\5\t\5\2\60-\3\2\2\2\60.\3\2\2\2\61\65\3\2\2")
        buf.write("\2\62\64\5\t\5\2\63\62\3\2\2\2\64\67\3\2\2\2\65\63\3\2")
        buf.write("\2\2\65\66\3\2\2\2\669\3\2\2\2\67\65\3\2\2\28:\7A\2\2")
        buf.write("98\3\2\2\29:\3\2\2\2:\f\3\2\2\2;=\5\5\3\2<;\3\2\2\2=>")
        buf.write("\3\2\2\2><\3\2\2\2>?\3\2\2\2?H\3\2\2\2@B\7a\2\2AC\5\5")
        buf.write("\3\2BA\3\2\2\2CD\3\2\2\2DB\3\2\2\2DE\3\2\2\2EG\3\2\2\2")
        buf.write("F@\3\2\2\2GJ\3\2\2\2HF\3\2\2\2HI\3\2\2\2I\16\3\2\2\2J")
        buf.write("H\3\2\2\2KM\t\4\2\2LN\7/\2\2ML\3\2\2\2MN\3\2\2\2NO\3\2")
        buf.write("\2\2OP\5\r\7\2P\20\3\2\2\2QR\5\r\7\2RS\7\60\2\2SU\5\r")
        buf.write("\7\2TV\5\17\b\2UT\3\2\2\2UV\3\2\2\2V[\3\2\2\2WX\5\r\7")
        buf.write("\2XY\5\17\b\2Y[\3\2\2\2ZQ\3\2\2\2ZW\3\2\2\2[\22\3\2\2")
        buf.write("\2\\_\n\5\2\2]_\5\27\f\2^\\\3\2\2\2^]\3\2\2\2_\24\3\2")
        buf.write("\2\2`a\t\6\2\2a\26\3\2\2\2bc\7^\2\2cl\t\7\2\2de\7^\2\2")
        buf.write("ef\7w\2\2fg\5\25\13\2gh\5\25\13\2hi\5\25\13\2ij\5\25\13")
        buf.write("\2jl\3\2\2\2kb\3\2\2\2kd\3\2\2\2l\30\3\2\2\2mq\7$\2\2")
        buf.write("np\5\23\n\2on\3\2\2\2ps\3\2\2\2qo\3\2\2\2qr\3\2\2\2rt")
        buf.write("\3\2\2\2sq\3\2\2\2tu\7$\2\2u\32\3\2\2\2vw\7\61\2\2wx\7")
        buf.write("\61\2\2x|\3\2\2\2y{\13\2\2\2zy\3\2\2\2{~\3\2\2\2|}\3\2")
        buf.write("\2\2|z\3\2\2\2}\u0080\3\2\2\2~|\3\2\2\2\177\u0081\7\17")
        buf.write("\2\2\u0080\177\3\2\2\2\u0080\u0081\3\2\2\2\u0081\u0082")
        buf.write("\3\2\2\2\u0082\u0083\7\f\2\2\u0083\u0084\3\2\2\2\u0084")
        buf.write("\u0085\b\16\2\2\u0085\34\3\2\2\2\u0086\u0087\7\61\2\2")
        buf.write("\u0087\u0088\7,\2\2\u0088\u008c\3\2\2\2\u0089\u008b\13")
        buf.write("\2\2\2\u008a\u0089\3\2\2\2\u008b\u008e\3\2\2\2\u008c\u008d")
        buf.write("\3\2\2\2\u008c\u008a\3\2\2\2\u008d\u008f\3\2\2\2\u008e")
        buf.write("\u008c\3\2\2\2\u008f\u0090\7,\2\2\u0090\u0091\7\61\2\2")
        buf.write("\u0091\u0092\3\2\2\2\u0092\u0093\b\17\2\2\u0093\36\3\2")
        buf.write("\2\2\u0094\u0095\t\b\2\2\u0095\u0096\3\2\2\2\u0096\u0097")
        buf.write("\b\20\2\2\u0097 \3\2\2\2\24\2\'+\60\659>DHMUZ^kq|\u0080")
        buf.write("\u008c\3\b\2\2")
        return buf.getvalue()


class commonLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    ID = 1
    INT = 2
    FLOAT = 3
    STRING = 4
    EOL_COMMENT = 5
    COMMENT = 6
    WS = 7

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
 ]

    symbolicNames = [ "<INVALID>",
            "ID", "INT", "FLOAT", "STRING", "EOL_COMMENT", "COMMENT", "WS" ]

    ruleNames = [ "ALPHA", "DIGIT", "ALNUM", "IDCHAR", "ID", "INT", "EXPT", 
                  "FLOAT", "STRING_CHAR", "HEX", "ESC_SEQ", "STRING", "EOL_COMMENT", 
                  "COMMENT", "WS" ]

    grammarFileName = "commonLexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


