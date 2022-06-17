from __future__ import annotations

from argparse import ArgumentParser, Namespace, _ArgumentGroup
from contextlib import redirect_stdout
import os.path
from typing import Optional, Union, Callable

from mpam.device import Board, System, Pad, Well
from mpam.dilution import dilution_sequences
from mpam.drop import Drop
from mpam.exerciser import Task, volume_arg, Exerciser, time_arg
from mpam.mixing import mixing_sequences
from mpam.paths import Path
from mpam.types import Liquid, unknown_reagent, XYCoord, Dir, \
    Reagent, Trigger, Delayed, Barrier
from quantities.SI import seconds, Hz, ms
from quantities.core import CountDim
from quantities.dimensions import Volume, Time
from quantities.timestamp import Timestamp, time_now, time_since


class Dispense(Task):
    def __init__(self) -> None:
        super().__init__(name="dispense",
                         description="Dispense a drop from a given well and leave it there.",
                         aliases=["disp"])

    def add_args_to(self, 
                    group: _ArgumentGroup,
                    parser: ArgumentParser, *, # @UnusedVariable
                    exerciser: Exerciser 
                    ) -> None:
        group.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=self.available_wells(exerciser),
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
        super().__init__(name="absorb",
                         description="Absorb a drop assumed to be on a well's exit pad.",
                         aliases=["abs"])

    def add_args_to(self,
                    group: _ArgumentGroup, 
                    parser: ArgumentParser, *,  # @UnusedVariable
                    exerciser: Exerciser 
                    ) -> None:
        group.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=self.available_wells(exerciser),
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
                         

    def add_args_to(self,
                    group: _ArgumentGroup, 
                    parser: ArgumentParser, *,
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        
        starts = group.add_mutually_exclusive_group(required=True)
        starts.add_argument('-sp', '--start-pad', type=int, nargs=2, metavar=('X','Y'), 
                            help="The (x,y) coordinates of the pad to start from.  The drop is assumed to be there")
        starts.add_argument('-sw', '--start-well', type=int, metavar='INT', 
                            choices=self.available_wells(exerciser),
                            help="The well to dispense from")
        
        group.add_argument('--path', required=True,
                            help='''
                            The path to walk.  Each step is indicated by a single character, optionally preceeded by
                            an integer indicating repetition.  'NSEW' or 'UDLR' indicate directions.  'A' at end signifies 
                            absorbing into a well.  An example path is '2RD10RUA'.  Paths are case-insensitive.
                            ''')
        group.add_argument('-v', '--volume', type=volume_arg, metavar='VOLUME',
                            help="The initial volume of the starting well.  Default is a full well.")
        
        time_group = parser.add_argument_group("timing characterization options")
        time_group.add_argument('-t', '--time-motion', action='store_true',
                                help='''Print total path time, path length, and whether or not the 
                                display was used.
                                ''')
        time_group.add_argument('--csv-file', metavar='FILE',
                                help='''Log total path time, path length, and whether or not the
                                display was used as CSV data appended to this file.
                                ''')
        # group.add_argument('-d', '--drops', type=int, default=1, metavar='N',
                            # help="The number of drops to walk along the path.  Default is 1")
        # parser.add_argument('-g', '--gap', type=int, default=8, metavar='N',
        #                     help="""
        #                     The gap between drops.  Default is 8
        #                     """)
        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        path: str = args.path.upper()
        
        enter_well_at_end = path.endswith("A")
        if enter_well_at_end:
            path = path[:-1]
        

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
            
        print_time: bool = args.time_motion
        csv_file: str = args.csv_file
        
        (drop_path, end_pad, path_len) = Path.from_spec(path, start=start_pad)
        
        if enter_well_at_end and end_pad.well is None:
            raise ValueError(f"Path '{path}' would attempt to enter well at {end_pad}")
        
        start_time: Timestamp
        def start_timer(drop: Drop) -> Delayed[Drop]:
            nonlocal start_time
            start_time = time_now() # @UnusedVariable
            return Delayed.complete(drop)
        
        class Steps(CountDim): ...
        steps = Steps.base_unit("step")

        def end_timer(drop: Drop) -> Drop:
            elapsed = time_since(start_time)
            plen = path_len*steps
            clock = system.clock
            
            dstatus = "on" if args.use_display else "off"
            
            if print_time:
                print(f"{plen:g} took {elapsed.in_units(seconds):g} ({elapsed/plen:g})")
                print(f"  Display was {dstatus}.")  
                print(f"  Clock speed was {clock.update_interval:g} ({clock.update_rate.in_units(Hz):g}).")

            if csv_file:
                new_csv = not os.path.exists(csv_file)
                with open(csv_file, "a") as out:
                    with redirect_stdout(out):
                        if new_csv:
                            print(",".join(["Path length (fluxels)",
                                            "Clock speed (ms)",
                                            "Display on",
                                            "Elapsed time (ms)",
                                            "Movement time (ms/fluxel)"]))
                        print(",".join([f"{path_len}",                         
                                        f"{clock.update_interval.as_number(ms):g}",
                                        "TRUE" if args.use_display else "FALSE",
                                        f"{elapsed.as_number(ms):g}",
                                        f"{elapsed.as_number(ms)/path_len:g}"
                                    
                            ]))
                        
            
            
            return drop
        
        
        drop_path = (Path.empty()
                     .then_process(start_timer)
                     .extended(drop_path)
                     .then_process(end_timer)
                    )
        
        if args.start_well is not None:
            path_start = Path.dispense_from(well)+drop_path
        else:
            path_start = Path.appear_at(start_pad, board=board)+drop_path
            
        if enter_well_at_end:
            path_start.enter_well().schedule()
        else:
            path_start.schedule()
        
            
class DisplayOnly(Task):
    def __init__(self) -> None:
        super().__init__(name="display-only",
                         description = "Just bring up the display.",
                         aliases=["display"])

    def add_args_to(self, 
                    group: _ArgumentGroup,
                    parser: ArgumentParser, *,  # @UnusedVariable
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        ...

        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        ...



class Mix(Task):
    def __init__(self) -> None:
        super().__init__(name="mix",
                         description="Dispense n drops, walk them out and mix them together")

    def add_args_to(self,
                    group: _ArgumentGroup, 
                    parser: ArgumentParser, *,  
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        parser.add_argument('num_drops', type=int, metavar='NUM-DROPS',                              
                           help=f""""The number of drops to mix.""")
        default_tolerance = 0.1
        group.add_argument('-t', '--tolerance', type=float, default=default_tolerance, metavar="FLOAT",
                           help=f"""Maximum allowed deviation between max and min proportion (relative to min).
                                    Default is {default_tolerance} ({100*default_tolerance:g}%%)""")
        group.add_argument('-f', '--full', action='store_true',  
                            help="Fully mix all drops")
        group.add_argument('--shuttles', type=int, metavar='INT', default=0,
                            help="The number of extra shuttles to perform.  Default is zero.")
        default_pause_before = Time.ZERO
        group.add_argument('-pb', '--pause-before', type=time_arg, metavar='TIME', default=default_pause_before,
                           help=f"Time to pause before the mixing operation.  Default is {default_pause_before:g}.")
        default_pause_after= Time.ZERO
        group.add_argument('-pa', '--pause-after', type=time_arg, metavar='TIME', default=default_pause_after,
                           help=f"Time to pause before the mixing operation.  Default is {default_pause_after:g}.")
        
        

    def run(self, board: Board, system: System, args: Namespace) -> None:
        n_drops: int = args.num_drops
        drops = board.drop_size.as_unit("drops", singular="drop")
        
        pms = mixing_sequences.lookup_placed(n_drops, 
                                             lower_left=board.pad_at(3,1),
                                             full=args.full,
                                             tolerance=args.tolerance,
                                             rows=5, cols=13)
        def sort_key(pad: Pad) -> tuple[int,int]:
            x,y = pad.location.coords
            # we want the first (smallest) to be the lowest row and furthest column
            return (-x, y)
        pads = sorted(pms.pads, key=sort_key)
        lead_pad = pms.fully_mixed_pads[0]
        
        pause_before: Time = args.pause_before
        pause_after: Time = args.pause_after
        
        print(n_drops)        
        pre_barrier = Barrier[Drop](n_drops)
        post_barrier = Barrier[Drop](n_drops)
        
        well: Well = board.wells[2]
        well.contains(Liquid(unknown_reagent, n_drops*drops))

        def create_path(i: int, pad: Pad, 
                        ) -> Path.Full:

            reagent = Reagent(f"R{i+1}")
            
            is_lead = pad is lead_pad 
            
            def change_reagent(r: Reagent) -> Callable[[Drop], None]:
                def fn(drop: Drop) -> None:
                    drop.reagent = r
                return fn
                
            loc = pad.location
            print(f"drop {i} goes to {loc}")
            path = (Path.dispense_from(well)
                    .then_process(change_reagent(reagent))
                    .to_row(loc.row)
                    .to_col(loc.col)
                    .reach(pre_barrier)
                    )
    
            if is_lead:
                path = (path
                        .wait_for(pause_before)
                        .start(pms.as_process(n_shuttles=args.shuttles))
                        .wait_for(pause_after)
                        )
            else:
                path = path.in_mix()
                
            path = path.reach(post_barrier)
    
            if is_lead:
                path = path.to_col(18).to_row(6)
            else:
                path = path.to_row(1).to_col(18).walk(Dir.DOWN)
            
            return path.enter_well()
            
        
        paths = [create_path(i, pad) for i,pad in enumerate(pads)]
        
        with system.batched():
            for p in paths:
                p.schedule()




class Dilute(Task):
    def __init__(self) -> None:
        super().__init__(name="dilute",
                         description="Perform an n-fold dilution")

    def add_args_to(self, 
                    group: _ArgumentGroup,
                    parser: ArgumentParser, *,  
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        parser.add_argument('fold', type=int, 
                           help=f""""The number of fold of the dilution (e.g., 8 for 8x). 
                                     Does not need to be an integer""")
        default_tolerance = 0.1
        group.add_argument('-t', '--tolerance', type=float, default=default_tolerance, metavar="FLOAT",
                           help=f"""Maximum allowed deviation between max and min proportion (relative to min).
                                    Default is {default_tolerance} ({100*default_tolerance:g}%%)""")
        group.add_argument('-f', '--full', action='store_true',  
                            help="Fully mix all drops")
        group.add_argument('--shuttles', type=int, metavar='INT', default=0,
                            help="The number of extra shuttles to perform.  Default is zero.")
        default_pause_before = Time.ZERO
        group.add_argument('-pb', '--pause-before', type=time_arg, metavar='TIME', default=default_pause_before,
                           help=f"Time to pause before the mixing operation.  Default is {default_pause_before:g}.")
        default_pause_after= Time.ZERO
        group.add_argument('-pa', '--pause-after', type=time_arg, metavar='TIME', default=default_pause_after,
                           help=f"Time to pause before the mixing operation.  Default is {default_pause_after:g}.")
        

    def run(self, board: Board, system: System, args: Namespace) -> None:
        fold: float = args.fold
        
        pause_before: Time = args.pause_before
        pause_after: Time = args.pause_after

        drop = drops = board.drop_size.as_unit("drops", singular="drop")
        
        reagent = Reagent.find("Reagent")
        solvent = Reagent.find("Solvent")
        
        pms = dilution_sequences.lookup_placed(fold,
                                               lower_left=board.pad_at(3,1),
                                               full=args.full,
                                               tolerance=args.tolerance,
                                               rows=5, cols=13)
        
        reagent_well = board.wells[2]
        reagent_well.contains(Liquid(reagent, 1*drop))
        solvent_well = board.wells[3]
        solvent_well.contains(Liquid(solvent, (pms.num_drops-1)*drops))
        
        lead_pad = pms.fully_mixed_pads[0]

        def sort_key(pad: Pad) -> tuple[bool, int,int]:
            # first, we want the ones on the other side of the lead pad.
            # So we start with False for that situation and True for others.
            # Otherwise (and even in that row, we go with the furthest one out
            # and bottom to top
            x,y = pad.location.coords
            return (y != lead_pad.row, -x, y)
        solvent_pads = sorted(pms.secondary_pads, key=sort_key)
        
        n_drops = len(solvent_pads)+1
        
        trigger = Trigger()
        
        pre_barrier = Barrier[Drop](n_drops)
        post_barrier = Barrier[Drop](n_drops)

        lead_path = Path.dispense_from(reagent_well) \
            .to_row(lead_pad.row) \
            .to_col(lead_pad.column) \
            .then_process(lambda _: trigger.fire()) \
            .reach(pre_barrier) \
            .wait_for(pause_before) \
            .start(pms.as_process(n_shuttles=args.shuttles)) \
            .wait_for(pause_after) \
            .reach(post_barrier) \
            .to_col(18) \
            .to_row(6) \
            .enter_well()
            
            
        bottom_row = 1
        
        
        def solvent_path(p: Pad) -> Path.Full:
            path = Path.dispense_from(solvent_well)
            if p.row == lead_pad.row and p.column > lead_pad.column:
                if lead_pad.row == bottom_row or lead_pad.row == bottom_row+1:
                    path = path.to_row(lead_pad.row+2) \
                                .to_col(p.column) \
                                .to_row(p.row)
                else:
                    path = path.to_row(lead_pad.row-2) \
                                .to_col(p.column) \
                                .to_row(p.row)
            else:
                path = path.to_row(p.row) \
                            .to_col(p.column)
            
            path = path.reach(pre_barrier) \
                    .in_mix() \
                    .reach(post_barrier) \
                    .to_row(1).to_col(18).walk(Dir.DOWN)
            return path.enter_well()
        
        solvent_paths = (solvent_path(p) for p in solvent_pads)
        
        def fire_solvents() -> None:
            with system.batched():
                for p in solvent_paths:
                    p.schedule()
        
        trigger.on_trigger(fire_solvents)
        
        lead_path.schedule()


