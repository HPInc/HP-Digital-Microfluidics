from __future__ import annotations
from quantities import dimensions
from typing import overload, Union, Final, ClassVar, Optional
from quantities.SI import deg_K

class TemperaturePoint:
    """
    An absolute temperature.  For temperature differences use :class:`.Temperature`.  
    
    :class:`TemperaturePoint`\s are most often created by multiplying a number
    and a :class:`Scale`, such as :attr:`abs_C`, :attr:`abs_K`, or
    :attr:`abs_F`, e.g., ::
    
        tp = 94.2*deg_C
        
    Note:
        :attr:`abs_K` is a :class:`Scale` for :class:`TemperaturePoint`\s.
        :attr:`SI.deg_K` is a :class:`.Unit`\[:class:`.Temperature`].

    If ``tp`` is a :class:`TemperaturePoint` and ``t`` is a :class:`.Temperature`, then ::
    
        tp2 = tp + t
        tp2 = t + tp
        tp2 = tp - t
        t = tp - tp2
        
    are all valid statements.
    
    :class:`TemperaturePoint`\s may be compared, regardless of the
    :class:`Scale`\s used to create them::
    
        if 25*abs_C < 60*abs_F:
            ...
            
    A :class:`TemperaturePoint` can be converted to a string (:func:`on_scale`)
    or a float (:func:`as_number`) by specifying :class:`Scale`.  If a
    :class:`TemperaturePoint` is converted to a string by using :func:`.str`,
    :func:`on_scale` is called using :attr:`default_scale`, which defaults to
    :attr:`deg_C`, but can be changed.
    
        
    """
    absolute: Final[dimensions.Temperature] #: The :class:`.Temperature` above :attr:`absolue_zero`
    
    default_scale: ClassVar[Scale] #: The default :class:`Scale` to use when converting :class:`TemperaturePoint`\s to strings.
    
    
    
    def __init__(self, absolute: dimensions.Temperature) -> None:
        """
        Initialize the object
        
        :class:`TemperaturePoint`\s are most often created by multiplying a
        number and a :class:`Scale`, e.g., ::
        
            tp = 94.2*deg_C
        
        Args:
            absolute: the :class:`.Temperature` above :attr:`absolute_zero`
        """
        self.absolute = absolute
        
    def __add__(self, rhs: dimensions.Temperature) -> TemperaturePoint:
        return TemperaturePoint(self.absolute+rhs)
    
    def __radd__(self, lhs: dimensions.Temperature) -> TemperaturePoint:
        return TemperaturePoint(lhs+self.absolute)

    @overload    
    def __sub__(self, rhs: TemperaturePoint) -> dimensions.Temperature: ...  # @UnusedVariable
    @overload
    def __sub__(self, rhs: dimensions.Temperature) -> TemperaturePoint: ...  # @UnusedVariable
    def __sub__(self, rhs: Union[TemperaturePoint, dimensions.Temperature]) -> Union[dimensions.Temperature,
                                                                                     TemperaturePoint]:
        if isinstance(rhs, TemperaturePoint):
            return self.absolute-rhs.absolute
        else:
            return TemperaturePoint(self.absolute-rhs)

    def __hash__(self) -> int:
        return hash(self.absolute)
    
    def __lt__(self, rhs: TemperaturePoint) -> bool:
        return self.absolute < rhs.absolute

    def __le__(self, rhs: TemperaturePoint) -> bool:
        return self.absolute <= rhs.absolute
    
    def as_number(self, scale: Scale) -> float:
        """
        The number of degrees on the given :class:`Scale`.
        
        Args:
            scale: the :class:`Scale` to use
        Returns:
            the number of degrees
        """
        return self.absolute.magnitude/scale.relative_to_kelvin+scale.absolute_zero
    
    def on_scale(self, scale: Scale, fmt_string: Optional[str] = None) -> str:
        """
        Format the :class:`TemperaturePoint` on the given :class:`Scale`.  If
        ``fmt_string`` is not specified, ``".2f"`` (format with two digits to
        the right of the decimal point) is used.
        
        Args:
            scale: the scale to use
        Keyword Args:
            fmt_string: an optional format to use to format the number
        Returns:
            the formatted string
        """
        if fmt_string is None:
            fmt_string = ".2f"
        n = format(self.as_number(scale), fmt_string)
        return f"{n} {scale.abbr}"
    
    def __repr__(self) -> str:
        return f"TemperaturePoint({self.absolute})"
    
    def __str__(self) -> str:
        return self.on_scale(TemperaturePoint.default_scale)
    
    
class Scale:
    """
    A unit to be used to specify a :class:`TemperaturePoint`.  
    
    To obtain a :class:`TemperaturePoint`, multiply a float by a :class:`Scale`,
    e.g., ::
    
        tp = 25*abs_C
    """
    absolute_zero: Final[float]         #: Absolute zero as a number in this unit
    relative_to_kelvin: Final[float]    #: The size of a degree relative to :attr:`.deg_K`
    abbr: Final[str]                    #: The unit abbreviation
    
    def __init__(self, abbr: str, 
                 absolute_zero: float,
                 relative_to_kelvin: float) -> None:
        """
        Initialize the object.
        
        Args:
            abbr: the unit abbreviation
            absolute_zero: absolute zero as a number in this unit
            relative_to_kelvin: the size of a degree relative to :attr:`.deg_K`
        """
        self.abbr = abbr
        self.absolute_zero = absolute_zero
        self.relative_to_kelvin = relative_to_kelvin
        
    def __rmul__(self, lhs: float) -> TemperaturePoint:
        return TemperaturePoint(((lhs-self.absolute_zero)*self.relative_to_kelvin)*deg_K)
        
abs_K = Scale('K', 0, 1)             #: :class:`TemperaturePoint` :class:`Scale` for the Kelvin scale
abs_C = Scale('°C', -273.15, 1)      #: :class:`TemperaturePoint` :class:`Scale` for the Celsius scale
abs_F = Scale('°F', -459.67, (5/9))  #: :class:`TemperaturePoint` :class:`Scale` for the Fahrenheit scale

absolute_zero: Final[TemperaturePoint] = 0*abs_K    #: Absolute zero as a :class:`TemperaturePoint`
    
TemperaturePoint.default_scale = abs_C  