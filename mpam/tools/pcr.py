from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser
from typing import Sequence

from devices import joey
from erk.stringutils import map_str
from mpam.device import Board, System, Pad, Well, ExtractionPoint
from mpam.exerciser import Exerciser, Task
from mpam.mixing import mixing_sequences
from mpam.paths import Path, Schedulable
from mpam.types import Reagent, schedule, Liquid, Dir
from quantities.SI import ms, second, seconds
from quantities.dimensions import Time
from quantities.temperature import abs_C
from mpam.thermocycle import ThermocyclePhase, ThermocycleProcessType
from mpam.processes import PlacedMixSequence
from mpam.dilution import dilution_sequences
from erk.basic import not_None
from mpam.drop import Drop

class PCRTask(Task):
    board: joey.Board
    tc_phases: Sequence[ThermocyclePhase]
    tc_cycles: int
    full_tc: ThermocycleProcessType

    shuttles: int

    def setup(self, board: joey.Board, *,
              args: Namespace) -> None:
        
        self.board = board
        
        self.tc_cycles = args.cycles
        self.shuttles = args.shuttles
        
        self.tc_phases = (ThermocyclePhase("denaturation", 95*abs_C, 1*second),
                          ThermocyclePhase("annealing", 64*abs_C, 1*second),
                          ThermocyclePhase("elongation", 80*abs_C, 3*seconds)) 
        
        self.full_tc = board.thermocycler.as_process(phases=self.tc_phases, 
                                                     channels=tuple(range(16)), 
                                                     n_iterations=self.tc_cycles)
      
