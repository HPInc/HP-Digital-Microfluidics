from __future__ import annotations

from abc import ABC, abstractmethod
from threading import Lock
from typing import Final, Iterator, Sequence, Optional, Callable, MutableMapping,\
    NamedTuple, Iterable

from mpam.device import Pad, Board
from mpam.drop import Drop
from mpam.types import Delayed, Callback, Ticks, tick, \
    DelayType, Reagent, waste_reagent, OnOff, Postable, CSOperation
from enum import Enum
from _collections import defaultdict
import sys
from erk.basic import not_None




FinishFunction = Callable[[MutableMapping[Pad, Postable[Drop]]], bool]

class MultiDropProcessType(ABC):
    n_drops: Final[int]

    def __init__(self, n_drops: int) -> None:
        self.n_drops = n_drops

    # returns None if the iterator still has work to do.  Otherwise, returns a function that will
    # be called after the last tick.  This function returns True if the passed-in futures should
    # be posted.
    @abstractmethod
    def iterator(self, pads: tuple[Pad, ...]) -> Iterator[Optional[FinishFunction]]:  # @UnusedVariable
        ...

    # # returns True if the futures should be posted.
    # def finish(self, drops: Sequence[Drop],                  # @UnusedVariable
    #            futures: dict[Drop, Delayed[Drop]]) -> bool:  # @UnusedVariable
    #     return True

    @abstractmethod
    def secondary_pads(self, lead_drop_pad: Pad) -> Sequence[Pad]:  # @UnusedVariable
        ...

    def start(self, lead_drop: Drop, future: Postable[Drop]) -> None:
        process = MultiDropProcess(self, lead_drop, future)
        process.start()


class MultiDropProcess:
    process_type: Final[MultiDropProcessType]
    futures: Final[dict[Pad, Postable[Drop]]]
    drops: Final[list[Optional[Drop]]]

    global_lock: Final[Lock] = Lock()

    def __init__(self, process_type: MultiDropProcessType,
                 lead_drop: Drop,
                 lead_future: Postable[Drop]
                 ) -> None:
        self.process_type = process_type
        self.futures = {lead_drop.on_board_pad: lead_future}
        self.drops = [None] * process_type.n_drops
        self.drops[0] = lead_drop

    def start(self) -> None:
        drops = self.drops
        lead_drop = drops[0]
        assert lead_drop is not None
        secondary_pads = self.process_type.secondary_pads(lead_drop.on_board_pad)
        futures = self.futures
        pending_drops = 0
        lock = self.global_lock

        def on_join_factory(i: int) -> Callable[[Drop, Postable[Drop]],
                                         Optional[Callback]]:
            # Called with global_lock locked.  Returns true if last one.
            def on_join(drop: Drop, future: Postable[Drop]) -> Optional[Callback]:
                nonlocal pending_drops
                drops[i+1] = drop
                futures[drop.on_board_pad] = future
                if pending_drops == 1:
                    return lambda: self.run()
                else:
                    pending_drops -= 1
                    return None
            return on_join

        with lock:
            for i,p in enumerate(secondary_pads):
                future: Optional[Postable[Drop]] = getattr(p, "_waiting_to_join", None)
                if future is None:
                    setattr(p, "_on_join", on_join_factory(i))
                    pending_drops += 1
                else:
                    setattr(p, "_waiting_to_join", None)
                    d = p.drop
                    assert d is not None
                    futures[p] = future
                    drops[i+1] = d
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
        pads = tuple(drop.on_board_pad for drop in drops)
        # drops = tuple(not_None(d) for d in drops)
        i = process_type.iterator(pads=pads)
        one_tick = 1*tick
        while True:
            finish = next(i)
            if finish is not None:
                break
            yield one_tick
        real_finish = finish
        def do_post() -> None:
            if real_finish(futures):
                for pad, future in futures.items():
                    drop = not_None(pad.drop, desc=lambda: f"{pad}.drop")
                    # print(f"Finished with {drop} at {pad}.")
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
        board = lead_drop.on_board_pad.board
        iterator = self.iterator(board, drops)

        # We're inside a before_tick, so we run the first step here.  Then we install
        # the callback before the next tick to do the rest
        after_first = next(iterator)
        if after_first is not None:
            board.before_tick(lambda: next(iterator))


