from __future__ import annotations

from argparse import Namespace, ArgumentParser, _ArgumentGroup

from mpam.device import System, Board
from mpam.exerciser import Task, Exerciser
from devices import joey
from typing import Sequence


class DoIt(Task):
    def __init__(self) -> None:
        super().__init__(name="doit",
                         description="Do the thing")
        
    def add_args_to(self, group: _ArgumentGroup,
                    parser:ArgumentParser, *, exerciser:Exerciser)->None: # @UnusedVariable
        group.add_argument("name", help="Your name")
        group.add_argument("--year", type=int, metavar="INT", help="Your birth year")
        
    def run(self, board:Board, system:System, args:Namespace)->None: # @UnusedVariable
        name = args.name
        year = args.year
        print(f"Hello, {name}")
        if year is not None:
            print(f"You were born in {year}")
            
class Prog(Exerciser):
    def __init__(self) -> None:
        super().__init__(task=DoIt())
        
    def make_board(self, args:Namespace)->Board:  # @UnusedVariable
        return joey.Board()

    def available_wells(self)->Sequence[int]:
        return range(8)
        
exerciser = Prog()
exerciser.parse_args_and_run()