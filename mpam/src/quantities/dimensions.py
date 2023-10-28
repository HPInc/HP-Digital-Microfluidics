
from __future__ import annotations

from quantities.core import BaseDim, DerivedDim, Scalar,    Quantity, UnitExpr, Unit, AbbrExp, ScalarUnitExpr
from typing import overload, Union, Literal, Optional, cast

###########################################
# This is a generated file. Do not edit it.
#
# To regenerate the file, edit and run
# tools/gen_dims.py
###########################################
        

import time
from abc import ABC, abstractmethod
from typing import Protocol, Sequence, ClassVar, Callable, Iterable, TypeVar
from quantities.core import Dimensionality, _BoundQuantity, _DecomposedQuantity, _DirectCreation

T = TypeVar('T')

Angle = Scalar
SolidAngle = Scalar


class Substance:
    """
    A restriction base class.  
    """
    ... 
        

class Solution:
    """
    A restriction base class.  
    """
    ... 
        

class Solvent:
    """
    A restriction base class.  
    """
    ... 
        
class Mass(BaseDim):
    """
    A :class`.Quantity` representing mass
    """
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Mass: ...
    @overload
    def __mul__(self, _rhs: Union[SpecificVolume, UnitExpr[SpecificVolume]]) -> Volume: ...
    @overload
    def __mul__(self, _rhs: Union[IonizingRadDose, UnitExpr[IonizingRadDose]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> DIM_dist1_mass1: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Mass: ...
    @overload
    def __mul__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> Force: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Mass, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Mass: ...
    @overload
    def __truediv__(self, _rhs: Union[Density, UnitExpr[Density]]) -> Volume: ...
    @overload
    def __truediv__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> Density: ...
    @overload
    def __truediv__(self, _rhs: Union[Mass, UnitExpr[Mass]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Mass: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Mass, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> MassUnitExpr:
        return MassUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> MassUnit:
        return MassUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> MassUnit:
        return cls._base_unit(MassUnit, abbr, singular=singular)
            

class MassUnitExpr(UnitExpr[Mass]):
    """
    A :class:`.UnitExpr`[:class:`Mass`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Mass]] = None, 
                singular: Optional[str] = None) -> MassUnit:
        return cast(MassUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Mass: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[SpecificVolume]) -> VolumeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[IonizingRadDose]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Distance]) -> DIM_dist1_mass1UnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> MassUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Acceleration]) -> ForceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Mass, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Mass: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Density]) -> VolumeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Volume]) -> DensityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Mass]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> MassUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Mass, UnitExpr]:
        return super().__truediv__(rhs)


class MassUnit(Unit[Mass], MassUnitExpr):
    """
    A :class:`.Unit`[:class:`Mass`] and a :class:`MassUnitExpr`
    """
    ...
        

class Distance(BaseDim):
    """
    A :class`.Quantity` representing distance
    """
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[0]) -> Scalar: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> Distance: ...
    @overload
    def __pow__(self, _rhs: Literal[2]) -> Area: ...
    @overload
    def __pow__(self, _rhs: Literal[3]) -> Volume: ...
    @overload
    def __pow__(self, _rhs: int) -> Quantity: ...
    def __pow__(self, rhs: int) -> Quantity:
        return super().__pow__(rhs)

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Distance: ...
    @overload
    def __mul__(self, _rhs: Union[Force, UnitExpr[Force]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Velocity: ...
    @overload
    def __mul__(self, _rhs: Union[Area, UnitExpr[Area]]) -> Volume: ...
    @overload
    def __mul__(self, _rhs: Union[Mass, UnitExpr[Mass]]) -> DIM_dist1_mass1: ...
    @overload
    def __mul__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Area: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Distance: ...
    @overload
    def __mul__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> IonizingRadDose: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Distance, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Distance: ...
    @overload
    def __truediv__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[DIM_time2, UnitExpr[DIM_time2]]) -> Acceleration: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Velocity: ...
    @overload
    def __truediv__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Distance: ...
    @overload
    def __truediv__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> DIM_time2: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Distance, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> DistanceUnitExpr:
        return DistanceUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> DistanceUnit:
        return DistanceUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> DistanceUnit:
        return cls._base_unit(DistanceUnit, abbr, singular=singular)
            

class DistanceUnitExpr(UnitExpr[Distance]):
    """
    A :class:`.UnitExpr`[:class:`Distance`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Distance]] = None, 
                singular: Optional[str] = None) -> DistanceUnit:
        return cast(DistanceUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[0]) -> ScalarUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> DistanceUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[2]) -> AreaUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[3]) -> VolumeUnitExpr: ...
    @overload
    def __pow__(self, _rhs: int) -> UnitExpr: ...
    def __pow__(self, rhs: int) -> UnitExpr:
        return super().__pow__(rhs)

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Distance: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Force]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> VelocityUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Area]) -> VolumeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Mass]) -> DIM_dist1_mass1UnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Distance]) -> AreaUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> DistanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Acceleration]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Distance, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Distance: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Velocity]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[DIM_time2]) -> AccelerationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> VelocityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Distance]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> DistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Acceleration]) -> DIM_time2UnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Distance, UnitExpr]:
        return super().__truediv__(rhs)


class DistanceUnit(Unit[Distance], DistanceUnitExpr):
    """
    A :class:`.Unit`[:class:`Distance`] and a :class:`DistanceUnitExpr`
    """
    ...
        

class Time(BaseDim):
    """
    A :class`.Quantity` representing time
    """
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> Frequency: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> Scalar: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> Time: ...
    @overload
    def __pow__(self, _rhs: Literal[2]) -> DIM_time2: ...
    @overload
    def __pow__(self, _rhs: int) -> Quantity: ...
    def __pow__(self, rhs: int) -> Quantity:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Frequency:
        return cast(Frequency, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Time: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Scalar: ...
    @overload
    def __mul__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> Distance: ...
    @overload
    def __mul__(self, _rhs: Union[PriceRate, UnitExpr[PriceRate]]) -> Money: ...
    @overload
    def __mul__(self, _rhs: Union[HeatingRate, UnitExpr[HeatingRate]]) -> Temperature: ...
    @overload
    def __mul__(self, _rhs: Union[FlowRate, UnitExpr[FlowRate]]) -> Volume: ...
    @overload
    def __mul__(self, _rhs: Union[DataRate, UnitExpr[DataRate]]) -> Storage: ...
    @overload
    def __mul__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Charge: ...
    @overload
    def __mul__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Capacitance: ...
    @overload
    def __mul__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Inductance: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> DIM_time2: ...
    @overload
    def __mul__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Power, UnitExpr[Power]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Time: ...
    @overload
    def __mul__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> Velocity: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Time, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> DIM_time2: ...
    @overload
    def __truediv__(self, _rhs: Union[DIM_time2, UnitExpr[DIM_time2]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Inductance, UnitExpr[Inductance]]) -> Conductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Inductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Capacitance: ...
    @overload
    def __truediv__(self, _rhs: Union[Capacitance, UnitExpr[Capacitance]]) -> Resistance: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Time, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> TimeUnitExpr:
        return TimeUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> TimeUnit:
        return TimeUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> TimeUnit:
        return cls._base_unit(TimeUnit, abbr, singular=singular)
            

    def sleep(self) -> None:
        from quantities import SI
        time.sleep(self.as_number(SI.seconds))
    @classmethod
    def rate_from(cls, val: Union[Time, Frequency]) -> Time:
        return val if isinstance(val, Time) else 1/val
    def in_HMS(self, sep: str = ":") -> _DecomposedQuantity.Joined:
        """
        Format the :class:`.Time` as hours, minutes, and seconds, separated by
        ``sep``.  If the resulting object is formatted, the precision will only
        apply to the seconds.  All numbers format with (at least) two digits
        with leading zeroes.
        
        Keyword Args:
            sep: the separator (default=":") to use between numbers
        """
        from quantities.SI import hours, minutes, seconds
        return self.decomposed([hours, minutes, seconds], required="all").joined(sep, 2)
    def in_HM(self, sep: str = ":") -> _DecomposedQuantity.Joined:
        """
        Format the :class:`.Time` as hours and minutes, separated by ``sep``.
        If the resulting object is formatted, the precision will only apply to
        the minutes.  Both numbers format with (at least) two digits with leading
        zeroes.
        
        Keyword Args:
            sep: the separator (default=":") to use between numbers
        """
        from quantities.SI import hours, minutes
        return self.decomposed([hours, minutes], required="all").joined(sep, 2)
    def in_MS(self, sep: str = ":") -> _DecomposedQuantity.Joined:
        """
        Format the :class:`.Time` as minutes and seconds, separated by ``sep``.
        If the resulting object is formatted, the precision will only apply to
        the seconds.  Both numbers format with (at least) two digits with leading
        zeroes.
        
        Keyword Args:
            sep: the separator (default=":") to use between numbers
        """
        from quantities.SI import minutes, seconds
        return self.decomposed([minutes, seconds], required="all").joined(sep, 2)


class TimeUnitExpr(UnitExpr[Time]):
    """
    A :class:`.UnitExpr`[:class:`Time`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Time]] = None, 
                singular: Optional[str] = None) -> TimeUnit:
        return cast(TimeUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> FrequencyUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> ScalarUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> TimeUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[2]) -> DIM_time2UnitExpr: ...
    @overload
    def __pow__(self, _rhs: int) -> UnitExpr: ...
    def __pow__(self, rhs: int) -> UnitExpr:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Frequency:
        return cast(Frequency, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Time: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> ScalarUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Velocity]) -> DistanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[PriceRate]) -> MoneyUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[HeatingRate]) -> TemperatureUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[FlowRate]) -> VolumeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[DataRate]) -> StorageUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Current]) -> ChargeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Conductance]) -> CapacitanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Resistance]) -> InductanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> DIM_time2UnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Voltage]) -> FluxUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Power]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> TimeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Acceleration]) -> VelocityUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Time, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Time: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> DIM_time2UnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[DIM_time2]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Inductance]) -> ConductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Conductance]) -> InductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Resistance]) -> CapacitanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Capacitance]) -> ResistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Time, UnitExpr]:
        return super().__truediv__(rhs)


class TimeUnit(Unit[Time], TimeUnitExpr):
    """
    A :class:`.Unit`[:class:`Time`] and a :class:`TimeUnitExpr`
    """
    ...
        

class Velocity(DerivedDim):
    """
    A :class`.Quantity` representing velocity (:class:`Distance`\ ``/``:class:`Time`)
    """
    derivation = Distance/Time

    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[0]) -> Scalar: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> Velocity: ...
    @overload
    def __pow__(self, _rhs: Literal[2]) -> IonizingRadDose: ...
    @overload
    def __pow__(self, _rhs: int) -> Quantity: ...
    def __pow__(self, rhs: int) -> Quantity:
        return super().__pow__(rhs)

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Velocity: ...
    @overload
    def __mul__(self, _rhs: Union[Force, UnitExpr[Force]]) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Acceleration: ...
    @overload
    def __mul__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> IonizingRadDose: ...
    @overload
    def __mul__(self, _rhs: Union[Area, UnitExpr[Area]]) -> FlowRate: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Distance: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Velocity: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Velocity, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Velocity: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Distance: ...
    @overload
    def __truediv__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Acceleration: ...
    @overload
    def __truediv__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Velocity: ...
    @overload
    def __truediv__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Velocity, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> VelocityUnitExpr:
        return VelocityUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> VelocityUnit:
        return VelocityUnit(abbr, self, singular=singular)
        

class VelocityUnitExpr(UnitExpr[Velocity]):
    """
    A :class:`.UnitExpr`[:class:`Velocity`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Velocity]] = None, 
                singular: Optional[str] = None) -> VelocityUnit:
        return cast(VelocityUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[0]) -> ScalarUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> VelocityUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[2]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __pow__(self, _rhs: int) -> UnitExpr: ...
    def __pow__(self, rhs: int) -> UnitExpr:
        return super().__pow__(rhs)

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Velocity: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Force]) -> PowerUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> AccelerationUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Velocity]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Area]) -> FlowRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> DistanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> VelocityUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Velocity, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Velocity: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> DistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Velocity]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> AccelerationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Distance]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> VelocityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Acceleration]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Velocity, UnitExpr]:
        return super().__truediv__(rhs)


