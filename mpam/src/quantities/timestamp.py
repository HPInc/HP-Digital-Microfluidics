from __future__ import annotations
import time
from .SI import sec, ns
from . import dimensions
from typing import overload, Union

class Timestamp:
    time: dimensions.Time
    
    def __init__(self, time: dimensions.Time) -> None:
        self.time = time
        
    def __repr__(self) -> str:
        return f"Timestamp({self.time.in_units(sec)})"
    
    @classmethod
    def now(cls) -> Timestamp:
        return Timestamp(time.monotonic_ns()*ns)
    
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
    
    def strftime(self, fmt: str = "%Y-m-%d.%H:%M:%S") -> str:
        stime = time.localtime(self.time.as_number(sec))
        return time.strftime(fmt, stime)

def time_now() -> Timestamp:
    return Timestamp.now()

def time_in(delta: dimensions.Time) -> Timestamp:
    return time_now()+delta

def time_since(ts: Timestamp) -> dimensions.Time:
    return ts-time_now()