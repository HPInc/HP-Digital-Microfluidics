lexer grammar commonLexer;

options {
	language = Python3;
}

@header {
from sifu.grid import Dir 
}

fragment ALPHA: [a-zA-Z];
fragment DIGIT: [0-9];
fragment ALNUM: ALPHA | DIGIT;
fragment IDCHAR: ALNUM | '_';


ID : (ALPHA | '_' IDCHAR) IDCHAR* '?'?;

/*
 * INT and FLOAT don't include leading minus sign so that 'x-2' is seen as <x><-><2> rather than <x><-2>
 */
INT : DIGIT+ ('_' DIGIT+)* ;

fragment EXPT : [eE] '-'? INT;

FLOAT : INT '.' INT EXPT? | INT EXPT;

fragment STRING_CHAR
  : ~["“”\\\r\n]
  | ESC_SEQ
  ;

fragment HEX : [0-9a-fA-F] ;

fragment ESC_SEQ
  : '\\' [tnr"'\\]
  | '\\' 'u' HEX HEX HEX HEX
  ;

fragment DQ : '"' | '“' | '”';
STRING : DQ STRING_CHAR* DQ ;

EOL_COMMENT : '//' .*? '\r'? '\n' -> skip ;
COMMENT : '/*' .*? '*/' -> skip ;

  
WS: [ \t\r\n] -> skip;