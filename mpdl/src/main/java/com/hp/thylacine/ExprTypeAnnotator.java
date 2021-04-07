package com.hp.thylacine;

import java.io.PrintStream;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.function.Consumer;
import java.util.function.Supplier;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.misc.Interval;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeProperty;

import com.hp.thylacine.CommonParser.Addsub_exprContext;
import com.hp.thylacine.CommonParser.AttributeContext;
import com.hp.thylacine.CommonParser.Attribute_exprContext;
import com.hp.thylacine.CommonParser.Boolean_litContext;
import com.hp.thylacine.CommonParser.Boolean_literalContext;
import com.hp.thylacine.CommonParser.Capacity_attrContext;
import com.hp.thylacine.CommonParser.Col_attrContext;
import com.hp.thylacine.CommonParser.Current_vol_attrContext;
import com.hp.thylacine.CommonParser.Distance_exprContext;
import com.hp.thylacine.CommonParser.Edge_literalContext;
import com.hp.thylacine.CommonParser.Exit_pad_attrContext;
import com.hp.thylacine.CommonParser.ExprContext;
import com.hp.thylacine.CommonParser.Float_literalContext;
import com.hp.thylacine.CommonParser.Int_literalContext;
import com.hp.thylacine.CommonParser.List_exprContext;
import com.hp.thylacine.CommonParser.List_index_exprContext;
import com.hp.thylacine.CommonParser.Located_wellContext;
import com.hp.thylacine.CommonParser.Muldiv_exprContext;
import com.hp.thylacine.CommonParser.NameContext;
import com.hp.thylacine.CommonParser.Negation_exprContext;
import com.hp.thylacine.CommonParser.Numbered_regionContext;
import com.hp.thylacine.CommonParser.Numbered_wellContext;
import com.hp.thylacine.CommonParser.Pad_coordsContext;
import com.hp.thylacine.CommonParser.Prenthesized_exprContext;
import com.hp.thylacine.CommonParser.Quantity_exprContext;
import com.hp.thylacine.CommonParser.Row_attrContext;
import com.hp.thylacine.CommonParser.Singleton_regionContext;
import com.hp.thylacine.CommonParser.Singleton_wellContext;
import com.hp.thylacine.CommonParser.Variable_nameContext;

class ExprTypeAnnotator extends CommonBaseListener {
  
  final ParseTreeProperty<Type> types = new ParseTreeProperty<>();
  final ParseTreeProperty<String> descriptions = new ParseTreeProperty<>();
  final TokenStream tokens;
  
  public ExprTypeAnnotator(TokenStream tokens) {
    this.tokens = tokens;
  }
  

  String mark_open = ANSI.BLUE;
  String mark_close = ANSI.BLACK;
  String basic_open_mark = "«";
  String basic_close_mark = "»";
  String open_mark = mark_open+basic_open_mark+mark_close;
  String close_mark = mark_open+basic_close_mark+mark_close;
  String token_open = ANSI.BLACK+ANSI.BOLD;
  String token_close= ANSI.BOLD_OFF;
  String type_open = ANSI.MAGENTA+ANSI.ITALIC;
  String type_close= ANSI.BLACK+ANSI.ITALIC_OFF;
  String unknown_type_open = ANSI.RED+ANSI.ITALIC;
  String unknown_type_close = ANSI.BLACK+ANSI.ITALIC_OFF;
  String error_open = ANSI.YELLOW_BG;
  String error_close = ANSI.RESET;
  boolean spacesp = false;
  

