from __future__ import annotations

from enum import Enum, auto
import logging

from mpam.pipettor import Pipettor, Transfer, EmptyTarget, PipettingSource,\
     WellPlate384, WellPlate96
from mpam.types import XferDir, waste_reagent, Reagent
from quantities.SI import seconds, second, uL
from quantities.core import DerivedDim
from quantities.dimensions import Time, Volume
from mpam.device import ProductLocation
from mpam import exerciser
from argparse import Namespace, _ArgumentGroup
from typing import Optional, Final, Mapping, Callable

logger = logging.getLogger(__name__)


class ArmPos(Enum):
    BOARD = auto()
    REAGENTS = auto()
    PRODUCTS = auto()
    TIPS = auto()
    WASTE = auto()

class FlowRate(DerivedDim):
    derived = Volume/Time


class DummyPipettor(Pipettor):
    dip_time: Time
    short_transit_time: Time
    long_transit_time: Time
    drop_tip_time: Time
    get_tip_time: Time
    flow_rate: FlowRate

    arm_pos: ArmPos
    
    _sources_by_reagent: Final[dict[Reagent, PipettingSource]]
    _sources_by_name: Final[Mapping[str, PipettingSource]]
    _unallocated_sources: Final[list[PipettingSource]]
    _unallocated_product_wells: Final[list[PipettingSource]]

    def __init__(self, *,
                 name: str="Dummy Pipettor",
                 dip_time: Time = 0.25*seconds,
                 short_transit_time: Time = 0.5*seconds,
                 long_transit_time: Time = 1*second,
                 get_tip_time: Time = 0.5*seconds,
                 drop_tip_time: Time = 0.5*seconds,
                 flow_rate: FlowRate = (100*uL/second).a(FlowRate),
                 n_source_plates: int = 1,
                 n_product_plates: int = 1,
                 speed_up: Optional[float] = None,
                 ) -> None:
        super().__init__(name=name)
        self.arm_pos = ArmPos.WASTE
        self.dip_time = dip_time
        self.short_transit_time = short_transit_time
        self.long_transit_time = long_transit_time
        self.get_tip_time = get_tip_time
        self.drop_tip_time = drop_tip_time
        self.flow_rate = flow_rate
        
        source_names = self._generate_source_names(plates=n_source_plates,
                                                   plate_type=WellPlate96,
                                                   prefix="source well ")
        sources = self._generate_sources_named(source_names)
        self._unallocated_sources = sources
        self._sources_by_reagent = {}
        self._sources_by_name = {s.name: s for s in sources}
        for source in sources:
            def remember_source(s: PipettingSource) -> Callable[[Reagent], None]:
                def doit(r: Reagent) -> None:
                    logger.info(f"Reagent {r} is in {s.name}")
                    
                    self._sources_by_reagent[r] = s
                return doit
            source.assigned_reagent.when_value(remember_source(source))
        
        product_names = self._generate_source_names(plates=n_product_plates,
                                                    plate_type=WellPlate384,
                                                    prefix="product well ")
        products = self._generate_sources_named(product_names)
        self._unallocated_product_wells = products

        if speed_up is not None:
            self.speed_up(speed_up)
        
        
    def source_named(self, name: str) -> Optional[PipettingSource]:
        return self._sources_by_name.get(name, None)
    
    def _assign_well(self, reagent: Reagent,
                     unassigned: list[PipettingSource],
                     kind: str) -> PipettingSource:
        while len(unassigned) > 0:
            source = self._unallocated_sources.pop(0)
            if not source.is_assigned:
                source.reagent = reagent
                return source
        
        raise ValueError(f"No unallocated {kind} wells available for {reagent}")
        
    
    def _new_source_for(self, reagent: Reagent) -> PipettingSource:
        return self._assign_well(reagent, self._unallocated_sources, "source")
    
    def sources_for(self, reagent: Reagent) -> tuple[PipettingSource]:
        return (self.source_for(reagent),)
    
    def source_for(self, reagent: Reagent) -> PipettingSource:
        source = self._sources_by_reagent.get(reagent)
        if source is None:
            source = self._new_source_for(reagent)
        return source

    def _product_well_for(self, reagent: Reagent) -> PipettingSource:
        return self._assign_well(reagent, self._unallocated_product_wells, "product")
        

    def speed_up(self, factor: float) -> None:
        self.dip_time /= factor
        self.short_transit_time /= factor
        self.long_transit_time /= factor
        self.drop_tip_time /= factor
        self.get_tip_time /= factor
        self.flow_rate *= factor

    def _sleep_for(self, time: Time) -> None:
        time.sleep()

    def move_to(self, pos = ArmPos) -> None:
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
        t = (volume/self.flow_rate).a(Time)
        self._sleep_for(t)


    def perform(self, transfer: Transfer) -> None:
        reagent = transfer.reagent

        total_volume = transfer.total_volume

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
                                                       + f"{source.max_volume} of {source.reagent}. "
                                                       + f"{x.volume} needed."))
                if source.max_volume < x.volume:
                    extra = 100*uL
                    logger.info(f"Adding {extra} to {source.name}")
                    source += extra
                source -= x.volume
            self.move_to(ArmPos.REAGENTS)
            self.down()
            self.xfer(total_volume)
            logging.info(f"Aspirating {total_volume} of {reagent} from {source.name}.")
            self.up()
        self.move_to(ArmPos.BOARD)
        for x in transfer.targets:
            self.down()
            x.in_position(reagent, x.volume)
            self.xfer(x.volume)
            if transfer.xfer_dir is XferDir.EMPTY:
                logging.info(f"Aspirating {x.volume} of {reagent} from {x.target}.")
            else:
                logging.info(f"Dispensing {x.volume} of {reagent} to {x.target}.")
            x.finished(reagent, x.volume)
            self.up()
        # Since we do pretend to do the whole thing each time, this shouldn't do anything.
        for x in transfer.targets:
            x.finished_overall_transfer(reagent)
        if transfer.xfer_dir is XferDir.EMPTY:
            if reagent is waste_reagent:
                self.move_to(ArmPos.WASTE)
                self.xfer(total_volume)
                logging.info(f"Dumping {total_volume} of {reagent} to trash.")
            else:
                if transfer.is_product:
                    dest = self._product_well_for(reagent)
                    self.move_to(ArmPos.PRODUCTS)
                else:
                    dest = self.source_for(reagent)
                    self.move_to(ArmPos.REAGENTS)
                self.down()
                self.xfer(total_volume)
                logging.info(f"Dispensing {total_volume} of {reagent} to {dest.name}.")
                self.up()
                if transfer.is_product:
                    loc = ProductLocation(reagent, dest.name)
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
        super().__init__("simulated", aliases=("sim", "dummy"))

    def create(self, args: Namespace) -> Pipettor:
        speedup: Optional[float] = args.pipettor_speed
        n_source_plates: int = args.n_source_plates
        n_product_plates: int = args.n_product_plates
        pipettor = DummyPipettor(n_source_plates = n_source_plates,
                                 n_product_plates = n_product_plates, 
                                 speed_up = speedup)
        return pipettor
    
    def add_args_to(self, group:_ArgumentGroup)->None:
        super().add_args_to(group)
        group.add_argument('-ps', '--pipettor-speed', type=float, metavar='MULT',
                           help="A speed-up factor for dummy pipettor operations.")
        default_n_source_plates = 1
        default_n_product_plates = 1
        group.add_argument('--n-source-plates', type=int, metavar='INT', default=default_n_source_plates,
                           help=f"The number of well plates to model.  Default is {default_n_source_plates}.")
        group.add_argument('--n-product-plates', type=int, metavar='INT', default=default_n_product_plates,
                           help=f"The number of well plates to model.  Default is {default_n_product_plates}.")
        