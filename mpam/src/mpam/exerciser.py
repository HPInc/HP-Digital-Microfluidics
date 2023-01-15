from __future__ import annotations

from abc import ABC, abstractmethod
from argparse import Namespace, ArgumentParser, \
    _SubParsersAction, _ArgumentGroup
import logging.config
import pathlib
from threading import Event
from typing import Final, Union, Optional, Sequence, Any, Callable, \
    NoReturn

from matplotlib.gridspec import SubplotSpec

from erk.stringutils import conj_str
from mpam.device import Board, System
from mpam.monitor import BoardMonitor
from mpam.types import PathOrStr, logging_levels, logging_formats, LoggingSpec,\
    LoggingLevel
from quantities.SI import ms, minutes, hr, days, uL, secs, \
    volts, deg_C
from quantities.core import set_default_units, UnitExpr
from quantities.dimensions import Time
from mpam.pipettor import Pipettor
from erk.basic import ValOrFn
from importlib import import_module
from mpam.cmd_line import time_arg, units_arg, logging_spec_arg, ip_addr_arg,\
    ip_subnet_arg


# import logging
logger = logging.getLogger(__name__)

    

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

    def add_args_to(self, group: _ArgumentGroup, # @UnusedVariable
                    parser: ArgumentParser, # @UnusedVariable
                    *, exerciser: Exerciser) -> None:  # @UnusedVariable
        ...

    def arg_group_in(self, parser: ArgumentParser,
                     name: str) -> _ArgumentGroup:
        return parser.add_argument_group(name)

    def control_setup(self, monitor: BoardMonitor, spec: SubplotSpec, exerciser: Exerciser) -> Any:
        return exerciser.control_setup(monitor, spec)
    
    def available_wells(self, exerciser: Exerciser) -> Sequence[int]:
        return exerciser.available_wells()

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
            subparsers = self.parser.add_subparsers(help="Tasks", dest='task_name', required=True, 
                                                    metavar=self._task_metavar())
        self.subparsers = subparsers
        
    def _task_metavar(self) -> str:
        return "TASK"

    @abstractmethod
    def make_board(self, args: Namespace) -> Board: ...  # @UnusedVariable

    @abstractmethod
    def available_wells(self) -> Sequence[int]: ...

    def control_setup(self, monitor: BoardMonitor, spec: SubplotSpec) -> Any: # @UnusedVariable
        return None
    
    def setup_task(self, task: Task, *,
                   parser: ArgumentParser,
                   group_name: Optional[str] = None) -> None:
        if group_name is None:
            group_name = "task-specific options"
        group = task.arg_group_in(parser, group_name)

        # We set default units first so that default values for help and errors
        # will be printed correctly by parse_args()
        set_default_units(ms, uL, deg_C, volts)
        
        task.add_args_to(group, parser, exerciser=self)
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
        system = System(board=board, 
                        local_ip = args.local_ip,
                        subnet = args.local_subnet,
                        subnet_mask = args.local_subnet_mask
                        )

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
            macro_files: Optional[list[str]] = args.macro_file
            system.run_monitored(lambda _: do_run(),
                                 min_time=args.min_time,
                                 max_time=args.max_time,
                                 update_interval=args.update_interval,
                                 control_setup = make_controls,
                                 macro_file_names = macro_files,
                                 thread_name = f"Monitored {task.name}",
                                 cmd_line_args = args)

    def parse_args(self,
                   args: Optional[Sequence[str]]=None,
                   namespace: Optional[Namespace]=None) -> tuple[Task, Namespace]:
        ns = self.parser.parse_args(args=args, namespace=namespace)
        Exerciser.setup_logging(levels=ns.log_level, file=ns.log_config)

        task: Task = ns.task
        return task, ns
    
    def parse_args_and_run(self,
                           args: Optional[Sequence[str]]=None,
                           namespace: Optional[Namespace]=None) -> None:
        task, ns = self.parse_args(args=args, namespace=namespace)
        if ns.trace_blobs:
            Board.trace_blobs = True
        default_units: Optional[Sequence[Sequence[UnitExpr]]] = ns.units
        if default_units is not None:
            set_default_units(*(u for us in default_units for u in us))
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
        group.add_argument('--paused', action='store_false', dest='start_clock',
                           help='''
                           Don't start the clock automatically. Note that operations that are not gated
                           by the clock may still run.
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
        group.add_argument('--macro-file', action='append',
                           # type=FileType(),
                           metavar='FILE',
                           help='A file containing DMF macro definitions.')
        group.add_argument('-ep-rad', '--extraction-point-splash-radius', type=int, metavar="PADS",
                           default=self.default_extraction_point_splash_radius,
                           help=f'''
                           The radius (of square shape) around extraction point that is held in place while fluid is transferred (added or removed) from the extraction point.
                           Default is {self.default_extraction_point_splash_radius}.
                           ''')
        group.add_argument('--local-ip', metavar="IP-ADDR", type=ip_addr_arg,
                           help=f'''
                           The IP address to use as the local IP address for listeners as a dotted
                           quad ("x.x.x.x").  
                           ''') 
        group.add_argument('--local-subnet', metavar="IP-ADDR", type=ip_subnet_arg,
                           help=f'''
                           The local subnet to match IP addresses against to select an IP address
                           for listeners on machines with more than one IP address.  The selected
                           address must match based on --local-subnet-mask.  If fewer than four components
                           are provided, trailing zeroes are assumed.
                           ''') 
        group.add_argument('--local-subnet-mask', metavar="IP-ADDR", type=ip_addr_arg,
                           help=f'''
                           The subnet mask to use for the local subnet for --local-subnet as a dotted
                           quad ("x.x.x.x").  If not provided, is the same length as --subnet.  (I.e.,
                           if --subnet is "192.168", the default will be "255.255.0.0", while if --subnet
                           is "192.168.0", the default will be "255.255.255.0".)
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
        debug_group = parser.add_argument_group("debugging options")
        debug_group.add_argument("--trace-blobs", action="store_true",
                                 help=f"Trace blobs.")
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
                      file: Optional[PathOrStr] = None,
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
                
        default_imports = ("matplotlib", "PIL", "aiohttp", "urllib3.connectionpool")
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
        # logger.info(f"Default logging level: {base_level.desc}")
        
        for name,level in imports.items():
            # logger.info(f"Setting logging level for {name} to {level.desc}")
            logging.getLogger(name).setLevel(level.desc)
            
PCTaskDesc = Union[str,ValOrFn['PlatformChoiceTask']]

class BadPlatformDescError(RuntimeError):
    desc: Final[str]
    error: Final[str]

    def __init__(self, desc: str, error: str) -> None:
        super(f"Platform description '{desc}' {error}") 
        self.desc = desc
        self.error = error

class PlatformChoiceTask(Task):
    
    def __init__(self, name: str, description: Optional[str] = None, *,
                 aliases: Optional[Sequence[str]]=None) -> None:
        if description is None:
            description = f"Run on the {name} platform"
        if aliases is None:
            lc_name = name.lower()
            if lc_name != name:
                aliases = (name.lower(),)
        super().__init__(name, description, aliases=aliases)
        
    @abstractmethod
    def make_board(self, args: Namespace, *, # @UnusedVariable
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                   pipettor: Pipettor) -> Board: # @UnusedVariable
        ...
        
    # available_wells() is implemented in Task, but we override it to make it
    # abstract here so that subclasses have to give the right answer for their
    # platform.
    @abstractmethod
    def available_wells(self, exerciser: Exerciser) -> Sequence[int]: # @UnusedVariable
        ...
        
    def run(self, board: Board, system: System, args: Namespace) -> NoReturn: # @UnusedVariable
        assert False, f"PlatformChoiceTask.run() should never be called: {self}"
        
    def add_args_to(self, group: _ArgumentGroup, # @UnusedVariable
                    parser:ArgumentParser, # @UnusedVariable
                    *, 
                    exerciser:Exerciser)->None: # @UnusedVariable
        group.add_argument('-ood','--off-on-delay', type=time_arg, metavar='TIME', 
                           default=self.default_off_on_delay(),
                           help=f'''
                            The amount of time to wait between turning pads off
                            and turning pads on in a clock tick.  0ms is no
                            delay.  Negative values means pads are turned on
                            before pads are turned off. Default is
                            {self.fmt_time(self.default_off_on_delay())}.
                            ''')
        
    def default_off_on_delay(self) -> Time:
        return 0*ms
    
    @classmethod
    def fmt_time(cls, t: Time) -> str:
        return Exerciser.fmt_time(t)
    
    @classmethod
    def from_desc(cls, desc: PCTaskDesc) -> PlatformChoiceTask:
        if isinstance(desc, str):
            def bad_spec(msg: str) -> NoReturn:
                assert isinstance(desc, str)
                raise BadPlatformDescError(desc, msg)
            
            cpts = desc.split(".")
            if len(cpts) < 2:
                bad_spec("doesn't specify a module")
            name = cpts[-1]
            module_name = '.'.join(cpts[0:-1])
            try:
                module = import_module(module_name)
                val = getattr(module, name)
            except ModuleNotFoundError as ex:
                bad_spec(f"requires '{ex.name}' module")
            if isinstance(val, PlatformChoiceTask):
                desc = val
            else:
                try:
                    pp = val()
                    if isinstance(pp, PlatformChoiceTask):
                        desc = pp
                    else:
                        bad_spec("doesn't return a PlatformChoiceTask")
                except TypeError:
                    bad_spec("neither a PlatformChoiceTask nor callable")
        if not isinstance(desc, PlatformChoiceTask):
            desc = desc()
        return desc
        
        
class PipettorConfig(ABC):
    name: Final[str]
    aliases: Final[tuple[str, ...]]
    
    @property
    def names(self) -> str:
        name = f'"{self.name}"'
        aliases = ", ".join(f'"{a}"' for a in self.aliases)
        return f"{name} ({aliases})" if aliases else name
    
    def __init__(self, name: str, *,
                 aliases: Sequence[str] = ()) -> None:
        self.name = name
        self.aliases = tuple(sorted(aliases))
        
    def add_args_to(self, group: _ArgumentGroup) -> None: # @UnusedVariable
        ...
    
    @abstractmethod    
    def create(self, args: Namespace) -> Pipettor: # @UnusedVariable
        ...
        
class PlatformChoiceExerciser(Exerciser):
    task: Final[Task]
    pipettors: Final[tuple[PipettorConfig, ...]]
    default_pipettor: Final[PipettorConfig]
    
    def __init__(self, description: Optional[str] = None, *,
                 task: Task,
                 platforms: Sequence[PCTaskDesc],
                 pipettors: Sequence[ValOrFn[PipettorConfig]] = (),
                 default_pipettor: Optional[ValOrFn[PipettorConfig]] = None,
                 ) -> None:
        if description is None:
            description = f"Run the {task.name} task"
        super().__init__(description)
        self.task = task
        
        from devices import dummy_pipettor, manual_pipettor
        dp = dummy_pipettor.PipettorConfig()
        mp = manual_pipettor.PipettorConfig()
        if default_pipettor is None:
            default_pipettor = dp
        elif not isinstance(default_pipettor, PipettorConfig):
            default_pipettor = default_pipettor()
        self.default_pipettor = default_pipettor
        plist = [p if isinstance(p, PipettorConfig) else p() for p in pipettors]
        if dp not in plist:
            plist.append(dp)
        if mp not in plist:
            plist.append(mp)
        plist.sort(key=lambda p:p.name)
        self.pipettors = tuple(plist)
        
        for p in platforms:
            try:
                platform = PlatformChoiceTask.from_desc(p)
            except BadPlatformDescError as ex:
                logger.warn(f"Platform option '{ex.desc}' '{ex.error}, ignoring")
                continue

            self.add_task(platform)
            
    @classmethod
    def for_task(cls, task: Union[Task, Callable[[], Task]], 
                 description: Optional[str] = None, 
                 *,
                 platforms: Sequence[PCTaskDesc],
                 pipettors: Sequence[ValOrFn[PipettorConfig]] = (),
                 default_pipettor: Optional[ValOrFn[PipettorConfig]] = None,
                 ) -> PlatformChoiceExerciser:
        if not isinstance(task, Task):
            task = task()
        return PlatformChoiceExerciser(description, 
                                       task=task,
                                       platforms=platforms,
                                       pipettors=pipettors,
                                       default_pipettor=default_pipettor)
        
        
    
    def _task_metavar(self)->str:
        return "PLATFORM"

    def setup_task(self, task: Task, *, 
                   parser: ArgumentParser,
                   group_name: Optional[str] = None)->None: # @UnusedVariable
        tgroup = self.task.arg_group_in(parser, "task-specific options")
        self.task.add_args_to(tgroup, parser, exerciser=self)
        super().setup_task(task, parser=parser, group_name=f"{task.name} platform options")
        for pipettor in self.pipettors:
            group = parser.add_argument_group(f"{pipettor.name} pipettor options")
            pipettor.add_args_to(group)
        
    def _find_pipettor(self, name: str, args: Namespace) -> Pipettor:
        for p in self.pipettors:
            if name == p.name or name in p.aliases:
                return p.create(args)
        choices = conj_str([p.names for p in self.pipettors])
        raise ValueError(f'"{name}" is not a known pipettor name.  Choices are {choices}.')
        
    def make_board(self, args: Namespace) -> Board:
        platform: Task = args.task
        assert isinstance(platform, PlatformChoiceTask), f"Task is not a PlatformChoiceTask: {platform}"
        pipettor = self._find_pipettor(args.pipettor, args)

        return platform.make_board(args, exerciser=self, pipettor=pipettor)
        
    def add_device_specific_common_args(self, 
                                        group:_ArgumentGroup, 
                                        parser:ArgumentParser)-> None:
        super().add_device_specific_common_args(group, parser)
        pipettor_choices = []
        for p in self.pipettors:
            pipettor_choices.append(p.name)
            pipettor_choices.extend(p.aliases)
        choices_desc = conj_str([p.names for p in self.pipettors])
        group.add_argument('--pipettor', default=self.default_pipettor.name,
                           metavar="PIPETTOR",
                           choices=sorted(pipettor_choices),
                           help=f'''
                           The pipettor to use if needed.  Valid options are: {choices_desc}.  
                           The default is "{self.default_pipettor.name}".
                           ''')
        

    def available_wells(self)->NoReturn:
        assert False, f"PlatformChoiceExerciser should get available wells from the platform"
        
    # We've used the provided task (the platform) to set up the board.  What we
    # really run is the Task we squirreled away.
    def run_task(self, task: Task, args: Namespace, *, board: Board)->None: # @UnusedVariable
        super().run_task(self.task, args, board=board)
        
