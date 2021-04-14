grammar MPAM;

@header{
package com.hp.mpam;	
}
just_expr: expr EOF ;

expr
  : '(' expr ')'                        # prenthesized_expr

  | obj=expr ATTSEL attr=attribute      # attribute_expr
  | ('its'|'it\'s') attr=attribute      # attribute_expr
  | list=expr '[' index=expr ']'        # list_index_expr
  | 'not' rhs=expr                      # not_expr
  | '-' rhs=expr                        # negation_expr
  | mag=expr unit                       # quantity_expr
//  | neg='-'? cmag=(INT|FLOAT) unit      # quantity_expr
  | mag=expr step_dir                   # delta_expr
  | n=expr kind=step_kind               # distance_expr
  | lhs=expr op=('*'|'/') rhs=expr      # muldiv_expr
  | lhs=expr relpos rhs=expr            # relpos_expr
  | lhs=expr op=('+'|'-') rhs=expr      # addsub_expr
//  | lhs=expr 'is'? 'not'? 'in' rhs=expr  # in_expr
  | obj=expr prop=property  (('and'|'or') property)*# property_expr
  | lhs=expr 'is' not='not'? relation rhs=expr  # relation_expr
  | lhs=expr not='not' relation rhs=expr  # relation_expr
  | lhs=expr op=rel_op rhs=expr         # order_expr
  | lhs=expr 'and' rhs=expr             # and_expr
  | lhs=expr 'or' rhs=expr              # or_expr

  | 'the' type=name 'well'              # singleton_well
  | type=name? 'well' '[' well_selector ']' # well_selector_expr 
  | 'the' type=name 'region'            # singleton_region
  | type=name? 'region' '[' region_selector']' # region_selector_expr 
  | '(' row=expr ',' col=expr ')'       # pad_coords
  | '[' elts+=expr (',' elts+=expr)* ']' # list_expr
  | 'call' name '(' args+=call_arg (',' args+=call_arg)* ')' #op_call
  | val=INT                # int_literal
  | val=FLOAT              # float_literal
  | val=('true' | 'false' | 'yes' | 'no')     # boolean_literal
  | 'max' val=('row' | 'col' | 'column')  # edge_literal
  | 'room' ('temp'|'temperature')   # room_temp_lit
  | 'it'                   # current_obj_lit
  | name                   # variable_name
  ;
  
well_selector
  : expr                                 # well_by_num_or_pad
  ;  
  
  
region_selector
  : expr                                 # region_by_num
  ;  
  
call_arg
  : name ':' expr                # in_arg
  | name 'as' name               # out_arg
  ;

relpos
  : ('to' 'the')? ('left'|'right') 'of'   # horizontal_relpos
  | ('above'|'below')                     # vertical_relpos
  | ('up'|'down') 'from'                  # vertical_relpos    
  ;

unit: kind=(VOLUME_UNIT|TIME_UNIT|TEMP_UNIT|FREQ_UNIT);   
  
step_kind: kind=('row'|'rows'|'col'|'column'|'cols'|'columns'|'pad'|'pads');

step_dir
  : dir=('up'|'down'|'left'|'right')
 // | 'toward' dest=expr
  ;
  
rel_op
  : 'not'? which=('=' | '<>' | '<=' | '<' | '>=' | '>') 
  ;  
  
attribute
  : 'count' 'in' unit   # unit_count_attr
  | name                # user_defined_attr
  ;
  
  
property
  : aux_verb? name
  ;
  
aux_verb
locals[boolean not, boolean can, boolean does, boolean is]
  : 'is' { $is=true;}
  | ('is' 'not' | 'isn\'t') { $is=true; $not=true; }
  | ('does' 'not' | 'doesn\'t') { $does=true; $not=true; }
  | 'can' { $can=true;}
  | ('can' 'not' | 'cannot' | 'can\'t') { $can=true; $not=true; }
  ;
relation
  : 'in'                # in_region_rel
//  | name prep='than'    # user_defined_rel
  | name     # user_defined_rel
  ;
  
boolean_lit
locals [boolean val]
  : ('true' | 'yes') { $val=true;}
  | ('false' | 'no') { $val=false;}
  ;
  

// Keywords that are allowed as names.  Need to make sure that
// none are expressions on their own.
kwd_names 
  : 'max'
  | 'row'  | 'col'  | 'column'  | 'pad'
  | 'rows' | 'cols' | 'columns' | 'pads'
  | 'up' | 'down' | 'left' | 'right' | 'toward'
  | 'exit' | 'current' | 'volume' | 'capacity'
  | 'on' | 'board' | 'off'
  | 'as' | 'room' | 'temp' | 'temperature'
  | 'than'
  ;  

/*
 * A multiword name may end with a unit token, so
 * "n mg" is ambiguous between a name and a quantity with
 * magnitude "n".  This should be distinguishable at type 
 * inference based on whether "n" or "n mg" are defined as 
 * names.  Will also have to pay attention to other contexts
 * in which a name can exist and which bind higher than 
 * the quantity rule (e.g., "-n mg" or "x's n mg").
 */
name : (ID | kwd_names | unit)+ ;

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
EQ: '=';
LT: '<';
GT: '>';
LE: '<=';
GE: '>=';
NE: '<>';
  

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
  
//TEMP 
//  : (INT | FLOAT) WS* TEMP_UNIT
//  | 'room' WS+ 'temp' 'erature'?
//  ;  
  


ATTSEL: '\'' 's' ;


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

EOL_COMMENT : '//' .*? '\r'? '\n' -> skip ;
COMMENT : '/*' .*? '*/' -> skip ;


WS: [ \t\r\n] -> skip;
