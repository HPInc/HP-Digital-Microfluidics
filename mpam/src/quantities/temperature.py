from __future__ import annotations
from quantities import dimensions
from typing import overload, Union, Final, ClassVar
from quantities.SI import K

class TemperaturePoint:
    absolute: Final[dimensions.Temperature]
    
    default_units: ClassVar[Unit]
    
    
    
    def __init__(self, absolute: dimensions.Temperature) -> None:
        self.absolute = absolute
        
    def __add__(self, rhs: dimensions.Temperature) -> TemperaturePoint:
        return TemperaturePoint(self.absolute+rhs)
    
    def __radd__(self, lhs: dimensions.Temperature) -> TemperaturePoint:
        return TemperaturePoint(lhs+self.absolute)

    @overload    
    def __sub__(self, rhs: TemperaturePoint) -> dimensions.Temperature: ...  # @UnusedVariable
    @overload
    def __sub__(self, rhs: dimensions.Temperature) -> TemperaturePoint: ...  # @UnusedVariable
    def __sub__(self, rhs: Union[TemperaturePoint, dimensions.Temperature]):
        if isinstance(rhs, TemperaturePoint):
            return self.absolute-rhs.absolute
        else:
            return TemperaturePoint(self.absolute-rhs)

    def __hash__(self) -> int:
        return hash(self.absolute)
    
    def __lt__(self, rhs: TemperaturePoint) -> bool:
        return self.absolute < rhs.absolute

    def __le__(self, rhs: TemperaturePoint) -> bool:
        return self.absolute <= rhs.absolute
    
    def as_number(self, unit: Unit) -> float:
        return self.absolute.magnitude/unit.relative_to_kelvin+unit.absolute_zero
    
    def in_units(self, unit: Unit) -> str:
        return f"{self.as_number(unit):.2f} {unit.abbr}"
    
    def __repr__(self) -> str:
        return f"Timepoint({self.absolute})"
    
    def __str__(self) -> str:
        return self.in_units(TemperaturePoint.default_units)
    
    
class Unit:
    absolute_zero: Final[float]
    relative_to_kelvin: Final[float]
    abbr: Final[str]
    
    def __init__(self, abbr: str, 
                 absolute_zero: float,
                 relative_to_kelvin: float) -> None:
        self.abbr = abbr
        self.absolute_zero = absolute_zero
        self.relative_to_kelvin = relative_to_kelvin
        
    def __rmul__(self, lhs: float) -> TemperaturePoint:
        return TemperaturePoint(((lhs-self.absolute_zero)*self.relative_to_kelvin)*K)
        
abs_K = Unit('K', 0, 1)
abs_C = Unit('°C', -273.15, 1)
abs_F = Unit('°F', -459.67, (5/9))
    
TemperaturePoint.default_units = abs_C