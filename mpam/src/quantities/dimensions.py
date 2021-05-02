from .core import scalar, BaseDimension, Dimensionality
from typing import NewType, cast

Mass = NewType('Mass', Dimensionality)
mass = BaseDimension[Mass]("mass")

Distance = NewType('Distance', Dimensionality)
distance = BaseDimension[Distance]("distance")

Time = NewType('Time', Dimensionality)
time = BaseDimension[Time]("time")

Temperature = NewType('Temperature', Dimensionality)
temperature = BaseDimension[Temperature]("temperature")

LumInt = NewType('LumInt', Dimensionality)
lum_int = BaseDimension[LumInt]("lum_int")

Current = NewType('Current', Dimensionality)
current = BaseDimension[Current]("current")

Storage = NewType('Storage', Dimensionality)
storage = BaseDimension[Storage]("storage")

Angle = NewType('Angle', Dimensionality)
angle = cast(Angle, scalar)

SolidAngle = NewType('SolidAngle', Dimensionality)
solid_angle = cast(SolidAngle, scalar)

Area = NewType('Area', Dimensionality)
area = (distance**2).named("area")

Volume = NewType('Volume', Dimensionality)
volume = (distance**3).named("volume")


Frequency = NewType('Frequency', Dimensionality)
frequency = (scalar/time).named("frequency")

Radioactivity = NewType('Radioactivity', Dimensionality)
radioactivity = frequency

Velocity = NewType('Velocity', Dimensionality)
velocity = (distance/time).named("velocity")

Acceleration = NewType('Acceleration', Dimensionality)
acceleration = (velocity/time).named("acceleration")

Force = NewType('Force', Dimensionality)
force = (mass*acceleration).named("force")

Work = NewType('Work', Dimensionality)
work = (force*distance).named("work")

Pressure = NewType('Pressure', Dimensionality)
pressure = (force/area).named("pressure")

Power = NewType('Power', Dimensionality)
power = (work/time).named("power")

LumFlux = NewType('LumFlux', Dimensionality)
lum_flux = lum_int

Illuminance = NewType('Illuminance', Dimensionality)
illuminance = (lum_flux/area).named("illuminance")

Charge = NewType('Charge', Dimensionality)
charge = (current*time).named("charge")

Voltage = NewType('Voltage', Dimensionality)
voltage = (work/charge).named("voltage")

Emf = NewType('Emf', Dimensionality)
emf = elec_potential = voltage

Flux = NewType('Flux', Dimensionality)
flux = (voltage*time).named("flux")

MagneticFlux = NewType('MagneticFlux', Dimensionality)
magnetic_flux = flux

FluxDensity = NewType('FluxDensity', Dimensionality)
flux_density = (flux/area).named("flux_density")

MagneticInduction = NewType('MagneticInduction', Dimensionality)
magnetic_induction = flux_density

Capacitance = NewType('Capacitance', Dimensionality)
capacitance = (charge/voltage).named("capacitance")

Resistance = NewType('Resistance', Dimensionality)
resistance = (voltage/current).named("resistance")

Conductance = NewType('Conductance', Dimensionality)
conductance = (current/voltage).named("conductance")

Inductance = NewType('Inductance', Dimensionality)
inductance = (resistance*time).named("inductance")

IonizingRadDose = NewType('IonizingRadDose', Dimensionality)
ionizing_rad_dose = (work/mass).named("ionizing_rad_dose")
