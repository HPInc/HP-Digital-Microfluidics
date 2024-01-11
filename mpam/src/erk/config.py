from __future__ import annotations

from argparse import Namespace, _ActionsContainer, ArgumentTypeError, \
    BooleanOptionalAction, ArgumentParser
import argparse
from enum import Enum, auto
from functools import cached_property
import itertools
import logging
from typing import Mapping, Any, Optional, Union, TypeVar, \
    Callable, Generic, Final, cast, Sequence, overload, Iterator, Iterable, \
    Literal, Type, NoReturn

from .stringutils import conj_str


logger = logging.getLogger(__name__)

T = TypeVar("T")
Default = TypeVar("Default")

class Unset(Enum):
    SINGLETON = auto()
    def __repr__(self) -> str:
        return "UNSET"
    
    # All Missing values (i.e., MISSING) are considered False
    def __bool__(self) -> bool:
        return False
    

UNSET: Final[Unset] = Unset.SINGLETON

class _TemporaryOverride:
    old_val: Optional[CPBindings]
    expect: CPBindings
    
    def __init__(self, overrides: CPBindings) -> None:
        current = ConfigParam._temp_overrides
        self.old_val = current
        if current is None:
            new_val = overrides
        else:
            new_val = current.but(overrides)
        self.expect = new_val
        ConfigParam._temp_overrides = new_val
        
    def close(self) -> None:
        if ConfigParam._temp_overrides is self.expect:
            ConfigParam._temp_overrides = self.old_val
        else:
            logger.warning(f"Exiting temporary ConfigParam bindings out of order.  Expected {self.expect}, found {ConfigParam._temp_overrides}.")
        
class CPBindings:
    _overrides: Final[dict[ConfigParam,Any]]
    _use_stack: Optional[list[_TemporaryOverride]] = None
    
    _Addable = Union['CPBindings', Iterable['CPBindings']]
    
    @overload
    def __init__(self, cp: ConfigParam[T], value: T) -> None: ... # @UnusedVariable
    @overload
    def __init__(self, first: _Addable, *rest: _Addable) -> None: ... # @UnusedVariable
    @overload
    def __init__(self) -> None: ...
    def __init__(self, *args) -> None: #type: ignore
        self._overrides = {}
        if len(args) > 0:
            self.update(*args)
                    

    @overload
    def update(self, cp: ConfigParam[T], value: T) -> None: ... # @UnusedVariable
    @overload
    def update(self, first: _Addable, *rest: _Addable) -> None: ... # @UnusedVariable
    def update(self, first: Union[ConfigParam[T], _Addable], # type: ignore[misc]
               second: Optional[Union[T, _Addable]] = None,
               *rest: _Addable) -> None: 
        if isinstance(first, ConfigParam):
            assert second is not None
            self[first] = second   #type: ignore[misc]
        else:
            def process(a: CPBindings._Addable) -> None:
                if isinstance(a, CPBindings):
                    self._overrides.update(a._overrides)
                else:
                    for a2 in a:
                        process(a2)
            process(first)
            if second is not None:
                process(cast(CPBindings._Addable, second))
            for a in rest:
                process(a)
                

    
    @overload
    def but(self, cp: ConfigParam[T], value: T) -> CPBindings: ... # @UnusedVariable
    @overload
    def but(self, first: _Addable, *rest: _Addable) -> CPBindings: ... # @UnusedVariable
    def but(self, *args) -> CPBindings: #type: ignore
        if len(args) == 2 and isinstance(args[0], ConfigParam):
            cp, val = args
            args = (cp >> val,)
        return CPBindings(self, *args)

    @overload        
    def get(self, cp: ConfigParam[T], default: Unset = UNSET) -> T: ... # @UnusedVariable
    @overload
    def get(self, cp: ConfigParam[T], default: Default) -> Union[T, Default]: ... # @UnusedVariable
    def get(self, cp: ConfigParam[T], default: Union[Unset, Default] = UNSET) -> Union[T,Default]:
        val: Union[T, Default] = self._overrides.get(cp, default)
        if val is UNSET:
            raise KeyError(f"No value for {cp.full_name}")
        return val

    def __getitem__(self, cp: ConfigParam[T]) -> T:
        return self.get(cp)
    
    def __setitem__(self, cp: ConfigParam[T], val: T) -> None:
        self._overrides[cp] = val
        
    def __delitem__(self, cp: ConfigParam[T]) -> None:
        del self._overrides[cp]
        
    def __len__(self) -> int:
        return len(self._overrides)
    
    def __contains__(self, cp: ConfigParam[T]) -> bool:
        return cp in self._overrides
    
    def __iter__(self) -> Iterator[ConfigParam]:
        return self._overrides.__iter__()
    
    def copy(self) -> CPBindings:
        cpo = CPBindings()
        cpo._overrides.update(self._overrides)
        return cpo
    
    def plus(self, cp: ConfigParam[T], val: T) -> CPBindings:
        self._overrides[cp] = val
        return self
    
    def __enter__(self) -> CPBindings:
        if self._use_stack is None:
            self._use_stack = []
        self._use_stack.append(_TemporaryOverride(self))
        return self
    
    def __exit__(self, _exc_type: Any, _exc_val: Any, _exc_tb: Any) -> Literal[False]:
        if not self._use_stack:
            logger.error("Exiting CPBindings that wasn't entered")
        else:
            self._use_stack.pop().close()
        return False
            
    
    def __and__(self, other: CPBindings._Addable) -> CPBindings:
        return CPBindings(self, other)
    
    
