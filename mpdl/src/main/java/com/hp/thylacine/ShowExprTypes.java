package com.hp.thylacine;

import java.io.IOException;

import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;


public class ShowExprTypes {

  public static void main(String[] args) throws IOException {
    CharStream input = CharStreams.fromFileName("expr.test");
    CommonLexer lexer = new CommonLexer(input);
    CommonTokenStream tokens = new CommonTokenStream(lexer);
    CommonParser parser = new CommonParser(tokens);
    ParseTree tree = parser.expr();
    
    ParseTreeWalker walker = new ParseTreeWalker();
    walker.walk(new ExprTypeAnnotator(tokens), tree);
    System.out.println();
    
  }

}
