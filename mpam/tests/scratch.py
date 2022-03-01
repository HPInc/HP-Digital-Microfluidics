from __future__ import annotations

from typing import TypeVar, Union, overload
from quantities.US import ft, acre
from quantities.SI import sec, m, kg

D = TypeVar('D', bound='Base')
class Base:
    @overload
    def foo(self, rhs: float) -> Base: ...
    # @overload
    # def foo(self: D, rhs: float) -> D: ...
    # @overload
    # def foo(self, rhs: Y) -> Base: ...
    @overload
    def foo(self, rhs: Base) -> Base: ...
    # def foo(self, rhs: Union[float,Base]) -> Base:
    # def foo(self, rhs: Base) -> Base:
    def foo(self, rhs: Union[float, Base]) -> Base:
        ...
class Y(Base): ...
        
class X(Base):
    @overload #type: ignore[override]
    def foo(self, rhs: float) -> X: ...
    @overload
    def foo(self, rhs: Y) -> Base: ...
    @overload
    def foo(self, rhs: Base) -> Base: ...
    def foo(self, rhs: Union[float, Base]) -> Base:
        ...

x = X()
y = Y()
b: Base = x
# reveal_type(x*y)

d = 2*ft
reveal_type(3*kg*(m/sec**2))