class VelocityUnit(Unit[Velocity], VelocityUnitExpr):
    """
    A :class:`.Unit`[:class:`Velocity`] and a :class:`VelocityUnitExpr`
    """
    ...
        

class Acceleration(DerivedDim):
    """
    A :class`.Quantity` representing acceleration (:class:`Velocity`\ ``/``:class:`Time`)
    """
    derivation = Velocity/Time

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Acceleration: ...
    @overload
    def __mul__(self, _rhs: Union[DIM_dist1_mass1, UnitExpr[DIM_dist1_mass1]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[DIM_time2, UnitExpr[DIM_time2]]) -> Distance: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Velocity: ...
    @overload
    def __mul__(self, _rhs: Union[Mass, UnitExpr[Mass]]) -> Force: ...
    @overload
    def __mul__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> IonizingRadDose: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Acceleration: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Acceleration, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Acceleration: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Velocity: ...
    @overload
    def __truediv__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Acceleration: ...
    @overload
    def __truediv__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Acceleration, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> AccelerationUnitExpr:
        return AccelerationUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> AccelerationUnit:
        return AccelerationUnit(abbr, self, singular=singular)
        

class AccelerationUnitExpr(UnitExpr[Acceleration]):
    """
    A :class:`.UnitExpr`[:class:`Acceleration`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Acceleration]] = None, 
                singular: Optional[str] = None) -> AccelerationUnit:
        return cast(AccelerationUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Acceleration: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[DIM_dist1_mass1]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[DIM_time2]) -> DistanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> VelocityUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Mass]) -> ForceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Distance]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> AccelerationUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Acceleration, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Acceleration: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> VelocityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Velocity]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> AccelerationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Acceleration]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Acceleration, UnitExpr]:
        return super().__truediv__(rhs)


class AccelerationUnit(Unit[Acceleration], AccelerationUnitExpr):
    """
    A :class:`.Unit`[:class:`Acceleration`] and a :class:`AccelerationUnitExpr`
    """
    ...
        

class Force(DerivedDim):
    """
    A :class`.Quantity` representing force (:class:`Mass`\ ``*``:class:`Acceleration`)
    """
    derivation = Mass*Acceleration

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Force: ...
    @overload
    def __mul__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[DIM_time2, UnitExpr[DIM_time2]]) -> DIM_dist1_mass1: ...
    @overload
    def __mul__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Force: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Force, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Force: ...
    @overload
    def __truediv__(self, _rhs: Union[Force, UnitExpr[Force]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Area, UnitExpr[Area]]) -> Pressure: ...
    @overload
    def __truediv__(self, _rhs: Union[Pressure, UnitExpr[Pressure]]) -> Area: ...
    @overload
    def __truediv__(self, _rhs: Union[Mass, UnitExpr[Mass]]) -> Acceleration: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Force: ...
    @overload
    def __truediv__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> Mass: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Force, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> ForceUnitExpr:
        return ForceUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> ForceUnit:
        return ForceUnit(abbr, self, singular=singular)
        

class ForceUnitExpr(UnitExpr[Force]):
    """
    A :class:`.UnitExpr`[:class:`Force`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Force]] = None, 
                singular: Optional[str] = None) -> ForceUnit:
        return cast(ForceUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Force: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Velocity]) -> PowerUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[DIM_time2]) -> DIM_dist1_mass1UnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Distance]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> ForceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Force, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Force: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Force]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Area]) -> PressureUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Pressure]) -> AreaUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Mass]) -> AccelerationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> ForceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Acceleration]) -> MassUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Force, UnitExpr]:
        return super().__truediv__(rhs)


class ForceUnit(Unit[Force], ForceUnitExpr):
    """
    A :class:`.Unit`[:class:`Force`] and a :class:`ForceUnitExpr`
    """
    ...
        

class Work(DerivedDim):
    """
    A :class`.Quantity` representing work (:class:`Force`\ ``*``:class:`Distance`)
    """
    derivation = Force*Distance

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Work, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Work: ...
    @overload
    def __truediv__(self, _rhs: Union[Work, UnitExpr[Work]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Force, UnitExpr[Force]]) -> Distance: ...
    @overload
    def __truediv__(self, _rhs: Union[DIM_dist1_mass1, UnitExpr[DIM_dist1_mass1]]) -> Acceleration: ...
    @overload
    def __truediv__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> Pressure: ...
    @overload
    def __truediv__(self, _rhs: Union[IonizingRadDose, UnitExpr[IonizingRadDose]]) -> Mass: ...
    @overload
    def __truediv__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Flux: ...
    @overload
    def __truediv__(self, _rhs: Union[Charge, UnitExpr[Charge]]) -> Voltage: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Power: ...
    @overload
    def __truediv__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Charge: ...
    @overload
    def __truediv__(self, _rhs: Union[Power, UnitExpr[Power]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Flux, UnitExpr[Flux]]) -> Current: ...
    @overload
    def __truediv__(self, _rhs: Union[Pressure, UnitExpr[Pressure]]) -> Volume: ...
    @overload
    def __truediv__(self, _rhs: Union[Mass, UnitExpr[Mass]]) -> IonizingRadDose: ...
    @overload
    def __truediv__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Force: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Work: ...
    @overload
    def __truediv__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> DIM_dist1_mass1: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Work, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> WorkUnitExpr:
        return WorkUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> WorkUnit:
        return WorkUnit(abbr, self, singular=singular)
        

class WorkUnitExpr(UnitExpr[Work]):
    """
    A :class:`.UnitExpr`[:class:`Work`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Work]] = None, 
                singular: Optional[str] = None) -> WorkUnit:
        return cast(WorkUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Work: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> PowerUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Work, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Work: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Work]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Force]) -> DistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[DIM_dist1_mass1]) -> AccelerationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Volume]) -> PressureUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[IonizingRadDose]) -> MassUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Current]) -> FluxUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Charge]) -> VoltageUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> PowerUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Voltage]) -> ChargeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Power]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Flux]) -> CurrentUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Pressure]) -> VolumeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Mass]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Distance]) -> ForceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> WorkUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Acceleration]) -> DIM_dist1_mass1UnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Work, UnitExpr]:
        return super().__truediv__(rhs)


class WorkUnit(Unit[Work], WorkUnitExpr):
    """
    A :class:`.Unit`[:class:`Work`] and a :class:`WorkUnitExpr`
    """
    ...
        

class Frequency(DerivedDim):
    """
    A :class`.Quantity` representing frequency (``1/``:class:`Time`)

    :class:`Radioactivity` is an alias.
    """
    derivation = Scalar/Time

    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-2]) -> DIM_time2: ...
    @overload
    def __pow__(self, _rhs: Literal[-1]) -> Time: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> Scalar: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> Frequency: ...
    @overload
    def __pow__(self, _rhs: int) -> Quantity: ...
    def __pow__(self, rhs: int) -> Quantity:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Time:
        return cast(Time, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Frequency: ...
    @overload
    def __mul__(self, _rhs: Union[Work, UnitExpr[Work]]) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> Acceleration: ...
    @overload
    def __mul__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> FlowRate: ...
    @overload
    def __mul__(self, _rhs: Union[DIM_time2, UnitExpr[DIM_time2]]) -> Time: ...
    @overload
    def __mul__(self, _rhs: Union[Money, UnitExpr[Money]]) -> PriceRate: ...
    @overload
    def __mul__(self, _rhs: Union[Storage, UnitExpr[Storage]]) -> DataRate: ...
    @overload
    def __mul__(self, _rhs: Union[Temperature, UnitExpr[Temperature]]) -> HeatingRate: ...
    @overload
    def __mul__(self, _rhs: Union[Inductance, UnitExpr[Inductance]]) -> Resistance: ...
    @overload
    def __mul__(self, _rhs: Union[Capacitance, UnitExpr[Capacitance]]) -> Conductance: ...
    @overload
    def __mul__(self, _rhs: Union[Charge, UnitExpr[Charge]]) -> Current: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Scalar: ...
    @overload
    def __mul__(self, _rhs: Union[Flux, UnitExpr[Flux]]) -> Voltage: ...
    @overload
    def __mul__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Velocity: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Frequency: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Frequency, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Frequency, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> FrequencyUnitExpr:
        return FrequencyUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> FrequencyUnit:
        return FrequencyUnit(abbr, self, singular=singular)
        

    @classmethod
    def rate_from(cls, val: Union[Time, Frequency]) -> Frequency:
        return val if isinstance(val, Frequency) else 1/val


Radioactivity = Frequency


class FrequencyUnitExpr(UnitExpr[Frequency]):
    """
    A :class:`.UnitExpr`[:class:`Frequency`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Frequency]] = None, 
                singular: Optional[str] = None) -> FrequencyUnit:
        return cast(FrequencyUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-2]) -> DIM_time2UnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[-1]) -> TimeUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> ScalarUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> FrequencyUnitExpr: ...
    @overload
    def __pow__(self, _rhs: int) -> UnitExpr: ...
    def __pow__(self, rhs: int) -> UnitExpr:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Time:
        return cast(Time, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Frequency: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Work]) -> PowerUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Velocity]) -> AccelerationUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Volume]) -> FlowRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[DIM_time2]) -> TimeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Money]) -> PriceRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Storage]) -> DataRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Temperature]) -> HeatingRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Inductance]) -> ResistanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Capacitance]) -> ConductanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Charge]) -> CurrentUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> ScalarUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Flux]) -> VoltageUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Distance]) -> VelocityUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> FrequencyUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Frequency, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Frequency, UnitExpr]:
        return super().__truediv__(rhs)


