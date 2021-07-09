from __future__ import annotations

from argparse import Namespace
from typing import Sequence

from mpam.exerciser import Exerciser
from mpam.exerciser_tasks import Dispense, Absorb, DisplayOnly, WalkPath, Mix,\
    Dilute
from quantities.SI import ms
from quantities.dimensions import Time
from devices import joey
from mpam.device import Board


class JoeyExerciser(Exerciser):
    def __init__(self, name: str = "Joey") -> None:
        super().__init__(description=f"Put the {name} board through its paces")
        self.add_task(Dispense())
        self.add_task(Absorb())      
        self.add_task(DisplayOnly())
        self.add_task(WalkPath())
        self.add_task(Mix())
        self.add_task(Dilute())
        
        
    def make_board(self, args:Namespace)->Board:  # @UnusedVariable
        return joey.Board()
    
    def available_wells(self)->Sequence[int]:
        return [0,1,2,3,4,5,6,7]

if __name__ == '__main__':
    Time.default_units(ms)
    exerciser = JoeyExerciser()
    exerciser.parse_args_and_run()





