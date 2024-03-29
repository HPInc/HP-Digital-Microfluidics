from __future__ import annotations

from abc import ABC, abstractmethod
from argparse import _ArgumentGroup
from enum import Enum, auto
import logging
from os import PathLike
import random
from typing import Sequence, Optional, Final, Union, Callable, Any, TypeVar, \
    Mapping

from sifu.afs import AsyncFunctionSerializer
from sifu.cmd_line import coord_arg, time_arg
from sifu.config import ConfigParam
from sifu.grid import XYCoord
from sifu.sample import IntSample, TemperaturePointSample, QuantitySample, Sample
from sifu.sched import Delayed, Postable
from dmf.device import Sensor, Pad, Laser, Board
from dmf.exerciser import ComponentConfig
from dmf.types import OnOff
from sifu.quant.SI import ms, mV
from sifu.quant.core import Unit, qstr
from sifu.quant.dimensions import Voltage, Time, Frequency
from sifu.quant.temperature import TemperaturePoint, abs_C
from sifu.quant.timestamp import Timestamp, time_now, sleep_until


logger = logging.getLogger(__name__)

_T = TypeVar('_T')

class Config:
    target: Final = ConfigParam[Optional[XYCoord]](None)
    file_name_template: Final = ConfigParam("eselog-%Y-%m-%d_%H_%M_%S.%f.csv")
    file_dir: Final = ConfigParam[Optional[Union[str, PathLike]]](None)
    timestamp_format: Final = ConfigParam('%H:%M:%S')
    timestamp_precision: Final = ConfigParam(ms)
    default_samples: Final = ConfigParam(10)
    sample_speed: Final = ConfigParam(650*ms)
    proxy_factory: Final = ConfigParam[Callable[['ESELog'], 'ESELog.Proxy']]()
    
class ESELogChannel(Enum):
    E1D1 = auto()
    E1D2 = auto()
    E2D2 = auto()


_KeyType = tuple[ESELogChannel, OnOff]
_MapType = Mapping[_KeyType, Voltage] 
    

