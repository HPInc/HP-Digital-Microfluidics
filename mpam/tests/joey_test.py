from __future__ import annotations
from devices import joey
from mpam.device import System, Well, TemperatureControl, Magnet
from mpam.types import StaticOperation, Dir, Reagent, Liquid, ticks, Operation,\
    Delayed
from mpam.drop import Drop
from quantities.dimensions import Volume, Time
from quantities.core import Unit
from quantities.SI import ms, sec, uL, minutes
from quantities.temperature import abs_C, TemperaturePoint
from typing import Sequence
from devices.joey import HeaterType

Volume.default_units = uL
Time.default_units = ms

board = joey.Board(heater_type=HeaterType.TSRs)

system = System(board=board)

drops: Unit[Volume] = board.drop_size.as_unit("drops")

def walk_across(well: Well, direction: Dir) -> StaticOperation[None]:
    return Drop.DispenseFrom(well) \
            .then(Drop.Move(direction, steps=18)) \
            .then(Drop.EnterWell)

def ramp_heater(temps: Sequence[TemperaturePoint]) -> Operation[TemperatureControl, TemperatureControl]:
    op: Operation[TemperatureControl,TemperatureControl] = TemperatureControl.SetTemperature(temps[0])
    for i in range(1, len(temps)):
        op = op.then(TemperatureControl.SetTemperature(temps[i]), after=5*sec)
    return op.then(TemperatureControl.SetTemperature(None), after=5*sec)


def experiment(system: System) -> None:
    r1 = Reagent('R1')
    r2 = Reagent('R2')
    board = system.board
    board.wells[4].contains(Liquid(r1, 40*drops))
    board.wells[6].contains(Liquid(r2, 40*drops))

    system.clock.start(100*ms)

    s1 = walk_across(board.wells[4], Dir.LEFT)
    s2 = walk_across(board.wells[6], Dir.LEFT)


    with system.batched():
        s1.schedule()
        s1.schedule(after=15*ticks)
        s1.schedule(after=20*ticks)
        s2.schedule()
        f = ramp_heater([80*abs_C, 60*abs_C, 90*abs_C, 40*abs_C, 120*abs_C]) \
                .schedule_for(board.temperature_controls[3])
        Magnet.TurnOn.schedule_for(board.pad_at(13,3).magnet, after=20*ticks)

    Delayed.join(f)

    print(f.value.current_temperature)

system.run_monitored(experiment, min_time=0*minutes)





system.stop()
