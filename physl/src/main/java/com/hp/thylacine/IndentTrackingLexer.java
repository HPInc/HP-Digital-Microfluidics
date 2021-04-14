package com.hp.thylacine;

import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Stack;

import org.antlr.v4.runtime.CommonToken;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.Token;

public abstract class IndentTrackingLexer extends Lexer {
  public static int tab_size = 8;
  
  private Queue<Token> pending_tokens = new ArrayDeque<>();
  private Stack<Integer> margins = new Stack<>();
  private int pos_after_initial_ws = 0;
  
  private final int indent_token_type;
  private final int dedent_token_type;
  
  public IndentTrackingLexer(int dedent_token_type, int indent_token_type) {
    this.indent_token_type = indent_token_type;
    this.dedent_token_type = dedent_token_type;
  }

  private int current_margin() {
    return margins.empty() ? 0 : margins.peek();
  }
  
  @Override
  public void emit(Token token) {
    super.setToken(token);
    pending_tokens.offer(token);
  }
  
  @Override
  public Token emitEOF() {
    /*
     * If we hit the EOF and there are still indents, we need to 
     * emit dedents.
     */
    while (pending_tokens.poll() != null) {
      pending_tokens.offer(dedent_token());
    }
    /*
     * Now we call our super to get the actual EOF token, which will
     * be emitted (and put on the queue.
     */
    return super.emitEOF();
  }
  
  private Token dedent_token() {
    return new_token(dedent_token_type);
  }

  private Token indent_token() {
    return new_token(indent_token_type);
  }

  @Override
  public Token nextToken() {
    /*
     * If there's nothing pending, we match one, which will call
     * emit(token) and put it on the queue.  It may enqueue indents 
     * and dedents as well.
     */
    if (pending_tokens.isEmpty()) {
      super.nextToken();
    }
    /*
     * Now, we should definitely have something in the queue.  We'll
     * return the oldest.
     */
    assert !pending_tokens.isEmpty();
    return pending_tokens.poll();
  }
  
  public void handle_ws() {
    if (_tokenStartCharPositionInLine == 0) {
      int margin = 0;
      String text = getText();
      for (int i=0; i<text.length(); i++) {
        margin += 
            switch (text.charAt(i)) {
            case ' ' -> 1;
            case '\t' -> tab_size - margin % tab_size;
            default -> throw new IllegalArgumentException(String.format("Unknown whitespace char: %d",
                                                                        text.charAt(i)));
            };
      }
      pos_after_initial_ws = margin;
    }
  }
  
  public void indent_or_dedent_to(int margin) {
    if (at_beginning_of_line()) {
      if (margin > current_margin()) {
        emit(indent_token());
      } else {
        dedent_if_necessary_to(margin);
      }
    }
  }

  private void dedent_if_necessary_to(int margin) {
    while (margin < current_margin()) {
      emit(dedent_token());
      margins.pop();
    }
  }

  private boolean at_beginning_of_line() {
    return _tokenStartCharPositionInLine == pos_after_initial_ws;
  }

  public void dedent_to(int margin) {
    if (at_beginning_of_line()) {
      dedent_if_necessary_to(margin);
    }
  }
  
  private Token new_token(int tokenType, int channel, String text) {
    int charIndex = getCharIndex();
    CommonToken token = new CommonToken(_tokenFactorySourcePair, tokenType, channel, charIndex - text.length(), charIndex);
    token.setLine(getLine());
    token.setCharPositionInLine(getCharPositionInLine());
    token.setText(text);

    return token;
  }
  
  private Token new_token(int tokenType) {
    return new_token(tokenType, DEFAULT_TOKEN_CHANNEL, "");
  }
}
