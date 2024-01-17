from __future__ import annotations

import random
from threading import RLock
from typing import TypeVar, Generic, Final, Optional, Callable, \
    Hashable, overload, Any, Union

from .basic import MissingOr, MISSING, Gettable


_T = TypeVar("_T")
_V = TypeVar("_V")
_Tco = TypeVar("_Tco", covariant=True)

    
ChangeCallback = Callable[[_T,_T],None]
"""
A function that takes two parameters of type :attr:`_T` representing the old and
new values of some attribute.
"""

class ChangeCallbackList(Generic[_T]):
    """
    A hook onto which value-change handlers may be added.  When the list is
    processed (via :func:`process`), each handler is passed the old and new
    values (which may be the same).

    Handlers may optionally be associated with a key (of any :class:`Hashable`
    type).  If a handler is added with a key that already exists in the
    :class:`ChangeCallbackList`, the old value is replaced.  If no key is specified,
    the handler itself is used as the key and no replacement will take place.

    Args:
        _T: the type of the value being managed
    """
    callbacks: Optional[dict[Hashable, ChangeCallback[_T]]] = None    #: A mapping from keys to handlers
    lock: Final[RLock]                              #: The object's lock

    def __init__(self) -> None:
        """
        Initialize the object.
        """
        self.lock = RLock()

    def add(self, cb: ChangeCallback[_T], *, key: Optional[Hashable] = None) -> None:
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

    def __call__(self, cb: ChangeCallback[_T], *, key: Optional[Hashable] = None) -> None:
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

    def mapped(self, transform: Callable[[_T,_T], Optional[tuple[_V,_V]]], *,
               key: Optional[Hashable] = None
               ) -> ChangeCallbackList[_V]:
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
        ccl = ChangeCallbackList[_V]()
        def cb(old: _T, new: _T) -> None:
            transformed = transform(old, new)
            if transformed is not None:
                ccl.process(transformed[0], transformed[1])
        self.add(cb, key=key)
        return ccl

    def filtered(self, test: Callable[[_T,_T], bool], *,
                 key: Optional[Hashable] = None) -> ChangeCallbackList[_T]:
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

    def process(self, old: _T, new: _T) -> None:
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
    

class _CCLProperty(Generic[_T]):
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
                 creator: Callable[[object], ChangeCallbackList[_T]]) -> None:
        self.prop = prop
        self.tag = tag
        self.creator = creator
    @overload
    def __get__(self, obj: None, objtype: Any) -> _CCLProperty[_T]: ... # @UnusedVariable
    @overload
    def __get__(self, obj: Any, objtype: Any) -> ChangeCallbackList[_T]: ... # @UnusedVariable
    def __get__(self, obj: Any, objtype: Any) -> Union[ChangeCallbackList[_T], _CCLProperty[_T]]: # @UnusedVariable
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

    def mapped(self, transform: Callable[[_T,_T], Optional[tuple[_V,_V]]], *,
               key: Optional[Hashable] = None
               ) -> Gettable[object, ChangeCallbackList[_V]]:
        me = self
        def creator(obj: Any) -> ChangeCallbackList[_V]:
            ccl: ChangeCallbackList[_T] = me.__get__(obj, None)
            return ccl.mapped(transform, key=key)
        return _CCLProperty(self.prop, self.new_tag(), creator)

    def filtered(self, test: Callable[[_T,_T], bool], *,
                 key: Optional[Hashable] = None
                 ) -> Gettable[object, ChangeCallbackList[_T]]:
        me = self
        def creator(obj: Any) -> ChangeCallbackList[_T]:
            ccl: ChangeCallbackList[_T] = me.__get__(obj, None)
            return ccl.filtered(test, key=key)
        return _CCLProperty(self.prop, self.new_tag(), creator)



