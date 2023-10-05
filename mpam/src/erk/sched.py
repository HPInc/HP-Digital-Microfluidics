
from __future__ import annotations
from typing import TypeVar, Generic, cast, Optional, Any, Callable, Union, Final,\
    runtime_checkable, Protocol
from threading import Lock, Event, RLock
from abc import abstractmethod, ABC
from enum import Enum, auto
from quantities.dimensions import Time
from _collections_abc import Iterable
from erk.basic import ComputedDefaultDict, Callback, not_None, assert_never
from quantities.ticks import Ticks

_T = TypeVar('_T')
_V = TypeVar('_V')
_V2 = TypeVar('_V2')
_V3 = TypeVar('_V3')
_Tco = TypeVar('_Tco', covariant=True) ; "A generic covariant type variable"
_Tcontra = TypeVar('_Tcontra', contravariant=True) ; "A generic contravariant type variable"


class NoWait(Enum):
    SINGLETON = auto()
    def __repr__(self) -> str:
        return "NO_WAIT"

NO_WAIT: Final[NoWait] = NoWait.SINGLETON

DelayType = Union[Ticks, Time]  ; "A delay amount, either :class:`Ticks` or :class:`.Time`"
WaitableType = Union[NoWait, DelayType, 'Trigger', 'Delayed[Any]']


@runtime_checkable
class CanDelay(Protocol):
    def delay_by(self, after: DelayType, fn: Callback) -> None: # @UnusedVariable
        ...
    def delay_by_and_return(self, after: DelayType, fn: Callable[[], _V]) -> Delayed[_V]:
        future = Postable[_V]()
        def run_then_post() -> None:
            future.post(fn())
        self.delay_by(after, run_then_post)
        return future
    def delay_by_and_chain(self, after: DelayType, fn: Callable[[], Delayed[_V]]) -> Delayed[_V]:
        future = Postable[_V]()
        def run_then_post() -> None:
            fn().post_to(future)
        self.delay_by(after, run_then_post)
        return future
        
    
class DelayScheduler:
    checked_classes: Final = ComputedDefaultDict[type, bool](lambda t: isinstance(t, CanDelay))
    
    @classmethod
    def for_obj(cls, obj: Any) -> Optional[CanDelay]:
        obj_type = type(obj)
        return cast(CanDelay, obj) if cls.checked_classes[obj_type] else None
    
        
    @classmethod
    def call_and_ignore(cls,
                        after: WaitableType,
                        fn: Callable[[], _V],
                        *, obj: Any) -> None:
        match after:
            case NoWait.SINGLETON | Time.ZERO | Ticks.ZERO:
                fn()
            case Time() | Ticks():
                assert after > 0
                can_delay = not_None(cls.for_obj(obj),
                                     desc = lambda: f"{after} ({type(after)}) doesn't support call_after().")
                can_delay.delay_by(after, fn)
            case Trigger():
                after.on_trigger(fn)
            case Delayed():
                after.when_value(lambda _: fn())
            case _:
                assert_never(after)
                
    @classmethod
    def call_and_return(cls,
                        after: WaitableType,
                        fn: Callable[[], _V],
                        *, obj: Any) -> Delayed[_V]:
        match after:
            case NoWait.SINGLETON | Time.ZERO | Ticks.ZERO:
                return Delayed.complete(fn())
        future = Postable[_V]()
        def run_then_post() -> None:
            future.post(fn())
            
        cls.call_and_ignore(after, run_then_post, obj=obj)
        return future

    @classmethod
    def call_and_chain(cls,
                        after: WaitableType,
                        fn: Callable[[], Delayed[_V]],
                        *, obj: Any) -> Delayed[_V]:
        match after:
            case NoWait.SINGLETON | Time.ZERO | Ticks.ZERO:
                return fn()
        future = Postable[_V]()
        def run_then_post() -> None:
            fn().post_to(future)
        cls.call_and_ignore(after, run_then_post, obj=obj)
        return future

