from __future__ import annotations

import pyglider
from pathlib import Path
from devices.glider_client import GliderClient
from erk.basic import not_None
from mpam.types import OnOff

help(pyglider.Board)

# wallaby = pyglider.Board.Find(pyglider.BoardId.Wallaby,
#                               dll_dir = Path("d:\\dmf-git\\DynamicHAL\\x64\\Debug"),
#                               config_dir = Path("d:\\dmf-git\\DynamicHAL\\WallabyHAL"))
wallaby = GliderClient(pyglider.BoardId.Wallaby,
                       dll_dir = Path("d:\\dmf-git\\DynamicHAL\\x64\\Debug"),
                       config_dir = Path("d:\\dmf-git\\DynamicHAL\\WallabyHAL"))

e = not_None(wallaby.electrode("G07"))
e.realize_state(OnOff.ON)
wallaby.update_state()