NO_OVERRIDES: Final = CPBindings()

class DeprecatedAction(argparse.Action):
    def __init__(self, *args: Any,
                 original_action_class: Type[argparse.Action],
                 warning_message: str, **kwargs: Any) -> None:
        self.warning_message = warning_message
        self.original_action = original_action_class(*args, **kwargs)
        kwargs.update(self.original_action._get_kwargs())

        super().__init__(*args, **kwargs)

    def __call__(self, parser: ArgumentParser, namespace: Namespace,
                 values: Any, option_string: Optional[str] = None) -> None:
        # def __call__(self, *args: Any, **kwargs: Any) -> None:
        where = option_string or "<UNKNOWN ARGUMENT>"
        logger.warning(f"ARGUMENT '{where}' {self.warning_message}")
        self.original_action(parser, namespace, values, option_string)


class ConfigParam(Generic[T]):
    _namespace: Optional[Namespace] = None
    _default_val: Union[Unset, T] = UNSET
    _transform: Optional[Callable[[Any], T]] = None
    _name_counter: Final = itertools.count()
    _name: Optional[str] = None
    _nested_name: Optional[str] = None
    _full_name: Optional[str] = None
    
    _key: Optional[str] = None
    _namespace_value: Union[Unset, T] = UNSET
    _overridden: Optional[tuple[CPBindings, T]] = None
    
    _temp_overrides: Optional[CPBindings] = None
    
    @staticmethod
    def _default_no_default_action(cp: ConfigParam) -> NoReturn:
        raise AttributeError(f"{cp.full_name} has no value")
        
    _on_no_default: Callable[[ConfigParam], NoReturn] = _default_no_default_action
    

    def __init__(self, default_val: Union[Unset, T] = UNSET, *,
                 name: Optional[str] = None):
        self._default_val = default_val
        self._name = name
        
    def __repr__(self) -> str:
        v = "<UNSET>"
        try:
            v = str(self.value)
        except AttributeError:
            pass
        return f"ConfigParam[{self.full_name}={v}]" 
        
    @property
    def default(self) -> T:
        if self._default_val is not UNSET:
            return self._default_val
        raise AttributeError(f"{self.full_name} has no default value")
    
    @default.setter
    def default(self, val: T) -> None:
        self._default_val = val
        
    @property
    def has_default(self) -> bool:
        return self._default_val is not UNSET
        
    @cached_property
    def name(self) -> str:
        if self._name is None:
            self._name = f"ConfigParam_{next(self._name_counter)}"
        return self._name
    
    @cached_property
    def nested_name(self) -> str:
        return self._nested_name or self.name

    @cached_property
    def full_name(self) -> str:
        return self._full_name or self.name
    
    @property
    def has_value(self) -> bool:
        try:
            self.value
            return True
        except AttributeError:
            return False


    @property
    def value(self) -> T:
        to = self._temp_overrides
        v: Union[T, Unset]
        if (to is not None
            and (o:=self._overridden) is not None
            and o[0] is to):
            return o[1]
        if to is not None:
            try:
                v = to[self]
                self._overridden = (to, v)
                return v
            except KeyError:
                pass
        v = self._namespace_value
        if v is UNSET:
            v = self._establish_value()
            self._namespace_value = v
        if to is not None:
            self._overridden = (to, v)
        return v
    
    @value.setter
    def value(self, val: T) -> None:
        self._namespace_value = val
        if self._temp_overrides is not None:
            self._overridden = (self._temp_overrides, val)

    def _establish_value(self) -> T:
        if self._temp_overrides is not None:
            try:
                v = self._temp_overrides[self]
                return v
            except KeyError:
                pass
        if self._key and self._namespace:
            key = self._key
            from_namespace = getattr(self._namespace, key, UNSET)
            if from_namespace is not UNSET: 
                if self._transform:
                    return self._transform(from_namespace)
                else:
                    # If it's there and we don't have a transform, we have to
                    # assume that what's there is what we need.
                    return cast(T, from_namespace)
        if self._default_val is not UNSET:
            return self._default_val
        handler = self._on_no_default
        handler(self)
        
    def on_no_default(self, fn: Callable[[ConfigParam], Any]) -> None:
        old_fn = self._on_no_default
        def composed(cp: ConfigParam) -> NoReturn:
            fn(cp)
            old_fn(cp)
        self._on_no_default = composed
        
    def raise_on_no_default(self, factory: Callable[[ConfigParam], Exception]) -> None:
        def raise_ex(cp: ConfigParam) -> NoReturn:
            ex = factory(cp)
            raise ex
        self.on_no_default(raise_ex)
        
    def __call__(self, val: Union[T, Unset, CPBindings] = UNSET) -> T:
        if val is UNSET:
            pass
        elif isinstance(val, CPBindings):
            if self in val:
                return val[self]
        else:
            self.value = val
        return self.value
    
    def __set_name__(self, owner: Any, name: str) -> None:
        self._name = name
        self._nested_name = f"{owner.__name__}.{name}"
        self._full_name = f"{owner.__module__}.{owner.__qualname__}.{name}"
        # logger.warning(f"Calling __set_name__() on {self._full_name}: {self._namespace_value}/{self._default_val}")
        

    # @overload
    # @classmethod
    # def temporary(cls, cp: ConfigParam[T], value: T) -> _TemporaryOverride: ... # @UnusedVariable
    # @overload
    # @classmethod
    # def temporary(cls, first: CPBindings._Addable, *rest: CPBindings._Addable) -> _TemporaryOverride: ... # @UnusedVariable
    # @classmethod #type: ignore
    # def temporary(cls, *args) -> _TemporaryOverride:
    #     if len(args) == 2 and isinstance(args[0], ConfigParam):
    #         cp, val = args
    #         args = (cp >> val,)
    #     new = CPBindings(*args)
    #     return _TemporaryOverride(new)
    
    def __rshift__(self, val: T) -> CPBindings:
        return CPBindings(self, val)


    
    # def __get__(self, _instance: Any, _owner: Any) -> T:
    #     return self.value

    # def __getattr__(self, name: str) -> Any:
    #     return getattr(self.value, name)
    
    @staticmethod
    def add_to_help(kwargs: dict[str, Any], s: str) -> None:
        if 'help' in kwargs:
            kwargs['help'] += f" {s}"
        else:
            kwargs['help'] = s

    @staticmethod            
    def use_instead(arg: str) -> str:
        return f"Use '{arg}' instead."
            
    class NoDefaultBooleanOptionalAction(BooleanOptionalAction):
        """
        A class that's only needed because BooleanOptionalAction insists
        on adding (default: True/False) to its help string.
        """
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            prefix = ' (default: '
            suffix = ')'
            s = self.help
            if s is not None and s.endswith(suffix) and prefix in s:
                start = s.rfind(prefix)
                self.help = s[:start]

    def add_arg_to(self, parser: _ActionsContainer, name: str, *args: str,
                   transform: Optional[Callable[[Any], T]] = None, 
                   default: Union[Unset, Any] = UNSET,
                   to_default: Optional[Callable[[T], Union[Any, Unset]]] = None,
                   default_desc: Optional[Union[str, Callable[[T], str]]] = None,
                   deprecated: Union[bool, str] = False,
                   ignored: bool = False,
                   **kwargs: Any) -> None:
        def desc_from_default(v: Any) -> str:
            if isinstance(v, str):
                return f"'{v}'"
            return str(v)
                    
        if default is not UNSET:
            assert default_desc is None or isinstance(default_desc, str)
            if default_desc is None:
                default_desc = desc_from_default(default)
        else:
            dv = self._default_val
            if dv is not UNSET:
                if to_default is not None:
                    default = to_default(dv)
                else:
                    default = dv
                if default_desc is None:
                    default_desc = desc_from_default(default)
                elif not isinstance(default_desc, str):
                    default_desc = default_desc(dv)
        if default is not UNSET:
            if isinstance(default_desc, str):
                self.add_to_help(kwargs, f"The default value is {default_desc}.")
                # kwargs['default'] = default
                
            
        # If the action is BooleanOptionalAction, we replace it with our own
        # subclass so that the default value doesn't wind up int he help string
        # twice.
        
        if kwargs.get('action', None) is BooleanOptionalAction:
            kwargs['action'] = self.NoDefaultBooleanOptionalAction
            
        if deprecated or ignored:
            warning = ""
            if deprecated:
                warning += " IS DEPRECATED"
            if ignored:
                if deprecated:
                    warning += " AND"
                warning += " WILL BE IGNORED"
            warning += "."
            if isinstance(deprecated, str):
                warning += f" {deprecated}"
            self.add_to_help(kwargs, "THIS ARGUMENT"+warning)
                
            old_action = kwargs.pop('action', argparse._StoreAction)
            if isinstance(old_action, str):
                old_action = parser._registries['action'][old_action]
            kwargs['warning_message'] = warning
            kwargs['original_action_class'] = old_action
            kwargs['action'] = DeprecatedAction
            
        # We need to make sure that the help string doesn't have a percent sign.
        help_str: Optional[str] = kwargs.get('help')
        if help_str is not None and '%' in help_str:
            kwargs['help'] = help_str.replace(r"%", r"%%")
            
        action = parser.add_argument(name, *args, default=default, **kwargs)
        self._key = None if ignored else action.dest
        if transform is not None:
            self._transform = transform

    
    def add_kwd_args_to(self, parser: _ActionsContainer, kwds: Mapping[str, T], *, 
                        dest: Optional[str] = None, 
                        **kwargs: Any) -> None:
        if dest is None:
            dest = self.name
        group = parser.add_mutually_exclusive_group()
        help_val: Optional[Union[str, Callable[[str, T], str]]] = kwargs.get('help', None)
        for k, v in kwds.items():
            if help_val is not None and not isinstance(help_val, str):
                kwargs['help'] = help_val(k,v)
            group.add_argument(f"--{k}", action='store_const', const=v, dest=dest, **kwargs)
        self._key = dest
        
    def add_bool_arg_to(self, parser: _ActionsContainer, name: str, *args: Any, **kwargs: Any) -> None:
        self.add_arg_to(parser, name, *args, action=BooleanOptionalAction, **kwargs)
        
        
    def add_choice_arg_to(self, parser: _ActionsContainer, 
                          options: Union[Mapping[str, T], 
                                         type[T], 
                                         tuple[type[T], Mapping[str, T]]],
                          name: str, *args: str, 
                          **kwargs: Any) -> None:
        def to_mapping(etype: type[T], extras: Mapping[str, T]) -> Mapping[str, T]:
            assert issubclass(etype, Enum), f"{etype} not an enum type"
            m = {k:v for k,v in extras.items()}
            seen: dict[str, Union[T, Unset]] = {k: v for k,v in m.items()}

            def check(s: str, val: T) -> None:
                old = seen.get(s)
                if old is None or old is val:
                    seen[s] = val
                else:
                    seen[s] = UNSET
                    
            for name,val in etype.__members__.items():
                v = cast(T, val)
                check(name, v)
                check(name.upper(), v)
                check(name.lower(), v)
            
            result = {k:v for k,v in seen.items() if v is not UNSET}
            return result
        
        
            
        if isinstance(options, type): 
            options = to_mapping(options, {})
        elif isinstance(options, tuple):
            options = to_mapping(*options)
        else:
            options = {k:v for k,v in options.items()}
        option_desc = conj_str(sorted(f"'{k}'" for k in options.keys()))
        def not_an_option(prefix: str, suffix: Optional[str] = None) -> str:
            if suffix is None:
                suffix = "."
            else:
                suffix = f", {suffix}."
            msg = f"{prefix} for {self.full_name} not one of {option_desc}{suffix}."
            logger.error(msg)
            return msg
        self.add_to_help(kwargs, f"Choices are {option_desc}.")
        choices: Sequence[str]
        if 'choices' in kwargs:
            choices = kwargs['choices']
            for c in choices:
                if c not in options:
                    not_an_option(f"Argument option {c}")
        else:
            choices = sorted(options.keys())
            kwargs['choices'] = choices
            
        opts = options
        def to_default(dv: T) -> Union[Unset, str]:
            for k,v in opts.items():
                if v == dv:
                    return k
            not_an_option(f"Default value for {self.full_name} [{dv}]", "ignoring")
            return UNSET
        def transform(v: Any) -> T:
            if not v in  opts:
                raise ArgumentTypeError(not_an_option(f"Argument {c} for {self.full_name}"))
            return opts[v]
        self.add_arg_to(parser, name, *args,
                        to_default=to_default, 
                        transform=transform, **kwargs)

    @classmethod
    def set_namespace(cls, namespace: Namespace) -> None:
        cls._namespace = namespace
        

if __name__ == '__main__':
    class TestConfig:
        int_cp = ConfigParam(5)     
        
    print(TestConfig.int_cp())
    with TestConfig.int_cp >> 7:
        print(TestConfig.int_cp())
    print(TestConfig.int_cp())
        
