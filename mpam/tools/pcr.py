from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser
from typing import Sequence

from devices import joey
from erk.stringutils import map_str
from mpam.device import Board, System
from mpam.exerciser import Exerciser, Task
from mpam.mixing import Mix2
from mpam.paths import Path
from mpam.types import Reagent, schedule, Liquid, Dir
from quantities.SI import ms
from quantities.dimensions import Time


class Prepare(Task):
    def __init__(self) -> None:
        super().__init__(name="prepare", 
                         description="Run preparation the phase.")
        
    def add_args_to(self, parser:ArgumentParser, *, 
                    exerciser:Exerciser)->None:  # @UnusedVariable
        group = self.arg_group_in(parser)
        default_speedup = 12
        speedup_options = [12]
        group.add_argument("-su", "--speed-up", type=int, metavar="FOLD", default=default_speedup,
                           help=f'''
                            The speedup to apply (as a multiplier).  
                            Available options are {map_str(speedup_options)}.
                            Default is {default_speedup}
                           ''')
        
    def run(self, board: Board, system: System, args: Namespace)->None:
        speedup = args.speed_up
        cycles = args.cycles
        shuttles = args.shuttles
        
        drops = board.drop_size.as_unit("drops", singular="drop")
        
        pmo = Reagent("Pre-Mixed Oligos_i")

        mm = Reagent("Master Mix")
        mm_well = board.wells[5]
        mm_well.contains(Liquid(mm, 17*drops))
         
        bd = Reagent("Dilution Buffer")
        bd_well = board.wells[6]
        bd_well.contains(Liquid(bd, 14*drops))
        
        primer = Reagent("Primer_i")
        primer_well = board.wells[4]
        primer_well.contains(Liquid(primer, 16*drops))
        
        ep = board.extraction_points[1]
        
        r1 = Reagent("R1")
        
        p1 = Path.teleport_into(ep, reagent = pmo) \
                .mix(Mix2(Dir.UP), n_shuttles=shuttles, result=r1, fully_mix=True) \
                .to_row(4) \
                .to_col(15)

        p2 = Path.dispense_from(mm_well) \
                .to_col(13) \
                .walk(Dir.DOWN) \
                .in_mix() \
                .to_row(6) \
                .to_col(15)

        
        with system.batched():
            schedule(p1)
            schedule(p2)
        


class PCRDriver(Exerciser):
    def __init__(self) -> None:
        super().__init__(description=f"Mockup of PCR tasks on Joey board")
        self.add_task(Prepare())

    def make_board(self, args:Namespace)->Board:  # @UnusedVariable
        return joey.Board()
    
    def available_wells(self)->Sequence[int]:
        return range(8)
    
    def add_device_specific_common_args(self, 
                                        group: _ArgumentGroup, 
                                        parser: ArgumentParser  # @UnusedVariable
                                        ) -> None:
        default_cycles = 4
        group.add_argument('--cycles', type=int, metavar='INT', default=default_cycles,
                           help=f'''
                                 The number of times to repeat each thermocycle.  
                                 Default is {default_cycles}.
                                 ''')
        default_shuttles = 0
        group.add_argument('--shuttles', type=int, metavar='INT', default=default_shuttles,
                           help=f'''
                                 The number of extra shuttles to perform during mixing and diluting.  
                                 Default is {default_shuttles}.
                                 ''')
    

if __name__ == '__main__':
    Time.default_units(ms)
    exerciser = PCRDriver()
    exerciser.parse_args_and_run()





