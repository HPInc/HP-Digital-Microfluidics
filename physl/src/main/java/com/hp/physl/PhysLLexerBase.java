package com.hp.physl;

import org.antlr.v4.runtime.CharStream;

public abstract class PhysLLexerBase extends IndentTrackingLexer {

  public PhysLLexerBase(CharStream input) {
    super(input, PhysLLexer.INDENT, PhysLLexer.DEDENT);
  }


}
