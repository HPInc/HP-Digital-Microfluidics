lexer grammar PhysLLexer;

@header {
package com.hp.thylacine;
}

options { 
	superClass=PhysLLexerBase;
}

tokens { INDENT, DEDENT }

BULLET:    '--' { bullet(); } ;
COLON:     ':';
PERIOD:    '.';

DEF:       'def' { dedented_kwd(); } ;
IF:        'if';
OTHERWISE: 'otherwise' { dedented_kwd(); } ;

fragment ALPHA: [a-zA-Z];
fragment DIGIT: [0-9];
fragment ALNUM: ALPHA | DIGIT;
fragment IDCHAR: ALNUM | '_';


ID : (ALPHA | '_' IDCHAR) IDCHAR* '?'?;


WS: [ \t]+ { handle_ws(); } -> skip;
NL: [\r\n] { handle_nl(); } -> skip;

EOL_COMMENT : '//' .*? '\r'? '\n' -> skip ;
COMMENT : '/*' .*? '*/' -> skip ;
