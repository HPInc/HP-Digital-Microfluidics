grammar DMF;

import pathLexer;

options {
	language = Python3;
}

@header {
from mpam.types import Dir, OnOff, Turn, ticks, unknown_reagent, waste_reagent
from langsup.type_supp import Type, Rel, PhysUnit, EnvRelativeUnit
from quantities import SI
}


macro_file
  : stat* EOF 
  ;
  
interactive
  : compound EOF  # compound_interactive
  | declaration TERMINATOR? EOF # decl_interactive
//  | assignment TERMINATOR? EOF # assignment_interactive
  | printing TERMINATOR? EOF # print_interactive
  | expr TERMINATOR? EOF # expr_interactive
  | EOF # empty_interactive
//  | pad_op EOF # pad_op_interactive 
  ;


//top_level_stat
//  : assignment TERMINATOR                        # assignment_tls
//  | which=name ASSIGN macro_header body=compound # macro_def_tls
//  ;
  
//assignment
//  : which=name (':' param_type)? ASSIGN what=expr           # name_assignment
////  | obj=expr ATTR attr ASSIGN what=expr   # attr_assignment
//  ;
  
declaration returns [Optional[Type] type, str pname, int n]
  : LOCAL name ASSIGN init=expr
  	{$ctx.pname=$name.text}
  	{$ctx.type=None} 
  | LOCAL? param_type INT ASSIGN init=expr? 
  	{$ctx.type=$param_type.type}
  	{$ctx.n=$INT.int}
  | LOCAL param_type INT
  	{$ctx.type=$param_type.type}
  	{$ctx.n=$INT.int}
  | LOCAL? param_type name (ASSIGN init=expr)? 
  	{$ctx.type=$param_type.type}
  	{$ctx.pname=$name.text}
  ;
  
printing : 'print' vals+=expr (',' vals+=expr)* ;
  
//pad_op
//  : 'turn'? which=expr (ON | OFF)
//  | 'turn' (ON|OFF) which=expr
//  | TOGGLE which=expr   
//  ;
  
stat
  : declaration TERMINATOR # decl_stat
//  | assignment TERMINATOR  # assign_stat
//  | which=name ASSIGN macro_header body=compound # macro_def_stat
//  | pad_op TERMINATOR    # pad_op_stat
  | 'pause' duration=expr TERMINATOR           # pause_stat
  | printing TERMINATOR                           # print_stat
  | 'if' tests+=expr bodies+=compound 
     ('else' 'if' tests+=expr bodies+=compound)*
     ('else' else_body=compound)?              # if_stat
  | expr TERMINATOR      # expr_stat
  | loop                 # loop_stat
  | compound             # compound_stat
  ;
  
compound
  : '{' stat* '}'         # block
  | '[[' stat* ']]'       # par_block
  ;
  
loop
  : 'repeat' n=expr 'times' body=stat   # repeat_loop
  | 'for' var=name 'in' '[' start=expr ',' stop=expr term_punct ('by' step=expr) body=stat # for_loop
  ;
  
term_punct returns [bool is_closed]
  : ']' {$ctx.is_closed=True}
  | ')' {$ctx.is_closed=False}
  ;

