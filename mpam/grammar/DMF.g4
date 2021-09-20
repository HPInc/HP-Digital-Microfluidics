grammar DMF;

import pathLexer;

options {
	language = Python3;
}

@header {
from mpam.types import Dir, OnOff
from langsup.type_supp import Type
from quantities import SI
}


macro_file
  : stat* EOF 
  ;
  
interactive
  : compound EOF  # compound_interactive
  | assignment EOF # assignment_interactive
  | expr EOF # expr_interactive
  | EOF # empty_interactive
//  | pad_op EOF # pad_op_interactive 
  ;


//top_level_stat
//  : assignment TERMINATOR                        # assignment_tls
//  | which=name ASSIGN macro_header body=compound # macro_def_tls
//  ;
  
assignment
  : which=name ASSIGN what=expr
  ;
  
//pad_op
//  : 'turn'? which=expr (ON | OFF)
//  | 'turn' (ON|OFF) which=expr
//  | TOGGLE which=expr   
//  ;
  
stat
  : assignment TERMINATOR  # assign_stat
//  | which=name ASSIGN macro_header body=compound # macro_def_stat
//  | pad_op TERMINATOR    # pad_op_stat
  | 'pause' duration=expr TERMINATOR           # pause_stat
  | expr TERMINATOR      # expr_stat
  | compound             # compound_stat
  ;
  
compound
  : '{' stat* '}'         # block
  | '[[' stat* ']]'       # par_block
  ;

expr 
  : '(' expr ')'  # paren_expr
  | '(' x=expr ',' y=expr ')' 		 # coord_expr
  | '-' rhs=expr                     # neg_expr
  | dist=expr direction              # delta_expr
  | INT rc[$INT.int]           # const_rc_expr
  | dist=expr rc[0]           # n_rc_expr
  | duration=expr time_unit          # time_expr
  | duration=expr ('tick' | 'ticks') # ticks_expr
  | lhs=expr (MUL | DIV) rhs=expr    # muldiv_expr 
  | lhs=expr (ADD | SUB) rhs=expr    # addsub_expr
  | direction dist=expr              # delta_expr
  | 'to' axis? which=expr            # to_expr
  | 'pause' duration=expr            # pause_expr
  | 'well' '#' which=expr            # well_expr
  | who=expr '[' which=expr ']'      # index_expr
  | well=expr ATTR 'gate'            # gate_expr
  | well=expr ATTR 'exit' 'pad'      # exit_pad_expr
  | 'drop' ('@' | 'at') loc=expr     # drop_expr 
  | who=expr INJECT what=expr        # injection_expr
  | macro_def                        # macro_expr
  | 'turn'? (ON | OFF)               # twiddle_expr
  | 'toggle' 'state'?                # twiddle_expr
  | 'the'? param_type                # type_name_expr
  | param_type n=INT                 # type_name_expr
  | name  '(' (args+=expr (',' args+=expr)*)? ')' # function_expr
  | name                             # name_expr
  | INT                              # int_expr
  ;


direction returns [Dir d, bool verticalp]
  : ('up' | 'north' ) {$ctx.d = Dir.UP}{$ctx.verticalp=True}
  | ('down' | 'south' ) {$ctx.d = Dir.DOWN}{$ctx.verticalp=True}
  | ('left' | 'west' ) {$ctx.d = Dir.LEFT}{$ctx.verticalp=False}
  | ('right' | 'east' ) {$ctx.d = Dir.RIGHT}{$ctx.verticalp=False}
  ;
  
rc[int n] returns [Dir d, bool verticalp]
  : {$n==1}? 'row' {$ctx.d = Dir.UP}{$ctx.verticalp=True}
  | 'rows' {$ctx.d = Dir.UP}{$ctx.verticalp=True}
  | {$n==1}? ('col' | 'column') {$ctx.d = Dir.RIGHT}{$ctx.verticalp=False}
  | ('cols' | 'columns') {$ctx.d = Dir.RIGHT}{$ctx.verticalp=False}
  ;
  
  
axis returns [bool verticalp]
  : 'row' {$ctx.verticalp=True}
  | ('col' | 'column') {$ctx.verticalp=False}
  ;
  
macro_def
  : macro_header (compound | expr)
  ;
  
macro_header
  : 'macro' '(' (param (',' param)*)? ')'
  ;
  
param returns[Type type, str pname, int n]
  : param_type {$ctx.type=$param_type.type} ( INT {$ctx.n=$INT.int} )?
  | name ':' param_type {$ctx.type=$param_type.type} {$ctx.pname=$name.text}
  ;
  
param_type returns[Type type]
  : 'drop' {$ctx.type=Type.DROP}
  | 'pad'  {$ctx.type=Type.PAD}
  | 'well' {$ctx.type=Type.WELL}
  | 'int'  {$ctx.type=Type.INT}
  ;
  
time_unit returns[Unit[Time] unit]
  : ('s' | 'sec' | 'secs' | 'second' | 'seconds') {$ctx.unit=SI.sec}
  | ('ms' | 'millisecond' | 'milliseconds') {$ctx.unit=SI.ms}
  ;

name : (ID | kwd_names) ;

kwd_names : '**__**';
  
ADD: '+';
ASSIGN: '=';
ATTR: '\'s';
DIV: '/';
INJECT: ':';
MUL: '*';
OFF: 'off';
ON: 'on';
SUB: '-';
TERMINATOR: ';';
TOGGLE: 'toggle';