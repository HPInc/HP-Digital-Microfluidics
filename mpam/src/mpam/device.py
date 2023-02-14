"""
Classes that describe hardware, but not specific devices.
"""
from __future__ import annotations

from _collections import defaultdict
from abc import ABC, abstractmethod
from enum import Enum, auto
import itertools
import logging
import random
from threading import Event, Lock, Thread, RLock
from types import TracebackType
from typing import Optional, Final, Mapping, Callable, Literal, \
    TypeVar, Sequence, TYPE_CHECKING, Union, ClassVar, Any, Iterator, \
    NamedTuple, Iterable

from matplotlib.gridspec import SubplotSpec

from erk.basic import not_None, assert_never
from erk.errors import ErrorHandler, PRINT
from mpam.engine import DevCommRequest, TimerFunc, ClockCallback, \
    Engine, ClockThread, _wait_timeout, Worker, TimerRequest, ClockRequest, \
    ClockCommRequest, TimerDeltaRequest, IdleBarrier
from mpam.exceptions import PadBrokenError
from mpam.types import XYCoord, Dir, OnOff, Delayed, Liquid, DelayType, \
    OpScheduler, Orientation, TickNumber, tick, Ticks, \
    unknown_reagent, waste_reagent, Reagent, ChangeCallbackList, \
    Callback, MixResult, State, CommunicationScheduler, Postable, \
    MonitoredProperty, DummyState, MissingOr, MISSING, RCOrder, WaitableType, \
    NO_WAIT, CSOperation, Trigger, AsyncFunctionSerializer
from quantities.SI import sec, ms, volts, deg_C
from quantities.core import Unit
from quantities.dimensions import Time, Volume, Frequency, Temperature, Voltage
from quantities.temperature import TemperaturePoint, abs_F
from quantities.timestamp import time_now, Timestamp
from argparse import Namespace
from erk.stringutils import map_str
from quantities.US import deg_F
from erk.network import local_ipv4_addr
from functools import cached_property

if TYPE_CHECKING:
    from mpam.drop import Drop, Blob
    from mpam.monitor import BoardMonitor
    from mpam.pipettor import Pipettor

logger = logging.getLogger(__name__)

PadArray = Mapping[XYCoord, 'Pad']

T = TypeVar('T')            #: A generic type variable
Modifier = Callable[[T],T]  #: A :class:`Callable` that returns a value of the same type as its argument

class BoardComponent:
    """
    A component of a :class:`Board`.  A :class:`BoardComponent` implements the
    :class:`.CommunicationScheduler` protocol by delegating to its
    associated :attr:`board`.  It can also be used to create a
    :class:`UserOperation` by calling :func:`user_operation`.
    """

    board: Final[Board] #: The containing :class:`Board`

    def __init__(self, board: Board) -> None:
        """
        Initialize the object.

        Args:
            board: the containing :class:`Board`
        """
        self.board = board

    def schedule_communication(self, cb: Callable[[], Optional[Callback]], *,
                               after: WaitableType = NO_WAIT) -> None:
        """
        Schedule communication of ``cb`` after optional delay ``after`` by
        delegating to :attr:`board`

        Args:
            cb: the callback function to schedule
        Keyword Args:
            after: an optional delay before scheduling
        """
        self.board.schedule(cb, after=after)

    def delayed(self, function: Callable[[], T], *,
                after: WaitableType) -> Delayed[T]:
        """
        Call a function after n optional delay by delegating to :attr:`board`

        Args:
            function: the function to call
        Keyword Args:
            after: an optional delay before calling
        Returns:
            A :class:`Delayed` object to which the value returned by the function will be posted.
        """
        return self.board.delayed(function, after=after)

    def user_operation(self, *, desc: Optional[Any] = None) -> UserOperation:
        """
        Create a new :class:`UserOperation` in the :attr:`board`'s
        :class:`System`

        Returns:
            the created :class:`UserOperation`
        """
        if desc is None:
            desc = self
        return UserOperation(self.board.system.engine.idle_barrier, desc=desc)

BC = TypeVar('BC', bound='BinaryComponent') #: A type variable ranging over :class:`BinaryComponent`\s

class BinaryComponent(BoardComponent, OpScheduler[BC]):
    """
    A subclass of :class:`BoardComponent` with an :class:`.OnOff` state.

    This class is parameterized by the actual subclass (:attr:`BC`) so that it
    can inherit from :class:`.OpScheduler`\[:attr:`BC`].  For example::

        class Magnet(BinaryComponent['Magnet']): ...

    This means that :class:`Magnet` can :func:`~mpam.types.OpScheduler.schedule`
    operations of type :class:`.Operation`\[:class:`Magnet`, ``V``].

    Each :class:`BinaryComponent` objects is associated with a
    :class:`.State`\[:class:`.OnOff`] object (:attr:`state`), which it delegates
    to to implement :attr:`current_state` and :attr:`on_state_change`.

    A :class:`BinaryComponent` may be :attr:`broken`, in which case attempting
    to schedule one of its :attr:`ModifyState` operations will result in
    :class:`.PadBrokenError` being raised.

    It can also be flagged as not being :attr:`live`.  The distinction between
    :attr:`broken` and :attr:`live` is somewhat confused, but the initial
    intention was that :attr:`live` was used to identify pads on a board that
    couldn't be used by design and :attr:`broken` was for pads that were
    discovered to be non-functional.

    Args:
        BC: The actual subclass of :class:`BinaryComponent`
    """
    state: Final[State[OnOff]]  #: The associated :class:`.State`\[:class:`.OnOff`]
    can_toggle: Final[bool]     #: Is changing :attr:`current_state` allowed?
    on_illegal_toggle: Final[ErrorHandler]
    """
    :class:`.ErrorHandler` invoked when :attr:`can_toggle` is ``False`` and an
    attempt is made to change state.
    """
    broken: bool                #: Is the :class:`BinaryComponent` broken?
    live: bool                  #: Is the :class:`BinaryComponent` live?

    def __init__(self, board: Board, *,
                 state: Union[State[OnOff], OnOff],
                 live: bool = True,
                 can_toggle: bool = True,
                 on_illegal_toggle: ErrorHandler = PRINT,
                 ) -> None:
        """
        Initialize the object.

        All :class:`BinaryComponent`\s start out with :attr:`broken` being
        ``False``.

        Args:
            board: the containing :class:`Board`
        Keyword Args:
            state: the associated :class:`.State`\[:class:`.OnOff`]
            can_toggle: is changing :attr:`current_state` allowed?
            live: is the :class:`BinaryComponent` live?
        """
        super().__init__(board)
        if isinstance(state, OnOff):
            state = DummyState(initial_state=state)
        self.state = state
        assert can_toggle or state.has_state, "Untoggleable BinaryComponents must have initial states"
        self.can_toggle = can_toggle
        self.on_illegal_toggle = on_illegal_toggle
        self.broken = False
        self.live = live

    @property
    def current_state(self) -> OnOff:
        """
        The current value.  Implemented by delegating to :attr:`state`. When
        this value is set to a value not equal to the prior value, callbacks
        registerd to :attr:`on_state_change` are called.
        """
        return self.state.current_state

    @current_state.setter
    def current_state(self, val: OnOff) -> None:
        def cannot_change() -> str:
            requested = "on" if val else "off"
            return f"Cannot turn {requested} {self}"
        if self.on_illegal_toggle.expect_true(self.can_toggle or val is self.current_state,
                                              cannot_change):
            self.state.current_state = val

    @property
    def on_state_change(self) -> ChangeCallbackList[OnOff]:
        """
        The :class:`.ChangeCallbackList` monitoring :attr:`current_state`.
        """
        return self.state.on_state_change

    def __repr__(self) -> str:
        tname = type(self).__name__
        if self.state.has_state:
            return f"{tname}({self.current_state})"
        else:
            return f"{tname}(--no value--)"


    class ModifyState(CSOperation[BC, OnOff]):
        """
        An :class:`~.Operation` that modifies the :attr:`~BinaryComponent.state`
        of a :class:`BinaryComponent`.

        The :class:`.ModifyState` object is associated with a :class:`Modifier`
        function (:attr:`mod`) that's used to compute the new value based on the
        old.

        The :class:`BinaryComponent` class (and, therefore, its subclasses) have
        premade instances for the common cases of
        :attr:`~BinaryComponent.TurnOn`, :attr:`~BinaryComponent.TurnOff`, and
        :attr:`~BinaryComponent.Toggle`
        """
        def _schedule_for(self, obj: BC, *,
                          post_result: bool = True,
                          ) -> Delayed[OnOff]:
            """
            The implementation of :func:`schedule_for`. Calls
            :func:`~mpam.types.State.realize_state` on ``obj``'s
            :attr:`~BinaryComponent.state`.

            :meta public:
            Args:
                obj: the :class:`BinaryComponent` object to schedule the operation for
            Keyword Args:
                post_result: whether to post the resulting value to the returned future object
            Returns:
                a :class:`Delayed`\[:class:`.OnOff`] future object to which the resulting
                value will be posted unless ``post_result`` is ``False``
            Raises:
                PadBrokenError: if ``obj`` is :attr:`~BinaryComponent.broken`
            """
            if obj.broken:
                raise PadBrokenError(obj)
            mod = self.mod
            future = Postable[OnOff]()
            # state_obj = obj.state

            def cb() -> Optional[Callback]:
                old = obj.current_state
                new = mod(old)
                # logging.info(f"Setting {obj} to {new}")
                obj.state.realize_state(new)
                obj.current_state = new
                # logging.info(f"Back from setting {obj} val = {obj.state}")
                finish: Optional[Callback] = None if not post_result else (lambda : future.post(old))
                return finish

            obj.board.schedule(cb)
            return future

        def __init__(self, mod: Modifier[OnOff]) -> None:
            """
            Initialize the object

            Args:
                mod: a function to compute the new value based on the old
            """
            self.mod: Final[Modifier[OnOff]] = mod
            """the function to compute the new value based on the old"""

    @staticmethod
    def SetState(val: OnOff) -> ModifyState:
        """
        A :attr:`ModifyState` that sets the state to a specific value.

        Args:
            val: the desired :class:`.OnOff` value
        Returns:
            :attr:`~BinaryComponent.TurnOn` or :attr:`~BinaryComponent.TurnOff`
        """
        return BinaryComponent[BC].TurnOn if val is OnOff.ON else BinaryComponent[BC].TurnOff


    TurnOn: ClassVar[ModifyState]   #: An :class:`.Operation` to turn on a :class:`BinaryComponent`
    TurnOff: ClassVar[ModifyState]  #: An :class:`.Operation` to turn on a :class:`BinaryComponent`
    Toggle: ClassVar[ModifyState]   #: An :class:`.Operation` to toggle the state of a :class:`BinaryComponent`

    ...

BinaryComponent[BC].TurnOn = BinaryComponent.ModifyState(lambda _: OnOff.ON)
BinaryComponent[BC].TurnOff = BinaryComponent.ModifyState(lambda _: OnOff.OFF)
BinaryComponent[BC].Toggle = BinaryComponent.ModifyState(lambda s: ~s)

class PipettingTarget(ABC):
    """
    A place a :class:`.Pipettor` can add :class:`.Liquid` to or take it from.

    A :class:`PipettingTarget` establishes a protocol with respect to to its
    (optional) associated :attr:`pipettor`:

        * When the :class:`.Pipettor` is in place and ready to add or remove
          :class:`.Liquid`, it calls :func:`prepare_for_add` or
          :func:`prepare_for_remove`, which does not return until it is safe for the
          :class:`.Pipettor` to perform the action.

        * When the action is done, the :class:`.Pipettor` calls
          :func:`pipettor_added_` or :func:`pipettor_remove` to signal completion
          and inform the :class:`PipettingTarget` of the :class:`.Reagent`, and
          :class:`.Volume` involved and whether that was the final such transfer to
          satisfy the request.


    Note:
        :class:`PipettingTarget` is an abstract class.  Concrete subclasses must
        define :attr:`contents`, :func:`prepare_for_add`,
        :func:`prepare_for_remove`, :func:`pipettor_added`, and
        :func:`pipettor_removed`.  If not overridden, :attr:`pipettor` will be
        ``None``, which will likely cause things to complain if a transfer is
        requested.
    """

    @property
    @abstractmethod
    def removable_liquid(self) -> Optional[Liquid]:
        """
        The :class:`.Liquid` that could be removed via this
        :class:`PipettingTarget` or ``None`` if there is no such
        :class:`.Liquid`.

        Note:
            This is an abstract attribute which must be overridden by concrete
            subclasses.
        """
        ...

    @property
    def pipettor(self) -> Optional[Pipettor]:
        """
        The :class:`.Pipettor` associated with this :class:`PipettingTarget` or
        ``None`` if there is no such :class:`.Pipettor`.

        By default, it will be ``None``.
        """
        return None

    @abstractmethod
    def prepare_for_add(self) -> None:
        """
        Block until it is safe for a :class:`.Pipettor` to add :class:`.Liquid`.
        This method is called when the :class:`.Pipettor` is in position.

        Note:
            This is an abstract attribute which must be overridden by concrete
            subclasses.
        """
        ...

    @abstractmethod
    def prepare_for_remove(self) -> None:
        """
        Block until it is safe for a :class:`.Pipettor` to remove
        :class:`.Liquid`. This method is called when the :class:`.Pipettor` is
        in position.

        Note:
            This is an abstract attribute which must be overridden by concrete
            subclasses.
        """
        ...


    @abstractmethod
    def pipettor_added(self, reagent: Reagent, volume: Volume, *, # @UnusedVariable
                       mix_result: Optional[MixResult], # @UnusedVariable
                       last: bool) -> None: # @UnusedVariable
        """
        Called when the :class:`.Pipettor` has finished adding :class:`.Liquid`.
        If ``mix_result`` is not ``None``, it should be used as the result of
        mixing the delivered :class:`.Liquid` to what is already there.  If
        ``last`` is ``False``, there will be at least one more transfer before
        the overall transfer operation is complete.

        Note:
            This is an abstract attribute which must be overridden by concrete
            subclasses.

        Args:
            reagent: the :class:`.Reagent` added
            volume: the :class:`.Volume` of :class:`.Reagent` added
        Keyword Args:
            mix_result: the (optional) result of mixing the added
                        :class:`.Liquid` with what's already there.
            last: ``True`` if this is the last transfer in a transfer request.
        """
        ...

    @abstractmethod
    def pipettor_removed(self, reagent: Reagent, volume: Volume, *, # @UnusedVariable
                         last: bool) -> None: # @UnusedVariable
        """
        Called when the :class:`.Pipettor` has finished removing
        :class:`.Liquid`. If ``last`` is ``False``, there will be at least one
        more transfer before the overall transfer operation is complete.

        Note:
            This is an abstract attribute which must be overridden by concrete
            subclasses.

        Args:
            reagent: the :class:`.Reagent` removed
            volume: the :class:`.Volume` of :class:`.Reagent` removed
        Keyword Args:
            last: ``True`` if this is the last transfer in a transfer request.
        """
        ...

class DropLoc(ABC, CommunicationScheduler):
    """
    A location that can hold a :class:`.Drop` and participate in a :class:`.Blob`.

    It maintains a :class:`.ChangeCallbackList` for its :attr:`drop` attribute
    to which callbacks can be added by means of :attr:`on_drop_change`.

    :attr:`checked_drop` is the same as :attr:`drop`, but it is guaranteed to be
    a :class:`.Drop`, raising a :class:`.TypeError` if :attr:`drop` is ``None``.

    Note:
        :class:`DropLoc` is an abstract class.  In addition to the abstract
        methods inherited from :class:`.CommunicationScheduler`, concrete
        subclasses must also define :func:`compute_neighbors_for_blob`.
    """
    blob: Optional[Blob] = None     #: The :class:`.Blob`, if any, this :class:`DropLoc` participates in
    _neighbors_for_blob: Optional[Sequence[DropLoc]] = None

    drop: MonitoredProperty[Optional[Drop]] = MonitoredProperty(default=None)
    """
    The :class:`.Drop`, if any, at this location.  When this value changes,
    callbacks registered to :attr:`on_drop_change` are called.
    """

    on_drop_change: ChangeCallbackList[Optional[Drop]] = drop.callback_list
    """
    The :class:`.ChangeCallbackList` monitoring :attr:`drop`.
    """


    @property
    def checked_drop(self) -> Drop:
        """
        The :class:`.Drop` at this location.  If there is none (i.e., if
        :attr:`drop` is ``None``), a :class:`.TypeError` will be raised.
        """
        if self.drop is not None:
            return self.drop
        print(f"Drop at {self}: {self.drop}")
        raise TypeError(f"{self} has no drop")


    @property
    def neighbors_for_blob(self) -> Sequence[DropLoc]:
        """
        The neighboring :class:`DropLoc`\s that could be part of the same :class:`.Blob`.

        The first time this is referenced, :func:`compute_neighbors_for_blob` is
        called, and the value is cached.
        """
        ns = self._neighbors_for_blob
        if ns is None:
            ns = self._neighbors_for_blob = self.compute_neighbors_for_blob()
        return ns

    @abstractmethod
    def compute_neighbors_for_blob(self) -> Sequence[DropLoc]:
        """
        The list of neighboring :class:`DropLoc`\s that could be part of the
        same :class:`.Blob`.  This is called the first time
        :attr:`neighbors_for_blob` is referenced, and the value is cached.

        Note:
            This is an abstract method which must be defined by concrete
            subclasses.

        Returns:
            the :class:`Sequence` of neighbors
        """
        ...


class LocatedPad:
    """
    An object with an associated :class:`.XYCoord`.  Provides :attr:`row` and
    :attr:`column` attributes that extract from the :attr:`location`.

    """
    location: Final[XYCoord]    #: the :class:`.XYCoord` of the object

    @property
    def row(self) -> int:
        """
        An alias for :attr:`~.LocatedPad.location` ``.``:attr:`~.XYCoord.y`
        """
        return self.location.y
    @property
    def column(self) -> int:
        """
        An alias for :attr:`~.LocatedPad.location` ``.``:attr:`~.XYCoord.x`
        """
        return self.location.x


    def __init__(self, loc: XYCoord) -> None:
        """
        Initialize the object

        Args:
            loc: the :class:`.XYCoord`
        """
        self.location = loc
        
class TempControllable:
    """
    An object that can have an associated an associated :class:`TemperatureControl`
    """
    _temperature_control: Optional[TemperatureControl] = None

    @property
    def temperature_control(self) -> Optional[TemperatureControl]:
        """
        The :class:`TemperatureControl`, if any that affects this :class:`TempControllable`
        """
        return self._temperature_control
    
    @property
    def current_temperatures(self) -> Optional[TemperaturePoint]:
        h = self.temperature_control
        if h is not None:
            return h.current_temperature
        if isinstance(self, BoardComponent):
            return self.board.ambient_temperature
        return None
    
    @property
    def heater(self) -> Optional[Heater]:
        tc = self.temperature_control
        if tc is None or not isinstance(tc, Heater):
            return None
        return tc
    
    @property
    def chiller(self) -> Optional[Chiller]:
        tc = self.temperature_control
        if tc is None or not isinstance(tc, Chiller):
            return None
        return tc
    
    
    