_ValTuple = tuple[bool, _T]

class Delayed(Generic[_Tco]):
    """
    A container that will (or may) eventually contain a value of type :attr:`_T`.

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
        _Tco: The covariant type of the value that will be asserted.
    """

    _val: _ValTuple[_Tco] = (False, cast(_Tco, None))
    """
    A tuple containing the validity status and value (if valid)

    All :class:`Delayed` objects share the same invalid value and assert their
    own local valid values.  This allows :class:`Delayed` objects to be
    trivially constructed.

    The cast is necessary because ``None`` is likely to not be a valid instance
    of :attr:`_T`, but nobody should be looking there if the first element is
    ``False``.
    """
    _maybe_lock: Optional[Lock] = None
    """
    A lock object, if any callbacks have been asserted.
    """

    _callbacks: list[Callable[[_Tco], Any]]
    """
    The list of callbacks.  This is created within :attr:`_lock` if necessary.

    This object can only be referenced while :attr:`_lock` is locked.
    """

    def __str__(self) -> str:
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

    def peek(self) -> _ValTuple[_Tco]:
        """
        Check both whether a value has been asserted and what that value is.

        Returns:
            (``True``, ``value``) if ``value`` is the asserted value, otherwise
            (``False``, ``None``)

        Warning:
            The type of the second element is only valid if the first element is
            ``True``.  If it is not, the second element will be ``None``, which
            may not be a valid :attr:`_T`.  It is therefore important not to use
            the second element if the first element is ``False``.

            Note that the second element being ``None`` does not indicate that
            the value has not been asserted if ``None`` is a valid :attr:`_T`.
        """
        return self._val

    def wait(self) -> None:
        """
        Block the thread until a value has been asserted
        """
        if not self.has_value:
            e = Event()
            def do_set(_: Any) -> None:
                e.set()
            self.when_value(do_set)
            # self.when_value(lambda _: e.set())
            while not e.is_set():
                # We probably want a timeout here to allow it to be interrupted
                e.wait()

    and_wait = wait

    @property
    def value(self) -> _Tco:
        """
        The asserted value, blocking if necessary.
        """
        self.wait()
        return self._val[1]

    @classmethod
    def complete(cls, val: _T) -> Delayed[_T]:
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

    def then_schedule(self, op: Union[Operation[_Tco, _V], StaticOperation[_V], # type: ignore [type-var]
                                      Callable[[], Operation[_Tco, _V]],
                                      Callable[[], StaticOperation[_V]]], *,
                      after: WaitableType = NO_WAIT,
                      post_result: bool = True) -> Delayed[_V]:
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

    def chain(self, fn: Callable[[_Tco], Delayed[_V]]) -> Delayed[_V]:
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
        future = Postable[_V]()
        def fn2(val: Any) -> None:
            fn(val).post_to(future)
        self.when_value(fn2)
        # self.when_value(lambda val: fn(val).post_to(future))
        return future

    def transformed(self, fn: Callable[[_Tco], _V]) -> Delayed[_V]:
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
        future = Postable[_V]()
        def post_transformed(val: Any) -> None:
            future.post(fn(val))
        self.when_value(post_transformed)
        # self.when_value(lambda val: future.post(fn(val)))
        return future
    
    def monitor(self, fn: Callable[[_Tco], Any]) -> Delayed[_Tco]:
        def call_and_post(val: _Tco) -> _Tco: # type: ignore[misc]
            fn(val)
            return val
        return self.transformed(call_and_post)
    
    def to_const(self, val: _V) -> Delayed[_V]:
        def ignore_arg(_v: Any) -> _V:
            return val
        return self.transformed(ignore_arg)

    def then_trigger(self, trigger: Trigger) -> Delayed[_Tco]:
        """
        When a value is asserted, fire a :class:`Trigger`.

        Args:
            trigger: the :class:`Trigger` to fire
        Returns
            this :class:`Delayed` object
        """
        def do_trigger(_: Any) -> None:
            trigger.fire()
        self.when_value(do_trigger)
        # self.when_value(lambda _: trigger.fire())
        return self

    def post_to(self, other: Postable[_Tco]) -> Delayed[_Tco]:
        """
        When a value is asserted, post it to another :class:`Delayed` object.

        Args:
            other: a second :class:`Delayed` object
        Returns
            this :class:`Delayed` object
        """
        def do_post(val: Any) -> None:
            other.post(val)
        self.when_value(do_post)
        # self.when_value(lambda val: other.post(val))
        return self

    def post_val_to(self, other: Postable[_V], value: _V) -> Delayed[_Tco]:
        """
        When a value is asserted, post a specific value to another
        :class:`Delayed` object.

        Args:
            other: a second :class:`Delayed` object
            value: the value to post
        Returns
            this :class:`Delayed` object
        """
        def do_post(_: Any) -> None:
            other.post(value)
        self.when_value(do_post)
        # self.when_value(lambda _: other.post(value))
        return self

    def post_transformed_to(self, other: Postable[_V],
                            transform: Callable[[_Tco], _V]) -> Delayed[_Tco]:
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
        def do_post(val: Any) -> None:
            other.post(transform(val))
        self.when_value(do_post)
        # self.when_value(lambda val: other.post(transform(cast(_T, val))))
        return self

    def when_value(self, fn: Callable[[_Tco], Any]) -> Delayed[_Tco]:
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

