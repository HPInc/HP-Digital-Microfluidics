from __future__ import annotations

from _collections import defaultdict
from enum import Enum, auto
import json
from typing import Sequence

from opentrons import protocol_api
from opentrons.protocol_api.instrument_context import InstrumentContext
from opentrons.protocol_api.labware import Well, Labware


def load_config(name: str):
    with open(name, 'rb') as f:
        return json.load(f)
        
def labware_from_config(spec, protocol: protocol_api.ProtocolContext) -> Labware:
    labware: Labware = protocol.load_labware(spec["name"], spec["slot"])
    return labware

def pipette_from_config(spec, 
                        protocol: protocol_api.ProtocolContext,
                        tipracks: Sequence[Labware]) -> InstrumentContext:
    pipette: InstrumentContext = protocol.load_instrument(spec["name"], spec["side"], 
                                                          tip_racks = tipracks)
    return pipette

class Joey:
    plate: Labware
    wells: Sequence[Well]
    extraction_ports: Sequence[Well]
    drop_size: float
    
    def __init__(self,
                 spec, 
                 protocol: protocol_api.ProtocolContext) -> None:
        self.plate = labware_from_config(spec["labware"], protocol)
        self.drop_size = spec["drop-size"]
        self.wells = [self.plate[w] for w in spec["wells"]]
        self.extraction_ports = [self.plate[w] for w in spec["extraction-ports"]]
        
class Direction(Enum):
    FILL = auto()
    EMPTY = auto()
        
