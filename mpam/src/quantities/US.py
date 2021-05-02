from . import core, prefixes, SI
from quantities import dimensions


# mass
lb = pound = core.Unit("lb", 0.45359237*SI.kg)
oz = ounce = core.Unit("oz", lb/16)
dr = dram = core.Unit("dr", oz/16)
gr = grain = core.Unit("gr", lb/7000)
ct = carat = core.Unit("ct", 200*SI.mg)
cwt = hundredweight = core.Unit("cwt", 100*lb)
ton = core.Unit("ton", 2000*lb)
long_cwt = long_hundredweight = core.Unit("long_cwt", 112*lb)
long_ton = core.Unit("long_ton", 2240*lb)

dwt = pennyweight = core.Unit("dwt", 24*gr)
oz_t = troy_oz = troy_ounce = core.Unit("oz_t", 20*dwt)
lb_t = troy_lb = troy_pound = core.Unit("lb_t", 12*oz_t)

slug = core.Unit("slug", 32.1740*lb)

# distance 

inch = core.Unit("in", 2.54*SI.cm)
ft = foot = core.Unit("ft", 12*inch)
yd = yard = core.Unit("yd", 3*ft)
mi = mile = core.Unit("mi", 5280*ft)
point = core.Unit("point", inch/72)
fur = furlong = core.Unit("fur", 660*ft)
lea = league = core.Unit("lea", 3*mi)
ftm = fathom = core.Unit("yd", 2*yd)
nmi = nautical_mile = core.Unit("nmi", 1.151*mi)
hand = core.Unit("hand", 4*inch)
th = thou = core.Unit("th", inch/1000)
ch = chain = core.Unit("ch", 66*ft)
cable = core.Unit("cable", 100*ftm)

#area

sq_in = square_inch = core.Unit[dimensions.Area]("sq_in", inch**2)
sq_ft = square_foot = core.Unit[dimensions.Area]("sq_ft", ft**2)
sq_mi = square_mile = core.Unit[dimensions.Area]("sq_mi", mi**2)
acre = core.Unit("acre", sq_mi/640)
section = core.Unit("section", sq_mi)

# volume
cu_in = cubic_inch = core.Unit[dimensions.Volume]("cu_in", inch**3)
gal = gallon = core.Unit("gal", 231*cu_in)
fl_oz = fluid_ounce = core.Unit("fl_oz", gal/128)
qt = quart = core.Unit("qt", 32*fl_oz)
pt = pint = core.Unit("pt", 16*fl_oz)
cup = core.Unit("C", 8*fl_oz)
Tbsp = tablespoon = core.Unit("Tbsp", fl_oz/2)
tsp = teaspoon = core.Unit("tsp", Tbsp/3)
fl_dr = fluid_dram = core.Unit("fl_dr", Tbsp/4)
minim = core.Unit("min", tsp/80)
shot = jig = jigger = core.Unit("jig", 1.5*fl_oz)
bbl = barrel = core.Unit("bbl", 31.5*gal)
hogshead = core.Unit("hogshead", 63*gal)
board_ft = board_foot = core.Unit[dimensions.Volume]("board_ft", ft**2*inch)

pt_d = dry_pt = dry_pint = core.Unit("pt_d", 33.6003125*cu_in)
qt_d = dry_qt = dry_quart = core.Unit("qt_d", 2*pt_d)
gal_d = dry_gal = dry_gallon = core.Unit("gal_d", 4*qt_d)
pk = peck = core.Unit("pk", 2*gal_d)
bu = bushel = core.Unit("bu", 4*pk)
bbl_d = dry_bbl = dry_barrel = core.Unit("bbl_d", 7056*cu_in)

# time

s = SI.s
mins = SI.mins
hr = SI.hr

# velocity
fps = foot_per_second = core.Unit[dimensions.Velocity]("fps", ft/s)
mph = mile_per_hour = core.Unit[dimensions.Velocity]("mph", mi/hr)

# temperature
deg_F = core.Unit("°F", 1.8*SI.deg_C)

# work
Btu = core.Unit("Btu", 1054*prefixes.kilo(SI.J))
cal = small_cal = small_calorie = core.Unit("cal", 4.184*SI.J)
kcal = kilocalorie = prefixes.kilo(small_cal)
Cal = food_calorie = calorie = core.Unit("Cal", kcal)

# force
pdl = poundal = core.Unit[dimensions.Force]("pdl", lb*ft/s**2)
lbf = pound_force = core.Unit[dimensions.Force]("lbf", slug*ft/s**2)

# pressure
psi = core.Unit[dimensions.Pressure]("psi", lbf/sq_in)

# power
hp = horsepower = core.Unit("hp", 845.7*SI.W)

