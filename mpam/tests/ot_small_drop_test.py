from __future__ import annotations

from typing import Optional

from opentrons import protocol_api
from opentrons.protocol_api.labware import Labware


metadata = {
    'protocolName': 'Testing ot small drops (local)',
    'author': 'Evan Kirshenbaum < evan.kirshenbaum@hp.com>',
    'apiLevel': '2.11'
}


        

def run(protocol: protocol_api.ProtocolContext) -> None:
    tiprack: Labware = protocol.load_labware("opentrons_96_filtertiprack_20ul", 6)
    # joey: Labware = protocol.load_labware("joey_drilled_flat_lid_adapted", 2)
    target: Labware = protocol.load_labware("biorad_96_wellplate_200ul_pcr", 2)
    plate: Labware = protocol.load_labware("nest_96_wellplate_2ml_deep", 1)
    
    pipette = protocol.load_instrument("p20_single_gen2", "left", tip_racks=[tiprack])
    tip = tiprack["A1"]
    source = plate["H12"]
    
    i: int = 0
    
    visible = 24
    
    def test(dispense: float, draw: Optional[float] = None) -> None:
        draw = draw or dispense+5
        assert draw >= dispense
        nonlocal i
        dispensed: float = 0
        while dispensed < visible:
            pipette.aspirate(draw, source)
            pipette.dispense(dispense, target.wells()[i])
            if draw > dispense:
                pipette.dispense(draw-dispense, source)
            dispensed += dispense
        i += 1
            
    pipette.pick_up_tip(tip)
    
    for v in (2.0, 1.95, 1.9):
        test(v)
    
    # test(visible)
    # test(0.5)
    # test(1.0)
    # test(2.0)
    # # test(0.5, 1)
    # test(0.5, 2)
    # test(1.0, 2)
    # test(0.5, 5)
    # test(1.0, 5)
    
    pipette.drop_tip(tip)

    
