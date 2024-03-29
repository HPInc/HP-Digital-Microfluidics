from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser, \
    ArgumentTypeError
from collections import deque
import logging
from random import sample
import random
from re import Pattern
import re
from typing import Sequence, Union, Optional, Final, NamedTuple, Callable

from devices import joey
from devices.dummy_pipettor import DummyPipettor
from sifu.basic import not_None
from sifu.color import Color
from sifu.grid import Dir
from sifu.quant.SI import second, seconds
from sifu.quant.temperature import abs_C
from sifu.sched import Barrier, WaitableType, NO_WAIT, Postable, \
    SingleFireTrigger, Delayed, schedule
from sifu.stringutils import map_str
from dmf.device import Board, System, Pad, Well, ExtractionPoint, \
    ProductLocation
from dmf.dilution import dilution_sequences
from dmf.drop import Drop
from dmf.exerciser import Exerciser, Task
from dmf.mixing import mixing_sequences
from dmf.monitor import BoardMonitor
from dmf.paths import Path, Schedulable
from dmf.processes import PlacedMixSequence, Transform
from dmf.thermocycle import ThermocyclePhase, ThermocycleProcessType, \
    Thermocycler, ShuttleDir
from dmf.types import Reagent, Liquid, waste_reagent


logger = logging.getLogger(__name__)


