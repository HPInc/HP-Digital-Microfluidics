from __future__ import annotations

from os import PathLike
import pyglider
from typing import Mapping, Final, Optional, Union, Sequence

from devices import joey, glider_client
from devices.glider_client import GliderClient
from mpam.pipettor import Pipettor
from mpam.types import OnOff, State, DummyState, GridRegion, Delayed
from mpam import device
from mpam.device import Pad
from quantities.dimensions import Time, Voltage
from quantities.SI import ms
from erk.stringutils import conj_str
from quantities.temperature import TemperaturePoint


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

class Heater(device.Heater):
    remote: Final[glider_client.Heater]
    def __init__(self, num: int, board: Board, *,
                 polling_interval: Time,
                 pads: Sequence[Pad]):
        super().__init__(num, board, polling_interval=polling_interval, pads=pads)
        names = set[str]()
        remote: Optional[glider_client.Heater] = None
        assert len(pads) > 0
        for pad in pads:
            s = pad.state
            assert isinstance(s, glider_client.Electrode)
            heater_names = s.heater_names()
            # print(f"Heaters for {pad}: {heater_names}")
            assert len(heater_names) > 0, f"{pad} has no heaters"
            assert len(heater_names) < 2, f"{pad} has multiple heaters: {conj_str(heater_names)}."
            names |= set(heater_names)
            if remote is None:
                remote = board._device.heater(heater_names[0])
                assert remote is not None, f"Heater {heater_names[0]} does not exist"
        assert len(names) == 1, f"Heater {num} on {conj_str(pads)} has multiple heaters: {conj_str(tuple(names))}."
        assert remote is not None
        self.remote = remote 
        def update_target(old: Optional[TemperaturePoint], new: Optional[TemperaturePoint]) -> None: # @UnusedVariable
            # We indirect through the board so that MakeItSo will be called.
            # This puts heater target changes synchronous with the clock.  I'm
            # not sure that's right, but it does allow the clock to be paused.
            # Note that this means that thermocycling needs to be not completely
            # asynchronous.
            self.board.communicate(lambda: self.remote.set_target(new)) 
        update_target_key = f"Update Target for {self}"
        self.on_target_change(update_target, key = update_target_key)
        
    def __repr__(self) -> str:
        return f"<Heater using {self.remote}>"

    
    def poll(self) -> Delayed[Optional[TemperaturePoint]]:
        temp = self.remote.read_temperature()
        self.current_temperature = temp
        return Delayed.complete(temp)
        
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
    
    def _heater(self, num:int, *, 
                polling_interval: Time=200*ms,
                regions:Sequence[GridRegion])->Heater:
        pads: list[Pad] = []
        for region in regions:
            pads += (self.pad_array[xy] for xy in region)
        return Heater(num, self, pads=pads, polling_interval=polling_interval)

    
    def __init__(self, *,
                 dll_dir: Optional[Union[str, PathLike]] = None,
                 config_dir: Optional[Union[str, PathLike]] = None,
                 pipettor: Optional[Pipettor] = None,
                 voltage: Optional[Voltage]) -> None:
        self._device = GliderClient(pyglider.BoardId.Wallaby, dll_dir=dll_dir, config_dir=config_dir)
        super().__init__(pipettor=pipettor)
        on_electrodes = self._device.on_electrodes()
        if on_electrodes:
            for e in on_electrodes:
                e.current_state = OnOff.ON
            self.infer_drop_motion()
        if voltage is None:
            print("Turning off high voltage")
        else:
            print(f"Turning on high voltage at {voltage}")
        
        self._device.voltage_level = voltage
        
    def update_state(self) -> None:
        self._device.update_state()
        super().update_state()
