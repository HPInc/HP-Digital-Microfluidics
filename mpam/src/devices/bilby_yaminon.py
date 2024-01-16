from __future__ import annotations

from devices import bilby, wombat

from typing import Final
from dmf.device import System
from dmf import device

class Board(bilby.Board):
    _yaminon: Final[wombat.Board]
    
    def __init__(self) -> None:
        with (wombat.Config.is_yaminon >> True
              & device.Config.owns_externals >> False
              ):
            self._yaminon = wombat.Board()
        super().__init__()
        self._yaminon.pipettor = self.pipettor
        
    def _add_pads(self)->None:
        self.pads.update(self._yaminon.pads)
        
    def _add_all_wells(self) -> None:
        assert len(self._well_list) == 0
        self._well_list.extend(self._yaminon.wells)
        
    def update_state(self)->None:
        self._yaminon.update_state()
        super().update_state()
        
        
    def finish_update(self)->None:
        # It's safe to call both, because inferring drop motion on super()
        # (Bilby) won't do anything (because no pads journal to it).  It's
        # necessary because changes to heater/chiller/magnet state will leave
        # callbacks to post results.
        self._yaminon.finish_update()
        super().finish_update()
        
    def join_system(self, system: System)->None:
        super().join_system(system)
        self._yaminon.join_system(system)
