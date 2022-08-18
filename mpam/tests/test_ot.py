from __future__ import annotations

from devices.joey import Board, HeaterType
from devices.opentrons import OT2
from mpam.device import System
from quantities.SI import uL
from quantities.dimensions import Volume

from mpam.types import Reagent

pipettor = OT2(robot_ip_addr = "192.168.86.32",
               config="../inputs/ot2.json",
               reagents="../inputs/reagents.json")

board = Board(pipettor=pipettor, heater_type=HeaterType.Paddles)
system = System(board=board)

pm_primers = Reagent.find("PM Primers")
dilution_buffer = Reagent.find("Dilution Buffer")
master_mix = Reagent.find("Master Mix")
prep_mixture = Reagent.find("Prep Mixture")
fragments = [Reagent.find(f"Fragment-{i+1}") for i in range(20)]

wells = board.wells
drops = board.drop_unit

Volume.default_units = uL 

with system:
    wells[0].add(pm_primers, 20*uL).wait()
    print("Back from call")
    print(f"Now contains {wells[0].contents}")
    
    ...

system.shutdown()