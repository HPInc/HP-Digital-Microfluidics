from __future__ import annotations

from typing import Union, Optional, Sequence, Final, Callable

from quantities.core import UnitExpr
from quantities.dimensions import MoneyUnit, Money
from threading import RLock
from erk.stringutils import is_are, conj_str, noun

CurrencyFormatter = Money.CurrencyFormatter

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
        
        
class Denomination(MoneyUnit, Money.CurrencyFormatter):
    currency: Final[Currency]
    decimal_places: Optional[int] = None
    separate_symbol: bool = True
    
    _symbol: str
    _symbol_is_prefix: bool = True

    @property
    def prefix_symbol(self) -> Optional[str]:
        return None if not self._symbol_is_prefix else self._symbol
    
    @prefix_symbol.setter
    def prefix_symbol(self, symbol: Optional[str]) -> None:
        if symbol is None:
            self.postfix_symbol = self.abbreviation
        else:
            self._symbol_is_prefix = True
            self._symbol = symbol

    @property
    def postfix_symbol(self) -> Optional[str]:
        return None if self._symbol_is_prefix else self._symbol
    
    @postfix_symbol.setter
    def postfix_symbol(self, symbol: Optional[str]) -> None:
        if symbol is None:
            symbol = self.abbreviation
        self._symbol_is_prefix = False
        self._symbol = symbol

    def __init__(self, abbr: str, quant: Union[Money,UnitExpr[Money]], 
                 *, 
                 currency: Currency,
                 prefix_symbol: Optional[str] = None,
                 postfix_symbol: Optional[str] = None,\
                 separate_symbol: Optional[bool] = None,
                 decimal_places: Optional[int] = None,
                 singular: Optional[str] = None):
        self.currency = currency
        super().__init__(abbr, quant, singular=singular)
        if separate_symbol is None:
            separate_symbol = prefix_symbol is None and postfix_symbol is None
        self.separate_symbol = separate_symbol 
        if prefix_symbol is not None:
            assert postfix_symbol is None, "Can't have both a prefix symbol and a postfix symbol"
            self.prefix_symbol = prefix_symbol
        else:
            self.postfix_symbol = postfix_symbol
        self.decimal_places = decimal_places
        
    def format_currency(self, money: Money, *,
                        force_prefix: bool = False,
                        force_suffix: bool = False,
                        decimal_places: Optional[int] = None) -> str:
        assert not (force_prefix and force_suffix), "Can't force both prefix and suffix"
        prefix = (self._symbol_is_prefix or force_prefix) and not force_suffix
        if decimal_places is None:
            decimal_places = self.decimal_places
        mag = money.as_number(self)
        fmt = "g" if decimal_places is None else f".{decimal_places}f"
        val = f"{mag:{fmt}}"
        separator = " " if self.separate_symbol else ""
        if prefix:
            return self._symbol+separator+val
        else:
            return val+separator+self._symbol 
        


class Currency(Denomination, Money.CurrencyProxy):
    exchange_rate: Optional[float] = None
    currency_formatter: Union[CurrencyFormatter,
                              Callable[[Money], str]]
    
    known_value_currencies: Final = set['Currency']()
    class_lock: Final = RLock()
    
    class NormalFormatter(CurrencyFormatter):
        currency: Final[Currency]
        
        def __init__(self, currency: Currency) -> None:
            self.currency = currency
        
        def format_currency(self, money:Money, 
                            *, force_prefix:bool=False, 
                            force_suffix:bool=False, 
                            decimal_places:Optional[int]=None)-> str:
            return self.currency._normal_cf(money, force_prefix=force_prefix,
                                            force_suffix=force_suffix,
                                            decimal_places=decimal_places)
    
    def _set_exchange_rate(self, exchange_rate: float) -> None:
        self.exchange_rate = exchange_rate
        with self.class_lock:
            self.known_value_currencies.add(self)
    
    def __init__(self, abbr: str, *, 
                 exchange_rate: Optional[Money] = None):
        quant = Money.dim().make_quantity(1, currency_proxy=self)
        super().__init__(abbr, quant, currency = self)
        if exchange_rate is not None:
            self.set_exchange_rate(exchange_rate)
        self.currency_formatter = Currency.NormalFormatter(self)
        
    def force_magnitude(self, money: Money)->None:
        # We do this all in a critical region to make sure it
        # only happens once per instance.
        with self.class_lock:
            rate = self.exchange_rate
            if rate is None:
                # If we're the first forced, we become the unit
                if len(self.known_value_currencies) == 0:
                    rate = 1.0
                    if Money.default_currency_formatter is None:
                        Money.default_currency_formatter = self
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
                        
    def as_currency_formatter(self) -> CurrencyFormatter:
        return self
                        
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
    
    def new_denomination(self, quant: Union[Money,UnitExpr[Money]],
                         abbr: str, 
                         *, 
                         prefix_symbol: Optional[str] = None,
                         postfix_symbol: Optional[str] = None,
                         separate_symbol: Optional[bool] = None,
                         decimal_places: Optional[int] = None,
                         singular: Optional[str] = None) -> Denomination:
        return Denomination(abbr, quant, currency=self,
                            prefix_symbol=prefix_symbol, postfix_symbol=postfix_symbol,
                            separate_symbol=separate_symbol,
                            decimal_places=decimal_places,
                            singular=singular)
        
    def _normal_cf(self, money: Money, *,
                   force_prefix: bool = False,
                   force_suffix: bool = False,
                   decimal_places: Optional[int] = None) -> str:
        return super().format_currency(money, force_prefix=force_prefix,
                                       force_suffix=force_suffix, 
                                       decimal_places=decimal_places)
        
    def format_currency(self, money: Money, *,
                        force_prefix: bool = False,
                        force_suffix: bool = False,
                        decimal_places: Optional[int] = None) -> str:
        formatter = self.currency_formatter
        if isinstance(formatter, Money.CurrencyFormatter):
            return formatter.format_currency(money, force_prefix=force_prefix, 
                                             force_suffix=force_suffix,
                                             decimal_places=decimal_places)
        else:
            return formatter(money)
    
        

  
        