def right_then_up(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.on_board_pad
    x,y = loc.location.coords
    return x,y

def right_then_down(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.on_board_pad
    x,y = loc.location.coords
    return x,-y

def left_then_down(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.on_board_pad
    x,y = loc.location.coords
    return -x,-y

def up_then_right(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.on_board_pad
    x,y = loc.location.coords
    return y,x

def down_then_right(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.on_board_pad
    x,y = loc.location.coords
    return -y,x

def down_then_left(loc: Union[Drop,Pad]) -> tuple[int, int]:
    if isinstance(loc, Drop):
        loc = loc.on_board_pad
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
        self.monitor = board.system.monitor

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
                logger.info(f"Speeding up pipettor arm by a factor of {ps}.")
                pipettor.speed_up(ps)
            else:
                logger.info(f"Cannot speed up {pipettor}.")

    def reagent(self, name: str, *,
                color: Optional[Union[Color, str, tuple[float,float,float]]] = None) -> Reagent:
        r = Reagent.find(name)
        if color is not None and self.monitor is not None:
            if not isinstance(color, Color):
                color = Color.find(color)
            self.monitor.reserve_color(r, color)
        return r
    
    def add_args_to(self,
                    group: _ArgumentGroup, 
                    parser: ArgumentParser, # @UnusedVariable
                    *, exerciser:Exerciser)->None: # @UnusedVariable
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

    def add_args_to(self,
                    group: _ArgumentGroup, 
                    parser:ArgumentParser, *,
                    exerciser:Exerciser)->None: 
        super().add_args_to(group, parser, exerciser=exerciser)
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

        self.park_R1 = board.pad_at(19, 11)
        self.park_R3 = (board.pad_at(1, 11), board.pad_at(3, 11),
                        board.pad_at(1, 9), board.pad_at(3, 9),
                        board.pad_at(19, 11))
        self.park_R4 = (board.pad_at(19,9), board.pad_at(17,9))

        self.dilution = dilution_sequences.lookup_placed(8, full=True,
                                                         lower_left=board.pad_at(6,3),
                                                         rows=5, cols=9)
        self.mix3 = tuple(mixing_sequences.lookup_placed(3, full=True,
                                                         lower_left=board.pad_at(2+3*i,2),
                                                         rows=5, cols=1)
                            for i in range(6))

        drops = board.drop_size.as_unit("drops", singular="drop")

        self.pmo = self.reagent("Pre-Mixed Oligos_i")
        mm = self.mm = self.reagent("Master Mix")
        bd = self.bd = self.reagent("Dilution Buffer")
        primer = self.primer = self.reagent("Primer_i")

        self.pmo_ep = board.extraction_point_number(2)

        self.mm_well = board.well_number(6)
        self.mm_well.contains(Liquid(mm, 17*drops))

        self.bd_well = board.well_number(7)
        self.bd_well.contains(Liquid(bd, 14*drops))

        self.primer_well = board.well_number(8)
        self.primer_well.contains(Liquid(primer, 16*drops))

        self.output_well = board.well_number(4)

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

        drops = Path.run_paths((p1,p2), system=self.board.system)
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
        return Path.run_paths(paths, system=self.board.system)

    def dilute_1(self, r1_drop: Drop) -> Sequence[Drop]:
        drops = sorted(self.dilute(r1_drop), key=right_then_up)
        n_parked = 2
        parking = [(drops[i], Path.to_pad(self.park_R3[i], row_first=False))
                    for i in range(n_parked)]
        Path.run_paths(parking, system=self.board.system)
        return drops[n_parked:]


    def dilute_2(self) -> Sequence[Drop]:
        r1_drop = self.parked_R1()
        Path.run_paths([(r1_drop, Path.to_col(15))], system=self.board.system)
        drops = sorted(self.dilute(r1_drop), key=right_then_up)
        parking = [(drops[0], Path.to_pad(self.park_R3[2], row_first=False)),
                   (drops[1], Path.to_pad(self.park_R3[3], row_first=False)),
                   (drops[-1], Path.to_col(15).to_pad(self.park_R3[4])),
                   ]
        Path.run_paths(parking, system=self.board.system)
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
        drops = Path.run_paths(paths, system=self.board.system)
        return drops

    def mix_3_1(self, drops: Sequence[Drop]) -> Sequence[Drop]:
        drops = sorted(self.mix_3(drops), key=left_then_down)
        n_parked = 2
        parking = [(drops[i], Path.to_pad(self.park_R4[i], row_first=False))
                    for i in range(n_parked)]
        Path.run_paths(parking, system=self.board.system)
        return drops[n_parked:]

    def mix_3_2(self, drops: Sequence[Drop]) -> Sequence[Drop]:
        drops = sorted(self.mix_3(drops), key=left_then_down)
        return drops
    def mix_3_3(self) -> Sequence[Drop]:
        drops = [self.parked_R3(i) for i in range(5)]
        Path.run_paths([(self.parked_R3(4), Path.to_col(15).to_row(2)),
                        (self.parked_R3(2), Path.to_col(5).to_row(2)),
                        (self.parked_R3(3), Path.to_col(7).to_row(2)),
                        (self.parked_R3(0), Path.to_row(2)),
                        (self.parked_R3(1), Path.to_row(2)),
                        ], system=self.board.system)
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
            path = path.to_col(6).to_pad(self.output_well.exit_pad)
            paths.append((drops[d_no], path.enter_well()))

        for i in (12, 13, 14, 15):
            add_path(i, Path.to_col(14).to_pad(pads[i-4]))

        add_path(7, Path.to_col(10).to_pad(pads[12]))

        for i in (9, 10, 11):
            add_path(i, Path.to_pad(pads[i+4]))

        add_path(6, Path.to_pad(pads[4]))
        add_path(8, Path.to_pad(pads[5]))
        add_path(4, Path.to_pad(pads[6]))
        add_path(5, Path.to_pad(pads[7]))
        add_path(3, Path.to_pad(pads[0]))
        add_path(1, Path.to_col(5).to_pad(pads[1]))
        add_path(2, Path.to_col(5).to_pad(pads[2]))
        add_path(0, Path.to_row(3).to_col(5).to_pad(pads[3]))

        drops = Path.run_paths(paths, system=self.board.system)
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
            path = path.to_col(6).to_pad(self.output_well.exit_pad)
            paths.append((drops[d_no], path.enter_well()))

        for i in (12, 13, 14):
            add_path(i, Path.to_col(14).to_pad(pads[i-4]))

        add_path(7, Path.to_col(10).to_pad(pads[12]))

        for i in (9, 10, 11):
            add_path(i, Path.to_pad(pads[i+4]))

        add_path(6, Path.to_pad(pads[4]))
        add_path(8, Path.to_pad(pads[5]))
        add_path(4, Path.to_pad(pads[6]))
        add_path(5, Path.to_pad(pads[7]))
        add_path(3, Path.to_pad(pads[0]))
        add_path(1, Path.to_col(5).to_pad(pads[1]))
        add_path(2, Path.to_col(5).to_pad(pads[2]))
        add_path(0, Path.to_row(3).to_col(5).to_pad(pads[3]))
        add_path(15, Path.to_pad(pads[11]))

        drops = Path.run_paths(paths, system=self.board.system)
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

        input_wells = [board.well_number(n) for n in range(1, 5)]
        output_wells = [board.well_number(n) for n in range(5, 9)]

        # it's easier if the last two output wells are swapped
        input_wells[2], input_wells[3] = input_wells[3], input_wells[2]

        well_colors = ("red", "yellow", "blue", "green")
        drops = board.drop_size.as_unit("drops", singular="drop")
        n_drops = 48

        for i,w in enumerate(input_wells):
            reagent = self.reagent(f"R4-{i}", color=well_colors[i])
            w.contains(Liquid(reagent, n_drops*drops))

        mix4 = mixing_sequences.lookup_placed(4, full=True,
                                              lower_left=board.pad_at(13, 9),
                                              rows=3, cols=5)

        pads = sorted(mix4.pads, key=down_then_left)
        logger.info(pads)
        paths = list[Schedulable]()
        for i,w in enumerate(input_wells):
            path = Path.dispense_from(w).to_pad(pads[i], row_first=False)
            if pads[i] is mix4.pads[0]:
                path = path.start(mix4.as_process(n_shuttles=self.shuttles))
            else:
                path = path.join()
            path = path.to_col(19).to_pad(output_wells[i].exit_pad)
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

    phase_barrier: Barrier

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

    def add_args_to(self,
                    group: _ArgumentGroup, 
                    parser: ArgumentParser, *,
                    exerciser:Exerciser)->None:  
        super().add_args_to(group, parser, exerciser=exerciser)
        default_n = 10
        parser.add_argument("n", type=int, metavar="N", default=default_n, nargs="?",
                            help=f"The number of combinations to run.  Default is {default_n}")

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
        self.phase_1_ep = board.extraction_point_number(1)
        self.phase_5_ep = board.extraction_point_number(2)
        self.phase_6_ep = board.extraction_point_number(3)

        self.phase_barrier = Barrier(0, name="phase-end")


        self.phase_2_dilution = dilution_sequences.lookup(8, full=False,
                                                          rows=3, cols=5) \
                                            .transformed(Transform.FLIP_Y) \
                                            .placed(board.pad_at(15,13))

        self.phase_2_mix = mixing_sequences.lookup_placed(3, full=False,
                                                          lower_left=board.pad_at(19,11),
                                                          rows=5, cols=1)

        self.phase_3_dilution = dilution_sequences.lookup(5, full=False,
                                                          rows=3, cols=3) \
                                            .transformed(Transform.ONE_EIGHTY) \
                                            .placed(board.pad_at(17, 1))

        self.phase_4_mix = mixing_sequences.lookup(2, full=False,
                                                   rows=3, cols=1) \
                                            .placed(board.pad_at(19,5))
        self.phase_4_dilution = (dilution_sequences.lookup(3, full=False,
                                                           rows=3, cols=3)
                                            .placed(board.pad_at(19,5)))

        self.phase_5_mix = mixing_sequences.lookup(2, full=False,
                                                   rows=3, cols=1) \
                                            .placed(board.pad_at(14,8))


        self.drops_needed = {}

        def well(n: int, r: str, drops_per_target: int) -> Well:
            w = board.well_number(n)
            w.contains(Reagent.find(r))
            drops_needed = drops_per_target * self.n_combinations
            w.required = drops_needed*w.dispensed_volume
            # self.drops_needed[w] = drops_per_target*self.n_combinations
            # w.compute_fill_to(lambda: min(w.capacity, self.drops_needed[w]*w.dispensed_volume))
            return w


        self.waste_well = board.well_number(1)
        self.pm_well = well(5, "PM Primers", 1)
        self.db_well = well(6, "Dilution Buffer", 3)
        self.mm_well = well(7, "Master Mix", 2)
        self.rsm_well = well(8, "Prep Mixture", 5)

        self.pf = Reagent.find("PF Primers")

    def to_waste_from_row(self, row: int) -> Path.Middle:
        def now_waste(drop: Drop) -> None:
            drop.reagent = waste_reagent

        path = Path.empty().then_process(now_waste)
        if row <= 7:
            path = path.to_col(12).to_row(8).to_col(7).to_row(12)
        elif row <= 12:
            path = path.to_col(14).to_row(14)
        path = (path.to_col(12).to_row(19).to_col(6)
                .reach(self.phase_barrier, wait=False).to_col(1)
                )
        return path

    def waste_drop(self,
                   source: Union[Well, tuple[ExtractionPoint, Reagent, Optional[WaitableType]]],
                   waste_row: int,
                   path: Path.Middle
                   ) -> Path.Full:
        if isinstance(source, Well):
            # well = source
            # def drop_used() -> None:
            #     self.drops_needed[well] -= 1
            #     if well is self.rsm_well:
            #         print(f"-- Now need {qstr(self.drops_needed[well], 'drop')} of {well.reagent}.  Well has {well.volume}")
            # start = Path.dispense_from(source, before_release=drop_used)
            start = Path.dispense_from(source)
        else:
            ep, reagent, after = source
            if after is None:
                after = NO_WAIT
            start = Path.teleport_into(ep, reagent=reagent, after=after)
        return (start+path+self.to_waste_from_row(waste_row)).enter_well()


    def mix_to_tcycle(self, row: int) -> Path.Middle:
        path = (Path.empty().reach(self.phase_barrier)
                        .to_col(16)
                        .to_row(1)
                        .to_col(12)
                        .to_row(7)
                        .to_col(6)
                        .to_row(row)
                        .to_col(8))
        return path

    def tcycle_to_mix(self, col: int, row: int) -> Path.Middle:
        path = (Path.empty().reach(self.phase_barrier)
                        .to_col(6)
                        .to_row(19)
                        .to_col(16)
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

        def update_drop(comb: CombSynth.Combination) -> Callable[[Drop], None]:
            def do_update(drop: Drop) -> None:
                comb.lead_drop = drop
            return do_update

        c1,c2,c3,c4,c5,c6 = mixing
        # We'll get c6 out out of the way first so it doesn't block the others.
        if c6 is not None:
            product_loc = Postable[ProductLocation]()
            product_loc.then_call(lambda pl: logger.info(f"Product {pl.reagent} wound up in {pl.location}"))
            paths.append((c6.lead_drop,
                          Path.empty()
                            .reach(self.phase_barrier, wait=False)
                            .then_process(lambda drop: logger.info(f"Extracting {drop.blob.contents}"))
                            .teleport_out(product_loc = product_loc))
                         )

        if c1 is not None:
            n = len(c1.fragments)
            mix = mixing_sequences.lookup_placed(n, full=False,
                                                  lower_left=board.pad_at(14,17),
                                                  rows=3, cols=6)
            pads = sorted(mix.pads, key=down_then_left)
            ep = self.phase_1_ep
            result = c1.my_reagent("R1")
            passed_by = Barrier(n)
            ready_for_next: WaitableType = NO_WAIT
            for pad, frag in zip(pads, c1.fragments):
                if pad is mix.lead_drop_pad:
                    # def remember_lead_drop(drop: Drop) -> None:
                    #     assert c1 is not None
                    #     c1.lead_drop = drop
                    new_trigger = SingleFireTrigger()
                    paths.append(Path.teleport_into(ep, reagent=frag, after=ready_for_next)
                                    .to_pad(pad)
                                    .then_fire(new_trigger)
                                    .start(mix.as_process(n_shuttles=n_shuttles, result=result))
                                    .to_pad(ep.pad)
                                    .reach(passed_by)
                                    .to_row(17)
                                    .then_process(update_drop(c1))
                                    .extended(self.mix_to_tcycle(1)))
                    ready_for_next = new_trigger
                else:
                    new_trigger = SingleFireTrigger()
                    paths.append(self.waste_drop((ep, frag, ready_for_next), pad.row,
                                                 Path.to_pad(pad)
                                                    .then_fire(new_trigger)
                                                    .join()
                                                    .to_col(12)
                                                    .reach(passed_by, wait=False)))
                    ready_for_next = new_trigger

        if c2 is not None:
            rdiluted = c2.my_reagent("R1[diluted]")
            result = c2.my_reagent("R2")
            in_pos = Barrier(2)
            passed_by = Barrier(2)

            paths.append((c2.lead_drop,
                          Path.empty().reach(in_pos)
                                .to_pad((17,13))
                                .start(self.phase_2_dilution.as_process(n_shuttles=n_shuttles,
                                                                        result=rdiluted))
                                .to_row(11).reach(passed_by)
                                .to_pad((19,13))
                                .start(self.phase_2_mix.as_process(n_shuttles=n_shuttles,
                                                                   result=result))
                                .then_process(update_drop(c2))
                                .extended(self.mix_to_tcycle(3))
                                ))

            paths.append(self.waste_drop(self.pm_well, 15,
                                         Path.to_row(15).join()))

            paths.append(self.waste_drop(self.mm_well, 14,
                                         Path.to_row(11).join()
                                            .to_col(15).to_row(14)))

            paths.append(self.waste_drop(self.db_well, 13,
                                         Path.to_pad((15,13)).join()))

            paths.append(self.waste_drop(self.db_well, 13,
                                         Path.to_pad((17,15), row_first=False)
                                            .reach(in_pos)
                                            .join()
                                            .to_row(13)))

            paths.append(self.waste_drop(self.db_well, 13,
                                         Path.join()
                                            .to_col(15)
                                            .reach(passed_by, wait=False)))

        # We do c4 before c3, because we need to get the rsm drops here first
        if c4 is not None:
            rmixed = c4.my_reagent("R3[mixed]")
            result = c4.my_reagent("R4")

            mix_done = Barrier(2)

            paths.append((c4.lead_drop,
                          Path.start(self.phase_4_mix.as_process(n_shuttles=n_shuttles, result=rmixed))
                                .start(self.phase_4_dilution.as_process(n_shuttles=n_shuttles, result=result))
                                .then_process(update_drop(c4))
                                .extended(self.mix_to_tcycle(15))
                                ))

            paths.append(self.waste_drop(self.rsm_well, 5,
                                         Path.to_row(3).to_col(17).to_row(7)
                                            .reach(mix_done).to_col(19)
                                            .join()
                                            .to_col(16).to_row(5)))

            paths.append(self.waste_drop(self.rsm_well, 5,
                                         Path.to_row(3).to_col(17).to_row(5)
                                            .join()))

            paths.append(self.waste_drop(self.mm_well, 5,
                                         Path.join()
                                            .reach(mix_done, wait = False)
                                            .to_row(9)
                                            .to_col(16).to_row(6)
                                            .to_col(15)))

        if c3 is not None:
            result = c3.my_reagent("R3")

            paths.append((c3.lead_drop,
                          Path.start(self.phase_3_dilution.as_process(n_shuttles=n_shuttles,
                                                                        result=result))
                                .then_process(update_drop(c3))
                                .extended(self.mix_to_tcycle(5))
                                ))

            paths.append(self.waste_drop(self.rsm_well, 3,
                                         Path.to_row(3).to_col(17)
                                            .join()))
            paths.append(self.waste_drop(self.rsm_well, 3,
                                         Path.to_row(3)
                                         .join()))

            paths.append(self.waste_drop(self.rsm_well, 3,
                                         Path.join()
                                            .to_row(3)))

        if c5 is not None:
            result = c5.my_reagent("R5")

            paths.append((c5.lead_drop,
                          Path.start(self.phase_5_mix.as_process(n_shuttles=n_shuttles,
                                                                 result=result))
                                .then_process(update_drop(c5))
                                .extended(self.mix_to_tcycle(17))
                                ))
            paths.append(self.waste_drop((self.phase_5_ep, self.pf, None), 10,
                                         Path.join()
                                            .to_row(14)))


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

        in_pos = Barrier(len(tuple(x for x in tcycling if x is not None)))
        c1,c2,c3,c4,c5 = tcycling
        # print(f"Tcycle channels: {channels_used}")
        if c1 is not None:
            # print(f"Starting tcycle with {c1.lead_drop}")
            paths.append((c1.lead_drop, to_mix(18,11).reach(in_pos).to_col(17)))
        if c2 is not None:
            # print(f"Joining tcycle with {c2.lead_drop}")
            paths.append((c2.lead_drop, to_mix(18,1).reach(in_pos).to_col(17)))
        if c3 is not None:
            paths.append((c3.lead_drop, to_mix(19,5).reach(in_pos)))
        if c4 is not None:
            paths.append((c4.lead_drop, to_mix(14,8).reach(in_pos)))
        if c5 is not None:
            paths.append((c5.lead_drop, to_mix(14,4).reach(in_pos)))

        return paths


    def pipeline_phase(self,
                       mixing: Sequence[Optional[CombSynth.Combination]],
                       tcycling: Sequence[Optional[CombSynth.Combination]]
                       ) -> Sequence[Schedulable]:
        # empty_waste = (mixing[-1] and tcycling[-1] and not mixing[-2] and not tcycling[-2])
        mixing_paths = self.pipleline_mixes(mixing)
        tcycle_paths = self.pipleline_tcycle(tcycling)

        # print(f"{len(mixing_paths)} mixing, {len(tcycle_paths)} thermocycles")

        return mixing_paths+tcycle_paths



    def run(self, board: Board,
            system: System,
            args: Namespace) -> None:
        assert isinstance(board, joey.Board)
        self.setup(board, args = args)

        # we wait for a tick, just in case we started paused.

        system.clock.await_tick()

        refills = (self.pm_well.refill(),
                   self.db_well.refill(),
                   self.mm_well.refill(),
                   self.rsm_well.refill())
        Delayed.join(refills)


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
        if self.waste_well.volume.is_positive:
            logger.info("Emptying waste well")
            self.waste_well.empty_well()


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

        ep1 = board.extraction_point_number(2)
        ep2 = board.extraction_point_number(3)

        path = Path.teleport_into(ep1).to_pad(ep2.pad).teleport_out()
        schedule(path)


