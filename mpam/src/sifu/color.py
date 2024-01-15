from __future__ import annotations

from _collections import deque
from _weakref import ReferenceType, ref
from threading import Lock, RLock
from typing import Union, Final, Generic, TypeVar, Hashable, ClassVar, Optional, \
    Sequence, Mapping
from weakref import WeakKeyDictionary, finalize

from matplotlib._color_data import XKCD_COLORS


_H = TypeVar('_H', bound=Hashable)    ; "A generic type variable representing a :class:`typing.Hashable` type"

ColorSpec = Union[str, tuple[float,float,float], tuple[float,float,float,float]]
"""
A value that can be used to identify a :class:`Color`
"""
class Color:
    """
    A color.  The mapping of names to RGBA tuples is taken from `matplotlib`.

    :class:`Color`\s are found by calling :func:`find`, passing in either a name
    or an RGB(A) tuple.  The values are cached, so subsequent calls to
    :func:`find` with the same argument will reasult in the same :class:`Color`.
    """
    description: Final[str]  #: The description of the :class:`Color`
    rgba: Final[tuple[float,float,float,float]]
    """
    A tuple of red, blue, green, and alpha components of the :class:`Color`.
    """

    _class_lock: Final[Lock] = Lock()       #: A class lock over the cache
    _known: Final[dict[str, Color]] = {}    #: The cache of known :class:`Color`\s

    def __init__(self, description: str, rgba: tuple[float,float,float,float]) -> None:
        """
        Initialize the object

        Args:
            description: the description
            rgba: a tuple of red, green, blue, and alpha components.
        """
        self.description = description
        self.rgba = rgba

    @classmethod
    def find(cls, description: ColorSpec) -> Color:
        """
        Find (or create) the :class:`Color` with the given name or RGB(A)
        components.  If a string is given as the ``description``, the RGBA
        components are looked up via `matplotlib`.  Otherwise, ``description``
        should be a touple of three (RGB) or four (RGBA) numbers from ``0.0`` to
        ``1.0`` inclusive, and the :attr:`description` of the resulting
        :class:`Color` will be the result of formatting ``description``.

        Args:
            description: the description of the :class:`Color`.
        """
        key = str(description)
        with cls._class_lock:
            c = cls._known.get(key, None)
            if c is None:
                from matplotlib import colors
                c = Color(key, colors.to_rgba(description))
            cls._known[key] = c
            return c

    def __repr__(self) -> str:
        return f"Color({repr(self.description)}, {repr(self.rgba)})"

    def __str__(self) -> str:
        return self.description

