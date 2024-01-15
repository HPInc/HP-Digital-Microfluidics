from __future__ import annotations

from argparse import _ArgumentGroup
from enum import Enum, auto
import logging
from typing import Optional, Final, Mapping, Callable

from sifu.config import ConfigParam
from sifu.quant.SI import seconds, second, uL
from sifu.quant.dimensions import Time, Volume, FlowRate
from mpam import exerciser
from mpam.device import ProductLocation
from mpam.pipettor import Pipettor, Transfer, EmptyTarget, PipettingSource
from mpam.types import XferDir, waste_reagent, Reagent


logger = logging.getLogger(__name__)


class ArmPos(Enum):
    BOARD = auto()
    REAGENTS = auto()
    PRODUCTS = auto()
    TIPS = auto()
    WASTE = auto()

class Config:
    dip_time: Final = ConfigParam(0.25*seconds)
    short_transit_time: Final = ConfigParam(0.5*seconds)
    long_transit_time: Final = ConfigParam(1*second)
    get_tip_time: Final = ConfigParam(0.5*seconds)
    drop_tip_time: Final = ConfigParam(0.5*seconds)
    flow_rate: Final = ConfigParam(100*uL/second)
    n_plates: Final = ConfigParam(1)
    speed_up: Final = ConfigParam[Optional[float]](None)


