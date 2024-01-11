from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cached_property
import statistics
from threading import RLock
from typing import Union, TypeVar, Protocol, Final, Generic, Sequence, overload, \
    cast

from quantities.core import Quantity, qstr
from quantities.dimensions import Temperature, Time
from quantities.temperature import TemperaturePoint
from quantities.timestamp import Timestamp

from .basic import assert_never


Sampleable = Union[float, int, Quantity, Timestamp, TemperaturePoint]
_ItemT = TypeVar("_ItemT", bound=Sampleable)
_DiffT = TypeVar("_DiffT", bound='_Addable')
_ContT = TypeVar("_ContT")
_D = TypeVar('_D', bound='Quantity')


class _Addable(Protocol):
    def __add__(self: _DiffT, _other: _DiffT) -> _DiffT: ...

class EmptySampleError(RuntimeError):
    sample: Final[Sample]
    def __init__(self, sample: Sample, required: int) -> None:
        msg = "Sample is empty" if required == 1 else f"Sample has fewer than {required} elements"
        super().__init__(msg)
        self.sample = sample

class Sample(Generic[_ItemT, _DiffT, _ContT], ABC):
    class_lock: Final = RLock()
    
    is_empty: bool
    
    def __init__(self, item_type: type[_ItemT], vals: Sequence[_ItemT]) -> None:
        self._vals: Final[list[_ItemT]] = [*vals]
        self.is_empty = len(vals) == 0
        self.item_type: Final = item_type
        
    def __str__(self) -> str:
        tname = self.item_type.__name__
        n = self.count
        desc = ""
        if not self.is_empty:
            desc = f", mean = {self.mean}"
        return f"Sample[{tname}]({qstr(n, 'value')}{desc})"
        
    @overload
    @classmethod
    def for_type(cls, item_type: type[TemperaturePoint],    # @UnusedVariable
                 items: Sequence[TemperaturePoint] = ()     # @UnusedVariable
                 ) -> TemperaturePointSample: ...
    @overload
    @classmethod
    def for_type(cls, item_type: type[Timestamp],    # @UnusedVariable 
                 items: Sequence[Timestamp] = ()     # @UnusedVariable
                 ) -> TimestampSample: ...
    @overload
    @classmethod
    def for_type(cls, item_type: type[int],    # @UnusedVariable 
                 items: Sequence[int] = ()     # @UnusedVariable
                 ) -> IntSample: ...
    @overload
    @classmethod
    def for_type(cls, item_type: type[float],    # @UnusedVariable 
                 items: Sequence[float] = ()     # @UnusedVariable
                 ) -> FloatSample: ...
    @overload
    @classmethod
    def for_type(cls, item_type: type[_D],    # @UnusedVariable 
                 items: Sequence[_D] = ()     # @UnusedVariable
                 ) -> QuantitySample[_D]: ...
    @classmethod # type: ignore[misc]
    def for_type(cls, item_type: type[_ItemT], items: Sequence[_ItemT] = ()) -> Sample:
        if issubclass(item_type, Quantity):
            return QuantitySample(item_type, items)
        elif issubclass(item_type, int):
            return IntSample(item_type, items) # type: ignore[arg-type]
        elif issubclass(item_type, float):
            return FloatSample(item_type, items)  # type: ignore[arg-type]
        elif issubclass(item_type, TemperaturePoint):
            return TemperaturePointSample(item_type, items)  # type: ignore[arg-type]
        elif issubclass(item_type, Timestamp):
            return TimestampSample(item_type, items)  # type: ignore[arg-type]
        assert_never(item_type) # type: ignore
        
    @abstractmethod
    def to_float(self, item: _ItemT) -> float: ...  # @UnusedVariable
    
    @abstractmethod
    def to_item(self, f: float) -> _ContT: ... # @UnusedVariable
        
    @abstractmethod
    def to_delta(self, f: float) -> _DiffT: ... # @UnusedVariable

    def _check(self, required: int = 1) -> int:
        n = self.count
        if n < required:
            raise EmptySampleError(self, required)
        return n
    
    _cached_properies = ("first", "last", "mean", "min_val", "max_val",
                         "_sorted", "median", "_magnitudes", "std_dev",
                         "geometric_mean", "harmonic_mean", "range")
    
    def _invalidate_cached_properties(self) -> None:
        for p in self._cached_properies:
            if p in self.__dict__:
                delattr(self, p)
                
    def add(self, item: _ItemT) -> Sample[_ItemT, _DiffT, _ContT]:
        with self.class_lock:
            self._invalidate_cached_properties()
            self._vals.append(item)
            self.is_empty = False
            return self
        
    @property
    def values(self) -> Sequence[_ItemT]:
        return self._vals
        
    @property
    def count(self) -> int:
        return len(self._vals)
    
    @cached_property
    def first(self) -> _ItemT:
        self._check()
        return self._vals[0]

    @cached_property
    def last(self) -> _ItemT:
        self._check()
        return self._vals[-1]
    
    @cached_property
    def min_val(self) -> _ItemT:
        self._check()
        return min(self._vals)
    
    @cached_property
    def max_val(self) -> _ItemT:
        self._check()
        return max(self._vals)
    
    @cached_property
    def range(self) -> _DiffT:
        return self.to_delta(self.to_float(self.max_val)-self.to_float(self.min_val))
    
    @cached_property
    def _magnitudes(self) -> Sequence[float]:
        return [self.to_float(i) for i in self._vals]

    @cached_property
    def _sorted(self) -> Sequence[_ItemT]:
        return sorted(self._vals)
    
    @cached_property
    def mean(self) -> _ContT:
        n = self._check()
        first = self._vals[0]
        if n == 1:
            return cast(_ContT, first)
        return self.to_item(statistics.mean(self._magnitudes))
    
    @cached_property
    def median(self) -> _ContT:
        self._check()
        return self.to_item(statistics.median(self._magnitudes))
    
    
    @cached_property
    def std_dev(self) -> _DiffT:
        self._check()
        sd = statistics.stdev(self._magnitudes)
        return self.to_delta(sd)
    
    @cached_property
    def geometric_mean(self) -> _ContT:
        n = self._check()
        first = self._vals[0]
        if n == 1:
            return cast(_ContT, first)
        return self.to_item(statistics.geometric_mean(self._magnitudes))
    
    @cached_property
    def harmonic_mean(self) -> _ContT:
        n = self._check()
        first = self._vals[0]
        if n == 1:
            return cast(_ContT, first)
        return self.to_item(statistics.harmonic_mean(self._magnitudes))
    
