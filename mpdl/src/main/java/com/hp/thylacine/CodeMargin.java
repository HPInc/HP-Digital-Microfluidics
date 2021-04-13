package com.hp.thylacine;
import java.util.HashMap;
import java.util.Map;

import org.antlr.v4.runtime.Token;

public class CodeMargin {
  static class LineIndent {
    int ws_chars = 0;
    int visible_pos = 0;
  }
  
  static LineIndent current_line;
  static Map<Integer, LineIndent> line_indents = new HashMap<>();
  static final int tab_size = 8;
  static int line_num = 0;
  
  static {
    see_newline();
  }
  
  public static void see_space_at (int pos) {
    if (pos == current_line.ws_chars) {
      current_line.ws_chars++;
      current_line.visible_pos++;
    }
  }
  
  public static void see_tab_at (int pos) {
    if (pos == current_line.ws_chars) {
      current_line.ws_chars++;
      int pad = 8-current_line.visible_pos;
      current_line.visible_pos += pad;
    }
  }
  
  public static void see_newline() {
    line_num++;
    current_line = new LineIndent();
    line_indents.put(line_num, current_line);
  }
  
  public static int margin_for(int line) {
    return line_indents.get(line).visible_pos;
  }
  
  public static int indent_level(Token token) {
    int line = token.getLine();
    int pos = token.getCharPositionInLine();
    LineIndent indent = line_indents.get(line);
    return pos+indent.visible_pos-indent.ws_chars;
  }
  
  public static boolean indented_at_least(int margin, Token token) {
    return indent_level(token) >= margin;
  }
}