expr 
  : '(' expr ')'  # paren_expr
  | func=expr  '(' (args+=expr (',' args+=expr)*)? ')' # function_expr
  | '(' x=expr ',' y=expr ')' 		 # coord_expr
  | '-' rhs=expr                     # neg_expr
  | dist=expr direction              # delta_expr
  | 'well' '#' which=expr            # well_expr
  | 'heater' '#' which=expr			 # heater_expr
  | quant=expr ATTR 'magnitude' 'in' dim_unit # magnitude_expr
  | quant=expr 'as' 'a'? 'string' 'in' dim_unit # unit_string_expr
  | obj=expr ATTR attr             # attr_expr
  | start_dir=expr 'turned' turn          # turn_expr
  | dist=expr 'in' ('dir' | 'direction') d=expr # in_dir_expr
  | INT rc[$INT.int]           # const_rc_expr
  | dist=expr rc[0]           # n_rc_expr
  | amount=expr dim_unit             # unit_expr
  | amount=expr 'C'					 # temperature_expr
  | 'the'? (reagent 'reagent'?)		 # reagent_lit_expr
  | ('the' | 'a')? 'reagent' 'named'? which=expr # reagent_expr
  | vol=expr 'of' which=expr       # liquid_expr
  | lhs=expr (MUL | DIV) rhs=expr    # muldiv_expr 
  | lhs=expr (ADD | SUB) rhs=expr    # addsub_expr
  | lhs=expr rel rhs=expr            # rel_expr
  | obj=expr 'has' ('a' | 'an') attr # has_expr
  | obj=expr 'is' NOT? pred=expr     # is_expr
  | 'not' expr                       # not_expr
  | lhs=expr 'and' rhs=expr          # and_expr
  | lhs=expr 'or' rhs=expr           # or_expr
  | direction dist=expr              # delta_expr
  | direction                        # dir_expr
  | 'to' axis? which=expr            # to_expr
  | 'pause' duration=expr            # pause_expr
  | who=expr '[' which=expr ']'      # index_expr
  | 'drop' ('@' | 'at') loc=expr     # drop_expr 
  | vol=expr ('@' | 'at') loc=expr   # drop_expr
  | who=expr INJECT what=expr        # injection_expr
  | first=expr 'if' cond=expr 'else' second=expr  # cond_expr
  | macro_def                        # macro_expr
  | no_arg_action                    # action_expr
//  | 'turn'? (ON | OFF)               # twiddle_expr
//  | 'toggle' 'state'?                # twiddle_expr
//  | 'remove' ('from' 'the'? 'board')? # remove_expr
  | 'the'? param_type                # type_name_expr
  | param_type n=INT                 # type_name_expr
  | val=bool_val                     # bool_const_expr
//  | 'reagent' STRING                 # reagent_expr
//  | name  '(' (args+=expr (',' args+=expr)*)? ')' # function_expr
  | name                             # name_expr
  | multi_word_name                  # mw_name_expr
  | which=name ASSIGN what=expr    # name_assign_expr
  | obj=expr ATTR attr ASSIGN what=expr  # attr_assign_expr
  | ptype=param_type n=INT ASSIGN what=expr # name_assign_expr
  | string # string_lit_expr
  | INT                              # int_expr
  | FLOAT							 # float_expr
  ;

reagent returns [Reagent r]
  : 'unknown' {$ctx.r = unknown_reagent}
  | 'waste' {$ctx.r = waste_reagent}
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
  
param returns[Type type, str pname, int n, bool deprecated]
  : ('a' | 'an')? param_type {$ctx.type=$param_type.type} 
  | param_type {$ctx.type=$param_type.type} INT {$ctx.n=$INT.int} 
  | param_type name {$ctx.type=$param_type.type} {$ctx.pname=$name.text}
  | name ':' param_type {$ctx.type=$param_type.type} {$ctx.pname=$name.text} {$ctx.deprecated=True}
  ;
  
no_arg_action returns[str which]
  : 'turn'? ON {$ctx.which="TURN-ON"}
  | 'turn'? OFF {$ctx.which="TURN-OFF"}
  | 'toggle' 'state'? {$ctx.which="TOGGLE"}
  | 'remove' ('from' 'the'? 'board')? {$ctx.which="REMOVE-FROM-BOARD"}
  ;
  
