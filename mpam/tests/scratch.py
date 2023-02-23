from __future__ import annotations
from quantities.money import USD, UKP, dollars, cents
from quantities.SI import day
from quantities.dimensions import Money

a = 1*USD
print(a)    

b = 5*UKP + 2*UKP   

print(b)

Money.default_units = USD

salary = 25*UKP/day

#UKP.set_exchange_rate(1.2*USD)
USD.set_exchange_rate(0.8*UKP)
# USD.set_exchange_rate(0.5*UKP)
print(salary.in_units(USD/day))
print(salary.in_units(UKP/day))

print(f"{b:.2f}")

print((1*USD).decomposed((dollars, cents), required="all"))

print((2*USD+3*UKP).in_units(UKP))





