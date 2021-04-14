package com.hp.thylacine;

import java.io.PrintStream;
import java.util.Arrays;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.function.Consumer;
import java.util.function.Supplier;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.misc.Interval;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeProperty;

import com.hp.thylacine.MPAMParser.Addsub_exprContext;
import com.hp.thylacine.MPAMParser.And_exprContext;
import com.hp.thylacine.MPAMParser.AttributeContext;
import com.hp.thylacine.MPAMParser.Attribute_exprContext;
import com.hp.thylacine.MPAMParser.Boolean_literalContext;
import com.hp.thylacine.MPAMParser.Current_obj_litContext;
import com.hp.thylacine.MPAMParser.Delta_exprContext;
import com.hp.thylacine.MPAMParser.Distance_exprContext;
import com.hp.thylacine.MPAMParser.Edge_literalContext;
import com.hp.thylacine.MPAMParser.ExprContext;
import com.hp.thylacine.MPAMParser.Float_literalContext;
import com.hp.thylacine.MPAMParser.Horizontal_relposContext;
import com.hp.thylacine.MPAMParser.In_region_relContext;
import com.hp.thylacine.MPAMParser.Int_literalContext;
import com.hp.thylacine.MPAMParser.List_exprContext;
import com.hp.thylacine.MPAMParser.List_index_exprContext;
import com.hp.thylacine.MPAMParser.Muldiv_exprContext;
import com.hp.thylacine.MPAMParser.Negation_exprContext;
import com.hp.thylacine.MPAMParser.Not_exprContext;
import com.hp.thylacine.MPAMParser.Op_callContext;
import com.hp.thylacine.MPAMParser.Or_exprContext;
import com.hp.thylacine.MPAMParser.Order_exprContext;
import com.hp.thylacine.MPAMParser.Pad_coordsContext;
import com.hp.thylacine.MPAMParser.Prenthesized_exprContext;
import com.hp.thylacine.MPAMParser.PropertyContext;
import com.hp.thylacine.MPAMParser.Property_exprContext;
import com.hp.thylacine.MPAMParser.Quantity_exprContext;
import com.hp.thylacine.MPAMParser.Region_by_numContext;
import com.hp.thylacine.MPAMParser.Region_selector_exprContext;
import com.hp.thylacine.MPAMParser.RelationContext;
import com.hp.thylacine.MPAMParser.Relation_exprContext;
import com.hp.thylacine.MPAMParser.RelposContext;
import com.hp.thylacine.MPAMParser.Relpos_exprContext;
import com.hp.thylacine.MPAMParser.Room_temp_litContext;
import com.hp.thylacine.MPAMParser.Singleton_regionContext;
import com.hp.thylacine.MPAMParser.Singleton_wellContext;
import com.hp.thylacine.MPAMParser.UnitContext;
import com.hp.thylacine.MPAMParser.Unit_count_attrContext;
import com.hp.thylacine.MPAMParser.User_defined_attrContext;
import com.hp.thylacine.MPAMParser.User_defined_relContext;
import com.hp.thylacine.MPAMParser.Variable_nameContext;
import com.hp.thylacine.MPAMParser.Vertical_relposContext;
import com.hp.thylacine.MPAMParser.Well_by_num_or_padContext;
import com.hp.thylacine.MPAMParser.Well_selector_exprContext;

class ExprTypeAnnotator extends MPAMBaseListener {
  
  final ParseTreeProperty<Type> types = new ParseTreeProperty<>();
  final ParseTreeProperty<String> descriptions = new ParseTreeProperty<>();
  final ParseTreeProperty<ExprContext> relation_rhs = new ParseTreeProperty<>();
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
  
