from __future__ import annotations
from mpam.device import System, Pad
import opendrop
from mpam.types import OnOff, unknown_reagent, Liquid, Dir
from quantities.SI import sec, uL
import time
from mpam.drop import Drop


board = opendrop.Board("COM5")

system = System(board=board)

with system:
    p: Pad = board.pad_at(2,3)
    p.request_turn_on()
    
    def cb():
        p.request_turn_off()
    system.call_after(1.5*sec, cb)

    for y in range(0,8):
        board.pad_at(3,y).set_state(OnOff.ON)

    for y in range(0,8):
        board.pad_at(5,y).gated_set_state(OnOff.ON)
    time.sleep(2)
    system.clock.start(0.5*sec)
    # system.clock.advance_clock()
    drop = Drop(board.pad_at(8, 1), Liquid(unknown_reagent, 0.5*uL))
    drop.gated_move(Dir.S, steps=3).then.gated_move(Dir.W, steps=5)
    time.sleep(2)
    with system.batched():
        for y in range(0,8):
            board.pad_at(6,y).async_set_state(OnOff.ON)
    time.sleep(2)
system.stop()