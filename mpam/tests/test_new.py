from typing import TypeVar, Type, ClassVar, Union
class Base: 
    name: ClassVar[str]

TT = TypeVar('TT', bound = Base)

def with_name(name:str):
    def decorator(cls: Type[TT]):
        cls.name = name
        return cls
    return decorator

def named(name_or_class: Union[Type[TT], str]):
    if isinstance(name_or_class, str):
        return with_name(name_or_class)
    else:
        return with_name(name_or_class.__name__)(name_or_class)
    
class Middle(Base):
    test: str = "Hi"     
    
def insert_middle(cls: Type[TT]):
    cls.__bases__ = (Middle,)
    return cls

@named("a")
@insert_middle
class A(Base):
    ...
    
@named
class B(Base):
    ...
    
print(A.name)
print(B.name)
print(A.__bases__)

class CMeta(type):
    def __init__(cls, name, bases, dct):
        cls.foo=7
#        c = super().__new__(cls, name, bases, dct)
#        c.foo = 5
#        return c
    
class C(metaclass=CMeta):
    foo: ClassVar[int]
    
c = C()
print(c.foo)
        