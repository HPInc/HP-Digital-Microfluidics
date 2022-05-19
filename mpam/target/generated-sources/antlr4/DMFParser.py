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
from langsup.type_supp import Type, Rel, PhysUnit, EnvRelativeUnit
from quantities import SI


from mpam.types import Dir 


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\u009d")
        buf.write("\u029e\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\3\2\7\2:\n\2\f\2\16")
        buf.write("\2=\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\5\3F\n\3\3\3\3\3")
        buf.write("\3\3\3\3\5\3L\n\3\3\3\3\3\3\3\3\3\5\3R\n\3\3\3\3\3\3\3")
        buf.write("\5\3W\n\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4a\n\4\3\4")
        buf.write("\3\4\3\4\3\4\5\4g\n\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\5\4s\n\4\3\4\3\4\3\4\3\4\5\4y\n\4\3\4\3\4\3\4")
        buf.write("\5\4~\n\4\3\5\3\5\3\5\3\5\7\5\u0084\n\5\f\5\16\5\u0087")
        buf.write("\13\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\7\6\u009b\n\6\f\6\16\6\u009e")
        buf.write("\13\6\3\6\3\6\5\6\u00a2\n\6\3\6\3\6\3\6\3\6\3\6\5\6\u00a9")
        buf.write("\n\6\3\7\3\7\7\7\u00ad\n\7\f\7\16\7\u00b0\13\7\3\7\3\7")
        buf.write("\3\7\7\7\u00b5\n\7\f\7\16\7\u00b8\13\7\3\7\5\7\u00bb\n")
        buf.write("\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b")
        buf.write("\3\b\3\b\3\b\3\b\3\b\5\b\u00cf\n\b\3\t\3\t\3\t\3\t\5\t")
        buf.write("\u00d5\n\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u00ed")
        buf.write("\n\n\3\n\3\n\5\n\u00f1\n\n\3\n\5\n\u00f4\n\n\3\n\3\n\5")
        buf.write("\n\u00f8\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u0103")
        buf.write("\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u010e\n\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\5\n\u0123\n\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\5\n\u0139\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\7\n\u0159\n\n\f\n\16")
        buf.write("\n\u015c\13\n\5\n\u015e\n\n\3\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\5\n\u016b\n\n\3\n\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n")
        buf.write("\3\n\3\n\3\n\3\n\3\n\7\n\u0185\n\n\f\n\16\n\u0188\13\n")
        buf.write("\3\13\3\13\3\13\3\13\5\13\u018e\n\13\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f\u019c\n\f\3\r\3\r\3")
        buf.write("\r\3\r\3\r\3\r\5\r\u01a4\n\r\3\16\3\16\3\16\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3\16\5\16\u01b4")
        buf.write("\n\16\3\17\3\17\3\17\3\17\5\17\u01ba\n\17\3\20\3\20\3")
        buf.write("\20\5\20\u01bf\n\20\3\21\3\21\3\21\3\21\3\21\7\21\u01c6")
        buf.write("\n\21\f\21\16\21\u01c9\13\21\5\21\u01cb\n\21\3\21\3\21")
        buf.write("\3\22\5\22\u01d0\n\22\3\22\3\22\3\22\3\22\3\22\3\22\3")
        buf.write("\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22\3\22")
        buf.write("\3\22\3\22\3\22\5\22\u01e6\n\22\3\23\5\23\u01e9\n\23\3")
        buf.write("\23\3\23\3\23\5\23\u01ee\n\23\3\23\3\23\3\23\3\23\5\23")
        buf.write("\u01f4\n\23\3\23\3\23\3\23\3\23\5\23\u01fa\n\23\3\23\5")
        buf.write("\23\u01fd\n\23\3\23\5\23\u0200\n\23\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\5\24\u020c\n\24\3\24\3")
        buf.write("\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\5\24\u0233\n\24\3\24\5\24\u0236\n\24\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\5\25\u0244\n\25\3\26\3\26\3\26\3\26\3\26\3\26\3")
        buf.write("\26\3\26\3\26\3\26\5\26\u0250\n\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\5\26\u0257\n\26\3\26\3\26\3\26\3\26\3\26\3\26\3")
        buf.write("\26\3\26\3\26\5\26\u0262\n\26\3\26\3\26\5\26\u0266\n\26")
        buf.write("\3\26\3\26\3\26\3\26\5\26\u026c\n\26\3\27\3\27\3\27\3")
        buf.write("\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\5\27\u027a")
        buf.write("\n\27\3\30\3\30\3\30\3\30\5\30\u0280\n\30\3\31\3\31\3")
        buf.write("\31\3\31\3\31\3\31\3\31\3\31\5\31\u028a\n\31\3\32\3\32")
        buf.write("\5\32\u028e\n\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3")
        buf.write("\32\5\32\u0298\n\32\3\33\3\33\3\34\3\34\3\34\2\3\22\35")
        buf.write("\2\4\6\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\60\62")
        buf.write("\64\66\2\35\4\2\30\30\36\36\3\2)*\3\2\33\34\4\2\u008a")
        buf.write("\u008a\u008e\u008e\4\2\u0087\u0087\u0092\u0092\4\2\30")
        buf.write("\30##\3\2-.\3\2/\60\3\2\61\62\3\2\63\64\4\2\63\63\65\65")
        buf.write("\4\2\61\61\66\66\3\2:;\3\2<=\3\2QR\4\2IIST\3\2VZ\3\2[")
        buf.write("]\3\2^c\3\2di\4\2MMjj\4\2((kk\3\2no\b\2\23\23\37\37((")
        buf.write("DDOO\u0097\u0097\3\2{\u0080\3\2\u0081\u0086\7\2IISV[[")
        buf.write("mmpp\2\u0327\2;\3\2\2\2\4V\3\2\2\2\6}\3\2\2\2\b\177\3")
        buf.write("\2\2\2\n\u00a8\3\2\2\2\f\u00ba\3\2\2\2\16\u00ce\3\2\2")
        buf.write("\2\20\u00d4\3\2\2\2\22\u0122\3\2\2\2\24\u018d\3\2\2\2")
        buf.write("\26\u019b\3\2\2\2\30\u01a3\3\2\2\2\32\u01b3\3\2\2\2\34")
        buf.write("\u01b9\3\2\2\2\36\u01bb\3\2\2\2 \u01c0\3\2\2\2\"\u01e5")
        buf.write("\3\2\2\2$\u01ff\3\2\2\2&\u0235\3\2\2\2(\u0243\3\2\2\2")
        buf.write("*\u026b\3\2\2\2,\u0279\3\2\2\2.\u027f\3\2\2\2\60\u0289")
        buf.write("\3\2\2\2\62\u0297\3\2\2\2\64\u0299\3\2\2\2\66\u029b\3")
        buf.write("\2\2\28:\5\n\6\298\3\2\2\2:=\3\2\2\2;9\3\2\2\2;<\3\2\2")
        buf.write("\2<>\3\2\2\2=;\3\2\2\2>?\7\2\2\3?\3\3\2\2\2@A\5\f\7\2")
        buf.write("AB\7\2\2\3BW\3\2\2\2CE\5\6\4\2DF\7\u0093\2\2ED\3\2\2\2")
        buf.write("EF\3\2\2\2FG\3\2\2\2GH\7\2\2\3HW\3\2\2\2IK\5\b\5\2JL\7")
        buf.write("\u0093\2\2KJ\3\2\2\2KL\3\2\2\2LM\3\2\2\2MN\7\2\2\3NW\3")
        buf.write("\2\2\2OQ\5\22\n\2PR\7\u0093\2\2QP\3\2\2\2QR\3\2\2\2RS")
        buf.write("\3\2\2\2ST\7\2\2\3TW\3\2\2\2UW\7\2\2\3V@\3\2\2\2VC\3\2")
        buf.write("\2\2VI\3\2\2\2VO\3\2\2\2VU\3\2\2\2W\5\3\2\2\2XY\7\u008d")
        buf.write("\2\2YZ\5\60\31\2Z[\7\u0088\2\2[\\\5\22\n\2\\]\b\4\1\2")
        buf.write("]^\b\4\1\2^~\3\2\2\2_a\7\u008d\2\2`_\3\2\2\2`a\3\2\2\2")
        buf.write("ab\3\2\2\2bc\5&\24\2cd\7\u0098\2\2df\7\u0088\2\2eg\5\22")
        buf.write("\n\2fe\3\2\2\2fg\3\2\2\2gh\3\2\2\2hi\b\4\1\2ij\b\4\1\2")
        buf.write("j~\3\2\2\2kl\7\u008d\2\2lm\5&\24\2mn\7\u0098\2\2no\b\4")
        buf.write("\1\2op\b\4\1\2p~\3\2\2\2qs\7\u008d\2\2rq\3\2\2\2rs\3\2")
        buf.write("\2\2st\3\2\2\2tu\5&\24\2ux\5\60\31\2vw\7\u0088\2\2wy\5")
        buf.write("\22\n\2xv\3\2\2\2xy\3\2\2\2yz\3\2\2\2z{\b\4\1\2{|\b\4")
        buf.write("\1\2|~\3\2\2\2}X\3\2\2\2}`\3\2\2\2}k\3\2\2\2}r\3\2\2\2")
        buf.write("~\7\3\2\2\2\177\u0080\7\3\2\2\u0080\u0085\5\22\n\2\u0081")
        buf.write("\u0082\7\4\2\2\u0082\u0084\5\22\n\2\u0083\u0081\3\2\2")
        buf.write("\2\u0084\u0087\3\2\2\2\u0085\u0083\3\2\2\2\u0085\u0086")
        buf.write("\3\2\2\2\u0086\t\3\2\2\2\u0087\u0085\3\2\2\2\u0088\u0089")
        buf.write("\5\6\4\2\u0089\u008a\7\u0093\2\2\u008a\u00a9\3\2\2\2\u008b")
        buf.write("\u008c\7\5\2\2\u008c\u008d\5\22\n\2\u008d\u008e\7\u0093")
        buf.write("\2\2\u008e\u00a9\3\2\2\2\u008f\u0090\5\b\5\2\u0090\u0091")
        buf.write("\7\u0093\2\2\u0091\u00a9\3\2\2\2\u0092\u0093\7\6\2\2\u0093")
        buf.write("\u0094\5\22\n\2\u0094\u009c\5\f\7\2\u0095\u0096\7\7\2")
        buf.write("\2\u0096\u0097\7\6\2\2\u0097\u0098\5\22\n\2\u0098\u0099")
        buf.write("\5\f\7\2\u0099\u009b\3\2\2\2\u009a\u0095\3\2\2\2\u009b")
        buf.write("\u009e\3\2\2\2\u009c\u009a\3\2\2\2\u009c\u009d\3\2\2\2")
        buf.write("\u009d\u00a1\3\2\2\2\u009e\u009c\3\2\2\2\u009f\u00a0\7")
        buf.write("\7\2\2\u00a0\u00a2\5\f\7\2\u00a1\u009f\3\2\2\2\u00a1\u00a2")
        buf.write("\3\2\2\2\u00a2\u00a9\3\2\2\2\u00a3\u00a4\5\22\n\2\u00a4")
        buf.write("\u00a5\7\u0093\2\2\u00a5\u00a9\3\2\2\2\u00a6\u00a9\5\16")
        buf.write("\b\2\u00a7\u00a9\5\f\7\2\u00a8\u0088\3\2\2\2\u00a8\u008b")
        buf.write("\3\2\2\2\u00a8\u008f\3\2\2\2\u00a8\u0092\3\2\2\2\u00a8")
        buf.write("\u00a3\3\2\2\2\u00a8\u00a6\3\2\2\2\u00a8\u00a7\3\2\2\2")
        buf.write("\u00a9\13\3\2\2\2\u00aa\u00ae\7\b\2\2\u00ab\u00ad\5\n")
        buf.write("\6\2\u00ac\u00ab\3\2\2\2\u00ad\u00b0\3\2\2\2\u00ae\u00ac")
        buf.write("\3\2\2\2\u00ae\u00af\3\2\2\2\u00af\u00b1\3\2\2\2\u00b0")
        buf.write("\u00ae\3\2\2\2\u00b1\u00bb\7\t\2\2\u00b2\u00b6\7\n\2\2")
        buf.write("\u00b3\u00b5\5\n\6\2\u00b4\u00b3\3\2\2\2\u00b5\u00b8\3")
        buf.write("\2\2\2\u00b6\u00b4\3\2\2\2\u00b6\u00b7\3\2\2\2\u00b7\u00b9")
        buf.write("\3\2\2\2\u00b8\u00b6\3\2\2\2\u00b9\u00bb\7\13\2\2\u00ba")
        buf.write("\u00aa\3\2\2\2\u00ba\u00b2\3\2\2\2\u00bb\r\3\2\2\2\u00bc")
        buf.write("\u00bd\7\f\2\2\u00bd\u00be\5\22\n\2\u00be\u00bf\7\r\2")
        buf.write("\2\u00bf\u00c0\5\n\6\2\u00c0\u00cf\3\2\2\2\u00c1\u00c2")
        buf.write("\7\16\2\2\u00c2\u00c3\5\60\31\2\u00c3\u00c4\7\17\2\2\u00c4")
        buf.write("\u00c5\7\20\2\2\u00c5\u00c6\5\22\n\2\u00c6\u00c7\7\4\2")
        buf.write("\2\u00c7\u00c8\5\22\n\2\u00c8\u00c9\5\20\t\2\u00c9\u00ca")
        buf.write("\7\21\2\2\u00ca\u00cb\5\22\n\2\u00cb\u00cc\3\2\2\2\u00cc")
        buf.write("\u00cd\5\n\6\2\u00cd\u00cf\3\2\2\2\u00ce\u00bc\3\2\2\2")
        buf.write("\u00ce\u00c1\3\2\2\2\u00cf\17\3\2\2\2\u00d0\u00d1\7\u0095")
        buf.write("\2\2\u00d1\u00d5\b\t\1\2\u00d2\u00d3\7\u0096\2\2\u00d3")
        buf.write("\u00d5\b\t\1\2\u00d4\u00d0\3\2\2\2\u00d4\u00d2\3\2\2\2")
        buf.write("\u00d5\21\3\2\2\2\u00d6\u00d7\b\n\1\2\u00d7\u00d8\7\22")
        buf.write("\2\2\u00d8\u00d9\5\22\n\2\u00d9\u00da\7\u0096\2\2\u00da")
        buf.write("\u0123\3\2\2\2\u00db\u00dc\7\22\2\2\u00dc\u00dd\5\22\n")
        buf.write("\2\u00dd\u00de\7\4\2\2\u00de\u00df\5\22\n\2\u00df\u00e0")
        buf.write("\7\u0096\2\2\u00e0\u0123\3\2\2\2\u00e1\u00e2\7\u0092\2")
        buf.write("\2\u00e2\u0123\5\22\n\60\u00e3\u00e4\7\23\2\2\u00e4\u00e5")
        buf.write("\7\24\2\2\u00e5\u0123\5\22\n.\u00e6\u00e7\7\25\2\2\u00e7")
        buf.write("\u00e8\7\24\2\2\u00e8\u0123\5\22\n-\u00e9\u00ea\7\u0098")
        buf.write("\2\2\u00ea\u0123\5\32\16\2\u00eb\u00ed\7\36\2\2\u00ec")
        buf.write("\u00eb\3\2\2\2\u00ec\u00ed\3\2\2\2\u00ed\u00ee\3\2\2\2")
        buf.write("\u00ee\u00f0\5\24\13\2\u00ef\u00f1\7\37\2\2\u00f0\u00ef")
        buf.write("\3\2\2\2\u00f0\u00f1\3\2\2\2\u00f1\u0123\3\2\2\2\u00f2")
        buf.write("\u00f4\t\2\2\2\u00f3\u00f2\3\2\2\2\u00f3\u00f4\3\2\2\2")
        buf.write("\u00f4\u00f5\3\2\2\2\u00f5\u00f7\7\37\2\2\u00f6\u00f8")
        buf.write("\7 \2\2\u00f7\u00f6\3\2\2\2\u00f7\u00f8\3\2\2\2\u00f8")
        buf.write("\u00f9\3\2\2\2\u00f9\u0123\5\22\n\"\u00fa\u00fb\7\u008f")
        buf.write("\2\2\u00fb\u0123\5\22\n\33\u00fc\u00fd\5\26\f\2\u00fd")
        buf.write("\u00fe\5\22\n\30\u00fe\u0123\3\2\2\2\u00ff\u0123\5\26")
        buf.write("\f\2\u0100\u0102\7\'\2\2\u0101\u0103\5\34\17\2\u0102\u0101")
        buf.write("\3\2\2\2\u0102\u0103\3\2\2\2\u0103\u0104\3\2\2\2\u0104")
        buf.write("\u0123\5\22\n\26\u0105\u0106\7\5\2\2\u0106\u0123\5\22")
        buf.write("\n\25\u0107\u0108\7(\2\2\u0108\u0109\t\3\2\2\u0109\u0123")
        buf.write("\5\22\n\23\u010a\u0123\5\36\20\2\u010b\u0123\5$\23\2\u010c")
        buf.write("\u010e\7\36\2\2\u010d\u010c\3\2\2\2\u010d\u010e\3\2\2")
        buf.write("\2\u010e\u010f\3\2\2\2\u010f\u0123\5&\24\2\u0110\u0111")
        buf.write("\5&\24\2\u0111\u0112\7\u0098\2\2\u0112\u0123\3\2\2\2\u0113")
        buf.write("\u0123\5.\30\2\u0114\u0123\5\60\31\2\u0115\u0123\5\62")
        buf.write("\32\2\u0116\u0117\5\60\31\2\u0117\u0118\7\u0088\2\2\u0118")
        buf.write("\u0119\5\22\n\b\u0119\u0123\3\2\2\2\u011a\u011b\5&\24")
        buf.write("\2\u011b\u011c\7\u0098\2\2\u011c\u011d\7\u0088\2\2\u011d")
        buf.write("\u011e\5\22\n\6\u011e\u0123\3\2\2\2\u011f\u0123\5\66\34")
        buf.write("\2\u0120\u0123\7\u0098\2\2\u0121\u0123\7\u0099\2\2\u0122")
        buf.write("\u00d6\3\2\2\2\u0122\u00db\3\2\2\2\u0122\u00e1\3\2\2\2")
        buf.write("\u0122\u00e3\3\2\2\2\u0122\u00e6\3\2\2\2\u0122\u00e9\3")
        buf.write("\2\2\2\u0122\u00ec\3\2\2\2\u0122\u00f3\3\2\2\2\u0122\u00fa")
        buf.write("\3\2\2\2\u0122\u00fc\3\2\2\2\u0122\u00ff\3\2\2\2\u0122")
        buf.write("\u0100\3\2\2\2\u0122\u0105\3\2\2\2\u0122\u0107\3\2\2\2")
        buf.write("\u0122\u010a\3\2\2\2\u0122\u010b\3\2\2\2\u0122\u010d\3")
        buf.write("\2\2\2\u0122\u0110\3\2\2\2\u0122\u0113\3\2\2\2\u0122\u0114")
        buf.write("\3\2\2\2\u0122\u0115\3\2\2\2\u0122\u0116\3\2\2\2\u0122")
        buf.write("\u011a\3\2\2\2\u0122\u011f\3\2\2\2\u0122\u0120\3\2\2\2")
        buf.write("\u0122\u0121\3\2\2\2\u0123\u0186\3\2\2\2\u0124\u0125\f")
        buf.write("(\2\2\u0125\u0126\7\17\2\2\u0126\u0127\t\4\2\2\u0127\u0185")
        buf.write("\5\22\n)\u0128\u0129\f!\2\2\u0129\u012a\7!\2\2\u012a\u0185")
        buf.write("\5\22\n\"\u012b\u012c\f \2\2\u012c\u012d\t\5\2\2\u012d")
        buf.write("\u0185\5\22\n!\u012e\u012f\f\37\2\2\u012f\u0130\t\6\2")
        buf.write("\2\u0130\u0185\5\22\n \u0131\u0132\f\36\2\2\u0132\u0133")
        buf.write("\5,\27\2\u0133\u0134\5\22\n\37\u0134\u0185\3\2\2\2\u0135")
        buf.write("\u0136\f\34\2\2\u0136\u0138\7$\2\2\u0137\u0139\7\u008f")
        buf.write("\2\2\u0138\u0137\3\2\2\2\u0138\u0139\3\2\2\2\u0139\u013a")
        buf.write("\3\2\2\2\u013a\u0185\5\22\n\35\u013b\u013c\f\32\2\2\u013c")
        buf.write("\u013d\7%\2\2\u013d\u0185\5\22\n\33\u013e\u013f\f\31\2")
        buf.write("\2\u013f\u0140\7&\2\2\u0140\u0185\5\22\n\32\u0141\u0142")
        buf.write("\f\22\2\2\u0142\u0143\t\3\2\2\u0143\u0185\5\22\n\23\u0144")
        buf.write("\u0145\f\21\2\2\u0145\u0146\7\u008c\2\2\u0146\u0185\5")
        buf.write("\22\n\22\u0147\u0148\f\20\2\2\u0148\u0149\7\6\2\2\u0149")
        buf.write("\u014a\5\22\n\2\u014a\u014b\7\7\2\2\u014b\u014c\5\22\n")
        buf.write("\21\u014c\u0185\3\2\2\2\u014d\u014e\f\7\2\2\u014e\u014f")
        buf.write("\7\u0089\2\2\u014f\u0150\5*\26\2\u0150\u0151\7\u0088\2")
        buf.write("\2\u0151\u0152\5\22\n\b\u0152\u0185\3\2\2\2\u0153\u0154")
        buf.write("\f\62\2\2\u0154\u015d\7\22\2\2\u0155\u015a\5\22\n\2\u0156")
        buf.write("\u0157\7\4\2\2\u0157\u0159\5\22\n\2\u0158\u0156\3\2\2")
        buf.write("\2\u0159\u015c\3\2\2\2\u015a\u0158\3\2\2\2\u015a\u015b")
        buf.write("\3\2\2\2\u015b\u015e\3\2\2\2\u015c\u015a\3\2\2\2\u015d")
        buf.write("\u0155\3\2\2\2\u015d\u015e\3\2\2\2\u015e\u015f\3\2\2\2")
        buf.write("\u015f\u0185\7\u0096\2\2\u0160\u0161\f/\2\2\u0161\u0185")
        buf.write("\5\26\f\2\u0162\u0163\f,\2\2\u0163\u0164\7\u0089\2\2\u0164")
        buf.write("\u0165\7\26\2\2\u0165\u0166\7\17\2\2\u0166\u0185\5(\25")
        buf.write("\2\u0167\u0168\f+\2\2\u0168\u016a\7\27\2\2\u0169\u016b")
        buf.write("\7\30\2\2\u016a\u0169\3\2\2\2\u016a\u016b\3\2\2\2\u016b")
        buf.write("\u016c\3\2\2\2\u016c\u016d\7\31\2\2\u016d\u016e\7\17\2")
        buf.write("\2\u016e\u0185\5(\25\2\u016f\u0170\f*\2\2\u0170\u0171")
        buf.write("\7\u0089\2\2\u0171\u0185\5*\26\2\u0172\u0173\f)\2\2\u0173")
        buf.write("\u0174\7\32\2\2\u0174\u0185\5\30\r\2\u0175\u0176\f&\2")
        buf.write("\2\u0176\u0185\5\32\16\2\u0177\u0178\f%\2\2\u0178\u0185")
        buf.write("\5(\25\2\u0179\u017a\f$\2\2\u017a\u0185\7\35\2\2\u017b")
        buf.write("\u017c\f\35\2\2\u017c\u017d\7\"\2\2\u017d\u017e\t\7\2")
        buf.write("\2\u017e\u0185\5*\26\2\u017f\u0180\f\24\2\2\u0180\u0181")
        buf.write("\7\20\2\2\u0181\u0182\5\22\n\2\u0182\u0183\7\u0095\2\2")
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
        buf.write("\3\2\2\2\u0188\u0186\3\2\2\2\u0189\u018a\7+\2\2\u018a")
        buf.write("\u018e\b\13\1\2\u018b\u018c\7,\2\2\u018c\u018e\b\13\1")
        buf.write("\2\u018d\u0189\3\2\2\2\u018d\u018b\3\2\2\2\u018e\25\3")
        buf.write("\2\2\2\u018f\u0190\t\b\2\2\u0190\u0191\b\f\1\2\u0191\u019c")
        buf.write("\b\f\1\2\u0192\u0193\t\t\2\2\u0193\u0194\b\f\1\2\u0194")
        buf.write("\u019c\b\f\1\2\u0195\u0196\t\n\2\2\u0196\u0197\b\f\1\2")
        buf.write("\u0197\u019c\b\f\1\2\u0198\u0199\t\13\2\2\u0199\u019a")
        buf.write("\b\f\1\2\u019a\u019c\b\f\1\2\u019b\u018f\3\2\2\2\u019b")
        buf.write("\u0192\3\2\2\2\u019b\u0195\3\2\2\2\u019b\u0198\3\2\2\2")
        buf.write("\u019c\27\3\2\2\2\u019d\u019e\t\f\2\2\u019e\u01a4\b\r")
        buf.write("\1\2\u019f\u01a0\t\r\2\2\u01a0\u01a4\b\r\1\2\u01a1\u01a2")
        buf.write("\7\67\2\2\u01a2\u01a4\b\r\1\2\u01a3\u019d\3\2\2\2\u01a3")
        buf.write("\u019f\3\2\2\2\u01a3\u01a1\3\2\2\2\u01a4\31\3\2\2\2\u01a5")
        buf.write("\u01a6\6\16\31\3\u01a6\u01a7\78\2\2\u01a7\u01a8\b\16\1")
        buf.write("\2\u01a8\u01b4\b\16\1\2\u01a9\u01aa\79\2\2\u01aa\u01ab")
        buf.write("\b\16\1\2\u01ab\u01b4\b\16\1\2\u01ac\u01ad\6\16\32\3\u01ad")
        buf.write("\u01ae\t\16\2\2\u01ae\u01af\b\16\1\2\u01af\u01b4\b\16")
        buf.write("\1\2\u01b0\u01b1\t\17\2\2\u01b1\u01b2\b\16\1\2\u01b2\u01b4")
        buf.write("\b\16\1\2\u01b3\u01a5\3\2\2\2\u01b3\u01a9\3\2\2\2\u01b3")
        buf.write("\u01ac\3\2\2\2\u01b3\u01b0\3\2\2\2\u01b4\33\3\2\2\2\u01b5")
        buf.write("\u01b6\78\2\2\u01b6\u01ba\b\17\1\2\u01b7\u01b8\t\16\2")
        buf.write("\2\u01b8\u01ba\b\17\1\2\u01b9\u01b5\3\2\2\2\u01b9\u01b7")
        buf.write("\3\2\2\2\u01ba\35\3\2\2\2\u01bb\u01be\5 \21\2\u01bc\u01bf")
        buf.write("\5\f\7\2\u01bd\u01bf\5\22\n\2\u01be\u01bc\3\2\2\2\u01be")
        buf.write("\u01bd\3\2\2\2\u01bf\37\3\2\2\2\u01c0\u01c1\7>\2\2\u01c1")
        buf.write("\u01ca\7\22\2\2\u01c2\u01c7\5\"\22\2\u01c3\u01c4\7\4\2")
        buf.write("\2\u01c4\u01c6\5\"\22\2\u01c5\u01c3\3\2\2\2\u01c6\u01c9")
        buf.write("\3\2\2\2\u01c7\u01c5\3\2\2\2\u01c7\u01c8\3\2\2\2\u01c8")
        buf.write("\u01cb\3\2\2\2\u01c9\u01c7\3\2\2\2\u01ca\u01c2\3\2\2\2")
        buf.write("\u01ca\u01cb\3\2\2\2\u01cb\u01cc\3\2\2\2\u01cc\u01cd\7")
        buf.write("\u0096\2\2\u01cd!\3\2\2\2\u01ce\u01d0\t\7\2\2\u01cf\u01ce")
        buf.write("\3\2\2\2\u01cf\u01d0\3\2\2\2\u01d0\u01d1\3\2\2\2\u01d1")
        buf.write("\u01d2\5&\24\2\u01d2\u01d3\b\22\1\2\u01d3\u01e6\3\2\2")
        buf.write("\2\u01d4\u01d5\5&\24\2\u01d5\u01d6\b\22\1\2\u01d6\u01d7")
        buf.write("\7\u0098\2\2\u01d7\u01d8\b\22\1\2\u01d8\u01e6\3\2\2\2")
        buf.write("\u01d9\u01da\5&\24\2\u01da\u01db\5\60\31\2\u01db\u01dc")
        buf.write("\b\22\1\2\u01dc\u01dd\b\22\1\2\u01dd\u01e6\3\2\2\2\u01de")
        buf.write("\u01df\5\60\31\2\u01df\u01e0\7\u008c\2\2\u01e0\u01e1\5")
        buf.write("&\24\2\u01e1\u01e2\b\22\1\2\u01e2\u01e3\b\22\1\2\u01e3")
        buf.write("\u01e4\b\22\1\2\u01e4\u01e6\3\2\2\2\u01e5\u01cf\3\2\2")
        buf.write("\2\u01e5\u01d4\3\2\2\2\u01e5\u01d9\3\2\2\2\u01e5\u01de")
        buf.write("\3\2\2\2\u01e6#\3\2\2\2\u01e7\u01e9\7?\2\2\u01e8\u01e7")
        buf.write("\3\2\2\2\u01e8\u01e9\3\2\2\2\u01e9\u01ea\3\2\2\2\u01ea")
        buf.write("\u01eb\7\u0091\2\2\u01eb\u0200\b\23\1\2\u01ec\u01ee\7")
        buf.write("?\2\2\u01ed\u01ec\3\2\2\2\u01ed\u01ee\3\2\2\2\u01ee\u01ef")
        buf.write("\3\2\2\2\u01ef\u01f0\7\u0090\2\2\u01f0\u0200\b\23\1\2")
        buf.write("\u01f1\u01f3\7\u0094\2\2\u01f2\u01f4\7@\2\2\u01f3\u01f2")
        buf.write("\3\2\2\2\u01f3\u01f4\3\2\2\2\u01f4\u01f5\3\2\2\2\u01f5")
        buf.write("\u0200\b\23\1\2\u01f6\u01fc\7A\2\2\u01f7\u01f9\7B\2\2")
        buf.write("\u01f8\u01fa\7\36\2\2\u01f9\u01f8\3\2\2\2\u01f9\u01fa")
        buf.write("\3\2\2\2\u01fa\u01fb\3\2\2\2\u01fb\u01fd\7C\2\2\u01fc")
        buf.write("\u01f7\3\2\2\2\u01fc\u01fd\3\2\2\2\u01fd\u01fe\3\2\2\2")
        buf.write("\u01fe\u0200\b\23\1\2\u01ff\u01e8\3\2\2\2\u01ff\u01ed")
        buf.write("\3\2\2\2\u01ff\u01f1\3\2\2\2\u01ff\u01f6\3\2\2\2\u0200")
        buf.write("%\3\2\2\2\u0201\u0202\7(\2\2\u0202\u0236\b\24\1\2\u0203")
        buf.write("\u0204\7D\2\2\u0204\u0236\b\24\1\2\u0205\u0206\7\23\2")
        buf.write("\2\u0206\u0236\b\24\1\2\u0207\u0208\7\23\2\2\u0208\u0209")
        buf.write("\7D\2\2\u0209\u0236\b\24\1\2\u020a\u020c\7\23\2\2\u020b")
        buf.write("\u020a\3\2\2\2\u020b\u020c\3\2\2\2\u020c\u020d\3\2\2\2")
        buf.write("\u020d\u020e\7E\2\2\u020e\u0236\b\24\1\2\u020f\u0210\7")
        buf.write("F\2\2\u0210\u0236\b\24\1\2\u0211\u0212\7G\2\2\u0212\u0236")
        buf.write("\b\24\1\2\u0213\u0214\7\31\2\2\u0214\u0236\b\24\1\2\u0215")
        buf.write("\u0216\7@\2\2\u0216\u0236\b\24\1\2\u0217\u0218\7H\2\2")
        buf.write("\u0218\u0236\b\24\1\2\u0219\u021a\7I\2\2\u021a\u0236\b")
        buf.write("\24\1\2\u021b\u021c\7J\2\2\u021c\u0236\b\24\1\2\u021d")
        buf.write("\u021e\7K\2\2\u021e\u0236\b\24\1\2\u021f\u0220\7L\2\2")
        buf.write("\u0220\u0236\b\24\1\2\u0221\u0222\7M\2\2\u0222\u0236\b")
        buf.write("\24\1\2\u0223\u0224\7N\2\2\u0224\u0236\b\24\1\2\u0225")
        buf.write("\u0226\t\4\2\2\u0226\u0236\b\24\1\2\u0227\u0228\7O\2\2")
        buf.write("\u0228\u0236\b\24\1\2\u0229\u022a\7\37\2\2\u022a\u0236")
        buf.write("\b\24\1\2\u022b\u022c\7P\2\2\u022c\u0236\b\24\1\2\u022d")
        buf.write("\u022e\t\20\2\2\u022e\u022f\t\21\2\2\u022f\u0236\b\24")
        buf.write("\1\2\u0230\u0232\t\20\2\2\u0231\u0233\7U\2\2\u0232\u0231")
        buf.write("\3\2\2\2\u0232\u0233\3\2\2\2\u0233\u0234\3\2\2\2\u0234")
        buf.write("\u0236\b\24\1\2\u0235\u0201\3\2\2\2\u0235\u0203\3\2\2")
        buf.write("\2\u0235\u0205\3\2\2\2\u0235\u0207\3\2\2\2\u0235\u020b")
        buf.write("\3\2\2\2\u0235\u020f\3\2\2\2\u0235\u0211\3\2\2\2\u0235")
        buf.write("\u0213\3\2\2\2\u0235\u0215\3\2\2\2\u0235\u0217\3\2\2\2")
        buf.write("\u0235\u0219\3\2\2\2\u0235\u021b\3\2\2\2\u0235\u021d\3")
        buf.write("\2\2\2\u0235\u021f\3\2\2\2\u0235\u0221\3\2\2\2\u0235\u0223")
        buf.write("\3\2\2\2\u0235\u0225\3\2\2\2\u0235\u0227\3\2\2\2\u0235")
        buf.write("\u0229\3\2\2\2\u0235\u022b\3\2\2\2\u0235\u022d\3\2\2\2")
        buf.write("\u0235\u0230\3\2\2\2\u0236\'\3\2\2\2\u0237\u0238\t\22")
        buf.write("\2\2\u0238\u0244\b\25\1\2\u0239\u023a\t\23\2\2\u023a\u0244")
        buf.write("\b\25\1\2\u023b\u023c\t\24\2\2\u023c\u0244\b\25\1\2\u023d")
        buf.write("\u023e\t\25\2\2\u023e\u0244\b\25\1\2\u023f\u0240\t\26")
        buf.write("\2\2\u0240\u0244\b\25\1\2\u0241\u0242\t\27\2\2\u0242\u0244")
        buf.write("\b\25\1\2\u0243\u0237\3\2\2\2\u0243\u0239\3\2\2\2\u0243")
        buf.write("\u023b\3\2\2\2\u0243\u023d\3\2\2\2\u0243\u023f\3\2\2\2")
        buf.write("\u0243\u0241\3\2\2\2\u0244)\3\2\2\2\u0245\u0246\7l\2\2")
        buf.write("\u0246\u0247\7D\2\2\u0247\u026c\b\26\1\2\u0248\u0249\7")
        buf.write("E\2\2\u0249\u026c\b\26\1\2\u024a\u024b\t\4\2\2\u024b\u026c")
        buf.write("\b\26\1\2\u024c\u0250\78\2\2\u024d\u024e\7m\2\2\u024e")
        buf.write("\u0250\t\30\2\2\u024f\u024c\3\2\2\2\u024f\u024d\3\2\2")
        buf.write("\2\u0250\u0251\3\2\2\2\u0251\u026c\b\26\1\2\u0252\u0257")
        buf.write("\7:\2\2\u0253\u0257\7;\2\2\u0254\u0255\7p\2\2\u0255\u0257")
        buf.write("\t\30\2\2\u0256\u0252\3\2\2\2\u0256\u0253\3\2\2\2\u0256")
        buf.write("\u0254\3\2\2\2\u0257\u0258\3\2\2\2\u0258\u026c\b\26\1")
        buf.write("\2\u0259\u025a\7l\2\2\u025a\u025b\t\4\2\2\u025b\u026c")
        buf.write("\b\26\1\2\u025c\u025d\7q\2\2\u025d\u025e\7r\2\2\u025e")
        buf.write("\u026c\b\26\1\2\u025f\u0261\7s\2\2\u0260\u0262\t\20\2")
        buf.write("\2\u0261\u0260\3\2\2\2\u0261\u0262\3\2\2\2\u0262\u0263")
        buf.write("\3\2\2\2\u0263\u026c\b\26\1\2\u0264\u0266\7t\2\2\u0265")
        buf.write("\u0264\3\2\2\2\u0265\u0266\3\2\2\2\u0266\u0267\3\2\2\2")
        buf.write("\u0267\u0268\t\20\2\2\u0268\u026c\b\26\1\2\u0269\u026a")
        buf.write("\t\31\2\2\u026a\u026c\b\26\1\2\u026b\u0245\3\2\2\2\u026b")
        buf.write("\u0248\3\2\2\2\u026b\u024a\3\2\2\2\u026b\u024f\3\2\2\2")
        buf.write("\u026b\u0256\3\2\2\2\u026b\u0259\3\2\2\2\u026b\u025c\3")
        buf.write("\2\2\2\u026b\u025f\3\2\2\2\u026b\u0265\3\2\2\2\u026b\u0269")
        buf.write("\3\2\2\2\u026c+\3\2\2\2\u026d\u026e\7u\2\2\u026e\u027a")
        buf.write("\b\27\1\2\u026f\u0270\7v\2\2\u0270\u027a\b\27\1\2\u0271")
        buf.write("\u0272\7w\2\2\u0272\u027a\b\27\1\2\u0273\u0274\7x\2\2")
        buf.write("\u0274\u027a\b\27\1\2\u0275\u0276\7y\2\2\u0276\u027a\b")
        buf.write("\27\1\2\u0277\u0278\7z\2\2\u0278\u027a\b\27\1\2\u0279")
        buf.write("\u026d\3\2\2\2\u0279\u026f\3\2\2\2\u0279\u0271\3\2\2\2")
        buf.write("\u0279\u0273\3\2\2\2\u0279\u0275\3\2\2\2\u0279\u0277\3")
        buf.write("\2\2\2\u027a-\3\2\2\2\u027b\u027c\t\32\2\2\u027c\u0280")
        buf.write("\b\30\1\2\u027d\u027e\t\33\2\2\u027e\u0280\b\30\1\2\u027f")
        buf.write("\u027b\3\2\2\2\u027f\u027d\3\2\2\2\u0280/\3\2\2\2\u0281")
        buf.write("\u0282\5\62\32\2\u0282\u0283\b\31\1\2\u0283\u028a\3\2")
        buf.write("\2\2\u0284\u0285\7\u0097\2\2\u0285\u028a\b\31\1\2\u0286")
        buf.write("\u0287\5\64\33\2\u0287\u0288\b\31\1\2\u0288\u028a\3\2")
        buf.write("\2\2\u0289\u0281\3\2\2\2\u0289\u0284\3\2\2\2\u0289\u0286")
        buf.write("\3\2\2\2\u028a\61\3\2\2\2\u028b\u028d\7\u0091\2\2\u028c")
        buf.write("\u028e\7\36\2\2\u028d\u028c\3\2\2\2\u028d\u028e\3\2\2")
        buf.write("\2\u028e\u028f\3\2\2\2\u028f\u0290\7C\2\2\u0290\u0298")
        buf.write("\b\32\1\2\u0291\u0292\7\u008b\2\2\u0292\u0293\7\37\2\2")
        buf.write("\u0293\u0298\b\32\1\2\u0294\u0295\7\u008b\2\2\u0295\u0296")
        buf.write("\7O\2\2\u0296\u0298\b\32\1\2\u0297\u028b\3\2\2\2\u0297")
        buf.write("\u0291\3\2\2\2\u0297\u0294\3\2\2\2\u0298\63\3\2\2\2\u0299")
        buf.write("\u029a\t\34\2\2\u029a\65\3\2\2\2\u029b\u029c\7\u009a\2")
        buf.write("\2\u029c\67\3\2\2\2@;EKQV`frx}\u0085\u009c\u00a1\u00a8")
        buf.write("\u00ae\u00b6\u00ba\u00ce\u00d4\u00ec\u00f0\u00f3\u00f7")
        buf.write("\u0102\u010d\u0122\u0138\u015a\u015d\u016a\u0184\u0186")
        buf.write("\u018d\u019b\u01a3\u01b3\u01b9\u01be\u01c7\u01ca\u01cf")
        buf.write("\u01e5\u01e8\u01ed\u01f3\u01f9\u01fc\u01ff\u020b\u0232")
        buf.write("\u0235\u0243\u024f\u0256\u0261\u0265\u026b\u0279\u027f")
        buf.write("\u0289\u028d\u0297")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'print'", "','", "'pause'", "'if'", "'else'", 
                     "'{'", "'}'", "'[['", "']]'", "'repeat'", "'times'", 
                     "'for'", "'in'", "'['", "'by'", "'('", "'well'", "'#'", 
                     "'heater'", "'magnitude'", "'as'", "'a'", "'string'", 
                     "'turned'", "'dir'", "'direction'", "'C'", "'the'", 
                     "'reagent'", "'named'", "'of'", "'has'", "'an'", "'is'", 
                     "'and'", "'or'", "'to'", "'drop'", "'@'", "'at'", "'unknown'", 
                     "'waste'", "'up'", "'north'", "'down'", "'south'", 
                     "'left'", "'west'", "'right'", "'east'", "'clockwise'", 
                     "'counterclockwise'", "'around'", "'row'", "'rows'", 
                     "'col'", "'column'", "'cols'", "'columns'", "'macro'", 
                     "'turn'", "'state'", "'remove'", "'from'", "'board'", 
                     "'pad'", "'gate'", "'int'", "'float'", "'electrode'", 
                     "'delta'", "'motion'", "'delay'", "'time'", "'ticks'", 
                     "'bool'", "'volume'", "'liquid'", "'temp'", "'temperature'", 
                     "'diff'", "'difference'", "'point'", "'s'", "'sec'", 
                     "'secs'", "'second'", "'seconds'", "'ms'", "'millisecond'", 
                     "'milliseconds'", "'uL'", "'ul'", "'microliter'", "'microlitre'", 
                     "'microliters'", "'microlitres'", "'mL'", "'ml'", "'milliliter'", 
                     "'millilitre'", "'milliliters'", "'millilitres'", "'tick'", 
                     "'drops'", "'exit'", "'y'", "'coord'", "'coordinate'", 
                     "'x'", "'remaining'", "'capacity'", "'target'", "'current'", 
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
                      "<INVALID>", "ADD", "ASSIGN", "ATTR", "DIV", "INTERACTIVE", 
                      "INJECT", "LOCAL", "MUL", "NOT", "OFF", "ON", "SUB", 
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
    RULE_attr = 20
    RULE_rel = 21
    RULE_bool_val = 22
    RULE_name = 23
    RULE_multi_word_name = 24
    RULE_kwd_names = 25
    RULE_string = 26

    ruleNames =  [ "macro_file", "interactive", "declaration", "printing", 
                   "stat", "compound", "loop", "term_punct", "expr", "reagent", 
                   "direction", "turn", "rc", "axis", "macro_def", "macro_header", 
                   "param", "no_arg_action", "param_type", "dim_unit", "attr", 
                   "rel", "bool_val", "name", "multi_word_name", "kwd_names", 
                   "string" ]

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
    ADD=133
    ASSIGN=134
    ATTR=135
    DIV=136
    INTERACTIVE=137
    INJECT=138
    LOCAL=139
    MUL=140
    NOT=141
    OFF=142
    ON=143
    SUB=144
    TERMINATOR=145
    TOGGLE=146
    CLOSE_BRACKET=147
    CLOSE_PAREN=148
    ID=149
    INT=150
    FLOAT=151
    STRING=152
    EOL_COMMENT=153
    COMMENT=154
    WS=155

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
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__9) | (1 << DMFParser.T__11) | (1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__18) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__66 - 66)) | (1 << (DMFParser.T__67 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.T__69 - 66)) | (1 << (DMFParser.T__70 - 66)) | (1 << (DMFParser.T__71 - 66)) | (1 << (DMFParser.T__72 - 66)) | (1 << (DMFParser.T__73 - 66)) | (1 << (DMFParser.T__74 - 66)) | (1 << (DMFParser.T__75 - 66)) | (1 << (DMFParser.T__76 - 66)) | (1 << (DMFParser.T__77 - 66)) | (1 << (DMFParser.T__78 - 66)) | (1 << (DMFParser.T__79 - 66)) | (1 << (DMFParser.T__80 - 66)) | (1 << (DMFParser.T__81 - 66)) | (1 << (DMFParser.T__82 - 66)) | (1 << (DMFParser.T__83 - 66)) | (1 << (DMFParser.T__88 - 66)) | (1 << (DMFParser.T__106 - 66)) | (1 << (DMFParser.T__109 - 66)) | (1 << (DMFParser.T__120 - 66)) | (1 << (DMFParser.T__121 - 66)) | (1 << (DMFParser.T__122 - 66)) | (1 << (DMFParser.T__123 - 66)) | (1 << (DMFParser.T__124 - 66)) | (1 << (DMFParser.T__125 - 66)) | (1 << (DMFParser.T__126 - 66)) | (1 << (DMFParser.T__127 - 66)) | (1 << (DMFParser.T__128 - 66)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__130 - 130)) | (1 << (DMFParser.T__131 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.LOCAL - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
                self.state = 54
                self.stat()
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 60
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
            self.state = 84
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 62
                self.compound()
                self.state = 63
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Decl_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 65
                self.declaration()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 66
                    self.match(DMFParser.TERMINATOR)


                self.state = 69
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Print_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 71
                self.printing()
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 72
                    self.match(DMFParser.TERMINATOR)


                self.state = 75
                self.match(DMFParser.EOF)
                pass

            elif la_ == 4:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 77
                self.expr(0)
                self.state = 79
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 78
                    self.match(DMFParser.TERMINATOR)


                self.state = 81
                self.match(DMFParser.EOF)
                pass

            elif la_ == 5:
                localctx = DMFParser.Empty_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 83
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
            self.state = 123
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 86
                self.match(DMFParser.LOCAL)
                self.state = 87
                localctx._name = self.name()
                self.state = 88
                self.match(DMFParser.ASSIGN)
                self.state = 89
                localctx.init = self.expr(0)
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                localctx.type=None
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 94
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.LOCAL:
                    self.state = 93
                    self.match(DMFParser.LOCAL)


                self.state = 96
                localctx._param_type = self.param_type()
                self.state = 97
                localctx._INT = self.match(DMFParser.INT)
                self.state = 98
                self.match(DMFParser.ASSIGN)
                self.state = 100
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__2) | (1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__18) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__66 - 66)) | (1 << (DMFParser.T__67 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.T__69 - 66)) | (1 << (DMFParser.T__70 - 66)) | (1 << (DMFParser.T__71 - 66)) | (1 << (DMFParser.T__72 - 66)) | (1 << (DMFParser.T__73 - 66)) | (1 << (DMFParser.T__74 - 66)) | (1 << (DMFParser.T__75 - 66)) | (1 << (DMFParser.T__76 - 66)) | (1 << (DMFParser.T__77 - 66)) | (1 << (DMFParser.T__78 - 66)) | (1 << (DMFParser.T__79 - 66)) | (1 << (DMFParser.T__80 - 66)) | (1 << (DMFParser.T__81 - 66)) | (1 << (DMFParser.T__82 - 66)) | (1 << (DMFParser.T__83 - 66)) | (1 << (DMFParser.T__88 - 66)) | (1 << (DMFParser.T__106 - 66)) | (1 << (DMFParser.T__109 - 66)) | (1 << (DMFParser.T__120 - 66)) | (1 << (DMFParser.T__121 - 66)) | (1 << (DMFParser.T__122 - 66)) | (1 << (DMFParser.T__123 - 66)) | (1 << (DMFParser.T__124 - 66)) | (1 << (DMFParser.T__125 - 66)) | (1 << (DMFParser.T__126 - 66)) | (1 << (DMFParser.T__127 - 66)) | (1 << (DMFParser.T__128 - 66)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__130 - 130)) | (1 << (DMFParser.T__131 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
                    self.state = 99
                    localctx.init = self.expr(0)


                localctx.type=localctx._param_type.type
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 105
                self.match(DMFParser.LOCAL)
                self.state = 106
                localctx._param_type = self.param_type()
                self.state = 107
                localctx._INT = self.match(DMFParser.INT)
                localctx.type=localctx._param_type.type
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.LOCAL:
                    self.state = 111
                    self.match(DMFParser.LOCAL)


                self.state = 114
                localctx._param_type = self.param_type()
                self.state = 115
                localctx._name = self.name()
                self.state = 118
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.ASSIGN:
                    self.state = 116
                    self.match(DMFParser.ASSIGN)
                    self.state = 117
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
            self.state = 125
            self.match(DMFParser.T__0)
            self.state = 126
            localctx._expr = self.expr(0)
            localctx.vals.append(localctx._expr)
            self.state = 131
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==DMFParser.T__1:
                self.state = 127
                self.match(DMFParser.T__1)
                self.state = 128
                localctx._expr = self.expr(0)
                localctx.vals.append(localctx._expr)
                self.state = 133
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
            self.state = 166
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Decl_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 134
                self.declaration()
                self.state = 135
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.Pause_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 137
                self.match(DMFParser.T__2)
                self.state = 138
                localctx.duration = self.expr(0)
                self.state = 139
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 3:
                localctx = DMFParser.Print_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 141
                self.printing()
                self.state = 142
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 4:
                localctx = DMFParser.If_statContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 144
                self.match(DMFParser.T__3)
                self.state = 145
                localctx._expr = self.expr(0)
                localctx.tests.append(localctx._expr)
                self.state = 146
                localctx._compound = self.compound()
                localctx.bodies.append(localctx._compound)
                self.state = 154
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 147
                        self.match(DMFParser.T__4)
                        self.state = 148
                        self.match(DMFParser.T__3)
                        self.state = 149
                        localctx._expr = self.expr(0)
                        localctx.tests.append(localctx._expr)
                        self.state = 150
                        localctx._compound = self.compound()
                        localctx.bodies.append(localctx._compound) 
                    self.state = 156
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

                self.state = 159
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__4:
                    self.state = 157
                    self.match(DMFParser.T__4)
                    self.state = 158
                    localctx.else_body = self.compound()


                pass

            elif la_ == 5:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 161
                self.expr(0)
                self.state = 162
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 6:
                localctx = DMFParser.Loop_statContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 164
                self.loop()
                pass

            elif la_ == 7:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 165
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
            self.state = 184
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__5]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 168
                self.match(DMFParser.T__5)
                self.state = 172
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__9) | (1 << DMFParser.T__11) | (1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__18) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__66 - 66)) | (1 << (DMFParser.T__67 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.T__69 - 66)) | (1 << (DMFParser.T__70 - 66)) | (1 << (DMFParser.T__71 - 66)) | (1 << (DMFParser.T__72 - 66)) | (1 << (DMFParser.T__73 - 66)) | (1 << (DMFParser.T__74 - 66)) | (1 << (DMFParser.T__75 - 66)) | (1 << (DMFParser.T__76 - 66)) | (1 << (DMFParser.T__77 - 66)) | (1 << (DMFParser.T__78 - 66)) | (1 << (DMFParser.T__79 - 66)) | (1 << (DMFParser.T__80 - 66)) | (1 << (DMFParser.T__81 - 66)) | (1 << (DMFParser.T__82 - 66)) | (1 << (DMFParser.T__83 - 66)) | (1 << (DMFParser.T__88 - 66)) | (1 << (DMFParser.T__106 - 66)) | (1 << (DMFParser.T__109 - 66)) | (1 << (DMFParser.T__120 - 66)) | (1 << (DMFParser.T__121 - 66)) | (1 << (DMFParser.T__122 - 66)) | (1 << (DMFParser.T__123 - 66)) | (1 << (DMFParser.T__124 - 66)) | (1 << (DMFParser.T__125 - 66)) | (1 << (DMFParser.T__126 - 66)) | (1 << (DMFParser.T__127 - 66)) | (1 << (DMFParser.T__128 - 66)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__130 - 130)) | (1 << (DMFParser.T__131 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.LOCAL - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
                    self.state = 169
                    self.stat()
                    self.state = 174
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 175
                self.match(DMFParser.T__6)
                pass
            elif token in [DMFParser.T__7]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 176
                self.match(DMFParser.T__7)
                self.state = 180
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__3) | (1 << DMFParser.T__5) | (1 << DMFParser.T__7) | (1 << DMFParser.T__9) | (1 << DMFParser.T__11) | (1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__18) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__66 - 66)) | (1 << (DMFParser.T__67 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.T__69 - 66)) | (1 << (DMFParser.T__70 - 66)) | (1 << (DMFParser.T__71 - 66)) | (1 << (DMFParser.T__72 - 66)) | (1 << (DMFParser.T__73 - 66)) | (1 << (DMFParser.T__74 - 66)) | (1 << (DMFParser.T__75 - 66)) | (1 << (DMFParser.T__76 - 66)) | (1 << (DMFParser.T__77 - 66)) | (1 << (DMFParser.T__78 - 66)) | (1 << (DMFParser.T__79 - 66)) | (1 << (DMFParser.T__80 - 66)) | (1 << (DMFParser.T__81 - 66)) | (1 << (DMFParser.T__82 - 66)) | (1 << (DMFParser.T__83 - 66)) | (1 << (DMFParser.T__88 - 66)) | (1 << (DMFParser.T__106 - 66)) | (1 << (DMFParser.T__109 - 66)) | (1 << (DMFParser.T__120 - 66)) | (1 << (DMFParser.T__121 - 66)) | (1 << (DMFParser.T__122 - 66)) | (1 << (DMFParser.T__123 - 66)) | (1 << (DMFParser.T__124 - 66)) | (1 << (DMFParser.T__125 - 66)) | (1 << (DMFParser.T__126 - 66)) | (1 << (DMFParser.T__127 - 66)) | (1 << (DMFParser.T__128 - 66)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__130 - 130)) | (1 << (DMFParser.T__131 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.LOCAL - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
                    self.state = 177
                    self.stat()
                    self.state = 182
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 183
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
            self.state = 204
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__9]:
                localctx = DMFParser.Repeat_loopContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 186
                self.match(DMFParser.T__9)
                self.state = 187
                localctx.n = self.expr(0)
                self.state = 188
                self.match(DMFParser.T__10)
                self.state = 189
                localctx.body = self.stat()
                pass
            elif token in [DMFParser.T__11]:
                localctx = DMFParser.For_loopContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 191
                self.match(DMFParser.T__11)
                self.state = 192
                localctx.var = self.name()
                self.state = 193
                self.match(DMFParser.T__12)
                self.state = 194
                self.match(DMFParser.T__13)
                self.state = 195
                localctx.start = self.expr(0)
                self.state = 196
                self.match(DMFParser.T__1)
                self.state = 197
                localctx.stop = self.expr(0)
                self.state = 198
                self.term_punct()

                self.state = 199
                self.match(DMFParser.T__14)
                self.state = 200
                localctx.step = self.expr(0)
                self.state = 202
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
            self.state = 210
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.CLOSE_BRACKET]:
                self.enterOuterAlt(localctx, 1)
                self.state = 206
                self.match(DMFParser.CLOSE_BRACKET)
                localctx.is_closed=True
                pass
            elif token in [DMFParser.CLOSE_PAREN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 208
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


    class Heater_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self.which = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHeater_expr" ):
                listener.enterHeater_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHeater_expr" ):
                listener.exitHeater_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHeater_expr" ):
                return visitor.visitHeater_expr(self)
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

                self.state = 213
                self.match(DMFParser.T__15)
                self.state = 214
                self.expr(0)
                self.state = 215
                self.match(DMFParser.CLOSE_PAREN)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 217
                self.match(DMFParser.T__15)
                self.state = 218
                localctx.x = self.expr(0)
                self.state = 219
                self.match(DMFParser.T__1)
                self.state = 220
                localctx.y = self.expr(0)
                self.state = 221
                self.match(DMFParser.CLOSE_PAREN)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 223
                self.match(DMFParser.SUB)
                self.state = 224
                localctx.rhs = self.expr(46)
                pass

            elif la_ == 4:
                localctx = DMFParser.Well_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 225
                self.match(DMFParser.T__16)
                self.state = 226
                self.match(DMFParser.T__17)
                self.state = 227
                localctx.which = self.expr(44)
                pass

            elif la_ == 5:
                localctx = DMFParser.Heater_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 228
                self.match(DMFParser.T__18)
                self.state = 229
                self.match(DMFParser.T__17)
                self.state = 230
                localctx.which = self.expr(43)
                pass

            elif la_ == 6:
                localctx = DMFParser.Const_rc_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 231
                localctx._INT = self.match(DMFParser.INT)
                self.state = 232
                self.rc((0 if localctx._INT is None else int(localctx._INT.text)))
                pass

            elif la_ == 7:
                localctx = DMFParser.Reagent_lit_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 234
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__27:
                    self.state = 233
                    self.match(DMFParser.T__27)


                self.state = 236
                self.reagent()
                self.state = 238
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
                if la_ == 1:
                    self.state = 237
                    self.match(DMFParser.T__28)


                pass

            elif la_ == 8:
                localctx = DMFParser.Reagent_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 241
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__21 or _la==DMFParser.T__27:
                    self.state = 240
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__21 or _la==DMFParser.T__27):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 243
                self.match(DMFParser.T__28)
                self.state = 245
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__29:
                    self.state = 244
                    self.match(DMFParser.T__29)


                self.state = 247
                localctx.which = self.expr(32)
                pass

            elif la_ == 9:
                localctx = DMFParser.Not_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 248
                self.match(DMFParser.NOT)
                self.state = 249
                self.expr(25)
                pass

            elif la_ == 10:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 250
                self.direction()
                self.state = 251
                localctx.dist = self.expr(22)
                pass

            elif la_ == 11:
                localctx = DMFParser.Dir_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 253
                self.direction()
                pass

            elif la_ == 12:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 254
                self.match(DMFParser.T__36)
                self.state = 256
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__53) | (1 << DMFParser.T__55) | (1 << DMFParser.T__56))) != 0):
                    self.state = 255
                    self.axis()


                self.state = 258
                localctx.which = self.expr(20)
                pass

            elif la_ == 13:
                localctx = DMFParser.Pause_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 259
                self.match(DMFParser.T__2)
                self.state = 260
                localctx.duration = self.expr(19)
                pass

            elif la_ == 14:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 261
                self.match(DMFParser.T__37)
                self.state = 262
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__38 or _la==DMFParser.T__39):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 263
                localctx.loc = self.expr(17)
                pass

            elif la_ == 15:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 264
                self.macro_def()
                pass

            elif la_ == 16:
                localctx = DMFParser.Action_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 265
                self.no_arg_action()
                pass

            elif la_ == 17:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 267
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__27:
                    self.state = 266
                    self.match(DMFParser.T__27)


                self.state = 269
                self.param_type()
                pass

            elif la_ == 18:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 270
                self.param_type()
                self.state = 271
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 19:
                localctx = DMFParser.Bool_const_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 273
                localctx.val = self.bool_val()
                pass

            elif la_ == 20:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 274
                self.name()
                pass

            elif la_ == 21:
                localctx = DMFParser.Mw_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 275
                self.multi_word_name()
                pass

            elif la_ == 22:
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

            elif la_ == 23:
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

            elif la_ == 24:
                localctx = DMFParser.String_lit_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 285
                self.string()
                pass

            elif la_ == 25:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 286
                localctx._INT = self.match(DMFParser.INT)
                pass

            elif la_ == 26:
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
                        if not(_la==DMFParser.T__24 or _la==DMFParser.T__25):
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
                        self.match(DMFParser.T__30)
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
                        self.match(DMFParser.T__33)
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
                        self.match(DMFParser.T__34)
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
                        self.match(DMFParser.T__35)
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
                        if not(_la==DMFParser.T__38 or _la==DMFParser.T__39):
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
                        if not self.precpred(self._ctx, 48):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 48)")
                        self.state = 338
                        self.match(DMFParser.T__15)
                        self.state = 347
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__2) | (1 << DMFParser.T__15) | (1 << DMFParser.T__16) | (1 << DMFParser.T__18) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__27) | (1 << DMFParser.T__28) | (1 << DMFParser.T__36) | (1 << DMFParser.T__37) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__43) | (1 << DMFParser.T__44) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60) | (1 << DMFParser.T__61) | (1 << DMFParser.T__62))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__66 - 66)) | (1 << (DMFParser.T__67 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.T__69 - 66)) | (1 << (DMFParser.T__70 - 66)) | (1 << (DMFParser.T__71 - 66)) | (1 << (DMFParser.T__72 - 66)) | (1 << (DMFParser.T__73 - 66)) | (1 << (DMFParser.T__74 - 66)) | (1 << (DMFParser.T__75 - 66)) | (1 << (DMFParser.T__76 - 66)) | (1 << (DMFParser.T__77 - 66)) | (1 << (DMFParser.T__78 - 66)) | (1 << (DMFParser.T__79 - 66)) | (1 << (DMFParser.T__80 - 66)) | (1 << (DMFParser.T__81 - 66)) | (1 << (DMFParser.T__82 - 66)) | (1 << (DMFParser.T__83 - 66)) | (1 << (DMFParser.T__88 - 66)) | (1 << (DMFParser.T__106 - 66)) | (1 << (DMFParser.T__109 - 66)) | (1 << (DMFParser.T__120 - 66)) | (1 << (DMFParser.T__121 - 66)) | (1 << (DMFParser.T__122 - 66)) | (1 << (DMFParser.T__123 - 66)) | (1 << (DMFParser.T__124 - 66)) | (1 << (DMFParser.T__125 - 66)) | (1 << (DMFParser.T__126 - 66)) | (1 << (DMFParser.T__127 - 66)) | (1 << (DMFParser.T__128 - 66)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__130 - 130)) | (1 << (DMFParser.T__131 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
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
                        if not self.precpred(self._ctx, 45):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 45)")
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
                        self.match(DMFParser.T__19)
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
                        self.match(DMFParser.T__20)
                        self.state = 360
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==DMFParser.T__21:
                            self.state = 359
                            self.match(DMFParser.T__21)


                        self.state = 362
                        self.match(DMFParser.T__22)
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
                        self.match(DMFParser.T__23)
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
                        self.match(DMFParser.T__26)
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
                        self.match(DMFParser.T__31)
                        self.state = 379
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__21 or _la==DMFParser.T__32):
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
            if token in [DMFParser.T__40]:
                self.enterOuterAlt(localctx, 1)
                self.state = 391
                self.match(DMFParser.T__40)
                localctx.r = unknown_reagent
                pass
            elif token in [DMFParser.T__41]:
                self.enterOuterAlt(localctx, 2)
                self.state = 393
                self.match(DMFParser.T__41)
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
            if token in [DMFParser.T__42, DMFParser.T__43]:
                self.enterOuterAlt(localctx, 1)
                self.state = 397
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__42 or _la==DMFParser.T__43):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__44, DMFParser.T__45]:
                self.enterOuterAlt(localctx, 2)
                self.state = 400
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__44 or _la==DMFParser.T__45):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__46, DMFParser.T__47]:
                self.enterOuterAlt(localctx, 3)
                self.state = 403
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__46 or _la==DMFParser.T__47):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__48, DMFParser.T__49]:
                self.enterOuterAlt(localctx, 4)
                self.state = 406
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__48 or _la==DMFParser.T__49):
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
            if token in [DMFParser.T__48, DMFParser.T__50]:
                self.enterOuterAlt(localctx, 1)
                self.state = 411
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__48 or _la==DMFParser.T__50):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.RIGHT
                pass
            elif token in [DMFParser.T__46, DMFParser.T__51]:
                self.enterOuterAlt(localctx, 2)
                self.state = 413
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__46 or _la==DMFParser.T__51):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.LEFT
                pass
            elif token in [DMFParser.T__52]:
                self.enterOuterAlt(localctx, 3)
                self.state = 415
                self.match(DMFParser.T__52)
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
                self.match(DMFParser.T__53)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 423
                self.match(DMFParser.T__54)
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
                if not(_la==DMFParser.T__55 or _la==DMFParser.T__56):
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
                if not(_la==DMFParser.T__57 or _la==DMFParser.T__58):
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
            if token in [DMFParser.T__53]:
                self.enterOuterAlt(localctx, 1)
                self.state = 435
                self.match(DMFParser.T__53)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__55, DMFParser.T__56]:
                self.enterOuterAlt(localctx, 2)
                self.state = 437
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__55 or _la==DMFParser.T__56):
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
            elif token in [DMFParser.T__2, DMFParser.T__15, DMFParser.T__16, DMFParser.T__18, DMFParser.T__21, DMFParser.T__22, DMFParser.T__24, DMFParser.T__25, DMFParser.T__27, DMFParser.T__28, DMFParser.T__36, DMFParser.T__37, DMFParser.T__40, DMFParser.T__41, DMFParser.T__42, DMFParser.T__43, DMFParser.T__44, DMFParser.T__45, DMFParser.T__46, DMFParser.T__47, DMFParser.T__48, DMFParser.T__49, DMFParser.T__59, DMFParser.T__60, DMFParser.T__61, DMFParser.T__62, DMFParser.T__65, DMFParser.T__66, DMFParser.T__67, DMFParser.T__68, DMFParser.T__69, DMFParser.T__70, DMFParser.T__71, DMFParser.T__72, DMFParser.T__73, DMFParser.T__74, DMFParser.T__75, DMFParser.T__76, DMFParser.T__77, DMFParser.T__78, DMFParser.T__79, DMFParser.T__80, DMFParser.T__81, DMFParser.T__82, DMFParser.T__83, DMFParser.T__88, DMFParser.T__106, DMFParser.T__109, DMFParser.T__120, DMFParser.T__121, DMFParser.T__122, DMFParser.T__123, DMFParser.T__124, DMFParser.T__125, DMFParser.T__126, DMFParser.T__127, DMFParser.T__128, DMFParser.T__129, DMFParser.T__130, DMFParser.T__131, DMFParser.INTERACTIVE, DMFParser.NOT, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT, DMFParser.FLOAT, DMFParser.STRING]:
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
            self.match(DMFParser.T__59)
            self.state = 447
            self.match(DMFParser.T__15)
            self.state = 456
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__16) | (1 << DMFParser.T__21) | (1 << DMFParser.T__22) | (1 << DMFParser.T__24) | (1 << DMFParser.T__25) | (1 << DMFParser.T__28) | (1 << DMFParser.T__32) | (1 << DMFParser.T__37) | (1 << DMFParser.T__61))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__66 - 66)) | (1 << (DMFParser.T__67 - 66)) | (1 << (DMFParser.T__68 - 66)) | (1 << (DMFParser.T__69 - 66)) | (1 << (DMFParser.T__70 - 66)) | (1 << (DMFParser.T__71 - 66)) | (1 << (DMFParser.T__72 - 66)) | (1 << (DMFParser.T__73 - 66)) | (1 << (DMFParser.T__74 - 66)) | (1 << (DMFParser.T__75 - 66)) | (1 << (DMFParser.T__76 - 66)) | (1 << (DMFParser.T__77 - 66)) | (1 << (DMFParser.T__78 - 66)) | (1 << (DMFParser.T__79 - 66)) | (1 << (DMFParser.T__80 - 66)) | (1 << (DMFParser.T__81 - 66)) | (1 << (DMFParser.T__82 - 66)) | (1 << (DMFParser.T__83 - 66)) | (1 << (DMFParser.T__88 - 66)) | (1 << (DMFParser.T__106 - 66)) | (1 << (DMFParser.T__109 - 66)))) != 0) or ((((_la - 137)) & ~0x3f) == 0 and ((1 << (_la - 137)) & ((1 << (DMFParser.INTERACTIVE - 137)) | (1 << (DMFParser.ON - 137)) | (1 << (DMFParser.ID - 137)))) != 0):
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
                if _la==DMFParser.T__21 or _la==DMFParser.T__32:
                    self.state = 460
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__21 or _la==DMFParser.T__32):
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
                if _la==DMFParser.T__60:
                    self.state = 485
                    self.match(DMFParser.T__60)


                self.state = 488
                self.match(DMFParser.ON)
                localctx.which="TURN-ON"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 491
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__60:
                    self.state = 490
                    self.match(DMFParser.T__60)


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
                    self.match(DMFParser.T__61)


                localctx.which="TOGGLE"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 500
                self.match(DMFParser.T__62)
                self.state = 506
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,46,self._ctx)
                if la_ == 1:
                    self.state = 501
                    self.match(DMFParser.T__63)
                    self.state = 503
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==DMFParser.T__27:
                        self.state = 502
                        self.match(DMFParser.T__27)


                    self.state = 505
                    self.match(DMFParser.T__64)


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
            self.state = 563
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,50,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 511
                self.match(DMFParser.T__37)
                localctx.type=Type.DROP
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 513
                self.match(DMFParser.T__65)
                localctx.type=Type.PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 515
                self.match(DMFParser.T__16)
                localctx.type=Type.WELL
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 517
                self.match(DMFParser.T__16)
                self.state = 518
                self.match(DMFParser.T__65)
                localctx.type=Type.WELL_PAD
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 521
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__16:
                    self.state = 520
                    self.match(DMFParser.T__16)


                self.state = 523
                self.match(DMFParser.T__66)
                localctx.type=Type.WELL_GATE
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 525
                self.match(DMFParser.T__67)
                localctx.type=Type.INT
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 527
                self.match(DMFParser.T__68)
                localctx.type=Type.FLOAT
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 529
                self.match(DMFParser.T__22)
                localctx.type=Type.STRING
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 531
                self.match(DMFParser.T__61)
                localctx.type=Type.BINARY_STATE
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 533
                self.match(DMFParser.T__69)
                localctx.type=Type.BINARY_CPT
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 535
                self.match(DMFParser.T__70)
                localctx.type=Type.DELTA
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 537
                self.match(DMFParser.T__71)
                localctx.type=Type.MOTION
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 539
                self.match(DMFParser.T__72)
                localctx.type=Type.DELAY
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 541
                self.match(DMFParser.T__73)
                localctx.type=Type.TIME
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 543
                self.match(DMFParser.T__74)
                localctx.type=Type.TICKS
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 545
                self.match(DMFParser.T__75)
                localctx.type=Type.BOOL
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 547
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__24 or _la==DMFParser.T__25):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.type=Type.DIR
                pass

            elif la_ == 18:
                self.enterOuterAlt(localctx, 18)
                self.state = 549
                self.match(DMFParser.T__76)
                localctx.type=Type.VOLUME
                pass

            elif la_ == 19:
                self.enterOuterAlt(localctx, 19)
                self.state = 551
                self.match(DMFParser.T__28)
                localctx.type=Type.REAGENT
                pass

            elif la_ == 20:
                self.enterOuterAlt(localctx, 20)
                self.state = 553
                self.match(DMFParser.T__77)
                localctx.type=Type.LIQUID
                pass

            elif la_ == 21:
                self.enterOuterAlt(localctx, 21)
                self.state = 555
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__78 or _la==DMFParser.T__79):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 556
                _la = self._input.LA(1)
                if not(((((_la - 71)) & ~0x3f) == 0 and ((1 << (_la - 71)) & ((1 << (DMFParser.T__70 - 71)) | (1 << (DMFParser.T__80 - 71)) | (1 << (DMFParser.T__81 - 71)))) != 0)):
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
                if not(_la==DMFParser.T__78 or _la==DMFParser.T__79):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 560
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
                if la_ == 1:
                    self.state = 559
                    self.match(DMFParser.T__82)


                localctx.type=Type.ABS_TEMP
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
            self.state = 577
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__83, DMFParser.T__84, DMFParser.T__85, DMFParser.T__86, DMFParser.T__87]:
                self.enterOuterAlt(localctx, 1)
                self.state = 565
                _la = self._input.LA(1)
                if not(((((_la - 84)) & ~0x3f) == 0 and ((1 << (_la - 84)) & ((1 << (DMFParser.T__83 - 84)) | (1 << (DMFParser.T__84 - 84)) | (1 << (DMFParser.T__85 - 84)) | (1 << (DMFParser.T__86 - 84)) | (1 << (DMFParser.T__87 - 84)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.sec
                pass
            elif token in [DMFParser.T__88, DMFParser.T__89, DMFParser.T__90]:
                self.enterOuterAlt(localctx, 2)
                self.state = 567
                _la = self._input.LA(1)
                if not(((((_la - 89)) & ~0x3f) == 0 and ((1 << (_la - 89)) & ((1 << (DMFParser.T__88 - 89)) | (1 << (DMFParser.T__89 - 89)) | (1 << (DMFParser.T__90 - 89)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.ms
                pass
            elif token in [DMFParser.T__91, DMFParser.T__92, DMFParser.T__93, DMFParser.T__94, DMFParser.T__95, DMFParser.T__96]:
                self.enterOuterAlt(localctx, 3)
                self.state = 569
                _la = self._input.LA(1)
                if not(((((_la - 92)) & ~0x3f) == 0 and ((1 << (_la - 92)) & ((1 << (DMFParser.T__91 - 92)) | (1 << (DMFParser.T__92 - 92)) | (1 << (DMFParser.T__93 - 92)) | (1 << (DMFParser.T__94 - 92)) | (1 << (DMFParser.T__95 - 92)) | (1 << (DMFParser.T__96 - 92)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.uL
                pass
            elif token in [DMFParser.T__97, DMFParser.T__98, DMFParser.T__99, DMFParser.T__100, DMFParser.T__101, DMFParser.T__102]:
                self.enterOuterAlt(localctx, 4)
                self.state = 571
                _la = self._input.LA(1)
                if not(((((_la - 98)) & ~0x3f) == 0 and ((1 << (_la - 98)) & ((1 << (DMFParser.T__97 - 98)) | (1 << (DMFParser.T__98 - 98)) | (1 << (DMFParser.T__99 - 98)) | (1 << (DMFParser.T__100 - 98)) | (1 << (DMFParser.T__101 - 98)) | (1 << (DMFParser.T__102 - 98)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.mL
                pass
            elif token in [DMFParser.T__74, DMFParser.T__103]:
                self.enterOuterAlt(localctx, 5)
                self.state = 573
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__74 or _la==DMFParser.T__103):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=ticks
                pass
            elif token in [DMFParser.T__37, DMFParser.T__104]:
                self.enterOuterAlt(localctx, 6)
                self.state = 575
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__37 or _la==DMFParser.T__104):
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
        self.enterRule(localctx, 40, self.RULE_attr)
        self._la = 0 # Token type
        try:
            self.state = 617
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,56,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 579
                self.match(DMFParser.T__105)
                self.state = 580
                self.match(DMFParser.T__65)
                localctx.which="#exit_pad"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 582
                self.match(DMFParser.T__66)
                localctx.which="gate"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 584
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__24 or _la==DMFParser.T__25):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="direction"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 589
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__53]:
                    self.state = 586
                    self.match(DMFParser.T__53)
                    pass
                elif token in [DMFParser.T__106]:
                    self.state = 587
                    self.match(DMFParser.T__106)
                    self.state = 588
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__107 or _la==DMFParser.T__108):
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
                self.state = 596
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__55]:
                    self.state = 592
                    self.match(DMFParser.T__55)
                    pass
                elif token in [DMFParser.T__56]:
                    self.state = 593
                    self.match(DMFParser.T__56)
                    pass
                elif token in [DMFParser.T__109]:
                    self.state = 594
                    self.match(DMFParser.T__109)
                    self.state = 595
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__107 or _la==DMFParser.T__108):
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
                self.state = 599
                self.match(DMFParser.T__105)
                self.state = 600
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__24 or _la==DMFParser.T__25):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#exit_dir"
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 602
                self.match(DMFParser.T__110)
                self.state = 603
                self.match(DMFParser.T__111)
                localctx.which="#remaining_capacity"
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 605
                self.match(DMFParser.T__112)
                self.state = 607
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
                if la_ == 1:
                    self.state = 606
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__78 or _la==DMFParser.T__79):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                localctx.which="#target_temperature"
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 611
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__113:
                    self.state = 610
                    self.match(DMFParser.T__113)


                self.state = 613
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__78 or _la==DMFParser.T__79):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#current_temperature"
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 615
                localctx.n = self._input.LT(1)
                _la = self._input.LA(1)
                if not(((((_la - 17)) & ~0x3f) == 0 and ((1 << (_la - 17)) & ((1 << (DMFParser.T__16 - 17)) | (1 << (DMFParser.T__28 - 17)) | (1 << (DMFParser.T__37 - 17)) | (1 << (DMFParser.T__65 - 17)) | (1 << (DMFParser.T__76 - 17)))) != 0) or _la==DMFParser.ID):
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
        self.enterRule(localctx, 42, self.RULE_rel)
        try:
            self.state = 631
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__114]:
                self.enterOuterAlt(localctx, 1)
                self.state = 619
                self.match(DMFParser.T__114)
                localctx.which=Rel.EQ
                pass
            elif token in [DMFParser.T__115]:
                self.enterOuterAlt(localctx, 2)
                self.state = 621
                self.match(DMFParser.T__115)
                localctx.which=Rel.NE
                pass
            elif token in [DMFParser.T__116]:
                self.enterOuterAlt(localctx, 3)
                self.state = 623
                self.match(DMFParser.T__116)
                localctx.which=Rel.LT
                pass
            elif token in [DMFParser.T__117]:
                self.enterOuterAlt(localctx, 4)
                self.state = 625
                self.match(DMFParser.T__117)
                localctx.which=Rel.LE
                pass
            elif token in [DMFParser.T__118]:
                self.enterOuterAlt(localctx, 5)
                self.state = 627
                self.match(DMFParser.T__118)
                localctx.which=Rel.GT
                pass
            elif token in [DMFParser.T__119]:
                self.enterOuterAlt(localctx, 6)
                self.state = 629
                self.match(DMFParser.T__119)
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
        self.enterRule(localctx, 44, self.RULE_bool_val)
        self._la = 0 # Token type
        try:
            self.state = 637
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__120, DMFParser.T__121, DMFParser.T__122, DMFParser.T__123, DMFParser.T__124, DMFParser.T__125]:
                self.enterOuterAlt(localctx, 1)
                self.state = 633
                _la = self._input.LA(1)
                if not(((((_la - 121)) & ~0x3f) == 0 and ((1 << (_la - 121)) & ((1 << (DMFParser.T__120 - 121)) | (1 << (DMFParser.T__121 - 121)) | (1 << (DMFParser.T__122 - 121)) | (1 << (DMFParser.T__123 - 121)) | (1 << (DMFParser.T__124 - 121)) | (1 << (DMFParser.T__125 - 121)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.val=True
                pass
            elif token in [DMFParser.T__126, DMFParser.T__127, DMFParser.T__128, DMFParser.T__129, DMFParser.T__130, DMFParser.T__131]:
                self.enterOuterAlt(localctx, 2)
                self.state = 635
                _la = self._input.LA(1)
                if not(((((_la - 127)) & ~0x3f) == 0 and ((1 << (_la - 127)) & ((1 << (DMFParser.T__126 - 127)) | (1 << (DMFParser.T__127 - 127)) | (1 << (DMFParser.T__128 - 127)) | (1 << (DMFParser.T__129 - 127)) | (1 << (DMFParser.T__130 - 127)) | (1 << (DMFParser.T__131 - 127)))) != 0)):
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
        self.enterRule(localctx, 46, self.RULE_name)
        try:
            self.state = 647
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.INTERACTIVE, DMFParser.ON]:
                self.enterOuterAlt(localctx, 1)
                self.state = 639
                localctx._multi_word_name = self.multi_word_name()
                localctx.val=localctx._multi_word_name.val
                pass
            elif token in [DMFParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 642
                localctx._ID = self.match(DMFParser.ID)
                localctx.val=(None if localctx._ID is None else localctx._ID.text)
                pass
            elif token in [DMFParser.T__70, DMFParser.T__80, DMFParser.T__81, DMFParser.T__82, DMFParser.T__83, DMFParser.T__88, DMFParser.T__106, DMFParser.T__109]:
                self.enterOuterAlt(localctx, 3)
                self.state = 644
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
        self.enterRule(localctx, 48, self.RULE_multi_word_name)
        self._la = 0 # Token type
        try:
            self.state = 661
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,61,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 649
                self.match(DMFParser.ON)
                self.state = 651
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__27:
                    self.state = 650
                    self.match(DMFParser.T__27)


                self.state = 653
                self.match(DMFParser.T__64)
                localctx.val="on board"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 655
                self.match(DMFParser.INTERACTIVE)
                self.state = 656
                self.match(DMFParser.T__28)
                localctx.val="interactive reagent"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 658
                self.match(DMFParser.INTERACTIVE)
                self.state = 659
                self.match(DMFParser.T__76)
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
        self.enterRule(localctx, 50, self.RULE_kwd_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 663
            _la = self._input.LA(1)
            if not(((((_la - 71)) & ~0x3f) == 0 and ((1 << (_la - 71)) & ((1 << (DMFParser.T__70 - 71)) | (1 << (DMFParser.T__80 - 71)) | (1 << (DMFParser.T__81 - 71)) | (1 << (DMFParser.T__82 - 71)) | (1 << (DMFParser.T__83 - 71)) | (1 << (DMFParser.T__88 - 71)) | (1 << (DMFParser.T__106 - 71)) | (1 << (DMFParser.T__109 - 71)))) != 0)):
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
        self.enterRule(localctx, 52, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 665
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
                return self.precpred(self._ctx, 48)
         

            if predIndex == 13:
                return self.precpred(self._ctx, 45)
         

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
         




