from __future__ import annotations
import joey
from mpam.device import System, Well
from mpam.types import StaticOperation, Dir, Reagent, Liquid, ticks
from mpam.drop import Drop
from quantities.dimensions import Volume
from quantities.core import Unit
from quantities.SI import ms

board = joey.Board()

system = System(board=board)

drops: Unit[Volume] = board.drop_size.as_unit("drops")

    
def walk_across(well: Well, direction: Dir) -> StaticOperation[None]:
    return Drop.DispenseFrom(well) \
            .then(Drop.Move(direction, steps=18)) \
            .then(Drop.EnterWell)
    pass    
    
def experiment(system: System) -> None:
    r1 = Reagent('R1')
    r2 = Reagent('R2')
    board = system.board
    board.wells[4].contains(Liquid(r1, 8*drops))
    board.wells[6].contains(Liquid(r2, 8*drops))

    system.clock.start(100*ms)
        
    s1 = walk_across(board.wells[4], Dir.LEFT)
    s2 = walk_across(board.wells[6], Dir.LEFT)
    with system.batched():
        s1.schedule()
        s1.schedule(after=15*ticks)
        s1.schedule(after=20*ticks)
        s2.schedule()
    
system.run_monitored(experiment)
    
    

            
            
system.stop()