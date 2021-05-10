from __future__ import annotations
from typing import Final, TYPE_CHECKING

if TYPE_CHECKING:
    from mpam.device import Pad, Well

class MPAMError(RuntimeError): ...

class PadBrokenError(MPAMError):
    pad: Final[Pad]
    def __init__(self, pad: Pad):
        super().__init__(f"{pad} is broken")
        self.pad = pad
        
class WellEmptyError(MPAMError):
    well: Final[Well]
    def __init__(self, well: Well):
        super().__init__(f"{well} is empty")
        self.well = well

class WellFullError(MPAMError):
    well: Final[Well]
    def __init__(self, well: Well):
        super().__init__(f"{well} is full")
        self.well = well

    