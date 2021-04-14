grammar Test;

@header {
import com.hp.thylacine.CodeMargin;
import java.util.Stack;
}

@parser::members {
final Stack<Integer> margins = new Stack<>();
final Stack<String> scope_descs = new Stack<>();

void enter_complex(Token kwd, String desc) {
	int margin = CodeMargin.indent_level(kwd);
	margins.push(margin);
	System.out.format("Entering %s on line %d, margin = %d%n", desc, kwd.getLine(), margin);
	scope_descs.push(desc);
}
void enter_complex(Token kwd) {
	enter_complex(kwd, kwd.getText());
}
void exit_complex() {
	margins.pop();
	String margin = margins.empty() ? "NONE" : margins.peek().toString();
	System.out.format("Exiting %s, margin now %s%n", scope_descs.pop(), margin);
}

int current_margin() {
	return margins.peek();
}

boolean stat_indent_ok(Token t) {
	if (margins.empty()) {
		return false;
	}
	int i = CodeMargin.indent_level(t);
	int m = current_margin();
	boolean val = i >= current_margin();
	if (val) {
		System.out.format("Statement %s on line %d, pos %d, margin = %d%n",
			t.getText(), t.getLine(), i, m);
	} else {
		System.out.format("Not a statement %s on line %d, pos %d, margin = %d%n",
			t.getText(), t.getLine(), i, m);
	}
	return val;
}
boolean kwd_indent_ok(Token t, String expected) {
	if (margins.empty()) {
		return false;
	}
	int i = CodeMargin.indent_level(t);
	int m = current_margin();
	boolean val = i >= current_margin();
	if (val) {
		System.out.format("Kwd %s <%s> on line %d, pos %d, margin = %d%n",
			t.getText(), expected, t.getLine(), i, m);
	} else {
		System.out.format("Not a kwd %s <%s> on line %d, pos %d, margin = %d%n",
			t.getText(), expected, t.getLine(), i, m);
	}
	return val;
}
	
}

stat
: kwd='for' ID ':' {enter_complex($kwd); } block_or_statement {exit_complex();}
| kwd='if' ID ':' {enter_complex($kwd); } block_or_statement 
  elsif_clause? 
 else_clause?
 {exit_complex();}
| ID
;

else_clause
: {kwd_indent_ok(getCurrentToken(), "else")}?
  kwd='otherwise' ':'
  block_or_statement
;

elsif_clause
: {kwd_indent_ok(getCurrentToken(), "elsif")}?
  kwd='otherwise if' ID ':'
  block_or_statement
;

block_or_statement
: stat
| block 'hi'
;

block
: ({stat_indent_ok(getCurrentToken())}?
   bullet='--'  last_stat=stat
	{System.out.format("Indent: %d, Margin: %d, Text: %s%n", 
		CodeMargin.indent_level($bullet), current_margin(), $last_stat.text);})+
; 


ID: [a-zA-Z][a-zA-Z0-9_]*;

SPACE: ' ' { CodeMargin.see_space_at(_tokenStartCharPositionInLine); } -> skip;
TAB: '\t' { CodeMargin.see_tab_at(_tokenStartCharPositionInLine); } -> skip;
NL: '\n' { CodeMargin.see_newline(); } -> skip;
CR: '\r' -> skip;

COMMENT: '//' (~'\n')* -> skip;