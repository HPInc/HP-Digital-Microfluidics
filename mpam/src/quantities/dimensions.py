from __future__ import annotations

from quantities.core import BaseDim, DerivedDim, _DecomposedQuantity, Scalar
import time

class Mass(BaseDim): 
    """
    A :class:`.Quantity` representing mass
    
    SI :class:`.Unit`\s include:
        * :attr:`~quantities.SI.grams` (:attr:`~quantities.SI.g`,
          :attr:`~quantities.SI.gram`, :attr:`~quantities.SI.grammes`,
          :attr:`~quantities.SI.gramme`)
        * :attr:`~quantities.SI.micrograms` (:attr:`~quantities.SI.µg`,
          :attr:`~quantities.SI.ug`, :attr:`~quantities.SI.microgram`,
          :attr:`~quantities.SI.microgrammes`, :attr:`~quantities.SI.microgramme`)
        * :attr:`~quantities.SI.milligrams` (:attr:`~quantities.SI.mg`,
          :attr:`~quantities.SI.milligram`, :attr:`~quantities.SI.milligrammes`,
          :attr:`~quantities.SI.milligramme`
        * :attr:`~quantities.SI.kilograms` (:attr:`~quantities.SI.kg`,
          :attr:`~quantities.SI.kilogram`, :attr:`~quantities.SI.kilogrammes`,
          :attr:`~quantities.SI.kilogramme`)
        * :attr:`~quantities.SI.tonnes` (:attr:`~quantities.SI.tonne`,
          :attr:`~quantities.SI.metric_tons`, :attr:`~quantities.SI.metric_ton`,
          :attr:`~quantities.SI.metric_tonnes`,
          :attr:`~quantities.SI.metric_tonne`)
    """
    ...
    

class Distance(BaseDim): 
    """
    A :class:`.Quantity` representing distance

    SI :class:`.Unit`\s include:

       * :attr:`~quantities.SI.meters` (:attr:`~quantities.SI.m`,
         :attr:`~quantities.SI.meter`, :attr:`~quantities.SI.metres`, :attr:`~quantities.SI.metre`)
       * :attr:`~quantities.SI.nanometers` (:attr:`~quantities.SI.nm`,
         :attr:`~quantities.SI.nanometer`, :attr:`~quantities.SI.nanometres`,
         :attr:`~quantities.SI.nanometre`)
       * :attr:`~quantities.SI.microns` (:attr:`~quantities.SI.µm`,
         :attr:`~quantities.SI.um`, :attr:`~quantities.SI.micron`,
         :attr:`~quantities.SI.micrometers`, :attr:`~quantities.SI.micrometer`,
         :attr:`~quantities.SI.micrometres`, :attr:`~quantities.SI.micrometre`)
       * :attr:`~quantities.SI.millimeters` (:attr:`~quantities.SI.mm`,
         :attr:`~quantities.SI.millimeter`, :attr:`~quantities.SI.millimetres`,
         :attr:`~quantities.SI.millimetres`)
       * :attr:`~quantities.SI.decimeters` (:attr:`~quantities.SI.dm`,
         :attr:`~quantities.SI.decimeter`, :attr:`~quantities.SI.decimetres`,
         :attr:`~quantities.SI.decimetre`)
       * :attr:`~quantities.SI.kilometers` (:attr:`~quantities.SI.km`,
         :attr:`~quantities.SI.kilometer`, :attr:`~quantities.SI.kilometres`,
         :attr:`~quantities.SI.kilometre`)
    

    
    """
    ...
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

