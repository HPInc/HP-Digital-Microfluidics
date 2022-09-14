from devices import joey, dummy_pipettor
from mpam.exerciser import Exerciser
from mpam.device import System
from mpam.paths import Path
from mpam.types import Dir, Reagent#, SingleFireTrigger
from quantities.SI import ms, s, minute, uL


def test_singlefiretrigger(system: System) -> None:
    ep = system.board.extraction_points[0]

    # gate2 = SingleFireTrigger()
    # gate3 = SingleFireTrigger()
    path1 = Path.teleport_into(ep, reagent=Reagent('R1')).walk(Dir.W).to_pad((6, 15))
    path2 = Path.teleport_into(ep, reagent=Reagent('R2')).walk(Dir.W).to_pad((8, 15))
    path3 = Path.teleport_into(ep, reagent=Reagent('R3')).to_pad((10, 15))

    all_paths = [path1,
                 path2,
                 path3,
                 ]

    system.clock.start(200 * ms)
    # system.clock.update_interval = 200 * ms # Start paused
    
    # path4 = Path.teleport_into(ep, reagent=Reagent("R4")).walk(Dir.W)
    # path4.schedule()

    with system.batched():
        for path in all_paths:
            path.schedule()
            print("scheduled")

    # Path.run_paths(all_paths, system=system)


Exerciser.setup_logging(levels='debug')

pipettor = dummy_pipettor.DummyPipettor(
    name="Dummy", 
    dip_time=400 * ms, 
    short_transit_time=1 * ms, 
    long_transit_time=1 * ms, 
    get_tip_time=1 * ms, 
    drop_tip_time=800 * ms, 
    flow_rate=(1 * uL / s).a(dummy_pipettor.FlowRate))

system = System(
    board=joey.Board(
        pipettor=pipettor))
system.run_monitored(test_singlefiretrigger,
                     min_time=3 * minute,
                     config_params = {"highlight_reservations": True})
system.stop()