class ESELog(Sensor):
    timestamp_format: Final[str]
    timestamp_precision: Final[Unit[Time]]
    proxy: Proxy
    
    class Sample(Sensor.Sample):
        _values: Final[_MapType]
        ticket: Final[int]
        temperature: Final[TemperaturePoint]
        
        def __init__(self, *,
                     ticket: int, 
                     time: Timestamp,
                     temperature: TemperaturePoint, 
                     values: _MapType) -> None:
            super().__init__(time)
            self.ticket = ticket
            self.temperature = temperature
            self. _values = values
        
        
        def value(self, channel: ESELogChannel, state:OnOff) -> Voltage:
            key = (channel, state)
            val = self._values.get(key)
            assert val is not None, f"No value at {key}"
            return val
        
        def _for_pairs(self, fn: Callable[[ESELogChannel, OnOff], _T]) -> Sequence[_T]:
            return [fn(c,s) for c in ESELogChannel for s in OnOff]
        
        @property
        def csv_headers(self)->Sequence[str]:
            def fn(c: ESELogChannel, s: OnOff) -> str:
                return f"{c.name}{s.name}".lower()
            return ['ticket', 'timestamp', 'temperature', *self._for_pairs(fn)]

        @property
        def csv_line(self)->Sequence[Any]:
            def fn(c: ESELogChannel, s: OnOff) -> float:
                return self.value(c,s).as_number(mV)
            return [self.ticket, self.timestamp, 
                    self.temperature.as_number(abs_C), 
                    *self._for_pairs(fn)]
        
    class Reading(Sensor.Reading):
        ticket: Final[IntSample]
        temperature: Final[TemperaturePointSample]
        _values: Final[Mapping[tuple[ESELogChannel,OnOff], QuantitySample[Voltage]]]
        
        def __init__(self, sensor: ESELog, samples: Sequence[ESELog.Sample]) -> None:
            super().__init__(sensor, samples)
            self.ticket = Sample.for_type(int, [s.ticket for s in samples])
            self.temperature = Sample.for_type(TemperaturePoint, [s.temperature for s in samples])
            self._values = {
                   (c,o): Sample.for_type(Voltage,[s.value(c,o) for s in samples]) for c in ESELogChannel for o in OnOff
                }
            
        def value(self, channel: ESELogChannel, state: OnOff) -> QuantitySample[Voltage]:
            return self._values[(channel,state)]
        
        def __str__(self) -> str:
            n = self.ticket.count
            vdesc = ""
            if n > 0:
                vals = list[str]()
                for c in ESELogChannel:
                    vals.append(f"{self.value(c,OnOff.ON).mean}/{self.value(c,OnOff.OFF).mean}")
                vdesc = f", {','.join(vals)}"
            return f"ESELog.Reading[{qstr(n, 'sample')}{vdesc}]"
        
    class Proxy(ABC):
        eseLog: Final[ESELog]
        
        def __init__(self, eseLog: ESELog) -> None:
            self.eseLog = eseLog
        
        @property
        @abstractmethod
        def available(self) -> bool:
            ...
        
    
        @abstractmethod
        def read(self, *,
                 n_samples: Optional[int] = None,                # @UnusedVariable
                 speed: Optional[Union[Time, Frequency]] = None, # @UnusedVariable
                 ) -> Delayed[Sequence[ESELog.Sample]]: 
            ...
            
        def reset(self)->None:
            ...
            
        

        
    def __init__(self, board: Board, *,
                 aiming_laser: Optional[Laser] = None,
                 target: Optional[Pad] = None,
                 proxy_factory: Optional[Callable[[ESELog], Proxy]] = None,
                 ) -> None:
        if aiming_laser is None:
            aiming_laser = Laser(board, state=OnOff.OFF) 
        super().__init__(board, name="ESELog",
                         aiming_laser=aiming_laser, target=target,
                         n_samples = Config.default_samples(),
                         sample_interval = Config.sample_speed(),
                         log_file_dir = Config.file_dir() or ".",
                         csv_file_template = Config.file_name_template()
                         )
        if target is None:
            xy = Config.target()
            if xy is not None:
                try:
                    self.target = board.pad_array[xy]
                except KeyError:
                    logger.warning(f"{self} Log target at ({xy.col, xy.row}) does not exist, ignoring.")
        aiming_laser.on_state_change(lambda _old, new: logger.info(f"{self}'s laser is now {new}"))
        self.file_name_template = Config.file_name_template()
        self.timestamp_format = Config.timestamp_format()
        self.timestamp_precision = Config.timestamp_precision()
        if proxy_factory is None:
            proxy_factory = Config.proxy_factory()
        self.proxy = proxy_factory(self)
        


    @property
    def available(self) -> bool:
        return self.proxy.available
    
    def read(self, *,
             n_samples: Optional[int] = None,                # @UnusedVariable
             speed: Optional[Union[Time, Frequency]] = None, # @UnusedVariable
             force_write: bool = False,                      # @UnusedVariable
             ) -> Delayed[Reading]:
        n = n_samples or self.n_samples
        interval = "" if n < 2 else f"(every {self.sample_interval}) "
        logger.info(f"Reading {qstr(n, 'sample')} {interval}from {self}.") 
        future = self.proxy.read(n_samples=n_samples, speed=speed)
        def make_reading(samples: Sequence[ESELog.Sample]) -> ESELog.Reading:
            return ESELog.Reading(self, samples)
        return future.transformed(make_reading)
    
    def reset_component(self)->None:
        super().reset_component()
        self.proxy.reset()
        
