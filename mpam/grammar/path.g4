grammar path;

options {
	language = Python3;
}

definition
  : name '=' path                    # path_def
  | name ('@' | 'at') coord          # drop_def
  | name ':' 'barrier' '(' n=INT ')' # barrier_def
  ;

path
  : motion
  | path ',' motion
  ;
  
motion
  : direction dist=INT?              # dir_motion
  | 'to' ('col' | 'column') col=INT  # to_col
  | 'to' 'row' row=INT               # to_row
  | 'to' coord                       # to_pad
  | 'absorb'                         # to_well 
  | 'to' 'well'           			 # to_well
  | ('pause' | 'wait') 'for'? ticks=INT ('tick' | 'ticks')?   # pause_ticks
  | ('reach' | 'wait' 'at') barrier       # reach_barrier
  | 'pass' 'through'? barrier        # pass_barrier
  
  ;
  
direction : which=('up' | 'north' | 'down' | 'south' | 'right' | 'east' | 'left' | 'west') ;

coord : '(' x=INT ',' y=INT ')' ;

barrier: name ;

name : (ID | kwd_names) ;

kwd_names : ;
  
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