  String with_spaces(ParseTree name) {
    Interval interval = name.getSourceInterval();
    StringBuilder s = new StringBuilder();
    String sep = "";
    for (int i = interval.a; i<=interval.b; i++) {
      s.append(sep);
      sep = " ";
      s.append(tokens.get(i).getText());
    }
    return s.toString();
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
                       out.print("  Expected ");
                       if (allowed.length == 1) {
                         out.println(allowed[0]);
                       } else if (allowed.length == 2) {
                         out.format("%s or %s%n", allowed[0], allowed[1]);
                       } else {
                         out.print("one of: ");
                         for (Type a : allowed) {
                           out.print(sep+a);
                           sep = ", ";
                         }
                         out.println();
                       }
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
      if (t.dominated_by(a)) {
        return t;
      }
    }
    throw new TypeError(t, ctx, allowed);
  }
  
  String getDesc(ParseTree tree) {
    return descriptions.get(tree);
  }
  
  static interface TypeSigBase {
    int arity();
    /*
     * Returns null if it doesn't match, return type otherwise
     */
    Type matches(Type...param_types);
    void add_arg_types_to(Set<Type> set, int i);
  }

  static class TypeSig implements TypeSigBase {
    final Type ret_type;
    final Type[] arg_types;
    final int arity;
    
    TypeSig(Type rt, Type...ats) {
      ret_type = rt;
      arg_types = ats;
      arity = ats.length;
    }
    
    @Override
    public Type matches(Type...param_types) {
      if (param_types.length != arity) {
        return null;
      }
      for (int i=0; i<arity; i++) {
        if (!param_types[i].dominated_by(arg_types[i])) {
          return null;
        }
      }
      return ret_type;
    }

    @Override
    public void add_arg_types_to(Set<Type> set, int i) {
      Type t = arg_types[i];
      if (t == null) {
        t = Type.MISSING;
      }
      set.add(t);
    }

    @Override
    public int arity() {
      return arg_types.length;
    }

  }
  
  static class SymmetricTypeSig implements TypeSigBase {
    private final Type ret_type;
    private final Type t1;
    private final Type t2;
    public SymmetricTypeSig(Type ret_type, Type t1, Type t2) {
      this.ret_type = ret_type;
      this.t1 = t1;
      this.t2 = t2;
    }
    
    @Override
    public
    Type matches(Type... param_types) {
      if (param_types.length == 2
          && ((param_types[0].dominated_by(t1) && param_types[1].dominated_by(t2))
              || (param_types[0].dominated_by(t2) && param_types[1].dominated_by(t1))))
      {
        return ret_type;
      }
      return null;
    }
    
    @Override
    public void add_arg_types_to(Set<Type> set, int i) {
      set.add(t1);
      set.add(t2);
    }

    @Override
    public int arity() {
      return 2;
    }
  }
  
  class TypePreservingSig implements TypeSigBase {
    final int arity;
    final EnumSet<Type> types;
    
    public TypePreservingSig(int arity, Type first, Type...rest) {
      this.arity = arity;
      types = EnumSet.of(first, rest);
    }

    @Override
    public int arity() {
      return arity;
    }
    
    private boolean acceptable(Type t) {
      for (Type a : types) {
        if (t.dominated_by(a)) {
          return true;
        }
      }
      return false;
    }

    @Override
    public Type matches(Type... param_types) {
      if (param_types.length == 0) {
        return null;
      }
      Type highest = param_types[0];
      if (!acceptable(highest)) {
        return null;
      }
      for (int i=1; i<param_types.length; i++) {
        Type pt = param_types[i];
        if (!pt.dominated_by(highest)) {
          Type lcd = highest.lowest_common_dominator(pt);
          if (acceptable(lcd)) {
            highest = lcd;
          } else {
            return null;
          }
        }
      }
      return highest;
    }

    @Override
    public void add_arg_types_to(Set<Type> set, int i) {
      set.addAll(types);
    }
    
  }
  
  
  class SigChecker {
    final TypeSigBase[] sigs;
    final int arity;
    final Type[][] constraints;
    
    SigChecker(TypeSigBase...sigs) {
      this.sigs = sigs;
      Map<Integer, Set<Type>> map = new HashMap<>();
      for (TypeSigBase sig : sigs) {
        for (int i=0; i<sig.arity(); i++) {
          Set<Type> set = map.get(i);
          if (set == null) {
            set = new HashSet<>();
            map.put(i, set);
          }
          sig.add_arg_types_to(set, i);
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
        Type ret_type = sig.matches(types);
        if (ret_type != null) {
          return ret_type;
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

  
  private Type unit_type(UnitContext uc) {
    if (uc.VOLUME_UNIT() != null) {
      return Type.VOLUME;
    } else if (uc.TIME_UNIT() != null) {
      return Type.TIME;
    } else if (uc.TEMP_UNIT() != null) {
      return Type.TEMP;
    } else if (uc.FREQ_UNIT() != null) {
      return Type.FREQ;
    } 
    return Type.UNKNOWN;
  }
  
  @Override
  public void exitInt_literal(Int_literalContext ctx) {
    noteType(ctx, Type.INT);
  }
  
  final SigChecker 
  add_sigs = new SigChecker(new TypePreservingSig(2, Type.FLOAT, 
                                                  Type.PADS,
                                                  Type.DELTA2D,
                                                  Type.REGION),
                            new SymmetricTypeSig(Type.PAD, Type.PAD, Type.DELTA2D)
                            );
  final SigChecker 
  sub_sigs = new SigChecker(new TypePreservingSig(2, Type.FLOAT, 
                                                  Type.PADS,
                                                  Type.DELTA2D,
                                                  Type.REGION),
                            new SymmetricTypeSig(Type.PAD, Type.PAD, Type.DELTA2D),
                            new TypeSig(Type.DELTA2D, Type.PAD, Type.PAD)
                            );
  @Override
  public void exitAddsub_expr(Addsub_exprContext ctx) {
    boolean is_add = ctx.op.getType() == MPAMParser.PLUS;
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
  negSigs = new SigChecker(new TypePreservingSig(1, Type.INT, Type.FLOAT));
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

  final SigChecker
  regionSelector_sigs = new SigChecker(new TypeSig(Type.REGION, Type.INT));
  @Override
  public void exitRegion_selector_expr(Region_selector_exprContext ctx) {
    var sel = ctx.region_selector();
    if (sel instanceof Region_by_numContext s) {
      noteType(ctx, regionSelector_sigs.check("region[]", s.expr()));
    } else {
      report_error("Unhandled selector", sel.getText());
      noteType(ctx, Type.REGION);
    }
  }
  

  @Override
  public void exitBoolean_literal(Boolean_literalContext ctx) {
    noteType(ctx, Type.BOOL);
  }
  
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
  
  final Map<String, SigChecker> attribute_sigs = new HashMap<>();
  {
    attribute_sigs.put("exit pad", new SigChecker(new TypeSig(Type.PAD, Type.WELL)));
    attribute_sigs.put("volume", new SigChecker(new TypeSig(Type.VOLUME, Type.WELL),
                                                new TypeSig(Type.VOLUME, Type.PAD)));
    attribute_sigs.put("current volume", attribute_sigs.get("volume"));
    attribute_sigs.put("row", new SigChecker(new TypeSig(Type.INT, Type.PAD)));
    attribute_sigs.put("col", attribute_sigs.get("row"));
    attribute_sigs.put("column", attribute_sigs.get("col"));
    attribute_sigs.put("capacity", new SigChecker(new TypeSig(Type.VOLUME, Type.PAD),
                                                  new TypeSig(Type.VOLUME, Type.WELL)));
  }
  
  @Override
  public void exitAttribute_expr(Attribute_exprContext ctx) {
    AttributeContext att = ctx.attr;
    if (att instanceof Unit_count_attrContext a) {
      Type t = unit_type(a.unit());
      if (t== Type.UNKNOWN) {
        report_error("Unhandled unit", with_spaces(a.unit()));
      } else {
        try {
          getCheckedType(ctx.obj, t);
          noteType(ctx, Type.FLOAT);
        } catch (TypeError e) {
          noteType(ctx, Type.ILLEGAL);
        }
      }
    } else if (att instanceof User_defined_attrContext c) {
      String att_name = with_spaces(c.name());
      SigChecker sigs = attribute_sigs.get(att_name);
      if (sigs != null) {
        noteType(ctx, sigs.check(att_name, ctx.obj));
      } else {
        report_error("Unhandled (user-defined?) Attribute", att_name);
        noteType(ctx, Type.UNKNOWN);
      }
    } else {
      report_error("Unhandled Attribute", "\""+with_spaces(att)+"\"");
      noteType(ctx, Type.ILLEGAL);
    }
  }
  
  final Map<String, Type[]> prop_obj_types = new HashMap<>();
  {
    prop_obj_types.put("empty", new Type[]{Type.WELL, Type.PAD});
    prop_obj_types.put("on_the_board", new Type[]{Type.PAD});
    prop_obj_types.put("on_board", prop_obj_types.get("on_board"));
    prop_obj_types.put("on", new Type[]{Type.PAD});
    prop_obj_types.put("off", prop_obj_types.get("on"));
    
  }

  @Override
  public void exitProperty_expr(Property_exprContext ctx) {
    for (PropertyContext prop : ctx.property()) {
      try {
        String att_name = with_spaces(prop.name());
        Type[] allowed_types = prop_obj_types.get(att_name);
        if (allowed_types != null) {
          getCheckedType(ctx.obj, allowed_types);
        } else {
          if (prop.aux_verb() != null) {
            att_name = with_spaces(prop.aux_verb())+" "+att_name;
          }
          report_error("Unhandled (user-defined?) Property", att_name);
        }        
      } catch (TypeError e) {
      }
    }
    noteType(ctx, Type.BOOL);
  }

  
  @Override
  public void exitRelation_expr(Relation_exprContext ctx) {
    RelationContext rel = ctx.relation();
    try {
      if (rel instanceof In_region_relContext) {
        getCheckedType(ctx.lhs, Type.PAD);
        getCheckedType(ctx.rhs, Type.REGION);
      } else if (rel instanceof User_defined_relContext) {
        report_error("Unhandled (user-defined?) Relation", with_spaces(rel),
                     (out)->{
//                       out.format("%s: %s%n", with_spaces(ctx.lhs), getDesc(ctx.lhs));
//                       out.format("%s: %s%n", with_spaces(ctx.rhs), getDesc(ctx.rhs));
                     });
      } else {
        report_error("Unhandled Relation", "\""+with_spaces(rel)+"\"");
      }
    } catch (TypeError e) {
    }
    noteType(ctx, Type.BOOL);

  }
  
  
  
  @Override
  public void exitSingleton_region(Singleton_regionContext ctx) {
    noteType(ctx, Type.REGION);
  }

  @Override
  public void exitDistance_expr(Distance_exprContext ctx) {
    try {
      getCheckedType(ctx.n, Type.INT);
      Type t = switch (ctx.kind.kind.getType()) 
          {
          case MPAMParser.ROW, MPAMParser.ROWS -> Type.ROWS;
          case MPAMParser.COL, MPAMParser.COLS, 
               MPAMParser.COLUMN, MPAMParser.COLUMNS -> Type.COLS;
          case MPAMParser.PAD, MPAMParser.PADS -> Type.PADS;
          default -> Type.ILLEGAL;
          };
      noteType(ctx, t);
    } catch (TypeError e) {
      noteType(ctx, Type.ILLEGAL);
    }
  }
  
  @Override
  public void exitDelta_expr(Delta_exprContext ctx) {
    try {
      Type t = switch (ctx.step_dir().dir.getType()) 
          {
          case MPAMParser.UP, MPAMParser.DOWN -> {
            getCheckedType(ctx.mag, Type.ROWS, Type.PADS, Type.INT);
            yield Type.VDELTA;
          }
          case MPAMParser.LEFT, MPAMParser.RIGHT -> {
            getCheckedType(ctx.mag, Type.COLS, Type.PADS, Type.INT);
            yield Type.HDELTA;
          }
          default -> Type.ILLEGAL;
      };
      noteType(ctx, t);
    } catch (TypeError e) {
      noteType(ctx, Type.ILLEGAL);
    }
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
    if (name.endsWith("?")) {
      noteType(ctx, Type.BOOL);
      return;
    }
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
  mul_sigs = new SigChecker(new TypePreservingSig(2, Type.FLOAT));
  final SigChecker 
  div_sigs = new SigChecker(new SymmetricTypeSig(Type.FLOAT, Type.FLOAT, Type.FLOAT));
                               
  @Override
  public void exitMuldiv_expr(Muldiv_exprContext ctx) {
    boolean is_mul = ctx.op.getType() == MPAMParser.STAR;
    if (is_mul) {
      noteType(ctx, mul_sigs.check(()->ctx.op.getText(), ctx.lhs, ctx.rhs));
    } else {
      noteType(ctx, div_sigs.check(()->ctx.op.getText(), ctx.lhs, ctx.rhs));
    }
  }

  final SigChecker
  wellSelector_sigs = new SigChecker(new TypeSig(Type.WELL, Type.PAD),
                                     new TypeSig(Type.WELL, Type.INT));
  @Override
  public void exitWell_selector_expr(Well_selector_exprContext ctx) {
    var sel = ctx.well_selector();
    if (sel instanceof Well_by_num_or_padContext s) {
      noteType(ctx, wellSelector_sigs.check("well[]", s.expr()));
    } else {
      report_error("Unhandled selector", sel.getText());
      noteType(ctx, Type.WELL);
    }
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
      if (ctx.mag != null) {
        getCheckedType(ctx.mag, Type.FLOAT);
      }
      var unit = ctx.unit();
      Type t = unit_type(unit);
      if (t != Type.UNKNOWN) {
        noteType(ctx, t);
      } else {
        report_error("Unhandled unit", unit.getText());
        noteType(ctx, Type.UNKNOWN);
      }
    } catch (TypeError e) {
      noteType(ctx, Type.ILLEGAL);
    }
  }
  
  @Override
  public void exitRoom_temp_lit(Room_temp_litContext ctx) {
    noteType(ctx, Type.TEMP);
  }
  
  @Override
  public void exitOp_call(Op_callContext ctx) {
    noteType(ctx, Type.OPCALL);
  }
  
  @Override
  public void exitRelpos_expr(Relpos_exprContext ctx) {
    try {
      getCheckedType(ctx.rhs, Type.PAD);
      RelposContext op = ctx.relpos();
      if (op instanceof Horizontal_relposContext) {
        getCheckedType(ctx.lhs, Type.INT, Type.COLS, Type.PADS);
        noteType(ctx, Type.PAD);
      } else if (op instanceof Vertical_relposContext) {
        getCheckedType(ctx.lhs, Type.INT, Type.ROWS, Type.PADS);
        noteType(ctx, Type.PAD);
      } else {
        report_error("Unhandled relative position", op.getText());
        noteType(ctx, Type.UNKNOWN);
      }
    } catch (TypeError e) {
      noteType(ctx, Type.ILLEGAL);
    }
  }
  
  final SigChecker
  not_sigs = new SigChecker(new TypeSig(Type.BOOL, Type.BOOL));
  @Override
  public void exitNot_expr(Not_exprContext ctx) {
    noteType(ctx, not_sigs.check("not", ctx.rhs));
  }
  
  final SigChecker
  and_sigs = new SigChecker(new TypeSig(Type.BOOL, Type.BOOL, Type.BOOL));
  @Override
  public void exitAnd_expr(And_exprContext ctx) {
    noteType(ctx, and_sigs.check("and",  ctx.lhs, ctx.rhs));
  }
  
  final SigChecker or_sigs = and_sigs;
  @Override
  public void exitOr_expr(Or_exprContext ctx) {
    noteType(ctx, or_sigs.check("or",  ctx.lhs, ctx.rhs));
  }
  
  @Override
  public void exitCurrent_obj_lit(Current_obj_litContext ctx) {
    noteType(ctx, Type.UNKNOWN);
  }
  
  final SigChecker
  relation_sigs = new SigChecker(new TypePreservingSig(2, Type.FLOAT, Type.PADS,
                                                       Type.HDELTA, Type.VDELTA, 
                                                       Type.VOLUME, Type.TIME, Type.TEMP, Type.FREQ),
                                 new SymmetricTypeSig(Type.BOOL, Type.FLOAT, Type.INT));
  @Override
  public void exitOrder_expr(Order_exprContext ctx) {
    ExprContext lhs = ctx.lhs;
    if (lhs instanceof Order_exprContext c) {
      lhs = relation_rhs.get(lhs);
    }
    Type t = relation_sigs.check(()->ctx.op.which.getText(), lhs, ctx.rhs);
    noteType(ctx, t == Type.ILLEGAL ? t : Type.BOOL);
    relation_rhs.put(ctx, ctx.rhs);
  }
}

