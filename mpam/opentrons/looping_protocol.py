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
    from opentrons_support import Robot, load_config
    config = load_config("config.json")

    # turn_off_lights_at_end = not protocol.rail_lights_on
    turn_off_lights_at_end = False
    if turn_off_lights_at_end:
        protocol.set_rail_lights(True)
        

        
    if not protocol.is_simulating():
        # board = Board(config["board"], protocol)
        robot = Robot(config, protocol)
        board = robot.board
        
        robot.message("Created robot and board")
        
        for n,w in board.well_map.items():
            robot.message(f"{n}: {w}")
    
        robot.message("Starting run")
        
        if robot.endpoint:
            robot.message(robot.endpoint)
        
        
        robot.loop()
                
        if turn_off_lights_at_end:
            protocol.set_rail_lights(False)
        robot.message("Done")
        robot.exit()