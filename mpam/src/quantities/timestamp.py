from __future__ import annotations
import time
from .SI import sec, ns, ms
from . import dimensions
from . import core
from typing import overload, Union, Final, ClassVar, MutableMapping
import math

class Timestamp:
    time: dimensions.Time
    
    def __init__(self, time: dimensions.Time) -> None:
        self.time = time
        
    def __repr__(self) -> str:
        return f"Timestamp({self.time.in_units(sec)})"
    
    @classmethod
    def now(cls) -> Timestamp:
        return Timestamp(time.time_ns()*ns)
    
    @classmethod
    def never(cls) -> Timestamp: 
        return Timestamp(dimensions.Time.ZERO())
    
    def __add__(self, rhs: dimensions.Time) -> Timestamp:
        return Timestamp(self.time+rhs)
    
    def __radd__(self, lhs: dimensions.Time) -> Timestamp:
        return Timestamp(lhs+self.time)
    
    # def __iadd__(self, rhs: dimensions.Time) -> Timestamp:
    #     self.time += rhs
    #     return self
    #

    @overload
    def __sub__(self, rhs: Timestamp) -> dimensions.Time: ...  # @UnusedVariable
    @overload
    def __sub__(self, rhs: dimensions.Time) -> Timestamp: ...  # @UnusedVariable
    def __sub__(self, rhs: Union[Timestamp, dimensions.Time]):
        if isinstance(rhs, Timestamp):
            return self.time-rhs.time
        else:
            return Timestamp(self.time-rhs)
    
    # def __isub__(self, rhs: dimensions.Time) -> Timestamp:  # type: ignore
    #     self.time -= rhs
    #     return self
    
    def __eq__(self, rhs: object) -> bool:
        if self is rhs: 
            return True
        if not isinstance(rhs, Timestamp):
            return False
        return self.time == rhs.time
    
    def __hash__(self) -> int:
        return hash(self.time)
    
    def __lt__(self, rhs: Timestamp) -> bool:
        return self.time < rhs.time

    def __le__(self, rhs: Timestamp) -> bool:
        return self.time <= rhs.time
    
    _precision_size: Final[ClassVar[MutableMapping[core.Unit[dimensions.Time], int]]] = {
        sec: 0
        }
    
    def strftime(self, *,  
                 fmt: str = "%Y-%m-%d_%H:%M:%S.%f", 
                 precision: core.Unit[dimensions.Time] = ms) -> str:
        
        if '.%f' in fmt:
            sizes = self._precision_size
            width = sizes.get(precision, None)
            if width is None:
                mag = (1*sec).as_number(precision)
                width = int(math.log10(mag))
                sizes[precision] = width
            if width > 0:
                in_secs = self.time.as_number(sec)
                
                fraction = math.modf(in_secs)[0]
                extra = (fraction*sec).as_number(precision)
                fmt = fmt.replace('%f', f"{int(extra):0{width}d}")
            else:
                fmt = fmt.replace('.%f', '')
        stime = time.localtime(self.time.as_number(sec))
        return time.strftime(fmt, stime)
    
    def __str__(self) -> str:
        return self.strftime()

def time_now() -> Timestamp:
    return Timestamp.now()

def time_in(delta: dimensions.Time) -> Timestamp:
    return time_now()+delta

def time_since(ts: Timestamp) -> dimensions.Time:
    return ts-time_now()