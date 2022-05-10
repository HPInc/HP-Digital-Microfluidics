import logging

from devices import joey, dummy_pipettor
from mpam.device import System
from mpam.paths import Path
from mpam.types import Reagent
from quantities.SI import ms


def test_splashzones(system: System) -> None:
    ep = system.board.extraction_points[0]
    p1 = Path.teleport_into(ep, reagent=Reagent('R1')).to_pad((11, 15))
    p2 = Path.teleport_into(ep, reagent=Reagent('R2')).to_pad((11, 13))
    p3 = Path.teleport_into(ep, reagent=Reagent('R3')).to_pad((11, 17))

    system.clock.start(200 * ms)
    with system.batched():
        p1.schedule()
        p2.schedule()
        p3.schedule()


logging.basicConfig(level=logging.DEBUG,
                    format='%(relativeCreated)6d|%(levelname)7s|%(threadName)s|%(filename)s:%(lineno)s:%(funcName)s|%(message)s')
logging.getLogger('matplotlib').setLevel(logging.INFO)
logging.getLogger('PIL').setLevel(logging.INFO)

system = System(
    board=joey.Board(
        pipettor=dummy_pipettor.DummyPipettor(
            name="Dummy",
            dip_time=200 * ms,
            short_transit_time=1 * ms,
            long_transit_time=1 * ms,
            get_tip_time=1 * ms,
            drop_tip_time=1 * ms)))
system.run_monitored(test_splashzones, min_time=0 * ms)
system.stop()
