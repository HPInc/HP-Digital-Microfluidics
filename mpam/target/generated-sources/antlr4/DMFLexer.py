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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2E")
        buf.write("\u0216\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("L\3\2\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\5")
        buf.write("\3\6\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\n\3\n\3")
        buf.write("\n\3\13\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3")
        buf.write("\r\3\r\3\r\3\16\3\16\3\17\3\17\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\21\3\21\3\22\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\25\3\25\3\26\3\26\3\26\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30\3\30\3\31")
        buf.write("\3\31\3\31\3\31\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\33")
        buf.write("\3\33\3\34\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35")
        buf.write("\3\35\3\36\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37")
        buf.write("\3 \3 \3 \3 \3 \3 \3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3#\3")
        buf.write("#\3#\3#\3#\3$\3$\3$\3$\3%\3%\3%\3%\3%\3%\3%\3&\3&\3&\3")
        buf.write("&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\3(\3(\3")
        buf.write("(\3)\3)\3)\3)\3*\3*\3+\3+\3+\3+\3,\3,\3,\3,\3,\3-\3-\3")
        buf.write("-\3-\3-\3-\3-\3.\3.\3.\3.\3.\3.\3.\3.\3/\3/\3/\3\60\3")
        buf.write("\60\3\60\3\60\3\60\3\60\3\60\3\60\3\60\3\60\3\60\3\60")
        buf.write("\3\61\3\61\3\61\3\61\3\61\3\61\3\61\3\61\3\61\3\61\3\61")
        buf.write("\3\61\3\61\3\62\3\62\3\62\3\62\3\62\3\62\3\62\3\63\3\63")
        buf.write("\3\64\3\64\3\65\3\65\3\65\3\66\3\66\3\67\3\67\38\38\3")
        buf.write("9\39\39\39\3:\3:\3:\3;\3;\3<\3<\3=\3=\3=\3=\3=\3=\3=\3")
        buf.write(">\3>\3?\3?\3@\3@\5@\u01a6\n@\3A\3A\5A\u01aa\nA\3B\3B\3")
        buf.write("B\5B\u01af\nB\3B\7B\u01b2\nB\fB\16B\u01b5\13B\3B\5B\u01b8")
        buf.write("\nB\3C\6C\u01bb\nC\rC\16C\u01bc\3C\3C\6C\u01c1\nC\rC\16")
        buf.write("C\u01c2\7C\u01c5\nC\fC\16C\u01c8\13C\3D\3D\5D\u01cc\n")
        buf.write("D\3D\3D\3E\3E\3E\3E\5E\u01d4\nE\3E\3E\3E\5E\u01d9\nE\3")
        buf.write("F\3F\5F\u01dd\nF\3G\3G\3H\3H\3H\3H\3H\3H\3H\3H\3H\5H\u01ea")
        buf.write("\nH\3I\3I\7I\u01ee\nI\fI\16I\u01f1\13I\3I\3I\3J\3J\3J")
        buf.write("\3J\7J\u01f9\nJ\fJ\16J\u01fc\13J\3J\5J\u01ff\nJ\3J\3J")
        buf.write("\3J\3J\3K\3K\3K\3K\7K\u0209\nK\fK\16K\u020c\13K\3K\3K")
        buf.write("\3K\3K\3K\3L\3L\3L\3L\4\u01fa\u020a\2M\3\3\5\4\7\5\t\6")
        buf.write("\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20")
        buf.write("\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65")
        buf.write("\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60")
        buf.write("_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w=y>{\2}\2\177\2")
        buf.write("\u0081\2\u0083?\u0085@\u0087\2\u0089A\u008b\2\u008d\2")
        buf.write("\u008f\2\u0091B\u0093C\u0095D\u0097E\3\2\t\4\2C\\c|\3")
        buf.write("\2\62;\4\2GGgg\6\2\f\f\17\17$$^^\5\2\62;CHch\b\2$$))^")
        buf.write("^ppttvv\5\2\13\f\17\17\"\"\2\u021e\2\3\3\2\2\2\2\5\3\2")
        buf.write("\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2")
        buf.write("\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2")
        buf.write("\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37")
        buf.write("\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2")
        buf.write("\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2")
        buf.write("\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2")
        buf.write("\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2")
        buf.write("\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2")
        buf.write("\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3")
        buf.write("\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a")
        buf.write("\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2")
        buf.write("k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2")
        buf.write("\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2\u0083\3\2\2\2\2\u0085")
        buf.write("\3\2\2\2\2\u0089\3\2\2\2\2\u0091\3\2\2\2\2\u0093\3\2\2")
        buf.write("\2\2\u0095\3\2\2\2\2\u0097\3\2\2\2\3\u0099\3\2\2\2\5\u009f")
        buf.write("\3\2\2\2\7\u00a1\3\2\2\2\t\u00a3\3\2\2\2\13\u00a6\3\2")
        buf.write("\2\2\r\u00a9\3\2\2\2\17\u00ab\3\2\2\2\21\u00ad\3\2\2\2")
        buf.write("\23\u00af\3\2\2\2\25\u00b4\3\2\2\2\27\u00ba\3\2\2\2\31")
        buf.write("\u00bd\3\2\2\2\33\u00c2\3\2\2\2\35\u00c4\3\2\2\2\37\u00c6")
        buf.write("\3\2\2\2!\u00c8\3\2\2\2#\u00cd\3\2\2\2%\u00d2\3\2\2\2")
        buf.write("\'\u00d6\3\2\2\2)\u00db\3\2\2\2+\u00dd\3\2\2\2-\u00e0")
        buf.write("\3\2\2\2/\u00e5\3\2\2\2\61\u00eb\3\2\2\2\63\u00ef\3\2")
        buf.write("\2\2\65\u00f2\3\2\2\2\67\u00f8\3\2\2\29\u00fd\3\2\2\2")
        buf.write(";\u0103\3\2\2\2=\u0108\3\2\2\2?\u010d\3\2\2\2A\u0113\3")
        buf.write("\2\2\2C\u0118\3\2\2\2E\u011c\3\2\2\2G\u0121\3\2\2\2I\u0125")
        buf.write("\3\2\2\2K\u012c\3\2\2\2M\u0131\3\2\2\2O\u0139\3\2\2\2")
        buf.write("Q\u013f\3\2\2\2S\u0143\3\2\2\2U\u0145\3\2\2\2W\u0149\3")
        buf.write("\2\2\2Y\u014e\3\2\2\2[\u0155\3\2\2\2]\u015d\3\2\2\2_\u0160")
        buf.write("\3\2\2\2a\u016c\3\2\2\2c\u0179\3\2\2\2e\u0180\3\2\2\2")
        buf.write("g\u0182\3\2\2\2i\u0184\3\2\2\2k\u0187\3\2\2\2m\u0189\3")
        buf.write("\2\2\2o\u018b\3\2\2\2q\u018d\3\2\2\2s\u0191\3\2\2\2u\u0194")
        buf.write("\3\2\2\2w\u0196\3\2\2\2y\u0198\3\2\2\2{\u019f\3\2\2\2")
        buf.write("}\u01a1\3\2\2\2\177\u01a5\3\2\2\2\u0081\u01a9\3\2\2\2")
        buf.write("\u0083\u01ae\3\2\2\2\u0085\u01ba\3\2\2\2\u0087\u01c9\3")
        buf.write("\2\2\2\u0089\u01d8\3\2\2\2\u008b\u01dc\3\2\2\2\u008d\u01de")
        buf.write("\3\2\2\2\u008f\u01e9\3\2\2\2\u0091\u01eb\3\2\2\2\u0093")
        buf.write("\u01f4\3\2\2\2\u0095\u0204\3\2\2\2\u0097\u0212\3\2\2\2")
        buf.write("\u0099\u009a\7r\2\2\u009a\u009b\7c\2\2\u009b\u009c\7w")
        buf.write("\2\2\u009c\u009d\7u\2\2\u009d\u009e\7g\2\2\u009e\4\3\2")
        buf.write("\2\2\u009f\u00a0\7}\2\2\u00a0\6\3\2\2\2\u00a1\u00a2\7")
        buf.write("\177\2\2\u00a2\b\3\2\2\2\u00a3\u00a4\7]\2\2\u00a4\u00a5")
        buf.write("\7]\2\2\u00a5\n\3\2\2\2\u00a6\u00a7\7_\2\2\u00a7\u00a8")
        buf.write("\7_\2\2\u00a8\f\3\2\2\2\u00a9\u00aa\7*\2\2\u00aa\16\3")
        buf.write("\2\2\2\u00ab\u00ac\7+\2\2\u00ac\20\3\2\2\2\u00ad\u00ae")
        buf.write("\7.\2\2\u00ae\22\3\2\2\2\u00af\u00b0\7v\2\2\u00b0\u00b1")
        buf.write("\7k\2\2\u00b1\u00b2\7e\2\2\u00b2\u00b3\7m\2\2\u00b3\24")
        buf.write("\3\2\2\2\u00b4\u00b5\7v\2\2\u00b5\u00b6\7k\2\2\u00b6\u00b7")
        buf.write("\7e\2\2\u00b7\u00b8\7m\2\2\u00b8\u00b9\7u\2\2\u00b9\26")
        buf.write("\3\2\2\2\u00ba\u00bb\7v\2\2\u00bb\u00bc\7q\2\2\u00bc\30")
        buf.write("\3\2\2\2\u00bd\u00be\7y\2\2\u00be\u00bf\7g\2\2\u00bf\u00c0")
        buf.write("\7n\2\2\u00c0\u00c1\7n\2\2\u00c1\32\3\2\2\2\u00c2\u00c3")
        buf.write("\7%\2\2\u00c3\34\3\2\2\2\u00c4\u00c5\7]\2\2\u00c5\36\3")
        buf.write("\2\2\2\u00c6\u00c7\7_\2\2\u00c7 \3\2\2\2\u00c8\u00c9\7")
        buf.write("i\2\2\u00c9\u00ca\7c\2\2\u00ca\u00cb\7v\2\2\u00cb\u00cc")
        buf.write("\7g\2\2\u00cc\"\3\2\2\2\u00cd\u00ce\7g\2\2\u00ce\u00cf")
        buf.write("\7z\2\2\u00cf\u00d0\7k\2\2\u00d0\u00d1\7v\2\2\u00d1$\3")
        buf.write("\2\2\2\u00d2\u00d3\7r\2\2\u00d3\u00d4\7c\2\2\u00d4\u00d5")
        buf.write("\7f\2\2\u00d5&\3\2\2\2\u00d6\u00d7\7f\2\2\u00d7\u00d8")
        buf.write("\7t\2\2\u00d8\u00d9\7q\2\2\u00d9\u00da\7r\2\2\u00da(\3")
        buf.write("\2\2\2\u00db\u00dc\7B\2\2\u00dc*\3\2\2\2\u00dd\u00de\7")
        buf.write("c\2\2\u00de\u00df\7v\2\2\u00df,\3\2\2\2\u00e0\u00e1\7")
        buf.write("v\2\2\u00e1\u00e2\7w\2\2\u00e2\u00e3\7t\2\2\u00e3\u00e4")
        buf.write("\7p\2\2\u00e4.\3\2\2\2\u00e5\u00e6\7u\2\2\u00e6\u00e7")
        buf.write("\7v\2\2\u00e7\u00e8\7c\2\2\u00e8\u00e9\7v\2\2\u00e9\u00ea")
        buf.write("\7g\2\2\u00ea\60\3\2\2\2\u00eb\u00ec\7v\2\2\u00ec\u00ed")
        buf.write("\7j\2\2\u00ed\u00ee\7g\2\2\u00ee\62\3\2\2\2\u00ef\u00f0")
        buf.write("\7w\2\2\u00f0\u00f1\7r\2\2\u00f1\64\3\2\2\2\u00f2\u00f3")
        buf.write("\7p\2\2\u00f3\u00f4\7q\2\2\u00f4\u00f5\7t\2\2\u00f5\u00f6")
        buf.write("\7v\2\2\u00f6\u00f7\7j\2\2\u00f7\66\3\2\2\2\u00f8\u00f9")
        buf.write("\7f\2\2\u00f9\u00fa\7q\2\2\u00fa\u00fb\7y\2\2\u00fb\u00fc")
        buf.write("\7p\2\2\u00fc8\3\2\2\2\u00fd\u00fe\7u\2\2\u00fe\u00ff")
        buf.write("\7q\2\2\u00ff\u0100\7w\2\2\u0100\u0101\7v\2\2\u0101\u0102")
        buf.write("\7j\2\2\u0102:\3\2\2\2\u0103\u0104\7n\2\2\u0104\u0105")
        buf.write("\7g\2\2\u0105\u0106\7h\2\2\u0106\u0107\7v\2\2\u0107<\3")
        buf.write("\2\2\2\u0108\u0109\7y\2\2\u0109\u010a\7g\2\2\u010a\u010b")
        buf.write("\7u\2\2\u010b\u010c\7v\2\2\u010c>\3\2\2\2\u010d\u010e")
        buf.write("\7t\2\2\u010e\u010f\7k\2\2\u010f\u0110\7i\2\2\u0110\u0111")
        buf.write("\7j\2\2\u0111\u0112\7v\2\2\u0112@\3\2\2\2\u0113\u0114")
        buf.write("\7g\2\2\u0114\u0115\7c\2\2\u0115\u0116\7u\2\2\u0116\u0117")
        buf.write("\7v\2\2\u0117B\3\2\2\2\u0118\u0119\7t\2\2\u0119\u011a")
        buf.write("\7q\2\2\u011a\u011b\7y\2\2\u011bD\3\2\2\2\u011c\u011d")
        buf.write("\7t\2\2\u011d\u011e\7q\2\2\u011e\u011f\7y\2\2\u011f\u0120")
        buf.write("\7u\2\2\u0120F\3\2\2\2\u0121\u0122\7e\2\2\u0122\u0123")
        buf.write("\7q\2\2\u0123\u0124\7n\2\2\u0124H\3\2\2\2\u0125\u0126")
        buf.write("\7e\2\2\u0126\u0127\7q\2\2\u0127\u0128\7n\2\2\u0128\u0129")
        buf.write("\7w\2\2\u0129\u012a\7o\2\2\u012a\u012b\7p\2\2\u012bJ\3")
        buf.write("\2\2\2\u012c\u012d\7e\2\2\u012d\u012e\7q\2\2\u012e\u012f")
        buf.write("\7n\2\2\u012f\u0130\7u\2\2\u0130L\3\2\2\2\u0131\u0132")
        buf.write("\7e\2\2\u0132\u0133\7q\2\2\u0133\u0134\7n\2\2\u0134\u0135")
        buf.write("\7w\2\2\u0135\u0136\7o\2\2\u0136\u0137\7p\2\2\u0137\u0138")
        buf.write("\7u\2\2\u0138N\3\2\2\2\u0139\u013a\7o\2\2\u013a\u013b")
        buf.write("\7c\2\2\u013b\u013c\7e\2\2\u013c\u013d\7t\2\2\u013d\u013e")
        buf.write("\7q\2\2\u013eP\3\2\2\2\u013f\u0140\7k\2\2\u0140\u0141")
        buf.write("\7p\2\2\u0141\u0142\7v\2\2\u0142R\3\2\2\2\u0143\u0144")
        buf.write("\7u\2\2\u0144T\3\2\2\2\u0145\u0146\7u\2\2\u0146\u0147")
        buf.write("\7g\2\2\u0147\u0148\7e\2\2\u0148V\3\2\2\2\u0149\u014a")
        buf.write("\7u\2\2\u014a\u014b\7g\2\2\u014b\u014c\7e\2\2\u014c\u014d")
        buf.write("\7u\2\2\u014dX\3\2\2\2\u014e\u014f\7u\2\2\u014f\u0150")
        buf.write("\7g\2\2\u0150\u0151\7e\2\2\u0151\u0152\7q\2\2\u0152\u0153")
        buf.write("\7p\2\2\u0153\u0154\7f\2\2\u0154Z\3\2\2\2\u0155\u0156")
        buf.write("\7u\2\2\u0156\u0157\7g\2\2\u0157\u0158\7e\2\2\u0158\u0159")
        buf.write("\7q\2\2\u0159\u015a\7p\2\2\u015a\u015b\7f\2\2\u015b\u015c")
        buf.write("\7u\2\2\u015c\\\3\2\2\2\u015d\u015e\7o\2\2\u015e\u015f")
        buf.write("\7u\2\2\u015f^\3\2\2\2\u0160\u0161\7o\2\2\u0161\u0162")
        buf.write("\7k\2\2\u0162\u0163\7n\2\2\u0163\u0164\7n\2\2\u0164\u0165")
        buf.write("\7k\2\2\u0165\u0166\7u\2\2\u0166\u0167\7g\2\2\u0167\u0168")
        buf.write("\7e\2\2\u0168\u0169\7q\2\2\u0169\u016a\7p\2\2\u016a\u016b")
        buf.write("\7f\2\2\u016b`\3\2\2\2\u016c\u016d\7o\2\2\u016d\u016e")
        buf.write("\7k\2\2\u016e\u016f\7n\2\2\u016f\u0170\7n\2\2\u0170\u0171")
        buf.write("\7k\2\2\u0171\u0172\7u\2\2\u0172\u0173\7g\2\2\u0173\u0174")
        buf.write("\7e\2\2\u0174\u0175\7q\2\2\u0175\u0176\7p\2\2\u0176\u0177")
        buf.write("\7f\2\2\u0177\u0178\7u\2\2\u0178b\3\2\2\2\u0179\u017a")
        buf.write("\7,\2\2\u017a\u017b\7,\2\2\u017b\u017c\7a\2\2\u017c\u017d")
        buf.write("\7a\2\2\u017d\u017e\7,\2\2\u017e\u017f\7,\2\2\u017fd\3")
        buf.write("\2\2\2\u0180\u0181\7-\2\2\u0181f\3\2\2\2\u0182\u0183\7")
        buf.write("?\2\2\u0183h\3\2\2\2\u0184\u0185\7)\2\2\u0185\u0186\7")
        buf.write("u\2\2\u0186j\3\2\2\2\u0187\u0188\7\61\2\2\u0188l\3\2\2")
        buf.write("\2\u0189\u018a\7<\2\2\u018an\3\2\2\2\u018b\u018c\7,\2")
        buf.write("\2\u018cp\3\2\2\2\u018d\u018e\7q\2\2\u018e\u018f\7h\2")
        buf.write("\2\u018f\u0190\7h\2\2\u0190r\3\2\2\2\u0191\u0192\7q\2")
        buf.write("\2\u0192\u0193\7p\2\2\u0193t\3\2\2\2\u0194\u0195\7/\2")
        buf.write("\2\u0195v\3\2\2\2\u0196\u0197\7=\2\2\u0197x\3\2\2\2\u0198")
        buf.write("\u0199\7v\2\2\u0199\u019a\7q\2\2\u019a\u019b\7i\2\2\u019b")
        buf.write("\u019c\7i\2\2\u019c\u019d\7n\2\2\u019d\u019e\7g\2\2\u019e")
        buf.write("z\3\2\2\2\u019f\u01a0\t\2\2\2\u01a0|\3\2\2\2\u01a1\u01a2")
        buf.write("\t\3\2\2\u01a2~\3\2\2\2\u01a3\u01a6\5{>\2\u01a4\u01a6")
        buf.write("\5}?\2\u01a5\u01a3\3\2\2\2\u01a5\u01a4\3\2\2\2\u01a6\u0080")
        buf.write("\3\2\2\2\u01a7\u01aa\5\177@\2\u01a8\u01aa\7a\2\2\u01a9")
        buf.write("\u01a7\3\2\2\2\u01a9\u01a8\3\2\2\2\u01aa\u0082\3\2\2\2")
        buf.write("\u01ab\u01af\5{>\2\u01ac\u01ad\7a\2\2\u01ad\u01af\5\u0081")
        buf.write("A\2\u01ae\u01ab\3\2\2\2\u01ae\u01ac\3\2\2\2\u01af\u01b3")
        buf.write("\3\2\2\2\u01b0\u01b2\5\u0081A\2\u01b1\u01b0\3\2\2\2\u01b2")
        buf.write("\u01b5\3\2\2\2\u01b3\u01b1\3\2\2\2\u01b3\u01b4\3\2\2\2")
        buf.write("\u01b4\u01b7\3\2\2\2\u01b5\u01b3\3\2\2\2\u01b6\u01b8\7")
        buf.write("A\2\2\u01b7\u01b6\3\2\2\2\u01b7\u01b8\3\2\2\2\u01b8\u0084")
        buf.write("\3\2\2\2\u01b9\u01bb\5}?\2\u01ba\u01b9\3\2\2\2\u01bb\u01bc")
        buf.write("\3\2\2\2\u01bc\u01ba\3\2\2\2\u01bc\u01bd\3\2\2\2\u01bd")
        buf.write("\u01c6\3\2\2\2\u01be\u01c0\7a\2\2\u01bf\u01c1\5}?\2\u01c0")
        buf.write("\u01bf\3\2\2\2\u01c1\u01c2\3\2\2\2\u01c2\u01c0\3\2\2\2")
        buf.write("\u01c2\u01c3\3\2\2\2\u01c3\u01c5\3\2\2\2\u01c4\u01be\3")
        buf.write("\2\2\2\u01c5\u01c8\3\2\2\2\u01c6\u01c4\3\2\2\2\u01c6\u01c7")
        buf.write("\3\2\2\2\u01c7\u0086\3\2\2\2\u01c8\u01c6\3\2\2\2\u01c9")
        buf.write("\u01cb\t\4\2\2\u01ca\u01cc\7/\2\2\u01cb\u01ca\3\2\2\2")
        buf.write("\u01cb\u01cc\3\2\2\2\u01cc\u01cd\3\2\2\2\u01cd\u01ce\5")
        buf.write("\u0085C\2\u01ce\u0088\3\2\2\2\u01cf\u01d0\5\u0085C\2\u01d0")
        buf.write("\u01d1\7\60\2\2\u01d1\u01d3\5\u0085C\2\u01d2\u01d4\5\u0087")
        buf.write("D\2\u01d3\u01d2\3\2\2\2\u01d3\u01d4\3\2\2\2\u01d4\u01d9")
        buf.write("\3\2\2\2\u01d5\u01d6\5\u0085C\2\u01d6\u01d7\5\u0087D\2")
        buf.write("\u01d7\u01d9\3\2\2\2\u01d8\u01cf\3\2\2\2\u01d8\u01d5\3")
        buf.write("\2\2\2\u01d9\u008a\3\2\2\2\u01da\u01dd\n\5\2\2\u01db\u01dd")
        buf.write("\5\u008fH\2\u01dc\u01da\3\2\2\2\u01dc\u01db\3\2\2\2\u01dd")
        buf.write("\u008c\3\2\2\2\u01de\u01df\t\6\2\2\u01df\u008e\3\2\2\2")
        buf.write("\u01e0\u01e1\7^\2\2\u01e1\u01ea\t\7\2\2\u01e2\u01e3\7")
        buf.write("^\2\2\u01e3\u01e4\7w\2\2\u01e4\u01e5\5\u008dG\2\u01e5")
        buf.write("\u01e6\5\u008dG\2\u01e6\u01e7\5\u008dG\2\u01e7\u01e8\5")
        buf.write("\u008dG\2\u01e8\u01ea\3\2\2\2\u01e9\u01e0\3\2\2\2\u01e9")
        buf.write("\u01e2\3\2\2\2\u01ea\u0090\3\2\2\2\u01eb\u01ef\7$\2\2")
        buf.write("\u01ec\u01ee\5\u008bF\2\u01ed\u01ec\3\2\2\2\u01ee\u01f1")
        buf.write("\3\2\2\2\u01ef\u01ed\3\2\2\2\u01ef\u01f0\3\2\2\2\u01f0")
        buf.write("\u01f2\3\2\2\2\u01f1\u01ef\3\2\2\2\u01f2\u01f3\7$\2\2")
        buf.write("\u01f3\u0092\3\2\2\2\u01f4\u01f5\7\61\2\2\u01f5\u01f6")
        buf.write("\7\61\2\2\u01f6\u01fa\3\2\2\2\u01f7\u01f9\13\2\2\2\u01f8")
        buf.write("\u01f7\3\2\2\2\u01f9\u01fc\3\2\2\2\u01fa\u01fb\3\2\2\2")
        buf.write("\u01fa\u01f8\3\2\2\2\u01fb\u01fe\3\2\2\2\u01fc\u01fa\3")
        buf.write("\2\2\2\u01fd\u01ff\7\17\2\2\u01fe\u01fd\3\2\2\2\u01fe")
        buf.write("\u01ff\3\2\2\2\u01ff\u0200\3\2\2\2\u0200\u0201\7\f\2\2")
        buf.write("\u0201\u0202\3\2\2\2\u0202\u0203\bJ\2\2\u0203\u0094\3")
        buf.write("\2\2\2\u0204\u0205\7\61\2\2\u0205\u0206\7,\2\2\u0206\u020a")
        buf.write("\3\2\2\2\u0207\u0209\13\2\2\2\u0208\u0207\3\2\2\2\u0209")
        buf.write("\u020c\3\2\2\2\u020a\u020b\3\2\2\2\u020a\u0208\3\2\2\2")
        buf.write("\u020b\u020d\3\2\2\2\u020c\u020a\3\2\2\2\u020d\u020e\7")
        buf.write(",\2\2\u020e\u020f\7\61\2\2\u020f\u0210\3\2\2\2\u0210\u0211")
        buf.write("\bK\2\2\u0211\u0096\3\2\2\2\u0212\u0213\t\b\2\2\u0213")
        buf.write("\u0214\3\2\2\2\u0214\u0215\bL\2\2\u0215\u0098\3\2\2\2")
        buf.write("\24\2\u01a5\u01a9\u01ae\u01b3\u01b7\u01bc\u01c2\u01c6")
        buf.write("\u01cb\u01d3\u01d8\u01dc\u01e9\u01ef\u01fa\u01fe\u020a")
        buf.write("\3\b\2\2")
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
    ADD = 50
    ASSIGN = 51
    ATTR = 52
    DIV = 53
    INJECT = 54
    MUL = 55
    OFF = 56
    ON = 57
    SUB = 58
    TERMINATOR = 59
    TOGGLE = 60
    ID = 61
    INT = 62
    FLOAT = 63
    STRING = 64
    EOL_COMMENT = 65
    COMMENT = 66
    WS = 67

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'pause'", "'{'", "'}'", "'[['", "']]'", "'('", "')'", "','", 
            "'tick'", "'ticks'", "'to'", "'well'", "'#'", "'['", "']'", 
            "'gate'", "'exit'", "'pad'", "'drop'", "'@'", "'at'", "'turn'", 
            "'state'", "'the'", "'up'", "'north'", "'down'", "'south'", 
            "'left'", "'west'", "'right'", "'east'", "'row'", "'rows'", 
            "'col'", "'column'", "'cols'", "'columns'", "'macro'", "'int'", 
            "'s'", "'sec'", "'secs'", "'second'", "'seconds'", "'ms'", "'millisecond'", 
            "'milliseconds'", "'**__**'", "'+'", "'='", "''s'", "'/'", "':'", 
            "'*'", "'off'", "'on'", "'-'", "';'", "'toggle'" ]

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
                  "T__44", "T__45", "T__46", "T__47", "T__48", "ADD", "ASSIGN", 
                  "ATTR", "DIV", "INJECT", "MUL", "OFF", "ON", "SUB", "TERMINATOR", 
                  "TOGGLE", "ALPHA", "DIGIT", "ALNUM", "IDCHAR", "ID", "INT", 
                  "EXPT", "FLOAT", "STRING_CHAR", "HEX", "ESC_SEQ", "STRING", 
                  "EOL_COMMENT", "COMMENT", "WS" ]

    grammarFileName = "DMF.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


