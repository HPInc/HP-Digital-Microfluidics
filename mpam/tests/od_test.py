from mpam.device import System, Pad
import opendrop
from mpam.types import OnOff
from quantities.SI import sec
import time


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
    system.clock.start()
    # system.clock.advance_clock()
    time.sleep(2)
system.stop()