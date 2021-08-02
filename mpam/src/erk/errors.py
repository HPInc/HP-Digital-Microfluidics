from __future__ import annotations
from typing import Callable, Final, TextIO, NoReturn
import sys
from abc import ABC, abstractmethod

class ErrorHandler(ABC):
    @abstractmethod
    def __call__(self, msg: str) -> None:  # @UnusedVariable
        ...
        
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
    def __init__(self, factory: Callable[[str], BaseException]) -> None:
        self.factory: Final[Callable[[str], BaseException]] = factory
        
    def __call__(self, msg: str) -> NoReturn:
        raise self.factory(msg)
    
class FIX_BY(ErrorHandler):
    def __init__(self, function: Callable[[], None]) -> None:
        self.fixer = function
        
    def __call__(self, msg: str) -> None: # @UnusedVariable
        (self.fixer)()

    def expect_true(self,
                    cond: bool, 
                    msg_fn: Callable[[], str]) -> None: # @UnusedVariable
        if not cond:
            (self.fixer)()

    def expect_false(self,
                     cond: bool, 
                     msg_fn: Callable[[], str]) -> None: # @UnusedVariable
        if cond:
            (self.fixer)()
