from __future__ import annotations

from enum import Enum, auto
from functools import cached_property
import logging
from typing import ClassVar, Mapping, Sequence, Union, Literal, Final, Callable,\
    TypeVar, Generator

from .basic import assert_never


logger = logging.getLogger(__name__)

_T = TypeVar('_T')

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
    
    @cached_property
    def is_cardinal(self) -> bool:
        return self in Dir.cardinals()

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
    
    def turn_to(self, d: Dir) -> Turn:
        for t in Turn.__members__.values():
            if self.turned(t) is d:
                return t
        logger.error(f"{self}.turn_to({d}) not defined")
        assert False, f"{self}.turn_to({d}) not defined"
        
        
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, XYCoord): return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"XYCoord({self.x},{self.y})"

    def __add__(self, offset: tuple[int, int]) -> XYCoord:
        return XYCoord(self.x+offset[0], self.y+offset[1])


Minus1To1 = Union[Literal[-1], Literal[0], Literal[1]]
"""A type representing literal `-1`, `0`, or `1`.

Primarily used in the implementation of :class:`Orientation`.
"""

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

    @cached_property
    def pos_x(self) -> Dir:
        '''
        The :class:`Dir` in which ``x`` coordinates increase
        '''
        return Dir.E if self.offset[Dir.E][0] > 0 else Dir.W
    @cached_property
    def pos_y(self) -> Dir:
        '''
        The :class:`Dir` in which ``y`` coordinates increase
        '''
        return Dir.N if self.offset[Dir.N][1] > 0 else Dir.S

    def __repr__(self) -> str:
        return f"Orientation.{self.name}"
    
    def is_above(self, c1: XYCoord, c2: XYCoord) -> bool:
        """
        Check whether one :class:`XYCoord` is above another
     
        Parameters:
            c1: A first :class:`XYCoord`
            c2: A second :class:`XYCoord`
        Returns:
            ``True`` if ``c1``\'s :attr:`~XYCoord.row` is to the
            :attr:`~Dir.NORTH` of ``c2``\'s
        """
        if self.pos_y is Dir.N:
            return c1.row > c2.row
        else:
            return c1.row < c2.row
        
    def is_left(self, c1: XYCoord, c2: XYCoord) -> bool:
        """
        Check whether one :class:`XYCoord` is to the left of another
     
        Parameters:
            c1: A first :class:`XYCoord`
            c2: A second :class:`XYCoord`
        Returns:
            ``True`` if ``c1``\'s :attr:`~XYCoord.col` is to the
            :attr:`~Dir.WEST` of ``c2``\'s
        """
        if self.pos_x is Dir.E:
            return c1.col < c2.col
        else:
            return c1.col > c2.col
        
    def remap(self, xy: tuple[float, float], from_dir: Dir, to_dir: Dir) -> tuple[float,float]:
        assert from_dir.is_cardinal, f"{from_dir} is not a cardinal direction"
        assert to_dir.is_cardinal, f"{to_dir} is not a cardinal direction"
        
        if from_dir is to_dir:
            return xy
        turn = from_dir.turn_to(to_dir)
        assert turn is not Turn.NONE
        x,y = xy
        if turn is Turn.AROUND:
            return (-x,-y)
        def adjust() -> None:
            # Get to or from a NORTH_POS_EAST_POS system
            nonlocal x,y
            if self.pos_y is Dir.SOUTH:
                y = -y
            if self.pos_x is Dir.WEST:
                x = -x
        # First we get to a NORTH_POS_EAST_POS system
        adjust()
        if turn is Turn.LEFT:
            x,y = -y,x
        elif turn is Turn.RIGHT:
            x,y = y,-x
        else:
            assert_never(turn)
        # Now we get back to our actual system
        adjust()
        return x,y 
            
            
        
class RCOrder(Enum):
    row_major: Final[bool]
    col_mult: Final[int]
    row_mult: Final[int]
    
    DOWN_RIGHT = ( False, True,  True )
    DOWN_LEFT =  ( False, True,  False )
    UP_RIGHT =   ( False, False, True )
    UP_LEFT =    ( False, False, False )
    RIGHT_DOWN = ( True,  True,  True )
    RIGHT_UP =   ( True,  False, True )
    LEFT_DOWN =  ( True,  True,  False )
    LEFT_UP =    ( True,  False, False )
    
    def __init__(self, row_major: bool, down_rows: bool, left_to_right: bool) -> None:
        self.row_major = row_major
        self.col_mult = 1 if left_to_right else -1
        self.row_mult = -1 if down_rows else 1

    def key_for(self, o: Orientation, *,
                loc: Callable[[_T], XYCoord]) -> Callable[[_T], tuple[int, int]]:

        ne = o.offset[Dir.NE]
        cmult = self.col_mult * ne[0]
        rmult = self.row_mult * ne[1]
        
        def make_key(obj: _T) -> tuple[int, int]:
            xy = loc(obj)
            c = cmult*xy.col
            r = rmult*xy.row
            return (r,c) if self.row_major else (c,r)
        return make_key



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