class EmulatedESELog(ESELog.Proxy):
    laser_attached: bool = False
    work_queue: Final[AsyncFunctionSerializer]
    
    def __init__(self, eseLog: ESELog) -> None:
        super().__init__(eseLog)
        self.work_queue = AsyncFunctionSerializer(thread_name="ESELog Thread")
    
    @property
    def available(self) -> bool:
        return True
    
        
    def reset(self)->None:
        ...
        
    _fake_centers: Final = {
        (ESELogChannel.E1D1, OnOff.ON): 1226752,
        (ESELogChannel.E1D2, OnOff.ON): 360208895,
        (ESELogChannel.E2D2, OnOff.ON): 1122961629,
        (ESELogChannel.E1D1, OnOff.OFF): 1184768,
        (ESELogChannel.E1D2, OnOff.OFF): 0,
        (ESELogChannel.E2D2, OnOff.OFF): 0
        }

    def _fake(self, ticket: int, start: Timestamp,
              duration: Time) -> ESELog.Sample:
        duration_noise = random.randint(-100, 100)*ms
        temperature_noise = random.randint(-1000, 1000)
        channel_noise = { c: random.randint(-400,400)*mV for c in ESELogChannel }

        timestamp = start+duration+duration_noise
        conversion_factor = 0.00029802325940409414
        temperature = (((211659+temperature_noise)*conversion_factor-54.3)/0.205)*abs_C
        
        def reading(c: ESELogChannel, s: OnOff) -> Voltage:
            center = self._fake_centers[(c,s)]*mV
            return center if center == 0 else (center+channel_noise[c])*conversion_factor
        values = { (c,s): reading(c,s) for c in ESELogChannel for s in OnOff }
        return ESELog.Sample(ticket=ticket,
                             time=timestamp,
                             temperature=temperature,
                             values=values)
        
        
        
        
    def read(self, *,
             n_samples: Optional[int] = None,                # @UnusedVariable
             speed: Optional[Union[Time, Frequency]] = None, # @UnusedVariable
             ) -> Delayed[Sequence[ESELog.Sample]]: 
        
        if n_samples is None:
            n_samples = self.eseLog.n_samples
        if speed is None:
            speed = self.eseLog.sample_interval
        elif isinstance(speed, Frequency):
            speed = 1/speed
            
        future = Postable[Sequence[ESELog.Sample]]()
        samples = list[ESELog.Sample]()
        
        start = time_now()
        now = start
            
        for ticket in range(n_samples):
            sample = self._fake(ticket+1, now, speed)
            samples.append(sample)
            now = sample.timestamp
        
        def worker() -> None:
            sleep_until(now)
            future.post(samples)
            
        self.work_queue.enqueue(worker)
        return future
    
Config.proxy_factory.value = EmulatedESELog

class ESELogConfig(ComponentConfig[ESELog]):
    
    def __init__(self) -> None:
        super().__init__("eselog", ESELog, group=Sensor)

        
    def add_args_to(self, group:_ArgumentGroup)->None:
        super().add_args_to(group)
        Config.target.add_arg_to(group, '--eselog-target', type=coord_arg, metavar="X,Y",
                                 help="The pad the ESELog is pointed at")
        def default_dir(s: Optional[Union[str, PathLike]]) -> str:
            return "the current directory" if s is None else str(s)
        Config.file_dir.add_arg_to(group, '--eselog-dir', metavar='DIR', 
                                   default_desc=default_dir,
                                   help="The directory to write ESELog files to")
        Config.file_name_template.add_arg_to(group, '--eselog-csv-template', metavar='TEMPLATE',
                                             help='''
                                             The template to use to create the ESELog CSV file for each 
                                             reading operation.  The syntax is as per strftime().
                                            ''')
        Config.timestamp_format.add_arg_to(group, '--eselog-timestamp-format', metavar='FORMAT',
                                           help='''
                                           The strftime-like format to use to format timestamps in the CSV file. 
                                           ''')
        Config.default_samples.add_arg_to(group, '--eselog-n-samples', type=int, metavar='INT',
                                          help="The default number of samples to take in an ESELog read operation.")
        Config.sample_speed.add_arg_to(group, '--eselog-sample-interval', type=time_arg, metavar='TIME',
                                       help='''
                                       The amount of time to wait between samples in an ESELog read operation.
                                       Note that this will be bounded by the speed of the hardware.
                                       ''')
        