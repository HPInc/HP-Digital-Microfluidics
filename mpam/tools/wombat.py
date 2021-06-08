from __future__ import annotations
from argparse import ArgumentParser, ArgumentTypeError, _SubParsersAction,\
    Namespace
from quantities.dimensions import Time, Volume
from typing import Mapping, Final, Union, Optional, Any, Sequence
from quantities.core import Unit
from quantities.SI import us, sec, ms, ns, minutes, hr, uL
from re import Pattern, Match
import re
from mpam.device import System, Pad, Well, Heater, Magnet
from devices.wombat import Board
from mpam.types import Dir, Liquid, unknown_reagent, ticks,\
    XYCoord, Operation, StaticOperation, RunMode, Reagent
from mpam.drop import Drop
from quantities.temperature import TemperaturePoint, abs_C

time_arg_units: Final[Mapping[str, Unit[Time]]] = {
    "ns": ns,
    "nsec": ns,
    "us": us,
    "usec": us,
    "ms": ms,
    "msec": ms,
    "s": sec,
    "sec": sec,
    "secs": sec,
    "second": sec,
    "seconds": sec,
    "min": minutes,
    "minute": minutes,
    "minutes": minutes,
    "hr": hr,
    "hour": hr,
    "hours": hr,
    }

time_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)({'|'.join(time_arg_units)})")

