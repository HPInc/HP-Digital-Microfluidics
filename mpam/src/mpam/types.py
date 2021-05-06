from enum import Enum
from typing import Union, Literal

class OnOff(Enum):
    OFF = 0
    ON = 1
    
    def __bool__(self):
        return self is OnOff.ON

class Dir(Enum):
    Minus1To1 = Union[Literal[-1], Literal[0], Literal[1]]
    delta_x: Minus1To1
    delta_y: Minus1To1
    
    def __init__(self, delta_x: Minus1To1, delta_y: Minus1To1):
        self.delta_x = delta_x
        self.delta_y = delta_y
    
    NORTH = (0, 1)
    N = NORTH
    NORTHEAST = (1, 1)
    NE = NORTHEAST
    EAST = (1, 0)
    E = EAST
    SOUTHEAST = (1, -1)
    SE = SOUTHEAST
    SOUTH = (0, -1)
    S = SOUTH
    SOUTHWEST = (-1, -1)
    SW = SOUTHWEST
    WEST = (-1, 0)
    W = WEST
    NORTHWEST = (-1, 1)
    NW = NORTHWEST

    UP = NORTH
    DOWN = SOUTH
    LEFT = WEST
    RIGHT = EAST

class XYCoord:
    x: int
    y: int
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def row(self):
        return self.y
    
    def col(self):
        return self.x
        
    def __eq__(self, other: object):
        if not isinstance(other, XYCoord): return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return "XYCoord({0},{1})".format(self.x, self.y)
    
    def __add__(self, delta: Dir):
        if not isinstance(delta, Dir):
            raise TypeError("{0} only supports addition with {1}: {2} provided"
                            .format(XYCoord, Dir, type(delta)))
        return XYCoord(self.x+delta.delta_x, self.y+delta.delta_y)
    
    def __radd__(self, delta: Dir):
        return self+delta
    
    def __iadd__(self, delta: Dir):
        if not isinstance(delta, Dir):
            raise TypeError("{0} only supports addition with {1}: {2} provided"
                            .format(XYCoord, Dir, type(delta)))
        self.x += delta.delta_x
        self.y += delta.delta_y
        return self
    
    
    
if __name__ == '__main__':
    print(OnOff.ON)
    print(Dir.NORTHWEST)
    print(Dir.NORTH)
    print(Dir.UP)
    print(Dir.NORTH == Dir.UP)
    coord = XYCoord(3,5)
    print(coord)
    print(coord+Dir.RIGHT)
    print(Dir.RIGHT+coord)
    coord += Dir.NORTHWEST
    print(coord)
