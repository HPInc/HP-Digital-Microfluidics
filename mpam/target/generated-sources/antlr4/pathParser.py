# Generated from path.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


from mpam.types import Dir 


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3*")
        buf.write("\u008f\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2%\n\2\3\2\3\2\3")
        buf.write("\2\5\2*\n\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\7\2\64\n\2")
        buf.write("\f\2\16\2\67\13\2\3\2\3\2\3\2\3\2\5\2=\n\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2K\n\2\3\2\3\2")
        buf.write("\3\2\5\2P\n\2\3\2\3\2\3\2\3\2\3\2\6\2W\n\2\r\2\16\2X\7")
        buf.write("\2[\n\2\f\2\16\2^\13\2\3\3\3\3\3\3\3\3\3\3\3\3\5\3f\n")
        buf.write("\3\3\4\3\4\3\4\5\4k\n\4\3\5\3\5\3\5\3\5\3\5\3\5\5\5s\n")
        buf.write("\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6}\n\6\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\7\3\7\5\7\u0087\n\7\3\b\3\b\5\b\u008b")
        buf.write("\n\b\3\t\3\t\3\t\2\3\2\n\2\4\6\b\n\f\16\20\2\5\3\2\7\b")
        buf.write("\4\2\27\27\31\31\4\2\25\25\32\32\2\u00a9\2<\3\2\2\2\4")
        buf.write("e\3\2\2\2\6j\3\2\2\2\br\3\2\2\2\n|\3\2\2\2\f\u0086\3\2")
        buf.write("\2\2\16\u008a\3\2\2\2\20\u008c\3\2\2\2\22\23\b\2\1\2\23")
        buf.write("\24\7\3\2\2\24\25\5\2\2\2\25\26\7\4\2\2\26=\3\2\2\2\27")
        buf.write("\30\7\3\2\2\30\31\5\2\2\2\31\32\7\5\2\2\32\33\5\2\2\2")
        buf.write("\33\34\7\4\2\2\34=\3\2\2\2\35\36\7\6\2\2\36\37\t\2\2\2")
        buf.write("\37=\5\2\2\16 !\7%\2\2!$\6\2\2\3\"%\5\4\3\2#%\5\b\5\2")
        buf.write("$\"\3\2\2\2$#\3\2\2\2$%\3\2\2\2%&\3\2\2\2&)\5\n\6\2\'")
        buf.write("(\7\t\2\2(*\5\2\2\2)\'\3\2\2\2)*\3\2\2\2*=\3\2\2\2+,\7")
        buf.write("%\2\2,-\6\2\3\3-=\5\4\3\2./\5\16\b\2/\60\7\3\2\2\60\65")
        buf.write("\5\2\2\2\61\62\7\5\2\2\62\64\5\2\2\2\63\61\3\2\2\2\64")
        buf.write("\67\3\2\2\2\65\63\3\2\2\2\65\66\3\2\2\2\668\3\2\2\2\67")
        buf.write("\65\3\2\2\289\7\4\2\29=\3\2\2\2:=\5\16\b\2;=\7%\2\2<\22")
        buf.write("\3\2\2\2<\27\3\2\2\2<\35\3\2\2\2< \3\2\2\2<+\3\2\2\2<")
        buf.write(".\3\2\2\2<:\3\2\2\2<;\3\2\2\2=\\\3\2\2\2>?\f\b\2\2?@\t")
        buf.write("\3\2\2@[\5\2\2\tAB\f\7\2\2BC\t\4\2\2C[\5\2\2\bDE\f\6\2")
        buf.write("\2EF\7\30\2\2F[\5\2\2\7GJ\f\r\2\2HK\5\4\3\2IK\5\b\5\2")
        buf.write("JH\3\2\2\2JI\3\2\2\2JK\3\2\2\2KL\3\2\2\2LO\5\n\6\2MN\7")
        buf.write("\t\2\2NP\5\2\2\2OM\3\2\2\2OP\3\2\2\2P[\3\2\2\2QR\f\f\2")
        buf.write("\2R[\5\4\3\2ST\f\t\2\2TV\7\26\2\2UW\5\16\b\2VU\3\2\2\2")
        buf.write("WX\3\2\2\2XV\3\2\2\2XY\3\2\2\2Y[\3\2\2\2Z>\3\2\2\2ZA\3")
        buf.write("\2\2\2ZD\3\2\2\2ZG\3\2\2\2ZQ\3\2\2\2ZS\3\2\2\2[^\3\2\2")
        buf.write("\2\\Z\3\2\2\2\\]\3\2\2\2]\3\3\2\2\2^\\\3\2\2\2_f\7\n\2")
        buf.write("\2`f\7\13\2\2ab\6\3\n\3bf\7\f\2\2cd\6\3\13\3df\7\r\2\2")
        buf.write("e_\3\2\2\2e`\3\2\2\2ea\3\2\2\2ec\3\2\2\2f\5\3\2\2\2gk")
        buf.write("\7\16\2\2hi\6\4\f\3ik\7\17\2\2jg\3\2\2\2jh\3\2\2\2k\7")
        buf.write("\3\2\2\2ls\7\20\2\2ms\7\21\2\2no\6\5\r\3os\7\22\2\2pq")
        buf.write("\6\5\16\3qs\7\23\2\2rl\3\2\2\2rm\3\2\2\2rn\3\2\2\2rp\3")
        buf.write("\2\2\2s\t\3\2\2\2tu\7\33\2\2u}\b\6\1\2vw\7\34\2\2w}\b")
        buf.write("\6\1\2xy\7\35\2\2y}\b\6\1\2z{\7\36\2\2{}\b\6\1\2|t\3\2")
        buf.write("\2\2|v\3\2\2\2|x\3\2\2\2|z\3\2\2\2}\13\3\2\2\2~\177\7")
        buf.write("\37\2\2\177\u0087\b\7\1\2\u0080\u0081\7 \2\2\u0081\u0087")
        buf.write("\b\7\1\2\u0082\u0083\7!\2\2\u0083\u0087\b\7\1\2\u0084")
        buf.write("\u0085\7\"\2\2\u0085\u0087\b\7\1\2\u0086~\3\2\2\2\u0086")
        buf.write("\u0080\3\2\2\2\u0086\u0082\3\2\2\2\u0086\u0084\3\2\2\2")
        buf.write("\u0087\r\3\2\2\2\u0088\u008b\7$\2\2\u0089\u008b\5\20\t")
        buf.write("\2\u008a\u0088\3\2\2\2\u008a\u0089\3\2\2\2\u008b\17\3")
        buf.write("\2\2\2\u008c\u008d\7\24\2\2\u008d\21\3\2\2\2\21$)\65<")
        buf.write("JOXZ\\ejr|\u0086\u008a")
        return buf.getvalue()


