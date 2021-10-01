from __future__ import annotations

from _collections import defaultdict
from enum import Enum, auto
from typing import Final, Optional, Sequence, NamedTuple, ClassVar, Callable, \
    Any, Mapping


class Type:
    name: Final[str]
    direct_supers: Final[Sequence[Type]]
    all_supers: Final[Sequence[Type]]
    direct_subs: Final[list[Type]]
    all_subs: Final[list[Type]]
    _maybe: Optional[MaybeType] = None
    
    @property
    def maybe(self) -> MaybeType:
        mt = self._maybe
        if mt is None:
            mt = self._maybe = MaybeType(self)
        return mt
    
    ANY: ClassVar[Type]
    NONE: ClassVar[Type]
    IGNORE: ClassVar[Type]
    ERROR: ClassVar[Type]
    NUMBER: ClassVar[Type]
    INT: ClassVar[Type]
    FLOAT: ClassVar[Type]
    BINARY_STATE: ClassVar[Type]
    WELL: ClassVar[Type]
    BINARY_CPT: ClassVar[Type]
    PAD: ClassVar[Type]
    WELL_PAD: ClassVar[Type]
    DROP: ClassVar[Type]
    ORIENTED_DROP: ClassVar[Type]
    DIR: ClassVar[Type]
    ORIENTED_DIR: ClassVar[Type]
    MOTION: ClassVar[MotionType]
    DELTA: ClassVar[Type]
    TWIDDLE_OP: ClassVar[TwiddleOpType]
    PAUSE: ClassVar[PauseType]
    ROW: ClassVar[Type]
    COLUMN: ClassVar[Type]
    BARRIER: ClassVar[Type]
    DELAY: ClassVar[Type]
    TIME: ClassVar[Type]
    TICKS: ClassVar[Type]
    BOOL: ClassVar[Type]
    VOLUME: ClassVar[Type]
    
    def __init__(self, name: str, supers: Optional[Sequence[Type]] = None, *, 
                 is_root: bool = False):
        self.name = name
        if supers is None:
            supers = [] if is_root else  [Type.ANY]
            
        self.direct_supers = supers
        self.direct_subs = []
        self.all_subs = []
        
        ancestors = set[Type](supers) 
        
        for st in supers:
            st.direct_subs.append(self)
            st.all_subs.append(self)
            for anc in st.all_supers:
                ancestors.add(anc)
                if self not in anc.all_subs:
                    anc.all_subs.append(self)
        self.all_supers = list(ancestors) 

    def __repr__(self) -> str:
        return f"Type.{self.name}"
    
    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, rhs: object) -> bool:
        return self is rhs
    def __lt__(self, rhs: Type) -> bool:
        if isinstance(rhs, MaybeType):
            return self <= rhs.if_there_type
        return  self in rhs.all_subs
    def __le__(self, rhs: Type) -> bool:
        return self is rhs or self < rhs
    
Type.ANY = Type("ANY", is_root=True)
Type.NONE = Type("NONE")
Type.IGNORE = Type("IGNORE")
Type.ERROR = Type("ERROR")
Type.WELL = Type("WELL")
Type.NUMBER = Type("NUMBER")
Type.FLOAT = Type("FLOAT", [Type.NUMBER])
Type.INT = Type("INT", [Type.FLOAT])
Type.BINARY_STATE = Type("BINARY_STATE")
Type.BINARY_CPT = Type("BINARY_CPT")
Type.PAD = Type("PAD", [Type.BINARY_CPT])
Type.WELL_PAD = Type("WELL_PAD", [Type.BINARY_CPT])
Type.DROP = Type("DROP", [Type.PAD])
Type.ORIENTED_DROP = Type("ORIENTED_DROP", [Type.DROP])
Type.DIR = Type("DIR")
Type.ORIENTED_DIR = Type("ORIENTED_DIR", [Type.DIR])
Type.ROW = Type("ROW")
Type.COLUMN = Type("COLUMN")
Type.BARRIER = Type("BARRIER")
Type.DELAY = Type("DELAY")
Type.TIME = Type("TIME", [Type.DELAY])
Type.TICKS = Type("TICKS", [Type.DELAY])
Type.BOOL = Type("BOOL")
Type.VOLUME = Type("VOLUME")

class MaybeType(Type):
    if_there_type: Final[Type]
    
    def __init__(self, if_there_type: Type) -> None:
        super().__init__(f"MAYBE({if_there_type.name})")
        self.if_there_type = if_there_type
        
    @property
    def maybe(self)->MaybeType:
        return self
        
    def __repr__(self) -> str:
        return f"Maybe({self.if_there_type})"
    
    def __lt__(self, rhs: Type) -> bool:
        if isinstance(rhs, MaybeType):
            return self.if_there_type < rhs.if_there_type
        return super().__lt__(rhs)
    

class Signature(NamedTuple):
    param_types: tuple[Type,...]
    return_type: Type
    
    @classmethod
    def of(cls, param_types: Sequence[Type], return_type: Type) -> Signature:
        if not isinstance(param_types, tuple):
            param_types = tuple(param_types)
        return Signature(param_types, return_type)
    
    # We are less than the rhs if our types are the same or wider than 
    # its and our return is the same or narrower, and at least one is different
    def __lt__(self, rhs) -> bool:
        if not isinstance(rhs, Signature):
            return False
        if self.return_type > rhs.return_type:
            return False
        narrower = self.return_type < rhs.return_type
        for mine,theirs in zip(self.param_types, rhs.param_types):
            if mine < theirs:
                return False
            if mine > theirs:
                narrower = True
        return narrower


