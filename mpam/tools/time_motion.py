from __future__ import annotations

from argparse import ArgumentParser, Namespace
from typing import Sequence, NamedTuple

from erk.stringutils import map_str
from mpam.exerciser import time_arg
from quantities.SI import ms
from quantities.dimensions import Time
from random import shuffle
import subprocess


def arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    
    
    default_reps = 10
    parser.add_argument('-r', '--reps', type=int, default=default_reps, metavar="INT", 
                        help=f"""The number of times to run each configuration.  Default is {default_reps}""")
    default_speeds = (10*ms, 50*ms, 100*ms, 200*ms)
    parser.add_argument('-s', '--speeds', type=time_arg, nargs="+", default=default_speeds, metavar="TIME", 
                        help=f"The clock speeds to investigate.  Default is {map_str(default_speeds)}"
                        )
    
    default_file = "logs/timing.csv"
    parser.add_argument('--csv-file', metavar='FILE', default=default_file,
                        help=f'''Log total path time, path length, and whether or not the
                        display was used as CSV data appended to this file.
                        Default is "{default_file}".
                        ''')
    
    default_start = (7,3)
    parser.add_argument('-sp', '--start-pad', type=int, nargs=2, metavar=('X','Y'), default=default_start,
                        help=f'''The (x,y) coordinates of the pad to start from.  The drop is assumed to be there.
                                Default is {default_start}''')
    default_path = "4RDU4L"
    parser.add_argument('--path', default=default_path,
                        help=f'''
                        The path to walk.  Each step is indicated by a single character, optionally preceeded by
                        an integer indicating repetition.  'NSEW' or 'UDLR' indicate directions.  'A' at end signifies 
                        absorbing into a well.  An example path is '2RD10RUA'.  Paths are case-insensitive.
                        Default is "{default_path}".
                        ''')
    disp_group = parser.add_mutually_exclusive_group()
    disp_group.add_argument('--no-display', action='store_true', 
                            help="Do not use the monitor display.")
    disp_group.add_argument('--only-display', action='store_true',
                            help="Only run with the monitor display")
    
    return parser

class Config(NamedTuple):
    speed: Time
    display: bool

def run_test(args: Namespace) -> None:
    reps: int = args.reps
    speeds: Sequence[Time] = args.speeds
    csv_file: str = args.csv_file
    start_pad: tuple[int, int] = args.start_pad
    path: str = args.path
    no_disp: bool = args.no_display
    only_disp: bool = args.only_display
    print(args)
    
    disp_states = [True, False]
    if no_disp:
        disp_states = [False]
    if only_disp:
        disp_states = [True]
    
    
    configs = list[Config]()
    for r in range(reps):                    # @UnusedVariable
        for speed in speeds:
            for ds in disp_states:
                config = Config(speed, ds)
                configs.append(config)
    shuffle(configs)
    
    for i,config in enumerate(configs):
        cmd_args = ["python", "tools/wombat.py", "path", "--min-time=0ms", "--initial-delay=0ms"]
        cmd_args.extend(("--clock-speed", f"{config.speed.as_number(ms):g}ms"))
        if not config.display:
            cmd_args.append("--no-display")
        cmd_args.extend(("--csv-file", csv_file))
        cmd_args.extend(("--start-pad", str(start_pad[0]), str(start_pad[1])))
        cmd_args.extend(("--path", path))
        
        print(f"{i+1:,} of {len(configs):,}: speed = {config.speed.in_units(ms):g}, display = {config.display}")
        subprocess.run(cmd_args)
        
        

if __name__ == '__main__':
    Time.default_units = ms
    parser = arg_parser()
    
    args = parser.parse_args()
    
    run_test(args)
    