class FrequencyUnit(Unit[Frequency], FrequencyUnitExpr):
    """
    A :class:`.Unit`[:class:`Frequency`] and a :class:`FrequencyUnitExpr`
    """
    ...
        

class Volume(DerivedDim):
    """
    A :class`.Quantity` representing volume (:class:`Distance`\ ``**3``)
    """
    derivation = Distance**3

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Volume: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> FlowRate: ...
    @overload
    def __mul__(self, _rhs: Union[MolarConcentration, UnitExpr[MolarConcentration]]) -> Amount: ...
    @overload
    def __mul__(self, _rhs: Union[Density, UnitExpr[Density]]) -> Mass: ...
    @overload
    def __mul__(self, _rhs: Union[VolumeConcentration, UnitExpr[VolumeConcentration]]) -> Volume_of_Substance: ...
    @overload
    def __mul__(self, _rhs: Union[Pressure, UnitExpr[Pressure]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Volume: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Volume, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Volume: ...
    @overload
    def __truediv__(self, _rhs: Union[SpecificVolume, UnitExpr[SpecificVolume]]) -> Mass: ...
    @overload
    def __truediv__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Area, UnitExpr[Area]]) -> Distance: ...
    @overload
    def __truediv__(self, _rhs: Union[FlowRate, UnitExpr[FlowRate]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> FlowRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Mass, UnitExpr[Mass]]) -> SpecificVolume: ...
    @overload
    def __truediv__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Area: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Volume: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Volume, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> VolumeUnitExpr:
        return VolumeUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> VolumeUnit:
        return VolumeUnit(abbr, self, singular=singular)
        

class VolumeUnitExpr(UnitExpr[Volume]):
    """
    A :class:`.UnitExpr`[:class:`Volume`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Volume]] = None, 
                singular: Optional[str] = None) -> VolumeUnit:
        return cast(VolumeUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Volume: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> FlowRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[MolarConcentration]) -> AmountUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Density]) -> MassUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[VolumeConcentration]) -> Volume_of_SubstanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Pressure]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> VolumeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Volume, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Volume: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[SpecificVolume]) -> MassUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Volume]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Area]) -> DistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[FlowRate]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> FlowRateUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Mass]) -> SpecificVolumeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Distance]) -> AreaUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> VolumeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Volume, UnitExpr]:
        return super().__truediv__(rhs)


class VolumeUnit(Unit[Volume], VolumeUnitExpr):
    """
    A :class:`.Unit`[:class:`Volume`] and a :class:`VolumeUnitExpr`
    """
    ...
        

class SpecificVolume(DerivedDim):
    """
    A :class`.Quantity` representing specific volume (:class:`Volume`\ ``/``:class:`Mass`)
    """
    derivation = Volume/Mass

    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> Density: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> Scalar: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> SpecificVolume: ...
    @overload
    def __pow__(self, _rhs: int) -> Quantity: ...
    def __pow__(self, rhs: int) -> Quantity:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Density:
        return cast(Density, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> SpecificVolume: ...
    @overload
    def __mul__(self, _rhs: Union[Density, UnitExpr[Density]]) -> Scalar: ...
    @overload
    def __mul__(self, _rhs: Union[Pressure, UnitExpr[Pressure]]) -> IonizingRadDose: ...
    @overload
    def __mul__(self, _rhs: Union[Mass, UnitExpr[Mass]]) -> Volume: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> SpecificVolume: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[SpecificVolume, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> SpecificVolume: ...
    @overload
    def __truediv__(self, _rhs: Union[SpecificVolume, UnitExpr[SpecificVolume]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> SpecificVolume: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[SpecificVolume, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> SpecificVolumeUnitExpr:
        return SpecificVolumeUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> SpecificVolumeUnit:
        return SpecificVolumeUnit(abbr, self, singular=singular)
        

class SpecificVolumeUnitExpr(UnitExpr[SpecificVolume]):
    """
    A :class:`.UnitExpr`[:class:`SpecificVolume`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[SpecificVolume]] = None, 
                singular: Optional[str] = None) -> SpecificVolumeUnit:
        return cast(SpecificVolumeUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> DensityUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> ScalarUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> SpecificVolumeUnitExpr: ...
    @overload
    def __pow__(self, _rhs: int) -> UnitExpr: ...
    def __pow__(self, rhs: int) -> UnitExpr:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Density:
        return cast(Density, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> SpecificVolume: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Density]) -> ScalarUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Pressure]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Mass]) -> VolumeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> SpecificVolumeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[SpecificVolume, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> SpecificVolume: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[SpecificVolume]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> SpecificVolumeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[SpecificVolume, UnitExpr]:
        return super().__truediv__(rhs)


class SpecificVolumeUnit(Unit[SpecificVolume], SpecificVolumeUnitExpr):
    """
    A :class:`.Unit`[:class:`SpecificVolume`] and a :class:`SpecificVolumeUnitExpr`
    """
    ...
        

class Amount(BaseDim):
    """
    A :class`.Quantity` representing amount
    """
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Amount: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Amount: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Amount, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Amount: ...
    @overload
    def __truediv__(self, _rhs: Union[MolarConcentration, UnitExpr[MolarConcentration]]) -> Volume: ...
    @overload
    def __truediv__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> MolarConcentration: ...
    @overload
    def __truediv__(self, _rhs: Union[Amount, UnitExpr[Amount]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Amount: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Amount, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> AmountUnitExpr:
        return AmountUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> AmountUnit:
        return AmountUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> AmountUnit:
        return cls._base_unit(AmountUnit, abbr, singular=singular)
            

class AmountUnitExpr(UnitExpr[Amount]):
    """
    A :class:`.UnitExpr`[:class:`Amount`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Amount]] = None, 
                singular: Optional[str] = None) -> AmountUnit:
        return cast(AmountUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Amount: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> AmountUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Amount, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Amount: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[MolarConcentration]) -> VolumeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Volume]) -> MolarConcentrationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Amount]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> AmountUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Amount, UnitExpr]:
        return super().__truediv__(rhs)


class AmountUnit(Unit[Amount], AmountUnitExpr):
    """
    A :class:`.Unit`[:class:`Amount`] and a :class:`AmountUnitExpr`
    """
    ...
        

class MolarConcentration(DerivedDim):
    """
    A :class`.Quantity` representing molar concentration (:class:`Amount`\ ``/``:class:`Volume`)

    :class:`Molarity` is an alias.
    """
    derivation = Amount/Volume

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> MolarConcentration: ...
    @overload
    def __mul__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> Amount: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> MolarConcentration: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[MolarConcentration, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> MolarConcentration: ...
    @overload
    def __truediv__(self, _rhs: Union[MolarConcentration, UnitExpr[MolarConcentration]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> MolarConcentration: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[MolarConcentration, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> MolarConcentrationUnitExpr:
        return MolarConcentrationUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> MolarConcentrationUnit:
        return MolarConcentrationUnit(abbr, self, singular=singular)
        
Molarity = MolarConcentration


class MolarConcentrationUnitExpr(UnitExpr[MolarConcentration]):
    """
    A :class:`.UnitExpr`[:class:`MolarConcentration`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[MolarConcentration]] = None, 
                singular: Optional[str] = None) -> MolarConcentrationUnit:
        return cast(MolarConcentrationUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> MolarConcentration: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Volume]) -> AmountUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> MolarConcentrationUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[MolarConcentration, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> MolarConcentration: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[MolarConcentration]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> MolarConcentrationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[MolarConcentration, UnitExpr]:
        return super().__truediv__(rhs)


class MolarConcentrationUnit(Unit[MolarConcentration], MolarConcentrationUnitExpr):
    """
    A :class:`.Unit`[:class:`MolarConcentration`] and a :class:`MolarConcentrationUnitExpr`
    """
    ...
        

class Density(DerivedDim):
    """
    A :class`.Quantity` representing density (:class:`Mass`\ ``/``:class:`Volume`)

    :class:`MassConcentration` is an alias.
    """
    derivation = Mass/Volume

    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> SpecificVolume: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> Scalar: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> Density: ...
    @overload
    def __pow__(self, _rhs: int) -> Quantity: ...
    def __pow__(self, rhs: int) -> Quantity:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> SpecificVolume:
        return cast(SpecificVolume, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Density: ...
    @overload
    def __mul__(self, _rhs: Union[SpecificVolume, UnitExpr[SpecificVolume]]) -> Scalar: ...
    @overload
    def __mul__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> Mass: ...
    @overload
    def __mul__(self, _rhs: Union[IonizingRadDose, UnitExpr[IonizingRadDose]]) -> Pressure: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Density: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Density, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Density: ...
    @overload
    def __truediv__(self, _rhs: Union[Density, UnitExpr[Density]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Density: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Density, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> DensityUnitExpr:
        return DensityUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> DensityUnit:
        return DensityUnit(abbr, self, singular=singular)
        
MassConcentration = Density


class DensityUnitExpr(UnitExpr[Density]):
    """
    A :class:`.UnitExpr`[:class:`Density`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Density]] = None, 
                singular: Optional[str] = None) -> DensityUnit:
        return cast(DensityUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> SpecificVolumeUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> ScalarUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> DensityUnitExpr: ...
    @overload
    def __pow__(self, _rhs: int) -> UnitExpr: ...
    def __pow__(self, rhs: int) -> UnitExpr:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> SpecificVolume:
        return cast(SpecificVolume, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Density: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[SpecificVolume]) -> ScalarUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Volume]) -> MassUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[IonizingRadDose]) -> PressureUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> DensityUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Density, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Density: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Density]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> DensityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Density, UnitExpr]:
        return super().__truediv__(rhs)


class DensityUnit(Unit[Density], DensityUnitExpr):
    """
    A :class:`.Unit`[:class:`Density`] and a :class:`DensityUnitExpr`
    """
    ...
        

class DIM_dist1_mass1(DerivedDim):
    derivation = Distance*Mass

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> DIM_dist1_mass1: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> DIM_dist1_mass1: ...
    @overload
    def __mul__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[DIM_dist1_mass1, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> DIM_dist1_mass1: ...
    @overload
    def __truediv__(self, _rhs: Union[Force, UnitExpr[Force]]) -> DIM_time2: ...
    @overload
    def __truediv__(self, _rhs: Union[DIM_dist1_mass1, UnitExpr[DIM_dist1_mass1]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[DIM_time2, UnitExpr[DIM_time2]]) -> Force: ...
    @overload
    def __truediv__(self, _rhs: Union[Mass, UnitExpr[Mass]]) -> Distance: ...
    @overload
    def __truediv__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Mass: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> DIM_dist1_mass1: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[DIM_dist1_mass1, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> DIM_dist1_mass1UnitExpr:
        return DIM_dist1_mass1UnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> DIM_dist1_mass1Unit:
        return DIM_dist1_mass1Unit(abbr, self, singular=singular)
        

class DIM_dist1_mass1UnitExpr(UnitExpr[DIM_dist1_mass1]):
    """
    A :class:`.UnitExpr`[:class:`DIM_dist1_mass1`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[DIM_dist1_mass1]] = None, 
                singular: Optional[str] = None) -> DIM_dist1_mass1Unit:
        return cast(DIM_dist1_mass1Unit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> DIM_dist1_mass1: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> DIM_dist1_mass1UnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Acceleration]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[DIM_dist1_mass1, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> DIM_dist1_mass1: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Force]) -> DIM_time2UnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[DIM_dist1_mass1]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[DIM_time2]) -> ForceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Mass]) -> DistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Distance]) -> MassUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> DIM_dist1_mass1UnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[DIM_dist1_mass1, UnitExpr]:
        return super().__truediv__(rhs)


