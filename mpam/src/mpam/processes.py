from __future__ import annotations

from abc import ABC, abstractmethod
from threading import Lock
from typing import Final, Iterator, Sequence, Optional, Callable

from mpam.device import Pad, Board
from mpam.drop import Drop
from mpam.types import Delayed, Callback, Ticks, tick, Operation, RunMode, \
    DelayType


    


class MultiDropProcessType(ABC):
    n_drops: Final[int]
    
    def __init__(self, n_drops: int) -> None:
        self.n_drops = n_drops
    
    # returns True if the iterator still has work to do
    @abstractmethod
    def iterator(self, drops: tuple[Drop, ...]) -> Iterator[bool]:  # @UnusedVariable
        ...
        
    # returns True if the futures should be posted.
    def finish(self, drops: Sequence[Drop],                  # @UnusedVariable
               futures: dict[Drop, Delayed[Drop]]) -> bool:  # @UnusedVariable
        return True
    
    @abstractmethod
    def secondary_pads(self, lead_drop: Drop) -> Sequence[Pad]:  # @UnusedVariable
        ...
        
    def start(self, lead_drop: Drop, future: Delayed[Drop]) -> None:
        process = MultiDropProcess(self, lead_drop, future)
        process.start()

    
class MultiDropProcess:
    process_type: Final[MultiDropProcessType]
    futures: Final[dict[Drop, Delayed[Drop]]]
    drops: Final[list[Optional[Drop]]]
    
    global_lock: Final[Lock] = Lock()
    
    def __init__(self, process_type: MultiDropProcessType,
                 lead_drop: Drop,
                 lead_future: Delayed[Drop]
                 ) -> None:
        self.process_type = process_type
        self.futures = {lead_drop: lead_future}
        self.drops = [None] * process_type.n_drops
        self.drops[0] = lead_drop
        
    def start(self) -> None:
        drops = self.drops
        lead_drop = drops[0]
        assert lead_drop is not None
        secondary_pads = self.process_type.secondary_pads(lead_drop)
        futures = self.futures
        pending_drops = 0
        lock = self.global_lock
        
        def on_join_factory(i: int) -> Callable[[Drop, Delayed[Drop]],
                                         Optional[Callback]]:
            # Called with global_lock locked.  Returns true if last one.
            def on_join(drop: Drop, future: Delayed[Drop]) -> Optional[Callback]:
                nonlocal pending_drops
                drops[i+1] = drop
                futures[drop] = future
                if pending_drops == 1:
                    return lambda: self.run()
                else:
                    pending_drops -= 1
                    return None
            return on_join
        
        with lock:
            for i,p in enumerate(secondary_pads):
                future: Optional[Delayed[Drop]] = getattr(p, "_waiting_to_join", None)
                if future is None:
                    setattr(p, "_on_join", on_join_factory(i))
                    pending_drops += 1
                else:
                    setattr(p, "_waiting_to_join", None)
                    d = p.drop
                    assert d is not None
                    futures[d] = future
                    drops[i] = d
            ready = (pending_drops == 0)
        if ready:
            self.run()


    @classmethod
    def join(cls, drop: Drop, future: Delayed[Drop]) -> None:
        p = drop.pad
        with cls.global_lock:
            fn: Optional[Callable[[Drop,Delayed[Drop]],
                                  Optional[Callback]]] = getattr(p, "_on_join", None)
            if fn is None:
                setattr(p, "_waiting_to_join", future)
                return
            else:
                setattr(p, "_on_join", None)
                cb = fn(drop, future)
        if cb is not None:
            cb()
            
    def iterator(self, board: Board, drops: Sequence[Drop]) -> Iterator[Optional[Ticks]]:
        process_type = self.process_type
        futures = self.futures
        def checked(d: Optional[Drop]) -> Drop:
            assert d is not None
            return d
        drops = tuple(checked(d) for d in drops)
        i = process_type.iterator(drops = drops)
        one_tick = 1*tick
        while next(i):
            yield one_tick
        def do_post() -> None:
            if process_type.finish(drops, futures):
                for drop, future in futures.items():
                    future.post(drop)
        board.after_tick(do_post)
        yield None
        
            
    def run(self) -> None:
        def checked(d: Optional[Drop]) -> Drop:
            assert d is not None
            return d
        drops = tuple(checked(d) for d in self.drops)
        lead_drop = drops[0]
        assert lead_drop is not None
        board = lead_drop.pad.board
        iterator = self.iterator(board, drops)
        
        # We're inside a before_tick, so we run the first step here.  Then we install
        # the callback before the next tick to do the rest
        after_first = next(iterator)
        if after_first is not None: 
            board.before_tick(lambda: next(iterator))


class StartProcess(Operation[Drop,Drop]):
    process_type: Final[MultiDropProcessType]
    
    def __repr__(self) -> str:
        return f"<StartProcess: {self.process_type}>"
    
    def __init__(self, process_type: MultiDropProcessType) -> None:
        self.process_type = process_type

    def _schedule_for(self, drop: Drop, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  # @UnusedVariable
                      ) -> Delayed[Drop]:
        board = drop.pad.board
        future = Delayed[Drop]()
            
        assert mode.is_gated
        def before_tick() -> None:
            # If all the other drops are waiting, this will install a callback on the next tick and then
            # call it immediately to do the first step.  Otherwise, that will happen when the last 
            # drop shows up.
            self.process_type.start(drop, future)
        board.before_tick(before_tick, delta=mode.gated_delay(after))
        return future
    
class JoinProcess(Operation[Drop,Drop]):
    
    def __repr__(self) -> str:
        return f"<Drop.Join>"
    
    def _schedule_for(self, drop: Drop, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  # @UnusedVariable
                      ) -> Delayed[Drop]:
        board = drop.pad.board
        future = Delayed[Drop]()
            
        assert mode.is_gated
        def before_tick() -> None:
            MultiDropProcess.join(drop, future)
        board.before_tick(before_tick, delta=mode.gated_delay(after))
        return future
