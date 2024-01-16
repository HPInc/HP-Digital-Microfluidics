from __future__ import annotations

from typing import Final, TYPE_CHECKING

from sifu.grid import XYCoord


if TYPE_CHECKING:
    from .device import Pad, Well, BinaryComponent

class MPAMError(RuntimeError): ...

class PadBrokenError(MPAMError):
    pad: Final[BinaryComponent]
    def __init__(self, pad: BinaryComponent):
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
        
class NoSuchPad(MPAMError):
    loc: Final[XYCoord]
    def __init__(self, loc: XYCoord):
        super().__init__(f"No usable pad at {loc}")
        self.loc = loc
        
class UnsafeMotion(MPAMError):
    pad: Final[Pad]
    def __init__(self, pad: Pad):
        super().__init__(f"Motion travels through unsafe {pad}")
        self.pad = pad

class NotAtWell(MPAMError): ...
    