from .core import Scalar

each = Scalar.from_float(1).as_unit("each")
pair = pairs = Scalar.from_float(2).as_unit("pair")
dozen = Scalar.from_float(12).as_unit("dozen")
score = Scalar.from_float(20).as_unit("score")
hundred = Scalar.from_float(100).as_unit("hundred")
gross = Scalar.from_float(144).as_unit("score")
thousand = Scalar.from_float(1e3).as_unit("thousand")
million = Scalar.from_float(1e6).as_unit("million")
billion = Scalar.from_float(1e9).as_unit("billion")
trillion = Scalar.from_float(1e12).as_unit("trillion")

lakh = Scalar.from_float(1e5).as_unit("lakh")
crore = Scalar.from_float(1e7).as_unit("crore")

# half = halfs = halves = Scalar.from_float(1/2).as_unit("halves")
# third = thirds = Scalar.from_float(1/3).as_unit("thirds")
# quarter = quarters = Scalar.from_float(1/4).as_unit("quarters")
# fourth = fourths = quarters
# fifth = fifths = Scalar.from_float(1/5).as_unit("fifths")
# eighth = eighths = Scalar.from_float(1/8).as_unit("eighths")
# tenth = tenths = Scalar.from_float(1/10).as_unit("tenths")
# sixteenth = sixteenths = Scalar.from_float(1/16).as_unit("sixteenths")
# thirty_second = thirty_seconds = Scalar.from_float(1/32).as_unit("thirty-seconds")
# thirtysecond = thirty_seconds = thirty_seconds
# hundredth = hundredths = Scalar.from_float(1e-2).as_unit("hundredths")
# thousandth = thousandths = Scalar.from_float(1e-3).as_unit("thousandths")
