from __future__ import annotations
from quantities.SI import kg
from quantities.dimensions import Scalar

s = Scalar(5)

f: float = float(s)
print(f)

print(f"{3:.2f}")

m = 3*kg
print(type(s))
print(type(m))
print(type(s*m))

# D = TypeVar('D', bound='Quant')
# class Quant(Generic[D]):
#     @overload
#     def __mul__(self, rhs: int) -> D: ...
#     @overload
#     def __mul__(self, rhs: Quant) -> Quant: ...
#     def __mul__(self, rhs): ...
#
#     def __rmul__(self, lhs: int) -> D: ...
#
# class Dist(Quant['Dist']):
#     @overload
#     def __mul__(self, rhs: int) -> Dist: ...
#     # @overload
#     # def __mul__(self, rhs: Dist) -> Area: ...
#     @overload
#     def __mul__(self, rhs: Quant) -> Quant: ...
#     def __mul__(self, rhs): 
#         return super().__mul__(rhs)
#
# class Area(Quant['Area']): ...
    
# class Quant:
#     @overload
#     def __mul__(self:D , rhs: int) -> D: ...
#     @overload
#     def __mul__(self, rhs: Quant) -> Quant: ...
#     def __mul__(self, rhs): ...
#
#     def __rmul__(self: D, lhs: int) -> D: ...
#
# class Dist(Quant):
#     @overload
#     def __mul__(self, rhs: int) -> Dist: ...
#     @overload
#     def __mul__(self, rhs: Dist) -> Area: ...
#     @overload
#     def __mul__(self, rhs: Quant) -> Quant: ...
#     def __mul__(self, rhs): 
#         return super().__mul__(rhs)
#
#
# class Area(Quant): ...
#
print(1/0)
