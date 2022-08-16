"""
Support classes for MPAM applications other than those that describe hardware.
"""
from __future__ import annotations

from _collections import deque
from _weakref import ReferenceType, ref
from abc import ABC, abstractmethod
from enum import Enum, auto
from fractions import Fraction
import math
from threading import Event, Lock, RLock, Thread
from typing import Union, Literal, Generic, TypeVar, Optional, Callable, Any, \
    cast, Final, ClassVar, Mapping, overload, Hashable, Tuple, Sequence, \
    Generator, Protocol, Iterable
from weakref import WeakKeyDictionary, finalize
import logging
import pathlib

from matplotlib._color_data import XKCD_COLORS

from erk.numutils import farey
from quantities.core import CountDim
from quantities.dimensions import Molarity, MassConcentration, \
    VolumeConcentration, Volume, Time
from quantities.temperature import TemperaturePoint

from quantities.SI import uL
import random
from argparse import Namespace
import typing

logger = logging.getLogger(__name__)

T = TypeVar('T')    ; "A generic type variable"
Tco = TypeVar('Tco', covariant=True) ; "A generic covariant type variable"
Tcontra = TypeVar('Tcontra', contravariant=True) ; "A generic contravariant type variable"
V = TypeVar('V')    ; "A generic type variable"
V2 = TypeVar('V2')  ; "A generic type variable"
H = TypeVar('H', bound=Hashable)    ; "A generic type variable representing a :class:`typing.Hashable` type"

PathOrStr = Union[str, pathlib.Path]

Callback = Callable[[], Any]

class OnOff(Enum):
    """ An enumerated type representing `ON` and `OFF` states.

    In boolean contexts, `OFF` is `False`, and `ON` is `True`.

    `!ON` is `OFF`, and vice versa.
    """
    OFF = 0 ; "Represents being off"
    ON = 1  ; "Represents being on"

    def __bool__(self) -> bool:
        "`ON` is `True`; `OFF is `False`"
        return self is OnOff.ON

    def __invert__(self) -> OnOff:
        "`!ON` is `OFF, and vice versa"
        return OnOff.OFF if self else OnOff.ON

    @classmethod
    def from_bool(cls, val: bool) -> OnOff:
        return OnOff.ON if val else OnOff.OFF


Minus1To1 = Union[Literal[-1], Literal[0], Literal[1]]
"""A type representing literal `-1`, `0`, or `1`.

Primarily used in the implementation of :class:`Orientation`.
"""


class Turn(Enum):
    """An enumerations of turns relative to a :class:`Dir`.

    Usually used in `dir.turned(turn)`.
    """
    NONE = auto()   ; "No turn.  (Remain in the same direction.)"
    LEFT = auto()   ; "Turn left."
    RIGHT = auto()  ; "Turn right."
    AROUND = auto() ; "Turn 180 degrees."



class Dir(Enum):
    '''
    An enumeration of possible directions.

    Used to move around an array of items indexed by :class:`XYCoord`.
    '''
    # BUG: MyPy 0.931 (12128).  MyPy is confused because _ignore_ is going to be
    # deleted by Enum's metaclass.  This has been fixed but not released.
    # https://github.com/python/mypy/pull/12128
    _ignore_ = ["_opposites", "_clockwise", "_counterclockwise", "_turns"] # type: ignore[misc]
    _opposites: ClassVar[Mapping[Dir, Dir]]
    _clockwise: ClassVar[Mapping[Dir, Dir]]
    _counterclockwise: ClassVar[Mapping[Dir, Dir]]
    _turns: ClassVar[Mapping[Turn, Mapping[Dir, Dir]]]

    NORTH = auto()      ; "To the north"
    N = NORTH           ; "To the north"
    NORTHEAST = auto()  ; "To the northeast"
    NE = NORTHEAST      ; "To the northeast"
    EAST = auto()       ; "To the east"
    E = EAST            ; "To the east"
    SOUTHEAST = auto()  ; "To the southeast"
    SE = SOUTHEAST      ; "To the southeast"
    SOUTH = auto()      ; "To the south"
    S = SOUTH           ; "To the south"
    SOUTHWEST = auto()  ; "To the southwest"
    SW = SOUTHWEST      ; "To the southwest"
    WEST = auto()       ; "To the west"
    W = WEST            ; "To the west"
    NORTHWEST = auto()  ; "To the northwest"
    NW = NORTHWEST      ; "To the northwest"

    UP = NORTH          ; "To the north"
    DOWN = SOUTH        ; "To the south"
    LEFT = WEST         ; "To the west"
    RIGHT = EAST        ; "To the east"

    @classmethod
    def cardinals(cls) -> Sequence[Dir]:
        '''
        The cardinal directions (`NORTH`, `SOUTH`, `EAST`, and `WEST`)
        '''
        return (Dir.N, Dir.S, Dir.E, Dir.W)

    @property
    def opposite(self) -> Dir:
        '''
        The direction opposite of this one (e.g., `SOUTH` for `NORTH`)
        '''
        return self._opposites[self]
    @property
    def clockwise(self) -> Dir:
        '''
        The direction clockwise of this one (e.g., `EAST` for `NORTH`)
        '''

        return self._clockwise[self]
    @property
    def counterclockwise(self) -> Dir:
        '''
        The direction counterclockwise of this one (e.g., `WEST` for `NORTH`)
        '''
        return self._counterclockwise[self]

    def turned(self, turn: Turn) -> Dir:
        '''
        The direction after taking the given turn.

        For example::

            Dir.NORTH.turned(Turn.NONE) is Dir.NORTH
            Dir.NORTH.turned(Turn.RIGHT) is Dir.EAST
            Dir.NORTH.turned(Turn.AROUND) is Dir.SOUTH
            Dir.NORTH.turned(Turn.LEFT) is Dir.WEST
        Parameters:
            turn: The direction to turn
        Returns:
            the resulting direction
        '''
        if turn is Turn.NONE:
            return self
        return self._turns[turn][self]

Dir._opposites = {
        Dir.N: Dir.S,
        Dir.NE: Dir.SW,
        Dir.E: Dir.W,
        Dir.SE: Dir.NW,
        Dir.S: Dir.N,
        Dir.SW: Dir.NE,
        Dir.W: Dir.E,
        Dir.NW: Dir.SE
    }

Dir._clockwise = {
        Dir.N: Dir.E,
        Dir.NE: Dir.SE,
        Dir.E: Dir.S,
        Dir.SE: Dir.SW,
        Dir.S: Dir.W,
        Dir.SW: Dir.NW,
        Dir.W: Dir.N,
        Dir.NW: Dir.NE
    }

Dir._counterclockwise = {
        Dir.N: Dir.W,
        Dir.NE: Dir.NW,
        Dir.E: Dir.N,
        Dir.SE: Dir.NE,
        Dir.S: Dir.E,
        Dir.SW: Dir.SE,
        Dir.W: Dir.S,
        Dir.NW: Dir.SW
    }

Dir._turns = {
    Turn.RIGHT: Dir._clockwise,
    Turn.LEFT: Dir._counterclockwise,
    Turn.AROUND: Dir._opposites
    }


class XYCoord:
    '''
    An x-y coordinate pair.

    The `x` and `y` attributes are also available as the `col` and `row` properties respectively.

    * :class:`XYCoord` objects are :class:`Hashable`.
    * Adding a :class:`tuple[int, int]` produces another :class:`XYCoord`.
    * :class:`XYCoord` objects are equal if their coordinates are equal.
    '''
    x: int  ; "The x coordinate"
    y: int  ; "The y coordinate"

    def __init__(self, x: int, y: int) -> None:
        '''
        Initialize the object

        Parameters:
            x: The x coordinate
            y: The y coordinate
        '''
        self.x = x
        self.y = y

    @property
    def row(self) -> int:
        '''
        An alias for the `y` coordinate
        '''
        return self.y

    @property
    def col(self) -> int:
        '''
        An alias for the `x` coordinate
        '''
        return self.x

    @property
    def coords(self) -> tuple[int, int]:
        '''
        The x and y coordinates as a :class:`tuple`.
        '''
        return (self.x, self.y)

    def __eq__(self, other: object):
        if not isinstance(other, XYCoord): return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"XYCoord({self.x},{self.y})"

    def __add__(self, offset: tuple[int, int]) -> XYCoord:
        return XYCoord(self.x+offset[0], self.y+offset[1])


class Orientation(Enum):
    '''
    An enumeration describing the orientation of an array indexed by :class:`XYCoord` objects.

    This class arose because we needed to support devices whose internal
    coordinate system had `y` coordinates increasing from bottom to top and
    those that hand them increasing from top to bottom.  These are encapsulated
    here by the values :attr:`NORTH_POS_EAST_POS` and :attr:`NORTH_NEG_EAST_POS`
    respectively.  The other values are included for completeness, although I
    don't expect to see them in practice.
    '''
    offset: Final[Mapping[Dir, tuple[Minus1To1, Minus1To1]]]
    """
    A mapping from :class:`Dir` to x-y pairs representing coordinate offset in that direction
    """
    up_right_delta: tuple[Minus1To1, Minus1To1]
    """
    A tuple representing the offsets when going up and to the right (i.e., :attr:`~Dir.NORTHEAST`).
    """

    NORTH_POS_EAST_POS = {Dir.N: (0,1), Dir.NE: (1,1), Dir.E: (1,0), Dir.SE: (1,-1),
                          Dir.S: (0,-1), Dir.SW: (-1,-1), Dir.W: (-1,0), Dir.NW: (-1,1)}
    "Going north increases `x`; going east increases `y`"
    NORTH_NEG_EAST_POS = {Dir.N: (0,-1), Dir.NE: (1,-1), Dir.E: (1,0), Dir.SE: (1,1),
                          Dir.S: (0,1), Dir.SW: (-1,1), Dir.W: (-1,0), Dir.NW: (-1,-1)}
    "Going north decreases `x`; going east increases `y`"
    NORTH_NEG_EAST_NEG = {Dir.N: (0,-1), Dir.NE: (-1,-1), Dir.E: (-1,0), Dir.SE: (-1,1),
                          Dir.S: (0,1), Dir.SW: (1,1), Dir.W: (1,0), Dir.NW: (1,-1)}
    "Going north decreases `x`; going east decreases `y`"
    NORTH_POS_EAST_NEG = {Dir.N: (0,-1), Dir.NE: (1,-1), Dir.E: (1,0), Dir.SE: (1,1),
                          Dir.S: (0,1), Dir.SW: (-1,1), Dir.W: (-1,0), Dir.NW: (-1,-1)}
    "Going north increases `x`; going east decreases `y`"

    def __init__(self, offset: Mapping[Dir, tuple[Minus1To1, Minus1To1]]) -> None:
        '''
        Parameters:
            offset: A mapping from :class:`Dir` to x-y pairs representing coordinate offset in that direction
        '''
        self.offset = offset
        self.up_right_delta = (offset[Dir.E][0], offset[Dir.N][1])
        # print(f"{self}.up_right_delta = {self.up_right_delta}")

    def neighbor(self, direction: Dir, coord: XYCoord, *, steps: int=1  ) -> XYCoord:
        """
        The coordinates of a neighbor of a given coordinate a given number of steps (default 1) away in a given direction

        Parameters:
            direction: The direction in which to look.
            coord: The starting point.
            steps: The number of steps to take.
        Returns:
            the resulting :class:`XYCoord`
        """
        (dx, dy) = self.offset[direction]
        return XYCoord(coord.x+dx*steps, coord.y+dy*steps)

    def up_right(self, coord: XYCoord, x: int, y: int) -> XYCoord:
        '''
        The :class:`XYCoord` obtained by going `x` steps :attr:`~Dir.EAST` and `y` steps :attr:`~Dir.NORTH`

        Parameters:
            coord: the starting coordinate
            x: The number of steps to travel :attr:`~Dir.EAST`
            y: The number of steps to travel :attr:`~Dir.NORTH`
        Returns:
            the resulting :class:`XYCoord`
        '''
        dx,dy = self.up_right_delta
        return XYCoord(coord.x+dx*x, coord.y+dy*y)

    @property
    def pos_x(self) -> Dir:
        '''
        The :class:`Dir` in which `x` coordinates increase
        '''
        return Dir.E if self.offset[Dir.E][0] > 0 else Dir.W
    @property
    def pos_y(self) -> Dir:
        '''
        The :class:`Dir` in which `y` coordinates increase
        '''
        return Dir.N if self.offset[Dir.N][1] > 0 else Dir.S

    def __repr__(self):
        return f"Orientation.{self.name}"

class GridRegion:
    '''
    A rectangular region in a coordinate space

    It is mostly used for checking whether an :class:`XYCoord` is in the region
    and for enumerating coordinates within the region.

    * An :class:`XYCoord` is in the region if its x and y values are between the
      corners of the region (inclusive).

    * Iterating through the region enumerates :class:`XYCoord` objects from the
      lower left through the upper right in row-major order.
    '''
    lower_left: Final[XYCoord]      ; "The lower left corner of the region"
    upper_right: Final[XYCoord]     ; "The upper right corner of the region"
    width: Final[int]               ; "The width of the region"
    height: Final[int]              ; "The height of the region"
    orientation: Final[Orientation] ; "The :class:`Orientation` of the region"
    min_x: Final[int]               ; "The minimum x coordinate"
    min_y: Final[int]               ; "The minimum y coordinate"
    max_x: Final[int]               ; "The maximum x coordinate"
    max_y: Final[int]               ; "The maximum y coordinate"

    def __init__(self, lower_left: XYCoord, width: int, height: int, *,
                 orientation: Orientation = Orientation.NORTH_POS_EAST_POS) -> None:
        '''
        Create a :class:`GridRegion`

        Parameters:
            lower_left: The lower left corner
            width: The width of the region
            height: The height of the region
            orientation: The :class:`Orientation` of the region
        '''
        lower_right = orientation.neighbor(Dir.RIGHT, lower_left, steps = width-1)
        upper_right = orientation.neighbor(Dir.UP, lower_right, steps=height-1)
        self.lower_left = lower_left
        self.upper_right = upper_right
        self.width = width
        self.height = height
        self.orientation = orientation
        self.min_x = min(lower_left.x, upper_right.x)
        self.min_y = min(lower_left.y, upper_right.y)
        self.max_x = max(lower_left.x, upper_right.x)
        self.max_y = max(lower_left.y, upper_right.y)

    def __contains__(self, xy: XYCoord) -> bool:
        '''
        An :class:`XYCoord` is in the region if its x and y values are between the corners of the region (inclusive).

        Parameters:
            xy: The coordinate to check
        '''
        return (xy.x >= self.min_x and xy.x <= self.max_x and xy.y >= self.min_y and xy.y <= self.max_y)

    def __iter__(self) -> Generator[XYCoord, None, None]:
        orientation = self.orientation
        left = self.lower_left

        for _ in range(self.height):
            current = left
            for _ in range(self.width):
                yield current
                current = orientation.neighbor(Dir.RIGHT, current)
            left = orientation.neighbor(Dir.UP, left)

