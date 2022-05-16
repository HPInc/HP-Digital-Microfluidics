from __future__ import annotations

from mpam.types import MonitoredProperty


sn: int = 100
def next_sn() -> int:
    global sn
    val = sn
    sn += 1
    return val

class Bar:
    count = MonitoredProperty[int]("count",
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
    
class Counter:
    count = MonitoredProperty[int]("count", default=0)
    on_count_change = count.callback_list 
    
    
    
    def inc(self, delta: int = 0) -> None:
        self.count += delta
        
class SpecialCounter(Counter):
    on_change = Counter.count.callback_list

print(SpecialCounter().on_change)

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