class DIM_dist1_mass1Unit(Unit[DIM_dist1_mass1], DIM_dist1_mass1UnitExpr):
    """
    A :class:`.Unit`[:class:`DIM_dist1_mass1`] and a :class:`DIM_dist1_mass1UnitExpr`
    """
    ...
        

class DIM_time2(DerivedDim):
    derivation = Time**2

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> DIM_time2: ...
    @overload
    def __mul__(self, _rhs: Union[Force, UnitExpr[Force]]) -> DIM_dist1_mass1: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Time: ...
    @overload
    def __mul__(self, _rhs: Union[IonizingRadDose, UnitExpr[IonizingRadDose]]) -> Area: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> DIM_time2: ...
    @overload
    def __mul__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> Distance: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[DIM_time2, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> DIM_time2: ...
    @overload
    def __truediv__(self, _rhs: Union[DIM_time2, UnitExpr[DIM_time2]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Inductance, UnitExpr[Inductance]]) -> Capacitance: ...
    @overload
    def __truediv__(self, _rhs: Union[Capacitance, UnitExpr[Capacitance]]) -> Inductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> DIM_time2: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[DIM_time2, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> DIM_time2UnitExpr:
        return DIM_time2UnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> DIM_time2Unit:
        return DIM_time2Unit(abbr, self, singular=singular)
        

class DIM_time2UnitExpr(UnitExpr[DIM_time2]):
    """
    A :class:`.UnitExpr`[:class:`DIM_time2`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[DIM_time2]] = None, 
                singular: Optional[str] = None) -> DIM_time2Unit:
        return cast(DIM_time2Unit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> DIM_time2: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Force]) -> DIM_dist1_mass1UnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> TimeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[IonizingRadDose]) -> AreaUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> DIM_time2UnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Acceleration]) -> DistanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[DIM_time2, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> DIM_time2: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[DIM_time2]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Inductance]) -> CapacitanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Capacitance]) -> InductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> DIM_time2UnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[DIM_time2, UnitExpr]:
        return super().__truediv__(rhs)


class DIM_time2Unit(Unit[DIM_time2], DIM_time2UnitExpr):
    """
    A :class:`.Unit`[:class:`DIM_time2`] and a :class:`DIM_time2UnitExpr`
    """
    ...
        

class Money(BaseDim):
    """
    A :class`.Quantity` representing money

    :class:`Price` is an alias.
    """
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Money: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> PriceRate: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Money: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Money, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Money: ...
    @overload
    def __truediv__(self, _rhs: Union[Money, UnitExpr[Money]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[PriceRate, UnitExpr[PriceRate]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> PriceRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Money: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Money, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> MoneyUnitExpr:
        return MoneyUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> MoneyUnit:
        return MoneyUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> MoneyUnit:
        return cls._base_unit(MoneyUnit, abbr, singular=singular)
            

    class CurrencyFormatter(ABC):
        @abstractmethod
        def format_currency(self, money: Money, *,      # @UnusedVariable
                            force_prefix: bool = False, # @UnusedVariable
                            force_suffix: bool = False, # @UnusedVariable
                            decimal_places: Optional[int] = None # @UnusedVariable
                            ) -> str: ...

    class CurrencyProxy(Protocol):
        # If the currency has an established value wrt the base,
        # force_magnitude() replaces money's magnitude with the scaled value and
        # clears its currency_proxy. Otherwise, it raises an exception
        # indicating that there's no established exchange rate
        def force_magnitude(self, money: Money) -> None: ...   # @UnusedVariable
        # Unless all the currencies match for the units and the money, force all
        # of the magnitudes.
        def unit_check(self, money: Money,                      # @UnusedVariable
                       units:Union[UnitExpr[Money],             # @UnusedVariable
                                   Sequence[UnitExpr[Money]]]) -> None: ...        
        def to_str(self, money: Money) -> str: ...    # @UnusedVariable
        def format_str(self, money: Money, format_spec: str) -> str: ...    # @UnusedVariable
        def as_currency_formatter(self) -> Money.CurrencyFormatter: ...
        
    
    currency_proxy: Optional[CurrencyProxy]
    default_currency_formatter: ClassVar[Optional[Union[CurrencyFormatter, 
                                                        Callable[[Money], str]]]] = None
    

    def __init__(self, mag: float, dim: Optional[Dimensionality[Money]] = None, *,
                 currency_proxy: Optional[CurrencyProxy] = None,
                 _dc: _DirectCreation) -> None:
        self.currency_proxy = currency_proxy
        super().__init__(mag, dim, _dc=_dc)
                
    def __repr__(self) -> str:
        cp = self.currency_proxy
        if cp is None:
            return super().__repr__()
        return f"Quantity({self.magnitude}, {self.dimensionality}, {cp})"
    
    def __str__(self) -> str:
        cp = self.currency_proxy
        if cp is None:
            return super().__str__()
        return cp.to_str(self)
        
    def __format__(self, format_spec: str) -> str:
        cp = self.currency_proxy
        if cp is None:
            return super().__format__(format_spec)
        return cp.format_str(self, format_spec)
        
    def same_dim(self, magnitude: float)-> Money:
        return Money.dim().make_quantity(magnitude, currency_proxy=self.currency_proxy)
    
    def _force_magnitude(self) -> None:
        cp = self.currency_proxy
        if cp is not None:
            cp.force_magnitude(self)
    
    def _ensure_dim_match(self, rhs: Quantity, op: str) -> None:
        if not isinstance(rhs, Money):
            return super()._ensure_dim_match(rhs, op)
        if self.currency_proxy is not rhs.currency_proxy:
            # One or both is not None, so we have to force them to the base.  If
            # we can, they will both be None, otherwise, an exception will be
            # raised.
            self._force_magnitude()
            rhs._force_magnitude()
            
    def ratio(self: Money, base: Money) -> float:
        self._ensure_dim_match(base, "/")
        return self.magnitude / base.magnitude

    def multiply_by(self, rhs: Quantity) -> Quantity:
        if isinstance(rhs, Scalar):
            return self.same_dim(rhs.magnitude)
        self._force_magnitude()
        return super().multiply_by(rhs)

    def divide_by(self, rhs: Quantity) -> Quantity:
        if isinstance(rhs, Scalar):
            return self.same_dim(rhs.magnitude)
        if isinstance(rhs, Money):
            # This will call _ensure_dim_match() to force the magnitude if they
            # don't already match.
            return Scalar.from_float(self.magnitude/rhs.magnitude)
        # If it's not a money ratio, we can only do this if the magnitude can be
        # forced (if it isn't already).
        self._force_magnitude()
        return super().divide_by(rhs)
    
    def in_denom(self, lhs:float) -> Quantity:
        self._force_magnitude()
        return super().in_denom(lhs)
    
    def to_power(self, rhs: int) -> Quantity:
        # if the power is 0 or 1, we're fine.  Otherwise, we can only do this if
        # the magnitude can be forced.
        if rhs != 0 and rhs != 1:
            self._force_magnitude()
        return super().to_power(rhs)
    
    def _force_if_necessary(self, units: Union[UnitExpr[Money], Sequence[UnitExpr[Money]]]) -> None:
        cp = self.currency_proxy
        if cp is not None:
            cp.unit_check(self, units)
        # We've been forced, so we need to make sure that all of the units are as well.
        elif isinstance(units, UnitExpr):
            units.quantity._force_magnitude()
        else:
            for u in units:
                u.quantity._force_magnitude()

    def in_units(self, units:Union[UnitExpr[Money], Sequence[UnitExpr[Money]]])->_BoundQuantity[Money]:
        self._force_if_necessary(units)
        return super().in_units(units)
    
    def decomposed(self, units: Iterable[UnitExpr[Money]], *, 
                   required: Optional[Union[Iterable[UnitExpr[Money]],
                                            Literal["all"]]] = None) -> _DecomposedQuantity[Money]:
        units = list(units)
        if required is not None and required != "all":
            required = list(required)
            self._force_if_necessary((*units, *required))
        else: 
            self._force_if_necessary(units)
        return super().decomposed(units, required=required)
        
    def of(self, restriction:T, *, dim: Optional[str] = None)-> BaseDim: # @UnusedVariable
        # We can only do this if forced.
        self._force_magnitude()
        return super().of(restriction)

    def as_currency(self,                     
                    formatter: Optional[Union[Money.CurrencyFormatter,
                                              Callable[[Money], str]]] = None,
                    *,
                    force_prefix: bool = False,
                    force_suffix: bool = False,
                    decimal_places: Optional[int] = None) -> str:
        if formatter is None:
            formatter = Money.default_currency_formatter
        if formatter is None: 
            assert self.currency_proxy is not None, f"No default currency formatter and no currency proxy: {self}"
            formatter = self.currency_proxy.as_currency_formatter()
        if isinstance(formatter, Money.CurrencyFormatter):
            return formatter.format_currency(self, force_prefix=force_prefix,
                                             force_suffix=force_suffix, 
                                             decimal_places=decimal_places)
        else:
            return formatter(self)

Price = Money


class MoneyUnitExpr(UnitExpr[Money]):
    """
    A :class:`.UnitExpr`[:class:`Money`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Money]] = None, 
                singular: Optional[str] = None) -> MoneyUnit:
        return cast(MoneyUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Money: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> PriceRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> MoneyUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Money, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Money: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Money]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[PriceRate]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> PriceRateUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> MoneyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Money, UnitExpr]:
        return super().__truediv__(rhs)


