from __future__ import annotations
from mpam.device import System
import opendrop
from mpam.types import unknown_reagent, Liquid, Dir, RunMode, OnOff, Delayed
from quantities.SI import sec, uL
from mpam.drop import Drop
from quantities.dimensions import Time


board = opendrop.Board("COM5")

system = System(board=board)

tick_interval: Time = 0.5*sec

async_mode = RunMode.asynchronous(tick_interval)
system.clock.start(tick_interval)

with system:
    d1 = Drop(board.pad_at(8,1), Liquid(unknown_reagent, 0.5*uL))
    d2 = Drop(board.pad_at(5,1), Liquid(unknown_reagent, 0.5*uL))
    f: Delayed[OnOff]
    with system.batched():
        d1.pad.schedule_turn_on(mode=async_mode)
        f=d2.pad.schedule_turn_on(mode=async_mode)
    f.wait()
    
    d1.schedule_move(Dir.SOUTH, steps=5).when_value(
        lambda d: d.schedule_move(Dir.EAST, steps=3)
        .when_value(
            lambda d: d.schedule_move(Dir.NORTH, steps=3)
            )
        )
    d2.schedule_move(Dir.SOUTH, steps=3)
system.stop()