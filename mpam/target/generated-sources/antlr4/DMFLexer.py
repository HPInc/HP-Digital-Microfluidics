# Generated from DMF.g4 by ANTLR 4.9.2
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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2I")
        buf.write("\u0239\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\t")
        buf.write("L\4M\tM\4N\tN\4O\tO\4P\tP\3\2\3\2\3\2\3\2\3\2\3\2\3\3")
        buf.write("\3\3\3\4\3\4\3\5\3\5\3\5\3\6\3\6\3\6\3\7\3\7\3\b\3\b\3")
        buf.write("\t\3\t\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3")
        buf.write("\13\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\16\3\16\3\17\3\17")
        buf.write("\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22")
        buf.write("\3\22\3\23\3\23\3\23\3\23\3\24\3\24\3\24\3\24\3\24\3\25")
        buf.write("\3\25\3\26\3\26\3\26\3\27\3\27\3\27\3\27\3\27\3\30\3\30")
        buf.write("\3\30\3\30\3\30\3\30\3\31\3\31\3\31\3\31\3\32\3\32\3\32")
        buf.write("\3\33\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\34")
        buf.write("\3\35\3\35\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\36")
        buf.write("\3\37\3\37\3\37\3\37\3\37\3 \3 \3 \3 \3 \3 \3!\3!\3!\3")
        buf.write("!\3!\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3#\3$\3$\3$\3$\3%\3%")
        buf.write("\3%\3%\3%\3%\3%\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'")
        buf.write("\3\'\3\'\3(\3(\3(\3(\3(\3(\3)\3)\3)\3)\3*\3*\3*\3*\3*")
        buf.write("\3*\3*\3*\3*\3*\3+\3+\3+\3+\3+\3+\3,\3,\3,\3,\3,\3,\3")
        buf.write(",\3-\3-\3-\3-\3-\3-\3.\3.\3.\3.\3.\3/\3/\3\60\3\60\3\60")
        buf.write("\3\60\3\61\3\61\3\61\3\61\3\61\3\62\3\62\3\62\3\62\3\62")
        buf.write("\3\62\3\62\3\63\3\63\3\63\3\63\3\63\3\63\3\63\3\63\3\64")
        buf.write("\3\64\3\64\3\65\3\65\3\65\3\65\3\65\3\65\3\65\3\65\3\65")
        buf.write("\3\65\3\65\3\65\3\66\3\66\3\66\3\66\3\66\3\66\3\66\3\66")
        buf.write("\3\66\3\66\3\66\3\66\3\66\3\67\3\67\38\38\39\39\39\3:")
        buf.write("\3:\3;\3;\3<\3<\3=\3=\3=\3=\3>\3>\3>\3?\3?\3@\3@\3A\3")
        buf.write("A\3A\3A\3A\3A\3A\3B\3B\3C\3C\3D\3D\5D\u01c9\nD\3E\3E\5")
        buf.write("E\u01cd\nE\3F\3F\3F\5F\u01d2\nF\3F\7F\u01d5\nF\fF\16F")
        buf.write("\u01d8\13F\3F\5F\u01db\nF\3G\6G\u01de\nG\rG\16G\u01df")
        buf.write("\3G\3G\6G\u01e4\nG\rG\16G\u01e5\7G\u01e8\nG\fG\16G\u01eb")
        buf.write("\13G\3H\3H\5H\u01ef\nH\3H\3H\3I\3I\3I\3I\5I\u01f7\nI\3")
        buf.write("I\3I\3I\5I\u01fc\nI\3J\3J\5J\u0200\nJ\3K\3K\3L\3L\3L\3")
        buf.write("L\3L\3L\3L\3L\3L\5L\u020d\nL\3M\3M\7M\u0211\nM\fM\16M")
        buf.write("\u0214\13M\3M\3M\3N\3N\3N\3N\7N\u021c\nN\fN\16N\u021f")
        buf.write("\13N\3N\5N\u0222\nN\3N\3N\3N\3N\3O\3O\3O\3O\7O\u022c\n")
        buf.write("O\fO\16O\u022f\13O\3O\3O\3O\3O\3O\3P\3P\3P\3P\4\u021d")
        buf.write("\u022d\2Q\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25")
        buf.write("\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+")
        buf.write("\27-\30/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E")
        buf.write("$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k")
        buf.write("\67m8o9q:s;u<w=y>{?}@\177A\u0081B\u0083\2\u0085\2\u0087")
        buf.write("\2\u0089\2\u008bC\u008dD\u008f\2\u0091E\u0093\2\u0095")
        buf.write("\2\u0097\2\u0099F\u009bG\u009dH\u009fI\3\2\t\4\2C\\c|")
        buf.write("\3\2\62;\4\2GGgg\6\2\f\f\17\17$$^^\5\2\62;CHch\b\2$$)")
        buf.write(")^^ppttvv\5\2\13\f\17\17\"\"\2\u0241\2\3\3\2\2\2\2\5\3")
        buf.write("\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2")
        buf.write("\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2")
        buf.write("\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2")
        buf.write("\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2")
        buf.write("\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3")
        buf.write("\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2")
        buf.write("\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2")
        buf.write("\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3")
        buf.write("\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W")
        buf.write("\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2")
        buf.write("a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2")
        buf.write("\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2\2")
        buf.write("\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2")
        buf.write("\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u008b\3\2\2\2\2\u008d")
        buf.write("\3\2\2\2\2\u0091\3\2\2\2\2\u0099\3\2\2\2\2\u009b\3\2\2")
        buf.write("\2\2\u009d\3\2\2\2\2\u009f\3\2\2\2\3\u00a1\3\2\2\2\5\u00a7")
        buf.write("\3\2\2\2\7\u00a9\3\2\2\2\t\u00ab\3\2\2\2\13\u00ae\3\2")
        buf.write("\2\2\r\u00b1\3\2\2\2\17\u00b3\3\2\2\2\21\u00b5\3\2\2\2")
        buf.write("\23\u00b7\3\2\2\2\25\u00bc\3\2\2\2\27\u00c2\3\2\2\2\31")
        buf.write("\u00c5\3\2\2\2\33\u00ca\3\2\2\2\35\u00cc\3\2\2\2\37\u00ce")
        buf.write("\3\2\2\2!\u00d0\3\2\2\2#\u00d5\3\2\2\2%\u00da\3\2\2\2")
        buf.write("\'\u00de\3\2\2\2)\u00e3\3\2\2\2+\u00e5\3\2\2\2-\u00e8")
        buf.write("\3\2\2\2/\u00ed\3\2\2\2\61\u00f3\3\2\2\2\63\u00f7\3\2")
        buf.write("\2\2\65\u00fa\3\2\2\2\67\u0100\3\2\2\29\u0105\3\2\2\2")
        buf.write(";\u010b\3\2\2\2=\u0110\3\2\2\2?\u0115\3\2\2\2A\u011b\3")
        buf.write("\2\2\2C\u0120\3\2\2\2E\u0124\3\2\2\2G\u0129\3\2\2\2I\u012d")
        buf.write("\3\2\2\2K\u0134\3\2\2\2M\u0139\3\2\2\2O\u0141\3\2\2\2")
        buf.write("Q\u0147\3\2\2\2S\u014b\3\2\2\2U\u0155\3\2\2\2W\u015b\3")
        buf.write("\2\2\2Y\u0162\3\2\2\2[\u0168\3\2\2\2]\u016d\3\2\2\2_\u016f")
        buf.write("\3\2\2\2a\u0173\3\2\2\2c\u0178\3\2\2\2e\u017f\3\2\2\2")
        buf.write("g\u0187\3\2\2\2i\u018a\3\2\2\2k\u0196\3\2\2\2m\u01a3\3")
        buf.write("\2\2\2o\u01a5\3\2\2\2q\u01a7\3\2\2\2s\u01aa\3\2\2\2u\u01ac")
        buf.write("\3\2\2\2w\u01ae\3\2\2\2y\u01b0\3\2\2\2{\u01b4\3\2\2\2")
        buf.write("}\u01b7\3\2\2\2\177\u01b9\3\2\2\2\u0081\u01bb\3\2\2\2")
        buf.write("\u0083\u01c2\3\2\2\2\u0085\u01c4\3\2\2\2\u0087\u01c8\3")
        buf.write("\2\2\2\u0089\u01cc\3\2\2\2\u008b\u01d1\3\2\2\2\u008d\u01dd")
        buf.write("\3\2\2\2\u008f\u01ec\3\2\2\2\u0091\u01fb\3\2\2\2\u0093")
        buf.write("\u01ff\3\2\2\2\u0095\u0201\3\2\2\2\u0097\u020c\3\2\2\2")
        buf.write("\u0099\u020e\3\2\2\2\u009b\u0217\3\2\2\2\u009d\u0227\3")
        buf.write("\2\2\2\u009f\u0235\3\2\2\2\u00a1\u00a2\7r\2\2\u00a2\u00a3")
        buf.write("\7c\2\2\u00a3\u00a4\7w\2\2\u00a4\u00a5\7u\2\2\u00a5\u00a6")
        buf.write("\7g\2\2\u00a6\4\3\2\2\2\u00a7\u00a8\7}\2\2\u00a8\6\3\2")
        buf.write("\2\2\u00a9\u00aa\7\177\2\2\u00aa\b\3\2\2\2\u00ab\u00ac")
        buf.write("\7]\2\2\u00ac\u00ad\7]\2\2\u00ad\n\3\2\2\2\u00ae\u00af")
        buf.write("\7_\2\2\u00af\u00b0\7_\2\2\u00b0\f\3\2\2\2\u00b1\u00b2")
        buf.write("\7*\2\2\u00b2\16\3\2\2\2\u00b3\u00b4\7+\2\2\u00b4\20\3")
        buf.write("\2\2\2\u00b5\u00b6\7.\2\2\u00b6\22\3\2\2\2\u00b7\u00b8")
        buf.write("\7v\2\2\u00b8\u00b9\7k\2\2\u00b9\u00ba\7e\2\2\u00ba\u00bb")
        buf.write("\7m\2\2\u00bb\24\3\2\2\2\u00bc\u00bd\7v\2\2\u00bd\u00be")
        buf.write("\7k\2\2\u00be\u00bf\7e\2\2\u00bf\u00c0\7m\2\2\u00c0\u00c1")
        buf.write("\7u\2\2\u00c1\26\3\2\2\2\u00c2\u00c3\7v\2\2\u00c3\u00c4")
        buf.write("\7q\2\2\u00c4\30\3\2\2\2\u00c5\u00c6\7y\2\2\u00c6\u00c7")
        buf.write("\7g\2\2\u00c7\u00c8\7n\2\2\u00c8\u00c9\7n\2\2\u00c9\32")
        buf.write("\3\2\2\2\u00ca\u00cb\7%\2\2\u00cb\34\3\2\2\2\u00cc\u00cd")
        buf.write("\7]\2\2\u00cd\36\3\2\2\2\u00ce\u00cf\7_\2\2\u00cf \3\2")
        buf.write("\2\2\u00d0\u00d1\7i\2\2\u00d1\u00d2\7c\2\2\u00d2\u00d3")
        buf.write("\7v\2\2\u00d3\u00d4\7g\2\2\u00d4\"\3\2\2\2\u00d5\u00d6")
        buf.write("\7g\2\2\u00d6\u00d7\7z\2\2\u00d7\u00d8\7k\2\2\u00d8\u00d9")
        buf.write("\7v\2\2\u00d9$\3\2\2\2\u00da\u00db\7r\2\2\u00db\u00dc")
        buf.write("\7c\2\2\u00dc\u00dd\7f\2\2\u00dd&\3\2\2\2\u00de\u00df")
        buf.write("\7f\2\2\u00df\u00e0\7t\2\2\u00e0\u00e1\7q\2\2\u00e1\u00e2")
        buf.write("\7r\2\2\u00e2(\3\2\2\2\u00e3\u00e4\7B\2\2\u00e4*\3\2\2")
        buf.write("\2\u00e5\u00e6\7c\2\2\u00e6\u00e7\7v\2\2\u00e7,\3\2\2")
        buf.write("\2\u00e8\u00e9\7v\2\2\u00e9\u00ea\7w\2\2\u00ea\u00eb\7")
        buf.write("t\2\2\u00eb\u00ec\7p\2\2\u00ec.\3\2\2\2\u00ed\u00ee\7")
        buf.write("u\2\2\u00ee\u00ef\7v\2\2\u00ef\u00f0\7c\2\2\u00f0\u00f1")
        buf.write("\7v\2\2\u00f1\u00f2\7g\2\2\u00f2\60\3\2\2\2\u00f3\u00f4")
        buf.write("\7v\2\2\u00f4\u00f5\7j\2\2\u00f5\u00f6\7g\2\2\u00f6\62")
        buf.write("\3\2\2\2\u00f7\u00f8\7w\2\2\u00f8\u00f9\7r\2\2\u00f9\64")
        buf.write("\3\2\2\2\u00fa\u00fb\7p\2\2\u00fb\u00fc\7q\2\2\u00fc\u00fd")
        buf.write("\7t\2\2\u00fd\u00fe\7v\2\2\u00fe\u00ff\7j\2\2\u00ff\66")
        buf.write("\3\2\2\2\u0100\u0101\7f\2\2\u0101\u0102\7q\2\2\u0102\u0103")
        buf.write("\7y\2\2\u0103\u0104\7p\2\2\u01048\3\2\2\2\u0105\u0106")
        buf.write("\7u\2\2\u0106\u0107\7q\2\2\u0107\u0108\7w\2\2\u0108\u0109")
        buf.write("\7v\2\2\u0109\u010a\7j\2\2\u010a:\3\2\2\2\u010b\u010c")
        buf.write("\7n\2\2\u010c\u010d\7g\2\2\u010d\u010e\7h\2\2\u010e\u010f")
        buf.write("\7v\2\2\u010f<\3\2\2\2\u0110\u0111\7y\2\2\u0111\u0112")
        buf.write("\7g\2\2\u0112\u0113\7u\2\2\u0113\u0114\7v\2\2\u0114>\3")
        buf.write("\2\2\2\u0115\u0116\7t\2\2\u0116\u0117\7k\2\2\u0117\u0118")
        buf.write("\7i\2\2\u0118\u0119\7j\2\2\u0119\u011a\7v\2\2\u011a@\3")
        buf.write("\2\2\2\u011b\u011c\7g\2\2\u011c\u011d\7c\2\2\u011d\u011e")
        buf.write("\7u\2\2\u011e\u011f\7v\2\2\u011fB\3\2\2\2\u0120\u0121")
        buf.write("\7t\2\2\u0121\u0122\7q\2\2\u0122\u0123\7y\2\2\u0123D\3")
        buf.write("\2\2\2\u0124\u0125\7t\2\2\u0125\u0126\7q\2\2\u0126\u0127")
        buf.write("\7y\2\2\u0127\u0128\7u\2\2\u0128F\3\2\2\2\u0129\u012a")
        buf.write("\7e\2\2\u012a\u012b\7q\2\2\u012b\u012c\7n\2\2\u012cH\3")
        buf.write("\2\2\2\u012d\u012e\7e\2\2\u012e\u012f\7q\2\2\u012f\u0130")
        buf.write("\7n\2\2\u0130\u0131\7w\2\2\u0131\u0132\7o\2\2\u0132\u0133")
        buf.write("\7p\2\2\u0133J\3\2\2\2\u0134\u0135\7e\2\2\u0135\u0136")
        buf.write("\7q\2\2\u0136\u0137\7n\2\2\u0137\u0138\7u\2\2\u0138L\3")
        buf.write("\2\2\2\u0139\u013a\7e\2\2\u013a\u013b\7q\2\2\u013b\u013c")
        buf.write("\7n\2\2\u013c\u013d\7w\2\2\u013d\u013e\7o\2\2\u013e\u013f")
        buf.write("\7p\2\2\u013f\u0140\7u\2\2\u0140N\3\2\2\2\u0141\u0142")
        buf.write("\7o\2\2\u0142\u0143\7c\2\2\u0143\u0144\7e\2\2\u0144\u0145")
        buf.write("\7t\2\2\u0145\u0146\7q\2\2\u0146P\3\2\2\2\u0147\u0148")
        buf.write("\7k\2\2\u0148\u0149\7p\2\2\u0149\u014a\7v\2\2\u014aR\3")
        buf.write("\2\2\2\u014b\u014c\7e\2\2\u014c\u014d\7q\2\2\u014d\u014e")
        buf.write("\7o\2\2\u014e\u014f\7r\2\2\u014f\u0150\7q\2\2\u0150\u0151")
        buf.write("\7p\2\2\u0151\u0152\7g\2\2\u0152\u0153\7p\2\2\u0153\u0154")
        buf.write("\7v\2\2\u0154T\3\2\2\2\u0155\u0156\7f\2\2\u0156\u0157")
        buf.write("\7g\2\2\u0157\u0158\7n\2\2\u0158\u0159\7v\2\2\u0159\u015a")
        buf.write("\7c\2\2\u015aV\3\2\2\2\u015b\u015c\7o\2\2\u015c\u015d")
        buf.write("\7q\2\2\u015d\u015e\7v\2\2\u015e\u015f\7k\2\2\u015f\u0160")
        buf.write("\7q\2\2\u0160\u0161\7p\2\2\u0161X\3\2\2\2\u0162\u0163")
        buf.write("\7f\2\2\u0163\u0164\7g\2\2\u0164\u0165\7n\2\2\u0165\u0166")
        buf.write("\7c\2\2\u0166\u0167\7{\2\2\u0167Z\3\2\2\2\u0168\u0169")
        buf.write("\7v\2\2\u0169\u016a\7k\2\2\u016a\u016b\7o\2\2\u016b\u016c")
        buf.write("\7g\2\2\u016c\\\3\2\2\2\u016d\u016e\7u\2\2\u016e^\3\2")
        buf.write("\2\2\u016f\u0170\7u\2\2\u0170\u0171\7g\2\2\u0171\u0172")
        buf.write("\7e\2\2\u0172`\3\2\2\2\u0173\u0174\7u\2\2\u0174\u0175")
        buf.write("\7g\2\2\u0175\u0176\7e\2\2\u0176\u0177\7u\2\2\u0177b\3")
        buf.write("\2\2\2\u0178\u0179\7u\2\2\u0179\u017a\7g\2\2\u017a\u017b")
        buf.write("\7e\2\2\u017b\u017c\7q\2\2\u017c\u017d\7p\2\2\u017d\u017e")
        buf.write("\7f\2\2\u017ed\3\2\2\2\u017f\u0180\7u\2\2\u0180\u0181")
        buf.write("\7g\2\2\u0181\u0182\7e\2\2\u0182\u0183\7q\2\2\u0183\u0184")
        buf.write("\7p\2\2\u0184\u0185\7f\2\2\u0185\u0186\7u\2\2\u0186f\3")
        buf.write("\2\2\2\u0187\u0188\7o\2\2\u0188\u0189\7u\2\2\u0189h\3")
        buf.write("\2\2\2\u018a\u018b\7o\2\2\u018b\u018c\7k\2\2\u018c\u018d")
        buf.write("\7n\2\2\u018d\u018e\7n\2\2\u018e\u018f\7k\2\2\u018f\u0190")
        buf.write("\7u\2\2\u0190\u0191\7g\2\2\u0191\u0192\7e\2\2\u0192\u0193")
        buf.write("\7q\2\2\u0193\u0194\7p\2\2\u0194\u0195\7f\2\2\u0195j\3")
        buf.write("\2\2\2\u0196\u0197\7o\2\2\u0197\u0198\7k\2\2\u0198\u0199")
        buf.write("\7n\2\2\u0199\u019a\7n\2\2\u019a\u019b\7k\2\2\u019b\u019c")
        buf.write("\7u\2\2\u019c\u019d\7g\2\2\u019d\u019e\7e\2\2\u019e\u019f")
        buf.write("\7q\2\2\u019f\u01a0\7p\2\2\u01a0\u01a1\7f\2\2\u01a1\u01a2")
        buf.write("\7u\2\2\u01a2l\3\2\2\2\u01a3\u01a4\7-\2\2\u01a4n\3\2\2")
        buf.write("\2\u01a5\u01a6\7?\2\2\u01a6p\3\2\2\2\u01a7\u01a8\7)\2")
        buf.write("\2\u01a8\u01a9\7u\2\2\u01a9r\3\2\2\2\u01aa\u01ab\7\61")
        buf.write("\2\2\u01abt\3\2\2\2\u01ac\u01ad\7<\2\2\u01adv\3\2\2\2")
        buf.write("\u01ae\u01af\7,\2\2\u01afx\3\2\2\2\u01b0\u01b1\7q\2\2")
        buf.write("\u01b1\u01b2\7h\2\2\u01b2\u01b3\7h\2\2\u01b3z\3\2\2\2")
        buf.write("\u01b4\u01b5\7q\2\2\u01b5\u01b6\7p\2\2\u01b6|\3\2\2\2")
        buf.write("\u01b7\u01b8\7/\2\2\u01b8~\3\2\2\2\u01b9\u01ba\7=\2\2")
        buf.write("\u01ba\u0080\3\2\2\2\u01bb\u01bc\7v\2\2\u01bc\u01bd\7")
        buf.write("q\2\2\u01bd\u01be\7i\2\2\u01be\u01bf\7i\2\2\u01bf\u01c0")
        buf.write("\7n\2\2\u01c0\u01c1\7g\2\2\u01c1\u0082\3\2\2\2\u01c2\u01c3")
        buf.write("\t\2\2\2\u01c3\u0084\3\2\2\2\u01c4\u01c5\t\3\2\2\u01c5")
        buf.write("\u0086\3\2\2\2\u01c6\u01c9\5\u0083B\2\u01c7\u01c9\5\u0085")
        buf.write("C\2\u01c8\u01c6\3\2\2\2\u01c8\u01c7\3\2\2\2\u01c9\u0088")
        buf.write("\3\2\2\2\u01ca\u01cd\5\u0087D\2\u01cb\u01cd\7a\2\2\u01cc")
        buf.write("\u01ca\3\2\2\2\u01cc\u01cb\3\2\2\2\u01cd\u008a\3\2\2\2")
        buf.write("\u01ce\u01d2\5\u0083B\2\u01cf\u01d0\7a\2\2\u01d0\u01d2")
        buf.write("\5\u0089E\2\u01d1\u01ce\3\2\2\2\u01d1\u01cf\3\2\2\2\u01d2")
        buf.write("\u01d6\3\2\2\2\u01d3\u01d5\5\u0089E\2\u01d4\u01d3\3\2")
        buf.write("\2\2\u01d5\u01d8\3\2\2\2\u01d6\u01d4\3\2\2\2\u01d6\u01d7")
        buf.write("\3\2\2\2\u01d7\u01da\3\2\2\2\u01d8\u01d6\3\2\2\2\u01d9")
        buf.write("\u01db\7A\2\2\u01da\u01d9\3\2\2\2\u01da\u01db\3\2\2\2")
        buf.write("\u01db\u008c\3\2\2\2\u01dc\u01de\5\u0085C\2\u01dd\u01dc")
        buf.write("\3\2\2\2\u01de\u01df\3\2\2\2\u01df\u01dd\3\2\2\2\u01df")
        buf.write("\u01e0\3\2\2\2\u01e0\u01e9\3\2\2\2\u01e1\u01e3\7a\2\2")
        buf.write("\u01e2\u01e4\5\u0085C\2\u01e3\u01e2\3\2\2\2\u01e4\u01e5")
        buf.write("\3\2\2\2\u01e5\u01e3\3\2\2\2\u01e5\u01e6\3\2\2\2\u01e6")
        buf.write("\u01e8\3\2\2\2\u01e7\u01e1\3\2\2\2\u01e8\u01eb\3\2\2\2")
        buf.write("\u01e9\u01e7\3\2\2\2\u01e9\u01ea\3\2\2\2\u01ea\u008e\3")
        buf.write("\2\2\2\u01eb\u01e9\3\2\2\2\u01ec\u01ee\t\4\2\2\u01ed\u01ef")
        buf.write("\7/\2\2\u01ee\u01ed\3\2\2\2\u01ee\u01ef\3\2\2\2\u01ef")
        buf.write("\u01f0\3\2\2\2\u01f0\u01f1\5\u008dG\2\u01f1\u0090\3\2")
        buf.write("\2\2\u01f2\u01f3\5\u008dG\2\u01f3\u01f4\7\60\2\2\u01f4")
        buf.write("\u01f6\5\u008dG\2\u01f5\u01f7\5\u008fH\2\u01f6\u01f5\3")
        buf.write("\2\2\2\u01f6\u01f7\3\2\2\2\u01f7\u01fc\3\2\2\2\u01f8\u01f9")
        buf.write("\5\u008dG\2\u01f9\u01fa\5\u008fH\2\u01fa\u01fc\3\2\2\2")
        buf.write("\u01fb\u01f2\3\2\2\2\u01fb\u01f8\3\2\2\2\u01fc\u0092\3")
        buf.write("\2\2\2\u01fd\u0200\n\5\2\2\u01fe\u0200\5\u0097L\2\u01ff")
        buf.write("\u01fd\3\2\2\2\u01ff\u01fe\3\2\2\2\u0200\u0094\3\2\2\2")
        buf.write("\u0201\u0202\t\6\2\2\u0202\u0096\3\2\2\2\u0203\u0204\7")
        buf.write("^\2\2\u0204\u020d\t\7\2\2\u0205\u0206\7^\2\2\u0206\u0207")
        buf.write("\7w\2\2\u0207\u0208\5\u0095K\2\u0208\u0209\5\u0095K\2")
        buf.write("\u0209\u020a\5\u0095K\2\u020a\u020b\5\u0095K\2\u020b\u020d")
        buf.write("\3\2\2\2\u020c\u0203\3\2\2\2\u020c\u0205\3\2\2\2\u020d")
        buf.write("\u0098\3\2\2\2\u020e\u0212\7$\2\2\u020f\u0211\5\u0093")
        buf.write("J\2\u0210\u020f\3\2\2\2\u0211\u0214\3\2\2\2\u0212\u0210")
        buf.write("\3\2\2\2\u0212\u0213\3\2\2\2\u0213\u0215\3\2\2\2\u0214")
        buf.write("\u0212\3\2\2\2\u0215\u0216\7$\2\2\u0216\u009a\3\2\2\2")
        buf.write("\u0217\u0218\7\61\2\2\u0218\u0219\7\61\2\2\u0219\u021d")
        buf.write("\3\2\2\2\u021a\u021c\13\2\2\2\u021b\u021a\3\2\2\2\u021c")
        buf.write("\u021f\3\2\2\2\u021d\u021e\3\2\2\2\u021d\u021b\3\2\2\2")
        buf.write("\u021e\u0221\3\2\2\2\u021f\u021d\3\2\2\2\u0220\u0222\7")
        buf.write("\17\2\2\u0221\u0220\3\2\2\2\u0221\u0222\3\2\2\2\u0222")
        buf.write("\u0223\3\2\2\2\u0223\u0224\7\f\2\2\u0224\u0225\3\2\2\2")
        buf.write("\u0225\u0226\bN\2\2\u0226\u009c\3\2\2\2\u0227\u0228\7")
        buf.write("\61\2\2\u0228\u0229\7,\2\2\u0229\u022d\3\2\2\2\u022a\u022c")
        buf.write("\13\2\2\2\u022b\u022a\3\2\2\2\u022c\u022f\3\2\2\2\u022d")
        buf.write("\u022e\3\2\2\2\u022d\u022b\3\2\2\2\u022e\u0230\3\2\2\2")
        buf.write("\u022f\u022d\3\2\2\2\u0230\u0231\7,\2\2\u0231\u0232\7")
        buf.write("\61\2\2\u0232\u0233\3\2\2\2\u0233\u0234\bO\2\2\u0234\u009e")
        buf.write("\3\2\2\2\u0235\u0236\t\b\2\2\u0236\u0237\3\2\2\2\u0237")
        buf.write("\u0238\bP\2\2\u0238\u00a0\3\2\2\2\24\2\u01c8\u01cc\u01d1")
        buf.write("\u01d6\u01da\u01df\u01e5\u01e9\u01ee\u01f6\u01fb\u01ff")
        buf.write("\u020c\u0212\u021d\u0221\u022d\3\b\2\2")
        return buf.getvalue()


class DMFLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    T__18 = 19
    T__19 = 20
    T__20 = 21
    T__21 = 22
    T__22 = 23
    T__23 = 24
    T__24 = 25
    T__25 = 26
    T__26 = 27
    T__27 = 28
    T__28 = 29
    T__29 = 30
    T__30 = 31
    T__31 = 32
    T__32 = 33
    T__33 = 34
    T__34 = 35
    T__35 = 36
    T__36 = 37
    T__37 = 38
    T__38 = 39
    T__39 = 40
    T__40 = 41
    T__41 = 42
    T__42 = 43
    T__43 = 44
    T__44 = 45
    T__45 = 46
    T__46 = 47
    T__47 = 48
    T__48 = 49
    T__49 = 50
    T__50 = 51
    T__51 = 52
    T__52 = 53
    ADD = 54
    ASSIGN = 55
    ATTR = 56
    DIV = 57
    INJECT = 58
    MUL = 59
    OFF = 60
    ON = 61
    SUB = 62
    TERMINATOR = 63
    TOGGLE = 64
    ID = 65
    INT = 66
    FLOAT = 67
    STRING = 68
    EOL_COMMENT = 69
    COMMENT = 70
    WS = 71

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'pause'", "'{'", "'}'", "'[['", "']]'", "'('", "')'", "','", 
            "'tick'", "'ticks'", "'to'", "'well'", "'#'", "'['", "']'", 
            "'gate'", "'exit'", "'pad'", "'drop'", "'@'", "'at'", "'turn'", 
            "'state'", "'the'", "'up'", "'north'", "'down'", "'south'", 
            "'left'", "'west'", "'right'", "'east'", "'row'", "'rows'", 
            "'col'", "'column'", "'cols'", "'columns'", "'macro'", "'int'", 
            "'component'", "'delta'", "'motion'", "'delay'", "'time'", "'s'", 
            "'sec'", "'secs'", "'second'", "'seconds'", "'ms'", "'millisecond'", 
            "'milliseconds'", "'+'", "'='", "''s'", "'/'", "':'", "'*'", 
            "'off'", "'on'", "'-'", "';'", "'toggle'" ]

    symbolicNames = [ "<INVALID>",
            "ADD", "ASSIGN", "ATTR", "DIV", "INJECT", "MUL", "OFF", "ON", 
            "SUB", "TERMINATOR", "TOGGLE", "ID", "INT", "FLOAT", "STRING", 
            "EOL_COMMENT", "COMMENT", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "T__20", "T__21", "T__22", "T__23", "T__24", "T__25", 
                  "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", 
                  "T__32", "T__33", "T__34", "T__35", "T__36", "T__37", 
                  "T__38", "T__39", "T__40", "T__41", "T__42", "T__43", 
                  "T__44", "T__45", "T__46", "T__47", "T__48", "T__49", 
                  "T__50", "T__51", "T__52", "ADD", "ASSIGN", "ATTR", "DIV", 
                  "INJECT", "MUL", "OFF", "ON", "SUB", "TERMINATOR", "TOGGLE", 
                  "ALPHA", "DIGIT", "ALNUM", "IDCHAR", "ID", "INT", "EXPT", 
                  "FLOAT", "STRING_CHAR", "HEX", "ESC_SEQ", "STRING", "EOL_COMMENT", 
                  "COMMENT", "WS" ]

    grammarFileName = "DMF.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