class Pad(BinaryComponent['Pad'], DropLoc, LocatedPad, TempControllable):
    """
    A pad, typically in the main array of its associated
    :class:`Board` (i.e., not in a :class:`Well`).

    *   As a :class:`BinaryComponent`, it has a :attr:`~BoardComponent.board` and a
        :attr:`~BinaryComponent.current_state`, it can act as both a
        :class:`.CommunicationScheduler` and a
        :class:`.OpScheduler`\[:class:`Pad`], and it supports
        :func:`~BinaryComponent.on_state_change`.  It also has an unchangeable
        version of :attr:`~BinaryComponent.live` (:attr:`exists`) that can be
        used to indicate that not only is the :class:`Pad` not currently live,
        but it never will be.

        To initialize this asspect of the :class:`Pad`, when it is created, it
        must be associated with a :class:`.State`\[:class:`.OnOff`] object that
        knows how to effect any changes on a physical device (via its
        :func:`~.State.realize_state` method).  If nothing needs to be done, a
        :class:`.DummyState` may be used.

    * As a :class:`DropLoc`, it had an optional :attr:`~DropLoc.drop` and
      :attr:`~DropLoc.blob`, and it supports :func:`~DropLoc.on_drop_change`. It
      is :attr:`empty` whenever :attr:`drop` is ``None``.

    * As a :class:`LocatedPad`, it has a :attr:`~LocatedPad.location`, a
      :attr:`~LocatedPad.row`, and a :attr:`~LocatedPad.column`.

    In addition, a :class:`Pad` may be associated with a :class:`Magnet`
    (:attr:`magnet`), a :class:`Well` (:attr:`well`, i.e., as the
    :class:`Well`'s :attr:`~Well.exit_pad`), a :class:`TemperatureControl`
    (:attr:`TemperatureControl`), an :class:`ExtractionPoint` (:attr:`extraction_point`),
    and a dried :class:`.Liquid` (:attr:`dried_liquid`).

    Whenever the :attr:`~BinaryState.current_state` changes,
    :attr:`~BoardComponent.board`'s :func:`~Board.journal_state_change` is
    called with the (necessarily different) old and new values to prep for drop
    motion inference.

    **Neighbors:**

        A :class:`Pad` can enumerate neighboring :class:`Pad`\s in several ways:

            * :func:`neighbor` takes a :class:`.Dir` and returns the neighboring pad
              in that direction, if one exists, optionally including pads with
              :attr:`exists` set to ``False``.

            * :attr:`all_neighbors` is the (up to 8) neighboring pads in all directions.

            * :attr:`neighbors` is the (up to 4) neighboring pads in the cardinal
              directions.

            * :attr:`corner_neighbors` is the (up to 4) neighboring pads in the
              non-cardinal directions.

            * :func:`compute_neighbors_for_blob` (the implementation of
              :attr:`~DropLoc.neighbors_for_blob`) is :attr:`neighbors` plus the
              :attr:`~Well.gate` of :attr:`well` (if it isn't ``None``).

            * :attr:`between_pads` is a mapping from :class:`Pad`\s two steps away
              in any cardinal direction to the :class:`Pad` one step away (i.e., the
              :class:`Pad` between that one and this one).

    **Traffic Control and Reservation**:

        The :class:`Pad` provides a rudimentary form of *traffic control* for
        :class:`.Drop` motion.  The basic notion is that

            * A thread participating in this traffic control will only
              move a :class:`.Drop` onto a :class:`Pad` if it has
              successfully called :func:`reserve` on it.  This will
              only succeed if :attr:`reserved` is ``False``, and it
              will have the side-effect of setting :attr:`reserved` to
              ``True``.

            * Before calling :func:`reserve`, the thread will first
              determine that the :class:`Pad` is :attr:`safe` (or
              :func:`safe_except()` for the :class:`Pad` or
              :class:`Well` that is the source of the motion). A
              :class:`Pad` is :attr:`safe` if it is :class:`empty` and
              none of its neighboring :class:`Pad`\s are
              :attr:`reserved` or have a :class:`.Drop`.

            * After the :class:`.Drop` has moved to the :class:`.Pad`,
              the thread should set call :func:`unreserve` to clear
              the reservation on the :class:`Pad`.

    Warning:
        This protocol is not thread-safe.  It probably should be made to be.
        The original expectation was that it would only be run from within
        the :class:`.ClockThread`

    Example:
        The following code might be used to move a :class:`.Drop` from a
        ``source`` :class:`.Pad` to a ``target`` :class:`.Pad`.  The
        :func:`Board.before_tick` method takes a :class:`Callable` that
        returns ``None`` when it is done and a number of :class:`.Tick`\s to
        wait until trying again when it is not. ::

            def do_it() -> Iterator[Optional[Ticks]]:
                one_tick = 1*ticks

                while not target.safe_except(source):
                    yield one_tick
                while not target.reserve():
                    yield one_tick

                with system.batched():
                    target.schedule(Pad.TurnOn)
                    source.schedule(Pad.TurnOff)

                    board.after_tick(target.unreserve)

                return None


            iterator = do_it()
            board.before_tick(lambda: next(iterator))

    **Traffic Control and Reservation**:

        After :class:`.Liquid` is added to or removed from a :class:`Pad`,
        typically via its :attr:`extraction_point`, :func:`liquid_added` or
        :func:`liquid_removed` are called.  This triggers any inferred
        :class:`.Drop` motion due to the transfer.

    Note:
        This :class:`.Drop` motion inference is asynchronous to any inference
        due to :class:`Pad` state changes.  This is because transfers are
        typically asynchronouse with respect to the :class:`Board`'s clock.

    """
    exists: Final[bool]         #: Is this a real :class:`Pad`

    # broken: bool

    _pads: Final[PadArray]
    _dried_liquid: Optional[Drop]
    _neighbors: Optional[Sequence[Pad]] = None
    _all_neighbors: Optional[Sequence[Pad]] = None
    _between_pads: Optional[Mapping[Pad,Pad]] = None
    _well: Optional[Well] = None
    _magnet: Optional[Magnet] = None
    # _temperature_control: Optional[TemperatureControl] = None
    _extraction_point: Optional[ExtractionPoint] = None

    # TODO: The name has to be specified, because otherwise it would be
    # "_reserved", which would clobber this attribute.  I'm planning on adding
    # the ability to declare a MonitoredProperty to be read-only, which would
    # give it a private_set() method (or something similar) to do the actual
    # modification.  When that's in, we can get rid of the val_attr.
    _reserved: MonitoredProperty[bool] = MonitoredProperty(default=False)

    on_reserved_change: ChangeCallbackList[bool] = _reserved.callback_list
    """
    The :class:`.ChangeCallbackList` monitoring :attr:`reserved`
    """

    @property
    def well(self) -> Optional[Well]:
        """
        The :class:`Well`, if any, that this :class:`Pad` is the :attr:`~Well.exit_pad` for
        """
        return self._well

    @property
    def magnet(self) -> Optional[Magnet]:
        """
        The :class:`Magnet`, if any that affects this :class:`Pad`
        """
        return self._magnet

    # @property
    # def TemperatureControl(self) -> Optional[TemperatureControl]:
    #     """
    #     The :class:`TemperatureControl`, if any that affects this :class:`Pad`
    #     """
    #     return self._temperature_control

    @property
    def extraction_point(self) -> Optional[ExtractionPoint]:
        """
        The :class:`ExtractionPoint`, if any that affects this :class:`Pad`
        """
        return self._extraction_point


    @property
    def dried_liquid(self) -> Optional[Drop]:
        """
        The dried :class:`.Liquid`, if any at this :class:`Pad`
        """
        return self._dried_liquid

    @property
    def neighbors(self) -> Sequence[Pad]:
        """
        Neighboring :class:`Pad`\s (that :attr:`exist`) in the cardinal directions
        """
        ns = self._neighbors
        if ns is None:
            ns = [n for d in (Dir.N,Dir.S,Dir.E,Dir.W) if (n := self.neighbor(d)) is not None]
            self._neighbors = ns
        return ns

    @property
    def all_neighbors(self) -> Sequence[Pad]:
        """
        Neighboring :class:`Pad`\s (that :attr:`exist`) in any direction
        """
        ns = self._all_neighbors
        if ns is None:
            ns = [n for d in Dir if (n := self.neighbor(d)) is not None]
            self._all_neighbors = ns
        return ns

    @property
    def corner_neighbors(self) -> Sequence[Pad]:
        """
        Neighboring :class:`Pad`\s (that :attr:`exist`) in corner directions
        """
        ns = self._neighbors
        if ns is None:
            ns = [n for d in (Dir.NE,Dir.SE,Dir.SW,Dir.NW) if (n := self.neighbor(d)) is not None]
            self._neighbors = ns
        return ns

    @property
    def between_pads(self) -> Mapping[Pad, Pad]:
        """
        A mapping from :class:`Pad`\s two steps away in cardinal directions to
        :class:`Pad`\s one step away.
        """
        bps: Optional[Mapping[Pad,Pad]] = getattr(self, '_between_pads', None)
        if bps is None:
            bps = {p: m for d in Dir.cardinals()
                   if (m := self.neighbor(d)) is not None
                        and (p := m.neighbor(d)) is not None}
            self._between_pads = bps
        return bps

    reserved: bool = _reserved.getter
    """
    Has the :class:`Pad` been reserved?
    """

    def __init__(self, loc: XYCoord, board: Board,
                 state: State[OnOff], *, exists: bool = True) -> None:
        """
        Initialize the object

        Args:
            loc: the :class:`Pad`'s location
            board: the :class:`Pad`'s board
            state: the associated :class:`.State`\[:class:`.OnOff`]
        Keyword Args:
            exists: whether the :class:`Pad` is real
        """
        BinaryComponent.__init__(self, board, state=state, live=exists)
        LocatedPad.__init__(self, loc)
        DropLoc.__init__(self)
        self.exists = exists
        # self.broken = False
        self._pads = board.pad_array
        self._dried_liquid = None
        def journal_change(old: OnOff, new: OnOff) -> None:
            if old is not new:
                board.journal_state_change(self, new)
        self.on_state_change(journal_change, key=f"Journal Change {self}")

    def __repr__(self) -> str:
        return f"Pad({self.column},{self.row})"

    def neighbor(self, d: Dir, *, only_existing: bool = True) -> Optional[Pad]:
        """
        The neighboring :class:`Pad` on the :class:`Board` in the given
        :`Dir`.  Returns ``None`` if there is no such :class:`Pad`. If
        ``only_existing`` is set to ``True`` (default value), the
        returned :class:`Pad` also needs to have :attr:`exists` set to
        ``True``.

        Args:
            d: the :class:`Dir` to look

            only_existing: only include pads wtih :attr:`exists` set
                to ``True`` (default: ``True``)
        Returns:
            the neighboring :class:`Pad` if one exists, otherwise ``None``.
        """
        n = self.board.orientation.neighbor(d, self.location)
        p = self._pads.get(n, None)
        if p is None or only_existing and not p.exists:
            return None
        return p

    @property
    def empty(self) -> bool:
        """
        ``True`` when :attr:`~DropLoc.drop` is ``None``
        """
        return self.drop is None

    @property
    def safe(self) -> bool:
        """
        Is it safe to :func:`reserve` the :class:`Pad`?  A :class:`Pad` is
        safe if it is :attr:`empty` and all of its neighbors are
        :attr:`empty` and none are :attr:`reserved`.

        """
        w = self.well
        if w is not None and (w.gate_on or w.gate_reserved):
            return False
        return self.empty and all(
            map(lambda n : n.empty and not n.reserved, self.all_neighbors))

    def safe_except(self, padOrWell: Union[Pad, Well]) -> bool:
        """
        Is it safe to :func:`reserve` the :class:`Pad` disregarding a specific
        :class:`Pad` or :class:`Well`?  This is identical to :attr:`safe` except
        that the :class:`Pad` or :class:`Well` (which are presumed to be the
        location that a :class:`.Drop` is moving from) are ignored.
        """
        if not self.empty:
            return False
        w = self.well
        if w is not None and w is not padOrWell and (w.gate_on or w.gate_reserved):
            return False
        for p in self.all_neighbors:
            if p is not padOrWell and (not p.empty or p.reserved):
                return False
        return True


    def reserve(self) -> bool:
        """Reserve the :class:`Pad`.  Returns ``False`` if the :class:`Pad` is
        already :attr:`reserved`, otherwise sets :attr:`reserved` to ``True``
        and returns ``True``.

        Returns:
            `True` if the :class:`Pad` has been successfly reserved
            and `False` if the :class:`Pad` cannot be reserved because
            it has already been reserved.
        """
        if self._reserved:
            return False
        self._reserved = True
        return True

    def unreserve(self) -> None:
        """
        Clears the reservation on the :class:`Pad`. If the pad is not
        reserved, it has no effect.

        """
        self._reserved = False

    def liquid_added(self, liquid: Liquid, *, mix_result: Optional[MixResult] = None) -> None:
        """
        Note that :class:`.Liquid` was added to the :class:`Pad`.  Typically
        called by the :class:`Pad`'s :attr:`extraction_point`.

        This is treated as an asynchronous operation.  A new
        :class:`ChangeJournal` is created and
        :func:`~ChangeJournal.process_changes()` is called so that :class:`Blob`
        motion happens immediately.

        Args:
            liquid: the added :class:`.Liquid`
        Keyword Args:
            mix_result: an optional :class:`.Reagent` specifying the result of
                        mixing ``liquid`` with the current contents of the :class:`Pad`.
        """
        # I'm treating adding and removing liquid as asynchronous
        journal = ChangeJournal()
        journal.note_delivery(self, liquid, mix_result=mix_result)
        journal.process_changes()
        # self.board.change_journal.note_delivery(self, liquid, mix_result=mix_result)

    def liquid_removed(self, volume: Volume) -> None:
        """
        Note that a :class:`.Volume` of :class:`.Liquid` was removed from the
        :class:`Pad`.  Typically called by the :class:`Pad`'s
        :attr:`extraction_point`.

        This is treated as an asynchronous operation.  A new
        :class:`ChangeJournal` is created and
        :func:`~ChangeJournal.process_changes()` is called so that :class:`Blob`
        motion happens immediately.

        Args:
            volume: the :class:`.Volume` of :class:`.Liquid` removed
        """
        # I'm treating adding and removing liquid as asynchronous
        journal = ChangeJournal()
        journal.note_removal(self, volume)
        journal.process_changes()
        # self.board.change_journal.note_removal(self, volume)

    def compute_neighbors_for_blob(self)->Sequence[DropLoc]:
        """
        The list of neighboring :class:`DropLoc`\s that could be part of the
        same :class:`.Blob`.  This is :attr:`neighbors` plus the
        :attr:`~Well.gate` of :attr:`well`, if it is not ``None``.

        Returns:
            the :class:`Sequence` of neighbors
        """
        if (well := self.well) is None:
            return self.neighbors
        else:
            return [*self.neighbors, well.gate]


# WellPadLoc = Union[tuple['WellGroup', int], 'Well']

class WellPad(BinaryComponent['WellPad'], DropLoc):
    """
    A pad inside a :class:Well`.

    *   As a :class:`BinaryComponent`, it has a :attr:`~BinaryComponent.board` and a
        :attr:`~BinaryComponent.current_state`, it can act as both a
        :class:`.CommunicationScheduler` and a
        :class:`.OpScheduler`\[:class:`Pad`], and it supports
        :func:`~BinaryComponent.on_state_change`.

        To initialize this asspect of the :class:`Pad`, when it is created, it
        must be associated with a :class:`.State`\[:class:`.OnOff`] object that
        knows how to effect any changes on a physical device (via its
        :func:`~.State.realize_state` method).  If nothing needs to be done, a
        :class:`.DummyState` may be used.

    * As a :class:`DropLoc`, it had an optional :attr:`~DropLoc.drop` and
      :attr:`~DropLoc.blob`, and it supports :func:`~DropLoc.on_drop_change`. It
      is :attr:`empty` whenever :attr:`drop` is ``None``.

    A :class:`WellPad` that is its :attr:`well`'s :attr:`~Well.gate` will be an
    instance of the subclass :class:`WellGate`.  The attribute :attr:`is_gate`
    can be used to distinguish gates from interior :class:`WellPad`\s.

    Each :class:`Well` had a list of :attr:`~Well.shared_pads` that enumerates
    the the interior pads inside it.  A :class:`WellPad`'s :attr:`index`
    specifies its position in this list.  If it is a :class:`WellGate`,
    :attr:`index` will be ``-1``.  This attribute is set by means of
    :func:`set_location`, called within :func:`Well.__init__`.  (The
    :class:`WellPad`s are created before the :class:`Well` and passed into its
    :func:`~Well.__init__` method, which calls :func:`set_location` to establish
    :attr:`well` and :attr:`index`.)

    Whenever the :attr:`~BinaryState.current_state` changes,
    :attr:`~BoardComponent.board`'s :func:`~Board.journal_state_change` is
    called with the (necessarily different) old and new values to prep for drop
    motion inference.

    """
    well: Well  #: The associated :class:`Well`
    index: int
    """
    The index of the :class:`WellPad` in :attr:`well`'s
    :attr:`~Well.shared_pads` or ``-1`` if :attr:`is_gate` is ``True``
    """
    _neighbor_indices: Final[Sequence[int]]
    _neighbors: Optional[Sequence[DropLoc]] = None

    @property
    def is_gate(self) -> bool:
        """
        Is this :attr:`well`'s :attr:`~Well.gate`?
        """
        return False

    def __init__(self, board: Board,
                 state: State[OnOff], *,
                 live: bool = True,
                 neighbors: Sequence[int]) -> None:
        """
        Initialize the object.

        This does not set :attr:`well` or :attr:`index`, because
        :class:`WellPad`/s are created before :class:`Well`s.  Rather,
        :func:`Well.__init__` calls :func:`set_location`, which sets them.

        Args:
            board: the containing :class:`Board`
            state: the associated :class:`.State`\[:class:`.OnOff`]
        Keyword Args:
            live: is the :class:`WellPad` live?
            neighbors: the :attr:`index` values of :class:`WellPad`\s that should
                       be included in :attr:`~DropLoc.neighbors_for_blob`.
        """
        BinaryComponent.__init__(self, board, state=state, live=live)
        DropLoc.__init__(self)
        self._neighbor_indices = neighbors
        # print(f"{self}.live = {self.live}")
        def journal_change(old: OnOff, new: OnOff) -> None:
            if old is not new:
                board.journal_state_change(self, new)
        self.on_state_change(journal_change, key=f"Journal Change {self}")


    def __repr__(self) -> str:
        well: Optional[Well] = getattr(self, 'well', None)
        if well is None:
            return f"WellPad(unassigned, {id(self)})"
        elif self.is_gate:
            return f"WellPad({well}[gate])"
        else:
            # return f"WellPad({well}[{self.index}]"
            return f"WellPad({self.index}, {well})"

    def set_location(self, well: Well, index: int) -> None:
        """
        Set the :attr:`well` and :attr:`index` attributes

        Args:
            well: the associated :class:`Well`
            index: the value for :attr:`index`
        """
        self.well = well
        self.index = index

    def compute_neighbors_for_blob(self)->Sequence[DropLoc]:
        """
        The list of neighboring :class:`DropLoc`\s that could be part of the
        same :class:`.Blob`.  This is called the first time
        :attr:`~DropLoc.neighbors_for_blob` is referenced, and the value is
        cached.

        This will be the :class:`WellPad`\s corresponding to the ``neighbors``
        indices provided to :func:`__init__`.  If :attr:`is_gate` is ``True``
        (i.e., this is a :class:`WellGate`), it will also include :attr:`well`'s
        :attr:`~Well.exit_pad`.

        Returns:
            the :class:`Sequence` of neighbors
        """
        ns = self._neighbors
        if ns is None:
            well = self.well
            ns = tuple(well.gate if n==-1 else well.shared_pads[n] for n in self._neighbor_indices)
            self._neighbors = ns
        return ns

class WellGate(WellPad, LocatedPad):
    """
    A :class:`WellPad` that is its :attr:`well`'s :attr:`~Well.gate`.

    As a :class:`LocatedPad`, it has a :attr:`~LocatedPad.location`, which is
    computed based on its :attr:`~WellPad.well`'s :attr:`~Well.exit_pad`.
    """
    @property
    def is_gate(self) -> bool:
        """
        ``True`` because this is :attr:`~WellPad.well`'s :attr:`~Well.gate`.
        """
        return True

    def __init__(self, board: Board,
                 exit_pad: Pad,
                 exit_dir: Dir,
                 state: State[OnOff], *,
                 neighbors: tuple[int, ...],
                 live: bool = True) -> None:
        """
        Initialize the object.

        :attr:`~LocatedPad.location` is computed based on ``exit_pad`` and
        ``exit_dir``.

        Args:
            board: the containing :class:`Board`
            exit_pad: the :class:`Pad` that will be :attr:`~WellPad.well`'s
                      :attr:~Well.exit_pad`
            exit_dir: the direction from this :class:`WellGate` to ``exit_pad``
            state: the associated :class:`.State`\[:class:`.OnOff`]
        Keyword Args:
            live: is the :class:`WellPad` live?
            neighbors: the :attr:`index` values of :class:`WellPad`\s that should
                       be included in :attr:`~DropLoc.neighbors_for_blob`.
        """
        WellPad.__init__(self, board, state, live=live, neighbors=neighbors)
        loc = board.orientation.neighbor(exit_dir.opposite, exit_pad.location)
        LocatedPad.__init__(self, loc)

    def __repr__(self) -> str:
        well: Optional[Well] = getattr(self, 'well', None)
        if well is None:
            return f"WellGate(unassigned, {id(self)})"
        else:
            return f"WellGate({well})"


    def compute_neighbors_for_blob(self)->Sequence[DropLoc]:
        """
        The list of neighboring :class:`DropLoc`\s that could be part of the
        same :class:`.Blob`.  This is called the first time
        :attr:`~DropLoc.neighbors_for_blob` is referenced, and the value is
        cached.

        This will be the :class:`WellPad`\s corresponding to the ``neighbors``
        indices provided to :func:`__init__` plus :attr:`well`'s
        :attr:`~Well.exit_pad`.

        Returns:
            the :class:`Sequence` of neighbors
        """
        ns = self._neighbors
        if ns is None:
            ns = (self.well.exit_pad, *super().compute_neighbors_for_blob())
            self._neighbors = ns
        return ns


class WellState(Enum):
    """
    An enumeration of states a :class:`Well` can be in.  This is used as the
    target of a :class:`Well.TransitionTo` :class:`.Operation`, most often as
    part of :class:`.Drop.DispenseFrom` or :class:`.Drop.EnterWell` (or the
    corresponding methods in :class:`.Path`)

    Note that these are target states.  While a :class:`Well` is transitioning
    (via a :class:`WellMotion`), it will not be in any of them.
    """
    EXTRACTABLE = auto()    #: The contents are in positition to be removed by a :class:`.Pipettor`
    INJECTABLE = auto()
    READY = auto()          #: The :class:`Well` is ready to move to a different :class:`WellState`
    DISPENSED = auto()      #: The :class:`Well` has just dispensed a :class:`.Drop`
    ABSORBED = auto()       #: The :class:`Well` has just absorbed a :class:`.Drop`

# -1 is the well's gate pad.  Others are indexes into the shared_pads list
WellOpStep = Sequence[int]
"""
The :attr:`~WellPad.index` values of the :class:`WellPad`\s that should be
:attr:`.OnOff.ON` in a given step.

``-1`` indicates the :class:`Well`'s :attr:`~Well.gate`.  Non-negative numbers
index into the :class:`Well`'s :attr:`~Well.shared_pads`.
"""
WellOpStepSeq = Sequence[WellOpStep]
"""
A sequence of :attr:`WellOpStep`\s
"""
WellOpSeqDict = Mapping[tuple[WellState,WellState], WellOpStepSeq]
"""
A :class:`Mapping` from source-target pairs of :class:`WellState`\s to
:class:`WellOpStepSeq`\s.
"""


class GateStatus(Enum):
    """
    The status of :class:`WellGate`\s during a :class:`WellMotion` transition.
    This is used to determine whether it is safe for another :class:`Well` in
    the same :class:`DispenseGroup` to piggyback on the motion when going to the
    same target :class:`WellState`.  This takes advantage of the fact that
    shared :class:`WellPad`\s on all :class:`Well`\s in the
    :class:`DispenseGroup` turn on and off together, so except for the gate, the
    :class:`Well` has been following along.  If it is safe to do so, this can
    result in efficiencies by having multiple :class:`Well`\s dispense or absorb
    at the same time, even if the requests are staggered.

    If the status is :attr:`NOT_YET`, the gates have not yet turned on, so it is
    known to be safe.  If it is :attr:`JUST_ON`, it is safe, but the new
    :class:`Well`'s gate needs to be scheduled to turn on.  If it is
    :attr:`UNSAFE`, the :class:`Well` cannot piggyback and must wait until the
    current motion is done.
    """
    NOT_YET = auto()    #: The :class:`WellGate`\s have no yet turned on
    JUST_ON = auto()    #: The :class:`WellGate`\s are scheduled to turn on
    UNSAFE = auto()     #: It is known to be unsafe.

class WellMotion:
    """
    A transition of (as subset of) the :class:`Well`\s in a
    :class:`DispenseGroup` to a target :class:`WellState`.

    The hard work is done by :func:`iterator`.  This is intended to be used as
    it is in :class:`Well.TransitionTo` ::

            motion = WellMotion(well, self.target, post_result=post_result, guard=self.guard)

            def before_tick() -> Iterator[Optional[Ticks]]:
                iterator = motion.iterator()
                one_tick = 1*tick
                while next(iterator):
                    yield one_tick
                yield None
            iterator = before_tick()
            board.before_tick(lambda: next(iterator), delta=after)
            return motion.initial_future

    """
    group: Final[DispenseGroup] #: The :class:`DispenseGroup` being moved
    board: Final[Board]         #: The :class:`Board` of the :class:`Well`\s
    target: Final[WellState]    #: The target :class:`WellState`
    initial_future: Final[Delayed[Well]] #: The :class:`.Delayed` object we were created with
    futures: Final[list[tuple[Well, Postable[Well]]]]
    """
    A list of pairs of :class:`Well` values and future to post the values to
    upon completion
    """
    # post_result: Final[bool]
    lead_well: Final[Well]
    well_gates: Final[set[WellGate]]    #: The :attr:`~Well.gate`\s of the :class:`Well`\s
    shared_pads: Final[Sequence[WellPad]]   #: The internal :class:`WellPad`\s of the initial :class:`Well`
    guard: Final[Optional[Iterator[bool]]]
    """
    An optional :class:`Iterator` that yields ``False`` when it's safe to proceed
    """
    # next_step: int
    # turned_gates_on: bool = False
    # turned_gates_off: bool = False
    # on_last_step: bool = False
    # one_tick: Final[Ticks] = 1*tick
    # sequence: WellOpStepSeq
    gate_status: GateStatus #: The :class:`GateStatus` of the :attr:`well_gates`

    def __init__(self, well: Well, target: WellState, *,
                 guard: Optional[Iterator[bool]] = None,
                 post_result: bool = True) -> None:
        """
        Initialize the object.

        Args:
            well: the first :class:`Well`
            target: the target :class:`WellState`
        Keyword Args:
            guard: an optional :class:`Iterator` that yields ``False`` when it's
                   safe to proceed post_result:
            post_result: whether to post ``well`` to :attr:`initial_future`
        """
        self.group = well.group
        self.board = well.board
        self.initial_future = Postable[Well]()
        self.futures = [(well, self.initial_future)] if post_result else []
        self.target = target
        # self.post_result = post_result
        self.lead_well = well
        self.well_gates = { well.gate }
        self.shared_pads = well.shared_pads
        self.guard = guard
        # self.next_step = 0
        self.gate_status = GateStatus.NOT_YET

    def try_adopt(self, other: WellMotion) -> bool:
        """
        Try to adopt another :class:`WellMotion`.  If successful, ``other``'s
        :func:`iterator` will yield ``False``, signalling that it is done, but
        its :attr:`initial_future` will not get a value posted until we call
        :func:`post_futures`.

        This is called from within :func:`iterator`, with :attr:`group`'s
        :attr:`~DispenseGroup.lock` locked:

            * after any :attr:`guard` has yielded ``False``

            * after it has been determined that the :attr:`group`'s
              :attr:`~DispenseGroup.motion` is this :class:`WellMotion`.

        :func:`try_adopt` will fail if

            * the two values of :attr:`target` do not match or

            * our :attr:`gate_status` is :attr:`~GateStatus.UNSAFE` or

            * the target is :attr:`~WellState.DISPENSED` and we are already
              working on the other's :class:`Well`.

        Args:
            other: the other :class:`WellMotion`
        Returns:
            ``True`` if we successfully adopted
        """
        # This is called from other.do_step(), with the group locked.
        if self.target is not other.target or self.gate_status is GateStatus.UNSAFE:
            return False
        # The other one wants to go to the same place we are, and either we haven't turned
        # any gates on yet or we just did in this tick.

        # If we're dispensing and we already have any of that motion's gates in our set,
        # it'll have to wait until we're done with this one.
        if self.target is WellState.DISPENSED and (self.well_gates & other.well_gates):
            return False

        # print(f"Piggybacking")
        self.well_gates.update(other.well_gates)
        # we don't have to add the shared pads.  Changing the ones we have will suffice.
        if self.gate_status is GateStatus.JUST_ON:
            for gate in other.well_gates:
                gate.schedule(WellPad.TurnOn, post_result = False)

        self.futures.extend(other.futures)

        return True

    def post_futures(self) -> None:
        """
        Walk through :attr:`futures` and post :class:`Well`\s to their
        respective :class:`.Delayed` objects.

        Note that if ``post_result`` was ``False`` for a :class:`Well`, nothing
        would be added to :attr:`futures` for that :class:`Well`.
        """
        for w,f in self.futures:
            f.post(w)

    # Returns True if it should keep going
    def iterator(self) -> Iterator[bool]:
        """
        Take one or more :class:`Well`\s to the :attr:`target`
        :class:`WellState`.  Yields ``True` whenever it should be asked to
        continue before the next clock tick.  Yields ``False`` if either it has
        finished or it has been adopted by another in-progress
        :class:`WellMotion`.  If it has finished, before yielding, it schedules
        calling :func:`post_futures` after the current tick.

        The basic procedure is:

            #. Wait (yielding ``True``) for any :attr:`guard` to signal that it
               is safe to proceed.

            #. If the :attr:`group` has a :attr:`~DispenseGroup.motion`, see if
               it can adopt us.  If we can, yield ``False``.

            #. If it can't, try again next tick.

            #. If there is no :attr:`~DispenseGroup.motion` in the
               :attr:`group`, set ourselves to be it.

            #. Grab a :class:`WellOpStepSeq` using the :attr:`group`'s
               :attr:`~DispenseGroup.transition_func`.

            #. Walk through each :class:`WellOpStep` in the sequence, setting
               pads to their stated values and updating :attr:`gate_status`.

               * At any point here, another :class:`WellMotion` may call
                 :func:`try_adopt` on us to get us to adopt them.

            #. When we are done, schedule calling :func:`post_futures` for after
               the next clock tick and yield ``False`` to signal that we're done.

        Args:
            self:
        Yields:
            ``True`` if the next value should be computed before the next clock
            tick, ``False`` if the motion is complete (or has been adopted)
        """
        target = self.target
        # On the first step, we need to see if this is really necessary or if we
        # can piggyback onto another motion (or just return)

        # print(f"New motion to {self.target}, gates = {self.well_gates}: {self}")
        group = self.group
        
        def current_state() -> Optional[WellState]:
            return group.states.state_for(self.lead_well)

        def with_lock() -> Optional[bool]:
            with group.lock:
                current = group.motion
                if current is not None:
                    # print(f"There already is a motion going to {current.target} (gate_status = {current.gate_status}): {current}")
                    if current.try_adopt(self):
                        # If we can piggyback, we do.
                        return False
                    else:
                        # Otherwise, we'll try again next time.  (I was going to reschedule
                        # when the current one was done, but it's almost certainly cheaper to
                        # just check each tick.
                        # print(f"Deferring")
                        return True
                # print(f"We're the first")
                if current_state() is target:
                    # There's no motion, and we're already where we want to be.
                    # If this is EXTRACTABLE or READY, we're fine, otherwise, we got here
                    # without using our gates, so we need to go through READY again
                    if target is WellState.READY or target is WellState.EXTRACTABLE:
                        self.post_futures()
                        # print(f"Already at {target}")
                        return False
                # if group.state is WellState.READY or target is WellState.READY:
                #     self.sequence = group.sequences[(group.state, target)]
                # else:
                #     self.sequence = list(group.sequences[(group.state, WellState.READY)])
                #     self.sequence += group.sequences[(WellState.READY, target)]
                # # print(f"Switching from {group.state} to {target}: {self.sequence}")
                # assert len(self.sequence) > 0
                group.motion = self
                return None

        # Even before we try to be adopted, if we're trying to dispense, we need to reserve the exit pad
        # (which means we won't have to later) and refill the well, if necessary.  If we're trying to absorb,
        # we wait until there's a drop there.  This is encapsulated in the object's guard

        guard = self.guard
        if guard is not None:
            while (next(guard)):
                yield True

        # This needs to be done as a separate call, because we need to release
        # the lock each time.

        # last_yield: Optional[bool] = None
        while (val := with_lock()) is not None:
            # print(f"Yielding {val}")
            # last_yield = val
            yield val

        # print(f"After loop ({val})")
        # assert last_yield != False

        shared_pads = self.shared_pads
        # turned_gates_on = self.turned_gates_on
        # turned_gates_off = self.turned_gates_off
        for on_last_step, step in group.states.transition_steps(self.lead_well, target):
            # We squirrel it away so that it can be used in try_adopt()
            # self.on_last_step = on_last_step
            states = list(itertools.repeat(OnOff.OFF, len(shared_pads)))
            gate_state = OnOff.OFF
            for pad_index in step:
                if pad_index == -1:
                    gate_state = OnOff.ON
                    # If we're turning the gates on to dispense, we need to make sure that the
                    # corresponding exit pads aren't occupied (or we'll slurp the drop back).
                    # If any are, we just return and try again next time.
                    if target is WellState.DISPENSED:
                        for g in self.well_gates:
                            assert(g.index == -1)
                            w = g.well
                            assert isinstance(w, Well)
                            while not w.exit_pad.empty:
                                yield True
                else:
                    states[pad_index-1] = OnOff.ON

            gs = self.gate_status

            if gs is GateStatus.JUST_ON and gate_state is OnOff.OFF:
                self.gate_status = GateStatus.UNSAFE
                # If we're dispensing, and we've turned the gate on and we're about
                # to turn it off for the first time, we need to make sure that the
                # exit pads are safe and reserved.
                if target is WellState.DISPENSED:
                    for g in self.well_gates:
                        well = g.well
                        pad = well.exit_pad
                        # The pad should already be reserved.
                        assert pad.reserved
                        # while not pad.safe_except(well):
                        #     yield True
                        # while not pad.reserve():
                        #     yield True
                        pad.schedule(Pad.TurnOn, post_result=False)
            elif gs is GateStatus.NOT_YET and gate_state is OnOff.ON:
                self.gate_status = GateStatus.JUST_ON
                # If we're abosrbing, and we're about to turn on the gate for the
                # first time, we need to turn off any pads in the blob at the exit pad
                if target is WellState.ABSORBED:
                    for g in self.well_gates:
                        well = g.well
                        pad = well.exit_pad
                        pads: Sequence[DropLoc] = (pad,)
                        if (blob := pad.blob) is not None:
                            pads = blob.pads
                        for p in pads:
                            assert isinstance(p, Pad)
                            p.schedule(Pad.TurnOff, post_result=False)
            for (i, shared) in enumerate(shared_pads):
                shared.schedule(WellPad.SetState(states[i]), post_result=False)
            for gate in self.well_gates:
                gate.schedule(WellPad.SetState(gate_state), post_result=False)
            # gs = self.gate_status
            # if gate_state is OnOff.ON and gs is GateStatus.NOT_YET:
            #     self.gate_status = GateStatus.JUST_ON
            # elif gs is GateStatus.JUST_ON and gate_state is OnOff.OFF:
            #     self.gate_status = GateStatus.UNSAFE
            #

            if not on_last_step:
                # We do the next step the next time around
                yield True
        # And on the other side, we clean up
        def cb() -> None:
            # # Any gates we turned on, we turn off at the next tick
            # for gate in self.well_gates:
            #     gate.schedule(WellPad.TurnOff, post_result=False)
            with group.lock:
                group.motion = None
                self.post_futures()
        self.board.after_tick(cb)
        yield False