class Ticks(CountDim):
    '''
    A :class:`~quantities.core.Quantity` dimension for counting clock ticks

    The units of this dimension are :attr:`ticks` and :attr:`tick`,
    so ::
        2*ticks
        1*tick
    result in :class:`Ticks` objects.

    To get zero on this dimension, you can
    use one of ::
        0*ticks
        Ticks.ZERO
    As this is a :class:`~quantities.core.CountDim` dimension, it can be freely
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

DelayType = Union[Ticks, Time]  ; "A delay amount, either :class:`Ticks` or :class:`.Time`"
WaitableType = Union[DelayType, 'Trigger', 'Delayed[Any]']
"""
Something that can be waited on.

Either a :attr:`DelayType` (i.e., a :class:`Ticks` or :class:`.Time`), a
:class:`Trigger` object, or a `Delayed` value.
"""


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
    def __sub__(self, rhs: Union[TickNumber, Ticks]):
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

    def __lt__(self, rhs: TickNumber):
        return self.tick < rhs.tick
    def __le__(self, rhs: TickNumber):
        return self.tick <= rhs.tick

TickNumber._zero = TickNumber(Ticks.ZERO)

# ValTuple = tuple[Literal[False],None]

# ValTuple = Union[tuple[Literal[False],None],Literal[True], T]

ValTuple = tuple[bool, T]

class Missing(Enum):
    """
    A singleton type to use for optional values when ``None`` is a possible non-
    default value.  Should be used via the type alias :attr:`MissingOr` and the
    constant :attr:`MISSING`, as in ::

        def foo(arg: MissingOr[Optional[A]] = MISSING) -> None:
            if arg is MISSING:
                ...
            else:
                # arg is deduced to be an Optional[A] here
                ...
    """
    SINGLETON = auto()
    def __repr__(self) -> str:
        return "MISSING"

MISSING: Final[Missing] = Missing.SINGLETON
"""
The singleton :class:`Missing` value.
"""
MissingOr = Union[Missing, T]
"""
Either the given type ``T`` or :attr:`MISSING`.  If the value is not the
constant :attr:`MISSING`, MyPy will deduce it to be ``T``.

Args:
    T: the type (if not :attr:`MISSING`)
"""

class NoWait(Enum):
    SINGLETON = auto()
    def __repr__(self) -> str:
        return "NO_WAIT"

NO_WAIT: Final[NoWait] = NoWait.SINGLETON

WaitCondition = Union[NoWait, DelayType]

class CommunicationScheduler(Protocol):
    """
    A :class:`typing.Protocol` that matches classes that define
    :func:`schedule_communication` and :func:`delayed`
    """
    def schedule_communication(self, cb: Callable[[], Optional[Callback]], *,  # @UnusedVariable
                               after: WaitCondition = NO_WAIT) -> None:  # @UnusedVariable
        """
        Schedule communication of ``cb`` after optional delay ``after``

        This is typically implemented by delegating and will result in calling
        :func:`SystemComponent.schedule`, which will call
        :func:`System.on_tick` if ``after`` is a :class:`Ticks` value and
        :func:`System.communicate` if ``after`` is a :class:`.Time` value.  If
        ``after`` is ``None``, it is up to the :class:`SystemComponent` to
        determine whether it should be interpreted as zero ticks or zero
        seconds.

        Args:
            cb: the callback function to schedule.
        Keyword Args:
            after: An optional delay before scheduling.
        """
        ...
    def delayed(self, function: Callable[[], T], *, # @UnusedVariable
                after: WaitCondition) -> Delayed[T]: # @UnusedVariable
        """
        Call a function after n optional delay.

        This is typically implemented by delegating and will result in a call to
        :func:`System.delayed`.

        Args:
            function: the function to call
        Keyword Args:
            after: an optional delay before calling
        Returns:
            A :class:`Delayed` object to which the value returned by the function will be posted.
        """
        ...


CS = TypeVar('CS', bound=CommunicationScheduler)    ; "A generic type variable representing a :class:`CommunicationScheduler`"

class Operation(Generic[T, V], ABC):
    '''
    An operation that can be scheduled for an object of type :attr:`T` and returns a delayed value of type :attr:`V`

    The basic notion is that if `op` is an :class:`Operation`\[:attr:`T`, :attr:`V`] and `t` is a :attr:`T`, in ::

        dv: Delayed[V] = op.schedule_for(t)

    the call will return immediately, and `dv` will obtain a value of type :attr:`V` at some point
    in the future, when the operation has completed.

    If :attr:`T` is a subclass of :class:`OpScheduler`, the same effect can be
    obtained by calling its :func:`~OpScheduler.schedule` method::

        dv: Delayed[V] = t.schedule(op)

    Note:
        :class:`Operation`\[:attr:`T`, :attr:`V`] is an abstract base class.
        The actual implementation class must implement :func:`_schedule_for` and :fund:`after_delay`.

    Args:
        T: the type of the object used to schedule the :class:`Operation`
        V: the type of the value produced by the operation
    '''

    @abstractmethod
    def _schedule_for(self, obj: T, *,                # @UnusedVariable
                      post_result: bool = True,       # @UnusedVariable
                      ) -> Delayed[V]:
        """
        The implementation of :func:`schedule_for`.  There is no default implementation.

        :meta public:
        Args:
            obj: the :attr:`T` object to schedule the operation for
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        ...

    def schedule_for(self, obj: Union[T, Delayed[T]], *,
                     after: WaitCondition = NO_WAIT,
                     post_result: bool = True,
                     ) -> Delayed[V]:
        """
        Schedule this operation for the given object.

        If ``obj`` is a :class:`Delayed` object, the actual scheduling will take
        place after a value has been posted to it, and that value will be used.
        Note that any delay specified by ``after`` will be applied **after**
        this value is obtained.

        Once an object has been identified, the actual scheduling will be
        delegated through :func:`_schedule_for`.

        Args:
            obj: The :attr:`T` object for which the operation will be scheduled
                or a :class:`Delayed`\[:attr:`T`] object which will produce it.
        Keyword Args:
            after: an optional delay to wait before scheduling the operation
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        # if after is None:
        #     logger.debug(f'{obj}')
        # else:
        #     logger.debug(f'{obj}|after:{after}')

        if isinstance(obj, Delayed):
            future = Postable[V]()
            def schedule_and_post(x: T) -> None:
                self.schedule_for(
                    x, after=after, post_result=post_result).post_to(future)
            obj.when_value(schedule_and_post)
            return future

        def cb():
            return self._schedule_for(obj, post_result=post_result)
        return self.after_delay(after, cb, obj=obj)

    @abstractmethod
    def after_delay(self,
                    after: WaitCondition,
                    fn: Callable[[], V],
                    *, obj: T) -> Delayed[V]:
        ...

    def then(self,
             op: Union[Operation[V, V2], StaticOperation[V2], # type: ignore [type-var]
                       Callable[[], Operation[V, V2]],
                       Callable[[], StaticOperation[V2]]], *,
             after: WaitCondition = NO_WAIT,
             ) -> Operation[T, V2]:
        """
        Chain this :class:`Operation` and another together to create a single
        new :class:`Operation`

        The value produced by this :class:`Operation` will be used to schedule
        the second one (unless the second is a :class:`StaticOperation`, in
        which case the second will be scheduled after this one is done).

        The actual result will be a :class:`CombinedOperation`\[:attr:`T`, :attr:`V`, :attr:`V2`].

        Note:
            If ``op`` is a :class:`.Callable`, it will be evaluated when the
            :class:`Operation` that is the result of :func:`then` is
            **scheduled**, not when this :class:`Operation` produces a value.

        Args:
            op: the second :class:`Operation` (or a :class:`StaticOperation`) or a :class:`Callable` that
                returns one
        Keyword Args:
            after: an optional delay to apply between the completion of this operation and the second
        Returns:
            the new :class:`Operation`
        """
        return CombinedOperation[T, V, V2](self, op, after=after)

    def then_compute(self, fn: Callable[[V], Delayed[V2]]) -> Operation[T, V2]:
        """
        Create a new :class:`Operation` that passes the result of this one to a :class:`Callable` that returns
        a :class:`Delayed` value.

        The only reason that both this and :func:`then_call` are needed is
        that Python can't distinguish :class:`Callable`\s based on their return
        types.

        Args:
            fn: the :class:`Callable` that computes the new operation's value
        Returns:
            the new :class:`Operation`
        """
        return self.then(ComputeOp[V, V2](fn))

    def then_call(self, fn: Callable[[V], V2]) -> Operation[T, V2]:
        """
        Create a new :class:`Operation` that passes the result of this one to a
        :class:`Callable` and use its value as the overall value.

        The only reason that both this and :func:`then_compute` are needed is
        that Python can't distinguish :class:`Callable`\s based on their return
        types.

        Args:
            fn: the :class:`Callable` that computes the new operation's value
        Returns:
            the new :class:`Operation`
        """
        def fn2(obj: V) -> Delayed[V2]:
            future = Postable[V2]()
            future.post(fn(obj))
            return future
        return self.then_compute(fn2)

    def then_process(self, fn: Callable[[V], Any]) -> Operation[T, V]:
        """
        Create a new :class:`Operation` that passes the result of this one to a
        :class:`Callable`, but uses this :class:`Operation`\s result as the
        final result.

        The difference between this and :func:`then_call` and :func:`then_compute` is
        that the result of the latter call is ignored.

        Args:
            fn: the :class:`Callable` that will be called with this :class:`Operation`\'s result
        Returns:
            the new :class:`Operation`
        """
        def fn2(obj: V) -> V:
            fn(obj)
            return obj
        return self.then_call(fn2)


class CSOperation(Operation[CS, V]):
    '''
    An operation that can be scheduled for an object of type :attr:`CS` and returns a delayed value of type :attr:`V`

    The basic notion is that if `op` is an :class:`Operation`\[:attr:`CS`, :attr:`V`] and `t` is a :attr:`CS`, in ::

        dv: Delayed[V] = op.schedule_for(t)

    the call will return immediately, and `dv` will obtain a value of type :attr:`V` at some point
    in the future, when the operation has completed.

    If :attr:`CS` is a subclass of :class:`OpScheduler`, the same effect can be
    obtained by calling its :func:`~OpScheduler.schedule` method::

        dv: Delayed[V] = t.schedule(op)

    Note:
        :class:`Operation`\[:attr:`CS`, :attr:`V`] is an abstract base class.
        The actual implementation class must implement :func:`_schedule_for`.

    Args:
        CS: the type of the object used to schedule the :class:`Operation`
        V: the type of the value produced by the operation
    '''
    def after_delay(self,
                    after: WaitCondition,
                    fn: Callable[[], V],
                    *, obj: CS) -> Delayed[V]:
        return obj.delayed(fn, after=after)


class CombinedOperation(Generic[T, V, V2], Operation[T, V2]):
    """
    An :class:`Operation` representing chaining two :class:`Operation`\s
    together.

    Objects of this class are built using :func:`Operation.then`,
    :func:`Operation.then_call`, :func:`Operation.then_compute`, and
    :func:`Operation.then_process`,

    Args:
        T: the type of the object used to schedule the :class:`Operation`
        V: the type of the value produced by the first operation
        V2: the type of the value produced by the second operation (and the
            :class:`CombinedOperation` overall)
    """
    first: Operation[T, V]               ; "The first :class:`Operation`"
    second: Union[Operation[V, V2], StaticOperation[V2], # type: ignore [type-var]
                  Callable[[], Operation[V, V2]],
                  Callable[[], StaticOperation[V2]]]
    """
    The second :class:`Operation` (or :class:`StaticOperation`) or a :class:`Callable` that produces one.
    """
    after: Final[WaitCondition]   ; "An optional delay to use between :attr:`first` and :attr:`second`"

    def __init__(self, first: Operation[T, V],
                 second: Union[Operation[V, V2], StaticOperation[V2], # type: ignore [type-var]
                               Callable[[], Operation[V, V2]],
                               Callable[[], StaticOperation[V2]]],
                 after: WaitCondition=NO_WAIT) -> None:
        """
        Initialize the :class:`CombinedOperation`

        Args:
            first: The first :class:`Operation`
            second: the second :class:`Operation` (or :class:`StaticOperation`) or a :class:`Callable`
                    that produces one.
            after: an optional delay to use between the two :class:`Operation`\s
        """
        self.first = first
        self.second = second
        self.after = after

    def __repr__(self) -> str:
        return f"<Combined: {self.first} {self.second}>"

    def _schedule_for(self, obj: T, *,
                      post_result: bool = True,
                      ) -> Delayed[V2]:
        """
        Implementat :func:`Operation.schedule_for` by scheduling :attr:`second` after :attr:`first` is done.

        :meta public:
        Args:
            obj: the :attr:`T` object to schedule the operation for
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``.
        """
        return self.first._schedule_for(obj) \
                    .then_schedule(self.second, after=self.after, post_result=post_result)

    def after_delay(self,
                    after: WaitCondition,
                    fn: Callable[[], V2],
                    *, obj: T) -> Delayed[V2]:
        return self.first.after_delay(after, fn, obj=obj)


class ComputeOp(Generic[T, V], Operation[T, V]):
    """
    A :class:`Operation` that when scheduled, returns the result of passing its
    scheduled-for object to a :class:`Callable` that returns a :class:`Delayed` object.

    Args:
        T: the type of the object used to schedule the :class:`Operation`
        V: the type of the value produced by the operation
    """
    def __init__(self, function: Callable[[T],Delayed[V]], * scheduler: CommunicationScheduler) -> None:
        """
        Initialize the :class:`ComputeOp`

        Args:
            function: The :class:`Callable` to call.
        """
        self.function: Final[Callable[[T],Delayed[V]]] = function   ; "The :class:`Callable` to call"

    def __repr__(self) -> str:
        return f"ComputeOp({self.function})"

    def _schedule_for(self, obj: T, *,
                      post_result: bool = True,
                      ) -> Delayed[V]:
        """
        Implement :func:`Operation.schedule_for` by passing `obj` to :attr:`function`.

        :meta public:

        Note:
            ``post_result`` is asserted to be ``True``.

        Args:
            obj: the :attr:`T` object to schedule the operation for
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``.
        """
        assert post_result == True
        return self.function(obj)

    def after_delay(self,
                    after: WaitCondition,
                    fn: Callable[[], V],
                    *, obj: T) -> Delayed[V]:
        raise NotImplementedError('"after_delay" not supported for "ComuteOp"')


class OpScheduler(Generic[T]):
    """
    A mixin base class giving a class the ability to schedule
    :class:`Operation`\[:attr:`CS`, :attr:`V`]s.

    Typically, this will be class :attr:`CS` itself, as in::

        class Drop(OpScheduler['Drop']):
            ...
    There are several :class:`Operation`\s (e.g., :class:`WaitAt`,
    :class:`Reach`, :class:`WaitFor`), that are defined for all
    :class:`OpScheduler`\s.

    Args:
        CS: A subclass of :class:`OpScheduler`
    """
    def schedule(self: CS,
                 op: Union[Operation[CS, V], Callable[[],Operation[CS, V]]],
                 after: WaitCondition = NO_WAIT,
                 post_result: bool = True,
                 ) -> Delayed[V]:
        """
        Schedule an operation for this object, which is assumed to be a :attr:`CS`.

        If ``op`` is a :class:`Callable`, it is called to get the actual :class:`Operation`.

        Args:
            op: The :class:`Operation` to schedule or a :class:`Callable` to call to obtain it.
            after: an optional delay to wait before scheduling the operation
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``.
        """
        if not isinstance(op, Operation):
            op = op()
        return op.schedule_for(self, after=after, post_result=post_result)

    class WaitAt(CSOperation[CS,CS]):
        """
        An :class:`Operation` during which the :attr:`CS` object waits at a
        :class:`Barrier`.  The operation completes when the appropriate number
        of objects have reached the barrier.  The value posted to the
        :class:`Delayed` value returned by :func:`schedule_for` is the object
        for which the operation was scheduled.
        """
        barrier: Barrier[CS]    ; "The :class:`Barrier` to wait at"
        def __init__(self, barrier: Barrier):
            """
            Initialize the object

            Args:
                barrier: the :class:`Barrier` to wait at
            """
            self.barrier = barrier

        def _schedule_for(self, obj: CS, *,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[CS]:
            """
            Implement :func:`Operation.schedule_for` by pausing at :attr:`barrier`.

            :meta public:
            The value posted to the returned future will be ``obj``.

            Args:
                obj: the :attr:`CS` object to schedule the operation for
            Keyword Args:
                post_result: whether to post the resulting value to the returned future object (unused)
            Returns:
                a :class:`Delayed`\[:attr:`CS`] future object to which ``obj``
                will be posted
            """
            future = Postable[CS]()
            self.barrier.pause(obj, future)
            return future

    class Reach(Operation[CS,CS]):
        """
        An :class:`Operation` during which the :attr:`CS` object reaches a
        :class:`Barrier` but does not pause there.  The operation completes
        immediately (or after the delay specified by ``after``).  The
        value posted to the :class:`Delayed` value returned by
        :func:`schedule_for` is the object for which the operation was
        scheduled.
        """
        barrier: Barrier[CS]    ; "The :class:`Barrier` to reach"
        def __init__(self, barrier: Barrier):
            """
            Initialize the object

            Args:
                barrier: the :class:`Barrier` to reach
            """
            self.barrier = barrier

        def _schedule_for(self, obj: CS, *,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[CS]:
            """
            Implement :func:`Operation.schedule_for` by reaching, but not
            pausing at :attr:`barrier`.

            :meta public:
            The value posted to the returned future will be ``obj``.

            Args:
                obj: the :attr:`CS` object to schedule the operation for
            Keyword Args:
                post_result: whether to post the resulting value to the returned future object
            Returns:
                a :class:`Delayed`\[:attr:`CS`] future object to which ``obj``
                will be posted unless ``post_result`` is ``False``
            """
            future = Postable[CS]()
            self.barrier.pass_through(obj)
            if post_result:
                future.post(obj)
            return future

    class WaitFor(CSOperation[CS,CS]):
        """
        An :class:`Operation` during which the :attr:`CS` object waits for a
        :class:`WaitableType` to be satisfied.

        * If :attr:`waitable` is a :class:`.Time` or :class:`Ticks`, the
          operation completes after that delay.

        * If :attr:`waitable` is a :class:`Delayed`, the operation completes
          when a value is posted to :attr:`waitable`.

        * If :attr:`waitable` is a :class:`Trigger`, the operation completes
          when :attr:`waitable` fires.

        The value posted to the :class:`Delayed` value returned by
        :func:`schedule_for` is the object for which the operation was
        scheduled.
        """
        waitable: WaitableType  ; "What to wait for"
        def _schedule_for(self, obj: CS, *,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[CS]:
            """
            Implement :func:`Operation.schedule_for` by waiting for :attr:`waitable`.

            :meta public:
            * If :attr:`waitable` is a :class:`.Time` or :class:`Ticks`, the
              operation completes after that delay.

            * If :attr:`waitable` is a :class:`Delayed`, the operation completes
              when a value is posted to :attr:`waitable`.

            * If :attr:`waitable` is a :class:`Trigger`, the operation completes
              when :attr:`waitable` fires.

            Args:
                obj: the :attr:`CS` object to schedule the operation for
            Keyword Args:
                post_result: whether to post the resulting value to the returned future object (unused)
            Returns:
                a :class:`Delayed`\[:attr:`CS`] future object to which ``obj``
                will be posted
            """
            future = Postable[CS]()

            waitable = self.waitable

            def cb() -> None:
                if isinstance(waitable, Delayed):
                    waitable.when_value(lambda _: future.post(obj))
                elif isinstance(waitable, Trigger):
                    waitable.wait(obj, future)
                else:
                    assert isinstance(waitable, Time) or isinstance(waitable, Ticks)
                    wait_future = obj.delayed(lambda: obj, after=waitable)
                    wait_future.post_to(future)
            cb()
            return future

        def __init__(self, waitable: WaitableType) -> None:
            """
            Initialize the object

            Args:
                waitable: what to wait for
            """
            self.waitable = waitable


class StaticOperation(Generic[V], ABC):
    '''
    An operation that can be scheduled and which returns a delayed value of type
    :attr:`V`.  This is like :class:`Operation`\[:attr:`T`, :attr:`V`], but it
    does not require an object of type :attr:`T`.

    The basic notion is that if `op` is a :class:`StaticOperation`\[:attr:`V`], in ::

        dv: Delayed[V] = op.schedule()

    the call will return immediately, and `dv` will obtain a value of type :attr:`V` at some point
    in the future, when the operation has completed.

    The same effect can be obtained by calling :func:`mpam.types.schedule`::

        dv: Delayed[V] = schedule(op)

    Note:
        :class:`StaticOperation`\[:attr:`V`] is an abstract base class.
        The actual implementation class must implement :func:`_schedule`.

    Args:
        V: The type of the value that is the result of the :class:`StaticOperation`
    '''

    scheduler: Final[CommunicationScheduler]

    def __init__(self, *, scheduler: CommunicationScheduler) -> None:
        self.scheduler = scheduler

    @abstractmethod
    def _schedule(self, *,
                  post_result: bool = True,       # @UnusedVariable
                  ) -> Delayed[V]:
        """
        The implementation of :func:`schedule`.  There is no default implementation.

        :meta public:
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        ...


    def schedule(self, *,
                 after: WaitCondition = NO_WAIT,
                 post_result: bool = True,
                 ) -> Delayed[V]:
        """
        Schedule this operation.

        Once an object has been identified, the actual scheduling will be
        delegated through :func:`_schedule_for`.

        Keyword Args:
            after: an optional delay to wait before scheduling the operation
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        def cb():
            self._schedule(post_result=post_result)
        return self.scheduler.delayed(cb, after=after)

    def then(self, op: Union[Operation[V, V2], StaticOperation[V2], # type: ignore [type-var]
                             Callable[[], Operation[V, V2]],
                             Callable[[], StaticOperation[V2]]],
             after: WaitCondition = NO_WAIT,
             ) -> StaticOperation[V2]:
        """
        Chain this :class:`StaticOperation` and follow-on :class:`Operation`
        together to create a single new :class:`StaticOperation`

        The value produced by this :class:`StaticOperation` will be used to schedule
        the second :class:`Operation` (unless the second is a :class:`StaticOperation`, in
        which case the second will be scheduled after this one is done).

        The actual result will be a :class:`CombinedStaticOperation`\[:attr:`V`, :attr:`V2`].

        Note:
            If ``op`` is a :class:`Callable`, it will be evaluated when the
            :class:`StaticOperation` that is the result of :func:`then` is
            **scheduled**, not when this :class:`StaticOperation` produces a value.

        Args:
            op: the second :class:`Operation` (or a :class:`StaticOperation`) or a :class:`Callable` that
                returns one
            after: an optional delay to apply between the completion of this operation and the second
        Returns:
            the new :class:`StaticOperation`
        """
        return CombinedStaticOperation[V, V2](self, op, after=after)

    def then_compute(self, fn: Callable[[V], Delayed[V2]]) -> StaticOperation[V2]:
        """
        Create a new :class:`StaticOperation` that passes the result of this one
        to a :class:`Callable` that returns a :class:`Delayed` value.

        The only reason that both this and :func:`then_call` are needed is
        that Python can't distinguish :class:`Callable`\s based on their return
        types.

        Args:
            fn: the :class:`Callable` that computes the new operation's value
        Returns:
            the new :class:`StaticOperation`
        """
        return self.then(ComputeOp[V, V2](fn))

    def then_call(self, fn: Callable[[V], V2]) -> StaticOperation[V2]:
        """
        Create a new :class:`StaticOperation` that passes the result of this one to a
        :class:`Callable` and use its value as the overall value.

        The only reason that both this and :func:`then_compute` are needed is
        that Python can't distinguish :class:`Callable`\s based on their return
        types.

        Args:
            fn: the :class:`Callable` that computes the new operation's value
        Returns:
            the new :class:`StaticOperation`
        """
        def fn2(obj: V) -> Delayed[V2]:
            future = Postable[V2]()
            future.post(fn(obj))
            return future
        return self.then_compute(fn2)

    def then_process(self, fn: Callable[[V], Any]) -> StaticOperation[V]:
        """
        Create a new :class:`StaticOperation` that passes the result of this one
        to a :class:`Callable`, but uses this :class:`SOperation`\s result as the
        final result.

        The difference between this and :func:`then_call` and :func:`then_compute` is
        that the result of the latter call is ignored.

        Args:
            fn: the :class:`Callable` that will be called with this :class:`Operation`\'s result
        Returns:
            the new :class:`Operation`
        """
        def fn2(obj: V) -> V:
            fn(obj)
            return obj
        return self.then_call(fn2)


class CombinedStaticOperation(Generic[V, V2], StaticOperation[V2]):
    """
    A :class:`StaticOperation` representing chaining a :class:`StaticOperation`
    and an :class:`Operation` together.

    Objects of this class are built using :func:`StaticOperation.then`,
    :func:`StaticOperation.then_call`, :func:`StaticOperation.then_compute`, and
    :func:`StaticOperation.then_process`,

    Args:
        V: the type of the value produced by the first operation
        V2: the type of the value produced by the second operation (and the
            :class:`CombinedStaticOperation` overall)
    """

    first: StaticOperation[V]               ; "The first :class:`StaticOperation`"
    second: Union[Operation[V, V2], StaticOperation[V2], # type: ignore [type-var]
                  Callable[[], Operation[V, V2]],
                  Callable[[], StaticOperation[V2]]]
    """
    The second :class:`Operation` (or :class:`StaticOperation`) or a :class:`Callable` that produces one.
    """
    after: Final[WaitCondition]   ; "An optional delay to use between :attr:`first` and :attr:`second`"

    def __init__(self, first: StaticOperation[V],
                 second: Union[Operation[V, V2], StaticOperation[V2], # type: ignore [type-var]
                               Callable[[], Operation[V, V2]],
                               Callable[[], StaticOperation[V2]]], *,
                 after: WaitCondition = NO_WAIT) -> None:
        """
        Initialize the object

        Args:
            first: The first :class:`StaticOperation`
            second: the second :class:`Operation` (or :class:`StaticOperation`) or a :class:`Callable`
                    that produces one.
        Keyword Args:
            after: an optional delay to use between the two :class:`Operation`\s
        """
        self.first = first
        self.second = second
        self.after = after

    def _schedule(self, *,
                  post_result: bool = True,
                  ) -> Delayed[V2]:
        """
        Implement :func:`Operation.schedule_for` by scheduling :attr:`second` after :attr:`first` is done.

        :meta public:
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`V2`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        return self.first._schedule() \
                    .then_schedule(self.second, after=self.after, post_result=post_result)


class Delayed(Generic[Tco]):
    """
    A container that will (or may) eventually contain a value of type :attr:`T`.

    :class:`Delayed` is an abstract class.  Instances are created either by
    using the :func:`complete` class method::

        dv = Delayed.complete(val)

    to create an instance that has its value from the start or by creating a
    :class:`Postable` subclass.  In the latter case, the value is asserted by
    calling the :class:`Postable`'s :func:`~Postable.post` method::

        postable.post(val)

    The value may only be specified once (although it need not ever be
    specified).  When a value is posted, any registered *callbacks* will be
    invoked and passed the posted value.

    :class:`Delayed` is *covariant* in its type parameter, so a
    :class:`Delayed`\[``Derived``] can be treated as a
    :class:`Delayed`\[``Base``].  Conversely, the concrete subclass
    :class:`Postable` is *contravariant* in its type parameter, so a
    :class:`Postable`\[``Base``] can be treated as a
    :class:`Postable`\[``Derived``].

    To register a callback, the :func:`when_value` method (or its alias,
    :func:`then_call`) or one of the many methods that delegate to it are used
    ::

        dv.when_value(do_the_stuff)
        dv.then_call(lambda val : print(f"got {val}")
        dv.post_to(future)
        dv.post_transformed_to(future, lambda v: str(v))
        dv.post_val_to(future, val)
        dv2 = dv.then_schedule(operation)
        dv2 = dv.chain(future)
        dv2 = dv.transformed(lambda n: n+1)

    Note:
        If the :class:`Delayed` object already has a value at the time the
        callback is added, the callback is invoked immediately.  Otherwise, it
        is remembered and invoked in the thread that calls
        :func:`~Postable.post` on its :class:`Postable` subclass instance.

    All methods that register callbacks return :class:`Delayed` objects and can,
    therefore, be chained to add more callbacks::

        dv.when_value(fn1)
          .when_value(fn2)
          .post_val_to(dv2, 7)

    Note, however, that some of the methods return different :class:`Delayed`
    objects that will receive transformed values.

    :class:`Delayed` objects are thread-safe.   A :class:`~threading.Lock` is
    only constructed if a value has not been asserted at the time the first
    callback is added.  (It would be trivial to avoid the lock if Python had an
    atomic compare-and-swap operation, but alas.)

    To obtain the value of a :class:`Delayed` object, use one of ::

        f(dv.value)        # blocks until a value is asserted

        dv.wait()          # blocks until a value is asserted
        f(dv.value)        # now guaranteed not to block

        if dv.has_value:
            f(dv.value)    # guaranteed to not block

        valid, val = dv.peek()    # returns immediately
        if valid:
            f(val)         # val is the value

    Note that there is a difference between the :class:`Delayed` object not
    having a value and having a value of ``None``.

    To block until more than one :class:`Delayed` object have all received
    values, use :func:`join`.

    Args:
        Tco: The covariant type of the value that will be asserted.
    """

    _val: ValTuple[Tco] = (False, cast(Tco, None))
    """
    A tuple containing the validity status and value (if valid)

    All :class:`Delayed` objects share the same invalid value and assert their
    own local valid values.  This allows :class:`Delayed` objects to be
    trivially constructed.

    The cast is necessary because ``None`` is likely to not be a valid instance
    of :attr:`T`, but nobody should be looking there if the first element is
    ``False``.
    """
    _maybe_lock: Optional[Lock] = None
    """
    A lock object, if any callbacks have been asserted.
    """

    _callbacks: list[Callable[[Tco], Any]]
    """
    The list of callbacks.  This is created within :attr:`_lock` if necessary.

    This object can only be referenced while :attr:`_lock` is locked.
    """

    def __str__(self):
        return f'Delayed({self._val})'

    @property
    def _lock(self) -> Lock:
        """
        The object's private lock.  We use a property so that we don't actually
        create the lock until we know we're going to need one.  The first time
        it is referenced, the lock is created.  Since :attr:`_callbacks` is only
        used while this lock is locked, when we create the lock, we also create
        that list.

        Note:
            Yes, there's a potential race here if two threads call
            :func:`when_value` at the same time and each decides that its the
            first one in, which will result in each creating different locks and
            callback lists, and the first callback never being seen.  There's
            only so much you can do without CAS operations.
        """
        # Yeah, there's a race here if two threads call
        # when_value() at the same time, as they'll each
        # lock different ones.  There's only so much
        # I can do if you won't give me a CAS operation
        lock = self._maybe_lock
        if lock is None:
            lock = Lock()
            self._maybe_lock = lock
            # if we're creating a lock, we're going to be
            # adding a callback, so we add that attribute
            # here.
            self._callbacks = []
        return lock

    @abstractmethod
    def _define_in_concrete(self) -> None: ...

    @property
    def has_value(self) -> bool:
        """
        Has a value been asserted?
        """
        return self._val[0]

    def peek(self) -> ValTuple[Tco]:
        """
        Check both whether a value has been asserted and what that value is.

        Returns:
            (``True``, ``value``) if ``value`` is the asserted value, otherwise
            (``False``, ``None``)

        Warning:
            The type of the second element is only valid if the first element is
            ``True``.  If it is not, the second element will be ``None``, which
            may not be a valid :attr:`T`.  It is therefore important not to use
            the second element if the first element is ``False``.

            Note that the second element being ``None`` does not indicate that
            the value has not been asserted if ``None`` is a valid :attr:`T`.
        """
        return self._val

    def wait(self) -> None:
        """
        Block the thread until a value has been asserted
        """
        if not self.has_value:
            e = Event()
            def do_set(_) -> None:
                e.set()
            self.when_value(do_set)
            # self.when_value(lambda _: e.set())
            while not e.is_set():
                # We probably want a timeout here to allow it to be interrupted
                e.wait()

    and_wait = wait

    @property
    def value(self) -> Tco:
        """
        The asserted value, blocking if necessary.
        """
        self.wait()
        return self._val[1]

    @classmethod
    def complete(cls, val: T) -> Delayed[T]:
        """
        A class method that constructs a :class:`Delayed` object with the value
        already asserted.  Since this happens before any callbacks can be
        attached, any callbacks will be executed immediately.

        Args:
            val: the value to be asserted
        Returns:
            A new :class:`Delayed` object with ``val`` as the asserted value.
        """
        return _CompleteDelayed(val)

    def then_schedule(self, op: Union[Operation[Tco, V], StaticOperation[V], # type: ignore [type-var]
                                      Callable[[], Operation[Tco, V]],
                                      Callable[[], StaticOperation[V]]], *,
                      after: WaitCondition = NO_WAIT,
                      post_result: bool = True) -> Delayed[V]:
        """
        Schedule an :class:`Operation` or :class:`StaticOperation` when a value
        is asserted.  If ``op`` is an :class:`Operation`, it is scheduled for
        the asserted value.

        If ``op`` is a :class:`Callable`, it is called to get the actual
        :class:`Operation` or :class:`StaticOperation`.

        Args:
            op: The :class:`Operation` or :class:`StaticOperation` to schedule
                or a :class:`Callable` to call to obtain it.
        Keyword Args:
            after: an optional delay to wait before scheduling the operation
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a new :class:`Delayed` object which will receive the result of
            ``op`` when it completed.
        """
        if isinstance(op, StaticOperation):
            return op.schedule(after=after, post_result=post_result)
        elif isinstance(op, Operation):
            return op.schedule_for(self, after=after, post_result=post_result)
        else:
            return self.then_schedule(op(), after=after, post_result=post_result)

    def chain(self, fn: Callable[[Tco], Delayed[V]]) -> Delayed[V]:
        """
        When a value is asserted, pass it to a function.  This is used when the
        function returns a :class:`Delayed` value.

        The only reason that both this and :func:`transformed` are needed is
        that Python can't distinguish :class:`Callable`\s based on their return
        types.

        Note:
            The :class:`Delayed` object returned by this function is not the
            same one as the one returned by ``fn``.  When the latter receives a
            value, so will the one returned by this function, so callbacks can
            be added to either.

        Args:
            fn: A function that can take the asserted value and which returns a
                :class:`Delayed` object
        Returns:
            A :class:`Delayed` object that will mirror the one returned by
            ``fn``
        """
        future = Postable[V]()
        def fn2(val) -> None:
            fn(val).post_to(future)
        self.when_value(fn2)
        # self.when_value(lambda val: fn(val).post_to(future))
        return future

    def transformed(self, fn: Callable[[Tco], V]) -> Delayed[V]:
        """
        When a value is asserted, pass it to a function.

        The only reason that both this and :func:`chain` are needed is
        that Python can't distinguish :class:`Callable`\s based on their return
        types.

        Args:
            fn: A function that can take the asserted value
        Returns:
            A :class:`Delayed` object that will receive the transformed value.
        """
        future = Postable[V]()
        def post_transformed(val) -> None:
            future.post(fn(val))
        self.when_value(post_transformed)
        # self.when_value(lambda val: future.post(fn(val)))
        return future

    def then_trigger(self, trigger: Trigger) -> Delayed[Tco]:
        """
        When a value is asserted, fire a :class:`Trigger`.

        Args:
            trigger: the :class:`Trigger` to fire
        Returns
            this :class:`Delayed` object
        """
        def do_trigger(_) -> None:
            trigger.fire()
        self.when_value(do_trigger)
        # self.when_value(lambda _: trigger.fire())
        return self

    def post_to(self, other: Postable[Tco]) -> Delayed[Tco]:
        """
        When a value is asserted, post it to another :class:`Delayed` object.

        Args:
            other: a second :class:`Delayed` object
        Returns
            this :class:`Delayed` object
        """
        def do_post(val) -> None:
            other.post(val)
        self.when_value(do_post)
        # self.when_value(lambda val: other.post(val))
        return self

    def post_val_to(self, other: Postable[V], value: V) -> Delayed[Tco]:
        """
        When a value is asserted, post a specific value to another
        :class:`Delayed` object.

        Args:
            other: a second :class:`Delayed` object
            value: the value to post
        Returns
            this :class:`Delayed` object
        """
        def do_post(_) -> None:
            other.post(value)
        self.when_value(do_post)
        # self.when_value(lambda _: other.post(value))
        return self

    def post_transformed_to(self, other: Postable[V],
                            transform: Callable[[T], V]) -> Delayed[Tco]:
        """
        When a value is asserted, transform it and post it to another
        :class:`Delayed` object.

        Args:
            other: a second :class:`Delayed` object
            transform: the :class:`Callable` to use to transform the asserted
                       value
        Returns
            this :class:`Delayed` object
        """
        def do_post(val) -> None:
            other.post(transform(val))
        self.when_value(do_post)
        # self.when_value(lambda val: other.post(transform(cast(T, val))))
        return self

    def when_value(self, fn: Callable[[Tco], Any]) -> Delayed[Tco]:
        """
        Register a callback to be passed the asserted value.

        If this :class:`Delayed` object already has a value, ``fn`` is called
        immediately.  Otherwise it will be called when the value is asserted.

        :func:`when_value` and :func:`then_call` refer to the same method.

        Note:
            If the callback is called when the value is asserted, it will be
            called in the thread asserting the value.

        Args:
            fn: a :class:`Callable` to receive the asserted value.
        Returns
            this :class:`Delayed` object
        """
        v = self._val
        just_run: bool = v[0]
        if not just_run:
            # print("Adding to wait queue")
            with self._lock:
                v = self._val
                just_run = v[0]
                if not just_run:
                    self._callbacks.append(fn)
        if just_run:
            fn(v[1])
        return self

    # or maybe then_call should create a new future, posted at the end.
    then_call = when_value


    @classmethod
    def join(cls, futures: Union[Delayed, Iterable[Delayed]]) -> None:
        """
        Block the thread until the provided :class:`Delayed` objects have all
        received values.

        Args:
            futures: a :class:`Delayed` object or a sequence of them.
        """
        if isinstance(futures, Delayed):
            futures.wait()
        else:
            for f in futures:
                f.wait()

class _CompleteDelayed(Delayed[T]):
    def _define_in_concrete(self)->None: ...

    def __init__(self, val: T) -> None:
        self._val = (True, val)

class Postable(Delayed[Tcontra]):
    """
    A concrete subclass of :class:`Delayed` that provides a :func:`post` method
    to assert a value, which will be passed to any waiting callbacks.

    :class:`Delayed` is *covariant* in its type parameter, so a
    :class:`Delayed`\[``Derived``] can be treated as a
    :class:`Delayed`\[``Base``].  Conversely, the concrete subclass
    :class:`Postable` is *contravariant* in its type parameter, so a
    :class:`Postable`\[``Base``] can be treated as a
    :class:`Postable`\[``Derived``].

    More concretely, given ::

        class Top: ...
        class Middle(Top): ...
        class Bottom(Middle): ...

        p = Postable[Middle]()
    ``p`` can be treated as a :class:`Delayed`\[``Middle``], a
    :class:`Delayed`\[``Top``], or a :class:`Postable`\[``Bottom``].

    :func:`post` may only be called once (although it need not ever be called).
    When a value is posted, any registered *callbacks* will be invoked and
    passed the posted value.

    Args:
        Tcontra: the contravariant type that can be asserted using :func:`post`.
    """

    def _define_in_concrete(self) -> None: ...

    # The logic here is a bit tricky, but I think it works.
    # We're racing against when_value().  If we see that there's
    # no _maybe_lock, that means that when_value() hasn't yet called
    # self._lock.  We've already set the value, so when it creates
    # the lock and locks it, it will then see that we've already set
    # the value and won't actually add anything.
    #
    # Conversely, if we see that there's a lock, we lock it.  Either
    # we beat the lock in when_value(), in which case it will notice
    # the value and not add, or it's already added and we process it.
    def post(self, val: Tcontra) -> None:
        """
        Assert a value and pass it to any registered callbacks.  Any callbacks
        registered after this point will immediately execute with this value.

        Note:
            :func:`post` may only be called once for any :class:`Postable`
            object.  Calling it a second time will result in an assertion
            failure.
        Note:
            Once :func:`post` has been called, any registered callbacks are
            forgotten.

        Args:
            val: the value to assert
        """
        # TODO: Should this throw an exception instead?
        assert not self.has_value
        self._val = (True, val)
        lock = self._maybe_lock
        if lock is not None:
            with lock:
                for fn in self._callbacks:
                    fn(val)
                # Just in case this object gets stuck somewhere.
                # The callbacks are never going to be needed again
                del self._callbacks


class Trigger:
    """
    An object to which actions may be attached that will be executed when the
    object is fired.

    The actions may be

    * a combination of objects and :class:`Delayed` objects to post them to (via: :func:`wait`)
    * a function of no arguments to be called (via :func:`on_trigger`)

    :class:`Trigger` objects can be fired more than once.  The list of actions
    is cleared every time the object is fired.

    Note:
        Unlike :class:`Delayed` objects, since :class:`Trigger` objects can be
        fired more than once, attaching an action to a :class`Trigger` that has
        already been fired **does not** immediately execute the action.  Rather,
        it waits for the next time the object is fired.

    :class:`Trigger` objects are thread safe
    """
    waiting: list[tuple[Any,Postable]]
    """
    The list of actions waiting to be executed

    Actions registered using :func:`on_trigger` are represented as tuples
    containing ``None`` and a :class:`Delayed` object which will execute the
    function.
    """
    lock: Final[RLock]  #: The object's lock

    @property
    def count(self) -> int:
        """
        The number of actions waiting to be executed
        """
        return len(self.waiting)

    def __init__(self) -> None:
        """
        Initialize the object.
        """
        self.waiting = []
        self.lock = RLock()

    def wait(self, val: Any, future: Postable) -> None:
        """
        When the :class:`Trigger` next fires, post a value to a future.

        Args:
            val: the value to post
            future: the :class:`Delayed` object to post to
        """
        with self.lock:
            self.waiting.append((val, future))

    def on_trigger(self, fn: Callable[[], Any]) -> None:
        """
        When the :class:`Trigger` next fires, call a function

        Args:
            fn: the function (taking no arguments) to call
        """
        future = Postable[None]()
        future.then_call(lambda _: fn())
        self.wait(None, future)

    def fire(self) -> int:
        """
        Process all waiting actions.

        Any actions registered while these actions are being processed will not
        be processed until the next time the :class:`Trigger` fires.

        Returns:
            the number of actions processed
        """
        waiting = self.waiting
        with self.lock:
            self.waiting = []
        val = len(waiting)
        for v,f in waiting:
            f.post(v)
        return val

    def reset(self) -> None:
        """
        Forget all waiting actions.
        """
        with self.lock:
            self.waiting.clear()



class Barrier(Trigger, Generic[T]):
    """
    A :class:`Trigger` that fires when a certain number of :attr:`T` objects
    reach it.  Objects reaching the :class:`Barrier` can optionally "pause" there
    by passing in a :class:`Delayed` object to which the waiting object is
    posted when the last object reaches the :class:`Barrier`.

    A :class:`Barrier` may be reset (by calling :func:`reset`), optionally
    changing the number of objects required required to reach it.  When that
    happens, any objects that had already reached it (and any other actions
    added to it as a :class:`Trigger`) are forgotten.

    Args:
        T: The type of object the :class:`Barrier` is waiting for.
    """
    required: int               #: The number of objects that need to reach the :class:`Barrier`
    waiting_for: int            #: The number of objects that have yet to reach the :class:`Barrier`
    name: Final[Optional[str]]  #: An optional name of the :class:`Barrier`

    @property
    def at_barrier(self) -> int:
        """
        The number of objects that have reached the :class:`Barrier`
        """
        return self.required-self.waiting_for


    def __init__(self, required: int, *, name: Optional[str] = None) -> None:
        """
        Initialize the object.

        Args:
            required: the number of objects that need to reach the :class:`Barrier`
        Keyword Args:
            name: an optional name of the :class:`Barrier`
        """
        super().__init__()
        self.required = required
        self.waiting_for = required
        self.name = name
    def __str__(self) -> str:
        name = (self.name+", ") if self.name is not None else ""
        return f"Barrier({name}{self.required}, {self.waiting_for})"
    def reach(self, val: T, future: Optional[Postable[T]] = None) -> int:
        """
        Note that an object reached the :class:`Barrier`.  If this is the last
        one, :func:`fire` the :class:`Barrier`, unpausing any paused objects.

        If ``future`` is not ``None``, when the :class:`Barrier` fires (e.g.,
        when the last object reaches it), ``val`` will be posted to ``future``.

        Args:
            val: the value that reached the :class:`Barrier`
            future: an optional :class:`Delayed` object that can receive ``val``
        Returns:
            the number of objects that had previously reached the
            :class:`Barrier`
        """
        with self.lock:
            wf = self.waiting_for
            ab = self.required - wf
            assert wf > 0, f"{val} reached un-waiting barrier {self}"
            self.waiting_for = wf-1
            if wf > 1:
                if future is not None:
                    self.wait(val, future)
                return ab
        # If we get here, we're the last one to reach, so we fire the trigger
        # and process this future.

        # Note that we're not inside the lock (we don't want to fire inside the
        # lock), so there will be a problem if somebody else calls reset()
        # before we call fire().
        self.fire()
        if future is not None:
            future.post(val)
        return ab

    def pause(self, val: T, future: Postable[T]) -> int:
        """
        Reach the :class:`Barrier` and pause there.  Equivalent to calling
        :func:`reach`, but ``future`` is not optional.

        Args:
            val: the value that reached the :class:`Barrier`
            future: a :class:`Delayed` object that can receive ``val``
        Returns:
            the number of objects that had previously reached the
            :class:`Barrier`
        """
        return self.reach(val, future)

    def pass_through(self, val: T) -> int:
        """
        Reach the :class:`Barrier` without pausing there.  Equivalent to calling
        :func:`reach` without a ``future`` parameter.

        Args:
            val: the value that reached the :class:`Barrier`
        Returns:
            the number of objects that had previously reached the
            :class:`Barrier`
        """
        return self.reach(val)

    def reset(self, required: Optional[int] = None) -> None:
        """
        Forget any objects that have reached the :class:`Barrier` and any pending actions.

        If ``required`` is not ``None``, it becomes the new number of objects
        the :class:`Barrier` is waiting for.

        Args:
            required: an optional integer specifying the new number of objects
                      to wait for.
        """
        with self.lock:
            if required is not None:
                self.required = required
            self.waiting_for = self.required
            # if self.name is not None:
            #     print(f"Reset {self} to {required}")
            super().reset()



def schedule(op: Union[StaticOperation[V], Callable[[], StaticOperation[V]]], *,
             after: WaitCondition = NO_WAIT,
             post_result: bool = True,
             ) -> Delayed[V]:
    """
    Schedule an :class:`StaticOperation`.

    If ``op`` is a :class:`Callable`, it is called to get the actual :class:`StaticOperation`.

    Args:
        op: The :class:`StaticOperation` to schedule or a :class:`Callable` to call to obtain it.
    Keyword Args:
        after: an optional delay to wait before scheduling the operation
        post_result: whether to post the resulting value to the returned future object
    Returns:
        a :class:`Delayed`\[:attr:`V`] future object to which the resulting
        value will be posted unless ``post_result`` is ``False``.
    """
    if isinstance(op, StaticOperation):
        return op.schedule(after=after, post_result=post_result)
    else:
        return op().schedule(after=after, post_result=post_result)

ChangeCallback = Callable[[T,T],None]
"""
A function that takes two parameters of type :attr:`T` representing the old and
new values of some attribute.
"""

class ChangeCallbackList(Generic[T]):
    """
    A hook onto which value-change handlers may be added.  When the list is
    processed (via :func:`process`), each handler is passed the old and new
    values (which may be the same).

    Handlers may optionally be associated with a key (of any :class:`Hashable`
    type).  If a handler is added with a key that already exists in the
    :class:`ChangeCallbackList`, the old value is replaced.  If no key is specified,
    the handler itself is used as the key and no replacement will take place.

    Args:
        T: the type of the value being managed
    """
    callbacks: Optional[dict[Hashable, ChangeCallback[T]]] = None    #: A mapping from keys to handlers
    lock: Final[RLock]                              #: The object's lock

    def __init__(self) -> None:
        """
        Initialize the object.
        """
        self.lock = RLock()

    def add(self, cb: ChangeCallback[T], *, key: Optional[Hashable] = None) -> None:
        """
        Add a new handler, replacing any with the specified key.  If ``key`` is
        ``None``, ``cb`` is used as the key

        Args:
            cb: the handler
        Keyword Args:
            key: the (optional) key
        """
        if key is None:
            key = cb
        with self.lock:
            if self.callbacks is None:
                self.callbacks = {}
            self.callbacks[key] = cb
            # print(f"Now {len(self.callbacks)} callback(s) on {self}")
            # if key is not cb:
                # print(f"Adding callback {key}")
                # print(f"  Callbacks now {map_str(list(self.callbacks.keys()))}")

    def __call__(self, cb: ChangeCallback[T], *, key: Optional[Hashable] = None) -> None:
        """
        Add a new handler, replacing any with the specified key.  If ``key`` is
        ``None``, ``cb`` is used as the key.

        An alias for :func:`add`.

        Args:
            cb: the handler
        Keyword Args:
            key: the (optional) key
        """
        self.add(cb, key=key)

    def mapped(self, transform: Callable[[T,T], Optional[tuple[V,V]]], *,
               key: Optional[Hashable] = None
               ) -> ChangeCallbackList[V]:
        """
        Create a new :class:`ChangeCallbackList` whose handlers receive
        transformed (and possibly filtered) values.

        ``transform`` is a function that takes the old and new values and
        returns either a tuple of transformed old and new values (possibly of a
        different type) or ``None``.  In the former case, the transformed values
        are :func:`process`ed by the new :class:`ChangeCallbackList`.  In the
        latter case, nothing is passed on.

        For example, after ::

            new_ccl = ccl.mapped(lambda old, new: (str(old), str(new)))

        ``new_ccl`` is a :class:`ChangeCallbackList`\[``str``] whose handlers
        receive the values of `ccl` transformed into strings.

        :func:`mapped` is implemented using :func:`add`.  If ``key`` is
        ``None``, the actual key will be something you can't get your hands on.

        Note:
            If :func:`clear` is called on this (i.e., the existing)
            :class:`ChangeCallbackList`, the link with the new one will be
            severed.

        Args:
            transform: a function that transforms old and new values into either
                       a pair of old and new values (possibly of a different
                       type) or ``None`` to signal that the values should not be
                       passed on.
        Keyword Args:
            key: the (optional) key
        Returns:
            a new :class:`ChangeCallbackList`
        """
        ccl = ChangeCallbackList[V]()
        def cb(old: T, new: T) -> None:
            transformed = transform(old, new)
            if transformed is not None:
                ccl.process(transformed[0], transformed[1])
        self.add(cb, key=key)
        return ccl

    def filtered(self, test: Callable[[T,T], bool], *,
                 key: Optional[Hashable] = None) -> ChangeCallbackList[T]:
        """
        Create a new :class:`ChangeCallbackList` whose handlers are invoked only
        if ``test`` returns ``True`` when passed the old and new values (as a pair).

        For example, after ::

            new_ccl = ccl.filtered(lambda old, new: new > old)

        ``new_ccl`` is a :class:`ChangeCallbackList` whose handlers are invoked
        only when the change is an increase in value.

        :func:`filtered` is implemented using :func:`add`.  If ``key`` is
        ``None``, the actual key will be something you can't get your hands on.

        Note:
            If :func:`clear` is called on this (i.e., the existing)
            :class:`ChangeCallbackList`, the link with the new one will be
            severed.

        Args:
            test: a function that returns ``True`` if the values should be
                  passed on and ``False`` otherwise
        Keyword Args:
            key: the (optional) key
        Returns:
            a new :class:`ChangeCallbackList`
        """
        return self.mapped(lambda old, new: (old, new) if test(old, new) else None,
                           key=key)

    def remove(self, key: Hashable) -> None:
        """
        Remove the handler with the given key, which must have been added.

        Args:
            key: the key to remove
        Raises:
            :class:`KeyError`: if no handler with that key exists
        """
        with self.lock:
            # val = self.callbacks[key]
            cbs = self.callbacks
            if cbs is None:
                raise KeyError(key)
            del cbs[key]
            if len(cbs) == 0:
                self.callbacks = None
            # if key is not val:
                # print(f"Removing callback {key}")
                # print(f"  Callbacks now {map_str(list(self.callbacks.keys()))}")

    def discard(self, key: Hashable) -> None:
        """
        Remove the handler with the given key if one exists.

        Args:
            key: the key to remove
        """
        cbs = self.callbacks
        if cbs is not None:
            with self.lock:
                cbs.pop(key, None)
                if len(cbs) == 0:
                    self.callbacks = None

    def clear(self) -> None:
        """
        Remove all handlers.
        """
        with self.lock:
            self.callbacks = None

    def process(self, old: T, new: T) -> None:
        """
        Pass old and new values to all handlers.

        The list of handlers is copied before calling any handlers, so any
        handlers added while handlers are being invoked will not be invoked
        until the next time :func:`process` is called.

        Args:
            old: the old value
            new: the new value
        """
        # print(f"Processing callbacks")
        if self.callbacks is None:
            return
        with self.lock:
            # Someone might've removed the last callback (and the list) since we
            # looked, so we get it again.
            if (cbs := self.callbacks) is None:
                # MyPy thinks this is unreachable.  It's wrong.
                return  # type: ignore [unreachable]
            copy = list((k,cb) for k,cb in cbs.items())
        for k,cb in copy:
            # print(f"Callback ({old}->{new}: {k}")
            cb(old, new)



OT = TypeVar("OT")
OTcontra = TypeVar("OTcontra", contravariant=True)

class Gettable(Protocol[OTcontra, Tco]):
    """
    A protocol specifying that calling ``__get__()`` on some object will return
    a value.

    Args:
        OTcontra: the (contravariant) type of the object
        Tco: the (covariant) type of the value returned
    """
    def __get__(self, obj: OTcontra, objtype: type[OTcontra]) -> Tco: ... # @UnusedVariable

class _CCLProperty(Generic[T]):
    prop: Final[MonitoredProperty]
    tag: Final[str]
    _attr: Optional[str] = None

    @property
    def attr(self) -> str:
        a = self._attr
        if a is None:
            a = f"{self.prop.callback_list_attr}{self.tag}"
            self._attr = a
        return a

    def __init__(self, prop: MonitoredProperty, tag: str,
                 creator: Callable[[object], ChangeCallbackList[T]]) -> None:
        self.prop = prop
        self.tag = tag
        self.creator = creator
    @overload
    def __get__(self, obj: None, objtype) -> _CCLProperty[T]: ...
    @overload
    def __get__(self, obj: Any, objtype) -> ChangeCallbackList[T]: ...
    def __get__(self, obj, objtype) -> Union[ChangeCallbackList[T], _CCLProperty[T]]: # @UnusedVariable
        if obj is None:
            return self
        attr = self.attr
        ccl = getattr(obj, attr, None)
        if ccl is None:
            ccl = (self.creator)(obj)
            setattr(obj, attr, ccl)
        return ccl

    @staticmethod
    def new_tag() -> str:
        return f"_{random.randrange(1000000)}"

    def mapped(self, transform: Callable[[T,T], Optional[tuple[V,V]]], *,
               key: Optional[Hashable] = None
               ) -> Gettable[object, ChangeCallbackList[V]]:
        me = self
        def creator(obj) -> ChangeCallbackList[V]:
            ccl: ChangeCallbackList[T] = me.__get__(obj, None)
            return ccl.mapped(transform, key=key)
        return _CCLProperty(self.prop, self.new_tag(), creator)

    def filtered(self, test: Callable[[T,T], bool], *,
                 key: Optional[Hashable] = None
                 ) -> Gettable[object, ChangeCallbackList[T]]:
        me = self
        def creator(obj) -> ChangeCallbackList[T]:
            ccl: ChangeCallbackList[T] = me.__get__(obj, None)
            return ccl.filtered(test, key=key)
        return _CCLProperty(self.prop, self.new_tag(), creator)



class MonitoredProperty(Generic[T]):
    """
    An object that behaves like a gettable and settable property, but which also
    provides optional bounds checking, transformation, and a :class:`ChangeCallbackList`

    To get access to the :class:`MonitoredProperty`'s
    :class:`ChangeCallbackList`, use its :attr:`callback_list` property::

        class Counter:
            count = MonitoredProperty[int](default=0)
            on_count_change = count.callback_list

            def inc(self, delta: int = 0) -> None:
                self.count += delta

        counter.on_count_change(lambda old, new: print(f"Changed from {old} to {new}")

    Note:
        The actual :class:`ChangeCallbackList` for an object is not created
        until somebody references it (e.g., by trying to add a callback).

    The optional ``default`` value is the default value to use for this property
    on all objects.  If ``default_fn`` is specified to be a function that takes
    the object and returns a :attr:`MissingOr`\[``T``], it is tried first the
    first time the property is read (via :func:`__get__`) on an object.  If it
    returns :attr:`MISSING`, the ``default`` (if any) will be used.  If it, too,
    is :attr:`MISSING`, then the object does not have a value for the property
    and an :class:`.AttributeError` is raised.  Otherwise, the default value
    will be cached as the value.

    When the property is set (via :func:`__set__`)::

        counter.count = 5

    if any callbacks have been registered for its :attr:`callback_list` on an
    object, all of the :attr:`callback_list`'s callbacks are called, passing in
    the old and new values.  This takes place after the new value has been set.
    The callbacks do not happen if

        1. the object does not have a value (including a default value) for the
           object, either because it has not yet been set or because it has been
           deleted, or

        2. the old and new values are equal (as defined by ``==``) and the
           ``process_duplicates`` parameter to the constructor was not ``True``.

    To check whether an object has a value for the property, use the property's
    :attr:`value_check` property::

        class Counter:
            count = MonitoredProperty[int]()
            has_count = count.value_check

        if counter.has_count:
            print(counter.count)

    After the property is deleted (via :func:`__delete__`) ::

        del counter.count

    it is reset to its initial state.  The next time it is read or has its value
    checked, it is reset to its (static or computed) default value or, if there
    is none, considered to not have a value.

    To provide a public read-only property alongside a protected writable
    property, use the property's :attr:`getter` property::

        class Counter:
            _count = MonitoredProperty[int](default=0)
            count = _count.getter



    Callback properties can be extended using functions akin to
    :class:`ChangeCallbackList`'s :func:`~ChangeCallbackList.mapped` and
    :func:`~ChangeCallbackList.filtered`, e.g. ::

        class Counter:
            count = MonitoredProperty[int](default=0)
            on_count_change = count.callback_list
            on_count_increase = on_count_change.filtered(lambda old, new: new > old)

    Here, a counter's ``on_count_increase`` is a :class:`ChangeCallbackList`
    whose callbacks are only invoked when a change is an increase.  As with
    ``on_count_change``, each object gets its own :class:`ChangeCallbackList`,
    and only gets one if somebody refers to it by trying to add a callback.


    You can also have the property refuse or modify attempted assignment by
    using the :deco:`transform` decorator ::

        @count.transform
        def clip_count(self, val: int) -> int:
            return min(val, self.max_count)

        @count.transform
        def bounds_check(self, val: int) -> MissingOr[int]:
            return val if val <= self.max_count else MISSING

        @count.transform(chain=True)
        def add_one(self, val: int) -> int:
            return val+1

    If the ``chain`` parameter is ``True``, the function will be applied to the
    value of any previous transformations (unless they return :attr:`MISSING`).
    Otherwise, the function replaces any current transformation for the property.

    If the function (or any function in a chain) returns :attr:`MISSING`, the
    assignment is silently aborted.

    Note:
        The decorated transformation functions have their own name, not (as with
        ``@property``), the name of the property.

    Note:
        The transformation chain is called **before** the old value is looked
        up, so if the transformations modify the property , the old value for
        the callbacks from this assignment will be the one immediately prior to
        the actual assignment.  (Any previous assignments would have triggered
        their own callbacks.)

    Note:
        When extracting documentation using Sphinx/Napoleon, the types of the
        properties and their derived properties are not picked up unless you are
        explicit::

            class Counter:
                count: MonitoredProperty[int] = MonitoredProperty(default=0)
                on_count_change: ChangeCallbackList[in] = count.callback_list

        MyPy won't let you annotate the property as ``int``, even though it
        reasons correctly about it.

    Args:
        T: the type of the value stored in the property.
    """

    _name: Optional[str] = None
    _val_attr: Optional[str] = None
    _callback_list_attr: Optional[str] = None


    @property
    def name(self) -> str:
        """
        The name of the property
        """
        n = self._name
        if n is None:
            n = f"monitored_{random.randrange(1000000)}"
            self._name = n
        return n

    @property
    def val_attr(self) -> str:
        """
        The attribute used to store the value on objects
        """
        attr = self._val_attr
        if attr is None:
            attr =  f"_{self.name}__value"
            self._val_attr = attr
        return attr

    @property
    def callback_list_attr(self) -> str:
        """
        The attribute used to store the :class:`ChangeCallbackList` on objects
        """
        attr = self._callback_list_attr
        if attr is None:
            attr = f"_{self.name}__callbacks"
            self._callback_list_attr = attr
        return attr

    _process_duplicates: Final[bool]
    """
    Should the :class:`ChangeCallbackList` be notified if a new
    value is the same as the previous one?
    """

    def __init__(self, name: Optional[str] = None, *,
                 val_attr: Optional[str] = None,
                 callback_list_attr: Optional[str] = None,
                 default: MissingOr[T] = MISSING,
                 default_fn: Optional[Callable[[Any], MissingOr[T]]] = None,
                 process_duplicates: bool = False
                 ) -> None:
        """
        Initialize the object.

        If ``name`` is not specified, the name of the class attribute will be
        used if the :class:`MonitoredProperty` is being used to define one, as in ::

            class Counter:
                count = MonitoredProperty[int](default=0)

        where ``name`` will be taken to be ``"count"``.  (If the attribute name
        begins with a single underscore, the underscore will be removed.)
        Otherwise, a gensymed string (e.g., ``"monitored_12345"``) will be used.
        If ``val_attr`` is not specified, it will be ``"_<name>__value"``.  If
        ``callback_list_attr`` is not specified, it will be
        ``"_<name>__callbacks"``.

        Args:
            name: the (optional) name of the property
        Keyword Args:
            val_attr: the (optional) attribute used to store the value on
                      objects

            callback_list_attr: the (optional) attribute used to store the
                                :class:`ChangeCallbackList` on objects

            default: an optional default value to use for all objects

            default_fn: an optional function to use to compute the default value
                        based on the object.  If it returns :attr:`MISSING`,
                        ``default`` is used.

            process_duplicates: if ``True``, send updates to the
                                :class:`ChangeCallbackList` even if the new and
                                old values are equal.
        """
        if name is not None:
            self._name = name
        if val_attr is not None:
            self._val_attr = val_attr
        if callback_list_attr is not None:
            self._callback_list_attr = callback_list_attr
        self._default_val = default
        self._default_fn = default_fn
        self._process_duplicates = process_duplicates
        self._transform: Callable[[Any, T], MissingOr[T]] = lambda _obj, v: v

    def __set_name__(self, _owner, name: str) -> None:
        if self._name is None:
            # print(f"Setting name for {_owner}.{name}")
            if name.startswith("_") and not name.startswith("__"):
                name = name[1:]
                # print(f"  Name now {name}")
            self._name = name

    def _default_value(self, obj) -> MissingOr[T]:
        dfn = self._default_fn
        if dfn is not None:
            val = dfn(obj)
            if val is not MISSING:
                return val
        return self._default_val


    def _lookup(self, obj) -> MissingOr[T]:
        key = self.val_attr
        val: MissingOr[T] = getattr(obj, key, MISSING)
        if val is MISSING:
            val = self._default_value(obj)
            if val is not MISSING:
                setattr(obj, key, val)
        return val

    def _callback_list(self, obj) -> Optional[ChangeCallbackList[T]]:
        key = self.callback_list_attr
        ccl = getattr(obj, key, None)
        return ccl

    @overload
    def __get__(self, obj: None, objtype) -> MonitoredProperty[T]: ... # @UnusedVariable
    @overload
    def __get__(self, obj: Any, objtype) -> T: ... # @UnusedVariable
    def __get__(self, obj, objtype) -> Union[T, MonitoredProperty[T]]: # @UnusedVariable
        """
        Get the current value of the property for ``obj``, if ``obj`` is not
        ``None``, otherwise return the property itself.  (This last is used to
        refer to the property as an attribute of the type.)

        If the value has not yet been set, this looks for a default value:

        1. First, the function (if any) specified as the ``default_fn`` in
           :func:`__init__` is called, passing in ``obj``.  If this returns
           a value other than :attr:`MISSING`, it is cached and returned.
        2. Otherwise, the value specified as the ``default`` in
           :func:`__init__` is checked.  If it is anything but
           :attr:`MISSING`, it is returned.
        3. Otherwise, :class:`.AttributeError` is raised.

        :meta public:
        Args:
            obj: the object on which to look for the value
            objtype: the type of the object (ignored)
        Returns:
            the value of the property for ``obj``
        Raises:
            AttributeError: when the property has not been set for ``obj`` and
                            there is no default value.
        """
        if obj is None:
            return self
        val = self._lookup(obj)
        if val is MISSING:
            raise AttributeError(f"Attribute '{self.name}' not set in {obj}")
        return val

    def __set__(self, obj, value: T) -> None:
        """
        Set the value of the property for ``obj``.

        If the property has any transformations registered by :deco:`transform`,
        the value is first transformed by calling them.  If the result is
        :attr:`MISSING`, the entire assignment is silently aborted.

        Otherwise, if a callback has been registered to the property's
        :class:`ChangeChallbackList` for ``obj`` the callbacks are processed
        unless

        1. ``obj`` does not have a value (including a default value) for the
           object, either because it has not yet been set or because it has been
           deleted, or

        2. the old and new values are equal (as defined by ``==``) and the
           ``process_duplicates`` parameter to the property's constructor was
           not ``True``.

        Args:
            obj: the object on which to set the value
            value: the value to set
        """

        key = self.val_attr
        maybe_value = (self._transform)(obj, value)
        if maybe_value is MISSING:
            return
        value = maybe_value
        old = self._lookup(obj)
        setattr(obj, key, value)
        if old is not MISSING and (self._process_duplicates or old != value):
            ccl = self._callback_list(obj)
            if ccl is not None:
                ccl.process(old, value)

    def __delete__(self, obj) -> None:
        """
        Remove any value of the property for ``obj``.  If it is subsequently
        read (using :func:`__get__`) before it is explicitly set, a new default
        value will be computed.

        Note:
            Deleting the property does not delete an associated
            :class:`ChangeCallbackList`, so any registered callbacks wiil remain
            registered.  However, if there is no default value, they will not be
            called the next time the value is set, since there will be no "old"
            value.

        Args:
            obj: the object on which to delete the value
        """
        key = self.val_attr
        delattr(obj, key)

    @property
    def callback_list(self) -> _CCLProperty[T]:
        """
        A property that returns the :class:`ChangeCallbackList` for this
        :class:`MonitoredProperty` associated with an object.

        When this property is accessed for an object for the first time, a
        :class:`ChangeCallbackList` is created and cached in the object.

        Typically, this will be used to define another property in a class,
        e.g., ::

            class Counter:
                count = MonitoredProperty[int]("count", default=0)
                on_count_change = count.callback_list

                def inc(self, delta: int = 0) -> None:
                    self.count += delta

        Then the defined property can be used::

            counter.on_count_change(lambda old, new: print(f"Changed from {old} to {new}")

        As this is the :class:`ChangeCallbackList` itself, other methods can
        also be used, e.g., ::

            counter.on_count_change(fn, key="my callback")
            counter.on_count_change.add(fn, key="my callback")
            counter.on_count_change.remove("my callback")
            counter.on_count_change.discard("my callback")
            counter.on_count_change.clear()

        The actual object returned by :attr:`callback_list` is a property object
        that can be extended (in the class, at least) to other similar
        properties using functions akin to :class:`ChangeCallbackList`'s
        :func:`~ChangeCallbackList.mapped` and
        :func:`~ChangeCallbackList.filtered`, e.g. ::

            class Counter:
                count = MonitoredProperty[int]("count", default=0)
                on_count_change = count.callback_list
                on_count_increase = on_count_change.filtered(lambda old, new: new > old)

        Here, a counter's ``on_count_increase`` is a :class:`ChangeCallbackList`
        whose callbacks are only invoked when a change is an increase.  As with
        ``on_count_change``, each object gets its own :class:`ChangeCallbackList`,
        and only gets one if somebody refers to it by trying to add a callback.
        """

        return _CCLProperty(self, "", lambda _: ChangeCallbackList[T]())

    @property
    def value_check(self) -> Gettable[object, bool]:
        """
        A property a property that returns ``True`` when an object doesn't have
        a value (including a default) value associated with this
        :class:`MonitoredProperty`.

        If there is no default value, the value starts out ``False``, becomes
        ``True`` the first time the :class:`MonitoredProperty` is set on an
        object, and becomes ``False`` again when the :class:`MonitoredProperty`
        is deleted on the object.  If there is a default value, it is always
        ``True``.
        """
        me = self
        class VC:
            def __get__(self, obj, objtype) -> bool: # @UnusedVariable
                val = me._lookup(obj)
                return val is not MISSING
        return VC()

    @property
    def getter(self) -> Gettable[object, T]:
        """
        A read-only property that returns the value associated with this
        :class:`MonitoredProperty` for an object or raises ``AttributeError`` if
        there is no such value.  This can be used to provide a read-only public
        property alongside a writable protected property, as in ::

            class Counter:
                _count = MonitoredProperty[int](default=0)
                on_count_change = _count.callback_list
                count = _count.getter

        With this in place, users of ``Counter`` can read ``count`` and register
        callbacks to ``on_count_change``, but modifications can only happen by
        means of ``_count``.
        """
        me = self
        class VC:
            def __get__(self, obj, objtype) -> T: # @UnusedVariable
                val = me._lookup(obj)
                if val is MISSING:
                    raise AttributeError(f"Attribute '{me.name}' not set in {obj}")
                return val
        return VC()

    @overload
    def transform(self, *,
                  chain: bool = False) -> Callable[[Callable[[Any, T], MissingOr[T]]], # @UnusedVariable
                                                   Callable[[Any, T], MissingOr[T]]]: ...
    @overload
    def transform(self, fn: Callable[[Any, T], MissingOr[T]], *, # @UnusedVariable
                  chain: bool = False) -> Callable[[Any, T], MissingOr[T]]: ... # @UnusedVariable
    def transform(self, fn: Optional[Callable[[Any, T], MissingOr[T]]] = None, *,
                  chain: bool = False) -> Union[Callable[[Any, T], MissingOr[T]],
                                                Callable[[Callable[[Any, T], MissingOr[T]]],
                                                         Callable[[Any, T], MissingOr[T]]]]:
        """
        A decorator that specifies that the decorated method should be called on
        the object, passing in the asserted value, e.g. ::

            class Counter:
                max_count = 100
                count = ManagedProperty[T]("count", default=0)

                @count.transform
                def clip(self, val: int) -> int:
                    return min(val, self.max_count)

        This will ensure that values greater than ``max_count`` will be clipped
        at that level, e.g. ::

            counter.count = 250
            print(counter.count)

        will print ``100``.

        If the function returns :attr:`MISSING`, the assignment is silently
        aborted.  For example, ::

            @count.transform
            def only_positive(self, val: int) -> MissingOr[in]:
                return val if val > 0 else MISSING

        Now ::

            counter.count = 2
            counter.count = -5
            print(counter.count)

        will print ``2``.

        If ``chain`` is ``True``, the function will be applied to the current
        transformation, unless it returns :attr:`MISSING`.  This is typically
        written calling :func:`transform` with **only** a ``chain`` parameter,
        which will return a decorator that finishes the job ::

            @count.transform
            def only_positive(self, val: int) -> MissingOr[in]:
                return val if val > 0 else MISSING

            @count.transform(chain = True)
            def clip(self, val: int) -> int:
                return min(val, self.max_count)

        Now, ``only_positive`` will be applied first.  If it passes the value,
        ``clip`` will be called to clip it to the maximum.

        Args:
            fn: the function used to check and/or transform a value on
                assignment.  If this is ``None``, the value will be a decorator
                that further applies to a function.  This is primarily seen when
                ``chain`` is present.
        Keyword Args:
            chain: if ``True``, the transformation will be applied to the result
                   of the current transformation.  If ``False``, it will replace
                   the current transformation.
        """
        def set_it(func: Callable[[Any, T], MissingOr[T]]) -> Callable[[Any, T], MissingOr[T]]:
            if chain:
                prior = self._transform
                this_func = func # Need a separate name to avoid infinite recursion.
                def chained_func(obj, val: T) -> MissingOr[T]:
                    pval = prior(obj, val)
                    return MISSING if pval is MISSING else this_func(obj, pval)
                func = chained_func
            self._transform = func
            return func
        if fn is None:
            return set_it
        else:
            return set_it(fn)

# Used in the case when a chemical is there, but its concentration
# cannot be computed.  Usually when two reagents specify the chemical,
# but with different concentration units
class UnknownConcentration:
    """
    Used in the case when a chemical is there but its concentration cannot be
    compute.  This usually occurs when two reagents specify the chemical, but
    they use different concentration units (e.g., :class:`.Molarity` and
    :class`.VolumeConcentration`).

    It is expected that the only instance of :class:`UnknownConcentration` will
    be the singleton constant :attr:`unknown_concentration`.

    Arithmetic on :class:`UnknownConcentration` does not change the value.
    """
    def __repr__(self) -> str:
        return "UnknownConcentration()"
    def __str__(self) -> str:
        return "unknown concentration"

    def __mul__(self, _: float) -> UnknownConcentration:
        return self

    def __plus_(self, _: UnknownConcentration) -> UnknownConcentration:
        return self

unknown_concentration: Final[UnknownConcentration] = UnknownConcentration()
"""
The constant singleton object of class :class:`UnknownConcentration`.
"""


Concentration = Union[Molarity, MassConcentration, VolumeConcentration, UnknownConcentration]
"""
Any of the many ways to describe the concentration of a chemical in a reagent.
"""


class Chemical:
    """
    A chemical that may exist as a component of a :class:`Reagent`.  It has a
    name and optionally a formula and a description, all strings.

    The class maintains a dictionary of instances keyed by name, so the
    encouraged way to obtain an object is to look it up using :func:`find`,
    which will create the :class:`Chemical` if one is not already there::

        c = Chemical.find("oxygen", formula="O2")

    ``name`` is final, but ``formula`` and ``description`` may be modified.
    """
    name: Final[str]            #: The name of the :class:`Chemical`
    formula: Optional[str]      #: The optional formula of the :class:`Chemical`
    description: Optional[str]  #: An optional description of the :class:`Chemical`

    known: ClassVar[dict[str, Chemical]] = {}
    """
    The known instances, keyed by name
    """

    def __init__(self, name: str, *,
                 formula: Optional[str] = None,
                 description: Optional[str] = None) -> None:
        """
        Initialize the object
        Args:
            name: the name of the :class:`Chemical`
        Keyword Args:
            formula: the optional formula of the :class:`Chemical`
            description: an optinal description of the :class:`Chemical`
        """
        self.name = name
        self.formula = formula
        self.description = description
        Chemical.known[name] = self

    @classmethod
    def find(cls, name: str, *,
             formula: Optional[str] = None,
             description: Optional[str] = None) -> Chemical:
        """
        Find a :class:`Chemical` with the given name, otherwise create one.  If
        a new :class:`Chemical` is created, it is added to ``known``.

        Note:
            If a :class:`Chemical` with the given name is already known, the
            formula and description will not be modified.

        Args:
            name: the name of the :class:`Chemical`
        Keyword Args:
            formula: the optional formula of the :class:`Chemical`
            description: an optinal description of the :class:`Chemical`
        Returns:
            the found or created :class:`Chemical`
        """
        c = cls.known.get(name, None)
        if c is None:
            c = Chemical(name, formula=formula, description=description)
        return c

    def __repr__(self) -> str:
        return f"Chemical[{self.name}]"

    def __str__(self) -> str:
        return self.name

ChemicalComposition = Mapping[Chemical, Concentration]
"""
A mapping from :class:`Chemical` to :class:`Concentration`
"""

class ProcessStep:
    """
    A processing step that a :class:`Reagent` can go through.

    The basic notion is that if ``r`` is a :class:`Reagent` and ``ps` is a
    :class:`ProcessStep`, after ::

        r2 = r.processed(ps)

    ``r2`` will be a different reagent with the property that
    ``r2.unprocessed()`` will be ``r`` (or, at least ``r.unprocessed()``) and
    ``r2.process_steps()`` will end with ``ps``.

    :class:`ProcessStep`\s can be obtained by calling :func:`find_or_create`,
    passing in a description::

        ps = ProcessStep.find_or_create("thermocycle")
    """
    description: Final[str]                     #: The description of the :class:`ProcessStep`
    _known: Final[dict[str, ProcessStep]] = {}  #: Known :class:`ProcessStep`\s keyed by description
    _class_lock: Final[Lock] = Lock()           #: The class lock.

    def __init__(self, description: str) -> None:
        """
        Initialize the object.

        Args:
            description: the description of the :class:`ProcessStep`
        """
        self.description = description

    def __repr__(self) -> str:
        return f"ProcessStep({repr(self.description)})"

    def __str__(self) -> str:
        return self.description

    # Note that this only works to find basic ProcessStep objects
    # created by this method. Those instantiated directly (including
    # by subclassing) will not be found.  Arguably, this is the correct
    # behavior.
    @classmethod
    def find_or_create(cls, description: str) -> ProcessStep:
        """
        Find or create a :class:`ProcessStep` with the given description.

        Note:
            This only works to find basic ProcessStep objects created by this
            method. Those instantiated directly (including by subclassing) will
            not be found.  Arguably, this is the correct behavior.
        Args:
            description: the description of the :class:`ProcessStep`
        Returns:
            the found or created :class:`ProcessStep`
        """
        with cls._class_lock:
            ps = cls._known.get(description, None)
            if ps is None:
                ps = ProcessStep(description)
                cls._known[description] = ps
            return ps

MixtureSpec = Tuple[tuple['Reagent', Fraction], ...]
"""
A description of :class:`Reagent` mixtures as a tuple of tuples of
:class:`Reagent` and :class:`Fraction`.

As used in :class:`Reagent`, the :class:`Reagent`\s will be unique, and the
overall tuple will be sorted by :class:`Reagent` name.
"""

class Reagent:
    """
    A reagent.  All :class:`Reagent`\s have

    * a :attr:`name`

    * a chemical :attr:`composition` (which will be an empty dict unless
      specified) as a mapping from :class:`Chemical` to :class:`Composition`

    * optional minimum (:attr:`min_storage_temp`) and maximum
      (:attr:`max_storage_temp`) storage temperatures

    * a :attr:`mixture` description, useful when a :class:`Reagent` is a not-
      otherwise-named mixture of two or more :class:`Reagent`\s

    * an indication of whether the :class:`Reagent` :attr:`is_pure` (i.e., not a
      mixture).

    * a tuple of :attr:`process_step` that the :class:`Reagent` has gone
      through.

    * the :attr:`unprocessed` :class:`Reagent` prior to any processing.  (Often
      this :class:`Reagent` itself.)

    :class:`Reagent`\s can be ordered, and sort by their :attr:`name`\s.
    """
    name: Final[str]                        #: The name of the :class:`Reagent`
    composition: ChemicalComposition
    """
    The composition of the :class:`Reagent`.  If this is empty, nothing is known
    about the composition.
    """
    min_storage_temp: Optional[TemperaturePoint] #: The (optional) minimum storage temperature of the :class:`Reagent`.
    max_storage_temp: Optional[TemperaturePoint] #: The (optional) maximum storage temperature of the :class:`Reagent`.
    _lock: Final[Lock] #: A local lock
    _process_results: Final[dict[ProcessStep, Reagent]]
    """
    A cache of the result of calling :func:`process` with different arguments.
    """

    known: ClassVar[dict[str, Reagent]] = dict[str, 'Reagent']()
    """
    A cache of known :class:`Reagent`\s, by name.
    """


    def __init__(self, name: str, *,
                 composition: Optional[ChemicalComposition] = None,
                 min_storage_temp: Optional[TemperaturePoint] = None,
                 max_storage_temp: Optional[TemperaturePoint] = None,
                 ) -> None:
        """
        Initialize the object.

        The new :class:`Reagent` will be pure (i.e., not a mixture) and will
        have no process steps.

        Args:
            name: the name of the :class:`Reagent`
        Keyword Args:
            composition: an optional composition as a mapping from
                         :class:`Chemical` to :class:`Concentration`
            min_storage_temp: an optional minimum storage temperature
            max_storage_temp: an optional maximum storage temperature
        """
        self.name = name
        self.composition = {} if composition is None else composition
        self.min_storage_temp = min_storage_temp
        self.max_storage_temp = max_storage_temp
        self._lock = Lock()
        self._process_results = {}
        Reagent.known[name] = self

    @classmethod
    def find(cls, name: str, *,
             composition: Optional[ChemicalComposition] = None,
             min_storage_temp: Optional[TemperaturePoint] = None,
             max_storage_temp: Optional[TemperaturePoint] = None) -> Reagent:
        """
        Find or create the :class:`Reagent` with a given name.

        Note:
            If an existing :class:`Reagent` with this name has previously been
            created, it will be returned and any specified ``composition``,
            ``min_storage_temp``, or ``max_storage_temp`` will be ignored.

        Args:
            name: the name of the :class:`Reagent`
        Keyword Args:
            composition: an optional composition as a mapping from
                         :class:`Chemical` to :class:`Concentration`
            min_storage_temp: an optional minimum storage temperature
            max_storage_temp: an optional maximum storage temperature
        Returns:
            the found or created :class:`Reagent`
        """
        c = cls.known.get(name, None)
        if c is None:
            c = Reagent(name, composition=composition,
                         min_storage_temp=min_storage_temp, max_storage_temp=max_storage_temp)
        return c

    @property
    def mixture(self) -> MixtureSpec:
        """
        A description of the :class:`Reagent` as a mixture of other
        :class:`Reagent`\s.  The description is a tuple of tuples, each of which
        contains a :class:`Reagent` and a :class:`Fraction` specifying how much
        of the overall mixture that :class:`Reagent` constitutes.

        The elements of this tuple will be sorted by :class:`Reagent` name,
        rendering the whole thing useful as a mapping key.

        This :class:`Reagent` :func:`is_pure` if and only if the the resulting
        tuple has one element, and the first element of that element will be
        this :class:`Reagent`.

        The second elements of each element of this tuple (:class:`Fraction`\s)
        will all add up to ``1``.
        """
        return ((self, Fraction.from_float(1)),)

    @property
    def is_pure(self) -> bool:
        """
        Is the :class:`Reagent` not a mixture?  ``True`` iff :func:`mixture` has
        exactly one element.
        """
        return len(self.mixture) == 1

    @property
    def process_steps(self) -> tuple[ProcessStep, ...]:
        """
        The :class:`ProcessStep`\s this :class:`Reagent` has gone through.
        """
        return ()

    @property
    def unprocessed(self) -> Reagent:
        """
        The unprocessed version of this :class:`Reagent`.
        """
        return self

    def liquid(self, volume: Volume, *, inexact: bool = False) -> Liquid:
        """
        A :class:`Liquid` containing a specified :class:`.Volume` of this
        :class:`Reagent`

        Args:
            volume: the volume of the resulting liquid
        Keyword Args:
            inexact: whether the volume is inexact
        Returns:
            a new :class:`Liquid`
        """
        return Liquid(self, volume, inexact=inexact)

    def __repr__(self) -> str:
        return f"Reagent({repr(self.name)})"

    def __str__(self) -> str:
        if self.process_steps:
            return f"{self.name}[{', '.join(str(ps) for ps in self.process_steps)}]"
        return self.name

    def __lt__(self, other: Reagent) -> bool:
        return self.name < other.name

    @staticmethod
    def SameComposition(composition: ChemicalComposition) -> ChemicalComposition:
        """
        A composition-altering function that doesn't change the composition.

        This function suitable for use as the ``new_omposition_function``
        argument to :func:`processed` when the :class:`ProcessStep` does not
        change the chemical composition.

        Args:
            composition: the old composition
        Returns:
            ``composition`` unchanged.
        """
        return composition

    @staticmethod
    def LoseComposition(composition: ChemicalComposition) -> ChemicalComposition:  # @UnusedVariable
        """
        A composition-altering function that returns an unknown composition.

        This function suitable for use as the ``new_omposition_function``
        argument to :func:`processed` when the :class:`ProcessStep` has an
        unknown effect on the chemical composition.

        Args:
            composition: the old composition
        Returns:
            an unknown composition (e.g., ``{}``)
        """
        return {}


    def processed(self, step: Union[str, ProcessStep],
                  new_composition_function: Optional[Callable[[ChemicalComposition], ChemicalComposition]] = None,
                  *,
                  min_storage_temp: Optional[TemperaturePoint] = None,
                  max_storage_temp: Optional[TemperaturePoint] = None) -> Reagent:
        """
        A new version of the :class:`Reagent` after it has been processed.

        If this :class:`Reagent` is the :attr:`waste_reagent`, it is returned
        unchanged.

        The results of calling :func:`processed` on a given :class:`Reagent` are
        cached, and an existing value will be reused.

        If a new one is created, the composition and minimum and maximum storage
        temperatures are modified as specified by the parameters or, if
        unspecified, copied from this :class:`Reagent`.

        Note:
            If a cached result of a prior call to :func:`processed` with this
            ``step`` is found, it will be returned, and the other arguments will
            be ignored.

        Args:
            step: the :class:`ProcessStep` applied or the name used to find or
                  create it.

            new_composition_function: an optional function to determine the new
                                      composition.
        Keyword Args:
            min_storage_temp: an optional minimum storage temperature
            max_storage_temp: an optional maximum storage temperature
        Returns:
            the resulting :class:`Reagent`
        """
        if self is waste_reagent:
            return self
        if isinstance(step, str):
            step = ProcessStep.find_or_create(step)
        with self._lock:
            r = self._process_results.get(step, None)
            if r is None:
                if new_composition_function is None:
                    new_composition_function = Reagent.SameComposition
                new_c = new_composition_function(self.composition)
                r = ProcessedReagent(self, step,
                                     composition = new_c,
                                     min_storage_temp = min_storage_temp or self.min_storage_temp,
                                     max_storage_temp = max_storage_temp or self.max_storage_temp)
                self._process_results[step] = r
            return r



waste_reagent: Final[Reagent] = Reagent.find("waste")
"""
The waste :class:`Reagent`.

If the :attr:`waste_reagent` goes through a :class:`ProcessStep` or is mixed with
another :class:`Reagent`, the result will be the :attr:`waste_reagent`.
"""
unknown_reagent: Final[Reagent] = Reagent.find("unknown")
"""
An unknown :class:`Reagent.

This :class:`Reagent` is typically used for zero-volume :class:`Liquid`\s and
the contents of empty wells, but it is also reasonable to use in contexts in
which the actual :class:`Reagent` is unknown or unimportant.
"""

MixResult = Union[Reagent, str]
"""
The specification of the result of a mixing operation.  Either a
:class:`Reagent` or the name of one.
"""

class Mixture(Reagent):
    """
    A :class:`Reagent` that is a mixture of two or more other :class:`Reagent`\s

    :class:`Mixture` objects are not typically created directly.  If one is
    needed as a :class:`Reagent`, you can use :func:`find_or_compute` which
    computes (or finds a cached version of) a mixture between to
    :class:`Reagent`\s.  More commonly, :class:`Mixture` objects will be created
    as a consequence of mixing together two :class:`Liquid` objects using
    :func:`Liquid.mix_with`, :func:`Liquid.mix_in`, or
    :func:`Liquid.mix_together`.

    When created using one of the aforementioned methods, if the name of the
    resulting :class:`Mixture` is not specified a name describing the relative
    proportions of the constituents will be constructed.  For example, after ::

        r3 = Mixture.find_or_compute(r1, r2, ratio = 0.4)

    the name of ``r3`` will be ``"2 r1 + 5 r2"``
    """
    _mixture: Final[MixtureSpec]        #: The mixture specification
    _class_lock: Final[Lock] = Lock()   #: A class lock for managing caches
    _known_mixtures: Final[dict[tuple[float,Reagent,Reagent], Reagent]] = {}
    "Cached results of calling :func:find_or_compute`"
    _instances: Final[dict[MixtureSpec, Mixture]] = {}
    "Cached results of calling :func:`new_mixture`"

    def __init__(self, name: str, mixture: MixtureSpec, *,
                 composition: Optional[ChemicalComposition] = None,
                 min_storage_temp: Optional[TemperaturePoint] = None,
                 max_storage_temp: Optional[TemperaturePoint] = None,
                 ) -> None:
        """
        Initialize the object.

        Args:
            name: the name of the :class:`Reagent`
            mixture: the :class:`MixtureSpec` describing the mixture
        Keyword Args:
            composition: an optional composition as a mapping from
                         :class:`Chemical` to :class:`Concentration`
            min_storage_temp: an optional minimum storage temperature
            max_storage_temp: an optional maximum storage temperature
        """
        super().__init__(name, composition=composition, min_storage_temp=min_storage_temp, max_storage_temp=max_storage_temp)
        self._mixture = mixture

    @property
    def mixture(self) -> MixtureSpec:
        return self._mixture

    def __repr__(self) -> str:
        return f"Mixture({repr(self.name), repr(self._mixture)})"


    @classmethod
    def new_mixture(cls, r1: Reagent, r2: Reagent, ratio: float, name: Optional[str] = None) -> Reagent:
        """
        A mixture of two :class:`Reagent`\s in a given ratio.

        The :attr:`composition` of the resulting :class:`Reagent` will be
        computed based on the same ratio of the compositions of ``r1`` and
        ``r2``.

        If ``name`` is not provided, a name describing the relative proportions
        of the constituents will be constructed.  For example, after ::

            r3 = Mixture.find_or_compute(r1, r2, ratio = 0.4)

        the name of ``r3`` will be ``"2 r1 + 5 r2"``


        Important:
            :func:`find_or_compute` is more efficient than :func:`new_mixture`
            and is the method that should be used.  (:func:`find_or_compute`
            uses :func:`new_mixture` internally if necessary.)  This is because
            in addition to caching results based on the constructed
            :class:`MixtureSpec`, :func:`find_or_compute` caches them based on
            the arguments, so if the same :class:`Reagent`\s are mixed
            repeatedly in the same proportions, the results will be found
            without having to compute the :class:`MixtureSpec`.

        Note:
            A ratio of ``n`` means ``n`` parts ``r1`` to one part ``r2``.  This
            means that a ratio of ``1`` means equal parts, and a ratio of, e.g.,
            ``0.4`` means two parts ``r1`` to five parts ``r2``.

        Note:
            The name of the method notwithstanding, the results of calling
            :func:`new_mixture` are cached, and if the same resulting
            :class:`MixtureSpec` is discovered, the prior result will be
            returned.  When mixtures are further mixed, this can happen even if
            a different path is taken
        Args:
            r1: the first :class:`Reagent`
            r2: the second :class:`Reagent`
        Keyword Args:
            ratio: the ratio of ``r1`` to ``r2``
            name: an optional name of the result.
        Returns:
            The mixture as a :class:`Reagent`
        """
        fraction = ratio/(ratio+1)
        # as_frac = Fraction.from_float(fraction)
        as_frac = farey(fraction)
        # print(f"fraction: {as_frac}")
        mixture = {r: f*as_frac for r,f in r1.mixture}
        composition = {chem: conc*fraction for chem, conc in r1.composition.items()}
        fraction = 1-fraction
        # as_frac = Fraction.from_float(fraction)
        as_frac = farey(fraction)
        for r,f in r2.mixture:
            cpt = f*as_frac
            f1 = mixture.get(r, None)
            mixture[r] = cpt if f1 is None else cpt+f1
        for chem, conc in r2.composition.items():
            r2_conc = conc*fraction
            r1_conc = composition.get(chem, None)
            if r1_conc is None:
                r_conc: Concentration = r2_conc
            elif isinstance(r1_conc, Molarity) and isinstance(r2_conc, Molarity):
                r_conc = r1_conc+r2_conc
            elif isinstance(r1_conc, MassConcentration) and isinstance(r2_conc, MassConcentration):
                r_conc = r1_conc+r2_conc
            elif isinstance(r1_conc, VolumeConcentration) and isinstance(r2_conc, VolumeConcentration):
                r_conc = r1_conc+r2_conc
            else:
                r_conc = unknown_concentration
            composition[chem] = r_conc

        # print(f"{mixture}")
        seq = sorted(mixture.items())
        t = tuple(seq)
        m = cls._instances.get(t, None)
        if m is None:
            if name is None:
                max_denom = 10000
                lcm = min(math.lcm(*(f.denominator for _,f in seq)), max_denom)
                def portion(f: Fraction) -> int:
                    return round(float(f)*lcm)
                mapped = tuple((r, portion(f)) for r,f in seq)
                name = ' + '.join(f"{p:,} {r.name}" for r,p in mapped)
            m = Mixture(name, t, composition=composition)
            # print(f"{ratio} {r1} x {r2} is")
            # print(f"{m}")
            cls._instances[t] = m
        return m

    # @classmethod
    # def find_or_compute_aux(cls, specs: tuple[tuple[float, Reagent]], *,
    #                         name: Optional[str] = None) -> Reagent:
    #     # TODO:
    #     # Note, need to normalize before lookup?
    #     ...

    @classmethod
    def find_or_compute(cls, r1: Reagent, r2: Reagent, *,
                        ratio: float = 1,
                        name: Optional[str] = None) -> Reagent:
        """
        A mixture of two :class:`Reagent`\s in a given ratio.

        The :attr:`composition` of the resulting :class:`Reagent` will be
        computed based on the same ratio of the compositions of ``r1`` and
        ``r2``.

        If ``name`` is not provided, a name describing the relative proportions
        of the constituents will be constructed.  For example, after ::

            r3 = Mixture.find_or_compute(r1, r2, ratio = 0.4)

        the name of ``r3`` will be ``"2 r1 + 5 r2"``

        Important:
            :func:`find_or_compute` is more efficient than :func:`new_mixture`
            and is the method that should be used.  (:func:`find_or_compute`
            uses :func:`new_mixture` internally if necessary.)  This is because
            in addition to caching results based on the constructed
            :class:`MixtureSpec`, :func:`find_or_compute` caches them based on
            the arguments, so if the same :class:`Reagent`\s are mixed
            repeatedly in the same proportions, the results will be found
            without having to compute the :class:`MixtureSpec`.

        Note:
            A ratio of ``n`` means ``n`` parts ``r1`` to one part ``r2``.  This
            means that a ratio of ``1`` means equal parts, and a ratio of, e.g.,
            ``0.4`` means two parts ``r1`` to five parts ``r2``.

        Note:
            The results of calling :func:`find_or_compute` are cached, and if the
            same resulting :class:`MixtureSpec` is discovered, the prior result
            will be returned.  When mixtures are further mixed, this can happen
            even if a different path is taken
        Args:
            r1: the first :class:`Reagent`
            r2: the second :class:`Reagent`
        Keyword Args:
            ratio: the ratio of ``r1`` to ``r2``
            name: an optional name of the result.
        Returns:
            The mixture as a :class:`Reagent`
        """
        if r1 is r2:
            return r1
        if r1 is waste_reagent or r2 is waste_reagent:
            return waste_reagent
        known = cls._known_mixtures
        with cls._class_lock:
            r = known.get((ratio, r1, r2), None)
            if r is not None:
                return r
            r = known.get((1/ratio, r2, r1))
            if r is not None:
                return r
            r = cls.new_mixture(r1, r2, ratio, name=name)
            known[(ratio, r1, r2)] = r
        return r

class ProcessedReagent(Reagent):
    """
    The :class:`Reagent` resulting from calling :func:`process`
    """
    last_step: Final[ProcessStep] #: The last :class:`ProcessStep` used to create this :class:`Reagent`
    prior: Final[Reagent]         #: The :class:`Reagent` prior to :attr:`last_step`

    def __init__(self, prior: Reagent, step: ProcessStep, *,
                 composition: Optional[ChemicalComposition] = None,
                 min_storage_temp: Optional[TemperaturePoint] = None,
                 max_storage_temp: Optional[TemperaturePoint] = None,
                 ) -> None:
        super().__init__(prior.name, composition=composition, min_storage_temp=min_storage_temp, max_storage_temp=max_storage_temp)
        self.prior = prior
        self.last_step = step

    @property
    def process_steps(self)->tuple[ProcessStep, ...]:
        return self.prior.process_steps+(self.last_step,)

    @property
    def unprocessed(self)->Reagent:
        return self.prior.unprocessed

    def __repr__(self) -> str:
        return f"ProcessedReagent({repr(self.prior), repr(self.last_step)})"



class Liquid:
    """
    A quantity of a :class:`Reagent`.  Both the :attr:`volume` and the
    :attr:`reagent` can change over time, and so differnt :class:`Liquid`\s may
    have the same state, but each will retain its own identity.

    Callbacks can be registered for both :attr:`volume` and :attr:`reagent` by
    using the :class:`ChangeCallbackList`\s :attr:`on_volume_change` and
    :attr:`on_reagent_change`::

        liq.on_reagent_change(note_reagent_change, key=nrc_key)
        liq.on_volume_change(note_volume_change)

    In addition to :attr:`volume`, a :class:`Liquid` also has an indication of
    whether the :attr:`volume` is :attr:`inexact`.  Typically, this will be
    ``False``, but if it is ``True``, it is not safe to assume that, e.g.,
    incrementally removing volume will necessarily have removed all of it.

    As a convenience, a :class:`.Volume` can be added to or subtracted from a
    :class:`Liquid`, e.g. ::

        liq -= 2*uL

    The resulting :class:`.Volume` is clipped at zero.

    :class:`Liquid`\s can be mixed together in several ways:

    * :func:`mix_with` returns the result of mixing a given :class:`Liquid` with
      another.  Neither :class:`Liquid` is modified.

    * :func:`mix_in` modifies a given :class:`Liquid` by setting it to the
      result of mixing in another.  The other :class:`Liquid` gets the
      :attr:`reagent` of the mixture, but its :attr:`volume` is set to zero.

    * :func:`Liquid.mix_together` returns the result of mixing together several
    :class:`Liquid`\s (or parts of them).  None are modified.

    For all of these, the resulting :class:`Reagent` will be proportional to the
    volumes.  For example, after ::

        liq1 = r1.liquid(1*mL)
        liq2 = r2.liquid(2*mL)
        r1.mix_in(r2)

    ``r1.volume`` will be ``3*mL`` and ``r1.reagent`` will print as ``1 r1 + 2
    r2``.  (``r2`` will have the same reagent, but its volume will be zero.)

    The mixing methods all take an optional ``result`` parameter, which is
    either a :class:`Reagent` or a string.  If it is a :class:`Reagent`, it will
    be used as the reagent for the mixture.  If it is a string, it will be used
    as the name for the resulting (computed) mixture unless either the reagents
    of the two liquids are the same (in which case the mixture has the same
    reagent) or one of them is the :attr:`waste_reagent` (in which case the
    mixture will be, as well).

    To split the contents of a :class:`Liquid` into two parts, use
    :func:`split_to`.  As this overwrites the content of the other
    :class:`Liquid`, it should only be used when the other is known to be empty.
    It is particularly useful when doing a "merge and split", as ::

        liq1.mix_in(liq2)
        liq1.split_to(liq2)

    After this sequence, both :class:`Liquid`\s will have the same (mixed)
    reagent and a volume that is the average of the two original volumes.



    """
    inexact: bool       #: Is :attr:`volume` inexact?

    volume: MonitoredProperty[Volume] = MonitoredProperty()
    """
    The :class:`.Volume` of the :class:`Liquid`.  In some cases, this should
    be interpreted in conjunction with :attr:`inexact`.

    Setting :attr:`volume` to a :class:`.Volume` different from the previous
    value will trigger the callbacks in :attr:`volume_change_callbacks`
    """

    on_volume_change: ChangeCallbackList[Volume] = volume.callback_list
    "The :class:`ChangeCallbackList` monitoring :attr:`volume`"

    reagent: MonitoredProperty[Reagent] = MonitoredProperty()
    """
    The :class:`Reagent` of the :class:`Liquid`.

    Setting :attr:`reagent` to a :class:`.Reagent` different from the previous
    value will trigger the callbacks in :attr:`reagent_change_callbacks` only if
    the new value is not the same as the old value.
    """

    on_reagent_change: ChangeCallbackList[Reagent] = reagent.callback_list
    "The :class:`ChangeCallbackList` monitoring :attr:`reagent`"

    def __init__(self, reagent: Reagent, volume: Volume, *, inexact: bool = False) -> None:
        """
        Initialize the object.

        Args:
            reagent: the :class:`Reagent` of the :class:`Liquid`
            volume: the :class:`.Volume` of the :class:`Liquid`
        Keyword Args:
            inexact: is ``volume`` inexact?
        """
        self.reagent = reagent
        self.volume = volume
        self.inexact = inexact

    def __repr__(self) -> str:
        return f"Liquid[{'~' if self.inexact else ''}{self.volume.in_units(uL)}, {self.reagent}]"

    def __str__(self) -> str:
        return f"{'~' if self.inexact else ''}{self.volume.in_units(uL):g} of {self.reagent}"

    def __iadd__(self, rhs: Volume) -> Liquid:
        self.volume = min(self.volume+rhs, Volume.ZERO)
        return self

    def __isub__(self, rhs: Volume) -> Liquid:
        self.volume = max(self.volume-rhs, Volume.ZERO)
        return self

    def mix_with(self, other: Liquid, *, result: Optional[MixResult] = None) -> Liquid:
        """
        A new :class:`Liquid` that is the result of mixing this :class:`Liquid`
        with another.

        The :attr:`volume` of the result is the sum of the volumes of the two
        :class:`Liquids`.  The :attr:`reagent` of the result is

        * ``result`` if this is a :class:`Reagent`
        * :attr:`reagent` if this is the same for both :class:`Liquid`\s
        * :attr:`waste_reagent`, if the :attr:`reagent` for either :class:`Liquid`
          is :attr:`waste_reagent`
        * the result of calling :func:`Mixture.find_or_compute`, passing in
          ``result`` (which is either a string or ``None``) as the ``name``
          parameter.

        The resulting :class:`Liquid` is :attr:`inexact` if either
        :class:`Liquid` is.

        Note:

            Neither :class:`Liquid` is modified.  To modify this :class:`Liquid`
            to be the result of the mixture (and clear the other), use
            :func:`mix_in`.

        Args:
            other:  the :class:`Liquid` to mix with
        Keyword Args:
            result: the resulting :class:`Reagent`, the name of the computed
                    :class:`Reagent`, or ``None`` (indicating that the name
                    should be computed)
        Returns:
            a new :class:`Liquid` with the resulting :class:`Reagent` and :class:`.Volume`.
        """
        my_v = self.volume
        my_r = self.reagent
        their_v = other.volume
        their_r = other.reagent

        v = my_v + their_v
        if isinstance(result, Reagent):
            r = result
        elif my_r is their_r:
            r = my_r
        elif my_r is waste_reagent or their_r is waste_reagent:
            r = waste_reagent if result is None else Reagent.find(result)
        else:
            ratio = my_v.ratio(their_v)
            r = Mixture.find_or_compute(my_r, their_r, ratio=ratio, name=result)
        return Liquid(reagent=r, volume=v, inexact=self.inexact or other.inexact)

    def mix_in(self, other: Liquid, *, result: Optional[MixResult] = None) -> None:
        """
        Modify this :class:`Liquid` to be the result of mixing it with another.

        The :attr:`volume` of the result is the sum of the volumes of the two
        :class:`Liquids`.  The :attr:`reagent` of the result is

        * ``result`` if this is a :class:`Reagent`
        * :attr:`reagent` if this is the same for both :class:`Liquid`\s
        * :attr:`waste_reagent`, if the :attr:`reagent` for either :class:`Liquid`
          is :attr:`waste_reagent`
        * the result of calling :func:`Mixture.find_or_compute`, passing in
          ``result`` (which is either a string or ``None``) as the ``name``
          parameter.

        The resulting :class:`Liquid` is :attr:`inexact` if either
        :class:`Liquid` is.

        After the operation, ``other`` will have the same :attr:`reagent` as
        this :class:`Liquid`, but its :attr:`volume` will be zero and it will
        not be :attr:`inexact`.

        Note:

            This method modifies both :class:`Liquid`\s.  To simply compute the
            result of such mixing and return it as a new :class:`Liquid` without
            modifying either, use :func:`mix_with`.

        Args:
            other:  the :class:`Liquid` to mix in
        Keyword Args:
            result: the resulting :class:`Reagent`, the name of the computed
                    :class:`Reagent`, or ``None`` (indicating that the name
                    should be computed)
        """
        my_v = self.volume
        my_r = self.reagent
        their_v = other.volume
        their_r = other.reagent

        v = my_v + their_v
        if isinstance(result, Reagent):
            r = result
        elif my_r is their_r or their_v == Volume.ZERO:
            r = my_r
        elif my_r is waste_reagent or their_r is waste_reagent:
            r = waste_reagent if result is None else Reagent.find(result)
        elif my_v == Volume.ZERO:
            r = their_r
        else:
            ratio = my_v.ratio(their_v)
            r = Mixture.find_or_compute(my_r, their_r, ratio=ratio, name=result)
        self.reagent = r
        self.inexact = self.inexact or other.inexact
        self.volume = v
        other.reagent = r
        other.inexact = False
        other.volume = Volume.ZERO

    def split_to(self, other: Liquid) -> None:
        """
        Split this :class:`Liquid` such that half of its :attr:`volume` is transfered to ``other``.

        Note:
            The incoming values of :attr:`reagent`, :attr:`volume`, and
            :attr:`inexact` are overwritten.  This method is designed to be used
            following :func:`mix_in`, which clears its argument :class:`Liquid`.

        Args:
            other: the :class:`Liquid` to mix in
        """

        other.reagent = self.reagent
        other.inexact = self.inexact
        v = self.volume/2
        self.volume = v
        other.volume = v

    def processed(self, step: Union[str, ProcessStep],
                  new_composition_function: Optional[Callable[[ChemicalComposition], ChemicalComposition]] = None) -> Liquid:
        """
        Alter this :attr:`reagent` to note a :class:`ProcessStep`.

        Args:
            step: the :class:`ProcessStep` applied or the name used to find or
                  create it.

            new_composition_function: an optional function to determine the new
                                      composition.
        Returns:
            this :class:`Liquid`
        See Also:
            :func:`Reagent.processed`
        """
        self.reagent = self.reagent.processed(step, new_composition_function)
        return self

    @classmethod
    def mix_together(cls, liquids: Sequence[Union[Liquid, tuple[Liquid, float]]], *,
                     result: Optional[MixResult] = None) -> Liquid:
        """
        A new :class:`Liquid` that is the result of mixing several :class:`Liquid`\s
        together.

        The ``liquids`` parameter specifies not only the :class:`Liquid`\s to
        use, but also the portion of the volume each to use.  (The default, if
        just the :class:`Liquid` is specified, is ``1``, repesenting that the
        whole volume is to be used.  This is useful when a given :class:`Liquid`
        is participating in more than one mixture at the same time.  By
        providing, e.g., ``0.5`` as the second element for each call to
        :func:`mix_together`, half the volume will be used in each.

        The :attr:`volume` of the result is the sum of the volumes used for each
        element of ``liquids``. The :attr:`reagent` of the result is

        * ``result``, if this is a :class:`Reagent`
        * the common :attr:`reagent`, if all :class:`Liquid`\s have the same
          :attr:`reagent`,
        * :attr:`waste_reagent`, if the :attr:`reagent` for any :class:`Liquid`
          is :attr:`waste_reagent`
        * the result of calling :func:`Mixture.find_or_compute`, passing in
          ``result`` (which is either a string or ``None``) as the ``name``
          parameter.

        The resulting :class:`Liquid` is :attr:`inexact` if any
        :class:`Liquid` is.

        This method does not modify any member of ``liquids``.

        If ``liquids`` is empty, the result will be a new :class:`Liquid` whose
        :attr:`reagent` is the :attr:`unknown_reagent` and whose :attr:`volume`
        is zero.

        Args:
            liquids:  the :class:`Liquid`\s to mix together.  These may be
                      specified alone or paired with a number indicating the
                      portion of the :class:`Liquid` to use
        Keyword Args:
            result: the resulting :class:`Reagent`, the name of the computed
                    :class:`Reagent`, or ``None`` (indicating that the name
                    should be computed)
        Returns:
            a new :class:`Liquid` with the resulting :class:`Reagent` and :class:`.Volume`.
        """
        if len(liquids) == 0:
            return Liquid(unknown_reagent, Volume.ZERO)
        ls = [(liquid, 1) if isinstance(liquid, Liquid) else liquid for liquid in liquids]
        first, first_frac = ls[0]
        v = first.volume*first_frac
        r = first.reagent
        last = len(ls)-2
        inexact = first.inexact
        for i, (liquid, frac) in enumerate(ls[1:]):
            v2 = liquid.volume * frac
            if v2 == Volume.ZERO:
                continue
            r2 = liquid.reagent
            if liquid.inexact:
                inexact = True
            if i == last and isinstance(result, Reagent):
                r = result
            elif r is r2:
                pass
            elif r is waste_reagent or r2 is waste_reagent:
                r = waste_reagent
            else:
                ratio = v.ratio(v2)
                result_name = result if i == last else None
                assert(not isinstance(result_name, Reagent))
                r = Mixture.find_or_compute(r, r2, ratio=ratio, name=result_name)
            v = v+v2
        return Liquid(r, v, inexact=inexact)

ColorSpec = Union[str, tuple[float,float,float], tuple[float,float,float,float]]
"""
A value that can be used to identify a :class:`Color`
"""
class Color:
    """
    A color.  The mapping of names to RGBA tuples is taken from `matplotlib`.

    :class:`Color`\s are found by calling :func:`find`, passing in either a name
    or an RGB(A) tuple.  The values are cached, so subsequent calls to
    :func:`find` with the same argument will reasult in the same :class:`Color`.
    """
    description: Final[str]  #: The description of the :class:`Color`
    rgba: Final[tuple[float,float,float,float]]
    """
    A tuple of red, blue, green, and alpha components of the :class:`Color`.
    """

    _class_lock: Final[Lock] = Lock()       #: A class lock over the cache
    _known: Final[dict[str, Color]] = {}    #: The cache of known :class:`Color`\s

    def __init__(self, description: str, rgba: tuple[float,float,float,float]) -> None:
        """
        Initialize the object

        Args:
            description: the description
            rgba: a tuple of red, green, blue, and alpha components.
        """
        self.description = description
        self.rgba = rgba

    @classmethod
    def find(cls, description: ColorSpec) -> Color:
        """
        Find (or create) the :class:`Color` with the given name or RGB(A)
        components.  If a string is given as the ``description``, the RGBA
        components are looked up via `matplotlib`.  Otherwise, ``description``
        should be a touple of three (RGB) or four (RGBA) numbers from ``0.0`` to
        ``1.0`` inclusive, and the :attr:`description` of the resulting
        :class:`Color` will be the result of formatting ``description``.

        Args:
            description: the description of the :class:`Color`.
        """
        key = str(description)
        with cls._class_lock:
            c = cls._known.get(key, None)
            if c is None:
                from matplotlib import colors
                c = Color(key, colors.to_rgba(description))
            cls._known[key] = c
            return c

    def __repr__(self) -> str:
        return f"Color({repr(self.description)}, {repr(self.rgba)})"

    def __str__(self) -> str:
        return self.description

class ColorAllocator(Generic[H]):
    """
    An allocator associating :class:`Color` objects with elments of some
    :class:`Hashable` type :attr:`H`.

    The basic idea is that you call :func:`get_color` to obtain a :class:`Color`
    to use to represent an element.  For example, if ``alloc`` is a
    :class:`ColorAllocator`\[:class:`Reagent`] and ``r`` is a :class:`Reagent`, then ::

        c = alloc.get_color(r)

    will obtain a :class:`Color` for ``r``.  If called again with the same
    argument, the same :class:`Color` will be returned.  To reserve a specific
    :class:`Color` for an object, use :func:`reserve_color`::

        alloc.reserve_color(waste_reagent, "black")

    The ``color`` argument to :func:`reserve_color` may be a :class:`Color` or
    anything usable as the argument to :func:`Color.find` (e.g., a string or
    tuple of floats).

    By default, :func:`get_color` will allocate :class:`Color`\s from
    :func:`ColorAllocator.default_color_list()`, which is an array of 954 common
    colors that can be found at https://xkcd.com/color/rgb/.  To use a different
    list (or a permutation of this list), specify the ``all_colors`` parameter
    when constructing the :class:`ColorAllocator`.

    Internally, the class uses a :class:`WeakKeyDictionary` to manage the
    associations, so it does not hold onto the objects for which
    :class:`Color`\s have been allocated, and when one gets garbage collected,
    the associated :class:`Color` may become available to be associated with a
    new object.  If a color is associated with more than one object (via
    :func:`reserve_color`), it does not become available until all such
    associations have been dropped.

    The colors are allocated in order, skipping any that have been reserved.
    Only when the list has been exhausted will colors that had been previously
    allocated for no-longer-extant objects be reused.  If all colors are
    associated with objects, :class:`IndexError` will be raised.

    To remove any :class:`Color` association for an object, use
    :func:`release_color_for`.  This will render the :class:`Color` (if any)
    available for future calls to :func:`get_color`.  Note that
    :func:`release_color` for can safely be called even if its argument was
    never used in a call to :func:`get_color`.

    Warning:
        Internally, the mapping from objects to :class:`Color`\s is kept in a
        :class:`WeakKeyDictionary`.  A consequence of this is that if :class:`H`
        defines equality as different from identity, non-identical equal objects
        will get the same :class:`Color`, but when the first such object gets
        garbage collected, the association will be removed from the table and
        any subsequent ones will not find a match and so will get allocated a
        new color.

    Args:
        H: The :class:`Hashable` type to associate :class:`Color`\s with.
    """
    _default_color_list: ClassVar[Optional[Sequence[str]]] = None

    all_colors: Final[Sequence[str]]
    "The colors accessible to :func:`get_color`"
    color_assignments: WeakKeyDictionary[H, tuple[Color, finalize]]
    "A weak key mapping from key to :class:`Color`"
    colors_in_use: Final[dict[Color, int]]
    "The count of objects using in-use :class:`Color`\s"
    returned_colors: Final[deque[Color]]
    "Previously-allocated :class:`Color` objects that have become available"
    next_reagent_color: int
    "The index of the next :class:`Color` to allocate in :attr:`all_colors`"
    _lock: Final[RLock]                 ; "A local lock for managing tables"
    _class_lock: Final[Lock] = Lock()   ; "A class lock for manageing :attr:`_default_color_list`"

    def __init__(self, *,
                 initial_reservations: Optional[Mapping[H, Union[Color,ColorSpec]]] = None,
                 all_colors: Optional[Sequence[str]] = None):
        """
        Initialize the object.

        The values of ``initial_reservation`` may be anything acceptable to
        :func:`reserve_color`.

        If ``all_colors`` is ``None``, :func:`default_color_list` will be used.

        Keyword Args:
            initial_reservations: initial :class:`Color` reservations
            all_colors: an optional list of :class:`Color`\s for :func:`get_color` to use.
        """
        self.color_assignments = WeakKeyDictionary()
        self.colors_in_use = {}
        self.returned_colors = deque[Color]()
        self.next_reagent_color = 0
        self._lock = RLock()
        if initial_reservations is not None:
            for k,c in initial_reservations.items():
                self.reserve_color(k, c)

        if all_colors is None:
            all_colors = self.default_color_list()
        self.all_colors = all_colors

    @classmethod
    def default_color_list(cls) -> Sequence[str]:
        """
        The default list of :class:`Color`\s to use.  This list is not created
        until it is needed.

        The current list is an array of 954 common colors that can be found at
        https://xkcd.com/color/rgb/.
        """
        all_colors = cls._default_color_list
        if all_colors is None:
            with cls._class_lock:
                all_colors = cls._default_color_list
                if all_colors is None:
                    all_colors = [k for k in XKCD_COLORS]
                    cls._default_color_list = all_colors
        return all_colors

    def _lose_mapping(self, color: Color) -> None:
        """
        Note that an association has been lost with a :class:`Color`.  If this
        is the last such association for the :class:`Color`, add it to
        :attr:`returned_colors`.

        Note:
            The method assumes that :attr:`_lock` is locked.

        Args:
            color: the :class:`Color` for which the association has been lost
        """
        uses = self.colors_in_use[color]
        if uses > 1:
            self.colors_in_use[color] = uses-1
        else:
            del self.colors_in_use[color]
            self.returned_colors.append(color)

    @staticmethod
    def _lose_mapping_on_gc(color: Color, selfref: ReferenceType[ColorAllocator]) -> None:
        """
        Handle GC of key object.  If the :class:`ColorAllocator` is still
        around, call :func:`_lose_mapping`.

        Args:
            color: the :class:`Color` associated with the lost key
            selfref: a weak reference to the :class:`ColorAllocator`
        """
        self = selfref()
        if self is not None:
            with self._lock:
                self._lose_mapping(color)

    def reserve_color(self, key: H,
                      color: Union[Color, ColorSpec]) -> None:
        """
        Associate a :class:`Color` with an object.  This renders the
        :class:`Color` unavailable to :func:`get_color`.

        ``color`` may be either a :class:`Color` or a :class:`ColorSpec`, i.e.,
        anything acceptable to :func:`Color.find`.  In particular, it may be a
        string or a 3- or 4-elment tuple of floats.

        If there was already a reservation for ``key``, this one replaces it,
        and subsequent calls to :func:`get_color` will return this one.

        Args:
            key: the object to associate with the :class:`Color`
            color: the :class:`Color` or a description by which it can be identified
        """
        assignments = self.color_assignments
        if not isinstance(color, Color):
            color = Color.find(color)
        with self._lock:
            old = assignments.get(key, None)
            if old is not None:
                if old[0] is color:
                    return
                self._lose_mapping(old[0])
                old[1].detach()
            assignments[key] = (color, finalize(key, self._lose_mapping_on_gc, color, ref(self)))
            self.colors_in_use[color] = self.colors_in_use.get(color, 0)+1

    # Called with lock held
    def _next_color(self) -> Color:
        """
        Return the next available :class:`Color`, modifying
        :attr:`next_reagent_color`.

        It continues through :attr:`all_colors` and then takes values off of
        :attr:`returned_colors`.

        Note:
            The method assumes that :attr:`_lock` is locked.

        Returns:
            the next :class:`Color`
        Raises:
            IndexError: if there are no more available :class:`Color`\s

        """
        color_list = self.all_colors
        bound = len(color_list)
        start = self.next_reagent_color
        if start < bound:
            for i in range(start, bound):
                c = Color.find(color_list[i])
                if c not in self.colors_in_use:
                    self.next_reagent_color = i+1
                    return c
            self.next_reagent_color = bound
        try:
            color: Color = self.returned_colors.popleft()
            return color
        except IndexError:
                raise IndexError(f"All colors in use")

    def get_color(self, key: H) -> Color:
        """
        Find the :class:`Color` associated with an object.

        If none has previously been associated with the object, the next
        unreserved :class:`Color` in :attr:`all_colors` is grabbed.  If
        :attr:`all_colors` has been exhausted, a :class:`Color` is pulled from
        :attr:`returned_colors`.  If this, too, is empty, an :class:`IndexError`
        is raised.

        If a new :class:`Color` is identified, it is associated with ``key`` by
        means of :func:`reserve_color`.

        Args:
            key: the domain object
        Returns:
            the associated :class:`Color`
        Raises:
            IndexError: if there are no more available :class:`Color`\s

        """
        assignments = self.color_assignments
        ct = assignments.get(key, None)
        if ct is not None:
            return ct[0]
        c = self._next_color()
        self.reserve_color(key, c)
        return c

    def release_color_for(self, key: H) -> bool:
        """
        Remove any :class:`Color` association with an object.  If no other
        object is associated with that :class:`Color`, it is added to
        :attr:`returned_colors`, making it available for future calls to
        :func:`get_color`.

        If :func:`get_color` is called in the future with ``key`` as the
        argument, a new :class:`Color` will be identified and associated with
        it.

        Args:
            key: the domain object
        Returns:
            ``True`` if there was an association to remove, ``False`` otherwise
        """
        assignments = self.color_assignments
        with self._lock:
            ct = assignments.pop(key, None)
            if ct is None:
                return False
            color = ct[0]
            self._lose_mapping(color)
            return True


class _AFS_Thread(Thread):
    """
    The thread used by :class:`AsyncFunctionSerializer`.
    """
    serializer: Final[AsyncFunctionSerializer]  #: The associated :class:`AsyncFunctionSerializer`
    before_task: Final[Optional[Callback]]      #: A callback called before every task
    after_task: Final[Optional[Callback]]       #: A callback called after every task
    on_empty_queue: Final[Optional[Callback]]   #: A callback called after the last task
    queue: Final[deque[Callback]]               #: The queue of callbacks.

    def __init__(self,
                 serializer: AsyncFunctionSerializer,
                 first_callback: Callback,
                 *,
                 name: Optional[str]=None,
                 daemon: bool=False,
                 before_task: Optional[Callback]=None,
                 after_task: Optional[Callback]=None,
                 on_empty_queue: Optional[Callback]=None
                 ) -> None:
        """
        Initialize the thread

        Args:
            serializer: the associated :class:`AsyncFunctionSerializer`
            first_callback: the first callback to process
            name: an optional name of the thread
        Keyword Args:
            daemon: whether or not the thread is a daemon
            before_task: A callback to call before every task
            after_task: A callback to call after every task
            on_empty_queue: A callback to call after the last task
        """
        super().__init__(name=name, daemon=daemon)
        self.serializer = serializer
        self.before_task = before_task
        self.after_task = after_task
        self.on_empty_queue = on_empty_queue
        self.queue = deque[Callback]((first_callback,))

    def run(self) -> None:
        """
        Process the callbacks in the :attr:`queue`.  Before each, call
        :attr:`before_task`. After each, call :attr:`after_task`.  When the
        queue is empty, call :attr:`on_empty` and remove ourself from our
        :attr:`serializer`

        Note:
            :attr:`on_empty` will be called with :attr:`serializer`'s lock
            locked.
        """
        queue = self.queue
        before_task = self.before_task
        after_task = self.after_task
        logger.debug(f'queue len:{len(queue)}|before_task:{before_task}|after_task:{after_task}')
        with self.serializer.lock:
            func: Callback = queue.popleft()
        while True:
            if before_task is not None:
                before_task()
            logger.debug(f'func:{func.__qualname__}')
            func()
            if after_task is not None:
                after_task()
            with self.serializer.lock:
                if len(queue) == 0:
                    # There's nothing left to do, and since we hold the lock, nothing will be added,
                    # so we can just get rid of ourself.
                    self.serializer.thread = None
                    on_empty = self.on_empty_queue
                    if on_empty is not None:
                        on_empty()
                    return
                else:
                    func = queue.popleft()

    def enqueue(self, fn: Callback) -> None:
        """
        Add an item to the :attr:`queue`

        Note:
            This method assumes that :attr:`serializer`'s
            :attr:`~AsyncFunctionSeraializer.lock` is locked.

        Args:
            fn: the callback function
        """
        # This is only called by the serializer while its lock is locked.
        self.queue.append(fn)


class AsyncFunctionSerializer:
    """
    Calls functions in a background thread.  Functions are added by means of
    :func:`enqueue` and are called sequentially.

    The :class:`AsyncFunctionSerializer` can specify actions to be performed
    around the enqueued functions:

    * :attr:`before_task`: called before each function

    * :attr:`after_task`: called after each function

    * :attr:`on_nonempty_queue`: called when the queue goes from being empty to
      being nonempty

    * :attr:`on_empty_queue`: called when the queue goes from being nonempty to
      being empty

    Note that it is legal for these actions to call :func:`enqueue`.

    The background thread is only created when the queue becomes non-empty, and
    it goes away when the queue becomes empty.

    By default, the background thread is not a daemon thread, and so the process
    will not die as long as there are items in the queue.  This can be altered
    by specifying ``daemon=True`` when the :class:`AsyncFunctionSerializer` is
    initialized.
    """

    thread: Optional[_AFS_Thread] = None        #: The background :class`.Thread`
    lock: Final[RLock]                          #: A local lock

    thread_name: Final[Optional[str]]           #: The name of the :class:`.Thread`
    daemon_thread: Final[bool]                  #: Is the :class:`.Thread` a daemon?
    before_task: Final[Optional[Callback]]      #: An optional callback called before each function
    after_task: Final[Optional[Callback]]       #: An optional callback called after each function
    on_empty_queue: Final[Optional[Callback]]   #: An optional callback called when queue becomes empty
    on_nonempty_queue: Final[Optional[Callback]] #: An optional callback called when queue becomes nonempty

    def __init__(self, *,
                 thread_name: Optional[str]=None,
                 daemon_thread: bool=False,
                 before_task: Optional[Callback]=None,
                 after_task: Optional[Callback]=None,
                 on_empty_queue: Optional[Callback]=None,
                 on_nonempty_queue: Optional[Callback]=None
                 ) -> None:
        """
        Initialize the object.

        Keyword Args:
            thread_name: the name of the thread
            daemon_thread: is the thread a daemon?
            before_task: an optional callback called before each function
            after_task: an optional callback called after each function
            on_empty_queue: an optional callback called when the queue becomes empty
            on_nonempty_queue: an optional callback called when the queue becomes nonempty
        """
        self.lock = RLock()
        self.thread_name = thread_name
        self.daemon_thread = daemon_thread
        self.before_task = before_task
        self.after_task = after_task
        self.on_empty_queue = on_empty_queue
        self.on_nonempty_queue = on_nonempty_queue

    def enqueue(self, fn: Callback) -> None:
        """
        Enqueue a function to be called in the background thread.

        Args:
            fn: the function to be enqueued.
        """
        with self.lock:
            thread = self.thread
            if thread is None:
                thread = _AFS_Thread(self, fn,
                                     name=self.thread_name,
                                     daemon=self.daemon_thread,
                                     before_task=self.before_task,
                                     after_task=self.after_task,
                                     on_empty_queue = self.on_empty_queue)
                self.thread = thread
                if self.on_nonempty_queue is not None:
                    self.on_nonempty_queue()
                thread.start()
            else:
                thread.enqueue(fn)

class XferDir(Enum):
    """
    An enumeration representing directions that :class:`Liquid` transfers can
    take.
    """
    FILL = auto()   #: Represents a transfer to add to a location
    EMPTY = auto()  #: Represents a transfer to remove from a location

class State(Generic[T], ABC):
    """
    An object that encapsulates a value and a :class:`ChangeCallbackList` for
    that value.

    :class:`State` is an abstract class that is required to define
    :func:`realize_state`.  This has to do with the way :class:`State` was used
    in the initial system as a base class for proxies for physical devices that
    had to not only track state changes but be able to effect them in the real
    world.  If this is inapplicable, use the subclass :class:`DummyState`, which
    implements :func:`realize_state` to do nothing

    Args:
        T: The value type
    """
    # _state: T   #: The current value

    current_state: MonitoredProperty[T] = MonitoredProperty()
    """
    The current value.  When this value is set to a value not equal to the prior
    value, callbacks registerd to :attr:`on_state_change` are called.
    """
    on_state_change: ChangeCallbackList[T] = current_state.callback_list
    """
    The :class:`.ChangeCallbackList` monitoring :attr:`current_state`.
    """

    has_state: bool = current_state.value_check
    """
    Does :attr:`current_state` have a value?
    """

    def __init__(self, *, initial_state: MissingOr[T]) -> None:
        """
        Initialize the object.  If ``initial_state`` is not :attr:`.MISSING`, it
        becomes the initial value of ``current_state``

        Keyword Args:
            initial_state: the initial value
        """
        if initial_state is not MISSING:
            self.current_state = initial_state
        "Callbacks invoked when :attr:`current_state` is set"

    @abstractmethod
    def realize_state(self, new_state: T) -> None: # @UnusedVariable
        """
        Called to effectuate a new value.  Note that ``new_state`` is not
        necessarily :attr:`current_state`.

        Note:
            This is an abstract method.  There is no default implementation.  If
            you want a trivial default implementation, use :class:`DummyState`
            rather than :class:`State`.

        Args:
            new_state: the value to realize
        """
        ...


class DummyState(State[T]):
    """
    A concrete subclass of :class:`State` that implements :func:`realize_state`
    to do nothing.

    Args:
        T: The value type
    """
    def realize_state(self, new_state:T)->None:
        """
        Do nothing.  Used when there is nothing to be done to realize the new state.

        Args:
            new_state: The (ignored) value tp realize
        """
    ...

class ConfigParams:
    defaults: Final[Namespace]
    cmd_line: Final[Namespace]
    from_code: Final[Mapping[str, Any]]

    def __init__(self, *,
                 defaults: Optional[Namespace] = None,
                 cmd_line: Optional[Namespace] = None,
                 from_code: Optional[Mapping[str, Any]] = None) -> None:
        self.defaults = defaults or Namespace()
        self.cmd_line = cmd_line or Namespace()
        self.from_code = from_code or {}

    def __getattr__(self, name: str) -> Any:
        val = getattr(self.cmd_line, name, MISSING)
        if val is not MISSING:
            return val
        val = self.from_code.get(name, MISSING)
        if val is not MISSING:
            return val
        val = getattr(self.defaults, name, MISSING)
        if val is not MISSING:
            return val
        raise AttributeError(name)

    _sentinel = (MISSING,)

    @overload
    def get(self, name: str, default: tuple[Missing] = (MISSING,), *, expect: typing.Type[T]) -> T: ...
    @overload
    def get(self, name: str, default: V, *, expect: typing.Type[T]) -> Union[V, T]: ...
    @overload
    def get(self, name: str, default: V) -> Any: ...
    @overload
    def get(self, name: str) -> Any: ...
    def get(self, name: str, default = (MISSING,), *, expect: Optional[typing.Type[T]] = None) -> Any:
        try:
            val = self.__getattr__(name)
            if expect is None or isinstance(val, expect):
                return val
            raise TypeError(f"Attribute {name} wrong type.  Expected {expect}, got value {val}")
        except AttributeError:
            if default != self._sentinel:
                return default
            raise

        ...
