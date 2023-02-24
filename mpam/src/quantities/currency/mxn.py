from __future__ import annotations
from quantities.money import Currency

mxn = MXN = Currency("MXN")
peso = pesos = MXN.new_denomination(MXN, "pesos", singular="peso", prefix_symbol="$", 
                                        decimal_places=2)
mxn.currency_formatter = pesos
centavo = centavos = MXN.new_denomination(peso/100, "centavos", singular="centavo", postfix_symbol="¢")
