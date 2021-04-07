package com.hp.thylacine;

public interface ANSI {
  
  static String escape_sequence(int n) {
    return String.format("\u001b[1;%dm", n);
  }
  


 

  static String RESET = escape_sequence(0);
  static String BOLD = escape_sequence(1);
  static String FAINT = escape_sequence(2);
  static String ITALIC = escape_sequence(3);
  static String UNDERLINE = escape_sequence(4);
  static String NEGATIVE = escape_sequence(7);
  static String CONCEAL = escape_sequence(8);
  static String CROSSED_OUT = escape_sequence(9);
  static String DOUBLE_UNDERLINE = escape_sequence(21);
  static String BOLD_OFF = escape_sequence(22);
  static String ITALIC_OFF = escape_sequence(23);
  static String UNDERLINE_OFF = escape_sequence(24);
  static String NEGATIVE_OFF = escape_sequence(27);
  static String CONCEAL_OFF = escape_sequence(28);
  static String CROSSED_OUT_OFF = escape_sequence(29);

  static String BLACK = escape_sequence(30);
  static String RED = escape_sequence(31);
  static String GREEN = escape_sequence(32);
  static String YELLOW = escape_sequence(33);
  static String BLUE = escape_sequence(34);
  static String MAGENTA = escape_sequence(35);
  static String CYAN = escape_sequence(36);
  static String WHITE = escape_sequence(37);
  
  static String BLACK_BG = escape_sequence(40);
  static String RED_BG = escape_sequence(41);
  static String GREEN_BG = escape_sequence(42);
  static String YELLOW_BG = escape_sequence(43);
  static String BLUE_BG = escape_sequence(44);
  static String MAGENTA_BG = escape_sequence(45);
  static String CYAN_BG = escape_sequence(46);
  static String WHITE_BG = escape_sequence(47);

  static String FRAMED = escape_sequence(51);
  static String FRAMED_OFF = escape_sequence(54);

  static String BLACK_HI = escape_sequence(90);
  static String RED_HI = escape_sequence(91);
  static String GREEN_HI = escape_sequence(92);
  static String YELLOW_HI = escape_sequence(93);
  static String BLUE_HI = escape_sequence(94);
  static String MAGENTA_HI = escape_sequence(95);
  static String CYAN_HI = escape_sequence(96);
  static String WHITE_HI = escape_sequence(97);
  
  static String BLACK_HI_BG = escape_sequence(100);
  static String RED_HI_BG = escape_sequence(101);
  static String GREEN_HI_BG = escape_sequence(102);
  static String YELLOW_HI_BG = escape_sequence(103);
  static String BLUE_HI_BG = escape_sequence(104);
  static String MAGENTA_HI_BG = escape_sequence(105);
  static String CYAN_HI_BG = escape_sequence(106);
  static String WHITE_HI_BG = escape_sequence(107);
  
}