class Time(BaseDim): 
    """
    A :class:`.Quantity` representing time.
    
    :class:`Time` objects can be converted to (objects that convert to) strings
    in common formats by means of :func:`in_HMS`, :func:`in_HM`, and :func:`in_MS`.
    
    A float divided by a :class:`Time` yields a :class:`Frequency`

    SI :class:`.Unit`\s include:
       * :attr:`~quantities.SI.seconds` (:attr:`~quantities.SI.s`,
         :attr:`~quantities.SI.second`, :attr:`~quantities.SI.secs`,
         :attr:`~quantities.SI.sec`)
       * :attr:`~quantities.SI.milliseconds` (:attr:`~quantities.SI.ms`,
         :attr:`~quantities.SI.millisecond`, :attr:`~quantities.SI.millisecs`,
         :attr:`~quantities.SI.millisec`, :attr:`~quantities.SI.msecs`,
         :attr:`~quantities.SI.msec`)
       * :attr:`~quantities.SI.microseconds` (:attr:`~quantities.SI.µs`,
         :attr:`~quantities.SI.us`, :attr:`~quantities.SI.microsecond`,
         :attr:`~quantities.SI.microsecs`, :attr:`~quantities.SI.microsec`,
         :attr:`~quantities.SI.µsecs`, :attr:`~quantities.SI.µsec`,
         :attr:`~quantities.SI.usecs`, :attr:`~quantities.SI.usec`)
       * :attr:`~quantities.SI.nanoseconds` (:attr:`~quantities.SI.ns`,
         :attr:`~quantities.SI.nanosecond`, :attr:`~quantities.SI.nanosecs`,
         :attr:`~quantities.SI.nanosec`, :attr:`~quantities.SI.nsecs`,
         :attr:`~quantities.SI.nsec`)
       * :attr:`~quantities.SI.minutes`, (:attr:`~quantities.SI.minute`,
         :attr:`~quantities.SI.mins`).
         * Note: ``min`` is a reserved word in Python.
       * :attr:`~quantities.SI.hours` (:attr:`~quantities.SI.hr`,
         :attr:`~quantities.SI.hour`)
       * :attr:`~quantities.SI.days`, (:attr:`~quantities.SI.day`)
       * :attr:`~quantities.SI.weeks` (:attr:`~quantities.SI.wk`,
         :attr:`~quantities.SI.week`)
       * There is no predefined :class:`.Unit` for months or years, as those
         vary in length.
    
    """
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
    def __rtruediv__(self, lhs: float) -> Frequency:
        return super().__rtruediv__(lhs).a(Frequency)
    
    def sleep(self) -> None:
        from quantities import SI
        time.sleep(self.as_number(SI.seconds))
    
    # class _UnitExpr(UnitExpr[Time]): ...
    # class _Unit(Unit[Time]): ...
    #
    # def as_unit(self, abbr:str, *, singular:Optional[str]=None)->Time._Unit:
    #     return Time._Unit(abbr, self, singular=singular)
    #
    # @classmethod
    # def base_unit(cls, abbr: str, *, singular: Optional[str]=None) -> _Unit:
    #     return cast(Time._Unit, super().base_unit(abbr, singular=singular))
    

class Temperature(BaseDim): 
    """
    A :class:`.Quantity` representing temperature differences.  For absolute
    temperatures, use :class:`.TemperaturePoint`.

    SI :class:`.Unit`\s include:
       * :attr:`~quantities.SI.degrees_Kelvin` (:attr:`~quantities.SI.deg_K`,
         :attr:`~quantities.SI.K`,
         :attr:`~quantities.SI.degree_Kelvin`, :attr:`~quantities.SI.degrees_K`,
         :attr:`~quantities.SI.degree_K`, :attr:`~quantities.SI.kelvins`,
         :attr:`~quantities.SI.kelvin`)
       * :attr:`~quantities.SI.degrees_Celsius` (:attr:`~quantities.SI.deg_C`,
         :attr:`~quantities.SI.degree_Celsius`, :attr:`~quantities.SI.degrees_C`,
         :attr:`~quantities.SI.degree_C`,
         :attr:`~quantities.SI.degrees_centigrade`,
         :attr:`~quantities.SI.degree_centigrade`)

    """
    ...

class LumInt(BaseDim):
    """
    A :class:`.Quantity` representing luminous intensity
    
    :class:`LumFlux` is an alias
    """ 
    ...

class Current(BaseDim): 
    """
    A :class:`.Quantity` representing current
    """ 
    ...

class Amount(BaseDim):
    """
    A :class:`.Quantity` representing an amount of substance.
    """ 
    ...

Angle = Scalar
"""
An alias for :attr:`.Scalar` for representing angles

:class:`.Unit`\s include:
    * :attr:`~quantities.SI.radians` (:attr:`~quantities.SI.rad`,
      :attr:`~quantities.SI.radian`)
    * :attr:`~quantities.SI.degrees` (:attr:`~quantities.SI.deg`,
      :attr:`~quantities.SI.degree`)

"""
SolidAngle = Scalar
"""
An alias for :attr:`.Scalar` for representing solid angles

:class:`.Unit`\s include:
    * :attr:`~quantities.SI.steradians` (:attr:`~quantities.SI.sr`,
      :attr:`~quantities.SI.steradian`)
"""

