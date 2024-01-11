from __future__ import annotations

from _collections import defaultdict
from argparse import ArgumentTypeError
from re import Pattern
import re
from typing import Final, Optional, Mapping, Sequence, TypeVar, Union, NoReturn

from quantities import temperature
from quantities.SI import ns, us, ms, sec, minutes, hr, days, mL, volts, uL, Hz, \
    deg_C, deg_K
from quantities.US import deg_F
from quantities.core import Quantity, UnitExpr
from quantities.dimensions import Time, Volume, Voltage, Frequency, Temperature, \
    TemperatureUnit
from quantities.prefixes import kilo, milli
from quantities.temperature import abs_C, abs_K, abs_F, TemperaturePoint

from .grid import XYCoord
from .logspec import logging_levels, logging_formats, LoggingSpec, \
    LoggingLevel
from .network import canonicalize_ip_addr
from .stringutils import conj_str


Q_ = TypeVar("Q_", bound = Quantity)


class ArgUnits:
    known: Final[dict[type[Quantity], dict[str, UnitExpr]]] = defaultdict(dict)
    patterns: Final[dict[type[Quantity], Pattern]] = {}
    all_unit_pattern: Optional[Pattern] = None
    
    @classmethod
    def register_units(cls, qt: type[Q_], units: Mapping[UnitExpr[Q_], Sequence[str]]) -> None:
        for unit,names in units.items():
            for name in names:
                cls.known[qt][name] = unit
                
    @classmethod
    def disjunction(cls, qt: type[Quantity]) -> str:
        return "|".join(sorted(cls.known[qt]))
    
    
    @classmethod
    def describe(cls, qt: type[Quantity], *, conj: str="and") -> str:
        tname = qt.__name__
        pairs = [(u,n) for n,u in cls.known[qt].items()]
        names = [f'"{n}"' for _u,n in sorted(pairs)]
        if len(names) == 0:
            return f"No known units for {tname}."
        return f"Known units for {tname} are: {conj_str(names, conj=conj)}."
    
    @classmethod
    def lookup(cls, qt: type[Q_], name: str) -> UnitExpr[Q_]:
        units = cls.known[qt]
        unit = units.get(name, None)
        if unit is None:
            raise ValueError(f"{name} is not a known {qt.__name__} unit. {cls.describe(qt)}")
        return unit
    
    
    @classmethod
    def parse_arg(cls, qt: type[Q_], arg: str, *, 
                  default: Optional[str] = None) -> Q_:
        pat = cls.patterns.get(qt, None)
        if pat is None:
            pat = re.compile(f"(-?\\d+(?:.\\d+)?)\\s*({ArgUnits.disjunction(qt)})") 
            cls.patterns[qt] = pat
        m = pat.fullmatch(arg)
        if m is None:
            if default is None:
                default = "200ms"
            raise ArgumentTypeError(f"""
                        {arg} not parsable as a {qt.__name__} value.
                        Requires a number followed immediately by units, e.g. '{default}'.
                        {ArgUnits.describe(qt)}""")
        n = float(m.group(1))
        # unit = time_arg_units.get(m.group(2), None)
        unit = ArgUnits.lookup(qt, m.group(2))
        val = n*unit
        return val
    
    
    @classmethod
    def find_unit(cls, arg: str) -> Optional[UnitExpr]:
        for units in cls.known.values():
            if (unit := units.get(arg, None)) is not None:
                return unit
        return None
    
    @classmethod
    def parse_unit_arg(cls, args: str) -> Sequence[UnitExpr]:
        units: list[UnitExpr] = []
        for arg in re.split(r'[ ,]\s*', args):
            unit = cls.find_unit(arg)
            if unit is None:
                raise ArgumentTypeError(f"""
                            '{arg}' not parsable as a unit.
                            {' '.join(cls.describe(qt) for qt in cls.known)}
                            """)
            units.append(unit)
        return units
        
        
ArgUnits.register_units(Time,
                        {
                            ns: ("ns", "nsec"),
                            us: ("us", "usec"),
                            ms: ("ms", "msec"),
                            sec: ("s", "sec", "secs", "second", "seconds"),
                            minutes: ("min", "minute", "minutes"),
                            hr: ("hr", "hour", "hours"),
                            days: ("days", "day"),
                            }                        
                        )

def time_arg(arg: str) -> Time:
    return ArgUnits.parse_arg(Time, arg, default="30ms")

ArgUnits.register_units(Frequency, { Hz: ("Hz", "hz")})