param_type returns[Type type]
  : 'drop' {$ctx.type=Type.DROP}
  | 'pad'  {$ctx.type=Type.PAD}
  | 'well' {$ctx.type=Type.WELL}
  | 'well' 'pad' {$ctx.type=Type.WELL_PAD}
  | 'well'? 'gate' {$ctx.type=Type.WELL_GATE} 
  | 'int'  {$ctx.type=Type.INT}
  | 'float' {$ctx.type=Type.FLOAT}
  | 'string' {$ctx.type=Type.STRING}
  | 'state' {$ctx.type=Type.BINARY_STATE}
  | 'electrode' {$ctx.type=Type.BINARY_CPT}
  | 'delta' {$ctx.type=Type.DELTA}
  | 'motion' {$ctx.type=Type.MOTION}
  | 'delay' {$ctx.type=Type.DELAY}
  | 'time' {$ctx.type=Type.TIME}
  | 'ticks' {$ctx.type=Type.TICKS}
  | 'bool' {$ctx.type=Type.BOOL}
  | ('direction' | 'dir') {$ctx.type=Type.DIR}
  | 'volume' {$ctx.type=Type.VOLUME}
  | 'reagent' {$ctx.type=Type.REAGENT}
  | 'liquid' {$ctx.type=Type.LIQUID}
  | ('temp' | 'temperature') ('diff' | 'difference' | 'delta') {$ctx.type=Type.REL_TEMP}
  | ('temp' | 'temperature') 'point'? {$ctx.type=Type.ABS_TEMP}
  ;
  
dim_unit returns[PhysUnit unit]
  : ('s' | 'sec' | 'secs' | 'second' | 'seconds') {$ctx.unit=SI.sec}
  | ('ms' | 'millisecond' | 'milliseconds') {$ctx.unit=SI.ms}
  | ('uL' | 'ul' | 'microliter' | 'microlitre' | 'microliters' | 'microlitres') {$ctx.unit=SI.uL}
  | ('mL' | 'ml' | 'milliliter' | 'millilitre' | 'milliliters' | 'millilitres') {$ctx.unit=SI.mL}
  | ('tick' | 'ticks') {$ctx.unit=ticks}
  | ('drop' | 'drops') {$ctx.unit=EnvRelativeUnit.DROP}
  ;

attr returns[str which]
  : 'exit' 'pad' {$ctx.which="#exit_pad"}
  | 'gate' {$ctx.which="gate"}
  | ('dir' | 'direction') {$ctx.which="direction"}
  | ('row' | 'y' ('coord' | 'coordinate')) {$ctx.which="row"}
  | ('col' | 'column' | 'x' ('coord' | 'coordinate')) {$ctx.which="column"}
  | 'exit' ('dir' | 'direction') {$ctx.which="#exit_dir"}
  | 'remaining' 'capacity' {$ctx.which="#remaining_capacity"}
  | 'target' ('temp' | 'temperature')? {$ctx.which="#target_temperature"}
  | 'current'? ('temp' | 'temperature') {$ctx.which="#current_temperature"}
  | n=('drop' | 'pad' | 'well' | 'volume' | 'reagent' | ID)
  	{$ctx.which=$n.text}
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

name returns[str val]
  : multi_word_name {$ctx.val=$multi_word_name.val}
  | ID {$ctx.val=$ID.text}
  | kwd_names {$ctx.val=$kwd_names.text}
  ;
  
multi_word_name returns[str val]
  : 'on' 'the'? 'board' {$ctx.val="on board"}
  | 'interactive' 'reagent' {$ctx.val="interactive reagent"}
  | 'interactive' 'volume' {$ctx.val="interactive volume"}
  ;

kwd_names : 's' | 'ms' | 'x' | 'y'
  | 'diff' | 'difference' | 'delta' | 'point'
  ;

string : STRING ;
  
ADD: '+';
ASSIGN: '=';
ATTR: '\'s';
DIV: '/';
INTERACTIVE: 'interactive';
INJECT: ':';
LOCAL: 'local';
MUL: '*';
NOT: 'not';
OFF: 'off';
ON: 'on';
SUB: '-';
TERMINATOR: ';';
TOGGLE: 'toggle';
CLOSE_BRACKET: ']';
CLOSE_PAREN: ')';
