from __future__ import annotations
from enum import Enum, auto
from typing import Union, Literal, Generic, TypeVar, Optional, Callable, Any,\
    cast, Final, ClassVar, Mapping, overload, Hashable, Tuple, Sequence,\
    Generator, Protocol
from threading import Event, Lock, RLock, Thread
from quantities.dimensions import Molarity, MassConcentration,\
    VolumeConcentration, Temperature, Volume, Time
from quantities.SI import ml, uL, ms
from quantities.core import CountDim
from matplotlib._color_data import XKCD_COLORS
from weakref import WeakKeyDictionary, finalize
from _weakref import ReferenceType, ref
from _collections import deque
from fractions import Fraction
import math
from abc import ABC, abstractmethod

T = TypeVar('T')
V = TypeVar('V')
V2 = TypeVar('V2')
H = TypeVar('H', bound=Hashable)

Callback = Callable[[], Any]

class OnOff(Enum):
    OFF = 0
    ON = 1
    
    def __bool__(self) -> bool:
        return self is OnOff.ON
    
    def __invert__(self) -> OnOff:
        return OnOff.OFF if self else OnOff.ON
    
    
Minus1To1 = Union[Literal[-1], Literal[0], Literal[1]]

class Dir(Enum):
    _ignore_ = ["_opposites"]
    _opposites: ClassVar[Mapping[Dir, Dir]]
    
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
    
    @classmethod
    def cardinals(cls) -> Sequence[Dir]:
        return (Dir.N, Dir.S, Dir.E, Dir.W)
    
    @property
    def opposite(self) -> Dir:
        return self._opposites[self]
    
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


class XYCoord:
    x: int
    y: int
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
    @property
    def row(self) -> int:
        return self.y
    
    @property
    def col(self) -> int:
        return self.x
    
    @property
    def coords(self) -> tuple[int, int]:
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
    offset: Final[Mapping[Dir, tuple[Minus1To1, Minus1To1]]]
    up_right_delta: tuple[Minus1To1, Minus1To1]
    
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
        self.up_right_delta = (offset[Dir.E][0], offset[Dir.N][1])
        # print(f"{self}.up_right_delta = {self.up_right_delta}")
        
    def neighbor(self, direction: Dir, coord: XYCoord, *, steps: int=1  ) -> XYCoord:
        (dx, dy) = self.offset[direction]
        return XYCoord(coord.x+dx*steps, coord.y+dy*steps)
    
    def up_right(self, coord: XYCoord, x: int, y: int) -> XYCoord:
        dx,dy = self.up_right_delta
        return XYCoord(coord.x+dx*x, coord.y+dy*y)
    
    @property
    def pos_x(self) -> Dir:
        return Dir.E if self.offset[Dir.E][0] > 0 else Dir.W
    @property
    def pos_y(self) -> Dir:
        return Dir.N if self.offset[Dir.N][1] > 0 else Dir.S
    
    def __repr__(self):
        return f"Orientation.{self.name}"
    
class GridRegion:
    lower_left: Final[XYCoord]
    upper_right: Final[XYCoord]
    width: Final[int]
    height: Final[int]
    orientation: Final[Orientation]
    min_x: Final[int]
    min_y: Final[int]
    max_x: Final[int]
    max_y: Final[int]
    
    def __init__(self, lower_left: XYCoord, width: int, height: int, *, 
                 orientation: Orientation = Orientation.NORTH_POS_EAST_POS) -> None:
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
            return f"RunMode.asynchronous({self.motion_time.in_units(ms)})"
        
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