ArgUnits.register_units(Volume,
                        {
                            uL: ("ul", "uL", "microliter", "microliters", "microlitre", "microliters"),
                            mL: ("ml", "mL", "milliliter", "milliliters", "millilitre", "milliliters"),
                            }
                        )

drops_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)(?:drops|drop)")

def volume_arg(arg: str) -> Union[Volume,float]:
    m = drops_arg_re.fullmatch(arg)
    if m is not None:
        return float(m.group(1))
    return ArgUnits.parse_arg(Volume, arg, default = "30uL' or '2drops")

abs_temperature_arg_scales: Final[Mapping[str, temperature.Scale]] = {
    "C": abs_C,
    "K": abs_K,
    "F": abs_F,
    }

abs_temperature_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)({'|'.join(abs_temperature_arg_scales)})")

def abs_temperature_arg(arg: str) -> TemperaturePoint:
    m = abs_temperature_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a temperature value.
                    Requires a number followed immediately by units, e.g. '40C' or '200F'""")
    n = float(m.group(1))
    ustr = m.group(2)
    unit = abs_temperature_arg_scales.get(ustr, None)
    if unit is None:
        raise ValueError(f"{ustr} is not a known temperature unit")
    val = n*unit
    return val

rel_temperature_arg_scales: Final[Mapping[str, TemperatureUnit]] = {
    "C": deg_C,
    "K": deg_K,
    "F": deg_F,
    }

rel_temperature_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)({'|'.join(rel_temperature_arg_scales)})")

def rel_temperature_arg(arg: str) -> Temperature:
    m = rel_temperature_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a temperature value.
                    Requires a number followed immediately by units, e.g. '2C' or '0.5F'""")
    n = float(m.group(1))
    ustr = m.group(2)
    unit = rel_temperature_arg_scales.get(ustr, None)
    if unit is None:
        raise ValueError(f"{ustr} is not a known temperature unit")
    val = n*unit
    return val

ArgUnits.register_units(Voltage,
                        {
                            volts: ("V", "v", "volt", "volts"),
                            kilo(volts): ("kV", "KV", "kv", "kilovolt", "kilovolts"),
                            milli(volts): ("mV", "mv", "millivolt", "millivolts")
                        })
def voltage_arg(arg: str) -> Voltage:
    return ArgUnits.parse_arg(Voltage, arg, default="60V")


def units_arg(arg: str) -> Sequence[UnitExpr]:
    return ArgUnits.parse_unit_arg(arg)

logging_spec_arg_re: Final[Pattern] = re.compile(f"""(?:(.*?):)?
                                                   ({'|'.join(logging_levels)}|[0-9]+)
                                                   (?::({'|'.join(logging_formats.keys())}))?""",
                                                 re.VERBOSE | re.IGNORECASE)
def logging_spec_arg(arg: str) -> LoggingSpec:
    def raise_error() -> NoReturn:
        raise ArgumentTypeError(f"""
                "{arg}" not parsable as a logging spec.  The format is [<name>:]<level>[:<format>],
                where <level> is an integer or one of {conj_str(logging_levels)}
                and <format> is one of {conj_str([k.upper() for k in
                logging_formats.keys()])}.
                """)
    m = logging_spec_arg_re.fullmatch(arg)
    if m is None:
        raise_error()
        
    name: Optional[str] = m.group(1)
    level = LoggingLevel.find(m.group(2).upper())
    fmt: Optional[str] = m.group(3)
    if not fmt is None:
        fmt = fmt.lower()
    val = LoggingSpec(level, name=name, fmt_name=fmt)
    # print(f"log spec: {val}")
    return val

def ip_addr_arg(arg: str) -> str:
    try:
        if arg.count(".") == 3:
            return canonicalize_ip_addr(arg)
    except ValueError:
        pass
    raise ArgumentTypeError(f'"{arg}" not parsable as an IP address')
    
def ip_subnet_arg(arg: str) -> str:
    try:
        canonicalize_ip_addr(arg)
        return arg
    except ValueError:
        pass
    raise ArgumentTypeError(f'"{arg}" not parsable as an IP subnet')

coord_arg_re: Final[Pattern] = re.compile(f"(\\d+),\s*(\\d+)")

def coord_arg(arg: str) -> XYCoord:
    m = coord_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a coordinate.
                    Requires a pair of non-negative integers separated by a comma""")
    x = int(m.group(1))
    y = int(m.group(2))
    return XYCoord(x,y)

