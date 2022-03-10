from __future__ import annotations
from devices import wombat
from mpam.device import System, Well, Heater, Magnet
from mpam.types import StaticOperation, Dir, Reagent, Liquid, ticks, Operation,\
    RunMode
from mpam.drop import Drop
from quantities.dimensions import Volume, Time
from quantities.core import Unit
from quantities.SI import ms, sec, uL, Hz, minutes
from quantities.temperature import abs_C, TemperaturePoint
from typing import Sequence
from devices.wombat import OpenDropVersion

Volume.default_units = uL
Time.default_units = ms

board = wombat.Board(device=None, od_version=OpenDropVersion.V40)

system = System(board=board)

drops: Unit[Volume] = board.drop_size.as_unit("drops")

async_mode = RunMode.asynchronous(100*ms)



def walk_across(well: Well, direction: Dir,
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


def ramp_heater(temps: Sequence[TemperaturePoint]) -> Operation[Heater, Heater]:
    op: Operation[Heater,Heater] = Heater.SetTemperature(temps[0])
    for i in range(1, len(temps)):
        op = op.then(Heater.SetTemperature(temps[i]), after=5*sec)
    return op.then(Heater.SetTemperature(None), after=5*sec)


def experiment(system: System) -> None:
    r1 = Reagent('R1')
    r2 = Reagent('R2')
    board = system.board
    board.wells[2].contains(Liquid(r1, 40*drops))
    board.wells[3].contains(Liquid(r2, 40*drops))

    system.clock.start(10*Hz)

    s1 = walk_across(board.wells[2], Dir.RIGHT, Dir.DOWN, Dir.UP)
    s2 = walk_across(board.wells[3], Dir.RIGHT, Dir.UP, Dir.DOWN)


    with system.batched():
        for i in range(30):
            delay = 0*ticks if i==0 else (8+8*i)*ticks
            s1.schedule(after=delay)
            s2.schedule(after=delay)
        # s1.schedule(after=15*ticks)
        # s1.schedule(after=20*ticks)
        # s2.schedule()
        ramp_heater([80*abs_C, 60*abs_C, 90*abs_C, 40*abs_C, 120*abs_C]) \
            .schedule_for(board.heaters[3], mode = async_mode)
        Magnet.TurnOn.schedule_for(board.pad_at(13,3).magnet, after=20*ticks)



system.run_monitored(experiment, min_time=0*minutes)
# cProfile.run('system.run_monitored(experiment, min_time=0*minutes)')





system.stop()
