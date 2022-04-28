from __future__ import annotations

def foo(a: int = 0, b: int = 0, *, c: int = 0):
    print(a, b, c)
    
foo(b=2, c=3)