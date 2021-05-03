from quantities import prefixes, SI, dimensions


# mass
lb = pound = (0.45359237*SI.kg).as_unit("lb")
oz = ounce = (lb/16).as_unit("oz")
dr = dram = (oz/16).as_unit("dr")
gr = grain = (lb/7000).as_unit("gr")
ct = carat = (200*SI.mg).as_unit("ct")
cwt = hundredweight = (100*lb).as_unit("cwt")
ton = (2000*lb).as_unit("ton")
long_cwt = long_hundredweight = (112*lb).as_unit("long_cwt")
long_ton = (2240*lb).as_unit("long_ton")

dwt = pennyweight = (24*gr).as_unit("dwt")
oz_t = troy_oz = troy_ounce = (20*dwt).as_unit("oz_t")
lb_t = troy_lb = troy_pound = (12*oz_t).as_unit("lb_t")

slug = (32.1740*lb).as_unit("slug")

# distance 

inch = (2.54*SI.cm).as_unit("in")
ft = foot = (12*inch).as_unit("ft")
yd = yard = (3*ft).as_unit("yd")
mi = mile = (5280*ft).as_unit("mi")
point = (inch/72).as_unit("point")
fur = furlong = (660*ft).as_unit("fur")
lea = league = (3*mi).as_unit("lea")
ftm = fathom = (2*yd).as_unit("yd")
nmi = nautical_mile = (1.151*mi).as_unit("nmi")
hand = (4*inch).as_unit("hand")
th = thou = (inch/1000).as_unit("th")
ch = chain = (66*ft).as_unit("ch")
cable = (100*ftm).as_unit("cable")

#area

sq_in = square_inch = (inch**2).a(dimensions.Area).as_unit("sq_in")
sq_ft = square_foot = (ft**2).a(dimensions.Area).as_unit("sq_ft")
sq_mi = square_mile = (mi**2).a(dimensions.Area).as_unit("sq_mi")
acre = (sq_mi/640).as_unit("acre")
section = (sq_mi).as_unit("section")

# volume
cu_in = cubic_inch = (inch**3).a(dimensions.Volume).as_unit("cu_in")
gal = gallon = (231*cu_in).as_unit("gal")
fl_oz = fluid_ounce = (gal/128).as_unit("fl_oz")
qt = quart = (32*fl_oz).as_unit("qt")
pt = pint = (16*fl_oz).as_unit("pt")
cup = (8*fl_oz).as_unit("C")
Tbsp = tablespoon = (fl_oz/2).as_unit("Tbsp")
tsp = teaspoon = (Tbsp/3).as_unit("tsp")
fl_dr = fluid_dram = (Tbsp/4).as_unit("fl_dr")
minim = (tsp/80).as_unit("min")
shot = jig = jigger = (1.5*fl_oz).as_unit("jig")
bbl = barrel = (31.5*gal).as_unit("bbl")
hogshead = (63*gal).as_unit("hogshead")
board_ft = board_foot = (ft**2*inch).a(dimensions.Volume).as_unit("board_ft")

pt_d = dry_pt = dry_pint = (33.6003125*cu_in).as_unit("pt_d")
qt_d = dry_qt = dry_quart = (2*pt_d).as_unit("qt_d")
gal_d = dry_gal = dry_gallon = (4*qt_d).as_unit("gal_d")
pk = peck = (2*gal_d).as_unit("pk")
bu = bushel = (4*pk).as_unit("bu")
bbl_d = dry_bbl = dry_barrel = (7056*cu_in).as_unit("bbl_d")

# time

s = SI.s
mins = SI.mins
hr = SI.hr

# velocity
fps = foot_per_second = (ft/s).a(dimensions.Velocity).as_unit("fps")
mph = mile_per_hour = (mi/hr).a(dimensions.Velocity).as_unit("mph")

# temperature
deg_F = (1.8*SI.deg_C).as_unit("°F")

# work
Btu = (1054*prefixes.kilo(SI.J)).as_unit("Btu")
cal = small_cal = small_calorie = (4.184*SI.J).as_unit("cal")
kcal = kilocalorie = prefixes.kilo(small_cal)
Cal = food_calorie = calorie = (kcal).as_unit("Cal")

# force
pdl = poundal = (lb*ft/s**2).a(dimensions.Force).as_unit("pdl")
lbf = pound_force = (slug*ft/s**2).a(dimensions.Force).as_unit("lbf")

# pressure
psi = (lbf/sq_in).a(dimensions.Pressure).as_unit("psi")

# power
hp = horsepower = (845.7*SI.W).as_unit("hp")

