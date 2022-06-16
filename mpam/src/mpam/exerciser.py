from __future__ import annotations

from abc import ABC, abstractmethod
from argparse import ArgumentTypeError, Namespace, ArgumentParser, \
    _SubParsersAction, _ArgumentGroup
import logging.config
import pathlib
from re import Pattern
import re
from threading import Event
from typing import Final, Mapping, Union, Optional, Sequence, Any, Callable, \
    NoReturn, ClassVar, TypeVar

from matplotlib.gridspec import SubplotSpec

from erk.stringutils import conj_str
from mpam.device import Board, System
from mpam.monitor import BoardMonitor
from mpam.types import PathOrStr
from quantities import temperature
from quantities.SI import ns, us, ms, sec, minutes, hr, days, uL, mL, secs, \
    volts, deg_C
from quantities.core import Unit, Quantity, Dimensionality
from quantities.dimensions import Time, Volume, Voltage, Temperature
from quantities.prefixes import kilo
from quantities.temperature import abs_C, abs_K, abs_F, TemperaturePoint
from _collections import defaultdict


# import logging
logger = logging.getLogger(__name__)

Q_ = TypeVar("Q_", bound = Quantity)

class ArgUnits:
    known: Final[dict[type[Quantity], dict[str, Unit]]] = defaultdict(dict)
    patterns: Final[dict[type[Quantity], Pattern]] = {}
    all_unit_pattern: Optional[Pattern] = None
    
    @classmethod
    def register_units(cls, qt: type[Q_], units: Mapping[Unit[Q_], Sequence[str]]) -> None:
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
    def lookup(cls, qt: type[Q_], name: str) -> Unit[Q_]:
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
    def find_unit(cls, arg: str) -> Optional[Unit]:
        for units in cls.known.values():
            if (unit := units.get(arg, None)) is not None:
                return unit
        return None
    
    @classmethod
    def parse_unit_arg(cls, args: str) -> Mapping[Dimensionality, Sequence[Unit]]:
        found: dict[Dimensionality, list[Unit]] = defaultdict(list)
        for arg in re.split(r'[ ,]\s*', args):
            unit = cls.find_unit(arg)
            if unit is None:
                raise ArgumentTypeError(f"""
                            '{arg}' not parsable as a unit.
                            {' '.join(cls.describe(qt) for qt in cls.known)}
                            """)
            found[unit.dimensionality()].append(unit)
        return found
        
        
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

temperature_arg_scales: Final[Mapping[str, temperature.Scale]] = {
    "C": abs_C,
    "K": abs_K,
    "F": abs_F,
    }

temperature_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)({'|'.join(temperature_arg_scales)})")

