grammar Indent;

@header {
import com.hp.thylacine.CodeMargin;
}


stat
  locals [int x]
  : kwd='for-header' {System.out.println("In for");} block_or_statement[$kwd.line] {System.out.println("out of for");}
  | ID {System.out.println($ID.text);}  
  ;
 
block_or_statement [int enclosing_line]
  : stat {$stat::x > 0}?
  | block[$enclosing_line] 
  ;

block[int enclosing_line]
  : (bullet='--' {CodeMargin.margin_for($bullet.line) >= CodeMargin.margin_for($enclosing_line)}? stas+=stat)+
//  |
  ;
  
mumble: 'mumble';  
  

ID: [a-zA-Z][a-zA-Z0-9_]*;

SPACE: ' ' { CodeMargin.see_space_at(_tokenStartCharPositionInLine); } -> skip;
TAB: '\t' { CodeMargin.see_tab_at(_tokenStartCharPositionInLine); } -> skip;
NL: '\n' { CodeMargin.see_newline(); } -> skip;
CR: '\r' -> skip;
