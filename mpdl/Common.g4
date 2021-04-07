grammar Common;

@header{
package com.hp.thylacine;	
}
just_expr: expr EOF ;

expr
  : '(' expr ')'                        # prenthesized_expr
  | obj=expr ATTSEL attr=attribute      # attribute_expr
  | '-' rhs=expr                        # negation_expr
  | list=expr '[' index=expr ']'        # list_index_expr
  | mag=expr unit                      # quantity_expr
  | n=expr kind=step_kind dir=step_dir? # distance_expr
  | lhs=expr op=('*'|'/') rhs=expr      # muldiv_expr
  | lhs=expr op=('+'|'-') rhs=expr      # addsub_expr
  | 'the' type=name 'well'              # singleton_well
  | type=name? 'well' which=INT         # numbered_well
  | 'the' type=name? 'well' 'at' loc=expr   # located_well
  | 'the' type=name 'region'            # singleton_region 
  | type=name? 'region' which=INT       # numbered_region
  | '(' row=expr ',' col=expr ')'       # pad_coords
  | '[' elts+=expr (',' elts+=expr)* ']' # list_expr
  | val=INT                # int_literal
  | val=FLOAT              # float_literal
  | val=('true' | 'false' | 'yes' | 'no')     # boolean_literal
  | 'max' val=('row' | 'col' | 'column')  # edge_literal
  | name                   # variable_name
  ;
  
unit: kind=(VOLUME_UNIT|TIME_UNIT|TEMP_UNIT|FREQ_UNIT);   
  
step_kind: kind=('row'|'rows'|'col'|'column'|'pad'|'pads');

step_dir
  : dir=('up'|'down'|'left'|'right')
  | 'toward' dest=expr
  ;
  
attribute
  : 'exit' 'pad'        # exit_pad_attr
  | 'row'               # row_attr
  | ('col' | 'column')  # col_attr
  | 'current'? 'volume' # current_vol_attr
  | 'capacity'          # capacity_attr
  ;
  
boolean_lit
locals [boolean val]
  : ('true' | 'yes') { $val=true;}
  | ('false' | 'no') { $val=false;}
  ;
  
ROW: 'row';
ROWS: 'rows';
COL: 'col';
COLS: 'cols';
COLUMN: 'column';
COLUMNS: 'columns';
PAD: 'pad';
PADS: 'pads';
UP: 'up';
DOWN: 'down';
LEFT: 'left';
RIGHT: 'right';
TRUE: 'true';
FALSE: 'false';
YES: 'yes';
NO: 'no';
PLUS: '+';
MINUS: '-';
STAR: '*';
SLASH: '/';





name : ID
  | 'at'
  | 'row' | 'rows' | 'col'
  | UP | DOWN | LEFT | RIGHT
  | TEMP_UNIT | FREQ_UNIT | TIME_UNIT | VOLUME_UNIT
  ;
  

fragment ERRE : ('er' | 're') ;

fragment MAYBE_S : 's'? ;

fragment ABBR_PREFIX : [uµmkM] 
  ;

fragment NAME_PREFIX
  : 'micro'
  | 'milli'
  | 'kilo'
  | 'mega'
  ;

VOLUME_UNIT
  : ABBR_PREFIX? [lL]
  | NAME_PREFIX? 'lit' ERRE MAYBE_S
  | 'drop' MAYBE_S
  ;

TIME_UNIT
  : ABBR_PREFIX? 's'
  | (ABBR_PREFIX | NAME_PREFIX)? 'sec' MAYBE_S
  | NAME_PREFIX? 'second' MAYBE_S
  | 'tick' MAYBE_S
  ;

FREQ_UNIT
  : ABBR_PREFIX? 'Hz'
  | NAME_PREFIX? 'hertz'
  ;

TEMP_UNIT
  : 'K'
  | ('°' | 'degrees')? 'C'
  | ('°' | 'degrees') 'F'
  ;
  
TEMP 
  : (INT | FLOAT) WS* TEMP_UNIT
  | 'room' WS+ 'temp' 'erature'?
  ;  
  


ATTSEL: '\'' 's' ;


fragment ALPHA: [a-zA-Z];
fragment DIGIT: [0-9];
fragment ALNUM: ALPHA | DIGIT;
fragment IDCHAR: ALNUM | '_';


ID : (ALPHA | '_' IDCHAR) IDCHAR*;

/*
 * INT and FLOAT don't include leading minus sign so that 'x-2' is seen as <x><-><2> rather than <x><-2>
 */
INT : DIGIT+ ('_' DIGIT+)* ;

fragment EXPT : [eE] '-'? INT;

FLOAT : INT '.' INT EXPT? | INT EXPT;

STRING : '"' ('\\' [\\"rnt]|.)*? '"' ;

EOL_COMMENT : '//' .*? '\r'? '\n' -> skip ;
COMMENT : '/*' .*? '*/' -> skip ;


WS: [ \t\r\n] -> skip;
