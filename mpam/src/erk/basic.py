from __future__ import annotations
from typing import TypeVar, Generic, Optional, Callable
from threading import Lock
from re import Pattern
import re

_T = TypeVar('_T')

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