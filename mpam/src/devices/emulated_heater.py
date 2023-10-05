from __future__ import annotations

from random import Random
import random
from typing import Sequence, Optional, Union, Final

from erk.grid import GridRegion
from erk.sched import Delayed
from mpam.device import TemperatureControl, Board, Well, Pad, TemperatureMode, \
    Heater, Chiller
from quantities.SI import deg_C, sec
from quantities.dimensions import Temperature, HeatingRate
from quantities.temperature import TemperaturePoint
from quantities.timestamp import Timestamp, time_now


class TemperatureControlEmulator:
    last_read_time: Timestamp
    driving_rate: Final[HeatingRate]
    return_rate: Final[HeatingRate]
    temp_control: Final[TemperatureControl]
    noise_sd: Final[Temperature]
    rng: Final[Random]

    def __init__(self, temp_control: TemperatureControl, *,
                 driving_rate: HeatingRate,
                 return_rate: HeatingRate,
                 noise_sd: Temperature = Temperature.ZERO) -> None:
        self.temp_control = temp_control
        self.last_read_time = time_now()
        self.driving_rate = driving_rate
        self.return_rate = return_rate
        self.noise_sd = noise_sd
        self.rng = Random()
        # It really seems as though we should be able to just override the target setter, but I
        # can't get the compiler (and MyPy) to accept it
        key=(self, "target changed", random.random())

        def set_lrt() -> None:
            self.last_read_time = time_now()
        temp_control.on_target_change(lambda _old,_new: set_lrt(), key=key)

    def new_temp(self) -> Optional[TemperaturePoint]:
        now = time_now()
        elapsed = now-self.last_read_time
        self.last_read_time = now
        tc = self.temp_control

        mode = tc.mode
        if mode.is_maintaining:
            return tc.target
        # if mode is TemperatureMode.AMBIENT or mode.is_maintaining:
        #     return tc.current_temperature
        current = tc.current_temperature
        assert current is not None

        target = tc.target
        if target is None:
            target = tc.board.ambient_temperature
        rate: HeatingRate
        if mode.is_active:
            heating = mode is TemperatureMode.HEATING
            sign = 1 if heating else -1
            rate = self.driving_rate 
            clip = min if heating else max
        else:
            cooling = current >= target
            sign = -1 if cooling else 1
            rate = self.return_rate
            clip = max if cooling else min
            
        delta = sign*rate*elapsed
        new_temp = current + delta
        new_temp = clip(new_temp, target)
        return new_temp
    
    def poll(self) -> Delayed[Optional[TemperaturePoint]]:
        t = self.new_temp()
        if t is not None:
            t += Temperature.noise(self.noise_sd, rng = self.rng)
        return Delayed.complete(t)

class EmulatedHeater(Heater):
    emulator: Final[TemperatureControlEmulator]
    
    def __init__(self, board: Board,*,
                 regions: Sequence[GridRegion],
                 wells: Sequence[Well],
                 limit: Optional[TemperaturePoint],
                 initial_temperature: Optional[TemperaturePoint] = None,
                 driving_rate: HeatingRate = 100*(deg_C/sec),
                 return_rate: HeatingRate = 10*(deg_C/sec),
                 noise_sd: Temperature = Temperature.ZERO) -> None:
        
        locs = list[Union[Pad, Well]]()

        for region in regions:
            locs += (board.pad_array[xy] for xy in region)
        locs += wells
        
        if initial_temperature is None:
            initial_temperature = board.ambient_temperature

        super().__init__(board, locations=locs, limit=limit, 
                         initial_temperature=initial_temperature)
        self.emulator = TemperatureControlEmulator(self, 
                                                   driving_rate=driving_rate, return_rate=return_rate,
                                                   noise_sd=noise_sd)
    
    def poll(self)->Delayed[Optional[TemperaturePoint]]:
        return self.emulator.poll()
    
class EmulatedChiller(Chiller):
    emulator: Final[TemperatureControlEmulator]
    
    def __init__(self, board: Board,*,
                 regions: Sequence[GridRegion],
                 wells: Sequence[Well],
                 limit: Optional[TemperaturePoint],
                 initial_temperature: Optional[TemperaturePoint] = None,
                 driving_rate: HeatingRate = 100*(deg_C/sec),
                 return_rate: HeatingRate = 10*(deg_C/sec),
                 noise_sd: Temperature = Temperature.ZERO) -> None:
        
        locs = list[Union[Pad, Well]]()

        for region in regions:
            locs += (board.pad_array[xy] for xy in region)
        locs += wells
        
        if initial_temperature is None:
            initial_temperature = board.ambient_temperature

        super().__init__(board, locations=locs, limit=limit, 
                         initial_temperature=initial_temperature)
        self.emulator = TemperatureControlEmulator(self, 
                                                   driving_rate=driving_rate, return_rate=return_rate,
                                                   noise_sd=noise_sd)
    
    def poll(self)->Delayed[Optional[TemperaturePoint]]:
        return self.emulator.poll()
    
    