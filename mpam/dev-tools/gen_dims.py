from __future__ import annotations

from dim_generator import Dimensionality, Emitter
    
scalar = Dimensionality.scalar()
scalar.aliases.extend(("Angle", "SolidAngle"))
distance = Dimensionality.base("dist").named("Distance")
mass = Dimensionality.base("mass").named("Mass")
time = Dimensionality.base("time").named("Time")
current = Dimensionality.base("curr").named("Current")
temperature = Dimensionality.base("temp").named("Temperature")
amount = Dimensionality.base("amt").named("Amount")
# volume_substance = Dimensionality.base("Vs").named("Volume[Substance]")
lum_flux = lum_int = Dimensionality.base("lum").named("LumInt", alias="LumFlux", description="luminous intensity")
storage = Dimensionality.base("storage").named("Storage")
money = Dimensionality.base("money").named("Money", alias="Price")

area = distance.derived_power(2, "Area")
volume = distance.derived_power(3, "Volume")
density = mass.derived_quotient(volume, "Density", alias="MassConcentration")
molar_concentration = amount.derived_quotient(volume, "MolarConcentration",
                                              alias = "Molarity")
specific_volume = volume.derived_quotient(mass, "SpecificVolume")
# volume_concentration = volume_substance.derived_quotient(volume, "VolumeConcentration") 
frequency = scalar.derived_quotient(time, "Frequency", alias="Radioactivity")
velocity = distance.derived_quotient(time, "Velocity")
acceleration = velocity.derived_quotient(time, "Acceleration")
force = mass.derived_product(acceleration, "Force")
work = force.derived_product(distance, "Work")
pressure = force.derived_quotient(area, "Pressure")
power = work.derived_quotient(time, "Power")
illuminance = lum_flux.derived_quotient(area, "Illuminance")
charge = current.derived_product(time, "Charge")
voltage = work.derived_quotient(charge, "Voltage", alias=("Emf", "EMF", "ElecPotential"))
flux = voltage.derived_product(time, "Flux", alias="MagneticFlux")
flux_density = flux.derived_quotient(area, "FluxDensity", alias="MagneticInduction")
capacitance = charge.derived_quotient(voltage, "Capacitance")
resistance = voltage.derived_quotient(current, "Resistance")
conductance = current.derived_quotient(voltage, "Conductance")
inductance = resistance.derived_product(time, "Inductance")
ionizing_rad_dose = work.derived_quotient(mass, "IonizingRadDose", description="ionizing radiation dose")
data_rate = storage.derived_quotient(time, "DataRate")
flow_rate = volume.derived_quotient(time, "FlowRate")
heating_rate = temperature.derived_quotient(time, "HeatingRate")
price_rate = money.derived_quotient(time, "PriceRate", alias="Salary")
vol_conc = volume["Substance"].derived_quotient(volume, "VolumeConcentration")

time.extra_code(f'''
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
''')

frequency.extra_code(f'''
    @classmethod
    def rate_from(cls, val: Union[Time, Frequency]) -> Frequency:
        return val if isinstance(val, Frequency) else 1/val

''')

money.extra_code(f'''
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
                 currency_proxy: Optional[CurrencyProxy] = None) -> None:
        self.currency_proxy = currency_proxy
        super().__init__(mag, dim)
                
    def __repr__(self) -> str:
        cp = self.currency_proxy
        if cp is None:
            return super().__repr__()
        return f"Quantity({{self.magnitude}}, {{self.dimensionality}}, {{cp}})"
    
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
        return Money(magnitude, dim=self.dimensionality, currency_proxy=self.currency_proxy)
    
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
            assert self.currency_proxy is not None, f"No default currency formatter and no currency proxy: {{self}}"
            formatter = self.currency_proxy.as_currency_formatter()
        if isinstance(formatter, Money.CurrencyFormatter):
            return formatter.format_currency(self, force_prefix=force_prefix,
                                             force_suffix=force_suffix, 
                                             decimal_places=decimal_places)
        else:
            return formatter(self)
''')

restrictions = ("Substance", "Solution", "Solvent")
extras = (time**2,
          mass*distance)

emitter = Emitter(extras=extras, restrictions=restrictions)
emitter.at_top(f'''
import time
from abc import ABC, abstractmethod
from typing import Protocol, Sequence, ClassVar, Callable, Iterable
from quantities.core import Dimensionality, _BoundQuantity, _DecomposedQuantity, T
''')
emitter.emit()