class pathParser ( Parser ):

    grammarFileName = "path.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "','", "'drop'", "'@'", 
                     "'at'", "'of'", "'cols'", "'columns'", "'col'", "'column'", 
                     "'rows'", "'row'", "'pads'", "'steps'", "'pad'", "'step'", 
                     "'**__**'", "'+'", "''s'", "'/'", "':'", "'*'", "'-'", 
                     "'left'", "'right'", "'east'", "'west'", "'up'", "'down'", 
                     "'north'", "'south'", "';'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "ADD", "ATTR", 
                      "DIV", "INJECT", "MUL", "SUB", "LEFT", "RIGHT", "EAST", 
                      "WEST", "UP", "DOWN", "NORTH", "SOUTH", "TERMINATOR", 
                      "ID", "INT", "FLOAT", "STRING", "EOL_COMMENT", "COMMENT", 
                      "WS" ]

    RULE_expr = 0
    RULE_horiz_unit = 1
    RULE_vert_unit = 2
    RULE_undirected_unit = 3
    RULE_horiz_dir = 4
    RULE_vertical_dir = 5
    RULE_name = 6
    RULE_kwd_names = 7

    ruleNames =  [ "expr", "horiz_unit", "vert_unit", "undirected_unit", 
                   "horiz_dir", "vertical_dir", "name", "kwd_names" ]

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
    ADD=19
    ATTR=20
    DIV=21
    INJECT=22
    MUL=23
    SUB=24
    LEFT=25
    RIGHT=26
    EAST=27
    WEST=28
    UP=29
    DOWN=30
    NORTH=31
    SOUTH=32
    TERMINATOR=33
    ID=34
    INT=35
    FLOAT=36
    STRING=37
    EOL_COMMENT=38
    COMMENT=39
    WS=40

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return pathParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class Paren_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(pathParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParen_expr" ):
                listener.enterParen_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParen_expr" ):
                listener.exitParen_expr(self)


    class Int_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(pathParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInt_expr" ):
                listener.enterInt_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInt_expr" ):
                listener.exitInt_expr(self)


    class Coord_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.first = None # ExprContext
            self.second = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(pathParser.ExprContext)
            else:
                return self.getTypedRuleContext(pathParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCoord_expr" ):
                listener.enterCoord_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCoord_expr" ):
                listener.exitCoord_expr(self)


    class Horiz_distContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.dist = None # ExprContext
            self.unit_dist = None # Token
            self.base = None # ExprContext
            self.copyFrom(ctx)

        def horiz_dir(self):
            return self.getTypedRuleContext(pathParser.Horiz_dirContext,0)

        def INT(self):
            return self.getToken(pathParser.INT, 0)
        def horiz_unit(self):
            return self.getTypedRuleContext(pathParser.Horiz_unitContext,0)

        def undirected_unit(self):
            return self.getTypedRuleContext(pathParser.Undirected_unitContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(pathParser.ExprContext)
            else:
                return self.getTypedRuleContext(pathParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHoriz_dist" ):
                listener.enterHoriz_dist(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHoriz_dist" ):
                listener.exitHoriz_dist(self)


    class Injection_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.who = None # ExprContext
            self.what = None # ExprContext
            self.copyFrom(ctx)

        def INJECT(self):
            return self.getToken(pathParser.INJECT, 0)
        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(pathParser.ExprContext)
            else:
                return self.getTypedRuleContext(pathParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInjection_expr" ):
                listener.enterInjection_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInjection_expr" ):
                listener.exitInjection_expr(self)


    class Drop_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.loc = None # ExprContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(pathParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDrop_expr" ):
                listener.enterDrop_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDrop_expr" ):
                listener.exitDrop_expr(self)


    class Function_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self._expr = None # ExprContext
            self.args = list() # of ExprContexts
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(pathParser.NameContext,0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(pathParser.ExprContext)
            else:
                return self.getTypedRuleContext(pathParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction_expr" ):
                listener.enterFunction_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction_expr" ):
                listener.exitFunction_expr(self)


    class Name_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(pathParser.NameContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterName_expr" ):
                listener.enterName_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitName_expr" ):
                listener.exitName_expr(self)


    class Addsub_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.lhs = None # ExprContext
            self.rhs = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(pathParser.ExprContext)
            else:
                return self.getTypedRuleContext(pathParser.ExprContext,i)

        def ADD(self):
            return self.getToken(pathParser.ADD, 0)
        def SUB(self):
            return self.getToken(pathParser.SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddsub_expr" ):
                listener.enterAddsub_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddsub_expr" ):
                listener.exitAddsub_expr(self)


    class Muldiv_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.lhs = None # ExprContext
            self.rhs = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(pathParser.ExprContext)
            else:
                return self.getTypedRuleContext(pathParser.ExprContext,i)

        def MUL(self):
            return self.getToken(pathParser.MUL, 0)
        def DIV(self):
            return self.getToken(pathParser.DIV, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMuldiv_expr" ):
                listener.enterMuldiv_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMuldiv_expr" ):
                listener.exitMuldiv_expr(self)


    class Attr_exprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.ExprContext
            super().__init__(parser)
            self.obj = None # ExprContext
            self._name = None # NameContext
            self.attr = list() # of NameContexts
            self.copyFrom(ctx)

        def ATTR(self):
            return self.getToken(pathParser.ATTR, 0)
        def expr(self):
            return self.getTypedRuleContext(pathParser.ExprContext,0)

        def name(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(pathParser.NameContext)
            else:
                return self.getTypedRuleContext(pathParser.NameContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttr_expr" ):
                listener.enterAttr_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttr_expr" ):
                listener.exitAttr_expr(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = pathParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = pathParser.Paren_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 17
                self.match(pathParser.T__0)
                self.state = 18
                self.expr(0)
                self.state = 19
                self.match(pathParser.T__1)
                pass

            elif la_ == 2:
                localctx = pathParser.Coord_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 21
                self.match(pathParser.T__0)
                self.state = 22
                localctx.first = self.expr(0)
                self.state = 23
                self.match(pathParser.T__2)
                self.state = 24
                localctx.second = self.expr(0)
                self.state = 25
                self.match(pathParser.T__1)
                pass

            elif la_ == 3:
                localctx = pathParser.Drop_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 27
                self.match(pathParser.T__3)
                self.state = 28
                _la = self._input.LA(1)
                if not(_la==pathParser.T__4 or _la==pathParser.T__5):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 29
                localctx.loc = self.expr(12)
                pass

            elif la_ == 4:
                localctx = pathParser.Horiz_distContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 30
                localctx.unit_dist = self.match(pathParser.INT)
                self.state = 31
                if not  (0 if localctx.unit_dist is None else int(localctx.unit_dist.text))==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, " $unit_dist.int==1")
                self.state = 34
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 32
                    self.horiz_unit(True)

                elif la_ == 2:
                    self.state = 33
                    self.undirected_unit(True)


                self.state = 36
                self.horiz_dir()
                self.state = 39
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                if la_ == 1:
                    self.state = 37
                    self.match(pathParser.T__6)
                    self.state = 38
                    localctx.base = self.expr(0)


                pass

            elif la_ == 5:
                localctx = pathParser.Horiz_distContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 41
                localctx.unit_dist = self.match(pathParser.INT)
                self.state = 42
                if not  (0 if localctx.unit_dist is None else int(localctx.unit_dist.text))==1:
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, " $unit_dist.int==1")
                self.state = 43
                self.horiz_unit(True)
                pass

            elif la_ == 6:
                localctx = pathParser.Function_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 44
                self.name()
                self.state = 45
                self.match(pathParser.T__0)
                self.state = 46
                localctx._expr = self.expr(0)
                localctx.args.append(localctx._expr)
                self.state = 51
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==pathParser.T__2:
                    self.state = 47
                    self.match(pathParser.T__2)
                    self.state = 48
                    localctx._expr = self.expr(0)
                    localctx.args.append(localctx._expr)
                    self.state = 53
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 54
                self.match(pathParser.T__1)
                pass

            elif la_ == 7:
                localctx = pathParser.Name_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 56
                self.name()
                pass

            elif la_ == 8:
                localctx = pathParser.Int_exprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 57
                self.match(pathParser.INT)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 90
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 88
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
                    if la_ == 1:
                        localctx = pathParser.Muldiv_exprContext(self, pathParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 60
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 61
                        _la = self._input.LA(1)
                        if not(_la==pathParser.DIV or _la==pathParser.MUL):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 62
                        localctx.rhs = self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = pathParser.Addsub_exprContext(self, pathParser.ExprContext(self, _parentctx, _parentState))
                        localctx.lhs = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 63
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 64
                        _la = self._input.LA(1)
                        if not(_la==pathParser.ADD or _la==pathParser.SUB):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 65
                        localctx.rhs = self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = pathParser.Injection_exprContext(self, pathParser.ExprContext(self, _parentctx, _parentState))
                        localctx.who = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 66
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 67
                        self.match(pathParser.INJECT)
                        self.state = 68
                        localctx.what = self.expr(5)
                        pass

                    elif la_ == 4:
                        localctx = pathParser.Horiz_distContext(self, pathParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 69
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 72
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                        if la_ == 1:
                            self.state = 70
                            self.horiz_unit(False)

                        elif la_ == 2:
                            self.state = 71
                            self.undirected_unit(False)


                        self.state = 74
                        self.horiz_dir()
                        self.state = 77
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
                        if la_ == 1:
                            self.state = 75
                            self.match(pathParser.T__6)
                            self.state = 76
                            localctx.base = self.expr(0)


                        pass

                    elif la_ == 5:
                        localctx = pathParser.Horiz_distContext(self, pathParser.ExprContext(self, _parentctx, _parentState))
                        localctx.dist = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 79
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 80
                        self.horiz_unit(False)
                        pass

                    elif la_ == 6:
                        localctx = pathParser.Attr_exprContext(self, pathParser.ExprContext(self, _parentctx, _parentState))
                        localctx.obj = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 81
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 82
                        self.match(pathParser.ATTR)
                        self.state = 84 
                        self._errHandler.sync(self)
                        _alt = 1
                        while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                            if _alt == 1:
                                self.state = 83
                                localctx._name = self.name()
                                localctx.attr.append(localctx._name)

                            else:
                                raise NoViableAltException(self)
                            self.state = 86 
                            self._errHandler.sync(self)
                            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

                        pass

             
                self.state = 92
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Horiz_unitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1, sing:bool=None):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.sing = None
            self.sing = sing


        def getRuleIndex(self):
            return pathParser.RULE_horiz_unit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHoriz_unit" ):
                listener.enterHoriz_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHoriz_unit" ):
                listener.exitHoriz_unit(self)




    def horiz_unit(self, sing:bool):

        localctx = pathParser.Horiz_unitContext(self, self._ctx, self.state, sing)
        self.enterRule(localctx, 2, self.RULE_horiz_unit)
        try:
            self.state = 99
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 93
                self.match(pathParser.T__7)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 94
                self.match(pathParser.T__8)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 95
                if not  localctx.sing :
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, " $sing ")
                self.state = 96
                self.match(pathParser.T__9)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 97
                if not  localctx.sing :
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, " $sing ")
                self.state = 98
                self.match(pathParser.T__10)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Vert_unitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1, sing:bool=None):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.sing = None
            self.sing = sing


        def getRuleIndex(self):
            return pathParser.RULE_vert_unit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVert_unit" ):
                listener.enterVert_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVert_unit" ):
                listener.exitVert_unit(self)




    def vert_unit(self, sing:bool):

        localctx = pathParser.Vert_unitContext(self, self._ctx, self.state, sing)
        self.enterRule(localctx, 4, self.RULE_vert_unit)
        try:
            self.state = 104
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 101
                self.match(pathParser.T__11)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 102
                if not  localctx.sing :
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, " $sing ")
                self.state = 103
                self.match(pathParser.T__12)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Undirected_unitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1, sing:bool=None):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.sing = None
            self.sing = sing


        def getRuleIndex(self):
            return pathParser.RULE_undirected_unit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUndirected_unit" ):
                listener.enterUndirected_unit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUndirected_unit" ):
                listener.exitUndirected_unit(self)




    def undirected_unit(self, sing:bool):

        localctx = pathParser.Undirected_unitContext(self, self._ctx, self.state, sing)
        self.enterRule(localctx, 6, self.RULE_undirected_unit)
        try:
            self.state = 112
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 106
                self.match(pathParser.T__13)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 107
                self.match(pathParser.T__14)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 108
                if not  localctx.sing :
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, " $sing ")
                self.state = 109
                self.match(pathParser.T__15)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 110
                if not  localctx.sing :
                    from antlr4.error.Errors import FailedPredicateException
                    raise FailedPredicateException(self, " $sing ")
                self.state = 111
                self.match(pathParser.T__16)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Horiz_dirContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.direction = None

        def LEFT(self):
            return self.getToken(pathParser.LEFT, 0)

        def RIGHT(self):
            return self.getToken(pathParser.RIGHT, 0)

        def EAST(self):
            return self.getToken(pathParser.EAST, 0)

        def WEST(self):
            return self.getToken(pathParser.WEST, 0)

        def getRuleIndex(self):
            return pathParser.RULE_horiz_dir

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHoriz_dir" ):
                listener.enterHoriz_dir(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHoriz_dir" ):
                listener.exitHoriz_dir(self)




    def horiz_dir(self):

        localctx = pathParser.Horiz_dirContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_horiz_dir)
        try:
            self.state = 122
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [pathParser.LEFT]:
                self.enterOuterAlt(localctx, 1)
                self.state = 114
                self.match(pathParser.LEFT)
                localctx.direction=Dir.LEFT
                pass
            elif token in [pathParser.RIGHT]:
                self.enterOuterAlt(localctx, 2)
                self.state = 116
                self.match(pathParser.RIGHT)
                localctx.direction=Dir.RIGHT
                pass
            elif token in [pathParser.EAST]:
                self.enterOuterAlt(localctx, 3)
                self.state = 118
                self.match(pathParser.EAST)
                localctx.direction=Dir.RIGHT
                pass
            elif token in [pathParser.WEST]:
                self.enterOuterAlt(localctx, 4)
                self.state = 120
                self.match(pathParser.WEST)
                localctx.direction=Dir.LEFT
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


    class Vertical_dirContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.direction = None

        def UP(self):
            return self.getToken(pathParser.UP, 0)

        def DOWN(self):
            return self.getToken(pathParser.DOWN, 0)

        def NORTH(self):
            return self.getToken(pathParser.NORTH, 0)

        def SOUTH(self):
            return self.getToken(pathParser.SOUTH, 0)

        def getRuleIndex(self):
            return pathParser.RULE_vertical_dir

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVertical_dir" ):
                listener.enterVertical_dir(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVertical_dir" ):
                listener.exitVertical_dir(self)




    def vertical_dir(self):

        localctx = pathParser.Vertical_dirContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_vertical_dir)
        try:
            self.state = 132
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [pathParser.UP]:
                self.enterOuterAlt(localctx, 1)
                self.state = 124
                self.match(pathParser.UP)
                localctx.direction=Dir.UP
                pass
            elif token in [pathParser.DOWN]:
                self.enterOuterAlt(localctx, 2)
                self.state = 126
                self.match(pathParser.DOWN)
                localctx.direction=Dir.DOWN
                pass
            elif token in [pathParser.NORTH]:
                self.enterOuterAlt(localctx, 3)
                self.state = 128
                self.match(pathParser.NORTH)
                localctx.direction=Dir.UP
                pass
            elif token in [pathParser.SOUTH]:
                self.enterOuterAlt(localctx, 4)
                self.state = 130
                self.match(pathParser.SOUTH)
                localctx.direction=Dir.DOWN
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
            return self.getToken(pathParser.ID, 0)

        def kwd_names(self):
            return self.getTypedRuleContext(pathParser.Kwd_namesContext,0)


        def getRuleIndex(self):
            return pathParser.RULE_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterName" ):
                listener.enterName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitName" ):
                listener.exitName(self)




    def name(self):

        localctx = pathParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [pathParser.ID]:
                self.state = 134
                self.match(pathParser.ID)
                pass
            elif token in [pathParser.T__17]:
                self.state = 135
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
            return pathParser.RULE_kwd_names

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKwd_names" ):
                listener.enterKwd_names(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKwd_names" ):
                listener.exitKwd_names(self)




    def kwd_names(self):

        localctx = pathParser.Kwd_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_kwd_names)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.match(pathParser.T__17)
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
        self._predicates[0] = self.expr_sempred
        self._predicates[1] = self.horiz_unit_sempred
        self._predicates[2] = self.vert_unit_sempred
        self._predicates[3] = self.undirected_unit_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return  (0 if localctx.unit_dist is None else int(localctx.unit_dist.text))==1
         

            if predIndex == 1:
                return  (0 if localctx.unit_dist is None else int(localctx.unit_dist.text))==1
         

            if predIndex == 2:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 7)
         

    def horiz_unit_sempred(self, localctx:Horiz_unitContext, predIndex:int):
            if predIndex == 8:
                return  localctx.sing 
         

            if predIndex == 9:
                return  localctx.sing 
         

    def vert_unit_sempred(self, localctx:Vert_unitContext, predIndex:int):
            if predIndex == 10:
                return  localctx.sing 
         

    def undirected_unit_sempred(self, localctx:Undirected_unitContext, predIndex:int):
            if predIndex == 11:
                return  localctx.sing 
         

            if predIndex == 12:
                return  localctx.sing 
         




