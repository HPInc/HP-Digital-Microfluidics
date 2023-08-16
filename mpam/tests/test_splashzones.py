from devices import joey
from mpam.exerciser import Exerciser
from mpam.device import System
from mpam.paths import Path
from mpam.types import Reagent
from quantities.SI import ms, s, uL
from devices.joey import HeaterType
from devices.dummy_pipettor import Config as dp_conf
from quantities.dimensions import FlowRate
from mpam import device, monitor


# splash_radius = 2
# loop_drops = 3

splash_radius = 4
loop_drops = 2

# splash_radius = 8
# loop_drops = 5

loop_io = 20


def test_splashzones(system: System) -> None:
    ep_1 = system.board.extraction_points[0]
    ep_2 = system.board.extraction_points[1] # @UnusedVariable

    loc = ep_1.pad.location
    min_board = 0
    max_board = 18
    well_1 = (0, 18)
    well_2 = (0, 6) # @UnusedVariable
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
    for _i in range(loop_drops):
        path = Path.teleport_into(ep_1, reagent=Reagent.find('L'))
        for pos in loop * 6:
            path = path.to_pad(pos, after=400 * ms)
        full_path = path.to_pad(well_1).enter_well()
        paths_loop.append(full_path)
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

    for loop2 in loops:
        path = Path.teleport_into(ep_1, reagent=Reagent.find('IO'))
        for pos in loop2 * loop_io:
            path = path.to_pad(pos, after=200 * ms)
        full_path = path.to_pad(well_1).enter_well()
        paths_io.append(full_path)

    all_paths.extend(paths_io)

    # ---
    # Waste drops
    # ---
    paths_waste = []
    for _i in range(3): 
        paths_waste.append(Path.teleport_into(ep_1, reagent=Reagent.find('W1')).to_pad(well_1).enter_well())
        # paths_waste.append(Path.teleport_into(ep_2, reagent=Reagent.find('W2')).to_pad(well_2).enter_well())
    all_paths.extend(paths_waste)

    system.clock.start(200 * ms)
    # system.clock.update_interval = 200 * ms # Start paused

    with system.batched():
        for full_path in all_paths:
            full_path.schedule()

Exerciser.setup_logging(levels='debug')

with (dp_conf.dip_time >> 400*ms
      & dp_conf.short_transit_time >> 1*ms
      & dp_conf.long_transit_time >> 1*ms
      & dp_conf.get_tip_time >> 1*ms
      & dp_conf.drop_tip_time >> 800*ms
      & dp_conf.flow_rate >> (1*uL/s).a(FlowRate)
      & device.Config.extraction_point_splash_radius >> splash_radius
      & joey.Config.heater_type >> HeaterType.TSRs
      & monitor.Config.highlight_reservations >> True
      ):

    system = System(
        board=joey.Board())
    system.run_monitored(test_splashzones)
    system.stop()
