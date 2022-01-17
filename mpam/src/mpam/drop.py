from __future__ import annotations
from mpam.types import Liquid, Dir, Delayed, RunMode, DelayType,\
    Operation, OpScheduler, XYCoord, unknown_reagent, Ticks, tick,\
    StaticOperation, Reagent, Callback, T
from mpam.device import Pad, Board, Well, WellGroup, WellState, ExtractionPoint,\
    ProductLocation, ChangeJournal
from mpam.exceptions import NoSuchPad, NotAtWell
from typing import Optional, Final, Union, Callable, Iterator, Iterable,\
    Sequence, Mapping, NamedTuple
from quantities.dimensions import Volume
from enum import Enum, auto
from abc import ABC, abstractmethod
from erk.errors import FIX_BY, PRINT
from quantities.core import qstr
from erk.basic import not_None, ComputedDefaultDict, Count
from _collections import defaultdict
import math
from erk.stringutils import map_str

# if TYPE_CHECKING:
    # from mpam.processes import MultiDropProcessType
    
class Pull(NamedTuple):
    puller: Pad
    pullee: Pad
    
    @property
    def pinned(self) -> Pad:
        return self.puller
    @property
    def unpinned(self) -> Pad:
        return self.pullee
    
class MotionInference:
    changes: Final[ChangeJournal]
    pin_state: Final[Mapping[Pad, bool]]
    # pulls: Final[list[Pull]]
    
    def __init__(self, changes: ChangeJournal) -> None:
        self.changes = changes
        def compute_pin_state(pad: Pad) -> bool:
            blob = pad.blob
            return False if blob is None else blob.pinned
        pin_state = ComputedDefaultDict(compute_pin_state)
        for p in changes.turned_off:
            pin_state[p] = False
        for p in changes.turned_on:
            pin_state[p] = True
        self.pin_state = pin_state
        # self.pulls = []
        
    def process_changes(self) -> None:
        # When we come in, no blobs abut and every unpinned blob has content
        if self.changes.has_transfer:
            self.process_transfers()
        # The invariant still holds
        pulls: list[Pull] = []
        # First, we divide the changes into those that flip bits inside a blob and those that extend 
        # a blob or create a new (empty) one:
        n_flips = Count[Blob]()
        extensions: list[Pad] = []
        for pad in self.changes.turned_off:
            # If we're turning off a pad, it must've been in a blob
            blob = not_None(pad.blob)
            if n_flips[blob] < blob.size-1:
                n_flips[blob] += 1
            else:
                # The whole of the blob has been flipped, we can just change the pinned status in place.
                if blob.size > 1:
                    del n_flips[blob]
                if blob.total_volume > Volume.ZERO():
                    blob.pinned = False
                else:
                    # There's nothing there and all the pads have been turned off.
                    blob.disappear()
        for pad in self.changes.turned_on:
            if (maybe_blob := pad.blob) is None:
                # If it's not in an unpinned blob, we'll process it later as an extension.
                extensions.append(pad)
            else:
                blob = maybe_blob
                if n_flips[blob] < blob.size-1:
                    n_flips[blob] += 1
                else:
                    # The whole of the blob has been flipped, we can just change the pinned status in place.
                    if blob.size > 1:
                        del n_flips[blob]
                    blob.pinned = True
        # Now the keys of n_flips are just the blobs that have to be partitioned
        pin_state = self.pin_state
        for blob in n_flips.keys():
            blob.partition(pin_state, pulls)
        # The invariant still holds, but there may be elements in pulls.  Now we process any pads that were
        # turned on and hadn't been in a blob.  This will merge abutting pinned blobs and pull on abutting
        # unpinned blobs
        for pad in extensions:
            my_blob: Optional[Blob] = None
            for neighbor in pad.neighbors:
                if (maybe_blob := neighbor.blob) is not None:
                    # It may be that it will become not None on a later extension, but we'll get it there
                    blob = maybe_blob
                    if blob.unpinned:
                        pulls.append(Pull(pad, neighbor))
                    elif my_blob is None:
                        my_blob = blob.extend(pad)
                    else:
                        my_blob = blob.merge_in(my_blob)
            if my_blob is None:
                Blob((pad,), pinned = True)
        # Finally, we process the pulls.  This will restore the invariant
        if pulls:
            self.process_pulls(pulls)
        # Now we need to make sure that the extensions all have drops in them (if they're supposed to).
        # process_pull() will have stashed the pulled drops in the destinations, but we need to unstash
        # for the extensions or create if necessary
        for pad in extensions:
            blob = not_None(pad.blob)
            blob.ensure_drop(pad)
        # TODO: Any pad that was touched needs to have its drop volume/reagent updated.  I'm going 
        # to have to keep track of that somehow.
        
    def process_transfers(self) -> None:
        pulls: list[Pull] = []
        for pad,liquids in self.changes.delivered.items():
            maybe_blob = pad.blob
            if maybe_blob is None:
                # The pad delivered to isn't in a blob yet.
                for neighbor in pad.neighbors:   # TODO: Should this be all_neighbors?
                    neighbor_blob = neighbor.blob
                    if neighbor_blob is not None:
                        if neighbor_blob.pinned:
                            pulls.append(Pull(neighbor, pad))
                        else:
                            maybe_blob = neighbor_blob.merge_in(maybe_blob)
                if maybe_blob is None:
                    maybe_blob = Blob((pad,), pinned=False)
            blob: Blob = maybe_blob
            # update_drops.add(blob)
            for liquid in liquids:
                blob.contents.mix_in(liquid)
        blobs_to_delete: list[Blob] = []
        for pad,volume in self.changes.removed.items():
            blob = not_None(pad.blob)
            # update_drops.add(blob)
            assert blob.total_volume >= volume, f"Removed {volume} at {pad} from a blob containing {blob.contents}" 
            blob.contents.volume -= volume
            if blob.unpinned and blob.total_volume == Volume.ZERO():
                blobs_to_delete.append(blob)
        if pulls:
            self.process_pulls(pulls)
        for blob in blobs_to_delete:
            blob.disappear()
    
    def process_pulls(self, pulls: Sequence[Pull]) -> None:
        pull_pads: dict[tuple[Blob,Blob], list[Pad]] = defaultdict(list)
        pullers: dict[Blob,set[Blob]] = defaultdict(set)
        for pp,up in pulls:
            pb = not_None(pp.blob)
            assert pb.pinned
            ub = not_None(up.blob)
            assert ub.unpinned
            pull_pads[(pb,ub)].append(up)
            pullers[ub].add(pb)
        for ub,pb_set in pullers.items():
            pull_strength: dict[Blob, float] = {}
            if len(pb_set) == 1:
                pb, = tuple(pb_set)
                pb.contents.mix_in(ub.contents)
                # TODO: pb gets all of ub's drops
            else:
                for pb in pb_set: 
                    ups = pull_pads[(pb,ub)]
                    def dist2(x: int, y: int, p: Pad) -> int:
                        return (x-p.column)**2 + (y-p.row)**2
                    if len(ups) == 1:
                        up = ups[0]
                        ux = up.column
                        uy = up.row
                        strength = sum((1.0/dist2(ux,uy,p) for p in pb.pads), 0.0)
                    else:
                        strength = 0.0
                        for p in pb.pads:
                            px = p.column
                            py = p.row
                            s = min((1.0/dist2(px,py,up) for up in ups))
                            strength += s
                    pull_strength[pb] = strength
                total_pull_strength = math.fsum(pull_strength.values())
                r = ub.reagent
                v = ub.total_volume
                for pb,s in pull_strength.items():
                    fraction = s/total_pull_strength
                    liquid = Liquid(r, v*fraction)
                    pb.contents.mix_in(liquid)
            # TODO: pb gets drops from ub when it's closest
            ub.disappear()
    
    
