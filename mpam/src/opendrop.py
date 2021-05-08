import mpam.device as device
from typing import Optional, Final
from mpam.types import OnOff, XYCoord
from serial import Serial

class Electrode:
    index: Final[int]
    array: Final[bytearray]
    
    def set_state(self, val: OnOff) -> None:
        self.array[self.index] = 1 if val else 0
    
    def __init__(self, i: int, a: bytearray) -> None:
        self.index = i
        self.array = a
        
class Pad(device.Pad):
    electrode: Electrode
    def __init__(self, e: Electrode, loc: XYCoord, board: 'Board'):
        super().__init__(loc, board)
        self.electrode = e
        
        self.set_device_state = lambda v: e.set_state(v)
    
        

class Board(device.Board):
    _dev: str
    _states: bytearray
    _port: Optional[Serial]
    
    def __init__(self, dev : str) -> None:
        pad_dict = dict[XYCoord, Pad]()
        super().__init__(pad_dict)
        self._dev = dev
        self._states = bytearray(128)
        # self._states[21] = 1
        # self._states[23] = 1
        # self._states[25] = 1
        self._port= None
        for x in range(1,15):
            for y in range(0,8):
                loc = XYCoord(x, y)
                index = x*8+y
                e = Electrode(index, self._states)
                p = Pad(e, loc, self)
                pad_dict[loc] = p
        
    def update_state(self) -> None:
        if self._port is None:
            self._port = Serial(self._dev)
            # self._stream = open(self._dev, "wb")
        self._port.write(self._states)
        # I'm not sure why, but it seems that nothing happens until the 
        # first byte of the next round gets sent. (Sending 129 bytes works, 
        # but then the next round will use that extra byte.  Sending everything
        # twice seems to do the job.  I'll look into this further.
        self._port.write(self._states)
        self.finish_update()
        
    def stop(self)->None:
        if self._port is not None:
            self._port.close()
            self._port = None
        super().stop()
        
    def electrode(self, i: int) -> Electrode:
        return Electrode(i, self._states)
    