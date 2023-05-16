from __future__ import annotations

from typing import Optional, Any

class A:
    _name: Optional[str] = None
    
    @property
    def name(self) -> Optional[str]:
        return self._name
    
    @name.setter
    def name(self, n: str) -> None:
        print(f"Name is now {n}")
        self._name = n
        
    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = f"{owner.__qualname__}.{name}"
        
class B:
    x = A()
    
class C:
    y = B.x
    
print(B.x._name)
print(C.y._name)
        