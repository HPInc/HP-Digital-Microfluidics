from devices import joey
from langsup.dmf_lang import DMFInterpreter
import sys
    
if __name__ == '__main__':
    board = joey.Board()
    interp = DMFInterpreter(sys.argv[1], board=board)