def temperature_arg(arg: str) -> TemperaturePoint:
    m = temperature_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a temperature value.
                    Requires a number followed immediately by units, e.g. '40C' or '200F'""")
    n = float(m.group(1))
    ustr = m.group(2)
    unit = temperature_arg_scales.get(ustr, None)
    if unit is None:
        raise ValueError(f"{ustr} is not a known temperature unit")
    val = n*unit
    return val

ArgUnits.register_units(Voltage,
                        {
                            volts: ("V", "v", "volt", "volts"),
                            kilo(volts): ("kV", "KV", "kv", "kilovolt", "kilovolts"),
                        })
def voltage_arg(arg: str) -> Voltage:
    return ArgUnits.parse_arg(Voltage, arg, default="60V")


def units_arg(arg: str) -> Mapping[Dimensionality, Sequence[Unit]]:
    return ArgUnits.parse_unit_arg(arg)

class LoggingLevel:
    desc: Final[str]
    level: Final[int]
    
    built_in: ClassVar[Mapping[str, LoggingLevel]]
    
    @classmethod
    def options(cls) -> Sequence[str]:
        levels = list(cls.built_in.values())
        levels.sort(key=lambda x: x.level)
        return [level.desc for level in levels]

    def __init__(self, desc: str, level: int) -> None:
        self.desc = desc
        self.level = level
        
    def __repr__(self) ->str:
        return f"{type(self).__name__}('{self.desc}', {self.level})"
        
    @classmethod
    def find(cls, level: Union[str, int]) -> LoggingLevel:
        if isinstance(level, int):
            return LoggingLevel(str(level), level)
        val = cls.built_in.get(level.upper(), None)
        if val is not None:
            return val
        try:
            return cls.find(int(level))
        except ValueError:
            raise ValueError(f"Couldn't find logging level for '{level}'")
    
        
LoggingLevel.built_in = {
    "DEBUG": LoggingLevel("DEBUG", logging.DEBUG),
    "INFO": LoggingLevel("INFO", logging.INFO),
    "WARN": LoggingLevel("WARN", logging.WARNING),
    "WARNING": LoggingLevel("WARNING", logging.WARNING),
    "ERROR": LoggingLevel("ERROR", logging.ERROR),
    "CRITICAL": LoggingLevel("CRITICAL", logging.CRITICAL)
    }
        

class LoggingSpec:
    level: LoggingLevel
    name: Optional[str]
    fmt_name: Optional[str]
    
    def __init__(self, level: Union[LoggingLevel, str, int], *,
                 name: Optional[str] = None,
                 fmt_name: Optional[str] = None) -> None:
        if not isinstance(level, LoggingLevel):
            level = LoggingLevel.find(level)
        self.level = level
        self.name = name
        self.fmt_name = fmt_name
        
    def __repr__(self) -> str:
        name = "" if self.name is None else f", name='{self.name}'"
        fmt_name = "" if self.fmt_name is None else f", name='{self.fmt_name}'"
        return f"{type(self).__name__}({self.level}{name}{fmt_name})"
        
    
    
logging_levels = LoggingLevel.options()
logging_formats = {
    'compact': '%(levelname)7s|%(module)s|%(message)s',
    'detailed': '%(relativeCreated)6d|%(levelname)7s|%(threadName)s|%(filename)s:%(lineno)s:%(funcName)s|%(message)s', 
    }
    
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

class Task(ABC):
    name: Final[str]
    description: Final[str]
    aliases: Final[Sequence[str]]

    def __init__(self, name: str, description: str, *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        self.name = name
        self.description = description
        self.aliases = [] if aliases is None else aliases

    @abstractmethod
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        ...

    def add_args_to(self, parser: ArgumentParser, *, exerciser: Exerciser) -> None:  # @UnusedVariable
        ...

    def arg_group_in(self, parser: ArgumentParser,
                     name: str="task-specific options") -> _ArgumentGroup:
        return parser.add_argument_group(name)

    def control_setup(self, monitor: BoardMonitor, spec: SubplotSpec, exerciser: Exerciser) -> Any:
        return exerciser.control_setup(monitor, spec)


class Exerciser(ABC):
    parser: Final[ArgumentParser]
    subparsers: Final[Optional[_SubParsersAction]]

    default_initial_delay: Time = 5*secs
    default_min_time: Time = 5*minutes
    default_update_interval: Time = 20*ms
    default_off_on_delay: Time = 0*ms
    default_extraction_point_splash_radius: int = 0

    def __init__(self, description: Optional[str] = None, *,
                 task: Optional[Task] = None) -> None:
        if description is None:
            description = "run tasks on a board" if task is None else task.description
        self.parser = ArgumentParser(description=description)
        subparsers: Optional[_SubParsersAction]
        if task is not None:
            self.setup_task(task, parser=self.parser)
            subparsers = None
        else:
            subparsers = self.parser.add_subparsers(help="Tasks", dest='task_name', required=True, metavar='TASK')
        self.subparsers = subparsers

    @abstractmethod
    def make_board(self, args: Namespace) -> Board: ...  # @UnusedVariable

    @abstractmethod
    def available_wells(self) -> Sequence[int]: ...

    def control_setup(self, monitor: BoardMonitor, spec: SubplotSpec) -> Any: # @UnusedVariable
        return None
    
    def setup_task(self, task: Task, *,
                   parser: ArgumentParser) -> None:
        task.add_args_to(parser, exerciser=self)
        self.add_common_args_to(parser)
        parser.set_defaults(task=task)

    def add_task(self, task: Task, *,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 aliases: Optional[Sequence[str]] = None) -> Exerciser:
        subparsers = self.subparsers
        assert subparsers is not None, f"Cannot add task to single-task Exerciser '{self.parser.description}'"
        name = task.name if name is None else name
        desc = task.description if description is None else description
        aliases = task.aliases if aliases is None else aliases
        parser = subparsers.add_parser(name, help=desc, description=desc, aliases=aliases)
        self.setup_task(task, parser=parser)
        
        return self

    def run_task(self, task: Task, args: Namespace, *, board: Board) -> None:
        system = System(board=board)

        def prepare_and_run() -> None:
            if args.start_clock:
                system.clock.start(args.clock_speed)
            else:
                system.clock.update_interval = args.clock_speed
            task.run(board, system, args)

        def do_run() -> None:
            event = Event()
            system.call_after(args.initial_delay, lambda: event.set())
            event.wait()
            prepare_and_run()

        def make_controls(monitor: BoardMonitor, spec: SubplotSpec) -> Any:
            return task.control_setup(monitor, spec, self)

        if not args.use_display:
            with system:
                do_run()
            system.shutdown()
        else:
            system.run_monitored(lambda _: do_run(),
                                 min_time=args.min_time,
                                 max_time=args.max_time,
                                 update_interval=args.update_interval,
                                 control_setup = make_controls,
                                 macro_file_name = args.macro_file,
                                 thread_name = f"Monitored {task.name}",
                                 cmd_line_args = args)

    def parse_args(self,
                   args: Optional[Sequence[str]]=None,
                   namespace: Optional[Namespace]=None) -> tuple[Task, Namespace]:
        ns = self.parser.parse_args(args=args, namespace=namespace)
        Exerciser.setup_logging(levels=ns.log_level, file=ns.log_config)

        task: Task = ns.task
        return task, ns
    
    @classmethod
    def set_default_units(cls, 
                          unit_maps: Optional[Sequence[Mapping[Dimensionality, Sequence[Unit]]]]) -> None:
        if unit_maps is None:
            return
        combined: dict[Dimensionality, list[Unit]] = defaultdict(list)
        for m in unit_maps:
            for d,units in m.items():
                combined[d].extend(units)
        for d,units in combined.items():
            d.default_units = tuple(units)

    def parse_args_and_run(self,
                           args: Optional[Sequence[str]]=None,
                           namespace: Optional[Namespace]=None) -> None:
        # We set default units first so that default values for help and errors
        # will be printed correctly by parse_args()
        Time.default_units = ms
        Volume.default_units = uL
        Temperature.default_units = deg_C
        Voltage.default_units = volts
        task, ns = self.parse_args(args=args, namespace=namespace)
        if ns.trace_blobs:
            Board.trace_blobs = True
        self.set_default_units(ns.units)
        board = self.make_board(ns)
        self.run_task(task, ns, board=board)

    @classmethod
    def fmt_time(self, t: Time) -> str:
        return str(t.decomposed((days, hr, minutes, secs)))

    def add_device_specific_common_args(self,
                                        group: _ArgumentGroup,  # @UnusedVariable
                                        parser: ArgumentParser  # @UnusedVariable
                                        ) -> None:
        # by default, no args to add.
        group.add_argument("--trace-blobs", action="store_true",
                           help=f"Trace blobs.")

    def add_common_args_to(self, parser: ArgumentParser) -> None:
        group = parser.add_argument_group(title="common options")
        self.add_device_specific_common_args(group, parser)
        default_clock_interval=100*ms
        group.add_argument('-cs', '--clock-speed', type=time_arg, default=default_clock_interval, metavar='TIME',
                           help=f'''
                           The amount of time between clock ticks.
                           Default is {default_clock_interval.in_units(ms)}.
                           ''')
        group.add_argument('--paused', action='store_false', dest='start_clock',
                           help='''
                           Don't start the clock automatically. Note that operations that are not gated
                           by the clock may still run.
                           ''')
        group.add_argument('-ood','--off-on-delay', type=time_arg, metavar='TIME', default=self.default_off_on_delay,
                           help=f'''
                           The amount of time to wait between turning pads off
                           and turning pads on in a clock tick.  0ms is no
                           delay.  Negative values means pads are turned on before pads are turned off.
                           Default is {self.fmt_time(self.default_initial_delay)}.
                           ''')
        group.add_argument('--initial-delay', type=time_arg, metavar='TIME', default=self.default_initial_delay,
                           help=f'''
                           The amount of time to wait before running the task.
                           Default is {self.fmt_time(self.default_initial_delay)}.
                           ''')
        group.add_argument('--min-time', type=time_arg, default=self.default_min_time, metavar='TIME',
                           help=f'''
                           The minimum amount of time to leave the display up, even if the
                           operation has finished. Default is {self.fmt_time(self.default_min_time)}.
                           ''')
        group.add_argument('--max-time', type=time_arg, metavar='TIME',
                           help='''
                           The maximum amount of time to leave the display up, even if the
                           operation hasn't finished. Default is no limit
                           ''')
        group.add_argument('-nd', '--no-display', action='store_false', dest='use_display',
                            help='Run the task without the on-screen display')
        group.add_argument('--update-interval', type=time_arg, metavar='TIME', default=self.default_update_interval,
                           help=f'''
                           The maximum amount of time between display updates.
                           Default is {self.default_update_interval}.
                           ''')
        group.add_argument('--macro-file',
                           # type=FileType(),
                           metavar='FILE',
                           help='A file containing DMF macro definitions.')
        group.add_argument('-ep-rad', '--extraction-point-splash-radius', type=int, metavar="PADS",
                           default=self.default_extraction_point_splash_radius,
                           help=f'''
                           The radius (of square shape) around extraction point that is held in place while fluid is transferred (added or removed) from the extraction point.
                           Default is {self.default_extraction_point_splash_radius}.
                           ''')
        group.add_argument('--units', type=units_arg, action='append',
                           help="""
                               A comma- or space-separated list of units to use
                               for printing.  This argument may be specified
                               multiple times.  If more than one value is
                               provided for a given dimension, the unit chosen
                               will be the largest one that's no bigger than the
                               printed value (or the smallest if none are
                               smaller).  Default is equivalent to 'uL,ms,V'.
                               """)
        display_group = parser.add_argument_group("display_options")
        BoardMonitor.add_args_to(display_group, parser)
        log_group = group.add_mutually_exclusive_group()
        # level_choices = ['debug', 'info', 'warning', 'error', 'critical']
        # log_group.add_argument('--log-level', metavar='LEVEL',
        #                        choices=level_choices,
        #                        help=f'''
        #                        Configure the logging level.  Options are {conj_str([f'"{s}"' for s in level_choices])}
        #                        ''')
        log_group.add_argument('--log-config', metavar='FILE',
                               help='Configuration file for logging')
        log_group.add_argument('--log-level', metavar='SPEC', type=logging_spec_arg, action='append',
                               help=f""" 
                                    Configure logging.  The format is <level>,
                                    <name>:<level> or <level>:<format>, where
                                    <level> is an integer or one of
                                    {conj_str(logging_levels)} and <format> is
                                    one of {conj_str([k.upper() for k in
                                    logging_formats.keys()])}.  If <name> is
                                    specified, the given level is used for that
                                    logger (or any children).  If <name> is
                                    'modules', the level is used (by default) for loggers 
                                    from all known imported modules.  <level>
                                    and <format> are case-insensitive.  This
                                    argument may be specified multiple times.
                                    """)
        

    @staticmethod
    def setup_logging(*, levels: Optional[Union[str, LoggingSpec, 
                                                Sequence[Union[str, LoggingSpec]]]] = None,
                      file: PathOrStr = None,
                      default_file: Optional[
                          Union[PathOrStr, Callable[[], PathOrStr]]] = None) -> None:
        
        if levels == ():
            levels = None
        if levels is not None and file is not None:
            raise Exception("Specify 'level' or 'file' to 'setup_logging' but not both.")

        default_level = LoggingLevel.find("INFO")
                
        if levels is None and file is None:
            if default_file is None:
                default_file = pathlib.Path.cwd() / ".logging"
            elif not (isinstance(default_file, (str, pathlib.Path))):
                default_file = default_file()
            if pathlib.Path(default_file).exists():
                file = default_file
            else:
                levels = (LoggingSpec(default_level),)
                
        if file is not None:
            assert levels is None
            logging.config.fileConfig(file,
                                      defaults = {
                                          "format": logging_formats["compact"]})
            return

        if isinstance(levels, (str, LoggingSpec)):
            levels = (levels,)
        primary: LoggingSpec = LoggingSpec(default_level)
        
        default_import_level = LoggingLevel.find("WARNING")
        
        assert levels is not None
        
        imports: dict[str, LoggingLevel] = {}
        
        for spec in levels:
            if isinstance(spec, str):
                spec = logging_spec_arg(spec)
            if spec.name is None:
                primary = spec
            elif spec.name == "modules":
                default_import_level = spec.level
            else:
                imports[spec.name] = spec.level
                
        default_imports = ("matplotlib", "PIL", "aiohttp")
        for i in default_imports:
            if i not in imports:
                imports[i] = default_import_level         

                    
        base_level = primary.level
        fmt = primary.fmt_name
        if fmt is None:
            if base_level.level < logging.INFO:
                fmt = "detailed"
            else:
                fmt = "compact"
        logging.basicConfig(level=base_level.desc, format=logging_formats[fmt])
        
        for name,level in imports.items():
            logging.getLogger(name).setLevel(level.desc)
