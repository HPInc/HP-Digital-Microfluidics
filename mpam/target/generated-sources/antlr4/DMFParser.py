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
from quantities import SI


from mpam.types import Dir 


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3I")
        buf.write("\u0129\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\3\2\7\2$\n\2\f\2\16")
        buf.write("\2\'\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\5\3\65\n\3\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\5\5F\n\5\3\6\3\6\7\6J\n\6\f\6\16")
        buf.write("\6M\13\6\3\6\3\6\3\6\7\6R\n\6\f\6\16\6U\13\6\3\6\5\6X")
        buf.write("\n\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7n\n\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7{\n\7\3\7\3\7\3\7\5")
        buf.write("\7\u0080\n\7\3\7\5\7\u0083\n\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\7\7\u008e\n\7\f\7\16\7\u0091\13\7\5\7\u0093")
        buf.write("\n\7\3\7\3\7\3\7\3\7\5\7\u0099\n\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\7\7\u00b8\n")
        buf.write("\7\f\7\16\7\u00bb\13\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b")
        buf.write("\3\b\3\b\3\b\3\b\5\b\u00c9\n\b\3\t\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\5\t\u00d9\n\t\3\n\3\n")
        buf.write("\3\n\3\n\5\n\u00df\n\n\3\13\3\13\3\13\5\13\u00e4\n\13")
        buf.write("\3\f\3\f\3\f\3\f\3\f\7\f\u00eb\n\f\f\f\16\f\u00ee\13\f")
        buf.write("\5\f\u00f0\n\f\3\f\3\f\3\r\3\r\3\r\3\r\5\r\u00f8\n\r\3")
        buf.write("\r\3\r\3\r\3\r\3\r\3\r\5\r\u0100\n\r\3\16\3\16\3\16\3")
        buf.write("\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16")
        buf.write("\5\16\u011b\n\16\3\17\3\17\3\17\3\17\5\17\u0121\n\17\3")
        buf.write("\20\3\20\5\20\u0125\n\20\3\21\3\21\3\21\2\3\f\22\2\4\6")
        buf.write("\b\n\f\16\20\22\24\26\30\32\34\36 \2\20\3\2\26\27\3\2")
        buf.write(">?\4\2;;==\4\288@@\3\2\13\f\3\2\33\34\3\2\35\36\3\2\37")
        buf.write(" \3\2!\"\3\2%&\3\2\'(\3\2\60\64\3\2\65\67\4\2\60\60\65")
        buf.write("\65\2\u015b\2%\3\2\2\2\4\64\3\2\2\2\6\66\3\2\2\2\bE\3")
        buf.write("\2\2\2\nW\3\2\2\2\f\u0098\3\2\2\2\16\u00c8\3\2\2\2\20")
        buf.write("\u00d8\3\2\2\2\22\u00de\3\2\2\2\24\u00e0\3\2\2\2\26\u00e5")
        buf.write("\3\2\2\2\30\u00ff\3\2\2\2\32\u011a\3\2\2\2\34\u0120\3")
        buf.write("\2\2\2\36\u0124\3\2\2\2 \u0126\3\2\2\2\"$\5\b\5\2#\"\3")
        buf.write("\2\2\2$\'\3\2\2\2%#\3\2\2\2%&\3\2\2\2&(\3\2\2\2\'%\3\2")
        buf.write("\2\2()\7\2\2\3)\3\3\2\2\2*+\5\n\6\2+,\7\2\2\3,\65\3\2")
        buf.write("\2\2-.\5\6\4\2./\7\2\2\3/\65\3\2\2\2\60\61\5\f\7\2\61")
        buf.write("\62\7\2\2\3\62\65\3\2\2\2\63\65\7\2\2\3\64*\3\2\2\2\64")
        buf.write("-\3\2\2\2\64\60\3\2\2\2\64\63\3\2\2\2\65\5\3\2\2\2\66")
        buf.write("\67\5\36\20\2\678\79\2\289\5\f\7\29\7\3\2\2\2:;\5\6\4")
        buf.write("\2;<\7A\2\2<F\3\2\2\2=>\7\3\2\2>?\5\f\7\2?@\7A\2\2@F\3")
        buf.write("\2\2\2AB\5\f\7\2BC\7A\2\2CF\3\2\2\2DF\5\n\6\2E:\3\2\2")
        buf.write("\2E=\3\2\2\2EA\3\2\2\2ED\3\2\2\2F\t\3\2\2\2GK\7\4\2\2")
        buf.write("HJ\5\b\5\2IH\3\2\2\2JM\3\2\2\2KI\3\2\2\2KL\3\2\2\2LN\3")
        buf.write("\2\2\2MK\3\2\2\2NX\7\5\2\2OS\7\6\2\2PR\5\b\5\2QP\3\2\2")
        buf.write("\2RU\3\2\2\2SQ\3\2\2\2ST\3\2\2\2TV\3\2\2\2US\3\2\2\2V")
        buf.write("X\7\7\2\2WG\3\2\2\2WO\3\2\2\2X\13\3\2\2\2YZ\b\7\1\2Z[")
        buf.write("\7\b\2\2[\\\5\f\7\2\\]\7\t\2\2]\u0099\3\2\2\2^_\7\b\2")
        buf.write("\2_`\5\f\7\2`a\7\n\2\2ab\5\f\7\2bc\7\t\2\2c\u0099\3\2")
        buf.write("\2\2de\7@\2\2e\u0099\5\f\7\33fg\7D\2\2g\u0099\5\20\t\2")
        buf.write("hi\5\16\b\2ij\5\f\7\23j\u0099\3\2\2\2km\7\r\2\2ln\5\22")
        buf.write("\n\2ml\3\2\2\2mn\3\2\2\2no\3\2\2\2o\u0099\5\f\7\22pq\7")
        buf.write("\3\2\2q\u0099\5\f\7\21rs\7\16\2\2st\7\17\2\2t\u0099\5")
        buf.write("\f\7\20uv\7\25\2\2vw\t\2\2\2w\u0099\5\f\7\fx\u0099\5\24")
        buf.write("\13\2y{\7\30\2\2zy\3\2\2\2z{\3\2\2\2{|\3\2\2\2|\u0099")
        buf.write("\t\3\2\2}\177\7B\2\2~\u0080\7\31\2\2\177~\3\2\2\2\177")
        buf.write("\u0080\3\2\2\2\u0080\u0099\3\2\2\2\u0081\u0083\7\32\2")
        buf.write("\2\u0082\u0081\3\2\2\2\u0082\u0083\3\2\2\2\u0083\u0084")
        buf.write("\3\2\2\2\u0084\u0099\5\32\16\2\u0085\u0086\5\32\16\2\u0086")
        buf.write("\u0087\7D\2\2\u0087\u0099\3\2\2\2\u0088\u0089\5\36\20")
        buf.write("\2\u0089\u0092\7\b\2\2\u008a\u008f\5\f\7\2\u008b\u008c")
        buf.write("\7\n\2\2\u008c\u008e\5\f\7\2\u008d\u008b\3\2\2\2\u008e")
        buf.write("\u0091\3\2\2\2\u008f\u008d\3\2\2\2\u008f\u0090\3\2\2\2")
        buf.write("\u0090\u0093\3\2\2\2\u0091\u008f\3\2\2\2\u0092\u008a\3")
        buf.write("\2\2\2\u0092\u0093\3\2\2\2\u0093\u0094\3\2\2\2\u0094\u0095")
        buf.write("\7\t\2\2\u0095\u0099\3\2\2\2\u0096\u0099\5\36\20\2\u0097")
        buf.write("\u0099\7D\2\2\u0098Y\3\2\2\2\u0098^\3\2\2\2\u0098d\3\2")
        buf.write("\2\2\u0098f\3\2\2\2\u0098h\3\2\2\2\u0098k\3\2\2\2\u0098")
        buf.write("p\3\2\2\2\u0098r\3\2\2\2\u0098u\3\2\2\2\u0098x\3\2\2\2")
        buf.write("\u0098z\3\2\2\2\u0098}\3\2\2\2\u0098\u0082\3\2\2\2\u0098")
        buf.write("\u0085\3\2\2\2\u0098\u0088\3\2\2\2\u0098\u0096\3\2\2\2")
        buf.write("\u0098\u0097\3\2\2\2\u0099\u00b9\3\2\2\2\u009a\u009b\f")
        buf.write("\25\2\2\u009b\u009c\t\4\2\2\u009c\u00b8\5\f\7\26\u009d")
        buf.write("\u009e\f\24\2\2\u009e\u009f\t\5\2\2\u009f\u00b8\5\f\7")
        buf.write("\25\u00a0\u00a1\f\13\2\2\u00a1\u00a2\7<\2\2\u00a2\u00b8")
        buf.write("\5\f\7\f\u00a3\u00a4\f\32\2\2\u00a4\u00b8\5\16\b\2\u00a5")
        buf.write("\u00a6\f\30\2\2\u00a6\u00b8\5\20\t\2\u00a7\u00a8\f\27")
        buf.write("\2\2\u00a8\u00b8\5\34\17\2\u00a9\u00aa\f\26\2\2\u00aa")
        buf.write("\u00b8\t\6\2\2\u00ab\u00ac\f\17\2\2\u00ac\u00ad\7\20\2")
        buf.write("\2\u00ad\u00ae\5\f\7\2\u00ae\u00af\7\21\2\2\u00af\u00b8")
        buf.write("\3\2\2\2\u00b0\u00b1\f\16\2\2\u00b1\u00b2\7:\2\2\u00b2")
        buf.write("\u00b8\7\22\2\2\u00b3\u00b4\f\r\2\2\u00b4\u00b5\7:\2\2")
        buf.write("\u00b5\u00b6\7\23\2\2\u00b6\u00b8\7\24\2\2\u00b7\u009a")
        buf.write("\3\2\2\2\u00b7\u009d\3\2\2\2\u00b7\u00a0\3\2\2\2\u00b7")
        buf.write("\u00a3\3\2\2\2\u00b7\u00a5\3\2\2\2\u00b7\u00a7\3\2\2\2")
        buf.write("\u00b7\u00a9\3\2\2\2\u00b7\u00ab\3\2\2\2\u00b7\u00b0\3")
        buf.write("\2\2\2\u00b7\u00b3\3\2\2\2\u00b8\u00bb\3\2\2\2\u00b9\u00b7")
        buf.write("\3\2\2\2\u00b9\u00ba\3\2\2\2\u00ba\r\3\2\2\2\u00bb\u00b9")
        buf.write("\3\2\2\2\u00bc\u00bd\t\7\2\2\u00bd\u00be\b\b\1\2\u00be")
        buf.write("\u00c9\b\b\1\2\u00bf\u00c0\t\b\2\2\u00c0\u00c1\b\b\1\2")
        buf.write("\u00c1\u00c9\b\b\1\2\u00c2\u00c3\t\t\2\2\u00c3\u00c4\b")
        buf.write("\b\1\2\u00c4\u00c9\b\b\1\2\u00c5\u00c6\t\n\2\2\u00c6\u00c7")
        buf.write("\b\b\1\2\u00c7\u00c9\b\b\1\2\u00c8\u00bc\3\2\2\2\u00c8")
        buf.write("\u00bf\3\2\2\2\u00c8\u00c2\3\2\2\2\u00c8\u00c5\3\2\2\2")
        buf.write("\u00c9\17\3\2\2\2\u00ca\u00cb\6\t\f\3\u00cb\u00cc\7#\2")
        buf.write("\2\u00cc\u00cd\b\t\1\2\u00cd\u00d9\b\t\1\2\u00ce\u00cf")
        buf.write("\7$\2\2\u00cf\u00d0\b\t\1\2\u00d0\u00d9\b\t\1\2\u00d1")
        buf.write("\u00d2\6\t\r\3\u00d2\u00d3\t\13\2\2\u00d3\u00d4\b\t\1")
        buf.write("\2\u00d4\u00d9\b\t\1\2\u00d5\u00d6\t\f\2\2\u00d6\u00d7")
        buf.write("\b\t\1\2\u00d7\u00d9\b\t\1\2\u00d8\u00ca\3\2\2\2\u00d8")
        buf.write("\u00ce\3\2\2\2\u00d8\u00d1\3\2\2\2\u00d8\u00d5\3\2\2\2")
        buf.write("\u00d9\21\3\2\2\2\u00da\u00db\7#\2\2\u00db\u00df\b\n\1")
        buf.write("\2\u00dc\u00dd\t\13\2\2\u00dd\u00df\b\n\1\2\u00de\u00da")
        buf.write("\3\2\2\2\u00de\u00dc\3\2\2\2\u00df\23\3\2\2\2\u00e0\u00e3")
        buf.write("\5\26\f\2\u00e1\u00e4\5\n\6\2\u00e2\u00e4\5\f\7\2\u00e3")
        buf.write("\u00e1\3\2\2\2\u00e3\u00e2\3\2\2\2\u00e4\25\3\2\2\2\u00e5")
        buf.write("\u00e6\7)\2\2\u00e6\u00ef\7\b\2\2\u00e7\u00ec\5\30\r\2")
        buf.write("\u00e8\u00e9\7\n\2\2\u00e9\u00eb\5\30\r\2\u00ea\u00e8")
        buf.write("\3\2\2\2\u00eb\u00ee\3\2\2\2\u00ec\u00ea\3\2\2\2\u00ec")
        buf.write("\u00ed\3\2\2\2\u00ed\u00f0\3\2\2\2\u00ee\u00ec\3\2\2\2")
        buf.write("\u00ef\u00e7\3\2\2\2\u00ef\u00f0\3\2\2\2\u00f0\u00f1\3")
        buf.write("\2\2\2\u00f1\u00f2\7\t\2\2\u00f2\27\3\2\2\2\u00f3\u00f4")
        buf.write("\5\32\16\2\u00f4\u00f7\b\r\1\2\u00f5\u00f6\7D\2\2\u00f6")
        buf.write("\u00f8\b\r\1\2\u00f7\u00f5\3\2\2\2\u00f7\u00f8\3\2\2\2")
        buf.write("\u00f8\u0100\3\2\2\2\u00f9\u00fa\5\36\20\2\u00fa\u00fb")
        buf.write("\7<\2\2\u00fb\u00fc\5\32\16\2\u00fc\u00fd\b\r\1\2\u00fd")
        buf.write("\u00fe\b\r\1\2\u00fe\u0100\3\2\2\2\u00ff\u00f3\3\2\2\2")
        buf.write("\u00ff\u00f9\3\2\2\2\u0100\31\3\2\2\2\u0101\u0102\7\25")
        buf.write("\2\2\u0102\u011b\b\16\1\2\u0103\u0104\7\24\2\2\u0104\u011b")
        buf.write("\b\16\1\2\u0105\u0106\7\16\2\2\u0106\u011b\b\16\1\2\u0107")
        buf.write("\u0108\7\16\2\2\u0108\u0109\7\24\2\2\u0109\u011b\b\16")
        buf.write("\1\2\u010a\u010b\7*\2\2\u010b\u011b\b\16\1\2\u010c\u010d")
        buf.write("\7\31\2\2\u010d\u011b\b\16\1\2\u010e\u010f\7+\2\2\u010f")
        buf.write("\u011b\b\16\1\2\u0110\u0111\7,\2\2\u0111\u011b\b\16\1")
        buf.write("\2\u0112\u0113\7-\2\2\u0113\u011b\b\16\1\2\u0114\u0115")
        buf.write("\7.\2\2\u0115\u011b\b\16\1\2\u0116\u0117\7/\2\2\u0117")
        buf.write("\u011b\b\16\1\2\u0118\u0119\7\f\2\2\u0119\u011b\b\16\1")
        buf.write("\2\u011a\u0101\3\2\2\2\u011a\u0103\3\2\2\2\u011a\u0105")
        buf.write("\3\2\2\2\u011a\u0107\3\2\2\2\u011a\u010a\3\2\2\2\u011a")
        buf.write("\u010c\3\2\2\2\u011a\u010e\3\2\2\2\u011a\u0110\3\2\2\2")
        buf.write("\u011a\u0112\3\2\2\2\u011a\u0114\3\2\2\2\u011a\u0116\3")
        buf.write("\2\2\2\u011a\u0118\3\2\2\2\u011b\33\3\2\2\2\u011c\u011d")
        buf.write("\t\r\2\2\u011d\u0121\b\17\1\2\u011e\u011f\t\16\2\2\u011f")
        buf.write("\u0121\b\17\1\2\u0120\u011c\3\2\2\2\u0120\u011e\3\2\2")
        buf.write("\2\u0121\35\3\2\2\2\u0122\u0125\7C\2\2\u0123\u0125\5 ")
        buf.write("\21\2\u0124\u0122\3\2\2\2\u0124\u0123\3\2\2\2\u0125\37")
        buf.write("\3\2\2\2\u0126\u0127\t\17\2\2\u0127!\3\2\2\2\34%\64EK")
        buf.write("SWmz\177\u0082\u008f\u0092\u0098\u00b7\u00b9\u00c8\u00d8")
        buf.write("\u00de\u00e3\u00ec\u00ef\u00f7\u00ff\u011a\u0120\u0124")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'pause'", "'{'", "'}'", "'[['", "']]'", 
                     "'('", "')'", "','", "'tick'", "'ticks'", "'to'", "'well'", 
                     "'#'", "'['", "']'", "'gate'", "'exit'", "'pad'", "'drop'", 
                     "'@'", "'at'", "'turn'", "'state'", "'the'", "'up'", 
                     "'north'", "'down'", "'south'", "'left'", "'west'", 
                     "'right'", "'east'", "'row'", "'rows'", "'col'", "'column'", 
                     "'cols'", "'columns'", "'macro'", "'int'", "'component'", 
                     "'delta'", "'motion'", "'delay'", "'time'", "'s'", 
                     "'sec'", "'secs'", "'second'", "'seconds'", "'ms'", 
                     "'millisecond'", "'milliseconds'", "'+'", "'='", "''s'", 
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
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "ADD", "ASSIGN", "ATTR", 
                      "DIV", "INJECT", "MUL", "OFF", "ON", "SUB", "TERMINATOR", 
                      "TOGGLE", "ID", "INT", "FLOAT", "STRING", "EOL_COMMENT", 
                      "COMMENT", "WS" ]

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
    RULE_time_unit = 13
    RULE_name = 14
    RULE_kwd_names = 15

    ruleNames =  [ "macro_file", "interactive", "assignment", "stat", "compound", 
                   "expr", "direction", "rc", "axis", "macro_def", "macro_header", 
                   "param", "param_type", "time_unit", "name", "kwd_names" ]

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
    T__38=39
    T__39=40
    T__40=41
    T__41=42
    T__42=43
    T__43=44
    T__44=45
    T__45=46
    T__46=47
    T__47=48
    T__48=49
    T__49=50
    T__50=51
    T__51=52
    T__52=53
    ADD=54
    ASSIGN=55
    ATTR=56
    DIV=57
    INJECT=58
    MUL=59
    OFF=60
    ON=61
    SUB=62
    TERMINATOR=63
    TOGGLE=64
    ID=65
    INT=66
    FLOAT=67
    STRING=68
    EOL_COMMENT=69
    COMMENT=70
    WS=71

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
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__9) | (1 << DMFParser.T__10) | (1 << DMFParser.T__11) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__50) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.TOGGLE - 64)) | (1 << (DMFParser.ID - 64)) | (1 << (DMFParser.INT - 64)))) != 0):
                self.state = 32
                self.stat()
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
            self.state = 50
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
                localctx = DMFParser.Empty_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 49
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
            self.state = 52
            localctx.which = self.name()
            self.state = 53
            self.match(DMFParser.ASSIGN)
            self.state = 54
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


    class Pause_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.duration = None # ExprContext
            self.copyFrom(ctx)

        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)
        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPause_stat" ):
                listener.enterPause_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPause_stat" ):
                listener.exitPause_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPause_stat" ):
                return visitor.visitPause_stat(self)
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
            self.state = 67
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Assign_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 56
                self.assignment()
                self.state = 57
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Pause_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.match(DMFParser.T__0)
                self.state = 60
                localctx.duration = self.expr(0)
                self.state = 61
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 3:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 63
                self.expr(0)
                self.state = 64
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 4:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 66
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
            self.state = 85
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__1]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 69
                self.match(DMFParser.T__1)
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__9) | (1 << DMFParser.T__10) | (1 << DMFParser.T__11) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__50) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.TOGGLE - 64)) | (1 << (DMFParser.ID - 64)) | (1 << (DMFParser.INT - 64)))) != 0):
                    self.state = 70
                    self.stat()
                    self.state = 75
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 76
                self.match(DMFParser.T__2)
                pass
            elif token in [DMFParser.T__3]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 77
                self.match(DMFParser.T__3)
                self.state = 81
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__9) | (1 << DMFParser.T__10) | (1 << DMFParser.T__11) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__50) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.TOGGLE - 64)) | (1 << (DMFParser.ID - 64)) | (1 << (DMFParser.INT - 64)))) != 0):
                    self.state = 78
                    self.stat()
                    self.state = 83
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 84
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


    class Time_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.duration = None # ExprContext
            self.copyFrom(ctx)

        def time_unit(self):
            return self.getTypedRuleContext(DMFParser.Time_unitContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTime_expr" ):
                listener.enterTime_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTime_expr" ):
                listener.exitTime_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTime_expr" ):
                return visitor.visitTime_expr(self)
            else:
                return visitor.visitChildren(self)


    class Ticks_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.duration = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTicks_expr" ):
                listener.enterTicks_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTicks_expr" ):
                listener.exitTicks_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTicks_expr" ):
                return visitor.visitTicks_expr(self)
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


    class Pause_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.duration = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPause_expr" ):
                listener.enterPause_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPause_expr" ):
                listener.exitPause_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPause_expr" ):
                return visitor.visitPause_expr(self)
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
            self.state = 150
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 88
                self.match(DMFParser.T__5)
                self.state = 89
                self.expr(0)
                self.state = 90
                self.match(DMFParser.T__6)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 92
                self.match(DMFParser.T__5)
                self.state = 93
                localctx.x = self.expr(0)
                self.state = 94
                self.match(DMFParser.T__7)
                self.state = 95
                localctx.y = self.expr(0)
                self.state = 96
                self.match(DMFParser.T__6)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 98
                self.match(DMFParser.SUB)
                self.state = 99
                localctx.rhs = self.expr(25)
                pass

            elif la_ == 4:
                localctx = DMFParser.Const_rc_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 100
                localctx._INT = self.match(DMFParser.INT)
                self.state = 101
                self.rc((0 if localctx._INT is None else int(localctx._INT.text)))
                pass

            elif la_ == 5:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 102
                self.direction()
                self.state = 103
                localctx.dist = self.expr(17)
                pass

            elif la_ == 6:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 105
                self.match(DMFParser.T__10)
                self.state = 107
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__32) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35))) != 0):
                    self.state = 106
                    self.axis()


                self.state = 109
                localctx.which = self.expr(16)
                pass

            elif la_ == 7:
                localctx = DMFParser.Pause_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 110
                self.match(DMFParser.T__0)
                self.state = 111
                localctx.duration = self.expr(15)
                pass

            elif la_ == 8:
                localctx = DMFParser.Well_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 112
                self.match(DMFParser.T__11)
                self.state = 113
                self.match(DMFParser.T__12)
                self.state = 114
                localctx.which = self.expr(14)
                pass

            elif la_ == 9:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 115
                self.match(DMFParser.T__18)
                self.state = 116
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__19 or _la==DMFParser.T__20):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 117
                localctx.loc = self.expr(10)
                pass

            elif la_ == 10:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 118
                self.macro_def()
                pass

            elif la_ == 11:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__21:
                    self.state = 119
                    self.match(DMFParser.T__21)


                self.state = 122
                _la = self._input.LA(1)
                if not(_la==DMFParser.OFF or _la==DMFParser.ON):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 12:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 123
                self.match(DMFParser.TOGGLE)
                self.state = 125
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                if la_ == 1:
                    self.state = 124
                    self.match(DMFParser.T__22)


                pass

            elif la_ == 13:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 128
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__23:
                    self.state = 127
                    self.match(DMFParser.T__23)


                self.state = 130
                self.param_type()
                pass

            elif la_ == 14:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 131
                self.param_type()
                self.state = 132
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 15:
                localctx = DMFParser.Function_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 134
                self.name()
                self.state = 135
                self.match(DMFParser.T__5)
                self.state = 144
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__5) | (1 << DMFParser.T__9) | (1 << DMFParser.T__10) | (1 << DMFParser.T__11) | (1 << DMFParser.T__17) | (1 << DMFParser.T__18) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__50) | (1 << DMFParser.OFF) | (1 << DMFParser.ON) | (1 << DMFParser.SUB))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.TOGGLE - 64)) | (1 << (DMFParser.ID - 64)) | (1 << (DMFParser.INT - 64)))) != 0):
                    self.state = 136
                    localctx._expr = self.expr(0)
                    localctx.args.append(localctx._expr)
                    self.state = 141
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==DMFParser.T__7:
                        self.state = 137
                        self.match(DMFParser.T__7)
                        self.state = 138
                        localctx._expr = self.expr(0)
                        localctx.args.append(localctx._expr)
                        self.state = 143
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 146
                self.match(DMFParser.T__6)
                pass

            elif la_ == 16:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 148
                self.name()
                pass

            elif la_ == 17:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 149
                localctx._INT = self.match(DMFParser.INT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 183
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 181
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 152
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 153
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 154
                        localctx.rhs = self.expr(20)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 155
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 156
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 157
                        localctx.rhs = self.expr(19)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 158
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 159
                        self.match(DMFParser.INJECT)
                        self.state = 160
                        localctx.what = self.expr(10)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 161
                        if not self.precpred(self._ctx, 24):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 24)")
                        self.state = 162
                        self.direction()
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.N_rc_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 163
                        if not self.precpred(self._ctx, 22):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 22)")
                        self.state = 164
                        self.rc(0)
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Time_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.duration = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 165
                        if not self.precpred(self._ctx, 21):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 21)")
                        self.state = 166
                        self.time_unit()
                        pass

                    elif la_ == 7:
                        localctx = DMFParser.Ticks_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.duration = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 167
                        if not self.precpred(self._ctx, 20):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 20)")
                        self.state = 168
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__8 or _la==DMFParser.T__9):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        pass

                    elif la_ == 8:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 169
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 170
                        self.match(DMFParser.T__13)
                        self.state = 171
                        localctx.which = self.expr(0)
                        self.state = 172
                        self.match(DMFParser.T__14)
                        pass

                    elif la_ == 9:
                        localctx = DMFParser.Gate_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.well = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 174
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 175
                        self.match(DMFParser.ATTR)
                        self.state = 176
                        self.match(DMFParser.T__15)
                        pass

                    elif la_ == 10:
                        localctx = DMFParser.Exit_pad_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.well = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 177
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 178
                        self.match(DMFParser.ATTR)
                        self.state = 179
                        self.match(DMFParser.T__16)
                        self.state = 180
                        self.match(DMFParser.T__17)
                        pass

             
                self.state = 185
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
            self.state = 198
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__24, DMFParser.T__25]:
                self.enterOuterAlt(localctx, 1)
                self.state = 186
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__24 or _la==DMFParser.T__25):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__26, DMFParser.T__27]:
                self.enterOuterAlt(localctx, 2)
                self.state = 189
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__26 or _la==DMFParser.T__27):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__28, DMFParser.T__29]:
                self.enterOuterAlt(localctx, 3)
                self.state = 192
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__28 or _la==DMFParser.T__29):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__30, DMFParser.T__31]:
                self.enterOuterAlt(localctx, 4)
                self.state = 195
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__30 or _la==DMFParser.T__31):
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
            self.state = 214
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 200
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 201
                self.match(DMFParser.T__32)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 204
                self.match(DMFParser.T__33)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 207
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 208
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__34 or _la==DMFParser.T__35):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 211
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__36 or _la==DMFParser.T__37):
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
            self.state = 220
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__32]:
                self.enterOuterAlt(localctx, 1)
                self.state = 216
                self.match(DMFParser.T__32)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__34, DMFParser.T__35]:
                self.enterOuterAlt(localctx, 2)
                self.state = 218
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__34 or _la==DMFParser.T__35):
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
            self.state = 222
            self.macro_header()
            self.state = 225
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__1, DMFParser.T__3]:
                self.state = 223
                self.compound()
                pass
            elif token in [DMFParser.T__0, DMFParser.T__5, DMFParser.T__9, DMFParser.T__10, DMFParser.T__11, DMFParser.T__17, DMFParser.T__18, DMFParser.T__21, DMFParser.T__22, DMFParser.T__23, DMFParser.T__24, DMFParser.T__25, DMFParser.T__26, DMFParser.T__27, DMFParser.T__28, DMFParser.T__29, DMFParser.T__30, DMFParser.T__31, DMFParser.T__38, DMFParser.T__39, DMFParser.T__40, DMFParser.T__41, DMFParser.T__42, DMFParser.T__43, DMFParser.T__44, DMFParser.T__45, DMFParser.T__50, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT]:
                self.state = 224
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
            self.state = 227
            self.match(DMFParser.T__38)
            self.state = 228
            self.match(DMFParser.T__5)
            self.state = 237
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 10)) & ~0x3f) == 0 and ((1 << (_la - 10)) & ((1 << (DMFParser.T__9 - 10)) | (1 << (DMFParser.T__11 - 10)) | (1 << (DMFParser.T__17 - 10)) | (1 << (DMFParser.T__18 - 10)) | (1 << (DMFParser.T__22 - 10)) | (1 << (DMFParser.T__39 - 10)) | (1 << (DMFParser.T__40 - 10)) | (1 << (DMFParser.T__41 - 10)) | (1 << (DMFParser.T__42 - 10)) | (1 << (DMFParser.T__43 - 10)) | (1 << (DMFParser.T__44 - 10)) | (1 << (DMFParser.T__45 - 10)) | (1 << (DMFParser.T__50 - 10)) | (1 << (DMFParser.ID - 10)))) != 0):
                self.state = 229
                self.param()
                self.state = 234
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__7:
                    self.state = 230
                    self.match(DMFParser.T__7)
                    self.state = 231
                    self.param()
                    self.state = 236
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 239
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
        self.enterRule(localctx, 22, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.state = 253
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__9, DMFParser.T__11, DMFParser.T__17, DMFParser.T__18, DMFParser.T__22, DMFParser.T__39, DMFParser.T__40, DMFParser.T__41, DMFParser.T__42, DMFParser.T__43, DMFParser.T__44]:
                self.enterOuterAlt(localctx, 1)
                self.state = 241
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 245
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.INT:
                    self.state = 243
                    localctx._INT = self.match(DMFParser.INT)
                    localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))


                pass
            elif token in [DMFParser.T__45, DMFParser.T__50, DMFParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 247
                localctx._name = self.name()
                self.state = 248
                self.match(DMFParser.INJECT)
                self.state = 249
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
            self.state = 280
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 255
                self.match(DMFParser.T__18)
                localctx.type=Type.DROP
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 257
                self.match(DMFParser.T__17)
                localctx.type=Type.PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 259
                self.match(DMFParser.T__11)
                localctx.type=Type.WELL
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 261
                self.match(DMFParser.T__11)
                self.state = 262
                self.match(DMFParser.T__17)
                localctx.type=Type.WELL_PAD
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 264
                self.match(DMFParser.T__39)
                localctx.type=Type.INT
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 266
                self.match(DMFParser.T__22)
                localctx.type=Type.BINARY_STATE
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 268
                self.match(DMFParser.T__40)
                localctx.type=Type.BINARY_CPT
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 270
                self.match(DMFParser.T__41)
                localctx.type=Type.DELTA
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 272
                self.match(DMFParser.T__42)
                localctx.type=Type.MOTION
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 274
                self.match(DMFParser.T__43)
                localctx.type=Type.DELAY
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 276
                self.match(DMFParser.T__44)
                localctx.type=Type.TIME
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 278
                self.match(DMFParser.T__9)
                localctx.type=Type.TICKS
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Time_unitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.unit = None


        def getRuleIndex(self):
            return DMFParser.RULE_time_unit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTime_unit" ):
                listener.enterTime_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTime_unit" ):
                listener.exitTime_unit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTime_unit" ):
                return visitor.visitTime_unit(self)
            else:
                return visitor.visitChildren(self)




    def time_unit(self):

        localctx = DMFParser.Time_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_time_unit)
        self._la = 0 # Token type
        try:
            self.state = 286
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__45, DMFParser.T__46, DMFParser.T__47, DMFParser.T__48, DMFParser.T__49]:
                self.enterOuterAlt(localctx, 1)
                self.state = 282
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.sec
                pass
            elif token in [DMFParser.T__50, DMFParser.T__51, DMFParser.T__52]:
                self.enterOuterAlt(localctx, 2)
                self.state = 284
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.ms
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
            self.state = 290
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.ID]:
                self.state = 288
                self.match(DMFParser.ID)
                pass
            elif token in [DMFParser.T__45, DMFParser.T__50]:
                self.state = 289
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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 292
            _la = self._input.LA(1)
            if not(_la==DMFParser.T__45 or _la==DMFParser.T__50):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
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
                return self.precpred(self._ctx, 19)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 24)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 22)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 21)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 20)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 11)
         

    def rc_sempred(self, localctx:RcContext, predIndex:int):
            if predIndex == 10:
                return localctx.n==1
         

            if predIndex == 11:
                return localctx.n==1
         




