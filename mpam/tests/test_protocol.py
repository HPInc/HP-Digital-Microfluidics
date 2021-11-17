from __future__ import annotations

from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware, Well
from opentrons.protocol_api.instrument_context import InstrumentContext

metadata = {
    'protocolName': 'Getting Up to Speed',
    'author': 'Evan Kirshenbaum < evan.kirshenbaum@hp.com>',
    'description': 'A test protocol to get some practice with OT-2',
    'apiLevel': '2.11'
}


class ReagentSource:
    plateWell: Well
    tipWell: Well
    joeyWell: Well
    
    def __init__(self, slot: str, plate: Labware, tiprack: Labware, joey: Labware) -> None:
        self.plateWell = plate[slot]
        self.tipWell = tiprack[slot]
        self.joeyWell = joey[slot]
        
    def refill(self, pipette: InstrumentContext, *,
               vol: float = 30) -> None:
        pipette.pick_up_tip(self.tipWell)
        pipette.aspirate(vol, self.plateWell)
        pipette.dispense(vol, self.joeyWell)
        pipette.drop_tip(self.tipWell)
        

def run(protocol: protocol_api.ProtocolContext) -> None:
    tiprack: Labware = protocol.load_labware("opentrons_96_filtertiprack_200ul", 3)
    joey: Labware = protocol.load_labware("biorad_96_wellplate_200ul_pcr", 8)
    plate: Labware = protocol.load_labware("nest_96_wellplate_2ml_deep", 6)
    
    pipette = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tiprack])

    r1 = ReagentSource("A1", plate, tiprack, joey)
    r2 = ReagentSource("B1", plate, tiprack, joey)
    r3 = ReagentSource("C1", plate, tiprack, joey)
    r4 = ReagentSource("D1", plate, tiprack, joey)
    
    r1.refill(pipette)
    r2.refill(pipette)
    r3.refill(pipette)
    r4.refill(pipette)
    
