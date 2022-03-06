from __future__ import annotations

from os import PathLike
import pyglider
from typing import Mapping, Final, Optional, Union

from devices import joey
from devices.glider_client import GliderClient
from mpam.pipettor import Pipettor
from mpam.types import OnOff, State, DummyState


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
    _device: Final[GliderClient]
    
    def _well_pad_state(self, group_name: str, num: int) -> State[OnOff]:
        cell = _shared_pad_cells.get((group_name, num))  
        # print(f"-- shared: {group_name} {num} -- {cell}")
        return self._device.electrode(cell) or DummyState(initial_state=OnOff.OFF)

    def _well_gate_state(self, well: int) -> State[OnOff]:
        cell = _well_gate_cells.get(well, None)
        # print(f"-- gate: {well} -- {cell}")
        return self._device.electrode(cell) or DummyState(initial_state=OnOff.OFF)
    
    def _pad_state(self, x: int, y: int) -> Optional[State[OnOff]]:
        cell = f"{ord('B')+y:c}{25-x:02d}"
        # print(f"({x}, {y}): {cell}")
        return self._device.electrode(cell)
    
    def __init__(self, *,
                 dll_dir: Optional[Union[str, PathLike]] = None,
                 config_dir: Optional[Union[str, PathLike]] = None,
                 pipettor: Optional[Pipettor] = None) -> None:
        self._device = GliderClient(pyglider.BoardId.Wallaby, dll_dir=dll_dir, config_dir=config_dir)
        super().__init__(pipettor=pipettor)
        
    def update_state(self) -> None:
        self._device.update_state()
        super().update_state()
