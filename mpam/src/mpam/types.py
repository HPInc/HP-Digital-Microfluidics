from __future__ import annotations
from enum import Enum
from typing import Union, Literal, Generic, TypeVar, Optional, Callable, Any,\
    cast, Final, ClassVar, Mapping
from threading import Event, Lock
from quantities.dimensions import Molarity, MassConcentration,\
    VolumeConcentration, Temperature, Volume
from quantities.SI import ml

T = TypeVar('T')

class OnOff(Enum):
    OFF = 0
    ON = 1
    
    def __bool__(self) -> bool:
        return self is OnOff.ON
    
    def __invert__(self) -> OnOff:
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
        return f"XYCoord({self.x},{self.y})"
    
    def __add__(self, delta: Dir):
        if not isinstance(delta, Dir):
            raise TypeError(f"{XYCoord} only supports addition with {Dir}: {type(delta)} provided")
        return XYCoord(self.x+delta.delta_x, self.y+delta.delta_y)
    
    def __radd__(self, delta: Dir):
        return self+delta
    
    def __iadd__(self, delta: Dir):
        if not isinstance(delta, Dir):
            raise TypeError(f"{XYCoord} only supports addition with {Dir}: {type(delta)} provided")
        self.x += delta.delta_x
        self.y += delta.delta_y
        return self
    
# ValTuple = tuple[Literal[False],None]

# ValTuple = Union[tuple[Literal[False],None],Literal[True], T]

ValTuple = tuple[bool, T]

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
    
    # This allows you to say "drop.move(N).then.move(S)"
    @property
    def then(self) -> T:
        return self.value()
    

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
            

Concentration = Union[Molarity, MassConcentration, VolumeConcentration]

class Chemical:
    name: Final[str]
    formula: Optional[str]
    description: Optional[str]
    
    known: ClassVar[dict[str, Chemical]] = dict[str, 'Chemical']()
    
    def __init__(self, name: str, *,
                 formula: Optional[str] = None, 
                 description: Optional[str] = None) -> None:
        self.name = name
        self.formula = formula
        self.description = description
        Chemical.known[name] = self
        
    @classmethod
    def find(cls, name: str, *,
             formula: Optional[str] = None, 
             description: Optional[str] = None) -> Chemical:
        c = cls.known.get(name, None)
        if c is None:
            c = Chemical(name, formula=formula, description=description)
        return c
    
    def __repr__(self) -> str:
        return f"Chemical[{self.name}]"
    
    def __str__(self) -> str:
        return self.name
        
class Reagent:
    name: Final[str]
    composition: Mapping[Chemical, Concentration]
    min_storage_temp: Optional[Temperature]
    max_storage_temp: Optional[Temperature]
    
    known: ClassVar[dict[str, Reagent]] = dict[str, 'Reagent']()

    def __init__(self, name: str, 
                 composition: Mapping[Chemical, Concentration] = {},
                 min_storage_temp: Optional[Temperature] = None,
                 max_storage_temp: Optional[Temperature] = None) -> None:
        self.name = name
        self.composition = composition
        self.min_storage_temp = min_storage_temp
        self.max_storage_temp = max_storage_temp
        Reagent.known[name] = self

    @classmethod        
    def find(cls, name: str, *,
             composition: Mapping[Chemical, Concentration] = {},
             min_storage_temp: Optional[Temperature] = None,
             max_storage_temp: Optional[Temperature] = None) -> Reagent:
        c = cls.known.get(name, None)
        if c is None:
            c = Reagent(name, composition=composition, 
                         min_storage_temp=min_storage_temp, max_storage_temp=max_storage_temp)
        return c
    
    def liquid(self, volume: Volume, *, inexact: bool = False) -> Liquid:
        return Liquid(self, volume, inexact=inexact)
    
    def __repr__(self) -> str:
        return f"Reagent[{self.name}]"
    
    def __str__(self) -> str:
        return self.name
    
waste_reagent: Final[Reagent] = Reagent.find("waste")
unknown_reagent: Final[Reagent] = Reagent.find("unknown")
    
class Liquid:
    reagent: Reagent
    volume: Volume
    inexact: bool
    
    def __init__(self, reagent: Reagent, volume: Volume, *, inexact: bool = False):
        self.reagent = reagent
        self.volume = volume
        self.inexact = inexact
        
    def __iadd__(self, rhs: Volume) -> Liquid:
        self.volume = max(self.volume+rhs, 0*ml)
        return self
    
    def __isub__(self, rhs: Volume) -> Liquid:
        self.volume = max(self.volume-rhs, 0*ml)
        return self
    
    
