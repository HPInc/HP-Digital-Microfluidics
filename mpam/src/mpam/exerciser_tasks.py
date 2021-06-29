from __future__ import annotations

from argparse import ArgumentParser, Namespace
from re import Pattern, Match
import re
from typing import Optional, Union, Any, NamedTuple, Final, ClassVar, Mapping, \
    Callable

from erk.stringutils import map_str
from mpam.device import Board, System, Pad, Well
from mpam.drop import Drop, MixingType, Mix2, Mix3, Mix4, Mix6, Mix9
from mpam.exerciser import Task, volume_arg, Exerciser
from mpam.types import Liquid, unknown_reagent, XYCoord, Operation, Dir, ticks, \
    StaticOperation, Reagent
from quantities.dimensions import Volume


class Dispense(Task):
    def __init__(self) -> None:
        super().__init__(name="dispense",
                         description="Dispense a drop from a given well and leave it there.",
                         aliases=["disp"])

    def add_args_to(self, parser: ArgumentParser, *,  
                    exerciser: Exerciser 
                    ) -> None:
        group = self.arg_group_in(parser)
        group.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=exerciser.available_wells(),
                            help="The well to dispense from")
        group.add_argument('-v', '--volume', type=volume_arg, metavar='VOLUME',
                            help="The initial volume of the well.  Default is a full well.")
        
    def run(self, board: Board, system: System, args: Namespace) -> None:
        well_no: int = args.well
        well = board.wells[well_no]

        drops = board.drop_size.as_unit("drops")
        volume: Optional[Union[Volume, float]] = args.volume
        if volume is None:
            volume = well.capacity
        elif isinstance(volume, float):
            volume = volume*drops
        well.contains(Liquid(unknown_reagent, volume))
        
        seq = Drop.DispenseFrom(well)
                
        with system.batched():
            seq.schedule()

class Absorb(Task):
    def __init__(self) -> None:
        super().__init__(name="absort",
                         description="Absorb a drop assumed to be on a well's exit pad.",
                         aliases=["abs"])

    def add_args_to(self, parser: ArgumentParser, *,  
                    exerciser: Exerciser 
                    ) -> None:
        group = self.arg_group_in(parser)
        group.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=exerciser.available_wells(),
                            help="The well to dispense from")
        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        well_no = args.well
        well = board.wells[well_no]

        drop = Drop.AppearAt(well.exit_pad, board=board).schedule().value
        drop.schedule(Drop.EnterWell)
        
