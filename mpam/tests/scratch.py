from __future__ import annotations

from mpam.types import MonitoredProperty, ConfigParams
from argparse import Namespace
from mpam.device import System
from devices import joey

sn: int = 100
def next_sn() -> int:
    global sn
    val = sn
    sn += 1
    return val

class Bar:
    count = MonitoredProperty[int](#"count",
                                    # default=0, 
                                    # default_fn = lambda _: next_sn(),
                                    ) #, init=0)
    on_count_change = count.callback_list
    has_count = count.value_check
    on_inc = on_count_change.filtered(lambda old, new: new > old)
    
    @count.transform
    def double(self, val: int) -> int:
        return 2*val
    
    @count.transform(chain=True)
    def add_one(self, val: int) -> int:
        return val+1

    # @count.transform
    # def clip(self, val: int) -> int:
    #     return min(val, 10)
    
    # @count.transform
    # def enforce_range(self, val: int) -> MissingOr[int]:
    #     return MISSING if val > 10 else val
    

bar = Bar()

print(bar.has_count)
bar.on_count_change(lambda old, new: print(f"{old} -> {new}"))
bar.on_inc(lambda old, new: print(f"incremented from {old} to {new}"))

# print(bar.count)
bar.count = 5    
print(bar.count)
print(bar.has_count)
bar.count = 10
print(bar.count)
bar.count = 10
print(bar.count)
bar.count = 20
print(bar.count)
bar.count = 15
print(bar.count)
del bar.count
bar.count = 2
print(bar.count)
bar.count = 6
print(bar.count)
bar.count += 1
print(bar.count)

defaults = Namespace(highlight_reservations=False)
cmd_line = Namespace()

params = ConfigParams(defaults=defaults, cmd_line=cmd_line, 
                      from_code = {"highlight_reservations": True})

print(params.highlight_reservations)
x = params.get("highlight_reservations", 1, expect=bool)
print(x)
# x = params.get("highlight_reservations", expect=bool)

system = System(board=joey.Board())

system.run_monitored(lambda sys: ...)
