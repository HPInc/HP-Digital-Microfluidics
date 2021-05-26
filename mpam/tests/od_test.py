from __future__ import annotations
from mpam.device import System
import opendrop
from mpam.types import Dir, unknown_reagent, Liquid, ticks
from quantities.SI import uL, ms
from mpam.drop import Drop
from quantities.dimensions import Volume
from quantities.core import Unit
from quantities.US import acre, ft
from typing import Optional

com_port: Optional[str] = "COM5"
com_port = None
board = opendrop.Board(com_port)

system = System(board=board)

# monitor_board(board)

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

# system.clock.start(100*ms)

# with system:
    # (d1, d2) = Drop.appear_at(board, [(8,1), (5,1)]).value
    #
    # d1.schedule(Drop.Move(Dir.SOUTH, steps=5)) \
    #     .then_schedule(Drop.Move(Dir.EAST, steps=5)) \
    #     .then_call(lambda d: print(f"Working on {d}")) \
    #     .then_schedule(Drop.Move(Dir.NORTH, steps=3))
    #
    # d2.schedule(Drop.Move(Dir.SOUTH, steps=6))
    #

    # well = board.wells[3]
    # Drop.Dispense(well).schedule() \
    #     .then_schedule(Drop.Move(Dir.LEFT, steps=5))
    
    # board.well_groups['left'].shared_pads[2].schedule(WellPad.TurnOn)
    # board.wells[3].gate.schedule(WellPad.TurnOn)
    
    # from_well = board.wells[1]
    # to_well = board.wells[0]
    # from_well.contains(Liquid(unknown_reagent, 8*drops))
    
    # Drop.DispenseFrom(from_well).schedule() \
    #     .then_schedule(Drop.Move(Dir.WEST, steps = 13)) \
    #     .then_schedule(Drop.Enter(to_well))
    
    # def dispense_drops(n_drops: int):
    #     w = board.wells[1]
    #     sequence = Drop.DispenseFrom(w) \
    #                 .then(Drop.Move(Dir.WEST, steps = 4)) \
    #                 .then(Drop.Move(Dir.WEST, steps=9)) \
    #                 .then(Drop.EnterWell)
    #     def dispense_and_walk(_=None):
    #         nonlocal n_drops
    #         if (n_drops > 0):
    #             # schedule(Drop.DispenseFrom(w)) \
    #             #     .then_schedule(Drop.Move(Dir.WEST, steps = 4)) \
    #             #     .then_call(dispense_and_walk) \
    #             #     .then_schedule(Drop.Move(Dir.WEST, steps=9)) \
    #             #     .then_schedule(Drop.EnterWell)
    #             sequence.schedule()
    #             sequence.schedule(after=10*ticks)
    #             sequence.schedule(after=15*ticks)
    #             n_drops -= 1
    #     dispense_and_walk()
    
def experiment(system: System) -> None:
    board = system.board
    well = board.wells[1]
    well.contains(Liquid(unknown_reagent, 8*drops))

    system.clock.start(100*ms)
        
    sequence = Drop.DispenseFrom(well) \
                .then(Drop.Move(Dir.WEST, steps=13)) \
                .then(Drop.EnterWell)
    with system.batched():
        sequence.schedule()
        sequence.schedule(after=10*ticks)
        sequence.schedule(after=15*ticks)
    
system.run_monitored(experiment)
    
    

            
            
system.stop()