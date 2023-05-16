from __future__ import annotations
from typing import Generic, TypeVar, Optional, Final, Callable, overload, Union
import random
from threading import Lock
from mpam.types import MISSING, MissingOr

Obj_ = TypeVar("Obj_")
T_ = TypeVar("T_")

class final_cached_property(Generic[Obj_, T_]):
    _name: Optional[str] = None
    _val_attr: Optional[str] = None
    _lock: Final[Lock]
    
    @property
    def name(self) -> str:
        n = self._name
        if n is None:
            with self._lock:
                n = self._name
                if n is None:
                    n = f"final_cached_{random.randrange(1000000)}"
            self._name = n
        return n
    
    @property
    def val_attr(self) -> str:
        attr = self._val_attr
        if attr is None:
            attr = f"_{self.name}__value"
            self._val_attr = attr
        return attr
    
    def __init__(self, func: Callable[[Obj_], T_]) -> None:
        self.func = func
        self.__doc__ = func.__doc__
        self._lock = Lock()
        
    def __set_name__(self, _owner: object, name: str) -> None:
        if self._name is None:
            self._name = name
        elif name != self._name:
            raise TypeError(f"Cannot call __set__name('{name}').  Already named '{self._name}'.")
    
    @overload
    def __get__(self, instance: None, owner: object) -> final_cached_property[Obj_, T_]: ... # @UnusedVariable
    @overload
    def __get__(self, instance: Obj_, owner: object) -> T_: ... # @UnusedVariable
    
    def __get__(self, instance: Optional[Obj_], owner: object=None) -> Union[T_, final_cached_property[Obj_,T_]]: # @UnusedVariable
        if instance is None:
            return self
        attr_name = self.val_attr
        if attr_name is None:
            raise(TypeError(f"Cannot use final_cached_property without calling __set_name__ on it"))
        try:
            cache = instance.__dict__
        except AttributeError:
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to cache {self._name!r} property."
            )
            raise TypeError(msg) from None
        val: MissingOr[T_] = cache.get(attr_name, MISSING)
        if val is MISSING:
            with self._lock:
                val = cache.get(attr_name, MISSING)
                if val is MISSING:
                    val = self.func(instance)
                    try:
                        cache[attr_name] = val
                    except:
                        msg = (
                            f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                            f"does not support item assignment for caching {attr_name!r} property."
                        )
                        raise TypeError(msg) from None
        return val

# @overload
# def locally_cached(arg: str) -> Callable[[Callable[[Obj_], T_]], Callable[[Obj_], T_]] : ...
# @overload
# def locally_cached(arg: Callable[[Obj_], T_]) -> Callable[[Obj_], T_] : ...
# def locally_cached(arg: Union[str, Callable[[Obj_], T_]]
#                               ) -> Union[Callable[[Obj_], T_],
#                                          Callable[[Callable[[Obj_], T_]], Callable[[Obj_], T_]]]:
#     ...  

