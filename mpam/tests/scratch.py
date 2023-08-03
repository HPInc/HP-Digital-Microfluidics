from __future__ import annotations
from typing import Generic, TypeVar, Any, Callable, Final
from enum import Enum, auto

T = TypeVar("T")

class Obj(Generic[T]):
    has_value: bool = False
    
    def when_value(self, fn: Callable[[T], Any]) -> None:
        if self.has_value:
            ...
            
            
class State(Enum):
    NO_VAL = auto()
    HAS_VAL = auto()
    HAS_ERROR = auto()
    
class Obj2(Generic[T]):
    has_error_val: Final = State.HAS_ERROR
    state: State = State.NO_VAL
    
    def when_value(self, fn: Callable[[T], Any]) -> None:
        if self.state is self.has_error_val:
            ...
            
