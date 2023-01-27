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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\u00bd")
        buf.write("\u0323\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23\t\23")
        buf.write("\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31")
        buf.write("\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36")
        buf.write("\4\37\t\37\3\2\7\2@\n\2\f\2\16\2C\13\2\3\2\3\2\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\3\3\3\5\3O\n\3\3\3\3\3\3\3\3\3\5\3")
        buf.write("U\n\3\3\3\3\3\3\3\5\3Z\n\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\5\4d\n\4\3\4\3\4\3\4\3\4\5\4j\n\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\4\3\4\5\4v\n\4\3\4\3\4\3\4\3\4\5\4")
        buf.write("|\n\4\3\4\3\4\3\4\5\4\u0081\n\4\3\5\3\5\3\5\3\5\3\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\7\5\u008e\n\5\f\5\16\5\u0091\13")
        buf.write("\5\3\5\3\5\5\5\u0095\n\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3")
        buf.write("\5\5\5\u009f\n\5\3\6\3\6\7\6\u00a3\n\6\f\6\16\6\u00a6")
        buf.write("\13\6\3\6\3\6\3\6\7\6\u00ab\n\6\f\6\16\6\u00ae\13\6\3")
        buf.write("\6\5\6\u00b1\n\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7\u00c6\n\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7\u00cf\n\7\5\7\u00d1\n\7")
        buf.write("\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\b\u00de")
        buf.write("\n\b\3\t\3\t\3\t\3\t\5\t\u00e4\n\t\3\t\3\t\3\t\3\t\3\n")
        buf.write("\3\n\5\n\u00ec\n\n\3\n\3\n\3\13\3\13\3\13\3\13\5\13\u00f4")
        buf.write("\n\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f")
        buf.write("\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f\u010a\n\f\3\f\3\f")
        buf.write("\5\f\u010e\n\f\3\f\5\f\u0111\n\f\3\f\3\f\5\f\u0115\n\f")
        buf.write("\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f\u0120\n\f\3\f")
        buf.write("\3\f\3\f\5\f\u0125\n\f\3\f\3\f\3\f\3\f\3\f\5\f\u012c\n")
        buf.write("\f\3\f\3\f\3\f\7\f\u0131\n\f\f\f\16\f\u0134\13\f\5\f\u0136")
        buf.write("\n\f\3\f\3\f\3\f\3\f\7\f\u013c\n\f\f\f\16\f\u013f\13\f")
        buf.write("\3\f\3\f\3\f\3\f\3\f\3\f\5\f\u0147\n\f\3\f\3\f\3\f\3\f")
        buf.write("\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\5\f\u015c\n\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f\u0172")
        buf.write("\n\f\3\f\5\f\u0175\n\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f")
        buf.write("\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\7\f\u0195\n\f\f\f\16")
        buf.write("\f\u0198\13\f\5\f\u019a\n\f\3\f\3\f\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\5\f\u01a7\n\f\3\f\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f")
        buf.write("\3\f\3\f\3\f\3\f\3\f\7\f\u01c1\n\f\f\f\16\f\u01c4\13\f")
        buf.write("\3\r\3\r\3\r\3\r\5\r\u01ca\n\r\3\16\3\16\3\16\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\3\16\3\16\3\16\5\16\u01d8\n\16\3")
        buf.write("\17\3\17\3\17\3\17\3\17\3\17\5\17\u01e0\n\17\3\20\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20")
        buf.write("\3\20\5\20\u01f0\n\20\3\21\3\21\3\21\3\21\5\21\u01f6\n")
        buf.write("\21\3\22\3\22\3\22\5\22\u01fb\n\22\3\23\3\23\3\23\3\23")
        buf.write("\3\23\7\23\u0202\n\23\f\23\16\23\u0205\13\23\5\23\u0207")
        buf.write("\n\23\3\23\3\23\3\24\5\24\u020c\n\24\3\24\3\24\3\24\3")
        buf.write("\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24\3\24")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\24\5\24\u0222\n\24\3\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\5\25\u022c\n\25\3\25")
        buf.write("\3\25\3\25\3\25\5\25\u0232\n\25\3\25\5\25\u0235\n\25\3")
        buf.write("\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\5\25\u0247\n\25\3\26\3\26\3")
        buf.write("\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\5\26\u0253\n\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\26\3\26\5\26\u027a\n\26\3\26\3\26\3\26\3")
        buf.write("\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\26")
        buf.write("\3\26\5\26\u028b\n\26\3\27\3\27\3\27\3\27\3\27\3\27\3")
        buf.write("\27\3\27\3\27\3\27\3\27\3\27\3\27\3\27\5\27\u029b\n\27")
        buf.write("\3\30\3\30\3\30\3\30\3\30\3\30\3\30\3\30\5\30\u02a5\n")
        buf.write("\30\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\5\31\u02b1\n\31\3\31\3\31\3\31\3\31\3\31\5\31\u02b8\n")
        buf.write("\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\5\31")
        buf.write("\u02c3\n\31\3\31\3\31\5\31\u02c7\n\31\3\31\3\31\3\31\3")
        buf.write("\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\5\31\u02dc\n\31\3\32\3\32\3")
        buf.write("\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\3\32\5\32")
        buf.write("\u02ea\n\32\3\33\3\33\3\33\3\33\5\33\u02f0\n\33\3\34\3")
        buf.write("\34\3\34\3\34\3\34\3\34\3\34\3\34\5\34\u02fa\n\34\3\35")
        buf.write("\3\35\5\35\u02fe\n\35\3\35\3\35\3\35\5\35\u0303\n\35\3")
        buf.write("\35\3\35\3\35\3\35\5\35\u0309\n\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\35\3\35\5\35\u0312\n\35\3\35\3\35\3\35\3\35\3")
        buf.write("\35\3\35\3\35\3\35\3\35\5\35\u031d\n\35\3\36\3\36\3\37")
        buf.write("\3\37\3\37\2\3\26 \2\4\6\b\n\f\16\20\22\24\26\30\32\34")
        buf.write("\36 \"$&(*,.\60\62\64\668:<\2#\3\2\u00b3\u00b4\4\2\31")
        buf.write("\31\37\37\3\2()\3\2./\3\2\34\35\4\2\u00a7\u00a7\u00ac")
        buf.write("\u00ac\4\2\u00a4\u00a4\u00b0\u00b0\4\2\31\31$$\3\2\62")
        buf.write("\63\4\2\17\17\64\64\3\2\65\66\3\2\678\4\2\67\6799\4\2")
        buf.write("\65\65::\3\2>?\3\2@A\3\2\\]\4\2TT^_\3\2hl\3\2mo\3\2pu")
        buf.write("\3\2v{\4\2XX||\4\2--}}\3\2~\u0080\3\2\u0082\u0083\3\2")
        buf.write("\u0089\u008a\3\2\u008c\u008d\4\2\\]\u0087\u0087\n\2  ")
        buf.write("--DDNOZZacgg\u00b7\u00b7\3\2\u0094\u0099\3\2\u009a\u009f")
        buf.write("\17\2\31\31$$HMTT^`hhmm\u0081\u0081\u0084\u0084\u0089")
        buf.write("\u008a\u008c\u008d\u00a0\u00a3\u00ae\u00af\2\u03d0\2A")
        buf.write("\3\2\2\2\4Y\3\2\2\2\6\u0080\3\2\2\2\b\u009e\3\2\2\2\n")
        buf.write("\u00b0\3\2\2\2\f\u00d0\3\2\2\2\16\u00dd\3\2\2\2\20\u00e3")
        buf.write("\3\2\2\2\22\u00e9\3\2\2\2\24\u00f3\3\2\2\2\26\u015b\3")
        buf.write("\2\2\2\30\u01c9\3\2\2\2\32\u01d7\3\2\2\2\34\u01df\3\2")
        buf.write("\2\2\36\u01ef\3\2\2\2 \u01f5\3\2\2\2\"\u01f7\3\2\2\2$")
        buf.write("\u01fc\3\2\2\2&\u0221\3\2\2\2(\u0246\3\2\2\2*\u028a\3")
        buf.write("\2\2\2,\u029a\3\2\2\2.\u02a4\3\2\2\2\60\u02db\3\2\2\2")
        buf.write("\62\u02e9\3\2\2\2\64\u02ef\3\2\2\2\66\u02f9\3\2\2\28\u031c")
        buf.write("\3\2\2\2:\u031e\3\2\2\2<\u0320\3\2\2\2>@\5\b\5\2?>\3\2")
        buf.write("\2\2@C\3\2\2\2A?\3\2\2\2AB\3\2\2\2BD\3\2\2\2CA\3\2\2\2")
        buf.write("DE\7\2\2\3E\3\3\2\2\2FG\5\n\6\2GH\7\2\2\3HZ\3\2\2\2IJ")
        buf.write("\5\20\t\2JK\7\2\2\3KZ\3\2\2\2LN\5\6\4\2MO\7\u00b1\2\2")
        buf.write("NM\3\2\2\2NO\3\2\2\2OP\3\2\2\2PQ\7\2\2\3QZ\3\2\2\2RT\5")
        buf.write("\26\f\2SU\7\u00b1\2\2TS\3\2\2\2TU\3\2\2\2UV\3\2\2\2VW")
        buf.write("\7\2\2\3WZ\3\2\2\2XZ\7\2\2\3YF\3\2\2\2YI\3\2\2\2YL\3\2")
        buf.write("\2\2YR\3\2\2\2YX\3\2\2\2Z\5\3\2\2\2[\\\7\u00ab\2\2\\]")
        buf.write("\5\66\34\2]^\7\u00a5\2\2^_\5\26\f\2_`\b\4\1\2`a\b\4\1")
        buf.write("\2a\u0081\3\2\2\2bd\7\u00ab\2\2cb\3\2\2\2cd\3\2\2\2de")
        buf.write("\3\2\2\2ef\5*\26\2fg\7\u00b8\2\2gi\7\u00a5\2\2hj\5\26")
        buf.write("\f\2ih\3\2\2\2ij\3\2\2\2jk\3\2\2\2kl\b\4\1\2lm\b\4\1\2")
        buf.write("m\u0081\3\2\2\2no\7\u00ab\2\2op\5*\26\2pq\7\u00b8\2\2")
        buf.write("qr\b\4\1\2rs\b\4\1\2s\u0081\3\2\2\2tv\7\u00ab\2\2ut\3")
        buf.write("\2\2\2uv\3\2\2\2vw\3\2\2\2wx\5*\26\2x{\5\66\34\2yz\7\u00a5")
        buf.write("\2\2z|\5\26\f\2{y\3\2\2\2{|\3\2\2\2|}\3\2\2\2}~\b\4\1")
        buf.write("\2~\177\b\4\1\2\177\u0081\3\2\2\2\u0080[\3\2\2\2\u0080")
        buf.write("c\3\2\2\2\u0080n\3\2\2\2\u0080u\3\2\2\2\u0081\7\3\2\2")
        buf.write("\2\u0082\u0083\5\6\4\2\u0083\u0084\7\u00b1\2\2\u0084\u009f")
        buf.write("\3\2\2\2\u0085\u0086\7\3\2\2\u0086\u0087\5\26\f\2\u0087")
        buf.write("\u008f\5\n\6\2\u0088\u0089\7\4\2\2\u0089\u008a\7\3\2\2")
        buf.write("\u008a\u008b\5\26\f\2\u008b\u008c\5\n\6\2\u008c\u008e")
        buf.write("\3\2\2\2\u008d\u0088\3\2\2\2\u008e\u0091\3\2\2\2\u008f")
        buf.write("\u008d\3\2\2\2\u008f\u0090\3\2\2\2\u0090\u0094\3\2\2\2")
        buf.write("\u0091\u008f\3\2\2\2\u0092\u0093\7\4\2\2\u0093\u0095\5")
        buf.write("\n\6\2\u0094\u0092\3\2\2\2\u0094\u0095\3\2\2\2\u0095\u009f")
        buf.write("\3\2\2\2\u0096\u0097\5\26\f\2\u0097\u0098\7\u00b1\2\2")
        buf.write("\u0098\u009f\3\2\2\2\u0099\u009f\5\20\t\2\u009a\u009b")
        buf.write("\5\22\n\2\u009b\u009c\7\u00b1\2\2\u009c\u009f\3\2\2\2")
        buf.write("\u009d\u009f\5\n\6\2\u009e\u0082\3\2\2\2\u009e\u0085\3")
        buf.write("\2\2\2\u009e\u0096\3\2\2\2\u009e\u0099\3\2\2\2\u009e\u009a")
        buf.write("\3\2\2\2\u009e\u009d\3\2\2\2\u009f\t\3\2\2\2\u00a0\u00a4")
        buf.write("\7\5\2\2\u00a1\u00a3\5\b\5\2\u00a2\u00a1\3\2\2\2\u00a3")
        buf.write("\u00a6\3\2\2\2\u00a4\u00a2\3\2\2\2\u00a4\u00a5\3\2\2\2")
        buf.write("\u00a5\u00a7\3\2\2\2\u00a6\u00a4\3\2\2\2\u00a7\u00b1\7")
        buf.write("\6\2\2\u00a8\u00ac\7\7\2\2\u00a9\u00ab\5\b\5\2\u00aa\u00a9")
        buf.write("\3\2\2\2\u00ab\u00ae\3\2\2\2\u00ac\u00aa\3\2\2\2\u00ac")
        buf.write("\u00ad\3\2\2\2\u00ad\u00af\3\2\2\2\u00ae\u00ac\3\2\2\2")
        buf.write("\u00af\u00b1\7\b\2\2\u00b0\u00a0\3\2\2\2\u00b0\u00a8\3")
        buf.write("\2\2\2\u00b1\13\3\2\2\2\u00b2\u00b3\5\26\f\2\u00b3\u00b4")
        buf.write("\7\t\2\2\u00b4\u00d1\3\2\2\2\u00b5\u00b6\7\n\2\2\u00b6")
        buf.write("\u00d1\5\26\f\2\u00b7\u00b8\t\2\2\2\u00b8\u00d1\5\26\f")
        buf.write("\2\u00b9\u00ba\7\13\2\2\u00ba\u00bb\5\66\34\2\u00bb\u00bc")
        buf.write("\7\f\2\2\u00bc\u00bd\5\26\f\2\u00bd\u00d1\3\2\2\2\u00be")
        buf.write("\u00bf\7\13\2\2\u00bf\u00c0\5\66\34\2\u00c0\u00c1\5\16")
        buf.write("\b\2\u00c1\u00c2\7\r\2\2\u00c2\u00c5\5\26\f\2\u00c3\u00c4")
        buf.write("\7\16\2\2\u00c4\u00c6\5\26\f\2\u00c5\u00c3\3\2\2\2\u00c5")
        buf.write("\u00c6\3\2\2\2\u00c6\u00d1\3\2\2\2\u00c7\u00c8\7\13\2")
        buf.write("\2\u00c8\u00c9\5&\24\2\u00c9\u00ca\5\16\b\2\u00ca\u00cb")
        buf.write("\7\r\2\2\u00cb\u00ce\5\26\f\2\u00cc\u00cd\7\16\2\2\u00cd")
        buf.write("\u00cf\5\26\f\2\u00ce\u00cc\3\2\2\2\u00ce\u00cf\3\2\2")
        buf.write("\2\u00cf\u00d1\3\2\2\2\u00d0\u00b2\3\2\2\2\u00d0\u00b5")
        buf.write("\3\2\2\2\u00d0\u00b7\3\2\2\2\u00d0\u00b9\3\2\2\2\u00d0")
        buf.write("\u00be\3\2\2\2\u00d0\u00c7\3\2\2\2\u00d1\r\3\2\2\2\u00d2")
        buf.write("\u00d3\7\u00a5\2\2\u00d3\u00d4\5\26\f\2\u00d4\u00d5\7")
        buf.write("\17\2\2\u00d5\u00d6\b\b\1\2\u00d6\u00de\3\2\2\2\u00d7")
        buf.write("\u00d8\7\u00a5\2\2\u00d8\u00d9\5\26\f\2\u00d9\u00da\b")
        buf.write("\b\1\2\u00da\u00de\3\2\2\2\u00db\u00dc\7\17\2\2\u00dc")
        buf.write("\u00de\b\b\1\2\u00dd\u00d2\3\2\2\2\u00dd\u00d7\3\2\2\2")
        buf.write("\u00dd\u00db\3\2\2\2\u00de\17\3\2\2\2\u00df\u00e0\7\20")
        buf.write("\2\2\u00e0\u00e1\5\66\34\2\u00e1\u00e2\7\u00b5\2\2\u00e2")
        buf.write("\u00e4\3\2\2\2\u00e3\u00df\3\2\2\2\u00e3\u00e4\3\2\2\2")
        buf.write("\u00e4\u00e5\3\2\2\2\u00e5\u00e6\7\21\2\2\u00e6\u00e7")
        buf.write("\5\f\7\2\u00e7\u00e8\5\n\6\2\u00e8\21\3\2\2\2\u00e9\u00eb")
        buf.write("\7\22\2\2\u00ea\u00ec\5\66\34\2\u00eb\u00ea\3\2\2\2\u00eb")
        buf.write("\u00ec\3\2\2\2\u00ec\u00ed\3\2\2\2\u00ed\u00ee\7\23\2")
        buf.write("\2\u00ee\23\3\2\2\2\u00ef\u00f0\7\u00b5\2\2\u00f0\u00f4")
        buf.write("\b\13\1\2\u00f1\u00f2\7\u00b6\2\2\u00f2\u00f4\b\13\1\2")
        buf.write("\u00f3\u00ef\3\2\2\2\u00f3\u00f1\3\2\2\2\u00f4\25\3\2")
        buf.write("\2\2\u00f5\u00f6\b\f\1\2\u00f6\u00f7\7\24\2\2\u00f7\u00f8")
        buf.write("\5\26\f\2\u00f8\u00f9\7\u00b6\2\2\u00f9\u015c\3\2\2\2")
        buf.write("\u00fa\u00fb\7\24\2\2\u00fb\u00fc\5\26\f\2\u00fc\u00fd")
        buf.write("\7\25\2\2\u00fd\u00fe\5\26\f\2\u00fe\u00ff\7\u00b6\2\2")
        buf.write("\u00ff\u015c\3\2\2\2\u0100\u0101\7\u00b0\2\2\u0101\u015c")
        buf.write("\5\26\f\61\u0102\u0103\5.\30\2\u0103\u0104\7\26\2\2\u0104")
        buf.write("\u0105\5\26\f/\u0105\u015c\3\2\2\2\u0106\u0107\7\u00b8")
        buf.write("\2\2\u0107\u015c\5\36\20\2\u0108\u010a\7\37\2\2\u0109")
        buf.write("\u0108\3\2\2\2\u0109\u010a\3\2\2\2\u010a\u010b\3\2\2\2")
        buf.write("\u010b\u010d\5\30\r\2\u010c\u010e\7 \2\2\u010d\u010c\3")
        buf.write("\2\2\2\u010d\u010e\3\2\2\2\u010e\u015c\3\2\2\2\u010f\u0111")
        buf.write("\t\3\2\2\u0110\u010f\3\2\2\2\u0110\u0111\3\2\2\2\u0111")
        buf.write("\u0112\3\2\2\2\u0112\u0114\7 \2\2\u0113\u0115\7!\2\2\u0114")
        buf.write("\u0113\3\2\2\2\u0114\u0115\3\2\2\2\u0115\u0116\3\2\2\2")
        buf.write("\u0116\u015c\5\26\f$\u0117\u0118\7\u00ad\2\2\u0118\u015c")
        buf.write("\5\26\f\35\u0119\u011a\5\32\16\2\u011a\u011b\5\26\f\32")
        buf.write("\u011b\u015c\3\2\2\2\u011c\u015c\5\32\16\2\u011d\u011f")
        buf.write("\7\r\2\2\u011e\u0120\5 \21\2\u011f\u011e\3\2\2\2\u011f")
        buf.write("\u0120\3\2\2\2\u0120\u0121\3\2\2\2\u0121\u015c\5\26\f")
        buf.write("\30\u0122\u0124\t\4\2\2\u0123\u0125\7\n\2\2\u0124\u0123")
        buf.write("\3\2\2\2\u0124\u0125\3\2\2\2\u0125\u0126\3\2\2\2\u0126")
        buf.write("\u015c\5\26\f\27\u0127\u0128\t\4\2\2\u0128\u0129\7\n\2")
        buf.write("\2\u0129\u012c\7*\2\2\u012a\u012c\7+\2\2\u012b\u0127\3")
        buf.write("\2\2\2\u012b\u012a\3\2\2\2\u012c\u0135\3\2\2\2\u012d\u0132")
        buf.write("\5\26\f\2\u012e\u012f\7\25\2\2\u012f\u0131\5\26\f\2\u0130")
        buf.write("\u012e\3\2\2\2\u0131\u0134\3\2\2\2\u0132\u0130\3\2\2\2")
        buf.write("\u0132\u0133\3\2\2\2\u0133\u0136\3\2\2\2\u0134\u0132\3")
        buf.write("\2\2\2\u0135\u012d\3\2\2\2\u0135\u0136\3\2\2\2\u0136\u015c")
        buf.write("\3\2\2\2\u0137\u0138\7,\2\2\u0138\u013d\5\26\f\2\u0139")
        buf.write("\u013a\7\25\2\2\u013a\u013c\5\26\f\2\u013b\u0139\3\2\2")
        buf.write("\2\u013c\u013f\3\2\2\2\u013d\u013b\3\2\2\2\u013d\u013e")
        buf.write("\3\2\2\2\u013e\u015c\3\2\2\2\u013f\u013d\3\2\2\2\u0140")
        buf.write("\u0141\7-\2\2\u0141\u0142\t\5\2\2\u0142\u015c\5\26\f\23")
        buf.write("\u0143\u015c\5\"\22\2\u0144\u015c\5(\25\2\u0145\u0147")
        buf.write("\7\37\2\2\u0146\u0145\3\2\2\2\u0146\u0147\3\2\2\2\u0147")
        buf.write("\u0148\3\2\2\2\u0148\u015c\5*\26\2\u0149\u014a\5*\26\2")
        buf.write("\u014a\u014b\7\u00b8\2\2\u014b\u015c\3\2\2\2\u014c\u015c")
        buf.write("\5\64\33\2\u014d\u015c\5\66\34\2\u014e\u015c\58\35\2\u014f")
        buf.write("\u0150\5\66\34\2\u0150\u0151\7\u00a5\2\2\u0151\u0152\5")
        buf.write("\26\f\b\u0152\u015c\3\2\2\2\u0153\u0154\5*\26\2\u0154")
        buf.write("\u0155\7\u00b8\2\2\u0155\u0156\7\u00a5\2\2\u0156\u0157")
        buf.write("\5\26\f\6\u0157\u015c\3\2\2\2\u0158\u015c\5<\37\2\u0159")
        buf.write("\u015c\7\u00b8\2\2\u015a\u015c\7\u00b9\2\2\u015b\u00f5")
        buf.write("\3\2\2\2\u015b\u00fa\3\2\2\2\u015b\u0100\3\2\2\2\u015b")
        buf.write("\u0102\3\2\2\2\u015b\u0106\3\2\2\2\u015b\u0109\3\2\2\2")
        buf.write("\u015b\u0110\3\2\2\2\u015b\u0117\3\2\2\2\u015b\u0119\3")
        buf.write("\2\2\2\u015b\u011c\3\2\2\2\u015b\u011d\3\2\2\2\u015b\u0122")
        buf.write("\3\2\2\2\u015b\u012b\3\2\2\2\u015b\u0137\3\2\2\2\u015b")
        buf.write("\u0140\3\2\2\2\u015b\u0143\3\2\2\2\u015b\u0144\3\2\2\2")
        buf.write("\u015b\u0146\3\2\2\2\u015b\u0149\3\2\2\2\u015b\u014c\3")
        buf.write("\2\2\2\u015b\u014d\3\2\2\2\u015b\u014e\3\2\2\2\u015b\u014f")
        buf.write("\3\2\2\2\u015b\u0153\3\2\2\2\u015b\u0158\3\2\2\2\u015b")
        buf.write("\u0159\3\2\2\2\u015b\u015a\3\2\2\2\u015c\u01c2\3\2\2\2")
        buf.write("\u015d\u015e\f*\2\2\u015e\u015f\7\f\2\2\u015f\u0160\t")
        buf.write("\6\2\2\u0160\u01c1\5\26\f+\u0161\u0162\f#\2\2\u0162\u0163")
        buf.write("\7\"\2\2\u0163\u01c1\5\26\f$\u0164\u0165\f\"\2\2\u0165")
        buf.write("\u0166\t\7\2\2\u0166\u01c1\5\26\f#\u0167\u0168\f!\2\2")
        buf.write("\u0168\u0169\t\b\2\2\u0169\u01c1\5\26\f\"\u016a\u016b")
        buf.write("\f \2\2\u016b\u016c\5\62\32\2\u016c\u016d\5\26\f!\u016d")
        buf.write("\u01c1\3\2\2\2\u016e\u0174\f\36\2\2\u016f\u0171\7%\2\2")
        buf.write("\u0170\u0172\7\u00ad\2\2\u0171\u0170\3\2\2\2\u0171\u0172")
        buf.write("\3\2\2\2\u0172\u0175\3\2\2\2\u0173\u0175\7\u00aa\2\2\u0174")
        buf.write("\u016f\3\2\2\2\u0174\u0173\3\2\2\2\u0175\u0176\3\2\2\2")
        buf.write("\u0176\u01c1\5\26\f\37\u0177\u0178\f\34\2\2\u0178\u0179")
        buf.write("\7&\2\2\u0179\u01c1\5\26\f\35\u017a\u017b\f\33\2\2\u017b")
        buf.write("\u017c\7\'\2\2\u017c\u01c1\5\26\f\34\u017d\u017e\f\22")
        buf.write("\2\2\u017e\u017f\t\5\2\2\u017f\u01c1\5\26\f\23\u0180\u0181")
        buf.write("\f\21\2\2\u0181\u0182\7\u00a9\2\2\u0182\u01c1\5\26\f\22")
        buf.write("\u0183\u0184\f\20\2\2\u0184\u0185\7\3\2\2\u0185\u0186")
        buf.write("\5\26\f\2\u0186\u0187\7\4\2\2\u0187\u0188\5\26\f\21\u0188")
        buf.write("\u01c1\3\2\2\2\u0189\u018a\f\7\2\2\u018a\u018b\7\u00a6")
        buf.write("\2\2\u018b\u018c\5\60\31\2\u018c\u018d\7\u00a5\2\2\u018d")
        buf.write("\u018e\5\26\f\b\u018e\u01c1\3\2\2\2\u018f\u0190\f\63\2")
        buf.write("\2\u0190\u0199\7\24\2\2\u0191\u0196\5\26\f\2\u0192\u0193")
        buf.write("\7\25\2\2\u0193\u0195\5\26\f\2\u0194\u0192\3\2\2\2\u0195")
        buf.write("\u0198\3\2\2\2\u0196\u0194\3\2\2\2\u0196\u0197\3\2\2\2")
        buf.write("\u0197\u019a\3\2\2\2\u0198\u0196\3\2\2\2\u0199\u0191\3")
        buf.write("\2\2\2\u0199\u019a\3\2\2\2\u019a\u019b\3\2\2\2\u019b\u01c1")
        buf.write("\7\u00b6\2\2\u019c\u019d\f\60\2\2\u019d\u01c1\5\32\16")
        buf.write("\2\u019e\u019f\f.\2\2\u019f\u01a0\7\u00a6\2\2\u01a0\u01a1")
        buf.write("\7\27\2\2\u01a1\u01a2\7\f\2\2\u01a2\u01c1\5,\27\2\u01a3")
        buf.write("\u01a4\f-\2\2\u01a4\u01a6\7\30\2\2\u01a5\u01a7\7\31\2")
        buf.write("\2\u01a6\u01a5\3\2\2\2\u01a6\u01a7\3\2\2\2\u01a7\u01a8")
        buf.write("\3\2\2\2\u01a8\u01a9\7\32\2\2\u01a9\u01aa\7\f\2\2\u01aa")
        buf.write("\u01c1\5,\27\2\u01ab\u01ac\f,\2\2\u01ac\u01ad\7\u00a6")
        buf.write("\2\2\u01ad\u01c1\5\60\31\2\u01ae\u01af\f+\2\2\u01af\u01b0")
        buf.write("\7\33\2\2\u01b0\u01c1\5\34\17\2\u01b1\u01b2\f(\2\2\u01b2")
        buf.write("\u01c1\5\36\20\2\u01b3\u01b4\f\'\2\2\u01b4\u01c1\5,\27")
        buf.write("\2\u01b5\u01b6\f&\2\2\u01b6\u01c1\7\36\2\2\u01b7\u01b8")
        buf.write("\f\37\2\2\u01b8\u01b9\7#\2\2\u01b9\u01ba\t\t\2\2\u01ba")
        buf.write("\u01c1\5\60\31\2\u01bb\u01bc\f\24\2\2\u01bc\u01bd\7\20")
        buf.write("\2\2\u01bd\u01be\5\26\f\2\u01be\u01bf\7\u00b5\2\2\u01bf")
        buf.write("\u01c1\3\2\2\2\u01c0\u015d\3\2\2\2\u01c0\u0161\3\2\2\2")
        buf.write("\u01c0\u0164\3\2\2\2\u01c0\u0167\3\2\2\2\u01c0\u016a\3")
        buf.write("\2\2\2\u01c0\u016e\3\2\2\2\u01c0\u0177\3\2\2\2\u01c0\u017a")
        buf.write("\3\2\2\2\u01c0\u017d\3\2\2\2\u01c0\u0180\3\2\2\2\u01c0")
        buf.write("\u0183\3\2\2\2\u01c0\u0189\3\2\2\2\u01c0\u018f\3\2\2\2")
        buf.write("\u01c0\u019c\3\2\2\2\u01c0\u019e\3\2\2\2\u01c0\u01a3\3")
        buf.write("\2\2\2\u01c0\u01ab\3\2\2\2\u01c0\u01ae\3\2\2\2\u01c0\u01b1")
        buf.write("\3\2\2\2\u01c0\u01b3\3\2\2\2\u01c0\u01b5\3\2\2\2\u01c0")
        buf.write("\u01b7\3\2\2\2\u01c0\u01bb\3\2\2\2\u01c1\u01c4\3\2\2\2")
        buf.write("\u01c2\u01c0\3\2\2\2\u01c2\u01c3\3\2\2\2\u01c3\27\3\2")
        buf.write("\2\2\u01c4\u01c2\3\2\2\2\u01c5\u01c6\7\60\2\2\u01c6\u01ca")
        buf.write("\b\r\1\2\u01c7\u01c8\7\61\2\2\u01c8\u01ca\b\r\1\2\u01c9")
        buf.write("\u01c5\3\2\2\2\u01c9\u01c7\3\2\2\2\u01ca\31\3\2\2\2\u01cb")
        buf.write("\u01cc\t\n\2\2\u01cc\u01cd\b\16\1\2\u01cd\u01d8\b\16\1")
        buf.write("\2\u01ce\u01cf\t\13\2\2\u01cf\u01d0\b\16\1\2\u01d0\u01d8")
        buf.write("\b\16\1\2\u01d1\u01d2\t\f\2\2\u01d2\u01d3\b\16\1\2\u01d3")
        buf.write("\u01d8\b\16\1\2\u01d4\u01d5\t\r\2\2\u01d5\u01d6\b\16\1")
        buf.write("\2\u01d6\u01d8\b\16\1\2\u01d7\u01cb\3\2\2\2\u01d7\u01ce")
        buf.write("\3\2\2\2\u01d7\u01d1\3\2\2\2\u01d7\u01d4\3\2\2\2\u01d8")
        buf.write("\33\3\2\2\2\u01d9\u01da\t\16\2\2\u01da\u01e0\b\17\1\2")
        buf.write("\u01db\u01dc\t\17\2\2\u01dc\u01e0\b\17\1\2\u01dd\u01de")
        buf.write("\7;\2\2\u01de\u01e0\b\17\1\2\u01df\u01d9\3\2\2\2\u01df")
        buf.write("\u01db\3\2\2\2\u01df\u01dd\3\2\2\2\u01e0\35\3\2\2\2\u01e1")
        buf.write("\u01e2\6\20\31\3\u01e2\u01e3\7<\2\2\u01e3\u01e4\b\20\1")
        buf.write("\2\u01e4\u01f0\b\20\1\2\u01e5\u01e6\7=\2\2\u01e6\u01e7")
        buf.write("\b\20\1\2\u01e7\u01f0\b\20\1\2\u01e8\u01e9\6\20\32\3\u01e9")
        buf.write("\u01ea\t\20\2\2\u01ea\u01eb\b\20\1\2\u01eb\u01f0\b\20")
        buf.write("\1\2\u01ec\u01ed\t\21\2\2\u01ed\u01ee\b\20\1\2\u01ee\u01f0")
        buf.write("\b\20\1\2\u01ef\u01e1\3\2\2\2\u01ef\u01e5\3\2\2\2\u01ef")
        buf.write("\u01e8\3\2\2\2\u01ef\u01ec\3\2\2\2\u01f0\37\3\2\2\2\u01f1")
        buf.write("\u01f2\7<\2\2\u01f2\u01f6\b\21\1\2\u01f3\u01f4\t\20\2")
        buf.write("\2\u01f4\u01f6\b\21\1\2\u01f5\u01f1\3\2\2\2\u01f5\u01f3")
        buf.write("\3\2\2\2\u01f6!\3\2\2\2\u01f7\u01fa\5$\23\2\u01f8\u01fb")
        buf.write("\5\n\6\2\u01f9\u01fb\5\26\f\2\u01fa\u01f8\3\2\2\2\u01fa")
        buf.write("\u01f9\3\2\2\2\u01fb#\3\2\2\2\u01fc\u01fd\7B\2\2\u01fd")
        buf.write("\u0206\7\24\2\2\u01fe\u0203\5&\24\2\u01ff\u0200\7\25\2")
        buf.write("\2\u0200\u0202\5&\24\2\u0201\u01ff\3\2\2\2\u0202\u0205")
        buf.write("\3\2\2\2\u0203\u0201\3\2\2\2\u0203\u0204\3\2\2\2\u0204")
        buf.write("\u0207\3\2\2\2\u0205\u0203\3\2\2\2\u0206\u01fe\3\2\2\2")
        buf.write("\u0206\u0207\3\2\2\2\u0207\u0208\3\2\2\2\u0208\u0209\7")
        buf.write("\u00b6\2\2\u0209%\3\2\2\2\u020a\u020c\t\t\2\2\u020b\u020a")
        buf.write("\3\2\2\2\u020b\u020c\3\2\2\2\u020c\u020d\3\2\2\2\u020d")
        buf.write("\u020e\5*\26\2\u020e\u020f\b\24\1\2\u020f\u0222\3\2\2")
        buf.write("\2\u0210\u0211\5*\26\2\u0211\u0212\b\24\1\2\u0212\u0213")
        buf.write("\7\u00b8\2\2\u0213\u0214\b\24\1\2\u0214\u0222\3\2\2\2")
        buf.write("\u0215\u0216\5*\26\2\u0216\u0217\5\66\34\2\u0217\u0218")
        buf.write("\b\24\1\2\u0218\u0219\b\24\1\2\u0219\u0222\3\2\2\2\u021a")
        buf.write("\u021b\5\66\34\2\u021b\u021c\7\u00a9\2\2\u021c\u021d\5")
        buf.write("*\26\2\u021d\u021e\b\24\1\2\u021e\u021f\b\24\1\2\u021f")
        buf.write("\u0220\b\24\1\2\u0220\u0222\3\2\2\2\u0221\u020b\3\2\2")
        buf.write("\2\u0221\u0210\3\2\2\2\u0221\u0215\3\2\2\2\u0221\u021a")
        buf.write("\3\2\2\2\u0222\'\3\2\2\2\u0223\u0224\7C\2\2\u0224\u0225")
        buf.write("\7\u00af\2\2\u0225\u0247\b\25\1\2\u0226\u0227\7C\2\2\u0227")
        buf.write("\u0228\7\u00ae\2\2\u0228\u0247\b\25\1\2\u0229\u022b\7")
        buf.write("\u00b2\2\2\u022a\u022c\7D\2\2\u022b\u022a\3\2\2\2\u022b")
        buf.write("\u022c\3\2\2\2\u022c\u022d\3\2\2\2\u022d\u0247\b\25\1")
        buf.write("\2\u022e\u0234\7E\2\2\u022f\u0231\7F\2\2\u0230\u0232\7")
        buf.write("\37\2\2\u0231\u0230\3\2\2\2\u0231\u0232\3\2\2\2\u0232")
        buf.write("\u0233\3\2\2\2\u0233\u0235\7G\2\2\u0234\u022f\3\2\2\2")
        buf.write("\u0234\u0235\3\2\2\2\u0235\u0236\3\2\2\2\u0236\u0247\b")
        buf.write("\25\1\2\u0237\u0238\7H\2\2\u0238\u0239\7I\2\2\u0239\u0247")
        buf.write("\b\25\1\2\u023a\u023b\7H\2\2\u023b\u023c\7J\2\2\u023c")
        buf.write("\u0247\b\25\1\2\u023d\u023e\7H\2\2\u023e\u023f\7K\2\2")
        buf.write("\u023f\u0247\b\25\1\2\u0240\u0241\7H\2\2\u0241\u0242\7")
        buf.write("L\2\2\u0242\u0247\b\25\1\2\u0243\u0244\7H\2\2\u0244\u0245")
        buf.write("\7M\2\2\u0245\u0247\b\25\1\2\u0246\u0223\3\2\2\2\u0246")
        buf.write("\u0226\3\2\2\2\u0246\u0229\3\2\2\2\u0246\u022e\3\2\2\2")
        buf.write("\u0246\u0237\3\2\2\2\u0246\u023a\3\2\2\2\u0246\u023d\3")
        buf.write("\2\2\2\u0246\u0240\3\2\2\2\u0246\u0243\3\2\2\2\u0247)")
        buf.write("\3\2\2\2\u0248\u0249\7-\2\2\u0249\u028b\b\26\1\2\u024a")
        buf.write("\u024b\7N\2\2\u024b\u028b\b\26\1\2\u024c\u024d\7O\2\2")
        buf.write("\u024d\u028b\b\26\1\2\u024e\u024f\7O\2\2\u024f\u0250\7")
        buf.write("N\2\2\u0250\u028b\b\26\1\2\u0251\u0253\7O\2\2\u0252\u0251")
        buf.write("\3\2\2\2\u0252\u0253\3\2\2\2\u0253\u0254\3\2\2\2\u0254")
        buf.write("\u0255\7P\2\2\u0255\u028b\b\26\1\2\u0256\u0257\7Q\2\2")
        buf.write("\u0257\u028b\b\26\1\2\u0258\u0259\7R\2\2\u0259\u028b\b")
        buf.write("\26\1\2\u025a\u025b\7\32\2\2\u025b\u028b\b\26\1\2\u025c")
        buf.write("\u025d\7D\2\2\u025d\u028b\b\26\1\2\u025e\u025f\7S\2\2")
        buf.write("\u025f\u028b\b\26\1\2\u0260\u0261\7T\2\2\u0261\u028b\b")
        buf.write("\26\1\2\u0262\u0263\7U\2\2\u0263\u028b\b\26\1\2\u0264")
        buf.write("\u0265\7V\2\2\u0265\u028b\b\26\1\2\u0266\u0267\7W\2\2")
        buf.write("\u0267\u028b\b\26\1\2\u0268\u0269\7X\2\2\u0269\u028b\b")
        buf.write("\26\1\2\u026a\u026b\7Y\2\2\u026b\u028b\b\26\1\2\u026c")
        buf.write("\u026d\t\6\2\2\u026d\u028b\b\26\1\2\u026e\u026f\7Z\2\2")
        buf.write("\u026f\u028b\b\26\1\2\u0270\u0271\7 \2\2\u0271\u028b\b")
        buf.write("\26\1\2\u0272\u0273\7[\2\2\u0273\u028b\b\26\1\2\u0274")
        buf.write("\u0275\t\22\2\2\u0275\u0276\t\23\2\2\u0276\u028b\b\26")
        buf.write("\1\2\u0277\u0279\t\22\2\2\u0278\u027a\7`\2\2\u0279\u0278")
        buf.write("\3\2\2\2\u0279\u027a\3\2\2\2\u027a\u027b\3\2\2\2\u027b")
        buf.write("\u028b\b\26\1\2\u027c\u027d\7a\2\2\u027d\u028b\b\26\1")
        buf.write("\2\u027e\u027f\7b\2\2\u027f\u028b\b\26\1\2\u0280\u0281")
        buf.write("\7c\2\2\u0281\u028b\b\26\1\2\u0282\u0283\7d\2\2\u0283")
        buf.write("\u0284\7e\2\2\u0284\u028b\b\26\1\2\u0285\u0286\7d\2\2")
        buf.write("\u0286\u0287\7f\2\2\u0287\u028b\b\26\1\2\u0288\u0289\7")
        buf.write("g\2\2\u0289\u028b\b\26\1\2\u028a\u0248\3\2\2\2\u028a\u024a")
        buf.write("\3\2\2\2\u028a\u024c\3\2\2\2\u028a\u024e\3\2\2\2\u028a")
        buf.write("\u0252\3\2\2\2\u028a\u0256\3\2\2\2\u028a\u0258\3\2\2\2")
        buf.write("\u028a\u025a\3\2\2\2\u028a\u025c\3\2\2\2\u028a\u025e\3")
        buf.write("\2\2\2\u028a\u0260\3\2\2\2\u028a\u0262\3\2\2\2\u028a\u0264")
        buf.write("\3\2\2\2\u028a\u0266\3\2\2\2\u028a\u0268\3\2\2\2\u028a")
        buf.write("\u026a\3\2\2\2\u028a\u026c\3\2\2\2\u028a\u026e\3\2\2\2")
        buf.write("\u028a\u0270\3\2\2\2\u028a\u0272\3\2\2\2\u028a\u0274\3")
        buf.write("\2\2\2\u028a\u0277\3\2\2\2\u028a\u027c\3\2\2\2\u028a\u027e")
        buf.write("\3\2\2\2\u028a\u0280\3\2\2\2\u028a\u0282\3\2\2\2\u028a")
        buf.write("\u0285\3\2\2\2\u028a\u0288\3\2\2\2\u028b+\3\2\2\2\u028c")
        buf.write("\u028d\t\24\2\2\u028d\u029b\b\27\1\2\u028e\u028f\t\25")
        buf.write("\2\2\u028f\u029b\b\27\1\2\u0290\u0291\t\26\2\2\u0291\u029b")
        buf.write("\b\27\1\2\u0292\u0293\t\27\2\2\u0293\u029b\b\27\1\2\u0294")
        buf.write("\u0295\t\30\2\2\u0295\u029b\b\27\1\2\u0296\u0297\t\31")
        buf.write("\2\2\u0297\u029b\b\27\1\2\u0298\u0299\t\32\2\2\u0299\u029b")
        buf.write("\b\27\1\2\u029a\u028c\3\2\2\2\u029a\u028e\3\2\2\2\u029a")
        buf.write("\u0290\3\2\2\2\u029a\u0292\3\2\2\2\u029a\u0294\3\2\2\2")
        buf.write("\u029a\u0296\3\2\2\2\u029a\u0298\3\2\2\2\u029b-\3\2\2")
        buf.write("\2\u029c\u029d\7O\2\2\u029d\u02a5\b\30\1\2\u029e\u029f")
        buf.write("\7a\2\2\u029f\u02a5\b\30\1\2\u02a0\u02a1\7b\2\2\u02a1")
        buf.write("\u02a5\b\30\1\2\u02a2\u02a3\7c\2\2\u02a3\u02a5\b\30\1")
        buf.write("\2\u02a4\u029c\3\2\2\2\u02a4\u029e\3\2\2\2\u02a4\u02a0")
        buf.write("\3\2\2\2\u02a4\u02a2\3\2\2\2\u02a5/\3\2\2\2\u02a6\u02a7")
        buf.write("\7\22\2\2\u02a7\u02a8\7N\2\2\u02a8\u02dc\b\31\1\2\u02a9")
        buf.write("\u02aa\7P\2\2\u02aa\u02dc\b\31\1\2\u02ab\u02ac\t\6\2\2")
        buf.write("\u02ac\u02dc\b\31\1\2\u02ad\u02b1\7<\2\2\u02ae\u02af\7")
        buf.write("\u0081\2\2\u02af\u02b1\t\33\2\2\u02b0\u02ad\3\2\2\2\u02b0")
        buf.write("\u02ae\3\2\2\2\u02b1\u02b2\3\2\2\2\u02b2\u02dc\b\31\1")
        buf.write("\2\u02b3\u02b8\7>\2\2\u02b4\u02b8\7?\2\2\u02b5\u02b6\7")
        buf.write("\u0084\2\2\u02b6\u02b8\t\33\2\2\u02b7\u02b3\3\2\2\2\u02b7")
        buf.write("\u02b4\3\2\2\2\u02b7\u02b5\3\2\2\2\u02b8\u02b9\3\2\2\2")
        buf.write("\u02b9\u02dc\b\31\1\2\u02ba\u02bb\7\22\2\2\u02bb\u02bc")
        buf.write("\t\6\2\2\u02bc\u02dc\b\31\1\2\u02bd\u02be\7\u0085\2\2")
        buf.write("\u02be\u02bf\7\u0086\2\2\u02bf\u02dc\b\31\1\2\u02c0\u02c2")
        buf.write("\7\u0087\2\2\u02c1\u02c3\t\22\2\2\u02c2\u02c1\3\2\2\2")
        buf.write("\u02c2\u02c3\3\2\2\2\u02c3\u02c4\3\2\2\2\u02c4\u02dc\b")
        buf.write("\31\1\2\u02c5\u02c7\7\u0088\2\2\u02c6\u02c5\3\2\2\2\u02c6")
        buf.write("\u02c7\3\2\2\2\u02c7\u02c8\3\2\2\2\u02c8\u02c9\t\22\2")
        buf.write("\2\u02c9\u02dc\b\31\1\2\u02ca\u02cb\7d\2\2\u02cb\u02cc")
        buf.write("\7e\2\2\u02cc\u02dc\b\31\1\2\u02cd\u02ce\t\34\2\2\u02ce")
        buf.write("\u02cf\7\u008b\2\2\u02cf\u02dc\b\31\1\2\u02d0\u02d1\t")
        buf.write("\35\2\2\u02d1\u02d2\7\u008b\2\2\u02d2\u02dc\b\31\1\2\u02d3")
        buf.write("\u02d4\t\34\2\2\u02d4\u02d5\t\36\2\2\u02d5\u02dc\b\31")
        buf.write("\1\2\u02d6\u02d7\t\35\2\2\u02d7\u02d8\t\36\2\2\u02d8\u02dc")
        buf.write("\b\31\1\2\u02d9\u02da\t\37\2\2\u02da\u02dc\b\31\1\2\u02db")
        buf.write("\u02a6\3\2\2\2\u02db\u02a9\3\2\2\2\u02db\u02ab\3\2\2\2")
        buf.write("\u02db\u02b0\3\2\2\2\u02db\u02b7\3\2\2\2\u02db\u02ba\3")
        buf.write("\2\2\2\u02db\u02bd\3\2\2\2\u02db\u02c0\3\2\2\2\u02db\u02c6")
        buf.write("\3\2\2\2\u02db\u02ca\3\2\2\2\u02db\u02cd\3\2\2\2\u02db")
        buf.write("\u02d0\3\2\2\2\u02db\u02d3\3\2\2\2\u02db\u02d6\3\2\2\2")
        buf.write("\u02db\u02d9\3\2\2\2\u02dc\61\3\2\2\2\u02dd\u02de\7\u008e")
        buf.write("\2\2\u02de\u02ea\b\32\1\2\u02df\u02e0\7\u008f\2\2\u02e0")
        buf.write("\u02ea\b\32\1\2\u02e1\u02e2\7\u0090\2\2\u02e2\u02ea\b")
        buf.write("\32\1\2\u02e3\u02e4\7\u0091\2\2\u02e4\u02ea\b\32\1\2\u02e5")
        buf.write("\u02e6\7\u0092\2\2\u02e6\u02ea\b\32\1\2\u02e7\u02e8\7")
        buf.write("\u0093\2\2\u02e8\u02ea\b\32\1\2\u02e9\u02dd\3\2\2\2\u02e9")
        buf.write("\u02df\3\2\2\2\u02e9\u02e1\3\2\2\2\u02e9\u02e3\3\2\2\2")
        buf.write("\u02e9\u02e5\3\2\2\2\u02e9\u02e7\3\2\2\2\u02ea\63\3\2")
        buf.write("\2\2\u02eb\u02ec\t \2\2\u02ec\u02f0\b\33\1\2\u02ed\u02ee")
        buf.write("\t!\2\2\u02ee\u02f0\b\33\1\2\u02ef\u02eb\3\2\2\2\u02ef")
        buf.write("\u02ed\3\2\2\2\u02f0\65\3\2\2\2\u02f1\u02f2\58\35\2\u02f2")
        buf.write("\u02f3\b\34\1\2\u02f3\u02fa\3\2\2\2\u02f4\u02f5\7\u00b7")
        buf.write("\2\2\u02f5\u02fa\b\34\1\2\u02f6\u02f7\5:\36\2\u02f7\u02f8")
        buf.write("\b\34\1\2\u02f8\u02fa\3\2\2\2\u02f9\u02f1\3\2\2\2\u02f9")
        buf.write("\u02f4\3\2\2\2\u02f9\u02f6\3\2\2\2\u02fa\67\3\2\2\2\u02fb")
        buf.write("\u02fd\7\u00af\2\2\u02fc\u02fe\7\37\2\2\u02fd\u02fc\3")
        buf.write("\2\2\2\u02fd\u02fe\3\2\2\2\u02fe\u02ff\3\2\2\2\u02ff\u0300")
        buf.write("\7G\2\2\u0300\u031d\b\35\1\2\u0301\u0303\7\37\2\2\u0302")
        buf.write("\u0301\3\2\2\2\u0302\u0303\3\2\2\2\u0303\u0304\3\2\2\2")
        buf.write("\u0304\u0305\7\u00a8\2\2\u0305\u0306\7 \2\2\u0306\u031d")
        buf.write("\b\35\1\2\u0307\u0309\7\37\2\2\u0308\u0307\3\2\2\2\u0308")
        buf.write("\u0309\3\2\2\2\u0309\u030a\3\2\2\2\u030a\u030b\7\u00a8")
        buf.write("\2\2\u030b\u030c\7Z\2\2\u030c\u031d\b\35\1\2\u030d\u030e")
        buf.write("\7\37\2\2\u030e\u030f\7G\2\2\u030f\u031d\b\35\1\2\u0310")
        buf.write("\u0312\7\37\2\2\u0311\u0310\3\2\2\2\u0311\u0312\3\2\2")
        buf.write("\2\u0312\u0313\3\2\2\2\u0313\u0314\7\u00a0\2\2\u0314\u0315")
        buf.write("\7\u00a1\2\2\u0315\u031d\b\35\1\2\u0316\u0317\7\u00a2")
        buf.write("\2\2\u0317\u0318\7-\2\2\u0318\u031d\b\35\1\2\u0319\u031a")
        buf.write("\7\u00a3\2\2\u031a\u031b\7O\2\2\u031b\u031d\b\35\1\2\u031c")
        buf.write("\u02fb\3\2\2\2\u031c\u0302\3\2\2\2\u031c\u0308\3\2\2\2")
        buf.write("\u031c\u030d\3\2\2\2\u031c\u0311\3\2\2\2\u031c\u0316\3")
        buf.write("\2\2\2\u031c\u0319\3\2\2\2\u031d9\3\2\2\2\u031e\u031f")
        buf.write("\t\"\2\2\u031f;\3\2\2\2\u0320\u0321\7\u00ba\2\2\u0321")
        buf.write("=\3\2\2\2KANTYciu{\u0080\u008f\u0094\u009e\u00a4\u00ac")
        buf.write("\u00b0\u00c5\u00ce\u00d0\u00dd\u00e3\u00eb\u00f3\u0109")
        buf.write("\u010d\u0110\u0114\u011f\u0124\u012b\u0132\u0135\u013d")
        buf.write("\u0146\u015b\u0171\u0174\u0196\u0199\u01a6\u01c0\u01c2")
        buf.write("\u01c9\u01d7\u01df\u01ef\u01f5\u01fa\u0203\u0206\u020b")
        buf.write("\u0221\u022b\u0231\u0234\u0246\u0252\u0279\u028a\u029a")
        buf.write("\u02a4\u02b0\u02b7\u02c2\u02c6\u02db\u02e9\u02ef\u02f9")
        buf.write("\u02fd\u0302\u0308\u0311\u031c")
        return buf.getvalue()


