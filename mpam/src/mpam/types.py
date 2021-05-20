from __future__ import annotations
from enum import Enum, auto
from typing import Union, Literal, Generic, TypeVar, Optional, Callable, Any,\
    cast, Final, ClassVar, Mapping, overload
from threading import Event, Lock
from quantities.dimensions import Molarity, MassConcentration,\
    VolumeConcentration, Temperature, Volume, Time
from quantities.SI import ml, uL, millisecond
from quantities.core import CountDim

T = TypeVar('T')
V = TypeVar('V')
V2 = TypeVar('V2')

class OnOff(Enum):
    OFF = 0
    ON = 1
    
    def __bool__(self) -> bool:
        return self is OnOff.ON
    
    def __invert__(self) -> OnOff:
        return OnOff.OFF if self else OnOff.ON
    
    
Minus1To1 = Union[Literal[-1], Literal[0], Literal[1]]

class Dir(Enum):
    NORTH = auto()
    N = NORTH
    NORTHEAST = auto()
    NE = NORTHEAST
    EAST = auto()
    E = EAST
    SOUTHEAST = auto()
    SE = SOUTHEAST
    SOUTH = auto()
    S = SOUTH
    SOUTHWEST = auto()
    SW = SOUTHWEST
    WEST = auto()
    W = WEST
    NORTHWEST = auto()
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
        return f"XYCoord({self.x},{self.y})"
    

class Orientation(Enum):
    offset: Final[Mapping[Dir, tuple[Minus1To1, Minus1To1]]]
    
    NORTH_POS_EAST_POS = {Dir.N: (0,1), Dir.NE: (1,1), Dir.E: (1,0), Dir.SE: (1,-1),
                          Dir.S: (0,-1), Dir.SW: (-1,-1), Dir.W: (-1,0), Dir.NW: (-1,1)}
    NORTH_NEG_EAST_POS = {Dir.N: (0,-1), Dir.NE: (1,-1), Dir.E: (1,0), Dir.SE: (1,1),
                          Dir.S: (0,1), Dir.SW: (-1,1), Dir.W: (-1,0), Dir.NW: (-1,-1)}
    NORTH_NEG_EAST_NEG = {Dir.N: (0,-1), Dir.NE: (-1,-1), Dir.E: (-1,0), Dir.SE: (-1,1),
                          Dir.S: (0,1), Dir.SW: (1,1), Dir.W: (1,0), Dir.NW: (1,-1)}
    NORTH_POS_EAST_NEG = {Dir.N: (0,-1), Dir.NE: (1,-1), Dir.E: (1,0), Dir.SE: (1,1),
                          Dir.S: (0,1), Dir.SW: (-1,1), Dir.W: (-1,0), Dir.NW: (-1,-1)}
    
    def __init__(self, offset: Mapping[Dir, tuple[Minus1To1, Minus1To1]]) -> None:
        self.offset = offset
        
    def neighbor(self, direction: Dir, coord: XYCoord) -> XYCoord:
        (dx, dy) = self.offset[direction]
        return XYCoord(coord.x+dx, coord.y+dy)
    
    def __repr__(self):
        return f"Orientation.{self.name}"
    
    
class Ticks(CountDim['Ticks']): ...
ticks = tick = Ticks.base_unit("tick")

DelayType = Union[Ticks, Time]

class TickNumber:
    tick: Ticks
    _zero: ClassVar[TickNumber]
    
    def __init__(self, tick: Ticks) -> None:
        self.tick = tick
        
    def __repr__(self) -> str:
        return f"TickNumber({self.tick.count})"
    
    # I had this cached, but there doesn't seem to be any way
    # to make it immutable, and something was incrementing it.
    @classmethod
    def ZERO(cls) -> TickNumber:
        return cls._zero
        # return TickNumber(0*ticks)
    
    @property
    def number(self) -> int:
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

TickNumber._zero = TickNumber(Ticks.ZERO())

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
    
    def _schedule_for(self, obj: T, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      future: Optional[Delayed[V]] = None
                      ) -> Delayed[V]:
        raise NotImplementedError()
    def schedule_for(self, obj: Union[T, Delayed[T]], *,
                     mode: RunMode = RunMode.GATED, 
                     after: Optional[DelayType] = None,
                     post_result: bool = True,
                     future: Optional[Delayed[V]] = None
                     ) -> Delayed[V]:
        if isinstance(obj, Delayed):
            if future is None:
                future = Delayed[V]()
            obj.when_value(lambda x : self._schedule_for(x, mode=mode, after=after, post_result=post_result, future=future))
            return future
        return self._schedule_for(obj, mode=mode, after=after, post_result=post_result, future=future)
    
    def then(self, op: Union[Operation[V,V2], Callable[[], Operation[V,V2]]], *,
             after: Optional[DelayType] = None,
             ) -> Operation[T,V2]:
        return CombinedOperation[T,V,V2](self, op, after=after)
    
