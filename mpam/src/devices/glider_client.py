from __future__ import annotations

from pathlib import Path
import pyglider
from typing import Union, Optional, Final, Generic, TypeVar, Callable
from mpam.types import State, OnOff
from os import PathLike
from quantities.temperature import TemperaturePoint, abs_C
from quantities.dimensions import Voltage
from quantities.SI import volts
import pathlib

def _to_path(p: Optional[Union[str, PathLike]]) -> Optional[PathLike]:
    if isinstance(p, str):
        return Path(p)
    return p

CT = TypeVar("CT")
ST = TypeVar("ST")

class BinState(Generic[CT, ST], State[OnOff]):
    kind: Final[str]
    name: Final[str]
    
    def __init__(self, *, kind: str, 
                 name: str, 
                 remote: CT,
                 on_val: ST,
                 off_val: ST,
                 realize: Callable[[CT, ST], pyglider.ErrorCode],
                 initial_state: Union[OnOff, Callable[[CT], ST]] = OnOff.OFF) -> None:
        if not isinstance(initial_state, OnOff):
            initial_state = OnOff.from_bool(initial_state(remote) is on_val)
        super().__init__(initial_state=initial_state)
        self.kind = kind
        self.name = name
        self.remote = remote
        self.on_val = on_val
        self.off_val = off_val
        self.realize = realize
        
    def __repr__(self) -> str:
        return f"<{self.kind.title()} {self.name}>"
        
    def realize_state(self, new_state: OnOff)->None:
        s = self.on_val if new_state else self.off_val
        # print(f"Setting {self.name} to {new_state} ({s})")
        ec = self.realize(self.remote, s)
        if ec != pyglider.ErrorCode.ErrorSuccess:
            print(f"Error {ec} returned trying to set electrode {self.name} to {new_state}.")
            
class Electrode(BinState[pyglider.Electrode, pyglider.Electrode.ElectrodeState]):
    def __init__(self, name: str, remote: pyglider.Electrode) -> None:
        super().__init__(kind = "electrode",
                         name = name,
                         remote = remote,
                         on_val = pyglider.Electrode.ElectrodeState.On,
                         off_val = pyglider.Electrode.ElectrodeState.Off,
                         realize = lambda r,s: r.SetTargetState(s),
                         initial_state = lambda r: r.GetCurrentState() )
        
    def heater_names(self) -> list[str]:
        return self.remote.GetHeaters()
    
    def magnet_names(self) -> list[str]:
        return self.remote.GetMagnets()
    
class Magnet(BinState[pyglider.Magnet, pyglider.Magnet.MagnetState]):
    def __init__(self, name: str, remote: pyglider.Magnet) -> None:
        super().__init__(kind = "magnet",
                         name = name,
                         remote = remote,
                         on_val = pyglider.Magnet.MagnetState.On,
                         off_val = pyglider.Magnet.MagnetState.Off,
                         realize = lambda r,s: r.SetTargetState(s))
    
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
    magnets: Final[dict[str, Magnet]]
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
            
    @property
    def fan_state(self) -> OnOff:
        return OnOff.from_bool(self.remote.IsFanEnabled())
    
    @fan_state.setter
    def fan_state(self, val: OnOff) -> None:
        if val:
            self.remote.EnableFan()
        else:
            self.remote.DisableFan()
    
    def __init__(self, board_type: pyglider.BoardId, *,
                 dll_dir: Optional[Union[str, PathLike]] = None,
                 config_dir: Optional[Union[str, PathLike]] = None) -> None:
        if config_dir is None:
            config_dir = pathlib.Path.cwd()
        dll_dir = _to_path(dll_dir)
        config_dir = _to_path(config_dir)
        self.remote = pyglider.Board.Find(board_type, 
                                          dll_dir=dll_dir,
                                          config_dir=config_dir)
        # self.remote_electrodes = { e.GetName(): e for e in b.GetElectrodes()}
        # print(f"Remote: {self.remote_electrodes}")
        # self.electrodes = { k: Electrode(k, v) for k,v in self.remote_electrodes.items()}
        assert self.remote is not None, f"""
        Couldn't instantiate Glider client.  
        DLL dir is {"<search>" if dll_dir is None else dll_dir}
        config_dir is {config_dir}
        """
        self.electrodes = {}
        self.heaters = {}
        self.magnets = {}
        ec, n = self.remote.GetHighVoltage()
        if ec != pyglider.ErrorCode.ErrorSuccess:
            print(f"Error {ec} returned trying to read voltage level.")
            self._voltage_level = None
        else:
            print(f"The voltage level is {n}")
            self._voltage_level = n*volts
        
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
    
    def magnet(self, name: Optional[str]) -> Optional[Magnet]:
        if name is None:
            return None
        m = self.magnets.get(name)
        if m is None:
            re = self.remote.MagnetNamed(name)
            if re is None:
                print(f"No magnet named {name}")
            else:
                m = Magnet(name, re)
                self.magnets[name] = m
        return m
    
