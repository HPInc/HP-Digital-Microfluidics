from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser

from typing import Sequence, Optional

from devices import joey
from devices.opentrons import OT2
from mpam.device import Board, System

from mpam.exerciser import Exerciser, Task
from mpam.paths import Path
from mpam.pipettor import Pipettor
from quantities.SI import ms, uL
from quantities.dimensions import Time, Volume


from mpam.types import schedule, Reagent
        

class Test(Task):
    def __init__(self) -> None:
        super().__init__(name="test", 
                         description="Test Extraction Points")
        
    # def add_args_to(self, parser:ArgumentParser, *, 
    #                 exerciser:Exerciser)->None:  # @UnusedVariable
    #     ...
    
    def run(self, board:Board, 
            system:System, # @UnusedVariable
            args:Namespace) -> None: # @UnusedVariable
        assert isinstance(board, joey.Board)
        
        reagent = Reagent.find(args.reagent)
        
        ep = board.extraction_points[0]
        
        path = Path.teleport_into(ep, reagent=reagent)
        schedule(path)
        
     


class Driver(Exerciser):
    def __init__(self) -> None:
        super().__init__(description=f"Mockup of PCR tasks on Joey board")
        self.add_task(Test())

    def make_board(self, args:Namespace)->Board:  # @UnusedVariable
        pipettor: Optional[Pipettor] = None
        if args.ot_ip is not None:
            assert args.ot_config is not None, f"Opentrons IP address given, but no config file"
            pipettor = OT2(robot_ip_addr = args.ot_ip,
                           config = args.ot_config,
                           reagents = args.ot_reagents,
                           board_def = args.ot_joey_labware)
        return joey.Board(pipettor = pipettor)
    
    def available_wells(self)->Sequence[int]:
        return range(8)
    
    def add_device_specific_common_args(self, 
                                        group: _ArgumentGroup, 
                                        parser: ArgumentParser  # @UnusedVariable
                                        ) -> None:
        default_reagent = "pretend"
        group.add_argument('--reagent', choices=['pretend', 'green'], default=default_reagent,
                           help =f'''
                                  The reagent to use.  Default is {default_reagent}.
                                  ''')
        group.add_argument('-ps', '--pipettor-speed', type=float, metavar='MULT',
                           help=f'''
                                 A speed-up factor for dummy pipettor operations.
                                 ''')
        group.add_argument("-ip", "--ot-ip", metavar="IP",
                           help=f"The IP address of the Opentrons robot")
        group.add_argument("-otc", "--ot-config", metavar="FILE",
                           help=f"The config file for the the Opentrons robot")
        group.add_argument("-otr", "--ot-reagents", metavar="FILE",
                           help=f"The reagents JSON file for the Opentrons robot")
        group.add_argument("-otjl", "--ot-joey-labware", metavar="FILE",
                           help=f"The JSON file for the Joey labware definition")
    

if __name__ == '__main__':
    Time.default_units = ms
    Volume.default_units = uL
    exerciser = Driver()
    exerciser.parse_args_and_run()





