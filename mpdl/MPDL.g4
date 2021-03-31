grammar MPDL;
@header{
package com.hp.thylacine;	
}

platform : 'platform' ID '{' platform_member* '}' ;

platform_member
  : drop_size_spec
  | clock_tick_spec
  | clock_rate_spec
  | board_size_spec
  | motion_rate_spec
  | well_type_definition
  | well_declaration
  | region_type_definition
  | region_declaration
  | op_declaration
  ;
  
drop_size_spec: 'drop' 'size' 'is' VOLUME ';' ;

clock_tick_spec: 'clock' 'tick' 'is' TIME ';' ;

clock_rate_spec: 'clock' 'rate' 'is' FREQ ';' ;

board_size_spec: 'board' 'is' POS_INT 'by' POS_INT 'pads'? ';' ;

dispensing_spec : 'dispenses' VOLUME time_or_freq? ';' ;
time_or_freq
  : 'every' TIME   # t_or_f_time
  | 'at' FREQ      # t_or_f_freq
  ;

motion_rate_spec : 'motion' 'takes' TIME ';';

volume_spec : 'holds' VOLUME ';' ;

dead_spec : 'is' 'non-functional' ';' ;

magnet_spec : 'has' 'magnet' ';' ;

temp_spec : ('heats' | 'cools') 'to' TEMP  temp_rate? ';' ;		
temp_rate
  : 'in' TIME     # temp_rate_time
  ;

dep_spec : 'does' ('dep' | 'DEP') 'from' FREQ 'to' FREQ ';' ;

well_type_definition : 'define' well_header '{' well_member* '}' ;

well_header
  : 'default'? 'well'           # default_well_header
  | name=non_def_adj 'well' (':' parent=adj 'well')? #named_well_header 
  ;

well_member
  : dispensing_spec
  | volume_spec
  | dead_spec
  | temp_spec
  ;
  
well_declaration 
  : adj? 'well' spec? 'at' pad ';'                                          # single_well_decl
  | adj? 'wells' (min=NON_NEG_INT 'to' max=NON_NEG_INT)? 'at' pad_list  ';' # multiple_well_decl
  ;

pad_type_definition : 'define' pad_header '{' pad_member* '}' ;

pad_header
  : 'default'? 'pad'           # default_pad_header
  | name=non_def_adj 'pad' (':' parent=adj 'pad')? #named_pad_header 
  ;

pad_member
  : volume_spec
  | dead_spec
  | magnet_spec
  | dep_spec
  ;
  
pad_declaration 
  : adj? 'pad' spec? 'at' pad ';'                                          # single_pad_decl
  | adj? 'pads' (min=NON_NEG_INT 'to' max=NON_NEG_INT)? 'at' pad_list  ';' # multiple_pad_decl
  ;

region_type_definition : 'define' region_header '{' region_member* '}' ;

region_header
  : name=non_def_adj 'region' (':' parent=non_def_adj 'region')? #named_region_header 
  ;

region_member
  : dead_spec
  | temp_spec
  ;
  
region_declaration 
  : non_def_adj 'region' spec? 'at' region ';'                                  # single_region_decl
  | non_def_adj 'regions' (min=NON_NEG_INT 'to' max=NON_NEG_INT)? 'at' region_list  ';' # multiple_region_decl
  ;

op_declaration
  : 'define' 'operation' op_name '{' op_member* '}' ;
  
op_name : ID ;

op_param : ;

op_member 
  : op_param_spec
  | op_return_spec
  ;
  
op_param_spec: 'optional'? 'param' param_name ':' param_type_and_default ';' ;

op_return_spec: 'returns' param_name ':' (is_list='list' 'of')? param_type ';' ; 
  
param_name : ID ;

param_type_and_default
  : type='integer' ('=' default_val=INT)?            # int_ptype
  | type='real' ('=' default_val=(INT | FLOAT ))?    # real_ptype
  | type='boolean' ('=' default_val=bool_const)?     # bool_ptype
  | type='string' ('=' default_val=STRING)?          # string_ptype
  | type='pad' ('=' default_val=pad)?                # pad_ptype
  | type='region' ('=' default_val=region)?          # region_ptype
  | type='well' ('=' default_val=well)?              # well_ptype
  | type='time' ('=' default_val=TIME)?              # time_ptype
  | type='temperature' ('=' default_val=TEMP)?       # temp_ptype
  | type='volume' ('=' default_val=VOLUME)?          # volume_ptype
  | type='frequency' ('=' default_val=FREQ)?          # volume_ptype
  | 'list' 'of' type='integer' ('=' default_val=int_list)?            # int_list_ptype
  | 'list' 'of' type='real' ('=' default_val=real_list)?    # real_list_ptype
  | 'list' 'of' type='boolean' ('=' default_val=bool_list)?     # bool_list_ptype
  | 'list' 'of' type='string' ('=' default_val=string_list)?          # string_list_ptype
  | 'list' 'of' type='pad' ('=' default_val=pad_list)?                # pad_list_ptype
  | 'list' 'of' type='region' ('=' default_val=region_list_lit)?          # region_list_ptype
  | 'list' 'of' type='well' ('=' default_val=well_list)?              # well_list_ptype
  | 'list' 'of' type='time' ('=' default_val=time_list)?              # time_list_ptype
  | 'list' 'of' type='temperature' ('=' default_val=temp_list)?       # temp_list_ptype
  | 'list' 'of' type='volume' ('=' default_val=volume_list)?          # volume_list_ptype
  | 'list' 'of' type='frequency' ('=' default_val=freq_list)?          # freq_list_ptype
  ;  

