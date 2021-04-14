parser grammar PhysLParser;

@header {
package com.hp.thylacine;
}

options {
	tokenVocab=PhysLLexer;
}

program: tlf+ EOF;

tlf
  : definition
  ;
  
definition
  : 'def' ':' ID block  ;
  

statement
  : simple_statement '.'
  | complex_statement
  ;
  
simple_statement
  : ID
  ;
  
complex_statement
  : 'if' expr ':' simple_or_block
     ('otherwise' ':' simple_or_block )?
  ;
  
expr : ID ;

simple_or_block
  : simple_statement
  | block
  ;
  
block
  : INDENT bulleted+ DEDENT
  ;
  
bulleted
  : '--' statement
  ;