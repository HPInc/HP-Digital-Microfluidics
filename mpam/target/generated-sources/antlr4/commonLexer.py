# Generated from commonLexer.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from erk.grid import Dir 



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\t")
        buf.write("\u009c\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\3\2\3\2\3\3\3")
        buf.write("\3\3\4\3\4\5\4*\n\4\3\5\3\5\5\5.\n\5\3\6\3\6\3\6\5\6\63")
        buf.write("\n\6\3\6\7\6\66\n\6\f\6\16\69\13\6\3\6\5\6<\n\6\3\7\6")
        buf.write("\7?\n\7\r\7\16\7@\3\7\3\7\6\7E\n\7\r\7\16\7F\7\7I\n\7")
        buf.write("\f\7\16\7L\13\7\3\b\3\b\5\bP\n\b\3\b\3\b\3\t\3\t\3\t\3")
        buf.write("\t\5\tX\n\t\3\t\3\t\3\t\5\t]\n\t\3\n\3\n\5\na\n\n\3\13")
        buf.write("\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\fn\n\f\3\r")
        buf.write("\3\r\3\16\3\16\7\16t\n\16\f\16\16\16w\13\16\3\16\3\16")
        buf.write("\3\17\3\17\3\17\3\17\7\17\177\n\17\f\17\16\17\u0082\13")
        buf.write("\17\3\17\5\17\u0085\n\17\3\17\3\17\3\17\3\17\3\20\3\20")
        buf.write("\3\20\3\20\7\20\u008f\n\20\f\20\16\20\u0092\13\20\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21\4\u0080\u0090")
        buf.write("\2\22\3\2\5\2\7\2\t\2\13\3\r\4\17\2\21\5\23\2\25\2\27")
        buf.write("\2\31\2\33\6\35\7\37\b!\t\3\2\n\4\2C\\c|\3\2\62;\4\2G")
        buf.write("Ggg\7\2\f\f\17\17$$^^\u201e\u201f\5\2\62;CHch\b\2$$))")
        buf.write("^^ppttvv\4\2$$\u201e\u201f\5\2\13\f\17\17\"\"\2\u00a3")
        buf.write("\2\13\3\2\2\2\2\r\3\2\2\2\2\21\3\2\2\2\2\33\3\2\2\2\2")
        buf.write("\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\3#\3\2\2\2\5%\3\2")
        buf.write("\2\2\7)\3\2\2\2\t-\3\2\2\2\13\62\3\2\2\2\r>\3\2\2\2\17")
        buf.write("M\3\2\2\2\21\\\3\2\2\2\23`\3\2\2\2\25b\3\2\2\2\27m\3\2")
        buf.write("\2\2\31o\3\2\2\2\33q\3\2\2\2\35z\3\2\2\2\37\u008a\3\2")
        buf.write("\2\2!\u0098\3\2\2\2#$\t\2\2\2$\4\3\2\2\2%&\t\3\2\2&\6")
        buf.write("\3\2\2\2\'*\5\3\2\2(*\5\5\3\2)\'\3\2\2\2)(\3\2\2\2*\b")
        buf.write("\3\2\2\2+.\5\7\4\2,.\7a\2\2-+\3\2\2\2-,\3\2\2\2.\n\3\2")
        buf.write("\2\2/\63\5\3\2\2\60\61\7a\2\2\61\63\5\t\5\2\62/\3\2\2")
        buf.write("\2\62\60\3\2\2\2\63\67\3\2\2\2\64\66\5\t\5\2\65\64\3\2")
        buf.write("\2\2\669\3\2\2\2\67\65\3\2\2\2\678\3\2\2\28;\3\2\2\29")
        buf.write("\67\3\2\2\2:<\7A\2\2;:\3\2\2\2;<\3\2\2\2<\f\3\2\2\2=?")
        buf.write("\5\5\3\2>=\3\2\2\2?@\3\2\2\2@>\3\2\2\2@A\3\2\2\2AJ\3\2")
        buf.write("\2\2BD\7a\2\2CE\5\5\3\2DC\3\2\2\2EF\3\2\2\2FD\3\2\2\2")
        buf.write("FG\3\2\2\2GI\3\2\2\2HB\3\2\2\2IL\3\2\2\2JH\3\2\2\2JK\3")
        buf.write("\2\2\2K\16\3\2\2\2LJ\3\2\2\2MO\t\4\2\2NP\7/\2\2ON\3\2")
        buf.write("\2\2OP\3\2\2\2PQ\3\2\2\2QR\5\r\7\2R\20\3\2\2\2ST\5\r\7")
        buf.write("\2TU\7\60\2\2UW\5\r\7\2VX\5\17\b\2WV\3\2\2\2WX\3\2\2\2")
        buf.write("X]\3\2\2\2YZ\5\r\7\2Z[\5\17\b\2[]\3\2\2\2\\S\3\2\2\2\\")
        buf.write("Y\3\2\2\2]\22\3\2\2\2^a\n\5\2\2_a\5\27\f\2`^\3\2\2\2`")
        buf.write("_\3\2\2\2a\24\3\2\2\2bc\t\6\2\2c\26\3\2\2\2de\7^\2\2e")
        buf.write("n\t\7\2\2fg\7^\2\2gh\7w\2\2hi\5\25\13\2ij\5\25\13\2jk")
        buf.write("\5\25\13\2kl\5\25\13\2ln\3\2\2\2md\3\2\2\2mf\3\2\2\2n")
        buf.write("\30\3\2\2\2op\t\b\2\2p\32\3\2\2\2qu\5\31\r\2rt\5\23\n")
        buf.write("\2sr\3\2\2\2tw\3\2\2\2us\3\2\2\2uv\3\2\2\2vx\3\2\2\2w")
        buf.write("u\3\2\2\2xy\5\31\r\2y\34\3\2\2\2z{\7\61\2\2{|\7\61\2\2")
        buf.write("|\u0080\3\2\2\2}\177\13\2\2\2~}\3\2\2\2\177\u0082\3\2")
        buf.write("\2\2\u0080\u0081\3\2\2\2\u0080~\3\2\2\2\u0081\u0084\3")
        buf.write("\2\2\2\u0082\u0080\3\2\2\2\u0083\u0085\7\17\2\2\u0084")
        buf.write("\u0083\3\2\2\2\u0084\u0085\3\2\2\2\u0085\u0086\3\2\2\2")
        buf.write("\u0086\u0087\7\f\2\2\u0087\u0088\3\2\2\2\u0088\u0089\b")
        buf.write("\17\2\2\u0089\36\3\2\2\2\u008a\u008b\7\61\2\2\u008b\u008c")
        buf.write("\7,\2\2\u008c\u0090\3\2\2\2\u008d\u008f\13\2\2\2\u008e")
        buf.write("\u008d\3\2\2\2\u008f\u0092\3\2\2\2\u0090\u0091\3\2\2\2")
        buf.write("\u0090\u008e\3\2\2\2\u0091\u0093\3\2\2\2\u0092\u0090\3")
        buf.write("\2\2\2\u0093\u0094\7,\2\2\u0094\u0095\7\61\2\2\u0095\u0096")
        buf.write("\3\2\2\2\u0096\u0097\b\20\2\2\u0097 \3\2\2\2\u0098\u0099")
        buf.write("\t\t\2\2\u0099\u009a\3\2\2\2\u009a\u009b\b\21\2\2\u009b")
        buf.write("\"\3\2\2\2\24\2)-\62\67;@FJOW\\`mu\u0080\u0084\u0090\3")
        buf.write("\b\2\2")
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
                  "FLOAT", "STRING_CHAR", "HEX", "ESC_SEQ", "DQ", "STRING", 
                  "EOL_COMMENT", "COMMENT", "WS" ]

    grammarFileName = "commonLexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


