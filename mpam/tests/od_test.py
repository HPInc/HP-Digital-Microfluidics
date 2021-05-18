from __future__ import annotations
from mpam.device import System, WellPad
import opendrop
from mpam.types import Dir
from quantities.SI import uL
from mpam.drop import Drop
from quantities.dimensions import Volume
from quantities.core import Unit
from quantities.US import acre, ft


board = opendrop.Board("COM5")

system = System(board=board)

# tick_interval: Time = 0.1*sec
# async_mode = RunMode.asynchronous(tick_interval)
# system.clock.start(tick_interval)


drops: Unit[Volume] = board.drop_size.as_unit("drops")

Volume.default_units(uL)
print(f"Drop size is {1*drops}")
v: Volume = 3*drops
print(f"{v}, {v.in_units(drops)}")
acre_ft = (acre*ft).a(Volume)
print(v.in_units(acre_ft))

system.clock.start()

with system:
    (d1, d2) = Drop.appear_at(board, [(8,1), (5,1)]).value
    
    d1.schedule(Drop.Move(Dir.SOUTH, steps=5)) \
        .then_schedule(Drop.Move(Dir.EAST, steps=4)) \
        .then_call(lambda d: print(f"Working on {d}")) \
        .then_schedule(Drop.Move(Dir.NORTH, steps=3))

    d2.schedule(Drop.Move(Dir.SOUTH, steps=3))
    
    board.well_groups['left'].shared_pads[2].schedule(WellPad.TurnOn)
    board.wells[3].gate.schedule(WellPad.TurnOn)
system.stop()