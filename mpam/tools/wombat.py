from __future__ import annotations
from argparse import ArgumentParser, ArgumentTypeError, _SubParsersAction,\
    Namespace
from quantities.dimensions import Time, Volume
from typing import Mapping, Final, Union
from quantities.core import Unit
from quantities.SI import us, sec, ms, ns, minutes, hr, uL
from re import Pattern
import re
from mpam.device import System
from devices.wombat import Board
from mpam.types import Dir, Liquid, unknown_reagent, ticks
from mpam.drop import Drop

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


def make_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Put the Wombat board through its paces")
    parser.add_argument('-p', '--port',
                        help='''
                       The communication port (e.g., COM5) to use to talk to the board.
                       By default, only the display is run
                       ''')
    default_clock_interval=100*ms
    parser.add_argument('-cs', '--clock-speed', type=time_arg, default=default_clock_interval, metavar='TIME',
                        help=f'''
                        The amount of time between clock ticks.  
                        Default is {default_clock_interval.in_units(ms)}.
                        ''')
    default_min_time=5*minutes
    parser.add_argument('--min-time', type=time_arg, default=default_min_time, metavar='TIME',
                        help=f'''
                        The minimum amount of time to leave the display up, even if the 
                        operation has finished.  Default is {default_min_time.in_units(minutes)}.
                        ''')
    parser.add_argument('--max-time', type=time_arg, metavar='TIME',
                        help=f'''
                        The maximum amount of time to leave the display up, even if the 
                        operation hasn't finished.  Default is no limit
                        ''')
    parser.add_argument('-nd', '--no-display', action='store_false', dest='use_display',
                        help=f'''
                        Run the task without the on-screen display
                        ''')
    subparsers = parser.add_subparsers(help="Tasks", dest='task_name', required=True, metavar='TASK')
    
    Dispense.add_task_args(subparsers)
    Absorb.add_task_args(subparsers)
    DispenseAndWalk.add_task_args(subparsers)
    DisplayOnly.add_task_args(subparsers)
    

    return parser

class Dispense(Task):

    @classmethod
    def add_task_args(cls, subparsers: _SubParsersAction):
        parser = subparsers.add_parser("dispense", aliases=["disp"], 
                                       help='''
                                       Dispense a drop from a given well and leave it there.
                                       '''
                                       )
        parser.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=[2,3,6,7],
                            help="The well to dispense from")
        parser.add_argument('-v', '--volume', type=volume_arg, metavar='VOLUME',
                            help="The initial volume of the well.  Default is a full well.")
        parser.set_defaults(task=Dispense())
        
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
        parser = subparsers.add_parser("absorb", aliases=["abs"], 
                                       help='''
                                       Absorb a drop assumed to be on a well's exit pad.
                                       '''
                                       )
        parser.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=[2,3,6,7],
                            help="The well to dispense from")
        parser.set_defaults(task=Absorb())
        
    def run(self, board: Board, system: System, args: Namespace) -> None:
        well_no = args.well
        well = board.wells[well_no]

        system.clock.start(args.clock_speed)
        
        drop = Drop.appear_at(board, [well.exit_pad.location]).value[0]
        print(drop)
        drop.schedule(Drop.EnterWell)
        print("scheduled")

class DispenseAndWalk(Task):

    @classmethod
    def add_task_args(cls, subparsers: _SubParsersAction):
        parser = subparsers.add_parser("walk", 
                                       help='''
                                       Dispense a drop from a given well and walk
                                       to the well across from it.
                                       '''
                                       )
        parser.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=[2,3,6,7],
                            help="The well to dispense from")
        parser.add_argument('-v', '--volume', type=volume_arg, metavar='VOLUME',
                            help="The initial volume of the well.  Default is a full well.")
        parser.add_argument('-d', '--drops', type=int, default=1, metavar='N',
                            help="The number of drops to walk.  Default is 1")
        # parser.add_argument('-g', '--gap', type=int, default=8, metavar='N',
        #                     help="""
        #                     The gap between drops.  Default is 8
        #                     """)
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
                delay = 0*ticks if i==0 else (8+8*i)*ticks
                seq.schedule(after=delay)

        
            
class DisplayOnly(Task):

    @classmethod
    def add_task_args(cls, subparsers: _SubParsersAction):
        parser = subparsers.add_parser("dispense-only", aliases=["disp", "do"], 
                                       help='''
                                       Just bring up the display
                                       '''
                                       )
        parser.set_defaults(task=DisplayOnly())
        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        system.clock.start(args.clock_speed)


        
            
        
    
def run_task(task: Task, args: Namespace) -> None:
    board = Board(device=args.port)
    system = System(board=board)
    if not args.use_display:
        task.run(board, system, args)
    else:
        system.run_monitored(lambda _: task.run(board, system, args),
                             min_time=args.min_time,
                             max_time=args.max_time
                             )

if __name__ == '__main__':
    Time.default_units(ms)
    parser = make_arg_parser()
    args = parser.parse_args()
    # print(args)
    run_task(args.task, args)





