from __future__ import annotations
from mpam.device import System, Pad
import opendrop
from mpam.types import unknown_reagent, Liquid, Dir, RunMode, OnOff, Delayed
from quantities.SI import sec, uL
from mpam.drop import Drop
from quantities.dimensions import Time


board = opendrop.Board("COM5")

system = System(board=board)

tick_interval: Time = 0.1*sec

async_mode = RunMode.asynchronous(tick_interval)
system.clock.start(tick_interval)

with system:
    (d1, d2) = Drop.appear_at(board, [(8,1), (5,1)]).value
    
    # Drop.Move(Dir.SOUTH, steps=5).schedule_for(d1) \
    d1.schedule(Drop.Move(Dir.SOUTH, steps=5)) \
        .then_schedule(Drop.Move(Dir.EAST, steps=4)) \
        .then_call(lambda d: print(f"Working on {d}")) \
        .then_schedule(Drop.Move(Dir.NORTH, steps=3))

    d2.schedule(Drop.Move(Dir.SOUTH, steps=3))
system.stop()