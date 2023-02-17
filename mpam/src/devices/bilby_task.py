from __future__ import annotations
from devices import joey
from typing import Optional, Sequence
from argparse import Namespace, _ArgumentGroup, ArgumentParser
from mpam.exerciser import PlatformChoiceExerciser, Exerciser
from quantities.dimensions import Voltage
from mpam.pipettor import Pipettor
from quantities.SI import volts
from mpam.cmd_line import voltage_arg
from devices.joey import HeaterType

class PlatformTask(joey.PlatformTask):
    def __init__(self, name: str = "Bilby",
                 description: Optional[str] = None,
                 *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
    
    
    def make_board(self, args: Namespace, *, 
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                   pipettor: Pipettor) -> joey.Board: # @UnusedVariable
        from devices import bilby
        voltage: Optional[Voltage] = args.voltage
        assert voltage is not None
        if voltage == 0:
            voltage = None
        return bilby.Board(heater_type = HeaterType.from_name(args.heaters),
                           holes=args.holes, default_holes=args.default_holes,
                           pipettor=pipettor,
                           dll_dir=args.dll_dir, config_dir=args.config_dir,
                           off_on_delay=args.off_on_delay,
                           voltage=voltage,
                           extraction_point_splash_radius=args.extraction_point_splash_radius)
        
    def add_args_to(self,
                    group: _ArgumentGroup, 
                    parser: ArgumentParser,
                    *,
                    exerciser: Exerciser) -> None:
        super().add_args_to(group, parser, exerciser=exerciser)
        group.add_argument("--dll-dir",
                           help='''
                           The directory that Wallaby.dll is found in.  Defaults to searching.
                           ''')
        group.add_argument("--config-dir",
                           help='''
                           The directory that WallabyElectrodes.csv and WallabyHeaters.csv
                           are found in.  Defaults to the current directory.
                           ''')
        default_voltage = 60*volts
        group.add_argument("--voltage", type=voltage_arg, metavar="VOLTAGE", default=default_voltage,
                           help=f'''
                           The voltage to set.  A value of 0V disables
                           the high voltage.  Any other value enables it.
                           The defaults is {default_voltage}.
                           ''')
        

