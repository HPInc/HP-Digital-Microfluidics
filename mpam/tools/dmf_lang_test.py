from devices import joey
from langsup.dmf_lang import DMFInterpreter
import sys
from mpam.device import System
    
if __name__ == '__main__':
    board = joey.Board()
    system = System(board=board)
    system.clock.start()
    # engine._trace_ticks = True
    with system:
        interp = DMFInterpreter(sys.argv[1], board=board)
        