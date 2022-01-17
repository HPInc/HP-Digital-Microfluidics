from __future__ import annotations
from typing import TypeVar, Generic, Optional, Callable, Hashable
from threading import Lock
from re import Pattern
import re

_T = TypeVar('_T')
_H = TypeVar('_H', bound=Hashable)

_ValTuple = tuple[bool, _T]

class Lazy(Generic[_T]):
    _val: _T
    _func: Optional[Callable[[], _T]]
    
    def __init__(self, func: Callable[[], _T]):
        lock = Lock()
        def compute_and_set() -> _T:
            with lock:
                if self._func is not None:
                    v = func()
                    self._val = v
                    self._func = None
                    return v
                else:
                    return self._val
        self._func = compute_and_set
    
    @property
    def value(self) -> _T:
        func = self._func
        if func is not None:
            return func()
        else:
            return self._val
        
class LazyPattern(Lazy[Pattern]):
    def __init__(self, pattern: str, flags: int = 0):
        super().__init__(lambda: re.compile(pattern, flags))
        
        
class Count(dict[_H,int]):
    def __missing__(self, elt: _H) -> int:  # @UnusedVariable
        return 0
    
    def inc(self, elt: _H) -> int:
        self[elt] += 1
        return self[elt]
    
    def dec(self, elt: _H) -> int:
        old = self[elt]
        new = old-1
        if old == 0:
            raise KeyError(f"No count for {elt} in Count object")
        elif new == 0:
            del self[elt]
        else:
            self[elt] = new
        return new
    
def not_None(x: Optional[_T]) -> _T:
    assert x is not None
    return x


def always(val: _T) -> Callable[[], _T]:
    return lambda: val
        
class ComputedDefaultDict(dict[_H,_T]):
    def __init__(self, factory: Callable[[_H], _T]):
        self.factory = factory
    def __missing__(self, key: _H) -> _T:
        ret = self.factory(key)
        self[key] = ret
        return ret
