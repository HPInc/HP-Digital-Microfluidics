from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser, \
    ArgumentTypeError
from collections import deque
from random import sample
import random
from re import Pattern
import re
from typing import Sequence, Union, Optional, Final, NamedTuple

from devices import joey
from erk.basic import not_None
from erk.stringutils import map_str
from mpam.device import Board, System, Pad, Well, ExtractionPoint,\
    ProductLocation
from mpam.dilution import dilution_sequences
from mpam.drop import Drop
from mpam.exerciser import Exerciser, Task
from mpam.mixing import mixing_sequences
from mpam.monitor import BoardMonitor
from mpam.paths import Path, Schedulable
from mpam.processes import PlacedMixSequence, Transform
from mpam.thermocycle import ThermocyclePhase, ThermocycleProcessType, \
    Thermocycler, ShuttleDir
from mpam.types import Reagent, Liquid, Dir, Color, waste_reagent, Barrier, \
    schedule, Delayed
from quantities.SI import ms, second, seconds, uL
from quantities.dimensions import Time, Volume
from quantities.temperature import abs_C
from devices.dummy_pipettor import DummyPipettor


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
        
        ps: Optional[float] = args.pipettor_speed
        if ps is not None:
            pipettor = board.pipettor
            if isinstance(pipettor, DummyPipettor):
                print(f"Speeding up pipettor arm by a factor of {ps}.")
                pipettor.speed_up(ps)
            else:
                print(f"Cannot speed up {pipettor}.")
        
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
            # print(pads)
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
        # print(map_str([d.pad.location.coords for d in drops]))
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
        # print(map_str([d.pad.location.coords for d in drops]))
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
        # print(f"diluted: {map_str(diluted)}")

        mixed = self.mix_3_1(diluted) 
        # print(mixed)
        thermocycled = self.tc_1(mixed)
        # print("Done with tcycle")
        assert len(thermocycled) == 0
        
        diluted = self.dilute_2()
        # print(f"{len(diluted)} diluted drops")

        mixed = self.mix_3_2(diluted)
        # print(f"Done with second dilution: {len(mixed)}")
        thermocycled = self.tc_23(mixed, 1)
        mixed = self.mix_3_3()
        self.tc_23(mixed, 0)
        # print(f"Done")
        
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

weighted_size_arg_re: Final[Pattern] = re.compile(f"([1-8])(?::(\\d+(?:\\.\\d+)?))?")

class WeightedSize(NamedTuple):
    size: int
    weight: float = 1
    
    def __repr__(self) -> str:
        return f"{self.size}:{self.weight:.1f}"

    

