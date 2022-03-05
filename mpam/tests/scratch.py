from __future__ import annotations

import pyglider
from pathlib import Path


wallaby = pyglider.Board.Find(pyglider.BoardId.Wallaby,
                              dll_dir = Path("d:\\dmf-git\\DynamicHAL\\x64\\Debug"),
                              config_dir = Path("d:\\dmf-git\\DynamicHAL\\WallabyHAL"))
print(wallaby)
print((wallaby.GetBoardRows(), wallaby.GetBoardColumns()))

es = wallaby.GetElectrodes()
print(len(es))
print(es[0])
# print(pyglider.test())

print([e.GetCoordinates() for e in es[0:5]])
print([e.GetCurrentState() for e in es[0:5]])
print([e.GetName() for e in es[130:132]])
print([e.GetName() for e in es[130:132]])
# print(wallaby.GetHeaters()[0].GetName())
# print(es[0].GetCoordinates())

# print(wallaby.GetElectrodes())
# print(wallaby.GetElectrodes()[0].GetName())
# wallaby: pyglider.Board


# import pyglider;
# pyglider.Bo
# # wallaby = pyglider.Board.Find(pyglider.BoardId.Wallaby, "d:\\dmf-git\\DynamicHAL\\x64\\Debug")
# wallaby = pyglider.Board.Find(pyglider.BoardId.Wallaby, "..\\local\\glider")


