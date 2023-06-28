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
from mpam.device import Board, System, PowerMode, EC, ExternalComponent,\
    BoardComponent, ComponentFactory
from mpam.monitor import BoardMonitor
from mpam.types import PathOrStr, logging_levels, logging_formats, LoggingSpec,\
    LoggingLevel, OnOff
from quantities.SI import ms, minutes, hr, days, uL, secs, \
    volts, deg_C, V
from quantities.core import set_default_units, UnitExpr, UEorSeq
from quantities.dimensions import Time
from mpam.pipettor import Pipettor
from erk.basic import ValOrFn
from importlib import import_module
from mpam.cmd_line import time_arg, units_arg, logging_spec_arg, ip_addr_arg,\
    ip_subnet_arg, voltage_arg
from erk.config import ConfigParam
from mpam import device, pipettor
from functools import cache


# import logging
logger = logging.getLogger(__name__)

class Config:
    clock_interval: Final = ConfigParam[Time](100*ms)
    start_clock: Final = ConfigParam(True)
    units: Final = ConfigParam[Optional[Sequence[Sequence[UnitExpr]]]]([[uL,ms,V]])
    log_config: Final = ConfigParam[Optional[str]](None)
    log_levels: Final = ConfigParam[list[LoggingSpec]]([])
    trace_blobs: Final = ConfigParam(False)
    

