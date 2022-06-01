# Generated from DMF.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


from mpam.types import Dir, OnOff, Turn, ticks, unknown_reagent, waste_reagent
from langsup.type_supp import Type, Rel, PhysUnit, EnvRelativeUnit, NumberedItem
from quantities import SI


from mpam.types import Dir 


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\u00b9")
        buf.write("\u02eb\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\3\2\7\2>\n\2\f\2\16\2A\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3")
        buf.write("\3\5\3J\n\3\3\3\3\3\3\3\3\3\5\3P\n\3\3\3\3\3\3\3\3\3\5")
        buf.write("\3V\n\3\3\3\3\3\3\3\5\3[\n\3\3\4\3\4\3\4\3\4\3\4\3\4\3")
        buf.write("\4\3\4\5\4e\n\4\3\4\3\4\3\4\3\4\5\4k\n\4\3\4\3\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4w\n\4\3\4\3\4\3\4\3\4\5")
        buf.write("\4}\n\4\3\4\3\4\3\4\5\4\u0082\n\4\3\5\3\5\3\5\3\5\7\5")
        buf.write("\u0088\n\5\f\5\16\5\u008b\13\5\3\6\3\6\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6\u009f")
        buf.write("\n\6\f\6\16\6\u00a2\13\6\3\6\3\6\5\6\u00a6\n\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\5\6\u00ad\n\6\3\7\3\7\7\7\u00b1\n\7\f\7\16")
        buf.write("\7\u00b4\13\7\3\7\3\7\3\7\7\7\u00b9\n\7\f\7\16\7\u00bc")
        buf.write("\13\7\3\7\5\7\u00bf\n\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3")
        buf.write("\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\b\u00d3\n")
        buf.write("\b\3\t\3\t\3\t\3\t\5\t\u00d9\n\t\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\5\n\u00ef\n\n\3\n\3\n\5\n\u00f3\n\n\3\n\5\n\u00f6")
        buf.write("\n\n\3\n\3\n\5\n\u00fa\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\5\n\u0105\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\5\n\u0110\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u0125\n\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u013b\n\n\3\n\5\n\u013e")
        buf.write("\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\7\n\u015e\n\n\f\n\16\n\u0161\13\n\5\n")
        buf.write("\u0163\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\5\n\u0170\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\7\n\u018a\n\n\f\n\16\n\u018d\13\n\3\13\3\13\3\13\3")
        buf.write("\13\5\13\u0193\n\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\5\f\u01a1\n\f\3\r\3\r\3\r\3\r\3\r\3\r\5")
        buf.write("\r\u01a9\n\r\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3")
        buf.write("\16\3\16\3\16\3\16\3\16\3\16\5\16\u01b9\n\16\3\17\3\17")
        buf.write("\3\17\3\17\5\17\u01bf\n\17\3\20\3\20\3\20\5\20\u01c4\n")
        buf.write("\20\3\21\3\21\3\21\3\21\3\21\7\21\u01cb\n\21\f\21\16\21")
        buf.write("\u01ce\13\21\5\21\u01d0\n\21\3\21\3\21\3\22\5\22\u01d5")
        buf.write("\n\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22")
        buf.write("\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\5\22")
        buf.write("\u01eb\n\22\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\5")
        buf.write("\23\u01f5\n\23\3\23\3\23\3\23\3\23\5\23\u01fb\n\23\3\23")
        buf.write("\5\23\u01fe\n\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3")
        buf.write("\23\3\23\3\23\3\23\3\23\3\23\5\23\u020d\n\23\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\5\24\u0219\n")
        buf.write("\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\5\24\u0240\n\24\3\24\3\24\3")
        buf.write("\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\5\24\u024f\n\24\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u025f\n\25\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\5\26\u0267\n\26\3\27\3\27\3")
        buf.write("\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\5\27\u0273\n\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\5\27\u027a\n\27\3\27\3\27\3")
        buf.write("\27\3\27\3\27\3\27\3\27\3\27\3\27\5\27\u0285\n\27\3\27")
        buf.write("\3\27\5\27\u0289\n\27\3\27\3\27\3\27\3\27\3\27\3\27\3")
        buf.write("\27\3\27\3\27\3\27\3\27\3\27\3\27\5\27\u0298\n\27\3\30")
        buf.write("\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30")
        buf.write("\5\30\u02a6\n\30\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3")
        buf.write("\31\3\31\3\31\5\31\u02b2\n\31\3\32\3\32\3\32\3\32\5\32")
        buf.write("\u02b8\n\32\3\33\3\33\3\33\3\33\3\33\3\33\3\33\3\33\5")
        buf.write("\33\u02c2\n\33\3\34\3\34\5\34\u02c6\n\34\3\34\3\34\3\34")
        buf.write("\5\34\u02cb\n\34\3\34\3\34\3\34\3\34\5\34\u02d1\n\34\3")
        buf.write("\34\3\34\3\34\3\34\3\34\3\34\3\34\5\34\u02da\n\34\3\34")
        buf.write("\3\34\3\34\3\34\3\34\3\34\3\34\3\34\3\34\5\34\u02e5\n")
        buf.write("\34\3\35\3\35\3\36\3\36\3\36\2\3\22\37\2\4\6\b\n\f\16")
        buf.write("\20\22\24\26\30\32\34\36 \"$&(*,.\60\62\64\668:\2!\3\2")
        buf.write("\5\6\4\2\27\27\35\35\3\2()\3\2\32\33\4\2\u00a5\u00a5\u00aa")
        buf.write("\u00aa\4\2\u00a2\u00a2\u00ae\u00ae\4\2\27\27\"\"\3\2,")
        buf.write("-\3\2./\3\2\60\61\3\2\62\63\4\2\62\62\64\64\4\2\60\60")
        buf.write("\65\65\3\29:\3\2;<\3\2VW\4\2NNXY\3\2ae\3\2fh\3\2in\3\2")
        buf.write("ot\4\2RRuu\4\2\'\'vv\3\2wy\3\2|}\3\2\u0083\u0084\3\2\u0086")
        buf.write("\u0087\n\2\36\36\'\'??HITT[\\``\u00b3\u00b3\3\2\u0092")
        buf.write("\u0097\3\2\u0098\u009d\r\2CGNNXZaaff{{~~\u0083\u0084\u0086")
        buf.write("\u0087\u009e\u00a1\u00ac\u00ad\2\u038a\2?\3\2\2\2\4Z\3")
        buf.write("\2\2\2\6\u0081\3\2\2\2\b\u0083\3\2\2\2\n\u00ac\3\2\2\2")
        buf.write("\f\u00be\3\2\2\2\16\u00d2\3\2\2\2\20\u00d8\3\2\2\2\22")
        buf.write("\u0124\3\2\2\2\24\u0192\3\2\2\2\26\u01a0\3\2\2\2\30\u01a8")
        buf.write("\3\2\2\2\32\u01b8\3\2\2\2\34\u01be\3\2\2\2\36\u01c0\3")
        buf.write("\2\2\2 \u01c5\3\2\2\2\"\u01ea\3\2\2\2$\u020c\3\2\2\2&")
        buf.write("\u024e\3\2\2\2(\u025e\3\2\2\2*\u0266\3\2\2\2,\u0297\3")
        buf.write("\2\2\2.\u02a5\3\2\2\2\60\u02b1\3\2\2\2\62\u02b7\3\2\2")
        buf.write("\2\64\u02c1\3\2\2\2\66\u02e4\3\2\2\28\u02e6\3\2\2\2:\u02e8")
        buf.write("\3\2\2\2<>\5\n\6\2=<\3\2\2\2>A\3\2\2\2?=\3\2\2\2?@\3\2")
        buf.write("\2\2@B\3\2\2\2A?\3\2\2\2BC\7\2\2\3C\3\3\2\2\2DE\5\f\7")
        buf.write("\2EF\7\2\2\3F[\3\2\2\2GI\5\6\4\2HJ\7\u00af\2\2IH\3\2\2")
        buf.write("\2IJ\3\2\2\2JK\3\2\2\2KL\7\2\2\3L[\3\2\2\2MO\5\b\5\2N")
        buf.write("P\7\u00af\2\2ON\3\2\2\2OP\3\2\2\2PQ\3\2\2\2QR\7\2\2\3")
        buf.write("R[\3\2\2\2SU\5\22\n\2TV\7\u00af\2\2UT\3\2\2\2UV\3\2\2")
        buf.write("\2VW\3\2\2\2WX\7\2\2\3X[\3\2\2\2Y[\7\2\2\3ZD\3\2\2\2Z")
        buf.write("G\3\2\2\2ZM\3\2\2\2ZS\3\2\2\2ZY\3\2\2\2[\5\3\2\2\2\\]")
        buf.write("\7\u00a9\2\2]^\5\64\33\2^_\7\u00a3\2\2_`\5\22\n\2`a\b")
        buf.write("\4\1\2ab\b\4\1\2b\u0082\3\2\2\2ce\7\u00a9\2\2dc\3\2\2")
        buf.write("\2de\3\2\2\2ef\3\2\2\2fg\5&\24\2gh\7\u00b4\2\2hj\7\u00a3")
        buf.write("\2\2ik\5\22\n\2ji\3\2\2\2jk\3\2\2\2kl\3\2\2\2lm\b\4\1")
        buf.write("\2mn\b\4\1\2n\u0082\3\2\2\2op\7\u00a9\2\2pq\5&\24\2qr")
        buf.write("\7\u00b4\2\2rs\b\4\1\2st\b\4\1\2t\u0082\3\2\2\2uw\7\u00a9")
        buf.write("\2\2vu\3\2\2\2vw\3\2\2\2wx\3\2\2\2xy\5&\24\2y|\5\64\33")
        buf.write("\2z{\7\u00a3\2\2{}\5\22\n\2|z\3\2\2\2|}\3\2\2\2}~\3\2")
        buf.write("\2\2~\177\b\4\1\2\177\u0080\b\4\1\2\u0080\u0082\3\2\2")
        buf.write("\2\u0081\\\3\2\2\2\u0081d\3\2\2\2\u0081o\3\2\2\2\u0081")
        buf.write("v\3\2\2\2\u0082\7\3\2\2\2\u0083\u0084\7\3\2\2\u0084\u0089")
        buf.write("\5\22\n\2\u0085\u0086\7\4\2\2\u0086\u0088\5\22\n\2\u0087")
        buf.write("\u0085\3\2\2\2\u0088\u008b\3\2\2\2\u0089\u0087\3\2\2\2")
        buf.write("\u0089\u008a\3\2\2\2\u008a\t\3\2\2\2\u008b\u0089\3\2\2")
        buf.write("\2\u008c\u008d\5\6\4\2\u008d\u008e\7\u00af\2\2\u008e\u00ad")
        buf.write("\3\2\2\2\u008f\u0090\t\2\2\2\u0090\u0091\5\22\n\2\u0091")
        buf.write("\u0092\7\u00af\2\2\u0092\u00ad\3\2\2\2\u0093\u0094\5\b")
        buf.write("\5\2\u0094\u0095\7\u00af\2\2\u0095\u00ad\3\2\2\2\u0096")
        buf.write("\u0097\7\7\2\2\u0097\u0098\5\22\n\2\u0098\u00a0\5\f\7")
        buf.write("\2\u0099\u009a\7\b\2\2\u009a\u009b\7\7\2\2\u009b\u009c")
        buf.write("\5\22\n\2\u009c\u009d\5\f\7\2\u009d\u009f\3\2\2\2\u009e")
        buf.write("\u0099\3\2\2\2\u009f\u00a2\3\2\2\2\u00a0\u009e\3\2\2\2")
        buf.write("\u00a0\u00a1\3\2\2\2\u00a1\u00a5\3\2\2\2\u00a2\u00a0\3")
        buf.write("\2\2\2\u00a3\u00a4\7\b\2\2\u00a4\u00a6\5\f\7\2\u00a5\u00a3")
        buf.write("\3\2\2\2\u00a5\u00a6\3\2\2\2\u00a6\u00ad\3\2\2\2\u00a7")
        buf.write("\u00a8\5\22\n\2\u00a8\u00a9\7\u00af\2\2\u00a9\u00ad\3")
        buf.write("\2\2\2\u00aa\u00ad\5\16\b\2\u00ab\u00ad\5\f\7\2\u00ac")
        buf.write("\u008c\3\2\2\2\u00ac\u008f\3\2\2\2\u00ac\u0093\3\2\2\2")
        buf.write("\u00ac\u0096\3\2\2\2\u00ac\u00a7\3\2\2\2\u00ac\u00aa\3")
        buf.write("\2\2\2\u00ac\u00ab\3\2\2\2\u00ad\13\3\2\2\2\u00ae\u00b2")
        buf.write("\7\t\2\2\u00af\u00b1\5\n\6\2\u00b0\u00af\3\2\2\2\u00b1")
        buf.write("\u00b4\3\2\2\2\u00b2\u00b0\3\2\2\2\u00b2\u00b3\3\2\2\2")
        buf.write("\u00b3\u00b5\3\2\2\2\u00b4\u00b2\3\2\2\2\u00b5\u00bf\7")
        buf.write("\n\2\2\u00b6\u00ba\7\13\2\2\u00b7\u00b9\5\n\6\2\u00b8")
        buf.write("\u00b7\3\2\2\2\u00b9\u00bc\3\2\2\2\u00ba\u00b8\3\2\2\2")
        buf.write("\u00ba\u00bb\3\2\2\2\u00bb\u00bd\3\2\2\2\u00bc\u00ba\3")
        buf.write("\2\2\2\u00bd\u00bf\7\f\2\2\u00be\u00ae\3\2\2\2\u00be\u00b6")
        buf.write("\3\2\2\2\u00bf\r\3\2\2\2\u00c0\u00c1\7\r\2\2\u00c1\u00c2")
        buf.write("\5\22\n\2\u00c2\u00c3\7\16\2\2\u00c3\u00c4\5\n\6\2\u00c4")
        buf.write("\u00d3\3\2\2\2\u00c5\u00c6\7\17\2\2\u00c6\u00c7\5\64\33")
        buf.write("\2\u00c7\u00c8\7\20\2\2\u00c8\u00c9\7\21\2\2\u00c9\u00ca")
        buf.write("\5\22\n\2\u00ca\u00cb\7\4\2\2\u00cb\u00cc\5\22\n\2\u00cc")
        buf.write("\u00cd\5\20\t\2\u00cd\u00ce\7\22\2\2\u00ce\u00cf\5\22")
        buf.write("\n\2\u00cf\u00d0\3\2\2\2\u00d0\u00d1\5\n\6\2\u00d1\u00d3")
        buf.write("\3\2\2\2\u00d2\u00c0\3\2\2\2\u00d2\u00c5\3\2\2\2\u00d3")
        buf.write("\17\3\2\2\2\u00d4\u00d5\7\u00b1\2\2\u00d5\u00d9\b\t\1")
        buf.write("\2\u00d6\u00d7\7\u00b2\2\2\u00d7\u00d9\b\t\1\2\u00d8\u00d4")
        buf.write("\3\2\2\2\u00d8\u00d6\3\2\2\2\u00d9\21\3\2\2\2\u00da\u00db")
        buf.write("\b\n\1\2\u00db\u00dc\7\23\2\2\u00dc\u00dd\5\22\n\2\u00dd")
        buf.write("\u00de\7\u00b2\2\2\u00de\u0125\3\2\2\2\u00df\u00e0\7\23")
        buf.write("\2\2\u00e0\u00e1\5\22\n\2\u00e1\u00e2\7\4\2\2\u00e2\u00e3")
        buf.write("\5\22\n\2\u00e3\u00e4\7\u00b2\2\2\u00e4\u0125\3\2\2\2")
        buf.write("\u00e5\u00e6\7\u00ae\2\2\u00e6\u0125\5\22\n/\u00e7\u00e8")
        buf.write("\5*\26\2\u00e8\u00e9\7\24\2\2\u00e9\u00ea\5\22\n-\u00ea")
        buf.write("\u0125\3\2\2\2\u00eb\u00ec\7\u00b4\2\2\u00ec\u0125\5\32")
        buf.write("\16\2\u00ed\u00ef\7\35\2\2\u00ee\u00ed\3\2\2\2\u00ee\u00ef")
        buf.write("\3\2\2\2\u00ef\u00f0\3\2\2\2\u00f0\u00f2\5\24\13\2\u00f1")
        buf.write("\u00f3\7\36\2\2\u00f2\u00f1\3\2\2\2\u00f2\u00f3\3\2\2")
        buf.write("\2\u00f3\u0125\3\2\2\2\u00f4\u00f6\t\3\2\2\u00f5\u00f4")
        buf.write("\3\2\2\2\u00f5\u00f6\3\2\2\2\u00f6\u00f7\3\2\2\2\u00f7")
        buf.write("\u00f9\7\36\2\2\u00f8\u00fa\7\37\2\2\u00f9\u00f8\3\2\2")
        buf.write("\2\u00f9\u00fa\3\2\2\2\u00fa\u00fb\3\2\2\2\u00fb\u0125")
        buf.write("\5\22\n\"\u00fc\u00fd\7\u00ab\2\2\u00fd\u0125\5\22\n\33")
        buf.write("\u00fe\u00ff\5\26\f\2\u00ff\u0100\5\22\n\30\u0100\u0125")
        buf.write("\3\2\2\2\u0101\u0125\5\26\f\2\u0102\u0104\7&\2\2\u0103")
        buf.write("\u0105\5\34\17\2\u0104\u0103\3\2\2\2\u0104\u0105\3\2\2")
        buf.write("\2\u0105\u0106\3\2\2\2\u0106\u0125\5\22\n\26\u0107\u0108")
        buf.write("\t\2\2\2\u0108\u0125\5\22\n\25\u0109\u010a\7\'\2\2\u010a")
        buf.write("\u010b\t\4\2\2\u010b\u0125\5\22\n\23\u010c\u0125\5\36")
        buf.write("\20\2\u010d\u0125\5$\23\2\u010e\u0110\7\35\2\2\u010f\u010e")
        buf.write("\3\2\2\2\u010f\u0110\3\2\2\2\u0110\u0111\3\2\2\2\u0111")
        buf.write("\u0125\5&\24\2\u0112\u0113\5&\24\2\u0113\u0114\7\u00b4")
        buf.write("\2\2\u0114\u0125\3\2\2\2\u0115\u0125\5\62\32\2\u0116\u0125")
        buf.write("\5\64\33\2\u0117\u0125\5\66\34\2\u0118\u0119\5\64\33\2")
        buf.write("\u0119\u011a\5\60\31\2\u011a\u011b\5\22\n\b\u011b\u0125")
        buf.write("\3\2\2\2\u011c\u011d\5&\24\2\u011d\u011e\7\u00b4\2\2\u011e")
        buf.write("\u011f\5\60\31\2\u011f\u0120\5\22\n\6\u0120\u0125\3\2")
        buf.write("\2\2\u0121\u0125\5:\36\2\u0122\u0125\7\u00b4\2\2\u0123")
        buf.write("\u0125\7\u00b5\2\2\u0124\u00da\3\2\2\2\u0124\u00df\3\2")
        buf.write("\2\2\u0124\u00e5\3\2\2\2\u0124\u00e7\3\2\2\2\u0124\u00eb")
        buf.write("\3\2\2\2\u0124\u00ee\3\2\2\2\u0124\u00f5\3\2\2\2\u0124")
        buf.write("\u00fc\3\2\2\2\u0124\u00fe\3\2\2\2\u0124\u0101\3\2\2\2")
        buf.write("\u0124\u0102\3\2\2\2\u0124\u0107\3\2\2\2\u0124\u0109\3")
        buf.write("\2\2\2\u0124\u010c\3\2\2\2\u0124\u010d\3\2\2\2\u0124\u010f")
        buf.write("\3\2\2\2\u0124\u0112\3\2\2\2\u0124\u0115\3\2\2\2\u0124")
        buf.write("\u0116\3\2\2\2\u0124\u0117\3\2\2\2\u0124\u0118\3\2\2\2")
        buf.write("\u0124\u011c\3\2\2\2\u0124\u0121\3\2\2\2\u0124\u0122\3")
        buf.write("\2\2\2\u0124\u0123\3\2\2\2\u0125\u018b\3\2\2\2\u0126\u0127")
        buf.write("\f(\2\2\u0127\u0128\7\20\2\2\u0128\u0129\t\5\2\2\u0129")
        buf.write("\u018a\5\22\n)\u012a\u012b\f!\2\2\u012b\u012c\7 \2\2\u012c")
        buf.write("\u018a\5\22\n\"\u012d\u012e\f \2\2\u012e\u012f\t\6\2\2")
        buf.write("\u012f\u018a\5\22\n!\u0130\u0131\f\37\2\2\u0131\u0132")
        buf.write("\t\7\2\2\u0132\u018a\5\22\n \u0133\u0134\f\36\2\2\u0134")
        buf.write("\u0135\5.\30\2\u0135\u0136\5\22\n\37\u0136\u018a\3\2\2")
        buf.write("\2\u0137\u013d\f\34\2\2\u0138\u013a\7#\2\2\u0139\u013b")
        buf.write("\7\u00ab\2\2\u013a\u0139\3\2\2\2\u013a\u013b\3\2\2\2\u013b")
        buf.write("\u013e\3\2\2\2\u013c\u013e\7\u00a8\2\2\u013d\u0138\3\2")
        buf.write("\2\2\u013d\u013c\3\2\2\2\u013e\u013f\3\2\2\2\u013f\u018a")
        buf.write("\5\22\n\35\u0140\u0141\f\32\2\2\u0141\u0142\7$\2\2\u0142")
        buf.write("\u018a\5\22\n\33\u0143\u0144\f\31\2\2\u0144\u0145\7%\2")
        buf.write("\2\u0145\u018a\5\22\n\32\u0146\u0147\f\22\2\2\u0147\u0148")
        buf.write("\t\4\2\2\u0148\u018a\5\22\n\23\u0149\u014a\f\21\2\2\u014a")
        buf.write("\u014b\7\u00a7\2\2\u014b\u018a\5\22\n\22\u014c\u014d\f")
        buf.write("\20\2\2\u014d\u014e\7\7\2\2\u014e\u014f\5\22\n\2\u014f")
        buf.write("\u0150\7\b\2\2\u0150\u0151\5\22\n\21\u0151\u018a\3\2\2")
        buf.write("\2\u0152\u0153\f\7\2\2\u0153\u0154\7\u00a4\2\2\u0154\u0155")
        buf.write("\5,\27\2\u0155\u0156\5\60\31\2\u0156\u0157\5\22\n\b\u0157")
        buf.write("\u018a\3\2\2\2\u0158\u0159\f\61\2\2\u0159\u0162\7\23\2")
        buf.write("\2\u015a\u015f\5\22\n\2\u015b\u015c\7\4\2\2\u015c\u015e")
        buf.write("\5\22\n\2\u015d\u015b\3\2\2\2\u015e\u0161\3\2\2\2\u015f")
        buf.write("\u015d\3\2\2\2\u015f\u0160\3\2\2\2\u0160\u0163\3\2\2\2")
        buf.write("\u0161\u015f\3\2\2\2\u0162\u015a\3\2\2\2\u0162\u0163\3")
        buf.write("\2\2\2\u0163\u0164\3\2\2\2\u0164\u018a\7\u00b2\2\2\u0165")
        buf.write("\u0166\f.\2\2\u0166\u018a\5\26\f\2\u0167\u0168\f,\2\2")
        buf.write("\u0168\u0169\7\u00a4\2\2\u0169\u016a\7\25\2\2\u016a\u016b")
        buf.write("\7\20\2\2\u016b\u018a\5(\25\2\u016c\u016d\f+\2\2\u016d")
        buf.write("\u016f\7\26\2\2\u016e\u0170\7\27\2\2\u016f\u016e\3\2\2")
        buf.write("\2\u016f\u0170\3\2\2\2\u0170\u0171\3\2\2\2\u0171\u0172")
        buf.write("\7\30\2\2\u0172\u0173\7\20\2\2\u0173\u018a\5(\25\2\u0174")
        buf.write("\u0175\f*\2\2\u0175\u0176\7\u00a4\2\2\u0176\u018a\5,\27")
        buf.write("\2\u0177\u0178\f)\2\2\u0178\u0179\7\31\2\2\u0179\u018a")
        buf.write("\5\30\r\2\u017a\u017b\f&\2\2\u017b\u018a\5\32\16\2\u017c")
        buf.write("\u017d\f%\2\2\u017d\u018a\5(\25\2\u017e\u017f\f$\2\2\u017f")
        buf.write("\u018a\7\34\2\2\u0180\u0181\f\35\2\2\u0181\u0182\7!\2")
        buf.write("\2\u0182\u0183\t\b\2\2\u0183\u018a\5,\27\2\u0184\u0185")
        buf.write("\f\24\2\2\u0185\u0186\7\21\2\2\u0186\u0187\5\22\n\2\u0187")
        buf.write("\u0188\7\u00b1\2\2\u0188\u018a\3\2\2\2\u0189\u0126\3\2")
        buf.write("\2\2\u0189\u012a\3\2\2\2\u0189\u012d\3\2\2\2\u0189\u0130")
        buf.write("\3\2\2\2\u0189\u0133\3\2\2\2\u0189\u0137\3\2\2\2\u0189")
        buf.write("\u0140\3\2\2\2\u0189\u0143\3\2\2\2\u0189\u0146\3\2\2\2")
        buf.write("\u0189\u0149\3\2\2\2\u0189\u014c\3\2\2\2\u0189\u0152\3")
        buf.write("\2\2\2\u0189\u0158\3\2\2\2\u0189\u0165\3\2\2\2\u0189\u0167")
        buf.write("\3\2\2\2\u0189\u016c\3\2\2\2\u0189\u0174\3\2\2\2\u0189")
        buf.write("\u0177\3\2\2\2\u0189\u017a\3\2\2\2\u0189\u017c\3\2\2\2")
        buf.write("\u0189\u017e\3\2\2\2\u0189\u0180\3\2\2\2\u0189\u0184\3")
        buf.write("\2\2\2\u018a\u018d\3\2\2\2\u018b\u0189\3\2\2\2\u018b\u018c")
        buf.write("\3\2\2\2\u018c\23\3\2\2\2\u018d\u018b\3\2\2\2\u018e\u018f")
        buf.write("\7*\2\2\u018f\u0193\b\13\1\2\u0190\u0191\7+\2\2\u0191")
        buf.write("\u0193\b\13\1\2\u0192\u018e\3\2\2\2\u0192\u0190\3\2\2")
        buf.write("\2\u0193\25\3\2\2\2\u0194\u0195\t\t\2\2\u0195\u0196\b")
        buf.write("\f\1\2\u0196\u01a1\b\f\1\2\u0197\u0198\t\n\2\2\u0198\u0199")
        buf.write("\b\f\1\2\u0199\u01a1\b\f\1\2\u019a\u019b\t\13\2\2\u019b")
        buf.write("\u019c\b\f\1\2\u019c\u01a1\b\f\1\2\u019d\u019e\t\f\2\2")
        buf.write("\u019e\u019f\b\f\1\2\u019f\u01a1\b\f\1\2\u01a0\u0194\3")
        buf.write("\2\2\2\u01a0\u0197\3\2\2\2\u01a0\u019a\3\2\2\2\u01a0\u019d")
        buf.write("\3\2\2\2\u01a1\27\3\2\2\2\u01a2\u01a3\t\r\2\2\u01a3\u01a9")
        buf.write("\b\r\1\2\u01a4\u01a5\t\16\2\2\u01a5\u01a9\b\r\1\2\u01a6")
        buf.write("\u01a7\7\66\2\2\u01a7\u01a9\b\r\1\2\u01a8\u01a2\3\2\2")
        buf.write("\2\u01a8\u01a4\3\2\2\2\u01a8\u01a6\3\2\2\2\u01a9\31\3")
        buf.write("\2\2\2\u01aa\u01ab\6\16\31\3\u01ab\u01ac\7\67\2\2\u01ac")
        buf.write("\u01ad\b\16\1\2\u01ad\u01b9\b\16\1\2\u01ae\u01af\78\2")
        buf.write("\2\u01af\u01b0\b\16\1\2\u01b0\u01b9\b\16\1\2\u01b1\u01b2")
        buf.write("\6\16\32\3\u01b2\u01b3\t\17\2\2\u01b3\u01b4\b\16\1\2\u01b4")
        buf.write("\u01b9\b\16\1\2\u01b5\u01b6\t\20\2\2\u01b6\u01b7\b\16")
        buf.write("\1\2\u01b7\u01b9\b\16\1\2\u01b8\u01aa\3\2\2\2\u01b8\u01ae")
        buf.write("\3\2\2\2\u01b8\u01b1\3\2\2\2\u01b8\u01b5\3\2\2\2\u01b9")
        buf.write("\33\3\2\2\2\u01ba\u01bb\7\67\2\2\u01bb\u01bf\b\17\1\2")
        buf.write("\u01bc\u01bd\t\17\2\2\u01bd\u01bf\b\17\1\2\u01be\u01ba")
        buf.write("\3\2\2\2\u01be\u01bc\3\2\2\2\u01bf\35\3\2\2\2\u01c0\u01c3")
        buf.write("\5 \21\2\u01c1\u01c4\5\f\7\2\u01c2\u01c4\5\22\n\2\u01c3")
        buf.write("\u01c1\3\2\2\2\u01c3\u01c2\3\2\2\2\u01c4\37\3\2\2\2\u01c5")
        buf.write("\u01c6\7=\2\2\u01c6\u01cf\7\23\2\2\u01c7\u01cc\5\"\22")
        buf.write("\2\u01c8\u01c9\7\4\2\2\u01c9\u01cb\5\"\22\2\u01ca\u01c8")
        buf.write("\3\2\2\2\u01cb\u01ce\3\2\2\2\u01cc\u01ca\3\2\2\2\u01cc")
        buf.write("\u01cd\3\2\2\2\u01cd\u01d0\3\2\2\2\u01ce\u01cc\3\2\2\2")
        buf.write("\u01cf\u01c7\3\2\2\2\u01cf\u01d0\3\2\2\2\u01d0\u01d1\3")
        buf.write("\2\2\2\u01d1\u01d2\7\u00b2\2\2\u01d2!\3\2\2\2\u01d3\u01d5")
        buf.write("\t\b\2\2\u01d4\u01d3\3\2\2\2\u01d4\u01d5\3\2\2\2\u01d5")
        buf.write("\u01d6\3\2\2\2\u01d6\u01d7\5&\24\2\u01d7\u01d8\b\22\1")
        buf.write("\2\u01d8\u01eb\3\2\2\2\u01d9\u01da\5&\24\2\u01da\u01db")
        buf.write("\b\22\1\2\u01db\u01dc\7\u00b4\2\2\u01dc\u01dd\b\22\1\2")
        buf.write("\u01dd\u01eb\3\2\2\2\u01de\u01df\5&\24\2\u01df\u01e0\5")
        buf.write("\64\33\2\u01e0\u01e1\b\22\1\2\u01e1\u01e2\b\22\1\2\u01e2")
        buf.write("\u01eb\3\2\2\2\u01e3\u01e4\5\64\33\2\u01e4\u01e5\7\u00a7")
        buf.write("\2\2\u01e5\u01e6\5&\24\2\u01e6\u01e7\b\22\1\2\u01e7\u01e8")
        buf.write("\b\22\1\2\u01e8\u01e9\b\22\1\2\u01e9\u01eb\3\2\2\2\u01ea")
        buf.write("\u01d4\3\2\2\2\u01ea\u01d9\3\2\2\2\u01ea\u01de\3\2\2\2")
        buf.write("\u01ea\u01e3\3\2\2\2\u01eb#\3\2\2\2\u01ec\u01ed\7>\2\2")
        buf.write("\u01ed\u01ee\7\u00ad\2\2\u01ee\u020d\b\23\1\2\u01ef\u01f0")
        buf.write("\7>\2\2\u01f0\u01f1\7\u00ac\2\2\u01f1\u020d\b\23\1\2\u01f2")
        buf.write("\u01f4\7\u00b0\2\2\u01f3\u01f5\7?\2\2\u01f4\u01f3\3\2")
        buf.write("\2\2\u01f4\u01f5\3\2\2\2\u01f5\u01f6\3\2\2\2\u01f6\u020d")
        buf.write("\b\23\1\2\u01f7\u01fd\7@\2\2\u01f8\u01fa\7A\2\2\u01f9")
        buf.write("\u01fb\7\35\2\2\u01fa\u01f9\3\2\2\2\u01fa\u01fb\3\2\2")
        buf.write("\2\u01fb\u01fc\3\2\2\2\u01fc\u01fe\7B\2\2\u01fd\u01f8")
        buf.write("\3\2\2\2\u01fd\u01fe\3\2\2\2\u01fe\u01ff\3\2\2\2\u01ff")
        buf.write("\u020d\b\23\1\2\u0200\u0201\7C\2\2\u0201\u0202\7D\2\2")
        buf.write("\u0202\u020d\b\23\1\2\u0203\u0204\7C\2\2\u0204\u0205\7")
        buf.write("E\2\2\u0205\u020d\b\23\1\2\u0206\u0207\7C\2\2\u0207\u0208")
        buf.write("\7F\2\2\u0208\u020d\b\23\1\2\u0209\u020a\7C\2\2\u020a")
        buf.write("\u020b\7G\2\2\u020b\u020d\b\23\1\2\u020c\u01ec\3\2\2\2")
        buf.write("\u020c\u01ef\3\2\2\2\u020c\u01f2\3\2\2\2\u020c\u01f7\3")
        buf.write("\2\2\2\u020c\u0200\3\2\2\2\u020c\u0203\3\2\2\2\u020c\u0206")
        buf.write("\3\2\2\2\u020c\u0209\3\2\2\2\u020d%\3\2\2\2\u020e\u020f")
        buf.write("\7\'\2\2\u020f\u024f\b\24\1\2\u0210\u0211\7H\2\2\u0211")
        buf.write("\u024f\b\24\1\2\u0212\u0213\7I\2\2\u0213\u024f\b\24\1")
        buf.write("\2\u0214\u0215\7I\2\2\u0215\u0216\7H\2\2\u0216\u024f\b")
        buf.write("\24\1\2\u0217\u0219\7I\2\2\u0218\u0217\3\2\2\2\u0218\u0219")
        buf.write("\3\2\2\2\u0219\u021a\3\2\2\2\u021a\u021b\7J\2\2\u021b")
        buf.write("\u024f\b\24\1\2\u021c\u021d\7K\2\2\u021d\u024f\b\24\1")
        buf.write("\2\u021e\u021f\7L\2\2\u021f\u024f\b\24\1\2\u0220\u0221")
        buf.write("\7\30\2\2\u0221\u024f\b\24\1\2\u0222\u0223\7?\2\2\u0223")
        buf.write("\u024f\b\24\1\2\u0224\u0225\7M\2\2\u0225\u024f\b\24\1")
        buf.write("\2\u0226\u0227\7N\2\2\u0227\u024f\b\24\1\2\u0228\u0229")
        buf.write("\7O\2\2\u0229\u024f\b\24\1\2\u022a\u022b\7P\2\2\u022b")
        buf.write("\u024f\b\24\1\2\u022c\u022d\7Q\2\2\u022d\u024f\b\24\1")
        buf.write("\2\u022e\u022f\7R\2\2\u022f\u024f\b\24\1\2\u0230\u0231")
        buf.write("\7S\2\2\u0231\u024f\b\24\1\2\u0232\u0233\t\5\2\2\u0233")
        buf.write("\u024f\b\24\1\2\u0234\u0235\7T\2\2\u0235\u024f\b\24\1")
        buf.write("\2\u0236\u0237\7\36\2\2\u0237\u024f\b\24\1\2\u0238\u0239")
        buf.write("\7U\2\2\u0239\u024f\b\24\1\2\u023a\u023b\t\21\2\2\u023b")
        buf.write("\u023c\t\22\2\2\u023c\u024f\b\24\1\2\u023d\u023f\t\21")
        buf.write("\2\2\u023e\u0240\7Z\2\2\u023f\u023e\3\2\2\2\u023f\u0240")
        buf.write("\3\2\2\2\u0240\u0241\3\2\2\2\u0241\u024f\b\24\1\2\u0242")
        buf.write("\u0243\7[\2\2\u0243\u024f\b\24\1\2\u0244\u0245\7\\\2\2")
        buf.write("\u0245\u024f\b\24\1\2\u0246\u0247\7]\2\2\u0247\u0248\7")
        buf.write("^\2\2\u0248\u024f\b\24\1\2\u0249\u024a\7]\2\2\u024a\u024b")
        buf.write("\7_\2\2\u024b\u024f\b\24\1\2\u024c\u024d\7`\2\2\u024d")
        buf.write("\u024f\b\24\1\2\u024e\u020e\3\2\2\2\u024e\u0210\3\2\2")
        buf.write("\2\u024e\u0212\3\2\2\2\u024e\u0214\3\2\2\2\u024e\u0218")
        buf.write("\3\2\2\2\u024e\u021c\3\2\2\2\u024e\u021e\3\2\2\2\u024e")
        buf.write("\u0220\3\2\2\2\u024e\u0222\3\2\2\2\u024e\u0224\3\2\2\2")
        buf.write("\u024e\u0226\3\2\2\2\u024e\u0228\3\2\2\2\u024e\u022a\3")
        buf.write("\2\2\2\u024e\u022c\3\2\2\2\u024e\u022e\3\2\2\2\u024e\u0230")
        buf.write("\3\2\2\2\u024e\u0232\3\2\2\2\u024e\u0234\3\2\2\2\u024e")
        buf.write("\u0236\3\2\2\2\u024e\u0238\3\2\2\2\u024e\u023a\3\2\2\2")
        buf.write("\u024e\u023d\3\2\2\2\u024e\u0242\3\2\2\2\u024e\u0244\3")
        buf.write("\2\2\2\u024e\u0246\3\2\2\2\u024e\u0249\3\2\2\2\u024e\u024c")
        buf.write("\3\2\2\2\u024f\'\3\2\2\2\u0250\u0251\t\23\2\2\u0251\u025f")
        buf.write("\b\25\1\2\u0252\u0253\t\24\2\2\u0253\u025f\b\25\1\2\u0254")
        buf.write("\u0255\t\25\2\2\u0255\u025f\b\25\1\2\u0256\u0257\t\26")
        buf.write("\2\2\u0257\u025f\b\25\1\2\u0258\u0259\t\27\2\2\u0259\u025f")
        buf.write("\b\25\1\2\u025a\u025b\t\30\2\2\u025b\u025f\b\25\1\2\u025c")
        buf.write("\u025d\t\31\2\2\u025d\u025f\b\25\1\2\u025e\u0250\3\2\2")
        buf.write("\2\u025e\u0252\3\2\2\2\u025e\u0254\3\2\2\2\u025e\u0256")
        buf.write("\3\2\2\2\u025e\u0258\3\2\2\2\u025e\u025a\3\2\2\2\u025e")
        buf.write("\u025c\3\2\2\2\u025f)\3\2\2\2\u0260\u0261\7I\2\2\u0261")
        buf.write("\u0267\b\26\1\2\u0262\u0263\7[\2\2\u0263\u0267\b\26\1")
        buf.write("\2\u0264\u0265\7\\\2\2\u0265\u0267\b\26\1\2\u0266\u0260")
        buf.write("\3\2\2\2\u0266\u0262\3\2\2\2\u0266\u0264\3\2\2\2\u0267")
        buf.write("+\3\2\2\2\u0268\u0269\7z\2\2\u0269\u026a\7H\2\2\u026a")
        buf.write("\u0298\b\27\1\2\u026b\u026c\7J\2\2\u026c\u0298\b\27\1")
        buf.write("\2\u026d\u026e\t\5\2\2\u026e\u0298\b\27\1\2\u026f\u0273")
        buf.write("\7\67\2\2\u0270\u0271\7{\2\2\u0271\u0273\t\32\2\2\u0272")
        buf.write("\u026f\3\2\2\2\u0272\u0270\3\2\2\2\u0273\u0274\3\2\2\2")
        buf.write("\u0274\u0298\b\27\1\2\u0275\u027a\79\2\2\u0276\u027a\7")
        buf.write(":\2\2\u0277\u0278\7~\2\2\u0278\u027a\t\32\2\2\u0279\u0275")
        buf.write("\3\2\2\2\u0279\u0276\3\2\2\2\u0279\u0277\3\2\2\2\u027a")
        buf.write("\u027b\3\2\2\2\u027b\u0298\b\27\1\2\u027c\u027d\7z\2\2")
        buf.write("\u027d\u027e\t\5\2\2\u027e\u0298\b\27\1\2\u027f\u0280")
        buf.write("\7\177\2\2\u0280\u0281\7\u0080\2\2\u0281\u0298\b\27\1")
        buf.write("\2\u0282\u0284\7\u0081\2\2\u0283\u0285\t\21\2\2\u0284")
        buf.write("\u0283\3\2\2\2\u0284\u0285\3\2\2\2\u0285\u0286\3\2\2\2")
        buf.write("\u0286\u0298\b\27\1\2\u0287\u0289\7\u0082\2\2\u0288\u0287")
        buf.write("\3\2\2\2\u0288\u0289\3\2\2\2\u0289\u028a\3\2\2\2\u028a")
        buf.write("\u028b\t\21\2\2\u028b\u0298\b\27\1\2\u028c\u028d\7]\2")
        buf.write("\2\u028d\u028e\7^\2\2\u028e\u0298\b\27\1\2\u028f\u0290")
        buf.write("\t\33\2\2\u0290\u0291\7\u0085\2\2\u0291\u0298\b\27\1\2")
        buf.write("\u0292\u0293\t\34\2\2\u0293\u0294\7\u0085\2\2\u0294\u0298")
        buf.write("\b\27\1\2\u0295\u0296\t\35\2\2\u0296\u0298\b\27\1\2\u0297")
        buf.write("\u0268\3\2\2\2\u0297\u026b\3\2\2\2\u0297\u026d\3\2\2\2")
        buf.write("\u0297\u0272\3\2\2\2\u0297\u0279\3\2\2\2\u0297\u027c\3")
        buf.write("\2\2\2\u0297\u027f\3\2\2\2\u0297\u0282\3\2\2\2\u0297\u0288")
        buf.write("\3\2\2\2\u0297\u028c\3\2\2\2\u0297\u028f\3\2\2\2\u0297")
        buf.write("\u0292\3\2\2\2\u0297\u0295\3\2\2\2\u0298-\3\2\2\2\u0299")
        buf.write("\u029a\7\u0088\2\2\u029a\u02a6\b\30\1\2\u029b\u029c\7")
        buf.write("\u0089\2\2\u029c\u02a6\b\30\1\2\u029d\u029e\7\u008a\2")
        buf.write("\2\u029e\u02a6\b\30\1\2\u029f\u02a0\7\u008b\2\2\u02a0")
        buf.write("\u02a6\b\30\1\2\u02a1\u02a2\7\u008c\2\2\u02a2\u02a6\b")
        buf.write("\30\1\2\u02a3\u02a4\7\u008d\2\2\u02a4\u02a6\b\30\1\2\u02a5")
        buf.write("\u0299\3\2\2\2\u02a5\u029b\3\2\2\2\u02a5\u029d\3\2\2\2")
        buf.write("\u02a5\u029f\3\2\2\2\u02a5\u02a1\3\2\2\2\u02a5\u02a3\3")
        buf.write("\2\2\2\u02a6/\3\2\2\2\u02a7\u02a8\7\u00a3\2\2\u02a8\u02b2")
        buf.write("\b\31\1\2\u02a9\u02aa\7\u008e\2\2\u02aa\u02b2\b\31\1\2")
        buf.write("\u02ab\u02ac\7\u008f\2\2\u02ac\u02b2\b\31\1\2\u02ad\u02ae")
        buf.write("\7\u0090\2\2\u02ae\u02b2\b\31\1\2\u02af\u02b0\7\u0091")
        buf.write("\2\2\u02b0\u02b2\b\31\1\2\u02b1\u02a7\3\2\2\2\u02b1\u02a9")
        buf.write("\3\2\2\2\u02b1\u02ab\3\2\2\2\u02b1\u02ad\3\2\2\2\u02b1")
        buf.write("\u02af\3\2\2\2\u02b2\61\3\2\2\2\u02b3\u02b4\t\36\2\2\u02b4")
        buf.write("\u02b8\b\32\1\2\u02b5\u02b6\t\37\2\2\u02b6\u02b8\b\32")
        buf.write("\1\2\u02b7\u02b3\3\2\2\2\u02b7\u02b5\3\2\2\2\u02b8\63")
        buf.write("\3\2\2\2\u02b9\u02ba\5\66\34\2\u02ba\u02bb\b\33\1\2\u02bb")
        buf.write("\u02c2\3\2\2\2\u02bc\u02bd\7\u00b3\2\2\u02bd\u02c2\b\33")
        buf.write("\1\2\u02be\u02bf\58\35\2\u02bf\u02c0\b\33\1\2\u02c0\u02c2")
        buf.write("\3\2\2\2\u02c1\u02b9\3\2\2\2\u02c1\u02bc\3\2\2\2\u02c1")
        buf.write("\u02be\3\2\2\2\u02c2\65\3\2\2\2\u02c3\u02c5\7\u00ad\2")
        buf.write("\2\u02c4\u02c6\7\35\2\2\u02c5\u02c4\3\2\2\2\u02c5\u02c6")
        buf.write("\3\2\2\2\u02c6\u02c7\3\2\2\2\u02c7\u02c8\7B\2\2\u02c8")
        buf.write("\u02e5\b\34\1\2\u02c9\u02cb\7\35\2\2\u02ca\u02c9\3\2\2")
        buf.write("\2\u02ca\u02cb\3\2\2\2\u02cb\u02cc\3\2\2\2\u02cc\u02cd")
        buf.write("\7\u00a6\2\2\u02cd\u02ce\7\36\2\2\u02ce\u02e5\b\34\1\2")
        buf.write("\u02cf\u02d1\7\35\2\2\u02d0\u02cf\3\2\2\2\u02d0\u02d1")
        buf.write("\3\2\2\2\u02d1\u02d2\3\2\2\2\u02d2\u02d3\7\u00a6\2\2\u02d3")
        buf.write("\u02d4\7T\2\2\u02d4\u02e5\b\34\1\2\u02d5\u02d6\7\35\2")
        buf.write("\2\u02d6\u02d7\7B\2\2\u02d7\u02e5\b\34\1\2\u02d8\u02da")
        buf.write("\7\35\2\2\u02d9\u02d8\3\2\2\2\u02d9\u02da\3\2\2\2\u02da")
        buf.write("\u02db\3\2\2\2\u02db\u02dc\7\u009e\2\2\u02dc\u02dd\7\u009f")
        buf.write("\2\2\u02dd\u02e5\b\34\1\2\u02de\u02df\7\u00a0\2\2\u02df")
        buf.write("\u02e0\7\'\2\2\u02e0\u02e5\b\34\1\2\u02e1\u02e2\7\u00a1")
        buf.write("\2\2\u02e2\u02e3\7I\2\2\u02e3\u02e5\b\34\1\2\u02e4\u02c3")
        buf.write("\3\2\2\2\u02e4\u02ca\3\2\2\2\u02e4\u02d0\3\2\2\2\u02e4")
        buf.write("\u02d5\3\2\2\2\u02e4\u02d9\3\2\2\2\u02e4\u02de\3\2\2\2")
        buf.write("\u02e4\u02e1\3\2\2\2\u02e5\67\3\2\2\2\u02e6\u02e7\t \2")
        buf.write("\2\u02e79\3\2\2\2\u02e8\u02e9\7\u00b6\2\2\u02e9;\3\2\2")
        buf.write("\2D?IOUZdjv|\u0081\u0089\u00a0\u00a5\u00ac\u00b2\u00ba")
        buf.write("\u00be\u00d2\u00d8\u00ee\u00f2\u00f5\u00f9\u0104\u010f")
        buf.write("\u0124\u013a\u013d\u015f\u0162\u016f\u0189\u018b\u0192")
        buf.write("\u01a0\u01a8\u01b8\u01be\u01c3\u01cc\u01cf\u01d4\u01ea")
        buf.write("\u01f4\u01fa\u01fd\u020c\u0218\u023f\u024e\u025e\u0266")
        buf.write("\u0272\u0279\u0284\u0288\u0297\u02a5\u02b1\u02b7\u02c1")
        buf.write("\u02c5\u02ca\u02d0\u02d9\u02e4")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'print'", "','", "'pause'", "'wait'", 
                     "'if'", "'else'", "'{'", "'}'", "'[['", "']]'", "'repeat'", 
                     "'times'", "'for'", "'in'", "'['", "'by'", "'('", "'#'", 
                     "'magnitude'", "'as'", "'a'", "'string'", "'turned'", 
                     "'dir'", "'direction'", "'C'", "'the'", "'reagent'", 
                     "'named'", "'of'", "'has'", "'an'", "'is'", "'and'", 
                     "'or'", "'to'", "'drop'", "'@'", "'at'", "'unknown'", 
                     "'waste'", "'up'", "'north'", "'down'", "'south'", 
                     "'left'", "'west'", "'right'", "'east'", "'clockwise'", 
                     "'counterclockwise'", "'around'", "'row'", "'rows'", 
                     "'col'", "'column'", "'cols'", "'columns'", "'macro'", 
                     "'turn'", "'state'", "'remove'", "'from'", "'board'", 
                     "'reset'", "'pads'", "'magnets'", "'heaters'", "'all'", 
                     "'pad'", "'well'", "'gate'", "'int'", "'float'", "'binary'", 
                     "'delta'", "'motion'", "'delay'", "'time'", "'ticks'", 
                     "'bool'", "'volume'", "'liquid'", "'temp'", "'temperature'", 
                     "'diff'", "'difference'", "'point'", "'heater'", "'magnet'", 
                     "'power'", "'supply'", "'mode'", "'fan'", "'s'", "'sec'", 
                     "'secs'", "'second'", "'seconds'", "'ms'", "'millisecond'", 
                     "'milliseconds'", "'uL'", "'ul'", "'microliter'", "'microlitre'", 
                     "'microliters'", "'microlitres'", "'mL'", "'ml'", "'milliliter'", 
                     "'millilitre'", "'milliliters'", "'millilitres'", "'tick'", 
                     "'drops'", "'V'", "'volt'", "'volts'", "'exit'", "'y'", 
                     "'coord'", "'coordinate'", "'x'", "'remaining'", "'capacity'", 
                     "'target'", "'current'", "'min'", "'minimum'", "'voltage'", 
                     "'max'", "'maximum'", "'=='", "'!='", "'<'", "'<='", 
                     "'>'", "'>='", "'+='", "'-='", "'*='", "'/='", "'True'", 
                     "'true'", "'TRUE'", "'Yes'", "'yes'", "'YES'", "'False'", 
                     "'false'", "'FALSE'", "'No'", "'no'", "'NO'", "'index'", 
                     "'base'", "'dispense'", "'enter'", "'+'", "'='", "<INVALID>", 
                     "'/'", "'interactive'", "':'", "'isn't'", "'local'", 
                     "'*'", "'not'", "'off'", "'on'", "'-'", "';'", "'toggle'", 
                     "']'", "')'" ]

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
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "ADD", "ASSIGN", "ATTR", "DIV", "INTERACTIVE", "INJECT", 
                      "ISNT", "LOCAL", "MUL", "NOT", "OFF", "ON", "SUB", 
                      "TERMINATOR", "TOGGLE", "CLOSE_BRACKET", "CLOSE_PAREN", 
                      "ID", "INT", "FLOAT", "STRING", "EOL_COMMENT", "COMMENT", 
                      "WS" ]

    RULE_macro_file = 0
    RULE_interactive = 1
    RULE_declaration = 2
    RULE_printing = 3
    RULE_stat = 4
    RULE_compound = 5
    RULE_loop = 6
    RULE_term_punct = 7
    RULE_expr = 8
    RULE_reagent = 9
    RULE_direction = 10
    RULE_turn = 11
    RULE_rc = 12
    RULE_axis = 13
    RULE_macro_def = 14
    RULE_macro_header = 15
    RULE_param = 16
    RULE_no_arg_action = 17
    RULE_param_type = 18
    RULE_dim_unit = 19
    RULE_numbered_type = 20
    RULE_attr = 21
    RULE_rel = 22
    RULE_assign_op = 23
    RULE_bool_val = 24
    RULE_name = 25
    RULE_multi_word_name = 26
    RULE_kwd_names = 27
    RULE_string = 28

    ruleNames =  [ "macro_file", "interactive", "declaration", "printing", 
                   "stat", "compound", "loop", "term_punct", "expr", "reagent", 
                   "direction", "turn", "rc", "axis", "macro_def", "macro_header", 
                   "param", "no_arg_action", "param_type", "dim_unit", "numbered_type", 
                   "attr", "rel", "assign_op", "bool_val", "name", "multi_word_name", 
                   "kwd_names", "string" ]

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
    T__53=54
    T__54=55
    T__55=56
    T__56=57
    T__57=58
    T__58=59
    T__59=60
    T__60=61
    T__61=62
    T__62=63
    T__63=64
    T__64=65
    T__65=66
    T__66=67
    T__67=68
    T__68=69
    T__69=70
    T__70=71
    T__71=72
    T__72=73
    T__73=74
    T__74=75
    T__75=76
    T__76=77
    T__77=78
    T__78=79
    T__79=80
    T__80=81
    T__81=82
    T__82=83
    T__83=84
    T__84=85
    T__85=86
    T__86=87
    T__87=88
    T__88=89
    T__89=90
    T__90=91
    T__91=92
    T__92=93
    T__93=94
    T__94=95
    T__95=96
    T__96=97
    T__97=98
    T__98=99
    T__99=100
    T__100=101
    T__101=102
    T__102=103
    T__103=104
    T__104=105
    T__105=106
    T__106=107
    T__107=108
    T__108=109
    T__109=110
    T__110=111
    T__111=112
    T__112=113
    T__113=114
    T__114=115
    T__115=116
    T__116=117
    T__117=118
    T__118=119
    T__119=120
    T__120=121
    T__121=122
    T__122=123
    T__123=124
    T__124=125
    T__125=126
    T__126=127
    T__127=128
    T__128=129
    T__129=130
    T__130=131
    T__131=132
    T__132=133
    T__133=134
    T__134=135
    T__135=136
    T__136=137
    T__137=138
    T__138=139
    T__139=140
    T__140=141
    T__141=142
    T__142=143
    T__143=144
    T__144=145
    T__145=146
    T__146=147
    T__147=148
    T__148=149
    T__149=150
    T__150=151
    T__151=152
    T__152=153
    T__153=154
    T__154=155
    T__155=156
    T__156=157
    T__157=158
    T__158=159
    ADD=160
    ASSIGN=161
    ATTR=162
    DIV=163
    INTERACTIVE=164
    INJECT=165
    ISNT=166
    LOCAL=167
    MUL=168
    NOT=169
    OFF=170
    ON=171
    SUB=172
    TERMINATOR=173
    TOGGLE=174
    CLOSE_BRACKET=175
    CLOSE_PAREN=176
    ID=177
    INT=178
    FLOAT=179
    STRING=180
    EOL_COMMENT=181
    COMMENT=182
    WS=183

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
            self.state = 61
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__4) | (1 << DMFParser.T__6) | (1 << DMFParser.T__8) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__16) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61))) != 0) or ((((_la - 65)) & ~0x3f) == 0 and ((1 << (_la - 65)) & ((1 << (DMFParser.T__64 - 65)) | (1 << (DMFParser.T__65 - 65)) | (1 << (DMFParser.T__66 - 65)) | (1 << (DMFParser.T__67 - 65)) | (1 << (DMFParser.T__68 - 65)) | (1 << (DMFParser.T__69 - 65)) | (1 << (DMFParser.T__70 - 65)) | (1 << (DMFParser.T__71 - 65)) | (1 << (DMFParser.T__72 - 65)) | (1 << (DMFParser.T__73 - 65)) | (1 << (DMFParser.T__74 - 65)) | (1 << (DMFParser.T__75 - 65)) | (1 << (DMFParser.T__76 - 65)) | (1 << (DMFParser.T__77 - 65)) | (1 << (DMFParser.T__78 - 65)) | (1 << (DMFParser.T__79 - 65)) | (1 << (DMFParser.T__80 - 65)) | (1 << (DMFParser.T__81 - 65)) | (1 << (DMFParser.T__82 - 65)) | (1 << (DMFParser.T__83 - 65)) | (1 << (DMFParser.T__84 - 65)) | (1 << (DMFParser.T__85 - 65)) | (1 << (DMFParser.T__86 - 65)) | (1 << (DMFParser.T__87 - 65)) | (1 << (DMFParser.T__88 - 65)) | (1 << (DMFParser.T__89 - 65)) | (1 << (DMFParser.T__90 - 65)) | (1 << (DMFParser.T__93 - 65)) | (1 << (DMFParser.T__94 - 65)) | (1 << (DMFParser.T__99 - 65)) | (1 << (DMFParser.T__120 - 65)) | (1 << (DMFParser.T__123 - 65)))) != 0) or ((((_la - 129)) & ~0x3f) == 0 and ((1 << (_la - 129)) & ((1 << (DMFParser.T__128 - 129)) | (1 << (DMFParser.T__129 - 129)) | (1 << (DMFParser.T__131 - 129)) | (1 << (DMFParser.T__132 - 129)) | (1 << (DMFParser.T__143 - 129)) | (1 << (DMFParser.T__144 - 129)) | (1 << (DMFParser.T__145 - 129)) | (1 << (DMFParser.T__146 - 129)) | (1 << (DMFParser.T__147 - 129)) | (1 << (DMFParser.T__148 - 129)) | (1 << (DMFParser.T__149 - 129)) | (1 << (DMFParser.T__150 - 129)) | (1 << (DMFParser.T__151 - 129)) | (1 << (DMFParser.T__152 - 129)) | (1 << (DMFParser.T__153 - 129)) | (1 << (DMFParser.T__154 - 129)) | (1 << (DMFParser.T__155 - 129)) | (1 << (DMFParser.T__156 - 129)) | (1 << (DMFParser.T__157 - 129)) | (1 << (DMFParser.T__158 - 129)) | (1 << (DMFParser.INTERACTIVE - 129)) | (1 << (DMFParser.LOCAL - 129)) | (1 << (DMFParser.NOT - 129)) | (1 << (DMFParser.OFF - 129)) | (1 << (DMFParser.ON - 129)) | (1 << (DMFParser.SUB - 129)) | (1 << (DMFParser.TOGGLE - 129)) | (1 << (DMFParser.ID - 129)) | (1 << (DMFParser.INT - 129)) | (1 << (DMFParser.FLOAT - 129)) | (1 << (DMFParser.STRING - 129)))) != 0):
                self.state = 58
                self.stat()
                self.state = 63
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 64
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


    class Decl_interactiveContext(InteractiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.InteractiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def declaration(self):
            return self.getTypedRuleContext(DMFParser.DeclarationContext,0)

        def EOF(self):
            return self.getToken(DMFParser.EOF, 0)
        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecl_interactive" ):
                listener.enterDecl_interactive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecl_interactive" ):
                listener.exitDecl_interactive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDecl_interactive" ):
                return visitor.visitDecl_interactive(self)
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


    class Expr_interactiveContext(InteractiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.InteractiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)

        def EOF(self):
            return self.getToken(DMFParser.EOF, 0)
        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

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


    class Print_interactiveContext(InteractiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.InteractiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def printing(self):
            return self.getTypedRuleContext(DMFParser.PrintingContext,0)

        def EOF(self):
            return self.getToken(DMFParser.EOF, 0)
        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrint_interactive" ):
                listener.enterPrint_interactive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrint_interactive" ):
                listener.exitPrint_interactive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrint_interactive" ):
                return visitor.visitPrint_interactive(self)
            else:
                return visitor.visitChildren(self)



    def interactive(self):

        localctx = DMFParser.InteractiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_interactive)
        self._la = 0 # Token type
        try:
            self.state = 88
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 66
                self.compound()
                self.state = 67
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Decl_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                self.declaration()
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 70
                    self.match(DMFParser.TERMINATOR)


                self.state = 73
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Print_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 75
                self.printing()
                self.state = 77
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 76
                    self.match(DMFParser.TERMINATOR)


                self.state = 79
                self.match(DMFParser.EOF)
                pass

            elif la_ == 4:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 81
                self.expr(0)
                self.state = 83
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 82
                    self.match(DMFParser.TERMINATOR)


                self.state = 85
                self.match(DMFParser.EOF)
                pass

            elif la_ == 5:
                localctx = DMFParser.Empty_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 87
                self.match(DMFParser.EOF)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.type = None
            self.pname = None
            self.n = None
            self._name = None # NameContext
            self.init = None # ExprContext
            self._param_type = None # Param_typeContext
            self._INT = None # Token

        def LOCAL(self):
            return self.getToken(DMFParser.LOCAL, 0)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)


        def ASSIGN(self):
            return self.getToken(DMFParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def param_type(self):
            return self.getTypedRuleContext(DMFParser.Param_typeContext,0)


        def INT(self):
            return self.getToken(DMFParser.INT, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = DMFParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_declaration)
        self._la = 0 # Token type
        try:
            self.state = 127
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 90
                self.match(DMFParser.LOCAL)
                self.state = 91
                localctx._name = self.name()
                self.state = 92
                self.match(DMFParser.ASSIGN)
                self.state = 93
                localctx.init = self.expr(0)
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                localctx.type=None
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 98
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.LOCAL:
                    self.state = 97
                    self.match(DMFParser.LOCAL)


                self.state = 100
                localctx._param_type = self.param_type()
                self.state = 101
                localctx._INT = self.match(DMFParser.INT)
                self.state = 102
                self.match(DMFParser.ASSIGN)
                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__16) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61))) != 0) or ((((_la - 65)) & ~0x3f) == 0 and ((1 << (_la - 65)) & ((1 << (DMFParser.T__64 - 65)) | (1 << (DMFParser.T__65 - 65)) | (1 << (DMFParser.T__66 - 65)) | (1 << (DMFParser.T__67 - 65)) | (1 << (DMFParser.T__68 - 65)) | (1 << (DMFParser.T__69 - 65)) | (1 << (DMFParser.T__70 - 65)) | (1 << (DMFParser.T__71 - 65)) | (1 << (DMFParser.T__72 - 65)) | (1 << (DMFParser.T__73 - 65)) | (1 << (DMFParser.T__74 - 65)) | (1 << (DMFParser.T__75 - 65)) | (1 << (DMFParser.T__76 - 65)) | (1 << (DMFParser.T__77 - 65)) | (1 << (DMFParser.T__78 - 65)) | (1 << (DMFParser.T__79 - 65)) | (1 << (DMFParser.T__80 - 65)) | (1 << (DMFParser.T__81 - 65)) | (1 << (DMFParser.T__82 - 65)) | (1 << (DMFParser.T__83 - 65)) | (1 << (DMFParser.T__84 - 65)) | (1 << (DMFParser.T__85 - 65)) | (1 << (DMFParser.T__86 - 65)) | (1 << (DMFParser.T__87 - 65)) | (1 << (DMFParser.T__88 - 65)) | (1 << (DMFParser.T__89 - 65)) | (1 << (DMFParser.T__90 - 65)) | (1 << (DMFParser.T__93 - 65)) | (1 << (DMFParser.T__94 - 65)) | (1 << (DMFParser.T__99 - 65)) | (1 << (DMFParser.T__120 - 65)) | (1 << (DMFParser.T__123 - 65)))) != 0) or ((((_la - 129)) & ~0x3f) == 0 and ((1 << (_la - 129)) & ((1 << (DMFParser.T__128 - 129)) | (1 << (DMFParser.T__129 - 129)) | (1 << (DMFParser.T__131 - 129)) | (1 << (DMFParser.T__132 - 129)) | (1 << (DMFParser.T__143 - 129)) | (1 << (DMFParser.T__144 - 129)) | (1 << (DMFParser.T__145 - 129)) | (1 << (DMFParser.T__146 - 129)) | (1 << (DMFParser.T__147 - 129)) | (1 << (DMFParser.T__148 - 129)) | (1 << (DMFParser.T__149 - 129)) | (1 << (DMFParser.T__150 - 129)) | (1 << (DMFParser.T__151 - 129)) | (1 << (DMFParser.T__152 - 129)) | (1 << (DMFParser.T__153 - 129)) | (1 << (DMFParser.T__154 - 129)) | (1 << (DMFParser.T__155 - 129)) | (1 << (DMFParser.T__156 - 129)) | (1 << (DMFParser.T__157 - 129)) | (1 << (DMFParser.T__158 - 129)) | (1 << (DMFParser.INTERACTIVE - 129)) | (1 << (DMFParser.NOT - 129)) | (1 << (DMFParser.OFF - 129)) | (1 << (DMFParser.ON - 129)) | (1 << (DMFParser.SUB - 129)) | (1 << (DMFParser.TOGGLE - 129)) | (1 << (DMFParser.ID - 129)) | (1 << (DMFParser.INT - 129)) | (1 << (DMFParser.FLOAT - 129)) | (1 << (DMFParser.STRING - 129)))) != 0):
                    self.state = 103
                    localctx.init = self.expr(0)


                localctx.type=localctx._param_type.type
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 109
                self.match(DMFParser.LOCAL)
                self.state = 110
                localctx._param_type = self.param_type()
                self.state = 111
                localctx._INT = self.match(DMFParser.INT)
                localctx.type=localctx._param_type.type
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 116
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.LOCAL:
                    self.state = 115
                    self.match(DMFParser.LOCAL)


                self.state = 118
                localctx._param_type = self.param_type()
                self.state = 119
                localctx._name = self.name()
                self.state = 122
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.ASSIGN:
                    self.state = 120
                    self.match(DMFParser.ASSIGN)
                    self.state = 121
                    localctx.init = self.expr(0)


                localctx.type=localctx._param_type.type
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrintingContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._expr = None # ExprContext
            self.vals = list() # of ExprContexts

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


        def getRuleIndex(self):
            return DMFParser.RULE_printing

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrinting" ):
                listener.enterPrinting(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrinting" ):
                listener.exitPrinting(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrinting" ):
                return visitor.visitPrinting(self)
            else:
                return visitor.visitChildren(self)




    def printing(self):

        localctx = DMFParser.PrintingContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_printing)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            self.match(DMFParser.T__0)
            self.state = 130
            localctx._expr = self.expr(0)
            localctx.vals.append(localctx._expr)
            self.state = 135
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DMFParser.T__1:
                self.state = 131
                self.match(DMFParser.T__1)
                self.state = 132
                localctx._expr = self.expr(0)
                localctx.vals.append(localctx._expr)
                self.state = 137
                self._errHandler.sync(self)
                _la = self._input.LA(1)

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



    class Print_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def printing(self):
            return self.getTypedRuleContext(DMFParser.PrintingContext,0)

        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrint_stat" ):
                listener.enterPrint_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrint_stat" ):
                listener.exitPrint_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrint_stat" ):
                return visitor.visitPrint_stat(self)
            else:
                return visitor.visitChildren(self)


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


    class If_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self._expr = None # ExprContext
            self.tests = list() # of ExprContexts
            self._compound = None # CompoundContext
            self.bodies = list() # of CompoundContexts
            self.else_body = None # CompoundContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)

        def compound(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.CompoundContext)
            else:
                return self.getTypedRuleContext(DMFParser.CompoundContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIf_stat" ):
                listener.enterIf_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIf_stat" ):
                listener.exitIf_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIf_stat" ):
                return visitor.visitIf_stat(self)
            else:
                return visitor.visitChildren(self)


    class Loop_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def loop(self):
            return self.getTypedRuleContext(DMFParser.LoopContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLoop_stat" ):
                listener.enterLoop_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLoop_stat" ):
                listener.exitLoop_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLoop_stat" ):
                return visitor.visitLoop_stat(self)
            else:
                return visitor.visitChildren(self)


    class Decl_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def declaration(self):
            return self.getTypedRuleContext(DMFParser.DeclarationContext,0)

        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDecl_stat" ):
                listener.enterDecl_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDecl_stat" ):
                listener.exitDecl_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDecl_stat" ):
                return visitor.visitDecl_stat(self)
            else:
                return visitor.visitChildren(self)



    def stat(self):

        localctx = DMFParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_stat)
        self._la = 0 # Token type
        try:
            self.state = 170
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Decl_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 138
                self.declaration()
                self.state = 139
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Pause_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 141
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__2 or _la==DMFParser.T__3):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 142
                localctx.duration = self.expr(0)
                self.state = 143
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 3:
                localctx = DMFParser.Print_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 145
                self.printing()
                self.state = 146
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 4:
                localctx = DMFParser.If_statContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 148
                self.match(DMFParser.T__4)
                self.state = 149
                localctx._expr = self.expr(0)
                localctx.tests.append(localctx._expr)
                self.state = 150
                localctx._compound = self.compound()
                localctx.bodies.append(localctx._compound)
                self.state = 158
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 151
                        self.match(DMFParser.T__5)
                        self.state = 152
                        self.match(DMFParser.T__4)
                        self.state = 153
                        localctx._expr = self.expr(0)
                        localctx.tests.append(localctx._expr)
                        self.state = 154
                        localctx._compound = self.compound()
                        localctx.bodies.append(localctx._compound) 
                    self.state = 160
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

                self.state = 163
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__5:
                    self.state = 161
                    self.match(DMFParser.T__5)
                    self.state = 162
                    localctx.else_body = self.compound()


                pass

            elif la_ == 5:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 165
                self.expr(0)
                self.state = 166
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 6:
                localctx = DMFParser.Loop_statContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 168
                self.loop()
                pass

            elif la_ == 7:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 169
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
        self.enterRule(localctx, 10, self.RULE_compound)
        self._la = 0 # Token type
        try:
            self.state = 188
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__6]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 172
                self.match(DMFParser.T__6)
                self.state = 176
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__4) | (1 << DMFParser.T__6) | (1 << DMFParser.T__8) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__16) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61))) != 0) or ((((_la - 65)) & ~0x3f) == 0 and ((1 << (_la - 65)) & ((1 << (DMFParser.T__64 - 65)) | (1 << (DMFParser.T__65 - 65)) | (1 << (DMFParser.T__66 - 65)) | (1 << (DMFParser.T__67 - 65)) | (1 << (DMFParser.T__68 - 65)) | (1 << (DMFParser.T__69 - 65)) | (1 << (DMFParser.T__70 - 65)) | (1 << (DMFParser.T__71 - 65)) | (1 << (DMFParser.T__72 - 65)) | (1 << (DMFParser.T__73 - 65)) | (1 << (DMFParser.T__74 - 65)) | (1 << (DMFParser.T__75 - 65)) | (1 << (DMFParser.T__76 - 65)) | (1 << (DMFParser.T__77 - 65)) | (1 << (DMFParser.T__78 - 65)) | (1 << (DMFParser.T__79 - 65)) | (1 << (DMFParser.T__80 - 65)) | (1 << (DMFParser.T__81 - 65)) | (1 << (DMFParser.T__82 - 65)) | (1 << (DMFParser.T__83 - 65)) | (1 << (DMFParser.T__84 - 65)) | (1 << (DMFParser.T__85 - 65)) | (1 << (DMFParser.T__86 - 65)) | (1 << (DMFParser.T__87 - 65)) | (1 << (DMFParser.T__88 - 65)) | (1 << (DMFParser.T__89 - 65)) | (1 << (DMFParser.T__90 - 65)) | (1 << (DMFParser.T__93 - 65)) | (1 << (DMFParser.T__94 - 65)) | (1 << (DMFParser.T__99 - 65)) | (1 << (DMFParser.T__120 - 65)) | (1 << (DMFParser.T__123 - 65)))) != 0) or ((((_la - 129)) & ~0x3f) == 0 and ((1 << (_la - 129)) & ((1 << (DMFParser.T__128 - 129)) | (1 << (DMFParser.T__129 - 129)) | (1 << (DMFParser.T__131 - 129)) | (1 << (DMFParser.T__132 - 129)) | (1 << (DMFParser.T__143 - 129)) | (1 << (DMFParser.T__144 - 129)) | (1 << (DMFParser.T__145 - 129)) | (1 << (DMFParser.T__146 - 129)) | (1 << (DMFParser.T__147 - 129)) | (1 << (DMFParser.T__148 - 129)) | (1 << (DMFParser.T__149 - 129)) | (1 << (DMFParser.T__150 - 129)) | (1 << (DMFParser.T__151 - 129)) | (1 << (DMFParser.T__152 - 129)) | (1 << (DMFParser.T__153 - 129)) | (1 << (DMFParser.T__154 - 129)) | (1 << (DMFParser.T__155 - 129)) | (1 << (DMFParser.T__156 - 129)) | (1 << (DMFParser.T__157 - 129)) | (1 << (DMFParser.T__158 - 129)) | (1 << (DMFParser.INTERACTIVE - 129)) | (1 << (DMFParser.LOCAL - 129)) | (1 << (DMFParser.NOT - 129)) | (1 << (DMFParser.OFF - 129)) | (1 << (DMFParser.ON - 129)) | (1 << (DMFParser.SUB - 129)) | (1 << (DMFParser.TOGGLE - 129)) | (1 << (DMFParser.ID - 129)) | (1 << (DMFParser.INT - 129)) | (1 << (DMFParser.FLOAT - 129)) | (1 << (DMFParser.STRING - 129)))) != 0):
                    self.state = 173
                    self.stat()
                    self.state = 178
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 179
                self.match(DMFParser.T__7)
                pass
            elif token in [DMFParser.T__8]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 180
                self.match(DMFParser.T__8)
                self.state = 184
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__4) | (1 << DMFParser.T__6) | (1 << DMFParser.T__8) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__16) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61))) != 0) or ((((_la - 65)) & ~0x3f) == 0 and ((1 << (_la - 65)) & ((1 << (DMFParser.T__64 - 65)) | (1 << (DMFParser.T__65 - 65)) | (1 << (DMFParser.T__66 - 65)) | (1 << (DMFParser.T__67 - 65)) | (1 << (DMFParser.T__68 - 65)) | (1 << (DMFParser.T__69 - 65)) | (1 << (DMFParser.T__70 - 65)) | (1 << (DMFParser.T__71 - 65)) | (1 << (DMFParser.T__72 - 65)) | (1 << (DMFParser.T__73 - 65)) | (1 << (DMFParser.T__74 - 65)) | (1 << (DMFParser.T__75 - 65)) | (1 << (DMFParser.T__76 - 65)) | (1 << (DMFParser.T__77 - 65)) | (1 << (DMFParser.T__78 - 65)) | (1 << (DMFParser.T__79 - 65)) | (1 << (DMFParser.T__80 - 65)) | (1 << (DMFParser.T__81 - 65)) | (1 << (DMFParser.T__82 - 65)) | (1 << (DMFParser.T__83 - 65)) | (1 << (DMFParser.T__84 - 65)) | (1 << (DMFParser.T__85 - 65)) | (1 << (DMFParser.T__86 - 65)) | (1 << (DMFParser.T__87 - 65)) | (1 << (DMFParser.T__88 - 65)) | (1 << (DMFParser.T__89 - 65)) | (1 << (DMFParser.T__90 - 65)) | (1 << (DMFParser.T__93 - 65)) | (1 << (DMFParser.T__94 - 65)) | (1 << (DMFParser.T__99 - 65)) | (1 << (DMFParser.T__120 - 65)) | (1 << (DMFParser.T__123 - 65)))) != 0) or ((((_la - 129)) & ~0x3f) == 0 and ((1 << (_la - 129)) & ((1 << (DMFParser.T__128 - 129)) | (1 << (DMFParser.T__129 - 129)) | (1 << (DMFParser.T__131 - 129)) | (1 << (DMFParser.T__132 - 129)) | (1 << (DMFParser.T__143 - 129)) | (1 << (DMFParser.T__144 - 129)) | (1 << (DMFParser.T__145 - 129)) | (1 << (DMFParser.T__146 - 129)) | (1 << (DMFParser.T__147 - 129)) | (1 << (DMFParser.T__148 - 129)) | (1 << (DMFParser.T__149 - 129)) | (1 << (DMFParser.T__150 - 129)) | (1 << (DMFParser.T__151 - 129)) | (1 << (DMFParser.T__152 - 129)) | (1 << (DMFParser.T__153 - 129)) | (1 << (DMFParser.T__154 - 129)) | (1 << (DMFParser.T__155 - 129)) | (1 << (DMFParser.T__156 - 129)) | (1 << (DMFParser.T__157 - 129)) | (1 << (DMFParser.T__158 - 129)) | (1 << (DMFParser.INTERACTIVE - 129)) | (1 << (DMFParser.LOCAL - 129)) | (1 << (DMFParser.NOT - 129)) | (1 << (DMFParser.OFF - 129)) | (1 << (DMFParser.ON - 129)) | (1 << (DMFParser.SUB - 129)) | (1 << (DMFParser.TOGGLE - 129)) | (1 << (DMFParser.ID - 129)) | (1 << (DMFParser.INT - 129)) | (1 << (DMFParser.FLOAT - 129)) | (1 << (DMFParser.STRING - 129)))) != 0):
                    self.state = 181
                    self.stat()
                    self.state = 186
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 187
                self.match(DMFParser.T__9)
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


    class LoopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return DMFParser.RULE_loop

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class For_loopContext(LoopContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.LoopContext
            super().__init__(parser)
            self.var = None # NameContext
            self.start = None # ExprContext
            self.stop = None # ExprContext
            self.step = None # ExprContext
            self.body = None # StatContext
            self.copyFrom(ctx)

        def term_punct(self):
            return self.getTypedRuleContext(DMFParser.Term_punctContext,0)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)

        def stat(self):
            return self.getTypedRuleContext(DMFParser.StatContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFor_loop" ):
                listener.enterFor_loop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFor_loop" ):
                listener.exitFor_loop(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFor_loop" ):
                return visitor.visitFor_loop(self)
            else:
                return visitor.visitChildren(self)


    class Repeat_loopContext(LoopContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.LoopContext
            super().__init__(parser)
            self.n = None # ExprContext
            self.body = None # StatContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)

        def stat(self):
            return self.getTypedRuleContext(DMFParser.StatContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRepeat_loop" ):
                listener.enterRepeat_loop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRepeat_loop" ):
                listener.exitRepeat_loop(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRepeat_loop" ):
                return visitor.visitRepeat_loop(self)
            else:
                return visitor.visitChildren(self)



    def loop(self):

        localctx = DMFParser.LoopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_loop)
        try:
            self.state = 208
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__10]:
                localctx = DMFParser.Repeat_loopContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 190
                self.match(DMFParser.T__10)
                self.state = 191
                localctx.n = self.expr(0)
                self.state = 192
                self.match(DMFParser.T__11)
                self.state = 193
                localctx.body = self.stat()
                pass
            elif token in [DMFParser.T__12]:
                localctx = DMFParser.For_loopContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 195
                self.match(DMFParser.T__12)
                self.state = 196
                localctx.var = self.name()
                self.state = 197
                self.match(DMFParser.T__13)
                self.state = 198
                self.match(DMFParser.T__14)
                self.state = 199
                localctx.start = self.expr(0)
                self.state = 200
                self.match(DMFParser.T__1)
                self.state = 201
                localctx.stop = self.expr(0)
                self.state = 202
                self.term_punct()

                self.state = 203
                self.match(DMFParser.T__15)
                self.state = 204
                localctx.step = self.expr(0)
                self.state = 206
                localctx.body = self.stat()
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


    class Term_punctContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.is_closed = None

        def CLOSE_BRACKET(self):
            return self.getToken(DMFParser.CLOSE_BRACKET, 0)

        def CLOSE_PAREN(self):
            return self.getToken(DMFParser.CLOSE_PAREN, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_term_punct

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm_punct" ):
                listener.enterTerm_punct(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm_punct" ):
                listener.exitTerm_punct(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm_punct" ):
                return visitor.visitTerm_punct(self)
            else:
                return visitor.visitChildren(self)




    def term_punct(self):

        localctx = DMFParser.Term_punctContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_term_punct)
        try:
            self.state = 214
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.CLOSE_BRACKET]:
                self.enterOuterAlt(localctx, 1)
                self.state = 210
                self.match(DMFParser.CLOSE_BRACKET)
                localctx.is_closed=True
                pass
            elif token in [DMFParser.CLOSE_PAREN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 212
                self.match(DMFParser.CLOSE_PAREN)
                localctx.is_closed=False
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

        def CLOSE_PAREN(self):
            return self.getToken(DMFParser.CLOSE_PAREN, 0)

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


    class Unit_string_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.quant = None # ExprContext
            self.copyFrom(ctx)

        def dim_unit(self):
            return self.getTypedRuleContext(DMFParser.Dim_unitContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnit_string_expr" ):
                listener.enterUnit_string_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnit_string_expr" ):
                listener.exitUnit_string_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnit_string_expr" ):
                return visitor.visitUnit_string_expr(self)
            else:
                return visitor.visitChildren(self)


    class Action_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def no_arg_action(self):
            return self.getTypedRuleContext(DMFParser.No_arg_actionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAction_expr" ):
                listener.enterAction_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAction_expr" ):
                listener.exitAction_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAction_expr" ):
                return visitor.visitAction_expr(self)
            else:
                return visitor.visitChildren(self)


    class Attr_assign_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.obj = None # ExprContext
            self.what = None # ExprContext
            self.copyFrom(ctx)

        def ATTR(self):
            return self.getToken(DMFParser.ATTR, 0)
        def attr(self):
            return self.getTypedRuleContext(DMFParser.AttrContext,0)

        def assign_op(self):
            return self.getTypedRuleContext(DMFParser.Assign_opContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr_assign_expr" ):
                listener.enterAttr_assign_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr_assign_expr" ):
                listener.exitAttr_assign_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr_assign_expr" ):
                return visitor.visitAttr_assign_expr(self)
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


    class Unit_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.amount = None # ExprContext
            self.copyFrom(ctx)

        def dim_unit(self):
            return self.getTypedRuleContext(DMFParser.Dim_unitContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnit_expr" ):
                listener.enterUnit_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnit_expr" ):
                listener.exitUnit_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnit_expr" ):
                return visitor.visitUnit_expr(self)
            else:
                return visitor.visitChildren(self)


    class Temperature_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.amount = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTemperature_expr" ):
                listener.enterTemperature_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTemperature_expr" ):
                listener.exitTemperature_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTemperature_expr" ):
                return visitor.visitTemperature_expr(self)
            else:
                return visitor.visitChildren(self)


    class Index_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.who = None # ExprContext
            self.which = None # ExprContext
            self.copyFrom(ctx)

        def CLOSE_BRACKET(self):
            return self.getToken(DMFParser.CLOSE_BRACKET, 0)
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


    class Numbered_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.kind = None # Numbered_typeContext
            self.which = None # ExprContext
            self.copyFrom(ctx)

        def numbered_type(self):
            return self.getTypedRuleContext(DMFParser.Numbered_typeContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumbered_expr" ):
                listener.enterNumbered_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumbered_expr" ):
                listener.exitNumbered_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumbered_expr" ):
                return visitor.visitNumbered_expr(self)
            else:
                return visitor.visitChildren(self)


    class Rel_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.lhs = None # ExprContext
            self.rhs = None # ExprContext
            self.copyFrom(ctx)

        def rel(self):
            return self.getTypedRuleContext(DMFParser.RelContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRel_expr" ):
                listener.enterRel_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRel_expr" ):
                listener.exitRel_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRel_expr" ):
                return visitor.visitRel_expr(self)
            else:
                return visitor.visitChildren(self)


    class Name_assign_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.which = None # NameContext
            self.what = None # ExprContext
            self.ptype = None # Param_typeContext
            self.n = None # Token
            self.copyFrom(ctx)

        def assign_op(self):
            return self.getTypedRuleContext(DMFParser.Assign_opContext,0)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)

        def param_type(self):
            return self.getTypedRuleContext(DMFParser.Param_typeContext,0)

        def INT(self):
            return self.getToken(DMFParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterName_assign_expr" ):
                listener.enterName_assign_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitName_assign_expr" ):
                listener.exitName_assign_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitName_assign_expr" ):
                return visitor.visitName_assign_expr(self)
            else:
                return visitor.visitChildren(self)


    class String_lit_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def string(self):
            return self.getTypedRuleContext(DMFParser.StringContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString_lit_expr" ):
                listener.enterString_lit_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString_lit_expr" ):
                listener.exitString_lit_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString_lit_expr" ):
                return visitor.visitString_lit_expr(self)
            else:
                return visitor.visitChildren(self)


    class Not_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(DMFParser.NOT, 0)
        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNot_expr" ):
                listener.enterNot_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNot_expr" ):
                listener.exitNot_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNot_expr" ):
                return visitor.visitNot_expr(self)
            else:
                return visitor.visitChildren(self)


    class Reagent_lit_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def reagent(self):
            return self.getTypedRuleContext(DMFParser.ReagentContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReagent_lit_expr" ):
                listener.enterReagent_lit_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReagent_lit_expr" ):
                listener.exitReagent_lit_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReagent_lit_expr" ):
                return visitor.visitReagent_lit_expr(self)
            else:
                return visitor.visitChildren(self)


    class And_exprContext(ExprContext):

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


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnd_expr" ):
                listener.enterAnd_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnd_expr" ):
                listener.exitAnd_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnd_expr" ):
                return visitor.visitAnd_expr(self)
            else:
                return visitor.visitChildren(self)


    class Magnitude_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.quant = None # ExprContext
            self.copyFrom(ctx)

        def ATTR(self):
            return self.getToken(DMFParser.ATTR, 0)
        def dim_unit(self):
            return self.getTypedRuleContext(DMFParser.Dim_unitContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMagnitude_expr" ):
                listener.enterMagnitude_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMagnitude_expr" ):
                listener.exitMagnitude_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMagnitude_expr" ):
                return visitor.visitMagnitude_expr(self)
            else:
                return visitor.visitChildren(self)


    class In_dir_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.dist = None # ExprContext
            self.d = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIn_dir_expr" ):
                listener.enterIn_dir_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIn_dir_expr" ):
                listener.exitIn_dir_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIn_dir_expr" ):
                return visitor.visitIn_dir_expr(self)
            else:
                return visitor.visitChildren(self)


    class Or_exprContext(ExprContext):

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


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOr_expr" ):
                listener.enterOr_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOr_expr" ):
                listener.exitOr_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOr_expr" ):
                return visitor.visitOr_expr(self)
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


    class Drop_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.vol = None # ExprContext
            self.loc = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


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
            self.func = None # ExprContext
            self._expr = None # ExprContext
            self.args = list() # of ExprContexts
            self.copyFrom(ctx)

        def CLOSE_PAREN(self):
            return self.getToken(DMFParser.CLOSE_PAREN, 0)
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


    class Bool_const_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.val = None # Bool_valContext
            self.copyFrom(ctx)

        def bool_val(self):
            return self.getTypedRuleContext(DMFParser.Bool_valContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBool_const_expr" ):
                listener.enterBool_const_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBool_const_expr" ):
                listener.exitBool_const_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBool_const_expr" ):
                return visitor.visitBool_const_expr(self)
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


    class Has_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.obj = None # ExprContext
            self.copyFrom(ctx)

        def attr(self):
            return self.getTypedRuleContext(DMFParser.AttrContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHas_expr" ):
                listener.enterHas_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHas_expr" ):
                listener.exitHas_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHas_expr" ):
                return visitor.visitHas_expr(self)
            else:
                return visitor.visitChildren(self)


    class Float_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(DMFParser.FLOAT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloat_expr" ):
                listener.enterFloat_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloat_expr" ):
                listener.exitFloat_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloat_expr" ):
                return visitor.visitFloat_expr(self)
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


    class Turn_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.start_dir = None # ExprContext
            self.copyFrom(ctx)

        def turn(self):
            return self.getTypedRuleContext(DMFParser.TurnContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTurn_expr" ):
                listener.enterTurn_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTurn_expr" ):
                listener.exitTurn_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTurn_expr" ):
                return visitor.visitTurn_expr(self)
            else:
                return visitor.visitChildren(self)


    class Cond_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.first = None # ExprContext
            self.cond = None # ExprContext
            self.second = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCond_expr" ):
                listener.enterCond_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCond_expr" ):
                listener.exitCond_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCond_expr" ):
                return visitor.visitCond_expr(self)
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


    class Mw_name_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def multi_word_name(self):
            return self.getTypedRuleContext(DMFParser.Multi_word_nameContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMw_name_expr" ):
                listener.enterMw_name_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMw_name_expr" ):
                listener.exitMw_name_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMw_name_expr" ):
                return visitor.visitMw_name_expr(self)
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


    class Liquid_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.vol = None # ExprContext
            self.which = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiquid_expr" ):
                listener.enterLiquid_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiquid_expr" ):
                listener.exitLiquid_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiquid_expr" ):
                return visitor.visitLiquid_expr(self)
            else:
                return visitor.visitChildren(self)


    class Reagent_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.which = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReagent_expr" ):
                listener.enterReagent_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReagent_expr" ):
                listener.exitReagent_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReagent_expr" ):
                return visitor.visitReagent_expr(self)
            else:
                return visitor.visitChildren(self)


    class Dir_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def direction(self):
            return self.getTypedRuleContext(DMFParser.DirectionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDir_expr" ):
                listener.enterDir_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDir_expr" ):
                listener.exitDir_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDir_expr" ):
                return visitor.visitDir_expr(self)
            else:
                return visitor.visitChildren(self)


    class Coord_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.x = None # ExprContext
            self.y = None # ExprContext
            self.copyFrom(ctx)

        def CLOSE_PAREN(self):
            return self.getToken(DMFParser.CLOSE_PAREN, 0)
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


    class Is_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.obj = None # ExprContext
            self.pred = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)

        def ISNT(self):
            return self.getToken(DMFParser.ISNT, 0)
        def NOT(self):
            return self.getToken(DMFParser.NOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIs_expr" ):
                listener.enterIs_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIs_expr" ):
                listener.exitIs_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIs_expr" ):
                return visitor.visitIs_expr(self)
            else:
                return visitor.visitChildren(self)


    class Attr_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.obj = None # ExprContext
            self.copyFrom(ctx)

        def ATTR(self):
            return self.getToken(DMFParser.ATTR, 0)
        def attr(self):
            return self.getTypedRuleContext(DMFParser.AttrContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr_expr" ):
                listener.enterAttr_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr_expr" ):
                listener.exitAttr_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr_expr" ):
                return visitor.visitAttr_expr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = DMFParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 16
        self.enterRecursionRule(localctx, 16, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 290
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,25,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 217
                self.match(DMFParser.T__16)
                self.state = 218
                self.expr(0)
                self.state = 219
                self.match(DMFParser.CLOSE_PAREN)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 221
                self.match(DMFParser.T__16)
                self.state = 222
                localctx.x = self.expr(0)
                self.state = 223
                self.match(DMFParser.T__1)
                self.state = 224
                localctx.y = self.expr(0)
                self.state = 225
                self.match(DMFParser.CLOSE_PAREN)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 227
                self.match(DMFParser.SUB)
                self.state = 228
                localctx.rhs = self.expr(45)
                pass

            elif la_ == 4:
                localctx = DMFParser.Numbered_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 229
                localctx.kind = self.numbered_type()
                self.state = 230
                self.match(DMFParser.T__17)
                self.state = 231
                localctx.which = self.expr(43)
                pass

            elif la_ == 5:
                localctx = DMFParser.Const_rc_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 233
                localctx._INT = self.match(DMFParser.INT)
                self.state = 234
                self.rc((0 if localctx._INT is None else int(localctx._INT.text)))
                pass

            elif la_ == 6:
                localctx = DMFParser.Reagent_lit_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 236
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__26:
                    self.state = 235
                    self.match(DMFParser.T__26)


                self.state = 238
                self.reagent()
                self.state = 240
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
                if la_ == 1:
                    self.state = 239
                    self.match(DMFParser.T__27)


                pass

            elif la_ == 7:
                localctx = DMFParser.Reagent_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 243
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__20 or _la==DMFParser.T__26:
                    self.state = 242
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__20 or _la==DMFParser.T__26):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 245
                self.match(DMFParser.T__27)
                self.state = 247
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__28:
                    self.state = 246
                    self.match(DMFParser.T__28)


                self.state = 249
                localctx.which = self.expr(32)
                pass

            elif la_ == 8:
                localctx = DMFParser.Not_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 250
                self.match(DMFParser.NOT)
                self.state = 251
                self.expr(25)
                pass

            elif la_ == 9:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 252
                self.direction()
                self.state = 253
                localctx.dist = self.expr(22)
                pass

            elif la_ == 10:
                localctx = DMFParser.Dir_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 255
                self.direction()
                pass

            elif la_ == 11:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 256
                self.match(DMFParser.T__35)
                self.state = 258
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__52) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55))) != 0):
                    self.state = 257
                    self.axis()


                self.state = 260
                localctx.which = self.expr(20)
                pass

            elif la_ == 12:
                localctx = DMFParser.Pause_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 261
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__2 or _la==DMFParser.T__3):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 262
                localctx.duration = self.expr(19)
                pass

            elif la_ == 13:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 263
                self.match(DMFParser.T__36)
                self.state = 264
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__37 or _la==DMFParser.T__38):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 265
                localctx.loc = self.expr(17)
                pass

            elif la_ == 14:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 266
                self.macro_def()
                pass

            elif la_ == 15:
                localctx = DMFParser.Action_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 267
                self.no_arg_action()
                pass

            elif la_ == 16:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 269
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__26:
                    self.state = 268
                    self.match(DMFParser.T__26)


                self.state = 271
                self.param_type()
                pass

            elif la_ == 17:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 272
                self.param_type()
                self.state = 273
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 18:
                localctx = DMFParser.Bool_const_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 275
                localctx.val = self.bool_val()
                pass

            elif la_ == 19:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 276
                self.name()
                pass

            elif la_ == 20:
                localctx = DMFParser.Mw_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 277
                self.multi_word_name()
                pass

            elif la_ == 21:
                localctx = DMFParser.Name_assign_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 278
                localctx.which = self.name()
                self.state = 279
                self.assign_op()
                self.state = 280
                localctx.what = self.expr(6)
                pass

            elif la_ == 22:
                localctx = DMFParser.Name_assign_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 282
                localctx.ptype = self.param_type()
                self.state = 283
                localctx.n = self.match(DMFParser.INT)
                self.state = 284
                self.assign_op()
                self.state = 285
                localctx.what = self.expr(4)
                pass

            elif la_ == 23:
                localctx = DMFParser.String_lit_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 287
                self.string()
                pass

            elif la_ == 24:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 288
                localctx._INT = self.match(DMFParser.INT)
                pass

            elif la_ == 25:
                localctx = DMFParser.Float_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 289
                self.match(DMFParser.FLOAT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 393
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,32,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 391
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.In_dir_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 292
                        if not self.precpred(self._ctx, 38):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 38)")
                        self.state = 293
                        self.match(DMFParser.T__13)
                        self.state = 294
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__23 or _la==DMFParser.T__24):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 295
                        localctx.d = self.expr(39)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Liquid_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.vol = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 296
                        if not self.precpred(self._ctx, 31):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 31)")
                        self.state = 297
                        self.match(DMFParser.T__29)
                        self.state = 298
                        localctx.which = self.expr(32)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 299
                        if not self.precpred(self._ctx, 30):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 30)")
                        self.state = 300
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 301
                        localctx.rhs = self.expr(31)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 302
                        if not self.precpred(self._ctx, 29):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 29)")
                        self.state = 303
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 304
                        localctx.rhs = self.expr(30)
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.Rel_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 305
                        if not self.precpred(self._ctx, 28):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 28)")
                        self.state = 306
                        self.rel()
                        self.state = 307
                        localctx.rhs = self.expr(29)
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Is_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 309
                        if not self.precpred(self._ctx, 26):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 26)")
                        self.state = 315
                        self._errHandler.sync(self)
                        token = self._input.LA(1)
                        if token in [DMFParser.T__32]:
                            self.state = 310
                            self.match(DMFParser.T__32)
                            self.state = 312
                            self._errHandler.sync(self)
                            la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
                            if la_ == 1:
                                self.state = 311
                                self.match(DMFParser.NOT)


                            pass
                        elif token in [DMFParser.ISNT]:
                            self.state = 314
                            self.match(DMFParser.ISNT)
                            pass
                        else:
                            raise NoViableAltException(self)

                        self.state = 317
                        localctx.pred = self.expr(27)
                        pass

                    elif la_ == 7:
                        localctx = DMFParser.And_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 318
                        if not self.precpred(self._ctx, 24):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 24)")
                        self.state = 319
                        self.match(DMFParser.T__33)
                        self.state = 320
                        localctx.rhs = self.expr(25)
                        pass

                    elif la_ == 8:
                        localctx = DMFParser.Or_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 321
                        if not self.precpred(self._ctx, 23):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 23)")
                        self.state = 322
                        self.match(DMFParser.T__34)
                        self.state = 323
                        localctx.rhs = self.expr(24)
                        pass

                    elif la_ == 9:
                        localctx = DMFParser.Drop_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.vol = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 324
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 325
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__37 or _la==DMFParser.T__38):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 326
                        localctx.loc = self.expr(17)
                        pass

                    elif la_ == 10:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 327
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 328
                        self.match(DMFParser.INJECT)
                        self.state = 329
                        localctx.what = self.expr(16)
                        pass

                    elif la_ == 11:
                        localctx = DMFParser.Cond_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.first = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 330
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 331
                        self.match(DMFParser.T__4)
                        self.state = 332
                        localctx.cond = self.expr(0)
                        self.state = 333
                        self.match(DMFParser.T__5)
                        self.state = 334
                        localctx.second = self.expr(15)
                        pass

                    elif la_ == 12:
                        localctx = DMFParser.Attr_assign_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 336
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 337
                        self.match(DMFParser.ATTR)
                        self.state = 338
                        self.attr()
                        self.state = 339
                        self.assign_op()
                        self.state = 340
                        localctx.what = self.expr(6)
                        pass

                    elif la_ == 13:
                        localctx = DMFParser.Function_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.func = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 342
                        if not self.precpred(self._ctx, 47):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 47)")
                        self.state = 343
                        self.match(DMFParser.T__16)
                        self.state = 352
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__16) | (1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61))) != 0) or ((((_la - 65)) & ~0x3f) == 0 and ((1 << (_la - 65)) & ((1 << (DMFParser.T__64 - 65)) | (1 << (DMFParser.T__65 - 65)) | (1 << (DMFParser.T__66 - 65)) | (1 << (DMFParser.T__67 - 65)) | (1 << (DMFParser.T__68 - 65)) | (1 << (DMFParser.T__69 - 65)) | (1 << (DMFParser.T__70 - 65)) | (1 << (DMFParser.T__71 - 65)) | (1 << (DMFParser.T__72 - 65)) | (1 << (DMFParser.T__73 - 65)) | (1 << (DMFParser.T__74 - 65)) | (1 << (DMFParser.T__75 - 65)) | (1 << (DMFParser.T__76 - 65)) | (1 << (DMFParser.T__77 - 65)) | (1 << (DMFParser.T__78 - 65)) | (1 << (DMFParser.T__79 - 65)) | (1 << (DMFParser.T__80 - 65)) | (1 << (DMFParser.T__81 - 65)) | (1 << (DMFParser.T__82 - 65)) | (1 << (DMFParser.T__83 - 65)) | (1 << (DMFParser.T__84 - 65)) | (1 << (DMFParser.T__85 - 65)) | (1 << (DMFParser.T__86 - 65)) | (1 << (DMFParser.T__87 - 65)) | (1 << (DMFParser.T__88 - 65)) | (1 << (DMFParser.T__89 - 65)) | (1 << (DMFParser.T__90 - 65)) | (1 << (DMFParser.T__93 - 65)) | (1 << (DMFParser.T__94 - 65)) | (1 << (DMFParser.T__99 - 65)) | (1 << (DMFParser.T__120 - 65)) | (1 << (DMFParser.T__123 - 65)))) != 0) or ((((_la - 129)) & ~0x3f) == 0 and ((1 << (_la - 129)) & ((1 << (DMFParser.T__128 - 129)) | (1 << (DMFParser.T__129 - 129)) | (1 << (DMFParser.T__131 - 129)) | (1 << (DMFParser.T__132 - 129)) | (1 << (DMFParser.T__143 - 129)) | (1 << (DMFParser.T__144 - 129)) | (1 << (DMFParser.T__145 - 129)) | (1 << (DMFParser.T__146 - 129)) | (1 << (DMFParser.T__147 - 129)) | (1 << (DMFParser.T__148 - 129)) | (1 << (DMFParser.T__149 - 129)) | (1 << (DMFParser.T__150 - 129)) | (1 << (DMFParser.T__151 - 129)) | (1 << (DMFParser.T__152 - 129)) | (1 << (DMFParser.T__153 - 129)) | (1 << (DMFParser.T__154 - 129)) | (1 << (DMFParser.T__155 - 129)) | (1 << (DMFParser.T__156 - 129)) | (1 << (DMFParser.T__157 - 129)) | (1 << (DMFParser.T__158 - 129)) | (1 << (DMFParser.INTERACTIVE - 129)) | (1 << (DMFParser.NOT - 129)) | (1 << (DMFParser.OFF - 129)) | (1 << (DMFParser.ON - 129)) | (1 << (DMFParser.SUB - 129)) | (1 << (DMFParser.TOGGLE - 129)) | (1 << (DMFParser.ID - 129)) | (1 << (DMFParser.INT - 129)) | (1 << (DMFParser.FLOAT - 129)) | (1 << (DMFParser.STRING - 129)))) != 0):
                            self.state = 344
                            localctx._expr = self.expr(0)
                            localctx.args.append(localctx._expr)
                            self.state = 349
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            while _la==DMFParser.T__1:
                                self.state = 345
                                self.match(DMFParser.T__1)
                                self.state = 346
                                localctx._expr = self.expr(0)
                                localctx.args.append(localctx._expr)
                                self.state = 351
                                self._errHandler.sync(self)
                                _la = self._input.LA(1)



                        self.state = 354
                        self.match(DMFParser.CLOSE_PAREN)
                        pass

                    elif la_ == 14:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 355
                        if not self.precpred(self._ctx, 44):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 44)")
                        self.state = 356
                        self.direction()
                        pass

                    elif la_ == 15:
                        localctx = DMFParser.Magnitude_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.quant = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 357
                        if not self.precpred(self._ctx, 42):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 42)")
                        self.state = 358
                        self.match(DMFParser.ATTR)
                        self.state = 359
                        self.match(DMFParser.T__18)
                        self.state = 360
                        self.match(DMFParser.T__13)
                        self.state = 361
                        self.dim_unit()
                        pass

                    elif la_ == 16:
                        localctx = DMFParser.Unit_string_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.quant = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 362
                        if not self.precpred(self._ctx, 41):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 41)")
                        self.state = 363
                        self.match(DMFParser.T__19)
                        self.state = 365
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==DMFParser.T__20:
                            self.state = 364
                            self.match(DMFParser.T__20)


                        self.state = 367
                        self.match(DMFParser.T__21)
                        self.state = 368
                        self.match(DMFParser.T__13)
                        self.state = 369
                        self.dim_unit()
                        pass

                    elif la_ == 17:
                        localctx = DMFParser.Attr_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 370
                        if not self.precpred(self._ctx, 40):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 40)")
                        self.state = 371
                        self.match(DMFParser.ATTR)
                        self.state = 372
                        self.attr()
                        pass

                    elif la_ == 18:
                        localctx = DMFParser.Turn_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.start_dir = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 373
                        if not self.precpred(self._ctx, 39):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 39)")
                        self.state = 374
                        self.match(DMFParser.T__22)
                        self.state = 375
                        self.turn()
                        pass

                    elif la_ == 19:
                        localctx = DMFParser.N_rc_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 376
                        if not self.precpred(self._ctx, 36):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 36)")
                        self.state = 377
                        self.rc(0)
                        pass

                    elif la_ == 20:
                        localctx = DMFParser.Unit_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 378
                        if not self.precpred(self._ctx, 35):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 35)")
                        self.state = 379
                        self.dim_unit()
                        pass

                    elif la_ == 21:
                        localctx = DMFParser.Temperature_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 380
                        if not self.precpred(self._ctx, 34):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 34)")
                        self.state = 381
                        self.match(DMFParser.T__25)
                        pass

                    elif la_ == 22:
                        localctx = DMFParser.Has_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 382
                        if not self.precpred(self._ctx, 27):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 27)")
                        self.state = 383
                        self.match(DMFParser.T__30)
                        self.state = 384
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__20 or _la==DMFParser.T__31):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 385
                        self.attr()
                        pass

                    elif la_ == 23:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 386
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 387
                        self.match(DMFParser.T__14)
                        self.state = 388
                        localctx.which = self.expr(0)
                        self.state = 389
                        self.match(DMFParser.CLOSE_BRACKET)
                        pass

             
                self.state = 395
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,32,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ReagentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.r = None


        def getRuleIndex(self):
            return DMFParser.RULE_reagent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReagent" ):
                listener.enterReagent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReagent" ):
                listener.exitReagent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReagent" ):
                return visitor.visitReagent(self)
            else:
                return visitor.visitChildren(self)




    def reagent(self):

        localctx = DMFParser.ReagentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_reagent)
        try:
            self.state = 400
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__39]:
                self.enterOuterAlt(localctx, 1)
                self.state = 396
                self.match(DMFParser.T__39)
                localctx.r = unknown_reagent
                pass
            elif token in [DMFParser.T__40]:
                self.enterOuterAlt(localctx, 2)
                self.state = 398
                self.match(DMFParser.T__40)
                localctx.r = waste_reagent
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
        self.enterRule(localctx, 20, self.RULE_direction)
        self._la = 0 # Token type
        try:
            self.state = 414
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__41, DMFParser.T__42]:
                self.enterOuterAlt(localctx, 1)
                self.state = 402
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__41 or _la==DMFParser.T__42):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__43, DMFParser.T__44]:
                self.enterOuterAlt(localctx, 2)
                self.state = 405
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__43 or _la==DMFParser.T__44):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__45, DMFParser.T__46]:
                self.enterOuterAlt(localctx, 3)
                self.state = 408
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__45 or _la==DMFParser.T__46):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__47, DMFParser.T__48]:
                self.enterOuterAlt(localctx, 4)
                self.state = 411
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__47 or _la==DMFParser.T__48):
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


    class TurnContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.t = None


        def getRuleIndex(self):
            return DMFParser.RULE_turn

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTurn" ):
                listener.enterTurn(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTurn" ):
                listener.exitTurn(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTurn" ):
                return visitor.visitTurn(self)
            else:
                return visitor.visitChildren(self)




    def turn(self):

        localctx = DMFParser.TurnContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_turn)
        self._la = 0 # Token type
        try:
            self.state = 422
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__47, DMFParser.T__49]:
                self.enterOuterAlt(localctx, 1)
                self.state = 416
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__47 or _la==DMFParser.T__49):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.RIGHT
                pass
            elif token in [DMFParser.T__45, DMFParser.T__50]:
                self.enterOuterAlt(localctx, 2)
                self.state = 418
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__45 or _la==DMFParser.T__50):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.LEFT
                pass
            elif token in [DMFParser.T__51]:
                self.enterOuterAlt(localctx, 3)
                self.state = 420
                self.match(DMFParser.T__51)
                localctx.t = Turn.AROUND
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
        self.enterRule(localctx, 24, self.RULE_rc)
        self._la = 0 # Token type
        try:
            self.state = 438
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,36,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 424
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 425
                self.match(DMFParser.T__52)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 428
                self.match(DMFParser.T__53)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 431
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 432
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__54 or _la==DMFParser.T__55):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 435
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__56 or _la==DMFParser.T__57):
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
        self.enterRule(localctx, 26, self.RULE_axis)
        self._la = 0 # Token type
        try:
            self.state = 444
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__52]:
                self.enterOuterAlt(localctx, 1)
                self.state = 440
                self.match(DMFParser.T__52)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__54, DMFParser.T__55]:
                self.enterOuterAlt(localctx, 2)
                self.state = 442
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__54 or _la==DMFParser.T__55):
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
        self.enterRule(localctx, 28, self.RULE_macro_def)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 446
            self.macro_header()
            self.state = 449
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__6, DMFParser.T__8]:
                self.state = 447
                self.compound()
                pass
            elif token in [DMFParser.T__2, DMFParser.T__3, DMFParser.T__16, DMFParser.T__20, DMFParser.T__21, DMFParser.T__23, DMFParser.T__24, DMFParser.T__26, DMFParser.T__27, DMFParser.T__35, DMFParser.T__36, DMFParser.T__39, DMFParser.T__40, DMFParser.T__41, DMFParser.T__42, DMFParser.T__43, DMFParser.T__44, DMFParser.T__45, DMFParser.T__46, DMFParser.T__47, DMFParser.T__48, DMFParser.T__58, DMFParser.T__59, DMFParser.T__60, DMFParser.T__61, DMFParser.T__64, DMFParser.T__65, DMFParser.T__66, DMFParser.T__67, DMFParser.T__68, DMFParser.T__69, DMFParser.T__70, DMFParser.T__71, DMFParser.T__72, DMFParser.T__73, DMFParser.T__74, DMFParser.T__75, DMFParser.T__76, DMFParser.T__77, DMFParser.T__78, DMFParser.T__79, DMFParser.T__80, DMFParser.T__81, DMFParser.T__82, DMFParser.T__83, DMFParser.T__84, DMFParser.T__85, DMFParser.T__86, DMFParser.T__87, DMFParser.T__88, DMFParser.T__89, DMFParser.T__90, DMFParser.T__93, DMFParser.T__94, DMFParser.T__99, DMFParser.T__120, DMFParser.T__123, DMFParser.T__128, DMFParser.T__129, DMFParser.T__131, DMFParser.T__132, DMFParser.T__143, DMFParser.T__144, DMFParser.T__145, DMFParser.T__146, DMFParser.T__147, DMFParser.T__148, DMFParser.T__149, DMFParser.T__150, DMFParser.T__151, DMFParser.T__152, DMFParser.T__153, DMFParser.T__154, DMFParser.T__155, DMFParser.T__156, DMFParser.T__157, DMFParser.T__158, DMFParser.INTERACTIVE, DMFParser.NOT, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT, DMFParser.FLOAT, DMFParser.STRING]:
                self.state = 448
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

        def CLOSE_PAREN(self):
            return self.getToken(DMFParser.CLOSE_PAREN, 0)

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
        self.enterRule(localctx, 30, self.RULE_macro_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 451
            self.match(DMFParser.T__58)
            self.state = 452
            self.match(DMFParser.T__16)
            self.state = 461
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__20) | (1 << DMFParser.T__21) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__27) | (1 << DMFParser.T__31) | (1 << DMFParser.T__36) | (1 << DMFParser.T__60))) != 0) or ((((_la - 65)) & ~0x3f) == 0 and ((1 << (_la - 65)) & ((1 << (DMFParser.T__64 - 65)) | (1 << (DMFParser.T__65 - 65)) | (1 << (DMFParser.T__66 - 65)) | (1 << (DMFParser.T__67 - 65)) | (1 << (DMFParser.T__68 - 65)) | (1 << (DMFParser.T__69 - 65)) | (1 << (DMFParser.T__70 - 65)) | (1 << (DMFParser.T__71 - 65)) | (1 << (DMFParser.T__72 - 65)) | (1 << (DMFParser.T__73 - 65)) | (1 << (DMFParser.T__74 - 65)) | (1 << (DMFParser.T__75 - 65)) | (1 << (DMFParser.T__76 - 65)) | (1 << (DMFParser.T__77 - 65)) | (1 << (DMFParser.T__78 - 65)) | (1 << (DMFParser.T__79 - 65)) | (1 << (DMFParser.T__80 - 65)) | (1 << (DMFParser.T__81 - 65)) | (1 << (DMFParser.T__82 - 65)) | (1 << (DMFParser.T__83 - 65)) | (1 << (DMFParser.T__84 - 65)) | (1 << (DMFParser.T__85 - 65)) | (1 << (DMFParser.T__86 - 65)) | (1 << (DMFParser.T__87 - 65)) | (1 << (DMFParser.T__88 - 65)) | (1 << (DMFParser.T__89 - 65)) | (1 << (DMFParser.T__90 - 65)) | (1 << (DMFParser.T__93 - 65)) | (1 << (DMFParser.T__94 - 65)) | (1 << (DMFParser.T__99 - 65)) | (1 << (DMFParser.T__120 - 65)) | (1 << (DMFParser.T__123 - 65)))) != 0) or ((((_la - 129)) & ~0x3f) == 0 and ((1 << (_la - 129)) & ((1 << (DMFParser.T__128 - 129)) | (1 << (DMFParser.T__129 - 129)) | (1 << (DMFParser.T__131 - 129)) | (1 << (DMFParser.T__132 - 129)) | (1 << (DMFParser.T__155 - 129)) | (1 << (DMFParser.T__156 - 129)) | (1 << (DMFParser.T__157 - 129)) | (1 << (DMFParser.T__158 - 129)) | (1 << (DMFParser.INTERACTIVE - 129)) | (1 << (DMFParser.OFF - 129)) | (1 << (DMFParser.ON - 129)) | (1 << (DMFParser.ID - 129)))) != 0):
                self.state = 453
                self.param()
                self.state = 458
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__1:
                    self.state = 454
                    self.match(DMFParser.T__1)
                    self.state = 455
                    self.param()
                    self.state = 460
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 463
            self.match(DMFParser.CLOSE_PAREN)
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
            self.deprecated = None
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
        self.enterRule(localctx, 32, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.state = 488
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,42,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 466
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__20 or _la==DMFParser.T__31:
                    self.state = 465
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__20 or _la==DMFParser.T__31):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 468
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 471
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 473
                localctx._INT = self.match(DMFParser.INT)
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 476
                localctx._param_type = self.param_type()
                self.state = 477
                localctx._name = self.name()
                localctx.type=localctx._param_type.type
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 481
                localctx._name = self.name()
                self.state = 482
                self.match(DMFParser.INJECT)
                self.state = 483
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                localctx.deprecated=True
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class No_arg_actionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.which = None

        def ON(self):
            return self.getToken(DMFParser.ON, 0)

        def OFF(self):
            return self.getToken(DMFParser.OFF, 0)

        def TOGGLE(self):
            return self.getToken(DMFParser.TOGGLE, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_no_arg_action

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNo_arg_action" ):
                listener.enterNo_arg_action(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNo_arg_action" ):
                listener.exitNo_arg_action(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNo_arg_action" ):
                return visitor.visitNo_arg_action(self)
            else:
                return visitor.visitChildren(self)




    def no_arg_action(self):

        localctx = DMFParser.No_arg_actionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_no_arg_action)
        self._la = 0 # Token type
        try:
            self.state = 522
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,46,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 490
                self.match(DMFParser.T__59)
                self.state = 491
                self.match(DMFParser.ON)
                localctx.which="TURN-ON"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 493
                self.match(DMFParser.T__59)
                self.state = 494
                self.match(DMFParser.OFF)
                localctx.which="TURN-OFF"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 496
                self.match(DMFParser.TOGGLE)
                self.state = 498
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,43,self._ctx)
                if la_ == 1:
                    self.state = 497
                    self.match(DMFParser.T__60)


                localctx.which="TOGGLE"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 501
                self.match(DMFParser.T__61)
                self.state = 507
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,45,self._ctx)
                if la_ == 1:
                    self.state = 502
                    self.match(DMFParser.T__62)
                    self.state = 504
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==DMFParser.T__26:
                        self.state = 503
                        self.match(DMFParser.T__26)


                    self.state = 506
                    self.match(DMFParser.T__63)


                localctx.which="REMOVE-FROM-BOARD"
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 510
                self.match(DMFParser.T__64)
                self.state = 511
                self.match(DMFParser.T__65)
                localctx.which="RESET PADS"
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 513
                self.match(DMFParser.T__64)
                self.state = 514
                self.match(DMFParser.T__66)
                localctx.which="RESET MAGNETS"
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 516
                self.match(DMFParser.T__64)
                self.state = 517
                self.match(DMFParser.T__67)
                localctx.which="RESET HEATERS"
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 519
                self.match(DMFParser.T__64)
                self.state = 520
                self.match(DMFParser.T__68)
                localctx.which="RESET ALL"
                pass


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
        self.enterRule(localctx, 36, self.RULE_param_type)
        self._la = 0 # Token type
        try:
            self.state = 588
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 524
                self.match(DMFParser.T__36)
                localctx.type=Type.DROP
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 526
                self.match(DMFParser.T__69)
                localctx.type=Type.PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 528
                self.match(DMFParser.T__70)
                localctx.type=Type.WELL
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 530
                self.match(DMFParser.T__70)
                self.state = 531
                self.match(DMFParser.T__69)
                localctx.type=Type.WELL_PAD
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 534
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__70:
                    self.state = 533
                    self.match(DMFParser.T__70)


                self.state = 536
                self.match(DMFParser.T__71)
                localctx.type=Type.WELL_GATE
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 538
                self.match(DMFParser.T__72)
                localctx.type=Type.INT
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 540
                self.match(DMFParser.T__73)
                localctx.type=Type.FLOAT
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 542
                self.match(DMFParser.T__21)
                localctx.type=Type.STRING
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 544
                self.match(DMFParser.T__60)
                localctx.type=Type.BINARY_STATE
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 546
                self.match(DMFParser.T__74)
                localctx.type=Type.BINARY_CPT
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 548
                self.match(DMFParser.T__75)
                localctx.type=Type.DELTA
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 550
                self.match(DMFParser.T__76)
                localctx.type=Type.MOTION
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 552
                self.match(DMFParser.T__77)
                localctx.type=Type.DELAY
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 554
                self.match(DMFParser.T__78)
                localctx.type=Type.TIME
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 556
                self.match(DMFParser.T__79)
                localctx.type=Type.TICKS
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 558
                self.match(DMFParser.T__80)
                localctx.type=Type.BOOL
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 560
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__23 or _la==DMFParser.T__24):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.type=Type.DIR
                pass

            elif la_ == 18:
                self.enterOuterAlt(localctx, 18)
                self.state = 562
                self.match(DMFParser.T__81)
                localctx.type=Type.VOLUME
                pass

            elif la_ == 19:
                self.enterOuterAlt(localctx, 19)
                self.state = 564
                self.match(DMFParser.T__27)
                localctx.type=Type.REAGENT
                pass

            elif la_ == 20:
                self.enterOuterAlt(localctx, 20)
                self.state = 566
                self.match(DMFParser.T__82)
                localctx.type=Type.LIQUID
                pass

            elif la_ == 21:
                self.enterOuterAlt(localctx, 21)
                self.state = 568
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__83 or _la==DMFParser.T__84):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 569
                _la = self._input.LA(1)
                if not(((((_la - 76)) & ~0x3f) == 0 and ((1 << (_la - 76)) & ((1 << (DMFParser.T__75 - 76)) | (1 << (DMFParser.T__85 - 76)) | (1 << (DMFParser.T__86 - 76)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.type=Type.REL_TEMP
                pass

            elif la_ == 22:
                self.enterOuterAlt(localctx, 22)
                self.state = 571
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__83 or _la==DMFParser.T__84):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 573
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,48,self._ctx)
                if la_ == 1:
                    self.state = 572
                    self.match(DMFParser.T__87)


                localctx.type=Type.ABS_TEMP
                pass

            elif la_ == 23:
                self.enterOuterAlt(localctx, 23)
                self.state = 576
                self.match(DMFParser.T__88)
                localctx.type=Type.HEATER
                pass

            elif la_ == 24:
                self.enterOuterAlt(localctx, 24)
                self.state = 578
                self.match(DMFParser.T__89)
                localctx.type=Type.MAGNET
                pass

            elif la_ == 25:
                self.enterOuterAlt(localctx, 25)
                self.state = 580
                self.match(DMFParser.T__90)
                self.state = 581
                self.match(DMFParser.T__91)
                localctx.type=Type.POWER_SUPPLY
                pass

            elif la_ == 26:
                self.enterOuterAlt(localctx, 26)
                self.state = 583
                self.match(DMFParser.T__90)
                self.state = 584
                self.match(DMFParser.T__92)
                localctx.type=Type.POWER_MODE
                pass

            elif la_ == 27:
                self.enterOuterAlt(localctx, 27)
                self.state = 586
                self.match(DMFParser.T__93)
                localctx.type=Type.FAN
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dim_unitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.unit = None


        def getRuleIndex(self):
            return DMFParser.RULE_dim_unit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDim_unit" ):
                listener.enterDim_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDim_unit" ):
                listener.exitDim_unit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDim_unit" ):
                return visitor.visitDim_unit(self)
            else:
                return visitor.visitChildren(self)




    def dim_unit(self):

        localctx = DMFParser.Dim_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_dim_unit)
        self._la = 0 # Token type
        try:
            self.state = 604
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__94, DMFParser.T__95, DMFParser.T__96, DMFParser.T__97, DMFParser.T__98]:
                self.enterOuterAlt(localctx, 1)
                self.state = 590
                _la = self._input.LA(1)
                if not(((((_la - 95)) & ~0x3f) == 0 and ((1 << (_la - 95)) & ((1 << (DMFParser.T__94 - 95)) | (1 << (DMFParser.T__95 - 95)) | (1 << (DMFParser.T__96 - 95)) | (1 << (DMFParser.T__97 - 95)) | (1 << (DMFParser.T__98 - 95)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.sec
                pass
            elif token in [DMFParser.T__99, DMFParser.T__100, DMFParser.T__101]:
                self.enterOuterAlt(localctx, 2)
                self.state = 592
                _la = self._input.LA(1)
                if not(((((_la - 100)) & ~0x3f) == 0 and ((1 << (_la - 100)) & ((1 << (DMFParser.T__99 - 100)) | (1 << (DMFParser.T__100 - 100)) | (1 << (DMFParser.T__101 - 100)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.ms
                pass
            elif token in [DMFParser.T__102, DMFParser.T__103, DMFParser.T__104, DMFParser.T__105, DMFParser.T__106, DMFParser.T__107]:
                self.enterOuterAlt(localctx, 3)
                self.state = 594
                _la = self._input.LA(1)
                if not(((((_la - 103)) & ~0x3f) == 0 and ((1 << (_la - 103)) & ((1 << (DMFParser.T__102 - 103)) | (1 << (DMFParser.T__103 - 103)) | (1 << (DMFParser.T__104 - 103)) | (1 << (DMFParser.T__105 - 103)) | (1 << (DMFParser.T__106 - 103)) | (1 << (DMFParser.T__107 - 103)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.uL
                pass
            elif token in [DMFParser.T__108, DMFParser.T__109, DMFParser.T__110, DMFParser.T__111, DMFParser.T__112, DMFParser.T__113]:
                self.enterOuterAlt(localctx, 4)
                self.state = 596
                _la = self._input.LA(1)
                if not(((((_la - 109)) & ~0x3f) == 0 and ((1 << (_la - 109)) & ((1 << (DMFParser.T__108 - 109)) | (1 << (DMFParser.T__109 - 109)) | (1 << (DMFParser.T__110 - 109)) | (1 << (DMFParser.T__111 - 109)) | (1 << (DMFParser.T__112 - 109)) | (1 << (DMFParser.T__113 - 109)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.mL
                pass
            elif token in [DMFParser.T__79, DMFParser.T__114]:
                self.enterOuterAlt(localctx, 5)
                self.state = 598
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__79 or _la==DMFParser.T__114):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=ticks
                pass
            elif token in [DMFParser.T__36, DMFParser.T__115]:
                self.enterOuterAlt(localctx, 6)
                self.state = 600
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__36 or _la==DMFParser.T__115):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=EnvRelativeUnit.DROP
                pass
            elif token in [DMFParser.T__116, DMFParser.T__117, DMFParser.T__118]:
                self.enterOuterAlt(localctx, 7)
                self.state = 602
                _la = self._input.LA(1)
                if not(((((_la - 117)) & ~0x3f) == 0 and ((1 << (_la - 117)) & ((1 << (DMFParser.T__116 - 117)) | (1 << (DMFParser.T__117 - 117)) | (1 << (DMFParser.T__118 - 117)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.volts
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


    class Numbered_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.kind = None


        def getRuleIndex(self):
            return DMFParser.RULE_numbered_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumbered_type" ):
                listener.enterNumbered_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumbered_type" ):
                listener.exitNumbered_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumbered_type" ):
                return visitor.visitNumbered_type(self)
            else:
                return visitor.visitChildren(self)




    def numbered_type(self):

        localctx = DMFParser.Numbered_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_numbered_type)
        try:
            self.state = 612
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__70]:
                self.enterOuterAlt(localctx, 1)
                self.state = 606
                self.match(DMFParser.T__70)
                localctx.kind=NumberedItem.WELL
                pass
            elif token in [DMFParser.T__88]:
                self.enterOuterAlt(localctx, 2)
                self.state = 608
                self.match(DMFParser.T__88)
                localctx.kind=NumberedItem.HEATER
                pass
            elif token in [DMFParser.T__89]:
                self.enterOuterAlt(localctx, 3)
                self.state = 610
                self.match(DMFParser.T__89)
                localctx.kind=NumberedItem.MAGNET
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


    class AttrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.which = None
            self.n = None # Token

        def ID(self):
            return self.getToken(DMFParser.ID, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_attr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr" ):
                listener.enterAttr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr" ):
                listener.exitAttr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr" ):
                return visitor.visitAttr(self)
            else:
                return visitor.visitChildren(self)




    def attr(self):

        localctx = DMFParser.AttrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_attr)
        self._la = 0 # Token type
        try:
            self.state = 661
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,56,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 614
                self.match(DMFParser.T__119)
                self.state = 615
                self.match(DMFParser.T__69)
                localctx.which="#exit_pad"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 617
                self.match(DMFParser.T__71)
                localctx.which="gate"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 619
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__23 or _la==DMFParser.T__24):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="direction"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 624
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__52]:
                    self.state = 621
                    self.match(DMFParser.T__52)
                    pass
                elif token in [DMFParser.T__120]:
                    self.state = 622
                    self.match(DMFParser.T__120)
                    self.state = 623
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__121 or _la==DMFParser.T__122):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    pass
                else:
                    raise NoViableAltException(self)

                localctx.which="row"
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 631
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__54]:
                    self.state = 627
                    self.match(DMFParser.T__54)
                    pass
                elif token in [DMFParser.T__55]:
                    self.state = 628
                    self.match(DMFParser.T__55)
                    pass
                elif token in [DMFParser.T__123]:
                    self.state = 629
                    self.match(DMFParser.T__123)
                    self.state = 630
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__121 or _la==DMFParser.T__122):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    pass
                else:
                    raise NoViableAltException(self)

                localctx.which="column"
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 634
                self.match(DMFParser.T__119)
                self.state = 635
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__23 or _la==DMFParser.T__24):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#exit_dir"
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 637
                self.match(DMFParser.T__124)
                self.state = 638
                self.match(DMFParser.T__125)
                localctx.which="#remaining_capacity"
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 640
                self.match(DMFParser.T__126)
                self.state = 642
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
                if la_ == 1:
                    self.state = 641
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__83 or _la==DMFParser.T__84):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                localctx.which="#target_temperature"
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 646
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__127:
                    self.state = 645
                    self.match(DMFParser.T__127)


                self.state = 648
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__83 or _la==DMFParser.T__84):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#current_temperature"
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 650
                self.match(DMFParser.T__90)
                self.state = 651
                self.match(DMFParser.T__91)
                localctx.which="#power_supply"
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 653
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__128 or _la==DMFParser.T__129):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 654
                self.match(DMFParser.T__130)
                localctx.which="#min_voltage"
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 656
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__131 or _la==DMFParser.T__132):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 657
                self.match(DMFParser.T__130)
                localctx.which="#max_voltage"
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 659
                localctx.n = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__27) | (1 << DMFParser.T__36) | (1 << DMFParser.T__60))) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DMFParser.T__69 - 70)) | (1 << (DMFParser.T__70 - 70)) | (1 << (DMFParser.T__81 - 70)) | (1 << (DMFParser.T__88 - 70)) | (1 << (DMFParser.T__89 - 70)) | (1 << (DMFParser.T__93 - 70)))) != 0) or _la==DMFParser.ID):
                    localctx.n = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which=(None if localctx.n is None else localctx.n.text)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.which = None


        def getRuleIndex(self):
            return DMFParser.RULE_rel

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRel" ):
                listener.enterRel(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRel" ):
                listener.exitRel(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRel" ):
                return visitor.visitRel(self)
            else:
                return visitor.visitChildren(self)




    def rel(self):

        localctx = DMFParser.RelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_rel)
        try:
            self.state = 675
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__133]:
                self.enterOuterAlt(localctx, 1)
                self.state = 663
                self.match(DMFParser.T__133)
                localctx.which=Rel.EQ
                pass
            elif token in [DMFParser.T__134]:
                self.enterOuterAlt(localctx, 2)
                self.state = 665
                self.match(DMFParser.T__134)
                localctx.which=Rel.NE
                pass
            elif token in [DMFParser.T__135]:
                self.enterOuterAlt(localctx, 3)
                self.state = 667
                self.match(DMFParser.T__135)
                localctx.which=Rel.LT
                pass
            elif token in [DMFParser.T__136]:
                self.enterOuterAlt(localctx, 4)
                self.state = 669
                self.match(DMFParser.T__136)
                localctx.which=Rel.LE
                pass
            elif token in [DMFParser.T__137]:
                self.enterOuterAlt(localctx, 5)
                self.state = 671
                self.match(DMFParser.T__137)
                localctx.which=Rel.GT
                pass
            elif token in [DMFParser.T__138]:
                self.enterOuterAlt(localctx, 6)
                self.state = 673
                self.match(DMFParser.T__138)
                localctx.which=Rel.GE
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


    class Assign_opContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.modifier = None

        def ASSIGN(self):
            return self.getToken(DMFParser.ASSIGN, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_assign_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssign_op" ):
                listener.enterAssign_op(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssign_op" ):
                listener.exitAssign_op(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssign_op" ):
                return visitor.visitAssign_op(self)
            else:
                return visitor.visitChildren(self)




    def assign_op(self):

        localctx = DMFParser.Assign_opContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_assign_op)
        try:
            self.state = 687
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.ASSIGN]:
                self.enterOuterAlt(localctx, 1)
                self.state = 677
                self.match(DMFParser.ASSIGN)
                localctx.modifier=None
                pass
            elif token in [DMFParser.T__139]:
                self.enterOuterAlt(localctx, 2)
                self.state = 679
                self.match(DMFParser.T__139)
                localctx.modifier="ADD"
                pass
            elif token in [DMFParser.T__140]:
                self.enterOuterAlt(localctx, 3)
                self.state = 681
                self.match(DMFParser.T__140)
                localctx.modifier="SUBTRACT"
                pass
            elif token in [DMFParser.T__141]:
                self.enterOuterAlt(localctx, 4)
                self.state = 683
                self.match(DMFParser.T__141)
                localctx.modifier="MULTIPLY"
                pass
            elif token in [DMFParser.T__142]:
                self.enterOuterAlt(localctx, 5)
                self.state = 685
                self.match(DMFParser.T__142)
                localctx.modifier="DIVIDE"
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


    class Bool_valContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.val = None


        def getRuleIndex(self):
            return DMFParser.RULE_bool_val

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBool_val" ):
                listener.enterBool_val(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBool_val" ):
                listener.exitBool_val(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBool_val" ):
                return visitor.visitBool_val(self)
            else:
                return visitor.visitChildren(self)




    def bool_val(self):

        localctx = DMFParser.Bool_valContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_bool_val)
        self._la = 0 # Token type
        try:
            self.state = 693
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__143, DMFParser.T__144, DMFParser.T__145, DMFParser.T__146, DMFParser.T__147, DMFParser.T__148]:
                self.enterOuterAlt(localctx, 1)
                self.state = 689
                _la = self._input.LA(1)
                if not(((((_la - 144)) & ~0x3f) == 0 and ((1 << (_la - 144)) & ((1 << (DMFParser.T__143 - 144)) | (1 << (DMFParser.T__144 - 144)) | (1 << (DMFParser.T__145 - 144)) | (1 << (DMFParser.T__146 - 144)) | (1 << (DMFParser.T__147 - 144)) | (1 << (DMFParser.T__148 - 144)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.val=True
                pass
            elif token in [DMFParser.T__149, DMFParser.T__150, DMFParser.T__151, DMFParser.T__152, DMFParser.T__153, DMFParser.T__154]:
                self.enterOuterAlt(localctx, 2)
                self.state = 691
                _la = self._input.LA(1)
                if not(((((_la - 150)) & ~0x3f) == 0 and ((1 << (_la - 150)) & ((1 << (DMFParser.T__149 - 150)) | (1 << (DMFParser.T__150 - 150)) | (1 << (DMFParser.T__151 - 150)) | (1 << (DMFParser.T__152 - 150)) | (1 << (DMFParser.T__153 - 150)) | (1 << (DMFParser.T__154 - 150)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.val=False
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
            self.val = None
            self._multi_word_name = None # Multi_word_nameContext
            self._ID = None # Token
            self._kwd_names = None # Kwd_namesContext

        def multi_word_name(self):
            return self.getTypedRuleContext(DMFParser.Multi_word_nameContext,0)


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
        self.enterRule(localctx, 50, self.RULE_name)
        try:
            self.state = 703
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,60,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 695
                localctx._multi_word_name = self.multi_word_name()
                localctx.val=localctx._multi_word_name.val
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 698
                localctx._ID = self.match(DMFParser.ID)
                localctx.val=(None if localctx._ID is None else localctx._ID.text)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 700
                localctx._kwd_names = self.kwd_names()
                localctx.val=(None if localctx._kwd_names is None else self._input.getText(localctx._kwd_names.start,localctx._kwd_names.stop))
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Multi_word_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.val = None

        def ON(self):
            return self.getToken(DMFParser.ON, 0)

        def INTERACTIVE(self):
            return self.getToken(DMFParser.INTERACTIVE, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_multi_word_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMulti_word_name" ):
                listener.enterMulti_word_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMulti_word_name" ):
                listener.exitMulti_word_name(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulti_word_name" ):
                return visitor.visitMulti_word_name(self)
            else:
                return visitor.visitChildren(self)




    def multi_word_name(self):

        localctx = DMFParser.Multi_word_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_multi_word_name)
        self._la = 0 # Token type
        try:
            self.state = 738
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,65,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 705
                self.match(DMFParser.ON)
                self.state = 707
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__26:
                    self.state = 706
                    self.match(DMFParser.T__26)


                self.state = 709
                self.match(DMFParser.T__63)
                localctx.val="on board"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 712
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__26:
                    self.state = 711
                    self.match(DMFParser.T__26)


                self.state = 714
                self.match(DMFParser.INTERACTIVE)
                self.state = 715
                self.match(DMFParser.T__27)
                localctx.val="interactive reagent"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 718
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__26:
                    self.state = 717
                    self.match(DMFParser.T__26)


                self.state = 720
                self.match(DMFParser.INTERACTIVE)
                self.state = 721
                self.match(DMFParser.T__81)
                localctx.val="interactive volume"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 723
                self.match(DMFParser.T__26)
                self.state = 724
                self.match(DMFParser.T__63)
                localctx.val="the board"
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 727
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__26:
                    self.state = 726
                    self.match(DMFParser.T__26)


                self.state = 729
                self.match(DMFParser.T__155)
                self.state = 730
                self.match(DMFParser.T__156)
                localctx.val="index base"
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 732
                self.match(DMFParser.T__157)
                self.state = 733
                self.match(DMFParser.T__36)
                localctx.val="dispense drop"
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 735
                self.match(DMFParser.T__158)
                self.state = 736
                self.match(DMFParser.T__70)
                localctx.val="enter well"
                pass


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

        def ON(self):
            return self.getToken(DMFParser.ON, 0)

        def OFF(self):
            return self.getToken(DMFParser.OFF, 0)

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
        self.enterRule(localctx, 54, self.RULE_kwd_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 740
            _la = self._input.LA(1)
            if not(((((_la - 65)) & ~0x3f) == 0 and ((1 << (_la - 65)) & ((1 << (DMFParser.T__64 - 65)) | (1 << (DMFParser.T__65 - 65)) | (1 << (DMFParser.T__66 - 65)) | (1 << (DMFParser.T__67 - 65)) | (1 << (DMFParser.T__68 - 65)) | (1 << (DMFParser.T__75 - 65)) | (1 << (DMFParser.T__85 - 65)) | (1 << (DMFParser.T__86 - 65)) | (1 << (DMFParser.T__87 - 65)) | (1 << (DMFParser.T__94 - 65)) | (1 << (DMFParser.T__99 - 65)) | (1 << (DMFParser.T__120 - 65)) | (1 << (DMFParser.T__123 - 65)))) != 0) or ((((_la - 129)) & ~0x3f) == 0 and ((1 << (_la - 129)) & ((1 << (DMFParser.T__128 - 129)) | (1 << (DMFParser.T__129 - 129)) | (1 << (DMFParser.T__131 - 129)) | (1 << (DMFParser.T__132 - 129)) | (1 << (DMFParser.T__155 - 129)) | (1 << (DMFParser.T__156 - 129)) | (1 << (DMFParser.T__157 - 129)) | (1 << (DMFParser.T__158 - 129)) | (1 << (DMFParser.OFF - 129)) | (1 << (DMFParser.ON - 129)))) != 0)):
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


    class StringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(DMFParser.STRING, 0)

        def getRuleIndex(self):
            return DMFParser.RULE_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)




    def string(self):

        localctx = DMFParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 742
            self.match(DMFParser.STRING)
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
        self._predicates[8] = self.expr_sempred
        self._predicates[12] = self.rc_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 38)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 31)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 30)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 29)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 28)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 26)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 24)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 23)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 16)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 11:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 12:
                return self.precpred(self._ctx, 47)
         

            if predIndex == 13:
                return self.precpred(self._ctx, 44)
         

            if predIndex == 14:
                return self.precpred(self._ctx, 42)
         

            if predIndex == 15:
                return self.precpred(self._ctx, 41)
         

            if predIndex == 16:
                return self.precpred(self._ctx, 40)
         

            if predIndex == 17:
                return self.precpred(self._ctx, 39)
         

            if predIndex == 18:
                return self.precpred(self._ctx, 36)
         

            if predIndex == 19:
                return self.precpred(self._ctx, 35)
         

            if predIndex == 20:
                return self.precpred(self._ctx, 34)
         

            if predIndex == 21:
                return self.precpred(self._ctx, 27)
         

            if predIndex == 22:
                return self.precpred(self._ctx, 18)
         

    def rc_sempred(self, localctx:RcContext, predIndex:int):
            if predIndex == 23:
                return localctx.n==1
         

            if predIndex == 24:
                return localctx.n==1
         