class Operation(Generic[T, V], ABC):

    @abstractmethod    
    def _schedule_for(self, obj: T, *,                      # @UnusedVariable
                      mode: RunMode = RunMode.GATED,        # @UnusedVariable
                      after: Optional[DelayType] = None,    # @UnusedVariable
                      post_result: bool = True,             # @UnusedVariable
                      ) -> Delayed[V]:
        ...
    def schedule_for(self, obj: Union[T, Delayed[T]], *,
                     mode: RunMode = RunMode.GATED, 
                     after: Optional[DelayType] = None,
                     post_result: bool = True,
                     ) -> Delayed[V]:
        if isinstance(obj, Delayed):
            
            future = Delayed[V]()
            def schedule_and_post(x: T) -> None:
                f = self._schedule_for(x, mode=mode, after=after, post_result=post_result)
                f.when_value(lambda val: future.post(val))
            obj.when_value(schedule_and_post)
            return future
        return self._schedule_for(obj, mode=mode, after=after, post_result=post_result)
    
    def then(self, op: Union[Operation[V,V2], StaticOperation[V2],
                             Callable[[], Operation[V,V2]],
                             Callable[[], StaticOperation[V2]]], *,
             after: Optional[DelayType] = None,
             ) -> Operation[T,V2]:
        return CombinedOperation[T,V,V2](self, op, after=after)
    def then_compute(self, fn: Callable[[V], Delayed[V2]]) -> Operation[T,V2]:
        return self.then(ComputeOp[V,V2](fn))
    def then_call(self, fn: Callable[[V], V2]) -> Operation[T,V2]:
        def fn2(obj: V):
            future = Delayed[V2]()
            future.post(fn(obj))
            return future
        return self.then_compute(fn2)
    def then_process(self, fn: Callable[[V], Any]) -> Operation[T,V]:
        def fn2(obj: V) -> V:
            fn(obj)
            return obj
        return self.then_call(fn2)
    
class CombinedOperation(Generic[T,V,V2], Operation[T,V2]):
    first: Operation[T,V]
    second: Union[Operation[V,V2], StaticOperation[V2],
                  Callable[[], Operation[V,V2]],
                  Callable[[], StaticOperation[V2]]]
    after: Final[Optional[DelayType]]
    
    def __init__(self, first: Operation[T, V],
                 second: Union[Operation[V,V2], StaticOperation[V2],
                               Callable[[], Operation[V,V2]],
                               Callable[[], StaticOperation[V2]]], 
                 after: Optional[DelayType] = None) -> None:
        self.first = first
        self.second = second
        self.after = after
        
    def __repr__(self) -> str:
        return f"<Combined: {self.first} {self.second}>"
        
    
    def _schedule_for(self, obj: T, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      ) -> Delayed[V2]:
        return self.first._schedule_for(obj, mode=mode, after=after) \
                    .then_schedule(self.second, mode=mode, after=self.after, post_result=post_result)
        

class ComputeOp(Operation[T,V]):
    def __init__(self, function: Callable[[T],Delayed[V]]) -> None:
        self.function: Final[Callable[[T],Delayed[V]]] = function
        
    def __repr__(self) -> str:
        return f"ComputeOp({self.function})"
    
    
    def _schedule_for(self, obj: T, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      ) -> Delayed[V]:
        assert after == None
        assert post_result == True
        assert mode is RunMode.GATED
        return self.function(obj)
            
            
class CommunicationScheduler(Protocol):
    def schedule_communication(self, cb: Callable[[], Optional[Callback]], mode: RunMode, *,  # @UnusedVariable
                               after: Optional[DelayType] = None) -> None:  # @UnusedVariable
        ...
        
CS = TypeVar('CS', bound=CommunicationScheduler)

