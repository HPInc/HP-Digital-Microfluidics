import argparse
import logging

from devices import joey, dummy_pipettor
from mpam.exerciser import Exerciser
from mpam.device import System
from mpam.paths import Path
from mpam.types import Reagent
from quantities.SI import ms, s, minute, uL


# splash_radius = 2
# loop_drops = 3

splash_radius = 4
loop_drops = 2

# splash_radius = 8
# loop_drops = 5

loop_io = 20


def test_splashzones(system: System) -> None:
    ep_1 = system.board.extraction_points[0]
    ep_2 = system.board.extraction_points[1]

    loc = ep_1.pad.location
    min_board = 0
    max_board = 18
    well_1 = (0, 18)
    well_2 = (0, 6)
    all_paths = []

    # ---
    # Looping Drops
    # ---
    paths_loop = []
    min_x = max(loc.x - splash_radius, min_board)
    max_x = min(loc.x + splash_radius, max_board)
    min_y = max(loc.y - splash_radius, min_board)
    max_y = min(loc.y + splash_radius, max_board)
    loop = ((min_x, max_y), (min_x, min_y), (max_x, min_y), (max_x, max_y))
    for i in range(loop_drops):
        path = Path.teleport_into(ep_1, reagent=Reagent('L'))
        for pos in loop * 6:
            path = path.to_pad(pos, after=400 * ms)
        path = path.to_pad(well_1).enter_well()
        paths_loop.append(path)
    all_paths.extend(paths_loop)

    # ---
    # In-n-Out Drops
    # ---
    paths_io = []
    loops = []

    # min_y = max(loc.y - splash_radius - 2, min_board)
    # max_y = max(loc.y - splash_radius + 2, min_board)
    # loops.append(((loc.x, min_y), (loc.x, max_y)))

    min_x = max(loc.x - splash_radius - 2, min_board)
    max_x = max(loc.x - splash_radius + 2, min_board)
    loops.append(((min_x, loc.y), (max_x, loc.y)))

    for loop in loops:
        path = Path.teleport_into(ep_1, reagent=Reagent('IO'))
        for pos in loop * loop_io:
            path = path.to_pad(pos, after=200 * ms)
        path = path.to_pad(well_1).enter_well()
        paths_io.append(path)

    all_paths.extend(paths_io)

    # ---
    # Waste drops
    # ---
    paths_waste = []
    for i in range(3):
        paths_waste.append(Path.teleport_into(ep_1, reagent=Reagent('W1')).to_pad(well_1).enter_well())
        # paths_waste.append(Path.teleport_into(ep_2, reagent=Reagent('W2')).to_pad(well_2).enter_well())
    all_paths.extend(paths_waste)

    system.clock.start(200 * ms)
    # system.clock.update_interval = 200 * ms # Start paused

    with system.batched():
        for path in all_paths:
            path.schedule()

Exerciser.setup_logging(level='debug')

system = System(
    board=joey.Board(
        pipettor=dummy_pipettor.DummyPipettor(
            name="Dummy",
            dip_time=400 * ms,
            short_transit_time=1 * ms,
            long_transit_time=1 * ms,
            get_tip_time=1 * ms,
            drop_tip_time=800 * ms,
            flow_rate=(1*uL/s).a(dummy_pipettor.FlowRate)),
        extraction_point_splash_radius=splash_radius))
system.run_monitored(test_splashzones, min_time=3 * minute, config_params = {"highlight_reservations": True})
system.stop()