PadBounds = Sequence[tuple[float,float]]
"""
A sequence of x-y values in a :class:`Board`'s coordinate space used to describe
the outline of a :class:`WellPad`.  Note that unlike for :class:`Pad`\s, these
values need not be integers.

For purposes of specifying these, a :class:`Pad`'s :attr:`~LocatedPad.location`
is considered to be its :attr:`~.Dir.SOUTHWEST` corner.
"""

class WellShape:
    """
    A description of the shape of a :class:`Well`, suitable for rendering by a
    :class:`.BoardMonitor`.

    For non-gate :class:`WellPad`\s, the shapes may be described by a single
    :class:`PadBounds` object or a sequence of them, to handle the case in which
    there are multiple physical electrodes ganged together.

    The :class:`WellShape` also describes the center and radius of a circle for
    the :class:`.BoardMonitor` to use to show the :class:`.Reagent` contained in
    the :class:`Well`
    """
    gate_pad_bounds: Final[PadBounds]
    """
    The shape of the :class:`Well`'s :attr:`~Well.gate`
    """
    shared_pad_bounds: Final[Sequence[Union[PadBounds, Sequence[PadBounds]]]]
    """
    The shape of the :class:`Well`'s :attr:`~Well.shared_pads`
    """
    reagent_id_circle_center: tuple[float,float]
    """
    The center of the :class:`Well`'s :class:`Reagent` circle
    """
    reagent_id_circle_radius: float
    """
    The radius of the :class:`Well`'s :class:`Reagent` circle
    """

    def __init__(self, *,
                 gate_pad_bounds: PadBounds,
                 shared_pad_bounds: Sequence[Union[PadBounds, Sequence[PadBounds]]],
                 reagent_id_circle_center: tuple[float, float],
                 reagent_id_circle_radius: float = 1):
        """
        Initialize the object

        Keyword Args:
            gate_pad_bounds: the shape of the :class:`Well`'s :attr:`~Well.gate`
            shared_pad_bounds: the shape of the :class:`Well`'s
                               :attr:`~Well.shared_pads`
            reagent_id_circle_center: the center of the :class:`Well`'s
                                      :class:`Reagent` circle
            reagent_id_circle_radius: the radius of the :class:`Well`'s
                                      :class:`Reagent` circle
        """
        self.gate_pad_bounds = gate_pad_bounds
        self.shared_pad_bounds = shared_pad_bounds
        self.reagent_id_circle_center = reagent_id_circle_center
        self.reagent_id_circle_radius = reagent_id_circle_radius

WellVolumeSpec = Union[Volume, Callable[[], Volume]]
"""
A :class:`.Volume` or a :class:`.Callable` that returns one
"""

TransitionStep = tuple[bool,WellOpStep]
"""
A pair in which the second element is a :class:`WellOpStep` and the first is an
``True`` if this is the last step in its :class:`WellOpStepSeq`
"""

class StateDefs:
    state_for_pads: Final[Mapping[tuple[int,...], WellState]]
    pads_for_state: Final[Mapping[WellState, tuple[int, ...]]]
    transitions: Final[dict[tuple[Optional[WellState], WellState], MissingOr[Sequence[TransitionStep]]]]
    ready_state: Final[tuple[int, ...]]

    def __init__(self, states: Mapping[WellState, tuple[int, ...]],
                 transitions: WellOpSeqDict)-> None:
        fwd = { state: tuple(sorted(pads)) for state,pads in states.items()}
        self.pads_for_state = fwd
        self.ready_state = states[WellState.READY]
        self.state_for_pads = { pads: state for state,pads in fwd.items() }
        self.transitions = { states: self.to_steps(seq) for states,seq in transitions.items() }
        self.transitions[(None, WellState.READY)] = [(True, self.ready_state)]
            
    def to_steps(self, seq: WellOpStepSeq) -> Sequence[TransitionStep]:
        last = len(seq)-1
        return [(i==last, step) for i,step in enumerate(seq)]
        
    def state_for(self, well: Well) -> Optional[WellState]:
        pads = [p.index for p in (well.gate, *well.shared_pads) if p.current_state is OnOff.ON]
        pads.sort()
        key = tuple(pads)
        return self.state_for_pads.get(key, None)
    
    def pads_for(self, state: WellState) -> Optional[tuple[int,...]]:
        return self.pads_for_state.get(state, None)
    
    def _transition_steps(self, start: Optional[WellState], end: WellState, *,
                          cached_only: bool = False) -> MissingOr[Sequence[TransitionStep]]:
        if start is end:
            return []
        steps = self.transitions.get((start,end), MISSING)
        if steps is MISSING and not cached_only:
            steps = self._compute_transition_steps(start, end)
            self.transitions[(start,end)] = steps
        return steps
    
    def transition_steps(self, well: Well, target: WellState) -> Sequence[TransitionStep]:
        start = self.state_for(well)
        steps = self._transition_steps(start, target)
        if steps is MISSING:
            state_desc= "unknown" if start is None else start.name
            logger.error(f"{well}'s state is {state_desc}.  Don't know how to get from there to {target.name}.")
            assert False
        return steps
    
    def _transition_through(self, middle: WellState, start: WellState, end: WellState) -> MissingOr[Sequence[TransitionStep]]:
        # We want to avoid a regress, so if we're called here and middle is one of the endpoints, we give up.
        if middle is start or middle is end:
            return MISSING
        to_middle = self._transition_steps(start, middle)
        from_middle = self._transition_steps(middle, end)
        if to_middle is MISSING or from_middle is MISSING:
            return MISSING
        # If both sides are just "Turn on the state", don't bother.
        if len(to_middle) == 1 and len(from_middle) == 1:
            return MISSING
        return [*((False, p[1]) for p in to_middle), *from_middle]
        
    
    def _compute_transition_steps(self, start: Optional[WellState], end: WellState) -> MissingOr[Sequence[TransitionStep]]:
        if start is None:
            # We don't know where we are.  If we have a sequence to get from READY, we assert READY and use it.
            from_ready = self._transition_steps(WellState.READY, end)
            if from_ready is not MISSING:
                return [(False, self.ready_state), *from_ready]
            # Otherwise, we just assert the end state if we know it.
            end_pads = self.pads_for(end)
            if end_pads is None:
                return MISSING
            return [(True, end_pads)]
        start_pads = self.pads_for(start)
        end_pads = self.pads_for(end)
        # If the two states are identical, we don't do anything
        if start_pads is not None and start_pads == end_pads:
            return ()
        # Can we go through READY?
        steps = self._transition_through(WellState.READY, start, end)
        if steps is not MISSING:
            return steps
        # Apparently not.  If we know the configuration for end, we just switch to it.
        if end_pads is not None:
            return [(True, end_pads)]
        # We really don't know.
        return MISSING
            

class DispenseGroup:
    """
    A group of :class:`Well`\s whose :attr:`~Well.shared_pads` are mirrored, so
    that changing the state of one changes the state of all.
    """
    key: Final[Any]
    """
    A key object (typically a string, number, or :class:`Well`) used when
    converting to a string
    """
    lock: Final[Lock]
    """
    A :class:`.Lock` used by :class:`WellMotion\s` to wrap changes to
    :attr:`motion` and :attr:`state`
    """
    motion: Optional[WellMotion]
    """
    The in-progress :class:`WellMotion`, if any for the :class:`Well`\s in this
    group.
    """
    # state: WellState
    # """
    # The current :class:`WellState` for the :class:`Well`\s in this group
    # """
    
    states: Final[StateDefs]

    def __init__(self, key: Any, *, states: StateDefs) -> None:
        """
        Initialize the object.

        The initial :attr:`state:` is assumed to be the
        :attr:`~WellState.Extractable`.

        Args:
            key:
            transition_func: the :class:`TransitionFunc` to use to change states.
        """
        self.key = key
        """
        The :class:`TransitionFunc` to use to iterate through
        :class:`WellOpStateSeq`\s to change to a new :class:`WellState`.
        """
        self.states = states
        self.lock = Lock()
        self.motion = None
        # self.state = WellState.EXTRACTABLE

    def __repr__(self) -> str:
        if isinstance(self.key, Well):
            return str(self.key)
        return f"DispenseGroup({self.key})"


