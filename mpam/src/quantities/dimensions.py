from __future__ import annotations

from quantities.core import BaseDim, DerivedDim, _DecomposedQuantity, Scalar,\
    Quantity, UnitExpr, QorU
from typing import overload, Literal, Union


class Mass(BaseDim): 
    @overload # type: ignore[override]
    def __mul__(self, rhs: float) -> Mass: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: QorU[Acceleration]) -> Force: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: Quantity) -> Quantity: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: UnitExpr) -> Quantity: ...  # @UnusedVariable
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) ->  Quantity:
        return super().__mul__(rhs)

    @overload # type: ignore[override]
    def __truediv__(self, rhs: float) -> Mass: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: QorU[Volume]) -> Density: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: Quantity) -> Quantity: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: UnitExpr) -> Quantity: ...  # @UnusedVariable
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) ->  Quantity:
        return super().__mul__(rhs)

class Distance(BaseDim): 
    @overload
    def __pow__(self, rhs: Literal[2]) -> Area: ...  # @UnusedVariable
    @overload
    def __pow__(self, rhs: Literal[3]) -> Volume: ...  # @UnusedVariable
    @overload
    def __pow__(self, rhs: int) -> Quantity: ...  # @UnusedVariable
    def __pow__(self, rhs: int):
        return super().__pow__(rhs)
    
    @overload # type: ignore[override]
    def __mul__(self, rhs: float) -> Distance: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: QorU[Distance]) -> Area: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: QorU[Area]) -> Volume: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: QorU[Force]) -> Work: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: Quantity) -> Quantity: ...  # @UnusedVariable
    @overload
    def __mul__(self, rhs: UnitExpr) -> Quantity: ...  # @UnusedVariable
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) ->  Quantity:
        return super().__mul__(rhs)
    
    @overload # type: ignore[override]
    def __truediv__(self, rhs: float) -> Distance: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: QorU[Time]) -> Velocity: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: Quantity) -> Quantity: ...  # @UnusedVariable
    @overload
    def __truediv__(self, rhs: UnitExpr) -> Quantity: ...  # @UnusedVariable
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) ->  Quantity:
        return super().__mul__(rhs)
    

class Time(BaseDim): 
    def in_HMS(self, sep: str = ":") -> _DecomposedQuantity.Joined:
        from quantities.SI import hours, minutes, seconds
        return self.decomposed([hours, minutes, seconds], required="all").joined(sep, 2)
    def in_HM(self, sep: str = ":") -> _DecomposedQuantity.Joined:
        from quantities.SI import hours, minutes
        return self.decomposed([hours, minutes], required="all").joined(sep, 2)
    def in_MS(self, sep: str = ":") -> _DecomposedQuantity.Joined:
        from quantities.SI import minutes, seconds
        return self.decomposed([minutes, seconds], required="all").joined(sep, 2)
    def __rtruediv__(self, lhs: float) -> Frequency:
        return super().__rtruediv__(lhs).a(Frequency)
    
    # class _UnitExpr(UnitExpr[Time]): ...
    # class _Unit(Unit[Time]): ...
    #
    # def as_unit(self, abbr:str, *, singular:Optional[str]=None)->Time._Unit:
    #     return Time._Unit(abbr, self, singular=singular)
    #
    # @classmethod
    # def base_unit(cls, abbr: str, *, singular: Optional[str]=None) -> _Unit:
    #     return cast(Time._Unit, super().base_unit(abbr, singular=singular))
    

class Temperature(BaseDim): ...

class LumInt(BaseDim): ...

class Current(BaseDim): ...

class Amount(BaseDim): ...

Angle = Scalar
SolidAngle = Scalar

class Area(DerivedDim): 
    derived = Distance**2
    # class AreaUnitExpr(UnitExpr['Area']): ...

class Volume(DerivedDim): 
    derived = Distance**3
    # class VolumeUnitExpr(UnitExpr['Volume']): ...
    
class Density(DerivedDim):
    derived = Mass/Volume
    
class Substance: ...
class Solution: ...
class Solvent: ...
    
MassConcentration = Density
    
class MolarConcentration(DerivedDim):
    derived = Amount/Volume
    
Molarity = MolarConcentration
    
class SpecificVolume(DerivedDim):
    derived = Volume/Mass
    
class VolumeConcentration(DerivedDim):
    derived = Volume[Substance]/Volume
    
class Frequency(DerivedDim): 
    derived = Scalar/Time
    def __rtruediv__(self, lhs: float) -> Time:
        return super().__rtruediv__(lhs).a(Time)
    

class Radioactivity(DerivedDim): 
    derived = Scalar/Time

class Velocity(DerivedDim): 
    derived = Distance/Time

class Acceleration(DerivedDim): 
    derived = Velocity/Time

class Force(DerivedDim): 
    derived = Mass*Acceleration

class Work(DerivedDim): 
    derived = Force*Distance

class Pressure(DerivedDim): 
    derived = Force/Area

class Power(DerivedDim): 
    derived = Work/Time

LumFlux = LumInt

class Illuminance(DerivedDim): 
    derived = LumFlux/Area

class Charge(DerivedDim): 
    derived = Current*Time

class Voltage(DerivedDim): 
    derived = Work/Charge

Emf = ElecPotential = Voltage

class Flux(DerivedDim): 
    derived = Voltage*Time

MagneticFlux = Flux

class FluxDensity(DerivedDim): 
    derived = Flux/Area

MagneticInduction = FluxDensity

class Capacitance(DerivedDim): 
    derived = Charge/Voltage

class Resistance(DerivedDim): 
    derived = Voltage/Current

class Conductance(DerivedDim): 
    derived = Current/Voltage

class Inductance(DerivedDim): 
    derived = Resistance*Time

class IonizingRadDose(DerivedDim): 
    derived = Work/Mass


    
    