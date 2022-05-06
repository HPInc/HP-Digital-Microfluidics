from __future__ import annotations

from argparse import ArgumentParser, Namespace, _ArgumentGroup
from typing import Union, Optional, Sequence

from devices import bilby
from joey import JoeyExerciser
from mpam.device import System, Well, Heater, Magnet, Board
from mpam.exerciser import Task, volume_arg, Exerciser, voltage_arg
from mpam.paths import Path
from mpam.types import Dir, Liquid, unknown_reagent, ticks, \
    Operation, StaticOperation, Reagent
from quantities.SI import sec, ms, uL, V
from quantities.dimensions import Time, Volume, Voltage
from quantities.temperature import TemperaturePoint, abs_C

class DispenseAndWalk(Task):
    def __init__(self) -> None:
        super().__init__(name="walk",
                         description="""Dispense a drop from a given well and
                                        walk to the well across from it.""")

    def add_args_to(self, parser: ArgumentParser, *,
                    exerciser: Exerciser
                    ) -> None:
        group = self.arg_group_in(parser)
        group.add_argument('-w', '--well', type=int, required=True, metavar="INT",
                            choices=exerciser.available_wells(),
                            help="The well to dispense from")
        group.add_argument('-v', '--volume', type=volume_arg, metavar='VOLUME',
                            help="The initial volume of the well.  Default is a full well.")
        group.add_argument('-d', '--drops', type=int, default=1, metavar='N',
                            help="The number of drops to walk.  Default is 1")
        # parser.add_argument('-g', '--gap', type=int, default=8, metavar='N',
        #                     help="""
        #                     The gap between drops.  Default is 8
        #                     """)


    def run(self, board: Board, system: System, args: Namespace) -> None:
        well_no: int = args.well
        well = board.wells[well_no]
        hdir = Dir.RIGHT if well_no == 2 or well_no == 3 else Dir.LEFT
        vdir1 = Dir.DOWN if well_no == 2 or well_no == 6 else Dir.UP
        vdir2 = Dir.UP if well_no == 2 or well_no == 6 else Dir.DOWN

        drops = board.drop_size.as_unit("drops")
        volume: Optional[Union[Volume, float]] = args.volume
        if volume is None:
            volume = well.capacity
        elif isinstance(volume, float):
            volume = volume*drops
        well.contains(Liquid(unknown_reagent, volume))

        seq = Path.dispense_from(well) \
                .walk(hdir) \
                .walk(vdir1, steps=2) \
                .walk(hdir, steps=16) \
                .walk(vdir2, steps=2) \
                .walk(hdir) \
                .enter_well()

        with system.batched():
            for i in range(args.drops):
                delay = 0*ticks if i==0 else (4+4*i)*ticks
                seq.schedule(after=delay)

class WombatTest(Task):
    def __init__(self) -> None:
        super().__init__(name="wombat-test",
                         description = "The original Wombat test.",
                         aliases=["test"])

    def add_args_to(self, parser: ArgumentParser, *,  # @UnusedVariable
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        ...

    def walk_across(self, well: Well, direction: Dir,
                    turn1: Dir,
                    turn2: Dir,
                    ) -> StaticOperation[None]:
        return Path.dispense_from(well) \
                .walk(direction) \
                .walk(turn1, steps=2) \
                .walk(direction, steps=16) \
                .walk(turn2, steps=2) \
                .walk(direction) \
                .enter_well()

    def ramp_heater(self, temps: Sequence[TemperaturePoint]) -> Operation[Heater, Heater]:
        op: Operation[Heater,Heater] = Heater.SetTemperature(temps[0])
        for i in range(1, len(temps)):
            op = op.then(Heater.SetTemperature(temps[i]), after=5*sec)
        return op.then(Heater.SetTemperature(None), after=5*sec)

    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable

        r1 = Reagent("R1")
        r2 = Reagent("R2")
        drops = board.drop_size.as_unit("drops")
        board.wells[2].contains(Liquid(r1, 40*drops))
        board.wells[3].contains(Liquid(r2, 40*drops))

        s1 = self.walk_across(board.wells[2], Dir.RIGHT, Dir.DOWN, Dir.UP)
        s2 = self.walk_across(board.wells[3], Dir.RIGHT, Dir.UP, Dir.DOWN)

        with system.batched():
            for i in range(30):
                delay = 0*ticks if i==0 else (4+4*i)*ticks
                s1.schedule(after=delay)
                s2.schedule(after=delay)
            self.ramp_heater([80*abs_C, 60*abs_C, 90*abs_C, 40*abs_C, 120*abs_C]) \
                .schedule_for(board.heaters[3])
            Magnet.TurnOn.schedule_for(board.pad_at(13,3).magnet, after=20*ticks)



class BilbyExerciser(JoeyExerciser):
    def __init__(self) -> None:
        super().__init__(name="Bilby")
        self.add_task(DispenseAndWalk())
        self.add_task(WombatTest())

    def add_device_specific_common_args(self,
                                        group: _ArgumentGroup,
                                        parser: ArgumentParser  # @UnusedVariable
                                        ) -> None:
        super().add_device_specific_common_args(group, parser)
        group.add_argument("--dll-dir",
                           help='''
                           The directory that Wallaby.dll is found in.  Defaults to searching.
                           ''')
        group.add_argument("--config-dir",
                           help='''
                           The directory that WallabyElectrodes.csv and WallabyHeaters.csv
                           are found in.  Defaults to the current directory.
                           ''')
        default_voltage = 60*V
        group.add_argument("--voltage", type=voltage_arg, metavar="VOLTAGE", default=default_voltage,
                           help=f'''
                           The voltage to set.  A value of 0V disables
                           the high voltage.  Any other value enables it.
                           The defaults is {default_voltage}.
                           ''')
        

    def make_board(self, args:Namespace)->Board:
        voltage: Optional[Voltage] = args.voltage
        assert voltage is not None
        if voltage == 0:
            voltage = None
        return bilby.Board(dll_dir=args.dll_dir, config_dir=args.config_dir, voltage=voltage)

if __name__ == '__main__':
    Time.default_units = ms
    Volume.default_units = uL
    Voltage.default_units = V
    exerciser = BilbyExerciser()
    exerciser.parse_args_and_run()
