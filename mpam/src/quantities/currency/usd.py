from __future__ import annotations
from ..money import Currency, Denomination
from ..dimensions import Money
from typing import Sequence

usd = USD = Currency("USD")
dollar = dollars = USD.new_denomination(USD, "dollars", singular="dollar", prefix_symbol="$", 
                                        decimal_places=2)
usd.currency_formatter = dollars
cent = cents = USD.new_denomination(USD/100, "cents", singular="cent", postfix_symbol="¢")
penny = pennies = USD.new_denomination(cent, "pennies", singular="penny")
nickel = nickels = USD.new_denomination(5*cents, "nickels", singular="nickel")
dime = dimes = USD.new_denomination(10*cents, "dimes", singular="dime")
quarter = quarters = USD.new_denomination(25*cents, "quarters", singular="quarter")
bit = bits = USD.new_denomination(dollar/8, "bits", singular="bit")
half_dollar = half_dollars = USD.new_denomination(50*cents, "half dollars", singular="half dollar")

coins = (pennies, nickels, dimes, quarters, half_dollars)
common_coins = (pennies, nickels, dimes, quarters)

def _bill(n: int) -> Denomination:
    return USD.new_denomination(n*dollars, f"${n} bills", singular=f"${n} bill")
one_dollar_bill = one_dollar_bills = _bill(1)
two_dollar_bill = two_dollar_bills = _bill(2)
five_dollar_bill = five_dollar_bills = _bill(5)
ten_dollar_bill = ten_dollar_bills = _bill(10)
twenty_dollar_bill = twenty_dollar_bills = _bill(20)
fifty_dollar_bill = fifty_dollar_bills = _bill(50)
hundred_dollar_bill = hundred_dollar_bills = _bill(100)

bills = (one_dollar_bills, two_dollar_bills, five_dollar_bills,
         ten_dollar_bills, twenty_dollar_bills, fifty_dollar_bills,
         hundred_dollar_bills)
def bills_to(limit: Money) -> Sequence[Denomination]:
    print(f"Limit is {limit}")
    return tuple(d for d in bills if 1*d <= limit)

common_bills = bills_to(20*dollars)
