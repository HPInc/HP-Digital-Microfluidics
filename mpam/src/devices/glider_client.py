from __future__ import annotations

from pathlib import Path
import pyglider
from typing import Union, Optional, Final
from mpam.types import State, OnOff
from os import PathLike

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
    

class GliderClient:
    remote: Final[pyglider.Board]
    electrodes: Final[dict[str, Electrode]]
    # remote_electrodes: Final[dict[str, pyglider.Electrode]]
    
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
