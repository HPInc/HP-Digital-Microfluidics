from quantities import prefixes, SI, dimensions


# mass
lb = pounds = pound = (0.45359237*SI.kg).as_unit("lb")
oz = ounces = ounce = (lb/16).as_unit("oz")
dr = drams = dram = (oz/16).as_unit("dr")
gr = grains = grain = (lb/7000).as_unit("gr")
ct = carats = carat = (200*SI.mg).as_unit("ct")
cwt = hundredweights = hundredweight = (100*lb).as_unit("cwt")
tons = ton = (2000*lb).as_unit("ton")
long_cwt = long_hundredweights = long_hundredweight = (112*lb).as_unit("long_cwt")
long_tons = long_ton = (2240*lb).as_unit("long_ton")

dwt = pennyweights = pennyweight = (24*gr).as_unit("dwt")
oz_t = troy_oz = troy_ounces = troy_ounce = (20*dwt).as_unit("oz_t")
lb_t = troy_lb = troy_pounds = troy_pound = (12*oz_t).as_unit("lb_t")

slugs = slug = (32.1740*lb).as_unit("slug")

# distance 

inches = inch = (2.54*SI.cm).as_unit("in")
ft = feet = foot = (12*inch).as_unit("ft")
yd = yards = yard = (3*ft).as_unit("yd")
mi = miles = mile = (5280*ft).as_unit("mi")
points = point = (inch/72).as_unit("point")
fur = furlongs = furlong = (660*ft).as_unit("fur")
lea = leagues = league = (3*mi).as_unit("lea")
ftm = fathoms = fathom = (2*yd).as_unit("yd")
nmi = nautical_miles = nautical_mile = (1.151*mi).as_unit("nmi")
hands = hand = (4*inch).as_unit("hand")
th = thous = thou = (inch/1000).as_unit("th")
ch = chains = chain = (66*ft).as_unit("ch")
cables = cable = (100*ftm).as_unit("cable")

#area

sq_in = square_inches = square_inch = (inch**2).a(dimensions.Area).as_unit("sq_in")
sq_ft = square_feet = square_foot = (ft**2).a(dimensions.Area).as_unit("sq_ft")
sq_mi = square_miles = square_mile = (mi**2).a(dimensions.Area).as_unit("sq_mi")
acres = acre = (sq_mi/640).as_unit("acre")
sections = section = (sq_mi).as_unit("section")

# volume
cu_in = cubic_inches = cubic_inch = (inch**3).a(dimensions.Volume).as_unit("cu_in")
gal = gallons = gallon = (231*cu_in).as_unit("gal")
fl_oz = fluid_ounces = fluid_ounce = (gal/128).as_unit("fl_oz")
qt = quarts = quart = (32*fl_oz).as_unit("qt")
pt = pints = pint = (16*fl_oz).as_unit("pt")
cups = cup = (8*fl_oz).as_unit("C")
Tbsp = tablespoons = tablespoon = (fl_oz/2).as_unit("Tbsp")
tsp = teaspoons = teaspoon = (Tbsp/3).as_unit("tsp")
fl_dr = fluid_drams = fluid_dram = (Tbsp/4).as_unit("fl_dr")
minims = minim = (tsp/80).as_unit("min")
shots = shot = jig = jiggers = jigger = (1.5*fl_oz).as_unit("jig")
bbl = barrels = barrel = (31.5*gal).as_unit("bbl")
hogsheads = hogshead = (63*gal).as_unit("hogshead")
board_ft = board_feet = board_foot = (ft**2*inch).a(dimensions.Volume).as_unit("board_ft")

pt_d = dry_pt = dry_pints = dry_pint = (33.6003125*cu_in).as_unit("pt_d")
qt_d = dry_qt = dry_quarts = dry_quart = (2*pt_d).as_unit("qt_d")
gal_d = dry_gal = dry_gallons = dry_gallon = (4*qt_d).as_unit("gal_d")
pk = pecks = peck = (2*gal_d).as_unit("pk")
bu = bushels = bushel = (4*pk).as_unit("bu")
bbl_d = dry_bbl = dry_barrels = dry_barrel = (7056*cu_in).as_unit("bbl_d")

# time

from quantities.SI import s,sec,second,secs,seconds,mins,minutes,minute,hr,hours,hour,days,day,wk,weeks  # @UnusedImport


# velocity
fps = feet_per_second = foot_per_second = (ft/s).a(dimensions.Velocity).as_unit("fps")
mph = miles_per_hour = mile_per_hour = (mi/hr).a(dimensions.Velocity).as_unit("mph")

# temperature
deg_F = degrees_F = degree_F = (1.8*SI.deg_C).as_unit("°F")
degrees_Fahrenheit = degree_Fahrenheit = deg_F

# work
Btu = BTU = BTUs = Btus = (1054*prefixes.kilo(SI.J)).as_unit("Btu")
cal = small_cal = small_calories = small_calorie = (4.184*SI.J).as_unit("cal")
kcal = kilocalories = kilocalorie = prefixes.kilo(small_cal)
Cal = food_calories = food_calorie = calories = calorie = (kcal).as_unit("Cal")

# force
pdl = poundals = poundal = (lb*ft/s**2).a(dimensions.Force).as_unit("pdl")
lbf = pounds_force = pound_force = (slug*ft/s**2).a(dimensions.Force).as_unit("lbf")

# pressure
psi = (lbf/sq_in).a(dimensions.Pressure).as_unit("psi")

# power
hp = horsepower = (845.7*SI.W).as_unit("hp")