class Area(DerivedDim): 
    """
    A :class:`.Quantity` representing area (:class:`Distance`\ ``**2``)

    SI :class:`.Unit`\s include:
       * :attr:`~quantities.SI.hectares` (:attr:`~quantities.SI.ha`,
         :attr:`~quantities.SI.hectare`)
    """ 
    derived = Distance**2
    # class AreaUnitExpr(UnitExpr['Area']): ...

class Volume(DerivedDim): 
    """
    A :class:`.Quantity` representing volume (:class:`Distance`\ ``**3``)

    SI :class:`.Unit`\s include:
       * :attr:`~quantities.SI.liters` (:attr:`~quantities.SI.L`,
         :attr:`~quantities.SI.l`, :attr:`~quantities.SI.liter`,
         :attr:`~quantities.SI.litres`, :attr:`~quantities.SI.litre`)
       * :attr:`~quantities.SI.deciliters` (:attr:`~quantities.SI.dL`,
         :attr:`~quantities.SI.dl`, :attr:`~quantities.SI.deciliter`,
         :attr:`~quantities.SI.decilitres`, :attr:`~quantities.SI.decilitre`)
       * :attr:`~quantities.SI.centiliters` (:attr:`~quantities.SI.cL`,
         :attr:`~quantities.SI.cl`, :attr:`~quantities.SI.centiliter`,
         :attr:`~quantities.SI.centilitres`, :attr:`~quantities.SI.centilitre`)
       * :attr:`~quantities.SI.milliliters` (:attr:`~quantities.SI.mL`,
         :attr:`~quantities.SI.ml`, :attr:`~quantities.SI.milliliter`,
         :attr:`~quantities.SI.millilitres`, :attr:`~quantities.SI.millilitre`)
       * :attr:`~quantities.SI.microliters` (:attr:`~quantities.SI.µL`,
         :attr:`~quantities.SI.µl`, :attr:`~quantities.SI.uL`,
         :attr:`~quantities.SI.ul`, :attr:`~quantities.SI.microliter`,
         :attr:`~quantities.SI.microlitres`, :attr:`~quantities.SI.microlitre`)
       * :attr:`~quantities.SI.nanoliters` (:attr:`~quantities.SI.nL`,
         :attr:`~quantities.SI.nl`, :attr:`~quantities.SI.nanoliter`,
         :attr:`~quantities.SI.nanolitres`, :attr:`~quantities.SI.nanolitre`)
       * :attr:`~quantities.SI.picoliters` (:attr:`~quantities.SI.pL`,
         :attr:`~quantities.SI.pl`, :attr:`~quantities.SI.picoliter`,
         :attr:`~quantities.SI.picolitres`, :attr:`~quantities.SI.picolitre`)
       * :attr:`~quantities.SI.cc`
       * :attr:`~quantities.SI.steres` (:attr:`~quantities.SI.st`,
         :attr:`~quantities.SI.stere`)
    """ 
    derived = Distance**3
    # class VolumeUnitExpr(UnitExpr['Volume']): ...
    
class Density(DerivedDim):
    """
    A :class:`.Quantity` representing density (:class:`Mass`\
    ``/``:class:`Volume`)
    
    :class:`MassConcentration` is an alias.
    """ 
    derived = Mass/Volume
    
class Substance:
    """
    A restriction base class.  
    
    This is mainly used for restricted dimensions when computing concentration
    dimensions such as 
    :class:`Volume`\ ``[``:class:`Substance`\ ``]/``:class:`Volume`\ ``[``:class:`Solution`\ ``]``.
    """ 
    ...
class Solution: 
    """
    A restriction base class.  
    
    This is mainly used for restricted dimensions when computing concentration
    dimensions such as 
    :class:`Volume`\ ``[``:class:`Substance`\ ``]/``:class:`Volume`\ ``[``:class:`Solution`\ ``]``.
    """ 
    ...
class Solvent: 
    """
    A restriction base class.  
    
    This is mainly used for restricted dimensions when computing concentration
    dimensions such as 
    :class:`Volume`\ ``[``:class:`Substance`\ ``]/``:class:`Volume`\ ``[``:class:`Solvent`\ ``]``.
    """ 
    ...
    
MassConcentration = Density
    
class MolarConcentration(DerivedDim):
    """
    A :class:`.Quantity` representing molar concentration 
    (:class:`Amount`\ ``/``:class:`Volume`)
    
    :class:`Molarity` is an alias.
    """ 
    derived = Amount/Volume
    
Molarity = MolarConcentration
    
