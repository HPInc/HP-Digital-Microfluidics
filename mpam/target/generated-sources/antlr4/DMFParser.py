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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\u009e")
        buf.write("\u02aa\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\3\2\7\2")
        buf.write("<\n\2\f\2\16\2?\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\5\3H")
        buf.write("\n\3\3\3\3\3\3\3\3\3\5\3N\n\3\3\3\3\3\3\3\3\3\5\3T\n\3")
        buf.write("\3\3\3\3\3\3\5\3Y\n\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\5\4c\n\4\3\4\3\4\3\4\3\4\5\4i\n\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\4\5\4u\n\4\3\4\3\4\3\4\3\4\5\4{\n\4")
        buf.write("\3\4\3\4\3\4\5\4\u0080\n\4\3\5\3\5\3\5\3\5\7\5\u0086\n")
        buf.write("\5\f\5\16\5\u0089\13\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6\u009d\n\6")
        buf.write("\f\6\16\6\u00a0\13\6\3\6\3\6\5\6\u00a4\n\6\3\6\3\6\3\6")
        buf.write("\3\6\3\6\5\6\u00ab\n\6\3\7\3\7\7\7\u00af\n\7\f\7\16\7")
        buf.write("\u00b2\13\7\3\7\3\7\3\7\7\7\u00b7\n\7\f\7\16\7\u00ba\13")
        buf.write("\7\3\7\5\7\u00bd\n\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3")
        buf.write("\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\b\u00d1\n\b\3")
        buf.write("\t\3\t\3\t\3\t\5\t\u00d7\n\t\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\5\n\u00ed\n\n\3\n\3\n\5\n\u00f1\n\n\3\n\5\n\u00f4\n\n")
        buf.write("\3\n\3\n\5\n\u00f8\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\5\n\u0103\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\5\n\u010e\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u0123\n\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\5\n\u0139\n\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\7\n\u0159")
        buf.write("\n\n\f\n\16\n\u015c\13\n\5\n\u015e\n\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u016b\n\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\7\n\u0185\n\n\f\n\16\n")
        buf.write("\u0188\13\n\3\13\3\13\3\13\3\13\5\13\u018e\n\13\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f\u019c\n")
        buf.write("\f\3\r\3\r\3\r\3\r\3\r\3\r\5\r\u01a4\n\r\3\16\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16")
        buf.write("\5\16\u01b4\n\16\3\17\3\17\3\17\3\17\5\17\u01ba\n\17\3")
        buf.write("\20\3\20\3\20\5\20\u01bf\n\20\3\21\3\21\3\21\3\21\3\21")
        buf.write("\7\21\u01c6\n\21\f\21\16\21\u01c9\13\21\5\21\u01cb\n\21")
        buf.write("\3\21\3\21\3\22\5\22\u01d0\n\22\3\22\3\22\3\22\3\22\3")
        buf.write("\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22")
        buf.write("\3\22\3\22\3\22\3\22\3\22\5\22\u01e6\n\22\3\23\5\23\u01e9")
        buf.write("\n\23\3\23\3\23\3\23\5\23\u01ee\n\23\3\23\3\23\3\23\3")
        buf.write("\23\5\23\u01f4\n\23\3\23\3\23\3\23\3\23\5\23\u01fa\n\23")
        buf.write("\3\23\5\23\u01fd\n\23\3\23\5\23\u0200\n\23\3\24\3\24\3")
        buf.write("\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\5\24\u020c\n\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\5\24\u0233\n\24\3\24\3\24\3\24\3")
        buf.write("\24\3\24\5\24\u023a\n\24\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u0248\n\25\3\26\3")
        buf.write("\26\3\26\3\26\3\26\3\26\5\26\u0250\n\26\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\3\27\5\27\u025c\n\27\3")
        buf.write("\27\3\27\3\27\3\27\3\27\5\27\u0263\n\27\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\5\27\u026e\n\27\3\27\3")
        buf.write("\27\5\27\u0272\n\27\3\27\3\27\3\27\3\27\5\27\u0278\n\27")
        buf.write("\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30")
        buf.write("\3\30\5\30\u0286\n\30\3\31\3\31\3\31\3\31\5\31\u028c\n")
        buf.write("\31\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\5\32\u0296")
        buf.write("\n\32\3\33\3\33\5\33\u029a\n\33\3\33\3\33\3\33\3\33\3")
        buf.write("\33\3\33\3\33\3\33\5\33\u02a4\n\33\3\34\3\34\3\35\3\35")
        buf.write("\3\35\2\3\22\36\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36")
        buf.write(" \"$&(*,.\60\62\64\668\2\35\4\2\26\26\34\34\3\2\'(\3\2")
        buf.write("\31\32\4\2\u008b\u008b\u008f\u008f\4\2\u0088\u0088\u0093")
        buf.write("\u0093\4\2\26\26!!\3\2+,\3\2-.\3\2/\60\3\2\61\62\4\2\61")
        buf.write("\61\63\63\4\2//\64\64\3\289\3\2:;\3\2PQ\4\2HHRS\3\2W[")
        buf.write("\3\2\\^\3\2_d\3\2ej\4\2LLkk\4\2&&ll\3\2op\b\2\35\35&&")
        buf.write("BCNNUV\u0098\u0098\3\2|\u0081\3\2\u0082\u0087\b\2HHRT")
        buf.write("WW\\\\nnqq\2\u0335\2=\3\2\2\2\4X\3\2\2\2\6\177\3\2\2\2")
        buf.write("\b\u0081\3\2\2\2\n\u00aa\3\2\2\2\f\u00bc\3\2\2\2\16\u00d0")
        buf.write("\3\2\2\2\20\u00d6\3\2\2\2\22\u0122\3\2\2\2\24\u018d\3")
        buf.write("\2\2\2\26\u019b\3\2\2\2\30\u01a3\3\2\2\2\32\u01b3\3\2")
        buf.write("\2\2\34\u01b9\3\2\2\2\36\u01bb\3\2\2\2 \u01c0\3\2\2\2")
        buf.write("\"\u01e5\3\2\2\2$\u01ff\3\2\2\2&\u0239\3\2\2\2(\u0247")
        buf.write("\3\2\2\2*\u024f\3\2\2\2,\u0277\3\2\2\2.\u0285\3\2\2\2")
        buf.write("\60\u028b\3\2\2\2\62\u0295\3\2\2\2\64\u02a3\3\2\2\2\66")
        buf.write("\u02a5\3\2\2\28\u02a7\3\2\2\2:<\5\n\6\2;:\3\2\2\2<?\3")
        buf.write("\2\2\2=;\3\2\2\2=>\3\2\2\2>@\3\2\2\2?=\3\2\2\2@A\7\2\2")
        buf.write("\3A\3\3\2\2\2BC\5\f\7\2CD\7\2\2\3DY\3\2\2\2EG\5\6\4\2")
        buf.write("FH\7\u0094\2\2GF\3\2\2\2GH\3\2\2\2HI\3\2\2\2IJ\7\2\2\3")
        buf.write("JY\3\2\2\2KM\5\b\5\2LN\7\u0094\2\2ML\3\2\2\2MN\3\2\2\2")
        buf.write("NO\3\2\2\2OP\7\2\2\3PY\3\2\2\2QS\5\22\n\2RT\7\u0094\2")
        buf.write("\2SR\3\2\2\2ST\3\2\2\2TU\3\2\2\2UV\7\2\2\3VY\3\2\2\2W")
        buf.write("Y\7\2\2\3XB\3\2\2\2XE\3\2\2\2XK\3\2\2\2XQ\3\2\2\2XW\3")
        buf.write("\2\2\2Y\5\3\2\2\2Z[\7\u008e\2\2[\\\5\62\32\2\\]\7\u0089")
        buf.write("\2\2]^\5\22\n\2^_\b\4\1\2_`\b\4\1\2`\u0080\3\2\2\2ac\7")
        buf.write("\u008e\2\2ba\3\2\2\2bc\3\2\2\2cd\3\2\2\2de\5&\24\2ef\7")
        buf.write("\u0099\2\2fh\7\u0089\2\2gi\5\22\n\2hg\3\2\2\2hi\3\2\2")
        buf.write("\2ij\3\2\2\2jk\b\4\1\2kl\b\4\1\2l\u0080\3\2\2\2mn\7\u008e")
        buf.write("\2\2no\5&\24\2op\7\u0099\2\2pq\b\4\1\2qr\b\4\1\2r\u0080")
        buf.write("\3\2\2\2su\7\u008e\2\2ts\3\2\2\2tu\3\2\2\2uv\3\2\2\2v")
        buf.write("w\5&\24\2wz\5\62\32\2xy\7\u0089\2\2y{\5\22\n\2zx\3\2\2")
        buf.write("\2z{\3\2\2\2{|\3\2\2\2|}\b\4\1\2}~\b\4\1\2~\u0080\3\2")
        buf.write("\2\2\177Z\3\2\2\2\177b\3\2\2\2\177m\3\2\2\2\177t\3\2\2")
        buf.write("\2\u0080\7\3\2\2\2\u0081\u0082\7\3\2\2\u0082\u0087\5\22")
        buf.write("\n\2\u0083\u0084\7\4\2\2\u0084\u0086\5\22\n\2\u0085\u0083")
        buf.write("\3\2\2\2\u0086\u0089\3\2\2\2\u0087\u0085\3\2\2\2\u0087")
        buf.write("\u0088\3\2\2\2\u0088\t\3\2\2\2\u0089\u0087\3\2\2\2\u008a")
        buf.write("\u008b\5\6\4\2\u008b\u008c\7\u0094\2\2\u008c\u00ab\3\2")
        buf.write("\2\2\u008d\u008e\7\5\2\2\u008e\u008f\5\22\n\2\u008f\u0090")
        buf.write("\7\u0094\2\2\u0090\u00ab\3\2\2\2\u0091\u0092\5\b\5\2\u0092")
        buf.write("\u0093\7\u0094\2\2\u0093\u00ab\3\2\2\2\u0094\u0095\7\6")
        buf.write("\2\2\u0095\u0096\5\22\n\2\u0096\u009e\5\f\7\2\u0097\u0098")
        buf.write("\7\7\2\2\u0098\u0099\7\6\2\2\u0099\u009a\5\22\n\2\u009a")
        buf.write("\u009b\5\f\7\2\u009b\u009d\3\2\2\2\u009c\u0097\3\2\2\2")
        buf.write("\u009d\u00a0\3\2\2\2\u009e\u009c\3\2\2\2\u009e\u009f\3")
        buf.write("\2\2\2\u009f\u00a3\3\2\2\2\u00a0\u009e\3\2\2\2\u00a1\u00a2")
        buf.write("\7\7\2\2\u00a2\u00a4\5\f\7\2\u00a3\u00a1\3\2\2\2\u00a3")
        buf.write("\u00a4\3\2\2\2\u00a4\u00ab\3\2\2\2\u00a5\u00a6\5\22\n")
        buf.write("\2\u00a6\u00a7\7\u0094\2\2\u00a7\u00ab\3\2\2\2\u00a8\u00ab")
        buf.write("\5\16\b\2\u00a9\u00ab\5\f\7\2\u00aa\u008a\3\2\2\2\u00aa")
        buf.write("\u008d\3\2\2\2\u00aa\u0091\3\2\2\2\u00aa\u0094\3\2\2\2")
        buf.write("\u00aa\u00a5\3\2\2\2\u00aa\u00a8\3\2\2\2\u00aa\u00a9\3")
        buf.write("\2\2\2\u00ab\13\3\2\2\2\u00ac\u00b0\7\b\2\2\u00ad\u00af")
        buf.write("\5\n\6\2\u00ae\u00ad\3\2\2\2\u00af\u00b2\3\2\2\2\u00b0")
        buf.write("\u00ae\3\2\2\2\u00b0\u00b1\3\2\2\2\u00b1\u00b3\3\2\2\2")
        buf.write("\u00b2\u00b0\3\2\2\2\u00b3\u00bd\7\t\2\2\u00b4\u00b8\7")
        buf.write("\n\2\2\u00b5\u00b7\5\n\6\2\u00b6\u00b5\3\2\2\2\u00b7\u00ba")
        buf.write("\3\2\2\2\u00b8\u00b6\3\2\2\2\u00b8\u00b9\3\2\2\2\u00b9")
        buf.write("\u00bb\3\2\2\2\u00ba\u00b8\3\2\2\2\u00bb\u00bd\7\13\2")
        buf.write("\2\u00bc\u00ac\3\2\2\2\u00bc\u00b4\3\2\2\2\u00bd\r\3\2")
        buf.write("\2\2\u00be\u00bf\7\f\2\2\u00bf\u00c0\5\22\n\2\u00c0\u00c1")
        buf.write("\7\r\2\2\u00c1\u00c2\5\n\6\2\u00c2\u00d1\3\2\2\2\u00c3")
        buf.write("\u00c4\7\16\2\2\u00c4\u00c5\5\62\32\2\u00c5\u00c6\7\17")
        buf.write("\2\2\u00c6\u00c7\7\20\2\2\u00c7\u00c8\5\22\n\2\u00c8\u00c9")
        buf.write("\7\4\2\2\u00c9\u00ca\5\22\n\2\u00ca\u00cb\5\20\t\2\u00cb")
        buf.write("\u00cc\7\21\2\2\u00cc\u00cd\5\22\n\2\u00cd\u00ce\3\2\2")
        buf.write("\2\u00ce\u00cf\5\n\6\2\u00cf\u00d1\3\2\2\2\u00d0\u00be")
        buf.write("\3\2\2\2\u00d0\u00c3\3\2\2\2\u00d1\17\3\2\2\2\u00d2\u00d3")
        buf.write("\7\u0096\2\2\u00d3\u00d7\b\t\1\2\u00d4\u00d5\7\u0097\2")
        buf.write("\2\u00d5\u00d7\b\t\1\2\u00d6\u00d2\3\2\2\2\u00d6\u00d4")
        buf.write("\3\2\2\2\u00d7\21\3\2\2\2\u00d8\u00d9\b\n\1\2\u00d9\u00da")
        buf.write("\7\22\2\2\u00da\u00db\5\22\n\2\u00db\u00dc\7\u0097\2\2")
        buf.write("\u00dc\u0123\3\2\2\2\u00dd\u00de\7\22\2\2\u00de\u00df")
        buf.write("\5\22\n\2\u00df\u00e0\7\4\2\2\u00e0\u00e1\5\22\n\2\u00e1")
        buf.write("\u00e2\7\u0097\2\2\u00e2\u0123\3\2\2\2\u00e3\u00e4\7\u0093")
        buf.write("\2\2\u00e4\u0123\5\22\n/\u00e5\u00e6\5*\26\2\u00e6\u00e7")
        buf.write("\7\23\2\2\u00e7\u00e8\5\22\n-\u00e8\u0123\3\2\2\2\u00e9")
        buf.write("\u00ea\7\u0099\2\2\u00ea\u0123\5\32\16\2\u00eb\u00ed\7")
        buf.write("\34\2\2\u00ec\u00eb\3\2\2\2\u00ec\u00ed\3\2\2\2\u00ed")
        buf.write("\u00ee\3\2\2\2\u00ee\u00f0\5\24\13\2\u00ef\u00f1\7\35")
        buf.write("\2\2\u00f0\u00ef\3\2\2\2\u00f0\u00f1\3\2\2\2\u00f1\u0123")
        buf.write("\3\2\2\2\u00f2\u00f4\t\2\2\2\u00f3\u00f2\3\2\2\2\u00f3")
        buf.write("\u00f4\3\2\2\2\u00f4\u00f5\3\2\2\2\u00f5\u00f7\7\35\2")
        buf.write("\2\u00f6\u00f8\7\36\2\2\u00f7\u00f6\3\2\2\2\u00f7\u00f8")
        buf.write("\3\2\2\2\u00f8\u00f9\3\2\2\2\u00f9\u0123\5\22\n\"\u00fa")
        buf.write("\u00fb\7\u0090\2\2\u00fb\u0123\5\22\n\33\u00fc\u00fd\5")
        buf.write("\26\f\2\u00fd\u00fe\5\22\n\30\u00fe\u0123\3\2\2\2\u00ff")
        buf.write("\u0123\5\26\f\2\u0100\u0102\7%\2\2\u0101\u0103\5\34\17")
        buf.write("\2\u0102\u0101\3\2\2\2\u0102\u0103\3\2\2\2\u0103\u0104")
        buf.write("\3\2\2\2\u0104\u0123\5\22\n\26\u0105\u0106\7\5\2\2\u0106")
        buf.write("\u0123\5\22\n\25\u0107\u0108\7&\2\2\u0108\u0109\t\3\2")
        buf.write("\2\u0109\u0123\5\22\n\23\u010a\u0123\5\36\20\2\u010b\u0123")
        buf.write("\5$\23\2\u010c\u010e\7\34\2\2\u010d\u010c\3\2\2\2\u010d")
        buf.write("\u010e\3\2\2\2\u010e\u010f\3\2\2\2\u010f\u0123\5&\24\2")
        buf.write("\u0110\u0111\5&\24\2\u0111\u0112\7\u0099\2\2\u0112\u0123")
        buf.write("\3\2\2\2\u0113\u0123\5\60\31\2\u0114\u0123\5\62\32\2\u0115")
        buf.write("\u0123\5\64\33\2\u0116\u0117\5\62\32\2\u0117\u0118\7\u0089")
        buf.write("\2\2\u0118\u0119\5\22\n\b\u0119\u0123\3\2\2\2\u011a\u011b")
        buf.write("\5&\24\2\u011b\u011c\7\u0099\2\2\u011c\u011d\7\u0089\2")
        buf.write("\2\u011d\u011e\5\22\n\6\u011e\u0123\3\2\2\2\u011f\u0123")
        buf.write("\58\35\2\u0120\u0123\7\u0099\2\2\u0121\u0123\7\u009a\2")
        buf.write("\2\u0122\u00d8\3\2\2\2\u0122\u00dd\3\2\2\2\u0122\u00e3")
        buf.write("\3\2\2\2\u0122\u00e5\3\2\2\2\u0122\u00e9\3\2\2\2\u0122")
        buf.write("\u00ec\3\2\2\2\u0122\u00f3\3\2\2\2\u0122\u00fa\3\2\2\2")
        buf.write("\u0122\u00fc\3\2\2\2\u0122\u00ff\3\2\2\2\u0122\u0100\3")
        buf.write("\2\2\2\u0122\u0105\3\2\2\2\u0122\u0107\3\2\2\2\u0122\u010a")
        buf.write("\3\2\2\2\u0122\u010b\3\2\2\2\u0122\u010d\3\2\2\2\u0122")
        buf.write("\u0110\3\2\2\2\u0122\u0113\3\2\2\2\u0122\u0114\3\2\2\2")
        buf.write("\u0122\u0115\3\2\2\2\u0122\u0116\3\2\2\2\u0122\u011a\3")
        buf.write("\2\2\2\u0122\u011f\3\2\2\2\u0122\u0120\3\2\2\2\u0122\u0121")
        buf.write("\3\2\2\2\u0123\u0186\3\2\2\2\u0124\u0125\f(\2\2\u0125")
        buf.write("\u0126\7\17\2\2\u0126\u0127\t\4\2\2\u0127\u0185\5\22\n")
        buf.write(")\u0128\u0129\f!\2\2\u0129\u012a\7\37\2\2\u012a\u0185")
        buf.write("\5\22\n\"\u012b\u012c\f \2\2\u012c\u012d\t\5\2\2\u012d")
        buf.write("\u0185\5\22\n!\u012e\u012f\f\37\2\2\u012f\u0130\t\6\2")
        buf.write("\2\u0130\u0185\5\22\n \u0131\u0132\f\36\2\2\u0132\u0133")
        buf.write("\5.\30\2\u0133\u0134\5\22\n\37\u0134\u0185\3\2\2\2\u0135")
        buf.write("\u0136\f\34\2\2\u0136\u0138\7\"\2\2\u0137\u0139\7\u0090")
        buf.write("\2\2\u0138\u0137\3\2\2\2\u0138\u0139\3\2\2\2\u0139\u013a")
        buf.write("\3\2\2\2\u013a\u0185\5\22\n\35\u013b\u013c\f\32\2\2\u013c")
        buf.write("\u013d\7#\2\2\u013d\u0185\5\22\n\33\u013e\u013f\f\31\2")
        buf.write("\2\u013f\u0140\7$\2\2\u0140\u0185\5\22\n\32\u0141\u0142")
        buf.write("\f\22\2\2\u0142\u0143\t\3\2\2\u0143\u0185\5\22\n\23\u0144")
        buf.write("\u0145\f\21\2\2\u0145\u0146\7\u008d\2\2\u0146\u0185\5")
        buf.write("\22\n\22\u0147\u0148\f\20\2\2\u0148\u0149\7\6\2\2\u0149")
        buf.write("\u014a\5\22\n\2\u014a\u014b\7\7\2\2\u014b\u014c\5\22\n")
        buf.write("\21\u014c\u0185\3\2\2\2\u014d\u014e\f\7\2\2\u014e\u014f")
        buf.write("\7\u008a\2\2\u014f\u0150\5,\27\2\u0150\u0151\7\u0089\2")
        buf.write("\2\u0151\u0152\5\22\n\b\u0152\u0185\3\2\2\2\u0153\u0154")
        buf.write("\f\61\2\2\u0154\u015d\7\22\2\2\u0155\u015a\5\22\n\2\u0156")
        buf.write("\u0157\7\4\2\2\u0157\u0159\5\22\n\2\u0158\u0156\3\2\2")
        buf.write("\2\u0159\u015c\3\2\2\2\u015a\u0158\3\2\2\2\u015a\u015b")
        buf.write("\3\2\2\2\u015b\u015e\3\2\2\2\u015c\u015a\3\2\2\2\u015d")
        buf.write("\u0155\3\2\2\2\u015d\u015e\3\2\2\2\u015e\u015f\3\2\2\2")
        buf.write("\u015f\u0185\7\u0097\2\2\u0160\u0161\f.\2\2\u0161\u0185")
        buf.write("\5\26\f\2\u0162\u0163\f,\2\2\u0163\u0164\7\u008a\2\2\u0164")
        buf.write("\u0165\7\24\2\2\u0165\u0166\7\17\2\2\u0166\u0185\5(\25")
        buf.write("\2\u0167\u0168\f+\2\2\u0168\u016a\7\25\2\2\u0169\u016b")
        buf.write("\7\26\2\2\u016a\u0169\3\2\2\2\u016a\u016b\3\2\2\2\u016b")
        buf.write("\u016c\3\2\2\2\u016c\u016d\7\27\2\2\u016d\u016e\7\17\2")
        buf.write("\2\u016e\u0185\5(\25\2\u016f\u0170\f*\2\2\u0170\u0171")
        buf.write("\7\u008a\2\2\u0171\u0185\5,\27\2\u0172\u0173\f)\2\2\u0173")
        buf.write("\u0174\7\30\2\2\u0174\u0185\5\30\r\2\u0175\u0176\f&\2")
        buf.write("\2\u0176\u0185\5\32\16\2\u0177\u0178\f%\2\2\u0178\u0185")
        buf.write("\5(\25\2\u0179\u017a\f$\2\2\u017a\u0185\7\33\2\2\u017b")
        buf.write("\u017c\f\35\2\2\u017c\u017d\7 \2\2\u017d\u017e\t\7\2\2")
        buf.write("\u017e\u0185\5,\27\2\u017f\u0180\f\24\2\2\u0180\u0181")
        buf.write("\7\20\2\2\u0181\u0182\5\22\n\2\u0182\u0183\7\u0096\2\2")
        buf.write("\u0183\u0185\3\2\2\2\u0184\u0124\3\2\2\2\u0184\u0128\3")
        buf.write("\2\2\2\u0184\u012b\3\2\2\2\u0184\u012e\3\2\2\2\u0184\u0131")
        buf.write("\3\2\2\2\u0184\u0135\3\2\2\2\u0184\u013b\3\2\2\2\u0184")
        buf.write("\u013e\3\2\2\2\u0184\u0141\3\2\2\2\u0184\u0144\3\2\2\2")
        buf.write("\u0184\u0147\3\2\2\2\u0184\u014d\3\2\2\2\u0184\u0153\3")
        buf.write("\2\2\2\u0184\u0160\3\2\2\2\u0184\u0162\3\2\2\2\u0184\u0167")
        buf.write("\3\2\2\2\u0184\u016f\3\2\2\2\u0184\u0172\3\2\2\2\u0184")
        buf.write("\u0175\3\2\2\2\u0184\u0177\3\2\2\2\u0184\u0179\3\2\2\2")
        buf.write("\u0184\u017b\3\2\2\2\u0184\u017f\3\2\2\2\u0185\u0188\3")
        buf.write("\2\2\2\u0186\u0184\3\2\2\2\u0186\u0187\3\2\2\2\u0187\23")
        buf.write("\3\2\2\2\u0188\u0186\3\2\2\2\u0189\u018a\7)\2\2\u018a")
        buf.write("\u018e\b\13\1\2\u018b\u018c\7*\2\2\u018c\u018e\b\13\1")
        buf.write("\2\u018d\u0189\3\2\2\2\u018d\u018b\3\2\2\2\u018e\25\3")
        buf.write("\2\2\2\u018f\u0190\t\b\2\2\u0190\u0191\b\f\1\2\u0191\u019c")
        buf.write("\b\f\1\2\u0192\u0193\t\t\2\2\u0193\u0194\b\f\1\2\u0194")
        buf.write("\u019c\b\f\1\2\u0195\u0196\t\n\2\2\u0196\u0197\b\f\1\2")
        buf.write("\u0197\u019c\b\f\1\2\u0198\u0199\t\13\2\2\u0199\u019a")
        buf.write("\b\f\1\2\u019a\u019c\b\f\1\2\u019b\u018f\3\2\2\2\u019b")
        buf.write("\u0192\3\2\2\2\u019b\u0195\3\2\2\2\u019b\u0198\3\2\2\2")
        buf.write("\u019c\27\3\2\2\2\u019d\u019e\t\f\2\2\u019e\u01a4\b\r")
        buf.write("\1\2\u019f\u01a0\t\r\2\2\u01a0\u01a4\b\r\1\2\u01a1\u01a2")
        buf.write("\7\65\2\2\u01a2\u01a4\b\r\1\2\u01a3\u019d\3\2\2\2\u01a3")
        buf.write("\u019f\3\2\2\2\u01a3\u01a1\3\2\2\2\u01a4\31\3\2\2\2\u01a5")
        buf.write("\u01a6\6\16\31\3\u01a6\u01a7\7\66\2\2\u01a7\u01a8\b\16")
        buf.write("\1\2\u01a8\u01b4\b\16\1\2\u01a9\u01aa\7\67\2\2\u01aa\u01ab")
        buf.write("\b\16\1\2\u01ab\u01b4\b\16\1\2\u01ac\u01ad\6\16\32\3\u01ad")
        buf.write("\u01ae\t\16\2\2\u01ae\u01af\b\16\1\2\u01af\u01b4\b\16")
        buf.write("\1\2\u01b0\u01b1\t\17\2\2\u01b1\u01b2\b\16\1\2\u01b2\u01b4")
        buf.write("\b\16\1\2\u01b3\u01a5\3\2\2\2\u01b3\u01a9\3\2\2\2\u01b3")
        buf.write("\u01ac\3\2\2\2\u01b3\u01b0\3\2\2\2\u01b4\33\3\2\2\2\u01b5")
        buf.write("\u01b6\7\66\2\2\u01b6\u01ba\b\17\1\2\u01b7\u01b8\t\16")
        buf.write("\2\2\u01b8\u01ba\b\17\1\2\u01b9\u01b5\3\2\2\2\u01b9\u01b7")
        buf.write("\3\2\2\2\u01ba\35\3\2\2\2\u01bb\u01be\5 \21\2\u01bc\u01bf")
        buf.write("\5\f\7\2\u01bd\u01bf\5\22\n\2\u01be\u01bc\3\2\2\2\u01be")
        buf.write("\u01bd\3\2\2\2\u01bf\37\3\2\2\2\u01c0\u01c1\7<\2\2\u01c1")
        buf.write("\u01ca\7\22\2\2\u01c2\u01c7\5\"\22\2\u01c3\u01c4\7\4\2")
        buf.write("\2\u01c4\u01c6\5\"\22\2\u01c5\u01c3\3\2\2\2\u01c6\u01c9")
        buf.write("\3\2\2\2\u01c7\u01c5\3\2\2\2\u01c7\u01c8\3\2\2\2\u01c8")
        buf.write("\u01cb\3\2\2\2\u01c9\u01c7\3\2\2\2\u01ca\u01c2\3\2\2\2")
        buf.write("\u01ca\u01cb\3\2\2\2\u01cb\u01cc\3\2\2\2\u01cc\u01cd\7")
        buf.write("\u0097\2\2\u01cd!\3\2\2\2\u01ce\u01d0\t\7\2\2\u01cf\u01ce")
        buf.write("\3\2\2\2\u01cf\u01d0\3\2\2\2\u01d0\u01d1\3\2\2\2\u01d1")
        buf.write("\u01d2\5&\24\2\u01d2\u01d3\b\22\1\2\u01d3\u01e6\3\2\2")
        buf.write("\2\u01d4\u01d5\5&\24\2\u01d5\u01d6\b\22\1\2\u01d6\u01d7")
        buf.write("\7\u0099\2\2\u01d7\u01d8\b\22\1\2\u01d8\u01e6\3\2\2\2")
        buf.write("\u01d9\u01da\5&\24\2\u01da\u01db\5\62\32\2\u01db\u01dc")
        buf.write("\b\22\1\2\u01dc\u01dd\b\22\1\2\u01dd\u01e6\3\2\2\2\u01de")
        buf.write("\u01df\5\62\32\2\u01df\u01e0\7\u008d\2\2\u01e0\u01e1\5")
        buf.write("&\24\2\u01e1\u01e2\b\22\1\2\u01e2\u01e3\b\22\1\2\u01e3")
        buf.write("\u01e4\b\22\1\2\u01e4\u01e6\3\2\2\2\u01e5\u01cf\3\2\2")
        buf.write("\2\u01e5\u01d4\3\2\2\2\u01e5\u01d9\3\2\2\2\u01e5\u01de")
        buf.write("\3\2\2\2\u01e6#\3\2\2\2\u01e7\u01e9\7=\2\2\u01e8\u01e7")
        buf.write("\3\2\2\2\u01e8\u01e9\3\2\2\2\u01e9\u01ea\3\2\2\2\u01ea")
        buf.write("\u01eb\7\u0092\2\2\u01eb\u0200\b\23\1\2\u01ec\u01ee\7")
        buf.write("=\2\2\u01ed\u01ec\3\2\2\2\u01ed\u01ee\3\2\2\2\u01ee\u01ef")
        buf.write("\3\2\2\2\u01ef\u01f0\7\u0091\2\2\u01f0\u0200\b\23\1\2")
        buf.write("\u01f1\u01f3\7\u0095\2\2\u01f2\u01f4\7>\2\2\u01f3\u01f2")
        buf.write("\3\2\2\2\u01f3\u01f4\3\2\2\2\u01f4\u01f5\3\2\2\2\u01f5")
        buf.write("\u0200\b\23\1\2\u01f6\u01fc\7?\2\2\u01f7\u01f9\7@\2\2")
        buf.write("\u01f8\u01fa\7\34\2\2\u01f9\u01f8\3\2\2\2\u01f9\u01fa")
        buf.write("\3\2\2\2\u01fa\u01fb\3\2\2\2\u01fb\u01fd\7A\2\2\u01fc")
        buf.write("\u01f7\3\2\2\2\u01fc\u01fd\3\2\2\2\u01fd\u01fe\3\2\2\2")
        buf.write("\u01fe\u0200\b\23\1\2\u01ff\u01e8\3\2\2\2\u01ff\u01ed")
        buf.write("\3\2\2\2\u01ff\u01f1\3\2\2\2\u01ff\u01f6\3\2\2\2\u0200")
        buf.write("%\3\2\2\2\u0201\u0202\7&\2\2\u0202\u023a\b\24\1\2\u0203")
        buf.write("\u0204\7B\2\2\u0204\u023a\b\24\1\2\u0205\u0206\7C\2\2")
        buf.write("\u0206\u023a\b\24\1\2\u0207\u0208\7C\2\2\u0208\u0209\7")
        buf.write("B\2\2\u0209\u023a\b\24\1\2\u020a\u020c\7C\2\2\u020b\u020a")
        buf.write("\3\2\2\2\u020b\u020c\3\2\2\2\u020c\u020d\3\2\2\2\u020d")
        buf.write("\u020e\7D\2\2\u020e\u023a\b\24\1\2\u020f\u0210\7E\2\2")
        buf.write("\u0210\u023a\b\24\1\2\u0211\u0212\7F\2\2\u0212\u023a\b")
        buf.write("\24\1\2\u0213\u0214\7\27\2\2\u0214\u023a\b\24\1\2\u0215")
        buf.write("\u0216\7>\2\2\u0216\u023a\b\24\1\2\u0217\u0218\7G\2\2")
        buf.write("\u0218\u023a\b\24\1\2\u0219\u021a\7H\2\2\u021a\u023a\b")
        buf.write("\24\1\2\u021b\u021c\7I\2\2\u021c\u023a\b\24\1\2\u021d")
        buf.write("\u021e\7J\2\2\u021e\u023a\b\24\1\2\u021f\u0220\7K\2\2")
        buf.write("\u0220\u023a\b\24\1\2\u0221\u0222\7L\2\2\u0222\u023a\b")
        buf.write("\24\1\2\u0223\u0224\7M\2\2\u0224\u023a\b\24\1\2\u0225")
        buf.write("\u0226\t\4\2\2\u0226\u023a\b\24\1\2\u0227\u0228\7N\2\2")
        buf.write("\u0228\u023a\b\24\1\2\u0229\u022a\7\35\2\2\u022a\u023a")
        buf.write("\b\24\1\2\u022b\u022c\7O\2\2\u022c\u023a\b\24\1\2\u022d")
        buf.write("\u022e\t\20\2\2\u022e\u022f\t\21\2\2\u022f\u023a\b\24")
        buf.write("\1\2\u0230\u0232\t\20\2\2\u0231\u0233\7T\2\2\u0232\u0231")
        buf.write("\3\2\2\2\u0232\u0233\3\2\2\2\u0233\u0234\3\2\2\2\u0234")
        buf.write("\u023a\b\24\1\2\u0235\u0236\7U\2\2\u0236\u023a\b\24\1")
        buf.write("\2\u0237\u0238\7V\2\2\u0238\u023a\b\24\1\2\u0239\u0201")
        buf.write("\3\2\2\2\u0239\u0203\3\2\2\2\u0239\u0205\3\2\2\2\u0239")
        buf.write("\u0207\3\2\2\2\u0239\u020b\3\2\2\2\u0239\u020f\3\2\2\2")
        buf.write("\u0239\u0211\3\2\2\2\u0239\u0213\3\2\2\2\u0239\u0215\3")
        buf.write("\2\2\2\u0239\u0217\3\2\2\2\u0239\u0219\3\2\2\2\u0239\u021b")
        buf.write("\3\2\2\2\u0239\u021d\3\2\2\2\u0239\u021f\3\2\2\2\u0239")
        buf.write("\u0221\3\2\2\2\u0239\u0223\3\2\2\2\u0239\u0225\3\2\2\2")
        buf.write("\u0239\u0227\3\2\2\2\u0239\u0229\3\2\2\2\u0239\u022b\3")
        buf.write("\2\2\2\u0239\u022d\3\2\2\2\u0239\u0230\3\2\2\2\u0239\u0235")
        buf.write("\3\2\2\2\u0239\u0237\3\2\2\2\u023a\'\3\2\2\2\u023b\u023c")
        buf.write("\t\22\2\2\u023c\u0248\b\25\1\2\u023d\u023e\t\23\2\2\u023e")
        buf.write("\u0248\b\25\1\2\u023f\u0240\t\24\2\2\u0240\u0248\b\25")
        buf.write("\1\2\u0241\u0242\t\25\2\2\u0242\u0248\b\25\1\2\u0243\u0244")
        buf.write("\t\26\2\2\u0244\u0248\b\25\1\2\u0245\u0246\t\27\2\2\u0246")
        buf.write("\u0248\b\25\1\2\u0247\u023b\3\2\2\2\u0247\u023d\3\2\2")
        buf.write("\2\u0247\u023f\3\2\2\2\u0247\u0241\3\2\2\2\u0247\u0243")
        buf.write("\3\2\2\2\u0247\u0245\3\2\2\2\u0248)\3\2\2\2\u0249\u024a")
        buf.write("\7C\2\2\u024a\u0250\b\26\1\2\u024b\u024c\7U\2\2\u024c")
        buf.write("\u0250\b\26\1\2\u024d\u024e\7V\2\2\u024e\u0250\b\26\1")
        buf.write("\2\u024f\u0249\3\2\2\2\u024f\u024b\3\2\2\2\u024f\u024d")
        buf.write("\3\2\2\2\u0250+\3\2\2\2\u0251\u0252\7m\2\2\u0252\u0253")
        buf.write("\7B\2\2\u0253\u0278\b\27\1\2\u0254\u0255\7D\2\2\u0255")
        buf.write("\u0278\b\27\1\2\u0256\u0257\t\4\2\2\u0257\u0278\b\27\1")
        buf.write("\2\u0258\u025c\7\66\2\2\u0259\u025a\7n\2\2\u025a\u025c")
        buf.write("\t\30\2\2\u025b\u0258\3\2\2\2\u025b\u0259\3\2\2\2\u025c")
        buf.write("\u025d\3\2\2\2\u025d\u0278\b\27\1\2\u025e\u0263\78\2\2")
        buf.write("\u025f\u0263\79\2\2\u0260\u0261\7q\2\2\u0261\u0263\t\30")
        buf.write("\2\2\u0262\u025e\3\2\2\2\u0262\u025f\3\2\2\2\u0262\u0260")
        buf.write("\3\2\2\2\u0263\u0264\3\2\2\2\u0264\u0278\b\27\1\2\u0265")
        buf.write("\u0266\7m\2\2\u0266\u0267\t\4\2\2\u0267\u0278\b\27\1\2")
        buf.write("\u0268\u0269\7r\2\2\u0269\u026a\7s\2\2\u026a\u0278\b\27")
        buf.write("\1\2\u026b\u026d\7t\2\2\u026c\u026e\t\20\2\2\u026d\u026c")
        buf.write("\3\2\2\2\u026d\u026e\3\2\2\2\u026e\u026f\3\2\2\2\u026f")
        buf.write("\u0278\b\27\1\2\u0270\u0272\7u\2\2\u0271\u0270\3\2\2\2")
        buf.write("\u0271\u0272\3\2\2\2\u0272\u0273\3\2\2\2\u0273\u0274\t")
        buf.write("\20\2\2\u0274\u0278\b\27\1\2\u0275\u0276\t\31\2\2\u0276")
        buf.write("\u0278\b\27\1\2\u0277\u0251\3\2\2\2\u0277\u0254\3\2\2")
        buf.write("\2\u0277\u0256\3\2\2\2\u0277\u025b\3\2\2\2\u0277\u0262")
        buf.write("\3\2\2\2\u0277\u0265\3\2\2\2\u0277\u0268\3\2\2\2\u0277")
        buf.write("\u026b\3\2\2\2\u0277\u0271\3\2\2\2\u0277\u0275\3\2\2\2")
        buf.write("\u0278-\3\2\2\2\u0279\u027a\7v\2\2\u027a\u0286\b\30\1")
        buf.write("\2\u027b\u027c\7w\2\2\u027c\u0286\b\30\1\2\u027d\u027e")
        buf.write("\7x\2\2\u027e\u0286\b\30\1\2\u027f\u0280\7y\2\2\u0280")
        buf.write("\u0286\b\30\1\2\u0281\u0282\7z\2\2\u0282\u0286\b\30\1")
        buf.write("\2\u0283\u0284\7{\2\2\u0284\u0286\b\30\1\2\u0285\u0279")
        buf.write("\3\2\2\2\u0285\u027b\3\2\2\2\u0285\u027d\3\2\2\2\u0285")
        buf.write("\u027f\3\2\2\2\u0285\u0281\3\2\2\2\u0285\u0283\3\2\2\2")
        buf.write("\u0286/\3\2\2\2\u0287\u0288\t\32\2\2\u0288\u028c\b\31")
        buf.write("\1\2\u0289\u028a\t\33\2\2\u028a\u028c\b\31\1\2\u028b\u0287")
        buf.write("\3\2\2\2\u028b\u0289\3\2\2\2\u028c\61\3\2\2\2\u028d\u028e")
        buf.write("\5\64\33\2\u028e\u028f\b\32\1\2\u028f\u0296\3\2\2\2\u0290")
        buf.write("\u0291\7\u0098\2\2\u0291\u0296\b\32\1\2\u0292\u0293\5")
        buf.write("\66\34\2\u0293\u0294\b\32\1\2\u0294\u0296\3\2\2\2\u0295")
        buf.write("\u028d\3\2\2\2\u0295\u0290\3\2\2\2\u0295\u0292\3\2\2\2")
        buf.write("\u0296\63\3\2\2\2\u0297\u0299\7\u0092\2\2\u0298\u029a")
        buf.write("\7\34\2\2\u0299\u0298\3\2\2\2\u0299\u029a\3\2\2\2\u029a")
        buf.write("\u029b\3\2\2\2\u029b\u029c\7A\2\2\u029c\u02a4\b\33\1\2")
        buf.write("\u029d\u029e\7\u008c\2\2\u029e\u029f\7\35\2\2\u029f\u02a4")
        buf.write("\b\33\1\2\u02a0\u02a1\7\u008c\2\2\u02a1\u02a2\7N\2\2\u02a2")
        buf.write("\u02a4\b\33\1\2\u02a3\u0297\3\2\2\2\u02a3\u029d\3\2\2")
        buf.write("\2\u02a3\u02a0\3\2\2\2\u02a4\65\3\2\2\2\u02a5\u02a6\t")
        buf.write("\34\2\2\u02a6\67\3\2\2\2\u02a7\u02a8\7\u009b\2\2\u02a8")
        buf.write("9\3\2\2\2A=GMSXbhtz\177\u0087\u009e\u00a3\u00aa\u00b0")
        buf.write("\u00b8\u00bc\u00d0\u00d6\u00ec\u00f0\u00f3\u00f7\u0102")
        buf.write("\u010d\u0122\u0138\u015a\u015d\u016a\u0184\u0186\u018d")
        buf.write("\u019b\u01a3\u01b3\u01b9\u01be\u01c7\u01ca\u01cf\u01e5")
        buf.write("\u01e8\u01ed\u01f3\u01f9\u01fc\u01ff\u020b\u0232\u0239")
        buf.write("\u0247\u024f\u025b\u0262\u026d\u0271\u0277\u0285\u028b")
        buf.write("\u0295\u0299\u02a3")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'print'", "','", "'pause'", "'if'", "'else'", 
                     "'{'", "'}'", "'[['", "']]'", "'repeat'", "'times'", 
                     "'for'", "'in'", "'['", "'by'", "'('", "'#'", "'magnitude'", 
                     "'as'", "'a'", "'string'", "'turned'", "'dir'", "'direction'", 
                     "'C'", "'the'", "'reagent'", "'named'", "'of'", "'has'", 
                     "'an'", "'is'", "'and'", "'or'", "'to'", "'drop'", 
                     "'@'", "'at'", "'unknown'", "'waste'", "'up'", "'north'", 
                     "'down'", "'south'", "'left'", "'west'", "'right'", 
                     "'east'", "'clockwise'", "'counterclockwise'", "'around'", 
                     "'row'", "'rows'", "'col'", "'column'", "'cols'", "'columns'", 
                     "'macro'", "'turn'", "'state'", "'remove'", "'from'", 
                     "'board'", "'pad'", "'well'", "'gate'", "'int'", "'float'", 
                     "'electrode'", "'delta'", "'motion'", "'delay'", "'time'", 
                     "'ticks'", "'bool'", "'volume'", "'liquid'", "'temp'", 
                     "'temperature'", "'diff'", "'difference'", "'point'", 
                     "'heater'", "'magnet'", "'s'", "'sec'", "'secs'", "'second'", 
                     "'seconds'", "'ms'", "'millisecond'", "'milliseconds'", 
                     "'uL'", "'ul'", "'microliter'", "'microlitre'", "'microliters'", 
                     "'microlitres'", "'mL'", "'ml'", "'milliliter'", "'millilitre'", 
                     "'milliliters'", "'millilitres'", "'tick'", "'drops'", 
                     "'exit'", "'y'", "'coord'", "'coordinate'", "'x'", 
                     "'remaining'", "'capacity'", "'target'", "'current'", 
                     "'=='", "'!='", "'<'", "'<='", "'>'", "'>='", "'True'", 
                     "'true'", "'TRUE'", "'Yes'", "'yes'", "'YES'", "'False'", 
                     "'false'", "'FALSE'", "'No'", "'no'", "'NO'", "'+'", 
                     "'='", "''s'", "'/'", "'interactive'", "':'", "'local'", 
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
                      "<INVALID>", "<INVALID>", "ADD", "ASSIGN", "ATTR", 
                      "DIV", "INTERACTIVE", "INJECT", "LOCAL", "MUL", "NOT", 
                      "OFF", "ON", "SUB", "TERMINATOR", "TOGGLE", "CLOSE_BRACKET", 
                      "CLOSE_PAREN", "ID", "INT", "FLOAT", "STRING", "EOL_COMMENT", 
                      "COMMENT", "WS" ]

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
    RULE_bool_val = 23
    RULE_name = 24
    RULE_multi_word_name = 25
    RULE_kwd_names = 26
    RULE_string = 27

    ruleNames =  [ "macro_file", "interactive", "declaration", "printing", 
                   "stat", "compound", "loop", "term_punct", "expr", "reagent", 
                   "direction", "turn", "rc", "axis", "macro_def", "macro_header", 
                   "param", "no_arg_action", "param_type", "dim_unit", "numbered_type", 
                   "attr", "rel", "bool_val", "name", "multi_word_name", 
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
    ADD=134
    ASSIGN=135
    ATTR=136
    DIV=137
    INTERACTIVE=138
    INJECT=139
    LOCAL=140
    MUL=141
    NOT=142
    OFF=143
    ON=144
    SUB=145
    TERMINATOR=146
    TOGGLE=147
    CLOSE_BRACKET=148
    CLOSE_PAREN=149
    ID=150
    INT=151
    FLOAT=152
    STRING=153
    EOL_COMMENT=154
    COMMENT=155
    WS=156

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
            self.state = 59
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__9) | (1 << DMFParser.T__11) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__20) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__67 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__110 - 64)) | (1 << (DMFParser.T__121 - 64)) | (1 << (DMFParser.T__122 - 64)) | (1 << (DMFParser.T__123 - 64)) | (1 << (DMFParser.T__124 - 64)) | (1 << (DMFParser.T__125 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (DMFParser.T__127 - 128)) | (1 << (DMFParser.T__128 - 128)) | (1 << (DMFParser.T__129 - 128)) | (1 << (DMFParser.T__130 - 128)) | (1 << (DMFParser.T__131 - 128)) | (1 << (DMFParser.T__132 - 128)) | (1 << (DMFParser.INTERACTIVE - 128)) | (1 << (DMFParser.LOCAL - 128)) | (1 << (DMFParser.NOT - 128)) | (1 << (DMFParser.OFF - 128)) | (1 << (DMFParser.ON - 128)) | (1 << (DMFParser.SUB - 128)) | (1 << (DMFParser.TOGGLE - 128)) | (1 << (DMFParser.ID - 128)) | (1 << (DMFParser.INT - 128)) | (1 << (DMFParser.FLOAT - 128)) | (1 << (DMFParser.STRING - 128)))) != 0):
                self.state = 56
                self.stat()
                self.state = 61
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 62
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
            self.state = 86
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 64
                self.compound()
                self.state = 65
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Decl_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 67
                self.declaration()
                self.state = 69
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 68
                    self.match(DMFParser.TERMINATOR)


                self.state = 71
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Print_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 73
                self.printing()
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 74
                    self.match(DMFParser.TERMINATOR)


                self.state = 77
                self.match(DMFParser.EOF)
                pass

            elif la_ == 4:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 79
                self.expr(0)
                self.state = 81
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 80
                    self.match(DMFParser.TERMINATOR)


                self.state = 83
                self.match(DMFParser.EOF)
                pass

            elif la_ == 5:
                localctx = DMFParser.Empty_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 85
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
            self.state = 125
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 88
                self.match(DMFParser.LOCAL)
                self.state = 89
                localctx._name = self.name()
                self.state = 90
                self.match(DMFParser.ASSIGN)
                self.state = 91
                localctx.init = self.expr(0)
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                localctx.type=None
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 96
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.LOCAL:
                    self.state = 95
                    self.match(DMFParser.LOCAL)


                self.state = 98
                localctx._param_type = self.param_type()
                self.state = 99
                localctx._INT = self.match(DMFParser.INT)
                self.state = 100
                self.match(DMFParser.ASSIGN)
                self.state = 102
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__2) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__20) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__67 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__110 - 64)) | (1 << (DMFParser.T__121 - 64)) | (1 << (DMFParser.T__122 - 64)) | (1 << (DMFParser.T__123 - 64)) | (1 << (DMFParser.T__124 - 64)) | (1 << (DMFParser.T__125 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (DMFParser.T__127 - 128)) | (1 << (DMFParser.T__128 - 128)) | (1 << (DMFParser.T__129 - 128)) | (1 << (DMFParser.T__130 - 128)) | (1 << (DMFParser.T__131 - 128)) | (1 << (DMFParser.T__132 - 128)) | (1 << (DMFParser.INTERACTIVE - 128)) | (1 << (DMFParser.NOT - 128)) | (1 << (DMFParser.OFF - 128)) | (1 << (DMFParser.ON - 128)) | (1 << (DMFParser.SUB - 128)) | (1 << (DMFParser.TOGGLE - 128)) | (1 << (DMFParser.ID - 128)) | (1 << (DMFParser.INT - 128)) | (1 << (DMFParser.FLOAT - 128)) | (1 << (DMFParser.STRING - 128)))) != 0):
                    self.state = 101
                    localctx.init = self.expr(0)


                localctx.type=localctx._param_type.type
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 107
                self.match(DMFParser.LOCAL)
                self.state = 108
                localctx._param_type = self.param_type()
                self.state = 109
                localctx._INT = self.match(DMFParser.INT)
                localctx.type=localctx._param_type.type
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 114
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.LOCAL:
                    self.state = 113
                    self.match(DMFParser.LOCAL)


                self.state = 116
                localctx._param_type = self.param_type()
                self.state = 117
                localctx._name = self.name()
                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.ASSIGN:
                    self.state = 118
                    self.match(DMFParser.ASSIGN)
                    self.state = 119
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
            self.state = 127
            self.match(DMFParser.T__0)
            self.state = 128
            localctx._expr = self.expr(0)
            localctx.vals.append(localctx._expr)
            self.state = 133
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DMFParser.T__1:
                self.state = 129
                self.match(DMFParser.T__1)
                self.state = 130
                localctx._expr = self.expr(0)
                localctx.vals.append(localctx._expr)
                self.state = 135
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
            self.state = 168
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Decl_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 136
                self.declaration()
                self.state = 137
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Pause_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 139
                self.match(DMFParser.T__2)
                self.state = 140
                localctx.duration = self.expr(0)
                self.state = 141
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 3:
                localctx = DMFParser.Print_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 143
                self.printing()
                self.state = 144
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 4:
                localctx = DMFParser.If_statContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 146
                self.match(DMFParser.T__3)
                self.state = 147
                localctx._expr = self.expr(0)
                localctx.tests.append(localctx._expr)
                self.state = 148
                localctx._compound = self.compound()
                localctx.bodies.append(localctx._compound)
                self.state = 156
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 149
                        self.match(DMFParser.T__4)
                        self.state = 150
                        self.match(DMFParser.T__3)
                        self.state = 151
                        localctx._expr = self.expr(0)
                        localctx.tests.append(localctx._expr)
                        self.state = 152
                        localctx._compound = self.compound()
                        localctx.bodies.append(localctx._compound) 
                    self.state = 158
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

                self.state = 161
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__4:
                    self.state = 159
                    self.match(DMFParser.T__4)
                    self.state = 160
                    localctx.else_body = self.compound()


                pass

            elif la_ == 5:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 163
                self.expr(0)
                self.state = 164
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 6:
                localctx = DMFParser.Loop_statContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 166
                self.loop()
                pass

            elif la_ == 7:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 167
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
            self.state = 186
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__5]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 170
                self.match(DMFParser.T__5)
                self.state = 174
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__9) | (1 << DMFParser.T__11) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__20) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__67 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__110 - 64)) | (1 << (DMFParser.T__121 - 64)) | (1 << (DMFParser.T__122 - 64)) | (1 << (DMFParser.T__123 - 64)) | (1 << (DMFParser.T__124 - 64)) | (1 << (DMFParser.T__125 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (DMFParser.T__127 - 128)) | (1 << (DMFParser.T__128 - 128)) | (1 << (DMFParser.T__129 - 128)) | (1 << (DMFParser.T__130 - 128)) | (1 << (DMFParser.T__131 - 128)) | (1 << (DMFParser.T__132 - 128)) | (1 << (DMFParser.INTERACTIVE - 128)) | (1 << (DMFParser.LOCAL - 128)) | (1 << (DMFParser.NOT - 128)) | (1 << (DMFParser.OFF - 128)) | (1 << (DMFParser.ON - 128)) | (1 << (DMFParser.SUB - 128)) | (1 << (DMFParser.TOGGLE - 128)) | (1 << (DMFParser.ID - 128)) | (1 << (DMFParser.INT - 128)) | (1 << (DMFParser.FLOAT - 128)) | (1 << (DMFParser.STRING - 128)))) != 0):
                    self.state = 171
                    self.stat()
                    self.state = 176
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 177
                self.match(DMFParser.T__6)
                pass
            elif token in [DMFParser.T__7]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 178
                self.match(DMFParser.T__7)
                self.state = 182
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__9) | (1 << DMFParser.T__11) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__20) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__67 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__110 - 64)) | (1 << (DMFParser.T__121 - 64)) | (1 << (DMFParser.T__122 - 64)) | (1 << (DMFParser.T__123 - 64)) | (1 << (DMFParser.T__124 - 64)) | (1 << (DMFParser.T__125 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (DMFParser.T__127 - 128)) | (1 << (DMFParser.T__128 - 128)) | (1 << (DMFParser.T__129 - 128)) | (1 << (DMFParser.T__130 - 128)) | (1 << (DMFParser.T__131 - 128)) | (1 << (DMFParser.T__132 - 128)) | (1 << (DMFParser.INTERACTIVE - 128)) | (1 << (DMFParser.LOCAL - 128)) | (1 << (DMFParser.NOT - 128)) | (1 << (DMFParser.OFF - 128)) | (1 << (DMFParser.ON - 128)) | (1 << (DMFParser.SUB - 128)) | (1 << (DMFParser.TOGGLE - 128)) | (1 << (DMFParser.ID - 128)) | (1 << (DMFParser.INT - 128)) | (1 << (DMFParser.FLOAT - 128)) | (1 << (DMFParser.STRING - 128)))) != 0):
                    self.state = 179
                    self.stat()
                    self.state = 184
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 185
                self.match(DMFParser.T__8)
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
            self.state = 206
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__9]:
                localctx = DMFParser.Repeat_loopContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 188
                self.match(DMFParser.T__9)
                self.state = 189
                localctx.n = self.expr(0)
                self.state = 190
                self.match(DMFParser.T__10)
                self.state = 191
                localctx.body = self.stat()
                pass
            elif token in [DMFParser.T__11]:
                localctx = DMFParser.For_loopContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 193
                self.match(DMFParser.T__11)
                self.state = 194
                localctx.var = self.name()
                self.state = 195
                self.match(DMFParser.T__12)
                self.state = 196
                self.match(DMFParser.T__13)
                self.state = 197
                localctx.start = self.expr(0)
                self.state = 198
                self.match(DMFParser.T__1)
                self.state = 199
                localctx.stop = self.expr(0)
                self.state = 200
                self.term_punct()

                self.state = 201
                self.match(DMFParser.T__14)
                self.state = 202
                localctx.step = self.expr(0)
                self.state = 204
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
            self.state = 212
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.CLOSE_BRACKET]:
                self.enterOuterAlt(localctx, 1)
                self.state = 208
                self.match(DMFParser.CLOSE_BRACKET)
                localctx.is_closed=True
                pass
            elif token in [DMFParser.CLOSE_PAREN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 210
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

        def ASSIGN(self):
            return self.getToken(DMFParser.ASSIGN, 0)
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

        def ASSIGN(self):
            return self.getToken(DMFParser.ASSIGN, 0)
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
            self.state = 288
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,25,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 215
                self.match(DMFParser.T__15)
                self.state = 216
                self.expr(0)
                self.state = 217
                self.match(DMFParser.CLOSE_PAREN)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 219
                self.match(DMFParser.T__15)
                self.state = 220
                localctx.x = self.expr(0)
                self.state = 221
                self.match(DMFParser.T__1)
                self.state = 222
                localctx.y = self.expr(0)
                self.state = 223
                self.match(DMFParser.CLOSE_PAREN)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 225
                self.match(DMFParser.SUB)
                self.state = 226
                localctx.rhs = self.expr(45)
                pass

            elif la_ == 4:
                localctx = DMFParser.Numbered_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 227
                localctx.kind = self.numbered_type()
                self.state = 228
                self.match(DMFParser.T__16)
                self.state = 229
                localctx.which = self.expr(43)
                pass

            elif la_ == 5:
                localctx = DMFParser.Const_rc_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 231
                localctx._INT = self.match(DMFParser.INT)
                self.state = 232
                self.rc((0 if localctx._INT is None else int(localctx._INT.text)))
                pass

            elif la_ == 6:
                localctx = DMFParser.Reagent_lit_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 234
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__25:
                    self.state = 233
                    self.match(DMFParser.T__25)


                self.state = 236
                self.reagent()
                self.state = 238
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
                if la_ == 1:
                    self.state = 237
                    self.match(DMFParser.T__26)


                pass

            elif la_ == 7:
                localctx = DMFParser.Reagent_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 241
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__19 or _la==DMFParser.T__25:
                    self.state = 240
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__19 or _la==DMFParser.T__25):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 243
                self.match(DMFParser.T__26)
                self.state = 245
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__27:
                    self.state = 244
                    self.match(DMFParser.T__27)


                self.state = 247
                localctx.which = self.expr(32)
                pass

            elif la_ == 8:
                localctx = DMFParser.Not_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 248
                self.match(DMFParser.NOT)
                self.state = 249
                self.expr(25)
                pass

            elif la_ == 9:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 250
                self.direction()
                self.state = 251
                localctx.dist = self.expr(22)
                pass

            elif la_ == 10:
                localctx = DMFParser.Dir_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 253
                self.direction()
                pass

            elif la_ == 11:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 254
                self.match(DMFParser.T__34)
                self.state = 256
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__51) | (1 << DMFParser.T__53) | (1 << DMFParser.T__54))) != 0):
                    self.state = 255
                    self.axis()


                self.state = 258
                localctx.which = self.expr(20)
                pass

            elif la_ == 12:
                localctx = DMFParser.Pause_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 259
                self.match(DMFParser.T__2)
                self.state = 260
                localctx.duration = self.expr(19)
                pass

            elif la_ == 13:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 261
                self.match(DMFParser.T__35)
                self.state = 262
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__36 or _la==DMFParser.T__37):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 263
                localctx.loc = self.expr(17)
                pass

            elif la_ == 14:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 264
                self.macro_def()
                pass

            elif la_ == 15:
                localctx = DMFParser.Action_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 265
                self.no_arg_action()
                pass

            elif la_ == 16:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 267
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__25:
                    self.state = 266
                    self.match(DMFParser.T__25)


                self.state = 269
                self.param_type()
                pass

            elif la_ == 17:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 270
                self.param_type()
                self.state = 271
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 18:
                localctx = DMFParser.Bool_const_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 273
                localctx.val = self.bool_val()
                pass

            elif la_ == 19:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 274
                self.name()
                pass

            elif la_ == 20:
                localctx = DMFParser.Mw_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 275
                self.multi_word_name()
                pass

            elif la_ == 21:
                localctx = DMFParser.Name_assign_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 276
                localctx.which = self.name()
                self.state = 277
                self.match(DMFParser.ASSIGN)
                self.state = 278
                localctx.what = self.expr(6)
                pass

            elif la_ == 22:
                localctx = DMFParser.Name_assign_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 280
                localctx.ptype = self.param_type()
                self.state = 281
                localctx.n = self.match(DMFParser.INT)
                self.state = 282
                self.match(DMFParser.ASSIGN)
                self.state = 283
                localctx.what = self.expr(4)
                pass

            elif la_ == 23:
                localctx = DMFParser.String_lit_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 285
                self.string()
                pass

            elif la_ == 24:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 286
                localctx._INT = self.match(DMFParser.INT)
                pass

            elif la_ == 25:
                localctx = DMFParser.Float_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 287
                self.match(DMFParser.FLOAT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 388
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,31,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 386
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.In_dir_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 290
                        if not self.precpred(self._ctx, 38):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 38)")
                        self.state = 291
                        self.match(DMFParser.T__12)
                        self.state = 292
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__22 or _la==DMFParser.T__23):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 293
                        localctx.d = self.expr(39)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Liquid_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.vol = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 294
                        if not self.precpred(self._ctx, 31):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 31)")
                        self.state = 295
                        self.match(DMFParser.T__28)
                        self.state = 296
                        localctx.which = self.expr(32)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 297
                        if not self.precpred(self._ctx, 30):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 30)")
                        self.state = 298
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 299
                        localctx.rhs = self.expr(31)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 300
                        if not self.precpred(self._ctx, 29):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 29)")
                        self.state = 301
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 302
                        localctx.rhs = self.expr(30)
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.Rel_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 303
                        if not self.precpred(self._ctx, 28):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 28)")
                        self.state = 304
                        self.rel()
                        self.state = 305
                        localctx.rhs = self.expr(29)
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Is_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 307
                        if not self.precpred(self._ctx, 26):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 26)")
                        self.state = 308
                        self.match(DMFParser.T__31)
                        self.state = 310
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
                        if la_ == 1:
                            self.state = 309
                            self.match(DMFParser.NOT)


                        self.state = 312
                        localctx.pred = self.expr(27)
                        pass

                    elif la_ == 7:
                        localctx = DMFParser.And_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 313
                        if not self.precpred(self._ctx, 24):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 24)")
                        self.state = 314
                        self.match(DMFParser.T__32)
                        self.state = 315
                        localctx.rhs = self.expr(25)
                        pass

                    elif la_ == 8:
                        localctx = DMFParser.Or_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 316
                        if not self.precpred(self._ctx, 23):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 23)")
                        self.state = 317
                        self.match(DMFParser.T__33)
                        self.state = 318
                        localctx.rhs = self.expr(24)
                        pass

                    elif la_ == 9:
                        localctx = DMFParser.Drop_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.vol = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 319
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 320
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__36 or _la==DMFParser.T__37):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 321
                        localctx.loc = self.expr(17)
                        pass

                    elif la_ == 10:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 322
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 323
                        self.match(DMFParser.INJECT)
                        self.state = 324
                        localctx.what = self.expr(16)
                        pass

                    elif la_ == 11:
                        localctx = DMFParser.Cond_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.first = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 325
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 326
                        self.match(DMFParser.T__3)
                        self.state = 327
                        localctx.cond = self.expr(0)
                        self.state = 328
                        self.match(DMFParser.T__4)
                        self.state = 329
                        localctx.second = self.expr(15)
                        pass

                    elif la_ == 12:
                        localctx = DMFParser.Attr_assign_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 331
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 332
                        self.match(DMFParser.ATTR)
                        self.state = 333
                        self.attr()
                        self.state = 334
                        self.match(DMFParser.ASSIGN)
                        self.state = 335
                        localctx.what = self.expr(6)
                        pass

                    elif la_ == 13:
                        localctx = DMFParser.Function_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.func = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 337
                        if not self.precpred(self._ctx, 47):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 47)")
                        self.state = 338
                        self.match(DMFParser.T__15)
                        self.state = 347
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__2) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__20) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__67 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__110 - 64)) | (1 << (DMFParser.T__121 - 64)) | (1 << (DMFParser.T__122 - 64)) | (1 << (DMFParser.T__123 - 64)) | (1 << (DMFParser.T__124 - 64)) | (1 << (DMFParser.T__125 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (DMFParser.T__127 - 128)) | (1 << (DMFParser.T__128 - 128)) | (1 << (DMFParser.T__129 - 128)) | (1 << (DMFParser.T__130 - 128)) | (1 << (DMFParser.T__131 - 128)) | (1 << (DMFParser.T__132 - 128)) | (1 << (DMFParser.INTERACTIVE - 128)) | (1 << (DMFParser.NOT - 128)) | (1 << (DMFParser.OFF - 128)) | (1 << (DMFParser.ON - 128)) | (1 << (DMFParser.SUB - 128)) | (1 << (DMFParser.TOGGLE - 128)) | (1 << (DMFParser.ID - 128)) | (1 << (DMFParser.INT - 128)) | (1 << (DMFParser.FLOAT - 128)) | (1 << (DMFParser.STRING - 128)))) != 0):
                            self.state = 339
                            localctx._expr = self.expr(0)
                            localctx.args.append(localctx._expr)
                            self.state = 344
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            while _la==DMFParser.T__1:
                                self.state = 340
                                self.match(DMFParser.T__1)
                                self.state = 341
                                localctx._expr = self.expr(0)
                                localctx.args.append(localctx._expr)
                                self.state = 346
                                self._errHandler.sync(self)
                                _la = self._input.LA(1)



                        self.state = 349
                        self.match(DMFParser.CLOSE_PAREN)
                        pass

                    elif la_ == 14:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 350
                        if not self.precpred(self._ctx, 44):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 44)")
                        self.state = 351
                        self.direction()
                        pass

                    elif la_ == 15:
                        localctx = DMFParser.Magnitude_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.quant = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 352
                        if not self.precpred(self._ctx, 42):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 42)")
                        self.state = 353
                        self.match(DMFParser.ATTR)
                        self.state = 354
                        self.match(DMFParser.T__17)
                        self.state = 355
                        self.match(DMFParser.T__12)
                        self.state = 356
                        self.dim_unit()
                        pass

                    elif la_ == 16:
                        localctx = DMFParser.Unit_string_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.quant = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 357
                        if not self.precpred(self._ctx, 41):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 41)")
                        self.state = 358
                        self.match(DMFParser.T__18)
                        self.state = 360
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==DMFParser.T__19:
                            self.state = 359
                            self.match(DMFParser.T__19)


                        self.state = 362
                        self.match(DMFParser.T__20)
                        self.state = 363
                        self.match(DMFParser.T__12)
                        self.state = 364
                        self.dim_unit()
                        pass

                    elif la_ == 17:
                        localctx = DMFParser.Attr_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 365
                        if not self.precpred(self._ctx, 40):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 40)")
                        self.state = 366
                        self.match(DMFParser.ATTR)
                        self.state = 367
                        self.attr()
                        pass

                    elif la_ == 18:
                        localctx = DMFParser.Turn_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.start_dir = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 368
                        if not self.precpred(self._ctx, 39):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 39)")
                        self.state = 369
                        self.match(DMFParser.T__21)
                        self.state = 370
                        self.turn()
                        pass

                    elif la_ == 19:
                        localctx = DMFParser.N_rc_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 371
                        if not self.precpred(self._ctx, 36):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 36)")
                        self.state = 372
                        self.rc(0)
                        pass

                    elif la_ == 20:
                        localctx = DMFParser.Unit_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 373
                        if not self.precpred(self._ctx, 35):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 35)")
                        self.state = 374
                        self.dim_unit()
                        pass

                    elif la_ == 21:
                        localctx = DMFParser.Temperature_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 375
                        if not self.precpred(self._ctx, 34):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 34)")
                        self.state = 376
                        self.match(DMFParser.T__24)
                        pass

                    elif la_ == 22:
                        localctx = DMFParser.Has_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 377
                        if not self.precpred(self._ctx, 27):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 27)")
                        self.state = 378
                        self.match(DMFParser.T__29)
                        self.state = 379
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__19 or _la==DMFParser.T__30):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 380
                        self.attr()
                        pass

                    elif la_ == 23:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 381
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 382
                        self.match(DMFParser.T__13)
                        self.state = 383
                        localctx.which = self.expr(0)
                        self.state = 384
                        self.match(DMFParser.CLOSE_BRACKET)
                        pass

             
                self.state = 390
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,31,self._ctx)

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
            self.state = 395
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__38]:
                self.enterOuterAlt(localctx, 1)
                self.state = 391
                self.match(DMFParser.T__38)
                localctx.r = unknown_reagent
                pass
            elif token in [DMFParser.T__39]:
                self.enterOuterAlt(localctx, 2)
                self.state = 393
                self.match(DMFParser.T__39)
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
            self.state = 409
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__40, DMFParser.T__41]:
                self.enterOuterAlt(localctx, 1)
                self.state = 397
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__40 or _la==DMFParser.T__41):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__42, DMFParser.T__43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 400
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__42 or _la==DMFParser.T__43):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__44, DMFParser.T__45]:
                self.enterOuterAlt(localctx, 3)
                self.state = 403
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__44 or _la==DMFParser.T__45):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__46, DMFParser.T__47]:
                self.enterOuterAlt(localctx, 4)
                self.state = 406
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__46 or _la==DMFParser.T__47):
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
            self.state = 417
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__46, DMFParser.T__48]:
                self.enterOuterAlt(localctx, 1)
                self.state = 411
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__46 or _la==DMFParser.T__48):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.RIGHT
                pass
            elif token in [DMFParser.T__44, DMFParser.T__49]:
                self.enterOuterAlt(localctx, 2)
                self.state = 413
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__44 or _la==DMFParser.T__49):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.LEFT
                pass
            elif token in [DMFParser.T__50]:
                self.enterOuterAlt(localctx, 3)
                self.state = 415
                self.match(DMFParser.T__50)
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
            self.state = 433
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,35,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 419
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 420
                self.match(DMFParser.T__51)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 423
                self.match(DMFParser.T__52)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 426
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 427
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__53 or _la==DMFParser.T__54):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 430
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__55 or _la==DMFParser.T__56):
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
            self.state = 439
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__51]:
                self.enterOuterAlt(localctx, 1)
                self.state = 435
                self.match(DMFParser.T__51)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__53, DMFParser.T__54]:
                self.enterOuterAlt(localctx, 2)
                self.state = 437
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__53 or _la==DMFParser.T__54):
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
            self.state = 441
            self.macro_header()
            self.state = 444
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__5, DMFParser.T__7]:
                self.state = 442
                self.compound()
                pass
            elif token in [DMFParser.T__2, DMFParser.T__15, DMFParser.T__19, DMFParser.T__20, DMFParser.T__22, DMFParser.T__23, DMFParser.T__25, DMFParser.T__26, DMFParser.T__34, DMFParser.T__35, DMFParser.T__38, DMFParser.T__39, DMFParser.T__40, DMFParser.T__41, DMFParser.T__42, DMFParser.T__43, DMFParser.T__44, DMFParser.T__45, DMFParser.T__46, DMFParser.T__47, DMFParser.T__57, DMFParser.T__58, DMFParser.T__59, DMFParser.T__60, DMFParser.T__63, DMFParser.T__64, DMFParser.T__65, DMFParser.T__66, DMFParser.T__67, DMFParser.T__68, DMFParser.T__69, DMFParser.T__70, DMFParser.T__71, DMFParser.T__72, DMFParser.T__73, DMFParser.T__74, DMFParser.T__75, DMFParser.T__76, DMFParser.T__77, DMFParser.T__78, DMFParser.T__79, DMFParser.T__80, DMFParser.T__81, DMFParser.T__82, DMFParser.T__83, DMFParser.T__84, DMFParser.T__89, DMFParser.T__107, DMFParser.T__110, DMFParser.T__121, DMFParser.T__122, DMFParser.T__123, DMFParser.T__124, DMFParser.T__125, DMFParser.T__126, DMFParser.T__127, DMFParser.T__128, DMFParser.T__129, DMFParser.T__130, DMFParser.T__131, DMFParser.T__132, DMFParser.INTERACTIVE, DMFParser.NOT, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT, DMFParser.FLOAT, DMFParser.STRING]:
                self.state = 443
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
            self.state = 446
            self.match(DMFParser.T__57)
            self.state = 447
            self.match(DMFParser.T__15)
            self.state = 456
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__19) | (1 << DMFParser.T__20) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__26) | (1 << DMFParser.T__30) | (1 << DMFParser.T__35) | (1 << DMFParser.T__59))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__67 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__110 - 64)))) != 0) or ((((_la - 138)) & ~0x3f) == 0 and ((1 << (_la - 138)) & ((1 << (DMFParser.INTERACTIVE - 138)) | (1 << (DMFParser.ON - 138)) | (1 << (DMFParser.ID - 138)))) != 0):
                self.state = 448
                self.param()
                self.state = 453
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__1:
                    self.state = 449
                    self.match(DMFParser.T__1)
                    self.state = 450
                    self.param()
                    self.state = 455
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 458
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
            self.state = 483
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,41,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 461
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__19 or _la==DMFParser.T__30:
                    self.state = 460
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__19 or _la==DMFParser.T__30):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 463
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 466
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 468
                localctx._INT = self.match(DMFParser.INT)
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 471
                localctx._param_type = self.param_type()
                self.state = 472
                localctx._name = self.name()
                localctx.type=localctx._param_type.type
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 476
                localctx._name = self.name()
                self.state = 477
                self.match(DMFParser.INJECT)
                self.state = 478
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
            self.state = 509
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,47,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 486
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__58:
                    self.state = 485
                    self.match(DMFParser.T__58)


                self.state = 488
                self.match(DMFParser.ON)
                localctx.which="TURN-ON"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 491
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__58:
                    self.state = 490
                    self.match(DMFParser.T__58)


                self.state = 493
                self.match(DMFParser.OFF)
                localctx.which="TURN-OFF"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 495
                self.match(DMFParser.TOGGLE)
                self.state = 497
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,44,self._ctx)
                if la_ == 1:
                    self.state = 496
                    self.match(DMFParser.T__59)


                localctx.which="TOGGLE"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 500
                self.match(DMFParser.T__60)
                self.state = 506
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,46,self._ctx)
                if la_ == 1:
                    self.state = 501
                    self.match(DMFParser.T__61)
                    self.state = 503
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==DMFParser.T__25:
                        self.state = 502
                        self.match(DMFParser.T__25)


                    self.state = 505
                    self.match(DMFParser.T__62)


                localctx.which="REMOVE-FROM-BOARD"
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
            self.state = 567
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,50,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 511
                self.match(DMFParser.T__35)
                localctx.type=Type.DROP
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 513
                self.match(DMFParser.T__63)
                localctx.type=Type.PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 515
                self.match(DMFParser.T__64)
                localctx.type=Type.WELL
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 517
                self.match(DMFParser.T__64)
                self.state = 518
                self.match(DMFParser.T__63)
                localctx.type=Type.WELL_PAD
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 521
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__64:
                    self.state = 520
                    self.match(DMFParser.T__64)


                self.state = 523
                self.match(DMFParser.T__65)
                localctx.type=Type.WELL_GATE
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 525
                self.match(DMFParser.T__66)
                localctx.type=Type.INT
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 527
                self.match(DMFParser.T__67)
                localctx.type=Type.FLOAT
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 529
                self.match(DMFParser.T__20)
                localctx.type=Type.STRING
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 531
                self.match(DMFParser.T__59)
                localctx.type=Type.BINARY_STATE
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 533
                self.match(DMFParser.T__68)
                localctx.type=Type.BINARY_CPT
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 535
                self.match(DMFParser.T__69)
                localctx.type=Type.DELTA
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 537
                self.match(DMFParser.T__70)
                localctx.type=Type.MOTION
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 539
                self.match(DMFParser.T__71)
                localctx.type=Type.DELAY
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 541
                self.match(DMFParser.T__72)
                localctx.type=Type.TIME
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 543
                self.match(DMFParser.T__73)
                localctx.type=Type.TICKS
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 545
                self.match(DMFParser.T__74)
                localctx.type=Type.BOOL
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 547
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__22 or _la==DMFParser.T__23):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.type=Type.DIR
                pass

            elif la_ == 18:
                self.enterOuterAlt(localctx, 18)
                self.state = 549
                self.match(DMFParser.T__75)
                localctx.type=Type.VOLUME
                pass

            elif la_ == 19:
                self.enterOuterAlt(localctx, 19)
                self.state = 551
                self.match(DMFParser.T__26)
                localctx.type=Type.REAGENT
                pass

            elif la_ == 20:
                self.enterOuterAlt(localctx, 20)
                self.state = 553
                self.match(DMFParser.T__76)
                localctx.type=Type.LIQUID
                pass

            elif la_ == 21:
                self.enterOuterAlt(localctx, 21)
                self.state = 555
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__77 or _la==DMFParser.T__78):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 556
                _la = self._input.LA(1)
                if not(((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DMFParser.T__69 - 70)) | (1 << (DMFParser.T__79 - 70)) | (1 << (DMFParser.T__80 - 70)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.type=Type.REL_TEMP
                pass

            elif la_ == 22:
                self.enterOuterAlt(localctx, 22)
                self.state = 558
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__77 or _la==DMFParser.T__78):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 560
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
                if la_ == 1:
                    self.state = 559
                    self.match(DMFParser.T__81)


                localctx.type=Type.ABS_TEMP
                pass

            elif la_ == 23:
                self.enterOuterAlt(localctx, 23)
                self.state = 563
                self.match(DMFParser.T__82)
                localctx.type=Type.HEATER
                pass

            elif la_ == 24:
                self.enterOuterAlt(localctx, 24)
                self.state = 565
                self.match(DMFParser.T__83)
                localctx.type=Type.MAGNET
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
            self.state = 581
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__84, DMFParser.T__85, DMFParser.T__86, DMFParser.T__87, DMFParser.T__88]:
                self.enterOuterAlt(localctx, 1)
                self.state = 569
                _la = self._input.LA(1)
                if not(((((_la - 85)) & ~0x3f) == 0 and ((1 << (_la - 85)) & ((1 << (DMFParser.T__84 - 85)) | (1 << (DMFParser.T__85 - 85)) | (1 << (DMFParser.T__86 - 85)) | (1 << (DMFParser.T__87 - 85)) | (1 << (DMFParser.T__88 - 85)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.sec
                pass
            elif token in [DMFParser.T__89, DMFParser.T__90, DMFParser.T__91]:
                self.enterOuterAlt(localctx, 2)
                self.state = 571
                _la = self._input.LA(1)
                if not(((((_la - 90)) & ~0x3f) == 0 and ((1 << (_la - 90)) & ((1 << (DMFParser.T__89 - 90)) | (1 << (DMFParser.T__90 - 90)) | (1 << (DMFParser.T__91 - 90)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.ms
                pass
            elif token in [DMFParser.T__92, DMFParser.T__93, DMFParser.T__94, DMFParser.T__95, DMFParser.T__96, DMFParser.T__97]:
                self.enterOuterAlt(localctx, 3)
                self.state = 573
                _la = self._input.LA(1)
                if not(((((_la - 93)) & ~0x3f) == 0 and ((1 << (_la - 93)) & ((1 << (DMFParser.T__92 - 93)) | (1 << (DMFParser.T__93 - 93)) | (1 << (DMFParser.T__94 - 93)) | (1 << (DMFParser.T__95 - 93)) | (1 << (DMFParser.T__96 - 93)) | (1 << (DMFParser.T__97 - 93)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.uL
                pass
            elif token in [DMFParser.T__98, DMFParser.T__99, DMFParser.T__100, DMFParser.T__101, DMFParser.T__102, DMFParser.T__103]:
                self.enterOuterAlt(localctx, 4)
                self.state = 575
                _la = self._input.LA(1)
                if not(((((_la - 99)) & ~0x3f) == 0 and ((1 << (_la - 99)) & ((1 << (DMFParser.T__98 - 99)) | (1 << (DMFParser.T__99 - 99)) | (1 << (DMFParser.T__100 - 99)) | (1 << (DMFParser.T__101 - 99)) | (1 << (DMFParser.T__102 - 99)) | (1 << (DMFParser.T__103 - 99)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.mL
                pass
            elif token in [DMFParser.T__73, DMFParser.T__104]:
                self.enterOuterAlt(localctx, 5)
                self.state = 577
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__73 or _la==DMFParser.T__104):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=ticks
                pass
            elif token in [DMFParser.T__35, DMFParser.T__105]:
                self.enterOuterAlt(localctx, 6)
                self.state = 579
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__35 or _la==DMFParser.T__105):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=EnvRelativeUnit.DROP
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
            self.state = 589
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__64]:
                self.enterOuterAlt(localctx, 1)
                self.state = 583
                self.match(DMFParser.T__64)
                localctx.kind=NumberedItem.WELL
                pass
            elif token in [DMFParser.T__82]:
                self.enterOuterAlt(localctx, 2)
                self.state = 585
                self.match(DMFParser.T__82)
                localctx.kind=NumberedItem.HEATER
                pass
            elif token in [DMFParser.T__83]:
                self.enterOuterAlt(localctx, 3)
                self.state = 587
                self.match(DMFParser.T__83)
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
            self.state = 629
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,57,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 591
                self.match(DMFParser.T__106)
                self.state = 592
                self.match(DMFParser.T__63)
                localctx.which="#exit_pad"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 594
                self.match(DMFParser.T__65)
                localctx.which="gate"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 596
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__22 or _la==DMFParser.T__23):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="direction"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 601
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__51]:
                    self.state = 598
                    self.match(DMFParser.T__51)
                    pass
                elif token in [DMFParser.T__107]:
                    self.state = 599
                    self.match(DMFParser.T__107)
                    self.state = 600
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__108 or _la==DMFParser.T__109):
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
                self.state = 608
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__53]:
                    self.state = 604
                    self.match(DMFParser.T__53)
                    pass
                elif token in [DMFParser.T__54]:
                    self.state = 605
                    self.match(DMFParser.T__54)
                    pass
                elif token in [DMFParser.T__110]:
                    self.state = 606
                    self.match(DMFParser.T__110)
                    self.state = 607
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__108 or _la==DMFParser.T__109):
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
                self.state = 611
                self.match(DMFParser.T__106)
                self.state = 612
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__22 or _la==DMFParser.T__23):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#exit_dir"
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 614
                self.match(DMFParser.T__111)
                self.state = 615
                self.match(DMFParser.T__112)
                localctx.which="#remaining_capacity"
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 617
                self.match(DMFParser.T__113)
                self.state = 619
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,55,self._ctx)
                if la_ == 1:
                    self.state = 618
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__77 or _la==DMFParser.T__78):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                localctx.which="#target_temperature"
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 623
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__114:
                    self.state = 622
                    self.match(DMFParser.T__114)


                self.state = 625
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__77 or _la==DMFParser.T__78):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#current_temperature"
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 627
                localctx.n = self._input.LT(1)
                _la = self._input.LA(1)
                if not(((((_la - 27)) & ~0x3f) == 0 and ((1 << (_la - 27)) & ((1 << (DMFParser.T__26 - 27)) | (1 << (DMFParser.T__35 - 27)) | (1 << (DMFParser.T__63 - 27)) | (1 << (DMFParser.T__64 - 27)) | (1 << (DMFParser.T__75 - 27)) | (1 << (DMFParser.T__82 - 27)) | (1 << (DMFParser.T__83 - 27)))) != 0) or _la==DMFParser.ID):
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
            self.state = 643
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__115]:
                self.enterOuterAlt(localctx, 1)
                self.state = 631
                self.match(DMFParser.T__115)
                localctx.which=Rel.EQ
                pass
            elif token in [DMFParser.T__116]:
                self.enterOuterAlt(localctx, 2)
                self.state = 633
                self.match(DMFParser.T__116)
                localctx.which=Rel.NE
                pass
            elif token in [DMFParser.T__117]:
                self.enterOuterAlt(localctx, 3)
                self.state = 635
                self.match(DMFParser.T__117)
                localctx.which=Rel.LT
                pass
            elif token in [DMFParser.T__118]:
                self.enterOuterAlt(localctx, 4)
                self.state = 637
                self.match(DMFParser.T__118)
                localctx.which=Rel.LE
                pass
            elif token in [DMFParser.T__119]:
                self.enterOuterAlt(localctx, 5)
                self.state = 639
                self.match(DMFParser.T__119)
                localctx.which=Rel.GT
                pass
            elif token in [DMFParser.T__120]:
                self.enterOuterAlt(localctx, 6)
                self.state = 641
                self.match(DMFParser.T__120)
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
        self.enterRule(localctx, 46, self.RULE_bool_val)
        self._la = 0 # Token type
        try:
            self.state = 649
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__121, DMFParser.T__122, DMFParser.T__123, DMFParser.T__124, DMFParser.T__125, DMFParser.T__126]:
                self.enterOuterAlt(localctx, 1)
                self.state = 645
                _la = self._input.LA(1)
                if not(((((_la - 122)) & ~0x3f) == 0 and ((1 << (_la - 122)) & ((1 << (DMFParser.T__121 - 122)) | (1 << (DMFParser.T__122 - 122)) | (1 << (DMFParser.T__123 - 122)) | (1 << (DMFParser.T__124 - 122)) | (1 << (DMFParser.T__125 - 122)) | (1 << (DMFParser.T__126 - 122)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.val=True
                pass
            elif token in [DMFParser.T__127, DMFParser.T__128, DMFParser.T__129, DMFParser.T__130, DMFParser.T__131, DMFParser.T__132]:
                self.enterOuterAlt(localctx, 2)
                self.state = 647
                _la = self._input.LA(1)
                if not(((((_la - 128)) & ~0x3f) == 0 and ((1 << (_la - 128)) & ((1 << (DMFParser.T__127 - 128)) | (1 << (DMFParser.T__128 - 128)) | (1 << (DMFParser.T__129 - 128)) | (1 << (DMFParser.T__130 - 128)) | (1 << (DMFParser.T__131 - 128)) | (1 << (DMFParser.T__132 - 128)))) != 0)):
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
        self.enterRule(localctx, 48, self.RULE_name)
        try:
            self.state = 659
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.INTERACTIVE, DMFParser.ON]:
                self.enterOuterAlt(localctx, 1)
                self.state = 651
                localctx._multi_word_name = self.multi_word_name()
                localctx.val=localctx._multi_word_name.val
                pass
            elif token in [DMFParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 654
                localctx._ID = self.match(DMFParser.ID)
                localctx.val=(None if localctx._ID is None else localctx._ID.text)
                pass
            elif token in [DMFParser.T__69, DMFParser.T__79, DMFParser.T__80, DMFParser.T__81, DMFParser.T__84, DMFParser.T__89, DMFParser.T__107, DMFParser.T__110]:
                self.enterOuterAlt(localctx, 3)
                self.state = 656
                localctx._kwd_names = self.kwd_names()
                localctx.val=(None if localctx._kwd_names is None else self._input.getText(localctx._kwd_names.start,localctx._kwd_names.stop))
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
        self.enterRule(localctx, 50, self.RULE_multi_word_name)
        self._la = 0 # Token type
        try:
            self.state = 673
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,62,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 661
                self.match(DMFParser.ON)
                self.state = 663
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__25:
                    self.state = 662
                    self.match(DMFParser.T__25)


                self.state = 665
                self.match(DMFParser.T__62)
                localctx.val="on board"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 667
                self.match(DMFParser.INTERACTIVE)
                self.state = 668
                self.match(DMFParser.T__26)
                localctx.val="interactive reagent"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 670
                self.match(DMFParser.INTERACTIVE)
                self.state = 671
                self.match(DMFParser.T__75)
                localctx.val="interactive volume"
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
        self.enterRule(localctx, 52, self.RULE_kwd_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 675
            _la = self._input.LA(1)
            if not(((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DMFParser.T__69 - 70)) | (1 << (DMFParser.T__79 - 70)) | (1 << (DMFParser.T__80 - 70)) | (1 << (DMFParser.T__81 - 70)) | (1 << (DMFParser.T__84 - 70)) | (1 << (DMFParser.T__89 - 70)) | (1 << (DMFParser.T__107 - 70)) | (1 << (DMFParser.T__110 - 70)))) != 0)):
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
        self.enterRule(localctx, 54, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 677
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
         