class CallableType(Type):
    sig: Final[Signature]
    
    @property
    def param_types(self) -> Sequence[Type]:
        return self.sig.param_types
    
    @property
    def return_type(self) -> Type:
        return self.sig.return_type
    
    # param_types: Final[Sequence[Type]]
    # return_type: Final[Type]
    
    def __init__(self,
                 name: str,  
                 param_types: Sequence[Type],
                 return_type: Type,
                 *,
                 supers: Optional[Sequence[Type]] = None):
        super().__init__(name, supers)
        self.sig = Signature.of(param_types, return_type)
        
        
class MotionType(CallableType):
    def __init__(self):
        super().__init__("MOTION", (Type.DROP,), Type.DROP)
        
Type.MOTION = MotionType()
        
Type.DELTA = Type("DELTA", [Type.MOTION])


class TwiddleOpType(CallableType):
    def __init__(self):
        super().__init__("TWIDDLE_OP", (Type.BINARY_CPT,), Type.BINARY_STATE)
        
Type.TWIDDLE_OP = TwiddleOpType()

class PauseType(CallableType):
    def __init__(self):
        super().__init__("PAUSE", (Type.ANY,), Type.NONE)
        
Type.PAUSE = PauseType()

class MacroType(CallableType):
    instances = dict[Signature, 'MacroType']()
    
    def __init__(self, 
                 param_types: Sequence[Type],
                 return_type: Type):
        super().__init__(f"Macro[({','.join(t.name for t in param_types)}),{return_type.name}]", 
                         param_types, return_type)
        
    @classmethod
    def find(cls, param_types: Sequence[Type], return_type: Type) -> MacroType:
        sig = Signature.of(param_types, return_type)
        mt = cls.instances.get(sig, None)
        if mt is None:
            mt = MacroType(param_types, return_type)
            cls.instances[sig] = mt
        return mt
    
    # I'm not sure if it's really correct to put this here, but
    # it will probably do the right thing.
    def __lt__(self, rhs:Type)->bool:
        if isinstance(rhs, MacroType):
            return self.sig < rhs.sig
        return Type.__lt__(self, rhs)
    
    # def __eq__(self, rhs:object)->bool:
    #     if isinstance(rhs, MacroType):
    #         return self.sig == rhs.sig
    #     return CallableType.__eq__(self, rhs)
    
    def __hash__(self)->int:
        return hash(self.sig)
    
class Attr(Enum):
    _ignore_ = ["_known"]    
    _known: ClassVar[dict[Attr, dict[Type, tuple[Type, Callable[[Any], Any]]]]]

    GATE = auto()
    EXIT_PAD = auto()
    STATE = auto()
    PAD = auto()
    DISTANCE = auto()
    DURATION = auto()
    ROW = auto()
    COLUMN = auto()
    WELL = auto()
    EXIT_DIR = auto()
    DROP = auto()
    
    @property
    def mappings(self) -> dict[Type, tuple[Type, Callable[[Any], Any]]]:
        return self._known[self]
    
    @property
    def known_types(self) -> Sequence[Type]:
        return tuple(self.mappings.keys())

    def register(self, otype: Type, rtype: Type, extractor: Callable[[Any], Any]) -> None:
        self.mappings[otype] = (rtype, extractor)
        
    def __getitem__(self, otype: Type) -> Optional[tuple[Type, Type, Callable[[Any], Any]]]:
        d = self.mappings
        best: Optional[Type] = None
        for t in d:
            if otype <= t and (best is None or t < best):
                best = t
        return None if best is None else (best, *d[best])
                
Attr._known = defaultdict(lambda : defaultdict(list))

class Rel(Enum):
    _ignore_ = ["_known"]    
    _known: ClassVar[Mapping[Rel, Callable[[Any,Any], Any]]]
    
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    
    def test(self, x, y) -> bool:
        fn = self._known[self]
        res = fn(x, y)
        assert isinstance(res, bool)
        return res
    
Rel._known = {
    Rel.EQ: lambda x,y: x == y,
    Rel.NE: lambda x,y: x != y,
    Rel.LT: lambda x,y: x < y,
    Rel.LE: lambda x,y: x <= y,
    Rel.GT: lambda x,y: x > y,
    Rel.GE: lambda x,y: x >= y,
    }
    

    
    
if __name__ == '__main__':
    def check(lhs: Type, rhs: Type) -> None:
        print(f"Comparing {lhs} and {rhs}:")
        # print(f"  {lhs}.all_subs = {map_str(lhs.all_subs)}")
        # print(f"  {rhs}.all_subs = {map_str(rhs.all_subs)}")
        print(f"  {lhs} == {rhs}: {lhs == rhs}")
        print(f"  {lhs} != {rhs}: {(lhs != rhs)}")
        print(f"  {lhs} < {rhs}: {lhs < rhs}")
        print(f"  {lhs} <= {rhs}: {lhs <= rhs}")
        print(f"  {lhs} > {rhs}: {lhs > rhs}")
        print(f"  {lhs} >= {rhs}: {lhs >= rhs}")
        
    
    check(Type.WELL, Type.INT)
    check(Type.INT, Type.NUMBER)
    check(Type.WELL, Type.WELL)
    check(Type.WELL, Type.ANY)