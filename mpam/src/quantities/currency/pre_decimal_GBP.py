from __future__ import annotations
from ..money import Currency
from ..dimensions import Money
import math

gbp = GBP = Currency("GBP")
pound = pounds = GBP.new_denomination(GBP, "pounds", singular="pound", prefix_symbol="£")
shilling = shillings = bob = GBP.new_denomination(pound/20, "shillings",
                                                  singular="shilling",
                                                  postfix_symbol="s.")
penny = pence = GBP.new_denomination(shilling/12, "pence",
                                                  singular="penny",
                                                  postfix_symbol="d.")
farthing = farthings = GBP.new_denomination(penny/4, "farthings", singular="farthing")
crown = crowns = GBP.new_denomination(5*shillings, "crowns", singular="crown")
half_crown = half_crowns = GBP.new_denomination(crown/2, "half crowns", singular="half crown")

sixpence = 6*pence
halfpenny = penny/2

def slashed(money: Money)->str:
    if money < 0:
        return "-"+slashed(-money)

    decomposition = money.decomposed((pounds, shillings, pence, farthings), required="all") 
    L,s,d,f = [t[1] for t in decomposition.tuples]
    remainder = decomposition.remainder.as_number(pence)

    if math.isclose(remainder, 0, abs_tol=0.00001):
        remainder = 0
    else:
        remainder += 0.25*f
        f = 0
    r_str = ""
    if remainder > 0:
        r_str = f"{remainder:.16f}"[1:].rstrip('0')
    f_str = ("", "¼", "½", "¾")[f] if f>0 else "" if remainder == 0 else r_str
    d_str = f"{d}{f_str}" if d>0 else f_str if f_str != "" else "0"
    if L == 0 and s == 0:
        return d_str+"d."
    if d_str == "0":
        d_str = "-"
    s_str = "-" if s == 0 else str(s)
    l_str = "" if L == 0 else f"£{L}/" 
    return f"{l_str}{s_str}/{d_str}"
    
GBP.currency_formatter = slashed

