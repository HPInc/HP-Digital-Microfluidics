from __future__ import annotations
from typing import TypeVar, Generic, Type, Any, Final, ClassVar

_T = TypeVar('_T')

_Src = TypeVar('_Src')
_From = TypeVar('_From')
_Mid = TypeVar('_Mid')
_To = TypeVar('_To')
_Further = TypeVar('_Further')

_API = TypeVar('_API')
_API2 = TypeVar('_API2')

class OpBase(Generic[_API]):
    # api_type: Type[_API]
    known: Final[ClassVar[dict[type, type]]] = {}
    def following(self, op: Op[_From, _To, _API2]) -> _API:
        api_type = self.api_type
        t = self.known.get(api_type, None)
        if t is None:
            name = f"CombinedTo{self.api_type.__name__}"
            print(f"Creating {name}")
            def init(self, first: Op, second: Op) -> None:
                CombinedOp.__init__(self, first, second)
                api_type.__init__(self)
            d = {
                '__init__': init
                }
            base = CombinedStaticOp if isinstance(op, StaticOp) else CombinedOp
            t = type(name, (base, self.api_type), d)
            self.known[api_type] = t
        combined = t(op, self)
        return combined
    
    def __init__(self, api_type: Type[_API]) -> None:
        self.api_type: Final[Type[_API]] = api_type

class Op(Generic[_From, _To, _API], OpBase[_API]):
        
    def then(self, op: Op[_To,_Further,_API2]) -> _API2:
        return op.following(self)
    
    def apply_to(self, obj: _From) -> _To:
        raise NotImplementedError()
    
class StaticOp(Op[None, _To, _API]):
    def apply(self) -> _To:
        return self.apply_to(None)
    

class CombinedOp(Generic[_From, _Mid, _To, _API], Op[_From,_To,_API]):
    first: Op[_From, _Mid, Any]
    second: Op[_Mid, _To, _API]
    
    def __init__(self, first: Op[_From, _Mid, Any], second: Op[_Mid, _To, _API]):
        self.first = first
        self.second = second 
    def apply_to(self, obj: _From) -> _To:
        mid = self.first.apply_to(obj)
        return self.second.apply_to(mid)
        
class CombinedStaticOp(Generic[_Mid, _To, _API], StaticOp[_To,_API]):
    first: StaticOp[_Mid, Any]
    second: Op[_Mid, _To, _API]
    
    def __init__(self, first: StaticOp[_Mid, Any], second: Op[_Mid, _To, _API]):
        self.first = first
        self.second = second 
    def apply_to(self, obj: None) -> _To:  # @UnusedVariable
        mid = self.first.apply()
        return self.second.apply_to(mid)
        
# class ToDrop(OpBase[_API]):
class ToDrop(Op[_From, 'Drop', 'ToDrop']):
    def then_move(self, direction: str) -> ToDrop[_From]:
        print("In then_move()")
        seq: ToDrop[_From] = Move(direction).following(self)
        return seq
    def __init__(self) -> None:
        super().__init__(ToDrop)
        


        
class JustNamed: 
    name: Final[str]
    def __init__(self, name: str) -> None:
        self.name = name
        
    def __repr__(self) -> str:
        return self.name
    
class Drop(JustNamed): 
    counter: int = 1
    @classmethod
    def new_drop(cls) -> Drop:
        drop = Drop(f"drop-{cls.counter}")
        cls.counter += 1
        return drop
    
class Well(JustNamed): ... 

class Move(ToDrop[Drop]):
    direction: Final[str]
    
    def __init__(self, direction: str) -> None:
        super().__init__()
        self.direction = direction
    def apply_to(self, drop: Drop) -> Drop:
        print(f"Moving {drop} {self.direction}")
        return drop

class Dispense(ToDrop[Well]):
    def apply_to(self, well: Well) -> Drop:
        drop = Drop.new_drop()
        print(f"Dispensing {drop} from {well}")
        return drop
    
class DispenseFrom(ToDrop[None], StaticOp[Drop, ToDrop[None]]):
    well: Final[Well]
    def __init__(self, well: Well) -> None:
        super().__init__()
        self.well = well
        
    def apply_to(self, _: None) -> Drop:
        drop = Drop.new_drop()
        print(f"Dispensing {drop} from {well} (static)")
        return drop
    
drop = Drop("d")
well = Well("w")

op = Move("up")
op.apply_to(drop)
# print(op.val)

op2 = op.then_move("down")
op2.apply_to(drop)
op3 = op2.then_move("right")
op3.apply_to(drop)

op4 = Dispense().then_move("up")
op4.apply_to(well)

op5 = Dispense().then(op3)
op6 = op3.following(Dispense())
op7: ToDrop[Well] = Dispense()
print("-----------")
op8 = DispenseFrom(well).then_move("right").then_move("down")
op8.apply_to(None)
            