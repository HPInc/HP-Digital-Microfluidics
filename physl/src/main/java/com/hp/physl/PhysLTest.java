package com.hp.physl;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;

public class PhysLTest {

  public static void main(String[] args) throws IOException {
    CharStream input;
    Charset charset = StandardCharsets.UTF_8;
    if (args.length > 0) {
      String inputFile = args[0];
      input = CharStreams.fromFileName(inputFile, charset);
    } else {
      input = CharStreams.fromStream(System.in, charset);
    }
    PhysLLexer lexer = new PhysLLexer(input);
    CommonTokenStream tokens = new CommonTokenStream(lexer);
    PhysLParser parser = new PhysLParser(tokens);
    ParseTree tree = parser.program();
    System.out.println(tree.toStringTree(parser));
    
//    ParseTreeWalker walker = new ParseTreeWalker();
//    walker.walk(new ExprTypeAnnotator(tokens), tree);
  }

}
