from __future__ import annotations

import logging

from mpam import exerciser
from mpam.pipettor import Pipettor, Transfer
from argparse import Namespace
from mpam.types import XferDir

logger = logging.getLogger(__name__)

class ManualPipettor(Pipettor):
    def __init__(self, *,
                 name: str="Manual Pipettor",
                 ) -> None:
        super().__init__(name=name)

    def perform(self, transfer: Transfer) -> None:
        reagent = transfer.reagent
        for target in transfer.targets:
            loc = target.target
            vol = target.volume
            target.in_position(reagent, vol)
            if transfer.xfer_dir is XferDir.FILL:
                print(f"Please add {vol} of {reagent} to {loc}.")
            else:
                product = "product " if transfer.is_product else ""
                print(f"Please remove {vol} of {product}{reagent} from {loc}")
            print("Hit return when done.")
            input()
            target.finished(reagent, vol)
        for target in transfer.targets:
            target.finished_overall_transfer(reagent)

class PipettorConfig(exerciser.PipettorConfig):
    def __init__(self) -> None:
        super().__init__("manual")
    
    def create(self, _args: Namespace) -> Pipettor:
        return ManualPipettor()