class MonitoredProperty(Generic[_T]):
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
    the object and returns a :attr:`MissingOr`\[``_T``], it is tried first the
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
        _T: the type of the value stored in the property.
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
                 default: MissingOr[_T] = MISSING,
                 default_fn: Optional[Callable[[Any], MissingOr[_T]]] = None,
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
        self._transform: Callable[[Any, _T], MissingOr[_T]] = lambda _obj, v: v

    def __set_name__(self, _owner: Any, name: str) -> None:
        if self._name is None:
            # print(f"Setting name for {_owner}.{name}")
            if name.startswith("_") and not name.startswith("__"):
                name = name[1:]
                # print(f"  Name now {name}")
            self._name = name

    def _default_value(self, obj: Any) -> MissingOr[_T]:
        dfn = self._default_fn
        if dfn is not None:
            val = dfn(obj)
            if val is not MISSING:
                return val
        return self._default_val


    def _lookup(self, obj: Any) -> MissingOr[_T]:
        key = self.val_attr
        val: MissingOr[_T] = getattr(obj, key, MISSING)
        if val is MISSING:
            val = self._default_value(obj)
            if val is not MISSING:
                setattr(obj, key, val)
        return val

    def _callback_list(self, obj: Any) -> Optional[ChangeCallbackList[_T]]:
        key = self.callback_list_attr
        ccl = getattr(obj, key, None)
        return ccl

    @overload
    def __get__(self, obj: None, objtype: Any) -> MonitoredProperty[_T]: ... # @UnusedVariable
    @overload
    def __get__(self, obj: Any, objtype: Any) -> _T: ... # @UnusedVariable
    def __get__(self, obj: Any, objtype: Any) -> Union[_T, MonitoredProperty[_T]]: # @UnusedVariable
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

    def __set__(self, obj: Any, value: _T) -> None:
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

    def __delete__(self, obj: Any) -> None:
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
    def callback_list(self) -> _CCLProperty[_T]:
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

        return _CCLProperty(self, "", lambda _: ChangeCallbackList[_T]())

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
            def __get__(self, obj: Any, objtype: Any) -> bool: # @UnusedVariable
                val = me._lookup(obj)
                return val is not MISSING
        return VC()

    @property
    def getter(self) -> Gettable[object, _T]:
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
            def __get__(self, obj: Any, objtype: Any) -> _T: # @UnusedVariable
                val = me._lookup(obj)
                if val is MISSING:
                    raise AttributeError(f"Attribute '{me.name}' not set in {obj}")
                return val
        return VC()

    @overload
    def transform(self, *,
                  chain: bool = False) -> Callable[[Callable[[Any, _T], MissingOr[_T]]], # @UnusedVariable
                                                   Callable[[Any, _T], MissingOr[_T]]]: ...
    @overload
    def transform(self, fn: Callable[[Any, _T], MissingOr[_T]], *, # @UnusedVariable
                  chain: bool = False) -> Callable[[Any, _T], MissingOr[_T]]: ... # @UnusedVariable
    def transform(self, fn: Optional[Callable[[Any, _T], MissingOr[_T]]] = None, *,
                  chain: bool = False) -> Union[Callable[[Any, _T], MissingOr[_T]],
                                                Callable[[Callable[[Any, _T], MissingOr[_T]]],
                                                         Callable[[Any, _T], MissingOr[_T]]]]:
        """
        A decorator that specifies that the decorated method should be called on
        the object, passing in the asserted value, e.g. ::

            class Counter:
                max_count = 100
                count = ManagedProperty[_T]("count", default=0)

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
        def set_it(func: Callable[[Any, _T], MissingOr[_T]]) -> Callable[[Any, _T], MissingOr[_T]]:
            if chain:
                prior = self._transform
                this_func = func # Need a separate name to avoid infinite recursion.
                def chained_func(obj: Any, val: _T) -> MissingOr[_T]:
                    pval = prior(obj, val)
                    return MISSING if pval is MISSING else this_func(obj, pval)
                func = chained_func
            self._transform = func
            return func
        if fn is None:
            return set_it
        else:
            return set_it(fn)