class StartProcess(CSOperation[Drop,Drop]):
    process_type: Final[MultiDropProcessType]

    def __repr__(self) -> str:
        return f"<StartProcess: {self.process_type}>"

    def __init__(self, process_type: MultiDropProcessType) -> None:
        self.process_type = process_type

    def _schedule_for(self, drop: Drop, *,
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  # @UnusedVariable
                      ) -> Delayed[Drop]:
        board = drop.on_board_pad.board
        future = Postable[Drop]()

        def before_tick() -> None:
            # If all the other drops are waiting, this will install a callback on the next tick and then
            # call it immediately to do the first step.  Otherwise, that will happen when the last
            # drop shows up.
            # print(f"Starting process with {drop}: {self.process_type}")
            self.process_type.start(drop, future)
        board.before_tick(before_tick, delta=after)
        return future

class JoinProcess(CSOperation[Drop,Drop]):

    def __repr__(self) -> str:
        return f"<Drop.Join>"

    def _schedule_for(self, drop: Drop, *,
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  # @UnusedVariable
                      ) -> Delayed[Drop]:
        board = drop.on_board_pad.board
        future = Postable[Drop]()

        def before_tick() -> None:
            # print(f"Joining process with {drop}")
            MultiDropProcess.join(drop, future)
        board.before_tick(before_tick, delta=after)
        return future

class PairwiseMix(NamedTuple):
    drop1_index: int
    drop2_index: int

    def merge(self, pads: tuple[Pad,...]) -> Delayed[OnOff]:
        # print(f"Merging {[d for d in drops]}")
        # drop1 = drops[self.drop1_index]
        # drop2 = drops[self.drop2_index]
        # pad1 = drop1.on_board_pad
        # pad2 = drop2.on_board_pad
        pad1 = pads[self.drop1_index]
        pad2 = pads[self.drop2_index]
        middle = pad1.between_pads[pad2]
        # l1 = drop1.liquid
        # l2 = drop2.liquid
        # def update(_) -> None:
        #     drop2.status = DropStatus.IN_MIX
        #     l1.mix_in(l2)
        #     pad2.drop = None
        #     drop1.pad = middle
        #     # print(f"Merged {[d for d in drops]}")

        pad1.schedule(Pad.TurnOff, post_result = False)
        pad2.schedule(Pad.TurnOff, post_result = False)
        return middle.schedule(Pad.TurnOn)   #.then_call(update)

    def split(self, pads: tuple[Pad,...]) -> Delayed[OnOff]:
        # print(f"Splitting {pads} ({[d for d in drops]})")
        # drop1 = drops[self.drop1_index]
        # drop2 = drops[self.drop2_index]
        pad1 = pads[self.drop1_index]
        pad2 = pads[self.drop2_index]
        middle = pad1.between_pads[pad2]
        # l1 = drop1.liquid
        # l2 = drop2.liquid
        # def update(_) -> None:
        #     l1.split_to(l2)
        #     drop2.status = DropStatus.ON_BOARD
        #     drop1.pad = pad1
        #     pad2.drop = drop2
        #     # print(f"Split {pads} ({[d for d in drops]})")
        pad1.schedule(Pad.TurnOn, post_result = False)
        pad2.schedule(Pad.TurnOn, post_result = False)
        return middle.schedule(Pad.TurnOff) #.then_call(update)


PM = PairwiseMix

class MixSequence(NamedTuple):
    error: float
    locations: Sequence[tuple[int,int]]
    steps: Sequence[Sequence[PairwiseMix]]
    fully_mixed: Sequence[int]
    size: tuple[int, int]
    lead_offset: tuple[int, int]

    @property
    def num_steps(self) -> int:
        return len(self.steps)

    @property
    def num_drops(self) -> int:
        return len(self.locations)

    @classmethod
    def run_script(cls, mixes: Sequence[Sequence[PairwiseMix]],
                   pads: tuple[Pad,...],
                   *,
                   n_shuttles: int = 0) -> Iterator[bool]:
        last_step = len(mixes)-1
        # pads = tuple(d.on_board_pad for d in drops)
        # We reserve the pads to make sure that nobody walks closer while
        # we're in a merge. We don't have to worry about contention, because we're
        # already sitting on the pad.
        for pad in pads:
            pad.reserve()
        for i, step in enumerate(mixes):
            for shuttle in range(n_shuttles+1):
                for mix in step:
                    mix.merge(pads)
                yield True
                for mix in step:
                    mix.split(pads)
                if i == last_step and shuttle == n_shuttles:
                    for pad in pads:
                        pad.unreserve()
                    yield False
                else:
                    yield True



    def iterator(self, pads: tuple[Pad, ...], n_shuttles: int) -> Iterator[bool]:
        return self.run_script(self.steps, pads, n_shuttles=n_shuttles)
        # last_step = len(self.steps)-1
        # pads = tuple(d.pad for d in drops)
        # for i, step in enumerate(self.steps):
        #     for shuttle in range(n_shuttles+1):
        #         for mix in step:
        #             mix.merge(drops)
        #         yield True
        #         for mix in step:
        #             mix.split(drops, pads)
        #         yield i<last_step or shuttle<n_shuttles
        #

    def transformed(self, transform: Transform) -> MixSequence:
        if transform is Transform.NONE:
            return self

        locs = tuple(transform.apply_to(x,y) for x,y in self.locations)
        lx = -min(x for x,y in locs)
        ly = -min(y for x,y in locs)
        sx,sy = self.size
        if transform.swap:
            sx,sy = sy,sx
        ms = MixSequence(self.error,
                         locs,
                           self.steps,
                           fully_mixed = self.fully_mixed,
                           size = (sx,sy),
                           lead_offset = (lx, ly)
                           )
        # print(f"{self} transformed {transform} is")
        # print(f"{ms}")
        return ms

    def placed(self, lead_drop_pad: Pad) -> PlacedMixSequence:
        return PlacedMixSequence(self, lead_drop_pad)