class Well(OpScheduler['Well'], BoardComponent, PipettingTarget, TempControllable):
    """
    A well.

    * As a :class:`BoardComponent`, it has a :attr:`~BoardComponent.board`, and
      it can act as a :class:`.CommunicationScheduler`.

    * As a :class:`PipettingTarget`, it participates in the pipetting protocol
      by defining :func:`prepare_for_add`, :func:`prepare_for_remove`,
      :func:`pipettor_added`, and :func:`pipettor_removed`.

    Callbacks registered to :attr:`on_liquid_change` are fired both when
    :attr:`contents` is set and on calls to :func:`transfer_in` and
    :func:`transfer_out`.  Note that on the transfer functions, the same value
    will be passed as both the ``old`` and ``new`` parameters.  To monitor
    reagent or volume changes, add callbacks to the :class:`.Liquid` itself
    using its :func:`~.Liquid.on_reagent_change` or
    :func:`~.Liquid.on_volume_change`.

    When a :class:`.Drop.DispenseFrom` :class:`.Operation` is scheduled, before
    making the request, it loops calling :attr:`reserve_gate` until it succeeds.
    When the dispense is finished, it sets :attr:`gate_reserved` to ``False``.
    This serializes multiple requests to dispense from the same :class:`Well`.

    Most of the actual interaction with a :class:`Well` involves querying or
    modifying its :attr:`contents`, which is either a :class:`.Liquid` or
    ``None``, which is the initial state before any :class:`.Liquid` is put in
    the well.

    * The :attr:`volume` and :attr:`reagent` of the :attr:`contents` can be
      obtained directly (but not modified).  If :attr:`contents` is ``None``,
      these are zero and :attr:`.unknown_reagent`, respectively.

    * A :class:`Well` has a :attr:`capacity` and a :attr:`remaining_capacity`
      (defined as :attr:`capacity` ``-`` :attr:`volume`).

    * A :class:`Well` has a :attr:`dispensed_volume` (the nominal size of a
      dispensed :class:`.Drop`).  Its :attr:`drop_availability` is the number of
      :class:`.Drop`\s of that size it can be dispensed.  It is considered to be
      :attr:`empty` if there is less than one :class:`.Drop` available.

    * If :attr:`is_voidable` (a constant property) is ``True``, when the
      :attr:`volume` becomes exactly zero, it is considered to have been voided,
      and it is safe for the :class:`Well` to be reused for a different
      :class:`.Reagent`.

    * A :class:`Well` is :attr:`available` if either its :attr:`contents`
      is ``None`` or it :attr:`is_voidable` and its :attr:`volume` is zero and
      its :attr:`contents` is not :attr:`.~Luquid.inexact`.

    * To test whether a :class:`Well` is compatible with a given
      :class:`.Reagent`, use :func:`can_provide` and :func:`can_accept`.  Both
      of these return ``True`` if the proffered :class:`.Reagent` matches the
      :class:`Well`'s :attr:`reagent`, if the :class:`Well` is :attr:`available`
      or if either :class:`.Reagent` is the :attr:`~mpam.types.unknown_reagent`.
      In addition, :func:`can_accept` returns ``True`` if the :class:`Well`'s
      :attr:`reagent` is the :attr:`~mpam.types.waste_reagent`, and
      :func:`can_provide` returns ``True`` if the queried :class:`.Reagent` is
      the :attr:`~mpam.types.waste_reagent`.

    * To assert the :attr:`contents` of a :class:`Well`, you can set
      :attr:`contents` directly (which simply adopts the proffered optional
      :class:`.Liquid`) or call :func:`contains`, specifying the
      :class:`.Liquid` or :class:`.Reagent`.  While the former is the only way
      to reset :class:`contents` to ``None``, the latter is safer in other
      cases, as it both creates a new :class:`.Liquid` and clips the volume at
      :attr:`capacity`.  It also takes an optional :class:`.ErrorHandler` that
      can be used to specify an action to take when the :attr:`~.Liquid.volume`
      of a :class:`.Liquid` argument is greater than :attr:`capacity`.  (The
      default is simply to print a message.)

    * To assert that :class:`.Liquid` has been added to or removed from a
      :class:`Well`, call :func:`transfer_in` or :func:`transfer_out`.  Note
      that these functions are not typically called directly.  Rather, they are
      called as part of the implementation of drop motion inference and
      pipetting actions.

    * To request that :class:`.Liquid` be added to or removed from a
      :class:`Well`, call :func:`add` or :func:`remove`.  The default
      implementation turns around and asks its associated
      :attr:`~PipettingTarget.pipettor` to do the work.  Note that if
      :attr:`pipettor` is ``None``, these operations will fail.

    * Calling :func:`refill` calls :func:`add` to add :class:`.Liquid` until
      :attr:`volume` reaches the :attr:`fill_to` level.  This level is the first
      of

        * a :class:`.Volume` set as the value of :attr:`fill_to`,

        * the result of calling a function passed to :func:`compute_fill_to`,

        * if :attr:`required` is not ``None``, the minimum of it and
          :attr:`capacity`.  :attr:`required` is an optional :class:`.Volume`
          that can be set to an overall amount of :class:`.Liquid` that will be
          needed from the :class:`Well`.  It is updated by :func:`transfer_out`.

        * the :class:`Well`'s :attr:`capacity`.

    * Similarly, calling :func:`empty_well` calls :func:`remove` to remove
      :class:`.Liquid` until :attr:`volume` reaches the :attr:`empty_to` level.
      This level is the first of

        * a :class:`.Volume` set as the value of :attr:`empty_to`,

        * the result of calling a function passed to :func:`compute_empty_to`, or

        * zero

    * Calling :func:`ensure_content` ensures that a :class:`Well` contains a
      sufficient amount of :class:`.Reagent` to perform an action.  If it
      doesn't or if removing the specified :class:`.Volume` would take it below
      a :attr:`min_fill` level, :func:`refill` is called first. :attr:`min_fill`
      defaults to zero, but can be set to be a :class:`.Volume` or a function
      that returns one (via :func:`compute_min_fill).

      This is called inside of dispense operations to automatically refill wells
      when they become empty (or close enough to empty that the hardware does
      not believe that they can accurately dispense).

    * Similarly, calling :func:`ensure_space` ensures that a :class:`Well`
      contains a sufficient amount of room to perform an action. If it doesn't
      or if adding the specified :class:`.Volume` would take it above a
      :attr:`max_fill` level, :func:`empty_well` is called first.
      :attr:`max_fill` defaults to :attr:`capacity`, but can be set to be a
      :class:`.Volume` or a function that returns one (via
      :func:`compute_max_fill).

      This is called inside of absorbtion operations to automatically emptywells
      when they become full (or close enough to full that the hardware does
      not believe that they can accurately absorb).
    """
    number: int = -1
    """The :class:`Well`'s index in its :attr:`~BoardCompoent.board`'s :attr:`~Board.wells` list"""
    group: Final[DispenseGroup]
    """The :class:`Well`'s :class:`DispenseGroup` (of which it may be the only member)"""
    capacity: Final[Volume]
    """The maximum :class:`.Volume` that can be stored in the :class:`Well`"""
    dispensed_volume: Final[Volume]
    """The :class:`.Volume` nominally dispensed by the :class:`Well`"""
    is_voidable: Final[bool]
    """``True`` if the :class:`Well` can be considered :attr:`empty` after dispensing its entire content"""
    exit_pad: Final[Pad]
    """
    The :class:`Pad` onto which the :class:`Well` will dispense.

    It should be next to the :class:`Well`'s :attr:`gate`, and its
    :attr:`~Well.well` will be this one.
    """

    shared_pads: Final[Sequence[WellPad]]
    """
    The :class:`WellPad`\s in this :class:`Well` whose control is shared with
    other :class:`Well`\s in :attr:`group`.  Each one's :attr:`~WellPad.index`
    will be its index in this list.
    """
    
    def shared_pad_number(self, n: int) -> WellPad:
        return self.shared_pads[n-1]
    
    gate: Final[WellGate]
    """
    The :class:`WellGate` for this :class:`Well`.  It must be next to the
    :class:`Well`'s :attr:`exit_pad`.
    """
    exit_dir: Final[Dir]
    """
    The direction from the :class:`Well`'s :attr:`gate` to its :attr:`exit_pad`
    """
    gate_reserved: bool = False
    """
    Has the :attr:`gate` been reserved for a dispense operation?

    Set by :func:`reserve_gate` and eplicitly set to ``False`` under control of
    whoever got ``True` from it.
    """
    
    # _contents: Optional[Liquid]
    _shape: Final[Optional[WellShape]]

    required: Optional[Volume] = None
    """
    The total :class:`.Volume` of :class:`.Reagent` expected to be removed from
    the :class:`Well`.  May be ``None``.

    When :func:`refill` is called and :attr:`required` is not ``None``, the
    computed :attr:`fill_to` level is capped at this value.

    When :func:`transfer_out` is called, this value is decreased, so it remains
    an estimate of how much will be needed for the remainder of the run.
    """

    contents: MonitoredProperty[Optional[Liquid]] = MonitoredProperty(default=None)
    """
    The :class:`.Liquid` contained in the :class:`Well`, or ``None`` if the
    :class:`Well` has never contained a :class:`.Liquid`.

    When :attr:`contents` is set to an ``Optional[``:class:`.Liquid` ``]``
    different from its prior value, the callbacks registered to
    :attr:`on_liquid_change` are run, passing in the old and new values.
    """

    on_liquid_change: ChangeCallbackList[Optional[Liquid]] = contents.callback_list
    """
    The :class:`.ChangeCallbackList` monitoring :attr:`contents`.

    Callbacks will be invoked both when :attr:`contents` is set to a different
    (optional) :class:`.Liquid` and when :func:`transfer_in()` or
    :func:`transfer_out` is called.  In the transfer function cases, the state
    (i.e., :attr:`~.Liquid.reagent` and/or :attr:`~.Liquid.volume`) of
    :attr:`contents` will have changed, but the object remains the same and is
    passed in as both ``old`` and ``new`` arguments.
    """

    @property
    def removable_liquid(self) -> Optional[Liquid]:
        return self.contents

    @property
    def volume(self) -> Volume:
        """
        The :attr:`.Liquid.volume` of :attr:`contents` or zero if
        :attr:`contents` is ``None``
        """
        c = self.contents
        if c is None:
            return Volume.ZERO
        else:
            return c.volume

    @property
    def reagent(self) -> Reagent:
        """
        The :attr:`.Liquid.reagent` of :attr:`contents` or
        :attr:`.unknown_reagent` if :attr:`contents` is ``None``
        """

        c = self.contents
        if c is None:
            return unknown_reagent
        else:
            return c.reagent

    @property
    def remaining_capacity(self) -> Volume:
        """
        The difference between :attr:`capacity` and :attr:`volume`
        """
        return self.capacity-self.volume

    @property
    def drop_availability(self) -> float:
        """
        The number of :class:`.Drop`s of size :attr:`dispensed_volume` that can
        be dispensed given :attr:`volume`.  This is not necessarily an integer.
        """
        return self.volume.ratio(self.dispensed_volume)

    @property
    def empty(self) -> bool:
        """
        ``True`` if :attr:`drop_availability` is less than one.
        """
        return self.drop_availability < 1

    @property
    def available(self) -> bool:
        """
        ``True`` if it is safe ot reassign this :class:`Well` to another
        :class:`.Reagent`.

        :attr:`available` will be ``True`` if :attr:`contents` is ``None`` or

            * the :class:`Well` :func:`is_voidable`,
            * :attr:`volume` is zero, and
            * :attr:`contents` is not :attr:`~.Liquid.inexact`
        """
        c = self.contents
        return c is None or self.is_voidable and c.volume==Volume.ZERO and not c.inexact

    @property
    def gate_on(self) -> bool:
        """
        ``True`` if :attr:`gate`'s :attr:`~BinaryComponent.current_state` is
        :attr:`~.OnOff.ON`
        """
        return self.gate.current_state is OnOff.ON

    # refill if dispensing would take you to this level
    _min_fill: Optional[WellVolumeSpec] = None

    @property
    def min_fill(self) -> Volume:
        """
        The minimum fill level for the :class:`Well`.  If :func:`ensure_content`
        is called, and the result of removing the required :class:`.Volume`
        would leave the :attr:`volume` less than this amount, :func:`refill` is
        called first.

        This can be set to a :class:`.Volume` or a :class:`.Callable` that
        returns one.  If not set (or set to ``None``) the value will be zero.

        Note:
            As of 4/20/22, MyPy has a bug (`issue #3004
            <https://github.com/python/mypy/issues/3004>`_) that causes it to
            complain if you try to assign a :class:`.Volume`-valued property
            anything other than a :class:`.Volume`.  To get around this, you can
            set the value using :func:`compute_min_fill`.

        """
        return self.volume_from_spec(self._min_fill, lambda: Volume.ZERO)

    @min_fill.setter
    def min_fill(self, volume: Optional[WellVolumeSpec]) -> None:
        self._min_fill = volume

    # The compute_V() functions are there because currently, MyPy will complain if you try to
    # assign a value of a type that doesn't match the *getter*. (MyPy issue #3004.  They agree
    # that it should be fixed, but it still isn't as of 4/20/22.)

    def compute_min_fill(self, volume: Optional[WellVolumeSpec]) -> None:
        """
        An alternative to setting :attr:`min_fill` to get around a MyPy bug.
        ``volume`` can be a :class:`.Volume`, a :class:`.Callable` returning
        one, or ``None`` (indicating a level of zero).

        Args:
            volume: The :class:`WellVolumeSpec` (or ``None``) to use for
            :attr:`min_fill`
        """
        self._min_fill = volume

    # empty if absorbing would take you above this level
    _max_fill: Optional[WellVolumeSpec] = None

    @property
    def max_fill(self) -> Volume:
        """
        The maximum fill level for the :class:`Well`.  If :func:`ensure_space`
        is called, and the result of adding the required :class:`.Volume` would
        leave the :attr:`volume` greater than this amount, :func:`empty_well` is
        called first.

        This can be set to a :class:`.Volume` or a :class:`.Callable` that
        returns one.  If not set (or set to ``None``) the value will be
        :attr:`capacity`.

        Note:
            As of 4/20/22, MyPy has a bug (`issue #3004
            <https://github.com/python/mypy/issues/3004>`_) that causes it to
            complain if you try to assign a :class:`.Volume`-valued property
            anything other than a :class:`.Volume`.  To get around this, you can
            set the value using :func:`compute_max_fill`.

        """
        return self.volume_from_spec(self._max_fill, lambda: self.capacity)

    @max_fill.setter
    def max_fill(self, volume: Optional[WellVolumeSpec]) -> None:
        self._max_fill = volume

    def compute_max_fill(self, volume: Optional[WellVolumeSpec]) -> None:
        """
        An alternative to setting :attr:`max_fill` to get around a MyPy bug.
        ``volume`` can be a :class:`.Volume`, a :class:`.Callable` returning
        one, or ``None`` (indicating :attr:`capacity`)

        Args:
            volume: The :class:`WellVolumeSpec` (or ``None``) to use for
            :attr:`max_fill`
        """
        self._max_fill = volume

    # when refilling, fill to this level
    _fill_to: Optional[WellVolumeSpec] = None


    @property
    def fill_to(self) -> Volume:
        """
        The target :attr:`volume` after a call to :func:`refill`.

        This can be set to a :class:`.Volume` or a :class:`.Callable` that
        returns one.  If not set (or set to ``None``) the value will be the
        minimum of :attr:`required` (if it is not ``None``) and :attr:`capacity`.

        Note:
            As of 4/20/22, MyPy has a bug (`issue #3004
            <https://github.com/python/mypy/issues/3004>`_) that causes it to
            complain if you try to assign a :class:`.Volume`-valued property
            anything other than a :class:`.Volume`.  To get around this, you can
            set the value using :func:`compute_fill_to`.

        """
        def default_fill_line() -> Volume:
            if self.required is None:
                return self.capacity
            return min(self.capacity, self.required)
        return self.volume_from_spec(self._fill_to, default_fill_line)

    @fill_to.setter
    def fill_to(self, volume: Optional[WellVolumeSpec]) -> None:
        self._fill_to = volume

    def compute_fill_to(self, volume: Optional[WellVolumeSpec]) -> None:
        """
        An alternative to setting :attr:`fill_to` to get around a MyPy bug.
        ``volume`` can be a :class:`.Volume`, a :class:`.Callable` returning
        one, or ``None`` (indicating :attr:`capacity`)

        Args:
            volume: The :class:`WellVolumeSpec` (or ``None``) to use for
            :attr:`fill_to`
        """
        self._fill_to = volume


    # when emptying, empty to this level
    _empty_to: Optional[WellVolumeSpec] = None

    @property
    def empty_to(self) -> Volume:
        """
        The target :attr:`volume` after a call to :func:`empty_well`.

        This can be set to a :class:`.Volume` or a :class:`.Callable` that
        returns one.  If not set (or set to ``None``) the value will be zero.

        Note:
            As of 4/20/22, MyPy has a bug (`issue #3004
            <https://github.com/python/mypy/issues/3004>`_) that causes it to
            complain if you try to assign a :class:`.Volume`-valued property
            anything other than a :class:`.Volume`.  To get around this, you can
            set the value using :func:`compute_empty_to`.

        """
        return self.volume_from_spec(self._empty_to, lambda: Volume.ZERO)

    @empty_to.setter
    def empty_to(self, volume: Optional[WellVolumeSpec]) -> None:
        self._empty_to = volume

    def compute_empty_to(self, volume: Optional[WellVolumeSpec]) -> None:
        """
        An alternative to setting :attr:`empty_to` to get around a MyPy bug.
        ``volume`` can be a :class:`.Volume`, a :class:`.Callable` returning
        one, or ``None`` (indicating :attr:`capacity`)

        Args:
            volume: The :class:`WellVolumeSpec` (or ``None``) to use for
            :attr:`empty_to`
        """
        self._empty_to = volume

    def __init__(self, *,
                 board: Board,
                 group: Union[DispenseGroup, StateDefs],
                 exit_pad: Pad,
                 gate: WellGate,
                 shared_pads: Sequence[WellPad],
                 capacity: Volume,
                 dispensed_volume: Volume,
                 exit_dir: Dir,
                 is_voidable: bool = False,
                 shape: Optional[WellShape] = None,
                 ) -> None:
        """
        Initialize the object.

        If ``group`` is a :class:`TransitionFunc` rather than a
        :class:`DispenseGroup`, a new :class:`DispenseGroup` is created to use
        it.  This :class:`Well` will be the only one that refers to this group.

        ``gate`` and all of the :class:`WellPad`\s in ``shared_pads`` will get
        their :attr:`~WellPad.well` and :attr:`~WellPad.index` set by calling
        :attr:`~WellPad.set_location` on them.

        Keyword Args:
            board: the :class:`Board` the :class:`Well` is on
            number: the index into :attr:`board`'s list of :attr:`~Board.wells`

            group: the :class:`DispenseGroup` the :class:`Well` is a member of
                   or a :class:`TransitionFunc` to use to create one containing only it

            exit_pad: the :class:`Well`'s :attr:`exit_pad`
            gate: the :class:`Well`'s :gate:

            shared_pads: the :class:`WellPad`\s the :class:`Well` shares control
                         of with other members of its :attr:`group`

            capacity: the maximum :class:`.Volume` that can be contained in the
                      :class:`Well`

            dispensed_volume: the :class:`.Volume` nominally dispensed by the
                              :class:`Well`

            exit_dir: the direction from the :class:`Well`'s :attr:`gate` to its
                      :attr:`exit_pad`

            is_voidable: is the :class:`Well` truly empty when its
                         :attr:`volume` hits zero?

            shape: an optional :class:`WellShape` describing the shape of the
                   :class:`Well`
        """
        BoardComponent.__init__(self, board)
        if not isinstance(group, DispenseGroup):
            group = DispenseGroup(self, states=group)
        self.group = group
        self.exit_pad = exit_pad
        self.gate = gate
        self.shared_pads = shared_pads
        self.capacity = capacity
        self.dispensed_volume = dispensed_volume
        self.exit_dir = exit_dir
        self.is_voidable = is_voidable
        self._shape = shape

        assert exit_pad._well is None, f"{exit_pad} is already associated with {exit_pad.well}"
        exit_pad._well = self
        gate.set_location(self, -1)
        for i,wp in enumerate(shared_pads):
            wp.set_location(self, i+1)

    def prepare_for_add(self) -> None:
        """
        Get into an injectable state.
        """
        op = Well.TransitionTo(WellState.INJECTABLE)
        self.schedule(op).wait()

    def prepare_for_remove(self) -> None:
        """
        Get into an extractable state
        """
        op = Well.TransitionTo(WellState.EXTRACTABLE)
        self.schedule(op).wait()


    def pipettor_added(self, reagent: Reagent, volume: Volume, *,
                       mix_result: Optional[MixResult],
                        last: bool) -> None: # @UnusedVariable
        """
        Called when the :class:`.Pipettor` has finished adding :class:`.Liquid`.

        Uses :func:`transfer_in` to update :attr:`contents`.

        If ``mix_result`` is not ``None``, it should be used as the result of
        mixing the delivered :class:`.Liquid` to what is already there.  If
        ``last`` is ``False``, there will be at least one more transfer before
        the overall transfer operation is complete.

        Args:
            reagent: the :class:`.Reagent` added
            volume: the :class:`.Volume` of :class:`.Reagent` added
        Keyword Args:
            mix_result: the (optional) result of mixing the added
                        :class:`.Liquid` with what's already there.
            last: ``True`` if this is the last transfer in a transfer request.
        """
        got = Liquid(reagent, volume)
        self.transfer_in(got, mix_result=mix_result)

    def pipettor_removed(self, reagent: Reagent, volume: Volume, *, # @UnusedVariable
                         last: bool) -> None: # @UnusedVariable
        """
        Called when the :class:`.Pipettor` has finished removing
        :class:`.Liquid`.

        Uses :func:`transfer_out` to update :attr:`contents`.

        If ``last`` is ``False``, there will be at least one more transfer
        before the overall transfer operation is complete.

        Args:
            reagent: the :class:`.Reagent` removed
            volume: the :class:`.Volume` of :class:`.Reagent` removed
        Keyword Args:
            last: ``True`` if this is the last transfer in a transfer request.
        """
        self.transfer_out(volume)


    def volume_from_spec(self, spec: Optional[WellVolumeSpec], default_fn: Callable[[], Volume]) -> Volume:
        """
        Obtain a :class:`.Volume` from an optional :class:`WellVolumeSpec`.

        If ``spec`` is a :class:`Volume`, it is used.  Otherwise, if it is not
        ``None``, it is called to obtain the value.  If ``spec`` is ``None``,
        ``default_fn`` is called to get the value.

        Args:
            spec: a :class:`.Volume`, a :class:`.Callable` that returns one, or
                  ``None``, indicating that ``default_fn`` should be used
            default_fn: called to get the :class:`.Volume` if ``spec`` is ``None``
        """
        if spec is None:
            return default_fn()
        if isinstance(spec, Volume):
            return spec
        return spec()

    def __repr__(self) -> str:
        # return f"Well[{self.number} <> {self.exit_pad}]"
        return f"Well[{self.number}]"

    def can_accept(self, reagent: Reagent) -> bool:
        """
        Can the :class:`Well` accept ``reagent``?

        Returns ``True`` if

            1. the :class:`Well` is :attr:`available`, or
            2. ``reagent`` matches the :class:`Well`'s :attr:`reagent`, or
            3. either :class:`.Reagent` is the
               :attr:`~mpam.types.unknown_reagent`, or
            4. the :class:`Well`'s :attr:`reagent` is the
               :attr:`~mpam.types.waste_reagent`.

        Args:
            reagent: the :class:`.Reagent` being provided
        Returns:
            ``True`` if the :class:`Well` can accept ``reagent``
        """
        if self.available: return True
        my_r = self.reagent
        return (my_r == reagent
                or my_r == unknown_reagent
                or reagent == unknown_reagent
                or my_r == waste_reagent)

    def can_provide(self, reagent: Reagent) -> bool:
        """
        Can the :class:`Well` provide ``reagent``?

        Returns ``True`` if

            1. the :class:`Well` is :attr:`available`, or
            2. ``reagent`` matches the :class:`Well`'s :attr:`reagent`, or
            3. either :class:`.Reagent` is the
               :attr:`~mpam.types.unknown_reagent`, or
            4. ``reagent`` is the :attr:`~mpam.types.waste_reagent`.

        The reason :func:`can_provide` returns ``True`` if the :class:`Well` is
        :attr:`available` is that it is assumed that :func:`ensure_content` will
        be called before anything is removed, and this will call :func:`refill`.

        Args:
            reagent: the :class:`.Reagent` required
        Returns:
            ``True`` if the :class:`Well` can provide ``reagent``
        """
        # If we're empty, there's no mismatch, but ensure_conent() will refill.  Otherwise, we can
        # do it if we don't know or care what we want or we don't know what we have
        if self.available: return True
        my_r = self.reagent
        return (my_r == reagent
                or my_r == unknown_reagent
                or reagent == unknown_reagent
                or reagent == waste_reagent)

    def transfer_in(self, liquid: Liquid, *,
                    volume: Optional[Volume] = None,
                    on_overflow: ErrorHandler = PRINT,
                    on_reagent_mismatch: ErrorHandler = PRINT,
                    mix_result: Optional[MixResult] = None) -> None:
        """
        Adjust the :class:`Well`'s :attr:`contents` to reflect the addition of
        ``liquid``.  If ``volume`` is specified, only that much of ``liquid`` is
        used.  If ``volume`` is greater than ``liquid``'s
        :attr:`.Liquid.volume`, all of ``liquid`` is used.

        Note:
            ``liquid`` is adjusted to account for the transfer as well.

        If the transfer would result in the :attr:`capacity` of the
        :class:`Well` being exceeded, ``on_overflow`` is invoked.

        If it's not the case that the :class:`Well` :func:`can_accept`
        ``liquid``'s :attr:`~.Liquid.reagent` and ``mix_result`` is ``None``,
        ``on_reagent_mismatch`` is invoked.

        After the adjustments, callbacks registered using
        :attr:`on_liquid_change` are run, passing in the new :attr:`contents` as
        both old and new values.

        Note:
            If :attr:`contents` was ``None``, it will first be changed to a
            volume-zero :class:`.Liquid` with the incoming :class:`.Reagent`.
            This will also trigger the liquid-change callbacks.

        Args:
            liquid: the :class:`.Liquid` that forms the source of the transfer
        Keyword Args:

            volume: the :class:`.Volume` of ``liquid`` transfered or ``None`` to
                    indicate all of it.
            on_overflow: an :class:`.ErrorHandler` for the case in which the
                         transfer would exceed the :attr:`capacity` of the
                         :class:`Well`
            on_reagent_mismatch: an :class:`.ErrorHandler` for the case in which
                         ``liquid``'s :attr:`~.Liquid.reagent` doesn't match
                         that of the :class:`Well`
            mix_result: the (optional) result of mixing the added
                        :class:`.Liquid` with what's already there.
        """
        if volume is None:
            volume = liquid.volume
        else:
            volume = min(volume, liquid.volume)
            if volume < liquid.volume:
                new_liquid = Liquid(liquid.reagent, volume)
                liquid.volume -= volume
                liquid = new_liquid
        on_overflow.expect_true(self.remaining_capacity >= volume,
                    lambda : f"Tried to add {volume} to {self}.  Remaining capacity only {self.remaining_capacity}")
        # available implies _contents is not None, but MyPy can't do the inference for the else
        # clause if I don't check it here.
        if self.contents is None or self.available:
            self.contents = Liquid(liquid.reagent, Volume.ZERO)
        else:
            r = self.contents.reagent
            on_reagent_mismatch.expect_true(mix_result is not None or self.can_accept(liquid.reagent),
                                            lambda : f"Adding {liquid.reagent} to {self} containing {r}")
        assert self.contents is not None
        self.contents.mix_in(liquid, result=mix_result)
        self.on_liquid_change.process(self.contents, self.contents)
        # print(f"{self} now contains {self.contents}")

    def transfer_out(self, volume: Volume, *,
                     on_empty: ErrorHandler = PRINT) -> Liquid:
        """
        Adjust the :class:`Well`'s :attr:`contents` to reflect the removal of
        ``volume`` from :attr:`contents`.

        If :attr:`volume` is less than ``volume``, ``on_empty`` is invoked.
        After the handler is invoked, ``volume`` is clipped to (the possibly
        altered) :attr:`volume`.

        If :attr:`reagent` is not ``None``, ``volume`` is subtracted from it.
        If this would render it zero or negative, it is set to ``None``.

        After the adjustments, callbacks registered to :attr:`on_liquid_change`
        are run, passing in the new :attr:`contents` as both old and new values.

        Note:
            In order to deal with rounding errors, ``on_empty`` is not invoked
            if ``volume`` exceeds :attr:`volume` by less than 5% of
            :attr:`dispensed_volume`.

        Args:
            volume: the :class:`.Volume` of :attr:`reagent` to remove
        Keyword Args:
            on_empty: an :class:`.ErrorHandler` for the case in which ``volume``
                      exceeds the :attr:`volume` of the :class:`Well`
        Returns:
            a :class:`Liquid` containing ``volume`` of :attr:`reagent`
        """
        on_empty.expect_true(self.volume >= volume
                             or self.volume.is_close_to(volume,
                                                        abs_tol=0.05*self.dispensed_volume),
                                lambda : f"Tried to draw {volume} from {self}, which only has {self.volume}")
        v = min(self.volume, volume)
        reagent: Reagent
        c = self.contents
        if c is None:
            reagent = unknown_reagent
        else:
            reagent = c.reagent
            # print(f"Removing {v} from {self._contents}")
            if v > 0:
                c -= v
                self.on_liquid_change.process(c, c)
        if self.required is not None:
            if self.required <= v:
                self.required = None
            else:
                self.required -= v
        # print(f"{self} now contains {self.contents}")
        return Liquid(reagent, v)

    def contains(self, content: Union[Liquid, Reagent],
                 *, on_overflow: ErrorHandler = PRINT) -> None:
        """
        Assert the :attr:`contents` of the :class:`Well`.

        If ``content`` is a :class:`.Reagent`, the volume is taken to be zero.

        If the volume is greater than the :class:`Well`'s :attr:`capacity`,
        ``on_overflow`` is invoked and the volume is trimmed to the
        :attr:`capacity`.

        Args:
            content: the initial :attr:`contents`, either a :class:`.Liquid` or
                     a :class:`.Reagent`
        Keyword Args:
            on_overflow: an :class:`.ErrorHandler` invoked if ``content`` is a
                         :class:`.Liquid` whose :attr:`~.Liquid.volume` is
                         greater than the :class:`Well`'s :attr:`capacity`
        """
        if isinstance(content, Reagent):
            liquid = Liquid(content, Volume.ZERO)
        else:
            liquid = content
        on_overflow.expect_true(liquid.volume <= self.capacity,
                                lambda : f"Asserted {self} contains {liquid}. Capacity only {self.capacity}")
        self.transfer_in(liquid, volume=min(liquid.volume, self.capacity))
        # print(f"Volume is now {self.volume}")

    def reserve_gate(self) -> bool:
        """
        Attempts to reserve the :class:`Well`'s gate for a dispense operation by
        setting :attr:`gate_reserved` to ``True``.  Fails if
        :attr:`gate_reserved` was already ``True``.

        It is expected that the caller will loop until this method returns
        ``True`` and then explicitly set :attr:`gate_reserved` to ``False`` when
        the reason for the reservation has finished.

        Returns:
            ``True`` if the gate was successfully reserved, ``False`` otherwise.
        """
        if self.gate_reserved:
            return False
        self.gate_reserved = True
        return True

    def add(self, reagent: Reagent, volume: Volume, *,
            mix_result: Optional[MixResult] = None,
            on_insufficient: ErrorHandler = PRINT,
            on_no_source: ErrorHandler = PRINT
            ) -> Delayed[Well]:
        """
        Request that ``volume`` of ``reagent`` be added to the :class:`Well`.
        Returns a :class:`.Delayed`\[:class:`Well`] that will receive this
        :class:`Well` as a value when the action is complete.

        Note:
            The default implementation of :func:`add` requires that
            :attr:`~PipettingTarget.pipettor` not be ``None``.  As ``None`` is
            the default, for :func:`add` to succeed, it must be set first.  If
            it is not, an assertion will fail.

        Note:
            The actual addition may take place in several steps.  If action
            should be taken on intermediate transfers, use
            :attr:`on_liquid_change` to register a callback or override
            :func:`pipettor_added`.

        Note:
            If the request cannot be fully satisfied, ``on_insufficient`` or
            ``on_no_source`` will be invoked, but he action will still complete.

        Warning:
            If the ``on_insufficient`` or ``on_no_source`` is invoked, it is
            likely that this will be in a different thread running the
            :attr:`~PipettingTarget.pipettor` and raising an exception will
            cause it to terminate in an unrecoverable way, so :class:`.RAISE`
            :class:`.ErrorHandler`\s should probably not be used.

        Args:
            reagent: the :class:`.Reagent` to add
            volume: the :class:`.Volume` of ``reagent`` to add
        Keyword Args:
            mix_result: the (optional) result of mixing the added
                        :class:`.Liquid` with what's already there.
            on_insufficient: an :class:`.ErrorHandler` invoked when the
                             :class:`Well`'s :attr:`~PipettingTarget.pipettor`
                             cannot provide ``volume`` of ``reagent``.
            on_no_source: an :class:`.ErrorHandler` invoked when the
                          :class:`Well`'s :attr:`~PipettingTarget.pipettor`
                          has no source for ``reagent``
        Returns:
            a :class:`.Delayed`\[:class:`Well`] that will receive this
            :class:`Well` when the :class:`.Liquid` has been added
        """
        pipettor = self.pipettor
        assert pipettor is not None, f"{self} has no pipettor and add() was not overridden"

        p_future = pipettor.schedule(pipettor.Supply(reagent, volume, self,
                                                     mix_result=mix_result,
                                                     on_insufficient=on_insufficient,
                                                     on_no_source=on_no_source))
        return p_future.transformed(lambda _: self)

    def remove(self, volume: Volume, *,
               on_no_sink: ErrorHandler = PRINT
               ) -> Delayed[Liquid]:
        """
        Request that ``volume`` of the :class:`Well`'s :attr:`reagent` be
        removed from the :class:`Well`. Returns a
        :class:`.Delayed`\[:class:`Well`] that will receive this :class:`Well`
        as a value when the action is complete.

        "Completion" in this sense, is intended to be the point at which the last
        of the :class:`.Liquid` is removed, not when it reaches its destination.

        Note:
            The default implementation of :func:`remove` requires that
            :attr:`~PipettingTarget.pipettor` not be ``None``.  As ``None`` is
            the default, for :func:`remove` to succeed, it must be set first.  If
            it is not, an assertion will fail.

        Note:
            The actual removal may take place in several steps.  If action
            should be taken on intermediate transfers, use
            :attr:`on_liquid_change` to register a callback or override
            :func:`pipettor_removed`.

        Note:
            If the :attr:`~PipettingTarget.pipettor` does not know where to put
            the :class:`Well`'s :attr:`reagent`, ``on_no_sink`` will be invoked,
            but the transfer is expected to take place, with the :attr:`reagent`
            going wherever the :attr:`~PipettingTarget.pipettor` would put the
            :attr:`mpam.types.waste_reagent`.

        Warning:
            If the ``on_insufficient`` or ``on_no_source`` is invoked, it is
            likely that this will be in a different thread running the
            :attr:`~PipettingTarget.pipettor` and raising an exception will
            cause it to terminate in an unrecoverable way, so :class:`.RAISE`
            :class:`.ErrorHandler`\s should probably not be used.

        Args:
            volume: the :class:`.Volume` of the :class:`Well`'s :attr:`reagent`
                    to remove
        Keyword Args:
            on_no_sink: an :class:`.ErrorHandler` invoked when the
                        :class:`Well`'s :attr:`~PipettingTarget.pipettor` has no
                        sink for the :class:`Well`'s :attr:`reagent`
        Returns:
            a :class:`.Delayed`\[:class:`Well`] that will receive this
            :class:`Well` when the :class:`.Liquid` has been removed
        """
        pipettor = self.pipettor
        assert pipettor is not None, f"{self} has no pipettor and remove() was not overridden"

        p_future = pipettor.schedule(pipettor.Extract(volume, self,
                                                      on_no_sink=on_no_sink))
        return p_future

    def refill(self, *, reagent: Optional[Reagent] = None) -> Delayed[Well]:
        """
        Request that ``reagent`` be added to bring the :class:`Well`'s
        :attr:`volume` to its current :attr:`fill_to` level.  If the
        :class:`Well`'s :attr:`volume` is already at or above that level, post
        the :class:`Well` to the returned :class:`Delayed` object immediately.

        Note:
            :func:`refill` is implemented by calling :func:`add`, which requires
            that :attr:`~PipettingTarget.pipettor` not be ``None``.

        Note:
            The actual addition may take place in several steps.  If action
            should be taken on intermediate transfers, use
            :attr:`on_liquid_change` to register a callback or override
            :func:`pipettor_added`.

        Keyword Args:
            reagent: the :class:`.Reagent` to fill with or ``None`` to indicate
                     the :class:`Well`'s :attr:`reagent`
        Returns:
            a :class:`.Delayed`\[:class:`Well`] that will receive this
            :class:`Well` when the :class:`.Liquid` has been added
        """
        volume = self.fill_to - self.volume
        # print(f"Fill line is {self.fill_to}.  Adding {volume}.")
        # assert volume > Volume.ZERO, f"refill(volume={volume}) called on {self}"
        if volume <= 0:
            return Delayed.complete(self)
        if reagent is None:
            reagent = self.reagent
        return self.add(reagent, volume)

    def empty_well(self) -> Delayed[Liquid]:
        """
        Request that :attr:`reagent` be added to bring the :class:`Well`'s
        :attr:`volume` to its current :attr:`empty_to` level.  If the
        :class:`Well`'s :attr:`volume` is already at or below that level, post
        the :class:`Well` to the returned :class:`Delayed` object immediately.

        Note:
            :func:`empty_well` is implemented by calling :func:`remove`, which
            requires that :attr:`~PipettingTarget.pipettor` not be ``None``.

        Note:
            The actual removal may take place in several steps.  If action
            should be taken on intermediate transfers, use
            :attr:`on_liquid_change` to register a callback or override
            :func:`pipettor_removed`.

        Returns:
            a :class:`.Delayed`\[:class:`Well`] that will receive this
            :class:`Well` when the :class:`.Liquid` has been removed
        """
        volume = self.volume - self.empty_to
        # assert volume > Volume.ZERO, f"empty_well(volume={volume}) called on {self}"
        if volume <= 0:
            return Delayed.complete(Liquid(self.reagent, Volume.ZERO))
        return self.remove(volume)


    def ensure_content(self,
                       volume: Optional[Volume] = None,
                       reagent: Optional[Reagent] = None,
                       *, on_reagent_mismatch: ErrorHandler = PRINT
                       # slop
                       ) -> Delayed[Well]:
        """
        Ensure that ``volume`` of ``reagent`` can be removed from the
        :class:`Well` without taking its :attr:`volume` below its current
        :attr:`min_fill` level.  If this is not the case, :func:`refill` is
        called first.

        If it's not the case that the :class:`Well` :func:`can_provide`
        ``reagent``, ``on_reagent_mismatch`` is invoked.

        :class:`.Reagent` matching is checked (and ``on_reagent_mismatch``
        invoked, if necessary) before the :attr:`volume` is checked, so on some
        architectures, a mismatch can be fixed by emptying the :class:`Well`
        first::

            empty_first = FIX_BY(lambda: well.remove(well.volume).wait())
            well.ensure_content(reagent=reagent, on_reagent_mismatch=empty_first)

        This will empty the :class:`Well`, setting its :attr:`volume` to zero,
        and then :func:`refill` it.

        Note:
            In order to deal with rounding errors, :func:`refill` is not called
            if the resulting :attr:`volume` would undershoot :attr:`min_fill` by
            less than 5% of :attr:`dispensed_volume`.

        Args:
            volume: the :class:`.Volume` of ``reagent`` required or ``None`` to
                    indicate the :class:`Well`'s :attr:`dispensed_volume`
            reagent: the :class:`.Reagent` required or ``None`` to indicate the
                     :class:`Well`'s :attr:`reagent`
        Keyword Args:
            on_reagent_mismatch: an :class:`.ErrorHandler` for the case in which
                                 ``reagent`` doesn't match the :class:`Well`'s
                                 :attr:`reagent`
        Returns:
            a :class:`.Delayed`\[:class:`Well`] that will receive this
            :class:`Well` when the availability has been confirmed

        """
        if volume is None:
            volume = self.dispensed_volume
        if reagent is not None:
            on_reagent_mismatch.expect_true(self.can_provide(reagent),
                                            lambda : f"{self} contains {self.reagent}.  Expected {reagent}")
        current_volume = self.volume
        resulting_volume = current_volume - volume
        if resulting_volume >= self.min_fill or resulting_volume.is_close_to(self.min_fill,
                                                                             abs_tol=0.05*self.dispensed_volume):
            return Delayed.complete(self)
        # print(f"Require {volume} of {reagent}.  Only have {current_volume}.  Refilling")
        return self.refill(reagent=reagent)

    def ensure_space(self,
                     volume: Volume,
                     reagent: Optional[Reagent] = None,
                     *, on_reagent_mismatch: ErrorHandler = PRINT
                     ) -> Delayed[Well]:
        """
        Ensure that ``volume`` of ``reagent`` can be added to the :class:`Well`
        without taking its :attr:`volume` above its current :attr:`max_fill`
        level.  If this is not the case, :func:`empty_well` is called first.

        If it's not the case that the :class:`Well` :func:`can_accept`
        ``reagent``, ``on_reagent_mismatch`` is invoked.

        :class:`.Reagent` matching is checked (and ``on_reagent_mismatch``
        invoked, if necessary) before the :attr:`volume` is checked, so on some
        architectures, a mismatch can be fixed by emptying the :class:`Well`
        first::

            empty_first = FIX_BY(lambda: well.remove(well.volume).wait())
            well.ensure_content(reagent=reagent, on_reagent_mismatch=empty_first)

        The downside to this approach is that the :func:`.Delayed.wait` call
        will block the thread until the :class:`.Liquid` has been removed.  If
        this is a problem, :class:`.RAISE` should be used instead::

            class Mismatch(RuntimeError): ...

            try:
                f = well.ensure_space(volume, reagent,
                                      on_reagent_mismatch=RAISE(Mismatch))
             except Mismatch:
                f = Delayed[Well]()
                def call_again(_) -> None:
                    well.ensure_space(volume, reagent).post_to(f)
                well.remove(well.volume).then_call(call_again)

        This catches the mismatch and calls :func:`remove`, but schedules a
        retry of :func:`ensure_space` after it is done.

        Note:
            In order to deal with rounding errors, :func:`refill` is not called
            if the resulting :attr:`volume` would undershoot :attr:`min_fill` by
            less than 5% of :attr:`dispensed_volume`.

        Args:
            volume: the :class:`.Volume` of ``reagent`` required or ``None`` to
                    indicate the :class:`Well`'s :attr:`dispensed_volume`
            reagent: the :class:`.Reagent` required or ``None`` to indicate the
                     :class:`Well`'s :attr:`reagent`
        Keyword Args:
            on_reagent_mismatch: an :class:`.ErrorHandler` for the case in which
                                 ``reagent`` doesn't match the :class:`Well`'s
                                 :attr:`reagent`
        Returns:
            a :class:`.Delayed`\[:class:`Well`] that will receive this
            :class:`Well` when the availability has been confirmed

        """
        if reagent is not None:
            on_reagent_mismatch.expect_true(self.can_accept(reagent),
                                            lambda : f"{self} contains {self.reagent}.  Expected {reagent}")
        current_volume = self.volume
        resulting_volume = current_volume + volume
        if resulting_volume <= self.max_fill or resulting_volume.is_close_to(self.max_fill,
                                                                             abs_tol=0.05*self.dispensed_volume):
            # print(f"{resulting_volume:g} <= {self.max_fill:g}")
            return Delayed.complete(self)
        # print(f"Need to empty well ({resulting_volume:g} > {self.max_fill:g}")
        return self.empty_well().transformed(lambda _: self)

    class TransitionTo(CSOperation['Well','Well']):
        """
        An :class:`.Operation` that requests that a :class:`Well` transition to
        a new :class:`WellState`.  Typically called from
        :class:`.Drop.DispenseFrom` (``target`` = :attr:`~WellState.DISPENSED`)
        or :class:`.Drop.EnterWell` (``target`` = :attr:`~WellState.ABSORBED`).

        Implemented by creating a :class:`WellMotion` and iterating through its
        :func:`~WellMotion.iterator`.  The value posted to the resulting
        :class:`Delayed` object on completion will be the :class:`Well` this
        :class:`.Operation` is scheduled for.
        """
        target: Final[WellState]    #: The target :class:`WellState`
        guard: Final[Optional[Iterator[bool]]]
        """
        The :class:`WellMonition`'s :attr:`~WellMonition.guard`
        """

        def __init__(self, target: WellState, *,
                     guard: Optional[Iterator[bool]] = None
                     ) -> None:
            """
            Initialize the object.

            Args:
                target: the target :class:`WellState`
                guard: an optional guard to use when creating the
                       :class:`WellMotion`
            """
            self.target = target
            self.guard = guard

        def _schedule_for(self, well: Well, *,
                          post_result: bool = True,
                          )-> Delayed[Well]:
            """
            The implementation of :func:`~.Operation.schedule_for`.

            Creates a :class:`WellMotion` and iterates through its
            :func:`~WellMotion.iterator`.

            The posted value will be ``well``.

            :meta public:
            Args:
                well: the :class:`Well` to schedule the operation for
            Keyword Args:
                post_result: whether to post ``well`` to the returned future
                             object
            Returns:
                a :class:`Delayed`\[:class:`.Well`] future object to which
                ``well`` will be posted unless ``post_result`` is ``False``
            """

            board = well.board
            motion = WellMotion(well, self.target, post_result=post_result, guard=self.guard)
            # target = self.target
            # assert target is WellState.DISPENSED or target is WellState.ABSORBED, \
                # f"Well provided on transition to {target}"
            # if target is WellState.DISPENSED:
            #     motion.pad_states[well.exit_pad] = OnOff.ON
            # motion.pad_states[well.exit_pad] = OnOff.ON if target is WellState.DISPENSED else OnOff.OFF

            def before_tick() -> Iterator[Optional[Ticks]]:
                iterator = motion.iterator()
                one_tick = 1*tick
                while next(iterator):
                    yield one_tick
                yield None
            iterator = before_tick()
            board.before_tick(lambda: next(iterator))
            return motion.initial_future

