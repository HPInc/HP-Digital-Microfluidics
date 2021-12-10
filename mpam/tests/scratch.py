from __future__ import annotations
from typing import Optional

class A:
    _p: Optional[int] = None
    @property
    def p(self) -> int:
        return self._p or 1
    
    @p.setter
    def p(self, v: int) -> None:
        self._p = v
    
class B(A):
    @property
    def p(self) -> int:
        return 2
    
    @p.setter
    
    
b = B()
print(b.p)