  private Type noteType(ExprContext ctx, Type type) {
    types.put(ctx, type);
    StringBuilder s = new StringBuilder();
    int n = ctx.getChildCount();
    Interval my_interval = ctx.getSourceInterval();
    boolean simple = my_interval.a == my_interval.b;
    if (!simple) {
      s.append(open_mark);
      if (spacesp) { 
        s.append(" "); 
      }
    }
    int next_token = my_interval.a;
    String sep = "";
    for (int i=0; i<n; i++) {
      ParseTree tree = ctx.getChild(i);
      String desc = getDesc(tree);
      if (desc != null) {
        Interval child_interval = tree.getSourceInterval();
        sep = append_tokens(s, next_token, child_interval.a, sep);
        s.append(sep);
        sep = " ";
        s.append(desc);
        next_token = child_interval.b+1;
      }
    }
    append_tokens(s, next_token, my_interval.b+1, sep);
    if (!simple) {
//    s.append(ctx.getText());
      s.append(close_mark);
    }
    s.append(":");
    boolean flagp = (type == Type.UNKNOWN || type == Type.ILLEGAL);
    s.append(flagp ? unknown_type_open : type_open);
    s.append(type);
    s.append(flagp ? unknown_type_close : type_close);
    descriptions.put(ctx, s.toString());
    System.out.println(s);
//    System.out.println(String.format("{%s} has type %s", ctx.getText(), type));
    return type;
  }
  
  private String append_tokens(StringBuilder s, int from, int to, String sep) {
    for (int i=from; i<to; i++) {
      s.append(sep);
      sep = " ";
      Token t = tokens.get(i);
//      s.append("<");
      s.append(token_open);
      s.append(t.getText());
      s.append(token_close);
//      s.append("> ");
    }
    return sep;
  }
  
  static interface PrintStreamConsumer extends Consumer<PrintStream> {}
  
  void report_error(PrintStream out, String kind, Supplier<String> first_line,  
                    PrintStreamConsumer... more_lines) 
  {
    out.println(error_open+kind+error_close+" "+first_line.get());
    for (var fn : more_lines) {
      fn.accept(out);
    }
  }
  
  void report_error(PrintStream out, String kind, String first_line,
                    PrintStreamConsumer... more_lines) 
  {
    report_error(out, kind, ()->first_line, more_lines);
  }
  
  void report_error(String kind, Supplier<String> first_line,  
                    PrintStreamConsumer... more_lines)
  {
    report_error(System.out, kind, first_line, more_lines);
  }
  
  void report_error(String kind, String first_line,  
                    PrintStreamConsumer... more_lines)
  {
    report_error(System.out, kind, first_line, more_lines);
  }
  
  
  
  @SuppressWarnings("serial")
  class TypeError extends Exception {

    public TypeError(Type t, ExprContext ctx, Type[] allowed) {
      if (t != Type.ILLEGAL) {
        report_error("Type Error", getDesc(ctx),
                     (out)->{
                       String sep = "";
                       out.print("  Expected one of: ");
                       for (Type a : allowed) {
                         out.print(sep+a);
                         sep = ", ";
                 }
                       out.println();
                     });
      }
    }
    
  }
  
  Type getType(ExprContext ctx) {
    if (ctx == null) {
      return Type.MISSING; 
    }
    Type t = types.get(ctx);
    if (t == null) {
      return Type.UNKNOWN;
    }
    return t;
  }  

  Type getCheckedType(ExprContext ctx, Type... allowed) throws TypeError {
    Type t = getType(ctx);
    if (allowed.length == 0) {
      return t;
    }
    for (Type a : allowed) {
      if (a == t) {
        return t;
      }
    }
    throw new TypeError(t, ctx, allowed);
  }
  
  String getDesc(ParseTree tree) {
    return descriptions.get(tree);
  }

  static class TypeSig {
    final Type ret_type;
    final Type[] arg_types;
    
    TypeSig(Type rt, Type...ats) {
      ret_type = rt;
      arg_types = ats;
    }
    
    boolean matches(Type...param_types) {
      return Arrays.equals(arg_types, param_types);
    }
  }
  
  class SigChecker {
    final TypeSig[] sigs;
    final int arity;
    final Type[][] constraints;
    
