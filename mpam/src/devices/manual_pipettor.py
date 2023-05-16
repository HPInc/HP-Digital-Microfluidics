from __future__ import annotations

import logging

from mpam import exerciser
from mpam.pipettor import Pipettor, Transfer, PipettingSource
from mpam.types import XferDir, Reagent, Postable
from typing import Final, Mapping, Sequence
from _collections import defaultdict
from erk.stringutils import conj_str
from quantities.dimensions import Volume
from erk.config import ConfigParam
from argparse import _ArgumentGroup
from quantities.SI import uL
import math

logger = logging.getLogger(__name__)

class Config:
    rounding: Final = ConfigParam(0.5)

class ManualPipettor(Pipettor):
    _sources_by_reagent: Final[dict[Reagent, list[PipettingSource]]]
    _sources_by_name: Final[Mapping[str, PipettingSource]]
    _ad_hoc_sources: Final[set[PipettingSource]]
    
    def __init__(self, *,
                 name: str="Manual Pipettor",
                 ) -> None:
        super().__init__(name=name)
        self._sources_by_reagent = defaultdict(list)
        self._sources_by_name = {}
        self._ad_hoc_sources = set()
        
    def source_named(self, name:str)->PipettingSource:
        source = self._sources_by_name.get(name, None)
        if source is None:
            source = PipettingSource(name, pipettor=self)
            s = source
            def remember_source(r: Reagent) -> None:
                self._sources_by_reagent[r].append(s)
            source.assigned_reagent.when_value(remember_source)
        return source
    
    def sources_for(self, reagent: Reagent) -> Sequence[PipettingSource]:
        sources = self._sources_by_reagent[reagent]
        if len(sources) == 0:
            name = f"well[{reagent.name}]"
            source = self.source_named(name)
            source.reagent = reagent
            self._ad_hoc_sources.add(source)
        return sources

    def _adjust_source(self, v: Volume, sources: Sequence[PipettingSource]) -> None:
        for source in sources:
            if v <= source.max_volume:
                source -= v
                return
            else:
                v -= source.max_volume
                source.exact_volume = Volume.ZERO
        # If we get here, as far as we know, everybody is empty, but for a
        # manual pipettor, we don't worry about it.

    def perform(self, transfer: Transfer) -> None:
        reagent = transfer.reagent
        sources = self.sources_for(reagent)
        
        not_ad_hoc = [s for s in sources if s not in self._ad_hoc_sources]
        if len(not_ad_hoc) == 0:
            sdesc = ""
        elif len(not_ad_hoc) == 1:
            source, = not_ad_hoc
            sdesc = f" (found in {source.name})"
        else:
            sdesc = f" (found in {conj_str([s.name for s in not_ad_hoc])})"

        for target in transfer.targets:
            loc = target.target
            vol = target.volume
            rounding = Config.rounding()
            if rounding >= 0:
                n = vol.as_number(uL)
                n = math.ceil(n/rounding)*rounding
                vol = n*uL
            target.in_position(reagent, vol)
            if transfer.xfer_dir is XferDir.FILL:
                msg = f"Please add {vol:g} of {reagent}{sdesc} to {loc}."
                self._adjust_source(vol, sources)
            else:
                product = "product " if transfer.is_product else ""
                msg = f"Please remove {vol:g} of {product}{reagent} from {loc}"
            future = Postable[None]()
            self.system.prompt_and_wait(future, prompt = msg)
            future.wait()
            target.finished(reagent, vol)
        for target in transfer.targets:
            target.finished_overall_transfer(reagent)

class PipettorConfig(exerciser.PipettorConfig):
    def __init__(self) -> None:
        super().__init__("manual")
        
    def add_args_to(self, group:_ArgumentGroup)->None:
        super().add_args_to(group)
        Config.rounding.add_arg_to(group, '--transfer-rounding', type=float, metavar='TO',
                                    help=f'''Manual transfers will round up to this resolution, in {uL}.
                                        A value of zero indicates no rounding.
                                        ''')
    
    def create(self) -> Pipettor:
        return ManualPipettor()