from __future__ import annotations
from devices import joey
from typing import Mapping, Final, Optional
from mpam.types import OnOff, XYCoord
from serial import Serial

_pins: Mapping[str, int] = {
    "B01": 244, "H06": 243, "B02": 242, "B03": 241, "C04": 240,
    "B04": 239, "A04": 238, "BC05": 237, "B05": 236, "AB05": 235,
    "B06": 234, "F07": 233, "E07": 232, "D07": 231, "C07": 230,
    "B07": 229, "F08": 228, "E08": 227, "D08": 226, "C08": 225,
    "B08": 224, "F09": 223, "E09": 222, "D09": 221, "C09": 220,
    "B09": 219, "F10": 218, "E10": 217, "D10": 216, "C10": 215,
    "G07": 214, "H07": 213, "F11": 212, "E11": 211, "D11": 210,
    "G08": 209, "H08": 208, "C11": 207, "F12": 206, "G09": 205,
    "E12": 204, "D12": 203, "C12": 202, "F13": 201, "E13": 200,
    "G10": 199, "D13": 198, "C13": 197, "G11": 196, "F14": 195,
    "E14": 194, "D14": 193, "G12": 192, "C14": 191, "F15": 190,
    "G13": 189, "E15": 188, "D15": 187, "C15": 186, "G14": 185,
    "G16": 184, "F16": 183, "G15": 182, "E16": 181, "D16": 180,
    "C16": 179, "G17": 178, "E17": 177, "D17": 176, "C17": 175,
    "G18": 174, "C18": 173, "F17": 172, "G19": 171, "F18": 170,
    "E18": 169, "D18": 168, "G20": 167, "D19": 166, "C19": 165,
    "G21": 164, "F19": 163, "E19": 162, "G22": 161, "E20": 160,
    "D20": 159, "C20": 158, "H23": 157, "C21": 156, "F20": 155,
    "G23": 154, "F21": 153, "E21": 152, "D21": 151, "G24": 150,
    "H24": 149, "D22": 148, "C22": 147, "G25": 146, "H25": 145,
    "B23": 144, "F22": 143, "E22": 142, "E23": 141, "D23": 140,
    "C23": 139, "C24": 138, "B24": 137, "F23": 136, "F24": 135,
    "E24": 134, "D24": 133, "D25": 132, "C25": 131, "B25": 130,
    "B26": 129, "F25": 128, "E25": 127, "A28": 126, "BC27": 125,
    "B27": 124, "AB27": 123, "B30": 65, "B29": 64, "C28": 63,
    "B28": 62, "B31": 61, "H26": 60
}

_opendrop: Mapping[int, tuple[int,int]] = {
    244: (1,1), 243: (1,2), 242: (1,3), 241: (1,4), 
    240: (1,5), 239: (1,6), 238: (1,7), 237: (1,8),
    236: (2,1), 235: (2,2), 234: (2,3), 233: (2,4),
    232: (2,5), 231: (2,6), 230: (2,7), 229: (2,8),
    228: (3,1), 227: (3,2), 226: (3,3), 225: (3,4),
    224: (3,5), 223: (3,6), 222: (3,7), 221: (3,8),
    220: (4,1), 219: (4,2), 218: (4,3), 217: (4,4),
    216: (4,5), 215: (4,6), 214: (4,7), 213: (4,8),
    212: (5,1), 211: (5,2), 210: (5,3), 209: (5,4),
    208: (5,5), 207: (5,6), 206: (5,7), 205: (5,8),
    204: (6,1), 203: (6,2), 202: (6,3), 201: (6,4),
    200: (6,5), 199: (6,6), 198: (6,7), 197: (6,8),
    196: (7,1), 195: (7,2), 194: (7,3), 193: (7,4),
    192: (7,5), 191: (7,6), 190: (7,7), 189: (7,8),
    188: (8,1), 187: (8,2), 186: (8,3), 185: (8,4),
    184: (8,5), 63: (8,6), 64: (8,7), 65: (8,8),
    60: (9,1), 61: (9,2), 62: (9,3), 183: (9,4),
    182: (9,5), 181: (9,6), 180: (9,7), 179: (9,8),
    178: (10,1), 177: (10,2), 176: (10,3), 175: (10,4),
    174: (10,5), 173: (10,6), 172: (10,7), 171: (10,8),
    170: (11,1), 169: (11,2), 168: (11,3), 167: (11,4),
    166: (11,5), 165: (11,6), 164: (11,7), 163: (11,8),
    162: (12,1), 161: (12,2), 160: (12,3), 159: (12,4),
    158: (12,5), 157: (12,6), 156: (12,7), 155: (12,8),
    154: (13,1), 153: (13,2), 152: (13,3), 151: (13,4),
    150: (13,5), 149: (13,6), 148: (13,7), 147: (13,8),
    146: (14,1), 145: (14,2), 144: (14,3), 143: (14,4),
    142: (14,5), 141: (14,6), 140: (14,7), 139: (14,8),
    138: (15,1), 137: (15,2), 136: (15,3), 135: (15,4),
    134: (15,5), 133: (15,6), 132: (15,7), 131: (15,8),
    130: (16,1), 129: (16,2), 128: (16,3), 127: (16,4),
    126: (16,5), 125: (16,6), 124: (16,7), 123: (16,8),
}

