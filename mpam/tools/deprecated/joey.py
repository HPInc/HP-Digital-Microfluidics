from __future__ import annotations

from argparse import Namespace, ArgumentParser, _ArgumentGroup
from typing import Sequence

from mpam.exerciser import Exerciser, Task
from mpam.exerciser_tasks import Dispense, Absorb, DisplayOnly, WalkPath, Mix,\
    Dilute
from quantities.dimensions import Time
from devices import joey
from mpam.device import Board, System, Pad, Well
from mpam.types import ticks, unknown_reagent, Liquid
from quantities.temperature import TemperaturePoint
from mpam.thermocycle import ThermocyclePhase, ThermocycleProcessType
from mpam.paths import Path
from devices.joey import HeaterType, heater_type_arg_name_for,\
    heater_type_arg_names
from mpam.cmd_line import temperature_arg, time_arg
import logging

logger = logging.getLogger(__name__)

class Thermocycle(Task):
    def __init__(self) -> None:
        super().__init__(name="thermocycle",
                         description="Run drops through a thermocycle process")

    def add_args_to(self, 
                        group: _ArgumentGroup, 
                        parser: ArgumentParser, *,
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        cg = group.add_mutually_exclusive_group()
        default_drops = 1
        cg.add_argument('-n', '--n-drops', type=int, metavar='INT', default=default_drops,
                        help=f"""The number of drops to run.  These are run in consecutive channels.
                                 Default is {default_drops}."""
                        )
        cg.add_argument('-ac', '--all-channels', action='store_true',
                        help=f"""Use all thermocycler channels""")
        cg.add_argument('-wc', '--wombat-channels', action='store_true',
                        help=f"""Use the thermocycler channels available on the wombat board""")
        cg.add_argument('-c', '--channels', type=int, nargs='+', metavar='INT',
                        help=f"""Specific thermocycler channels to use.""")


        group.add_argument('--names', nargs='*', metavar='NAME',
                           help=f"""The names of the phases.  Defaults to 'phase-1', etc.""")
        group.add_argument('-t', '--temperatures', nargs='+', type=temperature_arg, metavar='TEMP',
                           required=True,
                           help=f"""The temperatures at which to hold the drops.""")
        group.add_argument('-d', '--durations', nargs='+', type=time_arg, metavar='TIME',
                           required=True,
                           help=f"""How long to hold the drops at each temperature.""")

        default_reps = 2
        group.add_argument('-r', '--repetitions', type=int, metavar='INT', default=default_reps,
                           help=f"""The number of time to perform the phases.
                           Default is {default_reps}"""
                           )
        group.add_argument('--middle', action='store_true',
                           help=f"""Start at the middle heater.  If omitted, start at the outside heater"""
                           )

        default_pause_before = 0
        group.add_argument('-pb', '--pause-before', type=int, metavar='TICKS', default=default_pause_before,
                           help=f"Time to pause before the mixing operation.  Default is {default_pause_before*ticks:.0f}.")
        default_pause_after= 0
        group.add_argument('-pa', '--pause-after', type=int, metavar='TICKS', default=default_pause_after,
                           help=f"Time to pause before the mixing operation.  Default is {default_pause_after*ticks:.0f}.")


    def create_path(self, i: int, pad: Pad, well: Well, ptype: ThermocycleProcessType) -> Path.Full:
        path = Path.dispense_from(well) \
                .to_row(pad.row) \
                .to_col(pad.column)
        if i == 0:
            path = path.start(ptype)
        else:
            path = path.join()

        path = path.to_col(18).to_row(0)

        return path.enter_well()

    def run(self, board:Board, system:System, args:Namespace)->None:
        # print(args)
        assert isinstance(board, joey.Board)
        temps: Sequence[TemperaturePoint] = args.temperatures
        names: Sequence[str] = args.names if args.names is not None else [f"phase-{i}" for i in range(len(temps))]
        durations: Sequence[Time] = args.durations
        assert (len(names) == len(temps) == len(durations)), \
                f"--names, --temperatures, --durations must have the same number of entries"

        phases = tuple(ThermocyclePhase(*args) for args in zip(names, temps, durations))
        tc = board.thermocycler
        channels: Sequence[int]
        if args.channels is not None:
            channels = args.channels
        elif args.all_channels:
            channels = list(range(len(tc.channels)))
        elif args.wombat_channels:
            channels = [5,6,13,14]
        else:
            channels = list(range(args.n_drops))

        n_iters: int = args.repetitions

        ptype = tc.as_process(channels=channels,phases=phases,n_iterations=n_iters)
        end = 0 if args.middle else 1
        pads = sorted([tc.channels[i][end].threshold for i in channels],
                      key = lambda pad : (-pad.location.x, pad.location.y))
        drops = board.drop_size.as_unit("drops", singular="drop")
        well = board.wells[2]
        well.contains(Liquid(unknown_reagent, len(pads)*drops))
        paths = [self.create_path(i, pad, well, ptype) for i,pad in enumerate(pads)]

        with system.batched():
            for p in paths:
                p.schedule()


class JoeyExerciser(Exerciser):
    default_off_on_delay = Time.ZERO
    def __init__(self, name: str = "Joey") -> None:
        super().__init__(description=f"Put the {name} board through its paces")
        self.add_task(Dispense())
        self.add_task(Absorb())
        self.add_task(DisplayOnly())
        self.add_task(WalkPath())
        self.add_task(Mix())
        self.add_task(Dilute())
        self.add_task(Thermocycle())

    def make_board(self, args:Namespace)->Board:  # @UnusedVariable
        logger.warning("This tool is deprecated.  Please use 'interactive.py joey' instead.")
        off_on_delay: Time = args.off_on_delay
        return joey.Board(off_on_delay=off_on_delay,
                          heater_type=HeaterType.from_name(args.heaters),
                          extraction_point_splash_radius=args.extraction_point_splash_radius)

    def available_wells(self)->Sequence[int]:
        return [0,1,2,3,4,5,6,7]

    def add_device_specific_common_args(self,
                                        group: _ArgumentGroup,
                                        parser: ArgumentParser  # @UnusedVariable
                                        ) -> None:
        super().add_device_specific_common_args(group, parser)
        group.add_argument('-ood','--off-on-delay', type=time_arg, metavar='TIME', 
                           default=self.default_off_on_delay,
                           help=f'''
                            The amount of time to wait between turning pads off
                            and turning pads on in a clock tick.  0ms is no
                            delay.  Negative values means pads are turned on
                            before pads are turned off. Default is
                            {self.fmt_time(self.default_off_on_delay)}.
                            ''')
        default_heater_type = HeaterType.Paddles
        group.add_argument('--heaters', 
                           # type=heater_type_arg, 
                           default=heater_type_arg_name_for(default_heater_type),
                           metavar="TYPE", 
                           choices=sorted(heater_type_arg_names),
                           help=f'''
                           The type of heater to use.  The default is {default_heater_type}.
                           ''')


if __name__ == '__main__':
    exerciser = JoeyExerciser()
    exerciser.parse_args_and_run()
