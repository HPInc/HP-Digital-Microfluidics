from __future__ import annotations

from enum import Enum, auto
from typing import Mapping, Final, Optional, Sequence

from serial import Serial

from devices import joey
from mpam.types import OnOff, State, DummyState, XYCoord
from erk.basic import ComputedDefaultDict, assert_never
import logging
from mpam.exerciser import PlatformChoiceExerciser, Exerciser, BoardKwdArgs
from argparse import Namespace, _ArgumentGroup, ArgumentParser,\
    BooleanOptionalAction
from devices.joey import JoeyLayout
from mpam import device
from erk.config import ConfigParam

logger = logging.getLogger(__name__)



v1pins = {
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

v1_5pins = v1pins.copy()
for old,new in [
                #("BC27", "K16"), ("C28", "K18"), ("AB27", "K17"),
                #("A04", "L14"), ("AB05", "K15"), 
                ("C04", "B00"),
                #("BC05", "J14"), 
                # ("K07", "K14"), 
                ("A28", "B32")]:
    v1_5pins[new] = v1_5pins.pop(old)

_pins : Mapping[JoeyLayout, Mapping[str, int]] = {
    JoeyLayout.V1: v1pins,
    JoeyLayout.V1_5: v1_5pins
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

v1_shared_pad_cells: Mapping[tuple[str,int], str] = {
    ('left', 1): 'BC27', ('left', 2): 'B27', ('left', 3): 'AB27', 
    ('left', 4): 'C28', ('left', 5): 'B28', ('left', 6): 'A28',
    ('left', 7): 'B29', ('left', 8): 'B30', ('left', 9): 'B31',
    ('right', 1): 'BC05', ('right', 2): 'B05', ('right', 3): 'AB05', 
    ('right', 4): 'C04', ('right', 5): 'B04', ('right', 6): 'A04',
    ('right', 7): 'B03', ('right', 8): 'B02', ('right', 9): 'B01',
    }
v1_5_shared_pad_cells: Mapping[tuple[str,int], str] = {
    ('left', 1): 'B27', ('left', 2): 'B28', ('left', 3): 'B29', 
    ('left', 4): 'B30', ('left', 5): 'B31', ('left', 6): 'A32',
    ('right', 1): 'B05', ('right', 2): 'B04', ('right', 3): 'B03', 
    ('right', 4): 'B02', ('right', 5): 'B01', ('right', 6): 'B00',
    }

_shared_pad_cells: Mapping[JoeyLayout, Mapping[tuple[str,int], str]] = {
    JoeyLayout.V1: v1_shared_pad_cells,
    JoeyLayout.V1_5: v1_5_shared_pad_cells
} 
_well_gate_cells: Mapping[XYCoord, str] = {
    XYCoord(1,19): 'T26', XYCoord(1,13): 'N26', XYCoord(1,7): 'H26', XYCoord(1,1): 'B26',
    XYCoord(19,19): 'T06', XYCoord(19,13): 'N06', XYCoord(19,7): 'H06', XYCoord(19,1): 'B06'
    }

class OpenDropVersion(Enum):
    V40 = auto()
    V41 = auto()
    

class Electrode(State[OnOff]):
    byte_index: Final[int]
    bit_index: Final[int]

    array: Final[bytearray]
    
    def realize_state(self, val: OnOff) -> None:
        # assert self.index < len(self.array), f"{self.index} not in {len(self.array)}-byte array"
        
        bit = 1 << self.bit_index

        if val is OnOff.ON:
            self.array[self.byte_index] |= bit
        else:
            self.array[self.byte_index] &= ~bit
        
        # self.array[self.index] = 1 if val else 0
    
    def __init__(self, byte_index: int, bit_index: int, a: bytearray) -> None:
        super().__init__(initial_state=OnOff.OFF)
        self.byte_index = byte_index
        self.bit_index = bit_index
        self.array = a
        
class Config:
    is_yaminon: Final = ConfigParam(False)
    device: Final = ConfigParam[Optional[str]](None)
    od_version: Final = ConfigParam(OpenDropVersion.V40)
    double_write: Final = ConfigParam(False)
    
    _defaults_set_up = False
    @classmethod
    def setup_defaults(cls) -> None:
        if not cls._defaults_set_up:
            joey.Config.setup_defaults()
            print("Setting up Config defaults for Wombat")
            cls._defaults_set_up = True
    

class Board(joey.Board):
    _device: Final[Optional[str]]
    _states: Final[bytearray]
    _last_states: bytearray
    _port: Optional[Serial] 
    _od_version: Final[OpenDropVersion]
    _electrodes: Final[dict[int, Electrode]]
    _double_write: Final[bool]
    is_yaminon: Final[bool]
    
    def make_electrode(self, pin: int) -> Electrode:
        x,y = _opendrop[pin]
        if self._od_version is OpenDropVersion.V40:
            byte_index = (x-1)*8+(y-1)
            bit_index = 0
            assert byte_index < 128
        else:
            byte_index = x-1
            bit_index = y-1
        # print(f"  pin: {pin}, (x,y): ({x},{y}), index: {index}")
        return Electrode(byte_index, bit_index, self._states)
    
    def _electrode(self, cell: Optional[str]) -> Optional[Electrode]:
        if cell is None:
            return None
        pin_map = _pins
        pin = pin_map[self._layout].get(cell, None)
        if pin is None:
            return None
        return self._electrodes[pin]
    
    def _well_pad_state(self, group_name: str, num: int) -> State[OnOff]:
        cell = _shared_pad_cells[self._layout].get((group_name, num))  
        # print(f"-- shared: {group_name} {num} -- {cell}")
        return self._electrode(cell) or DummyState(initial_state=OnOff.OFF)

    def _well_gate_state(self, exit_pad: device.Pad) -> State[OnOff]:
        if self.is_yaminon:
            row = exit_pad.row
            if row > 10:
                exit_pad = self.pad_at(exit_pad.column, row-12)
        cell = _well_gate_cells.get(exit_pad.location, None)
        # print(f"-- gate: {well} -- {cell}")
        return self._electrode(cell) or DummyState(initial_state=OnOff.OFF)
    
    def _pad_state(self, x: int, y: int) -> Optional[State[OnOff]]:
        if self.is_yaminon and y >= 13:
            y = y-12
        cell = f"{ord('B')+y-1:c}{26-x:02d}"
        # print(f"({x}, {y}): {cell}")
        return self._electrode(cell)
    
    
    def __init__(self, 
                 ) -> None:
        od_version = Config.od_version()
        logger.info(f"Opendrop version is {od_version}",)
            
        if od_version is OpenDropVersion.V40:
            n_state_bytes = 128
        elif od_version is OpenDropVersion.V41:
            n_state_bytes = 32
        else:
            assert_never(od_version)
        self._states = bytearray(n_state_bytes)
        self._last_states = bytearray(n_state_bytes)
        self._od_version = Config.od_version()
        logger.info("is_yaminon = %s", Config.is_yaminon())
        self.is_yaminon = Config.is_yaminon()
        self._electrodes = ComputedDefaultDict[int, Electrode](lambda pin: self.make_electrode(pin))
        logger.info("double_write = %s", Config.double_write())
        self._double_write = Config.double_write()
        super().__init__()
        if Config.is_yaminon():
            for x, y in ((i, j) for i in range(1, 20) for j in range(1, 10)):
                y2 = y+12
                remove = False
                try:
                    remove = (not self.pad_at(x, y).exists
                              or not self.pad_at(x, y2).exists)
                except KeyError:
                    ...
                if remove:
                    self.remove_pad_at(x, y)
                    self.remove_pad_at(x, y2)
                
                
        self._device = Config.device()
        self._port = None
        
    def send_states(self, states: bytearray) -> None:
        logger.debug("sending %s", states.hex())
        if self._port is not None:
            self._port.write(states)
            # I'm not sure why, but it seems that nothing happens until the 
            # first byte of the next round gets sent. (Sending 129 bytes works, 
            # but then the next round will use that extra byte.  Sending everything
            # twice seems to do the job.  I'll look into this further.
            self._port.write(states)
        
        
    def update_state(self) -> None:
        if self._port is None and self._device is not None:
            self._port = Serial(self._device)
        delay = self.off_on_delay
        new_states = bytearray(self._states)
        send_first: Optional[bytearray] = None
        if delay > 0:
            # First we send 
            send_first = bytearray(x&y for x,y in zip(self._last_states, new_states))
        elif delay < 0:
            send_first = bytearray(x|y for x,y in zip(self._last_states, new_states))
            delay = -delay
        if send_first is not None:
            self.send_states(send_first)
            logger.debug("Delaying for %s", delay)
            delay.sleep()
        self.send_states(new_states)
        self._last_states = new_states
        super().update_state()

class PlatformTask(joey.PlatformTask):
    def __init__(self, name: str = "Wombat",
                 description: Optional[str] = None,
                 *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
    
    
    def make_board(self, args: Namespace, *, 
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                  ) -> Board: # @UnusedVariable
        kwds = self.board_kwd_args(args, announce=True)
        return Board(**kwds)

    def is_yaminon(self) -> bool:
        return False
        
    def available_wells(self, exerciser: Exerciser) -> Sequence[int]: # @UnusedVariable
        return [2,3,6,7]

    def setup_config_defaults(self) -> None:
        super().setup_config_defaults()
        Config.setup_defaults()

    def add_args_to(self, 
                    group: _ArgumentGroup, 
                    parser: ArgumentParser,
                    *,
                    exerciser: Exerciser) -> None:
        super().add_args_to(group, parser, exerciser=exerciser)
        ignored_cp = ConfigParam[str]()
        ignored_cp.add_arg_to(group, '-v1', '--v1', action='store_const', const="v1", 
                              deprecated = ConfigParam.use_instead("--joey-version 1.0"),
                              ignored = True, 
                              help = "Version 1 of the Wombat layout.")
        ignored_cp.add_arg_to(group, '-v2', '--v2', action='store_const', const="v2", 
                              deprecated = ConfigParam.use_instead("--joey-version 1.5"),
                              ignored = True, 
                              help = "Version 2 of the Wombat layout.")
        Config.device.add_arg_to(group, '-p', '--port',
                                 help='''
                                    The communication port (e.g., COM5) to use to talk to the board.
                                    By default, only the display is run
                                    ''')
        od_version_arg_names = {"4.0": OpenDropVersion.V40,    
                                "4.1": OpenDropVersion.V41
                                }        
        Config.od_version.add_choice_arg_to(group, od_version_arg_names,
                                            '--od-version', 
                                            metavar="VERSION",
                                            help="The version of the Opendrop firmware."
                                            )
        Config.od_version.add_arg_to(group, '-4.0', '--4.0',
                                     dest='od_version',
                                     action='store_const', const="4.0",
                                     deprecated=ConfigParam.use_instead("--od_version 4.0"),
                                     help="Opendrop firmware version 4.0")
        Config.od_version.add_arg_to(group, '-4.1', '--4.1',
                                     dest='od_version',
                                     action='store_const', const="4.1",
                                     deprecated=ConfigParam.use_instead("--od_version 4.1"),
                                     help="Opendrop firmware version 4.1")
        Config.double_write.add_arg_to(group, '--double-write', 
                                            action=BooleanOptionalAction, 
                           help=f'''
                           Send state array to OpenDrop twice.  
                           ''')
        
    def board_kwd_args(self, args: Namespace, announce: bool = False) -> BoardKwdArgs:
        kwds = super().board_kwd_args(args, announce=announce)
        Config.is_yaminon.value = self.is_yaminon()
        # kwds["is_yaminon"] = self.is_yaminon()
        # self.add_kwd_arg(args, kwds, "port", kwd="device")
        # self.add_kwd_arg(args, kwds, "od_version")
        # # self.add_kwd_arg(args, kwds, "wombat_version")
        # self.add_kwd_arg(args, kwds, "double_write")
        # # self.add_kwd_arg(args, kwds, "holes")
        # # self.add_kwd_arg(args, kwds, "default_holes")
        return kwds
        
        
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
    
        
        