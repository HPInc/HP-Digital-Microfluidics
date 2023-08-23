from __future__ import annotations
from typing import TypeVar, Optional, Callable,\
    Union, cast, Any, ClassVar
from inspect import signature
from functools import cached_property
import random
from _collections import defaultdict


# Tca_ = TypeVar('Tca_', contravariant=True)
# F_ = TypeVar('F_', bound = 'Formatter', contravariant=True)
#
# class FormatFunction(Protocol[Tca_, F_]):
#     def __call__(self, obj: Tca_,
#                  formatter: F_,
#                 **options: Any 
#                  ) -> str:
#         ...


Tca_ = TypeVar('Tca_')
F_ = TypeVar('F_', bound='Formatter')

FormatFunction = Callable[[Tca_, F_], str]
RegisterableFormatFunction = Union[Callable[[Tca_, F_], str],
                                   Callable[[Tca_], str]]

# When we do the `getattr`, what we get is a wrapped version
# with the first argument bound
BoundFormatFunction = Callable[[F_], str]

class _ImmutableProxy: ...

class Formatter:
    @cached_property
    def name(self) -> str:
        return f"formatter_{random.randrange(1000000)}"
    
    @cached_property
    def _attr(self) -> str:
        return f"_{self.name}__format_fn"
    
    def __init__(self, *, name: Optional[str] = None,
                 attr: Optional[str] = None) -> None:
        if name is not None:
            self.name = name
        if attr is not None:
            self._attr = attr
            
    def __repr__(self) -> str:
        return f"<Formatter {self.name}>"
    
    default_formatter: ClassVar[Formatter]
    
    def get_unbound_func(self: F_, val: Tca_, attr: str) -> Optional[FormatFunction[Tca_, F_]]:
        for cls in type(val).mro():
            d = self._mutable(cls).__dict__
            if attr in d:
                fn: FormatFunction[Tca_, F_] = d[attr]
                return fn
        return None
    
    
    def format_function_for(self: F_, val: Tca_) -> Optional[FormatFunction[Tca_, F_]]:
        fn = self.get_unbound_func(val, self._attr)
        return fn
    
    def format(self: F_, val: Tca_, **options: Any) -> str:
        fn = self.format_function_for(val)
        if fn is not None:
            return fn(val, self, **options)
        return str(val)
    
    # For some reason, if the only use of Any is as the type annoatation for
    # **options parameters, PyDev complains about an unused import
    __need_any: Any
            
    
    def wrap_if_necessary(self: F_,
                          fn: RegisterableFormatFunction[Tca_, F_],
                          formatter_type: type[F_]
                          ) -> Callable[[Tca_, F_], str]:
    
        sig = signature(fn)
        params = list(sig.parameters.values())[1:]  # skip the first parameter (obj)
        
        takes_formatter = any(p.annotation == formatter_type for p in params)        
        takes_options = any(p.kind == p.VAR_KEYWORD for p in params)
    
        # Handle the different cases based on the presence of formatter and options
        if takes_formatter and takes_options:
            return cast(Callable[[Tca_, F_], str], fn)
        elif takes_formatter and not takes_options:
            def wrapper(val: Tca_, formatter: F_, **options: Any) -> str:
                accepted_options = {k: v for k, v in options.items() if k in sig.parameters}
                return cast(Callable[[Tca_, F_], str], fn)(val, formatter, **accepted_options)
            return wrapper
        elif not takes_formatter and takes_options:
            def wrapper(val: Tca_, formatter: F_, **options: Any) -> str: # @UnusedVariable
                return cast(Callable[[Tca_], str], fn)(val, **options)
            return wrapper
        else:
            def wrapper(val: Tca_, formatter: F_, **options: Any) -> str: # @UnusedVariable
                accepted_options = {k: v for k, v in options.items() if k in sig.parameters}
                return cast(Callable[[Tca_], str], fn)(val, **accepted_options)
            return wrapper    
    
    _immutable_proxy = defaultdict[type, _ImmutableProxy](_ImmutableProxy)
    
    def _mutable(self, cls: type[Tca_]) -> object:
        if cls in self._immutable_proxy:
            return self._immutable_proxy[cls]
        else:
            return cls
    
    def _add_to_class(self, cls: type[Tca_], 
                      fn: FormatFunction[Tca_, F_],
                      attr: str
                      ) -> None:
        try:
            setattr(cls, attr, fn)
        except TypeError:
            proxy = self._immutable_proxy[cls]
            setattr(proxy, attr, fn)
    
    def register_formatter(self: F_, cls: type[Tca_], 
                           fn: RegisterableFormatFunction[Tca_, F_],
                           ) -> None:
        wrapped_fn = self.wrap_if_necessary(fn, type(self))
        self._add_to_class(cls, wrapped_fn, self._attr)
        
    
Formatter.default_formatter = Formatter(name="default")