def time_arg(arg: str) -> Time:
    m = time_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a time value.  
                    Requires a number followed immediately by units, e.g. '30ms'""")
    n = float(m.group(1))
    unit = time_arg_units.get(m.group(2), None)
    if unit is None:
        raise ValueError(f"{m.group(2)} is not a known time unit")
    val = n*unit
    return val

volume_arg_units: Final[Mapping[str, Unit[Volume]]] = {
    "ul": uL,
    "uL": uL,
    "microliter": uL,
    "microliters": uL,
    "microlitre": uL,
    "microliters": uL,
    "ml": uL,
    "mL": uL,
    "milliliter": uL,
    "milliiters": uL,
    "millilitre": uL,
    "milliliters": uL,
    }

volume_arg_re: Final[Pattern] = re.compile(f"(\\d+(?:.\\d+)?)({'|'.join(volume_arg_units)}|drops|drop)")

def volume_arg(arg: str) -> Union[Volume,float]:
    m = volume_arg_re.fullmatch(arg)
    if m is None:
        raise ArgumentTypeError(f"""
                    {arg} not parsable as a volume value.  
                    Requires a number followed immediately by units, e.g. '30uL' or '2drops'""")
    n = float(m.group(1))
    ustr = m.group(2)
    if ustr == "drops" or ustr == "drop":
        return n
    unit = volume_arg_units.get(ustr, None)
    if unit is None:
        raise ValueError(f"{ustr} is not a known volume unit")
    val = n*unit
    return val

class Task:
    def run(self, board: Board, system: System, args: Namespace) -> None:
        raise NotImplementedError(f"Task.run() not implemented for {self}")
    
    @classmethod
    def add_common_args(cls, parser: ArgumentParser) -> None:
        group = parser.add_argument_group(title="common options")
        group.add_argument('-p', '--port',
                            help='''
                           The communication port (e.g., COM5) to use to talk to the board.
                           By default, only the display is run
                           ''')
        default_clock_interval=100*ms
        group.add_argument('-cs', '--clock-speed', type=time_arg, default=default_clock_interval, metavar='TIME',
                            help=f'''
                            The amount of time between clock ticks.  
                            Default is {default_clock_interval.in_units(ms)}.
                            ''')
        default_min_time=5*minutes
        group.add_argument('--min-time', type=time_arg, default=default_min_time, metavar='TIME',
                            help=f'''
                            The minimum amount of time to leave the display up, even if the 
                            operation has finished.  Default is {default_min_time.in_units(minutes)}.
                            ''')
        group.add_argument('--max-time', type=time_arg, metavar='TIME',
                            help=f'''
                            The maximum amount of time to leave the display up, even if the 
                            operation hasn't finished.  Default is no limit
                            ''')
        group.add_argument('-nd', '--no-display', action='store_false', dest='use_display',
                            help=f'''
                            Run the task without the on-screen display
                            ''')
        default_update_interval=20*ms
        group.add_argument('--update-interval', type=time_arg, metavar='TIME', default=default_update_interval,
                            help=f'''
                            The maximum amount of time between display updates.  
                            Default is {default_update_interval}.
                            ''')
            


class Dispense(Task):

    @classmethod
    def add_task_args(cls, subparsers: _SubParsersAction):
        desc = "Dispense a drop from a given well and leave it there."
        parser = subparsers.add_parser("dispense", aliases=["disp"], 
                                       help=desc, description=desc
                                       )
        group = parser.add_argument_group(title="task-specific options")
        group.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=[2,3,6,7],
                            help="The well to dispense from")
        group.add_argument('-v', '--volume', type=volume_arg, metavar='VOLUME',
                            help="The initial volume of the well.  Default is a full well.")
        group.set_defaults(task=Dispense())
        cls.add_common_args(parser)
        
    def run(self, board: Board, system: System, args: Namespace) -> None:
        well_no = args.well
        well = board.wells[well_no]

        drops = board.drop_size.as_unit("drops")
        volume: Union[Volume, float] = args.volume
        if volume is None:
            volume = well.capacity
        elif isinstance(volume, float):
            volume = volume*drops
        well.contains(Liquid(unknown_reagent, volume))
        
        system.clock.start(args.clock_speed)

        seq = Drop.DispenseFrom(well)
                
        with system.batched():
            seq.schedule()

class Absorb(Task):

    @classmethod
    def add_task_args(cls, subparsers: _SubParsersAction):
        desc = "Absorb a drop assumed to be on a well's exit pad."

        parser = subparsers.add_parser("absorb", aliases=["abs"], 
                                       help=desc, description=desc
                                       )
        group = parser.add_argument_group(title="task-specific options")
        group.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=[2,3,6,7],
                            help="The well to dispense from")
        cls.add_common_args(parser)
        parser.set_defaults(task=Absorb())
        
    def run(self, board: Board, system: System, args: Namespace) -> None:
        well_no = args.well
        well = board.wells[well_no]

        system.clock.start(args.clock_speed)
        
        drop = Drop.appear_at(board, [well.exit_pad.location]).value[0]
        drop.schedule(Drop.EnterWell)

class DispenseAndWalk(Task):

    @classmethod
    def add_task_args(cls, subparsers: _SubParsersAction):
        desc = "Dispense a drop from a given well and walk to the well across from it."
        parser = subparsers.add_parser("walk", 
                                       help=desc, description=desc
                                       )
        group = parser.add_argument_group(title="task-specific options")
        group.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=[2,3,6,7],
                            help="The well to dispense from")
        group.add_argument('-v', '--volume', type=volume_arg, metavar='VOLUME',
                            help="The initial volume of the well.  Default is a full well.")
        group.add_argument('-d', '--drops', type=int, default=1, metavar='N',
                            help="The number of drops to walk.  Default is 1")
        # parser.add_argument('-g', '--gap', type=int, default=8, metavar='N',
        #                     help="""
        #                     The gap between drops.  Default is 8
        #                     """)
        cls.add_common_args(parser)
        parser.set_defaults(task=DispenseAndWalk())
        
    def run(self, board: Board, system: System, args: Namespace) -> None:
        well_no = args.well
        well = board.wells[well_no]
        hdir = Dir.RIGHT if well_no == 2 or well_no == 3 else Dir.LEFT
        vdir1 = Dir.DOWN if well_no == 2 or well_no == 6 else Dir.UP
        vdir2 = Dir.UP if well_no == 2 or well_no == 6 else Dir.DOWN
        
        drops = board.drop_size.as_unit("drops")
        volume: Union[Volume, float] = args.volume
        if volume is None:
            volume = well.capacity
        elif isinstance(volume, float):
            volume = volume*drops
        well.contains(Liquid(unknown_reagent, volume))
        
        system.clock.start(args.clock_speed)

        seq = Drop.DispenseFrom(well) \
                .then(Drop.Move(hdir)) \
                .then(Drop.Move(vdir1, steps=2)) \
                .then(Drop.Move(hdir, steps=16)) \
                .then(Drop.Move(vdir2, steps=2)) \
                .then(Drop.Move(hdir)) \
                .then(Drop.EnterWell)
                
        with system.batched():
            for i in range(args.drops):
                delay = 0*ticks if i==0 else (4+4*i)*ticks
                seq.schedule(after=delay)