    SigChecker(TypeSig...sigs) {
      this.sigs = sigs;
      Map<Integer, Set<Type>> map = new HashMap<>();
      for (TypeSig sig : sigs) {
        for (int i=0; i<sig.arg_types.length; i++) {
          Type type = sig.arg_types[i];
          if (type == null) {
            type = Type.MISSING;
          }
          Set<Type> set = map.get(i);
          if (set == null) {
            set = new HashSet<>();
            map.put(i, set);
          }
          set.add(type);
        }
      }
      arity = map.size();
      constraints = new Type[arity][];
      
      for (int i=0; i<arity; i++) {
        Set<Type> set = map.get(i);
        if (set.isEmpty()) {
          constraints[i] = new Type[0];
        } else {
          constraints[i] = set.toArray(new Type[set.size()]);
        }
      }
    }
    
    Type check(String op, ExprContext... params) {
      return check(()->op, params);
    }
    Type check(Supplier<String> op, ExprContext... params) {
      Type[] types = new Type[arity];
      for (int i=0; i<params.length; i++) {
        try {
          types[i] = getCheckedType(params[i], constraints[i]);
        } catch (TypeError e) {
          return Type.ILLEGAL;
        }
      }
      for (var sig : sigs) {
        if (sig.matches(types)) {
          return sig.ret_type;
        }
      }
      String ptype_descs = Arrays.stream(types).map(Type::toString).collect(Collectors.joining(", "));
      report_error("Type Error",
                   String.format("%s not defined on %s", op.get(), ptype_descs),
                   (out)->{
                     out.println("Params are ");
                     for (var p : params) {
                       String d = getDesc(p);
                       out.println("  "+d);
                     }
                   });
      return Type.ILLEGAL;
    }
        
  }

  
  
  @Override
  public void exitInt_literal(Int_literalContext ctx) {
    noteType(ctx, Type.INT);
  }
  
  final SigChecker 
  add_sigs = new SigChecker(new TypeSig(Type.INT, Type.INT, Type.INT),
                            new TypeSig(Type.FLOAT, Type.FLOAT, Type.FLOAT),
                            new TypeSig(Type.FLOAT, Type.INT, Type.FLOAT),
                            new TypeSig(Type.FLOAT, Type.FLOAT, Type.FLOAT),
                            new TypeSig(Type.ROW, Type.ROW, Type.INT),
                            new TypeSig(Type.ROW, Type.INT, Type.ROW),
                            new TypeSig(Type.COL, Type.COL, Type.INT),
                            new TypeSig(Type.COL, Type.INT, Type.COL));
  final SigChecker 
  sub_sigs = new SigChecker(new TypeSig(Type.INT, Type.INT, Type.INT),
                            new TypeSig(Type.FLOAT, Type.FLOAT, Type.FLOAT),
                            new TypeSig(Type.FLOAT, Type.INT, Type.FLOAT),
                            new TypeSig(Type.FLOAT, Type.FLOAT, Type.FLOAT),
                            new TypeSig(Type.ROW, Type.ROW, Type.INT),
                            new TypeSig(Type.COL, Type.COL, Type.INT),
                            new TypeSig(Type.INT, Type.COL, Type.COL),
                            new TypeSig(Type.INT, Type.ROW, Type.ROW));
                               
  @Override
  public void exitAddsub_expr(Addsub_exprContext ctx) {
    boolean is_add = ctx.op.getType() == CommonParser.PLUS;
    if (is_add) {
      noteType(ctx, add_sigs.check("+", ctx.lhs, ctx.rhs));
    } else {
      noteType(ctx, sub_sigs.check("-", ctx.lhs, ctx.rhs));
    }
  }


  @Override
  public void exitList_index_expr(List_index_exprContext ctx) {
    // TODO Auto-generated method stub
    noteType(ctx, Type.UNKNOWN);
  }

  final SigChecker
  negSigs = new SigChecker(new TypeSig(Type.INT, Type.INT),
                           new TypeSig(Type.FLOAT, Type.FLOAT));
  @Override
  public void exitNegation_expr(Negation_exprContext ctx) {
    noteType(ctx, negSigs.check("-", ctx.rhs));
  }

