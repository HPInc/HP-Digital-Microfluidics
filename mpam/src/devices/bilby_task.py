from __future__ import annotations
from devices import joey
from typing import Optional, Sequence, Union, Callable
from argparse import Namespace, _ArgumentGroup, ArgumentParser
from mpam.exerciser import PlatformChoiceExerciser, Exerciser
from quantities.SI import volts
from mpam.cmd_line import voltage_arg
from erk.basic import assert_never
from erk.config import ConfigParam
from os import PathLike
import os
import sys

class Config:
    dll_dir = ConfigParam[Optional[Union[str, PathLike]]](None)
    config_dir = ConfigParam[Optional[Union[str, PathLike]]](None)
    voltage = ConfigParam(60*volts)

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
    
    
    def make_board(self, args: Namespace, *, 
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                   ) -> joey.Board: # @UnusedVariable
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
        
        from devices import bilby
        
        return bilby.Board()
        
    def setup_config_defaults(self) -> None:
        super().setup_config_defaults()
        Config.setup_defaults()

    def add_args_to(self,
                    group: _ArgumentGroup, 
                    parser: ArgumentParser,
                    *,
                    exerciser: Exerciser) -> None:
        super().add_args_to(group, parser, exerciser=exerciser)
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
        

