from __future__ import annotations

from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware, Well
from opentrons.protocol_api.instrument_context import InstrumentContext

metadata = {
    'protocolName': 'Testing ep holes (local)',
    'author': 'Evan Kirshenbaum < evan.kirshenbaum@hp.com>',
    'apiLevel': '2.11'
}


class ReagentSource:
    plateWell: Well
    tipWell: Well
    joeyWell: Well
    
    def __init__(self, slot: str, plate: Labware, tiprack: Labware, joey: Labware, *, 
                 joey_slot: str="A1",
                 tip_slot: str="A1") -> None:
        self.plateWell = plate[slot]
        self.tipWell = tiprack[tip_slot]
        self.joeyWell = joey[joey_slot]
        
    def refill(self, pipette: InstrumentContext, *,
               vol: float = 1.0) -> None:
        pipette.pick_up_tip(self.tipWell)
        pipette.aspirate(vol, self.plateWell)
        pipette.dispense(vol, self.joeyWell)
        # pipette.drop_tip(self.tipWell)
        pipette.drop_tip()

FOR_REAL = True        

def run(protocol: protocol_api.ProtocolContext) -> None:
    tiprack: Labware = protocol.load_labware("opentrons_96_filtertiprack_20ul", 6)
    joey: Labware = protocol.load_labware("joey_drilled_flat_lid_adapted", 2)
    plate: Labware = protocol.load_labware("nest_96_wellplate_2ml_deep", 1)
    
    pipette = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[tiprack])

    pretend = ReagentSource("A1", plate, tiprack, joey)
    green = ReagentSource("H12", plate, tiprack, joey)
    
    r = green if FOR_REAL else pretend
    
    r.refill(pipette, vol=2.0)

    