class Magnet(BinaryComponent['Magnet']):
    """
    A magnet that affects a set of :class:`Pad`\s.

    As a :class:`BinaryComponent`, it has a :attr:`~BoardComponent.board` and a
    :attr:`~BinaryComponent.current_state`, it can act as both a
    :class:`.CommunicationScheduler` and a
    :class:`.OpScheduler`\[:class:`Magnet`], and it supports
    :func:`~BinaryComponent.on_state_change`.

    To initialize this asspect of the :class:`Magnet`, when it is created, it
    must be associated with a :class:`.State`\[:class:`.OnOff`] object that
    knows how to effect any changes on a physical device (via its
    :func:`~.State.realize_state` method).  If nothing needs to be done, a
    :class:`.DummyState` may be used.

    """
    number: int = -1
    """The :class:`Magnet`'s index in its :attr:`board`'s :attr:`~Board.magnets` list"""
    pads: Final[Sequence[Pad]] #: The :class:`Pad`\s affected by this :class:`Magnet`

    def __init__(self, board: Board, *, state: State[OnOff], pads: Sequence[Pad]) -> None:
        """
        Initialize the object.

        Args:
            board: the containing :class:`Board`
        Keyword Args:
            state: the associated :class:`.State`\[:class:`.OnOff`]
            pads: the :class:`Pad`\s affected by this :class:`Magnet`
        """

        BinaryComponent.__init__(self, board, state=state)
        self.pads = pads
        for pad in pads:
            pad._magnet = self

    def __repr__(self) -> str:
        return f"Magnet({map_str(self.pads)})"


class TemperatureMode(Enum):
    """
    An enumeration that tells whether a :class:`TemperatureControl` is
    :attr:`HEATING` or :attr:`CHILLING` to its
    :attr:`~TemperatureControl.target` temperature, maintaining at its
    :attr:`HOT` or :attr:`COLD` target, :attr:`COOLING` or :attr:`WARMING` to
    the ambient temperature, or off and at the :attr:`AMBIENT` temperature.
    """
    AMBIENT = auto()
    """
    The :class:`TemperatureControl`'s :attr:`~TemperatureControl.target` is ``None``, and its
    :attr:~TemperatureControl.current_temperature` is the ambient temperature.
    """
    HOT = auto()
    """
    The :class:`TemperatureControl` has reached its
    :attr:`~TemperatureControl.target` above the ambient temperature and is now
    maintaining that temperature.
    """
    COLD = auto()
    """
    The :class:`TemperatureControl` has reached its
    :attr:`~TemperatureControl.target` below the ambient temperature and is now
    maintaining that temperature.
    """
    HEATING = auto()
    """
    The :class:`TemperatureControl` is actively heating to its
    :attr:`~TemperatureControl.target` above the ambient temperature.
    """
    CHILLING = auto()
    """
    The :class:`TemperatureControl` is actively chilling to its
    :attr:`~TemperatureControl.target` below the ambient temperature.
    """
    COOLING = auto()
    """
    The :class:`TemperatureControl` is passively cooling to its
    :attr:`~TemperatureControl.target` or the ambient temperature if the
    :attr:`~TemperatureControl.target` is ``None``.
    """
    WARMING = auto()
    """
    The :class:`TemperatureControl` is passively warming to its
    :attr:`~TemperatureControl.target` or the ambient temperature if the
    :attr:`~TemperatureControl.target` is ``None``.
    """
    
    @property
    def is_active(self) -> bool:
        return self in (TemperatureMode.HEATING, TemperatureMode.CHILLING, TemperatureMode.HOT, TemperatureMode.COLD)
    
    @property
    def is_passive(self) -> bool:
        return not self.is_active
    
    @property
    def is_maintaining(self) -> bool:
        return self is TemperatureMode.HOT or self is TemperatureMode.COLD
    
    @property
    def going_up(self) -> bool:
        return self is TemperatureMode.HEATING or self is TemperatureMode.WARMING

    @property
    def going_down(self) -> bool:
        return self is TemperatureMode.CHILLING or self is TemperatureMode.COOLING


class TemperatureControl(ABC, BinaryComponent['TemperatureControl']):
    """
    A :class:`BoardComponent` that can be used to control the temperature of its
    associated :attr:`pads`.

    The :class:`TemperatureControl` is controlled by setting its :attr:`target` temperature.
    If its :attr:`current_temperature` is below its :attr:`target`, it attempts
    to become hotter until it reaches the :attr:`target`, at which point it
    attempts to maintain that temperature.  If its :attr:`current_temperature`
    is above its :attr:`target`, it turns off and cools off until it reaches its
    :attr:`target`, at which point it attempts to maintain that temperature.  If
    its :attr:`target` is ``None``, it turns off and cools down to the ambient
    temperature.

    As a :class:`.BinaryComponent`, its :attr:`~.BinaryComponent.current_state`
    is :attr:`~.OnOff.OFF` whenever its :attr:`target` is ``None`` and
    :attr:`~.OnOff.ON` otherwise.  Setting its
    :attr:`~.BinaryComponent.current_state` to :attr:`~.OnOff.OFF` is equivalent
    to setting its :attr:`target` to ``None``. Setting its
    :attr:`~.BinaryComponent.current_state` to a :class:`.TemperaturePoint` is
    equivalent to setting its :attr:`target` to its last non-``None`` value. (If
    there is no such value, its :attr:`~.BinaryComponent.current_state` will be
    reset to :attr:`~.OnOff.OFF`.)

    Note:
        The value of a :class:`TemperatureControl`'s :attr:`~.BinaryComponent.current_state`
        is based on its :attr:`target`, not the state of its underlying
        hardware, so it remains :attr:`~.OnOff.ON` when it is cooling to a
        target temperature or when it turns off briefly while maintaining a
        temperature.  It is also :attr:`~.OnOff.OFF` when its :attr:`target` is
        ``None``, even if it has not yet cooled to the ambient temperature.

    A :class:`TemperatureControl`'s public interface is primarily three
    :class:`.MonitoredProperty`\s, in addition to
    :attr:`~.BinaryComponent.current_state`.  Its :attr:`target` is the
    temperature it is to get to and maintain, or ``None`` to indicate that it
    should turn off.  Its read-only :attr:`current_temperature` is the last read
    (or modeled) temperature.  And its read-only :attr:`mode` is an indication
    of whether it is :attr:`~TemperatureMode.MAINTAINING` its :attr:`target`,
    :attr:`~TemperatureMode.HEATING` to its :attr:`target`,
    :attr:`~TemperatureMode.COOLING` to its :attr:`target` (or to the ambient
    temperature if its :attr:`target` is ``None``), or :attr:`~TemperatureMode.AMBIENT`
    (and at the ambient temperature).  These each have associated
    :class:`.CallbackChangeList`\s: :attr:`~BinaryComponent.on_state_change`,
    :attr:`on_target_change`, :attr:`on_temperature_change`, and
    :attr:`on_mode_change`.

    Note:
        :attr:`current_temperature` can be ``None``.  This indicates that the
        :class:`TemperatureControl` implementation has no way to read the temperature (or
        has not yet done so).  If this is the case, the implementation will have
        to update :attr:`mode` itself, as the automatic updating is by callbacks
        hung on :attr:`on_target_change` and :attr:`on_temperature_change`.


    The actual control of the hardware is expected to be a consequence of the
    the implementation subclass hanging a callback on :attr:`on_target_change`
    (and perhaps :attr:`on_mode_change` or :attr:`on_temperature_change`).  The
    :attr:`current_temperature` is set to the value posted to the result of
    :func:`poll`, which is called every :attr:`polling_interval`.  By default,
    it simply returns a future whose value is ``None``, but this method  is
    expected to be overridden by implementation subclasses. The polling can be
    stopped by :func:`stop_polling` and restarted by :func:`start_polling`.  It
    is started as soon as the :class:`TemperatureControl` joins the :class:`System`.

    Temperature changes on a :class:`TemperatureControl` take place within a
    :class:`UserOperation`, so the :class:`System` will not be considered to be
    idle (and will not exit a ``with system`` block) when the :class:`TemperatureControl`'s
    :attr:`mode` is :attr:`~TemperatureMode.HEATING` or
    :attr:`~TemperatureMode.COOLING`.

    To set the :attr:`target` using an :class:`.Operation`, the
    :class:`TemperatureControl.SetTemperature` operation is provided.  This
    :class:`.Operation` completes when the desired temperature has been reached.
    """
    number: int = -1
    """
    The :class:`TemperatureControl`'s index in its
    :attr:`~BoardComponent.board`'s :attr:`~Board.heaters` or
    :attr:`~Board.chillers` list.  A value of ``-1`` indicates that the
    TemperatureControl has not yet been added to the :class:`Board`.
    """
    locations: Final[Sequence[TempControllable]]
    """
    The locations affected by this :class:`TemperatureControl`
    """
    _pads: tuple[Pad, ...]
    @property
    def pads(self) -> Sequence[Pad]:
        """
        The :class:`Pad`\s affected by this :class:`TemperatureControl`
        """
        try:
            return self._pads
        except AttributeError:
            self._pads = tuple(c for c in self.locations if isinstance(c, Pad))
            return self._pads
    _wells: tuple[Well, ...]
    @property
    def wells(self) -> Sequence[Well]:
        """
        The :class:`Well`\s affected by this :class:`TemperatureControl`
        """
        try:
            return self._wells
        except AttributeError:
            self._wells= tuple(c for c in self.locations if isinstance(c, Well))
            return self._wells
        
        
    @property
    def pads_for_sort(self) -> Sequence[Pad]:
        return (*self.pads, *(w.exit_pad for w in self.wells))
    
    polling_interval: Time
    """
    The :class:`.Time` to wait between calls to :func:`poll` to get a new value
    for :attr:`current_temperature`.
    """
    limit: Final[Optional[TemperaturePoint]]
    """
    The maximum `.TemperaturePoint` this :class:`TemperatureControl` can heat to
    or the minimum `.TemperaturePoint` this :class:`TemperatureControl` can chill to, if known
    """
    
    # max_heat_temperature: Final[Optional[TemperaturePoint]]
    # """
    # The maximum `.TemperaturePoint` this :class:`TemperatureControl` can heat to, or
    # ``None`` if this :class:`TemperatureControl` only chills
    # """
    # @property
    # def can_heat(self) -> bool:
    #     """
    #     Can this :class:`TemperatureControl` heat (as opposed to only chilling)?
    #     """
    #     return self.max_heat_temperature is not None
    #
    # min_chill_temperature: Final[Optional[TemperaturePoint]]
    # """
    # The minimum `.TemperaturePoint` this :class:`TemperatureControl` can chill to, or
    # ``None`` if this :class:`TemperatureControl` only heats
    # """
    # @property
    # def can_chill(self) -> bool:
    #     """
    #     Can this :class:`TemperatureControl` chill (as opposed to only heating)?
    #     """
    #     return self.min_chill_temperature is not None
    
    _lock: Final[RLock]
    """
    An internal lock guarding changes
    """
    _polling: bool = False
    """
    Are we currently polling?
    """
    _user_op: Optional[UserOperation] = None
    """
    The :class:`UserOperation` associated with this :class:`TemperatureControl`.  This
    starts out ``None``, because it cannot be created until the :class:`TemperatureControl`
    joins a :class:`System`.
    """
    _last_target: Optional[TemperaturePoint] = None
    """
    The last non-``None`` :attr:`target` for this :class:`TemperatureControl`.  This is the
    value used when :attr:`~BinaryComponent.current_state` is set to
    :attr:`.OnOff.ON`.
    """

    _temperature: MonitoredProperty[Optional[TemperaturePoint]] = MonitoredProperty(default=None)
    """
    The private, settable value behind :attr:`current_temperature`
    """
    @property
    def current_temperature(self) -> Optional[TemperaturePoint]:
        """
        The current :class:`.TemperaturePoint` of the :class:`TemperatureControl`.  This is
        set to the value (posted to the future) returned by :func:`poll`.  If
        this value is ``None``, it means that no temperature has been
        established yet or the device cannot read its own temperature.

        Note:
            If, for some reason, an implementation needs to set this at some
            other time, the actual :class:`.MonitoredProperty` is
            :attr:`_temperature`
        """
        return self._temperature
    on_temperature_change: ChangeCallbackList[Optional[TemperaturePoint]] = _temperature.callback_list
    """
    The :class:`.ChangeCallbackList` monitoring :attr:`current_temperature`
    """

    target: MonitoredProperty[Optional[TemperaturePoint]] = MonitoredProperty(default=None)
    """
    The target :class:`.TemperaturePoint` of the :class:`TemperatureControl` or ``None`` to
    indicate that the :class:`TemperatureControl` should turn off and return to ambient temperature.
    """
    on_target_change: ChangeCallbackList[Optional[TemperaturePoint]] = target.callback_list
    """
    The :class:`.ChangeCallbackList` monitoring :attr:`target`
    """
    
    @abstractmethod
    def _check_target(self, target: Optional[TemperaturePoint]) -> MissingOr[Optional[TemperaturePoint]]: # @UnusedVariable
        ...
    
    @target.transform
    def clip_target(self, target: Optional[TemperaturePoint]) -> MissingOr[Optional[TemperaturePoint]]:
        return self._check_target(target)

    _mode: MonitoredProperty[TemperatureMode] = MonitoredProperty(default=TemperatureMode.AMBIENT)
    @property
    def mode(self) -> TemperatureMode:
        """
        The :class:`TemperatureControl`'s current :class:`TemperatureMode`.  If this is
        :attr:`~TemperatureMode.HEATING` or :attr:`~TemperatureMode.COOLING`, the
        :class:`TemperatureControl` is moving toward its :attr:`target` (or the ambient
        temperature if the  :attr:`target` is ``None``).  If it is
        :attr:`TemperatureMode.MAINTAINING`, the :class:`TemperatureControl` has reached its
        target and is attempting to maintain the temperature there.  And if it
        is :attr:`TemperatureMode.AMBIENT`, the :attr:`target` is ``None`` and the
        :class:`TemperatureControl` has cooled down to ambient temperature.
        """
        return self._mode
    on_mode_change: ChangeCallbackList[TemperatureMode] = _mode.callback_list
    """
    The :class:`.ChangeCallbackList` monitoring :attr:`mode`
    """
    
    tolerance: Temperature = 0.1*deg_C

    def __init__(self, board: Board, *,
                 locations: Sequence[TempControllable],
                 polling_interval: Time,
                 limit: Optional[TemperaturePoint],
                 # max_heat: Optional[TemperaturePoint],
                 # min_chill: Optional[TemperaturePoint],
                 initial_temperature: Optional[TemperaturePoint] = None,
                 ) -> None:
        """
        Initialize the object.

        Args:
            num: the :class:`TemperatureControl`'s index in its :attr:`~BoardComponent.board`'s
                 :attr:`~Board.temperature_controls` list
            board: the containing :class:`Board`
        Keyword Args:
            pads: the :class:`Pad`\s affected by this :class:`TemperatureControl`

            polling_interval: the :class:`.Time` to wait between calls to
                              :func:`poll`

            initial_temperature: an optional initial value for
                                 :attr:`current_temperature`
        """
        super().__init__(board=board, state=DummyState(initial_state=OnOff.OFF))
        self.locations = tuple(locations)
        self.limit = limit
        # self.max_heat_temperature = max_heat
        # self.min_chill_temperature = min_chill
        self._mode = TemperatureMode.AMBIENT
        self.polling_interval = polling_interval
        self._lock = RLock()
        # self._current_op_key = None
        for loc in locations:
            loc._temperature_control = self

        self.on_state_change(self._note_state_change)
        self.on_mode_change(self._note_mode_change)
        self.on_target_change(self._note_target_change)
        self.on_temperature_change(self._note_temperature_change)

        self._temperature = initial_temperature

    def _note_state_change(self, _old: OnOff, new: OnOff) -> None:
        with self._lock:
            # Turning on goes to the last target.  If we're called as a result
            # of setting target, this won't be a change, so no regress.  If
            # there was no last target, setting the target to None will turn us
            # off.
            if new is OnOff.OFF:
                self.target = None
            else:
                self.target = self._last_target

    def _note_mode_change(self, _old: TemperatureMode, new: TemperatureMode) -> None:
        # print(f"Mode is now {new}")
        with self._lock:
            # The operation ends when we hit ambient (OFF) or the target
            # (MAINTAINING).  If we're heating or cooling, we're still (or
            # newly) in the operation.
            op = self._user_op
            if op is None:
                op = self.user_operation()
                self._user_op = op
            if new is TemperatureMode.AMBIENT or new.is_maintaining:
                op.end()
            else:
                op.start()
            # print(f"{self}.mode now {new} (target: {self.target}, current: {self.current_temperature})")

    @property
    @abstractmethod
    def driving_mode(self) -> TemperatureMode: ...
    
    @property
    @abstractmethod
    def returning_mode(self) -> TemperatureMode: ...

    @property
    @abstractmethod
    def maintaining_mode(self) -> TemperatureMode: ...
        
    @abstractmethod
    def is_driving(self, current: TemperaturePoint, target: TemperaturePoint) -> bool: ... # @UnusedVariable
    
    def _new_mode(self, target: Optional[TemperaturePoint],
                  current: Optional[TemperaturePoint]) -> TemperatureMode:
        if current is None:
            # If we don't have a reading, there isn't a whole lot we can do.
            return TemperatureMode.AMBIENT if target is None else self.driving_mode
        elif target is not None and current.is_close_to(target, abs_tol = self.tolerance):
            return self.maintaining_mode
        elif target is None and self.board.is_ambient(current):
            return TemperatureMode.AMBIENT
        elif target is not None and self.is_driving(current, target):
            return self.driving_mode
        else:
            return self.returning_mode

    def _note_target_change(self,  _old: Optional[TemperaturePoint],
                            new: Optional[TemperaturePoint]) -> None:
        with self._lock:
            # We remember this as the last target if it's non-None.  When we set
            # the current state, it will try to set the target to this, which
            # won't be a change, so we won't be called again.
            if new is not None:
                self._last_target = new
            self.current_state = OnOff.from_bool(new is not None)
            self._mode = self._new_mode(new, self.current_temperature)

    def _note_temperature_change(self, _d: Optional[TemperaturePoint],
                                 new: Optional[TemperaturePoint]) -> None:
        if new is None:
            return
        with self._lock:
            target = self.target
            mode = self.mode
            if mode is TemperatureMode.AMBIENT or mode.is_maintaining:
                # If we're already off or maintaining, we assume that
                # temperature fluctuations don't change our mode.
                return
            self._mode = self._new_mode(target, new)
            # if mode is TemperatureMode.HEATING:
            #     assert target is not None
            #     if new >= target:
            #         self._mode = TemperatureMode.HOT
            # else:
            #     if target is None:
            #         if self.board.is_ambient(new):
            #             self._mode = TemperatureMode.AMBIENT
            #     elif new <= target:
            #         self._mode = TemperatureMode.HOT

    def start_polling(self) -> None:
        """
        Start (or resume) calling :func:`poll` to get new values for
        :attr:`current_temperature`.  Calls will be repeated with a delay of
        :attr:`polling_interval`.

        Calling :func:`start_polling` while polling is running does nothing.

        Note:
            :func:`start_polling` is called when the :class:`TemperatureControl`'s
            :attr:`board` joins a :class:`System`.
        """
        if self._polling:
            return
        self._polling = True
        def do_poll() -> Optional[Time]:
            def set_temp(t: Optional[TemperaturePoint]) -> None:
                self._temperature = t
            self.poll().then_call(set_temp)
            return self.polling_interval if self._polling else None
        self.board.call_after(Time.ZERO, do_poll, daemon=True)

    def stop_polling(self) -> None:
        """
        Stop calling :func:`poll` to get new values for :attr:`current_temperature`.

        Calling :func:`stop_polling` while polling is stopped does nothing.
        """
        self._polling = False

    def __repr__(self) -> str:
        return f"TemperatureControl({self.number})"

    # If the implementation doesn't override, then we always get back None (immediately)
    def poll(self) -> Delayed[Optional[TemperaturePoint]]:
        """
        Determine the current temperature.  Returns a :class:`.Delayed` object
        which will receive a :class:`.TemperaturePoint` or ``None`` to indicate
        that the temperature cannot be determined.

        When this is called during polling (i.e., after :func:`start_polling`
        has been called), when the future receives a value, it will become the
        new value of :attr:`current_temperature`.

        Note:
            The default implementation always returns a future that contains
            ``None``.

        Returns
            a future which will get the new value for
            :attr:`current_temperature`
        """
        return Delayed.complete(None)

    class SetTemperature(CSOperation['TemperatureControl','TemperatureControl']):
        """
        A :class:`~.Operation` that modifies the :attr:`~TemperatureControl.target` of a
        :class:`TemperatureControl`.  The :class:`~.Operation` is considered complete (and
        its future receives the :class:`TemperatureControl` as its value) when the
        :class:`TemperatureControl`'s :attr:`~TemperatureControl.current_temperature` reaches this
        target temperature.  (More precisely, when its :attr:`~TemperatureControl.mode`
        becomes :attr:`~TemperatureMode.MAINTAINING` or :attr:`~TemperatureMode.AMBIENT`.

        Note:
            If another :class:`SetTemperature` operation is scheduled before
            this one completes, this operation is cancelled, and its future will
            never receive a value.
        """
        target: Final[Optional[TemperaturePoint]]
        """
        The target :class:`TemperaturePoint` or ``None`` to indicate that the
        TemperatureControl should turn off and return to ambient temperature.
        """
        key_attr: Final[str] = "__set_temp_monitor_key"
        """
        The name of the attribute to use to store the key for the callback
        monitoring for :attr:`~TemperatureControl.mode` changes.
        """

        def _schedule_for(self, temperature_control: TemperatureControl, *,
                          post_result: bool = True,
                          ) -> Delayed[TemperatureControl]:
            """
            The implementation of :func:`~.Operation.schedule_for`. Sets
            ``temperature_control``'s :attr:`~TemperatureControl.target` and monitors changes in its
            :attr:`~TemperatureControl.mode`.  When this becomes
            :attr:`~TemperatureMode.MAINTAINING` or :attr:`~TemperatureMode.AMBIENT`,
            ``TemperatureControl`` is posted to the returned future.

            If another :class:`SetTemperature` is currently in progress, it is
            silently aborted.

            :meta public:
            Args:
                obj: the :class:`TemperatureControl` to schedule the operation for
            Keyword Args:
                post_result: whether to post the resulting value to the returned future object
            Returns:
                a :class:`Delayed`\[:class:`TemperatureControl`] future object to which the resulting
                value will be posted unless ``post_result`` is ``False``
            """
            future: Postable[TemperatureControl] = Postable()
            target = self.target

            def do_it() -> None:
                with temperature_control._lock:
                    attr = self.key_attr
                    old_key = getattr(temperature_control, attr, None)
                    if old_key is not None:
                        temperature_control.on_mode_change.remove(old_key)
                    if post_result:
                        key = (temperature_control, f"Temp->{target}", random.random())
                        def check(_old: TemperatureMode, mode: TemperatureMode) -> None:
                            if mode is TemperatureMode.AMBIENT or mode.is_maintaining:
                                future.post(temperature_control)
                                temperature_control.on_mode_change.remove(key)
                                setattr(temperature_control, attr, None)
                        setattr(temperature_control, attr, key)
                        temperature_control.on_mode_change(check, key=key)
                    temperature_control.target = target
            temperature_control.board.schedule(do_it)
            return future


        def __init__(self, target: Optional[TemperaturePoint]) -> None:
            """
            Initialize the object.

            Args:
                target: the target :class:`.TemperaturePoint` or ``None`` to
                        indicate that the :class:`TemperatureControl` should turn off.
            """
            self.target = target
            
            