class ColorAllocator(Generic[_H]):
    """
    An allocator associating :class:`Color` objects with elments of some
    :class:`Hashable` type :attr:`H`.

    The basic idea is that you call :func:`get_color` to obtain a :class:`Color`
    to use to represent an element.  For example, if ``alloc`` is a
    :class:`ColorAllocator`\[:class:`Reagent`] and ``r`` is a :class:`Reagent`, then ::

        c = alloc.get_color(r)

    will obtain a :class:`Color` for ``r``.  If called again with the same
    argument, the same :class:`Color` will be returned.  To reserve a specific
    :class:`Color` for an object, use :func:`reserve_color`::

        alloc.reserve_color(waste_reagent, "black")

    The ``color`` argument to :func:`reserve_color` may be a :class:`Color` or
    anything usable as the argument to :func:`Color.find` (e.g., a string or
    tuple of floats).

    By default, :func:`get_color` will allocate :class:`Color`\s from
    :func:`ColorAllocator.default_color_list()`, which is an array of 954 common
    colors that can be found at https://xkcd.com/color/rgb/.  To use a different
    list (or a permutation of this list), specify the ``all_colors`` parameter
    when constructing the :class:`ColorAllocator`.

    Internally, the class uses a :class:`WeakKeyDictionary` to manage the
    associations, so it does not hold onto the objects for which
    :class:`Color`\s have been allocated, and when one gets garbage collected,
    the associated :class:`Color` may become available to be associated with a
    new object.  If a color is associated with more than one object (via
    :func:`reserve_color`), it does not become available until all such
    associations have been dropped.

    The colors are allocated in order, skipping any that have been reserved.
    Only when the list has been exhausted will colors that had been previously
    allocated for no-longer-extant objects be reused.  If all colors are
    associated with objects, :class:`IndexError` will be raised.

    To remove any :class:`Color` association for an object, use
    :func:`release_color_for`.  This will render the :class:`Color` (if any)
    available for future calls to :func:`get_color`.  Note that
    :func:`release_color` for can safely be called even if its argument was
    never used in a call to :func:`get_color`.

    Warning:
        Internally, the mapping from objects to :class:`Color`\s is kept in a
        :class:`WeakKeyDictionary`.  A consequence of this is that if :class:`H`
        defines equality as different from identity, non-identical equal objects
        will get the same :class:`Color`, but when the first such object gets
        garbage collected, the association will be removed from the table and
        any subsequent ones will not find a match and so will get allocated a
        new color.

    Args:
        H: The :class:`Hashable` type to associate :class:`Color`\s with.
    """
    _default_color_list: ClassVar[Optional[Sequence[str]]] = None

    all_colors: Final[Sequence[str]]
    "The colors accessible to :func:`get_color`"
    color_assignments: WeakKeyDictionary[_H, tuple[Color, finalize]]
    "A weak key mapping from key to :class:`Color`"
    colors_in_use: Final[dict[Color, int]]
    "The count of objects using in-use :class:`Color`\s"
    returned_colors: Final[deque[Color]]
    "Previously-allocated :class:`Color` objects that have become available"
    next_reagent_color: int
    "The index of the next :class:`Color` to allocate in :attr:`all_colors`"
    _lock: Final[RLock]                 ; "A local lock for managing tables"
    _class_lock: Final[Lock] = Lock()   ; "A class lock for manageing :attr:`_default_color_list`"

    def __init__(self, *,
                 initial_reservations: Optional[Mapping[_H, Union[Color,ColorSpec]]] = None,
                 all_colors: Optional[Sequence[str]] = None):
        """
        Initialize the object.

        The values of ``initial_reservation`` may be anything acceptable to
        :func:`reserve_color`.

        If ``all_colors`` is ``None``, :func:`default_color_list` will be used.

        Keyword Args:
            initial_reservations: initial :class:`Color` reservations
            all_colors: an optional list of :class:`Color`\s for :func:`get_color` to use.
        """
        self.color_assignments = WeakKeyDictionary()
        self.colors_in_use = {}
        self.returned_colors = deque[Color]()
        self.next_reagent_color = 0
        self._lock = RLock()
        if initial_reservations is not None:
            for k,c in initial_reservations.items():
                self.reserve_color(k, c)

        if all_colors is None:
            all_colors = self.default_color_list()
        self.all_colors = all_colors

    @classmethod
    def default_color_list(cls) -> Sequence[str]:
        """
        The default list of :class:`Color`\s to use.  This list is not created
        until it is needed.

        The current list is an array of 954 common colors that can be found at
        https://xkcd.com/color/rgb/.
        """
        all_colors = cls._default_color_list
        if all_colors is None:
            with cls._class_lock:
                all_colors = cls._default_color_list
                if all_colors is None:
                    all_colors = [k for k in XKCD_COLORS]
                    cls._default_color_list = all_colors
        return all_colors

    def _lose_mapping(self, color: Color) -> None:
        """
        Note that an association has been lost with a :class:`Color`.  If this
        is the last such association for the :class:`Color`, add it to
        :attr:`returned_colors`.

        Note:
            The method assumes that :attr:`_lock` is locked.

        Args:
            color: the :class:`Color` for which the association has been lost
        """
        uses = self.colors_in_use[color]
        if uses > 1:
            self.colors_in_use[color] = uses-1
        else:
            del self.colors_in_use[color]
            self.returned_colors.append(color)

    @staticmethod
    def _lose_mapping_on_gc(color: Color, selfref: ReferenceType[ColorAllocator]) -> None:
        """
        Handle GC of key object.  If the :class:`ColorAllocator` is still
        around, call :func:`_lose_mapping`.

        Args:
            color: the :class:`Color` associated with the lost key
            selfref: a weak reference to the :class:`ColorAllocator`
        """
        self = selfref()
        if self is not None:
            with self._lock:
                self._lose_mapping(color)

    def reserve_color(self, key: _H,
                      color: Union[Color, ColorSpec]) -> None:
        """
        Associate a :class:`Color` with an object.  This renders the
        :class:`Color` unavailable to :func:`get_color`.

        ``color`` may be either a :class:`Color` or a :class:`ColorSpec`, i.e.,
        anything acceptable to :func:`Color.find`.  In particular, it may be a
        string or a 3- or 4-elment tuple of floats.

        If there was already a reservation for ``key``, this one replaces it,
        and subsequent calls to :func:`get_color` will return this one.

        Args:
            key: the object to associate with the :class:`Color`
            color: the :class:`Color` or a description by which it can be identified
        """
        assignments = self.color_assignments
        if not isinstance(color, Color):
            color = Color.find(color)
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
        """
        Return the next available :class:`Color`, modifying
        :attr:`next_reagent_color`.

        It continues through :attr:`all_colors` and then takes values off of
        :attr:`returned_colors`.

        Note:
            The method assumes that :attr:`_lock` is locked.

        Returns:
            the next :class:`Color`
        Raises:
            IndexError: if there are no more available :class:`Color`\s

        """
        color_list = self.all_colors
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

    def get_color(self, key: _H) -> Color:
        """
        Find the :class:`Color` associated with an object.

        If none has previously been associated with the object, the next
        unreserved :class:`Color` in :attr:`all_colors` is grabbed.  If
        :attr:`all_colors` has been exhausted, a :class:`Color` is pulled from
        :attr:`returned_colors`.  If this, too, is empty, an :class:`IndexError`
        is raised.

        If a new :class:`Color` is identified, it is associated with ``key`` by
        means of :func:`reserve_color`.

        Args:
            key: the domain object
        Returns:
            the associated :class:`Color`
        Raises:
            IndexError: if there are no more available :class:`Color`\s

        """
        assignments = self.color_assignments
        ct = assignments.get(key, None)
        if ct is not None:
            return ct[0]
        c = self._next_color()
        self.reserve_color(key, c)
        return c

    def release_color_for(self, key: _H) -> bool:
        """
        Remove any :class:`Color` association with an object.  If no other
        object is associated with that :class:`Color`, it is added to
        :attr:`returned_colors`, making it available for future calls to
        :func:`get_color`.

        If :func:`get_color` is called in the future with ``key`` as the
        argument, a new :class:`Color` will be identified and associated with
        it.

        Args:
            key: the domain object
        Returns:
            ``True`` if there was an association to remove, ``False`` otherwise
        """
        assignments = self.color_assignments
        with self._lock:
            ct = assignments.pop(key, None)
            if ct is None:
                return False
            color = ct[0]
            self._lose_mapping(color)
            return True
