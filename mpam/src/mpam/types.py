"""
Support classes for MPAM applications other than those that describe hardware.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from fractions import Fraction
import logging
import math
from threading import Lock
from typing import Union, Generic, TypeVar, Optional, Callable, \
    Final, ClassVar, Mapping, Tuple, Sequence

from erk.basic import MissingOr, MISSING
from erk.monitored import MonitoredProperty, ChangeCallbackList
from erk.numutils import farey
from quantities.SI import sec, deg_C
from quantities.dimensions import Molarity, MassConcentration, \
    VolumeConcentration, Volume
from quantities.temperature import TemperaturePoint


logger = logging.getLogger(__name__)

_T = TypeVar('_T')    ; "A generic type variable"

class OnOff(Enum):
    """ An enumerated type representing `ON` and `OFF` states.

    In boolean contexts, `OFF` is `False`, and `ON` is `True`.

    `!ON` is `OFF`, and vice versa.
    """
    OFF = 0 ; "Represents being off"
    ON = 1  ; "Represents being on"

    def __bool__(self) -> bool:
        "`ON` is `True`; `OFF is `False`"
        return self is OnOff.ON

    def __invert__(self) -> OnOff:
        "`!ON` is `OFF, and vice versa"
        return OnOff.OFF if self else OnOff.ON

    @classmethod
    def from_bool(cls, val: bool) -> OnOff:
        return OnOff.ON if val else OnOff.OFF



deg_C_per_sec: Final = (deg_C/sec)


    
        






# Used in the case when a chemical is there, but its concentration
# cannot be computed.  Usually when two reagents specify the chemical,
# but with different concentration units
class UnknownConcentration:
    """
    Used in the case when a chemical is there but its concentration cannot be
    compute.  This usually occurs when two reagents specify the chemical, but
    they use different concentration units (e.g., :class:`.Molarity` and
    :class`.VolumeConcentration`).

    It is expected that the only instance of :class:`UnknownConcentration` will
    be the singleton constant :attr:`unknown_concentration`.

    Arithmetic on :class:`UnknownConcentration` does not change the value.
    """
    def __repr__(self) -> str:
        return "UnknownConcentration()"
    def __str__(self) -> str:
        return "unknown concentration"

    def __mul__(self, _: float) -> UnknownConcentration:
        return self

    def __plus_(self, _: UnknownConcentration) -> UnknownConcentration:
        return self

unknown_concentration: Final[UnknownConcentration] = UnknownConcentration()
"""
The constant singleton object of class :class:`UnknownConcentration`.
"""


Concentration = Union[Molarity, MassConcentration, VolumeConcentration, UnknownConcentration]
"""
Any of the many ways to describe the concentration of a chemical in a reagent.
"""


class Chemical:
    """
    A chemical that may exist as a component of a :class:`Reagent`.  It has a
    name and optionally a formula and a description, all strings.

    The class maintains a dictionary of instances keyed by name, so the
    encouraged way to obtain an object is to look it up using :func:`find`,
    which will create the :class:`Chemical` if one is not already there::

        c = Chemical.find("oxygen", formula="O2")

    ``name`` is final, but ``formula`` and ``description`` may be modified.
    """
    name: Final[str]            #: The name of the :class:`Chemical`
    formula: Optional[str]      #: The optional formula of the :class:`Chemical`
    description: Optional[str]  #: An optional description of the :class:`Chemical`

    known: ClassVar[dict[str, Chemical]] = {}
    """
    The known instances, keyed by name
    """

    def __init__(self, name: str, *,
                 formula: Optional[str] = None,
                 description: Optional[str] = None) -> None:
        """
        Initialize the object
        Args:
            name: the name of the :class:`Chemical`
        Keyword Args:
            formula: the optional formula of the :class:`Chemical`
            description: an optinal description of the :class:`Chemical`
        """
        self.name = name
        self.formula = formula
        self.description = description
        Chemical.known[name] = self

    @classmethod
    def find(cls, name: str, *,
             formula: Optional[str] = None,
             description: Optional[str] = None) -> Chemical:
        """
        Find a :class:`Chemical` with the given name, otherwise create one.  If
        a new :class:`Chemical` is created, it is added to ``known``.

        Note:
            If a :class:`Chemical` with the given name is already known, the
            formula and description will not be modified.

        Args:
            name: the name of the :class:`Chemical`
        Keyword Args:
            formula: the optional formula of the :class:`Chemical`
            description: an optinal description of the :class:`Chemical`
        Returns:
            the found or created :class:`Chemical`
        """
        c = cls.known.get(name, None)
        if c is None:
            c = Chemical(name, formula=formula, description=description)
        return c

    def __repr__(self) -> str:
        return f"Chemical[{self.name}]"

    def __str__(self) -> str:
        return self.name

ChemicalComposition = Mapping[Chemical, Concentration]
"""
A mapping from :class:`Chemical` to :class:`Concentration`
"""

class ProcessStep:
    """
    A processing step that a :class:`Reagent` can go through.

    The basic notion is that if ``r`` is a :class:`Reagent` and ``ps` is a
    :class:`ProcessStep`, after ::

        r2 = r.processed(ps)

    ``r2`` will be a different reagent with the property that
    ``r2.unprocessed()`` will be ``r`` (or, at least ``r.unprocessed()``) and
    ``r2.process_steps()`` will end with ``ps``.

    :class:`ProcessStep`\s can be obtained by calling :func:`find_or_create`,
    passing in a description::

        ps = ProcessStep.find_or_create("thermocycle")
    """
    description: Final[str]                     #: The description of the :class:`ProcessStep`
    _known: Final[dict[str, ProcessStep]] = {}  #: Known :class:`ProcessStep`\s keyed by description
    _class_lock: Final[Lock] = Lock()           #: The class lock.

    def __init__(self, description: str) -> None:
        """
        Initialize the object.

        Args:
            description: the description of the :class:`ProcessStep`
        """
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
        """
        Find or create a :class:`ProcessStep` with the given description.

        Note:
            This only works to find basic ProcessStep objects created by this
            method. Those instantiated directly (including by subclassing) will
            not be found.  Arguably, this is the correct behavior.
        Args:
            description: the description of the :class:`ProcessStep`
        Returns:
            the found or created :class:`ProcessStep`
        """
        with cls._class_lock:
            ps = cls._known.get(description, None)
            if ps is None:
                ps = ProcessStep(description)
                cls._known[description] = ps
            return ps

MixtureSpec = Tuple[tuple['Reagent', Fraction], ...]
"""
A description of :class:`Reagent` mixtures as a tuple of tuples of
:class:`Reagent` and :class:`Fraction`.

As used in :class:`Reagent`, the :class:`Reagent`\s will be unique, and the
overall tuple will be sorted by :class:`Reagent` name.
"""

class Reagent:
    """
    A reagent.  All :class:`Reagent`\s have

    * a :attr:`name`

    * a chemical :attr:`composition` (which will be an empty dict unless
      specified) as a mapping from :class:`Chemical` to :class:`Composition`

    * optional minimum (:attr:`min_storage_temp`) and maximum
      (:attr:`max_storage_temp`) storage temperatures

    * a :attr:`mixture` description, useful when a :class:`Reagent` is a not-
      otherwise-named mixture of two or more :class:`Reagent`\s

    * an indication of whether the :class:`Reagent` :attr:`is_pure` (i.e., not a
      mixture).

    * a tuple of :attr:`process_step` that the :class:`Reagent` has gone
      through.

    * the :attr:`unprocessed` :class:`Reagent` prior to any processing.  (Often
      this :class:`Reagent` itself.)

    :class:`Reagent`\s can be ordered, and sort by their :attr:`name`\s.
    """
    name: Final[str]                        #: The name of the :class:`Reagent`
    composition: ChemicalComposition
    """
    The composition of the :class:`Reagent`.  If this is empty, nothing is known
    about the composition.
    """
    min_storage_temp: Optional[TemperaturePoint] #: The (optional) minimum storage temperature of the :class:`Reagent`.
    max_storage_temp: Optional[TemperaturePoint] #: The (optional) maximum storage temperature of the :class:`Reagent`.
    _lock: Final[Lock] #: A local lock
    _process_results: Final[dict[ProcessStep, Reagent]]
    """
    A cache of the result of calling :func:`process` with different arguments.
    """

    known: ClassVar[dict[str, Reagent]] = dict[str, 'Reagent']()
    """
    A cache of known :class:`Reagent`\s, by name.
    """


    def __init__(self, name: str, *,
                 composition: Optional[ChemicalComposition] = None,
                 min_storage_temp: Optional[TemperaturePoint] = None,
                 max_storage_temp: Optional[TemperaturePoint] = None,
                 ) -> None:
        """
        Initialize the object.

        The new :class:`Reagent` will be pure (i.e., not a mixture) and will
        have no process steps.

        Args:
            name: the name of the :class:`Reagent`
        Keyword Args:
            composition: an optional composition as a mapping from
                         :class:`Chemical` to :class:`Concentration`
            min_storage_temp: an optional minimum storage temperature
            max_storage_temp: an optional maximum storage temperature
        """
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
             min_storage_temp: Optional[TemperaturePoint] = None,
             max_storage_temp: Optional[TemperaturePoint] = None) -> Reagent:
        """
        Find or create the :class:`Reagent` with a given name.

        Note:
            If an existing :class:`Reagent` with this name has previously been
            created, it will be returned and any specified ``composition``,
            ``min_storage_temp``, or ``max_storage_temp`` will be ignored.

        Args:
            name: the name of the :class:`Reagent`
        Keyword Args:
            composition: an optional composition as a mapping from
                         :class:`Chemical` to :class:`Concentration`
            min_storage_temp: an optional minimum storage temperature
            max_storage_temp: an optional maximum storage temperature
        Returns:
            the found or created :class:`Reagent`
        """
        c = cls.known.get(name, None)
        if c is None:
            c = Reagent(name, composition=composition,
                         min_storage_temp=min_storage_temp, max_storage_temp=max_storage_temp)
        return c

    @property
    def mixture(self) -> MixtureSpec:
        """
        A description of the :class:`Reagent` as a mixture of other
        :class:`Reagent`\s.  The description is a tuple of tuples, each of which
        contains a :class:`Reagent` and a :class:`Fraction` specifying how much
        of the overall mixture that :class:`Reagent` constitutes.

        The elements of this tuple will be sorted by :class:`Reagent` name,
        rendering the whole thing useful as a mapping key.

        This :class:`Reagent` :func:`is_pure` if and only if the the resulting
        tuple has one element, and the first element of that element will be
        this :class:`Reagent`.

        The second elements of each element of this tuple (:class:`Fraction`\s)
        will all add up to ``1``.
        """
        return ((self, Fraction.from_float(1)),)

    @property
    def is_pure(self) -> bool:
        """
        Is the :class:`Reagent` not a mixture?  ``True`` iff :func:`mixture` has
        exactly one element.
        """
        return len(self.mixture) == 1

    @property
    def process_steps(self) -> tuple[ProcessStep, ...]:
        """
        The :class:`ProcessStep`\s this :class:`Reagent` has gone through.
        """
        return ()

    @property
    def unprocessed(self) -> Reagent:
        """
        The unprocessed version of this :class:`Reagent`.
        """
        return self

    def liquid(self, volume: Volume, *, inexact: bool = False) -> Liquid:
        """
        A :class:`Liquid` containing a specified :class:`.Volume` of this
        :class:`Reagent`

        Args:
            volume: the volume of the resulting liquid
        Keyword Args:
            inexact: whether the volume is inexact
        Returns:
            a new :class:`Liquid`
        """
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
        """
        A composition-altering function that doesn't change the composition.

        This function suitable for use as the ``new_omposition_function``
        argument to :func:`processed` when the :class:`ProcessStep` does not
        change the chemical composition.

        Args:
            composition: the old composition
        Returns:
            ``composition`` unchanged.
        """
        return composition

    @staticmethod
    def LoseComposition(composition: ChemicalComposition) -> ChemicalComposition:  # @UnusedVariable
        """
        A composition-altering function that returns an unknown composition.

        This function suitable for use as the ``new_omposition_function``
        argument to :func:`processed` when the :class:`ProcessStep` has an
        unknown effect on the chemical composition.

        Args:
            composition: the old composition
        Returns:
            an unknown composition (e.g., ``{}``)
        """
        return {}


    def processed(self, step: Union[str, ProcessStep],
                  new_composition_function: Optional[Callable[[ChemicalComposition], ChemicalComposition]] = None,
                  *,
                  min_storage_temp: Optional[TemperaturePoint] = None,
                  max_storage_temp: Optional[TemperaturePoint] = None) -> Reagent:
        """
        A new version of the :class:`Reagent` after it has been processed.

        If this :class:`Reagent` is the :attr:`waste_reagent`, it is returned
        unchanged.

        The results of calling :func:`processed` on a given :class:`Reagent` are
        cached, and an existing value will be reused.

        If a new one is created, the composition and minimum and maximum storage
        temperatures are modified as specified by the parameters or, if
        unspecified, copied from this :class:`Reagent`.

        Note:
            If a cached result of a prior call to :func:`processed` with this
            ``step`` is found, it will be returned, and the other arguments will
            be ignored.

        Args:
            step: the :class:`ProcessStep` applied or the name used to find or
                  create it.

            new_composition_function: an optional function to determine the new
                                      composition.
        Keyword Args:
            min_storage_temp: an optional minimum storage temperature
            max_storage_temp: an optional maximum storage temperature
        Returns:
            the resulting :class:`Reagent`
        """
        if self is waste_reagent:
            return self
        if isinstance(step, str):
            step = ProcessStep.find_or_create(step)
        with self._lock:
            r = self._process_results.get(step, None)
            if r is None:
                if new_composition_function is None:
                    new_composition_function = Reagent.SameComposition
                new_c = new_composition_function(self.composition)
                r = ProcessedReagent(self, step,
                                     composition = new_c,
                                     min_storage_temp = min_storage_temp or self.min_storage_temp,
                                     max_storage_temp = max_storage_temp or self.max_storage_temp)
                self._process_results[step] = r
            return r



waste_reagent: Final[Reagent] = Reagent.find("waste")
"""
The waste :class:`Reagent`.

If the :attr:`waste_reagent` goes through a :class:`ProcessStep` or is mixed with
another :class:`Reagent`, the result will be the :attr:`waste_reagent`.
"""
unknown_reagent: Final[Reagent] = Reagent.find("unknown")
"""
An unknown :class:`Reagent.