class Heater(TemperatureControl):
    @property
    def max_target(self) -> Optional[TemperaturePoint]:
        return self.limit
    
    @property
    def driving_mode(self) -> TemperatureMode:
        return TemperatureMode.HEATING
    
    @property
    def returning_mode(self) -> TemperatureMode:
        return TemperatureMode.COOLING
    
    @property
    def maintaining_mode(self) -> TemperatureMode:
        return TemperatureMode.HOT
    
    def __repr__(self) -> str:
        return f"Heater({self.number})"
    
    
    def is_driving(self, current: TemperaturePoint, target: TemperaturePoint)->bool:
        return current < target
    
    def _check_target(self, target: Optional[TemperaturePoint])->Optional[TemperaturePoint]:
        if target is not None:
            max_temp = self.max_target
            if max_temp is not None and target > max_temp:
                logger.warn(f"{self}: target ({target}) > maximum ({max_temp}), clipping")
                return max_temp
            ambient = self.board.ambient_temperature
            if target <= ambient:
                logger.warn(f"{self}: target ({target}) <= ambient ({ambient}), turning off")
                return None
        return target

class Chiller(TemperatureControl):
    @property
    def min_target(self) -> Optional[TemperaturePoint]:
        return self.limit
    
    @property
    def max_target(self) -> Optional[TemperaturePoint]:
        return self.limit
    
    @property
    def driving_mode(self) -> TemperatureMode:
        return TemperatureMode.CHILLING
    
    @property
    def returning_mode(self) -> TemperatureMode:
        return TemperatureMode.WARMING
    
    @property
    def maintaining_mode(self) -> TemperatureMode:
        return TemperatureMode.COLD
    
    def __repr__(self) -> str:
        return f"Chiller({self.number})"

    def is_driving(self, current: TemperaturePoint, target: TemperaturePoint)->bool:
        return current > target
    
    def _check_target(self, target: Optional[TemperaturePoint])->Optional[TemperaturePoint]:
        if target is not None:
            min_temp = self.min_target
            if min_temp is not None and target < min_temp:
                logger.warn(f"{self}: target ({target}) < maximum ({min_temp}), clipping")
                return min_temp
            ambient = self.board.ambient_temperature
            if target >= ambient:
                logger.warn(f"{self}: target ({target}) >= ambient ({ambient}), turning off")
                return None
        return target


            
class ProductLocation(NamedTuple):
    """
    The final disposition of the :class:`.Liquid` transfered by
    :func:`ExtractionPoint.transfer_out`.

    Contains a :class:`.Reagent` (:attr:`reagent`) and a :attr:`location`, which
    can be of any type.
    """
    reagent: Reagent
    """
    The :class:`.Reagent` that was transfered
    """
    location: Any
    """
    The location to which it was transfered
    """

class ExtractionPoint(OpScheduler['ExtractionPoint'], BoardComponent, PipettingTarget):
    """
    A component, (typically a hole in a :class:`Board`'s lid) that enables a
    :class:`.Pipettor` to add :class:`.Liquid` to or remove :class:`.Liquid`
    from a :class:`.Pad`.

    As a :class:`BoardComponent`, the :class:`ExtractionPoint` is associated
    with the same :attr:`~BoardComponent.board` as its :attr:`pad`.

    As a :class:`PipettingTarget`, :class:`ExtractionPoint` implements the
    pipetting protocol:

    * It has an (optional) associated :attr:`~PipettingTarget.pipettor`.  By
      default this is ``None``. A subclass should either provide one or override
      the implementations of :func:`transfer_in` and :func:`transfer_out`.

    * It can report its :attr:`removable_liquid`.  By default, this will be the
     :attr:`~.Blob.contents` of the :class:`Blob` that contains the
     :class:`Drop` (if any) at the :class:`ExtractionPoint`'s :attr:`pad`.

    * When the :class:`.Pipettor` is in position to add liquid, it calls
      :func:`prepare_for_add` and waits for it to complete.  By default, this
      reserves :attr:`pad` and turns it on.

    * After adding liquid, the :class:`.Pipettor` calls :func:`pipettor_added`.
      By default, this adds the described :class:`.Liquid`, and if this is the
      last transfer, unreserves :attr:`pad`.

    * When the :class:`.Pipettor` is in position to remove liquid, it calls
      :func:`prepare_for_remove`, which waits until there is a drop on
      :attr:`pad`.

    * After adding liquid, the :class:`.Pipettor` calls
      :func:`pipettor_removed`, which removes the described :class:`.Liquid`
      and, if there is no further :class:`.Liquid` in :attr:`pad`'s
      :attr:`~DropLoc.blob`, turns it off.

    To request that :class:`.Liquid` be transfered via an
    :class:`ExtractionPoint`, use :func:`transfer_in` and :func:`transfer_out`
    (or their wrapper :class:`.Operation`\s :class:`TransferIn` and
    :class:`TransferOut`).  The default implementations of these schedule
    :class:`.Pipettor.Supply` and :class:`.Pipettor.Extract` on
    :attr:`~PipettingTarget.pipettor`, failing an assertion if
    :attr:`~PipettingTarget.pipettor` is ``None``.

    When extracting using :func:`transfer_out` (or :class:`TransferOut`), if
    ``is_product`` is ``True`` (the default), the system is instructed to treat
    the extracted :class:`.Liquid` as a product of the overall process and
    identify a new location (e.g., in an product well plate) to store it.  If
    ``product_loc`` is also provided, a :class:`ProductLocation` (a combination
    of the :class:`.Reagent` and an implementation-specific description of the
    location) will be posted to it.
    """
    pad: Final[Pad] #: The :class:`Pad` associated with this :class:`ExtractionPoint`
    reserved_pads: set[Pad]
    splash_radius: Final[int]
    number: int = -1

    _splash_zone: Optional[set[Pad]] = None
    _splash_border: Optional[Sequence[Pad]] = None

    @property
    def removable_liquid(self) -> Optional[Liquid]:
        """
        The :class:`.Liquid` that could be removed via this
        :class:`ExtractionPoint` or ``None`` if there is no such
        :class:`.Liquid`.

        By default, this is the :attr:`~.Blob.contents` of the :class:`.Blob` at
        :attr:`pad` if there is a :class:`.Drop` there, otherwise ``None``.

        Note:
            The volume is that of the entire :class:`.Blob`, not merely the
            portion allocable to the :class:`.Drop` at the :class:`Pad`.

            Note also that the :class:`Pad`'s :attr:`~DropLoc.blob` may be
            non-``None`` even if there is no :class:`Drop` (in which case its
            volume will be zero).  In this case, :attr:`removable_liquid` will
            be ``None``, not a zero-volume :class:`.Liquid`.

        """
        drop = self.pad.drop
        if drop is None:
            return None
        return drop.blob.contents

    @property
    def splash_zone(self) -> set[Pad]:
        if self._splash_zone is None:
            self._compute_splash()
        return not_None(self._splash_zone)

    @property
    def splash_border(self) -> Sequence[Pad]:
        if self._splash_border is None:
            self._compute_splash()
        return not_None(self._splash_border)

    def __init__(self, pad: Pad, *, splash_radius: Optional[int] = None) -> None:
        """
        Initialize the object.

        Args:
            pad: the :class:`Pad` associated with the :class:`ExtractionPoint`.
        """
        BoardComponent.__init__(self, pad.board)
        self.pad = pad
        if splash_radius is None:
            splash_radius = pad.board.extraction_point_splash_radius
        self.splash_radius = splash_radius
        self.reserved_pads = set()
        pad._extraction_point = self

    def __repr__(self) -> str:
        return f"ExtractionPoint[{self.pad.location}]"

    def prepare_for_add(self) -> None:
        """
        Block until it is safe for a :class:`.Pipettor` to add :class:`.Liquid`.
        This method is called when the :class:`.Pipettor` is in position.

        By default, it reserves :attr:`pad` and turns it on.
        """
        expect_drop = self.pad.drop is not None
        self.reserve_pads(expect_drop=expect_drop).wait()
        self.pad.schedule(Pad.TurnOn).wait()

    def pipettor_added(self, reagent: Reagent, volume: Volume, *,
                       last: bool,
                       mix_result: Optional[MixResult]) -> None:
        """
        Called when the :class:`.Pipettor` has finished adding :class:`.Liquid`.
        If ``mix_result`` is not ``None``, it should be used as the result of
        mixing the delivered :class:`.Liquid` to what is already there.  If
        ``last`` is ``False``, there will be at least one more transfer before
        the overall transfer operation is complete.

        By default, calls :func:`Pad.liquid_added` on :attr:`pad` if ``volume``
        is non-zero.  If ``last`` is ``True``, unreserves :attr:`pad`.

        Args:
            reagent: the :class:`.Reagent` added
            volume: the :class:`.Volume` of :class:`.Reagent` added
        Keyword Args:
            mix_result: the (optional) result of mixing the added
                        :class:`.Liquid` with what's already there.
            last: ``True`` if this is the last transfer in a transfer request.
        """
        if volume > Volume.ZERO:
            got = Liquid(reagent, volume)
            self.pad.liquid_added(got, mix_result=mix_result)
        if last:
            self.unreserve_pads()

    def prepare_for_remove(self) -> None:
        """
        Block until it is safe for a :class:`.Pipettor` to remove
        :class:`.Liquid`. This method is called when the :class:`.Pipettor` is
        in position.

        By default, it waits until there is a :class:`.Drop` on :attr:`pad`.
        """
        from mpam.drop import Blob # @Reimport
        
        def after_drop(drop: Drop) -> Delayed[None]:
            return (self.reserve_pads(expect_drop=True)
                    .chain(lambda _: Blob.TurnOff.schedule_for(drop.blob)))
        self.ensure_drop().chain(after_drop).wait()
        

    def pipettor_removed(self, reagent: Reagent, volume: Volume, # @UnusedVariable
                         *, last: bool) -> None: # @UnusedVariable
        """
        Called when the :class:`.Pipettor` has finished removing
        :class:`.Liquid`. If ``last`` is ``False``, there will be at least one
        more transfer before the overall transfer operation is complete.

        By default, calls :func:`Pad.liquid_remove` if ``volume`` is non-zero.
        If this results in an empty :class:`.Blob`, schedules turning off all
        :class:`Pad`\s in the :class:`.Blob`.

        Args:
            reagent: the :class:`.Reagent` removed
            volume: the :class:`.Volume` of :class:`.Reagent` removed
        Keyword Args:
            last: ``True`` if this is the last transfer in a transfer request.
        """
        from mpam.drop import Blob # @Reimport
        
        pad = self.pad
        if volume > 0:
            pad.liquid_removed(volume)
        blob = pad.blob
        
        if blob is not None and not blob.total_volume.is_zero:
            Blob.TurnOn.schedule_for(blob)
        
        if last:
            self.unreserve_pads()

    def transfer_out(self, *,
                     volume: Optional[Volume] = None,
                     on_no_sink: ErrorHandler = PRINT,
                     is_product: bool = True,
                     product_loc: Optional[Postable[ProductLocation]] = None
                     ) -> Delayed[Liquid]:
        """
        Request that :class:`.Liquid` be extracted through the
        :class:`ExtractionPoint`.  The method returns a future to which the
        :class:`.Liquid` actually transfered will be posted when all of the
        :class:`.Liquid` that will be removed has been.

        If ``volume`` is ``None``, the volume of the :class:`.Blob` at
        :attr:`pad` (which must exist) is used.

        If ``is_product`` is ``True``, this transfer represents the extraction
        of a product and a new location (e.g., a new well in a product well
        plate) will be chosen for it.  If ``product_loc`` is not ``None``, a
        :class:`ProductLocation` will be posted to it describing the
        :class:`.Reagent` and location.

        If a location cannot be determined for the extracted :class:`.Liquid`,
        ``on_no_sink`` will be invoked.  If control continues, the
        :class:`.Pipettor` doing the removal is encouraged to dump the extracted
        :class:`.Liquid` into a trash receptacle or waste drain.

        By default, the transfer is implemented by scheduling a
        :class:`.Pipettor.Extract` :class:`.Operation` on the
        :class:`ExtractionPoint`'s :attr:`~PipettingTarget.pipettor` (which must
        exist).  Subclasses are free to override :func:`transfer_out` to remove
        this restriction.

        Note:
            The :attr:`~.Liquid.volume` of the :class:`.Liquid` posted to the
            resulting future may be different from ``volume``.

        Note:
            The value will be posted to the resulting future when the last of
            the liquid is removed, not when it reaches its destination.  The
            value posted to :class:`product_loc` can happen at any time.

        Args:

            volume: the :class:`.Volume` to remove or ``None`` to indicate using
                    the volume of the :class:`.Blob` at :attr:`pad` (which must
                    exist).
        Keyword Args:

            on_no_sink: an :class:`.ErrorHandler` invoked when there is no place
                        to store the extracted :class:`.liquid`.

            is_product: ``True`` if this transfer represents the extraction of a
                        product.

            product_loc: an optional :class:`.Postable` future to which the
                         resulting :class:`ProductLocation` will be posted if
                         ``is_product`` is ``True``.
        Returns:
            a :class"`.Delayed`\[:class:`.Liquid`] which receives the
            :class:`.Liquid` actually transfered.
        """
        pipettor = self.pipettor
        assert pipettor is not None, f"{self} has no pipettor and transfer_out() not overridden"
        if volume is None:
            drop = not_None(self.pad.drop, desc=lambda: f"{self.pad}.drop")
            volume = drop.blob_volume
        p_future = pipettor.schedule(pipettor.Extract(volume, self,
                                                      is_product = is_product,
                                                      product_loc = product_loc,
                                                      on_no_sink = on_no_sink))
        return p_future

    def transfer_in(self, reagent: Reagent, volume: Volume, *,
                     mix_result: Optional[MixResult]=None,
                     on_insufficient: ErrorHandler=PRINT,
                     on_no_source: ErrorHandler=PRINT
                     ) -> Delayed[Drop]:
        """
        Request that :class:`.Liquid` be extracted through the
        :class:`ExtractionPoint`.  The method returns a future to which the
        :class:`.Drop` on :attr:`pad` will be posted after all of the
        :class:`.Liquid` that will be added has been.

        ``on_no_source`` will be invoked if a source for ``reagent`` cannot be
        determined.  ``on_insufficient`` will be invoked if ``volume`` of
        ``reagent`` cannot be obtained.

        If there is already :class:`.Liquid` on :attr:`pad`, the added
        :class:`.Liquid` will be mixed with it.  If ``mix_result`` is not
        ``None``, it will be used as (or to fine) the resulting
        :class:`.Reagent`.

        By default, the transfer is implemented by scheduling a
        :class:`.Pipettor.Supply` :class:`.Operation` on the
        :class:`ExtractionPoint`'s :attr:`~PipettingTarget.pipettor` (which must
        exist). Subclasses are free to override :func:`transfer_in` to remove
        this restriction.

        Note:
            The :attr:`~.Liquid.volume` of the :class:`.Liquid` posted to the
            resulting future may be different from ``volume``.

        Args:
            reagent: the :class:`.Reagent` to transfer in
            volume: the :class:`.Volume` of ``reagent`` to transfer in
        Keyword Args:
            mix_result: the resulting :class:`.Reagent`, the name of the computed
                        :class:`.Reagent`, or ``None`` (indicating that the name
                        should be computed), when :attr:`pad` is not empty

            on_insufficient: an :class:`.ErrorHandler` invoked if ``volume`` of
                             ``reagent`` cannot be obtained

            on_no_source: an :class:`.ErrorHandler` invoked if ``reagent`` cannot
                          be obtained
        """
        from mpam.drop import Drop # @Reimport
        pipettor = self.pipettor
        assert pipettor is not None, f"{self} has no pipettor and transfer_in() not overridden"
        p_future = pipettor.schedule(pipettor.Supply(reagent, volume, self,
                                                     mix_result = mix_result,
                                                     on_insufficient = on_insufficient,
                                                     on_no_source = on_no_source))
        future = Postable[Drop]()
        # If I use a lambda, Mypy complains about not being able to infer the
        # type of the argument 1 [sic] of post_transformed_to()
        def xfer_result(_: Any) -> Drop:
            return not_None(self.pad.drop)

        p_future.post_transformed_to(future, xfer_result)
        return future

    def reserve_pads(self, *, expect_drop: bool = False) -> Delayed[None]:
        """
        Reserve :attr:`pad`, waiting until ``expect_drop`` matches whether
        there is a :class:`.Drop` at :attr:`pad`. A splash zone around
        the pad is also reserved if a :attr:`splash_radius` has been
        set.

        Args:
            expect_drop: ``True`` if the reservation should delay until there is
                         a :class:`.Drop` at :attr:`pad`, ``False`` if it should
                         wait until there is not.
        Returns:
            a future that will receive a value when the reservation is successful

        """
        # to_reserve stores pads that need to be reserved. Once a pad
        # is reserved, it gets removed from the list
        to_reserve = list(self.splash_zone)
        # logging.debug(f'{self.pad}|splash zone:{self.splash_zone}')
        # logging.debug(f'{self.pad}|splash border:{self.splash_border}')

        def reserve_condition() -> bool:
            # Check if the drop expectation is not met
            if expect_drop and self.pad.drop is None:
                return False
            if not expect_drop and self.pad.drop is not None:
                return False

            nonlocal to_reserve
            not_reserved = []
            for pad in to_reserve:
                if pad.reserve():
                    self.reserved_pads.add(pad)
                    # logging.debug(f'{self.pad}|splash|reserved:{pad}')
                else:
                    not_reserved.append(pad)
            to_reserve = not_reserved

            # For each pad on the border that had a drop, need to
            # reserve all its neighbors as well
            is_extra_reserved = True
            for pad in self.splash_border:
                if pad.drop is not None:
                    for neighbor in pad.all_neighbors:
                        if neighbor not in self.splash_zone and neighbor not in self.reserved_pads:
                            if neighbor.reserve():
                                self.reserved_pads.add(neighbor)
                                # logging.debug(f'{self.pad}|splash|reserved for border:{pad}')
                            else:
                                is_extra_reserved=False

            if len(to_reserve) == 0 and is_extra_reserved:
                # logging.debug(f'{self.pad}|splash|reserved all:{self.reserved_pads}')
                return True
            return False

        return self.pad.board.on_condition(reserve_condition, lambda: None)

    def unreserve_pads(self) -> None:
        """
        Unreserve any reserved pads
        """
        # logging.debug(f'{self.pad}|splash|unreserve:{self.reserved_pads}')
        while self.reserved_pads:
            self.reserved_pads.pop().unreserve()

    def ensure_drop(self) -> Delayed[Drop]:
        """
        Notify when there is a :class:`.Drop` at :attr:`pad`.

        Returns:
            a future that will receive a value when there is a :class:`.Drop` at
            :attr:`pad`
        """
        pad = self.pad
        return pad.board.on_condition(lambda: pad.drop is not None, 
                                      lambda: not_None(pad.drop, 
                                                       desc=lambda: f"{self} lost drop during ensure_drop()"))

    def _compute_splash(self) -> None:
        zone = set([self.pad])
        border = []
        if self.splash_radius > 0:
            border = [self.pad]
            for _ in range(self.splash_radius):
                new_border = []
                for pad in border:
                    for direction in Dir:
                        new_pad = pad.neighbor(direction, only_existing=False)
                        if new_pad is not None and new_pad not in zone:
                            new_border.append(new_pad)
                            zone.add(new_pad)
                border = new_border
        self._splash_zone = set(p for p in zone if p.exists)
        self._splash_border = [p for p in border if p.exists]

    class TransferIn(CSOperation['ExtractionPoint', 'Drop']):
        """
        A :class:`~.Operation` to transfer in :class:`.Liquid` via an :class:`ExtractionPoint`.

        Implemented by wrapping :func:`ExtractionPoint.transfer_in`.
        """
        reagent: Final[Reagent]
        """
        The :class:`.Reagent` to transfer in
        """
        volume: Final[Optional[Volume]]
        """
        The :class:`.Volume` of :attr:`reagent` to transfer in
        """
        mix_result: Final[Optional[MixResult]]
        """
        the resulting :class:`.Reagent`, the name of the computed
        :class:`.Reagent`, or ``None`` (indicating that the name should be
        computed), when the :class:`ExtractionPoint`'s
        :attr:`~ExtractionPoint.pad` is not empty
        """
        on_insufficient: Final[ErrorHandler]
        """
        an :class:`.ErrorHandler` invoked if :attr:`volume` of :attr:`reagent`
        cannot be obtained
        """
        on_no_source: Final[ErrorHandler]
        """
        an :class:`.ErrorHandler` invoked if :attr:`reagent` cannot be obtained
        """

        def __init__(self, reagent: Reagent, volume: Optional[Volume] = None, *,
                     mix_result: Optional[Union[Reagent, str]] = None,
                     on_insufficient: ErrorHandler = PRINT,
                     on_no_source: ErrorHandler = PRINT
                     ) -> None:
            """
            Initialize the object

            Args:
                reagent: the :class:`.Reagent` to transfer in
                volume: the :class:`.Volume` of ``reagent`` to transfer in
            Keyword Args:

                mix_result: the resulting :class:`.Reagent`, the name of the computed
                            :class:`.Reagent`, or ``None`` (indicating that the
                            name should be computed), when the
                            :class:`ExtractionPoint`'s
                            :attr:`~ExtractionPoint.pad` is not empty

                on_insufficient: an :class:`.ErrorHandler` invoked if ``volume`` of
                                 ``reagent`` cannot be obtained
                on_no_source: an :class:`.ErrorHandler` invoked if ``reagent`` cannot
                              be obtained
            """
            self.reagent = reagent
            self.volume = volume
            self.mix_result = mix_result
            self.on_insufficient = on_insufficient
            self.on_no_source = on_no_source

        def _schedule_for(self, extraction_point: ExtractionPoint, *,
                          post_result: bool = True, # @UnusedVariable
                          ) -> Delayed[Drop]:
            """
            The implementation of :func:`schedule_for`. Calls
            :func:`~ExtractionPoint.transfer_in` on ``extraction_point``.

            :meta public:
            Args:
                extraction_point: the :class:`ExtractionPoint` object to schedule the operation for
            Keyword Args:
                post_result: whether to post the resulting value to the returned future object
            Returns:
                a :class:`Delayed`\[:class:`.Drop`] future object to which the resulting
                value will be posted unless ``post_result`` is ``False``
            """
            from mpam.drop import Drop # @Reimport
            volume = extraction_point.board.drop_size if self.volume is None else self.volume
            future = Postable[Drop]()
            extraction_point.transfer_in(self.reagent, volume,
                                         mix_result = self.mix_result,
                                         on_insufficient = self.on_insufficient,
                                         on_no_source = self.on_no_source
                                         ).post_to(future)
            return future

    class TransferOut(CSOperation['ExtractionPoint', 'Liquid']):
        """
        A :class:`~.Operation` to remove :class:`.Liquid` via an :class:`ExtractionPoint`.

        Implemented by wrapping :func:`ExtractionPoint.transfer_out`.
        """
        volume: Final[Optional[Volume]]
        """
        The :class:`.Volume` to remove or ``None`` to indicate using the volume
        of the :class:`.Blob` at the :class:`ExtractionPoint`'s :attr:`pad`
        (which must exist).
        """
        is_product: Final[bool]
        """
        ``True`` if this transfer represents the extraction of a
        product
        """
        on_no_sink: Final[ErrorHandler]
        """
        An :class:`.ErrorHandler` invoked when there is no place to store
        the extracted :class:`.Liquid`.
        """
        product_loc: Final[Optional[Postable[ProductLocation]]]
        """
        An optional :class:`.Postable` future to which the resulting
        :class:`ProductLocation` will be posted if :attr:`is_product` is
        ``True``.
        """

        def __init__(self, volume: Optional[Volume] = None, *,
                     is_product: bool = True,
                     on_no_sink: ErrorHandler = PRINT,
                     product_loc: Optional[Postable[ProductLocation]] = None
                     ) -> None:
            """
            Initialize the object

            Args:
                volume: the :class:`.Volume` to remove or ``None`` to indicate using the volume
                        of the :class:`.Blob` at the :class:`ExtractionPoint`'s
                        :attr:`pad` (which must exist).
            Keyword Args:
                is_product: ``True`` if this transfer represents the extraction of a
                            product
                on_no_sink: an :class:`.ErrorHandler` invoked when there is no place to store
                            the extracted :class:`.Liquid`.

                product_loc: an optional :class:`.Postable` future to which the resulting
                            :class:`ProductLocation` will be posted if
                            :attr:`is_product` is ``True``.

            """
            self.volume = volume
            self.is_product = is_product
            self.on_no_sink = on_no_sink
            self.product_loc = product_loc

        def _schedule_for(self, extraction_point: ExtractionPoint, *,
                          post_result: bool = True, # @UnusedVariable
                          ) -> Delayed[Liquid]:
            """
            The implementation of :func:`schedule_for`. Calls
            :func:`~ExtractionPoint.transfer_out` on ``extraction_point``.

            :meta public:
            Args:
                extraction_point: the :class:`ExtractionPoint` object to schedule the operation for
            Keyword Args:
                post_result: whether to post the resulting value to the returned future object
            Returns:
                a :class:`Delayed`\[:class:`.Luiquid`] future object to which the resulting
                value will be posted unless ``post_result`` is ``False``
            """
            future = Postable[Liquid]()
            def finish(liquid: Liquid) -> None:
                future.post(liquid)
            extraction_point.transfer_out(volume = self.volume,
                                          is_product = self.is_product,
                                          on_no_sink = self.on_no_sink,
                                          product_loc = self.product_loc
                                         ).post_to(future)
            return future