class WalkPath(Task):

    @classmethod
    def add_task_args(cls, subparsers: _SubParsersAction):
        desc = "Walk a user-provided path from a starting well or pad."
        parser = subparsers.add_parser("path", 
                                       help=desc, description=desc
                                       )
        group = parser.add_argument_group(title="task-specific options")
        
        starts = group.add_mutually_exclusive_group(required=True)
        starts.add_argument('-sp', '--start-pad', type=int, nargs=2, metavar=('X','Y'), 
                            help="The (x,y) coordinates of the pad to start from.  The drop is assumed to be there")
        starts.add_argument('-sw', '--start-well', type=int, metavar='INT', 
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
        cls.add_common_args(parser)
        parser.set_defaults(task=WalkPath())
        
    def run(self, board: Board, system: System, args: Namespace) -> None:
        path: str = args.path.upper()

        if args.start_well is not None:
            well = board.wells[args.start_well]
            # seq: StaticOperation = Drop.DispenseFrom(well)
            start_pad: Pad = well.exit_pad
            drops = board.drop_size.as_unit("drops")
            volume: Union[Volume, float] = args.volume
            if volume is None:
                volume = well.capacity
            elif isinstance(volume, float):
                volume = volume*drops
            well.contains(Liquid(unknown_reagent, volume))
        else:
            assert args.start_pad is not None
            loc = XYCoord(args.start_pad[0], args.start_pad[1])
            start_pad = board.pad_array[loc]
            # seq = Drop.appear_at(board, loc)
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
                
        system.clock.start(args.clock_speed)
        
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
            drop = Drop.appear_at(board, [start_pad.location]).value[0]
            if full_op is not None:
                drop.schedule(full_op)
        
            
class DisplayOnly(Task):

    @classmethod
    def add_task_args(cls, subparsers: _SubParsersAction):
        desc="Just bring up the display"
        parser = subparsers.add_parser("display-only",  aliases=["display"],
                                       help=desc, description = desc)
        # group = parser.add_argument_group(title="task-specific options",)
        cls.add_common_args(parser)
        parser.set_defaults(task=DisplayOnly())
        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        system.clock.start(args.clock_speed)

class WombatTest(Task):

    @classmethod
    def add_task_args(cls, subparsers: _SubParsersAction):
        desc="The original Wombat test."
        parser = subparsers.add_parser("wombat-test",  aliases=["test"],
                                       help=desc, description = desc)
        # group = parser.add_argument_group(title="task-specific options",)
        cls.add_common_args(parser)
        parser.set_defaults(task=WombatTest())
        
    def walk_across(self, well: Well, direction: Dir,
                    turn1: Dir,
                    turn2: Dir,
                    ) -> StaticOperation[None]:
        return Drop.DispenseFrom(well) \
                .then(Drop.Move(direction)) \
                .then(Drop.Move(turn1, steps=2)) \
                .then(Drop.Move(direction, steps=16)) \
                .then(Drop.Move(turn2, steps=2)) \
                .then(Drop.Move(direction)) \
                .then(Drop.EnterWell)
    
    def ramp_heater(self, temps: Sequence[TemperaturePoint]) -> Operation[Heater, Heater]:
        op: Operation[Heater,Heater] = Heater.SetTemperature(temps[0])
        for i in range(1, len(temps)):
            op = op.then(Heater.SetTemperature(temps[i]), after=5*sec)
        return op.then(Heater.SetTemperature(None), after=5*sec)        
        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        
        r1 = Reagent("R1")
        r2 = Reagent("R2")
        drops = board.drop_size.as_unit("drops")
        board.wells[2].contains(Liquid(r1, 40*drops))
        board.wells[3].contains(Liquid(r2, 40*drops))
        
        async_mode = RunMode.asynchronous(args.clock_speed)
        
        system.clock.start(args.clock_speed)
        s1 = self.walk_across(board.wells[2], Dir.RIGHT, Dir.DOWN, Dir.UP)
        s2 = self.walk_across(board.wells[3], Dir.RIGHT, Dir.UP, Dir.DOWN)
        
        with system.batched():
            for i in range(30):
                delay = 0*ticks if i==0 else (4+4*i)*ticks
                s1.schedule(after=delay)
                s2.schedule(after=delay)
            self.ramp_heater([80*abs_C, 60*abs_C, 90*abs_C, 40*abs_C, 120*abs_C]) \
                .schedule_for(board.heaters[3], mode = async_mode)
            Magnet.TurnOn.schedule_for(board.pad_at(13,3).magnet, after=20*ticks)




def make_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Put the Wombat board through its paces")
    subparsers = parser.add_subparsers(help="Tasks", dest='task_name', required=True, metavar='TASK')
    
    Dispense.add_task_args(subparsers)
    Absorb.add_task_args(subparsers)
    DispenseAndWalk.add_task_args(subparsers)
    DisplayOnly.add_task_args(subparsers)
    WalkPath.add_task_args(subparsers)
    WombatTest.add_task_args(subparsers)

    return parser
        
            
        
    
def run_task(task: Task, args: Namespace) -> None:
    board = Board(device=args.port)
    system = System(board=board)
    if not args.use_display:
        with system:
            task.run(board, system, args)
    else:
        system.run_monitored(lambda _: task.run(board, system, args),
                             min_time=args.min_time,
                             max_time=args.max_time,
                             update_interval=args.update_interval
                             )

if __name__ == '__main__':
    Time.default_units(ms)
    parser = make_arg_parser()
    args = parser.parse_args()
    # print(args)
    run_task(args.task, args)





