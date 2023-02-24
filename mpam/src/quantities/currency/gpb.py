from __future__ import annotations
from quantities.money import Currency

gbp = GBP = Currency("GBP")
pound = pounds = GBP.new_denomination(GBP, "pounds", singular="pound", prefix_symbol="£", 
                                      decimal_places=2)
pee = penny = pence = GBP.new_denomination(GBP/100, "pence", singular="penny",
                                           postfix_symbol="p")


