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
from langsup.type_supp import Type, Attr
from quantities import SI


from mpam.types import Dir 


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3Y")
        buf.write("\u0162\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\3\2\7\2(\n\2\f\2\16\2+\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\5\39\n\3\3\4\3\4\3\4\3\4\3\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5J\n\5\3\6\3")
        buf.write("\6\7\6N\n\6\f\6\16\6Q\13\6\3\6\3\6\3\6\7\6V\n\6\f\6\16")
        buf.write("\6Y\13\6\3\6\5\6\\\n\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5")
        buf.write("\7s\n\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5")
        buf.write("\7\u0080\n\7\3\7\3\7\3\7\5\7\u0085\n\7\3\7\3\7\3\7\5\7")
        buf.write("\u008a\n\7\3\7\5\7\u008d\n\7\3\7\5\7\u0090\n\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\7\7\u009b\n\7\f\7\16\7\u009e")
        buf.write("\13\7\5\7\u00a0\n\7\3\7\3\7\3\7\3\7\5\7\u00a6\n\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7")
        buf.write("\3\7\3\7\3\7\3\7\7\7\u00c8\n\7\f\7\16\7\u00cb\13\7\3\b")
        buf.write("\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\b\u00d9")
        buf.write("\n\b\3\t\3\t\3\t\3\t\3\t\3\t\5\t\u00e1\n\t\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u00f1")
        buf.write("\n\n\3\13\3\13\3\13\3\13\5\13\u00f7\n\13\3\f\3\f\3\f\5")
        buf.write("\f\u00fc\n\f\3\r\3\r\3\r\3\r\3\r\7\r\u0103\n\r\f\r\16")
        buf.write("\r\u0106\13\r\5\r\u0108\n\r\3\r\3\r\3\16\3\16\3\16\3\16")
        buf.write("\5\16\u0110\n\16\3\16\3\16\3\16\3\16\3\16\3\16\5\16\u0118")
        buf.write("\n\16\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17")
        buf.write("\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17")
        buf.write("\3\17\3\17\3\17\3\17\5\17\u0133\n\17\3\20\3\20\3\20\3")
        buf.write("\20\5\20\u0139\n\20\3\21\3\21\3\21\3\21\3\21\3\21\3\21")
        buf.write("\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\3\21\5\21\u014b")
        buf.write("\n\21\3\21\3\21\3\21\3\21\3\21\5\21\u0152\n\21\3\21\3")
        buf.write("\21\3\21\3\21\3\21\3\21\5\21\u015a\n\21\3\22\3\22\5\22")
        buf.write("\u015e\n\22\3\23\3\23\3\23\2\3\f\24\2\4\6\b\n\f\16\20")
        buf.write("\22\24\26\30\32\34\36 \"$\2\24\3\2\27\30\3\2NO\3\2\r\16")
        buf.write("\4\2KKMM\4\2HHPP\3\2\17\20\3\2\37 \3\2!\"\3\2#$\3\2%&")
        buf.write("\4\2%%\'\'\4\2##((\3\2,-\3\2./\3\28<\3\2=?\3\2EF\6\28")
        buf.write("8==DDGG\2\u01a5\2)\3\2\2\2\48\3\2\2\2\6:\3\2\2\2\bI\3")
        buf.write("\2\2\2\n[\3\2\2\2\f\u00a5\3\2\2\2\16\u00d8\3\2\2\2\20")
        buf.write("\u00e0\3\2\2\2\22\u00f0\3\2\2\2\24\u00f6\3\2\2\2\26\u00f8")
        buf.write("\3\2\2\2\30\u00fd\3\2\2\2\32\u0117\3\2\2\2\34\u0132\3")
        buf.write("\2\2\2\36\u0138\3\2\2\2 \u0159\3\2\2\2\"\u015d\3\2\2\2")
        buf.write("$\u015f\3\2\2\2&(\5\b\5\2\'&\3\2\2\2(+\3\2\2\2)\'\3\2")
        buf.write("\2\2)*\3\2\2\2*,\3\2\2\2+)\3\2\2\2,-\7\2\2\3-\3\3\2\2")
        buf.write("\2./\5\n\6\2/\60\7\2\2\3\609\3\2\2\2\61\62\5\6\4\2\62")
        buf.write("\63\7\2\2\3\639\3\2\2\2\64\65\5\f\7\2\65\66\7\2\2\3\66")
        buf.write("9\3\2\2\2\679\7\2\2\38.\3\2\2\28\61\3\2\2\28\64\3\2\2")
        buf.write("\28\67\3\2\2\29\5\3\2\2\2:;\5\"\22\2;<\7I\2\2<=\5\f\7")
        buf.write("\2=\7\3\2\2\2>?\5\6\4\2?@\7Q\2\2@J\3\2\2\2AB\7\3\2\2B")
        buf.write("C\5\f\7\2CD\7Q\2\2DJ\3\2\2\2EF\5\f\7\2FG\7Q\2\2GJ\3\2")
        buf.write("\2\2HJ\5\n\6\2I>\3\2\2\2IA\3\2\2\2IE\3\2\2\2IH\3\2\2\2")
        buf.write("J\t\3\2\2\2KO\7\4\2\2LN\5\b\5\2ML\3\2\2\2NQ\3\2\2\2OM")
        buf.write("\3\2\2\2OP\3\2\2\2PR\3\2\2\2QO\3\2\2\2R\\\7\5\2\2SW\7")
        buf.write("\6\2\2TV\5\b\5\2UT\3\2\2\2VY\3\2\2\2WU\3\2\2\2WX\3\2\2")
        buf.write("\2XZ\3\2\2\2YW\3\2\2\2Z\\\7\7\2\2[K\3\2\2\2[S\3\2\2\2")
        buf.write("\\\13\3\2\2\2]^\b\7\1\2^_\7\b\2\2_`\5\f\7\2`a\7\t\2\2")
        buf.write("a\u00a6\3\2\2\2bc\7\b\2\2cd\5\f\7\2de\7\n\2\2ef\5\f\7")
        buf.write("\2fg\7\t\2\2g\u00a6\3\2\2\2hi\7P\2\2i\u00a6\5\f\7\36j")
        buf.write("k\7T\2\2k\u00a6\5\22\n\2lm\5\16\b\2mn\5\f\7\23n\u00a6")
        buf.write("\3\2\2\2o\u00a6\5\16\b\2pr\7\21\2\2qs\5\24\13\2rq\3\2")
        buf.write("\2\2rs\3\2\2\2st\3\2\2\2t\u00a6\5\f\7\21uv\7\3\2\2v\u00a6")
        buf.write("\5\f\7\20wx\7\22\2\2xy\7\23\2\2y\u00a6\5\f\7\17z{\7\26")
        buf.write("\2\2{|\t\2\2\2|\u00a6\5\f\7\r}\u00a6\5\26\f\2~\u0080\7")
        buf.write("\31\2\2\177~\3\2\2\2\177\u0080\3\2\2\2\u0080\u0081\3\2")
        buf.write("\2\2\u0081\u00a6\t\3\2\2\u0082\u0084\7R\2\2\u0083\u0085")
        buf.write("\7\32\2\2\u0084\u0083\3\2\2\2\u0084\u0085\3\2\2\2\u0085")
        buf.write("\u00a6\3\2\2\2\u0086\u008c\7\33\2\2\u0087\u0089\7\34\2")
        buf.write("\2\u0088\u008a\7\35\2\2\u0089\u0088\3\2\2\2\u0089\u008a")
        buf.write("\3\2\2\2\u008a\u008b\3\2\2\2\u008b\u008d\7\36\2\2\u008c")
        buf.write("\u0087\3\2\2\2\u008c\u008d\3\2\2\2\u008d\u00a6\3\2\2\2")
        buf.write("\u008e\u0090\7\35\2\2\u008f\u008e\3\2\2\2\u008f\u0090")
        buf.write("\3\2\2\2\u0090\u0091\3\2\2\2\u0091\u00a6\5\34\17\2\u0092")
        buf.write("\u0093\5\34\17\2\u0093\u0094\7T\2\2\u0094\u00a6\3\2\2")
        buf.write("\2\u0095\u0096\5\"\22\2\u0096\u009f\7\b\2\2\u0097\u009c")
        buf.write("\5\f\7\2\u0098\u0099\7\n\2\2\u0099\u009b\5\f\7\2\u009a")
        buf.write("\u0098\3\2\2\2\u009b\u009e\3\2\2\2\u009c\u009a\3\2\2\2")
        buf.write("\u009c\u009d\3\2\2\2\u009d\u00a0\3\2\2\2\u009e\u009c\3")
        buf.write("\2\2\2\u009f\u0097\3\2\2\2\u009f\u00a0\3\2\2\2\u00a0\u00a1")
        buf.write("\3\2\2\2\u00a1\u00a2\7\t\2\2\u00a2\u00a6\3\2\2\2\u00a3")
        buf.write("\u00a6\5\"\22\2\u00a4\u00a6\7T\2\2\u00a5]\3\2\2\2\u00a5")
        buf.write("b\3\2\2\2\u00a5h\3\2\2\2\u00a5j\3\2\2\2\u00a5l\3\2\2\2")
        buf.write("\u00a5o\3\2\2\2\u00a5p\3\2\2\2\u00a5u\3\2\2\2\u00a5w\3")
        buf.write("\2\2\2\u00a5z\3\2\2\2\u00a5}\3\2\2\2\u00a5\177\3\2\2\2")
        buf.write("\u00a5\u0082\3\2\2\2\u00a5\u0086\3\2\2\2\u00a5\u008f\3")
        buf.write("\2\2\2\u00a5\u0092\3\2\2\2\u00a5\u0095\3\2\2\2\u00a5\u00a3")
        buf.write("\3\2\2\2\u00a5\u00a4\3\2\2\2\u00a6\u00c9\3\2\2\2\u00a7")
        buf.write("\u00a8\f\32\2\2\u00a8\u00a9\7\f\2\2\u00a9\u00aa\t\4\2")
        buf.write("\2\u00aa\u00c8\5\f\7\33\u00ab\u00ac\f\25\2\2\u00ac\u00ad")
        buf.write("\t\5\2\2\u00ad\u00c8\5\f\7\26\u00ae\u00af\f\24\2\2\u00af")
        buf.write("\u00b0\t\6\2\2\u00b0\u00c8\5\f\7\25\u00b1\u00b2\f\f\2")
        buf.write("\2\u00b2\u00b3\7L\2\2\u00b3\u00c8\5\f\7\r\u00b4\u00b5")
        buf.write("\f\35\2\2\u00b5\u00c8\5\16\b\2\u00b6\u00b7\f\34\2\2\u00b7")
        buf.write("\u00b8\7J\2\2\u00b8\u00c8\5 \21\2\u00b9\u00ba\f\33\2\2")
        buf.write("\u00ba\u00bb\7\13\2\2\u00bb\u00c8\5\20\t\2\u00bc\u00bd")
        buf.write("\f\30\2\2\u00bd\u00c8\5\22\n\2\u00be\u00bf\f\27\2\2\u00bf")
        buf.write("\u00c8\5\36\20\2\u00c0\u00c1\f\26\2\2\u00c1\u00c8\t\7")
        buf.write("\2\2\u00c2\u00c3\f\16\2\2\u00c3\u00c4\7\24\2\2\u00c4\u00c5")
        buf.write("\5\f\7\2\u00c5\u00c6\7\25\2\2\u00c6\u00c8\3\2\2\2\u00c7")
        buf.write("\u00a7\3\2\2\2\u00c7\u00ab\3\2\2\2\u00c7\u00ae\3\2\2\2")
        buf.write("\u00c7\u00b1\3\2\2\2\u00c7\u00b4\3\2\2\2\u00c7\u00b6\3")
        buf.write("\2\2\2\u00c7\u00b9\3\2\2\2\u00c7\u00bc\3\2\2\2\u00c7\u00be")
        buf.write("\3\2\2\2\u00c7\u00c0\3\2\2\2\u00c7\u00c2\3\2\2\2\u00c8")
        buf.write("\u00cb\3\2\2\2\u00c9\u00c7\3\2\2\2\u00c9\u00ca\3\2\2\2")
        buf.write("\u00ca\r\3\2\2\2\u00cb\u00c9\3\2\2\2\u00cc\u00cd\t\b\2")
        buf.write("\2\u00cd\u00ce\b\b\1\2\u00ce\u00d9\b\b\1\2\u00cf\u00d0")
        buf.write("\t\t\2\2\u00d0\u00d1\b\b\1\2\u00d1\u00d9\b\b\1\2\u00d2")
        buf.write("\u00d3\t\n\2\2\u00d3\u00d4\b\b\1\2\u00d4\u00d9\b\b\1\2")
        buf.write("\u00d5\u00d6\t\13\2\2\u00d6\u00d7\b\b\1\2\u00d7\u00d9")
        buf.write("\b\b\1\2\u00d8\u00cc\3\2\2\2\u00d8\u00cf\3\2\2\2\u00d8")
        buf.write("\u00d2\3\2\2\2\u00d8\u00d5\3\2\2\2\u00d9\17\3\2\2\2\u00da")
        buf.write("\u00db\t\f\2\2\u00db\u00e1\b\t\1\2\u00dc\u00dd\t\r\2\2")
        buf.write("\u00dd\u00e1\b\t\1\2\u00de\u00df\7)\2\2\u00df\u00e1\b")
        buf.write("\t\1\2\u00e0\u00da\3\2\2\2\u00e0\u00dc\3\2\2\2\u00e0\u00de")
        buf.write("\3\2\2\2\u00e1\21\3\2\2\2\u00e2\u00e3\6\n\r\3\u00e3\u00e4")
        buf.write("\7*\2\2\u00e4\u00e5\b\n\1\2\u00e5\u00f1\b\n\1\2\u00e6")
        buf.write("\u00e7\7+\2\2\u00e7\u00e8\b\n\1\2\u00e8\u00f1\b\n\1\2")
        buf.write("\u00e9\u00ea\6\n\16\3\u00ea\u00eb\t\16\2\2\u00eb\u00ec")
        buf.write("\b\n\1\2\u00ec\u00f1\b\n\1\2\u00ed\u00ee\t\17\2\2\u00ee")
        buf.write("\u00ef\b\n\1\2\u00ef\u00f1\b\n\1\2\u00f0\u00e2\3\2\2\2")
        buf.write("\u00f0\u00e6\3\2\2\2\u00f0\u00e9\3\2\2\2\u00f0\u00ed\3")
        buf.write("\2\2\2\u00f1\23\3\2\2\2\u00f2\u00f3\7*\2\2\u00f3\u00f7")
        buf.write("\b\13\1\2\u00f4\u00f5\t\16\2\2\u00f5\u00f7\b\13\1\2\u00f6")
        buf.write("\u00f2\3\2\2\2\u00f6\u00f4\3\2\2\2\u00f7\25\3\2\2\2\u00f8")
        buf.write("\u00fb\5\30\r\2\u00f9\u00fc\5\n\6\2\u00fa\u00fc\5\f\7")
        buf.write("\2\u00fb\u00f9\3\2\2\2\u00fb\u00fa\3\2\2\2\u00fc\27\3")
        buf.write("\2\2\2\u00fd\u00fe\7\60\2\2\u00fe\u0107\7\b\2\2\u00ff")
        buf.write("\u0104\5\32\16\2\u0100\u0101\7\n\2\2\u0101\u0103\5\32")
        buf.write("\16\2\u0102\u0100\3\2\2\2\u0103\u0106\3\2\2\2\u0104\u0102")
        buf.write("\3\2\2\2\u0104\u0105\3\2\2\2\u0105\u0108\3\2\2\2\u0106")
        buf.write("\u0104\3\2\2\2\u0107\u00ff\3\2\2\2\u0107\u0108\3\2\2\2")
        buf.write("\u0108\u0109\3\2\2\2\u0109\u010a\7\t\2\2\u010a\31\3\2")
        buf.write("\2\2\u010b\u010c\5\34\17\2\u010c\u010f\b\16\1\2\u010d")
        buf.write("\u010e\7T\2\2\u010e\u0110\b\16\1\2\u010f\u010d\3\2\2\2")
        buf.write("\u010f\u0110\3\2\2\2\u0110\u0118\3\2\2\2\u0111\u0112\5")
        buf.write("\"\22\2\u0112\u0113\7L\2\2\u0113\u0114\5\34\17\2\u0114")
        buf.write("\u0115\b\16\1\2\u0115\u0116\b\16\1\2\u0116\u0118\3\2\2")
        buf.write("\2\u0117\u010b\3\2\2\2\u0117\u0111\3\2\2\2\u0118\33\3")
        buf.write("\2\2\2\u0119\u011a\7\26\2\2\u011a\u0133\b\17\1\2\u011b")
        buf.write("\u011c\7\61\2\2\u011c\u0133\b\17\1\2\u011d\u011e\7\22")
        buf.write("\2\2\u011e\u0133\b\17\1\2\u011f\u0120\7\22\2\2\u0120\u0121")
        buf.write("\7\61\2\2\u0121\u0133\b\17\1\2\u0122\u0123\7\62\2\2\u0123")
        buf.write("\u0133\b\17\1\2\u0124\u0125\7\32\2\2\u0125\u0133\b\17")
        buf.write("\1\2\u0126\u0127\7\63\2\2\u0127\u0133\b\17\1\2\u0128\u0129")
        buf.write("\7\64\2\2\u0129\u0133\b\17\1\2\u012a\u012b\7\65\2\2\u012b")
        buf.write("\u0133\b\17\1\2\u012c\u012d\7\66\2\2\u012d\u0133\b\17")
        buf.write("\1\2\u012e\u012f\7\67\2\2\u012f\u0133\b\17\1\2\u0130\u0131")
        buf.write("\7\20\2\2\u0131\u0133\b\17\1\2\u0132\u0119\3\2\2\2\u0132")
        buf.write("\u011b\3\2\2\2\u0132\u011d\3\2\2\2\u0132\u011f\3\2\2\2")
        buf.write("\u0132\u0122\3\2\2\2\u0132\u0124\3\2\2\2\u0132\u0126\3")
        buf.write("\2\2\2\u0132\u0128\3\2\2\2\u0132\u012a\3\2\2\2\u0132\u012c")
        buf.write("\3\2\2\2\u0132\u012e\3\2\2\2\u0132\u0130\3\2\2\2\u0133")
        buf.write("\35\3\2\2\2\u0134\u0135\t\20\2\2\u0135\u0139\b\20\1\2")
        buf.write("\u0136\u0137\t\21\2\2\u0137\u0139\b\20\1\2\u0138\u0134")
        buf.write("\3\2\2\2\u0138\u0136\3\2\2\2\u0139\37\3\2\2\2\u013a\u013b")
        buf.write("\7@\2\2\u013b\u015a\b\21\1\2\u013c\u013d\7A\2\2\u013d")
        buf.write("\u013e\7\61\2\2\u013e\u015a\b\21\1\2\u013f\u0140\7\32")
        buf.write("\2\2\u0140\u015a\b\21\1\2\u0141\u0142\7B\2\2\u0142\u015a")
        buf.write("\b\21\1\2\u0143\u0144\7C\2\2\u0144\u015a\b\21\1\2\u0145")
        buf.write("\u0146\7\61\2\2\u0146\u015a\b\21\1\2\u0147\u014b\7*\2")
        buf.write("\2\u0148\u0149\7D\2\2\u0149\u014b\t\22\2\2\u014a\u0147")
        buf.write("\3\2\2\2\u014a\u0148\3\2\2\2\u014b\u014c\3\2\2\2\u014c")
        buf.write("\u015a\b\21\1\2\u014d\u0152\7,\2\2\u014e\u0152\7-\2\2")
        buf.write("\u014f\u0150\7G\2\2\u0150\u0152\t\22\2\2\u0151\u014d\3")
        buf.write("\2\2\2\u0151\u014e\3\2\2\2\u0151\u014f\3\2\2\2\u0152\u0153")
        buf.write("\3\2\2\2\u0153\u015a\b\21\1\2\u0154\u0155\7\22\2\2\u0155")
        buf.write("\u015a\b\21\1\2\u0156\u0157\7A\2\2\u0157\u0158\t\4\2\2")
        buf.write("\u0158\u015a\b\21\1\2\u0159\u013a\3\2\2\2\u0159\u013c")
        buf.write("\3\2\2\2\u0159\u013f\3\2\2\2\u0159\u0141\3\2\2\2\u0159")
        buf.write("\u0143\3\2\2\2\u0159\u0145\3\2\2\2\u0159\u014a\3\2\2\2")
        buf.write("\u0159\u0151\3\2\2\2\u0159\u0154\3\2\2\2\u0159\u0156\3")
        buf.write("\2\2\2\u015a!\3\2\2\2\u015b\u015e\7S\2\2\u015c\u015e\5")
        buf.write("$\23\2\u015d\u015b\3\2\2\2\u015d\u015c\3\2\2\2\u015e#")
        buf.write("\3\2\2\2\u015f\u0160\t\23\2\2\u0160%\3\2\2\2\")8IOW[r")
        buf.write("\177\u0084\u0089\u008c\u008f\u009c\u009f\u00a5\u00c7\u00c9")
        buf.write("\u00d8\u00e0\u00f0\u00f6\u00fb\u0104\u0107\u010f\u0117")
        buf.write("\u0132\u0138\u014a\u0151\u0159\u015d")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'pause'", "'{'", "'}'", "'[['", "']]'", 
                     "'('", "')'", "','", "'turned'", "'in'", "'dir'", "'direction'", 
                     "'tick'", "'ticks'", "'to'", "'well'", "'#'", "'['", 
                     "']'", "'drop'", "'@'", "'at'", "'turn'", "'state'", 
                     "'remove'", "'from'", "'the'", "'board'", "'up'", "'north'", 
                     "'down'", "'south'", "'left'", "'west'", "'right'", 
                     "'east'", "'clockwise'", "'counterclockwise'", "'around'", 
                     "'row'", "'rows'", "'col'", "'column'", "'cols'", "'columns'", 
                     "'macro'", "'pad'", "'int'", "'component'", "'delta'", 
                     "'motion'", "'delay'", "'time'", "'s'", "'sec'", "'secs'", 
                     "'second'", "'seconds'", "'ms'", "'millisecond'", "'milliseconds'", 
                     "'gate'", "'exit'", "'distance'", "'duration'", "'y'", 
                     "'coord'", "'coordinate'", "'x'", "'+'", "'='", "''s'", 
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
    RULE_attr = 15
    RULE_name = 16
    RULE_kwd_names = 17

    ruleNames =  [ "macro_file", "interactive", "assignment", "stat", "compound", 
                   "expr", "direction", "turn", "rc", "axis", "macro_def", 
                   "macro_header", "param", "param_type", "time_unit", "attr", 
                   "name", "kwd_names" ]

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
    ADD=70
    ASSIGN=71
    ATTR=72
    DIV=73
    INJECT=74
    MUL=75
    OFF=76
    ON=77
    SUB=78
    TERMINATOR=79
    TOGGLE=80
    ID=81
    INT=82
    FLOAT=83
    STRING=84
    EOL_COMMENT=85
    COMMENT=86
    WS=87

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
            self.state = 39
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__13) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53) | (1 << DMFParser.T__58))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.OFF - 66)) | (1 << (DMFParser.ON - 66)) | (1 << (DMFParser.SUB - 66)) | (1 << (DMFParser.TOGGLE - 66)) | (1 << (DMFParser.ID - 66)) | (1 << (DMFParser.INT - 66)))) != 0):
                self.state = 36
                self.stat()
                self.state = 41
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 42
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
            self.state = 54
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 44
                self.compound()
                self.state = 45
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Assignment_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 47
                self.assignment()
                self.state = 48
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 50
                self.expr(0)
                self.state = 51
                self.match(DMFParser.EOF)
                pass

            elif la_ == 4:
                localctx = DMFParser.Empty_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 53
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
            self.state = 56
            localctx.which = self.name()
            self.state = 57
            self.match(DMFParser.ASSIGN)
            self.state = 58
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
            self.state = 71
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Assign_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 60
                self.assignment()
                self.state = 61
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Pause_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 63
                self.match(DMFParser.T__0)
                self.state = 64
                localctx.duration = self.expr(0)
                self.state = 65
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 3:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 67
                self.expr(0)
                self.state = 68
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 4:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 70
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
            self.state = 89
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__1]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 73
                self.match(DMFParser.T__1)
                self.state = 77
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__13) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53) | (1 << DMFParser.T__58))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.OFF - 66)) | (1 << (DMFParser.ON - 66)) | (1 << (DMFParser.SUB - 66)) | (1 << (DMFParser.TOGGLE - 66)) | (1 << (DMFParser.ID - 66)) | (1 << (DMFParser.INT - 66)))) != 0):
                    self.state = 74
                    self.stat()
                    self.state = 79
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 80
                self.match(DMFParser.T__2)
                pass
            elif token in [DMFParser.T__3]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 81
                self.match(DMFParser.T__3)
                self.state = 85
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__1) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__13) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53) | (1 << DMFParser.T__58))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.OFF - 66)) | (1 << (DMFParser.ON - 66)) | (1 << (DMFParser.SUB - 66)) | (1 << (DMFParser.TOGGLE - 66)) | (1 << (DMFParser.ID - 66)) | (1 << (DMFParser.INT - 66)))) != 0):
                    self.state = 82
                    self.stat()
                    self.state = 87
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 88
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
            self.state = 163
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 92
                self.match(DMFParser.T__5)
                self.state = 93
                self.expr(0)
                self.state = 94
                self.match(DMFParser.T__6)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 96
                self.match(DMFParser.T__5)
                self.state = 97
                localctx.x = self.expr(0)
                self.state = 98
                self.match(DMFParser.T__7)
                self.state = 99
                localctx.y = self.expr(0)
                self.state = 100
                self.match(DMFParser.T__6)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 102
                self.match(DMFParser.SUB)
                self.state = 103
                localctx.rhs = self.expr(28)
                pass

            elif la_ == 4:
                localctx = DMFParser.Const_rc_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 104
                localctx._INT = self.match(DMFParser.INT)
                self.state = 105
                self.rc((0 if localctx._INT is None else int(localctx._INT.text)))
                pass

            elif la_ == 5:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 106
                self.direction()
                self.state = 107
                localctx.dist = self.expr(17)
                pass

            elif la_ == 6:
                localctx = DMFParser.Dir_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 109
                self.direction()
                pass

            elif la_ == 7:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 110
                self.match(DMFParser.T__14)
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__39) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42))) != 0):
                    self.state = 111
                    self.axis()


                self.state = 114
                localctx.which = self.expr(15)
                pass

            elif la_ == 8:
                localctx = DMFParser.Pause_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 115
                self.match(DMFParser.T__0)
                self.state = 116
                localctx.duration = self.expr(14)
                pass

            elif la_ == 9:
                localctx = DMFParser.Well_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 117
                self.match(DMFParser.T__15)
                self.state = 118
                self.match(DMFParser.T__16)
                self.state = 119
                localctx.which = self.expr(13)
                pass

            elif la_ == 10:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 120
                self.match(DMFParser.T__19)
                self.state = 121
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__20 or _la==DMFParser.T__21):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 122
                localctx.loc = self.expr(11)
                pass

            elif la_ == 11:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 123
                self.macro_def()
                pass

            elif la_ == 12:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 125
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__22:
                    self.state = 124
                    self.match(DMFParser.T__22)


                self.state = 127
                _la = self._input.LA(1)
                if not(_la==DMFParser.OFF or _la==DMFParser.ON):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 13:
                localctx = DMFParser.Twiddle_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 128
                self.match(DMFParser.TOGGLE)
                self.state = 130
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                if la_ == 1:
                    self.state = 129
                    self.match(DMFParser.T__23)


                pass

            elif la_ == 14:
                localctx = DMFParser.Remove_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 132
                self.match(DMFParser.T__24)
                self.state = 138
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
                if la_ == 1:
                    self.state = 133
                    self.match(DMFParser.T__25)
                    self.state = 135
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==DMFParser.T__26:
                        self.state = 134
                        self.match(DMFParser.T__26)


                    self.state = 137
                    self.match(DMFParser.T__27)


                pass

            elif la_ == 15:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 141
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__26:
                    self.state = 140
                    self.match(DMFParser.T__26)


                self.state = 143
                self.param_type()
                pass

            elif la_ == 16:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 144
                self.param_type()
                self.state = 145
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 17:
                localctx = DMFParser.Function_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 147
                self.name()
                self.state = 148
                self.match(DMFParser.T__5)
                self.state = 157
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__5) | (1 << DMFParser.T__13) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__24) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__30) | (1 << DMFParser.T__31) | (1 << DMFParser.T__32) | (1 << DMFParser.T__33) | (1 << DMFParser.T__34) | (1 << DMFParser.T__35) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53) | (1 << DMFParser.T__58))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.OFF - 66)) | (1 << (DMFParser.ON - 66)) | (1 << (DMFParser.SUB - 66)) | (1 << (DMFParser.TOGGLE - 66)) | (1 << (DMFParser.ID - 66)) | (1 << (DMFParser.INT - 66)))) != 0):
                    self.state = 149
                    localctx._expr = self.expr(0)
                    localctx.args.append(localctx._expr)
                    self.state = 154
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==DMFParser.T__7:
                        self.state = 150
                        self.match(DMFParser.T__7)
                        self.state = 151
                        localctx._expr = self.expr(0)
                        localctx.args.append(localctx._expr)
                        self.state = 156
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)



                self.state = 159
                self.match(DMFParser.T__6)
                pass

            elif la_ == 18:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 161
                self.name()
                pass

            elif la_ == 19:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 162
                localctx._INT = self.match(DMFParser.INT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 199
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,16,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 197
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.In_dir_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 165
                        if not self.precpred(self._ctx, 24):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 24)")
                        self.state = 166
                        self.match(DMFParser.T__9)
                        self.state = 167
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__10 or _la==DMFParser.T__11):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 168
                        localctx.d = self.expr(25)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 169
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 170
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 171
                        localctx.rhs = self.expr(20)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 172
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 173
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 174
                        localctx.rhs = self.expr(19)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 175
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 176
                        self.match(DMFParser.INJECT)
                        self.state = 177
                        localctx.what = self.expr(11)
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 178
                        if not self.precpred(self._ctx, 27):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 27)")
                        self.state = 179
                        self.direction()
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Attr_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 180
                        if not self.precpred(self._ctx, 26):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 26)")
                        self.state = 181
                        self.match(DMFParser.ATTR)
                        self.state = 182
                        self.attr()
                        pass

                    elif la_ == 7:
                        localctx = DMFParser.Turn_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.start_dir = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 183
                        if not self.precpred(self._ctx, 25):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 25)")
                        self.state = 184
                        self.match(DMFParser.T__8)
                        self.state = 185
                        self.turn()
                        pass

                    elif la_ == 8:
                        localctx = DMFParser.N_rc_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 186
                        if not self.precpred(self._ctx, 22):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 22)")
                        self.state = 187
                        self.rc(0)
                        pass

                    elif la_ == 9:
                        localctx = DMFParser.Time_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.duration = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 188
                        if not self.precpred(self._ctx, 21):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 21)")
                        self.state = 189
                        self.time_unit()
                        pass

                    elif la_ == 10:
                        localctx = DMFParser.Ticks_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.duration = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 190
                        if not self.precpred(self._ctx, 20):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 20)")
                        self.state = 191
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__12 or _la==DMFParser.T__13):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        pass

                    elif la_ == 11:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 192
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 193
                        self.match(DMFParser.T__17)
                        self.state = 194
                        localctx.which = self.expr(0)
                        self.state = 195
                        self.match(DMFParser.T__18)
                        pass

             
                self.state = 201
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,16,self._ctx)

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
            self.state = 214
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__28, DMFParser.T__29]:
                self.enterOuterAlt(localctx, 1)
                self.state = 202
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__28 or _la==DMFParser.T__29):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__30, DMFParser.T__31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 205
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__30 or _la==DMFParser.T__31):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__32, DMFParser.T__33]:
                self.enterOuterAlt(localctx, 3)
                self.state = 208
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__32 or _la==DMFParser.T__33):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__34, DMFParser.T__35]:
                self.enterOuterAlt(localctx, 4)
                self.state = 211
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__34 or _la==DMFParser.T__35):
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
            self.state = 222
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__34, DMFParser.T__36]:
                self.enterOuterAlt(localctx, 1)
                self.state = 216
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__34 or _la==DMFParser.T__36):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.RIGHT
                pass
            elif token in [DMFParser.T__32, DMFParser.T__37]:
                self.enterOuterAlt(localctx, 2)
                self.state = 218
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__32 or _la==DMFParser.T__37):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.LEFT
                pass
            elif token in [DMFParser.T__38]:
                self.enterOuterAlt(localctx, 3)
                self.state = 220
                self.match(DMFParser.T__38)
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
            self.state = 238
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 224
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 225
                self.match(DMFParser.T__39)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 228
                self.match(DMFParser.T__40)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 231
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 232
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__41 or _la==DMFParser.T__42):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 235
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__43 or _la==DMFParser.T__44):
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
            self.state = 244
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__39]:
                self.enterOuterAlt(localctx, 1)
                self.state = 240
                self.match(DMFParser.T__39)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__41, DMFParser.T__42]:
                self.enterOuterAlt(localctx, 2)
                self.state = 242
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__41 or _la==DMFParser.T__42):
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
            self.state = 246
            self.macro_header()
            self.state = 249
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__1, DMFParser.T__3]:
                self.state = 247
                self.compound()
                pass
            elif token in [DMFParser.T__0, DMFParser.T__5, DMFParser.T__13, DMFParser.T__14, DMFParser.T__15, DMFParser.T__19, DMFParser.T__22, DMFParser.T__23, DMFParser.T__24, DMFParser.T__26, DMFParser.T__28, DMFParser.T__29, DMFParser.T__30, DMFParser.T__31, DMFParser.T__32, DMFParser.T__33, DMFParser.T__34, DMFParser.T__35, DMFParser.T__45, DMFParser.T__46, DMFParser.T__47, DMFParser.T__48, DMFParser.T__49, DMFParser.T__50, DMFParser.T__51, DMFParser.T__52, DMFParser.T__53, DMFParser.T__58, DMFParser.T__65, DMFParser.T__68, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT]:
                self.state = 248
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
            self.state = 251
            self.match(DMFParser.T__45)
            self.state = 252
            self.match(DMFParser.T__5)
            self.state = 261
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__13) | (1 << DMFParser.T__15) | (1 << DMFParser.T__19) | (1 << DMFParser.T__23) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53) | (1 << DMFParser.T__58))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.ID - 66)))) != 0):
                self.state = 253
                self.param()
                self.state = 258
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__7:
                    self.state = 254
                    self.match(DMFParser.T__7)
                    self.state = 255
                    self.param()
                    self.state = 260
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 263
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
        self.enterRule(localctx, 24, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.state = 277
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__13, DMFParser.T__15, DMFParser.T__19, DMFParser.T__23, DMFParser.T__46, DMFParser.T__47, DMFParser.T__48, DMFParser.T__49, DMFParser.T__50, DMFParser.T__51, DMFParser.T__52]:
                self.enterOuterAlt(localctx, 1)
                self.state = 265
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 269
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.INT:
                    self.state = 267
                    localctx._INT = self.match(DMFParser.INT)
                    localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))


                pass
            elif token in [DMFParser.T__53, DMFParser.T__58, DMFParser.T__65, DMFParser.T__68, DMFParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 271
                localctx._name = self.name()
                self.state = 272
                self.match(DMFParser.INJECT)
                self.state = 273
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
            self.state = 304
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,26,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 279
                self.match(DMFParser.T__19)
                localctx.type=Type.DROP
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 281
                self.match(DMFParser.T__46)
                localctx.type=Type.PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 283
                self.match(DMFParser.T__15)
                localctx.type=Type.WELL
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 285
                self.match(DMFParser.T__15)
                self.state = 286
                self.match(DMFParser.T__46)
                localctx.type=Type.WELL_PAD
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 288
                self.match(DMFParser.T__47)
                localctx.type=Type.INT
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 290
                self.match(DMFParser.T__23)
                localctx.type=Type.BINARY_STATE
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 292
                self.match(DMFParser.T__48)
                localctx.type=Type.BINARY_CPT
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 294
                self.match(DMFParser.T__49)
                localctx.type=Type.DELTA
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 296
                self.match(DMFParser.T__50)
                localctx.type=Type.MOTION
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 298
                self.match(DMFParser.T__51)
                localctx.type=Type.DELAY
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 300
                self.match(DMFParser.T__52)
                localctx.type=Type.TIME
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 302
                self.match(DMFParser.T__13)
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
        self.enterRule(localctx, 28, self.RULE_time_unit)
        self._la = 0 # Token type
        try:
            self.state = 310
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__53, DMFParser.T__54, DMFParser.T__55, DMFParser.T__56, DMFParser.T__57]:
                self.enterOuterAlt(localctx, 1)
                self.state = 306
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__53) | (1 << DMFParser.T__54) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56) | (1 << DMFParser.T__57))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.sec
                pass
            elif token in [DMFParser.T__58, DMFParser.T__59, DMFParser.T__60]:
                self.enterOuterAlt(localctx, 2)
                self.state = 308
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__58) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60))) != 0)):
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
            self.state = 343
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 312
                self.match(DMFParser.T__61)
                localctx.which=Attr.GATE
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 314
                self.match(DMFParser.T__62)
                self.state = 315
                self.match(DMFParser.T__46)
                localctx.which=Attr.EXIT_PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 317
                self.match(DMFParser.T__23)
                localctx.which=Attr.STATE
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 319
                self.match(DMFParser.T__63)
                localctx.which=Attr.DISTANCE
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 321
                self.match(DMFParser.T__64)
                localctx.which=Attr.DURATION
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 323
                self.match(DMFParser.T__46)
                localctx.which=Attr.PAD
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 328
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__39]:
                    self.state = 325
                    self.match(DMFParser.T__39)
                    pass
                elif token in [DMFParser.T__65]:
                    self.state = 326
                    self.match(DMFParser.T__65)
                    self.state = 327
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__66 or _la==DMFParser.T__67):
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
                self.state = 335
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__41]:
                    self.state = 331
                    self.match(DMFParser.T__41)
                    pass
                elif token in [DMFParser.T__42]:
                    self.state = 332
                    self.match(DMFParser.T__42)
                    pass
                elif token in [DMFParser.T__68]:
                    self.state = 333
                    self.match(DMFParser.T__68)
                    self.state = 334
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__66 or _la==DMFParser.T__67):
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
                self.state = 338
                self.match(DMFParser.T__15)
                localctx.which=Attr.WELL
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 340
                self.match(DMFParser.T__62)
                self.state = 341
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__10 or _la==DMFParser.T__11):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which=Attr.EXIT_DIR
                pass


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
        self.enterRule(localctx, 32, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 347
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.ID]:
                self.state = 345
                self.match(DMFParser.ID)
                pass
            elif token in [DMFParser.T__53, DMFParser.T__58, DMFParser.T__65, DMFParser.T__68]:
                self.state = 346
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
        self.enterRule(localctx, 34, self.RULE_kwd_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 349
            _la = self._input.LA(1)
            if not(((((_la - 54)) & ~0x3f) == 0 and ((1 << (_la - 54)) & ((1 << (DMFParser.T__53 - 54)) | (1 << (DMFParser.T__58 - 54)) | (1 << (DMFParser.T__65 - 54)) | (1 << (DMFParser.T__68 - 54)))) != 0)):
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
                return self.precpred(self._ctx, 24)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 19)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 27)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 26)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 25)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 22)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 21)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 20)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 12)
         

    def rc_sempred(self, localctx:RcContext, predIndex:int):
            if predIndex == 11:
                return localctx.n==1
         

            if predIndex == 12:
                return localctx.n==1
         