class TemperaturePointSample(Sample[TemperaturePoint, Temperature, TemperaturePoint]): 
    def to_float(self, item: TemperaturePoint) -> float:
        return item.absolute.magnitude
    def to_item(self, f: float) -> TemperaturePoint:
        return TemperaturePoint(self.to_delta(f))
    def to_delta(self, f: float) -> Temperature:
        return Temperature.dim().make_quantity(f)
    
class TimestampSample(Sample[Timestamp, Time, Timestamp]):
    def to_float(self, item: Timestamp) -> float:
        return item.time.magnitude
    def to_item(self, f: float) -> Timestamp:
        return Timestamp(self.to_delta(f))
    def to_delta(self, f: float) -> Time:
        return Time.dim().make_quantity(f)
    
class IntSample(Sample[int, float, float]): 
    def to_float(self, item: int) -> float:
        return item
    def to_item(self, f: float) -> float:
        return f
    def to_delta(self, f: float) -> float:
        return f
            

class FloatSample(Sample[float, float, float]):
    def to_float(self, item: float) -> float:
        return item
    def to_item(self, f: float) -> float:
        return f
    def to_delta(self, f: float) -> float:
        return f
    
class QuantitySample(Sample[_D, _D, _D]): 
    def to_float(self, item: _D) -> float:
        return item.magnitude
    def to_item(self, f: float) -> _D:
        return self.first.dimensionality.make_quantity(f)
    def to_delta(self, f: float) -> _D:
        return self.first.dimensionality.make_quantity(f)

