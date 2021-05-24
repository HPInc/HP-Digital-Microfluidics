from typing import Callable, Final, TextIO, NoReturn
import sys

class ErrorHandler:
    def __call__(self, msg: str) -> None:
        raise NotImplementedError()
    
    def expect_true(self,
                    cond: bool, 
                    msg_fn: Callable[[], str]) -> None:
        if not cond:
            self(msg_fn())

    def expect_false(self,
                     cond: bool, 
                     msg_fn: Callable[[], str]) -> None:
        if cond:
            self(msg_fn())
            
class DoNothing(ErrorHandler):
    def __call__(self, msg: str) -> None:
        pass

    def expect_true(self,
                    cond: bool, 
                    msg_fn: Callable[[], str]) -> None:
        pass

    def expect_false(self,
                     cond: bool, 
                     msg_fn: Callable[[], str]) -> None:
        pass
    
IGNORE = DoNothing()
    
class PRINT_TO(ErrorHandler):
    where: Final[TextIO]

    def __call__(self, msg: str) -> None:
        print(msg, file=self.where)
        
    def __init__(self, where: TextIO=sys.stdout):
        self.where = where
        
PRINT = PRINT_TO(sys.stdout)
PRINT_TO_STDERR = PRINT_TO(sys.stderr)
    
class RAISE(ErrorHandler):
    def __init__(self, factory: Callable[[str], BaseException]):
        self.factory: Final[Callable[[str], BaseException]] = factory
        
    def __call__(self, msg: str) -> NoReturn:
        raise self.factory(msg)

