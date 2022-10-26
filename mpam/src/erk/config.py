from __future__ import annotations

from argparse import Namespace
from enum import Enum, auto
from typing import Final, Mapping, Any, Optional, overload, Union, TypeVar,\
    Callable
import typing


T = TypeVar("T")
V = TypeVar("V")

class Unset(Enum):
    SINGLETON = auto()
UNSET: Final[Unset] = Unset.SINGLETON

class RunConfig:
    _defaults: Final[Mapping[str, Any]]
    _cmd_line: Final[Namespace]
    _overrides: Final[Mapping[str, Any]]
    _extra_defaults: Final[Mapping[str, Any]]
    
    def __init__(self, *,
                 defaults: Optional[Mapping[str, Any]] = None,
                 cmd_line: Optional[Namespace] = None,
                 extra_defaults: Optional[Mapping[str, Any]] = None,
                 overrides: Optional[Mapping[str, Any]] = None) -> None:
        self._defaults = defaults or {}
        self._cmd_line = cmd_line or Namespace()
        self._overrides = overrides or {}
        self._extra_defaults = extra_defaults or {}
        
    def __getattr__(self, name: str) -> Any:
        val = self._overrides.get(name, UNSET)
        if val is not UNSET:
            return val
        val = getattr(self._cmd_line, name, UNSET)
        if val is not UNSET:
            return val
        val = self._extra_defaults.get(name, UNSET)
        if val is not UNSET:
            return val
        val = self._defaults.get(name, UNSET)
        if val is not UNSET:
            return val
        raise AttributeError(name)
    
    def but(self, *, defaults: Optional[Mapping[str, Any]] = None, **overrides: Mapping[str, Any]) -> RunConfig:
        def extend(mine: Mapping[str, Any], theirs: Optional[Mapping[str, Any]]) -> Mapping[str, Any]:
            if theirs is None or len(theirs) == 0:
                return mine
            m = {k: v for k,v in mine.items()}
            for k,v in theirs.items():
                m[k] = v
            return m 
        return RunConfig(defaults = self._defaults,
                         cmd_line = self._cmd_line,
                         extra_defaults = extend(self._extra_defaults, defaults),
                         overrides = extend(self._overrides, overrides))
    
    @overload
    def get(self, name: str, default: Unset = UNSET, *, expect: typing.Type[T]) -> T: ... # @UnusedVariable
    @overload
    def get(self, name: str, default: V, *, expect: typing.Type[T]) -> Union[V, T]: ... # @UnusedVariable
    @overload
    def get(self, name: str, default: V) -> Any: ... # @UnusedVariable
    @overload
    def get(self, name: str) -> Any: ... # @UnusedVariable
    def get(self, name: str, default: Any = UNSET, *, expect: Optional[typing.Type[T]] = None) -> Any:
        try:
            val = self.__getattr__(name)
            if expect is None or isinstance(val, expect):
                return val
            raise TypeError(f"Attribute {name} wrong type.  Expected {expect}, got value {val}")
        except AttributeError:
            if default is not UNSET:
                return default
            raise
         
    
    _cached_defaults: dict[type, Mapping[str, Any]] = {}
    
    @classmethod
    def defaults_for(cls, t: type[T]) -> Mapping[str, Any]:
        cd = cls._cached_defaults
        val = cd.get(t, None)
        if val is None:
            fn: Callable[[], Mapping[str, Any]]  = getattr(t, "config_defaults", lambda: {})
            val = fn()
            cd[t] = val
        return val
    
    @classmethod
    def for_class(cls, t: type[T], cmd_line: Namespace) -> RunConfig:
        return RunConfig(defaults=cls.defaults_for(t), cmd_line=cmd_line)