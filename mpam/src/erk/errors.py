from __future__ import annotations
from typing import Callable, Final, TextIO, NoReturn
import sys
from abc import ABC, abstractmethod

class ErrorHandler(ABC):
    """
    An handler that can be used to handle (or check and, if necessary, handle)
    error conditions.
    
    Example:
        
        The following definition of ``factorial`` checks to make sure that the
        argument is not negative, allowing the caller to specify the action if
        it is.  By default, a warning will be printed, but this could be changed
        to having the code raise an exception or take other action. ::
        
            def lookup(index: int, on_out_of_range: ErrorHandler = PRINT) -> str:
                on_out_of_range.expect_true(index < self.size, 
                                            lambda: f"No element {index}. Only {self.size} elements")
                return self.content[index]
                
    All subclasses of :class:`ErrorHandler` must define :func:`__call__`, which
    is passed in a string describing the error.  :class:`ErrorHandler` itself
    defines :func:`expect_true` and :func:`expect_false`, which take a boolean
    and a :class:`.Callable` that returns a string.  If the boolean argument is
    ``False`` (for :func:`expect_true`) or ``True`` (for :func:`expect_false`),
    the :class:`.Callable` argument is evaluated and passed to :func:`__call__`.
    
    Defined subclasses of :class:`ErrorHandler` include
    
    :class:`DoNothing`
        Do nothing.  The condition is still evaluated, but it isn't checked and
        the message is never computed.  This is typically used via its instance
        :attr:`IGNORE`::
        
            s = obj.lookup(n, on_out_of_range = IGNORE)
        
    :class:`PRINT_TO` ``(where:`` :class:`.TextIO` ``)``
        Print the message to ``where``.  Predefined objects exist for printing
        to :attr:`sys.stdout` (:attr:`PRINT`) and :attr:`sys.stderr`
        (:attr:`PRINT_TO_STDERR`)
        
    :class:`RAISE` ``(factory)``
        Raise the exception returned by calling ``factory``.  Typically, this
        will be the name of the exception class, e.g., ::
        
            s = obj.lookup(n, on_out_of_range = RAISE(OutOfRangeError))
            
    :class:`FIX_BY` ``(function)``
        Call ``function`` (ignoring the message), which should, as a side effect,
        fix the problem.  For example, ::
        
            s = obj.lookup(n, on_out_of_range = FIX_BY(lambda: obj.grow_to(1.5*n)))
        
    """
    @abstractmethod
    def __call__(self, msg: str) -> None:  # @UnusedVariable
        """
        Call the handler, passing in the generated message.
        
        Note:
            This is an abstract method, which must be defined by subclasses.

        Args:
            msg: a message describing the error
        """
        ...
        
    def expect_true(self,
                    cond: bool, 
                    msg_fn: Callable[[], str]) -> bool:
        """
        Call the handler (via :func:`__call__`) passing in ``msg_fn()`` if ``cond`` is ``False``
        
        Returns ``True`` if the expectation succeeds (i.e., ``cond`` is
        ``True``).  This is to facilitate idioms like ::
        
            if not on_empty.expect_true(len(queue) > 0, lambda: f"The queue is empty"):
                return MISSING
        Args:
            cond: the condition to check
            msg_fn: a function to call to get the message
        Returns:
            ``True`` if the expectation succeeds (i.e., ``cond`` is ``True``) 
        """
        if not cond:
            self(msg_fn())
        return cond

    def expect_false(self,
                     cond: bool, 
                     msg_fn: Callable[[], str]) -> bool:
        """
        Call the handler (via :func:`__call__`) passing in ``msg_fn()`` if ``cond`` is ``True``

        Returns ``True`` if the expectation succeeds (i.e., ``cond`` is
        ``False``).  This is to facilitate idioms like ::
        
            if not on_empty.expect_false(len(queue) == 0, lambda: f"The queue is empty"):
                return MISSING
        Args:
            cond: the condition to check
            msg_fn: a function to call to get the message
        Returns:
            ``True`` if the expectation succeeds (i.e., ``cond`` is ``False``) 
        """
        if cond:
            self(msg_fn())
        return not cond
            
class DoNothing(ErrorHandler):
    """
    An :class:`ErrorHandler` that does nothing.
    
    The condition is still evaluated, but it isn't checked and
    the message is never computed.  This is typically used via its instance
    :attr:`IGNORE`
    
    Example:
        ::
        
            s = obj.lookup(n, on_out_of_range = IGNORE)
    """
    def __call__(self, msg: str) -> None:
        """
        Do nothing.
        
        Args:
            msg: a message describing the error, which is ignored
        
        """
        pass

    def expect_true(self,
                    cond: bool, 
                    msg_fn: Callable[[], str]) -> bool:
        """
        Do nothing.  
        
        ``cond`` is not checked, and ``msg_fn`` is never called

        Args:
            cond: the condition to check
            msg_fn: a function to call to get the message
        """
        return cond

    def expect_false(self,
                     cond: bool, 
                     msg_fn: Callable[[], str]) -> bool:
        """
        Do nothing.  
        
        ``cond`` is not checked, and ``msg_fn`` is never called

        Args:
            cond: the condition to check
            msg_fn: a function to call to get the message
        """
        return not cond
    
    def __repr__(self) -> str:
        return "IGNORE"
    
