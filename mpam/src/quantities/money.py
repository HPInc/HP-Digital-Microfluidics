from __future__ import annotations

from typing import Union, Optional, Sequence, Final

from quantities.core import UnitExpr
from quantities.dimensions import MoneyUnit, Money
from threading import RLock
from erk.stringutils import is_are, conj_str, noun

class NoExchangeRate(RuntimeError):
    currency: Final[Currency]
    
    def __init__(self, currency: Currency) -> None:
        self.currency = currency
        with Currency.class_lock:
            known_currencies = [*Currency.known_value_currencies]
        known_currencies.sort(key=lambda c: c.abbreviation)
        verb = is_are(len(known_currencies))
        rate = noun(len(known_currencies), "rate")
        currencies = conj_str(known_currencies)
        super().__init__(f"No exchange rate specified for {currency}.  Exchange {rate} {verb} known for {currencies}.")


class Currency(MoneyUnit, Money.CurrencyProxy):
    exchange_rate: Optional[float] = None
    
    known_value_currencies: Final = set['Currency']()
    class_lock: Final = RLock()
    
    def _set_exchange_rate(self, exchange_rate: float) -> None:
        self.exchange_rate = exchange_rate
        with self.class_lock:
            self.known_value_currencies.add(self)
    
    def __init__(self, abbr: str, *, 
                 exchange_rate: Optional[Money] = None):
        quant = Money(1, currency_proxy = self)
        super().__init__(abbr, quant)
        if exchange_rate is not None:
            self.set_exchange_rate(exchange_rate)
        
    def force_magnitude(self, money: Money)->None:
        # We do this all in a critical region to make sure it
        # only happens once per instance.
        with self.class_lock:
            rate = self.exchange_rate
            if rate is None:
                # If we're the first forced, we become the unit
                if len(self.known_value_currencies) == 0:
                    rate = 1.0
                    if Money.default_units is None:
                        Money.default_units = self
                    self._set_exchange_rate(rate)
                else:
                    raise NoExchangeRate(self)
            money.magnitude *= rate
            money.currency_proxy = None
                    
    def unit_check(self, money: Money, 
                   units: Union[UnitExpr[Money], Sequence[UnitExpr[Money]]])->None:
        cp = money.currency_proxy
        if isinstance(units, UnitExpr):
            units = (units,)
            for unit in units:
                if unit.quantity.currency_proxy is not cp:
                    money._force_magnitude()
                    for u in units:
                        u.quantity._force_magnitude()
                        
    def to_str(self, money: Money) -> str:
        if self.exchange_rate is None:
            return money.in_units(self).__str__()
        money._force_magnitude()
        return money.__str__()
    
    def format_str(self, money: Money, format_spec: str) -> str:
        if self.exchange_rate is None:
            return money.in_units(self).__format__(format_spec)
        money._force_magnitude()
        return money.__format__(format_spec)
    
    def set_exchange_rate(self, other: Money) -> None:
        with self.class_lock:
            if self.exchange_rate is None:
                other._force_magnitude()
                self._set_exchange_rate(other.magnitude)
                return
            # We have a value. Let's see if they do.
            their_currency = other.currency_proxy
            if their_currency is not None:
                assert isinstance(their_currency, Currency)
                if their_currency.exchange_rate is None:
                    rate = self.exchange_rate / other.magnitude
                    their_currency._set_exchange_rate(rate)
                    return
            other._force_magnitude()
            if other.magnitude != self.exchange_rate:
                raise ValueError(f"Attempting to change {self}'s exchange rate from {self.quantity} to {other}.")
    
                        
usd = USD = Currency("USD")
dollar = dollars = us_dollar = us_dollars = USD.as_unit("dollars", singular="dollar")
cent = cents = us_cent = us_cents = (USD/100).as_unit("cents", singular="cent")
dime = dimes = us_dim = us_dimes = (10*cents).as_unit("dimes", singular="dime")

ukp = UKP = Currency("UKP")
  
        