class SystemComponent(ABC):
    """
    A component of a :class:`System`.  Primary examples are :class:`Board` and
    :class:`.Pipettor`.

    When a :class:`SystemComponent` is created, it is not associated with a
    :class:`System`, and an attempt to read :attr:`system` will fail.
    :attr:`joined_system` can be used to determine this state.  :attr:`system`
    is set when :func:`join_system` is called.

    Note:
        :func:`join_system` will be called for a :class:`Board` during the
        initialization of the :class:`System`.  For other
        :class:`SystemComponent`\s, it must be called explicitly.  If a class
        overrides :func:`join_system`, it should delegate to the base
        implementation.

    The primary job of a :class:`SystemComponent` qua :class:`SystemComponent`
    is to delegate requests to its :attr:`system`, which itself will delegate
    them to its associated :class:`.Engine`.

    :attr:`.TimerFunc`\s (no-argument functions that optionally return a
    :class:`.Time` or :class:`.Timestamp`) are scheduled using :func:`call_at`
    or :func:`call_after`.  If they return a value (other than ``None``), they
    are scheduled to be called again based on the value.

    :attr:`.ClockCallback`\s (no-argument functions that optionally return a
    :class:`.Ticks`) are scheduled using :func:`before_tick` or
    :func:`after_tick`.  These schedule the function to be executed immediately
    before or immediately after the communication functions on a tick.  They
    take an optional ``after`` argument, which is either :class:`.Ticks` or
    :class:`.Time` to specify a delay.  If it is not specified, the function is
    called on the next tick.  If the :attr:`.ClockCallback` returns a
    :class:`.Ticks` value, it is scheduled to re-run before or after
    (respectively) that many :class:`.Ticks`.

    To schedule running again on the next tick, return ``1*tick``.  A common
    idiom is to use an :class:`.Iterable` that yields ``None`` when done and
    ``1*tick`` otherwise, e.g., ::

        def do_it() -> Iterator[Optional[Ticks]]:
            while not pad.reserve():
                yield 1*tick
            # do the actual work
            pad.unreserve()
            yield None

        iterator = do_it()
        board.before_tick(lambda: next(iterator))

    Every time the iterator fails to reserve the pad, it yields one tick (which
    is returned from the lambda) and will get another chance before the next
    tick, after whoever held the reservation may have released it.  This will
    repeat until the reservation succeeds, at which point the real work can be
    done.  When it is done, it unreserves the pad and yields ``None``,
    signalling that it is done.


    Note:
        :class:`SystemComponent` is an abstract base class.  Concrete instances
        must implement :func:`update_state`, although this implementation must
        either delegate back to :func:`SystemComponent.update_state` or call
        :func:`finish_update`.
    """
    _system: Optional[System] = None
    _after_update: Final[list[Callback]]
    # _monitor_callbacks: Final[list[Callback]]
    no_delay: DelayType = Time.ZERO

    @property
    def system(self) -> System:
        """
        The :class:`System` that the :class:`SystemComponent` has joined.

        Note:
            When a :class:`SystemComponent` is created, it is not associated
            with a :class:`System`, and an attempt to read :attr:`system` will
            fail. :attr:`joined_system` can be used to determine this state.
            :attr:`system` is set when :func:`join_system` is called.
        """
        return not_None(self._system, desc=lambda: f"{self} not in a system")

    @property
    def joined_system(self) -> bool:
        """
        ``True`` if :func:`join_system` has been called and :attr:`system` is
        valid.
        """
        return self._system is not None

    def __init__(self) -> None:
        """
        Initialize the object
        """
        self._after_update = []
        # self._monitor_callbacks = []

    def join_system(self, system: System) -> None:
        """
        Join ``system``.  After this call, :attr:`system` will be valid and
        :attr:`joined_system` will return ``True``.

        This calls :func:`component_joined` on ``system``.

        Note:
            :func:`join_system` will be called for a :class:`Board` during the
            initialization of the :class:`System`.  For other
            :class:`SystemComponent`\s, it must be called explicitly.  If a class
            overrides :func:`join_system`, it should delegate to the base
            implementation.

        Args:
            system: the :class:`System` to join
        """
        self._system = system
        system.component_joined(self)

    def system_shutdown(self) -> None:
        pass

    @abstractmethod
    def update_state(self) -> None:
        self.finish_update()

    # def add_monitor(self, cb: Callback) -> None:
    #     self._monitor_callbacks.append(cb)

    def finish_update(self) -> None:
        # This is assumed to only be called in the DevComm thread, so
        # no locking is necessary.
        for cb in self._after_update:
            cb()
        self._after_update.clear()
        # for cb in self._monitor_callbacks:
        #     cb()

    def make_request(self, cb: Callable[[], Optional[Callback]]) -> DevCommRequest:
        def req() -> tuple[SystemComponent]:
            new_cb = cb()
            if new_cb is not None:
                self._after_update.append(new_cb)
            return (self,)
        return req

    def communicate(self, cb: Callable[[], Optional[Callback]], delta: Time=Time.ZERO) -> None:
        req = self.make_request(cb)
        sys = self.system
        if delta > Time.ZERO:
            self.call_after(delta, lambda : sys.communicate(req))
        else:
            sys.communicate(req)

    def call_at(self, t: Timestamp, fn: TimerFunc, *, daemon: bool = False) -> None:
        """
        Call :class:`.TimerFunc` ``fn`` at :class:`.Timestamp` ``t``.  This will
        be delegated to :attr:`system`, possibly batched, and finally passed to
        :attr:`system`'s :class:`.Engine`.  At this point, if the time is at or
        after ``t``, it will be run, otherwise it will be scheduled to run.

        If ``fn`` returns a :class:`Time` or :class:`Timestamp` value, it will
        be rescheduled to run at the new time.

        If ``daemon`` is ``True``, the :class:`System` can be shut down even
        while ``fn`` is still scheduled to run (either the first time or
        subsequent times).  If it is ``False`` (the default), the
        :class:`System` is not considered to be idle while it is scheduled.

        Args:
            t: the :class:`.Timestamp` to run at
            fn: the :class:`.TimerFunc` to run
        Keyword Args
            daemon: ``True`` if ``fn`` should be considered to be a daemon
        """
        self.system.call_at(t, fn, daemon=daemon)

    def call_after(self, delta: Time, fn: TimerFunc, *, daemon: bool = False) -> None:
        """
        Call :class:`.TimerFunc` ``fn`` after a delay of ``delta``.  This will
        be delegated to :attr:`system`, possibly batched, and finally passed to
        :attr:`system`'s :class:`.Engine`.  At this point it will be
        treated as if it had been ::

            sys_cpt.call_at(time_now()+delta, fn, daemon=daemon)

        Note:

            :func:`.time_now` is not computed until all batching is finished.

        If ``fn`` returns a :class:`Time` or :class:`Timestamp` value, it will
        be rescheduled to run at the new time.

        If ``daemon`` is ``True``, the :class:`System` can be shut down even
        while ``fn`` is still scheduled to run (either the first time or
        subsequent times).  If it is ``False`` (the default), the
        :class:`System` is not considered to be idle while it is scheduled.

        Args:
            delta: the :class:`.Time` to delay before running
            fn: the :class:`.TimerFunc` to run
        Keyword Args:
            daemon: ``True`` if ``fn`` should be considered to be a daemon
        """
        self.system.call_after(delta, fn, daemon=daemon)

    def before_tick(self, fn: ClockCallback, *, delta: Optional[DelayType]=Ticks.ZERO) -> None:
        if delta is None:
            delta = Ticks.ZERO
        self.system.before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, *, delta: Optional[DelayType]=Ticks.ZERO) -> None:
        if delta is None:
            delta = Ticks.ZERO
        self.system.after_tick(fn, delta=delta)

    def on_tick(self, cb: Callable[[], Optional[Callback]], *, delta: Ticks = Ticks.ZERO) -> None:
        req = self.make_request(cb)
        self.system.on_tick(req, delta=delta)

    def delayed(self, function: Callable[[], T], *,
                after: WaitableType) -> Delayed[T]:
        return self.system.delayed(function, after=after)

    def schedule(self, cb: Callable[[], Optional[Callback]], *,
                 after: WaitableType = NO_WAIT) -> None:
        if after is NO_WAIT:
            after = self.no_delay
        if isinstance(after, Ticks):
            self.on_tick(cb, delta=after)
        elif isinstance(after, Time):
            self.communicate(cb, delta=after)
        elif isinstance(after, Trigger):
            after.on_trigger(cb)
        elif isinstance(after, Delayed):
            after.when_value(lambda _: cb())
        else:
            assert_never(after)

    def user_operation(self, *, desc: Optional[Any] = None) -> UserOperation:
        if desc is None:
            desc = self
        return UserOperation(self.system.engine.idle_barrier, desc=desc)

    def on_condition(self, pred: Callable[[], bool],
                     val_fn: Callable[[], T]) -> Delayed[T]:
        if pred():
            return Delayed.complete(val_fn())
        future = Postable[T]()
        one_tick = 1 * tick
        def keep_trying() -> Iterator[Optional[Ticks]]:
            while not pred():
                yield one_tick
            future.post(val_fn())
            yield None

        iterator = keep_trying()
        self.before_tick(lambda: next(iterator))
        return future

    # def schedule_before(self, cb: C):

class PowerMode(Enum):
    DC = auto()
    AC = auto()

class PowerSupply(BinaryComponent['PowerSupply']):
    _last_voltage: Voltage = Voltage.ZERO
    _lock: Final[RLock]

    min_voltage: Final[Voltage]
    max_voltage: Final[Voltage]
    allowed_mode: Final[Optional[PowerMode]]
    on_high_voltage: Final[ErrorHandler]
    on_low_voltage: Final[ErrorHandler]
    on_illegal_mode_change: Final[ErrorHandler]

    voltage: MonitoredProperty[Voltage] = MonitoredProperty()
    on_voltage_change: ChangeCallbackList[Voltage] = voltage.callback_list

    @voltage.transform
    def _check_voltage_bounds(self, v: Voltage) -> MissingOr[Voltage]:
        my_max = self.max_voltage
        if not self.on_high_voltage.expect_true(v <= my_max,
                                                lambda: f"Voltage {v} > maximum ({my_max})"):
            return self.max_voltage
        if not self.on_illegal_toggle.expect_true(v > 0 or self.can_toggle or self.current_state is OnOff.OFF,
                                                  lambda: "Power supply cannot be turned off"):
            return MISSING
        my_min = self.min_voltage

        if not self.on_low_voltage.expect_true(v >= my_min or v == 0,
                                                lambda: f"Voltage {v} < minimum ({my_min})"):
            return self.min_voltage
        return v

    mode: MonitoredProperty[PowerMode] = MonitoredProperty()
    on_mode_change: ChangeCallbackList[PowerMode] = mode.callback_list

    @mode.transform
    def _check_mode_change(self, m: PowerMode) -> MissingOr[PowerMode]:
        allowed = self.allowed_mode
        if not self.on_illegal_mode_change.expect_true(allowed is None or allowed is m,
                                                       lambda: "Power supply mode cannot be changed"):
            return MISSING
        return m

    def __init__(self, board: Board, *,
                 min_voltage: Voltage,
                 max_voltage: Voltage,
                 initial_voltage: Voltage,
                 mode: PowerMode,
                 can_toggle: bool = True,
                 can_change_mode: bool = True,
                 on_high_voltage: ErrorHandler = PRINT,
                 on_low_voltage: ErrorHandler = PRINT,
                 on_illegal_toggle: ErrorHandler = PRINT,
                 on_illegal_mode_change: ErrorHandler = PRINT,
                 ) -> None:
        initial_state = initial_voltage > 0
        super().__init__(board=board,
                         state=DummyState(initial_state=OnOff.from_bool(initial_state)),
                         can_toggle=can_toggle,
                         on_illegal_toggle=on_illegal_toggle)

        if not can_toggle:
            if initial_voltage == 0:
                min_voltage = 0*volts
                max_voltage = 0*volts

        self.min_voltage = min_voltage
        self.max_voltage = max_voltage

        self.allowed_mode = None if can_change_mode else mode
        self.on_high_voltage = on_high_voltage
        self.on_low_voltage = on_low_voltage
        self.on_illegal_mode_change = on_illegal_mode_change
        self._lock = RLock()

        self.mode = mode
        self.voltage = initial_voltage

        self.on_state_change(self._note_state_change)
        self.on_voltage_change(self._note_voltage_change)


    def _note_state_change(self, _old: OnOff, new: OnOff) -> None:
        with self._lock:
            if new is OnOff.OFF:
                self.voltage = Voltage.ZERO
            else:
                self.voltage = self._last_voltage

    def _note_voltage_change(self, _old: Voltage, new: Voltage) -> None:
        with self._lock:
            if new > 0:
                self._last_voltage = new
            self.current_state = OnOff.from_bool(new > 0)


    # # MyPy doesn't know what to do with this, but I believe it should work, and
    # # it appears to in practice.
    # @BinaryComponent.current_state.setter   # type: ignore[attr-defined]
    # def current_state(self, val: OnOff) -> None:
    #     allowed = self.allowed_state
    #     if allowed is None or allowed is val:
    #         BinaryComponent.current_state.fset(self, val) # type: ignore[attr-defined]
    #     elif val is OnOff.ON:
    #         self.on_illegal_toggle("Power supply cannot be turned on")
    #     else:
    #         self.on_illegal_toggle("Power supply cannot be turned off")

    def high_clip(self, v: Voltage) -> MissingOr[Voltage]: # @UnusedVariable
        return self.max_voltage

    def low_clip(self, v: Voltage) -> MissingOr[Voltage]: # @UnusedVariable
        return 0*volts

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.voltage} {self.mode.name}, {self.current_state.name})"

class FixedPowerSupply(PowerSupply):
    voltage_level: Final[Voltage]
    expected_state: Final[OnOff]
    is_toggleable: Final[bool]

    voltage: MonitoredProperty[Voltage] = MonitoredProperty(default=Voltage.ZERO)
    on_voltage_change: ChangeCallbackList[Voltage] = voltage.callback_list

    @voltage.transform
    def no_voltage_changes(self, v: Voltage) -> MissingOr[Voltage]:
        if v == self.voltage_level:
            return v
        if self.is_toggleable and v == 0:
            return v
        print("Power supply voltage level cannot be changed")
        return MISSING

    def __init__(self, board: Board, *,
                 voltage_level: Voltage = 0*volts,
                 is_toggleable: bool = False,
                 changeable_mode: bool = False,
                 mode: PowerMode = PowerMode.DC) -> None:
        self.is_toggleable = is_toggleable
        self.voltage_level = voltage_level
        self.expected_state = OnOff.from_bool(voltage_level > 0)

        super().__init__(board,
                         min_voltage=0*volts,
                         max_voltage=voltage_level,
                         initial_voltage=voltage_level,
                         can_change_mode=changeable_mode,
                         mode=mode)

        # def no_voltage_changes(ps: PowerSupply, v: Voltage) -> MissingOr[Voltage]:
        #     if not isinstance(ps, FixedPowerSupply):
        #         return v
        #     if v == self.voltage_level:
        #         return v
        #     if is_toggleable and v == 0:
        #         return v
        #     print("Power supply voltage level cannot be changed")
        #     return MISSING
        # PowerSupply.voltage.transform(no_voltage_changes)



    # MyPy doesn't know what to do with this, but I believe it should work, and
    # it appears to in practice.
    @BinaryComponent.current_state.setter   # type: ignore[attr-defined]
    def current_state(self, val: OnOff) -> None:
        if self.is_toggleable or val is self.expected_state:
            BinaryComponent.current_state.fset(self, val) # type: ignore[attr-defined]
        else:
            print("Power supply cannot be turned on or off")


class Fan(BinaryComponent["Fan"]):
    # There's nothing special about fans, but we make it a separate type for
    # type checking and value printing purposes.
    ...

class ChangeJournal:
    turned_on: Final[set[DropLoc]]
    turned_off: Final[set[DropLoc]]
    delivered: Final[dict[DropLoc, list[Liquid]]]
    removed: Final[dict[DropLoc, Volume]]
    mix_result: Final[dict[DropLoc, MixResult]]

    @property
    def has_transfer(self) -> bool:
        return bool(self.delivered) or bool(self.removed)

    def __init__(self) -> None:
        self.turned_on = set()
        self.turned_off = set()
        self.delivered = defaultdict(list)
        self.removed = defaultdict(lambda: Volume.ZERO)
        self.mix_result = {}

    def change_to(self, pad: DropLoc, new_state: OnOff) -> None:
        wrong,right = (self.turned_off,self.turned_on) if new_state else (self.turned_on, self.turned_off)
        if pad in wrong:
            wrong.remove(pad)
        else:
            right.add(pad)

    def note_removal(self, pad: DropLoc, volume: Volume) -> None:
        self.removed[pad] += volume

    def note_delivery(self, pad: DropLoc, liquid: Liquid, *, mix_result: Optional[MixResult] = None) -> None:
        self.delivered[pad].append(liquid)
        if mix_result:
            self.mix_result[pad] = mix_result

    def process_changes(self) -> None:
        from mpam.drop import Blob # @Reimport
        Blob.process_changes(self)


TempOrTP = Union[TemperaturePoint, Temperature]

