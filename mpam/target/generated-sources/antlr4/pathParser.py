# Generated from java-escape by ANTLR 4.4
from antlr4 import *
from io import StringIO
package = globals().get("__package__", None)
ischild = len(package)>0 if package is not None else False
if ischild:
    from .pathListener import pathListener
else:
    from pathListener import pathListener
def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\'")
        buf.write("c\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\5\2\"\n\2\3\3\3\3\3\3\3\3\3\3\3\3\7")
        buf.write("\3*\n\3\f\3\16\3-\13\3\3\4\3\4\5\4\61\n\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4@\n\4\3\4")
        buf.write("\3\4\5\4D\n\4\3\4\3\4\3\4\5\4I\n\4\3\4\3\4\3\4\5\4N\n")
        buf.write("\4\3\4\5\4Q\n\4\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3")
        buf.write("\7\3\b\3\b\5\b_\n\b\3\t\3\t\3\t\2\3\4\n\2\4\6\b\n\f\16")
        buf.write("\20\2\7\4\2\23\23\32\32\4\2\17\17\25\25\4\2\13\13\33\33")
        buf.write("\4\2\16\16\37\37\b\2\3\4\7\7\21\21\26\27\35\35  k\2!\3")
        buf.write("\2\2\2\4#\3\2\2\2\6P\3\2\2\2\bR\3\2\2\2\nT\3\2\2\2\fZ")
        buf.write("\3\2\2\2\16^\3\2\2\2\20`\3\2\2\2\22\23\5\16\b\2\23\24")
        buf.write("\7\6\2\2\24\25\5\4\3\2\25\"\3\2\2\2\26\27\5\16\b\2\27")
        buf.write("\30\t\2\2\2\30\31\5\n\6\2\31\"\3\2\2\2\32\33\5\16\b\2")
        buf.write("\33\34\7\31\2\2\34\35\7\n\2\2\35\36\7\f\2\2\36\37\7\"")
        buf.write("\2\2\37 \7\36\2\2 \"\3\2\2\2!\22\3\2\2\2!\26\3\2\2\2!")
        buf.write("\32\3\2\2\2\"\3\3\2\2\2#$\b\3\1\2$%\5\6\4\2%+\3\2\2\2")
        buf.write("&\'\f\3\2\2\'(\7\20\2\2(*\5\6\4\2)&\3\2\2\2*-\3\2\2\2")
        buf.write("+)\3\2\2\2+,\3\2\2\2,\5\3\2\2\2-+\3\2\2\2.\60\5\b\5\2")
        buf.write("/\61\7\"\2\2\60/\3\2\2\2\60\61\3\2\2\2\61Q\3\2\2\2\62")
        buf.write("\63\7\30\2\2\63\64\t\3\2\2\64Q\7\"\2\2\65\66\7\30\2\2")
        buf.write("\66\67\7\t\2\2\67Q\7\"\2\289\7\30\2\29Q\5\n\6\2:Q\7\22")
        buf.write("\2\2;<\7\30\2\2<Q\7\24\2\2=?\t\4\2\2>@\7\b\2\2?>\3\2\2")
        buf.write("\2?@\3\2\2\2@A\3\2\2\2AC\7\"\2\2BD\t\5\2\2CB\3\2\2\2C")
        buf.write("D\3\2\2\2DQ\3\2\2\2EI\7\r\2\2FG\7\33\2\2GI\7\23\2\2HE")
        buf.write("\3\2\2\2HF\3\2\2\2IJ\3\2\2\2JQ\5\f\7\2KM\7\34\2\2LN\7")
        buf.write("\5\2\2ML\3\2\2\2MN\3\2\2\2NO\3\2\2\2OQ\5\f\7\2P.\3\2\2")
        buf.write("\2P\62\3\2\2\2P\65\3\2\2\2P8\3\2\2\2P:\3\2\2\2P;\3\2\2")
        buf.write("\2P=\3\2\2\2PH\3\2\2\2PK\3\2\2\2Q\7\3\2\2\2RS\t\6\2\2")
        buf.write("S\t\3\2\2\2TU\7\f\2\2UV\7\"\2\2VW\7\20\2\2WX\7\"\2\2X")
        buf.write("Y\7\36\2\2Y\13\3\2\2\2Z[\5\16\b\2[\r\3\2\2\2\\_\7!\2\2")
        buf.write("]_\5\20\t\2^\\\3\2\2\2^]\3\2\2\2_\17\3\2\2\2`a\3\2\2\2")
        buf.write("a\21\3\2\2\2\13!+\60?CHMP^")
        return buf.getvalue()
		

class pathParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    EOF = Token.EOF
    T__29=1
    T__28=2
    T__27=3
    T__26=4
    T__25=5
    T__24=6
    T__23=7
    T__22=8
    T__21=9
    T__20=10
    T__19=11
    T__18=12
    T__17=13
    T__16=14
    T__15=15
    T__14=16
    T__13=17
    T__12=18
    T__11=19
    T__10=20
    T__9=21
    T__8=22
    T__7=23
    T__6=24
    T__5=25
    T__4=26
    T__3=27
    T__2=28
    T__1=29
    T__0=30
    ID=31
    INT=32
    FLOAT=33
    STRING=34
    EOL_COMMENT=35
    COMMENT=36
    WS=37

    tokenNames = [ "<INVALID>", "'down'", "'up'", "'through'", "'='", "'north'", 
                   "'for'", "'row'", "'barrier'", "'pause'", "'('", "'reach'", 
                   "'ticks'", "'column'", "','", "'right'", "'absorb'", 
                   "'at'", "'well'", "'col'", "'west'", "'left'", "'to'", 
                   "':'", "'@'", "'wait'", "'pass'", "'east'", "')'", "'tick'", 
                   "'south'", "ID", "INT", "FLOAT", "STRING", "EOL_COMMENT", 
                   "COMMENT", "WS" ]

    RULE_definition = 0
    RULE_path = 1
    RULE_motion = 2
    RULE_direction = 3
    RULE_coord = 4
    RULE_barrier = 5
    RULE_name = 6
    RULE_kwd_names = 7

    ruleNames =  [ "definition", "path", "motion", "direction", "coord", 
                   "barrier", "name", "kwd_names" ]

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.4")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class DefinitionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return pathParser.RULE_definition

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Path_defContext(DefinitionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.DefinitionContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(pathParser.NameContext,0)

        def path(self):
            return self.getTypedRuleContext(pathParser.PathContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterPath_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitPath_def(self)


    class Barrier_defContext(DefinitionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.DefinitionContext)
            super().__init__(parser)
            self.n = None # Token
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(pathParser.NameContext,0)

        def INT(self):
            return self.getToken(pathParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterBarrier_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitBarrier_def(self)


    class Drop_defContext(DefinitionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.DefinitionContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def name(self):
            return self.getTypedRuleContext(pathParser.NameContext,0)

        def coord(self):
            return self.getTypedRuleContext(pathParser.CoordContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterDrop_def(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitDrop_def(self)



    def definition(self):

        localctx = pathParser.DefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_definition)
        self._la = 0 # Token type
        try:
            self.state = 31
            la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
            if la_ == 1:
                localctx = pathParser.Path_defContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 16 
                self.name()
                self.state = 17
                self.match(self.T__26)
                self.state = 18 
                self.path(0)
                pass

            elif la_ == 2:
                localctx = pathParser.Drop_defContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 20 
                self.name()
                self.state = 21
                _la = self._input.LA(1)
                if not(_la==pathParser.T__13 or _la==pathParser.T__6):
                    self._errHandler.recoverInline(self)
                self.consume()
                self.state = 22 
                self.coord()
                pass

            elif la_ == 3:
                localctx = pathParser.Barrier_defContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 24 
                self.name()
                self.state = 25
                self.match(self.T__7)
                self.state = 26
                self.match(self.T__22)
                self.state = 27
                self.match(self.T__20)
                self.state = 28
                localctx.n = self.match(self.INT)
                self.state = 29
                self.match(self.T__2)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PathContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def motion(self):
            return self.getTypedRuleContext(pathParser.MotionContext,0)


        def path(self):
            return self.getTypedRuleContext(pathParser.PathContext,0)


        def getRuleIndex(self):
            return pathParser.RULE_path

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterPath(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitPath(self)



    def path(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = pathParser.PathContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_path, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34 
            self.motion()
            self._ctx.stop = self._input.LT(-1)
            self.state = 41
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = pathParser.PathContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_path)
                    self.state = 36
                    if not self.precpred(self._ctx, 1):
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 37
                    self.match(self.T__16)
                    self.state = 38 
                    self.motion() 
                self.state = 43
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class MotionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return pathParser.RULE_motion

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Dir_motionContext(MotionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.MotionContext)
            super().__init__(parser)
            self.dist = None # Token
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(pathParser.INT, 0)
        def direction(self):
            return self.getTypedRuleContext(pathParser.DirectionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterDir_motion(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitDir_motion(self)


    class To_padContext(MotionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.MotionContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def coord(self):
            return self.getTypedRuleContext(pathParser.CoordContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterTo_pad(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitTo_pad(self)


    class Reach_barrierContext(MotionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.MotionContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def barrier(self):
            return self.getTypedRuleContext(pathParser.BarrierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterReach_barrier(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitReach_barrier(self)


    class To_colContext(MotionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.MotionContext)
            super().__init__(parser)
            self.col = None # Token
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(pathParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterTo_col(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitTo_col(self)


    class Pause_ticksContext(MotionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.MotionContext)
            super().__init__(parser)
            self.ticks = None # Token
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(pathParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterPause_ticks(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitPause_ticks(self)


    class Pass_barrierContext(MotionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.MotionContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def barrier(self):
            return self.getTypedRuleContext(pathParser.BarrierContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterPass_barrier(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitPass_barrier(self)


    class To_rowContext(MotionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.MotionContext)
            super().__init__(parser)
            self.row = None # Token
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(pathParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterTo_row(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitTo_row(self)


    class To_wellContext(MotionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a pathParser.MotionContext)
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterTo_well(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitTo_well(self)



    def motion(self):

        localctx = pathParser.MotionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_motion)
        self._la = 0 # Token type
        try:
            self.state = 78
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                localctx = pathParser.Dir_motionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 44 
                self.direction()
                self.state = 46
                la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                if la_ == 1:
                    self.state = 45
                    localctx.dist = self.match(self.INT)


                pass

            elif la_ == 2:
                localctx = pathParser.To_colContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 48
                self.match(self.T__8)
                self.state = 49
                _la = self._input.LA(1)
                if not(_la==pathParser.T__17 or _la==pathParser.T__11):
                    self._errHandler.recoverInline(self)
                self.consume()
                self.state = 50
                localctx.col = self.match(self.INT)
                pass

            elif la_ == 3:
                localctx = pathParser.To_rowContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 51
                self.match(self.T__8)
                self.state = 52
                self.match(self.T__23)
                self.state = 53
                localctx.row = self.match(self.INT)
                pass

            elif la_ == 4:
                localctx = pathParser.To_padContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 54
                self.match(self.T__8)
                self.state = 55 
                self.coord()
                pass

            elif la_ == 5:
                localctx = pathParser.To_wellContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 56
                self.match(self.T__14)
                pass

            elif la_ == 6:
                localctx = pathParser.To_wellContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 57
                self.match(self.T__8)
                self.state = 58
                self.match(self.T__12)
                pass

            elif la_ == 7:
                localctx = pathParser.Pause_ticksContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 59
                _la = self._input.LA(1)
                if not(_la==pathParser.T__21 or _la==pathParser.T__5):
                    self._errHandler.recoverInline(self)
                self.consume()
                self.state = 61
                _la = self._input.LA(1)
                if _la==pathParser.T__24:
                    self.state = 60
                    self.match(self.T__24)


                self.state = 63
                localctx.ticks = self.match(self.INT)
                self.state = 65
                la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                if la_ == 1:
                    self.state = 64
                    _la = self._input.LA(1)
                    if not(_la==pathParser.T__18 or _la==pathParser.T__1):
                        self._errHandler.recoverInline(self)
                    self.consume()


                pass

            elif la_ == 8:
                localctx = pathParser.Reach_barrierContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 70
                token = self._input.LA(1)
                if token in [self.T__19]:
                    self.state = 67
                    self.match(self.T__19)

                elif token in [self.T__5]:
                    self.state = 68
                    self.match(self.T__5)
                    self.state = 69
                    self.match(self.T__13)

                else:
                    raise NoViableAltException(self)

                self.state = 72 
                self.barrier()
                pass

            elif la_ == 9:
                localctx = pathParser.Pass_barrierContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 73
                self.match(self.T__4)
                self.state = 75
                la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
                if la_ == 1:
                    self.state = 74
                    self.match(self.T__27)


                self.state = 77 
                self.barrier()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DirectionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.which = None # Token


        def getRuleIndex(self):
            return pathParser.RULE_direction

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterDirection(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitDirection(self)




    def direction(self):

        localctx = pathParser.DirectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_direction)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            localctx.which = self._input.LT(1)
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << self.T__29) | (1 << self.T__28) | (1 << self.T__25) | (1 << self.T__15) | (1 << self.T__10) | (1 << self.T__9) | (1 << self.T__3) | (1 << self.T__0))) != 0)):
                localctx.which = self._errHandler.recoverInline(self)
            self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CoordContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.x = None # Token
            self.y = None # Token

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(pathParser.INT)
            else:
                return self.getToken(pathParser.INT, i)

        def getRuleIndex(self):
            return pathParser.RULE_coord

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterCoord(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitCoord(self)




    def coord(self):

        localctx = pathParser.CoordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_coord)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(self.T__20)
            self.state = 83
            localctx.x = self.match(self.INT)
            self.state = 84
            self.match(self.T__16)
            self.state = 85
            localctx.y = self.match(self.INT)
            self.state = 86
            self.match(self.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BarrierContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def name(self):
            return self.getTypedRuleContext(pathParser.NameContext,0)


        def getRuleIndex(self):
            return pathParser.RULE_barrier

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterBarrier(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitBarrier(self)




    def barrier(self):

        localctx = pathParser.BarrierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_barrier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88 
            self.name()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NameContext(ParserRuleContext):

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
            if isinstance( listener, pathListener ):
                listener.enterName(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitName(self)




    def name(self):

        localctx = pathParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.state = 90
                self.match(self.ID)
                pass

            elif la_ == 2:
                self.state = 91 
                self.kwd_names()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Kwd_namesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return pathParser.RULE_kwd_names

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.enterKwd_names(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, pathListener ):
                listener.exitKwd_names(self)




    def kwd_names(self):

        localctx = pathParser.Kwd_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_kwd_names)
        try:
            self.enterOuterAlt(localctx, 1)

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
        self._predicates[1] = self.path_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def path_sempred(self, localctx:PathContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         



