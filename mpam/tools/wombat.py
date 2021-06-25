from __future__ import annotations

from argparse import ArgumentParser, Namespace, _ArgumentGroup
from typing import Union, Optional, Sequence 

from devices import wombat
from mpam.device import System, Well, Heater, Magnet, Board
from mpam.drop import Drop, Mix2, Mix3, Mix4
from mpam.exerciser import Task, volume_arg, Exerciser
from mpam.types import Dir, Liquid, unknown_reagent, ticks, \
    Operation, StaticOperation, RunMode, Reagent, tick
from quantities.SI import sec, ms
from quantities.dimensions import Time, Volume
from quantities.temperature import TemperaturePoint, abs_C
from joey import JoeyExerciser


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
        
        seq = Drop.DispenseFrom(well) \
                .then(Drop.Move(hdir)) \
                .then(Drop.Move(vdir1, steps=2)) \
                .then(Drop.Move(hdir, steps=16)) \
                .then(Drop.Move(vdir2, steps=2)) \
                .then(Drop.Move(hdir)) \
                .then(Drop.EnterWell)
                
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
        return Drop.DispenseFrom(well) \
                .then(Drop.Move(direction)) \
                .then(Drop.Move(turn1, steps=2)) \
                .then(Drop.Move(direction, steps=16)) \
                .then(Drop.Move(turn2, steps=2)) \
                .then(Drop.Move(direction)) \
                .then(Drop.EnterWell)
    
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
        
        async_mode = RunMode.asynchronous(args.clock_speed)
        
        s1 = self.walk_across(board.wells[2], Dir.RIGHT, Dir.DOWN, Dir.UP)
        s2 = self.walk_across(board.wells[3], Dir.RIGHT, Dir.UP, Dir.DOWN)
        
        with system.batched():
            for i in range(30):
                delay = 0*ticks if i==0 else (4+4*i)*ticks
                s1.schedule(after=delay)
                s2.schedule(after=delay)
            self.ramp_heater([80*abs_C, 60*abs_C, 90*abs_C, 40*abs_C, 120*abs_C]) \
                .schedule_for(board.heaters[3], mode = async_mode)
            Magnet.TurnOn.schedule_for(board.pad_at(13,3).magnet, after=20*ticks)

