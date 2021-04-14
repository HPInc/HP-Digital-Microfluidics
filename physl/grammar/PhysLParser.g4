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
  : 'Def' ':' ID block  
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
  | INT
  | FLOAT
  | name
  ;

attribute
  : name
  ;

kwd_name
  : BE | OWN
  ;

name: ID | kwd_name ;
  

label: (ID | INT);

  
