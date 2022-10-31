from __future__ import annotations

import random
from typing import Sequence, Optional, Union

from mpam.device import Heater, Board, Well, Pad, HeatingMode
from mpam.types import HeatingRate, GridRegion, Delayed
from quantities.SI import ms, deg_C, sec
from quantities.dimensions import Time, Temperature
from quantities.temperature import TemperaturePoint
from quantities.timestamp import Timestamp, time_now


class EmulatedHeater(Heater):
    _last_read_time: Timestamp
    _heating_rate: HeatingRate
    _cooling_rate: HeatingRate

    def __init__(self, board: Board, *,
                 regions: Sequence[GridRegion],
                 wells: Sequence[Well],
                 max_heat: Optional[TemperaturePoint],
                 min_chill: Optional[TemperaturePoint],
                 initial_temperature: Optional[TemperaturePoint] = None,
                 polling_interval: Time = 200*ms,
                 driving_rate: HeatingRate = 100*(deg_C/sec),
                 return_rate: HeatingRate = 10*(deg_C/sec),
                 noise_sd: Optional[Temperature] = None) -> None:
        locs = list[Union[Pad, Well]]()
        for region in regions:
            locs += (board.pad_array[xy] for xy in region)
        locs += wells
        
        if initial_temperature is None:
            initial_temperature = board.ambient_temperature
            
        super().__init__(board,
                         polling_interval = polling_interval,
                         locations = locs,
                         max_heat = max_heat,
                         min_chill = min_chill,
                         initial_temperature = initial_temperature)
        self._last_read_time = time_now()
        self._heating_rate = 100*(deg_C/sec).a(HeatingRate)
        self._cooling_rate = 10*(deg_C/sec).a(HeatingRate)
        # It really seems as though we should be able to just override the target setter, but I
        # can't get the compiler (and MyPy) to accept it
        key=(self, "target changed", random.random())

        def set_lrt() -> None:
            self._last_read_time = time_now()
        self.on_target_change(lambda _old,_new: set_lrt(), key=key)

    def new_temp(self, target: Optional[TemperaturePoint]) -> Optional[TemperaturePoint]:
        now = time_now()
        elapsed = now-self._last_read_time
        self._last_read_time = now
        mode = self.mode
        if mode is HeatingMode.MAINTAINING:
            return self.current_temperature
        assert self.current_temperature is not None
        if mode is HeatingMode.OFF and self.current_temperature <= self.board.ambient_temperature:
            return self.current_temperature
        delta: Temperature
        if mode is HeatingMode.HEATING:
            delta = (self._heating_rate*elapsed).a(Temperature)
            new_temp = self.current_temperature + delta
            if target is not None:
                new_temp = min(new_temp, target)
        else:
            delta = (self._cooling_rate*elapsed).a(Temperature)
            new_temp = self.current_temperature - delta
            if target is None:
                new_temp = max(new_temp, self.board.ambient_temperature)
            else:
                new_temp = max(new_temp, target)
        return new_temp

    def poll(self) -> Delayed[Optional[TemperaturePoint]]:
        return Delayed.complete(self.new_temp(self.target))
