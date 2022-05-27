from __future__ import annotations

from devices import joey
from quantities.SI import volts, V
from quantities.dimensions import Voltage
from mpam.types import OnOff
from mpam.device import PowerMode


Voltage.default_units = volts

board = joey.Board(ps_can_toggle=False, ps_initial_voltage=0*V)
ps = board.power_supply

print(ps)

ps.mode = PowerMode.AC
ps.voltage = 20*V
print(ps)

ps.voltage = 80*V
print(ps)

ps.voltage = 600*V
print(ps)
      
ps.current_state = OnOff.OFF
print(ps)

ps.current_state = OnOff.ON
print(ps)

ps.voltage = 0*V
print(ps)
