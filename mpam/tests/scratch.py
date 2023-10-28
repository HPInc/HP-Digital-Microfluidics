from __future__ import annotations
from quantities.currency.usd import quarters, dollars
from quantities.currency.gpb import pound, GBP


GBP.set_exchange_rate(1.5*dollars)
q = 4*quarters + 1*pound

print(q)