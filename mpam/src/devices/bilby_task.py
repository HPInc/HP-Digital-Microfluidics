from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser, \
    BooleanOptionalAction
from os import PathLike
import os
import sys
from typing import Optional, Sequence, Union, Callable

from devices import joey
from sifu.basic import assert_never, MissingOr, MISSING
from sifu.cmd_line import voltage_arg, rel_temperature_arg
from sifu.config import ConfigParam
from sifu.quant.SI import volts, deg_C
from dmf.exerciser import PlatformChoiceExerciser, Exerciser, \
    PlatformChoiceTask


class Config:
    dll_dir = ConfigParam[Optional[Union[str, PathLike]]](None)
    config_dir = ConfigParam[Optional[Union[str, PathLike]]](None)
    voltage = ConfigParam(60*volts)
    thermal_state_tolerance = ConfigParam(0*deg_C)
    remember_thermal_state_decisions = ConfigParam(True)
    use_thermal_states = ConfigParam(True)

    _defaults_set_up = False
    @classmethod
    def setup_defaults(cls) -> None:
        if not cls._defaults_set_up:
            joey.Config.setup_defaults()
            print("Setting up Config defaults for Bilby")
            cls._defaults_set_up = True


class PlatformTask(joey.PlatformTask):
    def __init__(self, name: str = "Bilby",
                 description: Optional[str] = None,
                 *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
        
    def _add_dll_dir(self, 
                     dll_dir: MissingOr[Optional[Union[str, PathLike]]] = MISSING) -> None:
        if dll_dir is MISSING:
            dll_dir = Config.dll_dir()
        if dll_dir is not None:
            to_add: str
            if isinstance(dll_dir, str):
                to_add = dll_dir
            elif isinstance(dll_dir, PathLike):
                dll_dir = os.fspath(dll_dir)
            else:
                assert_never(dll_dir)
            sys.path.append(to_add)
    
    
    def make_board(self, args: Namespace, *,            # @UnusedVariable
                   exerciser: PlatformChoiceExerciser,  # @UnusedVariable
                   ) -> joey.Board: # @UnusedVariable
        self._add_dll_dir()
        
        from devices import bilby
        
        return bilby.Board()
        
    def setup_config_defaults(self) -> None:
        super().setup_config_defaults()
        Config.setup_defaults()
        
    def _check_and_add_args_to(self, group:_ArgumentGroup, 
                               parser:ArgumentParser, 
                               *, processed:set[type[PlatformChoiceTask]], 
                               exerciser:Exerciser)->None:
        if not self._args_needed(PlatformTask, processed):
            return
        super()._check_and_add_args_to(group, parser, exerciser=exerciser, processed=processed)
        def describe_path(for_none: str) -> Callable[[Optional[Union[str, PathLike]]], str]:
            def describe(val: Optional[Union[str, PathLike]]) -> str:
                if val is None:
                    return for_none
                if isinstance(val, str):
                    s = val
                elif isinstance(val, PathLike):
                    s = os.fspath(val)
                else:
                    assert_never(val)
                return f"'{s}'"
            return describe

        Config.dll_dir.add_arg_to(group, "--dll-dir",
                                  default_desc=describe_path("to use $PYTHONPATH"),
                                  help="The directory that Wallaby.dll is found in.")
        Config.config_dir.add_arg_to(group, "--config-dir",
                                     default_desc=describe_path("the current directory"),
                                     help='''
                                       The directory that WallabyElectrodes.csv and WallabyHeaters.csv
                                       are found in.
                                       ''')
        Config.voltage.add_arg_to(group, "--voltage", type=voltage_arg, metavar="VOLTAGE", 
                                  help=f'''
                                   The voltage to set.  A value of 0V disables
                                   the high voltage.  Any other value enables it.
                                   ''')
        Config.thermal_state_tolerance.add_arg_to(group, "--thermal-state-tolerance", 
                                                  type=rel_temperature_arg, metavar="TEMP", 
                                  help=f'''
                                   When choosing a thermal state to use, the allowed tolerance
                                   to use without prompting the user for confirmation.
                                   ''')
        Config.remember_thermal_state_decisions.add_arg_to(group, "--remember-thermal-state-decisions",
                                                           action=BooleanOptionalAction,
                                  help=f'''
                                   Whether to remember (and not prompt again for) the choice of
                                   a thermal state when asking for a target temperature for a heater.
                                   ''')
        Config.use_thermal_states.add_arg_to(group, "--thermal-states", action=BooleanOptionalAction,
                                             help=f'''
                                             Whether to use thermal states (if the board has them).
                                             ''')

        

