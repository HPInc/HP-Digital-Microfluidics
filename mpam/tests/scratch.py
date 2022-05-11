from __future__ import annotations

import random
from typing import Generic, TypeVar, Optional, Callable, overload, Union, \
    Final

from mpam.types import ChangeCallbackList, monitored_property, MonitoredProperty,\
    MissingOr, MISSING

sn: int = 100
def next_sn() -> int:
    global sn
    val = sn
    sn += 1
    return val

class Bar:
    count = MonitoredProperty[int]("count",
                                    # default=0, 
                                    # default_fn = lambda _: next_sn(),
                                    ) #, init=0)
    on_count_change = count.callback_list
    has_count = count.value_check
    # @count.transform
    # def double(self, val: int) -> int:
        # return 2*val

    # @count.transform
    # def clip(self, val: int) -> int:
    #     return min(val, 10)
    
    @count.transform
    def enforce_range(self, val: int) -> MissingOr[int]:
        return MISSING if val > 10 else val
    
    
print("Hi")
bar = Bar()
print(bar.has_count)
bar.on_count_change(lambda old, new: print(f"{old} -> {new}"))
# print(bar.count)
bar.count = 5    
print(bar.count)
print(bar.has_count)
bar.count = 10
print(bar.count)
bar.count = 10
print(bar.count)
bar.count = 20
print(bar.count)
del bar.count
bar.count = 2
print(bar.count)
bar.count = 6
print(bar.count)
bar.count += 1
print(bar.count)
#
#
#
# T=TypeVar("T")
# OT = TypeVar("OT")
#
#
# class change_monitor(Generic[OT, T]):
#     _key: Final[str]
#
#     def __init__(self, fn: Callable[[OT], T]) -> None:
#         self._key = f"_{fn}_key_{random.random()}"
#         print(f"Key is {self._key}")
#
#     @overload
#     def __get__(self, obj: None, objtype: type[OT]) -> change_monitor[OT, T]: ... # @UnusedVariable
#     @overload
#     def __get__(self, obj: OT, objtype: type[OT]) -> ChangeCallbackList[T]: ... # @UnusedVariable
#     def __get__(self, obj: Optional[OT], 
#                 objtype: type[OT]) -> Union[ChangeCallbackList[T], change_monitor[OT, T]]: # @UnusedVariable
#         if obj is None:
#             return self
#         key = self._key
#         ccl = getattr(obj, key, None)
#         if ccl is None:
#             ccl = ChangeCallbackList[T]()
#             print(f"ccl for {obj} is {ccl}")
#             setattr(obj, key, ccl)
#         return ccl
#
# def monitored(monitor: change_monitor[OT, T]) -> Callable[[Callable[[T,T], None]],
#                                                           Callable[[T,T], None]]:
#     def decorator(setter: Callable[[T,T], None]) -> Callable[[T,T], None]:
#
#         ...
#     return decorator
#
# class Foo:
#     @change_monitor
#     def on_state_change(self) -> int: ...
#
#     _count: int = 0
#
#     @monitored_property
#     def count(self) -> int:
#         return self._count
#
#     @count.setter
#     def count(self, val: int) -> None:
#         self._count = val
#
#     @count.callbacks
#     def on_count_change(self) -> int: ...
#
#
# # cc = ChangeCallbackList[str]()
# # cc(lambda n: print(n))
# # cc.add(lambda n: print(n))
#
# foo = Foo()
# # reveal_type(foo.on_state_change)
# foo.on_state_change.add(lambda old, n: print(n))
# # foo.on_state_change = ChangeCallbackList[int]()
# foo.on_state_change(lambda old, n: print(n))
# f2 = Foo()
# f2.on_state_change(lambda old, new: None)
#
# print(foo.count)
# # reveal_type(foo.on_count_change)
# foo.on_count_change(lambda old, new: print(f"{old} -> {new}"), key="hi")
# foo.count = 3
# print(foo.count)
# # foo.on_count_change.remove("hi")
# foo.count = 5
# print(foo.count)
#
#
# # class our_property(Generic[OT, T]):
# #     """ emulation of the property class 
# #         for educational purposes """
# #
# #     inner: int = 2
# #
# #     def __init__(self, 
# #                  fget: Optional[Callable[[OT], T]]= None, 
# #                  fset: Optional[Callable[[OT, T], None]] = None, 
# #                  fdel: Optional[Callable[[OT], None]] = None, 
# #                  doc=None):
# #         """Attributes of 'our_decorator'
# #         fget
# #             function to be used for getting 
# #             an attribute value
# #         fset
# #             function to be used for setting 
# #             an attribute value
# #         fdel
# #             function to be used for deleting 
# #             an attribute
# #         doc
# #             the docstring
# #         """
# #         self.fget = fget
# #         self.fset = fset
# #         self.fdel = fdel
# #         if doc is None and fget is not None:
# #             doc = fget.__doc__
# #         self.__doc__ = doc
# #
# #     @overload
# #     def __get__(self, obj: None, objtype: type[OT]) -> our_property[OT, T]: ...
# #     @overload
# #     def __get__(self, obj: OT, objtype: type[OT]) -> T: ...
# #     def __get__(self, obj: Optional[OT], objtype: type[OT]) -> Union[T, our_property[OT, T]]:
# #         if obj is None:
# #             return self  
# #         if self.fget is None:
# #             raise AttributeError("unreadable attribute")
# #         return self.fget(obj)
# #
# #     def __set__(self, obj, value):
# #         if self.fset is None:
# #             raise AttributeError("can't set attribute")
# #         self.fset(obj, value)
# #
# #     def __delete__(self, obj):
# #         if self.fdel is None:
# #             raise AttributeError("can't delete attribute")
# #         self.fdel(obj)
# #
# #     def getter(self, fget: Callable[[OT], T]) -> our_property[OT, T]:
# #         return type(self)(fget, self.fset, self.fdel, self.__doc__)
# #
# #     def setter(self, fset: Callable[[OT, T], None]) -> our_property[OT, T]:
# #         return type(self)(self.fget, fset, self.fdel, self.__doc__)
# #
# #     def deleter(self, fdel: Callable[[OT], None]) -> our_property[OT, T]:
# #         return type(self)(self.fget, self.fset, fdel, self.__doc__)
# #
# # class Test:
# #     @our_property
# #     def foo(self) -> int:
# #         return 1
# #
# # test = Test()
# # print(type(test.foo))
# # reveal_type(test.foo)
# #
# # print(test.foo.inner)