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
vol_conc = volume["Substance"].derived_quotient(volume, "VolumeConcentration")

time.extra_code(f'''
    from quantities.core import _DecomposedQuantity
    def sleep(self) -> None:
        import time
        from quantities import SI
        time.sleep(self.as_number(SI.seconds))
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

restrictions = ("Substance", "Solution", "Solvent")
extras = (time**2,
          mass*distance)

emitter = Emitter(extras=extras, restrictions=restrictions)
emitter.emit()