class CombinedOperation(Generic[T,V,V2], Operation[T,V2]):
    first: Operation[T,V]
    second: Union[Operation[V,V2], Callable[[], Operation[V,V2]]]
    after: Final[Optional[DelayType]]
    
    def __init__(self, first: Operation[T, V], second: Union[Operation[V,V2], Callable[[], Operation[V,V2]]], *,
                 after: Optional[DelayType] = None) -> None:
        self.first = first
        self.second = second
        self.after = after
    
    def _schedule_for(self, obj: T, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      future: Optional[Delayed[V2]] = None
                      ) -> Delayed[V2]:
        return self.first._schedule_for(obj, mode=mode, after=after) \
                    .then_schedule(self.second, mode=mode, after=self.after, post_result=post_result, future=future)
        
class OpScheduler(Generic[T]):
    def schedule(self: T, op: Union[Operation[T, V], Callable[[],Operation[T,V]]],
                 mode: RunMode = RunMode.GATED, 
                 after: Optional[DelayType] = None,
                 post_result: bool = True,
                 future: Optional[Delayed[V]] = None
                 ) -> Delayed[V]:
        if not isinstance(op, Operation):
            op = op()
        return op.schedule_for(self, mode=mode, after=after, post_result=post_result, future=future)

class StaticOperation(Generic[V]):
    
    def _schedule(self, *,
                  mode: RunMode = RunMode.GATED, 
                  after: Optional[DelayType] = None,
                  post_result: bool = True,
                  future: Optional[Delayed[V]] = None
                  ) -> Delayed[V]:
        raise NotImplementedError()
    
    
    def schedule(self, *,
                 on_future: Optional[Delayed[Any]] = None,
                 mode: RunMode = RunMode.GATED, 
                 after: Optional[DelayType] = None,
                 post_result: bool = True,
                 future: Optional[Delayed[V]] = None
                 ) -> Delayed[V]:
        if on_future is not None:
            if future is None:
                future = Delayed[V]()
            on_future.when_value(lambda _ : self._schedule(mode=mode, after=after, post_result=post_result, future=future))
            return future
        return self._schedule(mode=mode, after=after, post_result=post_result, future=future)
    
    def then(self, op: Union[Operation[V,V2], Callable[[], Operation[V,V2]]], *,
             after: Optional[DelayType] = None,
             ) -> StaticOperation[V2]:
        return CombinedStaticOperation[V,V2](self, op, after=after)
    
class CombinedStaticOperation(Generic[V,V2], StaticOperation[V2]):
    first: StaticOperation[V]
    second: Union[Operation[V,V2], Callable[[], Operation[V,V2]]]
    after: Final[Optional[DelayType]]
    
    def __init__(self, first: StaticOperation[V], second: Union[Operation[V,V2], Callable[[], Operation[V,V2]]], *,
                 after: Optional[DelayType] = None) -> None:
        self.first = first
        self.second = second
        self.after = after
    
    def _schedule(self, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      future: Optional[Delayed[V2]] = None
                      ) -> Delayed[V2]:
        return self.first._schedule(mode=mode, after=after) \
                    .then_schedule(self.second, mode=mode, after=self.after, post_result=post_result, future=future)
    
# In an earlier iteration, Delayed[T] took a mandatory "guess" argument, and had "initial_guess" and "best_guess"
# properties (the latter returned the value if it was there and the initial guess otherwise).  This seemed to 
# unnecessarily complicate things and made me have to do things like creating a drop before it actually existed,
# which enabled errors.
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
    
    
    @property
    def has_value(self) -> bool:
        return self._val[0]
    
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
    
    def then_schedule(self, op: Union[Operation[T,V], StaticOperation[V],
                                      Callable[[], Operation[T,V]],
                                      Callable[[], StaticOperation[V]]], *, 
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      future: Optional[Delayed[V]] = None) -> Delayed[V]:
        if isinstance(op, StaticOperation):
            return op.schedule(on_future=self, mode=mode, after=after, post_result=post_result, future=future)
        elif isinstance(op, Operation):
            return op.schedule_for(self, mode=mode, after=after, post_result=post_result, future=future)
        else:
            return self.then_schedule(op(), mode=mode, after=after, post_result=post_result, future=future)


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

def schedule(op: Union[StaticOperation[V], Callable[[], StaticOperation[V]]], *,
             mode: RunMode = RunMode.GATED, 
             after: Optional[DelayType] = None,
             post_result: bool = True,
             future: Optional[Delayed[V]] = None
             ) -> Delayed[V]:
    if isinstance(op, StaticOperation):
        return op.schedule(mode=mode, after=after, post_result=post_result, future=future)
    else:
        return op().schedule(mode=mode, after=after, post_result=post_result, future=future)
        
            

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
    
    
    
