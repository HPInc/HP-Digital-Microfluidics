from __future__ import annotations

from pathlib import Path
import pyglider
from typing import Union, Optional, Final
from mpam.types import State, OnOff
from os import PathLike
from quantities.temperature import TemperaturePoint, abs_C
from quantities.dimensions import Voltage
from quantities.SI import volts

def _to_path(p: Optional[Union[str, PathLike]]) -> Optional[PathLike]:
    if isinstance(p, str):
        return Path(p)
    return p

class Electrode(State[OnOff]):
    name: Final[str]
    remote: Final[pyglider.Electrode]
    
    def __init__(self, name: str, remote: pyglider.Electrode) -> None:
        super().__init__(initial_state=OnOff.OFF)
        self.name = name
        self.remote = remote
        
    def __repr__(self) -> str:
        return f"<Electrode {self.name}>"
        
    def realize_state(self, new_state: OnOff)->None:
        s = pyglider.Electrode.ElectrodeState.On if new_state else pyglider.Electrode.ElectrodeState.Off
        # print(f"Setting {self.name} to {new_state} ({s})")
        ec = self.remote.SetTargetState(s)
        if ec != pyglider.ErrorCode.ErrorSuccess:
            print(f"Error {ec} returned trying to set electrode {self.name} to {new_state}.")
            
    def heater_names(self) -> list[str]:
        return self.remote.GetHeaters()
    
class Heater:
    name: Final[str]
    remote: Final[pyglider.Heater]
    
    def __init__(self, name: str, remote: pyglider.Heater) -> None:
        self.name = name
        self.remote = remote
        
    def __repr__(self) -> str:
        return f"<Heater {self.name}>"
        
    def read_temperature(self) -> TemperaturePoint:
        # s = self.remote.GetStatus()
        # print(f"{self.name}: Current: {s.GetCurrentTemperature()}, Target: {s.GetTargetTemperature()}, ETA: {s.GetEtaInMilliseconds()}")
        temp = self.remote.GetCurrentTemperature()
        tp = temp*abs_C
        # print(f"  {tp}")
        return tp
    
    def set_target(self, target: Optional[TemperaturePoint]) -> None:
        temp = 0.0 if target is None else target.as_number(abs_C)
        # print(f"Setting target for {self.name} to {target}")
        self.remote.SetTargetTemperature(temp)
        
class GliderClient:
    remote: Final[pyglider.Board]
    electrodes: Final[dict[str, Electrode]]
    heaters: Final[dict[str, Heater]]
    # remote_electrodes: Final[dict[str, pyglider.Electrode]]
    
    _voltage_level: Optional[Voltage] = None 
    
    @property
    def voltage_level(self) -> Optional[Voltage]:
        return self._voltage_level
    
    @voltage_level.setter
    def voltage_level(self, opt_volts: Optional[Voltage]) -> None:
        self._voltage_level = opt_volts
        if opt_volts is None:
            self.remote.DisableHighVoltage()
        else:
            self.remote.SetHighVoltage(opt_volts.as_number(volts))
            self.remote.EnableHighVoltage()
    
    def __init__(self, board_type: pyglider.BoardId, *,
                 dll_dir: Optional[Union[str, PathLike]] = None,
                 config_dir: Optional[Union[str, PathLike]] = None) -> None:
        self.remote = pyglider.Board.Find(board_type, 
                                          dll_dir=_to_path(dll_dir),
                                          config_dir=_to_path(config_dir))
        # self.remote_electrodes = { e.GetName(): e for e in b.GetElectrodes()}
        # print(f"Remote: {self.remote_electrodes}")
        # self.electrodes = { k: Electrode(k, v) for k,v in self.remote_electrodes.items()}
        self.electrodes = {}
        self.heaters = {}
        # print(f"Local: {self.electrodes}")

    def on_electrodes(self) -> list[Electrode]:
        return [e for e in self.electrodes.values() 
                if e.remote.GetCurrentState() == pyglider.Electrode.ElectrodeState.On]
        
    def update_state(self) -> None:
        ec = self.remote.MakeItSo()
        if ec != pyglider.ErrorCode.ErrorSuccess:
            print(f"Error {ec} returned trying to update board.")
            
            
    def electrode(self, name: Optional[str]) -> Optional[Electrode]:
        # print(f"Asking for electrode {name}")
        if name is None:
            # print("  not there")
            return None
        # print(f"  is {self.electrodes[name]}")
        e = self.electrodes.get(name)
        if e is None:
            re = self.remote.ElectrodeNamed(name)
            if re is None:
                print(f"No electrode named {name}!")
            else:
                e = Electrode(name, re)
                self.electrodes[name] = e
        return e
    
    def heater(self, name: Optional[str]) -> Optional[Heater]:
        if name is None:
            return None
        h = self.heaters.get(name)
        if h is None:
            re = self.remote.HeaterNamed(name)
            if re is None:
                print(f"No heater named {name}!")
            else:
                h = Heater(name, re)
                self.heaters[name] = h
        return h
    
