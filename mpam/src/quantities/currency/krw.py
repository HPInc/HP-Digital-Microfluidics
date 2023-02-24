from __future__ import annotations

from quantities.money import Currency

krw = KRW = Currency("KRW")
won = KRW.new_denomination(KRW, "won", prefix_symbol="₩")