class Transform(Enum):
    x_neg: Final[bool]
    y_neg: Final[bool]
    swap: Final[bool]
    NONE = (False, False, False)
    CLOCKWISE = (True, False, True)
    COUNTERCLOCKWISE = (False, True, True)
    ONE_EIGHTY = (True, True, True)
    FLIP_X = (True, False, False)
    FLIP_Y = (False, True, False)

    def __init__(self, x_neg: bool, y_neg: bool, swap: bool) -> None:
        self.x_neg = x_neg
        self.y_neg = y_neg
        self.swap = swap
        # print(f"{self}(1,2) = {self(1,2)}")

    def __repr__(self) -> str:
        return f"Transform.{self.name}"

    def __call__(self, x: int, y: int) -> tuple[int,int]:
        if self.x_neg:
            x = -x
        if self.y_neg:
            y = -y
        return (y,x) if self.swap else (x,y)

    def apply_to(self, x: int, y: int) -> tuple[int,int]:
        if self.x_neg:
            x = -x
        if self.y_neg:
            y = -y
        return (y,x) if self.swap else (x,y)


class DropCombinationProcessType(MultiDropProcessType):
    mix_seq: Final[MixSequence]
    result: Final[Optional[Reagent]]
    n_shuttles: Final[int]

    @property
    def num_drops(self) -> int:
        return self.mix_seq.num_drops

    @property
    def num_steps(self) -> int:
        return self.mix_seq.num_steps

    def __init__(self, mix_seq: MixSequence, *,
                 result: Optional[Reagent] = None,
                 n_shuttles: int = 0) -> None:
        super().__init__(len(mix_seq.locations))
        self.mix_seq = mix_seq
        self.result = result
        self.n_shuttles = n_shuttles

    def secondary_pads(self, lead_drop_pad: Pad)->Sequence[Pad]:
        board = lead_drop_pad.board
        lead_loc = lead_drop_pad.location
        orientation = board.orientation
        return tuple(board.pads[orientation.up_right(lead_loc, 2*x, 2*y)]
                     for x,y in self.mix_seq.locations
                     if x!=0 or y!=0)

    # returns the finish function when done
    def iterator(self, pads: tuple[Pad, ...]) -> Iterator[Optional[FinishFunction]]:  # @UnusedVariable
        i = self.mix_seq.iterator(pads, self.n_shuttles)
        while next(i):
            yield None
        result = self.result
        fully_mixed = { pads[i] for i in self.mix_seq.fully_mixed }
        def finish(futures: MutableMapping[Pad, Postable[Drop]]) -> bool:  # @UnusedVariable
            printed = False
            for pad in pads:
                if pad in fully_mixed:
                    if not printed:
                        # print(f"Result is {drop.reagent}")
                        printed = True
                    if result is not None:
                        pad.checked_drop.reagent = result
                else:
                    pad.checked_drop.reagent = waste_reagent
            return True
        yield finish