IGNORE = DoNothing()    #: A singleton instance of :class:`DoNothing`
    
class PRINT_TO(ErrorHandler):
    """
    An :class:`ErrorHandler` that prints a message to a :class:`.TextIO`.
    
    Predefined objects exist for printing
    to :attr:`sys.stdout` (:attr:`PRINT`) and :attr:`sys.stderr`
    (:attr:`PRINT_TO_STDERR`)
        
    Example:
        ::
        
            s = obj.lookup(n, on_out_of_range = PRINT_TO_STDERR)
            s = obj.lookup(n, on_out_of_range = PRINT_TO(logfile))
    """
    
    where: Final[TextIO] #: The :class:`.TextIO` to print to

    def __call__(self, msg: str) -> None:
        """
        Print ``msg`` to :attr:`where`
        
        Args:
            msg: a message describing the error
        """
        print(msg, file=self.where)
    def __init__(self, where: TextIO=sys.stdout):
        """
        Initialize the object 
        
        Args:
            where: the :class:`.TextIO` to print to
        """
        self.where = where
        
    def __repr__(self) -> str:
        if self.where is sys.stdout:
            return "PRINT_TO(stdout)"
        if self.where is sys.stderr:
            return "PRINT_TO(stderr)"
        return f"PRINT_TO({self.where})"
        
PRINT = PRINT_TO(sys.stdout)
"""
A :class:`PRINT_TO` :class:`ErrorHandler` that prints to :attr:`sys.stdout`
"""
PRINT_TO_STDERR = PRINT_TO(sys.stderr)
"""
A :class:`PRINT_TO` :class:`ErrorHandler` that prints to :attr:`sys.stderr`
"""
    
class RAISE(ErrorHandler):
    """
    An :class:`ErrorHandler` that raises an exception.
    
    It is initialized with a :attr:`factory` function that can take the message
    string and returns an exception instance.  Typically, this will be the
    exception class itself.
        
    Example:
        ::

            s = obj.lookup(n, on_out_of_range = RAISE(KeyError))
    """
    def __init__(self, factory: Callable[[str], BaseException]) -> None:
        """
        Initialize the object
        
        Args:
            factory: a factory function that takes a message string and returns
                     an exception instance
        """
        self.factory: Final[Callable[[str], BaseException]] = factory
        """
        A factory function that takes a message string returns an exception
        instance
        """
        
    def __call__(self, msg: str) -> NoReturn:
        """
        Create and raise the exception
        
        Args:
            msg: a message describing the error
        """
        raise self.factory(msg)
    
    def __repr__(self) -> str:
        return f"RAISE({self.factory})"
    
class FIX_BY(ErrorHandler):
    """
    An :class:`ErrorHandler` that fixes the problem by calling an arbitrary
    function.  
    
    It is initialized with a :attr:`factory` function taking no arguments.  Any
    value returned is ignored.
    
    This class reimplements :func:`expect_true` and :func:`expect_false` to
    never evaluate their `msg_fn` parameters.
    
    Note:
        The handler is assumed to have fixed the problem.  The condition is not
        rechecked.
        
    Example:
        ::

            s = obj.lookup(n, on_out_of_range = FIX_BY(lambda: obj.grow_to(n))
    """
    
    def __init__(self, function: Callable[[], None]) -> None:
        """
        Initialize the object.
        
        Args:
            function: a function of no arguments to call to fix the problem
        """
        self.fixer = function
        """
        A function of no arguments to call to fix the problem
        """
    def __call__(self, msg: str) -> None: # @UnusedVariable
        """
        Call :attr:`fixer` to fix the problem
        
        Args:
            msg: a message describing the error, which is ignored
        
        """
        (self.fixer)()

    def expect_true(self,
                    cond: bool, 
                    msg_fn: Callable[[], str]) -> bool: # @UnusedVariable
        """
        Call the :attr:`fixer` to fix the problem if ``cond`` is ``False``

        Args:
            cond: the condition to check
            msg_fn: a function to call to get the message, which is ignored
        """
        if not cond:
            (self.fixer)()
        return cond

    def expect_false(self,
                     cond: bool, 
                     msg_fn: Callable[[], str]) -> bool: # @UnusedVariable
        """
        Call the :attr:`fixer` to fix the problem if ``cond`` is ``True``

        Args:
            cond: the condition to check
            msg_fn: a function to call to get the message, which is ignored
        """
        if cond:
            (self.fixer)()
        return not cond
            
    def __repr__(self) -> str:
        return f"FIX_BY({self.fixer})"
