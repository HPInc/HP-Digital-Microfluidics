from . import engine

class Board:
    def __enter__(self):
        # check to ensure that _engine is None (or add a reentrancy count)
        self._engine = engine.Engine(self)
        self._engine.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        e = self._engine
        self._engine = None
        return e.__exit__(exc_type, exc_val, exc_tb)
    
        