class Blob:
    pads: Final[list[Pad]]
    pinned: bool
    contents: Liquid
    
    @property
    def size(self) -> int:
        return len(self.pads)
    
    @property
    def unpinned(self) -> bool:
        return not self.pinned
    
    @property
    def reagent(self) -> Reagent:
        return self.contents.reagent
    
    @property
    def total_volume(self) -> Volume:
        return self.contents.volume
    
    @property
    def per_pad_volume(self) -> Volume:
        n = self.size
        if n == 0:
            return Volume.ZERO()
        else:
            return self.total_volume/n 
        
    @property
    def is_singleton(self) -> bool:
        return self.size == 1
    
    @property
    def only_pad(self) -> Pad:
        assert self.size == 1
        for pad in self.pads:
            return pad
        assert False, "Somehow failed to enumerate singleton blob"
    
    @property
    def is_empty(self) -> bool:
        return self.size == 0 

    def __init__(self, pads: Iterable[Pad] = (), *,
                 pinned: bool,
                 set_pads: bool = True) -> None:
        self.pads = list(pads)
        self.pinned = pinned
        self.contents = Liquid(unknown_reagent, Volume.ZERO())
        if set_pads:
            for pad in pads:
                pad.blob = self
        
    def __str__(self) -> str:
        status = "pinned" if self.pinned else "unpinned"
        if self.total_volume == Volume.ZERO():
            cdesc = "empty"
        else:
            cdesc = str(self.contents)
            if self.size > 1:
                cdesc += f" ({self.per_pad_volume} each)"
        pads = map_str(self.pads)
        return f"Blob({status}, {cdesc}: {pads})"
        
    def merge_in(self, blob: Optional[Blob]) -> Blob:
        if blob is not None and blob is not self:
            for pad in blob.pads:
                pad.blob = self
            self.pads.extend(blob.pads)
            self.contents.mix_in(blob.contents)
        return self 
    
    def extend(self, pad: Pad) -> Blob:
        self.pads.append(pad)
        pad.blob = self
        return self
    
    def disappear(self) -> None:
        for pad in self.pads:
            pad.blob = None
        # TODO: update drops
        self.pads.clear()

    def ensure_drop(self, pad: Pad) -> None:
        # TODO: unstash a drop or create one
        ...
    
    @classmethod
    def process_changes(cls, changes: ChangeJournal, *, board: Board) -> None:
        mi = MotionInference(changes)
        mi.process_changes()
        return
        
    def partition(self, pin_state: Mapping[Pad, bool], pulls: list[Pull]) -> None:
        # We should only get here if fewer than all drops have changed.
        assert(not self.is_singleton)
        
        def expand(pad: Pad, blob: Blob, ps: bool):
            for n in pad.neighbors:
                if n.blob is self:
                    # When we partition, we still have a buffer between this blob and others,
                    # so if it's not self, we've already processed it
                    if ps == pin_state[n]:
                        blob.extend(n)
                        expand(n, blob, ps)
                    elif ps:
                        pulls.append(Pull(pad, n))
                    else:
                        # We have to account for both directions, since this pad's blob is no
                        # longer self
                        pulls.append(Pull(n, pad))
                        
        new_blobs: list[Blob] = []
        for pad in self.pads:
            # Every one whose blob is self when we look will be the seed of a new blob
            if pad.blob is self:
                ps = pin_state[pad]
                blob = Blob((pad,), pinned = ps)
                new_blobs.append(blob)
                expand(pad, blob, ps)
        # When we get here, every pad in this blob will have been migrated to some new blob.
        # We now need to partition the contents among them.
        my_size = float(self.size)
        reagent = self.reagent
        volume = self.total_volume
        for blob in new_blobs:
            fraction = blob.size/my_size
            blob.contents.reagent = reagent
            blob.contents.volume = volume*fraction
        
    
    # def partition_pinned(self, turned_off: set[Pad], pulling: set[Pad]) -> None:
    #     pads = self.pads
    #     n = len(pads)
    #     if n == 1:
    #         self.pinned = False
    #         return
    #     flipped = turned_off & pads
    #     if len(flipped) == n:
    #         # Everything's flipped.  This is now an unpinned set
    #         self.pinned = False
    #         return 
    #     pin_status = { p: p in flipped for p in pads}
    #
    #     def expand(pad: Pad, blob: Blob, ps: bool):
    #         for n in pad.neighbors:
    #             if n.blob is self:
    #                 # If it's not self, we've already processed it or it's not in the original blob
    #                 if ps == pin_status[n]:
    #                     blob.pads.add(n)
    #                     n.blob = blob
    #                     expand(n, blob, ps)
    #                 elif ps:
    #                     pulling.add(pad)
    #     for pad in pads:
    #         if pad.blob is self:
    #             ps = pin_status[pad]
    #             blob = Blob((pad,), pinned = ps)
    #             pad.blob = blob
    #             expand(pad, blob, ps)

