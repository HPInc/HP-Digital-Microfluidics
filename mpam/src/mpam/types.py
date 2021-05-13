from __future__ import annotations
from enum import Enum
from typing import Union, Literal, Generic, TypeVar, Optional, Callable, Any,\
    cast, Final, ClassVar, Mapping, Protocol, overload
from threading import Event, Lock
from quantities.dimensions import Molarity, MassConcentration,\
    VolumeConcentration, Temperature, Volume, Time
from quantities.SI import ml, uL, millisecond
from quantities.core import CountDim

T = TypeVar('T')
V = TypeVar('V')

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
    
    NORTH = (0, -1)
    N = NORTH
    NORTHEAST = (1, -1)
    NE = NORTHEAST
    EAST = (1, 0)
    E = EAST
    SOUTHEAST = (1, 1)
    SE = SOUTHEAST
    SOUTH = (0, 1)
    S = SOUTH
    SOUTHWEST = (-1, 1)
    SW = SOUTHWEST
    WEST = (-1, 0)
    W = WEST
    NORTHWEST = (-1, -1)
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
    
class Ticks(CountDim['Ticks']): ...
ticks = tick = Ticks.base_unit("tick")

DelayType = Union[Ticks, Time]

class RunMode:
    is_gated: Final[bool]
    motion_time: Time
    GATED: ClassVar[RunMode]
    
    def __init__(self, is_gated: bool, motion_time: Time):
        self.is_gated = is_gated
        self.motion_time = motion_time
        
    def __repr__(self) -> str:
        if (self.is_gated):
            return f"RunMode.GATED"
        else:
            return f"RunMode.asynchronous({self.motion_time.in_units(millisecond)})"
        
    def gated_delay(self, after: Optional[DelayType], *, step: int=0) -> Ticks:
        if after is None:
            return step*ticks
        assert isinstance(after, Ticks), f"Gated run mode incomapatible with delay of {after}"
        return after if step == 0 else after+step*ticks
 
    def asynchronous_delay(self, after: Optional[DelayType], step: int=0) -> Time:
        if after is None:
            return Time.ZERO() if step == 0 else step*self.motion_time
        assert isinstance(after, Time), f"Asynchronous run mode incomapatible with delay of {after}"
        return after if step == 0 else after+step*self.motion_time
 
    def step_delay(self, base: Optional[DelayType], step: int) -> DelayType:
        if self.is_gated:
            return self.gated_delay(base)+step*ticks
        else:
            return self.asynchronous_delay(base)+step*self.motion_time
                
    
    @classmethod   
    def asynchronous(cls, motion_time: Time) -> RunMode:
        return RunMode(False, motion_time)
    
RunMode.GATED = RunMode(True, Time.ZERO())


# ValTuple = tuple[Literal[False],None]

# ValTuple = Union[tuple[Literal[False],None],Literal[True], T]

ValTuple = tuple[bool, T]

class Missing: ...
MISSING: Final[Missing] = Missing()

class Operation(Generic[T, V]):
    
    def guess_value(self, obj: T) -> V: 
        raise NotImplementedError()
    def _schedule_for(self, obj: T, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      guess_only: bool = False,
                      future: Optional[Delayed[V]] = None
                      ) -> Delayed[V]:
        raise NotImplementedError()
    def schedule_for(self, obj: Union[T, Delayed[T]], *,
                     mode: RunMode = RunMode.GATED, 
                     after: Optional[DelayType] = None,
                     guess_only: bool = False,
                     future: Optional[Delayed[V]] = None
                     ) -> Delayed[V]:
        if isinstance(obj, Delayed):
            if future is None:
                future = Delayed[V](guess=self.guess_value(obj.best_guess), immediate=guess_only)
            obj.when_value(lambda x : self.schedule_for(x, mode=mode, after=after, guess_only=guess_only, future=future))
            return future
        return self._schedule_for(obj, mode=mode, after=after, guess_only=guess_only, future=future)
        
class OpScheduler(Generic[T]):
    def schedule(self: T, op: Operation[T, V],
                 mode: RunMode = RunMode.GATED, 
                 after: Optional[DelayType] = None,
                 guess_only: bool = False,
                 future: Optional[Delayed[V]] = None
                 ) -> Delayed[V]:
        return op.schedule_for(self, mode=mode, after=after, guess_only=guess_only,future=future)

class Delayed(Generic[T]):
    _val: ValTuple[T] = (False, cast(T, None))
    _maybe_lock: Optional[Lock] = None
    _callbacks: list[Callable[[T], Any]]
    _guess: T
    
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
    
    
    def __init__(self, *, guess: T, immediate: bool=False) -> None:
        self._guess = guess
        if immediate:
            self._val = (True, guess)
        
    @property
    def has_value(self) -> bool:
        return self._val[0]
    
    @property
    def initial_guess(self):
        return self.guess
    
    @property
    def best_guess(self):
        if self.has_value:
            return self._val[1]
        else:
            return self._guess
        
    
    def peek(self) -> ValTuple[T]:
        return self._val

    def wait(self) -> None:
        if not self.has_value:
            e = Event()
            self.when_value(lambda _: e.set())
            while not e.is_set():
                # We probably want a timeout here to allow it to be interrupted
                e.wait()
                
    and_wait = wait
    
    @property
    def value(self) -> T:
        self.wait()
        return self._val[1]
    
    def then_schedule(self, op: Operation[T,V], *, 
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      guess_only: bool = False,
                      future: Optional[Delayed[V]] = None) -> Delayed[V]:
        return op.schedule_for(self, mode=mode, after=after, guess_only=guess_only, future=future)


    def when_value(self, fn: Callable[[T], Any]) -> Delayed[T]:
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
        return self
            
    # or maybe then_call should create a new future, posted at the end.            
    then_call = when_value

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
    
    def __init__(self, reagent: Reagent, volume: Volume, *, inexact: bool = False) -> None:
        self.reagent = reagent
        self.volume = volume
        self.inexact = inexact
        
    def __repr__(self) -> str:
        return f"Liquid[{'~' if self.inexact else ''}{self.volume.in_units(uL)}, {self.reagent}]"

    def __str__(self) -> str:
        return f"{'~' if self.inexact else ''}{self.volume.in_units(uL)} of {self.reagent.name}"
        
    def __iadd__(self, rhs: Volume) -> Liquid:
        self.volume = max(self.volume+rhs, 0*ml)
        return self
    
    def __isub__(self, rhs: Volume) -> Liquid:
        self.volume = max(self.volume-rhs, 0*ml)
        return self
    
    