class DummyPipettor(Pipettor):
    dip_time: Time
    short_transit_time: Time
    long_transit_time: Time
    drop_tip_time: Time
    get_tip_time: Time
    flow_rate: FlowRate
    next_product: int

    arm_pos: ArmPos

    _sources_by_reagent: Final[dict[Reagent, PipettingSource]]
    _sources_by_name: Final[Mapping[str, PipettingSource]]
    _unallocated_sources: Final[list[PipettingSource]]

    def __init__(self, *,
                 name: str="Dummy Pipettor",
                 ) -> None:
        super().__init__(name=name)
        self.arm_pos = ArmPos.WASTE
        self.dip_time = Config.dip_time()
        self.short_transit_time = Config.short_transit_time()
        self.long_transit_time = Config.long_transit_time()
        self.get_tip_time = Config.get_tip_time()
        self.drop_tip_time = Config.drop_tip_time()
        self.flow_rate = Config.flow_rate()
        self.next_product = 1

        source_names = self._generate_source_names(plates=Config.n_plates())
        sources = self._generate_sources_named(source_names)
        self._unallocated_sources = sources
        self._sources_by_reagent = {}
        self._sources_by_name = {s.name: s for s in sources}
        for source in sources:
            def remember_source(s: PipettingSource) -> Callable[[Reagent], None]:
                def doit(r: Reagent) -> None:
                    logger.info(f"Reagent {r} is in source {s.name}")

                    self._sources_by_reagent[r] = s
                return doit
            source.assigned_reagent.when_value(remember_source(source))

        speed_up = Config.speed_up()
        if speed_up is not None:
            self.speed_up(speed_up)


    def source_named(self, name: str) -> Optional[PipettingSource]:
        return self._sources_by_name.get(name, None)

    def _new_source_for(self, reagent: Reagent) -> PipettingSource:
        unassigned = self._unallocated_sources
        while len(unassigned) > 0:
            source = self._unallocated_sources.pop(0)
            if not source.is_assigned:
                source.reagent = reagent
                # source.exact_volume = 0*uL
                return source

        raise ValueError(f"No unallocated sources available for {reagent}")


    def sources_for(self, reagent: Reagent) -> tuple[PipettingSource]:
        return (self.source_for(reagent),)

    def source_for(self, reagent: Reagent) -> PipettingSource:
        source = self._sources_by_reagent.get(reagent)
        if source is None:
            source = self._new_source_for(reagent)
        return source


    def speed_up(self, factor: float) -> None:
        self.dip_time /= factor
        self.short_transit_time /= factor
        self.long_transit_time /= factor
        self.drop_tip_time /= factor
        self.get_tip_time /= factor
        self.flow_rate *= factor

    def _sleep_for(self, time: Time) -> None:
        time.sleep()

    def move_to(self, pos: ArmPos) -> None:
        if pos is self.arm_pos:
            self._sleep_for(self.short_transit_time)
        else:
            self._sleep_for(self.long_transit_time)
            self.arm_pos = pos

    def down(self) -> None:
        self._sleep_for(self.dip_time)

    def up(self) -> None:
        self._sleep_for(self.dip_time)

    def drop_tip(self) -> None:
        self._sleep_for(self.drop_tip_time)

    def get_tip(self) -> None:
        self._sleep_for(self.get_tip_time)

    def xfer(self, volume: Volume) -> None:
        t = volume/self.flow_rate
        self._sleep_for(t)


    def perform(self, transfer: Transfer) -> None:
        reagent = transfer.reagent

        total_volume = transfer.total_volume
        
        ustr = self.user_str

        self.move_to(ArmPos.TIPS)
        self.down()
        self.get_tip()
        self.up()
        source = self.source_for(reagent)
        if transfer.xfer_dir is XferDir.FILL:
            for x in transfer.targets:
                x.on_insufficient.expect_true(source.max_volume >= x.volume,
                                              lambda: (f"{source.name} has "
                                                       + f"{'at most ' if source.exact_volume is None else ''}"
                                                       + f"{ustr(source.max_volume)} of {ustr(source.reagent)}. "
                                                       + f"{ustr(x.volume)} needed."))
                if source.max_volume < x.volume:
                    extra = 100*uL
                    logger.info(f"Adding {ustr(extra)} to {source.name}")
                    source += extra
                source -= x.volume
            self.move_to(ArmPos.REAGENTS)
            self.down()
            self.xfer(total_volume)
            logging.info(f"Aspirating {ustr(total_volume)} of {ustr(reagent)} from {source.name}.")
            self.up()
        self.move_to(ArmPos.BOARD)
        for x in transfer.targets:
            self.down()
            x.in_position(reagent, x.volume)
            self.xfer(x.volume)
            if transfer.xfer_dir is XferDir.EMPTY:
                logging.info(f"Aspirating {ustr(x.volume)} of {ustr(reagent)} from {ustr(x.target)}.")
            else:
                logging.info(f"Dispensing {ustr(x.volume)} of {ustr(reagent)} to {ustr(x.target)}.")
            x.finished(reagent, x.volume)
            self.up()
        # Since we do pretend to do the whole thing each time, this shouldn't do anything.
        for x in transfer.targets:
            x.finished_overall_transfer(reagent)
        if transfer.xfer_dir is XferDir.EMPTY:
            if reagent is waste_reagent:
                self.move_to(ArmPos.WASTE)
                self.xfer(total_volume)
                logging.info(f"Dumping {ustr(total_volume)} of {ustr(reagent)} to trash.")
            else:
                self.move_to(ArmPos.PRODUCTS if transfer.is_product else ArmPos.REAGENTS)
                self.down()
                self.xfer(total_volume)
                logging.info(f"Dispensing {ustr(total_volume)} of {ustr(reagent)} to {self.arm_pos}.")
                self.up()
                if transfer.is_product:
                    loc = ProductLocation(reagent, f"Product well {ustr(self.next_product)}")
                    self.next_product += 1
                    for x in transfer.targets:
                        assert isinstance(x, EmptyTarget)
                        x.note_product_loc(loc)
        if transfer.is_product:
            self.move_to(ArmPos.WASTE)
            self.drop_tip()
        else:
            self.move_to(ArmPos.TIPS)
            self.down()
            self.drop_tip()
            self.up()

class PipettorConfig(exerciser.PipettorConfig):
    def __init__(self) -> None:
        super().__init__("simulated", DummyPipettor, aliases=("sim", "dummy"))


    def add_args_to(self, group:_ArgumentGroup)->None:
        super().add_args_to(group)
        Config.speed_up.add_arg_to(group, '-ps', '--pipettor-speed', type=float, metavar='MULT',
                                   help="A speed-up factor for dummy pipettor operations.")
        default_n_well_plates = 1
        Config.n_plates.add_arg_to(group, '--n-well-plates', type=int, metavar='INT', default=default_n_well_plates,
                                   help=f"The number of well plates to model.  Default is {default_n_well_plates}.")
