from __future__ import annotations

from typing import Final, Optional, Union, Sequence

from mpam.device import Pad
from mpam.drop import Drop
from mpam.processes import MultiDropProcessType
from mpam.types import Reagent
from mpam.mixing import MixingBase
from abc import abstractmethod


class DilutionProcess(MultiDropProcessType):
    dilution_type: Final[DilutionType]
    result: Final[Optional[Reagent]]
    n_shuttles: Final[int]
    
    def __init__(self, dilution_type: DilutionType, *,
                 result: Optional[Reagent] = None,
                 tolerance: float = 0.1,
                 n_shuttles: int = 0,
                 fully_mix: Union[bool, Sequence[int]] = False,
                 ) -> None:
        super().__init__(dilution_type.n_drops)
        self.dilution_type = dilution_type
        self.result = result
        self.tolerance = tolerance
        self.n_shuttles = n_shuttles
        self.fully_mix = fully_mix
        
    def __repr__(self) -> str:
        return f"""<DilutionProcess: {self.dilution_type}, 
                        result={self.result}, 
                        shuttles={self.n_shuttles}>"""

    def secondary_pads(self, lead_drop: Drop) -> Sequence[Pad]:  # @UnusedVariable
        return self.dilution_type.secondary_pads(lead_drop)
        
        
class DilutionType(MixingBase):
    @abstractmethod            
    def secondary_pads(self, lead_drop: Drop) -> Sequence[Pad]: ...  # @UnusedVariable
    
    
    