grammar DMF;

import pathLexer;

options {
	language = Python3;
}

@header {
from mpam.types import Dir, OnOff, Turn
from langsup.type_supp import Type, Rel
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
  | 'if' tests+=expr bodies+=compound 
     ('else' 'if' tests+=expr bodies+=compound)*
     ('else' else_body=compound)?              # if_stat
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
  | obj=expr ATTR attr             # attr_expr
  | start_dir=expr 'turned' turn          # turn_expr
  | dist=expr 'in' ('dir' | 'direction') d=expr # in_dir_expr
  | INT rc[$INT.int]           # const_rc_expr
  | dist=expr rc[0]           # n_rc_expr
  | duration=expr time_unit          # time_expr
  | duration=expr ('tick' | 'ticks') # ticks_expr
  | amount=expr vol_unit             # vol_expr
  | amount=expr ('drop' | 'drops')   # drop_vol_expr
  | lhs=expr (MUL | DIV) rhs=expr    # muldiv_expr 
  | lhs=expr (ADD | SUB) rhs=expr    # addsub_expr
  | lhs=expr rel rhs=expr            # rel_expr
  | obj=expr 'has' ('a' | 'an') attr # has_expr
  | 'not' expr                       # not_expr
  | lhs=expr 'and' rhs=expr          # and_expr
  | lhs=expr 'or' rhs=expr           # or_expr
  | direction dist=expr              # delta_expr
  | direction                        # dir_expr
  | 'to' axis? which=expr            # to_expr
  | 'pause' duration=expr            # pause_expr
  | 'well' '#' which=expr            # well_expr
  | who=expr '[' which=expr ']'      # index_expr
  | 'drop' ('@' | 'at') loc=expr     # drop_expr 
  | who=expr INJECT what=expr        # injection_expr
  | first=expr 'if' cond=expr 'else' second=expr  # cond_expr
  | macro_def                        # macro_expr
  | 'turn'? (ON | OFF)               # twiddle_expr
  | 'toggle' 'state'?                # twiddle_expr
  | 'remove' ('from' 'the'? 'board')? # remove_expr
  | 'the'? param_type                # type_name_expr
  | param_type n=INT                 # type_name_expr
  | val=bool_val                     # bool_const_expr
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
  
turn returns [Turn t]
  : ('right' | 'clockwise') {$ctx.t = Turn.RIGHT}
  | ('left' | 'counterclockwise') {$ctx.t = Turn.LEFT}
  | 'around' {$ctx.t = Turn.AROUND}
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
  | 'well' 'pad' {$ctx.type=Type.WELL_PAD}
  | 'int'  {$ctx.type=Type.INT}
  | 'state' {$ctx.type=Type.BINARY_STATE}
  | 'component' {$ctx.type=Type.BINARY_CPT}
  | 'delta' {$ctx.type=Type.DELTA}
  | 'motion' {$ctx.type=Type.MOTION}
  | 'delay' {$ctx.type=Type.DELAY}
  | 'time' {$ctx.type=Type.TIME}
  | 'ticks' {$ctx.type=Type.TICKS}
  | 'bool' {$ctx.type=Type.BOOL}
  ;
  
time_unit returns[Unit[Time] unit]
  : ('s' | 'sec' | 'secs' | 'second' | 'seconds') {$ctx.unit=SI.sec}
  | ('ms' | 'millisecond' | 'milliseconds') {$ctx.unit=SI.ms}
  ;
  
vol_unit returns[Unit[Volume] unit]
  : ('uL' | 'ul' | 'microliter' | 'microlitre' | 'microliters' | 'microlitres') {$ctx.unit=SI.uL}
  | ('mL' | 'ml' | 'milliliter' | 'millilitre' | 'milliliters' | 'millilitres') {$ctx.unit=SI.mL}
  ;  
attr returns[str which]
  : 'gate' {$ctx.which="GATE"}
  | 'exit' 'pad' {$ctx.which="EXIT_PAD"}
  | 'state' {$ctx.which="STATE"}
  | 'distance' {$ctx.which="DISTANCE"}
  | 'duration' {$ctx.which="DURATION"}
  | 'pad' {$ctx.which="PAD"}
  | ('row' | 'y' ('coord' | 'coordinate')) {$ctx.which="ROW"}
  | ('col' | 'column' | 'x' ('coord' | 'coordinate')) {$ctx.which="COLUMN"}
  | 'well' {$ctx.which="WELL"}
  | 'exit' ('dir' | 'direction') {$ctx.which="EXIT_DIR"}
  | 'drop' {$ctx.which="DROP"}
  ;
  
rel returns[Rel which]
  : '==' {$ctx.which=Rel.EQ}
  | '!=' {$ctx.which=Rel.NE}
  | '<' {$ctx.which=Rel.LT}
  | '<=' {$ctx.which=Rel.LE}
  | '>' {$ctx.which=Rel.GT}
  | '>=' {$ctx.which=Rel.GE}
  ;
  
bool_val returns[bool val]
  : ('True' | 'true' | 'TRUE' | 'Yes' | 'yes' | 'YES') {$ctx.val=True}
  | ('False' | 'false' | 'FALSE' | 'No' | 'no' | 'NO') {$ctx.val=False}
  ;

name : (ID | kwd_names) ;

kwd_names : 's' | 'ms' | 'x' | 'y';
  
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
