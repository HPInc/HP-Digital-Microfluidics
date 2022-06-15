from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser
from typing import Sequence

from devices import opendrop
from mpam.device import Board
from mpam.exerciser import Exerciser
from mpam.exerciser_tasks import Dispense, Absorb, DisplayOnly, WalkPath, Mix, \
    Dilute

class OpenDropExerciser(Exerciser):
    def __init__(self, name: str = "OpenDrop") -> None:
        super().__init__(description=f"Put the {name} board through its paces")
        self.add_task(Dispense())
        self.add_task(Absorb())      
        self.add_task(DisplayOnly())
        self.add_task(WalkPath())
        self.add_task(Mix())
        self.add_task(Dilute())
        
    def add_device_specific_common_args(self, 
                                        group: _ArgumentGroup, 
                                        parser: ArgumentParser) -> None:
        super().add_device_specific_common_args(group, parser)
        group.add_argument('-p', '--port',
                           help='''
                           The communication port (e.g., COM5) to use to talk to the board.
                           By default, only the display is run
                           ''')
        
        
    def make_board(self, args:Namespace)->Board:  # @UnusedVariable
        return opendrop.Board(dev=args.port)
    
    def available_wells(self)->Sequence[int]:
        return [0,1,2,3,4,5,6,7]

if __name__ == '__main__':
    exerciser = OpenDropExerciser()
    exerciser.parse_args_and_run()