def weighted_size_arg(arg: str) -> WeightedSize:
    m = weighted_size_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as an integer or an integer and a float separated by a colon.""")
    n = int(m.group(1))
    wg = m.group(2)
    w = float(wg) if wg is not None else 1
    return WeightedSize(n, w)
    

class CombSynth(PCRTask):
    n_combinations: int
    fragments: Sequence[Reagent]
    sizes: Sequence[int]
    size_weights: Sequence[float]

    phase_1_ep: ExtractionPoint
    phase_4_ep: ExtractionPoint
    phase_6_ep: ExtractionPoint
    
    phase_2_dilution: PlacedMixSequence
    phase_2_mix: PlacedMixSequence
    
    phase_3_dilution: PlacedMixSequence

    phase_4_mix: PlacedMixSequence
    phase_4_dilution: PlacedMixSequence
    
    phase_5_mix: PlacedMixSequence

    phase_barrier: Barrier[Drop]
    
    thermocycler: Thermocycler
    
    waste_well: Well    
    pm_well: Well
    db_well: Well
    mm_well: Well
    rsm_well: Well

    drops_needed: dict[Well, int]
    
    pf: Reagent
    
    combo_colors: Final[Sequence[str]]
    
    @property
    def n_fragments(self) -> int:
        return len(self.fragments)

    def __init__(self) -> None:
        super().__init__(name = "combinatorial-synthesis", aliases = ["comb-synth", "cs"],
                         description = "Mix four outputs of the preparation phase.")
        self.combo_colors = ("red", "green", "yellow", "darkblue", "brown", 
                             "purple", "silver", "orange", "pink", "darkgreen")

    def add_args_to(self, parser: ArgumentParser, *,
                    exerciser:Exerciser)->None:  # @UnusedVariable
        default_n = 10
        parser.add_argument("n", type=int, metavar="N", default=default_n, nargs="?",
                            help=f"The number of combinations to run.  Default is {default_n}")
        group = self.arg_group_in(parser)
        
        default_sizes = (WeightedSize(2), WeightedSize(3,2), WeightedSize(4,5), WeightedSize(5))
        group.add_argument("-s", "--sizes", type=weighted_size_arg, nargs="*", default=default_sizes,
                           metavar="INT[:FLOAT]",
                           help=f'''
                            The allowed combination sizes.  Multiple sizes may be specified.
                            Each size is either an integer or an integer immediately followed by a colon
                            and a floating-point number representing the relative weight.
                            Default is {default_sizes}
                           ''')
        
        default_n_fragments = 30
        group.add_argument("-nf", "--fragments", type=int, metavar="INT", default=default_n_fragments,
                           help=f'''
                            The number of fragments to combine.
                            Default is {default_n_fragments}
                           ''')


    def setup(self, board: joey.Board, *,
              args: Namespace) -> None:
        
        super().setup(board, args=args)
        self.n_combinations = args.n
        n_fragments: int = args.fragments
        self.fragments = tuple(Reagent.find(f"Fragment-{i+1}") for i in range(n_fragments))
        sizes: Sequence[WeightedSize] = args.sizes
        self.sizes = tuple(s.size for s in sizes)
        self.size_weights = tuple(s.weight for s in sizes)
        self.phase_1_ep = board.extraction_points[0]
        self.phase_5_ep = board.extraction_points[1]
        self.phase_6_ep = board.extraction_points[2]
        
        self.phase_barrier = Barrier(0, name="phase-end")
        
        
        self.phase_2_dilution = dilution_sequences.lookup(8, full=False,
                                                          rows=3, cols=5) \
                                            .transformed(Transform.FLIP_Y) \
                                            .placed(board.pad_at(14,12))

        self.phase_2_mix = mixing_sequences.lookup_placed(3, full=False,
                                                          lower_left=board.pad_at(18,10),
                                                          rows=5, cols=1)
        
        self.phase_3_dilution = dilution_sequences.lookup(5, full=False,
                                                          rows=3, cols=3) \
                                            .transformed(Transform.ONE_EIGHTY) \
                                            .placed(board.pad_at(16, 0))
                                            
        self.phase_4_mix = mixing_sequences.lookup(2, full=False,
                                                   rows=3, cols=1) \
                                            .placed(board.pad_at(18,4))
        self.phase_4_dilution = (dilution_sequences.lookup(3, full=False,
                                                           rows=3, cols=3) 
                                            .placed(board.pad_at(18,4)))
        
        self.phase_5_mix = mixing_sequences.lookup(2, full=False,
                                                   rows=3, cols=1) \
                                            .placed(board.pad_at(13,7))
        
                              
        self.drops_needed = {}
                                            
        def well(n: int, r: str, drops_per_target: int) -> Well:
            w = board.wells[n]
            w.contains(Reagent.find(r))
            self.drops_needed[w] = drops_per_target*self.n_combinations
            # The +1 is a kludge needed because the drop being dispensed will already have been subtracted
            # out when the path was scheduled.
            w.compute_fill_to(lambda: min(w.capacity, (self.drops_needed[w]+1)*w.dispensed_volume))
            return w 
            
        
        self.waste_well = board.wells[0]
        self.pm_well = well(4, "PM Primers", 1)
        self.db_well = well(5, "Dilution Buffer", 3)
        self.mm_well = well(6, "Master Mix", 2)
        self.rsm_well = well(7, "Prep Mixture", 5)
        
        self.pf = Reagent.find("PF Primers")
        
    def to_waste_from_row(self, row: int) -> Path.Middle:
        def now_waste(drop: Drop) -> None:
            drop.reagent = waste_reagent
        
        path = Path.empty().then_process(now_waste)
        if row <= 7:
            path = path.to_col(11).to_row(7).to_col(6).to_row(11)
        elif row <= 12:
            path = path.to_col(13).to_row(13)
        path = (path.to_col(11).to_row(18).to_col(5)
                .reach(self.phase_barrier, wait=False).to_col(0)
                )
        return path
    
    def waste_drop(self, 
                   source: Union[Well, tuple[ExtractionPoint, Reagent]],
                   waste_row: int,
                   path: Path.Middle 
                   ) -> Path.Full:
        if isinstance(source, Well):
            start = Path.dispense_from(source)
            self.drops_needed[source] -= 1
        else:
            start = Path.teleport_into(source[0], reagent=source[1])
        return (start+path+self.to_waste_from_row(waste_row)).enter_well()
                              
    
    def mix_to_tcycle(self, row: int) -> Path.Middle:
        path = (Path.empty().reach(self.phase_barrier)
                        .to_col(15)
                        .to_row(0)
                        .to_col(11)
                        .to_row(6)
                        .to_col(5)
                        .to_row(row)
                        .to_col(7))
        return path
    
    def tcycle_to_mix(self, col: int, row: int) -> Path.Middle:
        path = (Path.empty().reach(self.phase_barrier)
                        .to_col(5)
                        .to_row(18)
                        .to_col(15)
                        .to_row(row)
                        .to_col(col))
        return path
    
    class Combination:
        serial_number: Final[int]
        task: Final[CombSynth]
        fragments: Final[Sequence[Reagent]]
        drop_color: Final[Color]
        lead_drop: Drop
        
        def __init__(self, serial_number: int, task: CombSynth) -> None:
            self.serial_number = serial_number
            self.task = task
            size = random.choices(task.sizes, task.size_weights)
            self.fragments = sample(task.fragments, size[0])
            self.drop_color = Color.find(task.combo_colors[serial_number % len(task.combo_colors)])
            
        def __repr__(self) -> str:
            return f"Combination({self.serial_number})"
        
        def my_reagent(self, prefix: str) -> Reagent:
            return self.task.reagent(f"{prefix} #{self.serial_number}", color=self.drop_color)
        
            
            
    def pipleline_mixes(self, 
                        mixing: Sequence[Optional[CombSynth.Combination]]
                        ) -> list[Schedulable]:

        n_shuttles = self.shuttles
        board = self.board
        
        paths = list[Schedulable]()
        
        assert len(mixing) == 6
        
        c1,c2,c3,c4,c5,c6 = mixing
        # We'll get c6 out out of the way first so it doesn't block the others.
        if c6 is not None:
            product_loc = Delayed[ProductLocation]()
            product_loc.then_call(lambda pl: print(f"Product {pl.reagent} wound up in {pl.location}"))
            paths.append((c6.lead_drop,
                          Path.empty()
                            .reach(self.phase_barrier, wait=False)
                            .then_process(lambda drop: print(f"Extracting {drop.liquid}"))
                            .teleport_out(product_loc = product_loc))
                         )
            
        if c1 is not None:
            n = len(c1.fragments)
            mix = mixing_sequences.lookup_placed(n, full=False,
                                                  lower_left=board.pad_at(13,16),
                                                  rows=3, cols=6)
            pads = sorted(mix.pads, key=down_then_left)
            ep = self.phase_1_ep
            result = c1.my_reagent("R1")
            passed_by = Barrier[Drop](n)
            for pad, frag in zip(pads, c1.fragments):
                if pad is mix.lead_drop_pad:
                    def remember_lead_drop(drop: Drop) -> None:
                        assert c1 is not None
                        c1.lead_drop = drop
                    paths.append(Path.teleport_into(ep, reagent=frag)
                                    .to_pad(pad)
                                    .start(mix.as_process(n_shuttles=n_shuttles, result=result))
                                    .then_process(remember_lead_drop)
                                    .to_pad(ep.pad)
                                    .reach(passed_by)
                                    .to_row(16)
                                    .extended(self.mix_to_tcycle(0)))
                else:
                    paths.append(self.waste_drop((ep, frag), pad.row,
                                                 Path.to_pad(pad)
                                                    .join()
                                                    .to_col(11)
                                                    .reach(passed_by, wait=False)))

        if c2 is not None:
            rdiluted = c2.my_reagent("R1[diluted]")
            result = c2.my_reagent("R2")
            in_pos = Barrier[Drop](2)
            passed_by = Barrier[Drop](2)
            
            paths.append((c2.lead_drop,
                          Path.empty().reach(in_pos)
                                .to_pad((16,12))
                                .start(self.phase_2_dilution.as_process(n_shuttles=n_shuttles,
                                                                        result=rdiluted))
                                .to_row(10).reach(passed_by)
                                .to_pad((18,12))
                                .start(self.phase_2_mix.as_process(n_shuttles=n_shuttles,
                                                                   result=result))
                                .extended(self.mix_to_tcycle(2))
                                ))                          

            paths.append(self.waste_drop(self.pm_well, 14,
                                         Path.to_row(14).join()))
            
            paths.append(self.waste_drop(self.mm_well, 13,
                                         Path.to_row(10).join()
                                            .to_col(14).to_row(13)))
            
            paths.append(self.waste_drop(self.db_well, 12,
                                         Path.to_pad((14,12)).join()))

            paths.append(self.waste_drop(self.db_well, 12,
                                         Path.to_pad((16,14), row_first=False)
                                            .reach(in_pos)
                                            .join()
                                            .to_row(12)))

            paths.append(self.waste_drop(self.db_well, 12,
                                         Path.join()
                                            .to_col(14)
                                            .reach(passed_by, wait=False)))
            
        # We do c4 before c3, because we need to get the rsm drops here first
        if c4 is not None:
            rmixed = c4.my_reagent("R3[mixed]")
            result = c4.my_reagent("R4")
            
            mix_done = Barrier[Drop](2)
            
            paths.append((c4.lead_drop,
                          Path.start(self.phase_4_mix.as_process(n_shuttles=n_shuttles, result=rmixed))
                                .start(self.phase_4_dilution.as_process(n_shuttles=n_shuttles, result=result))
                                .extended(self.mix_to_tcycle(14))
                                ))   
            
            paths.append(self.waste_drop(self.rsm_well, 4,
                                         Path.to_row(2).to_col(16).to_row(6)
                                            .reach(mix_done).to_col(18)
                                            .join()
                                            .to_col(15).to_row(4)))

            paths.append(self.waste_drop(self.rsm_well, 4, 
                                         Path.to_row(2).to_col(16).to_row(4)   
                                            .join()))

            paths.append(self.waste_drop(self.mm_well, 4, 
                                         Path.join()
                                            .reach(mix_done, wait = False)
                                            .to_row(8)
                                            .to_col(15).to_row(4)))

        if c3 is not None:
            result = c3.my_reagent("R3")
            
            paths.append((c3.lead_drop,
                          Path.start(self.phase_3_dilution.as_process(n_shuttles=n_shuttles,
                                                                        result=result))
                                .extended(self.mix_to_tcycle(4))
                                ))   
            
            paths.append(self.waste_drop(self.rsm_well, 2,
                                         Path.to_row(2).to_col(16)   
                                            .join()))
            paths.append(self.waste_drop(self.rsm_well, 2,
                                         Path.to_row(2)   
                                         .join()))

            paths.append(self.waste_drop(self.rsm_well, 2,
                                         Path.join()
                                            .to_row(2)))
            
        if c5 is not None:
            result = c5.my_reagent("R5")
            
            paths.append((c5.lead_drop,
                          Path.start(self.phase_5_mix.as_process(n_shuttles=n_shuttles,
                                                                 result=result))
                                .extended(self.mix_to_tcycle(16))
                                ))   
            paths.append(self.waste_drop((self.phase_5_ep, self.pf), 9,
                                         Path.join()
                                            .to_row(13)))
            
                               
        return paths

    def pipleline_tcycle(self, 
                         tcycling: Sequence[Optional[CombSynth.Combination]]
                         ) -> list[Schedulable]:
        paths = list[Schedulable]()
        
        channels = (7,6,5,2,1)
        
        channels_used = tuple(channels[i] for i,c in enumerate(tcycling) if c is not None)
        tc = self.board.thermocycler.as_process(phases=self.tc_phases,
                                                channels=channels_used,
                                                n_iterations=self.tc_cycles,
                                                shuttle_dir=ShuttleDir.ROW_ONLY)
        
        started = False
        
        def to_mix(col: int, row: int) -> Path.Middle:
            nonlocal started
            path = Path.empty()
            really_tcycle = True
            if really_tcycle:
                if started:
                    path = path.join()
                else:
                    started = True
                    path = path.start(tc)
            path += self.tcycle_to_mix(col, row)

            return path

        in_pos = Barrier[Drop](len(tuple(x for x in tcycling if x is not None)))
        c1,c2,c3,c4,c5 = tcycling
        if c1 is not None:
            paths.append((c1.lead_drop, to_mix(17,10).reach(in_pos).to_col(16)))
        if c2 is not None:
            paths.append((c2.lead_drop, to_mix(17,0).reach(in_pos).to_col(16)))
        if c3 is not None:
            paths.append((c3.lead_drop, to_mix(18,4).reach(in_pos)))
        if c4 is not None:
            paths.append((c4.lead_drop, to_mix(13,7).reach(in_pos)))
        if c5 is not None:
            paths.append((c5.lead_drop, to_mix(13,3).reach(in_pos)))
        
        # TODO: The rest
        
        return paths

            
    def pipeline_phase(self, 
                       mixing: Sequence[Optional[CombSynth.Combination]],
                       tcycling: Sequence[Optional[CombSynth.Combination]]
                       ) -> Sequence[Schedulable]:
        mixing_paths = self.pipleline_mixes(mixing)
        tcycle_paths = self.pipleline_tcycle(tcycling)
        
        # print(f"{len(mixing_paths)} mixing, {len(tcycle_paths)} thermocycles")
        
        return mixing_paths+tcycle_paths
        
        
        
    def run(self, board: Board,
            system: System,
            args: Namespace) -> None:
        assert isinstance(board, joey.Board)
        self.setup(board, args = args)
        

        combinations = deque(self.Combination(i+1, self) for i in range(self.n_combinations))

        mixing: list[Optional[CombSynth.Combination]] = [None] * 6
        tcycling: list[Optional[CombSynth.Combination]] = [None] * 5
        
        # mixing_fns: tuple[Callable[[CombSynth.Combination, Barrier], Sequence[Schedulable]], ...] = (
        #         self.Combination.phase_1,
        #     )
        
        
        n_left = len(combinations)
        
        while n_left > 0:
            mixing, tcycling = (tcycling, mixing[:-1])
            mixing.insert(0, combinations.popleft() if len(combinations) > 0 else None)
            if mixing[-1] is not None:
                n_left -= 1
            
            paths = self.pipeline_phase(mixing, tcycling)
            
            # paths: list[Schedulable] = []
            # for i,c in enumerate(mixing):
            #     if c is not None:
            #         fn = mixing_fns[i]
            #         paths.extend(fn(c, barrier))
            #
            # for i,c in enumerate(tcycling):
            #     if c is not None:
            #         path = Path.empty().reach(barrier).extended(self.after_tcycle[i])
            #         paths.append((c.lead_drop, path))

            self.phase_barrier.reset(len(paths))
            Path.run_paths(paths, system=system)
        

class Test(Task):
    def __init__(self) -> None:
        super().__init__(name="test", 
                         description="Test Extraction Points")
        
    # def add_args_to(self, parser:ArgumentParser, *, 
    #                 exerciser:Exerciser)->None:  # @UnusedVariable
    #     ...
    
    def run(self, board:Board, 
            system:System, 
            args:Namespace) -> None:
        assert isinstance(board, joey.Board)
        
        ep1 = board.extraction_points[1]
        ep2 = board.extraction_points[2]
        
        path = Path.teleport_into(ep1).to_pad(ep2.pad).teleport_out()
        schedule(path)
        
     


class PCRDriver(Exerciser):
    def __init__(self) -> None:
        super().__init__(description=f"Mockup of PCR tasks on Joey board")
        self.add_task(Prepare())
        self.add_task(MixPrep())
        self.add_task(CombSynth())
        self.add_task(Test())

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
    
        group.add_argument('-ps', '--pipettor-speed', type=float, metavar='MULT',
                           help=f'''
                                 A speed-up factor for pipettor operations.
                                 ''')
    

if __name__ == '__main__':
    Time.default_units(ms)
    Volume.default_units(uL)
    exerciser = PCRDriver()
    exerciser.parse_args_and_run()