class MoneyUnit(Unit[Money], MoneyUnitExpr):
    """
    A :class:`.Unit`[:class:`Money`] and a :class:`MoneyUnitExpr`
    """
    ...
        

class Volume_of_Substance(BaseDim):
    """
    A :class`.Quantity` representing :class:`Volume`[:class:`Substance`]
    """
    _dim_name = "Volume[Substance]"

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Volume_of_Substance: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Volume_of_Substance: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Volume_of_Substance, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Volume_of_Substance: ...
    @overload
    def __truediv__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> VolumeConcentration: ...
    @overload
    def __truediv__(self, _rhs: Union[VolumeConcentration, UnitExpr[VolumeConcentration]]) -> Volume: ...
    @overload
    def __truediv__(self, _rhs: Union[Volume_of_Substance, UnitExpr[Volume_of_Substance]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Volume_of_Substance: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Volume_of_Substance, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> Volume_of_SubstanceUnitExpr:
        return Volume_of_SubstanceUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> Volume_of_SubstanceUnit:
        return Volume_of_SubstanceUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> Volume_of_SubstanceUnit:
        return cls._base_unit(Volume_of_SubstanceUnit, abbr, singular=singular)
            
Volume.note_restriction(Substance, Volume_of_Substance)

class Volume_of_SubstanceUnitExpr(UnitExpr[Volume_of_Substance]):
    """
    A :class:`.UnitExpr`[:class:`Volume_of_Substance`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Volume_of_Substance]] = None, 
                singular: Optional[str] = None) -> Volume_of_SubstanceUnit:
        return cast(Volume_of_SubstanceUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Volume_of_Substance: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> Volume_of_SubstanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Volume_of_Substance, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Volume_of_Substance: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Volume]) -> VolumeConcentrationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[VolumeConcentration]) -> VolumeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Volume_of_Substance]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> Volume_of_SubstanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Volume_of_Substance, UnitExpr]:
        return super().__truediv__(rhs)


class Volume_of_SubstanceUnit(Unit[Volume_of_Substance], Volume_of_SubstanceUnitExpr):
    """
    A :class:`.Unit`[:class:`Volume_of_Substance`] and a :class:`Volume_of_SubstanceUnitExpr`
    """
    ...
        

class VolumeConcentration(DerivedDim):
    """
    A :class`.Quantity` representing volume concentration (:class:`Volume_of_Substance`\ ``/``:class:`Volume`)
    """
    derivation = Volume_of_Substance/Volume

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> VolumeConcentration: ...
    @overload
    def __mul__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> Volume_of_Substance: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> VolumeConcentration: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[VolumeConcentration, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> VolumeConcentration: ...
    @overload
    def __truediv__(self, _rhs: Union[VolumeConcentration, UnitExpr[VolumeConcentration]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> VolumeConcentration: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[VolumeConcentration, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> VolumeConcentrationUnitExpr:
        return VolumeConcentrationUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> VolumeConcentrationUnit:
        return VolumeConcentrationUnit(abbr, self, singular=singular)
        

class VolumeConcentrationUnitExpr(UnitExpr[VolumeConcentration]):
    """
    A :class:`.UnitExpr`[:class:`VolumeConcentration`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[VolumeConcentration]] = None, 
                singular: Optional[str] = None) -> VolumeConcentrationUnit:
        return cast(VolumeConcentrationUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> VolumeConcentration: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Volume]) -> Volume_of_SubstanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> VolumeConcentrationUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[VolumeConcentration, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> VolumeConcentration: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[VolumeConcentration]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> VolumeConcentrationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[VolumeConcentration, UnitExpr]:
        return super().__truediv__(rhs)


class VolumeConcentrationUnit(Unit[VolumeConcentration], VolumeConcentrationUnitExpr):
    """
    A :class:`.Unit`[:class:`VolumeConcentration`] and a :class:`VolumeConcentrationUnitExpr`
    """
    ...
        

class Area(DerivedDim):
    """
    A :class`.Quantity` representing area (:class:`Distance`\ ``**2``)
    """
    derivation = Distance**2

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Area: ...
    @overload
    def __mul__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> FlowRate: ...
    @overload
    def __mul__(self, _rhs: Union[FluxDensity, UnitExpr[FluxDensity]]) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Illuminance, UnitExpr[Illuminance]]) -> LumInt: ...
    @overload
    def __mul__(self, _rhs: Union[Pressure, UnitExpr[Pressure]]) -> Force: ...
    @overload
    def __mul__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Volume: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Area: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Area, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Area: ...
    @overload
    def __truediv__(self, _rhs: Union[DIM_time2, UnitExpr[DIM_time2]]) -> IonizingRadDose: ...
    @overload
    def __truediv__(self, _rhs: Union[Area, UnitExpr[Area]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[IonizingRadDose, UnitExpr[IonizingRadDose]]) -> DIM_time2: ...
    @overload
    def __truediv__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Distance: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Area: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Area, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> AreaUnitExpr:
        return AreaUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> AreaUnit:
        return AreaUnit(abbr, self, singular=singular)
        

class AreaUnitExpr(UnitExpr[Area]):
    """
    A :class:`.UnitExpr`[:class:`Area`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Area]] = None, 
                singular: Optional[str] = None) -> AreaUnit:
        return cast(AreaUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Area: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Velocity]) -> FlowRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[FluxDensity]) -> FluxUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Illuminance]) -> LumIntUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Pressure]) -> ForceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Distance]) -> VolumeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> AreaUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Area, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Area: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[DIM_time2]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Area]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[IonizingRadDose]) -> DIM_time2UnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Distance]) -> DistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> AreaUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Area, UnitExpr]:
        return super().__truediv__(rhs)


class AreaUnit(Unit[Area], AreaUnitExpr):
    """
    A :class:`.Unit`[:class:`Area`] and a :class:`AreaUnitExpr`
    """
    ...
        

class PriceRate(DerivedDim):
    """
    A :class`.Quantity` representing price rate (:class:`Money`\ ``/``:class:`Time`)

    :class:`Salary` is an alias.
    """
    derivation = Money/Time

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> PriceRate: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Money: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> PriceRate: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[PriceRate, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> PriceRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Money: ...
    @overload
    def __truediv__(self, _rhs: Union[Money, UnitExpr[Money]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[PriceRate, UnitExpr[PriceRate]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> PriceRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[PriceRate, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> PriceRateUnitExpr:
        return PriceRateUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> PriceRateUnit:
        return PriceRateUnit(abbr, self, singular=singular)
        
Salary = PriceRate


class PriceRateUnitExpr(UnitExpr[PriceRate]):
    """
    A :class:`.UnitExpr`[:class:`PriceRate`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[PriceRate]] = None, 
                singular: Optional[str] = None) -> PriceRateUnit:
        return cast(PriceRateUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> PriceRate: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> MoneyUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> PriceRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[PriceRate, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> PriceRate: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> MoneyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Money]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[PriceRate]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> PriceRateUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[PriceRate, UnitExpr]:
        return super().__truediv__(rhs)


class PriceRateUnit(Unit[PriceRate], PriceRateUnitExpr):
    """
    A :class:`.Unit`[:class:`PriceRate`] and a :class:`PriceRateUnitExpr`
    """
    ...
        

class Temperature(BaseDim):
    """
    A :class`.Quantity` representing temperature
    """
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Temperature: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> HeatingRate: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Temperature: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Temperature, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Temperature: ...
    @overload
    def __truediv__(self, _rhs: Union[HeatingRate, UnitExpr[HeatingRate]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Temperature, UnitExpr[Temperature]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> HeatingRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Temperature: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Temperature, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> TemperatureUnitExpr:
        return TemperatureUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> TemperatureUnit:
        return TemperatureUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> TemperatureUnit:
        return cls._base_unit(TemperatureUnit, abbr, singular=singular)
            

class TemperatureUnitExpr(UnitExpr[Temperature]):
    """
    A :class:`.UnitExpr`[:class:`Temperature`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Temperature]] = None, 
                singular: Optional[str] = None) -> TemperatureUnit:
        return cast(TemperatureUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Temperature: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> HeatingRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> TemperatureUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Temperature, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Temperature: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[HeatingRate]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Temperature]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> HeatingRateUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> TemperatureUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Temperature, UnitExpr]:
        return super().__truediv__(rhs)


class TemperatureUnit(Unit[Temperature], TemperatureUnitExpr):
    """
    A :class:`.Unit`[:class:`Temperature`] and a :class:`TemperatureUnitExpr`
    """
    ...
        

class HeatingRate(DerivedDim):
    """
    A :class`.Quantity` representing heating rate (:class:`Temperature`\ ``/``:class:`Time`)
    """
    derivation = Temperature/Time

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> HeatingRate: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Temperature: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> HeatingRate: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[HeatingRate, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> HeatingRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Temperature: ...
    @overload
    def __truediv__(self, _rhs: Union[HeatingRate, UnitExpr[HeatingRate]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Temperature, UnitExpr[Temperature]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> HeatingRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[HeatingRate, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> HeatingRateUnitExpr:
        return HeatingRateUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> HeatingRateUnit:
        return HeatingRateUnit(abbr, self, singular=singular)
        

class HeatingRateUnitExpr(UnitExpr[HeatingRate]):
    """
    A :class:`.UnitExpr`[:class:`HeatingRate`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[HeatingRate]] = None, 
                singular: Optional[str] = None) -> HeatingRateUnit:
        return cast(HeatingRateUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> HeatingRate: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> TemperatureUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> HeatingRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[HeatingRate, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> HeatingRate: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> TemperatureUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[HeatingRate]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Temperature]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> HeatingRateUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[HeatingRate, UnitExpr]:
        return super().__truediv__(rhs)


class HeatingRateUnit(Unit[HeatingRate], HeatingRateUnitExpr):
    """
    A :class:`.Unit`[:class:`HeatingRate`] and a :class:`HeatingRateUnitExpr`
    """
    ...
        

class FlowRate(DerivedDim):
    """
    A :class`.Quantity` representing flow rate (:class:`Volume`\ ``/``:class:`Time`)
    """
    derivation = Volume/Time

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> FlowRate: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Volume: ...
    @overload
    def __mul__(self, _rhs: Union[Pressure, UnitExpr[Pressure]]) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> FlowRate: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[FlowRate, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> FlowRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Volume: ...
    @overload
    def __truediv__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> Area: ...
    @overload
    def __truediv__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Area, UnitExpr[Area]]) -> Velocity: ...
    @overload
    def __truediv__(self, _rhs: Union[FlowRate, UnitExpr[FlowRate]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> FlowRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[FlowRate, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> FlowRateUnitExpr:
        return FlowRateUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> FlowRateUnit:
        return FlowRateUnit(abbr, self, singular=singular)
        

class FlowRateUnitExpr(UnitExpr[FlowRate]):
    """
    A :class:`.UnitExpr`[:class:`FlowRate`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[FlowRate]] = None, 
                singular: Optional[str] = None) -> FlowRateUnit:
        return cast(FlowRateUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> FlowRate: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> VolumeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Pressure]) -> PowerUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> FlowRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[FlowRate, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> FlowRate: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> VolumeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Velocity]) -> AreaUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Volume]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Area]) -> VelocityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[FlowRate]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> FlowRateUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[FlowRate, UnitExpr]:
        return super().__truediv__(rhs)


class FlowRateUnit(Unit[FlowRate], FlowRateUnitExpr):
    """
    A :class:`.Unit`[:class:`FlowRate`] and a :class:`FlowRateUnitExpr`
    """
    ...
        

class Storage(BaseDim):
    """
    A :class`.Quantity` representing storage
    """
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Storage: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> DataRate: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Storage: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Storage, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Storage: ...
    @overload
    def __truediv__(self, _rhs: Union[Storage, UnitExpr[Storage]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[DataRate, UnitExpr[DataRate]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> DataRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Storage: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Storage, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> StorageUnitExpr:
        return StorageUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> StorageUnit:
        return StorageUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> StorageUnit:
        return cls._base_unit(StorageUnit, abbr, singular=singular)
            

class StorageUnitExpr(UnitExpr[Storage]):
    """
    A :class:`.UnitExpr`[:class:`Storage`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Storage]] = None, 
                singular: Optional[str] = None) -> StorageUnit:
        return cast(StorageUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Storage: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> DataRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> StorageUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Storage, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Storage: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Storage]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[DataRate]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> DataRateUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> StorageUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Storage, UnitExpr]:
        return super().__truediv__(rhs)


class StorageUnit(Unit[Storage], StorageUnitExpr):
    """
    A :class:`.Unit`[:class:`Storage`] and a :class:`StorageUnitExpr`
    """
    ...
        

class DataRate(DerivedDim):
    """
    A :class`.Quantity` representing data rate (:class:`Storage`\ ``/``:class:`Time`)
    """
    derivation = Storage/Time

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> DataRate: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Storage: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> DataRate: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[DataRate, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> DataRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Storage: ...
    @overload
    def __truediv__(self, _rhs: Union[Storage, UnitExpr[Storage]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[DataRate, UnitExpr[DataRate]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> DataRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[DataRate, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> DataRateUnitExpr:
        return DataRateUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> DataRateUnit:
        return DataRateUnit(abbr, self, singular=singular)
        

class DataRateUnitExpr(UnitExpr[DataRate]):
    """
    A :class:`.UnitExpr`[:class:`DataRate`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[DataRate]] = None, 
                singular: Optional[str] = None) -> DataRateUnit:
        return cast(DataRateUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> DataRate: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> StorageUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> DataRateUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[DataRate, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> DataRate: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> StorageUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Storage]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[DataRate]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> DataRateUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[DataRate, UnitExpr]:
        return super().__truediv__(rhs)


class DataRateUnit(Unit[DataRate], DataRateUnitExpr):
    """
    A :class:`.Unit`[:class:`DataRate`] and a :class:`DataRateUnitExpr`
    """
    ...
        

class IonizingRadDose(DerivedDim):
    """
    A :class`.Quantity` representing ionizing radiation dose (:class:`Work`\ ``/``:class:`Mass`)
    """
    derivation = Work/Mass

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> IonizingRadDose: ...
    @overload
    def __mul__(self, _rhs: Union[Density, UnitExpr[Density]]) -> Pressure: ...
    @overload
    def __mul__(self, _rhs: Union[DIM_time2, UnitExpr[DIM_time2]]) -> Area: ...
    @overload
    def __mul__(self, _rhs: Union[Mass, UnitExpr[Mass]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> IonizingRadDose: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[IonizingRadDose, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> IonizingRadDose: ...
    @overload
    def __truediv__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> Velocity: ...
    @overload
    def __truediv__(self, _rhs: Union[SpecificVolume, UnitExpr[SpecificVolume]]) -> Pressure: ...
    @overload
    def __truediv__(self, _rhs: Union[IonizingRadDose, UnitExpr[IonizingRadDose]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Pressure, UnitExpr[Pressure]]) -> SpecificVolume: ...
    @overload
    def __truediv__(self, _rhs: Union[Distance, UnitExpr[Distance]]) -> Acceleration: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> IonizingRadDose: ...
    @overload
    def __truediv__(self, _rhs: Union[Acceleration, UnitExpr[Acceleration]]) -> Distance: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[IonizingRadDose, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> IonizingRadDoseUnitExpr:
        return IonizingRadDoseUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> IonizingRadDoseUnit:
        return IonizingRadDoseUnit(abbr, self, singular=singular)
        

class IonizingRadDoseUnitExpr(UnitExpr[IonizingRadDose]):
    """
    A :class:`.UnitExpr`[:class:`IonizingRadDose`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[IonizingRadDose]] = None, 
                singular: Optional[str] = None) -> IonizingRadDoseUnit:
        return cast(IonizingRadDoseUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> IonizingRadDose: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Density]) -> PressureUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[DIM_time2]) -> AreaUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Mass]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[IonizingRadDose, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> IonizingRadDose: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Velocity]) -> VelocityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[SpecificVolume]) -> PressureUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[IonizingRadDose]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Pressure]) -> SpecificVolumeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Distance]) -> AccelerationUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Acceleration]) -> DistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[IonizingRadDose, UnitExpr]:
        return super().__truediv__(rhs)


