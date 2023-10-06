from __future__ import annotations

import math
import time
from typing import overload, Union, Final, MutableMapping

from . import core
from . import dimensions
from .SI import sec, ns, ms
from quantities.SI import seconds
from quantities.core import ZeroOr


class Timestamp:
    """
    An object representing a fixed point in time.
    
    Its :attr:`time` represents the :class:`.Time` since the epoch used by the
    :module:`time` module.  Typically, this will not be interesting.
    
    If `ts` is a :class:`Timestamp` and `t` is a :class:`.Time`, then ::
    
        ts2 = ts + t
        ts2 = t + ts
        ts2 = ts - t
        t = ts - ts2
        
        if ts == ts2: ...
        if ts < ts2: ...
    
    are all valid statements.

    The current time can be obtained by :func:`Timestamp.now`.  The epoch (a
    :class:`Timestamp` with :attr:`time` equal to zero) is
    :func:`Timestamp.epoch` (also known as :func:`Timestamp.never`).  This is
    the same epoch that is used by the standard :module:`time` module.
    
    The following global functions are also useful:
    
        * :func:`time_now` is an alias for :func:`Timestamp.now`.
        * :func:`time_in` is :func:`now` plus a :class:`Time` delta.
        * :func:`time_since` is the :class:`Time` since another timestamp.
        
    To format a :class:`Timestamp`, use :func:`strftime`.  This takes an
    optional format (which defaults to ``"%Y-%m-%d_%H:%M:%S.%f"`` and an
    optional precision, expressed as a :class:`.Time` :class:`.Unit`.  The
    default precision is :attr:`~quantities.SI.ms`

    """
    time: dimensions.Time
    """
    The :class:`.Time` between the :func:`Timestamp.epoch` and this :class:`Timestamp`.
    """
    
    def __init__(self, time: dimensions.Time) -> None:
        """
        Initialize the object
        
        Args:
            time: the :class:`.Time` between the :func:`Timestamp.epoch` and
                  this :class:`Timestamp`.
        """
        self.time = time
        
    def __repr__(self) -> str:
        return f"Timestamp({self.time.in_units(sec)})"
    
    @classmethod
    def now(cls) -> Timestamp:
        """
        The current time as a :class:`Timestamp`
        """
        return Timestamp(time.time_ns()*ns)
    
    @classmethod
    def epoch(cls) -> Timestamp:
        """
        A :class:`Timestamp` with :attr:`time` equal to zero
        """
        return Timestamp(dimensions.Time.ZERO)
    
    @classmethod
    def never(cls) -> Timestamp: 
        """
        A :class:`Timestamp` with :attr:`time` equal to zero
        """
        return Timestamp(dimensions.Time.ZERO)
    
    @classmethod
    def from_time_t(cls, time_t: float) -> Timestamp:
        return Timestamp(time_t*seconds)
    
    def __add__(self, rhs: ZeroOr[dimensions.Time]) -> Timestamp:
        return Timestamp(self.time+rhs)
    
    def __radd__(self, lhs: ZeroOr[dimensions.Time]) -> Timestamp:
        return Timestamp(lhs+self.time)
    
    # def __iadd__(self, rhs: dimensions.Time) -> Timestamp:
    #     self.time += rhs
    #     return self
    #

    @overload
    def __sub__(self, rhs: Timestamp) -> dimensions.Time: ...  # @UnusedVariable
    @overload
    def __sub__(self, rhs: ZeroOr[dimensions.Time]) -> Timestamp: ...  # @UnusedVariable
    def __sub__(self, rhs: Union[Timestamp, ZeroOr[dimensions.Time]]) -> Union[dimensions.Time, Timestamp]:
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
    
    _precision_size: Final[MutableMapping[core.Unit[dimensions.Time], int]] = {
        sec: 0
        }
    
    def strftime(self, *,  
                 fmt: str = "%Y-%m-%d_%H:%M:%S.%f", 
                 precision: core.Unit[dimensions.Time] = ms) -> str:
        """
        Format the :class:`Timestamp` as a string.  
        
        The optional format specifier (``fmt``) is one appropriate for
        :func:`.time.strftime`.  It defaults to ``"%Y-%m-%d_%H:%M:%S.%f"``.  The
        optional ``precision`` specifies the precision of the result, expressed
        as a :class:`.Time` :class:`.Unit`.  It defaults to
        :attr:`~quantities.SI.ms`.
        
        Keyword Args:
            fmt: the format to use
            precision: the precision to use
        Returns:
            the formatted string
        """
        
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
    """
    The current time as a :class:`Timestamp`
    """
    return Timestamp.now()

def time_in(delta: dimensions.Time) -> Timestamp:
    """
    The current time plus ``delta``, which may be negative or zero.
    
    Args:
        delta: the delta :class:`.Time`
    Returns:
        the new :class:`Timestamp`
    """
    return time_now()+delta

def time_since(ts: Timestamp) -> dimensions.Time:
    """
    The delta between the current time and ``ts`` as a :class:`.Time`. 
    
    Depending on the ordering, this may be positive, negative, or zero.
    
    Args:
        ts: another :class:`Timestamp`
    Returns:
        the delta between now and ``ts``
    """
    
    return time_now()-ts

def time_until(ts: Timestamp) -> dimensions.Time:
    return ts-time_now()

def sleep_until(ts: Timestamp) -> None:
    t = time_until(ts)
    if t > 0:
        t.sleep()