class PlacedMixSequence:
    mix_seq: Final[MixSequence]
    lead_drop_pad: Final[Pad]
    _pads: Optional[Sequence[Pad]] = None
    _fully_mixed_pads: Optional[Sequence[Pad]] = None

    @property
    def num_drops(self) -> int:
        return self.mix_seq.num_drops

    @property
    def num_steps(self) -> int:
        return self.mix_seq.num_steps

    def __init__(self, mix_seq: MixSequence, lead_drop_pad: Pad) -> None:
        self.mix_seq = mix_seq
        self.lead_drop_pad = lead_drop_pad

    def _place(self, seq: Iterable[tuple[int, int]]) -> tuple[Pad, ...]:
        ldp = self.lead_drop_pad
        pad_array = ldp.board.pad_array
        orientation = ldp.board.orientation
        ldp_loc = ldp.location
        return tuple(pad_array[orientation.up_right(ldp_loc, 2*x,2*y)]
                     for x,y in seq)

    @property
    def pads(self) -> Sequence[Pad]:
        val = self._pads
        if val is None:
            val = self._pads = self._place(self.mix_seq.locations)
            # val = self._place(self.mix_seq.locations)
        return val


    @property
    def secondary_pads(self) -> Sequence[Pad]:
        return tuple(p for p in self.pads if p is not self.lead_drop_pad)


    @property
    def fully_mixed_pads(self) -> Sequence[Pad]:
        val = self._fully_mixed_pads
        if val is None:
            locs = self.mix_seq.locations
            val = self._fully_mixed_pads = self._place(locs[i] for i in self.mix_seq.fully_mixed)
        return val

    def as_process(self, *,
                   result: Optional[Reagent] = None,
                   n_shuttles: int = 0) -> DropCombinationProcessType:
        return DropCombinationProcessType(self.mix_seq, result=result,n_shuttles=n_shuttles)

class MSL_Cache_Key(NamedTuple):
    n: float
    fullp: bool
    tolerance: float
    rows: int
    cols: int

class MixSequenceLibrary:
    registered: Final[dict[float, list[MixSequence]]]
    cache: Final[dict[MSL_Cache_Key, MixSequence]]
    lock: Final[Lock]

    def __init__(self) -> None:
        self.registered = defaultdict(list)
        self.cache = {}
        self.lock = Lock()

    def register(self, n: float, mix_seq: MixSequence) -> None:
        with self.lock:
            self.registered[n].append(mix_seq)

    def lookup(self, n: float, *,
               full: bool,
               tolerance: float = 0.1,
               rows: int = sys.maxsize,
               cols: int = sys.maxsize,
               allow_best_match: bool = False,
               slop: float=1e-4) -> MixSequence:
        key = MSL_Cache_Key(n, full, tolerance, rows, cols)
        with self.lock:
            cached = self.cache.get(key, None)
            if cached is None:
                best: Optional[MixSequence] = None
                best_len: int = sys.maxsize
                rotate_best: bool = False
                for ms in self.registered[n]:
                    # If we want a full one, and this isn't, we go on to the next
                    if full and len(ms.fully_mixed) < len(ms.locations):
                        continue
                    c,r = ms.size
                    c = c*2-1
                    r = r*2-1
                    # if it won't fit into the region (even turned), we go on to the next
                    if (c>cols or r>rows) and (c>rows or r>cols):
                        continue
                    # if the error is too big and we don't allow best effort, we go on to the next
                    if ms.error > tolerance+slop and not allow_best_match:
                        continue
                    new_len = len(ms.steps)
                    if best is not None:
                        # if it's longer than the current best, skip it
                        if new_len > best_len:
                            continue
                        # if it's the same length, but doesn't have better error, skip it
                        if new_len == best_len and ms.error >= best.error:
                            continue
                    # if we've gotten here, either we didn't have a best before or the current
                    # one is better than the one we had

                    # if it doesn't fit as is, we have to rotate it
                    best = ms
                    rotate_best = (c>cols or r>rows)
                    best_len = new_len
                if best is None:
                    raise KeyError(f"No mixing sequence satisfying f{key}")
                if rotate_best:
                    best = best.transformed(Transform.CLOCKWISE)
                cached = self.cache[key] = best
            return cached
    def lookup_placed(self, n: float, *,
                      lower_left: Pad,
                      full: bool,
                      tolerance: float = 0.1,
                      rows: Optional[int] = None,
                      cols: Optional[int] = None,
                      allow_best_match: bool = False,
                      slop: float=1e-4
                      ) -> PlacedMixSequence:
        mix = self.lookup(n, full=full, tolerance=tolerance,
                          rows=sys.maxsize if rows is None else rows,
                          cols=sys.maxsize if cols is None else cols,
                          allow_best_match=allow_best_match,
                          slop=slop)
        pads = lower_left.board.pad_array
        width,height = (2*i-1 for i in mix.size)
        bx = 0 if cols is None else (cols-width)//2
        by = 0 if rows is None else (rows-height)//2
        orientation = lower_left.board.orientation
        lox,loy = (2*i for i in mix.lead_offset)
        lead_drop_pad = pads[orientation.up_right(lower_left.location, bx+lox, by+loy)]
        return mix.placed(lead_drop_pad)