class OpScheduler(Generic[CS]):
    def schedule(self: CS,
                 op: Union[Operation[CS, V], Callable[[],Operation[CS,V]]],
                 mode: RunMode = RunMode.GATED, 
                 after: Optional[DelayType] = None,
                 post_result: bool = True,
                 ) -> Delayed[V]:
        if not isinstance(op, Operation):
            op = op()
        return op.schedule_for(self, mode=mode, after=after, post_result=post_result)
    
    class WaitAt(Operation[CS,CS]):
        barrier: Barrier[CS]
        def __init__(self, barrier: Barrier):
            self.barrier = barrier
            
        def _schedule_for(self, obj: CS, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[CS]:
            
            future = Delayed[CS]()
            if after is None:
                self.barrier.pause(obj, future)
            else:
                def cb() -> None:
                    self.barrier.pause(obj, future)                    
                obj.schedule_communication(cb, mode, after=after)
            return future

    class Reach(Operation[CS,CS]):
        barrier: Barrier[CS]
        def __init__(self, barrier: Barrier):
            self.barrier = barrier
            
        def _schedule_for(self, obj: CS, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[CS]:
            
            future = Delayed[CS]()
            if after is None:
                self.barrier.pass_through(obj)
            else:
                def cb() -> None:
                    self.barrier.pass_through(obj)
                obj.schedule_communication(cb, mode, after=after)
            return future

    
    class WaitFor(Operation[CS,CS]):
        waitable: Union[Trigger, Delayed[Any]]
        def _schedule_for(self, obj: CS, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[CS]:
            
            future = Delayed[CS]()
            
            waitable = self.waitable
            
            def cb() -> None:
                if isinstance(waitable, Delayed):
                    waitable.when_value(lambda _: future.post(obj))
                else:
                    waitable.wait(obj, future)
            if after is None:
                cb()
            else:
                obj.schedule_communication(cb, mode, after=after)
            return future
        
        def __init__(self, waitable: Union[Trigger, Delayed[Any]]) -> None:
            self.waitable = waitable
        

class StaticOperation(Generic[V], ABC):
    
    @abstractmethod
    def _schedule(self, *,
                  mode: RunMode = RunMode.GATED,        # @UnusedVariable
                  after: Optional[DelayType] = None,    # @UnusedVariable
                  post_result: bool = True,             # @UnusedVariable
                  ) -> Delayed[V]:
        ...
    
    
    def schedule(self, *,
                 on_future: Optional[Delayed[Any]] = None,
                 mode: RunMode = RunMode.GATED, 
                 after: Optional[DelayType] = None,
                 post_result: bool = True,
                 ) -> Delayed[V]:
        if on_future is not None:
            future = Delayed[V]()
            def schedule_and_post(_) -> None:
                f = self._schedule(mode=mode, after=after, post_result=post_result)
                f.when_value(lambda val: future.post(val))
            on_future.when_value(schedule_and_post)
            return future
        return self._schedule(mode=mode, after=after, post_result=post_result)
    
    def then(self, op: Union[Operation[V,V2], StaticOperation[V2],
                             Callable[[], Operation[V,V2]],
                             Callable[[], StaticOperation[V2]]],
             after: Optional[DelayType] = None,
             ) -> StaticOperation[V2]:
        return CombinedStaticOperation[V,V2](self, op, after=after)
    def then_compute(self, fn: Callable[[V], Delayed[V2]]) -> StaticOperation[V2]:
        return self.then(ComputeOp[V,V2](fn))
    def then_call(self, fn: Callable[[V], V2]) -> StaticOperation[V2]:
        def fn2(obj: V) -> Delayed[V2]:
            future = Delayed[V2]()
            future.post(fn(obj))
            return future
        return self.then_compute(fn2)
    def then_process(self, fn: Callable[[V], Any]) -> StaticOperation[V]:
        def fn2(obj: V) -> V:
            fn(obj)
            return obj
        return self.then_call(fn2)
    
    
class CombinedStaticOperation(Generic[V,V2], StaticOperation[V2]):
    first: StaticOperation[V]
    second: Union[Operation[V,V2], StaticOperation[V2],
                  Callable[[], Operation[V,V2]],
                  Callable[[], StaticOperation[V2]]]
    after: Final[Optional[DelayType]]
    
    def __init__(self, first: StaticOperation[V], 
                 second: Union[Operation[V,V2], StaticOperation[V2],
                               Callable[[], Operation[V,V2]],
                               Callable[[], StaticOperation[V2]]], *,
                 after: Optional[DelayType] = None) -> None:
        self.first = first
        self.second = second
        self.after = after
    
    def _schedule(self, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      ) -> Delayed[V2]:
        return self.first._schedule(mode=mode, after=after) \
                    .then_schedule(self.second, mode=mode, after=self.after, post_result=post_result)
    
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
    
    @classmethod
    def complete(cls, val: T) -> Delayed[T]:
        future = Delayed[T]()
        future._val = (True, val)
        return future
    
    def then_schedule(self, op: Union[Operation[T,V], StaticOperation[V],
                                      Callable[[], Operation[T,V]],
                                      Callable[[], StaticOperation[V]]], *, 
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True) -> Delayed[V]:
        if isinstance(op, StaticOperation):
            return op.schedule(on_future=self, mode=mode, after=after, post_result=post_result)
        elif isinstance(op, Operation):
            return op.schedule_for(self, mode=mode, after=after, post_result=post_result)
        else:
            return self.then_schedule(op(), mode=mode, after=after, post_result=post_result)
        
    def chain(self, fn: Callable[[T], Delayed[V]]) -> Delayed[V]:
        future = Delayed[V]()
        self.when_value(lambda val: fn(val).post_to(future))
        return future
    
    def then_trigger(self, trigger: Trigger) -> Delayed[T]:
        self.when_value(lambda _: trigger.fire())
        return self

    def post_to(self, other: Delayed[T]) -> Delayed[T]:
        self.when_value(lambda val: other.post(val))
        return self
    
    def post_transformed_to(self, other: Delayed[V],
                            transform: Callable[[T], V]) -> Delayed[T]:
        self.when_value(lambda val: other.post(transform(val)))
        return self

    def when_value(self, fn: Callable[[T], Any]) -> Delayed[T]:
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
                
    @classmethod
    def join(cls, futures: Union[Delayed, Sequence[Delayed]]) -> None:
        if isinstance(futures, Delayed):
            futures.wait()
        else:
            for f in futures:
                f.wait()
        
class Trigger:
    waiting: list[tuple[Any,Delayed]]
    lock: Final[RLock]
    
    @property
    def count(self) -> int:
        return len(self.waiting)
    
    def __init__(self) -> None:
        self.waiting = []
        self.lock = RLock()
        
    def wait(self, val: Any, future: Delayed) -> None:
        with self.lock:
            self.waiting.append((val, future))
            
    def on_trigger(self, fn: Callable[[], Any]) -> None:
        future = Delayed[None]()
        future.then_call(lambda _: fn())
        self.wait(None, future)
            
    def fire(self) -> int:
        waiting = self.waiting
        with self.lock:
            self.waiting = []
        val = len(waiting)
        for v,f in waiting:
            f.post(v)
        return val
    
    def reset(self) -> None:
        with self.lock:
            self.waiting.clear()
    
    
                
class Barrier(Trigger, Generic[T]):
    required: int
    waiting_for: int
    name: Final[Optional[str]]
    
    @property
    def at_barrier(self) -> int:
        return self.required-self.waiting_for

    
    def __init__(self, required: int, *, name: Optional[str] = None) -> None:
        super().__init__()
        self.required = required
        self.waiting_for = required
        self.name = name
    def __str__(self) -> str:
        name = (self.name+", ") if self.name is not None else ""
        return f"Barrier({name}{self.required}, {self.waiting_for})"
    def reach(self, val: T, future: Optional[Delayed[T]] = None) -> int:
        with self.lock:
            # if self.name is not None:
            #     print(f"Reached {self}: {val}")
            if self.waiting_for == 1:
                # if self.name is not None:
                #     print(f"-- Firing {self}")
                self.fire()
                if future is not None:
                    future.post(val)
                return self.at_barrier
            else:
                if future is not None:
                    self.wait(val, future)
                self.waiting_for -= 1
                return self.at_barrier-1
            
    def pause(self, val: T, future: Delayed[T]) -> int:
        return self.reach(val, future)
    
    def pass_through(self, val: T) -> int:
        return self.reach(val)
    
    def reset(self, required: Optional[int] = None) -> None:
        with self.lock:
            if required is not None:
                self.required = required
            self.waiting_for = self.required
            # if self.name is not None:
            #     print(f"Reset {self} to {required}")
            super().reset()
            
            
    

def schedule(op: Union[StaticOperation[V], Callable[[], StaticOperation[V]]], *,
             mode: RunMode = RunMode.GATED, 
             after: Optional[DelayType] = None,
             post_result: bool = True,
             ) -> Delayed[V]:
    if isinstance(op, StaticOperation):
        return op.schedule(mode=mode, after=after, post_result=post_result)
    else:
        return op().schedule(mode=mode, after=after, post_result=post_result)
        
ChangeCallback = Callable[[T,T],None]
class ChangeCallbackList(Generic[T]):
    callbacks: dict[Hashable, ChangeCallback[T]]
    lock: Final[RLock]
    
    def __init__(self) -> None:
        self.callbacks = {}
        self.lock = RLock()
        
    def add(self, cb: ChangeCallback[T], *, key: Optional[Hashable] = None) -> None:
        if key is None:
            key = cb
        with self.lock:
            self.callbacks[key] = cb
            # if key is not cb:
                # print(f"Adding callback {key}")
                # print(f"  Callbacks now {map_str(list(self.callbacks.keys()))}")
        
    def remove(self, key: Hashable) -> None:
        with self.lock:
            # val = self.callbacks[key]
            del self.callbacks[key]
            # if key is not val:
                # print(f"Removing callback {key}")
                # print(f"  Callbacks now {map_str(list(self.callbacks.keys()))}")
        
    def discard(self, key: Hashable) -> None:
        with self.lock:
            self.callbacks.pop(key, None)
        
    def clear(self) -> None:
        with self.lock:
            self.callbacks.clear()
        
    def process(self, old: T, new: T) -> None:
        # print(f"Processing callbacks")
        with self.lock:
            copy = list((k,cb) for k,cb in self.callbacks.items())
        for k,cb in copy:
            # print(f"Callback ({old}->{new}: {k}")
            cb(old, new)

    
# Used in the case when a chemical is there, but its concentration
# cannot be computed.  Usually when two reagents specify the chemical,
# but with different concentration units
class UnknownConcentration:
    def __repr__(self) -> str:
        return "UnknownConcentration()"
    def __str__(self) -> str:
        return "unknown concentration"
    
    def __mul__(self, _: float) -> UnknownConcentration:
        return self
    
    def __plus_(self, _: UnknownConcentration) -> UnknownConcentration:
        return self
    
unknown_concentration: Final[UnknownConcentration] = UnknownConcentration()            
Concentration = Union[Molarity, MassConcentration, VolumeConcentration, UnknownConcentration]



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
    
ChemicalComposition = Mapping[Chemical, Concentration]
    
class ProcessStep:
    description: Final[str]
    _known: Final[ClassVar[dict[str, ProcessStep]]] = {}
    _class_lock: Final[ClassVar[Lock]] = Lock()
    
    def __init__(self, description: str) -> None:
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
        with cls._class_lock:
            ps = cls._known.get(description, None)
            if ps is None:
                ps = ProcessStep(description)
                cls._known[description] = ps
            return ps
                
MixtureSpec = Tuple[tuple['Reagent', Fraction], ...]
        
class Reagent:
    name: Final[str]
    composition: ChemicalComposition
    min_storage_temp: Optional[Temperature]
    max_storage_temp: Optional[Temperature]
    _lock: Final[Lock]
    _process_results: Final[dict[ProcessStep, Reagent]]
    
    known: ClassVar[dict[str, Reagent]] = dict[str, 'Reagent']()
    

    def __init__(self, name: str, *, 
                 composition: Optional[ChemicalComposition] = None,
                 min_storage_temp: Optional[Temperature] = None,
                 max_storage_temp: Optional[Temperature] = None,
                 ) -> None:
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
             min_storage_temp: Optional[Temperature] = None,
             max_storage_temp: Optional[Temperature] = None) -> Reagent:
        c = cls.known.get(name, None)
        if c is None:
            c = Reagent(name, composition=composition, 
                         min_storage_temp=min_storage_temp, max_storage_temp=max_storage_temp)
        return c
    
    @property
    def mixture(self) -> MixtureSpec:
        return ((self, Fraction.from_float(1)),)
    
    @property
    def is_pure(self) -> bool:
        return len(self.mixture) == 1
    
    @property
    def process_steps(self) -> tuple[ProcessStep, ...]:
        return ()
    
    @property
    def unprocessed(self) -> Reagent:
        return self
    
    def liquid(self, volume: Volume, *, inexact: bool = False) -> Liquid:
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
        return composition
    
    @staticmethod
    def LoseComposition(composition: ChemicalComposition) -> ChemicalComposition:  # @UnusedVariable
        return {}
    
    
    def processed(self, step: Union[str, ProcessStep], 
                  new_composition_function: Optional[Callable[[ChemicalComposition], ChemicalComposition]] = None) -> Reagent:
        if self is waste_reagent:
            return self
        if isinstance(step, str):
            step = ProcessStep.find_or_create(step)
        with self._lock:
            r = self._process_results.get(step, None)
            if r is None:
                if new_composition_function is None:
                    new_composition_function = Reagent.SameComposition
                r = ProcessedReagent(self, step)
                self._process_results[step] = r
            return r
    
    
    
waste_reagent: Final[Reagent] = Reagent.find("waste")
unknown_reagent: Final[Reagent] = Reagent.find("unknown")

class Mixture(Reagent):
    _mixture: Final[MixtureSpec]
    _class_lock: Final[ClassVar[Lock]] = Lock()
    _known_mixtures: Final[ClassVar[dict[tuple[float,Reagent,Reagent], Reagent]]] = {}
    _instances: Final[ClassVar[dict[MixtureSpec, Mixture]]] = {}
    
    def __init__(self, name: str, mixture: MixtureSpec, *, 
                 composition: Optional[ChemicalComposition] = None,
                 min_storage_temp: Optional[Temperature] = None,
                 max_storage_temp: Optional[Temperature] = None,
                 ) -> None:
        super().__init__(name, composition=composition, min_storage_temp=min_storage_temp, max_storage_temp=max_storage_temp)
        self._mixture = mixture

    @property
    def mixture(self) -> MixtureSpec:
        return self._mixture
    
    def __repr__(self) -> str:
        return f"Mixture({repr(self.name), repr(self._mixture)})"
    

    @classmethod
    def new_mixture(cls, r1: Reagent, r2: Reagent, ratio: float, name: Optional[str] = None) -> Reagent:
        fraction = ratio/(ratio+1)
        as_frac = Fraction.from_float(fraction)
        mixture = {r: f*as_frac for r,f in r1.mixture}
        composition = {chem: conc*fraction for chem, conc in r1.composition.items()}
        fraction = 1-fraction
        as_frac = Fraction.from_float(fraction)
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
    
    @classmethod
    def find_or_compute(cls, r1: Reagent, r2: Reagent, *, 
                        ratio: float = 1,
                        name: Optional[str] = None) -> Reagent:
        if r1 is r2:
            return r1
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
    last_step: Final[ProcessStep]
    prior: Final[Reagent]
    
    def __init__(self, prior: Reagent, step: ProcessStep, *, 
                 composition: Optional[ChemicalComposition] = None,
                 min_storage_temp: Optional[Temperature] = None,
                 max_storage_temp: Optional[Temperature] = None,
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
    _reagent: Reagent
    _volume: Volume
    inexact: bool
    
    volume_change_callbacks: Final[ChangeCallbackList[Volume]]
    reagent_change_callbacks: Final[ChangeCallbackList[Reagent]]
    
    @property
    def volume(self) -> Volume:
        return self._volume
    
    @volume.setter
    def volume(self, new: Volume) -> None:
        old = self._volume
        if old is not new:
            self._volume = new
            self.volume_change_callbacks.process(old, new)
        
    @property
    def reagent(self) -> Reagent:
        return self._reagent
    
    @reagent.setter
    def reagent(self, new: Reagent) -> None:
        old = self._reagent
        if old is not new:
            self._reagent = new
            self.reagent_change_callbacks.process(old, new)
    
    def __init__(self, reagent: Reagent, volume: Volume, *, inexact: bool = False) -> None:
        self._reagent = reagent
        self._volume = volume
        self.inexact = inexact
        
        self.volume_change_callbacks = ChangeCallbackList[Volume]()
        self.reagent_change_callbacks = ChangeCallbackList[Reagent]()
        
    def __repr__(self) -> str:
        return f"Liquid[{'~' if self.inexact else ''}{self.volume.in_units(uL)}, {self.reagent}]"

    def __str__(self) -> str:
        return f"{'~' if self.inexact else ''}{self.volume.in_units(uL):g} of {self.reagent}"
        
    def __iadd__(self, rhs: Volume) -> Liquid:
        self.volume = max(self.volume+rhs, 0*ml)
        return self
    
    def __isub__(self, rhs: Volume) -> Liquid:
        self.volume = max(self.volume-rhs, 0*ml)
        return self
    
    def on_volume_change(self, cb: ChangeCallback[Volume], *, key: Optional[Hashable] = None):
        if key is None:
            key = cb
        self.volume_change_callbacks.add(cb, key=key)
    
    def on_reagent_change(self, cb: ChangeCallback[Reagent], *, key: Optional[Hashable] = None):
        if key is None:
            key = cb
        self.reagent_change_callbacks.add(cb, key=key)
        
    def mix_with(self, other: Liquid, *, result: Optional[Union[Reagent, str]] = None) -> Liquid:
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
    
    def mix_in(self, other: Liquid, *, result: Optional[Union[Reagent, str]] = None) -> None:
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
        self.reagent = r
        self.inexact = self.inexact or other.inexact
        self.volume = v
        other.reagent = r
        other.inexact = False
        other.volume = Volume.ZERO()
        
    def split_to(self, other: Liquid) -> None:
        other.reagent = self.reagent
        other.inexact = self.inexact
        v = self.volume/2
        self.volume = v
        other.volume = v
    
    def processed(self, step: Union[str, ProcessStep], 
                  new_composition_function: Optional[Callable[[ChemicalComposition], ChemicalComposition]] = None) -> Liquid:
        self.reagent = self.reagent.processed(step, new_composition_function)
        return self
    
class Color:
    description: Final[str]
    rgba: Final[tuple[float,float,float,float]]
    
    _class_lock: Final[ClassVar[Lock]] = Lock()
    _known: Final[ClassVar[dict[str, Color]]] = {}
    
    def __init__(self, description: str, rgba: tuple[float,float,float,float]) -> None:
        self.description = description
        self.rgba = rgba
        
    @classmethod
    def find(cls, description: Union[str, tuple[float,float,float]]) -> Color:
        key = str(description)
        with cls._class_lock:
            c = cls._known.get(key, None)
            if c is None:
                from matplotlib import colors
                c = Color(key, colors.to_rgb(description))
            cls._known[key] = c
            return c
        
    def __repr__(self) -> str:
        return f"Color({repr(self.description)}, {repr(self.rgba)})"
    
    def __str__(self) -> str:
        return self.description
    
class ColorAllocator(Generic[H]):
    all_colors: ClassVar[Optional[Sequence[str]]] = None
    color_assignments: WeakKeyDictionary[H, tuple[Color, finalize]]
    colors_in_use: Final[dict[Color, int]]
    returned_colors: Final[deque[Color]]
    next_reagent_color: int
    first_pass_done: bool
    _lock: Final[RLock]
    _class_lock: Final[ClassVar[Lock]] = Lock()
    
    def __init__(self, initial_reservations: Optional[Mapping[H, Color]] = None):
        self.color_assignments = WeakKeyDictionary()
        self.colors_in_use = {}
        self.returned_colors = deque[Color]()
        self.next_reagent_color = 0
        self._lock = RLock()
        if initial_reservations is not None:
            for k,c in initial_reservations.items():
                self.reserve_color(k, c)
    
    def _lose_mapping(self, color: Color) -> None:
        uses = self.colors_in_use[color]
        if uses > 1:
            self.colors_in_use[color] = uses-1
        else:
            del self.colors_in_use[color]
            self.returned_colors.append(color)
    
    @staticmethod
    def _lose_mapping_on_gc(color: Color, selfref: ReferenceType[ColorAllocator]) -> None:
        self = selfref()
        if self is not None:
            with self._lock:
                self._lose_mapping(color)
    
    def reserve_color(self, key: H, color: Color) -> None:
        assignments = self.color_assignments
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
        color_list = ColorAllocator.all_colors
        if color_list is None:
            with ColorAllocator._class_lock:
                color_list = ColorAllocator.all_colors
                if color_list is None:
                    color_list = [k for k in XKCD_COLORS]
                    ColorAllocator.all_colors = color_list
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
        assignments = self.color_assignments
        ct = assignments.get(key, None)
        if ct is not None:
            return ct[0]
        c = self._next_color()
        self.reserve_color(key, c)
        return c

    
class _AFS_Thread(Thread):
    serializer: Final[AsyncFunctionSerializer]
    before_task: Final[Optional[Callback]]
    after_task: Final[Optional[Callback]]
    queue: Final[deque[Callback]]

    def __init__(self,
                 serializer: AsyncFunctionSerializer,
                 first_callback: Callback,
                 *,
                 name: Optional[str]=None,
                 daemon: bool=False,
                 before_task: Optional[Callback]=None,
                 after_task: Optional[Callback]=None
                 ) -> None:
        super().__init__(name=name, daemon=daemon)
        self.serializer = serializer
        self.before_task = before_task
        self.after_task = after_task
        self.queue = deque[Callback]((first_callback,))

    def run(self) -> None:
        queue = self.queue
        before_task = self.before_task
        after_task = self.after_task
        func: Callback = queue.popleft()
        while True:
            if before_task is not None:
                before_task()
            func()
            if after_task is not None:
                after_task()
            with self.serializer.lock:
                if len(queue) == 0:
                    # There's nothing left to do, and since we hold the lock, nothing will be added, 
                    # so we can just get rid of ourself.
                    self.serializer.thread = None
                    return
                else:
                    func = queue.popleft()

    def enqueue(self, fn: Callback) -> None:
        # This is only called by the serializer while its lock is locked.
        self.queue.append(fn)


class AsyncFunctionSerializer:
    thread: Optional[_AFS_Thread] = None
    lock: Final[Lock]

    thread_name: Final[Optional[str]]
    daemon_thread: Final[bool]
    before_task: Final[Optional[Callback]]
    after_task: Final[Optional[Callback]]

    def __init__(self, *,
                 thread_name: Optional[str]=None,
                 daemon_thread: bool=False,
                 before_task: Optional[Callback]=None,
                 after_task: Optional[Callback]=None
                 ) -> None:
        self.lock = Lock()
        self.thread_name = thread_name
        self.daemon_thread = daemon_thread
        self.before_task = before_task
        self.after_task = after_task

    def enqueue(self, fn: Callback) -> None:
        with self.lock:
            thread = self.thread
            if thread is None:
                thread = _AFS_Thread(self, fn,
                                     name=self.thread_name,
                                     daemon=self.daemon_thread,
                                     before_task=self.before_task,
                                     after_task=self.after_task)
                self.thread = thread
                thread.start()
            else:
                thread.enqueue(fn)
