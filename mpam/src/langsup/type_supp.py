from __future__ import annotations

from typing import Final, Optional, Sequence, NamedTuple


class Type:
    name: Final[str]
    direct_supers: Final[Sequence[Type]]
    all_supers: Final[Sequence[Type]]
    direct_subs: Final[list[Type]]
    all_subs: Final[list[Type]]
    
    ANY: Type
    NONE: Type
    IGNORE: Type
    ERROR: Type
    NUMBER: Type
    INT: Type
    FLOAT: Type
    BINARY_STATE: Type
    WELL: Type
    BINARY_CPT: Type
    PAD: Type
    WELL_PAD: Type
    DROP: Type
    ORIENTED_DROP: Type
    DIR: Type
    ORIENTED_DIR: Type
    MOTION: MotionType
    DELTA: Type
    TWIDDLE_OP: TwiddleOpType
    ROW: Type
    COLUMN: Type
    BARRIER: Type
    
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
        return  self in rhs.all_subs
    def __le__(self, rhs: Type) -> bool:
        return self is rhs or self < rhs
    
Type.ANY = Type("ANY", is_root=True)
Type.NONE = Type("NONE")
Type.IGNORE = Type("IGNORE")
Type.ERROR = Type("ERROR")
Type.WELL = Type("WELL")
Type.NUMBER = Type("NUMBER")
Type.INT = Type("INT", [Type.NUMBER])
Type.FLOAT = Type("FLOAT", [Type.NUMBER])
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

class Signature(NamedTuple):
    param_types: tuple[Type,...]
    return_type: Type
    
    @classmethod
    def of(cls, param_types: Sequence[Type], return_type: Type) -> Signature:
        if not isinstance(param_types, tuple):
            param_types = tuple(param_types)
        return Signature(param_types, return_type)


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



class MacroType(CallableType):
    instances = dict[Signature, 'MacroType']()
    
    def __init__(self, 
                 param_types: Sequence[Type],
                 return_type: Type):
        super().__init__(f"Callable[({','.join(t.name for t in param_types)}),{return_type.name}]", 
                         param_types, return_type)
        
    @classmethod
    def find(cls, param_types: Sequence[Type], return_type: Type) -> MacroType:
        sig = Signature.of(param_types, return_type)
        mt = cls.instances.get(sig, None)
        if mt is None:
            mt = MacroType(param_types, return_type)
            cls.instances[sig] = mt
        return mt

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