class Task(ABC):
    name: Final[str]
    description: Final[str]
    aliases: Final[Sequence[str]]
    
    # default_initial_delay: Time = 0*secs
    # default_hold_display: Optional[Time] = 0*ms
    # default_min_time: Optional[Time] = 0*ms
    # default_max_time: Optional[Time] = None
    # default_update_interval: Time = 20*ms
    # default_clock_interval=100*ms    

    def __init__(self, name: str, description: str, *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        self.name = name
        self.description = description
        self.aliases = [] if aliases is None else aliases
        
    @abstractmethod
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        ...
        
    def setup_config_defaults(self) -> None:
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
    
class _DeferredSubtaskParser(ArgumentParser):
    def __init__(self, *,
                 finish: Callable[[ArgumentParser], Any], 
                 **kwargs: Any) -> None:
        self.finish = finish
        self.parser = ArgumentParser(**kwargs)
    def parse_known_args(self, args: Optional[Sequence[str]]=None, 
                         namespace: Optional[Namespace]=None) -> tuple[Namespace, list[str]]:
        self.finish(self.parser)
        return self.parser.parse_known_args(args, namespace)
    
class Exerciser(ABC):
    parser: Final[ArgumentParser]
    subparsers: Final[Optional[_SubParsersAction]]


    def __init__(self, description: Optional[str] = None, *,
                 task: Optional[Task] = None,
                 fromfile_prefix_chars: Optional[str] = '@') -> None:
        if description is None:
            description = "run tasks on a board" if task is None else task.description
        self.parser = ArgumentParser(description=description, fromfile_prefix_chars=fromfile_prefix_chars)
        subparsers: Optional[_SubParsersAction]
        if task is not None:
            self.setup_task(task, parser=self.parser)
            subparsers = None
        else:
            subparsers = self.parser.add_subparsers(help="Tasks", dest='task_name', required=True, 
                                                    parser_class=_DeferredSubtaskParser,
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
        
        task.setup_config_defaults()
        task.add_args_to(group, parser, exerciser=self)
        self.add_common_args_to(parser, task=task)
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
        def finish(parser: ArgumentParser) -> None:
            self.setup_task(task, parser=parser)
        # add_parser turns around and passes all keywords into its parser_class,
        # which can require more keywords (as _DefaultSubtaskParser does), but
        # its .pyi doesn't allow that.
        subparsers.add_parser(name, help=desc, description=desc, aliases=aliases, finish=finish) # type: ignore[call-arg]
        
        return self

    def run_task(self, task: Task, args: Namespace, *, board: Board) -> None:
        from mpam import monitor
        system = System(board=board)

        def prepare_and_run() -> None:
            interval = Config.clock_interval()
            if Config.start_clock():
                system.clock.start(interval)
            else:
                system.clock.update_interval = interval
            task.run(board, system, args)

        def do_run() -> None:
            event = Event()
            system.call_after(monitor.Config.initial_delay(), lambda: event.set())
            event.wait()
            prepare_and_run()

        def make_controls(monitor: BoardMonitor, spec: SubplotSpec) -> Any:
            return task.control_setup(monitor, spec, self)

        if not monitor.Config.use_display():
            with system:
                do_run()
            system.shutdown()
        else:
            system.run_monitored(lambda _: do_run(),
                                 control_setup = make_controls,
                                 thread_name = f"Monitored {task.name}")

    def parse_args(self,
                   args: Optional[Sequence[str]]=None,
                   namespace: Optional[Namespace]=None) -> tuple[Task, Namespace]:
        ns = self.parser.parse_args(args=args, namespace=namespace)
        Exerciser.setup_logging(levels=Config.log_levels(), file=Config.log_config())

        task: Task = ns.task
        return task, ns
    
    def parse_args_and_run(self,
                           args: Optional[Sequence[str]]=None,
                           namespace: Optional[Namespace]=None) -> None:
        task, ns = self.parse_args(args=args, namespace=namespace)
        ConfigParam.set_namespace(ns)
        if Config.trace_blobs():
            Board.trace_blobs = True
        default_units: Optional[Sequence[Sequence[UnitExpr]]] = Config.units()
        if default_units is not None:
            set_default_units(*(u for us in default_units for u in us))
        board = self.make_board(ns)
        self.run_task(task, ns, board=board)

    @classmethod
    def fmt_time(self, t: Optional[Time], *,
                 units: Optional[UEorSeq[Time]] = None,
                 on_None: str = "unspecified") -> str:
        if t is None:
            return on_None
        if units is not None:
            return str(t.in_units(units))
        return str(t.decomposed((days, hr, minutes, secs)))

    def add_device_specific_common_args(self,
                                        group: _ArgumentGroup,  # @UnusedVariable
                                        parser: ArgumentParser  # @UnusedVariable
                                        ) -> None:
        # by default, no args to add.
        ...
        

    def add_common_args_to(self, parser: ArgumentParser, *,
                           task: Task) -> None:
        group = parser.add_argument_group(title="common options")
        self.add_device_specific_common_args(group, parser)
        
        devcon = device.Config

        Config.clock_interval.add_arg_to(group, '-cs', '--clock-speed', type=time_arg, metavar='TIME',
                                          default_desc = lambda t: self.fmt_time(t, units=ms),
                                          help="The amount of time between clock ticks.")
        devcon.off_on_delay.add_arg_to(group, '-ood','--off-on-delay', 
                                       type=time_arg, metavar='TIME', 
                           help=f'''
                            The amount of time to wait between turning pads off
                            and turning pads on in a clock tick.  0ms is no
                            delay.  Negative values means pads are turned on
                            before pads are turned off. 
                            ''')
        Config.start_clock.add_arg_to(group, '--paused', action='store_false', dest='start_clock',
                                      default_desc = lambda b: f"to {'' if b else 'not '} start the clock",
                           help='''
                           Don't start the clock automatically. Note that operations that are not gated
                           by the clock may still run.
                           ''')
        devcon.extraction_point_splash_radius.add_arg_to(group, '-ep-rad', '--extraction-point-splash-radius', 
                                                         type=int, metavar="PADS",
                                                         help=f'''
                                                           The radius (of square shape) around extraction point that is held 
                                                           in place while fluid is transferred 
                                                           (added or removed) from the extraction point.
                                                           ''')
        devcon.local_ip_addr.add_arg_to(group, '--local-ip', metavar="IP-ADDR", type=ip_addr_arg,
                           help=f'''
                           The IP address to use as the local IP address for listeners as a dotted
                           quad ("x.x.x.x").  
                           ''') 
        devcon.subnet.add_arg_to(group, '--local-subnet', metavar="IP-ADDR", type=ip_subnet_arg,
                           help=f'''
                           The local subnet to match IP addresses against to select an IP address
                           for listeners on machines with more than one IP address.  The selected
                           address must match based on --local-subnet-mask.  If fewer than four components
                           are provided, trailing zeroes are assumed.
                           ''') 
        devcon.subnet_mask.add_arg_to(group, '--local-subnet-mask', metavar="IP-ADDR", type=ip_addr_arg,
                           help=f'''
                           The subnet mask to use for the local subnet for --local-subnet as a dotted
                           quad ("x.x.x.x").  If not provided, is the same length as --subnet.  (I.e.,
                           if --subnet is "192.168", the default will be "255.255.0.0", while if --subnet
                           is "192.168.0", the default will be "255.255.255.0".)
                           ''') 
        Config.units.add_arg_to(group, '--units', type=units_arg, action='append',
                                default_desc = lambda uss: ("unknown" if uss is None 
                                                            else conj_str([u for us in uss for u in us])),
                           help="""
                               A comma- or space-separated list of units to use
                               for printing.  This argument may be specified
                               multiple times.  If more than one value is
                               provided for a given dimension, the unit chosen
                               will be the largest one that's no bigger than the
                               printed value (or the smallest if none are
                               smaller). 
                               """)
        display_group = parser.add_argument_group("display options")
        BoardMonitor.add_args_to(display_group, parser)
        input_group = parser.add_argument_group("input options")
        from mpam.interpreter import DMLInterpreter
        DMLInterpreter.add_args_to(input_group, parser)
        debug_group = parser.add_argument_group("debugging options")
        Config.trace_blobs.add_arg_to(debug_group, "--trace-blobs", action="store_true",
                                      help=f"Trace blobs.")
        Config.log_config.add_arg_to(group, '--log-config', metavar='FILE',
                                       help='Configuration file for logging')
        Config.log_levels.add_arg_to(group, '--log-level', metavar='SPEC', type=logging_spec_arg, action='append',
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

BoardKwdArgs = dict[str, Any]


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
        
    # def defaults_from(self, task: Task) -> None:
    #     self.default_initial_delay = task.default_initial_delay
    #     self.default_hold_display = task.default_hold_display
    #     self.default_min_time = task.default_min_time
    #     self.default_max_time = task.default_max_time
    #     self.default_update_interval = task.default_update_interval
    #     self.default_clock_interval=task.default_clock_interval

        
    @abstractmethod
    def make_board(self, args: Namespace, *, # @UnusedVariable
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                   ) -> Board: # @UnusedVariable
        ...
        
    # available_wells() is implemented in Task, but we override it to make it
    # abstract here so that subclasses have to give the right answer for their
    # platform.
    @abstractmethod
    def available_wells(self, exerciser: Exerciser) -> Sequence[int]: # @UnusedVariable
        ...
        
    def run(self, board: Board, system: System, args: Namespace) -> NoReturn: # @UnusedVariable
        assert False, f"PlatformChoiceTask.run() should never be called: {self}"
        
    def add_args_to(self, group: _ArgumentGroup, 
                    parser:ArgumentParser, # @UnusedVariable
                    *, 
                    exerciser:Exerciser)->None: # @UnusedVariable
        self._check_and_add_args_to(group, processed=set(), parser=parser, exerciser=exerciser)
        
    def _args_needed(self, my_type: type[PlatformChoiceTask],
                     processed: set[type[PlatformChoiceTask]]) -> bool:
        if my_type in processed:
            return False
        processed.add(my_type)
        return True
        
    @abstractmethod
    def _check_and_add_args_to(self, group: _ArgumentGroup, # @UnusedVariable
                               parser:ArgumentParser, # @UnusedVariable
                               *, 
                               processed: set[type[PlatformChoiceTask]], # @UnusedVariable
                               exerciser:Exerciser                               # @UnusedVariable
                               ) -> None:
        ...
        
    @cache
    def heater_group(self, parser: ArgumentParser) -> _ArgumentGroup:
        return parser.add_argument_group("heater options")
        
    def add_heater_args_to(self, parser: ArgumentParser, *, 
                           exerciser: Exerciser) ->None : # @UnusedVariable
        group = self.heater_group(parser)
        device.Config.polling_interval.add_arg_to(group, '--polling-interval',
                                                  type=time_arg, metavar="TIME",
                                                  help="The polling interval for checking heater temperatures.")
        
    @cache
    def power_supply_group(self, parser: ArgumentParser) -> _ArgumentGroup:
        return parser.add_argument_group("power supply options")
        
    def add_power_supply_args_to(self, parser: ArgumentParser, *, 
                           exerciser: Exerciser) ->None : # @UnusedVariable
        group = self.power_supply_group(parser)
        config = device.Config
        config.ps_min_voltage.add_arg_to(group, '--ps-min-voltage', type=voltage_arg, metavar="VOLTAGE",
                                         help="The minimum voltage for the power supply.")
        config.ps_max_voltage.add_arg_to(group, '--ps-max-voltage', type=voltage_arg, metavar="VOLTAGE",
                                         help="The maximum voltage for the power supply.")
        config.ps_initial_voltage.add_arg_to(group, '--ps-initial-voltage', type=voltage_arg, metavar="VOLTAGE",
                                             help="The initial voltage for the power supply.")
        config.ps_can_toggle.add_bool_arg_to(group, '--ps-can-toggle',
                                             help="Can the power supply be turned on and off?")
        config.ps_initial_mode.add_choice_arg_to(group, PowerMode, '--ps-initial-mode',
                                                 help="The initial mode for the power supply.")
        config.ps_can_change_mode.add_bool_arg_to(group, '--ps-can-change-mode',
                                                  help="Can the power supply's mode be changed between AC and DC?")
        
        
    @cache
    def fan_group(self, parser: ArgumentParser) -> _ArgumentGroup:
        return parser.add_argument_group("fan options")
        
    def add_fan_args_to(self, parser: ArgumentParser, *, 
                        exerciser: Exerciser) ->None : # @UnusedVariable
        group = self.fan_group(parser)
        config = device.Config
        config.fan_initial_state.add_choice_arg_to(group, OnOff, '--fan-initial-state', metavar="STATE",
                                                   help="The initial state of the fan.")
        config.fan_can_toggle.add_bool_arg_to(group, '--fan-can-toggle',
                                             help="Can the fan be turned on and off?")
        
    def add_kwd_arg(self, args: Namespace, kwds: BoardKwdArgs, arg: str, *,
                    kwd: Optional[str] = None,
                    transform: Optional[Callable[[Any], Any]] = None) -> None:
        if kwd is None:
            kwd = arg
        val = getattr(args, arg)
        if transform is not None:
            val = transform(val)
        kwds[kwd] = val


    def board_kwd_args(self, args: Namespace, *,
                       announce: bool = False) -> BoardKwdArgs: # @UnusedVariable
        kwds: BoardKwdArgs = {}
        
        return kwds
    
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
        
        
# class PipettorConfig(ABC):
#     name: Final[str]
#     aliases: Final[tuple[str, ...]]
#
#     @property
#     def names(self) -> str:
#         name = f'"{self.name}"'
#         aliases = ", ".join(f'"{a}"' for a in self.aliases)
#         return f"{name} ({aliases})" if aliases else name
#
#     def __init__(self, name: str, *,
#                  aliases: Sequence[str] = ()) -> None:
#         self.name = name
#         self.aliases = tuple(sorted(aliases))
#
#     def add_args_to(self, group: _ArgumentGroup) -> None: # @UnusedVariable
#         ...
#
#     @abstractmethod    
#     def create(self) -> Pipettor: # @UnusedVariable
#         ...
        
        
class ComponentConfig(ComponentFactory[EC], ABC):
    name: Final[str]
    aliases: Final[tuple[str, ...]]
    default_component_group: Final[type[ExternalComponent]]
    
    @property
    def names(self) -> str:
        name = f'"{self.name}"'
        aliases = ", ".join(f'"{a}"' for a in self.aliases)
        return f"{name} ({aliases})" if aliases else name
    
    def __init__(self, name: str, component_class: type[EC], *,
                 aliases: Sequence[str] = (),
                 group: type[ExternalComponent] = ExternalComponent) -> None:
        self.name = name
        self.aliases = tuple(sorted(aliases))
        self.component_class: Final = component_class
        self.default_component_group = group
        
        
    def __str__(self) -> str:
        return f"<{self.name} config>"
        
    def add_args_to(self, group: _ArgumentGroup) -> None: # @UnusedVariable
        ...
        
    def component_group(self, groups: Sequence[type[ExternalComponent]] = (), *,
                        use_default: bool = True) -> type[ExternalComponent]:
        best = self.default_component_group if use_default else ExternalComponent
        me = self.component_class
        for g in groups:
            if issubclass(me, g) and issubclass(g, best): 
                best = g
        return best
    
    def for_board(self, board: Board) -> EC:
        if issubclass(self.component_class, BoardComponent):
            return self.component_class(board)  # type: ignore[unreachable]
        return self.component_class()
    
    def create(self) -> EC:
        if issubclass(self.component_class, BoardComponent):
            raise ValueError(f"{self} creates a BoardComponent and can only be created using for_board().")
        return self.component_class()
        
        
    @classmethod
    def choices(cls, configs: Sequence[ComponentConfig[EC]]) -> Sequence[str]:
        choices = []
        for c in configs:
            choices.append(c.name)
            choices.extend(c.aliases)
        choices.sort()
        return choices
    
    @classmethod
    def choices_desc(cls, configs: Sequence[ComponentConfig[EC]]) -> str:
        return conj_str([c.names for c in configs])

class PipettorConfig(ComponentConfig[Pipettor]):
    
    def __init__(self, name: str, component_class: type[Pipettor], *,
                 aliases: Sequence[str] = (),
                 group: type[ExternalComponent] = Pipettor) -> None:
        super().__init__(name, component_class, aliases=aliases, group=group)

        

class PlatformChoiceExerciser(Exerciser):
    task: Final[Task]
    pipettors: Final[tuple[PipettorConfig, ...]]
    default_pipettor: Final[PipettorConfig]
    available_components: Final[tuple[ComponentConfig, ...]]
    
    def __init__(self, description: Optional[str] = None, *,
                 task: Task,
                 platforms: Sequence[PCTaskDesc],
                 pipettors: Sequence[ValOrFn[PipettorConfig]] = (),
                 components: Sequence[ValOrFn[ComponentConfig]] = (),
                 default_pipettor: Optional[ValOrFn[PipettorConfig]] = None,
                 fromfile_prefix_chars: Optional[str] = '@'
                 ) -> None:
        if description is None:
            description = f"Run the {task.name} task"
        super().__init__(description, fromfile_prefix_chars=fromfile_prefix_chars)
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
        
        clist = [c if isinstance(c, ComponentConfig) else c() for c in components]
        clist.sort(key = lambda c:c.name)
        self.available_components = tuple(clist)
        
        for p in platforms:
            try:
                platform = PlatformChoiceTask.from_desc(p)
                # platform.defaults_from(task)
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
                 components: Sequence[ValOrFn[ComponentConfig]] = (),
                 default_pipettor: Optional[ValOrFn[PipettorConfig]] = None,
                 ) -> PlatformChoiceExerciser:
        if not isinstance(task, Task):
            task = task()
        return PlatformChoiceExerciser(description, 
                                       task=task,
                                       platforms=platforms,
                                       pipettors=pipettors,
                                       components=components,
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
        for component in self.available_components:
            group = parser.add_argument_group(f"{component.name} options")
            component.add_args_to(group)
        
        
    def make_board(self, args: Namespace) -> Board:
        platform: Task = args.task
        assert isinstance(platform, PlatformChoiceTask), f"Task is not a PlatformChoiceTask: {platform}"

        return platform.make_board(args, exerciser=self)
        
    def add_device_specific_common_args(self, 
                                        group:_ArgumentGroup, 
                                        parser:ArgumentParser)-> None:
        super().add_device_specific_common_args(group, parser)

        def find(configs: Sequence[ComponentConfig[EC]], kind: str) -> Callable[[str], ComponentConfig[EC]]:
            def doit(name: str) -> ComponentConfig[EC]:
                for c in configs:
                    if name == c.name or name in c.aliases:
                        return c
                choices = conj_str([c.names for c in configs])
                raise ValueError(f'"{name}" is not a known {kind} name.  Choices are {choices}.')
            return doit

        def find_and_create(configs: Sequence[ComponentConfig[EC]], kind: str) -> Callable[[str], EC]:
            finder = find(configs, kind)
            def doit(name: str) -> EC:
                return finder(name).create()
            return doit

        # pipettor_choices = []
        # for p in self.pipettors:
        #     pipettor_choices.append(p.name)
        #     pipettor_choices.extend(p.aliases)
        # choices_desc = conj_str([p.names for p in self.pipettors])
        # def find_pipettor(name: str) -> Pipettor:
        #     for p in self.pipettors:
        #         if name == p.name or name in p.aliases:
        #             return p.create()
        #     choices = conj_str([p.names for p in self.pipettors])
        #     raise ValueError(f'"{name}" is not a known pipettor name.  Choices are {choices}.')
        
            
        pipettor.Config.pipettor.add_arg_to(group, '--pipettor', default=self.default_pipettor.name,
                           metavar="PIPETTOR",
                           choices=PipettorConfig.choices(self.pipettors),
                           transform = find_and_create(self.pipettors, "pipettor"),
                           help=f'''
                           The pipettor to use if needed.  Valid options are: {PipettorConfig.choices_desc(self.pipettors)}.  
                           ''')
        
        # component_choices = []
        # for c in self.available_components:
        #     component_choices.append(c.name)
        #     component_choices.extend(c.aliases)
        # choices_desc = conj_str([c.names for c in self.available_components])
        
        if self.available_components:
            def default_components_desc(components: Sequence[ComponentFactory]) -> str:
                if len(components) == 0:
                    return "to have no additional components"
                else:
                    return f"to have {conj_str(components)}"
            def transform(names: Sequence[str]) -> list[ComponentFactory]:
                finder = find(self.available_components, "component")
                return [finder(name) for name in names]
            device.Config.component_factories.add_arg_to(group, '--have', metavar="COMPONENT", action='append', 
                                                         choices=ComponentConfig.choices(self.available_components),
                                                         default_desc = default_components_desc,
                                                         transform = transform,
                                                         help=f'''
                                                            A component that is present.  Valid options are: 
                                                            {ComponentConfig.choices_desc(self.available_components)}.
                                                            This argument may be specified more than once.
                                                            '''
                                                )
        

    def available_wells(self)->NoReturn:
        assert False, f"PlatformChoiceExerciser should get available wells from the platform"
        
    # We've used the provided task (the platform) to set up the board.  What we
    # really run is the Task we squirreled away.
    def run_task(self, task: Task, args: Namespace, *, board: Board)->None: # @UnusedVariable
        super().run_task(self.task, args, board=board)
        