class Robot:
    protocol: protocol_api.ProtocolContext
    large_tipracks: Sequence[Labware]
    small_tipracks: Sequence[Labware]
    large_tips: list[Well]
    small_tips: list[Well]
    input_plates: Sequence[Labware] 
    output_plates: Sequence[Labware]
    output_wells: list[Well]
    large_pipette: InstrumentContext
    small_pipette: InstrumentContext
    threshold: float
    reagent_small_tip: dict[str, Well]
    reagent_large_tip: dict[str, Well]
    reagent_source: dict[str, list[tuple[Well, float]]]
    trash: Labware
    _next_product: int
    
    def message(self, msg: str) -> None:
        self.protocol.comment(msg)
    
    def __init__(self, config, protocol: protocol_api.ProtocolContext):
        self.protocol = protocol
        self.message("Creating the robot")
        self.large_tipracks = [labware_from_config(s,protocol) for s in config["tipracks"]["large"]]
        self.large_tips = []
        for tr in self.large_tipracks:
            self.large_tips += tr.wells()
        self.small_tipracks = [labware_from_config(s,protocol) for s in config["tipracks"]["small"]]
        self.small_tips = []
        for tr in self.small_tipracks:
            self.small_tips += tr.wells()
        self.input_plates = [labware_from_config(s,protocol) for s in config["input-wellplates"]]
        self.output_plates = [labware_from_config(s,protocol) for s in config["output-wellplates"]]
        self.output_wells = []
        for p in self.output_plates:
            self.output_wells += p.wells()
        
        self.large_pipette = pipette_from_config(config["pipettes"]["large"], protocol, self.large_tipracks) 
        self.small_pipette = pipette_from_config(config["pipettes"]["small"], protocol, self.small_tipracks)
        self.threshold: float = config["pipettes"]["small"]["max"] 
        self.reagent_small_tip = defaultdict(lambda: self.small_tips.pop(0))
        self.reagent_large_tip = defaultdict(lambda: self.large_tips.pop(0))
        self.reagent_source = {}
        for spec in config["reagents"]:
            rn = spec["name"]
            rw: list[tuple[Well, float]] = []
            for ws in spec["wells"]:
                rp = self.input_plates[ws["plate"]]
                rw.append((rp[ws["well"]], ws["quantity"]))
            self.reagent_source[rn] = rw
        
        
        self.trash = protocol.load_labware("opentrons_1_trash_1100ml_fixed", 12)
        
        self._next_product = 0
            
    def pipette_and_tip(self, reagent: str, volume: float) -> tuple[InstrumentContext, Well]:
        if volume > self.threshold:
            p = self.large_pipette
            tips = self.reagent_large_tip
        else:
            p = self.small_pipette
            tips = self.reagent_small_tip
        return (p, tips[reagent])
    
    # def acquire(self, reagent: str, pipette: InstrumentContext, volume: float,
    #             *, have: float = 0) -> float:
    #     need = min(volume, pipette.max_volume-have)
    #     while need > 0:
    #         sw, sv = self.reagent_source[reagent].pop(0)
    #         if sv > need:
    #             self.reagent_source[reagent].insert(0, (sw, sv-need))
    #             pipette.aspirate(need, sw)
    #             need = 0
    #             have += need
    #         else:
    #             pipette.aspirate(sv, sw)
    #             need -= sv
    #             have += sv
    #     return have
    #
    # def fill(self, reagent: str, target: Well, volume: float) -> None:
    #     (pipette, tip) = self.pipette_and_tip(reagent, volume)
    #     # pipette = self.large_pipette
    #     # tip = self.reagent_large_tip[reagent]
    #     pipette.pick_up_tip(tip)
    #     while volume > 0:
    #         got = self.acquire(reagent, pipette, volume)
    #         pipette.dispense(got, target)
    #         pipette.dispense(got, target)
    #         volume -= got
    #     pipette.drop_tip(tip)
    #

    def acquire(self, reagent: str, pipette: InstrumentContext, volume: float, *, 
                have: float = 0) -> float:
        need = min(volume, pipette.max_volume-have)
        # self.message(f"Looking for {need} uL.")
        while need > 0:
            sw, sv = self.reagent_source[reagent].pop(0)
            # self.message(f"Found {sv}uL in {sw}.")
            if sv > need:
                self.reagent_source[reagent].insert(0, (sw, sv-need))
                pipette.aspirate(need, sw)
                have += need
                need = 0
            else:
                pipette.aspirate(sv, sw)
                have += sv
                need -= sv
        return have
            
    def fill(self, reagent: str, target: Well, volume: float) -> None:
        self.message(f"Moving {volume}uL of {reagent} to {target}")
        
        (pipette, tip) = self.pipette_and_tip(reagent, volume)
        pipette.pick_up_tip(tip)
        while volume > 0:
            got = self.acquire(reagent, pipette, volume)
            # self.message(f"Need {volume}, got {got}")
            pipette.dispense(volume, target)
            volume -= got
            # break
        pipette.drop_tip(tip)
        
    def deliver(self, reagent: str, targets: Sequence[Well], drop_size: float) -> None:
        self.message(f"Delivering {len(targets)} drop(s) of {reagent}")
        (pipette, tip) = self.pipette_and_tip(reagent, drop_size)
        pipette.pick_up_tip(tip)
        total_volume = drop_size*len(targets)
        have: float = 0
        for target in targets:
            if have < drop_size:
                got = self.acquire(reagent, pipette, total_volume, have=have)
                have += got
                total_volume -= got
            pipette.dispense(drop_size, target)
            have -= drop_size
        pipette.drop_tip(tip) 
        
        
    

    def remove_product(self, source: Well, volume: float) -> None:
        reagent = f"**product {self._next_product}**"
        self._next_product += 1
        (pipette, tip) = self.pipette_and_tip(reagent, volume)
        target = self.output_wells.pop(0)
        pipette.pick_up_tip(tip)
        pipette.aspirate(volume, source)
        pipette.dispense(volume, target)
        pipette.drop_tip()
        
        
    def empty_waste(self, sources: Sequence[tuple[Well, float]]) -> None:
        reagent = "**waste**"
        total_volume = sum(p[1] for p in sources)
        (pipette, tip) = self.pipette_and_tip(reagent, total_volume)
        target = self.trash["A1"]
        pipette.pick_up_tip(tip)
        for w,v in sources:
            pipette.aspirate(v, w)
        pipette.aspirate(total_volume, target)
        pipette.drop_tip(tip)
        
        
    # def empty_waste(self, source: Well, volume: float) -> None:
    #     reagent = "**waste**"
    #     (pipette, tip) = self.pipette_and_tip(reagent, volume)
    #     target = self.trash["A1"]
    #     pipette.pick_up_tip(tip)
    #     pipette.aspirate(volume, source)
    #     pipette.aspirate(volume, target)
    #     pipette.drop_tip(tip)
        
        
