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
COMMA:         ',';
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
BY:        'by';
CAN:       'can';
CANNOT:    'cannot';
CAN_T:     'can\'t';
COUNT:     'count';
DEF:       'Def' { dedented_kwd(); } ;
DEFAULT:   'default';
DOES:      'does';
DOESN_T:   'doesn\'t';
FALSE:     'false';
FROM:      'from';
HAS:       'has';
IF:        'If';
IN:        'in';
INITIALLY: 'initially';
IS:        'is';
ISN_T:     'isn\'t';
IT:        'it';
IT_cap:    'It';
ITS:       'its';
ITS_cap:   'Its';
IT_S:      'it\'s';
IT_S_cap:  'It\'s';
ITSELF:    'itself';
LET:       'Let';
NO:        'no';
NOT:       'not';
OF:        'of';
OR:        'or';
OTHERWISE: 'Otherwise' { dedented_kwd(); } ;
OWN:       'own';
PLURAL:    'plural';
THE:       'the';
THE_cap:   'The';
TO:        'to';
TRUE:      'true';
UNCHANGEABLE: 'unchangeable';
UNIQUE:    'unique';
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
