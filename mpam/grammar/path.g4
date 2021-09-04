grammar path;

options {
	language = Python3;
}

@header {
from mpam.types import Dir 
}

expr
  : '(' expr ')'                     # paren_expr
  | '(' first=expr ',' second=expr ')' # coord_expr
  | 'drop' ('@' | 'at') loc=expr     # drop_expr
  | dist=expr (horiz_unit[False] | undirected_unit[False])? horiz_dir ('of' base=expr)?   # horiz_dist
  | dist=expr horiz_unit[False]    # horiz_dist
  | unit_dist=INT { $unit_dist.int==1}? (horiz_unit[True] | undirected_unit[True])? horiz_dir ('of' base=expr)? # horiz_dist 
  | unit_dist=INT { $unit_dist.int==1}? horiz_unit[True] # horiz_dist 
  
//  | dist=expr axis=('rows' | 'pads') direction=vertical_dir? # dist_expr
//  | dist=expr axis=('cols' | 'columns' | 'pads') direction=horiz_dir?  # dist_expr
  
//  | dist=INT { int($dist.text) == 1 }? axis=('row' | 'pad' ) direction=vertical_dir? # unit_dist_expr
//  | dist=INT { int($dist.text) == 1 }? axis=('col' | 'column' | 'pad' ) direction=horiz_dir? # unit_dist_expr
  | obj=expr ATTR (attr+=name)+        # attr_expr
  | lhs=expr (MUL | DIV) rhs=expr    # muldiv_expr
  | lhs=expr (ADD | SUB) rhs=expr    # addsub_expr
  | who=expr INJECT what=expr           # injection_expr
  | name  '(' args+=expr (',' args+=expr)* ')' # function_expr
  | name                             # name_expr
  | INT                              # int_expr
  ;
  
horiz_unit[bool sing] 
  : 'cols' 
  | 'columns'
  | { $sing }? 'col'
  | { $sing }? 'column'
  ; 
  
vert_unit[bool sing] 
  : 'rows' 
  | { $sing }? 'row'
  ;
  
undirected_unit[bool sing] 
  : 'pads' 
  | 'steps'
  | { $sing }? 'pad'
  | { $sing }? 'step'
  ; 

horiz_dir returns [Dir direction]
  : LEFT {$ctx.direction=Dir.LEFT} 
  | RIGHT {$ctx.direction=Dir.RIGHT}
  | EAST {$ctx.direction=Dir.RIGHT}
  | WEST {$ctx.direction=Dir.LEFT}
  ;
  
vertical_dir returns [Dir direction]
  : UP {$ctx.direction=Dir.UP}
  | DOWN {$ctx.direction=Dir.DOWN}
  | NORTH {$ctx.direction=Dir.UP}
  | SOUTH {$ctx.direction=Dir.DOWN}
  ;
  
ADD: '+';
ATTR: '\'s';
DIV: '/';
INJECT: ':';
MUL: '*';
SUB: '-';

//horiz_unit: COLS | COLUMNS;
//COLS: 'cols';
//COLUMNS: 'columns';


LEFT: 'left';
RIGHT: 'right';
EAST: 'east';
WEST: 'west';


UP: 'up';
DOWN: 'down';
NORTH: 'north';
SOUTH: 'south';

  
//callable_thing
//  : name  ( '(' args+=expr (',' args+=expr)* ')' )?
//  ;

//definition
//  : name '=' path                    # path_def
//  | name ('@' | 'at') coord          # drop_def
//  | name ':' 'barrier' '(' n=INT ')' # barrier_def
//  ;
//
//path
//  : motion
//  | path ',' motion
//  ;
//  
//motion
//  : direction dist=INT?              # dir_motion
//  | 'to' ('col' | 'column') col=INT  # to_col
//  | 'to' 'row' row=INT               # to_row
//  | 'to' coord                       # to_pad
//  | 'absorb'                         # to_well 
//  | 'to' 'well'           			 # to_well
//  | ('pause' | 'wait') 'for'? ticks=INT ('tick' | 'ticks')?   # pause_ticks
//  | ('reach' | 'wait' 'at') barrier       # reach_barrier
//  | 'pass' 'through'? barrier        # pass_barrier
//  
//  ;
//  
//direction : which=('up' | 'north' | 'down' | 'south' | 'right' | 'east' | 'left' | 'west') ;
//
//coord : '(' x=INT ',' y=INT ')' ;
//
//barrier: name ;

name : (ID | kwd_names) ;

kwd_names : '**__**';

TERMINATOR: ';';
 
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
  : ~["\\\r\n]
  | ESC_SEQ
  ;

fragment HEX : [0-9a-fA-F] ;

fragment ESC_SEQ
  : '\\' [tnr"'\\]
  | '\\' 'u' HEX HEX HEX HEX
  ;

STRING : '"' STRING_CHAR* '"' ;

EOL_COMMENT : '//' .*? '\r'? '\n' -> skip ;
COMMENT : '/*' .*? '*/' -> skip ;

  
WS: [ \t\r\n] -> skip;