class IonizingRadDoseUnit(Unit[IonizingRadDose], IonizingRadDoseUnitExpr):
    """
    A :class:`.Unit`[:class:`IonizingRadDose`] and a :class:`IonizingRadDoseUnitExpr`
    """
    ...
        

class LumInt(BaseDim):
    """
    A :class`.Quantity` representing luminous intensity

    :class:`LumFlux` is an alias.
    """
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> LumInt: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> LumInt: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[LumInt, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> LumInt: ...
    @overload
    def __truediv__(self, _rhs: Union[Area, UnitExpr[Area]]) -> Illuminance: ...
    @overload
    def __truediv__(self, _rhs: Union[LumInt, UnitExpr[LumInt]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Illuminance, UnitExpr[Illuminance]]) -> Area: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> LumInt: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[LumInt, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> LumIntUnitExpr:
        return LumIntUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> LumIntUnit:
        return LumIntUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> LumIntUnit:
        return cls._base_unit(LumIntUnit, abbr, singular=singular)
            
LumFlux = LumInt


class LumIntUnitExpr(UnitExpr[LumInt]):
    """
    A :class:`.UnitExpr`[:class:`LumInt`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[LumInt]] = None, 
                singular: Optional[str] = None) -> LumIntUnit:
        return cast(LumIntUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> LumInt: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> LumIntUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[LumInt, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> LumInt: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Area]) -> IlluminanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[LumInt]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Illuminance]) -> AreaUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> LumIntUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[LumInt, UnitExpr]:
        return super().__truediv__(rhs)


class LumIntUnit(Unit[LumInt], LumIntUnitExpr):
    """
    A :class:`.Unit`[:class:`LumInt`] and a :class:`LumIntUnitExpr`
    """
    ...
        

class Current(BaseDim):
    """
    A :class`.Quantity` representing current
    """
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Current: ...
    @overload
    def __mul__(self, _rhs: Union[Inductance, UnitExpr[Inductance]]) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Voltage: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Charge: ...
    @overload
    def __mul__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[Flux, UnitExpr[Flux]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Current: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Current, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Current: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Charge: ...
    @overload
    def __truediv__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Voltage: ...
    @overload
    def __truediv__(self, _rhs: Union[Charge, UnitExpr[Charge]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Conductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Current: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Current, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> CurrentUnitExpr:
        return CurrentUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> CurrentUnit:
        return CurrentUnit(abbr, self, singular=singular)
        

    @classmethod
    def base_unit(cls, abbr: str, *, singular: Optional[str] = None) -> CurrentUnit:
        return cls._base_unit(CurrentUnit, abbr, singular=singular)
            

class CurrentUnitExpr(UnitExpr[Current]):
    """
    A :class:`.UnitExpr`[:class:`Current`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Current]] = None, 
                singular: Optional[str] = None) -> CurrentUnit:
        return cast(CurrentUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Current: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Inductance]) -> FluxUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Resistance]) -> VoltageUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> ChargeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Voltage]) -> PowerUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Flux]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> CurrentUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Current, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Current: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> ChargeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Current]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Conductance]) -> VoltageUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Charge]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Voltage]) -> ConductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> CurrentUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Current, UnitExpr]:
        return super().__truediv__(rhs)


class CurrentUnit(Unit[Current], CurrentUnitExpr):
    """
    A :class:`.Unit`[:class:`Current`] and a :class:`CurrentUnitExpr`
    """
    ...
        