class WalkPath(Task):
    def __init__(self) -> None:
        super().__init__(name="path",
                         description = "Walk a user-provided path from a starting well or pad.")
                         

    def add_args_to(self, parser: ArgumentParser, *,
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        group = self.arg_group_in(parser)
        
        starts = group.add_mutually_exclusive_group(required=True)
        starts.add_argument('-sp', '--start-pad', type=int, nargs=2, metavar=('X','Y'), 
                            help="The (x,y) coordinates of the pad to start from.  The drop is assumed to be there")
        starts.add_argument('-sw', '--start-well', type=int, metavar='INT', 
                            choices=exerciser.available_wells(),
                            help="The well to dispense from")
        
        group.add_argument('--path', required=True,
                            help='''
                            The path to walk.  Each step is indicated by a single character, optionally preceeded by
                            an integer indicating repetition.  'NSEW' or 'UDLR' indicate directions.  'A' at end signifies 
                            absorbing into a well.  An example path is '2RD10RUA'.  Paths are case-insensitive.
                            ''')
        group.add_argument('-v', '--volume', type=volume_arg, metavar='VOLUME',
                            help="The initial volume of the starting well.  Default is a full well.")
        # group.add_argument('-d', '--drops', type=int, default=1, metavar='N',
                            # help="The number of drops to walk along the path.  Default is 1")
        # parser.add_argument('-g', '--gap', type=int, default=8, metavar='N',
        #                     help="""
        #                     The gap between drops.  Default is 8
        #                     """)
        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        path: str = args.path.upper()

        start_well: Optional[int] = args.start_well
        if start_well is not None:
            well = board.wells[start_well]
            # seq: StaticOperation = Drop.DispenseFrom(well)
            start_pad: Pad = well.exit_pad
            drops = board.drop_size.as_unit("drops")
            volume: Optional[Union[Volume, float]] = args.volume
            if volume is None:
                volume = well.capacity
            elif isinstance(volume, float):
                volume = volume*drops
            well.contains(Liquid(unknown_reagent, volume))
        else:
            assert args.start_pad is not None
            loc = XYCoord(args.start_pad[0], args.start_pad[1])
            start_pad = board.pad_array[loc]
        # print(f"Starting at {start_pad}")
        seq: Optional[Operation[Drop, Drop]] = None
        current_pad = start_pad
        step_re: Pattern = re.compile('(\\d*)([UDLRNSEWA])')
        full_path = path
        enter_well_at_end: bool = False
        while path:
            m: Optional[Match[str]] = step_re.match(path)
            if m is None:
                raise ValueError(f"Couldn't parse '{path}' in '{full_path} using {step_re}'")
            path = path[m.end():]
            n = int(m.group(1)) if len(m.group(1)) else 1
            d = m.group(2)
            if d == 'U' or d == 'N':
                direction: Dir = Dir.UP
            elif d == 'D' or d == 'S':
                direction = Dir.DOWN
            elif d == 'L' or d == 'W':
                direction = Dir.LEFT
            elif d == 'R' or d == 'E':
                direction = Dir.RIGHT
            elif d == 'A':
                if n != 1:
                    raise ValueError(f"Can't specify a number of steps with 'A': '{full_path}'")
                if path:
                    raise ValueError(f"'A' not at end: '{full_path}'")
                if current_pad.well is None:
                    raise ValueError(f"Path '{full_path}' would attempt to enter well at {current_pad}")
                enter_well_at_end = True
                continue
            else:
                raise ValueError(f"Unknown step '{d}' in '{full_path}'")
            # print(f"Walk {n} {direction}")
            op = Drop.Move(direction, steps=n)
            seq = op if seq is None else seq.then(op)
            # print(op, seq)
            for i in range(n):  # @UnusedVariable
                p = current_pad.neighbor(direction)
                if p is None:
                    raise ValueError(f"Can't walk {d} ({direction}) from {current_pad} in '{full_path}'")
                current_pad = p
                
        if seq is not None:
            full_op: Optional[Operation[Drop,Any]] = seq.then(Drop.EnterWell) if enter_well_at_end else seq
        else:
            full_op = Drop.EnterWell() if enter_well_at_end else None
                
        if args.start_well is not None:
            if full_op is None:
                Drop.DispenseFrom(well).schedule()
            else:
                Drop.DispenseFrom(well).then(full_op).schedule()
        else:
            if full_op is None:
                Drop.AppearAt(start_pad, board=board).schedule()
            else:
                Drop.AppearAt(start_pad, board=board).then(full_op).schedule()
        
            
class DisplayOnly(Task):
    def __init__(self) -> None:
        super().__init__(name="display-only",
                         description = "Just bring up the display.",
                         aliases=["display"])

    def add_args_to(self, parser: ArgumentParser, *,  # @UnusedVariable
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        ...

        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        ...


class Mix(Task):
    class Mixer(NamedTuple):
        type: MixingType
        n_rows: int
        n_cols: int
        
    mixers: Final[ClassVar[Mapping[int, Mixer]]] = {
            2: Mixer(Mix2(Dir.LEFT), 1, 2),
            3: Mixer(Mix3(Dir.LEFT, Dir.LEFT), 1, 3),
            4: Mixer(Mix4(Dir.LEFT, Dir.DOWN), 2, 2),
            6: Mixer(Mix6(Dir.LEFT, Dir.DOWN), 2, 3),
            9: Mixer(Mix9(Dir.LEFT, Dir.DOWN), 3, 3),
        }
    
    def __init__(self) -> None:
        super().__init__(name="mix",
                         description="Dispense n drops, walk them out and mix them together")

    def add_args_to(self, parser: ArgumentParser, *,  
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        choices=list(self.mixers)
        parser.add_argument('num_drops', type=int, metavar='NUM-DROPS',                              
                           choices=choices,
                           help=f""""The number of drops to mix.
                                     Choices are {map_str(choices)}""")
        group = self.arg_group_in(parser)
        default_tolerance = 0.1
        group.add_argument('-t', '--tolerance', type=float, default=default_tolerance, metavar="FLOAT",
                           help=f"""Maximum allowed deviation between max and min proportion (relative to min).
                                    Default is {default_tolerance} ({100*default_tolerance:g}%%)""")
        group.add_argument('-f', '--full', action='store_true',  
                            help="Fully mix all drops")
        group.add_argument('--shuttles', type=int, metavar='INT', default=0,
                            help="The number of extra shuttles to perform.  Default is zero.")
        default_pause_before = 0
        group.add_argument('-pb', '--pause-before', type=int, metavar='TICKS', default=default_pause_before,
                           help=f"Time to pause before the mixing operation.  Default is {default_pause_before*ticks:.0f}.")
        default_pause_after= 0
        group.add_argument('-pa', '--pause-after', type=int, metavar='TICKS', default=default_pause_after,
                           help=f"Time to pause before the mixing operation.  Default is {default_pause_after*ticks:.0f}.")
        
    def create_path(self, i: int, well: Well, args: Namespace) -> StaticOperation[None]:
        n_drops: int = args.num_drops
        mixer = self.mixers[n_drops]
        row = i//mixer.n_cols
        col = i%mixer.n_cols
        
        reagent = Reagent(f"R{i+1}")
        
        def change_reagent(r: Reagent) -> Callable[[Drop], None]:
            def fn(drop: Drop) -> None:
                drop.reagent = r
            return fn
        mixop: Operation[Drop,Drop]
        if i == 0:
            mixop = Drop.Mix(mixer.type, 
                             tolerance=args.tolerance,
                             n_shuttles=args.shuttles)
        else:
            mixop = Drop.InMix(fully_mixed=args.full)
        towell: Operation[Drop,Drop]
        if i == 0:
            # towell = Drop.Move(Dir.RIGHT, steps=6) \
            #             .then(Drop.Move(Dir.UP))
            towell = Drop.ToCol(18) \
                        .then(Drop.Move(Dir.UP))
        else:
            # towell = Drop.Move(Dir.DOWN, steps=2*(2-row)) \
            #             .then(Drop.Move(Dir.RIGHT, steps=6+2*col)) \
            #             .then(Drop.Move(Dir.DOWN))
            towell = Drop.ToRow(1) \
                        .then(Drop.ToCol(18)) \
                        .then(Drop.Move(Dir.DOWN))
            
                        
                # .then(Drop.Move(Dir.DOWN, steps=row*2+1)) \
                # .then(Drop.Move(Dir.RIGHT, steps = 12-2*col)) \
        op = Drop.DispenseFrom(well) \
                .then_process(change_reagent(reagent)) \
                .then(Drop.ToRow(5-2*row)) \
                .then(Drop.ToCol(12-2*col)) \
                .then(mixop) \
                .then(towell) \
                .then(Drop.EnterWell)
                
                
        return op
        

    def run(self, board: Board, system: System, args: Namespace) -> None:
        n_drops: int = args.num_drops
        drops = board.drop_size.as_unit("drops", singular="drop")
        
        well = board.wells[2]
        well.contains(Liquid(unknown_reagent, n_drops*drops))
        paths = [self.create_path(i, well, args) for i in range(n_drops)]
        
        with system.batched():
            for p in paths:
                p.schedule()


