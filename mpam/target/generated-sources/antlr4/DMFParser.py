# Generated from DMF.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


from mpam.types import Dir, OnOff, Turn
from langsup.type_supp import Type, Attr, Rel
from quantities import SI


from mpam.types import Dir 


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\u0081")
        buf.write("\u01b2\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\3\2\7\2.\n\2\f\2\16\2\61")
        buf.write("\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\5\3?\n\3\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5")
        buf.write("\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\7\5T\n\5\f\5\16\5W\13")
        buf.write("\5\3\5\3\5\5\5[\n\5\3\5\3\5\3\5\3\5\5\5a\n\5\3\6\3\6\7")
        buf.write("\6e\n\6\f\6\16\6h\13\6\3\6\3\6\3\6\7\6m\n\6\f\6\16\6p")
        buf.write("\13\6\3\6\5\6s\n\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\5\7\u008c\n\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\5\7\u0099\n\7\3\7\3\7\3\7\5\7\u009e\n\7\3\7\3\7")
        buf.write("\3\7\5\7\u00a3\n\7\3\7\5\7\u00a6\n\7\3\7\5\7\u00a9\n\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\7\7\u00b5\n\7")
        buf.write("\f\7\16\7\u00b8\13\7\5\7\u00ba\n\7\3\7\3\7\3\7\3\7\5\7")
        buf.write("\u00c0\n\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\7\7\u00fa\n\7\f\7\16\7\u00fd\13\7\3")
        buf.write("\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\b\u010b")
        buf.write("\n\b\3\t\3\t\3\t\3\t\3\t\3\t\5\t\u0113\n\t\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u0123")
        buf.write("\n\n\3\13\3\13\3\13\3\13\5\13\u0129\n\13\3\f\3\f\3\f\5")
        buf.write("\f\u012e\n\f\3\r\3\r\3\r\3\r\3\r\7\r\u0135\n\r\f\r\16")
        buf.write("\r\u0138\13\r\5\r\u013a\n\r\3\r\3\r\3\16\3\16\3\16\3\16")
        buf.write("\5\16\u0142\n\16\3\16\3\16\3\16\3\16\3\16\3\16\5\16\u014a")
        buf.write("\n\16\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17")
        buf.write("\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17")
        buf.write("\3\17\3\17\3\17\3\17\3\17\3\17\5\17\u0167\n\17\3\20\3")
        buf.write("\20\3\20\3\20\5\20\u016d\n\20\3\21\3\21\3\21\3\21\5\21")
        buf.write("\u0173\n\21\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3")
        buf.write("\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\5\22\u0185\n\22")
        buf.write("\3\22\3\22\3\22\3\22\3\22\5\22\u018c\n\22\3\22\3\22\3")
        buf.write("\22\3\22\3\22\3\22\3\22\3\22\5\22\u0196\n\22\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\23\5\23")
        buf.write("\u01a4\n\23\3\24\3\24\3\24\3\24\5\24\u01aa\n\24\3\25\3")
        buf.write("\25\5\25\u01ae\n\25\3\26\3\26\3\26\2\3\f\27\2\4\6\b\n")
        buf.write("\f\16\20\22\24\26\30\32\34\36 \"$&(*\2\32\3\2 !\3\2vw")
        buf.write("\3\2\17\20\4\2ssuu\4\2ppxx\3\2\21\22\3\2\23\24\3\2\26")
        buf.write("\27\3\2()\3\2*+\3\2,-\3\2./\4\2..\60\60\4\2,,\61\61\3")
        buf.write("\2\65\66\3\2\678\3\2BF\3\2GI\3\2JO\3\2PU\3\2[\\\3\2di")
        buf.write("\3\2jo\6\2BBGGZZ]]\2\u0207\2/\3\2\2\2\4>\3\2\2\2\6@\3")
        buf.write("\2\2\2\b`\3\2\2\2\nr\3\2\2\2\f\u00bf\3\2\2\2\16\u010a")
        buf.write("\3\2\2\2\20\u0112\3\2\2\2\22\u0122\3\2\2\2\24\u0128\3")
        buf.write("\2\2\2\26\u012a\3\2\2\2\30\u012f\3\2\2\2\32\u0149\3\2")
        buf.write("\2\2\34\u0166\3\2\2\2\36\u016c\3\2\2\2 \u0172\3\2\2\2")
        buf.write("\"\u0195\3\2\2\2$\u01a3\3\2\2\2&\u01a9\3\2\2\2(\u01ad")
        buf.write("\3\2\2\2*\u01af\3\2\2\2,.\5\b\5\2-,\3\2\2\2.\61\3\2\2")
        buf.write("\2/-\3\2\2\2/\60\3\2\2\2\60\62\3\2\2\2\61/\3\2\2\2\62")
        buf.write("\63\7\2\2\3\63\3\3\2\2\2\64\65\5\n\6\2\65\66\7\2\2\3\66")
        buf.write("?\3\2\2\2\678\5\6\4\289\7\2\2\39?\3\2\2\2:;\5\f\7\2;<")
        buf.write("\7\2\2\3<?\3\2\2\2=?\7\2\2\3>\64\3\2\2\2>\67\3\2\2\2>")
        buf.write(":\3\2\2\2>=\3\2\2\2?\5\3\2\2\2@A\5(\25\2AB\7q\2\2BC\5")
        buf.write("\f\7\2C\7\3\2\2\2DE\5\6\4\2EF\7y\2\2Fa\3\2\2\2GH\7\3\2")
        buf.write("\2HI\5\f\7\2IJ\7y\2\2Ja\3\2\2\2KL\7\4\2\2LM\5\f\7\2MU")
        buf.write("\5\n\6\2NO\7\5\2\2OP\7\4\2\2PQ\5\f\7\2QR\5\n\6\2RT\3\2")
        buf.write("\2\2SN\3\2\2\2TW\3\2\2\2US\3\2\2\2UV\3\2\2\2VZ\3\2\2\2")
        buf.write("WU\3\2\2\2XY\7\5\2\2Y[\5\n\6\2ZX\3\2\2\2Z[\3\2\2\2[a\3")
        buf.write("\2\2\2\\]\5\f\7\2]^\7y\2\2^a\3\2\2\2_a\5\n\6\2`D\3\2\2")
        buf.write("\2`G\3\2\2\2`K\3\2\2\2`\\\3\2\2\2`_\3\2\2\2a\t\3\2\2\2")
        buf.write("bf\7\6\2\2ce\5\b\5\2dc\3\2\2\2eh\3\2\2\2fd\3\2\2\2fg\3")
        buf.write("\2\2\2gi\3\2\2\2hf\3\2\2\2is\7\7\2\2jn\7\b\2\2km\5\b\5")
        buf.write("\2lk\3\2\2\2mp\3\2\2\2nl\3\2\2\2no\3\2\2\2oq\3\2\2\2p")
        buf.write("n\3\2\2\2qs\7\t\2\2rb\3\2\2\2rj\3\2\2\2s\13\3\2\2\2tu")
        buf.write("\b\7\1\2uv\7\n\2\2vw\5\f\7\2wx\7\13\2\2x\u00c0\3\2\2\2")
        buf.write("yz\7\n\2\2z{\5\f\7\2{|\7\f\2\2|}\5\f\7\2}~\7\13\2\2~\u00c0")
        buf.write("\3\2\2\2\177\u0080\7x\2\2\u0080\u00c0\5\f\7\'\u0081\u0082")
        buf.write("\7|\2\2\u0082\u00c0\5\22\n\2\u0083\u0084\7\30\2\2\u0084")
        buf.write("\u00c0\5\f\7\30\u0085\u0086\5\16\b\2\u0086\u0087\5\f\7")
        buf.write("\25\u0087\u00c0\3\2\2\2\u0088\u00c0\5\16\b\2\u0089\u008b")
        buf.write("\7\33\2\2\u008a\u008c\5\24\13\2\u008b\u008a\3\2\2\2\u008b")
        buf.write("\u008c\3\2\2\2\u008c\u008d\3\2\2\2\u008d\u00c0\5\f\7\23")
        buf.write("\u008e\u008f\7\3\2\2\u008f\u00c0\5\f\7\22\u0090\u0091")
        buf.write("\7\34\2\2\u0091\u0092\7\35\2\2\u0092\u00c0\5\f\7\21\u0093")
        buf.write("\u0094\7\23\2\2\u0094\u0095\t\2\2\2\u0095\u00c0\5\f\7")
        buf.write("\17\u0096\u00c0\5\26\f\2\u0097\u0099\7\"\2\2\u0098\u0097")
        buf.write("\3\2\2\2\u0098\u0099\3\2\2\2\u0099\u009a\3\2\2\2\u009a")
        buf.write("\u00c0\t\3\2\2\u009b\u009d\7z\2\2\u009c\u009e\7#\2\2\u009d")
        buf.write("\u009c\3\2\2\2\u009d\u009e\3\2\2\2\u009e\u00c0\3\2\2\2")
        buf.write("\u009f\u00a5\7$\2\2\u00a0\u00a2\7%\2\2\u00a1\u00a3\7&")
        buf.write("\2\2\u00a2\u00a1\3\2\2\2\u00a2\u00a3\3\2\2\2\u00a3\u00a4")
        buf.write("\3\2\2\2\u00a4\u00a6\7\'\2\2\u00a5\u00a0\3\2\2\2\u00a5")
        buf.write("\u00a6\3\2\2\2\u00a6\u00c0\3\2\2\2\u00a7\u00a9\7&\2\2")
        buf.write("\u00a8\u00a7\3\2\2\2\u00a8\u00a9\3\2\2\2\u00a9\u00aa\3")
        buf.write("\2\2\2\u00aa\u00c0\5\34\17\2\u00ab\u00ac\5\34\17\2\u00ac")
        buf.write("\u00ad\7|\2\2\u00ad\u00c0\3\2\2\2\u00ae\u00c0\5&\24\2")
        buf.write("\u00af\u00b0\5(\25\2\u00b0\u00b9\7\n\2\2\u00b1\u00b6\5")
        buf.write("\f\7\2\u00b2\u00b3\7\f\2\2\u00b3\u00b5\5\f\7\2\u00b4\u00b2")
        buf.write("\3\2\2\2\u00b5\u00b8\3\2\2\2\u00b6\u00b4\3\2\2\2\u00b6")
        buf.write("\u00b7\3\2\2\2\u00b7\u00ba\3\2\2\2\u00b8\u00b6\3\2\2\2")
        buf.write("\u00b9\u00b1\3\2\2\2\u00b9\u00ba\3\2\2\2\u00ba\u00bb\3")
        buf.write("\2\2\2\u00bb\u00bc\7\13\2\2\u00bc\u00c0\3\2\2\2\u00bd")
        buf.write("\u00c0\5(\25\2\u00be\u00c0\7|\2\2\u00bft\3\2\2\2\u00bf")
        buf.write("y\3\2\2\2\u00bf\177\3\2\2\2\u00bf\u0081\3\2\2\2\u00bf")
        buf.write("\u0083\3\2\2\2\u00bf\u0085\3\2\2\2\u00bf\u0088\3\2\2\2")
        buf.write("\u00bf\u0089\3\2\2\2\u00bf\u008e\3\2\2\2\u00bf\u0090\3")
        buf.write("\2\2\2\u00bf\u0093\3\2\2\2\u00bf\u0096\3\2\2\2\u00bf\u0098")
        buf.write("\3\2\2\2\u00bf\u009b\3\2\2\2\u00bf\u009f\3\2\2\2\u00bf")
        buf.write("\u00a8\3\2\2\2\u00bf\u00ab\3\2\2\2\u00bf\u00ae\3\2\2\2")
        buf.write("\u00bf\u00af\3\2\2\2\u00bf\u00bd\3\2\2\2\u00bf\u00be\3")
        buf.write("\2\2\2\u00c0\u00fb\3\2\2\2\u00c1\u00c2\f#\2\2\u00c2\u00c3")
        buf.write("\7\16\2\2\u00c3\u00c4\t\4\2\2\u00c4\u00fa\5\f\7$\u00c5")
        buf.write("\u00c6\f\34\2\2\u00c6\u00c7\t\5\2\2\u00c7\u00fa\5\f\7")
        buf.write("\35\u00c8\u00c9\f\33\2\2\u00c9\u00ca\t\6\2\2\u00ca\u00fa")
        buf.write("\5\f\7\34\u00cb\u00cc\f\32\2\2\u00cc\u00cd\5$\23\2\u00cd")
        buf.write("\u00ce\5\f\7\33\u00ce\u00fa\3\2\2\2\u00cf\u00d0\f\27\2")
        buf.write("\2\u00d0\u00d1\7\31\2\2\u00d1\u00fa\5\f\7\30\u00d2\u00d3")
        buf.write("\f\26\2\2\u00d3\u00d4\7\32\2\2\u00d4\u00fa\5\f\7\27\u00d5")
        buf.write("\u00d6\f\16\2\2\u00d6\u00d7\7t\2\2\u00d7\u00fa\5\f\7\17")
        buf.write("\u00d8\u00d9\f\r\2\2\u00d9\u00da\7\4\2\2\u00da\u00db\5")
        buf.write("\f\7\2\u00db\u00dc\7\5\2\2\u00dc\u00dd\5\f\7\16\u00dd")
        buf.write("\u00fa\3\2\2\2\u00de\u00df\f&\2\2\u00df\u00fa\5\16\b\2")
        buf.write("\u00e0\u00e1\f%\2\2\u00e1\u00e2\7r\2\2\u00e2\u00fa\5\"")
        buf.write("\22\2\u00e3\u00e4\f$\2\2\u00e4\u00e5\7\r\2\2\u00e5\u00fa")
        buf.write("\5\20\t\2\u00e6\u00e7\f!\2\2\u00e7\u00fa\5\22\n\2\u00e8")
        buf.write("\u00e9\f \2\2\u00e9\u00fa\5\36\20\2\u00ea\u00eb\f\37\2")
        buf.write("\2\u00eb\u00fa\t\7\2\2\u00ec\u00ed\f\36\2\2\u00ed\u00fa")
        buf.write("\5 \21\2\u00ee\u00ef\f\35\2\2\u00ef\u00fa\t\b\2\2\u00f0")
        buf.write("\u00f1\f\31\2\2\u00f1\u00f2\7\25\2\2\u00f2\u00f3\t\t\2")
        buf.write("\2\u00f3\u00fa\5\"\22\2\u00f4\u00f5\f\20\2\2\u00f5\u00f6")
        buf.write("\7\36\2\2\u00f6\u00f7\5\f\7\2\u00f7\u00f8\7\37\2\2\u00f8")
        buf.write("\u00fa\3\2\2\2\u00f9\u00c1\3\2\2\2\u00f9\u00c5\3\2\2\2")
        buf.write("\u00f9\u00c8\3\2\2\2\u00f9\u00cb\3\2\2\2\u00f9\u00cf\3")
        buf.write("\2\2\2\u00f9\u00d2\3\2\2\2\u00f9\u00d5\3\2\2\2\u00f9\u00d8")
        buf.write("\3\2\2\2\u00f9\u00de\3\2\2\2\u00f9\u00e0\3\2\2\2\u00f9")
        buf.write("\u00e3\3\2\2\2\u00f9\u00e6\3\2\2\2\u00f9\u00e8\3\2\2\2")
        buf.write("\u00f9\u00ea\3\2\2\2\u00f9\u00ec\3\2\2\2\u00f9\u00ee\3")
        buf.write("\2\2\2\u00f9\u00f0\3\2\2\2\u00f9\u00f4\3\2\2\2\u00fa\u00fd")
        buf.write("\3\2\2\2\u00fb\u00f9\3\2\2\2\u00fb\u00fc\3\2\2\2\u00fc")
        buf.write("\r\3\2\2\2\u00fd\u00fb\3\2\2\2\u00fe\u00ff\t\n\2\2\u00ff")
        buf.write("\u0100\b\b\1\2\u0100\u010b\b\b\1\2\u0101\u0102\t\13\2")
        buf.write("\2\u0102\u0103\b\b\1\2\u0103\u010b\b\b\1\2\u0104\u0105")
        buf.write("\t\f\2\2\u0105\u0106\b\b\1\2\u0106\u010b\b\b\1\2\u0107")
        buf.write("\u0108\t\r\2\2\u0108\u0109\b\b\1\2\u0109\u010b\b\b\1\2")
        buf.write("\u010a\u00fe\3\2\2\2\u010a\u0101\3\2\2\2\u010a\u0104\3")
        buf.write("\2\2\2\u010a\u0107\3\2\2\2\u010b\17\3\2\2\2\u010c\u010d")
        buf.write("\t\16\2\2\u010d\u0113\b\t\1\2\u010e\u010f\t\17\2\2\u010f")
        buf.write("\u0113\b\t\1\2\u0110\u0111\7\62\2\2\u0111\u0113\b\t\1")
        buf.write("\2\u0112\u010c\3\2\2\2\u0112\u010e\3\2\2\2\u0112\u0110")
        buf.write("\3\2\2\2\u0113\21\3\2\2\2\u0114\u0115\6\n\24\3\u0115\u0116")
        buf.write("\7\63\2\2\u0116\u0117\b\n\1\2\u0117\u0123\b\n\1\2\u0118")
        buf.write("\u0119\7\64\2\2\u0119\u011a\b\n\1\2\u011a\u0123\b\n\1")
        buf.write("\2\u011b\u011c\6\n\25\3\u011c\u011d\t\20\2\2\u011d\u011e")
        buf.write("\b\n\1\2\u011e\u0123\b\n\1\2\u011f\u0120\t\21\2\2\u0120")
        buf.write("\u0121\b\n\1\2\u0121\u0123\b\n\1\2\u0122\u0114\3\2\2\2")
        buf.write("\u0122\u0118\3\2\2\2\u0122\u011b\3\2\2\2\u0122\u011f\3")
        buf.write("\2\2\2\u0123\23\3\2\2\2\u0124\u0125\7\63\2\2\u0125\u0129")
        buf.write("\b\13\1\2\u0126\u0127\t\20\2\2\u0127\u0129\b\13\1\2\u0128")
        buf.write("\u0124\3\2\2\2\u0128\u0126\3\2\2\2\u0129\25\3\2\2\2\u012a")
        buf.write("\u012d\5\30\r\2\u012b\u012e\5\n\6\2\u012c\u012e\5\f\7")
        buf.write("\2\u012d\u012b\3\2\2\2\u012d\u012c\3\2\2\2\u012e\27\3")
        buf.write("\2\2\2\u012f\u0130\79\2\2\u0130\u0139\7\n\2\2\u0131\u0136")
        buf.write("\5\32\16\2\u0132\u0133\7\f\2\2\u0133\u0135\5\32\16\2\u0134")
        buf.write("\u0132\3\2\2\2\u0135\u0138\3\2\2\2\u0136\u0134\3\2\2\2")
        buf.write("\u0136\u0137\3\2\2\2\u0137\u013a\3\2\2\2\u0138\u0136\3")
        buf.write("\2\2\2\u0139\u0131\3\2\2\2\u0139\u013a\3\2\2\2\u013a\u013b")
        buf.write("\3\2\2\2\u013b\u013c\7\13\2\2\u013c\31\3\2\2\2\u013d\u013e")
        buf.write("\5\34\17\2\u013e\u0141\b\16\1\2\u013f\u0140\7|\2\2\u0140")
        buf.write("\u0142\b\16\1\2\u0141\u013f\3\2\2\2\u0141\u0142\3\2\2")
        buf.write("\2\u0142\u014a\3\2\2\2\u0143\u0144\5(\25\2\u0144\u0145")
        buf.write("\7t\2\2\u0145\u0146\5\34\17\2\u0146\u0147\b\16\1\2\u0147")
        buf.write("\u0148\b\16\1\2\u0148\u014a\3\2\2\2\u0149\u013d\3\2\2")
        buf.write("\2\u0149\u0143\3\2\2\2\u014a\33\3\2\2\2\u014b\u014c\7")
        buf.write("\23\2\2\u014c\u0167\b\17\1\2\u014d\u014e\7:\2\2\u014e")
        buf.write("\u0167\b\17\1\2\u014f\u0150\7\34\2\2\u0150\u0167\b\17")
        buf.write("\1\2\u0151\u0152\7\34\2\2\u0152\u0153\7:\2\2\u0153\u0167")
        buf.write("\b\17\1\2\u0154\u0155\7;\2\2\u0155\u0167\b\17\1\2\u0156")
        buf.write("\u0157\7#\2\2\u0157\u0167\b\17\1\2\u0158\u0159\7<\2\2")
        buf.write("\u0159\u0167\b\17\1\2\u015a\u015b\7=\2\2\u015b\u0167\b")
        buf.write("\17\1\2\u015c\u015d\7>\2\2\u015d\u0167\b\17\1\2\u015e")
        buf.write("\u015f\7?\2\2\u015f\u0167\b\17\1\2\u0160\u0161\7@\2\2")
        buf.write("\u0161\u0167\b\17\1\2\u0162\u0163\7\22\2\2\u0163\u0167")
        buf.write("\b\17\1\2\u0164\u0165\7A\2\2\u0165\u0167\b\17\1\2\u0166")
        buf.write("\u014b\3\2\2\2\u0166\u014d\3\2\2\2\u0166\u014f\3\2\2\2")
        buf.write("\u0166\u0151\3\2\2\2\u0166\u0154\3\2\2\2\u0166\u0156\3")
        buf.write("\2\2\2\u0166\u0158\3\2\2\2\u0166\u015a\3\2\2\2\u0166\u015c")
        buf.write("\3\2\2\2\u0166\u015e\3\2\2\2\u0166\u0160\3\2\2\2\u0166")
        buf.write("\u0162\3\2\2\2\u0166\u0164\3\2\2\2\u0167\35\3\2\2\2\u0168")
        buf.write("\u0169\t\22\2\2\u0169\u016d\b\20\1\2\u016a\u016b\t\23")
        buf.write("\2\2\u016b\u016d\b\20\1\2\u016c\u0168\3\2\2\2\u016c\u016a")
        buf.write("\3\2\2\2\u016d\37\3\2\2\2\u016e\u016f\t\24\2\2\u016f\u0173")
        buf.write("\b\21\1\2\u0170\u0171\t\25\2\2\u0171\u0173\b\21\1\2\u0172")
        buf.write("\u016e\3\2\2\2\u0172\u0170\3\2\2\2\u0173!\3\2\2\2\u0174")
        buf.write("\u0175\7V\2\2\u0175\u0196\b\22\1\2\u0176\u0177\7W\2\2")
        buf.write("\u0177\u0178\7:\2\2\u0178\u0196\b\22\1\2\u0179\u017a\7")
        buf.write("#\2\2\u017a\u0196\b\22\1\2\u017b\u017c\7X\2\2\u017c\u0196")
        buf.write("\b\22\1\2\u017d\u017e\7Y\2\2\u017e\u0196\b\22\1\2\u017f")
        buf.write("\u0180\7:\2\2\u0180\u0196\b\22\1\2\u0181\u0185\7\63\2")
        buf.write("\2\u0182\u0183\7Z\2\2\u0183\u0185\t\26\2\2\u0184\u0181")
        buf.write("\3\2\2\2\u0184\u0182\3\2\2\2\u0185\u0186\3\2\2\2\u0186")
        buf.write("\u0196\b\22\1\2\u0187\u018c\7\65\2\2\u0188\u018c\7\66")
        buf.write("\2\2\u0189\u018a\7]\2\2\u018a\u018c\t\26\2\2\u018b\u0187")
        buf.write("\3\2\2\2\u018b\u0188\3\2\2\2\u018b\u0189\3\2\2\2\u018c")
        buf.write("\u018d\3\2\2\2\u018d\u0196\b\22\1\2\u018e\u018f\7\34\2")
        buf.write("\2\u018f\u0196\b\22\1\2\u0190\u0191\7W\2\2\u0191\u0192")
        buf.write("\t\4\2\2\u0192\u0196\b\22\1\2\u0193\u0194\7\23\2\2\u0194")
        buf.write("\u0196\b\22\1\2\u0195\u0174\3\2\2\2\u0195\u0176\3\2\2")
        buf.write("\2\u0195\u0179\3\2\2\2\u0195\u017b\3\2\2\2\u0195\u017d")
        buf.write("\3\2\2\2\u0195\u017f\3\2\2\2\u0195\u0184\3\2\2\2\u0195")
        buf.write("\u018b\3\2\2\2\u0195\u018e\3\2\2\2\u0195\u0190\3\2\2\2")
        buf.write("\u0195\u0193\3\2\2\2\u0196#\3\2\2\2\u0197\u0198\7^\2\2")
        buf.write("\u0198\u01a4\b\23\1\2\u0199\u019a\7_\2\2\u019a\u01a4\b")
        buf.write("\23\1\2\u019b\u019c\7`\2\2\u019c\u01a4\b\23\1\2\u019d")
        buf.write("\u019e\7a\2\2\u019e\u01a4\b\23\1\2\u019f\u01a0\7b\2\2")
        buf.write("\u01a0\u01a4\b\23\1\2\u01a1\u01a2\7c\2\2\u01a2\u01a4\b")
        buf.write("\23\1\2\u01a3\u0197\3\2\2\2\u01a3\u0199\3\2\2\2\u01a3")
        buf.write("\u019b\3\2\2\2\u01a3\u019d\3\2\2\2\u01a3\u019f\3\2\2\2")
        buf.write("\u01a3\u01a1\3\2\2\2\u01a4%\3\2\2\2\u01a5\u01a6\t\27\2")
        buf.write("\2\u01a6\u01aa\b\24\1\2\u01a7\u01a8\t\30\2\2\u01a8\u01aa")
        buf.write("\b\24\1\2\u01a9\u01a5\3\2\2\2\u01a9\u01a7\3\2\2\2\u01aa")
        buf.write("\'\3\2\2\2\u01ab\u01ae\7{\2\2\u01ac\u01ae\5*\26\2\u01ad")
        buf.write("\u01ab\3\2\2\2\u01ad\u01ac\3\2\2\2\u01ae)\3\2\2\2\u01af")
        buf.write("\u01b0\t\31\2\2\u01b0+\3\2\2\2\'/>UZ`fnr\u008b\u0098\u009d")
        buf.write("\u00a2\u00a5\u00a8\u00b6\u00b9\u00bf\u00f9\u00fb\u010a")
        buf.write("\u0112\u0122\u0128\u012d\u0136\u0139\u0141\u0149\u0166")
        buf.write("\u016c\u0172\u0184\u018b\u0195\u01a3\u01a9\u01ad")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'pause'", "'if'", "'else'", "'{'", "'}'", 
                     "'[['", "']]'", "'('", "')'", "','", "'turned'", "'in'", 
                     "'dir'", "'direction'", "'tick'", "'ticks'", "'drop'", 
                     "'drops'", "'has'", "'a'", "'an'", "'not'", "'and'", 
                     "'or'", "'to'", "'well'", "'#'", "'['", "']'", "'@'", 
                     "'at'", "'turn'", "'state'", "'remove'", "'from'", 
                     "'the'", "'board'", "'up'", "'north'", "'down'", "'south'", 
                     "'left'", "'west'", "'right'", "'east'", "'clockwise'", 
                     "'counterclockwise'", "'around'", "'row'", "'rows'", 
                     "'col'", "'column'", "'cols'", "'columns'", "'macro'", 
                     "'pad'", "'int'", "'component'", "'delta'", "'motion'", 
                     "'delay'", "'time'", "'bool'", "'s'", "'sec'", "'secs'", 
                     "'second'", "'seconds'", "'ms'", "'millisecond'", "'milliseconds'", 
                     "'uL'", "'ul'", "'microliter'", "'microlitre'", "'microliters'", 
                     "'microlitres'", "'mL'", "'ml'", "'milliliter'", "'millilitre'", 
                     "'milliliters'", "'millilitres'", "'gate'", "'exit'", 
                     "'distance'", "'duration'", "'y'", "'coord'", "'coordinate'", 
                     "'x'", "'=='", "'!='", "'<'", "'<='", "'>'", "'>='", 
                     "'True'", "'true'", "'TRUE'", "'Yes'", "'yes'", "'YES'", 
                     "'False'", "'false'", "'FALSE'", "'No'", "'no'", "'NO'", 
                     "'+'", "'='", "''s'", "'/'", "':'", "'*'", "'off'", 
                     "'on'", "'-'", "';'", "'toggle'" ]

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
    RULE_turn = 7
    RULE_rc = 8
    RULE_axis = 9
    RULE_macro_def = 10
    RULE_macro_header = 11
    RULE_param = 12
    RULE_param_type = 13
    RULE_time_unit = 14
    RULE_vol_unit = 15
    RULE_attr = 16
    RULE_rel = 17
    RULE_bool_val = 18
    RULE_name = 19
    RULE_kwd_names = 20

    ruleNames =  [ "macro_file", "interactive", "assignment", "stat", "compound", 
                   "expr", "direction", "turn", "rc", "axis", "macro_def", 
                   "macro_header", "param", "param_type", "time_unit", "vol_unit", 
                   "attr", "rel", "bool_val", "name", "kwd_names" ]

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
    ADD=110
    ASSIGN=111
    ATTR=112
    DIV=113
    INJECT=114
    MUL=115
    OFF=116
    ON=117
    SUB=118
    TERMINATOR=119
    TOGGLE=120
    ID=121
    INT=122
    FLOAT=123
    STRING=124
    EOL_COMMENT=125
    COMMENT=126
    WS=127

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
            self.state = 45
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__21) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__31) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__35) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.T__97 - 64)) | (1 << (DMFParser.T__98 - 64)) | (1 << (DMFParser.T__99 - 64)) | (1 << (DMFParser.T__100 - 64)) | (1 << (DMFParser.T__101 - 64)) | (1 << (DMFParser.T__102 - 64)) | (1 << (DMFParser.T__103 - 64)) | (1 << (DMFParser.T__104 - 64)) | (1 << (DMFParser.T__105 - 64)) | (1 << (DMFParser.T__106 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__108 - 64)) | (1 << (DMFParser.OFF - 64)) | (1 << (DMFParser.ON - 64)) | (1 << (DMFParser.SUB - 64)) | (1 << (DMFParser.TOGGLE - 64)) | (1 << (DMFParser.ID - 64)) | (1 << (DMFParser.INT - 64)))) != 0):
                self.state = 42
                self.stat()
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 48
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
            self.state = 60
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 50
                self.compound()
                self.state = 51
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Assignment_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 53
                self.assignment()
                self.state = 54
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 56
                self.expr(0)
                self.state = 57
                self.match(DMFParser.EOF)
                pass

            elif la_ == 4:
                localctx = DMFParser.Empty_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 59
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
            self.state = 62
            localctx.which = self.name()
            self.state = 63
            self.match(DMFParser.ASSIGN)
            self.state = 64
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
            self.state = 94
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Assign_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 66
                self.assignment()
                self.state = 67
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Pause_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                self.match(DMFParser.T__0)
                self.state = 70
                localctx.duration = self.expr(0)
                self.state = 71
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 3:
                localctx = DMFParser.If_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 73
                self.match(DMFParser.T__1)
                self.state = 74
                localctx._expr = self.expr(0)
                localctx.tests.append(localctx._expr)
                self.state = 75
                localctx._compound = self.compound()
                localctx.bodies.append(localctx._compound)
                self.state = 83
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 76
                        self.match(DMFParser.T__2)
                        self.state = 77
                        self.match(DMFParser.T__1)
                        self.state = 78
                        localctx._expr = self.expr(0)
                        localctx.tests.append(localctx._expr)
                        self.state = 79
                        localctx._compound = self.compound()
                        localctx.bodies.append(localctx._compound) 
                    self.state = 85
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

                self.state = 88
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__2:
                    self.state = 86
                    self.match(DMFParser.T__2)
                    self.state = 87
                    localctx.else_body = self.compound()


                pass

            elif la_ == 4:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 90
                self.expr(0)
                self.state = 91
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 5:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 93
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
            self.state = 112
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__3]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 96
                self.match(DMFParser.T__3)
                self.state = 100
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__21) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__31) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__35) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.T__97 - 64)) | (1 << (DMFParser.T__98 - 64)) | (1 << (DMFParser.T__99 - 64)) | (1 << (DMFParser.T__100 - 64)) | (1 << (DMFParser.T__101 - 64)) | (1 << (DMFParser.T__102 - 64)) | (1 << (DMFParser.T__103 - 64)) | (1 << (DMFParser.T__104 - 64)) | (1 << (DMFParser.T__105 - 64)) | (1 << (DMFParser.T__106 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__108 - 64)) | (1 << (DMFParser.OFF - 64)) | (1 << (DMFParser.ON - 64)) | (1 << (DMFParser.SUB - 64)) | (1 << (DMFParser.TOGGLE - 64)) | (1 << (DMFParser.ID - 64)) | (1 << (DMFParser.INT - 64)))) != 0):
                    self.state = 97
                    self.stat()
                    self.state = 102
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 103
                self.match(DMFParser.T__4)
                pass
            elif token in [DMFParser.T__5]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 104
                self.match(DMFParser.T__5)
                self.state = 108
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__21) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__31) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__35) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.T__97 - 64)) | (1 << (DMFParser.T__98 - 64)) | (1 << (DMFParser.T__99 - 64)) | (1 << (DMFParser.T__100 - 64)) | (1 << (DMFParser.T__101 - 64)) | (1 << (DMFParser.T__102 - 64)) | (1 << (DMFParser.T__103 - 64)) | (1 << (DMFParser.T__104 - 64)) | (1 << (DMFParser.T__105 - 64)) | (1 << (DMFParser.T__106 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__108 - 64)) | (1 << (DMFParser.OFF - 64)) | (1 << (DMFParser.ON - 64)) | (1 << (DMFParser.SUB - 64)) | (1 << (DMFParser.TOGGLE - 64)) | (1 << (DMFParser.ID - 64)) | (1 << (DMFParser.INT - 64)))) != 0):
                    self.state = 105
                    self.stat()
                    self.state = 110
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 111
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


    class Vol_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.amount = None # ExprContext
            self.copyFrom(ctx)

        def vol_unit(self):
            return self.getTypedRuleContext(DMFParser.Vol_unitContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVol_expr" ):
                listener.enterVol_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVol_expr" ):
                listener.exitVol_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVol_expr" ):
                return visitor.visitVol_expr(self)
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
            self.state = 189
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 115
                self.match(DMFParser.T__7)
                self.state = 116
                self.expr(0)
                self.state = 117
                self.match(DMFParser.T__8)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 119
                self.match(DMFParser.T__7)
                self.state = 120
                localctx.x = self.expr(0)
                self.state = 121
                self.match(DMFParser.T__9)
                self.state = 122
                localctx.y = self.expr(0)
                self.state = 123
                self.match(DMFParser.T__8)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 125
                self.match(DMFParser.SUB)
                self.state = 126
                localctx.rhs = self.expr(37)
                pass

            elif la_ == 4:
                localctx = DMFParser.Const_rc_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 127
                localctx._INT = self.match(DMFParser.INT)
                self.state = 128
                self.rc((0 if localctx._INT is None else int(localctx._INT.text)))
                pass

            elif la_ == 5:
                localctx = DMFParser.Not_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 129
                self.match(DMFParser.T__21)
                self.state = 130
                self.expr(22)
                pass

            elif la_ == 6:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 131
                self.direction()
                self.state = 132
                localctx.dist = self.expr(19)
                pass

            elif la_ == 7:
                localctx = DMFParser.Dir_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 134
                self.direction()
                pass

            elif la_ == 8:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 135
                self.match(DMFParser.T__24)
                self.state = 137
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__48) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51))) != 0):
                    self.state = 136
                    self.axis()


                self.state = 139
                localctx.which = self.expr(17)
                pass

            elif la_ == 9:
                localctx = DMFParser.Pause_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 140
                self.match(DMFParser.T__0)
                self.state = 141
                localctx.duration = self.expr(16)
                pass

            elif la_ == 10:
                localctx = DMFParser.Well_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 142
                self.match(DMFParser.T__25)
                self.state = 143
                self.match(DMFParser.T__26)
                self.state = 144
                localctx.which = self.expr(15)
                pass

            elif la_ == 11:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 145
                self.match(DMFParser.T__16)
                self.state = 146
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__29 or _la==DMFParser.T__30):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 147
                localctx.loc = self.expr(13)
                pass

            elif la_ == 12:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 148
                self.macro_def()
                pass

            elif la_ == 13:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 150
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__31:
                    self.state = 149
                    self.match(DMFParser.T__31)


                self.state = 152
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
                self.state = 153
                self.match(DMFParser.TOGGLE)
                self.state = 155
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
                if la_ == 1:
                    self.state = 154
                    self.match(DMFParser.T__32)


                pass

            elif la_ == 15:
                localctx = DMFParser.Remove_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 157
                self.match(DMFParser.T__33)
                self.state = 163
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
                if la_ == 1:
                    self.state = 158
                    self.match(DMFParser.T__34)
                    self.state = 160
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==DMFParser.T__35:
                        self.state = 159
                        self.match(DMFParser.T__35)


                    self.state = 162
                    self.match(DMFParser.T__36)


                pass

            elif la_ == 16:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 166
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__35:
                    self.state = 165
                    self.match(DMFParser.T__35)


                self.state = 168
                self.param_type()
                pass

            elif la_ == 17:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 169
                self.param_type()
                self.state = 170
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 18:
                localctx = DMFParser.Bool_const_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 172
                localctx.val = self.bool_val()
                pass

            elif la_ == 19:
                localctx = DMFParser.Function_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 173
                self.name()
                self.state = 174
                self.match(DMFParser.T__7)
                self.state = 183
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__7) | (1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__21) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__31) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__35) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__39) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.T__97 - 64)) | (1 << (DMFParser.T__98 - 64)) | (1 << (DMFParser.T__99 - 64)) | (1 << (DMFParser.T__100 - 64)) | (1 << (DMFParser.T__101 - 64)) | (1 << (DMFParser.T__102 - 64)) | (1 << (DMFParser.T__103 - 64)) | (1 << (DMFParser.T__104 - 64)) | (1 << (DMFParser.T__105 - 64)) | (1 << (DMFParser.T__106 - 64)) | (1 << (DMFParser.T__107 - 64)) | (1 << (DMFParser.T__108 - 64)) | (1 << (DMFParser.OFF - 64)) | (1 << (DMFParser.ON - 64)) | (1 << (DMFParser.SUB - 64)) | (1 << (DMFParser.TOGGLE - 64)) | (1 << (DMFParser.ID - 64)) | (1 << (DMFParser.INT - 64)))) != 0):
                    self.state = 175
                    localctx._expr = self.expr(0)
                    localctx.args.append(localctx._expr)
                    self.state = 180
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==DMFParser.T__9:
                        self.state = 176
                        self.match(DMFParser.T__9)
                        self.state = 177
                        localctx._expr = self.expr(0)
                        localctx.args.append(localctx._expr)
                        self.state = 182
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 185
                self.match(DMFParser.T__8)
                pass

            elif la_ == 20:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 187
                self.name()
                pass

            elif la_ == 21:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 188
                localctx._INT = self.match(DMFParser.INT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 249
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 247
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.In_dir_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 191
                        if not self.precpred(self._ctx, 33):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 33)")
                        self.state = 192
                        self.match(DMFParser.T__11)
                        self.state = 193
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__12 or _la==DMFParser.T__13):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 194
                        localctx.d = self.expr(34)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 195
                        if not self.precpred(self._ctx, 26):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 26)")
                        self.state = 196
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 197
                        localctx.rhs = self.expr(27)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 198
                        if not self.precpred(self._ctx, 25):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 25)")
                        self.state = 199
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 200
                        localctx.rhs = self.expr(26)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Rel_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 201
                        if not self.precpred(self._ctx, 24):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 24)")
                        self.state = 202
                        self.rel()
                        self.state = 203
                        localctx.rhs = self.expr(25)
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.And_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 205
                        if not self.precpred(self._ctx, 21):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 21)")
                        self.state = 206
                        self.match(DMFParser.T__22)
                        self.state = 207
                        localctx.rhs = self.expr(22)
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Or_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 208
                        if not self.precpred(self._ctx, 20):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 20)")
                        self.state = 209
                        self.match(DMFParser.T__23)
                        self.state = 210
                        localctx.rhs = self.expr(21)
                        pass

                    elif la_ == 7:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 211
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 212
                        self.match(DMFParser.INJECT)
                        self.state = 213
                        localctx.what = self.expr(13)
                        pass

                    elif la_ == 8:
                        localctx = DMFParser.Cond_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.first = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 214
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 215
                        self.match(DMFParser.T__1)
                        self.state = 216
                        localctx.cond = self.expr(0)
                        self.state = 217
                        self.match(DMFParser.T__2)
                        self.state = 218
                        localctx.second = self.expr(12)
                        pass

                    elif la_ == 9:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 220
                        if not self.precpred(self._ctx, 36):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 36)")
                        self.state = 221
                        self.direction()
                        pass

                    elif la_ == 10:
                        localctx = DMFParser.Attr_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 222
                        if not self.precpred(self._ctx, 35):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 35)")
                        self.state = 223
                        self.match(DMFParser.ATTR)
                        self.state = 224
                        self.attr()
                        pass

                    elif la_ == 11:
                        localctx = DMFParser.Turn_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.start_dir = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 225
                        if not self.precpred(self._ctx, 34):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 34)")
                        self.state = 226
                        self.match(DMFParser.T__10)
                        self.state = 227
                        self.turn()
                        pass

                    elif la_ == 12:
                        localctx = DMFParser.N_rc_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 228
                        if not self.precpred(self._ctx, 31):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 31)")
                        self.state = 229
                        self.rc(0)
                        pass

                    elif la_ == 13:
                        localctx = DMFParser.Time_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.duration = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 230
                        if not self.precpred(self._ctx, 30):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 30)")
                        self.state = 231
                        self.time_unit()
                        pass

                    elif la_ == 14:
                        localctx = DMFParser.Ticks_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.duration = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 232
                        if not self.precpred(self._ctx, 29):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 29)")
                        self.state = 233
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__14 or _la==DMFParser.T__15):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        pass

                    elif la_ == 15:
                        localctx = DMFParser.Vol_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 234
                        if not self.precpred(self._ctx, 28):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 28)")
                        self.state = 235
                        self.vol_unit()
                        pass

                    elif la_ == 16:
                        localctx = DMFParser.Drop_vol_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 236
                        if not self.precpred(self._ctx, 27):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 27)")
                        self.state = 237
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__16 or _la==DMFParser.T__17):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        pass

                    elif la_ == 17:
                        localctx = DMFParser.Has_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 238
                        if not self.precpred(self._ctx, 23):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 23)")
                        self.state = 239
                        self.match(DMFParser.T__18)
                        self.state = 240
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__19 or _la==DMFParser.T__20):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 241
                        self.attr()
                        pass

                    elif la_ == 18:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 242
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 243
                        self.match(DMFParser.T__27)
                        self.state = 244
                        localctx.which = self.expr(0)
                        self.state = 245
                        self.match(DMFParser.T__28)
                        pass

             
                self.state = 251
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
            self.state = 264
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__37, DMFParser.T__38]:
                self.enterOuterAlt(localctx, 1)
                self.state = 252
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__37 or _la==DMFParser.T__38):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__39, DMFParser.T__40]:
                self.enterOuterAlt(localctx, 2)
                self.state = 255
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__39 or _la==DMFParser.T__40):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__41, DMFParser.T__42]:
                self.enterOuterAlt(localctx, 3)
                self.state = 258
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__41 or _la==DMFParser.T__42):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__43, DMFParser.T__44]:
                self.enterOuterAlt(localctx, 4)
                self.state = 261
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__43 or _la==DMFParser.T__44):
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
            self.state = 272
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__43, DMFParser.T__45]:
                self.enterOuterAlt(localctx, 1)
                self.state = 266
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__43 or _la==DMFParser.T__45):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.RIGHT
                pass
            elif token in [DMFParser.T__41, DMFParser.T__46]:
                self.enterOuterAlt(localctx, 2)
                self.state = 268
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__41 or _la==DMFParser.T__46):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.LEFT
                pass
            elif token in [DMFParser.T__47]:
                self.enterOuterAlt(localctx, 3)
                self.state = 270
                self.match(DMFParser.T__47)
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
            self.state = 288
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 274
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 275
                self.match(DMFParser.T__48)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 278
                self.match(DMFParser.T__49)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 281
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 282
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__50 or _la==DMFParser.T__51):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 285
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__52 or _la==DMFParser.T__53):
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
            self.state = 294
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__48]:
                self.enterOuterAlt(localctx, 1)
                self.state = 290
                self.match(DMFParser.T__48)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__50, DMFParser.T__51]:
                self.enterOuterAlt(localctx, 2)
                self.state = 292
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__50 or _la==DMFParser.T__51):
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
            self.state = 296
            self.macro_header()
            self.state = 299
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__3, DMFParser.T__5]:
                self.state = 297
                self.compound()
                pass
            elif token in [DMFParser.T__0, DMFParser.T__7, DMFParser.T__15, DMFParser.T__16, DMFParser.T__21, DMFParser.T__24, DMFParser.T__25, DMFParser.T__31, DMFParser.T__32, DMFParser.T__33, DMFParser.T__35, DMFParser.T__37, DMFParser.T__38, DMFParser.T__39, DMFParser.T__40, DMFParser.T__41, DMFParser.T__42, DMFParser.T__43, DMFParser.T__44, DMFParser.T__54, DMFParser.T__55, DMFParser.T__56, DMFParser.T__57, DMFParser.T__58, DMFParser.T__59, DMFParser.T__60, DMFParser.T__61, DMFParser.T__62, DMFParser.T__63, DMFParser.T__68, DMFParser.T__87, DMFParser.T__90, DMFParser.T__97, DMFParser.T__98, DMFParser.T__99, DMFParser.T__100, DMFParser.T__101, DMFParser.T__102, DMFParser.T__103, DMFParser.T__104, DMFParser.T__105, DMFParser.T__106, DMFParser.T__107, DMFParser.T__108, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT]:
                self.state = 298
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
            self.state = 301
            self.match(DMFParser.T__54)
            self.state = 302
            self.match(DMFParser.T__7)
            self.state = 311
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__25) | (1 << DMFParser.T__32) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57) | (1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.ID - 64)))) != 0):
                self.state = 303
                self.param()
                self.state = 308
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__9:
                    self.state = 304
                    self.match(DMFParser.T__9)
                    self.state = 305
                    self.param()
                    self.state = 310
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 313
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
            self.state = 327
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__15, DMFParser.T__16, DMFParser.T__25, DMFParser.T__32, DMFParser.T__55, DMFParser.T__56, DMFParser.T__57, DMFParser.T__58, DMFParser.T__59, DMFParser.T__60, DMFParser.T__61, DMFParser.T__62]:
                self.enterOuterAlt(localctx, 1)
                self.state = 315
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 319
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.INT:
                    self.state = 317
                    localctx._INT = self.match(DMFParser.INT)
                    localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))


                pass
            elif token in [DMFParser.T__63, DMFParser.T__68, DMFParser.T__87, DMFParser.T__90, DMFParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 321
                localctx._name = self.name()
                self.state = 322
                self.match(DMFParser.INJECT)
                self.state = 323
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
            self.state = 356
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,28,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 329
                self.match(DMFParser.T__16)
                localctx.type=Type.DROP
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 331
                self.match(DMFParser.T__55)
                localctx.type=Type.PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 333
                self.match(DMFParser.T__25)
                localctx.type=Type.WELL
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 335
                self.match(DMFParser.T__25)
                self.state = 336
                self.match(DMFParser.T__55)
                localctx.type=Type.WELL_PAD
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 338
                self.match(DMFParser.T__56)
                localctx.type=Type.INT
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 340
                self.match(DMFParser.T__32)
                localctx.type=Type.BINARY_STATE
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 342
                self.match(DMFParser.T__57)
                localctx.type=Type.BINARY_CPT
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 344
                self.match(DMFParser.T__58)
                localctx.type=Type.DELTA
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 346
                self.match(DMFParser.T__59)
                localctx.type=Type.MOTION
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 348
                self.match(DMFParser.T__60)
                localctx.type=Type.DELAY
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 350
                self.match(DMFParser.T__61)
                localctx.type=Type.TIME
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 352
                self.match(DMFParser.T__15)
                localctx.type=Type.TICKS
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 354
                self.match(DMFParser.T__62)
                localctx.type=Type.BOOL
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
        self.enterRule(localctx, 28, self.RULE_time_unit)
        self._la = 0 # Token type
        try:
            self.state = 362
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__63, DMFParser.T__64, DMFParser.T__65, DMFParser.T__66, DMFParser.T__67]:
                self.enterOuterAlt(localctx, 1)
                self.state = 358
                _la = self._input.LA(1)
                if not(((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__67 - 64)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.sec
                pass
            elif token in [DMFParser.T__68, DMFParser.T__69, DMFParser.T__70]:
                self.enterOuterAlt(localctx, 2)
                self.state = 360
                _la = self._input.LA(1)
                if not(((((_la - 69)) & ~0x3f) == 0 and ((1 << (_la - 69)) & ((1 << (DMFParser.T__68 - 69)) | (1 << (DMFParser.T__69 - 69)) | (1 << (DMFParser.T__70 - 69)))) != 0)):
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


    class Vol_unitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.unit = None


        def getRuleIndex(self):
            return DMFParser.RULE_vol_unit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVol_unit" ):
                listener.enterVol_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVol_unit" ):
                listener.exitVol_unit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVol_unit" ):
                return visitor.visitVol_unit(self)
            else:
                return visitor.visitChildren(self)




    def vol_unit(self):

        localctx = DMFParser.Vol_unitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_vol_unit)
        self._la = 0 # Token type
        try:
            self.state = 368
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__71, DMFParser.T__72, DMFParser.T__73, DMFParser.T__74, DMFParser.T__75, DMFParser.T__76]:
                self.enterOuterAlt(localctx, 1)
                self.state = 364
                _la = self._input.LA(1)
                if not(((((_la - 72)) & ~0x3f) == 0 and ((1 << (_la - 72)) & ((1 << (DMFParser.T__71 - 72)) | (1 << (DMFParser.T__72 - 72)) | (1 << (DMFParser.T__73 - 72)) | (1 << (DMFParser.T__74 - 72)) | (1 << (DMFParser.T__75 - 72)) | (1 << (DMFParser.T__76 - 72)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.uL
                pass
            elif token in [DMFParser.T__77, DMFParser.T__78, DMFParser.T__79, DMFParser.T__80, DMFParser.T__81, DMFParser.T__82]:
                self.enterOuterAlt(localctx, 2)
                self.state = 366
                _la = self._input.LA(1)
                if not(((((_la - 78)) & ~0x3f) == 0 and ((1 << (_la - 78)) & ((1 << (DMFParser.T__77 - 78)) | (1 << (DMFParser.T__78 - 78)) | (1 << (DMFParser.T__79 - 78)) | (1 << (DMFParser.T__80 - 78)) | (1 << (DMFParser.T__81 - 78)) | (1 << (DMFParser.T__82 - 78)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.mL
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
        self.enterRule(localctx, 32, self.RULE_attr)
        self._la = 0 # Token type
        try:
            self.state = 403
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,33,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 370
                self.match(DMFParser.T__83)
                localctx.which=Attr.GATE
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 372
                self.match(DMFParser.T__84)
                self.state = 373
                self.match(DMFParser.T__55)
                localctx.which=Attr.EXIT_PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 375
                self.match(DMFParser.T__32)
                localctx.which=Attr.STATE
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 377
                self.match(DMFParser.T__85)
                localctx.which=Attr.DISTANCE
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 379
                self.match(DMFParser.T__86)
                localctx.which=Attr.DURATION
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 381
                self.match(DMFParser.T__55)
                localctx.which=Attr.PAD
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 386
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__48]:
                    self.state = 383
                    self.match(DMFParser.T__48)
                    pass
                elif token in [DMFParser.T__87]:
                    self.state = 384
                    self.match(DMFParser.T__87)
                    self.state = 385
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__88 or _la==DMFParser.T__89):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    pass
                else:
                    raise NoViableAltException(self)

                localctx.which=Attr.ROW
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 393
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__50]:
                    self.state = 389
                    self.match(DMFParser.T__50)
                    pass
                elif token in [DMFParser.T__51]:
                    self.state = 390
                    self.match(DMFParser.T__51)
                    pass
                elif token in [DMFParser.T__90]:
                    self.state = 391
                    self.match(DMFParser.T__90)
                    self.state = 392
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__88 or _la==DMFParser.T__89):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    pass
                else:
                    raise NoViableAltException(self)

                localctx.which=Attr.COLUMN
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 396
                self.match(DMFParser.T__25)
                localctx.which=Attr.WELL
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 398
                self.match(DMFParser.T__84)
                self.state = 399
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__12 or _la==DMFParser.T__13):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which=Attr.EXIT_DIR
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 401
                self.match(DMFParser.T__16)
                localctx.which=Attr.DROP
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
        self.enterRule(localctx, 34, self.RULE_rel)
        try:
            self.state = 417
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__91]:
                self.enterOuterAlt(localctx, 1)
                self.state = 405
                self.match(DMFParser.T__91)
                localctx.which=Rel.EQ
                pass
            elif token in [DMFParser.T__92]:
                self.enterOuterAlt(localctx, 2)
                self.state = 407
                self.match(DMFParser.T__92)
                localctx.which=Rel.NE
                pass
            elif token in [DMFParser.T__93]:
                self.enterOuterAlt(localctx, 3)
                self.state = 409
                self.match(DMFParser.T__93)
                localctx.which=Rel.LT
                pass
            elif token in [DMFParser.T__94]:
                self.enterOuterAlt(localctx, 4)
                self.state = 411
                self.match(DMFParser.T__94)
                localctx.which=Rel.LE
                pass
            elif token in [DMFParser.T__95]:
                self.enterOuterAlt(localctx, 5)
                self.state = 413
                self.match(DMFParser.T__95)
                localctx.which=Rel.GT
                pass
            elif token in [DMFParser.T__96]:
                self.enterOuterAlt(localctx, 6)
                self.state = 415
                self.match(DMFParser.T__96)
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
        self.enterRule(localctx, 36, self.RULE_bool_val)
        self._la = 0 # Token type
        try:
            self.state = 423
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__97, DMFParser.T__98, DMFParser.T__99, DMFParser.T__100, DMFParser.T__101, DMFParser.T__102]:
                self.enterOuterAlt(localctx, 1)
                self.state = 419
                _la = self._input.LA(1)
                if not(((((_la - 98)) & ~0x3f) == 0 and ((1 << (_la - 98)) & ((1 << (DMFParser.T__97 - 98)) | (1 << (DMFParser.T__98 - 98)) | (1 << (DMFParser.T__99 - 98)) | (1 << (DMFParser.T__100 - 98)) | (1 << (DMFParser.T__101 - 98)) | (1 << (DMFParser.T__102 - 98)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.val=True
                pass
            elif token in [DMFParser.T__103, DMFParser.T__104, DMFParser.T__105, DMFParser.T__106, DMFParser.T__107, DMFParser.T__108]:
                self.enterOuterAlt(localctx, 2)
                self.state = 421
                _la = self._input.LA(1)
                if not(((((_la - 104)) & ~0x3f) == 0 and ((1 << (_la - 104)) & ((1 << (DMFParser.T__103 - 104)) | (1 << (DMFParser.T__104 - 104)) | (1 << (DMFParser.T__105 - 104)) | (1 << (DMFParser.T__106 - 104)) | (1 << (DMFParser.T__107 - 104)) | (1 << (DMFParser.T__108 - 104)))) != 0)):
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
        self.enterRule(localctx, 38, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 427
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.ID]:
                self.state = 425
                self.match(DMFParser.ID)
                pass
            elif token in [DMFParser.T__63, DMFParser.T__68, DMFParser.T__87, DMFParser.T__90]:
                self.state = 426
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
        self.enterRule(localctx, 40, self.RULE_kwd_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 429
            _la = self._input.LA(1)
            if not(((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__68 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__90 - 64)))) != 0)):
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
                return self.precpred(self._ctx, 33)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 26)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 25)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 24)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 21)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 20)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 36)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 35)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 34)
         

            if predIndex == 11:
                return self.precpred(self._ctx, 31)
         

            if predIndex == 12:
                return self.precpred(self._ctx, 30)
         

            if predIndex == 13:
                return self.precpred(self._ctx, 29)
         

            if predIndex == 14:
                return self.precpred(self._ctx, 28)
         

            if predIndex == 15:
                return self.precpred(self._ctx, 27)
         

            if predIndex == 16:
                return self.precpred(self._ctx, 23)
         

            if predIndex == 17:
                return self.precpred(self._ctx, 14)
         

    def rc_sempred(self, localctx:RcContext, predIndex:int):
            if predIndex == 18:
                return localctx.n==1
         

            if predIndex == 19:
                return localctx.n==1
         




