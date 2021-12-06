from __future__ import annotations

import opentrons_support
import importlib
from opentrons import protocol_api

# If I don't explicitly reload opentrons_support, changes between runs don't get reflected.
opentrons_suport = importlib.reload(opentrons_support)




metadata = {
    'protocolName': 'Joey Peripheral Protocol',
    'author': 'Evan Kirshenbaum < evan.kirshenbaum@hp.com>',
    'description': 'A generic looping client to use the OT-2 as a peripheral for Joey',
    'apiLevel': '2.11'
}

        
            
            

def run(protocol: protocol_api.ProtocolContext) -> None:
    from opentrons_support import Robot, load_config, Board
    config = load_config("config.json")

    turn_off_lights_at_end = not protocol.rail_lights_on
    if turn_off_lights_at_end:
        protocol.set_rail_lights(True)
    
    
    if not protocol.is_simulating():
        board = Board(config["board"], protocol)
        robot = Robot(config, protocol)
        
        for n,w in board.well_map.items():
            robot.message(f"{n}: {w}")
    
        robot.message("Starting run")
        
        if robot.endpoint:
            robot.message(robot.endpoint)
        
        well = board.wells
        ep = board.extraction_ports
        
    
        # # robot.fill("oil", board.oil_reservoir, 200)
        # # robot.fill("oil", board.oil_reservoir, 200)
        # robot.fill("r1", well[4], 30)
        # robot.deliver("r2", [ep[0], ep[0], ep[1]], drop_size=board.drop_size)
        # robot.remove_product(ep[2], board.drop_size)
        # # robot.remove_product(ep[2], board.drop_size)
        # #
        # robot.empty_waste([(well[1], 50), (well[2], 50)])
    
        
        if turn_off_lights_at_end:
            protocol.set_rail_lights(False)
        robot.message("Done")
        robot.exit()