param_type 
  : 'integer' | 'real' | 'boolean' | 'string'
  | 'pad' | 'region' | 'well'
  | 'time' | 'temperature' | 'volume' | 'frequency'
  ; 

int_list : '[' elts+=INT (',' elts+=INT)* ']' ;
real_list : '[' elts+=(INT|FLOAT) (',' elts+=(INT|FLOAT))* ']' ;
bool_list : '[' elts+=bool_const (',' elts+=bool_const)* ']' ;
string_list : '[' elts+=STRING (',' elts+=STRING)* ']' ;
region_list_lit : '[' elts+=region (',' elts+=region)* ']' ;
well_list : '[' elts+=well (',' elts+=well)* ']' ;
time_list : '[' elts+=TIME (',' elts+=TIME)* ']' ;
temp_list : '[' elts+=TEMP (',' elts+=TEMP)* ']' ;
volume_list : '[' elts+=VOLUME (',' elts+=VOLUME)* ']' ;
freq_list : '[' elts+=FREQ (',' elts+=FREQ)* ']' ;


/*
 * PADS
 */  

pad : '(' x=row_col ',' y=row_col ')' # pad_literal
    | PARAM_NAME                      # pad_param
    | pad '+' distance                # pad_relative
    | well 'exit'                     # well_exit
    | '(' pad ')'                     # parenthesized_pad_expr
    ;

row_col : NON_NEG_INT | 'max';
distance : POS_INT PADS dir ;
dir : direction=(UP|DOWN|LEFT|RIGHT);

pad_list : '[' elts+=pad (',' elts+=pad)* ']';

region 
  : from=pad 'to' to=pad                   # region_bounds
  | non_def_adj 'region' spec?             # typed_named_region
  | 'region' spec                          # untyped_region
  | '(' region ')'                         # parenthesized_region_expr
  | region '+' region                      # region_sum
  | region '-' region                      # region_difference
  | POS_INT PADS 'around' pad      # buffered_pad
  | POS_INT PADS 'around' region   # buffered_region
  ;
  
region_list : region (',' region*) ;  

well : adj? 'well' spec? ;

adj: 'default' | non_def_adj ;

non_def_adj : ID | 'dep' | 'DEP';

spec : NON_NEG_INT | ID ;

bool_const : 'true' | 'false' ;

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

fragment VOLUME_UNIT
  : ABBR_PREFIX? [lL]
  | NAME_PREFIX? 'lit' ERRE MAYBE_S
  | 'drop' MAYBE_S
  ;

VOLUME : (NON_NEG_INT | NON_NEG_FLOAT) WS* VOLUME_UNIT ;

fragment TIME_UNIT
  : ABBR_PREFIX? 's'
  | (ABBR_PREFIX | NAME_PREFIX)? 'sec' MAYBE_S
  | NAME_PREFIX? 'second' MAYBE_S
  | 'tick' MAYBE_S
  ;

TIME : (NON_NEG_INT | NON_NEG_FLOAT) WS* TIME_UNIT ;

fragment FREQ_UNIT
  : ABBR_PREFIX? 'Hz'
  | NAME_PREFIX? 'hertz'
  ;

FREQ : (NON_NEG_INT | NON_NEG_FLOAT) WS* FREQ_UNIT ;

fragment TEMP_UNIT
  : 'K'
  | ('°' | 'degrees')? 'C'
  | ('°' | 'degrees') 'F'
  ;
  
TEMP 
  : (INT | FLOAT) WS* TEMP_UNIT
  | 'room' WS+ 'temp' 'erature'?
  ;  

UP: 'up';
DOWN: 'down';
LEFT: 'left';
RIGHT: 'right';
MAX: 'max';

PADS: 'pad' MAYBE_S ;

fragment ALPHA: [a-zA-Z];
fragment ALNUM: ALPHA | [0-9];
fragment IDCHAR: ALNUM | '_';

PARAM_NAME: '$' ALNUM IDCHAR*;

ID : (ALNUM | '_' IDCHAR) IDCHAR*;

NON_NEG_INT : '0' | POS_INT ;

POS_INT : [1-9][0-9]* ;

INT : '-'? POS_INT;

fragment EXPT : [eE] INT;

NON_NEG_FLOAT : NON_NEG_INT '.' [0-9]+ EXPT? | NON_NEG_INT EXPT;

FLOAT : '-'? NON_NEG_FLOAT;

STRING : '"' ('\\' [\\"rnt]|.)*? '"' ;

EOL_COMMENT : '//' .*? '\r'? '\n' -> skip ;
COMMENT : '/*' .*? '*/' -> skip ;


WS: [ \t\r\n] -> skip;
