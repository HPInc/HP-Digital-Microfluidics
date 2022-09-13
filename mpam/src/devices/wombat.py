from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser

import logging
from typing import Mapping, Final, Optional, Sequence

from devices import joey
from devices.opendrop import OpenDropFirmware, Electrode
from erk.basic import ComputedDefaultDict
from mpam.exerciser import PlatformChoiceExerciser, Exerciser
from mpam.pipettor import Pipettor
from mpam.types import OnOff, State, DummyState
from quantities.dimensions import Time


logger = logging.getLogger(__name__)


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
    123: (1, 1), 124: (1, 2), 125: (1, 3), 126: (1, 4),
    127: (1, 5), 128: (1, 6), 129: (1, 7), 130: (1, 8),
    131: (2, 1), 132: (2, 2), 133: (2, 3), 134: (2, 4),
    135: (2, 5), 136: (2, 6), 137: (2, 7), 138: (2, 8),
    139: (3, 1), 140: (3, 2), 141: (3, 3), 142: (3, 4),
    143: (3, 5), 144: (3, 6), 145: (3, 7), 146: (3, 8),
    147: (4, 1), 148: (4, 2), 149: (4, 3), 150: (4, 4),
    151: (4, 5), 152: (4, 6), 153: (4, 7), 154: (4, 8),
    155: (5, 1), 156: (5, 2), 157: (5, 3), 158: (5, 4),
    159: (5, 5), 160: (5, 6), 161: (5, 7), 162: (5, 8),
    163: (6, 1), 164: (6, 2), 165: (6, 3), 166: (6, 4),
    167: (6, 5), 168: (6, 6), 169: (6, 7), 170: (6, 8),
    171: (7, 1), 172: (7, 2), 173: (7, 3), 174: (7, 4),
    175: (7, 5), 176: (7, 6), 177: (7, 7), 178: (7, 8),
    179: (8, 1), 180: (8, 2), 181: (8, 3), 182: (8, 4),
    183: (8, 5), 63: (8, 6), 64: (8, 7), 65: (8, 8),
    60: (9, 1), 61: (9, 2), 62: (9, 3), 184: (9, 4),
    185: (9, 5), 186: (9, 6), 187: (9, 7), 188: (9, 8),
    189: (10, 1), 190: (10, 2), 191: (10, 3), 192: (10, 4),
    193: (10, 5), 194: (10, 6), 195: (10, 7), 196: (10, 8),
    197: (11, 1), 198: (11, 2), 199: (11, 3), 200: (11, 4),
    201: (11, 5), 202: (11, 6), 203: (11, 7), 204: (11, 8),
    205: (12, 1), 206: (12, 2), 207: (12, 3), 208: (12, 4),
    209: (12, 5), 210: (12, 6), 211: (12, 7), 212: (12, 8),
    213: (13, 1), 214: (13, 2), 215: (13, 3), 216: (13, 4),
    217: (13, 5), 218: (13, 6), 219: (13, 7), 220: (13, 8),
    221: (14, 1), 222: (14, 2), 223: (14, 3), 224: (14, 4),
    225: (14, 5), 226: (14, 6), 227: (14, 7), 228: (14, 8),
    229: (15, 1), 230: (15, 2), 231: (15, 3), 232: (15, 4),
    233: (15, 5), 234: (15, 6), 235: (15, 7), 236: (15, 8),
    237: (16, 1), 238: (16, 2), 239: (16, 3), 240: (16, 4),
    241: (16, 5), 242: (16, 6), 243: (16, 7), 244: (16, 8),
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

        


class Board(joey.Board):
    _firmware: Final[OpenDropFirmware]
    _electrodes: Final[dict[int, Electrode]]
    is_yaminon: Final[bool]
    
    def make_electrode(self, pin: int) -> Electrode:
        x,y = _opendrop[pin]
        return self._firmware.make_electrode(x-1,y-1)
    
    def _electrode(self, cell: Optional[str]) -> Optional[Electrode]:
        if cell is None:
            return None
        pin = _pins.get(cell, None)
        if pin is None:
            return None
        return self._electrodes[pin]
    
    def _well_pad_state(self, group_name: str, num: int) -> State[OnOff]:
        cell = _shared_pad_cells.get((group_name, num))  
        # print(f"-- shared: {group_name} {num} -- {cell}")
        return self._electrode(cell) or DummyState(initial_state=OnOff.OFF)

    def _well_gate_state(self, well: int) -> State[OnOff]:
        if self.is_yaminon:
            mirroring = { 0:2, 1:3, 2:2, 3:3, 4:6, 5:7, 6:6, 7:7}
            well = mirroring[well]
        cell = _well_gate_cells.get(well, None)
        # print(f"-- gate: {well} -- {cell}")
        return self._electrode(cell) or DummyState(initial_state=OnOff.OFF)
    
    def _pad_state(self, x: int, y: int) -> Optional[State[OnOff]]:
        if self.is_yaminon and y >= 12:
            y = y-12
        cell = f"{ord('B')+y:c}{25-x:02d}"
        if cell in _pins:
            print(f"({x}, {y}): {cell} : {_pins[cell]} : {_opendrop[_pins[cell]]}")
        
        return self._electrode(cell)
    
    def __init__(self, od_firmware: OpenDropFirmware, *,
                 is_yaminon: bool = False,
                 off_on_delay: Time = Time.ZERO,
                 pipettor: Optional[Pipettor] = None) -> None:
        self._firmware = od_firmware
        self._electrodes = ComputedDefaultDict[int, Electrode](lambda pin: self.make_electrode(pin))
        logger.info("is_yaminon = %s", is_yaminon)
        self.is_yaminon = is_yaminon
        super().__init__(pipettor=pipettor, off_on_delay=off_on_delay)
        
    def update_state(self) -> None:
        self._firmware.update_state(self.off_on_delay)
        super().update_state()
        
    def stop(self)->None:
        self._firmware.stop()
        super().stop()
        

class PlatformTask(joey.PlatformTask):
    def __init__(self, name: str = "Wombat",
                 description: Optional[str] = None,
                 *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
    
    
    def make_board(self, args: Namespace, *, 
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                   pipettor: Pipettor) -> Board: # @UnusedVariable
        logger.info(f"Version is {args.od_version}")
        firmware = OpenDropFirmware.make_firmware(args)
        return Board(pipettor=pipettor,
                     od_firmware=firmware,
                     is_yaminon=self.is_yaminon(),
                     off_on_delay=args.off_on_delay)
        
    def is_yaminon(self) -> bool:
        return False
        
    def available_wells(self, exerciser: Exerciser) -> Sequence[int]: # @UnusedVariable
        return [2,3,6,7]

    def add_args_to(self, 
                    group: _ArgumentGroup, 
                    parser: ArgumentParser,
                    *,
                    exerciser: Exerciser) -> None:
        super().add_args_to(group, parser, exerciser=exerciser)
        OpenDropFirmware.add_args_to(group, parser)
        
class YaminonPlatformTask(PlatformTask):
    def __init__(self, name: str = "Yaminon",
                 description: str = "Run tasks on the Yaminon (mirrored Wombat) platform",
                 *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
    
    
    def available_wells(self, exerciser: Exerciser) -> Sequence[int]: # @UnusedVariable
        return range(0,8)
    
    def is_yaminon(self) -> bool:
        return True
    
        
        