class DropStatus(Enum):
    ON_BOARD = auto()
    IN_WELL = auto()
    IN_MIX = auto()
    OFF_BOARD = auto()
    
class MotionOp(Operation['Drop', 'Drop'], ABC):
    allow_unsafe: Final[bool]
    
    def __init__(self, *, allow_unsafe: bool):
        self.allow_unsafe = allow_unsafe
    
    @abstractmethod
    def dirAndSteps(self, drop: Drop) -> tuple[Dir, int]: ...  # @UnusedVariable
    def _schedule_for(self, drop: Drop, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      ) -> Delayed[Drop]:
        board = drop.pad.board
        system = board.in_system()
        
        direction, steps = self.dirAndSteps(drop)
        # allow_unsafe_motion = self.allow_unsafe_motion
        
        if drop.status is not DropStatus.ON_BOARD:
            print(f"Drop {drop} is not on board, cannot move {qstr(steps,'step')} {direction.name}")
            return Delayed.complete(drop)
        
        if steps == 0:
            return Delayed.complete(drop)
        future = Delayed[Drop]()
            
        one_tick: Ticks = 1*tick
        allow_unsafe = self.allow_unsafe
        assert mode.is_gated
        def before_tick() -> Iterator[Optional[Ticks]]:
            last_pad = drop.pad
            for i in range(steps):
                next_pad = last_pad.neighbor(direction)
                if next_pad is None or next_pad.broken:
                    raise NoSuchPad(board.orientation.neighbor(direction, last_pad.location))
                if not allow_unsafe:
                    while not next_pad.safe_except(last_pad):
                        # print(f"unsafe: {i} of {steps}, {drop}, lp = {last_pad}, np = {next_pad}")
                        yield one_tick
                while not next_pad.reserve():
                    if allow_unsafe:
                        break
                    yield one_tick
                with system.batched():
                    # print(f"Tick number {system.clock.next_tick}")
                    # print(f"Moving drop from {last_pad} to {next_pad}")
                    assert last_pad == drop.pad, f"{i} of {steps}, {drop}, lp = {last_pad}, np = {next_pad}"
                    next_pad.schedule(Pad.TurnOn, mode=mode, post_result=False)
                    last_pad.schedule(Pad.TurnOff, mode=mode, post_result=False)
                    board.after_tick(drop._update_pad_fn(last_pad, next_pad))
                    # print(f"i = {i}, steps = {steps}, drop = {drop}, lp = {last_pad}, np = {next_pad}")
                    if post_result and i == steps-1:
                        board.after_tick(lambda : future.post(drop))
                last_pad = next_pad
                if i < steps-1:
                    yield one_tick
            yield None
        iterator = before_tick()
        board.before_tick(lambda: next(iterator), delta=mode.gated_delay(after))
        return future
    
    
    
    