This :class:`Reagent` is typically used for zero-volume :class:`Liquid`\s and
the contents of empty wells, but it is also reasonable to use in contexts in
which the actual :class:`Reagent` is unknown or unimportant.
"""

MixResult = Union[Reagent, str]
"""
The specification of the result of a mixing operation.  Either a
:class:`Reagent` or the name of one.
"""

class Mixture(Reagent):
    """
    A :class:`Reagent` that is a mixture of two or more other :class:`Reagent`\s

    :class:`Mixture` objects are not typically created directly.  If one is
    needed as a :class:`Reagent`, you can use :func:`find_or_compute` which
    computes (or finds a cached version of) a mixture between to
    :class:`Reagent`\s.  More commonly, :class:`Mixture` objects will be created
    as a consequence of mixing together two :class:`Liquid` objects using
    :func:`Liquid.mix_with`, :func:`Liquid.mix_in`, or
    :func:`Liquid.mix_together`.

    When created using one of the aforementioned methods, if the name of the
    resulting :class:`Mixture` is not specified a name describing the relative
    proportions of the constituents will be constructed.  For example, after ::

        r3 = Mixture.find_or_compute(r1, r2, ratio = 0.4)

    the name of ``r3`` will be ``"2 r1 + 5 r2"``
    """
    _mixture: Final[MixtureSpec]        #: The mixture specification
    _class_lock: Final[Lock] = Lock()   #: A class lock for managing caches
    _known_mixtures: Final[dict[tuple[float,Reagent,Reagent], Reagent]] = {}
    "Cached results of calling :func:find_or_compute`"
    _instances: Final[dict[MixtureSpec, Mixture]] = {}
    "Cached results of calling :func:`new_mixture`"

    def __init__(self, name: str, mixture: MixtureSpec, *,
                 composition: Optional[ChemicalComposition] = None,
                 min_storage_temp: Optional[TemperaturePoint] = None,
                 max_storage_temp: Optional[TemperaturePoint] = None,
                 ) -> None:
        """
        Initialize the object.

        Args:
            name: the name of the :class:`Reagent`
            mixture: the :class:`MixtureSpec` describing the mixture
        Keyword Args:
            composition: an optional composition as a mapping from
                         :class:`Chemical` to :class:`Concentration`
            min_storage_temp: an optional minimum storage temperature
            max_storage_temp: an optional maximum storage temperature
        """
        super().__init__(name, composition=composition, min_storage_temp=min_storage_temp, max_storage_temp=max_storage_temp)
        self._mixture = mixture

    @property
    def mixture(self) -> MixtureSpec:
        return self._mixture

    def __repr__(self) -> str:
        return f"Mixture({repr(self.name), repr(self._mixture)})"


    @classmethod
    def new_mixture(cls, r1: Reagent, r2: Reagent, ratio: float, name: Optional[str] = None) -> Reagent:
        """
        A mixture of two :class:`Reagent`\s in a given ratio.

        The :attr:`composition` of the resulting :class:`Reagent` will be
        computed based on the same ratio of the compositions of ``r1`` and
        ``r2``.

        If ``name`` is not provided, a name describing the relative proportions
        of the constituents will be constructed.  For example, after ::

            r3 = Mixture.find_or_compute(r1, r2, ratio = 0.4)

        the name of ``r3`` will be ``"2 r1 + 5 r2"``


        Important:
            :func:`find_or_compute` is more efficient than :func:`new_mixture`
            and is the method that should be used.  (:func:`find_or_compute`
            uses :func:`new_mixture` internally if necessary.)  This is because
            in addition to caching results based on the constructed
            :class:`MixtureSpec`, :func:`find_or_compute` caches them based on
            the arguments, so if the same :class:`Reagent`\s are mixed
            repeatedly in the same proportions, the results will be found
            without having to compute the :class:`MixtureSpec`.

        Note:
            A ratio of ``n`` means ``n`` parts ``r1`` to one part ``r2``.  This
            means that a ratio of ``1`` means equal parts, and a ratio of, e.g.,
            ``0.4`` means two parts ``r1`` to five parts ``r2``.

        Note:
            The name of the method notwithstanding, the results of calling
            :func:`new_mixture` are cached, and if the same resulting
            :class:`MixtureSpec` is discovered, the prior result will be
            returned.  When mixtures are further mixed, this can happen even if
            a different path is taken
        Args:
            r1: the first :class:`Reagent`
            r2: the second :class:`Reagent`
        Keyword Args:
            ratio: the ratio of ``r1`` to ``r2``
            name: an optional name of the result.
        Returns:
            The mixture as a :class:`Reagent`
        """
        fraction = ratio/(ratio+1)
        # as_frac = Fraction.from_float(fraction)
        as_frac = farey(fraction)
        # print(f"fraction: {as_frac}")
        mixture = {r: f*as_frac for r,f in r1.mixture}
        composition = {chem: conc*fraction for chem, conc in r1.composition.items()}
        fraction = 1-fraction
        # as_frac = Fraction.from_float(fraction)
        as_frac = farey(fraction)
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

        # print(f"{mixture}")
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

    # @classmethod
    # def find_or_compute_aux(cls, specs: tuple[tuple[float, Reagent]], *,
    #                         name: Optional[str] = None) -> Reagent:
    #     # TODO:
    #     # Note, need to normalize before lookup?
    #     ...

    @classmethod
    def find_or_compute(cls, r1: Reagent, r2: Reagent, *,
                        ratio: float = 1,
                        name: Optional[str] = None) -> Reagent:
        """
        A mixture of two :class:`Reagent`\s in a given ratio.

        The :attr:`composition` of the resulting :class:`Reagent` will be
        computed based on the same ratio of the compositions of ``r1`` and
        ``r2``.

        If ``name`` is not provided, a name describing the relative proportions
        of the constituents will be constructed.  For example, after ::

            r3 = Mixture.find_or_compute(r1, r2, ratio = 0.4)

        the name of ``r3`` will be ``"2 r1 + 5 r2"``

        Important:
            :func:`find_or_compute` is more efficient than :func:`new_mixture`
            and is the method that should be used.  (:func:`find_or_compute`
            uses :func:`new_mixture` internally if necessary.)  This is because
            in addition to caching results based on the constructed
            :class:`MixtureSpec`, :func:`find_or_compute` caches them based on
            the arguments, so if the same :class:`Reagent`\s are mixed
            repeatedly in the same proportions, the results will be found
            without having to compute the :class:`MixtureSpec`.

        Note:
            A ratio of ``n`` means ``n`` parts ``r1`` to one part ``r2``.  This
            means that a ratio of ``1`` means equal parts, and a ratio of, e.g.,
            ``0.4`` means two parts ``r1`` to five parts ``r2``.

        Note:
            The results of calling :func:`find_or_compute` are cached, and if the
            same resulting :class:`MixtureSpec` is discovered, the prior result
            will be returned.  When mixtures are further mixed, this can happen
            even if a different path is taken
        Args:
            r1: the first :class:`Reagent`
            r2: the second :class:`Reagent`
        Keyword Args:
            ratio: the ratio of ``r1`` to ``r2``
            name: an optional name of the result.
        Returns:
            The mixture as a :class:`Reagent`
        """
        if r1 is r2:
            return r1
        if r1 is waste_reagent or r2 is waste_reagent:
            return waste_reagent
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
    """
    The :class:`Reagent` resulting from calling :func:`process`
    """
    last_step: Final[ProcessStep] #: The last :class:`ProcessStep` used to create this :class:`Reagent`
    prior: Final[Reagent]         #: The :class:`Reagent` prior to :attr:`last_step`

    def __init__(self, prior: Reagent, step: ProcessStep, *,
                 composition: Optional[ChemicalComposition] = None,
                 min_storage_temp: Optional[TemperaturePoint] = None,
                 max_storage_temp: Optional[TemperaturePoint] = None,
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
    """
    A quantity of a :class:`Reagent`.  Both the :attr:`volume` and the
    :attr:`reagent` can change over time, and so differnt :class:`Liquid`\s may
    have the same state, but each will retain its own identity.

    Callbacks can be registered for both :attr:`volume` and :attr:`reagent` by
    using the :class:`ChangeCallbackList`\s :attr:`on_volume_change` and
    :attr:`on_reagent_change`::

        liq.on_reagent_change(note_reagent_change, key=nrc_key)
        liq.on_volume_change(note_volume_change)

    In addition to :attr:`volume`, a :class:`Liquid` also has an indication of
    whether the :attr:`volume` is :attr:`inexact`.  Typically, this will be
    ``False``, but if it is ``True``, it is not safe to assume that, e.g.,
    incrementally removing volume will necessarily have removed all of it.

    As a convenience, a :class:`.Volume` can be added to or subtracted from a
    :class:`Liquid`, e.g. ::

        liq -= 2*uL

    The resulting :class:`.Volume` is clipped at zero.

    :class:`Liquid`\s can be mixed together in several ways:

    * :func:`mix_with` returns the result of mixing a given :class:`Liquid` with
      another.  Neither :class:`Liquid` is modified.

    * :func:`mix_in` modifies a given :class:`Liquid` by setting it to the
      result of mixing in another.  The other :class:`Liquid` gets the
      :attr:`reagent` of the mixture, but its :attr:`volume` is set to zero.

    * :func:`Liquid.mix_together` returns the result of mixing together several
    :class:`Liquid`\s (or parts of them).  None are modified.

    For all of these, the resulting :class:`Reagent` will be proportional to the
    volumes.  For example, after ::

        liq1 = r1.liquid(1*mL)
        liq2 = r2.liquid(2*mL)
        r1.mix_in(r2)

    ``r1.volume`` will be ``3*mL`` and ``r1.reagent`` will print as ``1 r1 + 2
    r2``.  (``r2`` will have the same reagent, but its volume will be zero.)

    The mixing methods all take an optional ``result`` parameter, which is
    either a :class:`Reagent` or a string.  If it is a :class:`Reagent`, it will
    be used as the reagent for the mixture.  If it is a string, it will be used
    as the name for the resulting (computed) mixture unless either the reagents
    of the two liquids are the same (in which case the mixture has the same
    reagent) or one of them is the :attr:`waste_reagent` (in which case the
    mixture will be, as well).

    To split the contents of a :class:`Liquid` into two parts, use
    :func:`split_to`.  As this overwrites the content of the other
    :class:`Liquid`, it should only be used when the other is known to be empty.
    It is particularly useful when doing a "merge and split", as ::

        liq1.mix_in(liq2)
        liq1.split_to(liq2)

    After this sequence, both :class:`Liquid`\s will have the same (mixed)
    reagent and a volume that is the average of the two original volumes.



    """
    inexact: bool       #: Is :attr:`volume` inexact?

    volume: MonitoredProperty[Volume] = MonitoredProperty()
    """
    The :class:`.Volume` of the :class:`Liquid`.  In some cases, this should
    be interpreted in conjunction with :attr:`inexact`.

    Setting :attr:`volume` to a :class:`.Volume` different from the previous
    value will trigger the callbacks in :attr:`volume_change_callbacks`
    """

    on_volume_change: ChangeCallbackList[Volume] = volume.callback_list
    "The :class:`ChangeCallbackList` monitoring :attr:`volume`"

    reagent: MonitoredProperty[Reagent] = MonitoredProperty()
    """
    The :class:`Reagent` of the :class:`Liquid`.

    Setting :attr:`reagent` to a :class:`.Reagent` different from the previous
    value will trigger the callbacks in :attr:`reagent_change_callbacks` only if
    the new value is not the same as the old value.
    """

    on_reagent_change: ChangeCallbackList[Reagent] = reagent.callback_list
    "The :class:`ChangeCallbackList` monitoring :attr:`reagent`"

    def __init__(self, reagent: Reagent, volume: Volume, *, inexact: bool = False) -> None:
        """
        Initialize the object.

        Args:
            reagent: the :class:`Reagent` of the :class:`Liquid`
            volume: the :class:`.Volume` of the :class:`Liquid`
        Keyword Args:
            inexact: is ``volume`` inexact?
        """
        self.reagent = reagent
        self.volume = volume
        self.inexact = inexact

    def __repr__(self) -> str:
        return f"Liquid[{'~' if self.inexact else ''}{self.volume}, {self.reagent}]"

    def __str__(self) -> str:
        return f"{'~' if self.inexact else ''}{self.volume:,g} of {self.reagent}"

    def __iadd__(self, rhs: Volume) -> Liquid:
        self.volume = min(self.volume+rhs, Volume.ZERO)
        return self

    def __isub__(self, rhs: Volume) -> Liquid:
        self.volume = max(self.volume-rhs, Volume.ZERO)
        return self

    def mix_with(self, other: Liquid, *, result: Optional[MixResult] = None) -> Liquid:
        """
        A new :class:`Liquid` that is the result of mixing this :class:`Liquid`
        with another.

        The :attr:`volume` of the result is the sum of the volumes of the two
        :class:`Liquids`.  The :attr:`reagent` of the result is

        * ``result`` if this is a :class:`Reagent`
        * :attr:`reagent` if this is the same for both :class:`Liquid`\s
        * :attr:`waste_reagent`, if the :attr:`reagent` for either :class:`Liquid`
          is :attr:`waste_reagent`
        * the result of calling :func:`Mixture.find_or_compute`, passing in
          ``result`` (which is either a string or ``None``) as the ``name``
          parameter.

        The resulting :class:`Liquid` is :attr:`inexact` if either
        :class:`Liquid` is.

        Note:

            Neither :class:`Liquid` is modified.  To modify this :class:`Liquid`
            to be the result of the mixture (and clear the other), use
            :func:`mix_in`.

        Args:
            other:  the :class:`Liquid` to mix with
        Keyword Args:
            result: the resulting :class:`Reagent`, the name of the computed
                    :class:`Reagent`, or ``None`` (indicating that the name
                    should be computed)
        Returns:
            a new :class:`Liquid` with the resulting :class:`Reagent` and :class:`.Volume`.
        """
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

    def mix_in(self, other: Liquid, *, result: Optional[MixResult] = None) -> None:
        """
        Modify this :class:`Liquid` to be the result of mixing it with another.

        The :attr:`volume` of the result is the sum of the volumes of the two
        :class:`Liquids`.  The :attr:`reagent` of the result is

        * ``result`` if this is a :class:`Reagent`
        * :attr:`reagent` if this is the same for both :class:`Liquid`\s
        * :attr:`waste_reagent`, if the :attr:`reagent` for either :class:`Liquid`
          is :attr:`waste_reagent`
        * the result of calling :func:`Mixture.find_or_compute`, passing in
          ``result`` (which is either a string or ``None``) as the ``name``
          parameter.

        The resulting :class:`Liquid` is :attr:`inexact` if either
        :class:`Liquid` is.

        After the operation, ``other`` will have the same :attr:`reagent` as
        this :class:`Liquid`, but its :attr:`volume` will be zero and it will
        not be :attr:`inexact`.

        Note:

            This method modifies both :class:`Liquid`\s.  To simply compute the
            result of such mixing and return it as a new :class:`Liquid` without
            modifying either, use :func:`mix_with`.

        Args:
            other:  the :class:`Liquid` to mix in
        Keyword Args:
            result: the resulting :class:`Reagent`, the name of the computed
                    :class:`Reagent`, or ``None`` (indicating that the name
                    should be computed)
        """
        my_v = self.volume
        my_r = self.reagent
        their_v = other.volume
        their_r = other.reagent

        v = my_v + their_v
        if isinstance(result, Reagent):
            r = result
        elif my_r is their_r or their_v == Volume.ZERO:
            r = my_r
        elif my_r is waste_reagent or their_r is waste_reagent:
            r = waste_reagent if result is None else Reagent.find(result)
        elif my_v == Volume.ZERO:
            r = their_r
        else:
            ratio = my_v.ratio(their_v)
            r = Mixture.find_or_compute(my_r, their_r, ratio=ratio, name=result)
        self.reagent = r
        self.inexact = self.inexact or other.inexact
        self.volume = v
        other.reagent = r
        other.inexact = False
        other.volume = Volume.ZERO

    def split_to(self, other: Liquid) -> None:
        """
        Split this :class:`Liquid` such that half of its :attr:`volume` is transfered to ``other``.

        Note:
            The incoming values of :attr:`reagent`, :attr:`volume`, and
            :attr:`inexact` are overwritten.  This method is designed to be used
            following :func:`mix_in`, which clears its argument :class:`Liquid`.

        Args:
            other: the :class:`Liquid` to mix in
        """

        other.reagent = self.reagent
        other.inexact = self.inexact
        v = self.volume/2
        self.volume = v
        other.volume = v

    def processed(self, step: Union[str, ProcessStep],
                  new_composition_function: Optional[Callable[[ChemicalComposition], ChemicalComposition]] = None) -> Liquid:
        """
        Alter this :attr:`reagent` to note a :class:`ProcessStep`.

        Args:
            step: the :class:`ProcessStep` applied or the name used to find or
                  create it.

            new_composition_function: an optional function to determine the new
                                      composition.
        Returns:
            this :class:`Liquid`
        See Also:
            :func:`Reagent.processed`
        """
        self.reagent = self.reagent.processed(step, new_composition_function)
        return self

    @classmethod
    def mix_together(cls, liquids: Sequence[Union[Liquid, tuple[Liquid, float]]], *,
                     result: Optional[MixResult] = None) -> Liquid:
        """
        A new :class:`Liquid` that is the result of mixing several :class:`Liquid`\s
        together.

        The ``liquids`` parameter specifies not only the :class:`Liquid`\s to
        use, but also the portion of the volume each to use.  (The default, if
        just the :class:`Liquid` is specified, is ``1``, repesenting that the
        whole volume is to be used.  This is useful when a given :class:`Liquid`
        is participating in more than one mixture at the same time.  By
        providing, e.g., ``0.5`` as the second element for each call to
        :func:`mix_together`, half the volume will be used in each.

        The :attr:`volume` of the result is the sum of the volumes used for each
        element of ``liquids``. The :attr:`reagent` of the result is

        * ``result``, if this is a :class:`Reagent`
        * the common :attr:`reagent`, if all :class:`Liquid`\s have the same
          :attr:`reagent`,
        * :attr:`waste_reagent`, if the :attr:`reagent` for any :class:`Liquid`
          is :attr:`waste_reagent`
        * the result of calling :func:`Mixture.find_or_compute`, passing in
          ``result`` (which is either a string or ``None``) as the ``name``
          parameter.

        The resulting :class:`Liquid` is :attr:`inexact` if any
        :class:`Liquid` is.

        This method does not modify any member of ``liquids``.

        If ``liquids`` is empty, the result will be a new :class:`Liquid` whose
        :attr:`reagent` is the :attr:`unknown_reagent` and whose :attr:`volume`
        is zero.

        Args:
            liquids:  the :class:`Liquid`\s to mix together.  These may be
                      specified alone or paired with a number indicating the
                      portion of the :class:`Liquid` to use
        Keyword Args:
            result: the resulting :class:`Reagent`, the name of the computed
                    :class:`Reagent`, or ``None`` (indicating that the name
                    should be computed)
        Returns:
            a new :class:`Liquid` with the resulting :class:`Reagent` and :class:`.Volume`.
        """
        if len(liquids) == 0:
            return Liquid(unknown_reagent, Volume.ZERO)
        ls = [(liquid, 1) if isinstance(liquid, Liquid) else liquid for liquid in liquids]
        first, first_frac = ls[0]
        v = first.volume*first_frac
        r = first.reagent
        last = len(ls)-2
        inexact = first.inexact
        for i, (liquid, frac) in enumerate(ls[1:]):
            v2 = liquid.volume * frac
            if v2 == Volume.ZERO:
                continue
            r2 = liquid.reagent
            if liquid.inexact:
                inexact = True
            if i == last and isinstance(result, Reagent):
                r = result
            elif r is r2:
                pass
            elif r is waste_reagent or r2 is waste_reagent:
                r = waste_reagent
            else:
                ratio = v.ratio(v2)
                result_name = result if i == last else None
                assert(not isinstance(result_name, Reagent))
                r = Mixture.find_or_compute(r, r2, ratio=ratio, name=result_name)
            v = v+v2
        return Liquid(r, v, inexact=inexact)




class XferDir(Enum):
    """
    An enumeration representing directions that :class:`Liquid` transfers can
    take.
    """
    FILL = auto()   #: Represents a transfer to add to a location
    EMPTY = auto()  #: Represents a transfer to remove from a location

class State(Generic[_T], ABC):
    """
    An object that encapsulates a value and a :class:`ChangeCallbackList` for
    that value.

    :class:`State` is an abstract class that is required to define
    :func:`realize_state`.  This has to do with the way :class:`State` was used
    in the initial system as a base class for proxies for physical devices that
    had to not only track state changes but be able to effect them in the real
    world.  If this is inapplicable, use the subclass :class:`DummyState`, which
    implements :func:`realize_state` to do nothing

    Args:
        _T: The value type
    """
    # _state: _T   #: The current value

    current_state: MonitoredProperty[_T] = MonitoredProperty()
    """
    The current value.  When this value is set to a value not equal to the prior
    value, callbacks registerd to :attr:`on_state_change` are called.
    """
    on_state_change: ChangeCallbackList[_T] = current_state.callback_list
    """
    The :class:`.ChangeCallbackList` monitoring :attr:`current_state`.
    """

    has_state: bool = current_state.value_check
    """
    Does :attr:`current_state` have a value?
    """

    def __init__(self, *, initial_state: MissingOr[_T]) -> None:
        """
        Initialize the object.  If ``initial_state`` is not :attr:`.MISSING`, it
        becomes the initial value of ``current_state``

        Keyword Args:
            initial_state: the initial value
        """
        if initial_state is not MISSING:
            self.current_state = initial_state
        "Callbacks invoked when :attr:`current_state` is set"

    @abstractmethod
    def realize_state(self, new_state: _T) -> None: # @UnusedVariable
        """
        Called to effectuate a new value.  Note that ``new_state`` is not
        necessarily :attr:`current_state`.

        Note:
            This is an abstract method.  There is no default implementation.  If
            you want a trivial default implementation, use :class:`DummyState`
            rather than :class:`State`.

        Args:
            new_state: the value to realize
        """
        ...


class DummyState(State[_T]):
    """
    A concrete subclass of :class:`State` that implements :func:`realize_state`
    to do nothing.

    Args:
        _T: The value type
    """
    def realize_state(self, new_state:_T)->None:
        """
        Do nothing.  Used when there is nothing to be done to realize the new state.

        Args:
            new_state: The (ignored) value tp realize
        """
    ...
