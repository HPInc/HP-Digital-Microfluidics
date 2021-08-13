from __future__ import annotations

from abc import ABC, abstractmethod
from argparse import ArgumentTypeError, Namespace, ArgumentParser, \
    _SubParsersAction, _ArgumentGroup
from re import Pattern
import re
from typing import Final, Mapping, Union, Optional, Sequence

from mpam.device import Board, System
from quantities.SI import ns, us, ms, sec, minutes, hr, days, uL, mL, secs
from quantities.core import Unit
from quantities.dimensions import Time, Volume
from quantities.temperature import abs_C, abs_K, abs_F, TemperaturePoint
from quantities import temperature
from threading import Event


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

time_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)\\s*({'|'.join(time_arg_units)})")

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

temperature_arg_units: Final[Mapping[str, temperature.Unit]] = {
    "C": abs_C,
    "K": abs_K,
    "F": abs_F,
    }

temperature_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)({'|'.join(temperature_arg_units)})")

def temperature_arg(arg: str) -> TemperaturePoint:
    m = temperature_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a temperature value.  
                    Requires a number followed immediately by units, e.g. '40C' or '200F'""")
    n = float(m.group(1))
    ustr = m.group(2)
    unit = temperature_arg_units.get(ustr, None)
    if unit is None:
        raise ValueError(f"{ustr} is not a known temperature unit")
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
    
            

        
class Exerciser(ABC):
    parser: Final[ArgumentParser]
    subparsers: Final[_SubParsersAction]
    
    default_initial_delay: Time = 5*secs
    default_min_time: Time = 5*minutes
    default_update_interval: Time = 20*ms
    
    def __init__(self, description: str = "run tasks on a board") -> None:
        self.parser = ArgumentParser(description=description)
        self.subparsers = self.parser.add_subparsers(help="Tasks", dest='task_name', required=True, metavar='TASK')
        
    @abstractmethod
    def make_board(self, args: Namespace) -> Board: ...  # @UnusedVariable
    
    @abstractmethod
    def available_wells(self) -> Sequence[int]: ...
        

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

    def run_task(self, task: Task, args: Namespace, *,
                 board: Board
                 ) -> None:
        system = System(board=board)
    
        def prepare_and_run() -> None:
            system.clock.start(args.clock_speed)
            task.run(board, system, args)
    
        def do_run() -> None:
            event = Event()
            system.call_after(args.initial_delay, lambda: event.set())
            event.wait()
            prepare_and_run()
    
        if not args.use_display:
            with system:
                do_run()
        else:
            system.run_monitored(lambda _: do_run(),
                                 min_time=args.min_time,
                                 max_time=args.max_time,
                                 update_interval=args.update_interval
                                 )
            
    def parse_args(self, 
                   args: Optional[Sequence[str]]=None, 
                   namespace: Optional[Namespace]=None) -> tuple[Task, Namespace]:
        ns = self.parser.parse_args(args=args, namespace=namespace)
        task: Task = ns.task
        return task, ns
    
    def parse_args_and_run(self,
                           args: Optional[Sequence[str]]=None, 
                           namespace: Optional[Namespace]=None) -> None:
        task, ns = self.parse_args(args=args, namespace=namespace)
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
        ...
    
    def add_common_args_to(self, parser: ArgumentParser) -> None:
        group = parser.add_argument_group(title="common options")
        self.add_device_specific_common_args(group, parser)
        default_clock_interval=100*ms
        group.add_argument('-cs', '--clock-speed', type=time_arg, default=default_clock_interval, metavar='TIME',
                            help=f'''
                            The amount of time between clock ticks.  
                            Default is {default_clock_interval.in_units(ms)}.
                            ''')
        group.add_argument('--initial-delay', type=time_arg, metavar='TIME', default=self.default_initial_delay,
                            help=f'''
                            The amount of time to wait before running the task.
                            Default is {self.fmt_time(self.default_initial_delay)}.
                            ''')
        
        group.add_argument('--min-time', type=time_arg, default=self.default_min_time, metavar='TIME',
                            help=f'''
                            The minimum amount of time to leave the display up, even if the 
                            operation has finished.  Default is {self.fmt_time(self.default_min_time)}.
                            ''')
        group.add_argument('--max-time', type=time_arg, metavar='TIME',
                            help=f'''
                            The maximum amount of time to leave the display up, even if the 
                            operation hasn't finished.  Default is no limit
                            ''')
        group.add_argument('-nd', '--no-display', action='store_false', dest='use_display',
                            help=f'''
                            Run the task without the on-screen display
                            ''')
        group.add_argument('--update-interval', type=time_arg, metavar='TIME', default=self.default_update_interval,
                            help=f'''
                            The maximum amount of time between display updates.  
                            Default is {self.default_update_interval}.
                            ''')

