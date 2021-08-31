from __future__ import annotations

from typing import Final, Sequence, NamedTuple, Mapping, Optional

from mpam.device import Pad


class PathStep(NamedTuple):
    next: Optional[Pad]
    number: int

class Pathway:
    _pads: Final[Sequence[Pad]]
    _steps: Optional[Mapping[Pad, PathStep]] = None
    
    @property
    def first(self) -> Pad:
        return self._pads[0]
    
    @property
    def steps(self) -> Mapping[Pad, PathStep]:
        d = self._steps
        if d is None:
            d = {}
            prev = self.first
            for i,p in enumerate(self._pads[1:]):
                d[prev] = PathStep(p,i)
                prev = p
            d[self.last] = PathStep(None,len(self._pads)-1)
            self._steps = d
        return d
    
    @property
    def last(self) -> Pad:
        return self._pads[-1]
    
    def __init__(self, pads: Sequence[Pad]) -> None:
        assert(len(pads) > 0)
        self._pads = pads 
        
    def next(self, pad: Pad) -> Optional[Pad]:
        return self.steps[pad].next
    
    def number(self, pad: Pad) -> int:
        return self.steps[pad].number
    
    def __contains__(self, pad: Pad) -> bool: 
        return pad in self.steps
    
    @classmethod
    def starting_at(cls, pad: Pad) -> Pathway:
        assert pad.exists
        return Pathway((pad,))
    
    def to_col(self, col: int) -> Pathway:
        current = self.last
        current_col = current.column
        if col == current_col:
            return self
        row = current.row
        board = current.board
        new_pads = list(self._pads)
        step = 1 if col > current_col else -1
        while current_col != col:
            current_col += step
            p = board.pad_at(current_col, row)
            assert p.exists
            new_pads.append(p)
        return Pathway(new_pads)
            
    def to_row(self, row: int) -> Pathway:
        current = self.last
        current_row = current.row
        if row == current_row:
            return self
        col = current.column
        board = current.board
        new_pads = list(self._pads)
        step = 1 if row > current_row else -1
        while current_row != row :
            current_row += step
            p = board.pad_at(col, current_row)
            assert p.exists
            new_pads.append(p)
        return Pathway(new_pads)
            
    def entry_for(self, pad: Pad, exit_at: Optional[Pad] = None) -> Pad:
        if exit_at is None:
            exit_at = self.last
