from __future__ import annotations
from mpam.device import Sensor
from abc import ABC, abstractmethod
from typing import Optional, Sequence
from quantities.core import Unit
from quantities.dimensions import Voltage
from quantities.timestamp import Timestamp
from mpam.types import Delayed

class ESELog(Sensor):
    class Sample(Sensor.Sample, ABC):
        @property
        @abstractmethod
        def e1d1_valueOff(self) -> Voltage: ...
        @property
        @abstractmethod
        def e1d1_valueOn(self) -> Voltage: ...
        @property
        @abstractmethod
        def e1d2_valueOff(self) -> Voltage: ...
        @property
        @abstractmethod
        def e1d2_valueOn(self) -> Voltage: ...
        @property
        @abstractmethod
        def e2d2_valueOff(self) -> Voltage: ...
        @property
        @abstractmethod
        def e2d2_valueOn(self) -> Voltage: ...
        @property
        @abstractmethod
        def ticket(self) -> int: ...
        @property
        @abstractmethod
        def time(self) -> Timestamp: ...
        @property
        @abstractmethod
        def units(self) -> Optional[Unit[Voltage]]: ...
    @abstractmethod
    def read_samples(self, *, read_async: bool = False) -> Delayed[Sequence[Sample]]:
        ...
        