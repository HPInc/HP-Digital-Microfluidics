from __future__ import annotations
from typing import TypeVar, Generic, Optional, Callable, Hashable, Union, cast,\
    NoReturn, Any, Mapping
from threading import Lock
from re import Pattern
import re

_T = TypeVar('_T')
_H = TypeVar('_H', bound=Hashable)
_V = TypeVar('_V')

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
    
ValOrFn = Union[_T, Callable[[], _T]]

def ensure_val(val: ValOrFn[_T], as_class: type[_T]) -> _T:
    # Note, we're making an assumption that the type passed in is exactly _T. It
    # could be a subtype, in which case, this might not work, but the explicit
    # call we would have made would've failed, too.
    if isinstance(val, as_class):
        return val
    fn = cast(Callable[[], _T], val)
    return fn()

def not_None(x: Optional[_T], *, 
             desc: Optional[ValOrFn[str]] = None) -> _T:
    def error_msg() -> str:
        d = "argument to not_None" if desc is None else ensure_val(desc, str)
        return f"{d} is None"
    assert x is not None, error_msg()
    return x

def if_not_None(x: Optional[_T], fn: Callable[[_T], Any]) -> None:
    if x is not None:
        fn(x)
        
def call_unless_None(obj: Optional[_T], fn: Callable[[_T], _V]) -> Optional[_V]:
    return None if obj is None else fn(obj)

def map_unless_None(obj: Optional[_T], m: Mapping[_T, _V]) -> Optional[_V]:
    return None if obj is None else m[obj]


def always(val: _T) -> Callable[[], _T]:
    return lambda: val

def to_const(val: _T) -> Callable[[Any], _T]:
    return lambda _: val

class ComputedDefaultDict(dict[_H,_T]):
    def __init__(self, factory: Callable[[_H], _T]):
        self.factory = factory
    def __missing__(self, key: _H) -> _T:
        ret = self.factory(key)
        self[key] = ret
        return ret
    

def assert_never(value: NoReturn) -> NoReturn:
    assert False, f'Unhandled value: {value} ({type(value).__name__})'