class Drop(OpScheduler['Drop']):
    liquid: Liquid
    _pad: Pad
    status: DropStatus
    
    @property
    def pad(self) -> Pad:
        return self._pad
    
    @pad.setter
    def pad(self, pad: Pad) -> None:
        old = self._pad
        # assert?
        if old.drop is self:
            old.drop = None
        self._pad = pad
        pad.drop = self
    
    @property
    def volume(self) -> Volume:
        return self.liquid.volume
    
    @volume.setter
    def volume(self, val: Volume) -> None:
        self.liquid.volume= val

    @property
    def reagent(self) -> Reagent:
        return self.liquid.reagent
    
    @reagent.setter
    def reagent(self, val: Reagent) -> None:
        self.liquid.reagent = val
    
    
    def __init__(self, pad: Pad, liquid: Liquid, *,
                 status: DropStatus = DropStatus.ON_BOARD) -> None:
        assert pad.drop is None, f"Trying to create a second drop at {pad}"
        self.liquid = liquid
        self._pad = pad
        self.status = status
        if status is DropStatus.ON_BOARD:
            pad.drop = self
        
    def __repr__(self) -> str:
        st = self.status
        place = f"{st.name}: " if st is not DropStatus.ON_BOARD else ""
        return f"Drop[{place}{self.pad}, {self.liquid}]"
    
    def schedule_communication(self, cb: Callable[[], Optional[Callback]], mode: RunMode, *,  
                               after: Optional[DelayType] = None) -> None:  
        self.pad.schedule_communication(cb, mode=mode, after=after)
        
    def delayed(self, function: Callable[[], T], *,
                after: Optional[DelayType]) -> Delayed[T]:
        return self.pad.delayed(function, after=after)
        
    
    
    # @classmethod
    # def appear_at(cls, board: Board, locations: Sequence[Union[XYCoord, tuple[int, int]]],
    #              liquid: Liquid = Liquid(unknown_reagent, 0.5*uL) 
    #              ) -> Delayed[Sequence[Drop]]:
    #     locs = ((loc.x, loc.y) if isinstance(loc, XYCoord) else loc for loc in locations)
    #     drops = tuple(Drop(board.pad_at(x,y), liquid) for (x, y) in locs)
    #     future = Delayed[Sequence[Drop]]()
    #     system = board.system
    #     assert system is not None
    #     outstanding: int = len(drops)
    #     lock = Lock()
    #     def join(_) -> None:
    #         # print("joining")
    #         with lock:
    #             nonlocal outstanding
    #             outstanding -= 1
    #             if outstanding == 0:
    #                 future.post(drops)
    #     with system.batched():
    #         for drop in drops:
    #             drop.pad.schedule(Pad.TurnOn).when_value(join)
    #     return future
        
    class AppearAt(StaticOperation['Drop']):
        pad: Final[Pad]
        liquid: Final[Liquid]
        
        def __init__(self, pad: Union[Pad, XYCoord, tuple[int, int]], *, 
                     board: Board,
                     liquid: Optional[Liquid] = None,
                     ) -> None:
            if isinstance(pad, XYCoord):
                pad = board.pad_array[pad]
            elif isinstance(pad, tuple):
                pad = board.pad_at(pad[0], pad[1])
            self.pad = pad
            if liquid is None:
                liquid = Liquid(unknown_reagent, board.drop_size)
            self.liquid = liquid
            
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  
                      ) -> Delayed[Drop]:
            future = Delayed[Drop]()
            assert mode.is_gated
            pad = self.pad
            def make_drop(_) -> None:
                drop = Drop(pad=pad, liquid=self.liquid)
                pad.board.change_journal.note_delivery(pad, self.liquid)
                if post_result:
                    future.post(drop)
            pad.schedule(Pad.TurnOn, mode=mode, after=after) \
                .then_call(make_drop)
            return future
            
    class TeleportInTo(StaticOperation['Drop']):
        extraction_point: Final[ExtractionPoint]
        liquid: Final[Liquid]
        mix_result: Final[Optional[Union[Reagent,str]]]
        def __init__(self, extraction_point: ExtractionPoint, *,
                     liquid: Optional[Liquid] = None, 
                     reagent: Optional[Reagent] = None,
                     mix_result: Optional[Union[Reagent,str]] = None,
                     ) -> None:
            self.extraction_point = extraction_point
            board = extraction_point.pad.board 
            if liquid is None:
                if reagent is None:
                    reagent = unknown_reagent
                liquid = Liquid(reagent, board.drop_size)
            self.liquid = liquid
            self.mix_result = mix_result
            
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  
                      ) -> Delayed[Drop]:
            liquid = self.liquid
            op = ExtractionPoint.TransferIn(liquid.reagent, liquid.volume, mix_result=self.mix_result)
            return self.extraction_point.schedule(op, mode=mode, after=after, post_result=post_result)
    
    class TeleportOut(Operation['Drop', None]):
        volume: Final[Optional[Volume]]
        product_loc: Final[Optional[Delayed[ProductLocation]]]
        
        def __init__(self, *,
                     volume: Optional[Volume],
                     product_loc: Optional[Delayed[ProductLocation]] = None
                     ) -> None:
            self.volume = volume
            self.product_loc = product_loc
            
        def _schedule_for(self, drop: Drop, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  # @UnusedVariable
                      ) -> Delayed[None]:
            op = ExtractionPoint.TransferOut(volume=self.volume, product_loc=self.product_loc)
            future = Delayed[None]()
            
            def do_it() -> None:
                ep = drop.pad.extraction_point
                assert ep is not None, f"{drop} is not at an extraction point"
                ep.schedule(op).then_call(lambda _: future.post(None))
            drop.pad.delayed(do_it, after=after)
            return future

    class Move(MotionOp):
        direction: Final[Dir]
        steps: Final[int]
        
        def __repr__(self) -> str:
            return f"<Drop.Move: {self.steps} {self.direction}>"
        
        def __init__(self, direction: Dir, *, steps: int = 1, 
                     allow_unsafe: bool = False) -> None:
            super().__init__(allow_unsafe=allow_unsafe)
            self.direction = direction
            self.steps = steps
            
        def dirAndSteps(self, drop: Drop)->tuple[Dir, int]:  # @UnusedVariable
            if self.steps >= 0:
                return self.direction, self.steps
            else:
                return self.direction.opposite, -self.steps
            
    class ToCol(MotionOp):
        col: Final[int]
        
        def __repr__(self) -> str:
            return f"<Drop.ToCol: {self.col}>"

        def __init__(self, col: int, *, allow_unsafe: bool = False) -> None:
            super().__init__(allow_unsafe=allow_unsafe)
            self.col = col
            
        def dirAndSteps(self, drop: Drop)->tuple[Dir, int]:
            pad = drop.pad
            direction = pad.board.orientation.pos_x
            current = pad.column
            steps = self.col-current
            return (direction, steps) if steps >=0 else (direction.opposite, -steps)
            
    class ToRow(MotionOp):
        row: Final[int]
        
        def __repr__(self) -> str:
            return f"<Drop.ToRow: {self.row}>"

        def __init__(self, row: int, *, allow_unsafe: bool = False) -> None:
            super().__init__(allow_unsafe=allow_unsafe)
            self.row = row
            
        def dirAndSteps(self, drop: Drop)->tuple[Dir, int]:
            pad = drop.pad
            direction = pad.board.orientation.pos_y
            current = pad.row
            steps = self.row-current
            return (direction, steps) if steps >=0 else (direction.opposite, -steps)
            
            
         
            
    class DispenseFrom(StaticOperation['Drop']):
        well: Final[Well]
        volume: Final[Optional[Volume]]
        reagent: Final[Optional[Reagent]]
        empty_wrong_reagent: Final[bool]
        
        def _schedule(self, *,
                      mode: RunMode = RunMode.GATED, 
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  
                      ) -> Delayed[Drop]:
            future = Delayed[Drop]()
            well = self.well
            pad = self.well.exit_pad
            volume = self.volume if self.volume is not None else well.dispensed_volume
            def make_drop(_) -> None:
                liquid = well.transfer_out(volume)
                drop = Drop(pad=pad, liquid=liquid)
                well.gate_reserved = False
                pad.reserved = False
                if post_result:
                    future.post(drop)
                    
            # The guard will be iterated when the motion is started, after any delay, but before the created
            # WellMotion tries to either get adopted by an in-progress motion or make changes on the well pads.
            def guard() -> Iterator[bool]:
                # First, we reserve the gate.  If there's a dispense in progress for this well, it will already have
                # the gate reserved, and we will spin until it's done.
                while not well.reserve_gate():
                    yield True
                # Next, we make sure that there's enough of the right reagent for us.
                def empty_first() -> None:
                    well.remove(well.volume)
                mismatch_behavior = FIX_BY(empty_first) if self.empty_wrong_reagent else PRINT
                f = well.ensure_content(volume=volume, reagent=self.reagent,
                                        on_reagent_mismatch=mismatch_behavior)
                while not f.has_value:
                    yield True
                # Finally, we wait until we can safely reserve the exit pad
                while not pad.safe_except(well):
                    yield True
                while not pad.reserve():
                    yield True
                yield False
                
                
            def run_group(_) -> None:
                # Note, we post the drop as soon as we get to the DISPENSED state, even theough
                # we continue on to READY
                group = self.well.group
                group.schedule(WellGroup.TransitionTo(WellState.DISPENSED, well = self.well, guard=guard()), 
                               mode=mode, after=after) \
                    .then_call(make_drop) \
                    .then_schedule(WellGroup.TransitionTo(WellState.READY))
            # well.ensure_content().then_call(run_group)
            run_group(None)
            return future
            
        
        def __init__(self, well: Well, *,
                     volume: Optional[Volume] = None,
                     reagent: Optional[Reagent] = None,
                     empty_wrong_reagent: bool = False) -> None:
            self.well = well
            self.volume = volume
            self.reagent = reagent
            self.empty_wrong_reagent = empty_wrong_reagent
            
    class EnterWell(Operation['Drop',None]):
        well: Final[Optional[Well]]
        empty_wrong_reagent: Final[bool]
        
        def __repr__(self) -> str:
            return f"<Drop.EnterWell: {self.well}>"
        
        def _schedule_for(self, drop: Drop, *,
                          mode: RunMode = RunMode.GATED, 
                          after: Optional[DelayType] = None,
                          post_result: bool = True,  
                          ) -> Delayed[None]:
            future = Delayed[None]()
            if self.well is None:
                if drop.pad.well is None:
                    raise NotAtWell(f"{drop} not at a well")
                well = drop.pad.well
            else:
                well = self.well
            def consume_drop(_) -> None:
                well.transfer_in(drop.liquid)
                drop.status = DropStatus.IN_WELL
                drop.pad.drop = None
                if post_result:
                    future.post(None)
                    
            # The guard will be iterated when the motion is started, after any delay, but before the created
            # WellMotion tries to either get adopted by an in-progress motion or make changes on the well pads.
            def guard() -> Iterator[bool]:
                # Unlike with dispensing, we don't need to reserve the pad, because there's a drop there, which
                # will keep anybody from trying to walk to it.

                # We, do, however, need to make sure that there's room for the drop and that the well can hold
                # the drop's reagent
                def empty_first() -> None:
                    well.remove(well.volume)
                mismatch_behavior = FIX_BY(empty_first) if self.empty_wrong_reagent else PRINT
                f = well.ensure_space(volume=drop.volume, reagent=drop.reagent,
                                        on_reagent_mismatch=mismatch_behavior)
                while not f.has_value:
                    yield True
                yield False
                
            # Note, we post the drop as soon as we get to the DISPENSED state, even theough
            # we continue on to READY
            group = well.group
            group.schedule(WellGroup.TransitionTo(WellState.ABSORBED, well=well, guard=guard()), mode=mode, after=after) \
                .then_call(consume_drop) \
                .then_schedule(WellGroup.TransitionTo(WellState.READY, well=well))
            return future
            
        
        def __init__(self, well: Optional[Well] = None, *,
                     empty_wrong_reagent: bool = False) -> None:
            self.well = well
            self.empty_wrong_reagent = empty_wrong_reagent
        
            
        
    def _update_pad_fn(self, from_pad: Pad, to_pad: Pad):
        def fn() -> None:
            assert from_pad.drop is self, f"Moved {self}, but thought it was at {from_pad}"
            assert to_pad.drop is None, f"Moving {self} to non-empty {to_pad}"
            # print(f"Moved drop from {from_pad} to {to_pad}")
            self.pad = to_pad
            to_pad.reserved = False
            # print(f"Drop now at {to_pad}")
        return fn
    

