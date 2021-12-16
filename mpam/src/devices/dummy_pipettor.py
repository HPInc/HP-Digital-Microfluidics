from __future__ import annotations

from enum import Enum, auto
from time import sleep

from mpam.pipettor import Pipettor, Transfer, EmptyTarget
from mpam.types import XferDir, waste_reagent
from quantities.SI import seconds, second, uL
from quantities.core import DerivedDim
from quantities.dimensions import Time, Volume
from mpam.device import ProductLocation


class ArmPos(Enum):
    BOARD = auto()
    REAGENTS = auto()
    PRODUCTS = auto()
    TIPS = auto()
    WASTE = auto()

class FlowRate(DerivedDim['FlowRate']):
    derived = Volume.dim()/Time.dim()


class DummyPipettor(Pipettor):
    dip_time: Time
    short_transit_time: Time
    long_transit_time: Time
    drop_tip_time: Time
    get_tip_time: Time
    flow_rate: FlowRate
    next_product: int
    
    arm_pos: ArmPos
    
    def __init__(self, *,
                 name: str="Dummy Pipettor",
                 dip_time: Time = 0.25*seconds,
                 short_transit_time: Time = 0.5*seconds,
                 long_transit_time: Time = 1*second,
                 get_tip_time: Time = 0.5*seconds,
                 drop_tip_time: Time = 0.5*seconds,
                 flow_rate: FlowRate = (100*uL/second).a(FlowRate),
                 ) -> None:
        super().__init__(name=name)
        self.arm_pos = ArmPos.WASTE
        self.dip_time = dip_time
        self.short_transit_time = short_transit_time
        self.long_transit_time = long_transit_time
        self.get_tip_time = get_tip_time
        self.drop_tip_time = drop_tip_time
        self.flow_rate = flow_rate
        self.next_product = 1
        
    def speed_up(self, factor: float) -> None:
        self.dip_time /= factor
        self.short_transit_time /= factor
        self.long_transit_time /= factor
        self.drop_tip_time /= factor
        self.get_tip_time /= factor
        self.flow_rate *= factor
        
    def _sleep_for(self, time: Time) -> None:
        sleep(time.as_number(seconds))
        
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
        
        total_volume = sum((x.volume for x in transfer.targets), start = Volume.ZERO())

        self.move_to(ArmPos.TIPS)
        self.down()
        self.get_tip()
        self.up()
        if transfer.xfer_dir is XferDir.FILL:
            self.move_to(ArmPos.REAGENTS)
            self.down()
            self.xfer(total_volume)
            print(f"Aspirating {total_volume} of {reagent} from reagent block.")
            self.up()
        self.move_to(ArmPos.BOARD)
        for x in transfer.targets:
            self.down()
            x.in_position(reagent, x.volume)
            self.xfer(x.volume)
            if transfer.xfer_dir is XferDir.EMPTY:
                print(f"Aspirating {x.volume} of {reagent} from {x.target}.")
            else:
                print(f"Dispensing {x.volume} of {reagent} to {x.target}.")
            x.finished(reagent, x.volume)
            self.up()
        # Since we do pretend to do the whole thing each time, this shouldn't do anything.
        for x in transfer.targets:
            x.finished_overall_transfer(reagent)
        if transfer.xfer_dir is XferDir.EMPTY:
            if reagent is waste_reagent:
                self.move_to(ArmPos.WASTE)
                self.xfer(total_volume)
                print(f"Dumping {total_volume} of {reagent} to trash.")
            else:
                self.move_to(ArmPos.PRODUCTS if transfer.is_product else ArmPos.REAGENTS)
                self.down()
                self.xfer(total_volume)
                print(f"Dispensing {total_volume} of {reagent} to {self.arm_pos}.")
                self.up()
                if transfer.is_product:
                    loc = ProductLocation(reagent, f"Product well {self.next_product}")
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