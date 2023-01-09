from __future__ import annotations
from typing import Callable

def test() -> tuple[Callable[[int], None], Callable[[], int]]:
    x: int
    def foo(i: int) -> None:
        nonlocal x
        x = i
        print(f"Setting to {x}")
        
    def bar() -> int:
        return x
    
    return (foo, bar)


setter, getter = test()
setter(5)
print(f"got {getter()}")
    

                    