class Charge(DerivedDim):
    """
    A :class`.Quantity` representing charge (:class:`Current`\ ``*``:class:`Time`)
    """
    derivation = Current*Time

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Charge: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Current: ...
    @overload
    def __mul__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Charge: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Charge, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Charge: ...
    @overload
    def __truediv__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Flux: ...
    @overload
    def __truediv__(self, _rhs: Union[Capacitance, UnitExpr[Capacitance]]) -> Voltage: ...
    @overload
    def __truediv__(self, _rhs: Union[Charge, UnitExpr[Charge]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Current: ...
    @overload
    def __truediv__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Capacitance: ...
    @overload
    def __truediv__(self, _rhs: Union[Flux, UnitExpr[Flux]]) -> Conductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Charge: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Charge, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> ChargeUnitExpr:
        return ChargeUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> ChargeUnit:
        return ChargeUnit(abbr, self, singular=singular)
        

class ChargeUnitExpr(UnitExpr[Charge]):
    """
    A :class:`.UnitExpr`[:class:`Charge`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Charge]] = None, 
                singular: Optional[str] = None) -> ChargeUnit:
        return cast(ChargeUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Charge: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> CurrentUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Resistance]) -> FluxUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Voltage]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> ChargeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Charge, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Charge: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Current]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Conductance]) -> FluxUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Capacitance]) -> VoltageUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Charge]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> CurrentUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Voltage]) -> CapacitanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Flux]) -> ConductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> ChargeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Charge, UnitExpr]:
        return super().__truediv__(rhs)


class ChargeUnit(Unit[Charge], ChargeUnitExpr):
    """
    A :class:`.Unit`[:class:`Charge`] and a :class:`ChargeUnitExpr`
    """
    ...
        

class Voltage(DerivedDim):
    """
    A :class`.Quantity` representing voltage (:class:`Work`\ ``/``:class:`Charge`)

    :class:`Emf`, :class:`EMF`, and :class:`ElecPotential` are aliases.
    """
    derivation = Work/Charge

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Voltage: ...
    @overload
    def __mul__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Current: ...
    @overload
    def __mul__(self, _rhs: Union[Capacitance, UnitExpr[Capacitance]]) -> Charge: ...
    @overload
    def __mul__(self, _rhs: Union[Charge, UnitExpr[Charge]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Voltage: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Voltage, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Voltage: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Flux: ...
    @overload
    def __truediv__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Resistance: ...
    @overload
    def __truediv__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Current: ...
    @overload
    def __truediv__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Flux, UnitExpr[Flux]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Voltage: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Voltage, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> VoltageUnitExpr:
        return VoltageUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> VoltageUnit:
        return VoltageUnit(abbr, self, singular=singular)
        
Emf = Voltage
EMF = Voltage
ElecPotential = Voltage


class VoltageUnitExpr(UnitExpr[Voltage]):
    """
    A :class:`.UnitExpr`[:class:`Voltage`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Voltage]] = None, 
                singular: Optional[str] = None) -> VoltageUnit:
        return cast(VoltageUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Voltage: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Current]) -> PowerUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Conductance]) -> CurrentUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Capacitance]) -> ChargeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Charge]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> FluxUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> VoltageUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Voltage, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Voltage: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> FluxUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Current]) -> ResistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Resistance]) -> CurrentUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Voltage]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Flux]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> VoltageUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Voltage, UnitExpr]:
        return super().__truediv__(rhs)


class VoltageUnit(Unit[Voltage], VoltageUnitExpr):
    """
    A :class:`.Unit`[:class:`Voltage`] and a :class:`VoltageUnitExpr`
    """
    ...
        

class Resistance(DerivedDim):
    """
    A :class`.Quantity` representing resistance (:class:`Voltage`\ ``/``:class:`Current`)
    """
    derivation = Voltage/Current

    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> Conductance: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> Scalar: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> Resistance: ...
    @overload
    def __pow__(self, _rhs: int) -> Quantity: ...
    def __pow__(self, rhs: int) -> Quantity:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Conductance:
        return cast(Conductance, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Resistance: ...
    @overload
    def __mul__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Voltage: ...
    @overload
    def __mul__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Scalar: ...
    @overload
    def __mul__(self, _rhs: Union[Capacitance, UnitExpr[Capacitance]]) -> Time: ...
    @overload
    def __mul__(self, _rhs: Union[Charge, UnitExpr[Charge]]) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Inductance: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Resistance: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Resistance, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Resistance: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Inductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Inductance, UnitExpr[Inductance]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Resistance: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Resistance, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> ResistanceUnitExpr:
        return ResistanceUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> ResistanceUnit:
        return ResistanceUnit(abbr, self, singular=singular)
        

class ResistanceUnitExpr(UnitExpr[Resistance]):
    """
    A :class:`.UnitExpr`[:class:`Resistance`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Resistance]] = None, 
                singular: Optional[str] = None) -> ResistanceUnit:
        return cast(ResistanceUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> ConductanceUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> ScalarUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> ResistanceUnitExpr: ...
    @overload
    def __pow__(self, _rhs: int) -> UnitExpr: ...
    def __pow__(self, rhs: int) -> UnitExpr:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Conductance:
        return cast(Conductance, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Resistance: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Current]) -> VoltageUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Conductance]) -> ScalarUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Capacitance]) -> TimeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Charge]) -> FluxUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> InductanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> ResistanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Resistance, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Resistance: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> InductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Inductance]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Resistance]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> ResistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Resistance, UnitExpr]:
        return super().__truediv__(rhs)


class ResistanceUnit(Unit[Resistance], ResistanceUnitExpr):
    """
    A :class:`.Unit`[:class:`Resistance`] and a :class:`ResistanceUnitExpr`
    """
    ...
        

class Inductance(DerivedDim):
    """
    A :class`.Quantity` representing inductance (:class:`Resistance`\ ``*``:class:`Time`)
    """
    derivation = Resistance*Time

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Inductance: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Resistance: ...
    @overload
    def __mul__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Time: ...
    @overload
    def __mul__(self, _rhs: Union[Capacitance, UnitExpr[Capacitance]]) -> DIM_time2: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Inductance: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Inductance, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Inductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Inductance, UnitExpr[Inductance]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Resistance: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Inductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Inductance, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> InductanceUnitExpr:
        return InductanceUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> InductanceUnit:
        return InductanceUnit(abbr, self, singular=singular)
        

class InductanceUnitExpr(UnitExpr[Inductance]):
    """
    A :class:`.UnitExpr`[:class:`Inductance`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Inductance]] = None, 
                singular: Optional[str] = None) -> InductanceUnit:
        return cast(InductanceUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Inductance: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> ResistanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Current]) -> FluxUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Conductance]) -> TimeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Capacitance]) -> DIM_time2UnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> InductanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Inductance, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Inductance: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Inductance]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Resistance]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> ResistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> InductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Inductance, UnitExpr]:
        return super().__truediv__(rhs)


class InductanceUnit(Unit[Inductance], InductanceUnitExpr):
    """
    A :class:`.Unit`[:class:`Inductance`] and a :class:`InductanceUnitExpr`
    """
    ...
        

class Conductance(DerivedDim):
    """
    A :class`.Quantity` representing conductance (:class:`Current`\ ``/``:class:`Voltage`)
    """
    derivation = Current/Voltage

    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> Resistance: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> Scalar: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> Conductance: ...
    @overload
    def __pow__(self, _rhs: int) -> Quantity: ...
    def __pow__(self, rhs: int) -> Quantity:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Resistance:
        return cast(Resistance, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Conductance: ...
    @overload
    def __mul__(self, _rhs: Union[Inductance, UnitExpr[Inductance]]) -> Time: ...
    @overload
    def __mul__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Scalar: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Capacitance: ...
    @overload
    def __mul__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Current: ...
    @overload
    def __mul__(self, _rhs: Union[Flux, UnitExpr[Flux]]) -> Charge: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Conductance: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Conductance, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Conductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Capacitance: ...
    @overload
    def __truediv__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Capacitance, UnitExpr[Capacitance]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Conductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Conductance, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> ConductanceUnitExpr:
        return ConductanceUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> ConductanceUnit:
        return ConductanceUnit(abbr, self, singular=singular)
        

class ConductanceUnitExpr(UnitExpr[Conductance]):
    """
    A :class:`.UnitExpr`[:class:`Conductance`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Conductance]] = None, 
                singular: Optional[str] = None) -> ConductanceUnit:
        return cast(ConductanceUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __pow__(self, _rhs: Literal[-1]) -> ResistanceUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[0]) -> ScalarUnitExpr: ...
    @overload
    def __pow__(self, _rhs: Literal[1]) -> ConductanceUnitExpr: ...
    @overload
    def __pow__(self, _rhs: int) -> UnitExpr: ...
    def __pow__(self, rhs: int) -> UnitExpr:
        return super().__pow__(rhs)


    def __rtruediv__(self, n: float) -> Resistance:
        return cast(Resistance, super().__rtruediv__(n))
                
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Conductance: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Inductance]) -> TimeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Resistance]) -> ScalarUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> CapacitanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Voltage]) -> CurrentUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Flux]) -> ChargeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> ConductanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Conductance, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Conductance: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> CapacitanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Conductance]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Capacitance]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> ConductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Conductance, UnitExpr]:
        return super().__truediv__(rhs)


class ConductanceUnit(Unit[Conductance], ConductanceUnitExpr):
    """
    A :class:`.Unit`[:class:`Conductance`] and a :class:`ConductanceUnitExpr`
    """
    ...
        

class Capacitance(DerivedDim):
    """
    A :class`.Quantity` representing capacitance (:class:`Charge`\ ``/``:class:`Voltage`)
    """
    derivation = Charge/Voltage

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Capacitance: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Conductance: ...
    @overload
    def __mul__(self, _rhs: Union[Inductance, UnitExpr[Inductance]]) -> DIM_time2: ...
    @overload
    def __mul__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Time: ...
    @overload
    def __mul__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Charge: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Capacitance: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Capacitance, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Capacitance: ...
    @overload
    def __truediv__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Capacitance, UnitExpr[Capacitance]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Conductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Capacitance: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Capacitance, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> CapacitanceUnitExpr:
        return CapacitanceUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> CapacitanceUnit:
        return CapacitanceUnit(abbr, self, singular=singular)
        

class CapacitanceUnitExpr(UnitExpr[Capacitance]):
    """
    A :class:`.UnitExpr`[:class:`Capacitance`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Capacitance]] = None, 
                singular: Optional[str] = None) -> CapacitanceUnit:
        return cast(CapacitanceUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Capacitance: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> ConductanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Inductance]) -> DIM_time2UnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Resistance]) -> TimeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Voltage]) -> ChargeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> CapacitanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Capacitance, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Capacitance: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Conductance]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Capacitance]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> ConductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> CapacitanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Capacitance, UnitExpr]:
        return super().__truediv__(rhs)


class CapacitanceUnit(Unit[Capacitance], CapacitanceUnitExpr):
    """
    A :class:`.Unit`[:class:`Capacitance`] and a :class:`CapacitanceUnitExpr`
    """
    ...
        