class RealMix(Task):
    def __init__(self) -> None:
        super().__init__(name="old-mix",
                         description="Dispense two drops, walk them out and mix them together")

    def add_args_to(self, parser: ArgumentParser, *,  
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        group = self.arg_group_in(parser)
        group.add_argument('-n', '--num-drops', type=int, metavar='INT', default=2,                             
                           choices=[2,3,4],
                           help="The number of drops to mix.")
        group.add_argument('-f', '--full', action='store_true',  
                            help="Fully mix all drops")
        group.add_argument('--shuttles', type=int, metavar='INT', default=0,
                            help="The number of extra shuttles to perform.  Default is zero.")
        
    def run2(self, board: Board, system: System, args: Namespace) -> None:
        well1 = board.wells[2]
        well2 = board.wells[3]
        r1 = Reagent("R1")
        r2 = Reagent("R2")
        
        well1.contains(Liquid(r1, well1.capacity))
        well2.contains(Liquid(r2, well2.capacity))
        
        seq1 = Drop.DispenseFrom(well1) \
                .then(Drop.Move(Dir.RIGHT, steps=2)) \
                .then(Drop.Move(Dir.DOWN, steps=2)) \
                .then(Drop.Move(Dir.RIGHT, steps=10)) \
                .then(Drop.Mix(Mix2(Dir.DOWN), n_shuttles=args.shuttles)) \
                .then(Drop.Move(Dir.RIGHT, steps=5)) \
                .then(Drop.Move(Dir.UP, steps=2)) \
                .then(Drop.Move(Dir.RIGHT)) \
                .then(Drop.EnterWell)
                
        seq2 = Drop.DispenseFrom(well2) \
                .then(Drop.Move(Dir.RIGHT, steps=2)) \
                .then(Drop.Move(Dir.UP, steps=2)) \
                .then(Drop.Move(Dir.RIGHT, steps=10)) \
                .then(Drop.InMix(fully_mixed = args.full)) \
                .then(Drop.Move(Dir.RIGHT, steps=5)) \
                .then(Drop.Move(Dir.DOWN, steps=2)) \
                .then(Drop.Move(Dir.RIGHT)) \
                .then(Drop.EnterWell)
        with system.batched():
            seq1.schedule()
            seq2.schedule()

    def run3(self, board: Board, system: System, args: Namespace) -> None:
        well1 = board.wells[2]
        well2 = board.wells[3]
        well3 = board.wells[7]
        r1 = Reagent("R1")
        r2 = Reagent("R2")
        r3 = Reagent("R3")
        
        drop = board.drop_size.as_unit("drops", singular="drop")
        
        well1.contains(Liquid(r1, 1*drop))
        well2.contains(Liquid(r2, 1*drop))
        well3.contains(Liquid(r3, 1*drop))
        
        seq1 = Drop.DispenseFrom(well1) \
                .then(Drop.Move(Dir.RIGHT, steps=2)) \
                .then(Drop.Move(Dir.DOWN, steps=2)) \
                .then(Drop.Move(Dir.RIGHT, steps=10)) \
                .then(Drop.Mix(Mix3(Dir.DOWN, Dir.RIGHT), n_shuttles=args.shuttles)) \
                .then(Drop.Move(Dir.RIGHT, steps=5)) \
                .then(Drop.Move(Dir.UP, steps=2)) \
                .then(Drop.Move(Dir.RIGHT)) \
                .then(Drop.EnterWell)
                
        seq2 = Drop.DispenseFrom(well2) \
                .then(Drop.Move(Dir.RIGHT, steps=2)) \
                .then(Drop.Move(Dir.UP, steps=2)) \
                .then(Drop.Move(Dir.RIGHT, steps=10)) \
                .then(Drop.InMix(fully_mixed = args.full)) \
                .then(Drop.Move(Dir.RIGHT, steps=6), after=2*ticks) \
                .then(Drop.Move(Dir.DOWN, steps=2)) \
                .then(Drop.EnterWell)
                
        seq3 = Drop.DispenseFrom(well3) \
                .then(Drop.Move(Dir.LEFT, steps=2)) \
                .then(Drop.Move(Dir.UP, steps=2)) \
                .then(Drop.Move(Dir.LEFT, steps=2)) \
                .then(Drop.InMix(fully_mixed = args.full)) \
                .then(Drop.Move(Dir.RIGHT, steps=4)) \
                .then(Drop.Move(Dir.DOWN, steps=2)) \
                .then(Drop.EnterWell)
        with system.batched():
            seq1.schedule()
            seq2.schedule()
            seq3.schedule()

    def run4(self, board: Board, system: System, args: Namespace) -> None:
        well1 = board.wells[2]
        well2 = board.wells[3]
        well3 = board.wells[6]
        well4 = board.wells[7]
        r1 = Reagent("R1")
        r2 = Reagent("R2")
        r3 = Reagent("R3")
        r4 = Reagent("R4")
        
        drop = board.drop_size.as_unit("drops", singular="drop")

        well1.contains(Liquid(r1, 1*drop))
        well2.contains(Liquid(r2, 1*drop))
        well3.contains(Liquid(r3, 1*drop))
        well4.contains(Liquid(r4, 1*drop))
        
        seq1 = Drop.DispenseFrom(well1) \
                .then(Drop.Move(Dir.RIGHT, steps=2)) \
                .then(Drop.Move(Dir.DOWN, steps=2)) \
                .then(Drop.Move(Dir.RIGHT, steps=10)) \
                .then(Drop.Mix(Mix4(Dir.DOWN, Dir.RIGHT), n_shuttles=args.shuttles)) \
                .then(Drop.Move(Dir.RIGHT, steps=5), after=1*tick) \
                .then(Drop.Move(Dir.UP, steps=2)) \
                .then(Drop.Move(Dir.RIGHT)) \
                .then(Drop.EnterWell)
                
        seq2 = Drop.DispenseFrom(well2) \
                .then(Drop.Move(Dir.RIGHT, steps=2)) \
                .then(Drop.Move(Dir.UP, steps=2)) \
                .then(Drop.Move(Dir.RIGHT, steps=10)) \
                .then(Drop.InMix(fully_mixed = args.full)) \
                .then(Drop.Move(Dir.RIGHT, steps=6), after=3*ticks) \
                .then(Drop.Move(Dir.DOWN, steps=2)) \
                .then(Drop.EnterWell)
                
        seq3 = Drop.DispenseFrom(well3) \
                .then(Drop.Move(Dir.DOWN, steps=2)) \
                .then(Drop.Move(Dir.LEFT, steps=4)) \
                .then(Drop.InMix(fully_mixed = args.full)) \
                .then(Drop.Move(Dir.RIGHT, steps=4)) \
                .then(Drop.Move(Dir.DOWN, steps=4)) \
                .then(Drop.EnterWell)

        seq4 = Drop.DispenseFrom(well4) \
                .then(Drop.Move(Dir.LEFT, steps=2)) \
                .then(Drop.Move(Dir.UP, steps=2)) \
                .then(Drop.Move(Dir.LEFT, steps=2)) \
                .then(Drop.InMix(fully_mixed = args.full)) \
                .then(Drop.Move(Dir.RIGHT, steps=4)) \
                .then(Drop.Move(Dir.DOWN, steps=2)) \
                .then(Drop.EnterWell)

        with system.batched():
            seq1.schedule()
            seq2.schedule()
            seq3.schedule()
            seq4.schedule()

    def run(self, board: Board, system: System, args: Namespace) -> None:
        if args.num_drops == 2:
            self.run2(board, system, args)
        elif args.num_drops == 3:
            self.run3(board, system, args)
        elif args.num_drops == 4:
            self.run4(board, system, args)
        else:
            raise ValueError(f"Don't know how to do a {args.num_drops}-way mix")
            


class WombatExerciser(JoeyExerciser):
    def __init__(self) -> None:
        super().__init__(name="Wombat")
        self.add_task(DispenseAndWalk())
        self.add_task(WombatTest())
        
    def add_device_specific_common_args(self, 
                                        group: _ArgumentGroup, 
                                        parser: ArgumentParser  # @UnusedVariable
                                        ) -> None:
        group.add_argument('-p', '--port',
                           help='''
                           The communication port (e.g., COM5) to use to talk to the board.
                           By default, only the display is run
                           ''')
        
    def make_board(self, args:Namespace)->Board:
        return wombat.Board(device=args.port)
    
    def available_wells(self)->Sequence[int]:
        return [2,3,6,7]

if __name__ == '__main__':
    Time.default_units(ms)
    exerciser = WombatExerciser()
    exerciser.parse_args_and_run()





