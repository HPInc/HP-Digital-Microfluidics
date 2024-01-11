from __future__ import annotations
from .core import CountDim
from typing import overload, Union, ClassVar

class Ticks(CountDim):
    '''
    A :class:`~.core.Quantity` dimension for counting clock ticks

    The units of this dimension are :attr:`ticks` and :attr:`tick`,
    so ::
        2*ticks
        1*tick
    result in :class:`Ticks` objects.

    To get zero on this dimension, you can
    use one of ::
        0*ticks
        Ticks.ZERO
    As this is a :class:`~.core.CountDim` dimension, it can be freely
    added to or compared with a number.
    '''
    ...

ticks = Ticks.base_unit("tick")
"""
The base unit of the :class:`Ticks` dimension

Multiplying a number by this, e.g., ::

    2*ticks
results in a :class:`Ticks` object.
"""
tick = ticks    ; "An alias for :attr:`ticks`, usually used when the magnitude is `1`"

class TickNumber:
    '''
    An absolute tick number (as opposed to a number of :class:`Ticks`).

    If ``tn`` is a :class:`TickNumber` and ``t`` is a :class:`Ticks`, then ::

        tn = TickNumber.ZERO()
        tn2 = tn + t
        tn2 = t + tn
        tn2 = tn - t
        t2 = tn1 - tn2
        tn1 == tn2 # and <, >=, etc.
    are all valid.
    '''
    tick: Ticks ; "The tick number as a :class:`Ticks` value"
    _zero: ClassVar[TickNumber]

    def __init__(self, tick: Ticks) -> None:
        self.tick = tick

    def __repr__(self) -> str:
        return f"TickNumber({self.tick.count})"

    # I had this cached, but there doesn't seem to be any way
    # to make it immutable, and something was incrementing it.
    @classmethod
    def ZERO(cls) -> TickNumber:
        '''
        The base of the :class:`TickNumber` number line.
        '''
        return cls._zero
        # return TickNumber(0*ticks)

    @property
    def number(self) -> int:
        '''
        The tick number as an integer
        '''
        return self.tick.count

    def __add__(self, rhs: Ticks) -> TickNumber:
        return TickNumber(self.tick+rhs)
    def __radd__(self, lhs: Ticks) -> TickNumber:
        return TickNumber(lhs+self.tick)
    # def __iadd__(self, rhs: Ticks) -> TickNumber:
    #     self.tick += rhs
    #     return self

    @overload
    def __sub__(self, rhs: TickNumber) -> Ticks: ...  # @UnusedVariable
    @overload
    def __sub__(self, rhs: Ticks) -> TickNumber: ...  # @UnusedVariable
    def __sub__(self, rhs: Union[TickNumber, Ticks]) -> Union[Ticks, TickNumber]:
        if isinstance(rhs, TickNumber):
            return self.tick-rhs.tick
        else:
            return TickNumber(self.tick-rhs)

    def __eq__(self, rhs: object) -> bool:
        if self is rhs:
            return True
        if not isinstance(rhs, TickNumber):
            return False
        return self.tick == rhs.tick

    def __hash__(self) -> int:
        return hash(self.tick)

    def __lt__(self, rhs: TickNumber) -> bool:
        return self.tick < rhs.tick
    def __le__(self, rhs: TickNumber) -> bool:
        return self.tick <= rhs.tick

TickNumber._zero = TickNumber(Ticks.ZERO)
