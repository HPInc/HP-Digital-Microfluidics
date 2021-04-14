package com.hp.mpam;

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

import com.hp.physl.ANSI;
import com.hp.thylacine.MPAMBaseListener;
import com.hp.thylacine.MPAMParser;
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
  
  final ParseTreeProperty<MPAMType> types = new ParseTreeProperty<>();
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
  

  private MPAMType noteType(ExprContext ctx, MPAMType type) {
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
    boolean flagp = (type == MPAMType.UNKNOWN || type == MPAMType.ILLEGAL);
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

    public TypeError(MPAMType t, ExprContext ctx, MPAMType[] allowed) {
      if (t != MPAMType.ILLEGAL) {
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
                         for (MPAMType a : allowed) {
                           out.print(sep+a);
                           sep = ", ";
                         }
                         out.println();
                       }
                     });
      }
    }
    
  }
  
  MPAMType getType(ExprContext ctx) {
    if (ctx == null) {
      return MPAMType.MISSING; 
    }
    MPAMType t = types.get(ctx);
    if (t == null) {
      return MPAMType.UNKNOWN;
    }
    return t;
  }  

  MPAMType getCheckedType(ExprContext ctx, MPAMType... allowed) throws TypeError {
    MPAMType t = getType(ctx);
    if (allowed.length == 0) {
      return t;
    }
    for (MPAMType a : allowed) {
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
    MPAMType matches(MPAMType...param_types);
    void add_arg_types_to(Set<MPAMType> set, int i);
  }

  static class TypeSig implements TypeSigBase {
    final MPAMType ret_type;
    final MPAMType[] arg_types;
    final int arity;
    
    TypeSig(MPAMType rt, MPAMType...ats) {
      ret_type = rt;
      arg_types = ats;
      arity = ats.length;
    }
    
    @Override
    public MPAMType matches(MPAMType...param_types) {
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
    public void add_arg_types_to(Set<MPAMType> set, int i) {
      MPAMType t = arg_types[i];
      if (t == null) {
        t = MPAMType.MISSING;
      }
      set.add(t);
    }

    @Override
    public int arity() {
      return arg_types.length;
    }

  }
  
  static class SymmetricTypeSig implements TypeSigBase {
    private final MPAMType ret_type;
    private final MPAMType t1;
    private final MPAMType t2;
    public SymmetricTypeSig(MPAMType ret_type, MPAMType t1, MPAMType t2) {
      this.ret_type = ret_type;
      this.t1 = t1;
      this.t2 = t2;
    }
    
    @Override
    public
    MPAMType matches(MPAMType... param_types) {
      if (param_types.length == 2
          && ((param_types[0].dominated_by(t1) && param_types[1].dominated_by(t2))
              || (param_types[0].dominated_by(t2) && param_types[1].dominated_by(t1))))
      {
        return ret_type;
      }
      return null;
    }
    
    @Override
    public void add_arg_types_to(Set<MPAMType> set, int i) {
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
    final EnumSet<MPAMType> types;
    
    public TypePreservingSig(int arity, MPAMType first, MPAMType...rest) {
      this.arity = arity;
      types = EnumSet.of(first, rest);
    }

    @Override
    public int arity() {
      return arity;
    }
    
    private boolean acceptable(MPAMType t) {
      for (MPAMType a : types) {
        if (t.dominated_by(a)) {
          return true;
        }
      }
      return false;
    }

    @Override
    public MPAMType matches(MPAMType... param_types) {
      if (param_types.length == 0) {
        return null;
      }
      MPAMType highest = param_types[0];
      if (!acceptable(highest)) {
        return null;
      }
      for (int i=1; i<param_types.length; i++) {
        MPAMType pt = param_types[i];
        if (!pt.dominated_by(highest)) {
          MPAMType lcd = highest.lowest_common_dominator(pt);
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
    public void add_arg_types_to(Set<MPAMType> set, int i) {
      set.addAll(types);
    }
    
  }
  
  
  class SigChecker {
    final TypeSigBase[] sigs;
    final int arity;
    final MPAMType[][] constraints;
    
    SigChecker(TypeSigBase...sigs) {
      this.sigs = sigs;
      Map<Integer, Set<MPAMType>> map = new HashMap<>();
      for (TypeSigBase sig : sigs) {
        for (int i=0; i<sig.arity(); i++) {
          Set<MPAMType> set = map.get(i);
          if (set == null) {
            set = new HashSet<>();
            map.put(i, set);
          }
          sig.add_arg_types_to(set, i);
        }
      }
      arity = map.size();
      constraints = new MPAMType[arity][];
      
      for (int i=0; i<arity; i++) {
        Set<MPAMType> set = map.get(i);
        if (set.isEmpty()) {
          constraints[i] = new MPAMType[0];
        } else {
          constraints[i] = set.toArray(new MPAMType[set.size()]);
        }
      }
    }
    
    MPAMType check(String op, ExprContext... params) {
      return check(()->op, params);
    }
    MPAMType check(Supplier<String> op, ExprContext... params) {
      MPAMType[] types = new MPAMType[arity];
      for (int i=0; i<params.length; i++) {
        try {
          types[i] = getCheckedType(params[i], constraints[i]);
        } catch (TypeError e) {
          return MPAMType.ILLEGAL;
        }
      }
      for (var sig : sigs) {
        MPAMType ret_type = sig.matches(types);
        if (ret_type != null) {
          return ret_type;
        }
      }
      String ptype_descs = Arrays.stream(types).map(MPAMType::toString).collect(Collectors.joining(", "));
      report_error("Type Error",
                   String.format("%s not defined on %s", op.get(), ptype_descs),
                   (out)->{
                     out.println("Params are ");
                     for (var p : params) {
                       String d = getDesc(p);
                       out.println("  "+d);
                     }
                   });
      return MPAMType.ILLEGAL;
    }
        
  }

  
  private MPAMType unit_type(UnitContext uc) {
    if (uc.VOLUME_UNIT() != null) {
      return MPAMType.VOLUME;
    } else if (uc.TIME_UNIT() != null) {
      return MPAMType.TIME;
    } else if (uc.TEMP_UNIT() != null) {
      return MPAMType.TEMP;
    } else if (uc.FREQ_UNIT() != null) {
      return MPAMType.FREQ;
    } 
    return MPAMType.UNKNOWN;
  }
  
  @Override
  public void exitInt_literal(Int_literalContext ctx) {
    noteType(ctx, MPAMType.INT);
  }
  
  final SigChecker 
  add_sigs = new SigChecker(new TypePreservingSig(2, MPAMType.FLOAT, 
                                                  MPAMType.PADS,
                                                  MPAMType.DELTA2D,
                                                  MPAMType.REGION),
                            new SymmetricTypeSig(MPAMType.PAD, MPAMType.PAD, MPAMType.DELTA2D)
                            );
  final SigChecker 
  sub_sigs = new SigChecker(new TypePreservingSig(2, MPAMType.FLOAT, 
                                                  MPAMType.PADS,
                                                  MPAMType.DELTA2D,
                                                  MPAMType.REGION),
                            new SymmetricTypeSig(MPAMType.PAD, MPAMType.PAD, MPAMType.DELTA2D),
                            new TypeSig(MPAMType.DELTA2D, MPAMType.PAD, MPAMType.PAD)
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
    noteType(ctx, MPAMType.UNKNOWN);
  }

  final SigChecker
  negSigs = new SigChecker(new TypePreservingSig(1, MPAMType.INT, MPAMType.FLOAT));
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
    noteType(ctx, MPAMType.INT);
  }

  final SigChecker
  regionSelector_sigs = new SigChecker(new TypeSig(MPAMType.REGION, MPAMType.INT));
  @Override
  public void exitRegion_selector_expr(Region_selector_exprContext ctx) {
    var sel = ctx.region_selector();
    if (sel instanceof Region_by_numContext s) {
      noteType(ctx, regionSelector_sigs.check("region[]", s.expr()));
    } else {
      report_error("Unhandled selector", sel.getText());
      noteType(ctx, MPAMType.REGION);
    }
  }
  

  @Override
  public void exitBoolean_literal(Boolean_literalContext ctx) {
    noteType(ctx, MPAMType.BOOL);
  }
  
  final SigChecker
  row_attr_sigs = new SigChecker(new TypeSig(MPAMType.INT, MPAMType.PAD));
  final SigChecker
  col_attr_sigs = new SigChecker(new TypeSig(MPAMType.INT, MPAMType.PAD));
  final SigChecker
  volume_attr_sigs = new SigChecker(new TypeSig(MPAMType.VOLUME, MPAMType.PAD),
                                    new TypeSig(MPAMType.VOLUME, MPAMType.WELL));
  final SigChecker
  capacity_attr_sigs = new SigChecker(new TypeSig(MPAMType.VOLUME, MPAMType.PAD),
                                      new TypeSig(MPAMType.VOLUME, MPAMType.WELL));
  
  final Map<String, SigChecker> attribute_sigs = new HashMap<>();
  {
    attribute_sigs.put("exit pad", new SigChecker(new TypeSig(MPAMType.PAD, MPAMType.WELL)));
    attribute_sigs.put("volume", new SigChecker(new TypeSig(MPAMType.VOLUME, MPAMType.WELL),
                                                new TypeSig(MPAMType.VOLUME, MPAMType.PAD)));
    attribute_sigs.put("current volume", attribute_sigs.get("volume"));
    attribute_sigs.put("row", new SigChecker(new TypeSig(MPAMType.INT, MPAMType.PAD)));
    attribute_sigs.put("col", attribute_sigs.get("row"));
    attribute_sigs.put("column", attribute_sigs.get("col"));
    attribute_sigs.put("capacity", new SigChecker(new TypeSig(MPAMType.VOLUME, MPAMType.PAD),
                                                  new TypeSig(MPAMType.VOLUME, MPAMType.WELL)));
  }
  
  @Override
  public void exitAttribute_expr(Attribute_exprContext ctx) {
    AttributeContext att = ctx.attr;
    if (att instanceof Unit_count_attrContext a) {
      MPAMType t = unit_type(a.unit());
      if (t== MPAMType.UNKNOWN) {
        report_error("Unhandled unit", with_spaces(a.unit()));
      } else {
        try {
          getCheckedType(ctx.obj, t);
          noteType(ctx, MPAMType.FLOAT);
        } catch (TypeError e) {
          noteType(ctx, MPAMType.ILLEGAL);
        }
      }
    } else if (att instanceof User_defined_attrContext c) {
      String att_name = with_spaces(c.name());
      SigChecker sigs = attribute_sigs.get(att_name);
      if (sigs != null) {
        noteType(ctx, sigs.check(att_name, ctx.obj));
      } else {
        report_error("Unhandled (user-defined?) Attribute", att_name);
        noteType(ctx, MPAMType.UNKNOWN);
      }
    } else {
      report_error("Unhandled Attribute", "\""+with_spaces(att)+"\"");
      noteType(ctx, MPAMType.ILLEGAL);
    }
  }
  
  final Map<String, MPAMType[]> prop_obj_types = new HashMap<>();
  {
    prop_obj_types.put("empty", new MPAMType[]{MPAMType.WELL, MPAMType.PAD});
    prop_obj_types.put("on_the_board", new MPAMType[]{MPAMType.PAD});
    prop_obj_types.put("on_board", prop_obj_types.get("on_board"));
    prop_obj_types.put("on", new MPAMType[]{MPAMType.PAD});
    prop_obj_types.put("off", prop_obj_types.get("on"));
    
  }

  @Override
  public void exitProperty_expr(Property_exprContext ctx) {
    for (PropertyContext prop : ctx.property()) {
      try {
        String att_name = with_spaces(prop.name());
        MPAMType[] allowed_types = prop_obj_types.get(att_name);
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
    noteType(ctx, MPAMType.BOOL);
  }

  
  @Override
  public void exitRelation_expr(Relation_exprContext ctx) {
    RelationContext rel = ctx.relation();
    try {
      if (rel instanceof In_region_relContext) {
        getCheckedType(ctx.lhs, MPAMType.PAD);
        getCheckedType(ctx.rhs, MPAMType.REGION);
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
    noteType(ctx, MPAMType.BOOL);

  }
  
  
  
  @Override
  public void exitSingleton_region(Singleton_regionContext ctx) {
    noteType(ctx, MPAMType.REGION);
  }

  @Override
  public void exitDistance_expr(Distance_exprContext ctx) {
    try {
      getCheckedType(ctx.n, MPAMType.INT);
      MPAMType t = switch (ctx.kind.kind.getType()) 
          {
          case MPAMParser.ROW, MPAMParser.ROWS -> MPAMType.ROWS;
          case MPAMParser.COL, MPAMParser.COLS, 
               MPAMParser.COLUMN, MPAMParser.COLUMNS -> MPAMType.COLS;
          case MPAMParser.PAD, MPAMParser.PADS -> MPAMType.PADS;
          default -> MPAMType.ILLEGAL;
          };
      noteType(ctx, t);
    } catch (TypeError e) {
      noteType(ctx, MPAMType.ILLEGAL);
    }
  }
  
  @Override
  public void exitDelta_expr(Delta_exprContext ctx) {
    try {
      MPAMType t = switch (ctx.step_dir().dir.getType()) 
          {
          case MPAMParser.UP, MPAMParser.DOWN -> {
            getCheckedType(ctx.mag, MPAMType.ROWS, MPAMType.PADS, MPAMType.INT);
            yield MPAMType.VDELTA;
          }
          case MPAMParser.LEFT, MPAMParser.RIGHT -> {
            getCheckedType(ctx.mag, MPAMType.COLS, MPAMType.PADS, MPAMType.INT);
            yield MPAMType.HDELTA;
          }
          default -> MPAMType.ILLEGAL;
      };
      noteType(ctx, t);
    } catch (TypeError e) {
      noteType(ctx, MPAMType.ILLEGAL);
    }
  }

  @Override
  public void exitSingleton_well(Singleton_wellContext ctx) {
    noteType(ctx, MPAMType.WELL);
  }

  @Override
  public void exitList_expr(List_exprContext ctx) {
    // TODO Auto-generated method stub
    noteType(ctx, MPAMType.UNKNOWN);
  }

  @Override
  public void exitFloat_literal(Float_literalContext ctx) {
    noteType(ctx, MPAMType.FLOAT);
  }

  static Pattern var_pat = Pattern.compile("(.*[^_0-9])_?[0-9]*");
  
  static Map<String, MPAMType> var_types = new HashMap<>();
  static {
    var_types.put("b", MPAMType.BOOL);
    var_types.put("i", MPAMType.INT);
    var_types.put("f", MPAMType.FLOAT);
    var_types.put("p", MPAMType.PAD);
    var_types.put("pth", MPAMType.PATH);
    var_types.put("r", MPAMType.REGION);
    var_types.put("s", MPAMType.STRING);
    var_types.put("temp", MPAMType.TEMP);
    var_types.put("time", MPAMType.TIME);
    var_types.put("vol", MPAMType.VOLUME);
    var_types.put("w", MPAMType.WELL);
  }
  
  @Override
  public void exitVariable_name(Variable_nameContext ctx) {
    String name = ctx.name().getText();
    if (name.endsWith("?")) {
      noteType(ctx, MPAMType.BOOL);
      return;
    }
    Matcher m = var_pat.matcher(name);
    if (m.matches()) {
      String base = m.group(1);
      MPAMType t = var_types.getOrDefault(base, MPAMType.UNKNOWN);
      noteType(ctx, t);
    } else {
      noteType(ctx, MPAMType.UNKNOWN);
    }
  }

  @Override
  public void exitPrenthesized_expr(Prenthesized_exprContext ctx) {
    MPAMType inner_type = getType(ctx.expr());
    noteType(ctx, inner_type);
  }

  final SigChecker 
  mul_sigs = new SigChecker(new TypePreservingSig(2, MPAMType.FLOAT));
  final SigChecker 
  div_sigs = new SigChecker(new SymmetricTypeSig(MPAMType.FLOAT, MPAMType.FLOAT, MPAMType.FLOAT));
                               
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
  wellSelector_sigs = new SigChecker(new TypeSig(MPAMType.WELL, MPAMType.PAD),
                                     new TypeSig(MPAMType.WELL, MPAMType.INT));
  @Override
  public void exitWell_selector_expr(Well_selector_exprContext ctx) {
    var sel = ctx.well_selector();
    if (sel instanceof Well_by_num_or_padContext s) {
      noteType(ctx, wellSelector_sigs.check("well[]", s.expr()));
    } else {
      report_error("Unhandled selector", sel.getText());
      noteType(ctx, MPAMType.WELL);
    }
  }

  final SigChecker
  coords_sigs = new SigChecker(new TypeSig(MPAMType.PAD, MPAMType.INT, MPAMType.INT));
  @Override
  public void exitPad_coords(Pad_coordsContext ctx) {
    noteType(ctx, coords_sigs.check("(x,y)", ctx.row, ctx.col));
  }

  @Override
  public void exitQuantity_expr(Quantity_exprContext ctx) {
    try {
      if (ctx.mag != null) {
        getCheckedType(ctx.mag, MPAMType.FLOAT);
      }
      var unit = ctx.unit();
      MPAMType t = unit_type(unit);
      if (t != MPAMType.UNKNOWN) {
        noteType(ctx, t);
      } else {
        report_error("Unhandled unit", unit.getText());
        noteType(ctx, MPAMType.UNKNOWN);
      }
    } catch (TypeError e) {
      noteType(ctx, MPAMType.ILLEGAL);
    }
  }
  
  @Override
  public void exitRoom_temp_lit(Room_temp_litContext ctx) {
    noteType(ctx, MPAMType.TEMP);
  }
  
  @Override
  public void exitOp_call(Op_callContext ctx) {
    noteType(ctx, MPAMType.OPCALL);
  }
  
  @Override
  public void exitRelpos_expr(Relpos_exprContext ctx) {
    try {
      getCheckedType(ctx.rhs, MPAMType.PAD);
      RelposContext op = ctx.relpos();
      if (op instanceof Horizontal_relposContext) {
        getCheckedType(ctx.lhs, MPAMType.INT, MPAMType.COLS, MPAMType.PADS);
        noteType(ctx, MPAMType.PAD);
      } else if (op instanceof Vertical_relposContext) {
        getCheckedType(ctx.lhs, MPAMType.INT, MPAMType.ROWS, MPAMType.PADS);
        noteType(ctx, MPAMType.PAD);
      } else {
        report_error("Unhandled relative position", op.getText());
        noteType(ctx, MPAMType.UNKNOWN);
      }
    } catch (TypeError e) {
      noteType(ctx, MPAMType.ILLEGAL);
    }
  }
  
  final SigChecker
  not_sigs = new SigChecker(new TypeSig(MPAMType.BOOL, MPAMType.BOOL));
  @Override
  public void exitNot_expr(Not_exprContext ctx) {
    noteType(ctx, not_sigs.check("not", ctx.rhs));
  }
  
  final SigChecker
  and_sigs = new SigChecker(new TypeSig(MPAMType.BOOL, MPAMType.BOOL, MPAMType.BOOL));
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
    noteType(ctx, MPAMType.UNKNOWN);
  }
  
  final SigChecker
  relation_sigs = new SigChecker(new TypePreservingSig(2, MPAMType.FLOAT, MPAMType.PADS,
                                                       MPAMType.HDELTA, MPAMType.VDELTA, 
                                                       MPAMType.VOLUME, MPAMType.TIME, MPAMType.TEMP, MPAMType.FREQ),
                                 new SymmetricTypeSig(MPAMType.BOOL, MPAMType.FLOAT, MPAMType.INT));
  @Override
  public void exitOrder_expr(Order_exprContext ctx) {
    ExprContext lhs = ctx.lhs;
    if (lhs instanceof Order_exprContext c) {
      lhs = relation_rhs.get(lhs);
    }
    MPAMType t = relation_sigs.check(()->ctx.op.which.getText(), lhs, ctx.rhs);
    noteType(ctx, t == MPAMType.ILLEGAL ? t : MPAMType.BOOL);
    relation_rhs.put(ctx, ctx.rhs);
  }
}

