from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser
from typing import Sequence, Union, Optional

from devices import joey
from erk.basic import not_None
from erk.stringutils import map_str
from mpam.device import Board, System, Pad, Well, ExtractionPoint
from mpam.dilution import dilution_sequences
from mpam.drop import Drop
from mpam.exerciser import Exerciser, Task
from mpam.mixing import mixing_sequences
from mpam.paths import Path, Schedulable
from mpam.processes import PlacedMixSequence
from mpam.thermocycle import ThermocyclePhase, ThermocycleProcessType
from mpam.types import Reagent, Liquid, Dir, Color
from quantities.SI import ms, second, seconds
from quantities.dimensions import Time
from quantities.temperature import abs_C
from mpam.monitor import BoardMonitor


def right_then_up(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.pad
    x,y = loc.location.coords
    return x,y

def right_then_down(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.pad
    x,y = loc.location.coords
    return x,-y

def left_then_down(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.pad
    x,y = loc.location.coords
    return -x,-y

def up_then_right(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.pad
    x,y = loc.location.coords
    return y,x

def down_then_right(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.pad
    x,y = loc.location.coords
    return -y,x

def down_then_left(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.pad
    x,y = loc.location.coords
    return -y,-x

class PCRTask(Task):
    board: joey.Board
    monitor: Optional[BoardMonitor] 
    tc_phases: Sequence[ThermocyclePhase]
    tc_cycles: int
    full_tc: ThermocycleProcessType

    shuttles: int

    def setup(self, board: joey.Board, *,
              args: Namespace) -> None:
        
        self.board = board
        self.monitor = board.in_system().monitor
        
        self.tc_cycles = args.cycles
        self.shuttles = args.shuttles
        
        self.tc_phases = (ThermocyclePhase("denaturation", 95*abs_C, 1*second),
                          ThermocyclePhase("annealing", 64*abs_C, 1*second),
                          ThermocyclePhase("elongation", 80*abs_C, 3*seconds)) 
        
        self.full_tc = board.thermocycler.as_process(phases=self.tc_phases, 
                                                     channels=tuple(range(16)), 
                                                     n_iterations=self.tc_cycles)
        
    def reagent(self, name: str, *,
                color: Optional[Union[Color, str, tuple[float,float,float]]] = None) -> Reagent:
        r = Reagent.find(name)
        if color is not None and self.monitor is not None:
            if not isinstance(color, Color):
                color = Color.find(color)
            self.monitor.reserve_color(r, color)
        return r
      
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
    output_well: Well
    
    def __init__(self) -> None:
        super().__init__(name="prepare", 
                         description="Run the preparation phase.")
        
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
        self.park_R3 = (board.pad_at(0, 10), board.pad_at(2, 10), 
                        board.pad_at(0, 8), board.pad_at(2, 8),
                        board.pad_at(18, 10))
        self.park_R4 = (board.pad_at(18,8), board.pad_at(16,8))
        
        self.dilution = dilution_sequences.lookup_placed(8, full=True,
                                                         lower_left=board.pad_at(5,2),
                                                         rows=5, cols=9)
        self.mix3 = tuple(mixing_sequences.lookup_placed(3, full=True,
                                                         lower_left=board.pad_at(1+3*i,1),
                                                         rows=5, cols=1)
                            for i in range(6))
      
        drops = board.drop_size.as_unit("drops", singular="drop")
        
        self.pmo = self.reagent("Pre-Mixed Oligos_i")
        mm = self.mm = self.reagent("Master Mix")
        bd = self.bd = self.reagent("Dilution Buffer")
        primer = self.primer = self.reagent("Primer_i")
        
        self.pmo_ep = board.extraction_points[1]
        
        self.mm_well = board.wells[5]
        self.mm_well.contains(Liquid(mm, 17*drops))
         
        self.bd_well = board.wells[6]
        self.bd_well.contains(Liquid(bd, 14*drops))
        
        self.primer_well = board.wells[7]
        self.primer_well.contains(Liquid(primer, 16*drops))

        self.output_well = board.wells[3]

    def initial_mix_and_tc(self) -> Drop:
        thermocycler = self.board.thermocycler
    
        r1 = self.reagent("R1", color="yellow")
        
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
    
    def dilute(self, r1_drop: Drop) -> Sequence[Drop]:
        r3 = self.reagent("R3", color="darkblue")
        d_mix = self.dilution
        
        r1_pad = d_mix.lead_drop_pad
        paths: list[Schedulable] = [(r1_drop, Path.to_pad(r1_pad)
                                                .start(d_mix.as_process(result=r3,
                                                                        n_shuttles=self.shuttles)))]
        for p in sorted(d_mix.secondary_pads, key=right_then_up):
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
        return Path.run_paths(paths, system=self.board.in_system())
        
    def dilute_1(self, r1_drop: Drop) -> Sequence[Drop]:
        drops = sorted(self.dilute(r1_drop), key=right_then_up)
        n_parked = 2
        parking = [(drops[i], Path.to_pad(self.park_R3[i], row_first=False))
                    for i in range(n_parked)]
        Path.run_paths(parking, system=self.board.in_system())
        return drops[n_parked:]
    
    
    def dilute_2(self) -> Sequence[Drop]:
        r1_drop = self.parked_R1()
        Path.run_paths([(r1_drop, Path.to_col(14))], system=self.board.in_system())
        drops = sorted(self.dilute(r1_drop), key=right_then_up)
        parking = [(drops[0], Path.to_pad(self.park_R3[2], row_first=False)),
                   (drops[1], Path.to_pad(self.park_R3[3], row_first=False)),
                   (drops[-1], Path.to_col(14).to_pad(self.park_R3[4])),
                   ]
        Path.run_paths(parking, system=self.board.in_system())
        return drops[2:-1]
    
    
    def mix_3(self, drops: Sequence[Drop], *, row_first: bool=False) -> Sequence[Drop]:
        paths = list[Schedulable]()
        
        
        r4 = self.reagent("R4", color="purple")

        for i,d in enumerate(sorted(drops, key=up_then_right)):
            mix = self.mix3[i]
            pads = mix.pads
            print(pads)
            d_path = Path.to_pad(pads[0], row_first=row_first) \
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
            if i > 3 and len(drops) == 6:
                i = 9-i
            mix = self.mix3[i]
            pads = mix.pads
            mm_path = Path.dispense_from(self.mm_well)\
                        .walk(Dir.LEFT, steps = 4) \
                        .to_pad(pads[2]) \
                        .join()
            paths.append(mm_path)
        drops = Path.run_paths(paths, system=self.board.in_system())
        return drops
        
    def mix_3_1(self, drops: Sequence[Drop]) -> Sequence[Drop]:
        drops = sorted(self.mix_3(drops), key=left_then_down)
        n_parked = 2
        parking = [(drops[i], Path.to_pad(self.park_R4[i], row_first=False))
                    for i in range(n_parked)]
        Path.run_paths(parking, system=self.board.in_system())
        return drops[n_parked:]
    
    def mix_3_2(self, drops: Sequence[Drop]) -> Sequence[Drop]:
        drops = sorted(self.mix_3(drops), key=left_then_down)
        return drops
    def mix_3_3(self) -> Sequence[Drop]:
        drops = [self.parked_R3(i) for i in range(5)]
        Path.run_paths([(self.parked_R3(4), Path.to_col(14).to_row(1)),
                        (self.parked_R3(2), Path.to_col(4).to_row(1)),
                        (self.parked_R3(3), Path.to_col(6).to_row(1)),
                        (self.parked_R3(0), Path.to_row(1)),
                        (self.parked_R3(1), Path.to_row(1)),
                        ], system=self.board.in_system())
        drops = sorted(self.mix_3(drops, row_first=True), key=left_then_down)
        return drops
    
    def tc_1(self, drops: Sequence[Drop]) -> Sequence[Drop]:
        tc = self.full_tc
        paths = list[Schedulable]()
        drops = sorted(drops, key=right_then_down)
        print(map_str([d.pad.location.coords for d in drops]))
        pads = tc.pads(0)
        
        def add_path(d_no: int, path: Path.Middle) -> None:
            if d_no == 0:
                path = path.start(self.full_tc)
            else:
                path = path.join()
            path = path.to_col(5).to_pad(self.output_well.exit_pad)
            paths.append((drops[d_no], path.enter_well()))
            
        for i in (12, 13, 14, 15):
            add_path(i, Path.to_col(13).to_pad(pads[i-4]))
            
        add_path(7, Path.to_col(9).to_pad(pads[12]))
    
        for i in (9, 10, 11):
            add_path(i, Path.to_pad(pads[i+4]))
            
        add_path(6, Path.to_pad(pads[4]))
        add_path(8, Path.to_pad(pads[5]))
        add_path(4, Path.to_pad(pads[6]))
        add_path(5, Path.to_pad(pads[7]))
        add_path(3, Path.to_pad(pads[0]))
        add_path(1, Path.to_col(4).to_pad(pads[1]))
        add_path(2, Path.to_col(4).to_pad(pads[2]))
        add_path(0, Path.to_row(2).to_col(4).to_pad(pads[3]))
    
        drops = Path.run_paths(paths, system=self.board.in_system())
        return drops
        
    def tc_23(self, drops: Sequence[Drop], parked: int) -> Sequence[Drop]:
        tc = self.full_tc
        paths = list[Schedulable]()
        drops = sorted(drops, key=right_then_down)
        drops.append(self.parked_R4(parked))
        print(map_str([d.pad.location.coords for d in drops]))
        pads = tc.pads(0)
        
        def add_path(d_no: int, path: Path.Middle) -> None:
            if d_no == 0:
                path = path.start(self.full_tc)
            else:
                path = path.join()
            path = path.to_col(5).to_pad(self.output_well.exit_pad)
            paths.append((drops[d_no], path.enter_well()))
            
        for i in (12, 13, 14):
            add_path(i, Path.to_col(13).to_pad(pads[i-4]))
            
        add_path(7, Path.to_col(9).to_pad(pads[12]))
    
        for i in (9, 10, 11):
            add_path(i, Path.to_pad(pads[i+4]))
            
        add_path(6, Path.to_pad(pads[4]))
        add_path(8, Path.to_pad(pads[5]))
        add_path(4, Path.to_pad(pads[6]))
        add_path(5, Path.to_pad(pads[7]))
        add_path(3, Path.to_pad(pads[0]))
        add_path(1, Path.to_col(4).to_pad(pads[1]))
        add_path(2, Path.to_col(4).to_pad(pads[2]))
        add_path(0, Path.to_row(2).to_col(4).to_pad(pads[3]))
        add_path(15, Path.to_pad(pads[11]))
    
        drops = Path.run_paths(paths, system=self.board.in_system())
        return drops
        
        
        
    def run(self, 
            board: Board, 
            system: System,                 # @UnusedVariable
            args: Namespace) -> None:
        assert isinstance(board, joey.Board)
        # speedup: int = args.speed_up
        # cycles: int = args.cycles
        # shuttles: int = args.shuttles
        
        self.setup(board, args = args)
        r1_drop = self.initial_mix_and_tc()
        
        # Path.run_paths([(parked_r1_drop, Path.to_pad(self.park_R1))], system=system)
        
        diluted: Sequence[Drop] = sorted(self.dilute_1(r1_drop), key=right_then_up)
        print(f"diluted: {map_str(diluted)}")

        mixed = self.mix_3_1(diluted) 
        print(mixed)
        thermocycled = self.tc_1(mixed)
        print("Done with tcycle")
        assert len(thermocycled) == 0
        
        diluted = self.dilute_2()
        print(f"{len(diluted)} diluted drops")

        mixed = self.mix_3_2(diluted)
        print(f"Done with second dilution: {len(mixed)}")
        thermocycled = self.tc_23(mixed, 1)
        mixed = self.mix_3_3()
        self.tc_23(mixed, 0)
        print(f"Done")
        
class MixPrep(PCRTask):
    def __init__(self) -> None:
        super().__init__(name="mix-prep", 
                         description="Mix four outputs of the preparation phase.")
        
    # def add_args_to(self, parser:ArgumentParser, *, 
    #                 exerciser:Exerciser)->None:  # @UnusedVariable
    #     ...
    
    def run(self, board:Board, 
            system:System, 
            args:Namespace) -> None:
        assert isinstance(board, joey.Board)
        super().setup(board, args = args)
        
        input_wells = list(board.wells[0:4])
        output_wells = list(board.wells[4:])
        
        # it's easier if the last two output wells are swapped
        input_wells[2], input_wells[3] = input_wells[3], input_wells[2]
        
        well_colors = ("red", "yellow", "blue", "green")
        drops = board.drop_size.as_unit("drops", singular="drop")
        n_drops = 48
        
        for i,w in enumerate(input_wells):
            reagent = self.reagent(f"R4-{i}", color=well_colors[i])
            w.contains(Liquid(reagent, n_drops*drops))
            
        mix4 = mixing_sequences.lookup_placed(4, full=True,
                                              lower_left=board.pad_at(12, 8),
                                              rows=3, cols=5)
        
        pads = sorted(mix4.pads, key=down_then_left)
        print(pads)
        paths = list[Schedulable]()
        for i,w in enumerate(input_wells):
            path = Path.dispense_from(w).to_pad(pads[i], row_first=False)
            if pads[i] is mix4.pads[0]:
                path = path.start(mix4.as_process(n_shuttles=self.shuttles))
            else:
                path = path.join()
            path = path.to_col(18).to_pad(output_wells[i].exit_pad)
            paths.append(path.enter_well())
            
        paths = paths * n_drops
        
        Path.run_paths(paths, system=system)

        


class PCRDriver(Exerciser):
    def __init__(self) -> None:
        super().__init__(description=f"Mockup of PCR tasks on Joey board")
        self.add_task(Prepare())
        self.add_task(MixPrep())

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





