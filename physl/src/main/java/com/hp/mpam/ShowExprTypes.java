package com.hp.mpam;

import java.io.IOException;

import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

import com.hp.thylacine.MPAMLexer;
import com.hp.thylacine.MPAMParser;


public class ShowExprTypes {

  public static void main(String[] args) throws IOException {
    CharStream input = CharStreams.fromFileName("expr.test");
    MPAMLexer lexer = new MPAMLexer(input);
    CommonTokenStream tokens = new CommonTokenStream(lexer);
    MPAMParser parser = new MPAMParser(tokens);
    ParseTree tree = parser.expr();
    
    ParseTreeWalker walker = new ParseTreeWalker();
    walker.walk(new ExprTypeAnnotator(tokens), tree);
    System.out.println();
    
  }

}
