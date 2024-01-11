from __future__ import annotations

from ..money import Currency

jpy = JPY = Currency("JPY")
yen = JPY.new_denomination(JPY, "yen", prefix_symbol="¥")
