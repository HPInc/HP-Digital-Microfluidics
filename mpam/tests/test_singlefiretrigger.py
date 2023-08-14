from devices import joey
from mpam.exerciser import Exerciser
from mpam.device import System
from mpam.paths import Path
from mpam.types import Reagent, SingleFireTrigger, Postable
from quantities.SI import ms, s, uL
from mpam import monitor
from quantities.dimensions import FlowRate
from devices.joey import HeaterType
from devices.dummy_pipettor import Config as dp_conf

# Graphical representation of the relevant parts of the board and how
# they should look throughout the run.
#
# Legend   P: Pipettor, 1: Reagent 1, etc.
#
# Phase 1  _______
#          _______
#          __1_2_P
#          _______
#          _______
#
# Phase 2  __1____
#          _______
#          ______P
#          _______
#          ____2__
#
# Phase 3  __1____
#          _______
#          3_____P
#          _______
#          ____2__
#
# Phase 4  _______
#          _______
#          3_1_2_P
#          _______
#          _______

def test_singlefiretrigger(system: System) -> None:
    ep = system.board.extraction_points[0]

    gate1 = SingleFireTrigger()
    gate2 = Postable[bool]()
    gate3 = SingleFireTrigger()
    gate4 = SingleFireTrigger()
    gate5 = SingleFireTrigger()

    home1 = (9, 15)
    home2 = (11, 15)
    home3 = (7, 15)

    path1 = Path.teleport_into(
        ep, reagent=Reagent.find('R1')).to_pad(
            home1).then_fire(gate1).to_pad(
                (home1[0], home1[1] + 2), after=gate2).then_fire(gate4).to_pad(
                    home1, after=gate5)
    path2 = Path.teleport_into(
        ep, reagent=Reagent.find('R2'), after=gate1).to_pad(
            home2).then_process(lambda _: gate2.post(True)).to_pad(
                (home2[0], home2[1] - 2)).then_fire(gate3).to_pad(
                    home2, after=gate5)
    path3 = Path.teleport_into(
        ep, reagent=Reagent.find('R3'), after=gate2).to_pad(
            home2, after=gate3).to_pad(
                home3, after=gate4).then_fire(gate5)

    all_paths = [path3,
                 path2,
                 path1,
                 ]

    system.clock.start(200 * ms)

    Path.run_paths(all_paths, system=system)


Exerciser.setup_logging(levels='debug')
with (dp_conf.dip_time >> 400*ms
      and dp_conf.short_transit_time >> 1*ms
      and dp_conf.long_transit_time >> 1*ms
      and dp_conf.get_tip_time >> 1*ms
      and dp_conf.drop_tip_time >> 800*ms
      and dp_conf.flow_rate >> (1*uL/s).a(FlowRate)
      and joey.Config.heater_type >> HeaterType.TSRs
      and monitor.Config.highlight_reservations >> True
      ):

    system = System(
        board=joey.Board())
    system.run_monitored(test_singlefiretrigger)
    system.stop()
