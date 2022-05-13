from __future__ import annotations
from pcr import PCRDriver
from mpam.pipettor import Pipettor
from typing import Optional
from argparse import Namespace, _ArgumentGroup, ArgumentParser
from devices.bilby import Board
from devices.opentrons import OT2
from devices import bilby
from quantities.dimensions import Time, Volume, Voltage
from quantities.SI import ms, uL, V
from mpam.exerciser import voltage_arg
class BilbyPCRDriver(PCRDriver):
    def __init__(self) -> None:
        super().__init__()

    def make_board(self, args:Namespace)->Board:  # @UnusedVariable
        pipettor: Optional[Pipettor] = None
        if args.ot_ip is not None:
            assert args.ot_config is not None, f"Opentrons IP address given, but no config file"
            pipettor = OT2(robot_ip_addr = args.ot_ip,
                           config = args.ot_config,
                           reagents = args.ot_reagents)
        voltage: Optional[Voltage] = args.voltage
        assert voltage is not None
        if voltage == 0:
            voltage = None
        return bilby.Board(dll_dir=args.dll_dir,
                           config_dir=args.config_dir,
                           pipettor = pipettor,
                           voltage = voltage)
    
    def add_device_specific_common_args(self, 
                                        group: _ArgumentGroup, 
                                        parser: ArgumentParser  # @UnusedVariable
                                        ) -> None:
        super().add_device_specific_common_args(group, parser)
        group.add_argument("--dll-dir",
                           help='''
                           The directory that Wallaby.dll is found in.  Defaults to searching.
                           ''')
        group.add_argument("--config-dir",
                           help='''
                           The directory that WallabyElectrodes.csv and WallabyHeaters.csv
                           are found in.  Defaults to the current directory.
                           ''')
        default_voltage = 60*V
        group.add_argument("--voltage", type=voltage_arg, metavar="VOLTAGE", default=default_voltage,
                           help=f'''
                           The voltage to set.  A value of 0V disables
                           the high voltage.  Any other value enables it.
                           The defaults is {default_voltage}.
                           ''')
    

if __name__ == '__main__':
    Time.default_units = ms
    Volume.default_units = uL
    exerciser = BilbyPCRDriver()
    exerciser.parse_args_and_run()





