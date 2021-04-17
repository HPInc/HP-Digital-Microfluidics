parser grammar PhysLParser;

@header {
package com.hp.physl;
}

options {
	tokenVocab=PhysLLexer;
}

program: tlf+ EOF;

tlf
  : definition
  | 'Block' ':' block
  ;
  
definition
  : 'Let' new_kind 'be' nk_supers? ('.' | 'defined'? ':' nk_body)
  ;
  
new_kind
  : det adj=name? kind=name nk_generic_decls? ('(' nk_props ')')?
  ;
  
nk_generic_decls
  : '[' nk_generic_decl+ ']'
  ;

nk_generic_decl: prep generic_type_param;
   
generic_type_param
  : name '(' type ')'
  | type
  ;

nk_supers
  : new_kind_super (((',' new_kind_super)+ ','?)? 'and' new_kind_super)?
  ;
  
new_kind_super
  : a_type
  ;  
  
new_kind_adj
  : 'unique'
  ; 
  
nk_props
  : new_kind_prop (((',' new_kind_prop)+ ','?)? 'and' new_kind_prop)?
  ;
  
new_kind_prop
  : 'plural' 'is'? name
  ; 
  
nk_body : INDENT kind_def+ DEDENT ;  
  
kind_body
  : '.'
  | 'defined'? ':' INDENT kind_def+ DEDENT
  ;
  
kind_def
  : '--' it[true] 'has' new_att_names new_att_props? '.'
  ;     
  
new_att_props
  : '(' new_att_prop (',' new_att_prop)* ')'
  ;
  
new_att_prop
  : a_type
  | type /* For plurals */
  | 'by' 'default' expr
  | 'initially' expr
  ;  

new_att_names
  : new_att_name (((',' new_att_name)+ ','?)? 'and' new_att_name)?
  ;
  
/*
 * An att name declaration can have up to three names, at most one of which
 * is new information (the others must indicate a type).  We can't pick out 
 * which it is until the kinds have been declared.
 */
new_att_name
  : a_or_an new_att_flag* (name? name)? name
  ;
  
new_att_flag
  : 'unchangeable'
  ;  

statement
  : simple_statement '.'
  | complex_statement
  ;
  
simple_statement
  : 'Let' var=ID 'be' expr
  | ID
  ;
  
complex_statement
  : 'If' expr ':' simple_or_block
     ('Otherwise' ':' simple_or_block )?
  ;
  
simple_or_block
  : simple_statement
  | block
  ;
  
block
  : INDENT bulleted+ DEDENT
  ;
  
bulleted
  : '--' ('{' label '}')* statement
  ;
  
expr
  : '(' expr ')'
  | obj=expr APOSTROPHE_S attr=attribute
  | ('its' | 'it\'s') 'own'? attr=attribute
  | list=expr '[' index=expr ']'
  | 'not' rhs=expr
  | '-' rhs=expr
  | 'the' type
  | INT
  | FLOAT
  | name
  ;

attribute
  : name
  ;
  
type: adj=name? type_name=name generic_type_params? ;

/*
 * These types will likely be plural or generic type vars
 */
generic_type_params: '[' (prep type)+ ']';


prep: 'from' | 'to' | 'of' ;

a_type: a_or_an type ;

det : 'the' | a_or_an ;

a_or_an: 'a' | 'an' ;
  
it[boolean capp]
  : {$capp}? 'It'
  | 'it'
  ;  

kwd_name
  : 'a' | 'be' | 'count' | 'own' | 'unique'
  ;

name: ID | kwd_name ;
  

label: (ID | INT);

  
