from __future__ import annotations

from enum import Enum, auto
from re import Pattern
import re
from threading import Lock
from typing import TypeVar, Generic, Optional, Callable, Hashable, Union, cast, \
    NoReturn, Any, Mapping, Sequence, Final, Protocol
import pathlib


_T = TypeVar('_T')
_Tco = TypeVar('_Tco', covariant=True)
_H = TypeVar('_H', bound=Hashable)
_V = TypeVar('_V')

Callback = Callable[[], Any]
PathOrStr = Union[str, pathlib.Path]

class Missing(Enum):
    """
    A singleton type to use for optional values when ``None`` is a possible non-
    default value.  Should be used via the type alias :attr:`MissingOr` and the
    constant :attr:`MISSING`, as in ::

        def foo(arg: MissingOr[Optional[A]] = MISSING) -> None:
            if arg is MISSING:
                ...
            else:
                # arg is deduced to be an Optional[A] here
                ...
    """
    SINGLETON = auto()
    def __repr__(self) -> str:
        return "MISSING"
    
    # All Missing values (i.e., MISSING) are considered False
    def __bool__(self) -> bool:
        return False
    

MISSING: Final[Missing] = Missing.SINGLETON
"""
The singleton :class:`Missing` value.
"""
MissingOr = Union[Missing, _T]
"""
Either the given type ``T`` or :attr:`MISSING`.  If the value is not the
constant :attr:`MISSING`, MyPy will deduce it to be ``T``.

Args:
    T: the type (if not :attr:`MISSING`)
"""

def not_Missing(x: MissingOr[_T], *, 
                desc: Optional[Union[str, Callable[[], str]]] = None) -> _T:
    def error_msg() -> str:
        nonlocal desc
        if desc is None:
            desc = "argument to not_MISSING"
        elif not isinstance(desc, str):
            desc = desc()
        return f"{desc} is None"
    assert x is not MISSING, error_msg()
    return x



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

def partial_order_sort(items: Sequence[_T], subsumes: Callable[[_T, _T], bool]) -> list[_T]:
    # Create a mapping of items to their dependencies
    dependencies = {item: set[_T]() for item in items}
    for i, item in enumerate(items):
        for other_item in items[i + 1:]:
            if subsumes(item, other_item):
                dependencies[other_item].add(item)
            elif subsumes(other_item, item):
                dependencies[item].add(other_item)

    # Create a function to perform a depth-first search on the items
    def dfs(item: _T, seen: set[_T], result: list[_T]) -> None:
        if item in seen:
            return
        seen.add(item)
        for dependency in dependencies[item]:
            dfs(dependency, seen, result)
        result.append(item)

    # Perform a depth-first search on all items
    seen = set[_T]()
    result = list[_T]()
    for item in items:
        dfs(item, seen, result)

    return result

_OTcontra = TypeVar("_OTcontra", contravariant=True)

class Gettable(Protocol[_OTcontra, _Tco]):
    """
    A protocol specifying that calling ``__get__()`` on some object will return
    a value.

    Args:
        OTcontra: the (contravariant) type of the object
        Tco: the (covariant) type of the value returned
    """
    def __get__(self, obj: _OTcontra, objtype: type[_OTcontra]) -> _Tco: ... # @UnusedVariable
