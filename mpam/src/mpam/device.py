from . import engine
from typing import Type, Optional
from types import TracebackType

class Board:
    ...

class System:
    board: Board
    engine: engine.Engine
    
    def __init__(self, *, board: Board):
        self.board = board
        self.engine = engine.Engine()

    def __enter__(self) -> 'System':
        self.engine.__enter__()
        return self
    
    def __exit__(self, 
                 exc_type: Optional[Type[BaseException]], 
                 exc_val: Optional[BaseException], 
                 exc_tb: Optional[TracebackType]) -> bool:
        return self.engine.__exit__(exc_type, exc_val, exc_tb)
    
    
    
        