from __future__ import annotations
from quantities.core import BaseDim, DerivedDim, _DecomposedQuantity,\
    NamedDim, Dimensionality

class Scalar(NamedDim['Scalar']):
    _dim = Dimensionality['Scalar']((), 'scalar')
    def __float__(self) -> float:
        return float(self.magnitude)
    # @overload
    # def __mul__(self, rhs: float) -> Scalar: ...  # @UnusedVariable
    # # @overload
    # # def __mul__(self, rhs: Time) -> Time: ...  # @UnusedVariable
    # @overload
    # def __mul__(self, rhs: Quantity) -> Quant: ...  # @UnusedVariable
    # @overload
    # def __mul__(self, rhs: UnitExpr) -> Quant: ...  # @UnusedVariable
    # def __mul__(self, rhs):
    #     return super().__mul__(rhs)    
    
Scalar._dim.quant_class = Scalar


class Mass(BaseDim['Mass']): ...
    

class Distance(BaseDim['Distance']): ...
    # @overload
    # def __pow__(self, rhs: Literal[2]) -> 'Area': ...  # @UnusedVariable
    # @overload
    # def __pow__(self, rhs: Literal[3]) -> 'Volume': ...  # @UnusedVariable
    # @overload
    # def __pow__(self, rhs: int) -> Quantity: ...  # @UnusedVariable
    # def __pow__(self, rhs: int):
    #     return super().__pow__(rhs)
    #
    # class DistanceUnitExpr(UnitExpr['Distance']):
    #     @overload
    #     def __pow__(self, rhs: Literal[2]) -> 'Area.AreaUnitExpr': ...  # @UnusedVariable
    #     @overload
    #     def __pow__(self, rhs: Literal[3]) -> 'Volume.VolumeUnitExpr': ...  # @UnusedVariable
    #     @overload
    #     def __pow__(self, rhs: int) -> UnitExpr: ...  # @UnusedVariable
    #     def __pow__(self, rhs: int):
    #         return super().__pow__(rhs)
    #
    # class DistanceUnit(Unit['Distance'], DistanceUnitExpr):
    #     ...

    # @overload
    # def __mul__(self, rhs: float) -> Distance: ...  # @UnusedVariable
    # @overload
    # def __mul__(self, rhs: Distance) -> Area: ...  # @UnusedVariable
    # @overload
    # def __mul__(self, rhs: Quant) -> Quant: ...  # @UnusedVariable
    # @overload
    # def __mul__(self, rhs: UnitExpr) -> Quant: ...  # @UnusedVariable
    # def __mul__(self, rhs):
    #     return super().__mul__(rhs)

class Time(BaseDim['Time']): 
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
    

class Temperature(BaseDim['Temperature']): ...

class LumInt(BaseDim['LumInt']): ...

class Current(BaseDim['Current']): ...

class Amount(BaseDim['Amount']): ...

Angle = Scalar
SolidAngle = Scalar

class Area(DerivedDim['Area']): 
    derived = Distance.dim()**2
    # class AreaUnitExpr(UnitExpr['Area']): ...

class Volume(DerivedDim['Volume']): 
    derived = Distance.dim()**3
    # class VolumeUnitExpr(UnitExpr['Volume']): ...
    
class Density(DerivedDim['Density']):
    derived = Mass.dim()/Volume.dim()
    
class Substance: ...
class Solution: ...
class Solvent: ...
    
MassConcentration = Density
    
class MolarConcentration(DerivedDim['MolarConcentration']):
    derived = Amount.dim()/Volume.dim()
    
Molarity = MolarConcentration
    
class SpecificVolume(DerivedDim['SpecificVolume']):
    derived = Volume.dim()/Mass.dim()
    
class VolumeConcentration(DerivedDim['VolumeConcentration']):
    derived = Volume.dim().of(Substance)/Volume.dim()    
    
class Frequency(DerivedDim['Frequency']): 
    derived = Scalar.dim()/Time.dim()
    def __rtruediv__(self, lhs: float) -> Time:
        return super().__rtruediv__(lhs).a(Time)
    

class Radioactivity(DerivedDim['Radioactivity']): 
    derived = Scalar.dim()/Time.dim()

class Velocity(DerivedDim['Velocity']): 
    derived = Distance.dim()/Time.dim()

class Acceleration(DerivedDim['Acceleration']): 
    derived = Velocity.dim()/Time.dim()

class Force(DerivedDim['Force']): 
    derived = Mass.dim()*Acceleration.dim()

class Work(DerivedDim['Work']): 
    derived = Force.dim()*Distance.dim()

class Pressure(DerivedDim['Pressure']): 
    derived = Force.dim()/Area.dim()

class Power(DerivedDim['Power']): 
    derived = Work.dim()/Time.dim()

LumFlux = LumInt

class Illuminance(DerivedDim['Illuminance']): 
    derived = LumFlux.dim()/Area.dim()

class Charge(DerivedDim['Charge']): 
    derived = Current.dim()*Time.dim()

class Voltage(DerivedDim['Voltage']): 
    derived = Work.dim()/Charge.dim()

Emf = ElecPotential = Voltage

class Flux(DerivedDim['Flux']): 
    derived = Voltage.dim()*Time.dim()

MagneticFlux = Flux

class FluxDensity(DerivedDim['FluxDensity']): 
    derived = Flux.dim()/Area.dim()

MagneticInduction = FluxDensity

class Capacitance(DerivedDim['Capacitance']): 
    derived = Charge.dim()/Voltage.dim()

class Resistance(DerivedDim['Resistance']): 
    derived = Voltage.dim()/Current.dim()

class Conductance(DerivedDim['Conductance']): 
    derived = Current.dim()/Voltage.dim()

class Inductance(DerivedDim['Inductance']): 
    derived = Resistance.dim()*Time.dim()

class IonizingRadDose(DerivedDim['IonizingRadDose']): 
    derived = Work.dim()/Mass.dim()


    
    