class DMFParser ( Parser ):

    grammarFileName = "DMF.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'else'", "'{'", "'}'", "'[['", 
                     "']]'", "'times'", "'for'", "'with'", "'in'", "'to'", 
                     "'by'", "'down'", "'['", "'repeat'", "'exit'", "'loop'", 
                     "'('", "','", "'#'", "'magnitude'", "'as'", "'a'", 
                     "'string'", "'turned'", "'dir'", "'direction'", "'C'", 
                     "'the'", "'reagent'", "'named'", "'of'", "'has'", "'an'", 
                     "'is'", "'and'", "'or'", "'pause'", "'wait'", "'user'", 
                     "'prompt'", "'print'", "'drop'", "'@'", "'at'", "'unknown'", 
                     "'waste'", "'up'", "'north'", "'south'", "'left'", 
                     "'west'", "'right'", "'east'", "'clockwise'", "'counterclockwise'", 
                     "'around'", "'row'", "'rows'", "'col'", "'column'", 
                     "'cols'", "'columns'", "'macro'", "'turn'", "'state'", 
                     "'remove'", "'from'", "'board'", "'reset'", "'pads'", 
                     "'magnets'", "'heaters'", "'chillers'", "'all'", "'pad'", 
                     "'well'", "'gate'", "'int'", "'float'", "'binary'", 
                     "'delta'", "'motion'", "'delay'", "'time'", "'ticks'", 
                     "'bool'", "'volume'", "'liquid'", "'temp'", "'temperature'", 
                     "'diff'", "'difference'", "'point'", "'heater'", "'chiller'", 
                     "'magnet'", "'power'", "'supply'", "'mode'", "'fan'", 
                     "'s'", "'sec'", "'secs'", "'second'", "'seconds'", 
                     "'ms'", "'millisecond'", "'milliseconds'", "'uL'", 
                     "'ul'", "'microliter'", "'microlitre'", "'microliters'", 
                     "'microlitres'", "'mL'", "'ml'", "'milliliter'", "'millilitre'", 
                     "'milliliters'", "'millilitres'", "'tick'", "'drops'", 
                     "'V'", "'volt'", "'volts'", "'y'", "'coord'", "'coordinate'", 
                     "'x'", "'remaining'", "'capacity'", "'target'", "'current'", 
                     "'min'", "'minimum'", "'voltage'", "'max'", "'maximum'", 
                     "'=='", "'!='", "'<'", "'<='", "'>'", "'>='", "'True'", 
                     "'true'", "'TRUE'", "'Yes'", "'yes'", "'YES'", "'False'", 
                     "'false'", "'FALSE'", "'No'", "'no'", "'NO'", "'index'", 
                     "'base'", "'dispense'", "'enter'", "'+'", "'='", "<INVALID>", 
                     "'/'", "'interactive'", "':'", "'isn't'", "'local'", 
                     "'*'", "'not'", "'off'", "'on'", "'-'", "';'", "'toggle'", 
                     "'until'", "'while'", "']'", "')'" ]

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
                      "<INVALID>", "<INVALID>", "ADD", "ASSIGN", "ATTR", 
                      "DIV", "INTERACTIVE", "INJECT", "ISNT", "LOCAL", "MUL", 
                      "NOT", "OFF", "ON", "SUB", "TERMINATOR", "TOGGLE", 
                      "UNTIL", "WHILE", "CLOSE_BRACKET", "CLOSE_PAREN", 
                      "ID", "INT", "FLOAT", "STRING", "EOL_COMMENT", "COMMENT", 
                      "WS" ]

    RULE_macro_file = 0
    RULE_interactive = 1
    RULE_declaration = 2
    RULE_stat = 3
    RULE_compound = 4
    RULE_loop_header = 5
    RULE_step_first_and_dir = 6
    RULE_loop = 7
    RULE_exit = 8
    RULE_term_punct = 9
    RULE_expr = 10
    RULE_reagent = 11
    RULE_direction = 12
    RULE_turn = 13
    RULE_rc = 14
    RULE_axis = 15
    RULE_macro_def = 16
    RULE_macro_header = 17
    RULE_param = 18
    RULE_no_arg_action = 19
    RULE_param_type = 20
    RULE_dim_unit = 21
    RULE_numbered_type = 22
    RULE_attr = 23
    RULE_rel = 24
    RULE_bool_val = 25
    RULE_name = 26
    RULE_multi_word_name = 27
    RULE_kwd_names = 28
    RULE_string = 29

    ruleNames =  [ "macro_file", "interactive", "declaration", "stat", "compound", 
                   "loop_header", "step_first_and_dir", "loop", "exit", 
                   "term_punct", "expr", "reagent", "direction", "turn", 
                   "rc", "axis", "macro_def", "macro_header", "param", "no_arg_action", 
                   "param_type", "dim_unit", "numbered_type", "attr", "rel", 
                   "bool_val", "name", "multi_word_name", "kwd_names", "string" ]

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
    T__159=160
    T__160=161
    ADD=162
    ASSIGN=163
    ATTR=164
    DIV=165
    INTERACTIVE=166
    INJECT=167
    ISNT=168
    LOCAL=169
    MUL=170
    NOT=171
    OFF=172
    ON=173
    SUB=174
    TERMINATOR=175
    TOGGLE=176
    UNTIL=177
    WHILE=178
    CLOSE_BRACKET=179
    CLOSE_PAREN=180
    ID=181
    INT=182
    FLOAT=183
    STRING=184
    EOL_COMMENT=185
    COMMENT=186
    WS=187

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
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__4) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__13) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__17) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__33) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__85 - 64)) | (1 << (DMFParser.T__86 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__88 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.T__91 - 64)) | (1 << (DMFParser.T__92 - 64)) | (1 << (DMFParser.T__93 - 64)) | (1 << (DMFParser.T__94 - 64)) | (1 << (DMFParser.T__95 - 64)) | (1 << (DMFParser.T__96 - 64)) | (1 << (DMFParser.T__97 - 64)) | (1 << (DMFParser.T__100 - 64)) | (1 << (DMFParser.T__101 - 64)) | (1 << (DMFParser.T__106 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__134 - 130)) | (1 << (DMFParser.T__135 - 130)) | (1 << (DMFParser.T__137 - 130)) | (1 << (DMFParser.T__138 - 130)) | (1 << (DMFParser.T__145 - 130)) | (1 << (DMFParser.T__146 - 130)) | (1 << (DMFParser.T__147 - 130)) | (1 << (DMFParser.T__148 - 130)) | (1 << (DMFParser.T__149 - 130)) | (1 << (DMFParser.T__150 - 130)) | (1 << (DMFParser.T__151 - 130)) | (1 << (DMFParser.T__152 - 130)) | (1 << (DMFParser.T__153 - 130)) | (1 << (DMFParser.T__154 - 130)) | (1 << (DMFParser.T__155 - 130)) | (1 << (DMFParser.T__156 - 130)) | (1 << (DMFParser.T__157 - 130)) | (1 << (DMFParser.T__158 - 130)) | (1 << (DMFParser.T__159 - 130)) | (1 << (DMFParser.T__160 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.LOCAL - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
                self.state = 60
                self.stat()
                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 66
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


    class Loop_interactiveContext(InteractiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.InteractiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def loop(self):
            return self.getTypedRuleContext(DMFParser.LoopContext,0)

        def EOF(self):
            return self.getToken(DMFParser.EOF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLoop_interactive" ):
                listener.enterLoop_interactive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLoop_interactive" ):
                listener.exitLoop_interactive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLoop_interactive" ):
                return visitor.visitLoop_interactive(self)
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



    def interactive(self):

        localctx = DMFParser.InteractiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_interactive)
        self._la = 0 # Token type
        try:
            self.state = 87
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Compound_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 68
                self.compound()
                self.state = 69
                self.match(DMFParser.EOF)
                pass

            elif la_ == 2:
                localctx = DMFParser.Loop_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 71
                self.loop()
                self.state = 72
                self.match(DMFParser.EOF)
                pass

            elif la_ == 3:
                localctx = DMFParser.Decl_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 74
                self.declaration()
                self.state = 76
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 75
                    self.match(DMFParser.TERMINATOR)


                self.state = 78
                self.match(DMFParser.EOF)
                pass

            elif la_ == 4:
                localctx = DMFParser.Expr_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 80
                self.expr(0)
                self.state = 82
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.TERMINATOR:
                    self.state = 81
                    self.match(DMFParser.TERMINATOR)


                self.state = 84
                self.match(DMFParser.EOF)
                pass

            elif la_ == 5:
                localctx = DMFParser.Empty_interactiveContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 86
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
            self.state = 126
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 89
                self.match(DMFParser.LOCAL)
                self.state = 90
                localctx._name = self.name()
                self.state = 91
                self.match(DMFParser.ASSIGN)
                self.state = 92
                localctx.init = self.expr(0)
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                localctx.type=None
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 97
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.LOCAL:
                    self.state = 96
                    self.match(DMFParser.LOCAL)


                self.state = 99
                localctx._param_type = self.param_type()
                self.state = 100
                localctx._INT = self.match(DMFParser.INT)
                self.state = 101
                self.match(DMFParser.ASSIGN)
                self.state = 103
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__17) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__33) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__85 - 64)) | (1 << (DMFParser.T__86 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__88 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.T__91 - 64)) | (1 << (DMFParser.T__92 - 64)) | (1 << (DMFParser.T__93 - 64)) | (1 << (DMFParser.T__94 - 64)) | (1 << (DMFParser.T__95 - 64)) | (1 << (DMFParser.T__96 - 64)) | (1 << (DMFParser.T__97 - 64)) | (1 << (DMFParser.T__100 - 64)) | (1 << (DMFParser.T__101 - 64)) | (1 << (DMFParser.T__106 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__134 - 130)) | (1 << (DMFParser.T__135 - 130)) | (1 << (DMFParser.T__137 - 130)) | (1 << (DMFParser.T__138 - 130)) | (1 << (DMFParser.T__145 - 130)) | (1 << (DMFParser.T__146 - 130)) | (1 << (DMFParser.T__147 - 130)) | (1 << (DMFParser.T__148 - 130)) | (1 << (DMFParser.T__149 - 130)) | (1 << (DMFParser.T__150 - 130)) | (1 << (DMFParser.T__151 - 130)) | (1 << (DMFParser.T__152 - 130)) | (1 << (DMFParser.T__153 - 130)) | (1 << (DMFParser.T__154 - 130)) | (1 << (DMFParser.T__155 - 130)) | (1 << (DMFParser.T__156 - 130)) | (1 << (DMFParser.T__157 - 130)) | (1 << (DMFParser.T__158 - 130)) | (1 << (DMFParser.T__159 - 130)) | (1 << (DMFParser.T__160 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
                    self.state = 102
                    localctx.init = self.expr(0)


                localctx.type=localctx._param_type.type
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 108
                self.match(DMFParser.LOCAL)
                self.state = 109
                localctx._param_type = self.param_type()
                self.state = 110
                localctx._INT = self.match(DMFParser.INT)
                localctx.type=localctx._param_type.type
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 115
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.LOCAL:
                    self.state = 114
                    self.match(DMFParser.LOCAL)


                self.state = 117
                localctx._param_type = self.param_type()
                self.state = 118
                localctx._name = self.name()
                self.state = 121
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.ASSIGN:
                    self.state = 119
                    self.match(DMFParser.ASSIGN)
                    self.state = 120
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


    class Exit_statContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def exit(self):
            return self.getTypedRuleContext(DMFParser.ExitContext,0)

        def TERMINATOR(self):
            return self.getToken(DMFParser.TERMINATOR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExit_stat" ):
                listener.enterExit_stat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExit_stat" ):
                listener.exitExit_stat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExit_stat" ):
                return visitor.visitExit_stat(self)
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
        self.enterRule(localctx, 6, self.RULE_stat)
        self._la = 0 # Token type
        try:
            self.state = 156
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Decl_statContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 128
                self.declaration()
                self.state = 129
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 2:
                localctx = DMFParser.If_statContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 131
                self.match(DMFParser.T__0)
                self.state = 132
                localctx._expr = self.expr(0)
                localctx.tests.append(localctx._expr)
                self.state = 133
                localctx._compound = self.compound()
                localctx.bodies.append(localctx._compound)
                self.state = 141
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 134
                        self.match(DMFParser.T__1)
                        self.state = 135
                        self.match(DMFParser.T__0)
                        self.state = 136
                        localctx._expr = self.expr(0)
                        localctx.tests.append(localctx._expr)
                        self.state = 137
                        localctx._compound = self.compound()
                        localctx.bodies.append(localctx._compound) 
                    self.state = 143
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

                self.state = 146
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__1:
                    self.state = 144
                    self.match(DMFParser.T__1)
                    self.state = 145
                    localctx.else_body = self.compound()


                pass

            elif la_ == 3:
                localctx = DMFParser.Expr_statContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 148
                self.expr(0)
                self.state = 149
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 4:
                localctx = DMFParser.Loop_statContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 151
                self.loop()
                pass

            elif la_ == 5:
                localctx = DMFParser.Exit_statContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 152
                self.exit()
                self.state = 153
                self.match(DMFParser.TERMINATOR)
                pass

            elif la_ == 6:
                localctx = DMFParser.Compound_statContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 155
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
            self.state = 174
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__2]:
                localctx = DMFParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 158
                self.match(DMFParser.T__2)
                self.state = 162
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__4) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__13) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__17) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__33) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__85 - 64)) | (1 << (DMFParser.T__86 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__88 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.T__91 - 64)) | (1 << (DMFParser.T__92 - 64)) | (1 << (DMFParser.T__93 - 64)) | (1 << (DMFParser.T__94 - 64)) | (1 << (DMFParser.T__95 - 64)) | (1 << (DMFParser.T__96 - 64)) | (1 << (DMFParser.T__97 - 64)) | (1 << (DMFParser.T__100 - 64)) | (1 << (DMFParser.T__101 - 64)) | (1 << (DMFParser.T__106 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__134 - 130)) | (1 << (DMFParser.T__135 - 130)) | (1 << (DMFParser.T__137 - 130)) | (1 << (DMFParser.T__138 - 130)) | (1 << (DMFParser.T__145 - 130)) | (1 << (DMFParser.T__146 - 130)) | (1 << (DMFParser.T__147 - 130)) | (1 << (DMFParser.T__148 - 130)) | (1 << (DMFParser.T__149 - 130)) | (1 << (DMFParser.T__150 - 130)) | (1 << (DMFParser.T__151 - 130)) | (1 << (DMFParser.T__152 - 130)) | (1 << (DMFParser.T__153 - 130)) | (1 << (DMFParser.T__154 - 130)) | (1 << (DMFParser.T__155 - 130)) | (1 << (DMFParser.T__156 - 130)) | (1 << (DMFParser.T__157 - 130)) | (1 << (DMFParser.T__158 - 130)) | (1 << (DMFParser.T__159 - 130)) | (1 << (DMFParser.T__160 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.LOCAL - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
                    self.state = 159
                    self.stat()
                    self.state = 164
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 165
                self.match(DMFParser.T__3)
                pass
            elif token in [DMFParser.T__4]:
                localctx = DMFParser.Par_blockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 166
                self.match(DMFParser.T__4)
                self.state = 170
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__0) | (1 << DMFParser.T__2) | (1 << DMFParser.T__4) | (1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__13) | (1 << DMFParser.T__14) | (1 << DMFParser.T__15) | (1 << DMFParser.T__17) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__33) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__85 - 64)) | (1 << (DMFParser.T__86 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__88 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.T__91 - 64)) | (1 << (DMFParser.T__92 - 64)) | (1 << (DMFParser.T__93 - 64)) | (1 << (DMFParser.T__94 - 64)) | (1 << (DMFParser.T__95 - 64)) | (1 << (DMFParser.T__96 - 64)) | (1 << (DMFParser.T__97 - 64)) | (1 << (DMFParser.T__100 - 64)) | (1 << (DMFParser.T__101 - 64)) | (1 << (DMFParser.T__106 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__134 - 130)) | (1 << (DMFParser.T__135 - 130)) | (1 << (DMFParser.T__137 - 130)) | (1 << (DMFParser.T__138 - 130)) | (1 << (DMFParser.T__145 - 130)) | (1 << (DMFParser.T__146 - 130)) | (1 << (DMFParser.T__147 - 130)) | (1 << (DMFParser.T__148 - 130)) | (1 << (DMFParser.T__149 - 130)) | (1 << (DMFParser.T__150 - 130)) | (1 << (DMFParser.T__151 - 130)) | (1 << (DMFParser.T__152 - 130)) | (1 << (DMFParser.T__153 - 130)) | (1 << (DMFParser.T__154 - 130)) | (1 << (DMFParser.T__155 - 130)) | (1 << (DMFParser.T__156 - 130)) | (1 << (DMFParser.T__157 - 130)) | (1 << (DMFParser.T__158 - 130)) | (1 << (DMFParser.T__159 - 130)) | (1 << (DMFParser.T__160 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.LOCAL - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
                    self.state = 167
                    self.stat()
                    self.state = 172
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 173
                self.match(DMFParser.T__5)
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


    class Loop_headerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return DMFParser.RULE_loop_header

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Duration_loop_headerContext(Loop_headerContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.Loop_headerContext
            super().__init__(parser)
            self.duration = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDuration_loop_header" ):
                listener.enterDuration_loop_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDuration_loop_header" ):
                listener.exitDuration_loop_header(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDuration_loop_header" ):
                return visitor.visitDuration_loop_header(self)
            else:
                return visitor.visitChildren(self)


    class Test_loop_headerContext(Loop_headerContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.Loop_headerContext
            super().__init__(parser)
            self.cond = None # ExprContext
            self.copyFrom(ctx)

        def WHILE(self):
            return self.getToken(DMFParser.WHILE, 0)
        def UNTIL(self):
            return self.getToken(DMFParser.UNTIL, 0)
        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTest_loop_header" ):
                listener.enterTest_loop_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTest_loop_header" ):
                listener.exitTest_loop_header(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTest_loop_header" ):
                return visitor.visitTest_loop_header(self)
            else:
                return visitor.visitChildren(self)


    class Seq_iter_loop_headerContext(Loop_headerContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.Loop_headerContext
            super().__init__(parser)
            self.var = None # NameContext
            self.seq = None # ExprContext
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSeq_iter_loop_header" ):
                listener.enterSeq_iter_loop_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSeq_iter_loop_header" ):
                listener.exitSeq_iter_loop_header(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSeq_iter_loop_header" ):
                return visitor.visitSeq_iter_loop_header(self)
            else:
                return visitor.visitChildren(self)


    class Step_iter_loop_headerContext(Loop_headerContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.Loop_headerContext
            super().__init__(parser)
            self.var = None # NameContext
            self.first = None # Step_first_and_dirContext
            self.bound = None # ExprContext
            self.step = None # ExprContext
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)

        def step_first_and_dir(self):
            return self.getTypedRuleContext(DMFParser.Step_first_and_dirContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)

        def param(self):
            return self.getTypedRuleContext(DMFParser.ParamContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStep_iter_loop_header" ):
                listener.enterStep_iter_loop_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStep_iter_loop_header" ):
                listener.exitStep_iter_loop_header(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStep_iter_loop_header" ):
                return visitor.visitStep_iter_loop_header(self)
            else:
                return visitor.visitChildren(self)


    class N_times_loop_headerContext(Loop_headerContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.Loop_headerContext
            super().__init__(parser)
            self.n = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterN_times_loop_header" ):
                listener.enterN_times_loop_header(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitN_times_loop_header" ):
                listener.exitN_times_loop_header(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitN_times_loop_header" ):
                return visitor.visitN_times_loop_header(self)
            else:
                return visitor.visitChildren(self)



    def loop_header(self):

        localctx = DMFParser.Loop_headerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_loop_header)
        self._la = 0 # Token type
        try:
            self.state = 206
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                localctx = DMFParser.N_times_loop_headerContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 176
                localctx.n = self.expr(0)
                self.state = 177
                self.match(DMFParser.T__6)
                pass

            elif la_ == 2:
                localctx = DMFParser.Duration_loop_headerContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 179
                self.match(DMFParser.T__7)
                self.state = 180
                localctx.duration = self.expr(0)
                pass

            elif la_ == 3:
                localctx = DMFParser.Test_loop_headerContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 181
                _la = self._input.LA(1)
                if not(_la==DMFParser.UNTIL or _la==DMFParser.WHILE):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 182
                localctx.cond = self.expr(0)
                pass

            elif la_ == 4:
                localctx = DMFParser.Seq_iter_loop_headerContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 183
                self.match(DMFParser.T__8)
                self.state = 184
                localctx.var = self.name()
                self.state = 185
                self.match(DMFParser.T__9)
                self.state = 186
                localctx.seq = self.expr(0)
                pass

            elif la_ == 5:
                localctx = DMFParser.Step_iter_loop_headerContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 188
                self.match(DMFParser.T__8)
                self.state = 189
                localctx.var = self.name()
                self.state = 190
                localctx.first = self.step_first_and_dir()
                self.state = 191
                self.match(DMFParser.T__10)
                self.state = 192
                localctx.bound = self.expr(0)
                self.state = 195
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__11:
                    self.state = 193
                    self.match(DMFParser.T__11)
                    self.state = 194
                    localctx.step = self.expr(0)


                pass

            elif la_ == 6:
                localctx = DMFParser.Step_iter_loop_headerContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 197
                self.match(DMFParser.T__8)
                self.state = 198
                localctx.var = self.param()
                self.state = 199
                localctx.first = self.step_first_and_dir()
                self.state = 200
                self.match(DMFParser.T__10)
                self.state = 201
                localctx.bound = self.expr(0)
                self.state = 204
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__11:
                    self.state = 202
                    self.match(DMFParser.T__11)
                    self.state = 203
                    localctx.step = self.expr(0)


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Step_first_and_dirContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.is_down = None

        def ASSIGN(self):
            return self.getToken(DMFParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(DMFParser.ExprContext,0)


        def getRuleIndex(self):
            return DMFParser.RULE_step_first_and_dir

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStep_first_and_dir" ):
                listener.enterStep_first_and_dir(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStep_first_and_dir" ):
                listener.exitStep_first_and_dir(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStep_first_and_dir" ):
                return visitor.visitStep_first_and_dir(self)
            else:
                return visitor.visitChildren(self)




    def step_first_and_dir(self):

        localctx = DMFParser.Step_first_and_dirContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_step_first_and_dir)
        try:
            self.state = 219
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 208
                self.match(DMFParser.ASSIGN)
                self.state = 209
                self.expr(0)
                self.state = 210
                self.match(DMFParser.T__12)
                localctx.is_down=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 213
                self.match(DMFParser.ASSIGN)
                self.state = 214
                self.expr(0)
                localctx.is_down=False
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 217
                self.match(DMFParser.T__12)
                localctx.is_down=True
                pass


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
            self.loop_name = None # NameContext
            self.header = None # Loop_headerContext
            self.body = None # CompoundContext

        def loop_header(self):
            return self.getTypedRuleContext(DMFParser.Loop_headerContext,0)


        def compound(self):
            return self.getTypedRuleContext(DMFParser.CompoundContext,0)


        def CLOSE_BRACKET(self):
            return self.getToken(DMFParser.CLOSE_BRACKET, 0)

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)


        def getRuleIndex(self):
            return DMFParser.RULE_loop

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLoop" ):
                listener.enterLoop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLoop" ):
                listener.exitLoop(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLoop" ):
                return visitor.visitLoop(self)
            else:
                return visitor.visitChildren(self)




    def loop(self):

        localctx = DMFParser.LoopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_loop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 225
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==DMFParser.T__13:
                self.state = 221
                self.match(DMFParser.T__13)
                self.state = 222
                localctx.loop_name = self.name()
                self.state = 223
                self.match(DMFParser.CLOSE_BRACKET)


            self.state = 227
            self.match(DMFParser.T__14)
            self.state = 228
            localctx.header = self.loop_header()
            self.state = 229
            localctx.body = self.compound()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.loop_name = None # NameContext

        def name(self):
            return self.getTypedRuleContext(DMFParser.NameContext,0)


        def getRuleIndex(self):
            return DMFParser.RULE_exit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExit" ):
                listener.enterExit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExit" ):
                listener.exitExit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExit" ):
                return visitor.visitExit(self)
            else:
                return visitor.visitChildren(self)




    def exit(self):

        localctx = DMFParser.ExitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_exit)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 231
            self.match(DMFParser.T__15)
            self.state = 233
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__22) | (1 << DMFParser.T__28) | (1 << DMFParser.T__33))) != 0) or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DMFParser.T__69 - 70)) | (1 << (DMFParser.T__70 - 70)) | (1 << (DMFParser.T__71 - 70)) | (1 << (DMFParser.T__72 - 70)) | (1 << (DMFParser.T__73 - 70)) | (1 << (DMFParser.T__74 - 70)) | (1 << (DMFParser.T__81 - 70)) | (1 << (DMFParser.T__91 - 70)) | (1 << (DMFParser.T__92 - 70)) | (1 << (DMFParser.T__93 - 70)) | (1 << (DMFParser.T__101 - 70)) | (1 << (DMFParser.T__106 - 70)) | (1 << (DMFParser.T__126 - 70)) | (1 << (DMFParser.T__129 - 70)))) != 0) or ((((_la - 135)) & ~0x3f) == 0 and ((1 << (_la - 135)) & ((1 << (DMFParser.T__134 - 135)) | (1 << (DMFParser.T__135 - 135)) | (1 << (DMFParser.T__137 - 135)) | (1 << (DMFParser.T__138 - 135)) | (1 << (DMFParser.T__157 - 135)) | (1 << (DMFParser.T__158 - 135)) | (1 << (DMFParser.T__159 - 135)) | (1 << (DMFParser.T__160 - 135)) | (1 << (DMFParser.INTERACTIVE - 135)) | (1 << (DMFParser.OFF - 135)) | (1 << (DMFParser.ON - 135)) | (1 << (DMFParser.ID - 135)))) != 0):
                self.state = 232
                localctx.loop_name = self.name()


            self.state = 235
            self.match(DMFParser.T__16)
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
        self.enterRule(localctx, 18, self.RULE_term_punct)
        try:
            self.state = 241
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.CLOSE_BRACKET]:
                self.enterOuterAlt(localctx, 1)
                self.state = 237
                self.match(DMFParser.CLOSE_BRACKET)
                localctx.is_closed=True
                pass
            elif token in [DMFParser.CLOSE_PAREN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 239
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


    class Print_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self._expr = None # ExprContext
            self.vals = list() # of ExprContexts
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrint_expr" ):
                listener.enterPrint_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrint_expr" ):
                listener.exitPrint_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrint_expr" ):
                return visitor.visitPrint_expr(self)
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


    class Prompt_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a DMFParser.ExprContext
            super().__init__(parser)
            self._expr = None # ExprContext
            self.vals = list() # of ExprContexts
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(DMFParser.ExprContext)
            else:
                return self.getTypedRuleContext(DMFParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrompt_expr" ):
                listener.enterPrompt_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrompt_expr" ):
                listener.exitPrompt_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrompt_expr" ):
                return visitor.visitPrompt_expr(self)
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
        _startState = 20
        self.enterRecursionRule(localctx, 20, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 345
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,33,self._ctx)
            if la_ == 1:
                localctx = DMFParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 244
                self.match(DMFParser.T__17)
                self.state = 245
                self.expr(0)
                self.state = 246
                self.match(DMFParser.CLOSE_PAREN)
                pass

            elif la_ == 2:
                localctx = DMFParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 248
                self.match(DMFParser.T__17)
                self.state = 249
                localctx.x = self.expr(0)
                self.state = 250
                self.match(DMFParser.T__18)
                self.state = 251
                localctx.y = self.expr(0)
                self.state = 252
                self.match(DMFParser.CLOSE_PAREN)
                pass

            elif la_ == 3:
                localctx = DMFParser.Neg_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 254
                self.match(DMFParser.SUB)
                self.state = 255
                localctx.rhs = self.expr(47)
                pass

            elif la_ == 4:
                localctx = DMFParser.Numbered_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 256
                localctx.kind = self.numbered_type()
                self.state = 257
                self.match(DMFParser.T__19)
                self.state = 258
                localctx.which = self.expr(45)
                pass

            elif la_ == 5:
                localctx = DMFParser.Const_rc_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 260
                localctx._INT = self.match(DMFParser.INT)
                self.state = 261
                self.rc((0 if localctx._INT is None else int(localctx._INT.text)))
                pass

            elif la_ == 6:
                localctx = DMFParser.Reagent_lit_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 263
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__28:
                    self.state = 262
                    self.match(DMFParser.T__28)


                self.state = 265
                self.reagent()
                self.state = 267
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
                if la_ == 1:
                    self.state = 266
                    self.match(DMFParser.T__29)


                pass

            elif la_ == 7:
                localctx = DMFParser.Reagent_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 270
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__22 or _la==DMFParser.T__28:
                    self.state = 269
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__22 or _la==DMFParser.T__28):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 272
                self.match(DMFParser.T__29)
                self.state = 274
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__30:
                    self.state = 273
                    self.match(DMFParser.T__30)


                self.state = 276
                localctx.which = self.expr(34)
                pass

            elif la_ == 8:
                localctx = DMFParser.Not_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 277
                self.match(DMFParser.NOT)
                self.state = 278
                self.expr(27)
                pass

            elif la_ == 9:
                localctx = DMFParser.Delta_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 279
                self.direction()
                self.state = 280
                localctx.dist = self.expr(24)
                pass

            elif la_ == 10:
                localctx = DMFParser.Dir_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 282
                self.direction()
                pass

            elif la_ == 11:
                localctx = DMFParser.To_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 283
                self.match(DMFParser.T__10)
                self.state = 285
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__57) | (1 << DMFParser.T__59) | (1 << DMFParser.T__60))) != 0):
                    self.state = 284
                    self.axis()


                self.state = 287
                localctx.which = self.expr(22)
                pass

            elif la_ == 12:
                localctx = DMFParser.Pause_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 288
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__37 or _la==DMFParser.T__38):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 290
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__7:
                    self.state = 289
                    self.match(DMFParser.T__7)


                self.state = 292
                localctx.duration = self.expr(21)
                pass

            elif la_ == 13:
                localctx = DMFParser.Prompt_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 297
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__37, DMFParser.T__38]:
                    self.state = 293
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__37 or _la==DMFParser.T__38):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 294
                    self.match(DMFParser.T__7)
                    self.state = 295
                    self.match(DMFParser.T__39)
                    pass
                elif token in [DMFParser.T__40]:
                    self.state = 296
                    self.match(DMFParser.T__40)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 307
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
                if la_ == 1:
                    self.state = 299
                    localctx._expr = self.expr(0)
                    localctx.vals.append(localctx._expr)
                    self.state = 304
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,29,self._ctx)
                    while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                        if _alt==1:
                            self.state = 300
                            self.match(DMFParser.T__18)
                            self.state = 301
                            localctx._expr = self.expr(0)
                            localctx.vals.append(localctx._expr) 
                        self.state = 306
                        self._errHandler.sync(self)
                        _alt = self._interp.adaptivePredict(self._input,29,self._ctx)



                pass

            elif la_ == 14:
                localctx = DMFParser.Print_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 309
                self.match(DMFParser.T__41)
                self.state = 310
                localctx._expr = self.expr(0)
                localctx.vals.append(localctx._expr)
                self.state = 315
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,31,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 311
                        self.match(DMFParser.T__18)
                        self.state = 312
                        localctx._expr = self.expr(0)
                        localctx.vals.append(localctx._expr) 
                    self.state = 317
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,31,self._ctx)

                pass

            elif la_ == 15:
                localctx = DMFParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 318
                self.match(DMFParser.T__42)
                self.state = 319
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__43 or _la==DMFParser.T__44):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 320
                localctx.loc = self.expr(17)
                pass

            elif la_ == 16:
                localctx = DMFParser.Macro_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 321
                self.macro_def()
                pass

            elif la_ == 17:
                localctx = DMFParser.Action_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 322
                self.no_arg_action()
                pass

            elif la_ == 18:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 324
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__28:
                    self.state = 323
                    self.match(DMFParser.T__28)


                self.state = 326
                self.param_type()
                pass

            elif la_ == 19:
                localctx = DMFParser.Type_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 327
                self.param_type()
                self.state = 328
                localctx.n = self.match(DMFParser.INT)
                pass

            elif la_ == 20:
                localctx = DMFParser.Bool_const_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 330
                localctx.val = self.bool_val()
                pass

            elif la_ == 21:
                localctx = DMFParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 331
                self.name()
                pass

            elif la_ == 22:
                localctx = DMFParser.Mw_name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 332
                self.multi_word_name()
                pass

            elif la_ == 23:
                localctx = DMFParser.Name_assign_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 333
                localctx.which = self.name()
                self.state = 334
                self.match(DMFParser.ASSIGN)
                self.state = 335
                localctx.what = self.expr(6)
                pass

            elif la_ == 24:
                localctx = DMFParser.Name_assign_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 337
                localctx.ptype = self.param_type()
                self.state = 338
                localctx.n = self.match(DMFParser.INT)
                self.state = 339
                self.match(DMFParser.ASSIGN)
                self.state = 340
                localctx.what = self.expr(4)
                pass

            elif la_ == 25:
                localctx = DMFParser.String_lit_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 342
                self.string()
                pass

            elif la_ == 26:
                localctx = DMFParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 343
                localctx._INT = self.match(DMFParser.INT)
                pass

            elif la_ == 27:
                localctx = DMFParser.Float_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 344
                self.match(DMFParser.FLOAT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 448
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,40,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 446
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
                    if la_ == 1:
                        localctx = DMFParser.In_dir_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 347
                        if not self.precpred(self._ctx, 40):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 40)")
                        self.state = 348
                        self.match(DMFParser.T__9)
                        self.state = 349
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__25 or _la==DMFParser.T__26):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 350
                        localctx.d = self.expr(41)
                        pass

                    elif la_ == 2:
                        localctx = DMFParser.Liquid_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.vol = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 351
                        if not self.precpred(self._ctx, 33):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 33)")
                        self.state = 352
                        self.match(DMFParser.T__31)
                        self.state = 353
                        localctx.which = self.expr(34)
                        pass

                    elif la_ == 3:
                        localctx = DMFParser.Muldiv_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 354
                        if not self.precpred(self._ctx, 32):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 32)")
                        self.state = 355
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.DIV or _la==DMFParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 356
                        localctx.rhs = self.expr(33)
                        pass

                    elif la_ == 4:
                        localctx = DMFParser.Addsub_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 357
                        if not self.precpred(self._ctx, 31):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 31)")
                        self.state = 358
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.ADD or _la==DMFParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 359
                        localctx.rhs = self.expr(32)
                        pass

                    elif la_ == 5:
                        localctx = DMFParser.Rel_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 360
                        if not self.precpred(self._ctx, 30):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 30)")
                        self.state = 361
                        self.rel()
                        self.state = 362
                        localctx.rhs = self.expr(31)
                        pass

                    elif la_ == 6:
                        localctx = DMFParser.Is_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 364
                        if not self.precpred(self._ctx, 28):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 28)")
                        self.state = 370
                        self._errHandler.sync(self)
                        token = self._input.LA(1)
                        if token in [DMFParser.T__34]:
                            self.state = 365
                            self.match(DMFParser.T__34)
                            self.state = 367
                            self._errHandler.sync(self)
                            la_ = self._interp.adaptivePredict(self._input,34,self._ctx)
                            if la_ == 1:
                                self.state = 366
                                self.match(DMFParser.NOT)


                            pass
                        elif token in [DMFParser.ISNT]:
                            self.state = 369
                            self.match(DMFParser.ISNT)
                            pass
                        else:
                            raise NoViableAltException(self)

                        self.state = 372
                        localctx.pred = self.expr(29)
                        pass

                    elif la_ == 7:
                        localctx = DMFParser.And_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 373
                        if not self.precpred(self._ctx, 26):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 26)")
                        self.state = 374
                        self.match(DMFParser.T__35)
                        self.state = 375
                        localctx.rhs = self.expr(27)
                        pass

                    elif la_ == 8:
                        localctx = DMFParser.Or_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 376
                        if not self.precpred(self._ctx, 25):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 25)")
                        self.state = 377
                        self.match(DMFParser.T__36)
                        self.state = 378
                        localctx.rhs = self.expr(26)
                        pass

                    elif la_ == 9:
                        localctx = DMFParser.Drop_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.vol = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 379
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 380
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__43 or _la==DMFParser.T__44):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 381
                        localctx.loc = self.expr(17)
                        pass

                    elif la_ == 10:
                        localctx = DMFParser.Injection_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 382
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 383
                        self.match(DMFParser.INJECT)
                        self.state = 384
                        localctx.what = self.expr(16)
                        pass

                    elif la_ == 11:
                        localctx = DMFParser.Cond_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.first = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 385
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 386
                        self.match(DMFParser.T__0)
                        self.state = 387
                        localctx.cond = self.expr(0)
                        self.state = 388
                        self.match(DMFParser.T__1)
                        self.state = 389
                        localctx.second = self.expr(15)
                        pass

                    elif la_ == 12:
                        localctx = DMFParser.Attr_assign_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 391
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 392
                        self.match(DMFParser.ATTR)
                        self.state = 393
                        self.attr()
                        self.state = 394
                        self.match(DMFParser.ASSIGN)
                        self.state = 395
                        localctx.what = self.expr(6)
                        pass

                    elif la_ == 13:
                        localctx = DMFParser.Function_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.func = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 397
                        if not self.precpred(self._ctx, 49):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 49)")
                        self.state = 398
                        self.match(DMFParser.T__17)
                        self.state = 407
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__10) | (1 << DMFParser.T__12) | (1 << DMFParser.T__17) | (1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__33) | (1 << DMFParser.T__37) | (1 << DMFParser.T__38) | (1 << DMFParser.T__40) | (1 << DMFParser.T__41) | (1 << DMFParser.T__42) | (1 << DMFParser.T__45) | (1 << DMFParser.T__46) | (1 << DMFParser.T__47) | (1 << DMFParser.T__48) | (1 << DMFParser.T__49) | (1 << DMFParser.T__50) | (1 << DMFParser.T__51) | (1 << DMFParser.T__52) | (1 << DMFParser.T__53))) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & ((1 << (DMFParser.T__63 - 64)) | (1 << (DMFParser.T__64 - 64)) | (1 << (DMFParser.T__65 - 64)) | (1 << (DMFParser.T__66 - 64)) | (1 << (DMFParser.T__69 - 64)) | (1 << (DMFParser.T__70 - 64)) | (1 << (DMFParser.T__71 - 64)) | (1 << (DMFParser.T__72 - 64)) | (1 << (DMFParser.T__73 - 64)) | (1 << (DMFParser.T__74 - 64)) | (1 << (DMFParser.T__75 - 64)) | (1 << (DMFParser.T__76 - 64)) | (1 << (DMFParser.T__77 - 64)) | (1 << (DMFParser.T__78 - 64)) | (1 << (DMFParser.T__79 - 64)) | (1 << (DMFParser.T__80 - 64)) | (1 << (DMFParser.T__81 - 64)) | (1 << (DMFParser.T__82 - 64)) | (1 << (DMFParser.T__83 - 64)) | (1 << (DMFParser.T__84 - 64)) | (1 << (DMFParser.T__85 - 64)) | (1 << (DMFParser.T__86 - 64)) | (1 << (DMFParser.T__87 - 64)) | (1 << (DMFParser.T__88 - 64)) | (1 << (DMFParser.T__89 - 64)) | (1 << (DMFParser.T__90 - 64)) | (1 << (DMFParser.T__91 - 64)) | (1 << (DMFParser.T__92 - 64)) | (1 << (DMFParser.T__93 - 64)) | (1 << (DMFParser.T__94 - 64)) | (1 << (DMFParser.T__95 - 64)) | (1 << (DMFParser.T__96 - 64)) | (1 << (DMFParser.T__97 - 64)) | (1 << (DMFParser.T__100 - 64)) | (1 << (DMFParser.T__101 - 64)) | (1 << (DMFParser.T__106 - 64)) | (1 << (DMFParser.T__126 - 64)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__134 - 130)) | (1 << (DMFParser.T__135 - 130)) | (1 << (DMFParser.T__137 - 130)) | (1 << (DMFParser.T__138 - 130)) | (1 << (DMFParser.T__145 - 130)) | (1 << (DMFParser.T__146 - 130)) | (1 << (DMFParser.T__147 - 130)) | (1 << (DMFParser.T__148 - 130)) | (1 << (DMFParser.T__149 - 130)) | (1 << (DMFParser.T__150 - 130)) | (1 << (DMFParser.T__151 - 130)) | (1 << (DMFParser.T__152 - 130)) | (1 << (DMFParser.T__153 - 130)) | (1 << (DMFParser.T__154 - 130)) | (1 << (DMFParser.T__155 - 130)) | (1 << (DMFParser.T__156 - 130)) | (1 << (DMFParser.T__157 - 130)) | (1 << (DMFParser.T__158 - 130)) | (1 << (DMFParser.T__159 - 130)) | (1 << (DMFParser.T__160 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.NOT - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.SUB - 130)) | (1 << (DMFParser.TOGGLE - 130)) | (1 << (DMFParser.ID - 130)) | (1 << (DMFParser.INT - 130)) | (1 << (DMFParser.FLOAT - 130)) | (1 << (DMFParser.STRING - 130)))) != 0):
                            self.state = 399
                            localctx._expr = self.expr(0)
                            localctx.args.append(localctx._expr)
                            self.state = 404
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            while _la==DMFParser.T__18:
                                self.state = 400
                                self.match(DMFParser.T__18)
                                self.state = 401
                                localctx._expr = self.expr(0)
                                localctx.args.append(localctx._expr)
                                self.state = 406
                                self._errHandler.sync(self)
                                _la = self._input.LA(1)



                        self.state = 409
                        self.match(DMFParser.CLOSE_PAREN)
                        pass

                    elif la_ == 14:
                        localctx = DMFParser.Delta_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 410
                        if not self.precpred(self._ctx, 46):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 46)")
                        self.state = 411
                        self.direction()
                        pass

                    elif la_ == 15:
                        localctx = DMFParser.Magnitude_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.quant = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 412
                        if not self.precpred(self._ctx, 44):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 44)")
                        self.state = 413
                        self.match(DMFParser.ATTR)
                        self.state = 414
                        self.match(DMFParser.T__20)
                        self.state = 415
                        self.match(DMFParser.T__9)
                        self.state = 416
                        self.dim_unit()
                        pass

                    elif la_ == 16:
                        localctx = DMFParser.Unit_string_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.quant = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 417
                        if not self.precpred(self._ctx, 43):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 43)")
                        self.state = 418
                        self.match(DMFParser.T__21)
                        self.state = 420
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==DMFParser.T__22:
                            self.state = 419
                            self.match(DMFParser.T__22)


                        self.state = 422
                        self.match(DMFParser.T__23)
                        self.state = 423
                        self.match(DMFParser.T__9)
                        self.state = 424
                        self.dim_unit()
                        pass

                    elif la_ == 17:
                        localctx = DMFParser.Attr_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 425
                        if not self.precpred(self._ctx, 42):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 42)")
                        self.state = 426
                        self.match(DMFParser.ATTR)
                        self.state = 427
                        self.attr()
                        pass

                    elif la_ == 18:
                        localctx = DMFParser.Turn_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.start_dir = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 428
                        if not self.precpred(self._ctx, 41):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 41)")
                        self.state = 429
                        self.match(DMFParser.T__24)
                        self.state = 430
                        self.turn()
                        pass

                    elif la_ == 19:
                        localctx = DMFParser.N_rc_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 431
                        if not self.precpred(self._ctx, 38):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 38)")
                        self.state = 432
                        self.rc(0)
                        pass

                    elif la_ == 20:
                        localctx = DMFParser.Unit_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 433
                        if not self.precpred(self._ctx, 37):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 37)")
                        self.state = 434
                        self.dim_unit()
                        pass

                    elif la_ == 21:
                        localctx = DMFParser.Temperature_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.amount = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 435
                        if not self.precpred(self._ctx, 36):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 36)")
                        self.state = 436
                        self.match(DMFParser.T__27)
                        pass

                    elif la_ == 22:
                        localctx = DMFParser.Has_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 437
                        if not self.precpred(self._ctx, 29):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 29)")
                        self.state = 438
                        self.match(DMFParser.T__32)
                        self.state = 439
                        _la = self._input.LA(1)
                        if not(_la==DMFParser.T__22 or _la==DMFParser.T__33):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 440
                        self.attr()
                        pass

                    elif la_ == 23:
                        localctx = DMFParser.Index_exprContext(self, DMFParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 441
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 442
                        self.match(DMFParser.T__13)
                        self.state = 443
                        localctx.which = self.expr(0)
                        self.state = 444
                        self.match(DMFParser.CLOSE_BRACKET)
                        pass

             
                self.state = 450
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,40,self._ctx)

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
        self.enterRule(localctx, 22, self.RULE_reagent)
        try:
            self.state = 455
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__45]:
                self.enterOuterAlt(localctx, 1)
                self.state = 451
                self.match(DMFParser.T__45)
                localctx.r = unknown_reagent
                pass
            elif token in [DMFParser.T__46]:
                self.enterOuterAlt(localctx, 2)
                self.state = 453
                self.match(DMFParser.T__46)
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
        self.enterRule(localctx, 24, self.RULE_direction)
        self._la = 0 # Token type
        try:
            self.state = 469
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__47, DMFParser.T__48]:
                self.enterOuterAlt(localctx, 1)
                self.state = 457
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__47 or _la==DMFParser.T__48):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__12, DMFParser.T__49]:
                self.enterOuterAlt(localctx, 2)
                self.state = 460
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__12 or _la==DMFParser.T__49):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.DOWN
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__50, DMFParser.T__51]:
                self.enterOuterAlt(localctx, 3)
                self.state = 463
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__50 or _la==DMFParser.T__51):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.LEFT
                localctx.verticalp=False
                pass
            elif token in [DMFParser.T__52, DMFParser.T__53]:
                self.enterOuterAlt(localctx, 4)
                self.state = 466
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__52 or _la==DMFParser.T__53):
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
        self.enterRule(localctx, 26, self.RULE_turn)
        self._la = 0 # Token type
        try:
            self.state = 477
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__52, DMFParser.T__54]:
                self.enterOuterAlt(localctx, 1)
                self.state = 471
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__52 or _la==DMFParser.T__54):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.RIGHT
                pass
            elif token in [DMFParser.T__50, DMFParser.T__55]:
                self.enterOuterAlt(localctx, 2)
                self.state = 473
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__50 or _la==DMFParser.T__55):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.t = Turn.LEFT
                pass
            elif token in [DMFParser.T__56]:
                self.enterOuterAlt(localctx, 3)
                self.state = 475
                self.match(DMFParser.T__56)
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
        self.enterRule(localctx, 28, self.RULE_rc)
        self._la = 0 # Token type
        try:
            self.state = 493
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,44,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 479
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 480
                self.match(DMFParser.T__57)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 483
                self.match(DMFParser.T__58)
                localctx.d = Dir.UP
                localctx.verticalp=True
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 486
                if not localctx.n==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, "$n==1")
                self.state = 487
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__59 or _la==DMFParser.T__60):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.d = Dir.RIGHT
                localctx.verticalp=False
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 490
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__61 or _la==DMFParser.T__62):
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
        self.enterRule(localctx, 30, self.RULE_axis)
        self._la = 0 # Token type
        try:
            self.state = 499
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__57]:
                self.enterOuterAlt(localctx, 1)
                self.state = 495
                self.match(DMFParser.T__57)
                localctx.verticalp=True
                pass
            elif token in [DMFParser.T__59, DMFParser.T__60]:
                self.enterOuterAlt(localctx, 2)
                self.state = 497
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__59 or _la==DMFParser.T__60):
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
        self.enterRule(localctx, 32, self.RULE_macro_def)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 501
            self.macro_header()
            self.state = 504
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__2, DMFParser.T__4]:
                self.state = 502
                self.compound()
                pass
            elif token in [DMFParser.T__10, DMFParser.T__12, DMFParser.T__17, DMFParser.T__22, DMFParser.T__23, DMFParser.T__25, DMFParser.T__26, DMFParser.T__28, DMFParser.T__29, DMFParser.T__33, DMFParser.T__37, DMFParser.T__38, DMFParser.T__40, DMFParser.T__41, DMFParser.T__42, DMFParser.T__45, DMFParser.T__46, DMFParser.T__47, DMFParser.T__48, DMFParser.T__49, DMFParser.T__50, DMFParser.T__51, DMFParser.T__52, DMFParser.T__53, DMFParser.T__63, DMFParser.T__64, DMFParser.T__65, DMFParser.T__66, DMFParser.T__69, DMFParser.T__70, DMFParser.T__71, DMFParser.T__72, DMFParser.T__73, DMFParser.T__74, DMFParser.T__75, DMFParser.T__76, DMFParser.T__77, DMFParser.T__78, DMFParser.T__79, DMFParser.T__80, DMFParser.T__81, DMFParser.T__82, DMFParser.T__83, DMFParser.T__84, DMFParser.T__85, DMFParser.T__86, DMFParser.T__87, DMFParser.T__88, DMFParser.T__89, DMFParser.T__90, DMFParser.T__91, DMFParser.T__92, DMFParser.T__93, DMFParser.T__94, DMFParser.T__95, DMFParser.T__96, DMFParser.T__97, DMFParser.T__100, DMFParser.T__101, DMFParser.T__106, DMFParser.T__126, DMFParser.T__129, DMFParser.T__134, DMFParser.T__135, DMFParser.T__137, DMFParser.T__138, DMFParser.T__145, DMFParser.T__146, DMFParser.T__147, DMFParser.T__148, DMFParser.T__149, DMFParser.T__150, DMFParser.T__151, DMFParser.T__152, DMFParser.T__153, DMFParser.T__154, DMFParser.T__155, DMFParser.T__156, DMFParser.T__157, DMFParser.T__158, DMFParser.T__159, DMFParser.T__160, DMFParser.INTERACTIVE, DMFParser.NOT, DMFParser.OFF, DMFParser.ON, DMFParser.SUB, DMFParser.TOGGLE, DMFParser.ID, DMFParser.INT, DMFParser.FLOAT, DMFParser.STRING]:
                self.state = 503
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
        self.enterRule(localctx, 34, self.RULE_macro_header)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 506
            self.match(DMFParser.T__63)
            self.state = 507
            self.match(DMFParser.T__17)
            self.state = 516
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << DMFParser.T__22) | (1 << DMFParser.T__23) | (1 << DMFParser.T__25) | (1 << DMFParser.T__26) | (1 << DMFParser.T__28) | (1 << DMFParser.T__29) | (1 << DMFParser.T__33) | (1 << DMFParser.T__42))) != 0) or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__69 - 66)) | (1 << (DMFParser.T__70 - 66)) | (1 << (DMFParser.T__71 - 66)) | (1 << (DMFParser.T__72 - 66)) | (1 << (DMFParser.T__73 - 66)) | (1 << (DMFParser.T__74 - 66)) | (1 << (DMFParser.T__75 - 66)) | (1 << (DMFParser.T__76 - 66)) | (1 << (DMFParser.T__77 - 66)) | (1 << (DMFParser.T__78 - 66)) | (1 << (DMFParser.T__79 - 66)) | (1 << (DMFParser.T__80 - 66)) | (1 << (DMFParser.T__81 - 66)) | (1 << (DMFParser.T__82 - 66)) | (1 << (DMFParser.T__83 - 66)) | (1 << (DMFParser.T__84 - 66)) | (1 << (DMFParser.T__85 - 66)) | (1 << (DMFParser.T__86 - 66)) | (1 << (DMFParser.T__87 - 66)) | (1 << (DMFParser.T__88 - 66)) | (1 << (DMFParser.T__89 - 66)) | (1 << (DMFParser.T__90 - 66)) | (1 << (DMFParser.T__91 - 66)) | (1 << (DMFParser.T__92 - 66)) | (1 << (DMFParser.T__93 - 66)) | (1 << (DMFParser.T__94 - 66)) | (1 << (DMFParser.T__95 - 66)) | (1 << (DMFParser.T__96 - 66)) | (1 << (DMFParser.T__97 - 66)) | (1 << (DMFParser.T__100 - 66)) | (1 << (DMFParser.T__101 - 66)) | (1 << (DMFParser.T__106 - 66)) | (1 << (DMFParser.T__126 - 66)))) != 0) or ((((_la - 130)) & ~0x3f) == 0 and ((1 << (_la - 130)) & ((1 << (DMFParser.T__129 - 130)) | (1 << (DMFParser.T__134 - 130)) | (1 << (DMFParser.T__135 - 130)) | (1 << (DMFParser.T__137 - 130)) | (1 << (DMFParser.T__138 - 130)) | (1 << (DMFParser.T__157 - 130)) | (1 << (DMFParser.T__158 - 130)) | (1 << (DMFParser.T__159 - 130)) | (1 << (DMFParser.T__160 - 130)) | (1 << (DMFParser.INTERACTIVE - 130)) | (1 << (DMFParser.OFF - 130)) | (1 << (DMFParser.ON - 130)) | (1 << (DMFParser.ID - 130)))) != 0):
                self.state = 508
                self.param()
                self.state = 513
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==DMFParser.T__18:
                    self.state = 509
                    self.match(DMFParser.T__18)
                    self.state = 510
                    self.param()
                    self.state = 515
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 518
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
        self.enterRule(localctx, 36, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.state = 543
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,50,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 521
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__22 or _la==DMFParser.T__33:
                    self.state = 520
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__22 or _la==DMFParser.T__33):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 523
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 526
                localctx._param_type = self.param_type()
                localctx.type=localctx._param_type.type
                self.state = 528
                localctx._INT = self.match(DMFParser.INT)
                localctx.n=(0 if localctx._INT is None else int(localctx._INT.text))
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 531
                localctx._param_type = self.param_type()
                self.state = 532
                localctx._name = self.name()
                localctx.type=localctx._param_type.type
                localctx.pname=(None if localctx._name is None else self._input.getText(localctx._name.start,localctx._name.stop))
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 536
                localctx._name = self.name()
                self.state = 537
                self.match(DMFParser.INJECT)
                self.state = 538
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
        self.enterRule(localctx, 38, self.RULE_no_arg_action)
        self._la = 0 # Token type
        try:
            self.state = 580
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,54,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 545
                self.match(DMFParser.T__64)
                self.state = 546
                self.match(DMFParser.ON)
                localctx.which="TURN-ON"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 548
                self.match(DMFParser.T__64)
                self.state = 549
                self.match(DMFParser.OFF)
                localctx.which="TURN-OFF"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 551
                self.match(DMFParser.TOGGLE)
                self.state = 553
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,51,self._ctx)
                if la_ == 1:
                    self.state = 552
                    self.match(DMFParser.T__65)


                localctx.which="TOGGLE"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 556
                self.match(DMFParser.T__66)
                self.state = 562
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,53,self._ctx)
                if la_ == 1:
                    self.state = 557
                    self.match(DMFParser.T__67)
                    self.state = 559
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==DMFParser.T__28:
                        self.state = 558
                        self.match(DMFParser.T__28)


                    self.state = 561
                    self.match(DMFParser.T__68)


                localctx.which="REMOVE-FROM-BOARD"
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 565
                self.match(DMFParser.T__69)
                self.state = 566
                self.match(DMFParser.T__70)
                localctx.which="RESET PADS"
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 568
                self.match(DMFParser.T__69)
                self.state = 569
                self.match(DMFParser.T__71)
                localctx.which="RESET MAGNETS"
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 571
                self.match(DMFParser.T__69)
                self.state = 572
                self.match(DMFParser.T__72)
                localctx.which="RESET HEATERS"
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 574
                self.match(DMFParser.T__69)
                self.state = 575
                self.match(DMFParser.T__73)
                localctx.which="RESET CHILLERS"
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 577
                self.match(DMFParser.T__69)
                self.state = 578
                self.match(DMFParser.T__74)
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
        self.enterRule(localctx, 40, self.RULE_param_type)
        self._la = 0 # Token type
        try:
            self.state = 648
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,57,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 582
                self.match(DMFParser.T__42)
                localctx.type=Type.DROP
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 584
                self.match(DMFParser.T__75)
                localctx.type=Type.PAD
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 586
                self.match(DMFParser.T__76)
                localctx.type=Type.WELL
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 588
                self.match(DMFParser.T__76)
                self.state = 589
                self.match(DMFParser.T__75)
                localctx.type=Type.WELL_PAD
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 592
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__76:
                    self.state = 591
                    self.match(DMFParser.T__76)


                self.state = 594
                self.match(DMFParser.T__77)
                localctx.type=Type.WELL_GATE
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 596
                self.match(DMFParser.T__78)
                localctx.type=Type.INT
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 598
                self.match(DMFParser.T__79)
                localctx.type=Type.FLOAT
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 600
                self.match(DMFParser.T__23)
                localctx.type=Type.STRING
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 602
                self.match(DMFParser.T__65)
                localctx.type=Type.BINARY_STATE
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 604
                self.match(DMFParser.T__80)
                localctx.type=Type.BINARY_CPT
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 606
                self.match(DMFParser.T__81)
                localctx.type=Type.DELTA
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 608
                self.match(DMFParser.T__82)
                localctx.type=Type.MOTION
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 610
                self.match(DMFParser.T__83)
                localctx.type=Type.DELAY
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 612
                self.match(DMFParser.T__84)
                localctx.type=Type.TIME
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 614
                self.match(DMFParser.T__85)
                localctx.type=Type.TICKS
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 616
                self.match(DMFParser.T__86)
                localctx.type=Type.BOOL
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 618
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__25 or _la==DMFParser.T__26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.type=Type.DIR
                pass

            elif la_ == 18:
                self.enterOuterAlt(localctx, 18)
                self.state = 620
                self.match(DMFParser.T__87)
                localctx.type=Type.VOLUME
                pass

            elif la_ == 19:
                self.enterOuterAlt(localctx, 19)
                self.state = 622
                self.match(DMFParser.T__29)
                localctx.type=Type.REAGENT
                pass

            elif la_ == 20:
                self.enterOuterAlt(localctx, 20)
                self.state = 624
                self.match(DMFParser.T__88)
                localctx.type=Type.LIQUID
                pass

            elif la_ == 21:
                self.enterOuterAlt(localctx, 21)
                self.state = 626
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__89 or _la==DMFParser.T__90):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 627
                _la = self._input.LA(1)
                if not(((((_la - 82)) & ~0x3f) == 0 and ((1 << (_la - 82)) & ((1 << (DMFParser.T__81 - 82)) | (1 << (DMFParser.T__91 - 82)) | (1 << (DMFParser.T__92 - 82)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.type=Type.REL_TEMP
                pass

            elif la_ == 22:
                self.enterOuterAlt(localctx, 22)
                self.state = 629
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__89 or _la==DMFParser.T__90):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 631
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,56,self._ctx)
                if la_ == 1:
                    self.state = 630
                    self.match(DMFParser.T__93)


                localctx.type=Type.ABS_TEMP
                pass

            elif la_ == 23:
                self.enterOuterAlt(localctx, 23)
                self.state = 634
                self.match(DMFParser.T__94)
                localctx.type=Type.HEATER
                pass

            elif la_ == 24:
                self.enterOuterAlt(localctx, 24)
                self.state = 636
                self.match(DMFParser.T__95)
                localctx.type=Type.CHILLER
                pass

            elif la_ == 25:
                self.enterOuterAlt(localctx, 25)
                self.state = 638
                self.match(DMFParser.T__96)
                localctx.type=Type.MAGNET
                pass

            elif la_ == 26:
                self.enterOuterAlt(localctx, 26)
                self.state = 640
                self.match(DMFParser.T__97)
                self.state = 641
                self.match(DMFParser.T__98)
                localctx.type=Type.POWER_SUPPLY
                pass

            elif la_ == 27:
                self.enterOuterAlt(localctx, 27)
                self.state = 643
                self.match(DMFParser.T__97)
                self.state = 644
                self.match(DMFParser.T__99)
                localctx.type=Type.POWER_MODE
                pass

            elif la_ == 28:
                self.enterOuterAlt(localctx, 28)
                self.state = 646
                self.match(DMFParser.T__100)
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
        self.enterRule(localctx, 42, self.RULE_dim_unit)
        self._la = 0 # Token type
        try:
            self.state = 664
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__101, DMFParser.T__102, DMFParser.T__103, DMFParser.T__104, DMFParser.T__105]:
                self.enterOuterAlt(localctx, 1)
                self.state = 650
                _la = self._input.LA(1)
                if not(((((_la - 102)) & ~0x3f) == 0 and ((1 << (_la - 102)) & ((1 << (DMFParser.T__101 - 102)) | (1 << (DMFParser.T__102 - 102)) | (1 << (DMFParser.T__103 - 102)) | (1 << (DMFParser.T__104 - 102)) | (1 << (DMFParser.T__105 - 102)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.sec
                pass
            elif token in [DMFParser.T__106, DMFParser.T__107, DMFParser.T__108]:
                self.enterOuterAlt(localctx, 2)
                self.state = 652
                _la = self._input.LA(1)
                if not(((((_la - 107)) & ~0x3f) == 0 and ((1 << (_la - 107)) & ((1 << (DMFParser.T__106 - 107)) | (1 << (DMFParser.T__107 - 107)) | (1 << (DMFParser.T__108 - 107)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.ms
                pass
            elif token in [DMFParser.T__109, DMFParser.T__110, DMFParser.T__111, DMFParser.T__112, DMFParser.T__113, DMFParser.T__114]:
                self.enterOuterAlt(localctx, 3)
                self.state = 654
                _la = self._input.LA(1)
                if not(((((_la - 110)) & ~0x3f) == 0 and ((1 << (_la - 110)) & ((1 << (DMFParser.T__109 - 110)) | (1 << (DMFParser.T__110 - 110)) | (1 << (DMFParser.T__111 - 110)) | (1 << (DMFParser.T__112 - 110)) | (1 << (DMFParser.T__113 - 110)) | (1 << (DMFParser.T__114 - 110)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.uL
                pass
            elif token in [DMFParser.T__115, DMFParser.T__116, DMFParser.T__117, DMFParser.T__118, DMFParser.T__119, DMFParser.T__120]:
                self.enterOuterAlt(localctx, 4)
                self.state = 656
                _la = self._input.LA(1)
                if not(((((_la - 116)) & ~0x3f) == 0 and ((1 << (_la - 116)) & ((1 << (DMFParser.T__115 - 116)) | (1 << (DMFParser.T__116 - 116)) | (1 << (DMFParser.T__117 - 116)) | (1 << (DMFParser.T__118 - 116)) | (1 << (DMFParser.T__119 - 116)) | (1 << (DMFParser.T__120 - 116)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=SI.mL
                pass
            elif token in [DMFParser.T__85, DMFParser.T__121]:
                self.enterOuterAlt(localctx, 5)
                self.state = 658
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__85 or _la==DMFParser.T__121):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=ticks
                pass
            elif token in [DMFParser.T__42, DMFParser.T__122]:
                self.enterOuterAlt(localctx, 6)
                self.state = 660
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__42 or _la==DMFParser.T__122):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.unit=EnvRelativeUnit.DROP
                pass
            elif token in [DMFParser.T__123, DMFParser.T__124, DMFParser.T__125]:
                self.enterOuterAlt(localctx, 7)
                self.state = 662
                _la = self._input.LA(1)
                if not(((((_la - 124)) & ~0x3f) == 0 and ((1 << (_la - 124)) & ((1 << (DMFParser.T__123 - 124)) | (1 << (DMFParser.T__124 - 124)) | (1 << (DMFParser.T__125 - 124)))) != 0)):
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
        self.enterRule(localctx, 44, self.RULE_numbered_type)
        try:
            self.state = 674
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__76]:
                self.enterOuterAlt(localctx, 1)
                self.state = 666
                self.match(DMFParser.T__76)
                localctx.kind=NumberedItem.WELL
                pass
            elif token in [DMFParser.T__94]:
                self.enterOuterAlt(localctx, 2)
                self.state = 668
                self.match(DMFParser.T__94)
                localctx.kind=NumberedItem.HEATER
                pass
            elif token in [DMFParser.T__95]:
                self.enterOuterAlt(localctx, 3)
                self.state = 670
                self.match(DMFParser.T__95)
                localctx.kind=NumberedItem.CHILLER
                pass
            elif token in [DMFParser.T__96]:
                self.enterOuterAlt(localctx, 4)
                self.state = 672
                self.match(DMFParser.T__96)
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
        self.enterRule(localctx, 46, self.RULE_attr)
        self._la = 0 # Token type
        try:
            self.state = 729
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,64,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 676
                self.match(DMFParser.T__15)
                self.state = 677
                self.match(DMFParser.T__75)
                localctx.which="#exit_pad"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 679
                self.match(DMFParser.T__77)
                localctx.which="gate"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 681
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__25 or _la==DMFParser.T__26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="direction"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 686
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__57]:
                    self.state = 683
                    self.match(DMFParser.T__57)
                    pass
                elif token in [DMFParser.T__126]:
                    self.state = 684
                    self.match(DMFParser.T__126)
                    self.state = 685
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__127 or _la==DMFParser.T__128):
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
                self.state = 693
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [DMFParser.T__59]:
                    self.state = 689
                    self.match(DMFParser.T__59)
                    pass
                elif token in [DMFParser.T__60]:
                    self.state = 690
                    self.match(DMFParser.T__60)
                    pass
                elif token in [DMFParser.T__129]:
                    self.state = 691
                    self.match(DMFParser.T__129)
                    self.state = 692
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__127 or _la==DMFParser.T__128):
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
                self.state = 696
                self.match(DMFParser.T__15)
                self.state = 697
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__25 or _la==DMFParser.T__26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#exit_dir"
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 699
                self.match(DMFParser.T__130)
                self.state = 700
                self.match(DMFParser.T__131)
                localctx.which="#remaining_capacity"
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 702
                self.match(DMFParser.T__132)
                self.state = 704
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,62,self._ctx)
                if la_ == 1:
                    self.state = 703
                    _la = self._input.LA(1)
                    if not(_la==DMFParser.T__89 or _la==DMFParser.T__90):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                localctx.which="#target_temperature"
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 708
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__133:
                    self.state = 707
                    self.match(DMFParser.T__133)


                self.state = 710
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__89 or _la==DMFParser.T__90):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#current_temperature"
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 712
                self.match(DMFParser.T__97)
                self.state = 713
                self.match(DMFParser.T__98)
                localctx.which="#power_supply"
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 715
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__134 or _la==DMFParser.T__135):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 716
                self.match(DMFParser.T__136)
                localctx.which="#min_voltage"
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 718
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__137 or _la==DMFParser.T__138):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 719
                self.match(DMFParser.T__136)
                localctx.which="#max_voltage"
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 721
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__134 or _la==DMFParser.T__135):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 722
                _la = self._input.LA(1)
                if not(((((_la - 90)) & ~0x3f) == 0 and ((1 << (_la - 90)) & ((1 << (DMFParser.T__89 - 90)) | (1 << (DMFParser.T__90 - 90)) | (1 << (DMFParser.T__132 - 90)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#min_target"
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 724
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__137 or _la==DMFParser.T__138):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 725
                _la = self._input.LA(1)
                if not(((((_la - 90)) & ~0x3f) == 0 and ((1 << (_la - 90)) & ((1 << (DMFParser.T__89 - 90)) | (1 << (DMFParser.T__90 - 90)) | (1 << (DMFParser.T__132 - 90)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.which="#max_target"
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 727
                localctx.n = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==DMFParser.T__29 or _la==DMFParser.T__42 or ((((_la - 66)) & ~0x3f) == 0 and ((1 << (_la - 66)) & ((1 << (DMFParser.T__65 - 66)) | (1 << (DMFParser.T__75 - 66)) | (1 << (DMFParser.T__76 - 66)) | (1 << (DMFParser.T__87 - 66)) | (1 << (DMFParser.T__94 - 66)) | (1 << (DMFParser.T__95 - 66)) | (1 << (DMFParser.T__96 - 66)) | (1 << (DMFParser.T__100 - 66)))) != 0) or _la==DMFParser.ID):
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
        self.enterRule(localctx, 48, self.RULE_rel)
        try:
            self.state = 743
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__139]:
                self.enterOuterAlt(localctx, 1)
                self.state = 731
                self.match(DMFParser.T__139)
                localctx.which=Rel.EQ
                pass
            elif token in [DMFParser.T__140]:
                self.enterOuterAlt(localctx, 2)
                self.state = 733
                self.match(DMFParser.T__140)
                localctx.which=Rel.NE
                pass
            elif token in [DMFParser.T__141]:
                self.enterOuterAlt(localctx, 3)
                self.state = 735
                self.match(DMFParser.T__141)
                localctx.which=Rel.LT
                pass
            elif token in [DMFParser.T__142]:
                self.enterOuterAlt(localctx, 4)
                self.state = 737
                self.match(DMFParser.T__142)
                localctx.which=Rel.LE
                pass
            elif token in [DMFParser.T__143]:
                self.enterOuterAlt(localctx, 5)
                self.state = 739
                self.match(DMFParser.T__143)
                localctx.which=Rel.GT
                pass
            elif token in [DMFParser.T__144]:
                self.enterOuterAlt(localctx, 6)
                self.state = 741
                self.match(DMFParser.T__144)
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
        self.enterRule(localctx, 50, self.RULE_bool_val)
        self._la = 0 # Token type
        try:
            self.state = 749
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [DMFParser.T__145, DMFParser.T__146, DMFParser.T__147, DMFParser.T__148, DMFParser.T__149, DMFParser.T__150]:
                self.enterOuterAlt(localctx, 1)
                self.state = 745
                _la = self._input.LA(1)
                if not(((((_la - 146)) & ~0x3f) == 0 and ((1 << (_la - 146)) & ((1 << (DMFParser.T__145 - 146)) | (1 << (DMFParser.T__146 - 146)) | (1 << (DMFParser.T__147 - 146)) | (1 << (DMFParser.T__148 - 146)) | (1 << (DMFParser.T__149 - 146)) | (1 << (DMFParser.T__150 - 146)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                localctx.val=True
                pass
            elif token in [DMFParser.T__151, DMFParser.T__152, DMFParser.T__153, DMFParser.T__154, DMFParser.T__155, DMFParser.T__156]:
                self.enterOuterAlt(localctx, 2)
                self.state = 747
                _la = self._input.LA(1)
                if not(((((_la - 152)) & ~0x3f) == 0 and ((1 << (_la - 152)) & ((1 << (DMFParser.T__151 - 152)) | (1 << (DMFParser.T__152 - 152)) | (1 << (DMFParser.T__153 - 152)) | (1 << (DMFParser.T__154 - 152)) | (1 << (DMFParser.T__155 - 152)) | (1 << (DMFParser.T__156 - 152)))) != 0)):
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
        self.enterRule(localctx, 52, self.RULE_name)
        try:
            self.state = 759
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,67,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 751
                localctx._multi_word_name = self.multi_word_name()
                localctx.val=localctx._multi_word_name.val
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 754
                localctx._ID = self.match(DMFParser.ID)
                localctx.val=(None if localctx._ID is None else localctx._ID.text)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 756
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
        self.enterRule(localctx, 54, self.RULE_multi_word_name)
        self._la = 0 # Token type
        try:
            self.state = 794
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,72,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 761
                self.match(DMFParser.ON)
                self.state = 763
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__28:
                    self.state = 762
                    self.match(DMFParser.T__28)


                self.state = 765
                self.match(DMFParser.T__68)
                localctx.val="on board"
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 768
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__28:
                    self.state = 767
                    self.match(DMFParser.T__28)


                self.state = 770
                self.match(DMFParser.INTERACTIVE)
                self.state = 771
                self.match(DMFParser.T__29)
                localctx.val="interactive reagent"
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 774
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__28:
                    self.state = 773
                    self.match(DMFParser.T__28)


                self.state = 776
                self.match(DMFParser.INTERACTIVE)
                self.state = 777
                self.match(DMFParser.T__87)
                localctx.val="interactive volume"
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 779
                self.match(DMFParser.T__28)
                self.state = 780
                self.match(DMFParser.T__68)
                localctx.val="the board"
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 783
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==DMFParser.T__28:
                    self.state = 782
                    self.match(DMFParser.T__28)


                self.state = 785
                self.match(DMFParser.T__157)
                self.state = 786
                self.match(DMFParser.T__158)
                localctx.val="index base"
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 788
                self.match(DMFParser.T__159)
                self.state = 789
                self.match(DMFParser.T__42)
                localctx.val="dispense drop"
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 791
                self.match(DMFParser.T__160)
                self.state = 792
                self.match(DMFParser.T__76)
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
        self.enterRule(localctx, 56, self.RULE_kwd_names)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 796
            _la = self._input.LA(1)
            if not(_la==DMFParser.T__22 or _la==DMFParser.T__33 or ((((_la - 70)) & ~0x3f) == 0 and ((1 << (_la - 70)) & ((1 << (DMFParser.T__69 - 70)) | (1 << (DMFParser.T__70 - 70)) | (1 << (DMFParser.T__71 - 70)) | (1 << (DMFParser.T__72 - 70)) | (1 << (DMFParser.T__73 - 70)) | (1 << (DMFParser.T__74 - 70)) | (1 << (DMFParser.T__81 - 70)) | (1 << (DMFParser.T__91 - 70)) | (1 << (DMFParser.T__92 - 70)) | (1 << (DMFParser.T__93 - 70)) | (1 << (DMFParser.T__101 - 70)) | (1 << (DMFParser.T__106 - 70)) | (1 << (DMFParser.T__126 - 70)) | (1 << (DMFParser.T__129 - 70)))) != 0) or ((((_la - 135)) & ~0x3f) == 0 and ((1 << (_la - 135)) & ((1 << (DMFParser.T__134 - 135)) | (1 << (DMFParser.T__135 - 135)) | (1 << (DMFParser.T__137 - 135)) | (1 << (DMFParser.T__138 - 135)) | (1 << (DMFParser.T__157 - 135)) | (1 << (DMFParser.T__158 - 135)) | (1 << (DMFParser.T__159 - 135)) | (1 << (DMFParser.T__160 - 135)) | (1 << (DMFParser.OFF - 135)) | (1 << (DMFParser.ON - 135)))) != 0)):
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
        self.enterRule(localctx, 58, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 798
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
        self._predicates[10] = self.expr_sempred
        self._predicates[14] = self.rc_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 40)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 33)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 32)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 31)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 30)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 28)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 26)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 25)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 16)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 11:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 12:
                return self.precpred(self._ctx, 49)
         

            if predIndex == 13:
                return self.precpred(self._ctx, 46)
         

            if predIndex == 14:
                return self.precpred(self._ctx, 44)
         

            if predIndex == 15:
                return self.precpred(self._ctx, 43)
         

            if predIndex == 16:
                return self.precpred(self._ctx, 42)
         

            if predIndex == 17:
                return self.precpred(self._ctx, 41)
         

            if predIndex == 18:
                return self.precpred(self._ctx, 38)
         

            if predIndex == 19:
                return self.precpred(self._ctx, 37)
         

            if predIndex == 20:
                return self.precpred(self._ctx, 36)
         

            if predIndex == 21:
                return self.precpred(self._ctx, 29)
         

            if predIndex == 22:
                return self.precpred(self._ctx, 18)
         

    def rc_sempred(self, localctx:RcContext, predIndex:int):
            if predIndex == 23:
                return localctx.n==1
         

            if predIndex == 24:
                return localctx.n==1
         




