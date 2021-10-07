# Generated from DMF.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


from mpam.types import Dir, OnOff, Turn, ticks
from langsup.type_supp import Type, Rel
from quantities import SI


from mpam.types import Dir 


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\u0082")
        buf.write("\u01af\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\3\2\7\2,\n\2\f\2\16\2/\13\2\3\2\3")
        buf.write("\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\5\3=\n\3\3")
        buf.write("\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5")
        buf.write("\3\5\3\5\3\5\3\5\3\5\7\5R\n\5\f\5\16\5U\13\5\3\5\3\5\5")
        buf.write("\5Y\n\5\3\5\3\5\3\5\3\5\5\5_\n\5\3\6\3\6\7\6c\n\6\f\6")
        buf.write("\16\6f\13\6\3\6\3\6\3\6\7\6k\n\6\f\6\16\6n\13\6\3\6\5")
        buf.write("\6q\n\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7\u008a")
        buf.write("\n\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7\u0097")
        buf.write("\n\7\3\7\3\7\3\7\5\7\u009c\n\7\3\7\3\7\3\7\5\7\u00a1\n")
        buf.write("\7\3\7\5\7\u00a4\n\7\3\7\5\7\u00a7\n\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\7\7\u00b3\n\7\f\7\16\7\u00b6")
        buf.write("\13\7\5\7\u00b8\n\7\3\7\3\7\3\7\3\7\3\7\5\7\u00bf\n\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\7\7\u00f5")
        buf.write("\n\7\f\7\16\7\u00f8\13\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3")
        buf.write("\b\3\b\3\b\3\b\3\b\5\b\u0106\n\b\3\t\3\t\3\t\3\t\3\t\3")
        buf.write("\t\5\t\u010e\n\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\5\n\u011e\n\n\3\13\3\13\3\13\3\13\5")
        buf.write("\13\u0124\n\13\3\f\3\f\3\f\5\f\u0129\n\f\3\r\3\r\3\r\3")
        buf.write("\r\3\r\7\r\u0130\n\r\f\r\16\r\u0133\13\r\5\r\u0135\n\r")
        buf.write("\3\r\3\r\3\16\3\16\3\16\3\16\5\16\u013d\n\16\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\5\16\u0145\n\16\3\17\3\17\3\17\3")
        buf.write("\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17")
        buf.write("\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17")
        buf.write("\3\17\3\17\5\17\u0162\n\17\3\20\3\20\3\20\3\20\3\20\3")
        buf.write("\20\3\20\3\20\3\20\3\20\5\20\u016e\n\20\3\21\3\21\3\21")
        buf.write("\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21")
        buf.write("\3\21\3\21\5\21\u0180\n\21\3\21\3\21\3\21\3\21\3\21\5")
        buf.write("\21\u0187\n\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21")
        buf.write("\3\21\3\21\5\21\u0193\n\21\3\22\3\22\3\22\3\22\3\22\3")
        buf.write("\22\3\22\3\22\3\22\3\22\3\22\3\22\5\22\u01a1\n\22\3\23")
        buf.write("\3\23\3\23\3\23\5\23\u01a7\n\23\3\24\3\24\5\24\u01ab\n")
        buf.write("\24\3\25\3\25\3\25\2\3\f\26\2\4\6\b\n\f\16\20\22\24\26")
        buf.write("\30\32\34\36 \"$&(\2\32\3\2\36\37\3\2wx\3\2\17\20\4\2")
        buf.write("ttvv\4\2qqyy\3\2\21\22\3\2\24\25\3\2&\'\3\2()\3\2*+\3")
        buf.write("\2,-\4\2,,..\4\2**//\3\2\63\64\3\2\65\66\3\2AE\3\2FH\3")
        buf.write("\2IN\3\2OT\4\2??UU\3\2[\\\3\2ej\3\2kp\6\2AAFFZZ]]\2\u0207")
        buf.write("\2-\3\2\2\2\4<\3\2\2\2\6>\3\2\2\2\b^\3\2\2\2\np\3\2\2")
        buf.write("\2\f\u00be\3\2\2\2\16\u0105\3\2\2\2\20\u010d\3\2\2\2\22")
        buf.write("\u011d\3\2\2\2\24\u0123\3\2\2\2\26\u0125\3\2\2\2\30\u012a")
        buf.write("\3\2\2\2\32\u0144\3\2\2\2\34\u0161\3\2\2\2\36\u016d\3")
        buf.write("\2\2\2 \u0192\3\2\2\2\"\u01a0\3\2\2\2$\u01a6\3\2\2\2&")
        buf.write("\u01aa\3\2\2\2(\u01ac\3\2\2\2*,\5\b\5\2+*\3\2\2\2,/\3")
        buf.write("\2\2\2-+\3\2\2\2-.\3\2\2\2.\60\3\2\2\2/-\3\2\2\2\60\61")
        buf.write("\7\2\2\3\61\3\3\2\2\2\62\63\5\n\6\2\63\64\7\2\2\3\64=")
        buf.write("\3\2\2\2\65\66\5\6\4\2\66\67\7\2\2\3\67=\3\2\2\289\5\f")
        buf.write("\7\29:\7\2\2\3:=\3\2\2\2;=\7\2\2\3<\62\3\2\2\2<\65\3\2")
        buf.write("\2\2<8\3\2\2\2<;\3\2\2\2=\5\3\2\2\2>?\5&\24\2?@\7r\2\2")
        buf.write("@A\5\f\7\2A\7\3\2\2\2BC\5\6\4\2CD\7z\2\2D_\3\2\2\2EF\7")
        buf.write("\3\2\2FG\5\f\7\2GH\7z\2\2H_\3\2\2\2IJ\7\4\2\2JK\5\f\7")
        buf.write("\2KS\5\n\6\2LM\7\5\2\2MN\7\4\2\2NO\5\f\7\2OP\5\n\6\2P")
        buf.write("R\3\2\2\2QL\3\2\2\2RU\3\2\2\2SQ\3\2\2\2ST\3\2\2\2TX\3")
        buf.write("\2\2\2US\3\2\2\2VW\7\5\2\2WY\5\n\6\2XV\3\2\2\2XY\3\2\2")
        buf.write("\2Y_\3\2\2\2Z[\5\f\7\2[\\\7z\2\2\\_\3\2\2\2]_\5\n\6\2")
        buf.write("^B\3\2\2\2^E\3\2\2\2^I\3\2\2\2^Z\3\2\2\2^]\3\2\2\2_\t")
        buf.write("\3\2\2\2`d\7\6\2\2ac\5\b\5\2ba\3\2\2\2cf\3\2\2\2db\3\2")
        buf.write("\2\2de\3\2\2\2eg\3\2\2\2fd\3\2\2\2gq\7\7\2\2hl\7\b\2\2")
        buf.write("ik\5\b\5\2ji\3\2\2\2kn\3\2\2\2lj\3\2\2\2lm\3\2\2\2mo\3")
        buf.write("\2\2\2nl\3\2\2\2oq\7\t\2\2p`\3\2\2\2ph\3\2\2\2q\13\3\2")
        buf.write("\2\2rs\b\7\1\2st\7\n\2\2tu\5\f\7\2uv\7\13\2\2v\u00bf\3")
        buf.write("\2\2\2wx\7\n\2\2xy\5\f\7\2yz\7\f\2\2z{\5\f\7\2{|\7\13")
        buf.write("\2\2|\u00bf\3\2\2\2}~\7y\2\2~\u00bf\5\f\7&\177\u0080\7")
        buf.write("}\2\2\u0080\u00bf\5\22\n\2\u0081\u0082\7\26\2\2\u0082")
        buf.write("\u00bf\5\f\7\31\u0083\u0084\5\16\b\2\u0084\u0085\5\f\7")
        buf.write("\26\u0085\u00bf\3\2\2\2\u0086\u00bf\5\16\b\2\u0087\u0089")
        buf.write("\7\31\2\2\u0088\u008a\5\24\13\2\u0089\u0088\3\2\2\2\u0089")
        buf.write("\u008a\3\2\2\2\u008a\u008b\3\2\2\2\u008b\u00bf\5\f\7\24")
        buf.write("\u008c\u008d\7\3\2\2\u008d\u00bf\5\f\7\23\u008e\u008f")
        buf.write("\7\32\2\2\u008f\u0090\7\33\2\2\u0090\u00bf\5\f\7\22\u0091")
        buf.write("\u0092\7\21\2\2\u0092\u0093\t\2\2\2\u0093\u00bf\5\f\7")
        buf.write("\20\u0094\u00bf\5\26\f\2\u0095\u0097\7 \2\2\u0096\u0095")
        buf.write("\3\2\2\2\u0096\u0097\3\2\2\2\u0097\u0098\3\2\2\2\u0098")
        buf.write("\u00bf\t\3\2\2\u0099\u009b\7{\2\2\u009a\u009c\7!\2\2\u009b")
        buf.write("\u009a\3\2\2\2\u009b\u009c\3\2\2\2\u009c\u00bf\3\2\2\2")
        buf.write("\u009d\u00a3\7\"\2\2\u009e\u00a0\7#\2\2\u009f\u00a1\7")
        buf.write("$\2\2\u00a0\u009f\3\2\2\2\u00a0\u00a1\3\2\2\2\u00a1\u00a2")
        buf.write("\3\2\2\2\u00a2\u00a4\7%\2\2\u00a3\u009e\3\2\2\2\u00a3")
        buf.write("\u00a4\3\2\2\2\u00a4\u00bf\3\2\2\2\u00a5\u00a7\7$\2\2")
        buf.write("\u00a6\u00a5\3\2\2\2\u00a6\u00a7\3\2\2\2\u00a7\u00a8\3")
        buf.write("\2\2\2\u00a8\u00bf\5\34\17\2\u00a9\u00aa\5\34\17\2\u00aa")
        buf.write("\u00ab\7}\2\2\u00ab\u00bf\3\2\2\2\u00ac\u00bf\5$\23\2")
        buf.write("\u00ad\u00ae\5&\24\2\u00ae\u00b7\7\n\2\2\u00af\u00b4\5")
        buf.write("\f\7\2\u00b0\u00b1\7\f\2\2\u00b1\u00b3\5\f\7\2\u00b2\u00b0")
        buf.write("\3\2\2\2\u00b3\u00b6\3\2\2\2\u00b4\u00b2\3\2\2\2\u00b4")
        buf.write("\u00b5\3\2\2\2\u00b5\u00b8\3\2\2\2\u00b6\u00b4\3\2\2\2")
        buf.write("\u00b7\u00af\3\2\2\2\u00b7\u00b8\3\2\2\2\u00b8\u00b9\3")
        buf.write("\2\2\2\u00b9\u00ba\7\13\2\2\u00ba\u00bf\3\2\2\2\u00bb")
        buf.write("\u00bf\5&\24\2\u00bc\u00bf\7}\2\2\u00bd\u00bf\7~\2\2\u00be")
        buf.write("r\3\2\2\2\u00bew\3\2\2\2\u00be}\3\2\2\2\u00be\177\3\2")
        buf.write("\2\2\u00be\u0081\3\2\2\2\u00be\u0083\3\2\2\2\u00be\u0086")
        buf.write("\3\2\2\2\u00be\u0087\3\2\2\2\u00be\u008c\3\2\2\2\u00be")
        buf.write("\u008e\3\2\2\2\u00be\u0091\3\2\2\2\u00be\u0094\3\2\2\2")
        buf.write("\u00be\u0096\3\2\2\2\u00be\u0099\3\2\2\2\u00be\u009d\3")
        buf.write("\2\2\2\u00be\u00a6\3\2\2\2\u00be\u00a9\3\2\2\2\u00be\u00ac")
        buf.write("\3\2\2\2\u00be\u00ad\3\2\2\2\u00be\u00bb\3\2\2\2\u00be")
        buf.write("\u00bc\3\2\2\2\u00be\u00bd\3\2\2\2\u00bf\u00f6\3\2\2\2")
        buf.write("\u00c0\u00c1\f\"\2\2\u00c1\u00c2\7\16\2\2\u00c2\u00c3")
        buf.write("\t\4\2\2\u00c3\u00f5\5\f\7#\u00c4\u00c5\f\35\2\2\u00c5")
        buf.write("\u00c6\t\5\2\2\u00c6\u00f5\5\f\7\36\u00c7\u00c8\f\34\2")
        buf.write("\2\u00c8\u00c9\t\6\2\2\u00c9\u00f5\5\f\7\35\u00ca\u00cb")
        buf.write("\f\33\2\2\u00cb\u00cc\5\"\22\2\u00cc\u00cd\5\f\7\34\u00cd")
        buf.write("\u00f5\3\2\2\2\u00ce\u00cf\f\30\2\2\u00cf\u00d0\7\27\2")
        buf.write("\2\u00d0\u00f5\5\f\7\31\u00d1\u00d2\f\27\2\2\u00d2\u00d3")
        buf.write("\7\30\2\2\u00d3\u00f5\5\f\7\30\u00d4\u00d5\f\17\2\2\u00d5")
        buf.write("\u00d6\7u\2\2\u00d6\u00f5\5\f\7\20\u00d7\u00d8\f\16\2")
        buf.write("\2\u00d8\u00d9\7\4\2\2\u00d9\u00da\5\f\7\2\u00da\u00db")
        buf.write("\7\5\2\2\u00db\u00dc\5\f\7\17\u00dc\u00f5\3\2\2\2\u00dd")
        buf.write("\u00de\f%\2\2\u00de\u00f5\5\16\b\2\u00df\u00e0\f$\2\2")
        buf.write("\u00e0\u00e1\7s\2\2\u00e1\u00f5\5 \21\2\u00e2\u00e3\f")
        buf.write("#\2\2\u00e3\u00e4\7\r\2\2\u00e4\u00f5\5\20\t\2\u00e5\u00e6")
        buf.write("\f \2\2\u00e6\u00f5\5\22\n\2\u00e7\u00e8\f\37\2\2\u00e8")
        buf.write("\u00f5\5\36\20\2\u00e9\u00ea\f\36\2\2\u00ea\u00f5\t\7")
        buf.write("\2\2\u00eb\u00ec\f\32\2\2\u00ec\u00ed\7\23\2\2\u00ed\u00ee")
        buf.write("\t\b\2\2\u00ee\u00f5\5 \21\2\u00ef\u00f0\f\21\2\2\u00f0")
        buf.write("\u00f1\7\34\2\2\u00f1\u00f2\5\f\7\2\u00f2\u00f3\7\35\2")
        buf.write("\2\u00f3\u00f5\3\2\2\2\u00f4\u00c0\3\2\2\2\u00f4\u00c4")
        buf.write("\3\2\2\2\u00f4\u00c7\3\2\2\2\u00f4\u00ca\3\2\2\2\u00f4")
        buf.write("\u00ce\3\2\2\2\u00f4\u00d1\3\2\2\2\u00f4\u00d4\3\2\2\2")
        buf.write("\u00f4\u00d7\3\2\2\2\u00f4\u00dd\3\2\2\2\u00f4\u00df\3")
        buf.write("\2\2\2\u00f4\u00e2\3\2\2\2\u00f4\u00e5\3\2\2\2\u00f4\u00e7")
        buf.write("\3\2\2\2\u00f4\u00e9\3\2\2\2\u00f4\u00eb\3\2\2\2\u00f4")
        buf.write("\u00ef\3\2\2\2\u00f5\u00f8\3\2\2\2\u00f6\u00f4\3\2\2\2")
        buf.write("\u00f6\u00f7\3\2\2\2\u00f7\r\3\2\2\2\u00f8\u00f6\3\2\2")
        buf.write("\2\u00f9\u00fa\t\t\2\2\u00fa\u00fb\b\b\1\2\u00fb\u0106")
        buf.write("\b\b\1\2\u00fc\u00fd\t\n\2\2\u00fd\u00fe\b\b\1\2\u00fe")
        buf.write("\u0106\b\b\1\2\u00ff\u0100\t\13\2\2\u0100\u0101\b\b\1")
        buf.write("\2\u0101\u0106\b\b\1\2\u0102\u0103\t\f\2\2\u0103\u0104")
        buf.write("\b\b\1\2\u0104\u0106\b\b\1\2\u0105\u00f9\3\2\2\2\u0105")
        buf.write("\u00fc\3\2\2\2\u0105\u00ff\3\2\2\2\u0105\u0102\3\2\2\2")
        buf.write("\u0106\17\3\2\2\2\u0107\u0108\t\r\2\2\u0108\u010e\b\t")
        buf.write("\1\2\u0109\u010a\t\16\2\2\u010a\u010e\b\t\1\2\u010b\u010c")
        buf.write("\7\60\2\2\u010c\u010e\b\t\1\2\u010d\u0107\3\2\2\2\u010d")
        buf.write("\u0109\3\2\2\2\u010d\u010b\3\2\2\2\u010e\21\3\2\2\2\u010f")
        buf.write("\u0110\6\n\22\3\u0110\u0111\7\61\2\2\u0111\u0112\b\n\1")
        buf.write("\2\u0112\u011e\b\n\1\2\u0113\u0114\7\62\2\2\u0114\u0115")
        buf.write("\b\n\1\2\u0115\u011e\b\n\1\2\u0116\u0117\6\n\23\3\u0117")
        buf.write("\u0118\t\17\2\2\u0118\u0119\b\n\1\2\u0119\u011e\b\n\1")
        buf.write("\2\u011a\u011b\t\20\2\2\u011b\u011c\b\n\1\2\u011c\u011e")
        buf.write("\b\n\1\2\u011d\u010f\3\2\2\2\u011d\u0113\3\2\2\2\u011d")
        buf.write("\u0116\3\2\2\2\u011d\u011a\3\2\2\2\u011e\23\3\2\2\2\u011f")
        buf.write("\u0120\7\61\2\2\u0120\u0124\b\13\1\2\u0121\u0122\t\17")
        buf.write("\2\2\u0122\u0124\b\13\1\2\u0123\u011f\3\2\2\2\u0123\u0121")
        buf.write("\3\2\2\2\u0124\25\3\2\2\2\u0125\u0128\5\30\r\2\u0126\u0129")
        buf.write("\5\n\6\2\u0127\u0129\5\f\7\2\u0128\u0126\3\2\2\2\u0128")
        buf.write("\u0127\3\2\2\2\u0129\27\3\2\2\2\u012a\u012b\7\67\2\2\u012b")
        buf.write("\u0134\7\n\2\2\u012c\u0131\5\32\16\2\u012d\u012e\7\f\2")
        buf.write("\2\u012e\u0130\5\32\16\2\u012f\u012d\3\2\2\2\u0130\u0133")
        buf.write("\3\2\2\2\u0131\u012f\3\2\2\2\u0131\u0132\3\2\2\2\u0132")
        buf.write("\u0135\3\2\2\2\u0133\u0131\3\2\2\2\u0134\u012c\3\2\2\2")
        buf.write("\u0134\u0135\3\2\2\2\u0135\u0136\3\2\2\2\u0136\u0137\7")
        buf.write("\13\2\2\u0137\31\3\2\2\2\u0138\u0139\5\34\17\2\u0139\u013c")
        buf.write("\b\16\1\2\u013a\u013b\7}\2\2\u013b\u013d\b\16\1\2\u013c")
        buf.write("\u013a\3\2\2\2\u013c\u013d\3\2\2\2\u013d\u0145\3\2\2\2")
        buf.write("\u013e\u013f\5&\24\2\u013f\u0140\7u\2\2\u0140\u0141\5")
        buf.write("\34\17\2\u0141\u0142\b\16\1\2\u0142\u0143\b\16\1\2\u0143")
        buf.write("\u0145\3\2\2\2\u0144\u0138\3\2\2\2\u0144\u013e\3\2\2\2")
        buf.write("\u0145\33\3\2\2\2\u0146\u0147\7\21\2\2\u0147\u0162\b\17")
        buf.write("\1\2\u0148\u0149\78\2\2\u0149\u0162\b\17\1\2\u014a\u014b")
        buf.write("\7\32\2\2\u014b\u0162\b\17\1\2\u014c\u014d\7\32\2\2\u014d")
        buf.write("\u014e\78\2\2\u014e\u0162\b\17\1\2\u014f\u0150\79\2\2")
        buf.write("\u0150\u0162\b\17\1\2\u0151\u0152\7!\2\2\u0152\u0162\b")
        buf.write("\17\1\2\u0153\u0154\7:\2\2\u0154\u0162\b\17\1\2\u0155")
        buf.write("\u0156\7;\2\2\u0156\u0162\b\17\1\2\u0157\u0158\7<\2\2")
        buf.write("\u0158\u0162\b\17\1\2\u0159\u015a\7=\2\2\u015a\u0162\b")
        buf.write("\17\1\2\u015b\u015c\7>\2\2\u015c\u0162\b\17\1\2\u015d")
        buf.write("\u015e\7?\2\2\u015e\u0162\b\17\1\2\u015f\u0160\7@\2\2")
        buf.write("\u0160\u0162\b\17\1\2\u0161\u0146\3\2\2\2\u0161\u0148")
        buf.write("\3\2\2\2\u0161\u014a\3\2\2\2\u0161\u014c\3\2\2\2\u0161")
        buf.write("\u014f\3\2\2\2\u0161\u0151\3\2\2\2\u0161\u0153\3\2\2\2")
        buf.write("\u0161\u0155\3\2\2\2\u0161\u0157\3\2\2\2\u0161\u0159\3")
        buf.write("\2\2\2\u0161\u015b\3\2\2\2\u0161\u015d\3\2\2\2\u0161\u015f")
        buf.write("\3\2\2\2\u0162\35\3\2\2\2\u0163\u0164\t\21\2\2\u0164\u016e")
        buf.write("\b\20\1\2\u0165\u0166\t\22\2\2\u0166\u016e\b\20\1\2\u0167")
        buf.write("\u0168\t\23\2\2\u0168\u016e\b\20\1\2\u0169\u016a\t\24")
        buf.write("\2\2\u016a\u016e\b\20\1\2\u016b\u016c\t\25\2\2\u016c\u016e")
        buf.write("\b\20\1\2\u016d\u0163\3\2\2\2\u016d\u0165\3\2\2\2\u016d")
        buf.write("\u0167\3\2\2\2\u016d\u0169\3\2\2\2\u016d\u016b\3\2\2\2")
        buf.write("\u016e\37\3\2\2\2\u016f\u0170\7V\2\2\u0170\u0193\b\21")
        buf.write("\1\2\u0171\u0172\7W\2\2\u0172\u0173\78\2\2\u0173\u0193")
        buf.write("\b\21\1\2\u0174\u0175\7!\2\2\u0175\u0193\b\21\1\2\u0176")
        buf.write("\u0177\7X\2\2\u0177\u0193\b\21\1\2\u0178\u0179\7Y\2\2")
        buf.write("\u0179\u0193\b\21\1\2\u017a\u017b\78\2\2\u017b\u0193\b")
        buf.write("\21\1\2\u017c\u0180\7\61\2\2\u017d\u017e\7Z\2\2\u017e")
        buf.write("\u0180\t\26\2\2\u017f\u017c\3\2\2\2\u017f\u017d\3\2\2")
        buf.write("\2\u0180\u0181\3\2\2\2\u0181\u0193\b\21\1\2\u0182\u0187")
        buf.write("\7\63\2\2\u0183\u0187\7\64\2\2\u0184\u0185\7]\2\2\u0185")
        buf.write("\u0187\t\26\2\2\u0186\u0182\3\2\2\2\u0186\u0183\3\2\2")
        buf.write("\2\u0186\u0184\3\2\2\2\u0187\u0188\3\2\2\2\u0188\u0193")
        buf.write("\b\21\1\2\u0189\u018a\7\32\2\2\u018a\u0193\b\21\1\2\u018b")
        buf.write("\u018c\7W\2\2\u018c\u018d\t\4\2\2\u018d\u0193\b\21\1\2")
        buf.write("\u018e\u018f\7\21\2\2\u018f\u0193\b\21\1\2\u0190\u0191")
        buf.write("\7^\2\2\u0191\u0193\b\21\1\2\u0192\u016f\3\2\2\2\u0192")
        buf.write("\u0171\3\2\2\2\u0192\u0174\3\2\2\2\u0192\u0176\3\2\2\2")
        buf.write("\u0192\u0178\3\2\2\2\u0192\u017a\3\2\2\2\u0192\u017f\3")
        buf.write("\2\2\2\u0192\u0186\3\2\2\2\u0192\u0189\3\2\2\2\u0192\u018b")
        buf.write("\3\2\2\2\u0192\u018e\3\2\2\2\u0192\u0190\3\2\2\2\u0193")
        buf.write("!\3\2\2\2\u0194\u0195\7_\2\2\u0195\u01a1\b\22\1\2\u0196")
        buf.write("\u0197\7`\2\2\u0197\u01a1\b\22\1\2\u0198\u0199\7a\2\2")
        buf.write("\u0199\u01a1\b\22\1\2\u019a\u019b\7b\2\2\u019b\u01a1\b")
        buf.write("\22\1\2\u019c\u019d\7c\2\2\u019d\u01a1\b\22\1\2\u019e")
        buf.write("\u019f\7d\2\2\u019f\u01a1\b\22\1\2\u01a0\u0194\3\2\2\2")
        buf.write("\u01a0\u0196\3\2\2\2\u01a0\u0198\3\2\2\2\u01a0\u019a\3")
        buf.write("\2\2\2\u01a0\u019c\3\2\2\2\u01a0\u019e\3\2\2\2\u01a1#")
        buf.write("\3\2\2\2\u01a2\u01a3\t\27\2\2\u01a3\u01a7\b\23\1\2\u01a4")
        buf.write("\u01a5\t\30\2\2\u01a5\u01a7\b\23\1\2\u01a6\u01a2\3\2\2")
        buf.write("\2\u01a6\u01a4\3\2\2\2\u01a7%\3\2\2\2\u01a8\u01ab\7|\2")
        buf.write("\2\u01a9\u01ab\5(\25\2\u01aa\u01a8\3\2\2\2\u01aa\u01a9")
        buf.write("\3\2\2\2\u01ab\'\3\2\2\2\u01ac\u01ad\t\31\2\2\u01ad)\3")
        buf.write("\2\2\2&-<SX^dlp\u0089\u0096\u009b\u00a0\u00a3\u00a6\u00b4")
        buf.write("\u00b7\u00be\u00f4\u00f6\u0105\u010d\u011d\u0123\u0128")
        buf.write("\u0131\u0134\u013c\u0144\u0161\u016d\u017f\u0186\u0192")
        buf.write("\u01a0\u01a6\u01aa")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'pause'", "'if'", "'else'", "'{'", "'}'", 
                     "'[['", "']]'", "'('", "')'", "','", "'turned'", "'in'", 
                     "'dir'", "'direction'", "'drop'", "'drops'", "'has'", 
                     "'a'", "'an'", "'not'", "'and'", "'or'", "'to'", "'well'", 
                     "'#'", "'['", "']'", "'@'", "'at'", "'turn'", "'state'", 
                     "'remove'", "'from'", "'the'", "'board'", "'up'", "'north'", 
                     "'down'", "'south'", "'left'", "'west'", "'right'", 
                     "'east'", "'clockwise'", "'counterclockwise'", "'around'", 
                     "'row'", "'rows'", "'col'", "'column'", "'cols'", "'columns'", 
                     "'macro'", "'pad'", "'int'", "'component'", "'delta'", 
                     "'motion'", "'delay'", "'time'", "'ticks'", "'bool'", 
                     "'s'", "'sec'", "'secs'", "'second'", "'seconds'", 
                     "'ms'", "'millisecond'", "'milliseconds'", "'uL'", 
                     "'ul'", "'microliter'", "'microlitre'", "'microliters'", 
                     "'microlitres'", "'mL'", "'ml'", "'milliliter'", "'millilitre'", 
                     "'milliliters'", "'millilitres'", "'tick'", "'gate'", 
                     "'exit'", "'distance'", "'duration'", "'y'", "'coord'", 
                     "'coordinate'", "'x'", "'magnitude'", "'=='", "'!='", 
                     "'<'", "'<='", "'>'", "'>='", "'True'", "'true'", "'TRUE'", 
                     "'Yes'", "'yes'", "'YES'", "'False'", "'false'", "'FALSE'", 
                     "'No'", "'no'", "'NO'", "'+'", "'='", "''s'", "'/'", 
                     "':'", "'*'", "'off'", "'on'", "'-'", "';'", "'toggle'" ]

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
    RULE_turn = 7
    RULE_rc = 8
    RULE_axis = 9
    RULE_macro_def = 10
    RULE_macro_header = 11
    RULE_param = 12
    RULE_param_type = 13
    RULE_dim_unit = 14
    RULE_attr = 15
    RULE_rel = 16
    RULE_bool_val = 17
    RULE_name = 18
    RULE_kwd_names = 19

    ruleNames =  [ "macro_file", "interactive", "assignment", "stat", "compound", 
                   "expr", "direction", "turn", "rc", "axis", "macro_def", 
                   "macro_header", "param", "param_type", "dim_unit", "attr", 
                   "rel", "bool_val", "name", "kwd_names" ]

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
    ADD=111
    ASSIGN=112
    ATTR=113
    DIV=114
    INJECT=115
    MUL=116
    OFF=117
    ON=118
    SUB=119
    TERMINATOR=120
    TOGGLE=121
    ID=122
    INT=123
    FLOAT=124
    STRING=125
    EOL_COMMENT=126
    COMMENT=127
    WS=128

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
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__14) | (1 << DMFParser.T__19) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__33) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (DMFParser.T__67 - 68)) | (1 << (DMFParser.T__87 - 68)) | (1 << (DMFParser.T__90 - 68)) | (1 << (DMFParser.T__98 - 68)) | (1 << (DMFParser.T__99 - 68)) | (1 << (DMFParser.T__100 - 68)) | (1 << (DMFParser.T__101 - 68)) | (1 << (DMFParser.T__102 - 68)) | (1 << (DMFParser.T__103 - 68)) | (1 << (DMFParser.T__104 - 68)) | (1 << (DMFParser.T__105 - 68)) | (1 << (DMFParser.T__106 - 68)) | (1 << (DMFParser.T__107 - 68)) | (1 << (DMFParser.T__108 - 68)) | (1 << (DMFParser.T__109 - 68)) | (1 << (DMFParser.OFF - 68)) | (1 << (DMFParser.ON - 68)) | (1 << (DMFParser.SUB - 68)) | (1 << (DMFParser.TOGGLE - 68)) | (1 << (DMFParser.ID - 68)) | (1 << (DMFParser.INT - 68)) | (1 << (DMFParser.FLOAT - 68)))) != 0):
                self.state = 40
                self.stat()
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 46
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
            self.state = 58
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 48
                self.compound()
                self.state = 49
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Assignment_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 51
                self.assignment()
                self.state = 52
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 54
                self.expr(0)
                self.state = 55
                self.match(DMFParser.EOF)
                pass

            elif la_ == 4:
                localctx = DMFParser.Empty_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 57
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
            self.state = 60
            localctx.which = self.name()
            self.state = 61
            self.match(DMFParser.ASSIGN)
            self.state = 62
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



    def stat(self):

        localctx = DMFParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_stat)
        self._la = 0 # Token type
        try:
            self.state = 92
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Assign_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 64
                self.assignment()
                self.state = 65
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Pause_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 67
                self.match(DMFParser.T__0)
                self.state = 68
                localctx.duration = self.expr(0)
                self.state = 69
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 3:
                localctx = DMFParser.If_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 71
                self.match(DMFParser.T__1)
                self.state = 72
                localctx._expr = self.expr(0)
                localctx.tests.append(localctx._expr)
                self.state = 73
                localctx._compound = self.compound()
                localctx.bodies.append(localctx._compound)
                self.state = 81
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 74
                        self.match(DMFParser.T__2)
                        self.state = 75
                        self.match(DMFParser.T__1)
                        self.state = 76
                        localctx._expr = self.expr(0)
                        localctx.tests.append(localctx._expr)
                        self.state = 77
                        localctx._compound = self.compound()
                        localctx.bodies.append(localctx._compound) 
                    self.state = 83
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

                self.state = 86
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__2:
                    self.state = 84
                    self.match(DMFParser.T__2)
                    self.state = 85
                    localctx.else_body = self.compound()


                pass

            elif la_ == 4:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 88
                self.expr(0)
                self.state = 89
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 5:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 91
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
            self.state = 110
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__3]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 94
                self.match(DMFParser.T__3)
                self.state = 98
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__14) | (1 << DMFParser.T__19) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__33) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (DMFParser.T__67 - 68)) | (1 << (DMFParser.T__87 - 68)) | (1 << (DMFParser.T__90 - 68)) | (1 << (DMFParser.T__98 - 68)) | (1 << (DMFParser.T__99 - 68)) | (1 << (DMFParser.T__100 - 68)) | (1 << (DMFParser.T__101 - 68)) | (1 << (DMFParser.T__102 - 68)) | (1 << (DMFParser.T__103 - 68)) | (1 << (DMFParser.T__104 - 68)) | (1 << (DMFParser.T__105 - 68)) | (1 << (DMFParser.T__106 - 68)) | (1 << (DMFParser.T__107 - 68)) | (1 << (DMFParser.T__108 - 68)) | (1 << (DMFParser.T__109 - 68)) | (1 << (DMFParser.OFF - 68)) | (1 << (DMFParser.ON - 68)) | (1 << (DMFParser.SUB - 68)) | (1 << (DMFParser.TOGGLE - 68)) | (1 << (DMFParser.ID - 68)) | (1 << (DMFParser.INT - 68)) | (1 << (DMFParser.FLOAT - 68)))) != 0):
                    self.state = 95
                    self.stat()
                    self.state = 100
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 101
                self.match(DMFParser.T__4)
                pass
            elif token in [DMFParser.T__5]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 102
                self.match(DMFParser.T__5)
                self.state = 106
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__14) | (1 << DMFParser.T__19) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__33) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (DMFParser.T__67 - 68)) | (1 << (DMFParser.T__87 - 68)) | (1 << (DMFParser.T__90 - 68)) | (1 << (DMFParser.T__98 - 68)) | (1 << (DMFParser.T__99 - 68)) | (1 << (DMFParser.T__100 - 68)) | (1 << (DMFParser.T__101 - 68)) | (1 << (DMFParser.T__102 - 68)) | (1 << (DMFParser.T__103 - 68)) | (1 << (DMFParser.T__104 - 68)) | (1 << (DMFParser.T__105 - 68)) | (1 << (DMFParser.T__106 - 68)) | (1 << (DMFParser.T__107 - 68)) | (1 << (DMFParser.T__108 - 68)) | (1 << (DMFParser.T__109 - 68)) | (1 << (DMFParser.OFF - 68)) | (1 << (DMFParser.ON - 68)) | (1 << (DMFParser.SUB - 68)) | (1 << (DMFParser.TOGGLE - 68)) | (1 << (DMFParser.ID - 68)) | (1 << (DMFParser.INT - 68)) | (1 << (DMFParser.FLOAT - 68)))) != 0):
                    self.state = 103
                    self.stat()
                    self.state = 108
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 109
                self.match(DMFParser.T__6)
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


    class Not_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

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


    class Remove_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRemove_expr" ):
                listener.enterRemove_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRemove_expr" ):
                listener.exitRemove_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRemove_expr" ):
                return visitor.visitRemove_expr(self)
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


    class Drop_vol_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.amount = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDrop_vol_expr" ):
                listener.enterDrop_vol_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDrop_vol_expr" ):
                listener.exitDrop_vol_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDrop_vol_expr" ):
                return visitor.visitDrop_vol_expr(self)
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
            self.state = 188
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 113
                self.match(DMFParser.T__7)
                self.state = 114
                self.expr(0)
                self.state = 115
                self.match(DMFParser.T__8)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 117
                self.match(DMFParser.T__7)
                self.state = 118
                localctx.x = self.expr(0)
                self.state = 119
                self.match(DMFParser.T__9)
                self.state = 120
                localctx.y = self.expr(0)
                self.state = 121
                self.match(DMFParser.T__8)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 123
                self.match(DMFParser.SUB)
                self.state = 124
                localctx.rhs = self.expr(36)
                pass

            elif la_ == 4:
                localctx = DMFParser.Const_rc_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 125
                localctx._INT = self.match(DMFParser.INT)
                self.state = 126
                self.rc((0 if localctx._INT is None else int(localctx._INT.text)))
                pass

            elif la_ == 5:
                localctx = DMFParser.Not_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 127
                self.match(DMFParser.T__19)
                self.state = 128
                self.expr(23)
                pass

            elif la_ == 6:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 129
                self.direction()
                self.state = 130
                localctx.dist = self.expr(20)
                pass

            elif la_ == 7:
                localctx = DMFParser.Dir_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 132
                self.direction()
                pass

            elif la_ == 8:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 133
                self.match(DMFParser.T__22)
                self.state = 135
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__46) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49))) != 0):
                    self.state = 134
                    self.axis()


                self.state = 137
                localctx.which = self.expr(18)
                pass

            elif la_ == 9:
                localctx = DMFParser.Pause_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 138
                self.match(DMFParser.T__0)
                self.state = 139
                localctx.duration = self.expr(17)
                pass

            elif la_ == 10:
                localctx = DMFParser.Well_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 140
                self.match(DMFParser.T__23)
                self.state = 141
                self.match(DMFParser.T__24)
                self.state = 142
                localctx.which = self.expr(16)
                pass

            elif la_ == 11:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 143
                self.match(DMFParser.T__14)
                self.state = 144
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__27 or _la==DMFParser.T__28):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 145
                localctx.loc = self.expr(14)
                pass

            elif la_ == 12:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 146
                self.macro_def()
                pass

            elif la_ == 13:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 148
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__29:
                    self.state = 147
                    self.match(DMFParser.T__29)


                self.state = 150
                _la = self._input.LA(1)
                if not(_la==DMFParser.OFF or _la==DMFParser.ON):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 14:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 151
                self.match(DMFParser.TOGGLE)
                self.state = 153
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
                if la_ == 1:
                    self.state = 152
                    self.match(DMFParser.T__30)


                pass

            elif la_ == 15:
                localctx = DMFParser.Remove_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 155
                self.match(DMFParser.T__31)
                self.state = 161
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
                if la_ == 1:
                    self.state = 156
                    self.match(DMFParser.T__32)
                    self.state = 158
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==DMFParser.T__33:
                        self.state = 157
                        self.match(DMFParser.T__33)


                    self.state = 160
                    self.match(DMFParser.T__34)


                pass

            elif la_ == 16:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 164
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__33:
                    self.state = 163
                    self.match(DMFParser.T__33)


                self.state = 166
                self.param_type()
                pass

            elif la_ == 17:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 167
                self.param_type()
                self.state = 168
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 18:
                localctx = DMFParser.Bool_const_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 170
                localctx.val = self.bool_val()
                pass

            elif la_ == 19:
                localctx = DMFParser.Function_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 171
                self.name()
                self.state = 172
                self.match(DMFParser.T__7)
                self.state = 181
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__7) | (1 << DMFParser.T__14) | (1 << DMFParser.T__19) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__33) | (1 << DMFParser.T__35) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (DMFParser.T__67 - 68)) | (1 << (DMFParser.T__87 - 68)) | (1 << (DMFParser.T__90 - 68)) | (1 << (DMFParser.T__98 - 68)) | (1 << (DMFParser.T__99 - 68)) | (1 << (DMFParser.T__100 - 68)) | (1 << (DMFParser.T__101 - 68)) | (1 << (DMFParser.T__102 - 68)) | (1 << (DMFParser.T__103 - 68)) | (1 << (DMFParser.T__104 - 68)) | (1 << (DMFParser.T__105 - 68)) | (1 << (DMFParser.T__106 - 68)) | (1 << (DMFParser.T__107 - 68)) | (1 << (DMFParser.T__108 - 68)) | (1 << (DMFParser.T__109 - 68)) | (1 << (DMFParser.OFF - 68)) | (1 << (DMFParser.ON - 68)) | (1 << (DMFParser.SUB - 68)) | (1 << (DMFParser.TOGGLE - 68)) | (1 << (DMFParser.ID - 68)) | (1 << (DMFParser.INT - 68)) | (1 << (DMFParser.FLOAT - 68)))) != 0):
                    self.state = 173
                    localctx._expr = self.expr(0)
                    localctx.args.append(localctx._expr)
                    self.state = 178
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==DMFParser.T__9:
                        self.state = 174
                        self.match(DMFParser.T__9)
                        self.state = 175
                        localctx._expr = self.expr(0)
                        localctx.args.append(localctx._expr)
                        self.state = 180
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 183
                self.match(DMFParser.T__8)
                pass

            elif la_ == 20:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 185
                self.name()
                pass

            elif la_ == 21:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 186
                localctx._INT = self.match(DMFParser.INT)
                pass

            elif la_ == 22:
                localctx = DMFParser.Float_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 187
                self.match(DMFParser.FLOAT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 244
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 242
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.In_dir_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 190
                        if not self.precpred(self._ctx, 32):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 32)")
                        self.state = 191
                        self.match(DMFParser.T__11)
                        self.state = 192
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__12 or _la==DMFParser.T__13):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 193
                        localctx.d = self.expr(33)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 194
                        if not self.precpred(self._ctx, 27):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 27)")
                        self.state = 195
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 196
                        localctx.rhs = self.expr(28)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 197
                        if not self.precpred(self._ctx, 26):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 26)")
                        self.state = 198
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 199
                        localctx.rhs = self.expr(27)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Rel_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 200
                        if not self.precpred(self._ctx, 25):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 25)")
                        self.state = 201
                        self.rel()
                        self.state = 202
                        localctx.rhs = self.expr(26)
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.And_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 204
                        if not self.precpred(self._ctx, 22):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 22)")
                        self.state = 205
                        self.match(DMFParser.T__20)
                        self.state = 206
                        localctx.rhs = self.expr(23)
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Or_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 207
                        if not self.precpred(self._ctx, 21):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 21)")
                        self.state = 208
                        self.match(DMFParser.T__21)
                        self.state = 209
                        localctx.rhs = self.expr(22)
                        pass

                    elif la_ == 7:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 210
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 211
                        self.match(DMFParser.INJECT)
                        self.state = 212
                        localctx.what = self.expr(14)
                        pass

                    elif la_ == 8:
                        localctx = DMFParser.Cond_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.first = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 213
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 214
                        self.match(DMFParser.T__1)
                        self.state = 215
                        localctx.cond = self.expr(0)
                        self.state = 216
                        self.match(DMFParser.T__2)
                        self.state = 217
                        localctx.second = self.expr(13)
                        pass

                    elif la_ == 9:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 219
                        if not self.precpred(self._ctx, 35):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 35)")
                        self.state = 220
                        self.direction()
                        pass

                    elif la_ == 10:
                        localctx = DMFParser.Attr_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 221
                        if not self.precpred(self._ctx, 34):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 34)")
                        self.state = 222
                        self.match(DMFParser.ATTR)
                        self.state = 223
                        self.attr()
                        pass

                    elif la_ == 11:
                        localctx = DMFParser.Turn_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.start_dir = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 224
                        if not self.precpred(self._ctx, 33):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 33)")
                        self.state = 225
                        self.match(DMFParser.T__10)
                        self.state = 226
                        self.turn()
                        pass

                    elif la_ == 12:
                        localctx = DMFParser.N_rc_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 227
                        if not self.precpred(self._ctx, 30):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 30)")
                        self.state = 228
                        self.rc(0)
                        pass

                    elif la_ == 13:
                        localctx = DMFParser.Unit_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 229
                        if not self.precpred(self._ctx, 29):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 29)")
                        self.state = 230
                        self.dim_unit()
                        pass

                    elif la_ == 14:
                        localctx = DMFParser.Drop_vol_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 231
                        if not self.precpred(self._ctx, 28):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 28)")
                        self.state = 232
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__14 or _la==DMFParser.T__15):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        pass

                    elif la_ == 15:
                        localctx = DMFParser.Has_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 233
                        if not self.precpred(self._ctx, 24):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 24)")
                        self.state = 234
                        self.match(DMFParser.T__16)
                        self.state = 235
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__17 or _la==DMFParser.T__18):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 236
                        self.attr()
                        pass

                    elif la_ == 16:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 237
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 238
                        self.match(DMFParser.T__25)
                        self.state = 239
                        localctx.which = self.expr(0)
                        self.state = 240
                        self.match(DMFParser.T__26)
                        pass

             
                self.state = 246
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

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
            self.state = 259
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__35, DMFParser.T__36]:
                self.enterOuterAlt(localctx, 1)
                self.state = 247
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__35 or _la==DMFParser.T__36):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__37, DMFParser.T__38]:
                self.enterOuterAlt(localctx, 2)
                self.state = 250
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__37 or _la==DMFParser.T__38):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__39, DMFParser.T__40]:
                self.enterOuterAlt(localctx, 3)
                self.state = 253
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__39 or _la==DMFParser.T__40):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__41, DMFParser.T__42]:
                self.enterOuterAlt(localctx, 4)
                self.state = 256
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__41 or _la==DMFParser.T__42):
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
        self.enterRule(localctx, 14, self.RULE_turn)
        self._la = 0 # Token type
        try:
            self.state = 267
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__41, DMFParser.T__43]:
                self.enterOuterAlt(localctx, 1)
                self.state = 261
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__41 or _la==DMFParser.T__43):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.RIGHT
                pass
            elif token in [DMFParser.T__39, DMFParser.T__44]:
                self.enterOuterAlt(localctx, 2)
                self.state = 263
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__39 or _la==DMFParser.T__44):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.LEFT
                pass
            elif token in [DMFParser.T__45]:
                self.enterOuterAlt(localctx, 3)
                self.state = 265
                self.match(DMFParser.T__45)
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
        self.enterRule(localctx, 16, self.RULE_rc)
        self._la = 0 # Token type
        try:
            self.state = 283
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 269
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 270
                self.match(DMFParser.T__46)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 273
                self.match(DMFParser.T__47)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 276
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 277
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__48 or _la==DMFParser.T__49):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 280
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__50 or _la==DMFParser.T__51):
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
        self.enterRule(localctx, 18, self.RULE_axis)
        self._la = 0 # Token type
        try:
            self.state = 289
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__46]:
                self.enterOuterAlt(localctx, 1)
                self.state = 285
                self.match(DMFParser.T__46)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__48, DMFParser.T__49]:
                self.enterOuterAlt(localctx, 2)
                self.state = 287
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__48 or _la==DMFParser.T__49):
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
            self.state = 291
            self.macro_header()
            self.state = 294
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__3, DMFParser.T__5]:
                self.state = 292
                self.compound()
                pass
            elif token in [DMFParser.T__0, DMFParser.T__7, DMFParser.T__14, DMFParser.T__19, DMFParser.T__22, DMFParser.T__23, DMFParser.T__29, DMFParser.T__30, DMFParser.T__31, DMFParser.T__33, DMFParser.T__35, DMFParser.T__36, DMFParser.T__37, DMFParser.T__38, DMFParser.T__39, DMFParser.T__40, DMFParser.T__41, DMFParser.T__42, DMFParser.T__52, DMFParser.T__53, DMFParser.T__54, DMFParser.T__55, DMFParser.T__56, DMFParser.T__57, DMFParser.T__58, DMFParser.T__59, DMFParser.T__60, DMFParser.T__61, DMFParser.T__62, DMFParser.T__67, DMFParser.T__87, DMFParser.T__90, DMFParser.T__98, DMFParser.T__99, DMFParser.T__100, DMFParser.T__101, DMFParser.T__102, DMFParser.T__103, DMFParser.T__104, DMFParser.T__105, DMFParser.T__106, DMFParser.T__107, DMFParser.T__108, DMFParser.T__109, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT, DMFParser.FLOAT]:
                self.state = 293
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
            self.state = 296
            self.match(DMFParser.T__52)
            self.state = 297
            self.match(DMFParser.T__7)
            self.state = 306
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__14) | (1 << DMFParser.T__23) | (1 << DMFParser.T__30) | (1 << DMFParser.T__53) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (DMFParser.T__67 - 68)) | (1 << (DMFParser.T__87 - 68)) | (1 << (DMFParser.T__90 - 68)) | (1 << (DMFParser.ID - 68)))) != 0):
                self.state = 298
                self.param()
                self.state = 303
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__9:
                    self.state = 299
                    self.match(DMFParser.T__9)
                    self.state = 300
                    self.param()
                    self.state = 305
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 308
            self.match(DMFParser.T__8)
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
            self.state = 322
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__14, DMFParser.T__23, DMFParser.T__30, DMFParser.T__53, DMFParser.T__54, DMFParser.T__55, DMFParser.T__56, DMFParser.T__57, DMFParser.T__58, DMFParser.T__59, DMFParser.T__60, DMFParser.T__61]:
                self.enterOuterAlt(localctx, 1)
                self.state = 310
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 314
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.INT:
                    self.state = 312
                    localctx._INT = self.match(DMFParser.INT)
                    localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))


                pass
            elif token in [DMFParser.T__62, DMFParser.T__67, DMFParser.T__87, DMFParser.T__90, DMFParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 316
                localctx._name = self.name()
                self.state = 317
                self.match(DMFParser.INJECT)
                self.state = 318
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
            self.state = 351
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 324
                self.match(DMFParser.T__14)
                localctx.type=Type.DROP
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 326
                self.match(DMFParser.T__53)
                localctx.type=Type.PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 328
                self.match(DMFParser.T__23)
                localctx.type=Type.WELL
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 330
                self.match(DMFParser.T__23)
                self.state = 331
                self.match(DMFParser.T__53)
                localctx.type=Type.WELL_PAD
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 333
                self.match(DMFParser.T__54)
                localctx.type=Type.INT
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 335
                self.match(DMFParser.T__30)
                localctx.type=Type.BINARY_STATE
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 337
                self.match(DMFParser.T__55)
                localctx.type=Type.BINARY_CPT
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 339
                self.match(DMFParser.T__56)
                localctx.type=Type.DELTA
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 341
                self.match(DMFParser.T__57)
                localctx.type=Type.MOTION
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 343
                self.match(DMFParser.T__58)
                localctx.type=Type.DELAY
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 345
                self.match(DMFParser.T__59)
                localctx.type=Type.TIME
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 347
                self.match(DMFParser.T__60)
                localctx.type=Type.TICKS
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 349
                self.match(DMFParser.T__61)
                localctx.type=Type.BOOL
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
        self.enterRule(localctx, 28, self.RULE_dim_unit)
        self._la = 0 # Token type
        try:
            self.state = 363
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__62, DMFParser.T__63, DMFParser.T__64, DMFParser.T__65, DMFParser.T__66]:
                self.enterOuterAlt(localctx, 1)
                self.state = 353
                _la = self._input.LA(1)
                if not(((((_la - 63)) & ~0x3f) == 0 and ((1 << (_la - 63)) & ((1 << (DMFParser.T__62 - 63)) | (1 << (DMFParser.T__63 - 63)) | (1 << (DMFParser.T__64 - 63)) | (1 << (DMFParser.T__65 - 63)) | (1 << (DMFParser.T__66 - 63)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.sec
                pass
            elif token in [DMFParser.T__67, DMFParser.T__68, DMFParser.T__69]:
                self.enterOuterAlt(localctx, 2)
                self.state = 355
                _la = self._input.LA(1)
                if not(((((_la - 68)) & ~0x3f) == 0 and ((1 << (_la - 68)) & ((1 << (DMFParser.T__67 - 68)) | (1 << (DMFParser.T__68 - 68)) | (1 << (DMFParser.T__69 - 68)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.ms
                pass
            elif token in [DMFParser.T__70, DMFParser.T__71, DMFParser.T__72, DMFParser.T__73, DMFParser.T__74, DMFParser.T__75]:
                self.enterOuterAlt(localctx, 3)
                self.state = 357
                _la = self._input.LA(1)
                if not(((((_la - 71)) & ~0x3f) == 0 and ((1 << (_la - 71)) & ((1 << (DMFParser.T__70 - 71)) | (1 << (DMFParser.T__71 - 71)) | (1 << (DMFParser.T__72 - 71)) | (1 << (DMFParser.T__73 - 71)) | (1 << (DMFParser.T__74 - 71)) | (1 << (DMFParser.T__75 - 71)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.uL
                pass
            elif token in [DMFParser.T__76, DMFParser.T__77, DMFParser.T__78, DMFParser.T__79, DMFParser.T__80, DMFParser.T__81]:
                self.enterOuterAlt(localctx, 4)
                self.state = 359
                _la = self._input.LA(1)
                if not(((((_la - 77)) & ~0x3f) == 0 and ((1 << (_la - 77)) & ((1 << (DMFParser.T__76 - 77)) | (1 << (DMFParser.T__77 - 77)) | (1 << (DMFParser.T__78 - 77)) | (1 << (DMFParser.T__79 - 77)) | (1 << (DMFParser.T__80 - 77)) | (1 << (DMFParser.T__81 - 77)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.mL
                pass
            elif token in [DMFParser.T__60, DMFParser.T__82]:
                self.enterOuterAlt(localctx, 5)
                self.state = 361
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__60 or _la==DMFParser.T__82):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=ticks
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
        self.enterRule(localctx, 30, self.RULE_attr)
        self._la = 0 # Token type
        try:
            self.state = 400
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 365
                self.match(DMFParser.T__83)
                localctx.which="GATE"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 367
                self.match(DMFParser.T__84)
                self.state = 368
                self.match(DMFParser.T__53)
                localctx.which="EXIT_PAD"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 370
                self.match(DMFParser.T__30)
                localctx.which="STATE"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 372
                self.match(DMFParser.T__85)
                localctx.which="DISTANCE"
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 374
                self.match(DMFParser.T__86)
                localctx.which="DURATION"
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 376
                self.match(DMFParser.T__53)
                localctx.which="PAD"
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 381
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__46]:
                    self.state = 378
                    self.match(DMFParser.T__46)
                    pass
                elif token in [DMFParser.T__87]:
                    self.state = 379
                    self.match(DMFParser.T__87)
                    self.state = 380
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__88 or _la==DMFParser.T__89):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    pass
                else:
                    raise NoViableAltException(self)

                localctx.which="ROW"
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 388
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__48]:
                    self.state = 384
                    self.match(DMFParser.T__48)
                    pass
                elif token in [DMFParser.T__49]:
                    self.state = 385
                    self.match(DMFParser.T__49)
                    pass
                elif token in [DMFParser.T__90]:
                    self.state = 386
                    self.match(DMFParser.T__90)
                    self.state = 387
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__88 or _la==DMFParser.T__89):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    pass
                else:
                    raise NoViableAltException(self)

                localctx.which="COLUMN"
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 391
                self.match(DMFParser.T__23)
                localctx.which="WELL"
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 393
                self.match(DMFParser.T__84)
                self.state = 394
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__12 or _la==DMFParser.T__13):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="EXIT_DIR"
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 396
                self.match(DMFParser.T__14)
                localctx.which="DROP"
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 398
                self.match(DMFParser.T__91)
                localctx.which="MAGNITUDE"
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
        self.enterRule(localctx, 32, self.RULE_rel)
        try:
            self.state = 414
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__92]:
                self.enterOuterAlt(localctx, 1)
                self.state = 402
                self.match(DMFParser.T__92)
                localctx.which=Rel.EQ
                pass
            elif token in [DMFParser.T__93]:
                self.enterOuterAlt(localctx, 2)
                self.state = 404
                self.match(DMFParser.T__93)
                localctx.which=Rel.NE
                pass
            elif token in [DMFParser.T__94]:
                self.enterOuterAlt(localctx, 3)
                self.state = 406
                self.match(DMFParser.T__94)
                localctx.which=Rel.LT
                pass
            elif token in [DMFParser.T__95]:
                self.enterOuterAlt(localctx, 4)
                self.state = 408
                self.match(DMFParser.T__95)
                localctx.which=Rel.LE
                pass
            elif token in [DMFParser.T__96]:
                self.enterOuterAlt(localctx, 5)
                self.state = 410
                self.match(DMFParser.T__96)
                localctx.which=Rel.GT
                pass
            elif token in [DMFParser.T__97]:
                self.enterOuterAlt(localctx, 6)
                self.state = 412
                self.match(DMFParser.T__97)
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
        self.enterRule(localctx, 34, self.RULE_bool_val)
        self._la = 0 # Token type
        try:
            self.state = 420
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__98, DMFParser.T__99, DMFParser.T__100, DMFParser.T__101, DMFParser.T__102, DMFParser.T__103]:
                self.enterOuterAlt(localctx, 1)
                self.state = 416
                _la = self._input.LA(1)
                if not(((((_la - 99)) & ~0x3f) == 0 and ((1 << (_la - 99)) & ((1 << (DMFParser.T__98 - 99)) | (1 << (DMFParser.T__99 - 99)) | (1 << (DMFParser.T__100 - 99)) | (1 << (DMFParser.T__101 - 99)) | (1 << (DMFParser.T__102 - 99)) | (1 << (DMFParser.T__103 - 99)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.val=True
                pass
            elif token in [DMFParser.T__104, DMFParser.T__105, DMFParser.T__106, DMFParser.T__107, DMFParser.T__108, DMFParser.T__109]:
                self.enterOuterAlt(localctx, 2)
                self.state = 418
                _la = self._input.LA(1)
                if not(((((_la - 105)) & ~0x3f) == 0 and ((1 << (_la - 105)) & ((1 << (DMFParser.T__104 - 105)) | (1 << (DMFParser.T__105 - 105)) | (1 << (DMFParser.T__106 - 105)) | (1 << (DMFParser.T__107 - 105)) | (1 << (DMFParser.T__108 - 105)) | (1 << (DMFParser.T__109 - 105)))) != 0)):
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
        self.enterRule(localctx, 36, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 424
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.ID]:
                self.state = 422
                self.match(DMFParser.ID)
                pass
            elif token in [DMFParser.T__62, DMFParser.T__67, DMFParser.T__87, DMFParser.T__90]:
                self.state = 423
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
        self.enterRule(localctx, 38, self.RULE_kwd_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 426
            _la = self._input.LA(1)
            if not(((((_la - 63)) & ~0x3f) == 0 and ((1 << (_la - 63)) & ((1 << (DMFParser.T__62 - 63)) | (1 << (DMFParser.T__67 - 63)) | (1 << (DMFParser.T__87 - 63)) | (1 << (DMFParser.T__90 - 63)))) != 0)):
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
        self._predicates[8] = self.rc_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 32)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 27)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 26)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 25)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 22)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 21)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 35)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 34)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 33)
         

            if predIndex == 11:
                return self.precpred(self._ctx, 30)
         

            if predIndex == 12:
                return self.precpred(self._ctx, 29)
         

            if predIndex == 13:
                return self.precpred(self._ctx, 28)
         

            if predIndex == 14:
                return self.precpred(self._ctx, 24)
         

            if predIndex == 15:
                return self.precpred(self._ctx, 15)
         

    def rc_sempred(self, localctx:RcContext, predIndex:int):
            if predIndex == 16:
                return localctx.n==1
         

            if predIndex == 17:
                return localctx.n==1
         




