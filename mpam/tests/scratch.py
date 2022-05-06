from __future__ import annotations
from typing import TypeVar, Generic, Callable

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
V = TypeVar("V")

class Source(Generic[T]):
    _callbacks: list[Callable[[T], None]]
    
    def __init__(self) -> None:
        self._callbacks = []
        
    def add_callback(self, cb: Callable[[T], None]) -> None:
        self._callbacks.append(cb)
        
    def transform(self, xf: Callable[[T], V]) -> Source[V]:
        sink = Sink[V]()
        self.add_callback(lambda val: sink.receive(xf(val)))
        return sink
        
class Sink(Source[T]):
    def receive(self, val: T) -> None:
        for cb in self._callbacks:
            cb(val)

class CoSource(Generic[T_co]):
    _callbacks: list[Callable[[T_co], None]]
    
    def __init__(self) -> None:
        self._callbacks = []
        
    def add_callback(self, cb: Callable[[T_co], None]) -> None:
        self._callbacks.append(cb)
        
    def transform(self, xf: Callable[[T_co], V]) -> CoSource[V]:
        sink = ContraSink[V]()
        def turn_around(val) -> None:
            sink.receive(xf(val))
        self.add_callback(turn_around)
        # self.add_callback(lambda val: sink.receive(xf(val)))
        return sink
        
class ContraSink(CoSource[T_contra]):
    def receive(self, val: T_contra) -> None:
        for cb in self._callbacks:
            cb(val)
            
class A: ...
class B(A): ...

a_sink = ContraSink[A]()
a_sink.add_callback(lambda a: print(a))

a_source: CoSource[A] = a_sink
a_source.add_callback(lambda a: print(a))
def cb1(a: A): ...
a_source.add_callback(cb1)

str_source = a_source.transform(lambda val: f"transformed: {val}")
str_source.add_callback(lambda a: print(a))

a_sink.receive(A())