class Prepare(PCRTask):
    # board: joey.Board
    park_R1: Pad
    park_R3: Sequence[Pad]
    park_R4: Sequence[Pad]
    
    mix3: Sequence[PlacedMixSequence]
    dilution: PlacedMixSequence
    
    # tc_phases: Sequence[ThermocyclePhase]
    # tc_cycles: int
    # full_tc: ThermocycleProcessType
    
    # shuttles: int
    
    pmo: Reagent
    mm: Reagent
    bd: Reagent
    primer: Reagent

    pmo_ep: ExtractionPoint
    mm_well: Well
    bd_well: Well
    primer_well: Well
    
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
        
    def parked_drop(self, pad: Pad) -> Drop:
        return not_None(pad.drop)

    def parked_R1(self) -> Drop:
        return self.parked_drop(self.park_R1)
    def parked_R3(self, i: int) -> Drop:
        return self.parked_drop(self.park_R3[i])
    def parked_R4(self, i: int) -> Drop:
        return self.parked_drop(self.park_R4[i])
    
    def setup(self, board: joey.Board, *,
              args: Namespace) -> None:
        
        super().setup(board, args=args)
        
        self.park_R1 = board.pad_at(18, 10)
        self.park_R3 = (board.pad_at(0, 10), board.pad_at(2, 10), board.pad_at(4,10),
                        board.pad_at(0, 8), board.pad_at(2, 8))
        self.park_R4 = (board.pad_at(18,8), board.pad_at(16,8))
        
        self.dilution = dilution_sequences.lookup_placed(8, full=True,
                                                         lower_left=board.pad_at(5,2),
                                                         rows=5, cols=9)
        self.mix3 = tuple(mixing_sequences.lookup_placed(3, full=True,
                                                         lower_left=board.pad_at(1+3*i,1),
                                                         rows=5, cols=1)
                            for i in range(6))
      
        drops = board.drop_size.as_unit("drops", singular="drop")
        
        self.pmo = Reagent.find("Pre-Mixed Oligos_i")
        mm = self.mm = Reagent.find("Master Mix")
        bd = self.bd = Reagent.find("Dilution Buffer")
        primer = self.primer = Reagent("Primer_i")

        self.pmo_ep = board.extraction_points[1]
        
        self.mm_well = board.wells[5]
        self.mm_well.contains(Liquid(mm, 17*drops))
         
        self.bd_well = board.wells[6]
        self.bd_well.contains(Liquid(bd, 14*drops))
        
        self.primer_well = board.wells[7]
        self.primer_well.contains(Liquid(primer, 16*drops))



    def initial_mix_and_tc(self) -> Drop:
        thermocycler = self.board.thermocycler
    
        r1 = Reagent.find("R1")
        mix2 = mixing_sequences.lookup(2, full=True).placed(self.pmo_ep.pad)
        tc2 = thermocycler.as_process(phases=self.tc_phases, 
                                      channels=(12,13), 
                                      n_iterations=self.tc_cycles)
    
        p1 = Path.teleport_into(self.pmo_ep, reagent = self.pmo) \
                .start(mix2.as_process(n_shuttles=self.shuttles, result=r1)) \
                .to_pad(tc2.pads(1)[0]) \
                .start(tc2) \
                .to_pad(self.park_R1)
                
    
        p2 = Path.dispense_from(self.mm_well) \
                .to_pad(mix2.pads[1]) \
                .join() \
                .to_pad(tc2.pads(1)[1]) \
                .join()
                
        drops = Path.run_paths((p1,p2), system=self.board.in_system())
        return drops[1]
    
    def dilute_1(self, r1_drop: Drop) -> Sequence[Drop]:
        r3 = Reagent.find("R3")
        d_mix = self.dilution
        
        r1_pad = d_mix.lead_drop_pad
        paths: list[Schedulable] = [(r1_drop, Path.to_pad(r1_pad)
                                                .start(d_mix.as_process(result=r3,
                                                                        n_shuttles=self.shuttles)))]
        for p in sorted(d_mix.secondary_pads, key=lambda p: p.location.coords):
            path = Path.dispense_from(self.bd_well)
            if p.row == r1_pad.row and p.column < r1_pad.column:
                path = path.to_row(r1_pad.row-2) \
                            .to_col(p.column) \
                            .to_row(p.row)
            else:
                path = path.to_pad(p, row_first=False)
            paths.append(path.join())
            
        # paths.extend(Path.dispense_from(self.bd_well)
                            # .to_pad((p.column, p.row+2))
                            # .to_pad(p)
                        # for p in d_mix.secondary_pads)
        drops = sorted(Path.run_paths(paths, system=self.board.in_system()),
                       key=lambda d: d.pad.location.coords)
        
        n_parked = 2
        parking = [(drops[i], Path.to_pad(self.park_R3[i], row_first=False))
                    for i in range(n_parked)]
        Path.run_paths(parking, system=self.board.in_system())
        return drops[n_parked:]
    
    def mix_3(self, drops: Sequence[Drop]) -> Sequence[Drop]:
        paths = list[Schedulable]()
        
        def bottom_first(d: Drop) -> tuple[int, int]:
            x,y = d.pad.location.coords
            return y,x
        
        r4 = Reagent.find("R4")

        for i,d in enumerate(sorted(drops, key=bottom_first)):
            mix = self.mix3[i]
            pads = mix.pads
            print(pads)
            d_path = Path.to_pad(pads[0], row_first=False) \
                                .start(mix.as_process(result=r4,
                                                      n_shuttles=self.shuttles))
            primer_path = Path.dispense_from(self.primer_well) \
                                .to_pad(pads[1]) \
                                .join()
            # mm_path = Path.dispense_from(self.mm_well)\
                        # .walk(Dir.LEFT, steps = 4) \
                        # .to_pad(pads[2])
            paths.extend(((d,d_path), primer_path))
        for i in range(len(drops)):
            if i > 3:
                i = 9-i
            mix = self.mix3[i]
            pads = mix.pads
            mm_path = Path.dispense_from(self.mm_well)\
                        .walk(Dir.LEFT, steps = 4) \
                        .to_pad(pads[2]) \
                        .join()
            paths.append(mm_path)
        return Path.run_paths(paths, system=self.board.in_system())
        
    def run(self, board: Board, system: System, args: Namespace) -> None:
        assert isinstance(board, joey.Board)
        # speedup: int = args.speed_up
        # cycles: int = args.cycles
        # shuttles: int = args.shuttles
        
        self.setup(board, args = args)
        r1_drop = self.initial_mix_and_tc()
        
        # Path.run_paths([(parked_r1_drop, Path.to_pad(self.park_R1))], system=system)
        
        diluted = sorted(self.dilute_1(r1_drop), key=lambda d: d.pad.location.coords)
        print(f"diluted: {map_str(diluted)}")

        mixed = self.mix_3(diluted) 
        print(mixed)
        

        


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





