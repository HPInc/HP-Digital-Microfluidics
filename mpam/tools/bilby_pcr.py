from __future__ import annotations
from pcr import PCRDriver
from mpam.pipettor import Pipettor
from typing import Optional
from argparse import Namespace, _ArgumentGroup, ArgumentParser
from devices.bilby import Board
from devices.opentrons import OT2
from devices import bilby
from quantities.dimensions import Time, Volume
from quantities.SI import ms, uL
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
        return bilby.Board(dll_dir=args.dll_dir,
                           config_dir=args.config_dir,
                           pipettor = pipettor)
    
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
    

if __name__ == '__main__':
    Time.default_units = ms
    Volume.default_units = uL
    exerciser = BilbyPCRDriver()
    exerciser.parse_args_and_run()