class Flux(DerivedDim):
    """
    A :class`.Quantity` representing flux (:class:`Voltage`\ ``*``:class:`Time`)

    :class:`MagneticFlux` is an alias.
    """
    derivation = Voltage*Time

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Voltage: ...
    @overload
    def __mul__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Conductance, UnitExpr[Conductance]]) -> Charge: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Flux, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Flux: ...
    @overload
    def __truediv__(self, _rhs: Union[Area, UnitExpr[Area]]) -> FluxDensity: ...
    @overload
    def __truediv__(self, _rhs: Union[Inductance, UnitExpr[Inductance]]) -> Current: ...
    @overload
    def __truediv__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Inductance: ...
    @overload
    def __truediv__(self, _rhs: Union[Resistance, UnitExpr[Resistance]]) -> Charge: ...
    @overload
    def __truediv__(self, _rhs: Union[FluxDensity, UnitExpr[FluxDensity]]) -> Area: ...
    @overload
    def __truediv__(self, _rhs: Union[Charge, UnitExpr[Charge]]) -> Resistance: ...
    @overload
    def __truediv__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Voltage: ...
    @overload
    def __truediv__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Time: ...
    @overload
    def __truediv__(self, _rhs: Union[Flux, UnitExpr[Flux]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Flux: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Flux, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> FluxUnitExpr:
        return FluxUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> FluxUnit:
        return FluxUnit(abbr, self, singular=singular)
        
MagneticFlux = Flux


class FluxUnitExpr(UnitExpr[Flux]):
    """
    A :class:`.UnitExpr`[:class:`Flux`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Flux]] = None, 
                singular: Optional[str] = None) -> FluxUnit:
        return cast(FluxUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Flux: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Frequency]) -> VoltageUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Current]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Conductance]) -> ChargeUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> FluxUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Flux, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Flux: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Area]) -> FluxDensityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Inductance]) -> CurrentUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Current]) -> InductanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Resistance]) -> ChargeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[FluxDensity]) -> AreaUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Charge]) -> ResistanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Time]) -> VoltageUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Voltage]) -> TimeUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Flux]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> FluxUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Flux, UnitExpr]:
        return super().__truediv__(rhs)


class FluxUnit(Unit[Flux], FluxUnitExpr):
    """
    A :class:`.Unit`[:class:`Flux`] and a :class:`FluxUnitExpr`
    """
    ...
        

class FluxDensity(DerivedDim):
    """
    A :class`.Quantity` representing flux density (:class:`Flux`\ ``/``:class:`Area`)

    :class:`MagneticInduction` is an alias.
    """
    derivation = Flux/Area

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> FluxDensity: ...
    @overload
    def __mul__(self, _rhs: Union[Area, UnitExpr[Area]]) -> Flux: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> FluxDensity: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[FluxDensity, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> FluxDensity: ...
    @overload
    def __truediv__(self, _rhs: Union[FluxDensity, UnitExpr[FluxDensity]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> FluxDensity: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[FluxDensity, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> FluxDensityUnitExpr:
        return FluxDensityUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> FluxDensityUnit:
        return FluxDensityUnit(abbr, self, singular=singular)
        
MagneticInduction = FluxDensity


class FluxDensityUnitExpr(UnitExpr[FluxDensity]):
    """
    A :class:`.UnitExpr`[:class:`FluxDensity`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[FluxDensity]] = None, 
                singular: Optional[str] = None) -> FluxDensityUnit:
        return cast(FluxDensityUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> FluxDensity: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Area]) -> FluxUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> FluxDensityUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[FluxDensity, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> FluxDensity: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[FluxDensity]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> FluxDensityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[FluxDensity, UnitExpr]:
        return super().__truediv__(rhs)


class FluxDensityUnit(Unit[FluxDensity], FluxDensityUnitExpr):
    """
    A :class:`.Unit`[:class:`FluxDensity`] and a :class:`FluxDensityUnitExpr`
    """
    ...
        

class Power(DerivedDim):
    """
    A :class`.Quantity` representing power (:class:`Work`\ ``/``:class:`Time`)
    """
    derivation = Work/Time

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[Time, UnitExpr[Time]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Power, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Power: ...
    @overload
    def __truediv__(self, _rhs: Union[Work, UnitExpr[Work]]) -> Frequency: ...
    @overload
    def __truediv__(self, _rhs: Union[Force, UnitExpr[Force]]) -> Velocity: ...
    @overload
    def __truediv__(self, _rhs: Union[Frequency, UnitExpr[Frequency]]) -> Work: ...
    @overload
    def __truediv__(self, _rhs: Union[Velocity, UnitExpr[Velocity]]) -> Force: ...
    @overload
    def __truediv__(self, _rhs: Union[FlowRate, UnitExpr[FlowRate]]) -> Pressure: ...
    @overload
    def __truediv__(self, _rhs: Union[Current, UnitExpr[Current]]) -> Voltage: ...
    @overload
    def __truediv__(self, _rhs: Union[Voltage, UnitExpr[Voltage]]) -> Current: ...
    @overload
    def __truediv__(self, _rhs: Union[Power, UnitExpr[Power]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Pressure, UnitExpr[Pressure]]) -> FlowRate: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Power: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Power, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> PowerUnitExpr:
        return PowerUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> PowerUnit:
        return PowerUnit(abbr, self, singular=singular)
        

class PowerUnitExpr(UnitExpr[Power]):
    """
    A :class:`.UnitExpr`[:class:`Power`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Power]] = None, 
                singular: Optional[str] = None) -> PowerUnit:
        return cast(PowerUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Power: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Time]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> PowerUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Power, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Power: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Work]) -> FrequencyUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Force]) -> VelocityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Frequency]) -> WorkUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Velocity]) -> ForceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[FlowRate]) -> PressureUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Current]) -> VoltageUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Voltage]) -> CurrentUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Power]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Pressure]) -> FlowRateUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> PowerUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Power, UnitExpr]:
        return super().__truediv__(rhs)


class PowerUnit(Unit[Power], PowerUnitExpr):
    """
    A :class:`.Unit`[:class:`Power`] and a :class:`PowerUnitExpr`
    """
    ...
        

class Illuminance(DerivedDim):
    """
    A :class`.Quantity` representing illuminance (:class:`LumInt`\ ``/``:class:`Area`)
    """
    derivation = LumInt/Area

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Illuminance: ...
    @overload
    def __mul__(self, _rhs: Union[Area, UnitExpr[Area]]) -> LumInt: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Illuminance: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Illuminance, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Illuminance: ...
    @overload
    def __truediv__(self, _rhs: Union[Illuminance, UnitExpr[Illuminance]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Illuminance: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Illuminance, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> IlluminanceUnitExpr:
        return IlluminanceUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> IlluminanceUnit:
        return IlluminanceUnit(abbr, self, singular=singular)
        

class IlluminanceUnitExpr(UnitExpr[Illuminance]):
    """
    A :class:`.UnitExpr`[:class:`Illuminance`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Illuminance]] = None, 
                singular: Optional[str] = None) -> IlluminanceUnit:
        return cast(IlluminanceUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Illuminance: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Area]) -> LumIntUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> IlluminanceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Illuminance, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Illuminance: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Illuminance]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> IlluminanceUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Illuminance, UnitExpr]:
        return super().__truediv__(rhs)


class IlluminanceUnit(Unit[Illuminance], IlluminanceUnitExpr):
    """
    A :class:`.Unit`[:class:`Illuminance`] and a :class:`IlluminanceUnitExpr`
    """
    ...
        

class Pressure(DerivedDim):
    """
    A :class`.Quantity` representing pressure (:class:`Force`\ ``/``:class:`Area`)
    """
    derivation = Force/Area

    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Pressure: ...
    @overload
    def __mul__(self, _rhs: Union[SpecificVolume, UnitExpr[SpecificVolume]]) -> IonizingRadDose: ...
    @overload
    def __mul__(self, _rhs: Union[Volume, UnitExpr[Volume]]) -> Work: ...
    @overload
    def __mul__(self, _rhs: Union[Area, UnitExpr[Area]]) -> Force: ...
    @overload
    def __mul__(self, _rhs: Union[FlowRate, UnitExpr[FlowRate]]) -> Power: ...
    @overload
    def __mul__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Pressure: ...
    @overload
    def __mul__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __mul__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Pressure, Quantity]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Pressure: ...
    @overload
    def __truediv__(self, _rhs: Union[Density, UnitExpr[Density]]) -> IonizingRadDose: ...
    @overload
    def __truediv__(self, _rhs: Union[IonizingRadDose, UnitExpr[IonizingRadDose]]) -> Density: ...
    @overload
    def __truediv__(self, _rhs: Union[Pressure, UnitExpr[Pressure]]) -> Scalar: ...
    @overload
    def __truediv__(self, _rhs: Union[Scalar, UnitExpr[Scalar]]) -> Pressure: ...
    @overload
    def __truediv__(self, _rhs: Union[Quantity, UnitExpr]) -> Quantity: ...
    def __truediv__(self, rhs: Union[float, Quantity, UnitExpr]) -> Union[Pressure, Quantity]:
        return super().__truediv__(rhs)


    def as_unit_expr(self, num: tuple[AbbrExp, ...], denom: tuple[AbbrExp, ...]) -> PressureUnitExpr:
        return PressureUnitExpr(self, num, denom)
        
    def as_unit(self, abbr: str, *, singular: Optional[str] = None) -> PressureUnit:
        return PressureUnit(abbr, self, singular=singular)
        

class PressureUnitExpr(UnitExpr[Pressure]):
    """
    A :class:`.UnitExpr`[:class:`Pressure`]
    """
    
    def as_unit(self, abbr: str, *,
                check: Optional[type[Pressure]] = None, 
                singular: Optional[str] = None) -> PressureUnit:
        return cast(PressureUnit, super().as_unit(abbr, check=check, singular=singular))
        
    @overload    # type: ignore[override]
    def __mul__(self, _rhs: float) -> Pressure: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[SpecificVolume]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Volume]) -> WorkUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Area]) -> ForceUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[FlowRate]) -> PowerUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr[Scalar]) -> PressureUnitExpr: ...
    @overload
    def __mul__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __mul__(self, rhs: Union[float, UnitExpr]) -> Union[Pressure, UnitExpr]:
        return super().__mul__(rhs)

    @overload    # type: ignore[override]
    def __truediv__(self, _rhs: float) -> Pressure: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Density]) -> IonizingRadDoseUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[IonizingRadDose]) -> DensityUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Pressure]) -> ScalarUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr[Scalar]) -> PressureUnitExpr: ...
    @overload
    def __truediv__(self, _rhs: UnitExpr) -> UnitExpr: ...
    def __truediv__(self, rhs: Union[float, UnitExpr]) -> Union[Pressure, UnitExpr]:
        return super().__truediv__(rhs)


class PressureUnit(Unit[Pressure], PressureUnitExpr):
    """
    A :class:`.Unit`[:class:`Pressure`] and a :class:`PressureUnitExpr`
    """
    ...
        

