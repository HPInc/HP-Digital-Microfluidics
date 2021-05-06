from enum import Enum
from typing import Union, Literal, Generic, TypeVar, Optional, Final, Callable, Any,\
    cast
from threading import Event, Lock

T = TypeVar('T')

class OnOff(Enum):
    OFF = 0
    ON = 1
    
    def __bool__(self) -> bool:
        return self is OnOff.ON
    
    def __invert__(self) -> 'OnOff':
        return OnOff.OFF if self else OnOff.ON
    
    
Minus1To1 = Union[Literal[-1], Literal[0], Literal[1]]

class Dir(Enum):
    delta_x: Minus1To1
    delta_y: Minus1To1
    
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

    def __init__(self, dx: Minus1To1, dy: Minus1To1):
        self.delta_x = dx
        self.delta_y = dy

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
    
# ValTuple = tuple[Literal[False],None]

# ValTuple = Union[tuple[Literal[False],None],Literal[True], T]

ValTuple = tuple[bool, T]

class Waiting: ...
WAITING = Waiting()
DelayedValue = Union[Waiting, T]

class Missing: ...
MISSING = Missing()

class Delayed(Generic[T]):
    _val: ValTuple[T] = (False, cast(T, None))
    _maybe_lock: Optional[Lock] = None
    _callbacks: list[Callable[[T], Any]]
    
    @property
    def _lock(self) -> Lock:
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
    
    
    def __init__(self, *, value: Union[Missing, T] = MISSING) -> None:
        if value != MISSING:
            self._val = (True, cast(T, value))
        
    def has_value(self) -> bool:
        return self._val[0]
    
    def peek(self) -> ValTuple[T]:
        return self._val

    def wait(self) -> None:
        if not self.has_value():
            e = Event()
            self.when_value(lambda _: e.set())
            while not e.is_set():
                # We probably want a timeout here to allow it to be interrupted
                e.wait()

    def value(self) -> T:
        self.wait()
        return self._val[1]
    

    def when_value(self, fn: Callable[[T], Any]) -> None:
        v = self._val
        just_run: bool = v[0]
        if not just_run:
            with self._lock:
                v = self._val
                just_run = v[0]
                if not just_run:
                    self._callbacks.append(fn)
        if just_run:
            fn(v[1])

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
    def post(self, val: T) -> None:
        assert not self.has_value()
        self._val = (True, val)
        if self._maybe_lock:
            with self._lock:
                for fn in self._callbacks:
                    fn(val)
                # Just in case this object gets stuck somewhere.
                # The callbacks are never going to be needed again
                del self._callbacks
            

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