AmbientThreshold = Union[TempOrTP, tuple[TempOrTP, TempOrTP]]
"""
Either a :class:`.TemperaturePoint`, a :class:`.Temperature` offset, or a pair
of such values (as lower and upper values, respectively).
"""

class Board(SystemComponent):
    pads: Final[PadArray]
    
    _well_list: Final[list[Well]]
    @property
    def wells(self) -> Sequence[Well]:
        return self._well_list
    _magnet_list: Final[list[Magnet]]

    @property
    def magnets(self) -> Sequence[Magnet]:
        return self._magnet_list

    heaters: Final[list[Heater]]
    chillers: Final[list[Chiller]]
    @property
    def temperature_controls(self) -> Sequence[TemperatureControl]:
        return (*self.heaters, *self.chillers)
    
    _extraction_points: Final[list[ExtractionPoint]]
    @property
    def extraction_points(self) -> Sequence[ExtractionPoint]:
        return self._extraction_points
    extraction_point_splash_radius: Final[int]
    power_supply: Final[PowerSupply]
    fan: Final[Optional[Fan]]
    orientation: Final[Orientation]
    drop_motion_time: Final[Time]
    off_on_delay: Time
    _drop_size: Volume
    _reserved_well_gates: list[Well]
    _lock: Final[Lock]
    _drop_unit: Unit[Volume]
    # _drops: Final[list[Drop]]
    # _to_appear: Final[list[tuple[Pad, Liquid]]]
    _change_journal: ChangeJournal
    trace_blobs: ClassVar[bool] = False
    no_delay: DelayType = Ticks.ZERO
    component_layout: Final[Optional[RCOrder]]

    ambient_temperature: TemperaturePoint = 75*abs_F

    ambient_threshold: AmbientThreshold = 5*deg_F
    """
    The value used by :func:`is_ambient` to compute the threshold (based on
    :attr:`ambient_temperature`) to be used by :func:`is_ambient`. If it is a
    :class:`.TemperaturePoint`, it is used directly as the threshold.  If it is
    a :class:`.Temperature`, it is added to the ambient temperature.  If it is a
    tuple, the two values are taken to be the lower and upper bounds,
    respectively, with a lower :class:`.Temperature` subtracted from
    :attr:`ambient_temperature`.
    """


    @property
    def change_journal(self) -> ChangeJournal:
        with self._lock:
            return self._change_journal

    def __init__(self, *,
                 pads: PadArray,
                 wells: Optional[Sequence[Well]] = None,
                 magnets: Optional[Sequence[Magnet]] = None,
                 heaters: Optional[Sequence[Heater]] = None,
                 chillers: Optional[Sequence[Chiller]] = None,
                 extraction_points: Optional[Sequence[ExtractionPoint]] = None,
                 extraction_point_splash_radius: int = 0,
                 power_supply: Optional[PowerSupply] = None,
                 fan: Optional[Fan] = None,
                 orientation: Orientation,
                 drop_motion_time: Time,
                 off_on_delay: Time = Time.ZERO,
                 cpt_layout: Optional[RCOrder] = None) -> None:
        super().__init__()
        self._change_journal = ChangeJournal()
        self.pads = pads
        self.component_layout = cpt_layout
        self._well_list = []
        if wells:
            self._add_wells(wells)
        self.heaters = []
        if heaters:
            self._add_heaters(heaters)
        self.chillers = []
        if chillers:
            self._add_chillers(chillers)
        self._magnet_list = [] 
        if magnets:
            self._add_magnets(magnets)
        self._extraction_points = [] 
        if extraction_points:
            self._add_extraction_points(extraction_points)
        self.extraction_point_splash_radius = extraction_point_splash_radius
        self.power_supply = power_supply or FixedPowerSupply(self)
        self.fan = fan
        self.orientation = orientation
        self.drop_motion_time = drop_motion_time
        self.off_on_delay = off_on_delay
        if off_on_delay != 0:
            logger.info("off-on delay is %s", off_on_delay)
        self._lock = Lock()
        self._reserved_well_gates = []
        # self._drops = []
        # self._to_appear = []
        
    def _add_well(self, well: Well) -> int:
        wells = self._well_list
        n = len(wells)
        well.number = n+1
        wells.append(well)
        return n
        
    def _add_wells(self, wells: Sequence[Well], *, order: Optional[RCOrder] = None) -> None:
        if order is None:
            order = self.component_layout
        wells = self.sorted(wells, get_pads = lambda w: (w.exit_pad,), order=order)
        for w in wells:
            self._add_well(w)
            
    def _add_heater(self, heater: Heater) -> int:
        heaters = self.heaters
        n = len(heaters)
        heater.number = n+1
        heaters.append(heater)
        return n
        
    def _add_heaters(self, heaters: Sequence[Heater], *, order: Optional[RCOrder] = None) -> None:
        if order is None:
            order = self.component_layout
        heaters = self.sorted(heaters, get_pads=lambda h: h.pads_for_sort, order=order)
        for h in heaters:
            self._add_heater(h)

    def _add_chiller(self, chiller: Chiller) -> int:
        chillers = self.chillers
        n = len(chillers)
        chiller.number = n+1
        chillers.append(chiller)
        return n

    def _add_chillers(self, chillers: Sequence[Chiller], *, order: Optional[RCOrder] = None) -> None:
        if order is None:
            order = self.component_layout
        chillers = self.sorted(chillers, get_pads=lambda c: c.pads_for_sort, order=order)
        for c in chillers:
            self._add_chiller(c)
            
    def _add_extraction_point(self, ep: ExtractionPoint) -> int:
        eps = self._extraction_points
        n = len(eps)
        ep.number = n+1
        eps.append(ep)
        return n

    def _add_extraction_points(self, eps: Sequence[ExtractionPoint], *, order: Optional[RCOrder] = None) -> None:
        if order is None:
            order = self.component_layout
        eps = self.sorted(eps, get_pads=lambda ep: (ep.pad,), order=order)
        for ep in eps:
            self._add_extraction_point(ep)
            
    

    # def _add_temperature_control(self, temperature_control: Union[Heater,Chiller]) -> int:
    #     if isinstance(temperature_control, Heater):
    #         return self._add_heater(temperature_control)
    #     elif isinstance(temperature_control, Chiller):
    #         return self._add_chiller(temperature_control)
    #     else:
    #         assert_never(temperature_control)
    #
    # def _add_temperature_controls(self, temperature_controls: Sequence[Union[Heater,Chiller]], *, order: Optional[RCOrder] = None) -> None:
    #     if order is None:
    #         order = self.component_layout
    #     temperature_controls = self.sorted(temperature_controls, get_pads=TemperatureControl.pads_for_sort, order=order)
    #     for tc in temperature_controls:
    #         self._add_temperature_control(tc)

    def _add_magnet(self, magnet: Magnet) -> int:
        magnets = self._magnet_list
        n = len(magnets)
        magnet.number = n+1
        magnets.append(magnet)
        return n
        
    def _add_magnets(self, magnets: Sequence[Magnet], *, order: Optional[RCOrder] = None) -> None:
        if order is None:
            order = self.component_layout
        magnets = self.sorted(magnets, get_pads = lambda m: m.pads, order=order)
        for m in magnets:
            self._add_magnet(m)

    def replace_change_journal(self) -> ChangeJournal:
        with self._lock:
            old = self._change_journal
            self._change_journal = ChangeJournal()
            return old

    def stop(self) -> None:
        pass
    def abort(self) -> None:
        pass

    @property
    def pad_array(self) -> PadArray:
        return self.pads

    def pad_at(self, x: int, y: int) -> Pad:
        return self.pads[XYCoord(x,y)]

    @cached_property
    def max_row(self) -> int:
        return max(coord.y for coord in self.pads)

    @cached_property
    def min_row(self) -> int:
        return min(coord.y for coord in self.pads)

    @cached_property
    def max_column(self) -> int:
        return max(coord.x for coord in self.pads)

    @cached_property
    def min_column(self) -> int:
        return min(coord.x for coord in self.pads)
    
    def edge(self, side: Dir) -> int:
        orientation = self.orientation
        if side is Dir.NORTH or side is Dir.SOUTH:
            return self.max_row if orientation.pos_y is side else self.min_row
        elif side is Dir.EAST or side is Dir.WEST:
            return self.max_column if orientation.pos_x is side else self.min_column
        assert False, f"Board.edge() requires a cardinal direction, got {side}."
    
    def well_number(self, n: int) -> Well:
        return self.wells[n-1]
    
    def heater_number(self, n: int) -> Heater:
        return self.heaters[n-1]
    
    def chiller_number(self, n: int) -> Chiller:
        return self.chillers[n-1]
    
    def extraction_point_number(self, n: int) -> ExtractionPoint:
        return self.extraction_points[n-1]
    
    def magnet_number(self, n: int) -> Magnet:
        return self.magnets[n-1]

    # @property
    # def well_groups(self) -> Mapping[str, WellGroup]:
    #     cache: Optional[Mapping[str, WellGroup]] = getattr(self, '_well_groups', None)
    #     if cache is None:
    #         cache = {well.group.name: well.group for well in self.wells}
    #         self._well_groups = cache
    #     return cache

    @property
    def drop_size(self) -> Volume:
        cache: Optional[Volume] = getattr(self, '_drop_size', None)
        if cache is None:
            cache = self.wells[0].dispensed_volume
            assert all(w.dispensed_volume==cache for w in self.wells), "Not all wells dispense the same volume"
            self._drop_size = cache
        return cache

    @property
    def drop_unit(self) -> Unit[Volume]:
        cache: Optional[Unit[Volume]] = getattr(self, '_drop_unit', None)
        if cache is None:
            cache = self.drop_size.as_unit("drops", singular="drop")
            self._drop_unit = cache
        return cache

    def finish_update(self) -> None:
        self.infer_drop_motion()
        super().finish_update()

    def join_system(self, system: System)->None:
        super().join_system(system)
        for h in self.temperature_controls:
            h.start_polling()

    def _amb_threshold(self, t: TempOrTP, upper: bool) -> TemperaturePoint:
        if isinstance(t, TemperaturePoint):
            return t
        elif upper:
            return self.ambient_temperature+t
        else:
            return self.ambient_temperature-t


    def is_ambient(self, temp: TemperaturePoint) -> bool:
        at = self.ambient_threshold
        if isinstance(at, tuple):
            low = self._amb_threshold(at[0], False)
            high = self._amb_threshold(at[1], True)
            return temp <= high and temp >= low
        else:
            high = self._amb_threshold(at, True)
            return temp <= high

    def print_blobs(self, *, force: bool = False) -> None:
        if not force and not self.trace_blobs:
            return
        from mpam.drop import Blob # @Reimport
        print("--------------")
        print("Blobs on board")
        print("--------------")
        blobs = set[Blob]()

        def check_pads(pads: Iterable[DropLoc]) -> None:
            nonlocal blobs
            for pad in pads:
                if pad is not None and pad.blob is not None:
                    if not pad in pad.blob.pads:
                        print(f"{pad} not in {pad.blob}")
                    blobs.add(pad.blob)

        check_pads(self.pads.values())
        for well in self.wells:
            check_pads(well.shared_pads)
            check_pads((well.gate,))

        for blob in blobs:
            print(blob)

    def infer_drop_motion(self) -> None:
        self.replace_change_journal().process_changes()
        self.print_blobs()

    def journal_state_change(self, pad: DropLoc, new_state: OnOff) -> None:
        self.change_journal.change_to(pad, new_state)

    def journal_removal(self, pad: DropLoc, volume: Volume) -> None:
        self.change_journal.note_removal(pad, volume)

    def journal_delivery(self, pad: DropLoc, liquid: Liquid, *,
                         mix_result: Optional[MixResult] = None) -> None:
        self.change_journal.note_delivery(pad, liquid, mix_result=mix_result)

    def _reset(self, *cpts: BinaryComponent) -> None:
        for c in cpts:
            c.current_state = OnOff.OFF

    def reset_pads(self) -> None:
        self._reset(*self.pad_array.values())
        for well in self.wells:
            self._reset(well.gate, *well.shared_pads)

    def reset_temperature_controls(self) -> None:
        self._reset(*self.temperature_controls)

    def reset_heaters(self) -> None:
        self._reset(*self.heaters)

    def reset_chillers(self) -> None:
        self._reset(*self.chillers)

    def reset_magnets(self) -> None:
        self._reset(*self.magnets)

    def reset_all(self) -> None:
        self.reset_pads()
        self.reset_temperature_controls()
        self.reset_magnets()
        self._reset(self.power_supply)
        if self.fan is not None:
            self._reset(self.fan)

    def sorted(self, cpts: Sequence[T], *,
               get_pads: Callable[[T], Sequence[LocatedPad]],
               order: Optional[RCOrder]) -> Sequence[T]:
        if order is None: return cpts
        def get_loc(p: LocatedPad) -> XYCoord:
            return p.location
        key = order.key_for(self.orientation, loc=get_loc)
        min_pad = { c: min(get_pads(c), key=key) for c in cpts }
        return sorted(cpts, key=lambda c: key(min_pad[c]))

class UserOperation(Worker):
    def __init__(self, idle_barrier: IdleBarrier, desc: Optional[Any] = None) -> None:
        super().__init__(idle_barrier, desc=desc)

    def __enter__(self) -> UserOperation:
        self.not_idle()
        return self

    def __exit__(self,
                 exc_type: Optional[type[BaseException]],  # @UnusedVariable
                 exc_val: Optional[BaseException],  # @UnusedVariable
                 exc_tb: Optional[TracebackType]) -> Literal[False]:  # @UnusedVariable
        self.idle()
        return False

    def start(self) -> None:
        self.__enter__()

    def end(self) -> None:
        self.__exit__(None, None, None)

class Clock:
    system: Final[System]
    engine: Final[Engine]
    clock_thread: Final[ClockThread]

    on_interval_change: Final[ChangeCallbackList[Time]]
    on_state_change: Final[ChangeCallbackList[bool]]

    def __init__(self, system: System) -> None:
        self.system = system
        self.engine = system.engine
        self.clock_thread = system.engine.clock_thread
        self.on_interval_change = ChangeCallbackList[Time]()
        self.on_state_change = ChangeCallbackList[bool]()

    @property
    def update_interval(self) -> Time:
        return self.clock_thread.update_interval

    @update_interval.setter
    def update_interval(self, interval: Time) -> None:
        old = self.clock_thread.update_interval
        if old != interval:
            self.clock_thread.update_interval = interval
            self.on_interval_change.process(old, interval)

    @property
    def update_rate(self) -> Frequency:
        return 1/self.update_interval

    @update_rate.setter
    def update_rate(self, rate: Frequency) -> None:
        self.update_interval = 1/rate

    @property
    def next_tick(self) -> TickNumber:
        return self.clock_thread.next_tick

    @property
    def last_tick(self) -> TickNumber:
        return self.next_tick-1*tick

    @property
    def running(self) -> bool:
        return self.clock_thread.running

    def before_tick(self, fn: ClockCallback, tick: Optional[TickNumber] = None, delta: Optional[Ticks] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.before_tick() called with both tick and delta specified"
            delta = max(Ticks.ZERO, tick-self.next_tick)
        elif delta is None:
            delta = Ticks.ZERO
        self.system.before_tick(fn, delta=delta)

    def after_tick(self, fn: ClockCallback, tick: Optional[TickNumber] = None, delta: Optional[Ticks] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.after_tick() called with both tick and delta specified"
            delta = max(Ticks.ZERO, tick-self.next_tick)
        elif delta is None:
            delta = Ticks.ZERO
        self.system.after_tick(fn, delta=delta)

    # Calling await_tick() when the clock isn't running only works if there is another thread that
    # will advance it.
    def await_tick(self, tick: Optional[TickNumber] = None, delta: Optional[Ticks] = None) -> None:
        if tick is not None:
            assert delta is None, "Clock.await_tick() called with both tick and delta specified"
            delta = tick-self.next_tick
        elif delta is None:
            delta = Ticks.ZERO
        if delta >= 0:
            e = Event()
            def cb() -> None:
                e.set()
            self.clock_thread.after_tick([(delta, cb)])
            while not e.is_set():
                e.wait(_wait_timeout)

    def advance(self, min_delay: Optional[Time] = None) -> None:
        assert not self.running, "Clock.advance_clock() called while clock is running"
        ct = self.clock_thread
        if min_delay is not None:
            next_allowed = ct.last_tick_time+min_delay
            if next_allowed > time_now():
                def do_advance() -> None:
                    ct.wake_up()
                self.system.engine.call_at([(next_allowed, do_advance, False)])
                return
        ct.wake_up()

    def start(self, interval: Optional[Union[Time,Frequency]] = None) -> None:
        assert not self.running, "Clock.start() called while clock is running"
        if isinstance(interval, Frequency):
            interval = (1/interval).a(Time)
        if interval is not None:
            self.update_interval = interval
        self.on_state_change.process(False, True)
        self.clock_thread.start_clock(interval)

    def pause(self) -> None:
        assert self.running, "Clock.pause() called while clock is not running"
        self.on_state_change.process(True, False)
        self.clock_thread.pause_clock()

class Batch:
    system: Final[System]
    nested: Final[Optional[Batch]]

    buffer_communicate: list[DevCommRequest]
    buffer_call_at: list[TimerRequest]
    buffer_call_after: list[TimerDeltaRequest]
    buffer_before_tick: list[ClockRequest]
    buffer_after_tick: list[ClockRequest]
    buffer_on_tick: list[ClockCommRequest]

    def __init__(self, system: System, *, nested: Optional[Batch]) -> None:
        self.system = system
        self.nested = nested
        self.buffer_communicate = []
        self.buffer_call_at = []
        self.buffer_call_after = []
        self.buffer_before_tick = []
        self.buffer_after_tick = []
        self.buffer_on_tick = []

    def communicate(self, reqs: Sequence[DevCommRequest]) -> None:
        self.buffer_communicate.extend(reqs)

    def call_at(self, reqs: Sequence[TimerRequest]) -> None:
        self.buffer_call_at.extend(reqs)

    def call_after(self, reqs: Sequence[TimerDeltaRequest]) -> None:
        self.buffer_call_after.extend(reqs)

    def before_tick(self, reqs: Sequence[ClockRequest]) -> None:
        self.buffer_before_tick.extend(reqs)

    def after_tick(self, reqs: Sequence[ClockRequest]) -> None:
        self.buffer_after_tick.extend(reqs)

    def on_tick(self, reqs: Sequence[ClockCommRequest]) -> None:
        self.buffer_on_tick.extend(reqs)

    def __enter__(self) -> Batch:
        return self

    # I'm currently assuming that if we get an exception,
    # we don't want to try to do the communication.  Instead
    # we just return, clearing ourselves from the system
    # if we're not nested
    def __exit__(self,
                 exc_type: Optional[type[BaseException]],
                 exc_val: Optional[BaseException],  # @UnusedVariable
                 exc_tb: Optional[TracebackType]) -> Literal[False]:  # @UnusedVariable
        if exc_type is None:
            sink: Union[Batch,Engine] = self.nested or self.system.engine
            sink.communicate(self.buffer_communicate)
            sink.call_at(self.buffer_call_at)
            sink.call_after(self.buffer_call_after)
            sink.before_tick(self.buffer_before_tick)
            sink.after_tick(self.buffer_after_tick)
            sink.on_tick(self.buffer_on_tick)
            with self.system._batch_lock:
                self.system._batch = self.nested
        return False

class System:
    board: Board
    engine: Engine
    clock: Clock
    _batch_lock: Final[Lock]
    _batch: Optional[Batch]
    monitor: Optional[BoardMonitor] = None
    _cpts_lock: Final[Lock]
    components: Final[list[SystemComponent]]
    running: bool = True
    _local_ip_addr: MissingOr[Optional[str]] = MISSING
    _requested_ip: Optional[str]
    _subnet: Optional[str]
    _subnet_mask: Optional[str]
    terminal_interaction: Final[AsyncFunctionSerializer]
    
    
    @property
    def local_ip_addr(self) -> Optional[str]:
        ip = self._local_ip_addr
        if ip is MISSING:
            ip = local_ipv4_addr(addr = self._requested_ip,
                                 subnet = self._subnet,
                                 subnet_mask = self._subnet_mask)
            self._local_ip_addr = ip
        return ip
    

    def __init__(self, *, board: Board,
                 local_ip: Optional[str] = None,
                 subnet: Optional[str] = None,
                 subnet_mask: Optional[str] = None
                 ):
        self.board = board
        self.engine = Engine(default_clock_interval=board.drop_motion_time)
        self.clock = Clock(self)
        self._batch = None
        self._batch_lock = Lock()
        self._cpts_lock = Lock()
        self.components = []
        self._requested_ip = local_ip
        self._subnet = subnet
        self._subnet_mask = subnet_mask
        self.terminal_interaction = AsyncFunctionSerializer(thread_name="Terminal interaction thread")
        
        board.join_system(self)

    def __enter__(self) -> System:
        self.engine.__enter__()
        return self

    def __exit__(self,
                 exc_type: Optional[type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> Literal[False]:
        return self.engine.__exit__(exc_type, exc_val, exc_tb)

    def component_joined(self, component: SystemComponent) -> None:
        with self._cpts_lock:
            assert self.running, f"Tried to add {component} to system after shutdown"
            self.components.append(component)

    def shutdown(self) -> None:
        with self._cpts_lock:
            for cpt in self.components:
                cpt.system_shutdown()

    def stop(self) -> None:
        self.engine.stop()
        self.board.stop()

    def abort(self) -> None:
        self.engine.abort()
        self.board.abort()

    def _channel(self) -> Union[Batch, Engine]:
        with self._batch_lock:
            return self._batch or self.engine
    def communicate(self, req: DevCommRequest) -> None:
        self._channel().communicate([req])

    def call_at(self, t: Timestamp, fn: TimerFunc, *, daemon: bool = False) -> None:
        self._channel().call_at([(t, fn, daemon)])

    def call_after(self, delta: Time, fn: TimerFunc, *, daemon: bool = False) -> None:
        self._channel().call_after([(delta, fn, daemon)])

    def before_tick(self, fn: ClockCallback, *, delta: DelayType=Ticks.ZERO) -> None:
        if isinstance(delta, Ticks):
            self._channel().before_tick([(delta, fn)])
        else:
            self.call_after(delta, lambda: self.before_tick(fn))

    def after_tick(self, fn: ClockCallback, *, delta: DelayType=Ticks.ZERO) -> None:
        if isinstance(delta, Ticks):
            self._channel().after_tick([(delta, fn)])
        else:
            self.call_after(delta, lambda: self.after_tick(fn))

    def on_tick(self, req: DevCommRequest, *, delta: DelayType=Ticks.ZERO) -> None:
        if isinstance(delta, Ticks):
            self._channel().on_tick([(delta, req)])
        else:
            self.call_after(delta, lambda: self.on_tick(req))

    def delayed(self, function: Callable[[], T], *,
                after: WaitableType) -> Delayed[T]:
        if after is NO_WAIT:
            return Delayed.complete(function())
        future = Postable[T]()
        def run_then_post() -> None:
            future.post(function())
        if isinstance(after, Time):
            if after > Time.ZERO:
                self.call_after(after, run_then_post)
            else:
                return Delayed.complete(function())
        elif isinstance(after, Ticks):
            if after > Ticks.ZERO:
                self.before_tick(run_then_post, delta = after)
            else:
                return Delayed.complete(function())
        elif isinstance(after, Trigger):
            after.on_trigger(run_then_post)
        elif isinstance(after, Delayed):
            after.when_value(lambda _: run_then_post())
        else:
            assert_never(after)
        return future

    def batched(self) -> Batch:
        with self._batch_lock:
            self._batch = Batch(self, nested=self._batch)
            return self._batch


    def run_monitored(self, fn: Callable[[System],T],
                      *,
                      min_time: Time = 0*sec,
                      max_time: Optional[Time] = None,
                      update_interval: Time = 20*ms,
                      control_setup: Optional[Callable[[BoardMonitor, SubplotSpec], Any]] = None,
                      control_fraction: Optional[float] = None,
                      macro_file_names: Optional[list[str]] = None,
                      thread_name: Optional[str] = None,
                      cmd_line_args: Optional[Namespace] = None,
                      config_params: Optional[Mapping[str, Any]] = None,
                      ) -> T:
        from mpam.monitor import BoardMonitor  # @Reimport
        val: T

        done = Event()
        def run_it() -> None:
            nonlocal val
            with self:
                val = fn(self)  # @UnusedVariable
            done.set()
            self.shutdown()

        if thread_name is None:
            thread_name = f"Monitored task @ {time_now()}"
        thread = Thread(target=run_it, name=thread_name)
        if cmd_line_args is None:
            cmd_line_args = Namespace()
        monitor = BoardMonitor(self.board,
                               control_setup=control_setup,
                               control_fraction=control_fraction,
                               macro_file_names=macro_file_names,
                               cmd_line_args=cmd_line_args,
                               from_code=config_params
                               )
        self.monitor = monitor
        # print(f"System's monitor is {monitor}")
        thread.start()
        monitor.keep_alive(sentinel = lambda : done.is_set(),
                           min_time = min_time,
                           max_time = max_time,
                           update_interval = update_interval)

        return val
    
    def prompt_and_wait(self, future: Postable[None], *, prompt: Optional[str] = None) -> None:
        def doit() -> None:
            if prompt is not None:
                print(prompt)
            print("Hit <RETURN> to continue.")
            input()
            future.post(None)
        self.terminal_interaction.enqueue(doit)
    