  @Override
  public void exitEdge_literal(Edge_literalContext ctx) {
    /*
     * I'm thinking that it might be a bit too constraining to have to
     * worry about rows and columns as a specific type.  For now, they'll all
     * be ints
     */
//    boolean is_row = ctx.ROW() != null; 
//    noteType(ctx, is_row ? Type.ROW : Type.COL);
    noteType(ctx, Type.INT);
  }

  @Override
  public void exitNumbered_region(Numbered_regionContext ctx) {
    noteType(ctx, Type.REGION);
  }

  @Override
  public void exitBoolean_literal(Boolean_literalContext ctx) {
    noteType(ctx, Type.BOOL);
  }

  @Override
  public void exitNumbered_well(Numbered_wellContext ctx) {
    noteType(ctx, Type.WELL);
  }

  
  final SigChecker
  exit_pad_attr_sigs = new SigChecker(new TypeSig(Type.PAD, Type.WELL));
  final SigChecker
  row_attr_sigs = new SigChecker(new TypeSig(Type.INT, Type.PAD));
  final SigChecker
  col_attr_sigs = new SigChecker(new TypeSig(Type.INT, Type.PAD));
  final SigChecker
  volume_attr_sigs = new SigChecker(new TypeSig(Type.VOLUME, Type.PAD),
                                    new TypeSig(Type.VOLUME, Type.WELL));
  final SigChecker
  capacity_attr_sigs = new SigChecker(new TypeSig(Type.VOLUME, Type.PAD),
                                      new TypeSig(Type.VOLUME, Type.WELL));
  
  @SuppressWarnings("preview")
  @Override
  public void exitAttribute_expr(Attribute_exprContext ctx) {
    AttributeContext att = ctx.attr;
    if (att instanceof Exit_pad_attrContext a) {
      noteType(ctx, exit_pad_attr_sigs.check(a.getText(), ctx.obj));
    } else if (att instanceof Row_attrContext a) {
        noteType(ctx, row_attr_sigs.check(a.getText(), ctx.obj));
    } else if (att instanceof Col_attrContext a) {
      noteType(ctx, col_attr_sigs.check(a.getText(), ctx.obj));
    } else if (att instanceof Current_vol_attrContext a) {
      noteType(ctx, volume_attr_sigs.check(a.getText(), ctx.obj));
    } else if (att instanceof Capacity_attrContext a) {
      noteType(ctx, capacity_attr_sigs.check(a.getText(), ctx.obj));
    } else {
      report_error("Unknown Attribute", "\""+att.getText()+"\"");
      noteType(ctx, Type.ILLEGAL);
    }
  }

  @Override
  public void exitSingleton_region(Singleton_regionContext ctx) {
    noteType(ctx, Type.REGION);
  }

  @Override
  public void exitDistance_expr(Distance_exprContext ctx) {
    noteType(ctx, Type.DIST);
  }

  @Override
  public void exitSingleton_well(Singleton_wellContext ctx) {
    noteType(ctx, Type.WELL);
  }

  @Override
  public void exitList_expr(List_exprContext ctx) {
    // TODO Auto-generated method stub
    noteType(ctx, Type.UNKNOWN);
  }

  @Override
  public void exitFloat_literal(Float_literalContext ctx) {
    noteType(ctx, Type.FLOAT);
  }

  static Pattern var_pat = Pattern.compile("(.*[^_0-9])_?[0-9]*");
  
  static Map<String, Type> var_types = new HashMap<>();
  static {
    var_types.put("b", Type.BOOL);
    var_types.put("i", Type.INT);
    var_types.put("f", Type.FLOAT);
    var_types.put("p", Type.PAD);
    var_types.put("pth", Type.PATH);
    var_types.put("r", Type.REGION);
    var_types.put("s", Type.STRING);
    var_types.put("temp", Type.TEMP);
    var_types.put("time", Type.TIME);
    var_types.put("vol", Type.VOLUME);
    var_types.put("w", Type.WELL);
  }
  
