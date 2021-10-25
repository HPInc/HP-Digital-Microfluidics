# Generated from pathLexer.g4 by ANTLR 4.9.2
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
        buf.write("\u009a\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\3\2\3\2\3\3\3\3\3\4\3\4")
        buf.write("\5\4(\n\4\3\5\3\5\5\5,\n\5\3\6\3\6\3\6\5\6\61\n\6\3\6")
        buf.write("\7\6\64\n\6\f\6\16\6\67\13\6\3\6\5\6:\n\6\3\7\6\7=\n\7")
        buf.write("\r\7\16\7>\3\7\3\7\6\7C\n\7\r\7\16\7D\7\7G\n\7\f\7\16")
        buf.write("\7J\13\7\3\b\3\b\5\bN\n\b\3\b\3\b\3\t\3\t\3\t\5\tU\n\t")
        buf.write("\3\t\5\tX\n\t\3\t\3\t\3\t\5\t]\n\t\3\n\3\n\5\na\n\n\3")
        buf.write("\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\fn\n\f")
        buf.write("\3\r\3\r\7\rr\n\r\f\r\16\ru\13\r\3\r\3\r\3\16\3\16\3\16")
        buf.write("\3\16\7\16}\n\16\f\16\16\16\u0080\13\16\3\16\5\16\u0083")
        buf.write("\n\16\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17\7\17\u008d")
        buf.write("\n\17\f\17\16\17\u0090\13\17\3\17\3\17\3\17\3\17\3\17")
        buf.write("\3\20\3\20\3\20\3\20\4~\u008e\2\21\3\2\5\2\7\2\t\2\13")
        buf.write("\3\r\4\17\2\21\5\23\2\25\2\27\2\31\6\33\7\35\b\37\t\3")
        buf.write("\2\t\4\2C\\c|\3\2\62;\4\2GGgg\6\2\f\f\17\17$$^^\5\2\62")
        buf.write(";CHch\b\2$$))^^ppttvv\5\2\13\f\17\17\"\"\2\u00a3\2\13")
        buf.write("\3\2\2\2\2\r\3\2\2\2\2\21\3\2\2\2\2\31\3\2\2\2\2\33\3")
        buf.write("\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\3!\3\2\2\2\5#\3\2\2\2")
        buf.write("\7\'\3\2\2\2\t+\3\2\2\2\13\60\3\2\2\2\r<\3\2\2\2\17K\3")
        buf.write("\2\2\2\21\\\3\2\2\2\23`\3\2\2\2\25b\3\2\2\2\27m\3\2\2")
        buf.write("\2\31o\3\2\2\2\33x\3\2\2\2\35\u0088\3\2\2\2\37\u0096\3")
        buf.write("\2\2\2!\"\t\2\2\2\"\4\3\2\2\2#$\t\3\2\2$\6\3\2\2\2%(\5")
        buf.write("\3\2\2&(\5\5\3\2\'%\3\2\2\2\'&\3\2\2\2(\b\3\2\2\2),\5")
        buf.write("\7\4\2*,\7a\2\2+)\3\2\2\2+*\3\2\2\2,\n\3\2\2\2-\61\5\3")
        buf.write("\2\2./\7a\2\2/\61\5\t\5\2\60-\3\2\2\2\60.\3\2\2\2\61\65")
        buf.write("\3\2\2\2\62\64\5\t\5\2\63\62\3\2\2\2\64\67\3\2\2\2\65")
        buf.write("\63\3\2\2\2\65\66\3\2\2\2\669\3\2\2\2\67\65\3\2\2\28:")
        buf.write("\7A\2\298\3\2\2\29:\3\2\2\2:\f\3\2\2\2;=\5\5\3\2<;\3\2")
        buf.write("\2\2=>\3\2\2\2><\3\2\2\2>?\3\2\2\2?H\3\2\2\2@B\7a\2\2")
        buf.write("AC\5\5\3\2BA\3\2\2\2CD\3\2\2\2DB\3\2\2\2DE\3\2\2\2EG\3")
        buf.write("\2\2\2F@\3\2\2\2GJ\3\2\2\2HF\3\2\2\2HI\3\2\2\2I\16\3\2")
        buf.write("\2\2JH\3\2\2\2KM\t\4\2\2LN\7/\2\2ML\3\2\2\2MN\3\2\2\2")
        buf.write("NO\3\2\2\2OP\5\r\7\2P\20\3\2\2\2QR\5\r\7\2RT\7\60\2\2")
        buf.write("SU\5\r\7\2TS\3\2\2\2TU\3\2\2\2UW\3\2\2\2VX\5\17\b\2WV")
        buf.write("\3\2\2\2WX\3\2\2\2X]\3\2\2\2YZ\5\r\7\2Z[\5\17\b\2[]\3")
        buf.write("\2\2\2\\Q\3\2\2\2\\Y\3\2\2\2]\22\3\2\2\2^a\n\5\2\2_a\5")
        buf.write("\27\f\2`^\3\2\2\2`_\3\2\2\2a\24\3\2\2\2bc\t\6\2\2c\26")
        buf.write("\3\2\2\2de\7^\2\2en\t\7\2\2fg\7^\2\2gh\7w\2\2hi\5\25\13")
        buf.write("\2ij\5\25\13\2jk\5\25\13\2kl\5\25\13\2ln\3\2\2\2md\3\2")
        buf.write("\2\2mf\3\2\2\2n\30\3\2\2\2os\7$\2\2pr\5\23\n\2qp\3\2\2")
        buf.write("\2ru\3\2\2\2sq\3\2\2\2st\3\2\2\2tv\3\2\2\2us\3\2\2\2v")
        buf.write("w\7$\2\2w\32\3\2\2\2xy\7\61\2\2yz\7\61\2\2z~\3\2\2\2{")
        buf.write("}\13\2\2\2|{\3\2\2\2}\u0080\3\2\2\2~\177\3\2\2\2~|\3\2")
        buf.write("\2\2\177\u0082\3\2\2\2\u0080~\3\2\2\2\u0081\u0083\7\17")
        buf.write("\2\2\u0082\u0081\3\2\2\2\u0082\u0083\3\2\2\2\u0083\u0084")
        buf.write("\3\2\2\2\u0084\u0085\7\f\2\2\u0085\u0086\3\2\2\2\u0086")
        buf.write("\u0087\b\16\2\2\u0087\34\3\2\2\2\u0088\u0089\7\61\2\2")
        buf.write("\u0089\u008a\7,\2\2\u008a\u008e\3\2\2\2\u008b\u008d\13")
        buf.write("\2\2\2\u008c\u008b\3\2\2\2\u008d\u0090\3\2\2\2\u008e\u008f")
        buf.write("\3\2\2\2\u008e\u008c\3\2\2\2\u008f\u0091\3\2\2\2\u0090")
        buf.write("\u008e\3\2\2\2\u0091\u0092\7,\2\2\u0092\u0093\7\61\2\2")
        buf.write("\u0093\u0094\3\2\2\2\u0094\u0095\b\17\2\2\u0095\36\3\2")
        buf.write("\2\2\u0096\u0097\t\b\2\2\u0097\u0098\3\2\2\2\u0098\u0099")
        buf.write("\b\20\2\2\u0099 \3\2\2\2\25\2\'+\60\659>DHMTW\\`ms~\u0082")
        buf.write("\u008e\3\b\2\2")
        return buf.getvalue()


class pathLexer(Lexer):

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

    grammarFileName = "pathLexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


