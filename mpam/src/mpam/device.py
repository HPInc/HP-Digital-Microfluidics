from . import engine

class System:
    def __init__(self, *, board):
        self.board = board
        self.engine = engine.Engine()

    def __enter__(self):
        self._engine.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        e = self._engine
        self._engine = None
        return e.__exit__(exc_type, exc_val, exc_tb)
    
    
class Board:
    ...
    
        