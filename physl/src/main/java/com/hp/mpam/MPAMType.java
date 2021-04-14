package com.hp.mpam;

import java.util.HashSet;
import java.util.Set;

public enum MPAMType {
  UNKNOWN, ILLEGAL, MISSING,
  BOOL, STRING, 
  FLOAT, INT(FLOAT), 
  QUANTITY, VOLUME(QUANTITY), TEMP(QUANTITY), TIME(QUANTITY), FREQ(),
  DELTA2D,
  HDELTA(DELTA2D), COLS(HDELTA), 
  VDELTA(DELTA2D), ROWS(VDELTA), PADS,
  PAD, WELL, REGION, RECT, SEGMENT, PATH,
  OPCALL;
  
  /*
   * Can't just use EnumSet<Type> because Type isn't known to be an enum here.  Sigh.
   */
  private final Set<MPAMType> dominators = new HashSet<MPAMType>();
  
  MPAMType(MPAMType...supers) {
    for (MPAMType d : supers) {
      dominators.add(d);
      dominators.addAll(d.dominators);
    }

  }
  
  boolean dominates(MPAMType other) {
    return this==other || other.dominated_by(this);
  }
  
  boolean dominated_by(MPAMType other) {
    return this==other || dominators.contains(other);
  }
  
  MPAMType lowest_common_dominator(MPAMType other) {
    if (this==other || other.dominated_by(this)) {
      return this;
    } else if (this.dominated_by(other)) {
      return other;
    }
    MPAMType lowest = null;
    for (MPAMType d : dominators) {
      if (other.dominators.contains(d)) {
        if (lowest == null || d.dominated_by(lowest)) {
          lowest = d;
        }
      }
    }
    return lowest;
  }
}
