grammar simple;

import pathLexer;

options {
	language = Python3;
}

@header {
from mpam.types import Dir 
from langsup.type_supp import Type
}


macro_file
  : top_level_stat* EOF
  ;


top_level_stat
  : which=name ASSIGN what=expr TERMINATOR   # assign_stat
  ;
  
stat
  : top_level_stat                   
  | expr TERMINATOR
  ;
  
compound
  : '{' stat* '}'         # block
  | '[[' stat* ']]'       # par_block
  ;

expr
  : '(' expr ')'                     # paren_expr
  | '(' x=expr ',' y=expr ')' 		 # coord_expr
  | '-' rhs=expr                     # neg_expr
  | who=expr '[' which=expr ']'      # index_expr
  | dist=expr direction              # delta_expr
  | lhs=expr (MUL | DIV) rhs=expr    # muldiv_expr
  | lhs=expr (ADD | SUB) rhs=expr    # addsub_expr
  | direction dist=expr              # delta_expr
  | 'to' axis? which=expr            # to_expr
  | 'well' '#' which=expr            # well_expr
  | 'drop' ('@' | 'at') loc=expr     # drop_expr
  | well=expr ATTR 'gate'            # gate_expr
  | who=expr INJECT what=expr        # injection_expr
  | macro_def                        # macro_expr
  | param_type ( n=INT )?            # type_name_expr
  | name  '(' args+=expr (',' args+=expr)* ')' # function_expr
  | name                             # name_expr
  | INT                              # int_expr
  ;


direction returns [Dir d, bool verticalp]
  : ('up' | 'north' ) {$ctx.d = Dir.UP}{$ctx.verticalp=True}
  | ('down' | 'south' ) {$ctx.d = Dir.DOWN}{$ctx.verticalp=True}
  | ('left' | 'west' ) {$ctx.d = Dir.LEFT}{$ctx.verticalp=False}
  | ('right' | 'east' ) {$ctx.d = Dir.RIGHT}{$ctx.verticalp=False}
  ;
  
axis returns [bool verticalp]
  : 'row' {$ctx.verticalp=True}
  | ('col' | 'column') {$ctx.verticalp=False}
  ;
  
macro_def
  : 'macro' '(' (param (',' param)*)? ')' compound
  ;
  
param returns[Type type, str pname, int n]
  : param_type {$ctx.type=$param_type.type} ( INT {$ctx.n=$INT.int} )?
  | name ':' param_type {$ctx.type=$param_type.type} {$ctx.pname=$name.text}
  ;
  
param_type returns[Type type]
  : 'drop' {$ctx.type=Type.DROP}
  | 'well' {$ctx.type=Type.WELL}
  | 'int'  {$ctx.type=Type.INT}
  ;

name : (ID | kwd_names) ;

kwd_names : '**__**';
  
ADD: '+';
ASSIGN: '=';
ATTR: '\'s';
DIV: '/';
INJECT: ':';
MUL: '*';
SUB: '-';
TERMINATOR: ';';