_shared_pad_cells: Mapping[tuple[str,int], str] = {
    ('left', 0): 'BC27', ('left', 1): 'B27', ('left', 2): 'AB27', 
    ('left', 3): 'C28', ('left', 4): 'B28', ('left', 5): 'A28',
    ('left', 6): 'B29', ('left', 7): 'B30', ('left', 8): 'B31',
    ('right', 0): 'BC05', ('right', 1): 'B05', ('right', 2): 'AB05', 
    ('right', 3): 'C04', ('right', 4): 'B04', ('right', 5): 'A04',
    ('right', 6): 'B03', ('right', 7): 'B02', ('right', 8): 'B01',
    }

_well_gate_cells: Mapping[int, str] = {
    0: 'T26', 1: 'N26', 2: 'H26', 3: 'B26',
    4: 'T06', 5: 'N06', 6: 'H06', 7: 'B06'
    }

class Electrode:
    index: Final[int]
    array: Final[bytearray]
    
    def set_state(self, val: OnOff) -> None:
        # assert self.index < len(self.array), f"{self.index} not in {len(self.array)}-byte array"
        self.array[self.index] = 1 if val else 0
    
    def __init__(self, index: int, a: bytearray) -> None:
        self.index = index
        self.array = a
        
    
class Pad(joey.Pad):
    electrode: Final[Optional[Electrode]]

    def __init__(self, electrode: Optional[Electrode], loc: XYCoord, board: Board, *, exists: bool) -> None:
        super().__init__(loc, board, exists = exists and electrode is not None)
        self.electrode = electrode
        if electrode is None:
            self.set_device_state = lambda _: None
        else:
            real_e = electrode
            self.set_device_state = lambda v: real_e.set_state(v)
            
class WellPad(joey.WellPad):
    electrode: Final[Optional[Electrode]]

    def __init__(self, electrode: Optional[Electrode], board: Board) -> None:
        super().__init__(board, live=electrode is not None)
        self.electrode = electrode
        if electrode is None:
            self.set_device_state = lambda _: None
        else:
            real_e = electrode
            self.set_device_state = lambda v: real_e.set_state(v)

class Board(joey.Board):
    _device: Final[Optional[str]]
    _states: Final[bytearray]
    _port: Optional[Serial] 
    
    def _electrode(self, cell: Optional[str]) -> Optional[Electrode]:
        if cell is None:
            return None
        pin = _pins.get(cell, None)
        if pin is None:
            return None
        x,y = _opendrop[pin]
        index = (x-1)*8+(y-1)
        assert index < 128
        # print(f"  pin: {pin}, (x,y): ({x},{y}), index: {index}")
        return Electrode(index, self._states)
    
    def _make_well_pad(self, group_name: str, num: int) -> WellPad:
        cell = _shared_pad_cells.get((group_name, num))  
        # print(f"-- shared: {group_name} {num} -- {cell}")
        return WellPad(self._electrode(cell), board=self)

    def _make_well_gate(self, well: int) -> WellPad:
        cell = _well_gate_cells.get(well, None)
        # print(f"-- gate: {well} -- {cell}")
        return WellPad(self._electrode(cell), board=self)
    
    def _make_pad(self, x: int, y: int, *, exists: bool) -> Pad:
        cell = f"{ord('B')+y:c}{25-x:02d}"
        # print(f"({x}, {y}): {cell}")
        return Pad(self._electrode(cell), XYCoord(x, y), self, exists=exists)
    
    
    
    
    def __init__(self, device: Optional[str]) -> None:
        self._states = bytearray(128)
        super().__init__()
        self._device = device
        self._port = None
        
    def update_state(self) -> None:
        if self._port is None:
            if self._device is None:
                return
            self._port = Serial(self._device)
            # self._stream = open(self._dev, "wb")
        self._port.write(self._states)
        # I'm not sure why, but it seems that nothing happens until the 
        # first byte of the next round gets sent. (Sending 129 bytes works, 
        # but then the next round will use that extra byte.  Sending everything
        # twice seems to do the job.  I'll look into this further.
        self._port.write(self._states)
        self.finish_update()