class _CompleteDelayed(Delayed[_T]):
    def _define_in_concrete(self)->None: ...
    
    def __init__(self, val: _T) -> None:
        self._val = (True, val)
        self._constant: Final[_T] = val
        
    def wait(self) -> None:
        pass
    
    @property
    def value(self) -> _T:
        return self._constant
    
    def chain(self, fn: Callable[[_T], Delayed[_V]]) -> Delayed[_V]:
        return fn(self._constant)
    
    def transformed(self, fn:Callable[[_T], _V]) -> Delayed[_V]:
        return Delayed.complete(fn(self._constant))
    
    def monitor(self, fn: Callable[[_T], Any]) -> _CompleteDelayed[_T]:
        fn(self._constant)
        return self
    
    def to_const(self, val:_V) -> Delayed[_V]:
        return Delayed.complete(val)
    
    def then_trigger(self, trigger:Trigger) -> _CompleteDelayed[_T]:
        trigger.fire()
        return self
    
    def post_to(self, other: Postable[_T]) -> _CompleteDelayed[_T]:
        other.post(self._constant)
        return self
    
    def post_val_to(self, other: Postable[_V], value: _V) -> _CompleteDelayed[_T]:
        other.post(value)
        return self
    
    def post_transformed_to(self, other: Postable[_V], 
                            transform: Callable[[_T], _V]) -> _CompleteDelayed[_T]:
        other.post(transform(self._constant))
        return self
    
    def when_value(self, fn: Callable[[_T], Any]) -> _CompleteDelayed[_T]:
        fn(self._constant)
        return self
    
    

# MyPy complains about the variance mismatch between Postable and Delayed,
# although only with Python 3.10.
class Postable(Delayed[_Tcontra]): # type: ignore [type-var]
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
        _Tcontra: the contravariant type that can be asserted using :func:`post`.
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
    def post(self, val: _Tcontra) -> None:
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
    waiting: list[Callable[[], Any]]
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

    def wait(self, val: _T, future: Postable[_T]) -> None:
        """
        When the :class:`Trigger` next fires, post a value to a future.

        Args:
            val: the value to post
            future: the :class:`Delayed` object to post to
        """
        self.on_trigger(lambda: future.post(val))

    def on_trigger(self, fn: Callable[[], Any]) -> None:
        """
        When the :class:`Trigger` next fires, call a function

        Args:
            fn: the function (taking no arguments) to call
        """
        with self.lock:
            self.waiting.append(fn)

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
        for fn in waiting:
            fn()
        return val

    def reset(self) -> None:
        """
        Forget all waiting actions.
        """
        with self.lock:
            self.waiting.clear()