  @Override
  public void exitVariable_name(Variable_nameContext ctx) {
    String name = ctx.name().getText();
    Matcher m = var_pat.matcher(name);
    if (m.matches()) {
      String base = m.group(1);
      Type t = var_types.getOrDefault(base, Type.UNKNOWN);
      noteType(ctx, t);
    } else {
      noteType(ctx, Type.UNKNOWN);
    }
  }

  @Override
  public void exitPrenthesized_expr(Prenthesized_exprContext ctx) {
    Type inner_type = getType(ctx.expr());
    noteType(ctx, inner_type);
  }

  final SigChecker 
  mulDiv_sigs = new SigChecker(new TypeSig(Type.INT, Type.INT, Type.INT),
                               new TypeSig(Type.FLOAT, Type.FLOAT, Type.FLOAT),
                               new TypeSig(Type.FLOAT, Type.INT, Type.FLOAT),
                               new TypeSig(Type.FLOAT, Type.FLOAT, Type.FLOAT));
                               
  @Override
  public void exitMuldiv_expr(Muldiv_exprContext ctx) {
    noteType(ctx, mulDiv_sigs.check(()->ctx.op.getText(), ctx.lhs, ctx.rhs));
  }

  final SigChecker
  locatedWell_sigs = new SigChecker(new TypeSig(Type.WELL, Type.PAD));
  @Override
  public void exitLocated_well(Located_wellContext ctx) {
    noteType(ctx, locatedWell_sigs.check("well-at", ctx.loc));
  }

  final SigChecker
  coords_sigs = new SigChecker(new TypeSig(Type.PAD, Type.INT, Type.INT));
  @Override
  public void exitPad_coords(Pad_coordsContext ctx) {
    noteType(ctx, coords_sigs.check("(x,y)", ctx.row, ctx.col));
  }

  @Override
  public void exitQuantity_expr(Quantity_exprContext ctx) {
    try {
      getCheckedType(ctx.mag, Type.INT, Type.FLOAT);
      var unit = ctx.unit();
      if (unit.VOLUME_UNIT() != null) {
        noteType(ctx, Type.VOLUME);
      } else if (unit.TIME_UNIT() != null) {
        noteType(ctx, Type.TIME); 
      } else if (unit.TEMP_UNIT() != null) {
        noteType(ctx, Type.TEMP);
      } else if (unit.FREQ_UNIT() != null) {
        noteType(ctx, Type.FREQ);
      } else {
        report_error("Unknown unit", unit.getText());
        System.out.println(error_open+"Unknown unit:"+error_close+" "+unit.getText());
      }
    } catch (TypeError e) {
      noteType(ctx, Type.ILLEGAL);
    }
  }

  @Override
  public void exitExit_pad_attr(Exit_pad_attrContext ctx) {
    // TODO Auto-generated method stub
    super.exitExit_pad_attr(ctx);
  }

  @Override
  public void exitRow_attr(Row_attrContext ctx) {
    // TODO Auto-generated method stub
    super.exitRow_attr(ctx);
  }

  @Override
  public void exitCol_attr(Col_attrContext ctx) {
    // TODO Auto-generated method stub
    super.exitCol_attr(ctx);
  }

  @Override
  public void exitCurrent_vol_attr(Current_vol_attrContext ctx) {
    // TODO Auto-generated method stub
    super.exitCurrent_vol_attr(ctx);
  }

  @Override
  public void exitCapacity_attr(Capacity_attrContext ctx) {
    // TODO Auto-generated method stub
    super.exitCapacity_attr(ctx);
  }

  @Override
  public void exitBoolean_lit(Boolean_litContext ctx) {
    // TODO Auto-generated method stub
    super.exitBoolean_lit(ctx);
  }

  @Override
  public void exitName(NameContext ctx) {
    // TODO Auto-generated method stub
    super.exitName(ctx);
  }

  @Override
  public void exitEveryRule(ParserRuleContext ctx) {
    // TODO Auto-generated method stub
    super.exitEveryRule(ctx);
  }
  
  
}