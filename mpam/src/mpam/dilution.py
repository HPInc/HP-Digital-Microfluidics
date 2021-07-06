from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Final, Optional, Sequence, Iterator, MutableMapping

from mpam.device import Pad
from mpam.drop import Drop
from mpam.processes import MultiDropProcessType, FinishFunction
from mpam.types import Reagent, Delayed, waste_reagent, Dir


class DilutionProcess(MultiDropProcessType):
    dilution_type: Final[DilutionType]
    result: Final[Optional[Reagent]]
    n_shuttles: Final[int]
    
    def __init__(self, dilution_type: DilutionType, *,
                 result: Optional[Reagent] = None,
                 n_shuttles: int = 0,
                 ) -> None:
        super().__init__(dilution_type.n_drops)
        self.dilution_type = dilution_type
        self.result = result
        self.n_shuttles = n_shuttles
        
    def __repr__(self) -> str:
        return f"""<DilutionProcess: {self.dilution_type}, 
                        result={self.result}, 
                        shuttles={self.n_shuttles}>"""

    def secondary_pads(self, lead_drop_pad: Pad) -> Sequence[Pad]:  # @UnusedVariable
        return self.dilution_type.secondary_pads(lead_drop_pad)
        
    # returns the finish function when done
    def iterator(self, drops: tuple[Drop, ...]) -> Iterator[Optional[FinishFunction]]:  # @UnusedVariable
        i = self.dilution_type.perform(drops = drops, n_shuttles = self.n_shuttles)
        while next(i):
            yield None
                
        result = self.result
        fully_diluted = { drops[i] for i in self.dilution_type.fully_diluted()}
        def finish(futures: MutableMapping[Drop, Delayed[Drop]]) -> bool:  # @UnusedVariable
            for drop in drops:
                if drop in fully_diluted:
                    if result is not None:
                        drop.reagent = result
                else:
                    drop.reagent = waste_reagent
            return True
        yield finish
            
        
        
class DilutionType(ABC):
    is_approximate: Final[bool]
    n_drops: Final[int]
    
    def __init__(self, *, n_drops: int, is_approximate: bool) -> None:
        self.n_drops = n_drops
        self.is_approximate = is_approximate

    @abstractmethod            
    def secondary_pads(self, lead_drop_pad: Pad) -> Sequence[Pad]: ...  # @UnusedVariable
    
    @abstractmethod
    def fully_diluted(self) -> Sequence[int]: ...
    
    @abstractmethod    
    def perform(self, *,
                drops: tuple[Drop,...],     # @UnusedVariable
                n_shuttles: int,            # @UnusedVariable
                ) -> Iterator[bool]:
        ...
        
    def two_steps_from(self, pad: Pad, direction: Dir) -> Pad:
        m = pad.neighbor(direction)
        assert m is not None
        p = m.neighbor(direction)
        assert p is not None
        return p
    
    