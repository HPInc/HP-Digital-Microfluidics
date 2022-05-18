from __future__ import annotations

from abc import ABC, abstractmethod
from argparse import ArgumentTypeError, Namespace, ArgumentParser, \
    _SubParsersAction, _ArgumentGroup
from re import Pattern
import re
from typing import Final, Mapping, Union, Optional, Sequence, Any
# import logging
import logging.config

from mpam.device import Board, System
from quantities.SI import ns, us, ms, sec, minutes, hr, days, uL, mL, secs,\
    volts
from quantities.core import Unit
from quantities.dimensions import Time, Volume, Voltage
from quantities.temperature import abs_C, abs_K, abs_F, TemperaturePoint
from quantities import temperature
from threading import Event
from matplotlib.gridspec import SubplotSpec
from mpam.monitor import BoardMonitor
import pathlib
from erk.stringutils import conj_str
from quantities.prefixes import kilo

logger = logging.getLogger(__name__)

time_arg_units: Final[Mapping[str, Unit[Time]]] = {
    "ns": ns,
    "nsec": ns,
    "us": us,
    "usec": us,
    "ms": ms,
    "msec": ms,
    "s": sec,
    "sec": sec,
    "secs": sec,
    "second": sec,
    "seconds": sec,
    "min": minutes,
    "minute": minutes,
    "minutes": minutes,
    "hr": hr,
    "hour": hr,
    "hours": hr,
    "days": days,
    "day": days
    }

time_arg_re: Final[Pattern] = re.compile(f"(-?\\d+(?:.\\d+)?)\\s*({'|'.join(time_arg_units)})")

def time_arg(arg: str) -> Time:
    m = time_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a time value.
                    Requires a number followed immediately by units, e.g. '30ms'""")
    n = float(m.group(1))
    unit = time_arg_units.get(m.group(2), None)
    if unit is None:
        raise ValueError(f"{m.group(2)} is not a known time unit")
    val = n*unit
    return val

volume_arg_units: Final[Mapping[str, Unit[Volume]]] = {
    "ul": uL,
    "uL": uL,
    "microliter": uL,
    "microliters": uL,
    "microlitre": uL,
    "microliters": uL,
    "ml": mL,
    "mL": mL,
    "milliliter": mL,
    "milliiters": mL,
    "millilitre": mL,
    "milliliters": mL,
    }

volume_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)({'|'.join(volume_arg_units)}|drops|drop)")

def volume_arg(arg: str) -> Union[Volume,float]:
    m = volume_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a volume value.
                    Requires a number followed immediately by units, e.g. '30uL' or '2drops'""")
    n = float(m.group(1))
    ustr = m.group(2)
    if ustr == "drops" or ustr == "drop":
        return n
    unit = volume_arg_units.get(ustr, None)
    if unit is None:
        raise ValueError(f"{ustr} is not a known volume unit")
    val = n*unit
    return val

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

voltage_arg_units: Final[Mapping[str, Unit[Voltage]]] = {
    "V": volts,
    "v": volts,
    "kV": kilo(volts),
    "kv": kilo(volts)
    }
voltage_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)({'|'.join(voltage_arg_units)})")

def voltage_arg(arg: str) -> Voltage:
    m = voltage_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a voltage value.
                    Requires a number followed immediately by units, e.g. '100V'""")
    n = float(m.group(1))
    unit = voltage_arg_units.get(m.group(2), None)
    if unit is None:
        raise ValueError(f"{m.group(2)} is not a known time unit")
    val = n*unit
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
    subparsers: Final[_SubParsersAction]

    default_initial_delay: Time = 5*secs
    default_min_time: Time = 5*minutes
    default_update_interval: Time = 20*ms
    default_off_on_delay: Time = 0*ms
    default_extraction_point_splash_radius: int = 0

    def __init__(self, description: str = "run tasks on a board") -> None:
        self.parser = ArgumentParser(description=description)
        self.subparsers = self.parser.add_subparsers(help="Tasks", dest='task_name', required=True, metavar='TASK')

    @abstractmethod
    def make_board(self, args: Namespace) -> Board: ...  # @UnusedVariable

    @abstractmethod
    def available_wells(self) -> Sequence[int]: ...

    def control_setup(self, monitor: BoardMonitor, spec: SubplotSpec) -> Any: # @UnusedVariable
        return None

    def add_task(self, task: Task, *,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 aliases: Optional[Sequence[str]] = None) -> Exerciser:
        name = task.name if name is None else name
        desc = task.description if description is None else description
        aliases = task.aliases if aliases is None else aliases
        parser = self.subparsers.add_parser(name, help=desc, description=desc, aliases=aliases)
        task.add_args_to(parser, exerciser=self)
        self.add_common_args_to(parser)
        parser.set_defaults(task=task)

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
        Exerciser.setup_logging(ns.log_level, ns.log_config)

        task: Task = ns.task
        return task, ns

    def parse_args_and_run(self,
                           args: Optional[Sequence[str]]=None,
                           namespace: Optional[Namespace]=None) -> None:
        task, ns = self.parse_args(args=args, namespace=namespace)
        if ns.trace_blobs:
            Board.trace_blobs = True
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
        group.add_argument('-ep-rad', '--extraction-point-splash-radius', type=int, default=0,
                           help=f'''
                           The radius (of square shape) around extraction point that is held in place while fluid is transferred (added or removed) from the extraction point.
                           Default is {self.default_extraction_point_splash_radius}.
                           ''')
        display_group = parser.add_argument_group("display_options")
        BoardMonitor.add_args_to(display_group, parser)
        log_group = group.add_mutually_exclusive_group()
        level_choices = ['debug', 'info', 'warning', 'error', 'critical']
        log_group.add_argument('--log-level', metavar='LEVEL',
                               choices=level_choices,
                               help=f'''
                               Configure the logging level.  Options are {conj_str([f'"{s}"' for s in level_choices])}
                               ''')
        log_group.add_argument('--log-config', metavar='FILE',
                               help='Configuration file for logging')

    @staticmethod
    def setup_logging(level: str = 'info',
                      file: Union[str, pathlib.Path] = None) -> None:
        default_format = '%(levelname)7s|%(module)s|%(message)s'

        if level is None and file is None:
            path = pathlib.Path.cwd() / ".logging"
            if path.exists():
                file = path
            else:
                level = "INFO"
        if level is not None:
            log_level = getattr(logging, level.upper())
            if (log_level < logging.INFO):
                logging.basicConfig(level=log_level,
                                    format='%(relativeCreated)6d|%(levelname)7s|%(threadName)s|%(filename)s:%(lineno)s:%(funcName)s|%(message)s')
                logging.getLogger('matplotlib').setLevel(logging.INFO)
                logging.getLogger('PIL').setLevel(logging.INFO)
            else:
                logging.basicConfig(level=log_level,
                                    format=default_format)
        else:
            assert file is not None
            logging.config.fileConfig(file,
                                      defaults = {
                                          "format": default_format
                                          })
