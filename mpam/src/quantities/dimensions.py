from .core import scalar, BaseDimension
mass = BaseDimension("mass")
distance = BaseDimension("distance")
time = BaseDimension("time")
temperature = BaseDimension("temperature")
lum_int = BaseDimension("lum_int")
current = BaseDimension("current")
storage = BaseDimension("storage")

angle = scalar
solid_angle = scalar
area = (distance**2).named("area")
volume = (distance**3).named("volume")
frequency = (scalar/time).named("frequency")
radioactivity = frequency
velocity = (distance/time).named("velocity")
acceleration = (velocity/time).named("acceleration")
force = (mass*acceleration).named("force")
work = (force*distance).named("work")
pressure = (force/area).named("pressure")
power = (work/time).named("power")
lum_flux = lum_int
charge = (current*time).named("charge")
voltage = (work/charge).named("voltage")
emf = elec_potential = voltage
flux = (voltage*time).named("flux")
magnetic_flux = flux
flux_density = (flux/area).named("flux_density")
magnetic_induction = flux_density
capacitance = (charge/voltage).named("capacitance")
resistance = (voltage/current).named("resistance")
conductance = (current/voltage).named("conductance")
inductance = (resistance*time).named("inductance")
ionizing_rad_dose = (work/mass).named("ionizing_rad_dose")
