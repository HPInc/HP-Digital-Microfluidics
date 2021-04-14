lexer grammar PhysLLexer;

@header {
package com.hp.physl;
}

options { 
	superClass=PhysLLexerBase;
}

tokens { INDENT, DEDENT }

APOSTROPHE_S:  '\'s' ;
BULLET:        '--' { bullet(); } ;
CLOSE_BRACE:   '}';
CLOSE_BRACKET: ']';
CLOSE_PAREN:   ')';
COLON:         ':';
EQUALS:        '=';
GREATER:       '>';
GREATER_EQ:    '>=';
LESS:          '<';
LESS_EQ:       '<=';
MINUS:         '-';
NOT_EQ:        '<>';
OPEN_BRACE:    '{' ;
OPEN_BRACKET:  '[' ;
OPEN_PAREN:    '(' ;
PERIOD:        '.';
PLUS:          '+';
SLASH:         '/';
STAR:          '*';

A:         'a';
A_cap:     'A';
AN:        'an';
AN_cap:    'An';
AND:       'and';
BE:        'be';
BLOCK:     'Block' { dedented_kwd(); } ;
CAN:       'can';
CANNOT:    'cannot';
CAN_T:     'can\'t';
COUNT:     'count';
DEF:       'Def' { dedented_kwd(); } ;
DOES:      'does';
DOESN_T:   'doesn\'t';
FALSE:     'false';
IF:        'If';
IN:        'in';
IS:        'is';
ISN_T:     'isn\'t';
IT:        'it';
ITS:       'its';
IT_S:      'it\'s';
ITSELF:    'itself';
LET:       'Let';
NO:        'no';
NOT:       'not';
OWN:       'own';
OR:        'or';
OTHERWISE: 'Otherwise' { dedented_kwd(); } ;
THE:       'the';
THE_cap:   'The';
TRUE:      'true';
YES:       'yes';

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

STRING : '"' ('\\' [\\"rnt]|.)*? '"' ;

WS: [ \t]+ { handle_ws(); } -> skip;
NL: [\r\n] { handle_nl(); } -> skip;

EOL_COMMENT : '//' .*? '\r'? '\n' -> skip ;
COMMENT : '/*' .*? '*/' -> skip ;
