import mpam.device as device
from typing import Optional, Final
from mpam.types import OnOff, XYCoord, Orientation
from serial import Serial
from mpam.device import WellGroup, Well, WellOpSeqDict, WellState
from quantities.SI import uL, ms

class Electrode:
    index: Final[int]
    array: Final[bytearray]
    
    def set_state(self, val: OnOff) -> None:
        self.array[self.index] = 1 if val else 0
    
    def __init__(self, x: int, y: int, a: bytearray) -> None:
        self.index = x*8+y
        self.array = a
        
class Pad(device.Pad):
    electrode: Electrode
    def __init__(self, e: Electrode, loc: XYCoord, board: 'Board'):
        super().__init__(loc, board)
        self.electrode = e
        
        self.set_device_state = lambda v: e.set_state(v)
    
class WellGatePad(device.WellPad):
    electrode: Electrode
    def __init__(self, e: Electrode, board: 'Board'):
        super().__init__(board)
        self.electrode = e
        
        self.set_device_state = lambda v: e.set_state(v)

class SharedWellPad(device.WellPad):
    upper_electrode: Electrode
    lower_electrode: Electrode
    def __init__(self, upper: Electrode, lower: Electrode, board: 'Board'):
        super().__init__(board)
        self.upper_electrode = upper
        self.lower_electrode = lower
        
        def set_state(val: OnOff):
            upper.set_state(val)
            lower.set_state(val)
            
        self.set_device_state = set_state

class Board(device.Board):
    _dev: str
    _states: bytearray
    _port: Optional[Serial]
    
    def _well(self, num: int, group: WellGroup, gate_loc: XYCoord, exit_pad: device.Pad):
        return Well(number=num,
                    board=self,
                    group=group,
                    exit_pad=exit_pad,
                    gate=WellGatePad(Electrode(gate_loc.x, gate_loc.y, self._states), self),
                    capacity=12*uL,
                    dispensed_volume=2*uL)
    
    def __init__(self, dev : str) -> None:
        pad_dict = dict[XYCoord, Pad]()
        wells: list[Well] = []
        super().__init__(pads=pad_dict, 
                         wells=wells,
                         orientation=Orientation.NORTH_NEG_EAST_POS,
                         drop_motion_time=100*ms)
        self._dev = dev
        self._states = bytearray(128)
        self._port= None
        for x in range(1,15):
            for y in range(0,8):
                loc = XYCoord(x, y)
                e = Electrode(x, y, self._states)
                p = Pad(e, loc, self)
                pad_dict[loc] = p
                
        sequences: WellOpSeqDict = {
            (WellState.EXTRACTABLE, WellState.READY): ((2,),(1,2)),
            (WellState.READY, WellState.EXTRACTABLE): ((2,), ()),
            (WellState.READY, WellState.DISPENSED): ((-1,0,1),(-1,)),
            (WellState.DISPENSED, WellState.READY): ((1,2),),
            (WellState.READY, WellState.ABSORBED): ((-1,2),),
            (WellState.ABSORBED, WellState.READY): ((1,2),)
            }
        
        left_group = WellGroup("left", (SharedWellPad(Electrode(0, 1, self._states),
                                                      Electrode(0, 6, self._states), self),
                                        SharedWellPad(Electrode(0, 2, self._states),
                                                      Electrode(0, 5, self._states), self),
                                        SharedWellPad(Electrode(0, 3, self._states),
                                                      Electrode(0, 4, self._states), self)),
                                sequences)
        right_group = WellGroup("right", (SharedWellPad(Electrode(15, 1, self._states),
                                                        Electrode(15, 6, self._states), self),
                                          SharedWellPad(Electrode(15, 2, self._states),
                                                        Electrode(15, 5, self._states), self),
                                          SharedWellPad(Electrode(15, 3, self._states),
                                                        Electrode(15, 4, self._states), self)),
                                sequences)
        
        upper_left = self._well(0, left_group, XYCoord(0,0), self.pad_at(1,1))
        upper_right = self._well(1, right_group, XYCoord(15,0), self.pad_at(14,1))
        lower_left = self._well(2, left_group, XYCoord(0,7), self.pad_at(1,7))
        lower_right = self._well(1, right_group, XYCoord(15,7), self.pad_at(14,7))
        wells.extend((upper_left, upper_right, lower_left, lower_right))
        
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
        
    # def electrode(self, i: int) -> Electrode:
    #     return Electrode(i, self._states)
    