class SpecificVolume(DerivedDim):
    """
    A :class:`.Quantity` representing specific volume
    (:class:`Volume`\ ``/``:class:`Mass`)
    """
    derived = Volume/Mass

class VolumeConcentration(DerivedDim):
    """
    A :class:`.Quantity` representing volume concentration
    (:class:`Volume`\ ``[``:class:`Substance`\ ``/``:class:`Volume`)
    """
    derived = Volume[Substance]/Volume
    
class Frequency(DerivedDim):
    """
    A :class:`.Quantity` representing frequency (``1/``:class:`Time`)
    
    A number divided by a :class:`Frequency` is a :class:`Time`.

    SI :class:`.Unit`\s include:

      * :attr:`~quantities.SI.hertz` (:attr:`~quantities.SI.Hz`)

    """ 
    derived = Scalar/Time
    def __rtruediv__(self, lhs: float) -> Time:
        return super().__rtruediv__(lhs).a(Time)
    

class Radioactivity(DerivedDim):
    """
    A :class:`.Quantity` representing radioactivity (``1/``:class:`Time`)

    """ 
    derived = Scalar/Time

class Velocity(DerivedDim): 
    """
    A :class:`.Quantity` representing velocity (:class:`Distance`\ ``/``:class:`Time`)
    """
    derived = Distance/Time

class Acceleration(DerivedDim): 
    """
    A :class:`.Quantity` representing acceleration (:class:`Velocity`\ ``/``:class:`Time`)
    """
    derived = Velocity/Time

class Force(DerivedDim): 
    """
    A :class:`.Quantity` representing force (:class:`Mass`\ ``*``:class:`Acceleration`)
    """
    derived = Mass*Acceleration

class Work(DerivedDim): 
    """
    A :class:`.Quantity` representing work (:class:`Force`\ ``*``:class:`Distance`)
    """
    derived = Force*Distance

class Pressure(DerivedDim): 
    """
    A :class:`.Quantity` representing pressure (:class:`Force`\ ``/``:class:`Area`)
    """
    derived = Force/Area

class Power(DerivedDim): 
    """
    A :class:`.Quantity` representing power (:class:`Work`\ ``/``:class:`Time`)
    """
    derived = Work/Time

LumFlux = LumInt

class Illuminance(DerivedDim): 
    """
    A :class:`.Quantity` representing illuminance (:class:`LumFlux`\ ``/``:class:`Area`)
    """
    derived = LumFlux/Area

class Charge(DerivedDim): 
    """
    A :class:`.Quantity` representing charge (:class:`Current`\ ``*``:class:`Time`)
    """
    derived = Current*Time

class Voltage(DerivedDim): 
    """
    A :class:`.Quantity` representing voltage (:class:`Work`\ ``/``:class:`Charge`)
    
    Aliases include :class:`Emf` and :class:`ElecPotential`.
    """
    derived = Work/Charge

Emf = ElecPotential = Voltage

class Flux(DerivedDim): 
    """
    A :class:`.Quantity` representing flux (:class:`Voltage`\ ``*``:class:`Time`)
    
    :class:`MagneticFlux` is an alias.
    """
    derived = Voltage*Time

MagneticFlux = Flux

class FluxDensity(DerivedDim): 
    """
    A :class:`.Quantity` representing flux density (:class:`Flux`\ ``/``:class:`Area`)
    
    :class:`MagneticInduction` is an alias.
    """
    derived = Flux/Area

MagneticInduction = FluxDensity

class Capacitance(DerivedDim): 
    """
    A :class:`.Quantity` representing capacitance (:class:`Charge`\ ``/``:class:`Voltage`)
    """
    derived = Charge/Voltage

class Resistance(DerivedDim): 
    """
    A :class:`.Quantity` representing resistance (:class:`Voltage`\ ``/``:class:`Current`)
    """
    derived = Voltage/Current

class Conductance(DerivedDim): 
    """
    A :class:`.Quantity` representing conductance (:class:`Current`\ ``/``:class:`Voltage`)
    """
    derived = Current/Voltage

class Inductance(DerivedDim): 
    """
    A :class:`.Quantity` representing inductance (:class:`Resistance`\ ``*``:class:`Time`)
    """
    derived = Resistance*Time

class IonizingRadDose(DerivedDim): 
    """
    A :class:`.Quantity` representing ionizing radiation dose (:class:`Work`\ ``/``:class:`Mass`)
    """
    derived = Work/Mass


    
    