class SingleFireTrigger(Trigger):
    """
    A subclass of :class:`Trigger` that keeps track of whether it's been
    :func:`fire`ed and invokes any callbacks immediately on :func:`wait`
    if it has.
    """
    fired: bool
    
    def __init__(self) -> None:
        super().__init__()
        self.fired = False

    def fire(self) -> int:
        with self.lock:
            if not self.fired:
                self.fired = True
                return super().fire()
            else:
                assert self.count == 0, f"Single fire trigger already fired but has callbacks waiting."
                return 0

    def wait(self, val: Any, future: Postable) -> None:
        """
        When the :class:`Trigger` next fires, post a value to a future.

        Args:
            val: the value to post
            future: the :class:`Delayed` object to post to
        """
        with self.lock:
            if self.fired:
                future.post(val)
            else:
                super().wait(val, future)

BarrierAction = Union[tuple[_T,Postable[_T]], Callable[[], Any]]

class Barrier(Trigger):

    """
    A :class:`Trigger` that fires when a certain number of :attr:`_T` objects
    reach it.  Objects reaching the :class:`Barrier` can optionally "pause" there
    by passing in a :class:`Delayed` object to which the waiting object is
    posted when the last object reaches the :class:`Barrier`.

    A :class:`Barrier` may be reset (by calling :func:`reset`), optionally
    changing the number of objects required required to reach it.  When that
    happens, any objects that had already reached it (and any other actions
    added to it as a :class:`Trigger`) are forgotten.

    Args:
        _T: The type of object the :class:`Barrier` is waiting for.
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
    def reach(self, action: Optional[BarrierAction[_T]] = None) -> int:
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
        
        val: Any = None
        if isinstance(action, tuple):
            val, future = action
            action = lambda: future.post(val)
        with self.lock:
            wf = self.waiting_for
            ab = self.required - wf
            def assert_msg() -> str:
                who = "object" if val is None else val
                return f"{who} reached un-waiting barrier {self}"
            assert wf > 0, assert_msg()
            self.waiting_for = wf-1
            if wf > 1:
                if action is not None:
                    self.on_trigger(action)
                return ab
        # If we get here, we're the last one to reach, so we fire the trigger
        # and process this future.

        # Note that we're not inside the lock (we don't want to fire inside the
        # lock), so there will be a problem if somebody else calls reset()
        # before we call fire().
        self.fire()
        if action is not None:
            action()
        return ab

    def pause(self, val: _T, future: Postable[_T]) -> int:
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
        return self.reach((val, future))

    def pass_through(self) -> int:
        """
        Reach the :class:`Barrier` without pausing there.  Equivalent to calling
        :func:`reach` without a ``future`` parameter.

        Args:
            val: the value that reached the :class:`Barrier`
        Returns:
            the number of objects that had previously reached the
            :class:`Barrier`
        """
        return self.reach()

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



def schedule(op: Union[StaticOperation[_V], Callable[[], StaticOperation[_V]]], *,
             after: WaitableType = NO_WAIT,
             post_result: bool = True,
             ) -> Delayed[_V]:
    """
    Schedule an :class:`StaticOperation`.

    If ``op`` is a :class:`Callable`, it is called to get the actual :class:`StaticOperation`.

    Args:
        op: The :class:`StaticOperation` to schedule or a :class:`Callable` to call to obtain it.
    Keyword Args:
        after: an optional delay to wait before scheduling the operation
        post_result: whether to post the resulting value to the returned future object
    Returns:
        a :class:`Delayed`\[:attr:`_V`] future object to which the resulting
        value will be posted unless ``post_result`` is ``False``.
    """
    if isinstance(op, StaticOperation):
        return op.schedule(after=after, post_result=post_result)
    else:
        return op().schedule(after=after, post_result=post_result)
    
    
class Operation(Generic[_T, _V], ABC):
    '''
    An operation that can be scheduled for an object of type :attr:`_T` and returns a delayed value of type :attr:`_V`

    The basic notion is that if `op` is an :class:`Operation`\[:attr:`_T`, :attr:`_V`] and `t` is a :attr:`_T`, in ::

        dv: Delayed[_V] = op.schedule_for(t)

    the call will return immediately, and `dv` will obtain a value of type :attr:`_V` at some point
    in the future, when the operation has completed.

    If :attr:`_T` is a subclass of :class:`OpScheduler`, the same effect can be
    obtained by calling its :func:`~OpScheduler.schedule` method::

        dv: Delayed[_V] = t.schedule(op)

    Note:
        :class:`Operation`\[:attr:`_T`, :attr:`_V`] is an abstract base class.
        The actual implementation class must implement :func:`_schedule_for` and :fund:`after_delay`.

    Args:
        _T: the type of the object used to schedule the :class:`Operation`
        _V: the type of the value produced by the operation
    '''
    
    @abstractmethod
    def _schedule_for(self, obj: _T, *,                # @UnusedVariable
                      post_result: bool = True,       # @UnusedVariable
                      ) -> Delayed[_V]:
        """
        The implementation of :func:`schedule_for`.  There is no default implementation.

        :meta public:
        Args:
            obj: the :attr:`_T` object to schedule the operation for
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`_V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        ...

    def schedule_for(self, obj: Union[_T, Delayed[_T]], *,
                     after: WaitableType = NO_WAIT,
                     post_result: bool = True,
                     ) -> Delayed[_V]:
        """
        Schedule this operation for the given object.

        If ``obj`` is a :class:`Delayed` object, the actual scheduling will take
        place after a value has been posted to it, and that value will be used.
        Note that any delay specified by ``after`` will be applied **after**
        this value is obtained.

        Once an object has been identified, the actual scheduling will be
        delegated through :func:`_schedule_for`.

        Args:
            obj: The :attr:`_T` object for which the operation will be scheduled
                or a :class:`Delayed`\[:attr:`_T`] object which will produce it.
        Keyword Args:
            after: an optional delay to wait before scheduling the operation
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`_V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        # if after is None:
        #     logger.debug(f'{obj}')
        # else:
        #     logger.debug(f'{obj}|after:{after}')

        if isinstance(obj, Delayed):
            future = Postable[_V]()
            def schedule_and_post(x: _T) -> None:
                self.schedule_for(
                    x, after=after, post_result=post_result).post_to(future)
            obj.when_value(schedule_and_post)
            return future

        real_obj = obj
        def cb() -> Delayed[_V]:
            return self._schedule_for(real_obj, post_result=post_result)
        return DelayScheduler.call_and_chain(after, cb, obj=obj)
    
    def then(self,
             op: Union[Operation[_V, _V2], StaticOperation[_V2], # type: ignore [type-var]
                       Callable[[], Operation[_V, _V2]],
                       Callable[[], StaticOperation[_V2]]], *,
             after: WaitableType = NO_WAIT,
             ) -> Operation[_T, _V2]:
        """
        Chain this :class:`Operation` and another together to create a single
        new :class:`Operation`

        The value produced by this :class:`Operation` will be used to schedule
        the second one (unless the second is a :class:`StaticOperation`, in
        which case the second will be scheduled after this one is done).

        The actual result will be a :class:`CombinedOperation`\[:attr:`_T`, :attr:`_V`, :attr:`_V2`].

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
        return CombinedOperation[_T, _V, _V2](self, op, after=after)

    def then_compute(self, fn: Callable[[_V], Delayed[_V2]]) -> Operation[_T, _V2]:
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
        return self.then(ComputeOp[_V, _V2](fn))

    def then_call(self, fn: Callable[[_V], _V2]) -> Operation[_T, _V2]:
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
        def fn2(obj: _V) -> Delayed[_V2]:
            future = Postable[_V2]()
            future.post(fn(obj))
            return future
        return self.then_compute(fn2)

    def then_process(self, fn: Callable[[_V], Any]) -> Operation[_T, _V]:
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
        def fn2(obj: _V) -> _V:
            fn(obj)
            return obj
        return self.then_call(fn2)




class CombinedOperation(Generic[_T, _V, _V3], Operation[_T, _V3]):
    """
    An :class:`Operation` representing chaining two :class:`Operation`\s
    together.

    Objects of this class are built using :func:`Operation.then`,
    :func:`Operation.then_call`, :func:`Operation.then_compute`, and
    :func:`Operation.then_process`,

    Args:
        _T: the type of the object used to schedule the :class:`Operation`
        _V: the type of the value produced by the first operation
        _V3: the type of the value produced by the second operation (and the
            :class:`CombinedOperation` overall)
    """
    first: Operation[_T, _V]               ; "The first :class:`Operation`"
    second: Union[Operation[_V, _V3], StaticOperation[_V3], # type: ignore [type-var]
                  Callable[[], Operation[_V, _V3]],
                  Callable[[], StaticOperation[_V3]]]
    """
    The second :class:`Operation` (or :class:`StaticOperation`) or a :class:`Callable` that produces one.
    """
    after: Final[WaitableType]   ; "An optional delay to use between :attr:`first` and :attr:`second`"

    def __init__(self, first: Operation[_T, _V],
                 second: Union[Operation[_V, _V3], StaticOperation[_V3], # type: ignore [type-var]
                               Callable[[], Operation[_V, _V3]],
                               Callable[[], StaticOperation[_V3]]],
                 after: WaitableType=NO_WAIT) -> None:
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

    def _schedule_for(self, obj: _T, *,
                      post_result: bool = True,
                      ) -> Delayed[_V3]:
        """
        Implementat :func:`Operation.schedule_for` by scheduling :attr:`second` after :attr:`first` is done.

        :meta public:
        Args:
            obj: the :attr:`_T` object to schedule the operation for
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`_V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``.
        """
        return self.first._schedule_for(obj) \
                    .then_schedule(self.second, after=self.after, post_result=post_result)


class ComputeOp(Generic[_T, _V], Operation[_T, _V]):
    """
    A :class:`Operation` that when scheduled, returns the result of passing its
    scheduled-for object to a :class:`Callable` that returns a :class:`Delayed` object.

    Args:
        _T: the type of the object used to schedule the :class:`Operation`
        _V: the type of the value produced by the operation
    """
    def __init__(self, function: Callable[[_T],Delayed[_V]]) -> None: 
        """
        Initialize the :class:`ComputeOp`

        Args:
            function: The :class:`Callable` to call.
        """
        self.function: Final[Callable[[_T],Delayed[_V]]] = function   ; "The :class:`Callable` to call"

    def __repr__(self) -> str:
        return f"ComputeOp({self.function})"

    def _schedule_for(self, obj: _T, *,
                      post_result: bool = True,
                      ) -> Delayed[_V]:
        """
        Implement :func:`Operation.schedule_for` by passing `obj` to :attr:`function`.

        :meta public:

        Note:
            ``post_result`` is asserted to be ``True``.

        Args:
            obj: the :attr:`_T` object to schedule the operation for
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`_V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``.
        """
        assert post_result == True
        return self.function(obj)


class OpScheduler(Generic[_T]):
    """
    A mixin base class giving a class the ability to schedule
    :class:`Operation`\[:attr:`CS`, :attr:`_V`]s.

    Typically, this will be class :attr:`CS` itself, as in::

        class Drop(OpScheduler['Drop']):
            ...
    There are several :class:`Operation`\s (e.g., :class:`WaitAt`,
    :class:`Reach`, :class:`WaitFor`), that are defined for all
    :class:`OpScheduler`\s.

    Args:
        CS: A subclass of :class:`OpScheduler`
    """
    def schedule(self: _T,
                 op: Union[Operation[_T, _V], Callable[[],Operation[_T, _V]]],
                 after: WaitableType = NO_WAIT,
                 post_result: bool = True,
                 ) -> Delayed[_V]:
        """
        Schedule an operation for this object, which is assumed to be a :attr:`CS`.

        If ``op`` is a :class:`Callable`, it is called to get the actual :class:`Operation`.

        Args:
            op: The :class:`Operation` to schedule or a :class:`Callable` to call to obtain it.
            after: an optional delay to wait before scheduling the operation
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`_V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``.
        """
        if not isinstance(op, Operation):
            op = op()
        return op.schedule_for(self, after=after, post_result=post_result)

    class WaitAt(Operation[_T,_T]):
        """
        An :class:`Operation` during which the :attr:`CS` object waits at a
        :class:`Barrier`.  The operation completes when the appropriate number
        of objects have reached the barrier.  The value posted to the
        :class:`Delayed` value returned by :func:`schedule_for` is the object
        for which the operation was scheduled.
        """
        barrier: Barrier    ; "The :class:`Barrier` to wait at"
        def __init__(self, barrier: Barrier):
            """
            Initialize the object

            Args:
                barrier: the :class:`Barrier` to wait at
            """
            self.barrier = barrier

        def _schedule_for(self, obj: _T, *,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[_T]:
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
            future = Postable[_T]()
            self.barrier.pause(obj, future)
            return future

    class Reach(Operation[_T,_T]):
        """
        An :class:`Operation` during which the :attr:`CS` object reaches a
        :class:`Barrier` but does not pause there.  The operation completes
        immediately (or after the delay specified by ``after``).  The
        value posted to the :class:`Delayed` value returned by
        :func:`schedule_for` is the object for which the operation was
        scheduled.
        """
        barrier: Barrier    ; "The :class:`Barrier` to reach"
        def __init__(self, barrier: Barrier):
            """
            Initialize the object

            Args:
                barrier: the :class:`Barrier` to reach
            """
            self.barrier = barrier

        def _schedule_for(self, obj: _T, *,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[_T]:
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
            future = Postable[_T]()
            self.barrier.pass_through()
            if post_result:
                future.post(obj)
            return future

    class WaitFor(Operation[_T,_T]):
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
        def _schedule_for(self, obj: _T, *,
                          post_result: bool = True,  # @UnusedVariable
                          ) -> Delayed[_T]:
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
            return DelayScheduler.call_and_return(self.waitable, 
                                                  lambda: obj,
                                                  obj = obj)

        def __init__(self, waitable: WaitableType) -> None:
            """
            Initialize the object

            Args:
                waitable: what to wait for
            """
            self.waitable = waitable


class StaticOperation(Generic[_V], ABC):
    '''
    An operation that can be scheduled and which returns a delayed value of type
    :attr:`_V`.  This is like :class:`Operation`\[:attr:`_T`, :attr:`_V`], but it
    does not require an object of type :attr:`_T`.

    The basic notion is that if `op` is a :class:`StaticOperation`\[:attr:`_V`], in ::

        dv: Delayed[_V] = op.schedule()

    the call will return immediately, and `dv` will obtain a value of type :attr:`_V` at some point
    in the future, when the operation has completed.

    The same effect can be obtained by calling :func:`mpam.types.schedule`::

        dv: Delayed[_V] = schedule(op)

    Note:
        :class:`StaticOperation`\[:attr:`_V`] is an abstract base class.
        The actual implementation class must implement :func:`_schedule`.

    Args:
        _V: The type of the value that is the result of the :class:`StaticOperation`
    '''

    scheduler: Final[Any]

    def __init__(self, *, scheduler: Any) -> None:
        self.scheduler = scheduler

    @abstractmethod
    def _schedule(self, *,
                  post_result: bool = True,       # @UnusedVariable
                  ) -> Delayed[_V]:
        """
        The implementation of :func:`schedule`.  There is no default implementation.

        :meta public:
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`_V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        ...


    def schedule(self, *,
                 after: WaitableType = NO_WAIT,
                 post_result: bool = True,
                 ) -> Delayed[_V]:
        """
        Schedule this operation.

        Once an object has been identified, the actual scheduling will be
        delegated through :func:`_schedule_for`.

        Keyword Args:
            after: an optional delay to wait before scheduling the operation
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`_V`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        def cb() -> Delayed[_V]:
            return self._schedule(post_result=post_result)
        return DelayScheduler.call_and_chain(after, cb, obj=self.scheduler)

    def then(self, op: Union[Operation[_V, _V2], StaticOperation[_V2], # type: ignore [type-var]
                             Callable[[], Operation[_V, _V2]],
                             Callable[[], StaticOperation[_V2]]],
             after: WaitableType = NO_WAIT,
             ) -> StaticOperation[_V2]:
        """
        Chain this :class:`StaticOperation` and follow-on :class:`Operation`
        together to create a single new :class:`StaticOperation`

        The value produced by this :class:`StaticOperation` will be used to schedule
        the second :class:`Operation` (unless the second is a :class:`StaticOperation`, in
        which case the second will be scheduled after this one is done).

        The actual result will be a :class:`CombinedStaticOperation`\[:attr:`_V`, :attr:`_V2`].

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
        return CombinedStaticOperation[_V, _V2](self, op, after=after)

    def then_compute(self, fn: Callable[[_V], Delayed[_V2]]) -> StaticOperation[_V2]:
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
        return self.then(ComputeOp[_V, _V2](fn))

    def then_call(self, fn: Callable[[_V], _V2]) -> StaticOperation[_V2]:
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
        def fn2(obj: _V) -> Delayed[_V2]:
            future = Postable[_V2]()
            future.post(fn(obj))
            return future
        return self.then_compute(fn2)

    def then_process(self, fn: Callable[[_V], Any]) -> StaticOperation[_V]:
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
        def fn2(obj: _V) -> _V:
            fn(obj)
            return obj
        return self.then_call(fn2)


