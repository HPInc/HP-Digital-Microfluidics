from __future__ import annotations

from typing import Final, Optional, Sequence


class Type:
    name: Final[str]
    direct_supers: Final[Sequence[Type]]
    all_supers: Final[Sequence[Type]]
    direct_subs: Final[list[Type]]
    all_subs: Final[list[Type]]
    
    ANY: Type
    NUMBER: Type
    INT: Type
    FLOAT: Type
    WELL: Type
    PAD: Type
    DROP: Type
    ORIENTED_DROP: Type
    DIR: Type
    ORIENTED_DIR: Type
    DELTA: Type
    ROW: Type
    COLUMN: Type
    BARRIER: Type
    CALLABLE: Type
    MACRO: Type
    BOUND_MACRO: Type
    
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
Type.WELL = Type("WELL")
Type.NUMBER = Type("NUMBER")
Type.INT = Type("INT", [Type.NUMBER])
Type.FLOAT = Type("FLOAT", [Type.NUMBER])
Type.PAD = Type("PAD")
Type.DROP = Type("DROP", [Type.PAD])
Type.ORIENTED_DROP = Type("ORIENTED_DROP", [Type.DROP])
Type.DIR = Type("DIR")
Type.ORIENTED_DIR = Type("ORIENTED_DIR", [Type.DIR])
Type.CALLABLE = Type("CALLABLE")
Type.DELTA = Type("DELTA", [Type.CALLABLE])
Type.ROW = Type("ROW")
Type.COLUMN = Type("COLUMN")
Type.BARRIER = Type("BARRIER")
Type.MACRO = Type("MACRO", [Type.CALLABLE])
Type.BOUND_MACRO = Type("BOUND_MACRO", [Type.MACRO])

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