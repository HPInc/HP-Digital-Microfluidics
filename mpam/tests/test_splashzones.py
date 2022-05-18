import argparse
import logging

from devices import joey, dummy_pipettor
from mpam.device import System
from mpam.paths import Path
from mpam.types import Reagent
from quantities.SI import ms, s



def test_splashzones(system: System) -> None:
    ep= system.board.extraction_points[0]
    loop = ((11, 17), (11, 13), (15, 13), (15, 17))

    paths_loop = []
    for i in range(3):
        path = Path.teleport_into(ep, reagent=Reagent(f'R{i}'))
        seq = loop * 3
        if i:
            seq = seq[:-i]
        for pos in seq:
            path = path.to_pad(pos, after=1 * s)
        paths_loop.append(path)

    paths_waste = []
    for i in range(10):
        paths_waste.append(Path.teleport_into(ep, reagent=Reagent('R')).to_pad((0, 18)).enter_well())

    system.clock.start(200 * ms)
    # system.clock.update_interval = 200 * ms

    with system.batched():
        for p in paths_loop + paths_waste:
            p.schedule()


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
            drop_tip_time=1 * ms),
        extraction_point_splash_radius=2))
system.run_monitored(test_splashzones, min_time=30 * s, config_params = {"highlight_reservations": True})
system.stop()
