from __future__ import annotations

from ..money import Currency


eur = EUR = Currency("EUR")
euro = euros = EUR.new_denomination(EUR, "euros", singular="euro", prefix_symbol="€", 
                                      decimal_places=2)
cent = cents = pence = EUR.new_denomination(EUR/100, "cents", singular="cent",
                                           postfix_symbol="c")
eur.currency_formatter = euros