class CombinedStaticOperation(Generic[_V, _V2], StaticOperation[_V2]):
    """
    A :class:`StaticOperation` representing chaining a :class:`StaticOperation`
    and an :class:`Operation` together.

    Objects of this class are built using :func:`StaticOperation.then`,
    :func:`StaticOperation.then_call`, :func:`StaticOperation.then_compute`, and
    :func:`StaticOperation.then_process`,

    Args:
        _V: the type of the value produced by the first operation
        _V2: the type of the value produced by the second operation (and the
            :class:`CombinedStaticOperation` overall)
    """

    first: StaticOperation[_V]               ; "The first :class:`StaticOperation`"
    second: Union[Operation[_V, _V2], StaticOperation[_V2], # type: ignore [type-var]
                  Callable[[], Operation[_V, _V2]],
                  Callable[[], StaticOperation[_V2]]]
    """
    The second :class:`Operation` (or :class:`StaticOperation`) or a :class:`Callable` that produces one.
    """
    after: Final[WaitableType]   ; "An optional delay to use between :attr:`first` and :attr:`second`"

    def __init__(self, first: StaticOperation[_V],
                 second: Union[Operation[_V, _V2], StaticOperation[_V2], # type: ignore [type-var]
                               Callable[[], Operation[_V, _V2]],
                               Callable[[], StaticOperation[_V2]]], *,
                 after: WaitableType = NO_WAIT) -> None:
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
                  ) -> Delayed[_V2]:
        """
        Implement :func:`Operation.schedule_for` by scheduling :attr:`second` after :attr:`first` is done.

        :meta public:
        Keyword Args:
            post_result: whether to post the resulting value to the returned future object
        Returns:
            a :class:`Delayed`\[:attr:`_V2`] future object to which the resulting
            value will be posted unless ``post_result`` is ``False``
        """
        return self.first._schedule() \
                    .then_schedule(self.second, after=self.after, post_result=post_result)



