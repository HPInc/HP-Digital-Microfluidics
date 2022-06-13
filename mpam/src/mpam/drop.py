from __future__ import annotations

from _collections import defaultdict
from abc import ABC, abstractmethod
from enum import Enum, auto
import math
from typing import Optional, Final, Union, Callable, Iterator, Iterable, \
    Sequence, Mapping, NamedTuple, cast
import logging

from erk.basic import not_None, ComputedDefaultDict, Count
from erk.errors import FIX_BY, PRINT
from erk.stringutils import map_str
from mpam.device import Pad, Board, Well, WellState, ExtractionPoint, \
    ProductLocation, ChangeJournal, DropLoc, WellPad, LocatedPad
from mpam.exceptions import NoSuchPad, NotAtWell
from mpam.types import Liquid, Dir, Delayed, DelayType, \
    Operation, OpScheduler, XYCoord, unknown_reagent, Ticks, tick, \
    StaticOperation, Reagent, Callback, T, MixResult, Postable
from quantities.core import qstr
from quantities.dimensions import Volume

logger = logging.getLogger(__name__)


# if TYPE_CHECKING:
    # from mpam.processes import MultiDropProcessType
class Pull(NamedTuple):
    puller: DropLoc
    pullee: DropLoc

    @property
    def pinned(self) -> DropLoc:
        return self.puller
    @property
    def unpinned(self) -> DropLoc:
        return self.pullee


class MotionInference:
    changes: Final[ChangeJournal]
    pin_state: Final[Mapping[DropLoc, bool]]
    need_drop_update: Final[set[Blob]]

    def __init__(self, changes: ChangeJournal) -> None:
        self.changes = changes
        def compute_pin_state(pad: DropLoc) -> bool:
            blob = pad.blob
            return False if blob is None else blob.pinned
        pin_state = ComputedDefaultDict(compute_pin_state)
        for p in changes.turned_off:
            pin_state[p] = False
        for p in changes.turned_on:
            pin_state[p] = True
        self.pin_state = pin_state
        self.need_drop_update = set()

    def process_changes(self) -> None:
        # When we come in, no blobs abut and every unpinned blob has content
        if self.changes.has_transfer:
            self.process_transfers()
        # The invariant still holds
        pulls: list[Pull] = []
        # First, we divide the changes into those that flip bits inside a blob and those that extend
        # a blob or create a new (empty) one:
        n_flips = Count[Blob]()
        extensions: list[DropLoc] = []
        for pad in self.changes.turned_off:
            # If we're turning off a pad, it must've been in a blob
            blob = not_None(pad.blob)
            if n_flips[blob] < blob.size-1:
                n_flips[blob] += 1
            else:
                # The whole of the blob has been flipped, we can just change the pinned status in place.
                if blob.size > 1:
                    del n_flips[blob]
                if blob.total_volume.is_positive:
                    blob.pinned = False
                    # If it was a gate blob attached to the well, we detach
                    if blob.well is not None and blob.has_gate:
                        blob.detach_from_well()
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
            self.need_drop_update.add(blob)
        # The invariant still holds, but there may be elements in pulls.  Now we process any pads that were
        # turned on and hadn't been in a blob.  This will merge abutting pinned blobs and pull on abutting
        # unpinned blobs
        for pad in extensions:
            my_blob: Optional[Blob] = None
            for neighbor in pad.neighbors_for_blob:
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
                my_blob = Blob((pad,), pinned = True, well_from = pad)
            self.need_drop_update.add(my_blob)
        # Finally, we process the pulls.  This will restore the invariant
        if pulls:
            self.process_pulls(pulls)
        for blob in self.need_drop_update:
            if not blob.is_empty:
                # update_drops() will unstash or create drops for pads that don't have them.
                blob.update_drops()

    def process_transfers(self) -> None:
        pulls: list[Pull] = []
        blobs_to_delete: list[Blob] = []
        for pad,liquids in self.changes.delivered.items():
            maybe_blob = pad.blob
            if maybe_blob is None:
                # The pad delivered to isn't in a blob yet.
                for neighbor in pad.neighbors_for_blob:
                    neighbor_blob = neighbor.blob
                    if neighbor_blob is not None:
                        if neighbor_blob.pinned:
                            pulls.append(Pull(neighbor, pad))
                        else:
                            maybe_blob = neighbor_blob.merge_in(maybe_blob)
                if maybe_blob is None:
                    maybe_blob = Blob((pad,), pinned=False, well_from = pad)
            blob: Blob = maybe_blob
            self.need_drop_update.add(blob)
            for liquid in liquids:
                blob.mix_in(liquid, mix_result=self.changes.mix_result.get(pad, None))
            # If there's only one inner well pad and it's this pad, then we
            # created the blob, but we really don't want it, so we'll let it go.
            # (If we keep it around, it will have volume and the next time we
            # transfer into it, we'll get the wrong amount.)
            if blob.n_inner_well_pads == 1 and blob.pads[0] is pad:
                blobs_to_delete.append(blob)
        for pad,volume in self.changes.removed.items():
            if pad.blob is None:
                # If we get here without a blob, this must be an internal well gate that
                # wasn't next to a blob.  So we just take the liquid out of the well
                assert isinstance(pad, WellPad) and not pad.is_gate
                well = pad.well
                well.transfer_out(volume)
            else:
                blob = pad.blob
                # update_drops.add(blob)
                assert blob.total_volume >= volume, f"Removed {volume} at {pad} from a blob containing {blob.contents}"
                blob.contents.volume -= volume
                if blob.unpinned and blob.total_volume.is_zero:
                    blobs_to_delete.append(blob)
                else:
                    self.need_drop_update.add(blob)
        if pulls:
            self.process_pulls(pulls)
        for blob in blobs_to_delete:
            blob.disappear()

    def process_pulls(self, pulls: Sequence[Pull]) -> None:
        pull_pads: dict[tuple[Blob,Blob], list[DropLoc]] = defaultdict(list)
        pullers: dict[Blob,set[Blob]] = defaultdict(set)
        for pp,up in pulls:
            # print(f"Pulling {up} to {pp}")
            pb = not_None(pp.blob)
            assert pb.pinned
            ub = not_None(up.blob)
            assert ub.unpinned
            pull_pads[(pb,ub)].append(up)
            pullers[ub].add(pb)
            # If the pulling pad is empty and the pulled pad isn't, we can move
            # the drop over. If this is the case, we don't need to update the
            # drop in the pulling blob if both blobs are singletons since the
            # drop will already have the full volume unless something else goes
            # into the pulling blob (in which case, it will get added then).
            if pp.drop is None and up.drop is not None:
                up.drop.pad = pp
                if not (pb.is_singleton and ub.is_singleton):
                    self.need_drop_update.add(pb)
            else:
                self.need_drop_update.add(pb)

        for ub,pb_set in pullers.items():
            # If the blob is attached to the well, we detach it.  This will keep
            # it from refilling when we move its contents in.  We keep track of
            # what it was to condition on whether to draw from it.
            well = ub.well
            if well is not None and ub.has_gate:
                ub.detach_from_well()

            preserve_unpinned = False

            if len(pb_set) == 1:
                # If everything goes one place, we don't have to split.  If this
                # is pulling to a blob tied to a well, it will add to the well
                # (and maybe pull out to the gate).  If it's pulling an
                # internal-only blob to a blob with a gate, we do an explicit
                # pull from the well.  If there's anything left in the well, we
                # assume (since nothing else is pulling on ub) that it's still
                # sitting there, and so we attach the puller.  However, if the
                # puller also has an internal pad, we defer to it.
                pb, = tuple(pb_set)
                if well is not None and pb.has_gate and not pb.has_inner_well_pad:
                    pb.pull_from_well(well)
                    if well.volume.is_positive:
                        pb.attach_to_well(well)
                        preserve_unpinned = True
                else:
                    pb.mix_in(ub.contents)
            elif well is not None and not ub.has_gate:
                # If we're splitting an internal-only blob, we simply let any
                # non-internal with-gate blob take what it needs.
                for pb in pb_set:
                    if pb.well is None and pb.has_gate:
                        pb.pull_from_well(well)
                        # There can only be one of these.
                        break
            else:
                pull_strength: dict[Blob, float] = {}

                def dist2(x: int, y: int, p: Pad) -> int:
                    return (x-p.column)**2 + (y-p.row)**2


                for pb in pb_set:
                    if pb.has_inner_well_pad and ub.has_gate:
                        # An internal blob pulls on a gate blob with strength
                        # one, no matter the size.  This is almost certainly
                        # wrong, but we'll go with it for now.
                        assert ub.has_gate
                        pull_strength[pb] = 1.0
                        continue

                    # At this point, both pb and ub have either a gate or a
                    # board pad.  We'll just ignore inner pads when computing
                    # strength (this may not be right.

                    def compute_strength(u: LocatedPad, p: DropLoc) -> float:
                        if not isinstance(p, LocatedPad):
                            return 0.0
                        dist2 = (u.column-p.column)**2 + (u.row-p.row)**2
                        return 1.0/dist2

                    ups = pull_pads[(pb,ub)]
                    # By construction, everything in ups is either a pad or a gate.

                    if len(ups) == 1:
                        up = ups[0]
                        assert isinstance(up, LocatedPad)
                        strength = sum((compute_strength(up, p) for p in pb.pads), 0.0)
                    else:
                        strength = 0.0
                        for p in pb.pads:
                            if not isinstance(p, LocatedPad):
                                # We don't worry about pull contributions from internal pads
                                continue
                            s = min(compute_strength(cast(LocatedPad, up), p) for up in ups)
                            assert s > 0.0
                            strength += s
                    assert strength > 0.0
                    pull_strength[pb] = strength
                total_pull_strength = math.fsum(pull_strength.values())
                r = ub.reagent
                v = ub.total_volume
                for pb,s in pull_strength.items():
                    fraction = s/total_pull_strength
                    liquid = Liquid(r, v*fraction)
                    pb.mix_in(liquid)
            # print(f"{preserve_unpinned}: {ub}")
            if not preserve_unpinned:
                ub.disappear()


class Blob:
    pads: Final[list[DropLoc]]
    pinned: bool
    contents: Liquid
    well: Optional[Well] = None
    n_inner_well_pads: int = 0
    has_board_pad: bool = False
    has_gate: bool = False
    _in_pull: bool = False
    pull_key: Final[str] = "Pull to blob"
    attachment_attr: Final[str] = "_attached_blob"
    attached_to_well: bool = False

    @property
    def has_inner_well_pad(self) -> bool:
        return self.n_inner_well_pads > 0

    @property
    def n_display_pads(self) -> int:
        return len(self.pads) - self.n_inner_well_pads

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
        n = self.n_display_pads
        if n == 0:
            return Volume.ZERO
        else:
            return self.total_volume/n

    @property
    def is_singleton(self) -> bool:
        return self.size == 1

    @property
    def only_pad(self) -> DropLoc:
        assert self.size == 1
        for pad in self.pads:
            return pad
        assert False, "Somehow failed to enumerate singleton blob"

    @property
    def is_empty(self) -> bool:
        return self.size == 0

    def __init__(self, pads: Iterable[DropLoc] = (), *,
                 pinned: bool,
                 well: Optional[Well] = None,
                 well_from: Optional[DropLoc] = None,
                 set_pads: bool = True) -> None:
        self.pads = list(pads)
        if well_from is not None:
            well = well_from.well if (isinstance(well_from, WellPad)
                                      and well_from is not well_from.well.gate) else None
        self.well = well
        for pad in pads:
            self.note_pad(pad)
        self.pinned = pinned
        self.contents = Liquid(unknown_reagent, Volume.ZERO)
        if well is not None and self.has_gate:
            self.pull_from_well()
            self.attach_to_well()
        if set_pads:
            for pad in pads:
                pad.blob = self

    def __repr__(self) -> str:
        status = "pinned" if self.pinned else "unpinned"
        if self.total_volume.is_zero:
            cdesc = "empty"
        else:
            cdesc = str(self.contents)
            if self.size > 1:
                cdesc += f" ({self.per_pad_volume} each)"
        pads = map_str(self.pads)
        wdesc = f", {self.well}" if self.well is not None else ""
        return f"Blob({status}, {cdesc}: {pads}{wdesc})"

    def note_pad(self, pad: DropLoc) -> None:
        if isinstance(pad, WellPad):
            well = self.well
            assert well is None or well is pad.well, f"Adding {pad} to {self}, which has pads from {well}"
            if pad.is_gate:
                self.has_gate = True
            else:
                self.n_inner_well_pads += 1
        else:
            self.has_board_pad = True

    def attach_to_well(self, well: Optional[Well] = None) -> None:
        if well is None:
            well = self.well
        else:
            self.well = well
        assert well is not None
        attr = self.attachment_attr
        old: Optional[Blob] = getattr(well, attr, None)
        if old is not None:
            old.attached_to_well = False
        self.attached_to_well = True
        setattr(well, attr, self)
        well.on_liquid_change(lambda _old,_new: self.pull_from_well(), key=Blob.pull_key)


    def detach_from_well(self) -> None:
        well = self.well
        assert well is not None
        setattr(well, self.attachment_attr, None)
        self.attached_to_well = False
        well.on_liquid_change.remove(Blob.pull_key)
        self.well = None


    def pull_from_well(self, well: Optional[Well] = None) -> None:
        # We need to be careful here.  If we wind up taking something out of the
        # well, that will change its contents, which will trigger a new call. So
        # we give ourselves a flag to prevent a loop.  For now, I'm not worried
        # about locking.  This might be a mistake.
        if self._in_pull:
            return
        well = well or self.well
        assert well is not None
        # We don't bother an empty well
        if well.volume.is_positive:
            desired = self.n_display_pads*well.dispensed_volume-self.total_volume
            # The only way we go down is when we partition, and that's a new blob.
            assert not desired.is_negative
            if desired.is_positive:
                # At this point, either we're doing an initial pull or we've already
                # mixed our content into the well, so the reagents should match.
                assert self.total_volume.is_zero or self.reagent is well.reagent
                self._in_pull = True
                try:
                    got = well.transfer_out(desired)
                finally:
                    self._in_pull = False
                self.contents.mix_in(got)
                self.update_drops()


    def drop_in(self, pad: DropLoc) -> Drop:
        return Drop(pad, Liquid(self.reagent, self.per_pad_volume))

    def remove_drops(self) -> None:
        # print(f"Removing drops in {self}")
        for pad in self.pads:
            if (drop := pad.drop) is not None:
                # print(f"  Removing drop at {pad}")
                drop.status = DropStatus.OFF_BOARD
                pad.drop = None
            else:
                # print(f"  {pad} has no drop")
                pass


    def update_drops(self) -> None:
        reagent = self.reagent
        volume = self.per_pad_volume
        if volume.is_zero:
            self.remove_drops()
        else:
            for pad in self.pads:
                drop = pad.drop or self.drop_in(pad)
                liquid = drop._display_liquid
                liquid.reagent = reagent
                liquid.volume = volume



    def die(self) -> None:
        self.pads.clear()
        # if self.has_gate and self.well is not None:
        #     self.detach_from_well()

    def mix_in(self, liquid: Liquid, mix_result: Optional[MixResult] = None) -> None:
        if liquid.volume.is_positive:
            well = self.well
            if well is None:
                self.contents.mix_in(liquid, result = mix_result)
            else:
                self.contents.mix_in(liquid)
                if self.total_volume.is_positive or mix_result is not None:
                    # If we've got a well and there's something.  If we're attached to the well,
                    # this will clear our contents and then trigger it coming out again.
                    well.transfer_in(self.contents, mix_result=mix_result)

    def merge_in(self, blob: Optional[Blob]) -> Blob:
        if blob is not None and blob is not self:
            for pad in blob.pads:
                pad.blob = self
            self.pads.extend(blob.pads)
            self.mix_in(blob.contents)

            if blob.has_board_pad:
                self.has_board_pad = True
            if blob.has_gate:
                self.has_gate = True
            n = blob.n_inner_well_pads
            if n > 0:
                self.n_inner_well_pads += n
            if blob.well is not self.well:
                well = blob.well or self.well
                assert well is not None

                if not self.attached_to_well:
                    # Either (1) one of the two of us is an untied blob with a
                    # gate and the other is an internal-only blob or (2) we're a
                    # board-pad-only blob and it's a tied blob with a gate.  In
                    # either case, we attach ourselves, which will detach them
                    # if they were attached.
                    self.attach_to_well(well)

                # Otherwise, we were the attached blob and they just have board
                # pads.

                # If we have content, we mix it into the well.  If we're
                # attached at this point, this will have the effect of pulling
                # out the right amount.
                if self.total_volume.is_positive:
                    well.transfer_in(self.contents)
                # Otherwise, we're empty to start, but we might still want to pull some out.
                elif self.has_gate and well.volume.is_positive:
                    self.pull_from_well()
            blob.die()
        return self

    def extend(self, pad: DropLoc) -> Blob:
        self.pads.append(pad)
        pad.blob = self
        self.note_pad(pad)
        well = self.well
        if well is not None:
            if pad is well.gate:
                # If we're adding the gate to a pad already tied to a well, we
                # attach the pull and pull liquid.
                self.attach_to_well()
                self.pull_from_well()
            elif isinstance(pad, Pad):
                # If we're extending a pad, we necessarily have the gate, so
                # we just pull to cover.
                assert self.has_gate
                self.pull_from_well()
        return self

    def disappear(self) -> None:
        # print(f"Disappearing {self}")
        self.remove_drops()
        for pad in self.pads:
            pad.blob = None
        self.die()

    @classmethod
    def process_changes(cls, changes: ChangeJournal) -> None:
        mi = MotionInference(changes)
        mi.process_changes()
        return

    def partition(self, pin_state: Mapping[DropLoc, bool], pulls: list[Pull]) -> None:
        # We should only get here if fewer than all drops have changed.
        assert(not self.is_singleton)

        has_volume = self.total_volume.is_positive
        well = self.well

        def expand(pad: DropLoc, blob: Blob, ps: bool):
            for n in pad.neighbors_for_blob:
                if n.blob is self:
                    # When we partition, we still have a buffer between this blob and others,
                    # so if it's not self, we've already processed it
                    if ps == pin_state[n]:
                        blob.extend(n)
                        expand(n, blob, ps)
                    elif has_volume or (well is not None and well.volume > 0):
                        # If there's no volume (i.e., we're partitioning a
                        # pinned empty blob), there's nothing to pull, so we
                        # don't bother unless we're tied to the well.  (We leave
                        # that there so that unpinned internal blobs pulled only
                        # by internal blobs disappear.)
                        if ps:
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

        # We now need to partition the contents among them.  If we're attached
        # to a well, the fluid will be pulled out to the display pads (pads and
        # gate), if any, so we split blobs by fraction of display pads.
        my_size = float(self.n_display_pads)
        # If we have volume, we must have display pads
        assert my_size > 0 or not has_volume
        reagent = self.reagent
        volume = self.total_volume
        need_to_detach = well is not None and self.has_gate
        for blob in new_blobs:
            if blob.has_inner_well_pad:
                if well is not None:
                    blob.well = well
                    if blob.has_gate:
                        # This attaches to the well (and detaches us), but doesn't
                        # draw.  The blob will get it's contents normally.
                        blob.attach_to_well()
                        need_to_detach = False
                elif not blob.has_gate:
                    # We've split off an internal-only blob, so we need to find
                    # the well.
                    pad = blob.pads[0]
                    assert isinstance(pad, WellPad)
                    blob.well = pad.well
            if has_volume:
                fraction = blob.n_display_pads/my_size
                if fraction > 0:
                    blob.contents.reagent = reagent
                    blob.contents.volume = volume*fraction
            elif blob.unpinned and blob.well is None:
                blob.disappear()
        if need_to_detach:
            self.detach_from_well()
        self.die()


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
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      ) -> Delayed[Drop]:
        assert isinstance(drop.pad, Pad), f"{drop} not on board.  Can't create MotionOp {self}"
        board = drop.pad.board
        system = board.system

        direction, steps = self.dirAndSteps(drop)
        # allow_unsafe_motion = self.allow_unsafe_motion

        # if after is None:
        #     logger.debug(f'direction:{direction}|steps:{steps}')
        # else:
        #     logger.debug(f'direction:{direction}|steps:{steps}|after:{after}')

        if drop.status is not DropStatus.ON_BOARD:
            logger.warning(f"Drop {drop} is not on board, cannot move {qstr(steps,'step')} {direction.name}")
            return Delayed.complete(drop)

        if steps == 0:
            return Delayed.complete(drop)
        future = Postable[Drop]()

        one_tick: Ticks = 1*tick
        allow_unsafe = self.allow_unsafe
        def before_tick() -> Iterator[Optional[Ticks]]:
            last_pad = cast(Pad, drop.pad)
            for i in range(steps):
                next_pad = last_pad.neighbor(direction)
                if next_pad is None or next_pad.broken:
                    raise NoSuchPad(board.orientation.neighbor(direction, last_pad.location))
                if not allow_unsafe:
                    while not next_pad.safe_except(last_pad):
                        # logger.debug(f"unsafe:{i} of {steps}|{drop}|lp:{last_pad}|np:{next_pad}")
                        yield one_tick
                while not next_pad.reserve():
                    if allow_unsafe:
                        break
                    # logger.debug(f"can't reserve:{i} of {steps}|{drop}|lp:{last_pad}|np:{next_pad}")
                    yield one_tick
                with system.batched():
                    # logger.debug(f"tick:{system.clock.next_tick}|{i}/{steps}|{drop}|{last_pad}->{next_pad}")
                    assert last_pad == drop.pad, f"{i} of {steps}|{drop}|lp:{last_pad}|np:{next_pad}"
                    next_pad.schedule(Pad.TurnOn, post_result=False)
                    last_pad.schedule(Pad.TurnOff, post_result=False)
                    real_next_pad = next_pad
                    def unreserve() -> None:
                        real_next_pad.unreserve()
                    board.after_tick(unreserve)
                    # logger.debug(f"{i} of {steps}|{drop}|lp:{last_pad}|np:{next_pad}")
                    if post_result and i == steps-1:
                        final_pad = next_pad
                        board.after_tick(lambda : future.post(final_pad.checked_drop))
                last_pad = next_pad
                if i < steps-1:
                    yield one_tick
            yield None
        iterator = before_tick()
        board.before_tick(lambda: next(iterator), delta=after)
        return future


class Drop(OpScheduler['Drop']):
    _display_liquid: Liquid
    _pad: DropLoc
    status: DropStatus

    @property
    def pad(self) -> DropLoc:
        return self._pad

    @pad.setter
    def pad(self, pad: DropLoc) -> None:
        old = self._pad
        # assert?
        if old.drop is self:
            old.drop = None
        self._pad = pad
        pad.drop = self

    @property
    def on_board_pad(self) -> Pad:
        assert isinstance(self.pad, Pad)
        return self.pad

    @property
    def blob(self) -> Blob:
        return not_None(self._pad.blob)

    @property
    def blob_volume(self) -> Volume:
        return self.blob.total_volume

    @blob_volume.setter
    def blob_volume(self, volume: Volume) -> None:
        blob = self.blob
        blob.contents.volume = volume
        blob.update_drops()

    @property
    def display_volume(self) -> Volume:
        return self._display_liquid.volume

    @property
    def reagent(self) -> Reagent:
        return self._display_liquid.reagent

    @reagent.setter
    def reagent(self, reagent: Reagent) -> None:
        blob = self.blob
        blob.contents.reagent = reagent
        blob.update_drops()

    def __init__(self, pad: DropLoc,
                 display_liquid: Liquid,
                 *,
                 status: DropStatus = DropStatus.ON_BOARD) -> None:
        assert pad.drop is None, f"Trying to create a second drop at {pad}"
        self._display_liquid = display_liquid
        self._pad = pad
        self.status = status
        if status is DropStatus.ON_BOARD:
            pad.drop = self

    def __repr__(self) -> str:
        st = self.status
        place = ""
        liquid = ""
        if st is DropStatus.ON_BOARD:
            blob = self.blob
            mine = ""
            if not blob.is_singleton:
                mine = f"{blob.per_pad_volume} of "
            liquid = f", {mine}{blob.total_volume} of {self.reagent}"
        else:
            place = f"{st.name}: "

        return f"Drop[{place}{self.pad}{liquid}]"

    def schedule_communication(self, cb: Callable[[], Optional[Callback]], *,
                               after: Optional[DelayType] = None) -> None:
        self.pad.schedule_communication(cb, after=after)

    def delayed(self, function: Callable[[], T], *,
                after: Optional[DelayType]) -> Delayed[T]:
        return self.pad.delayed(function, after=after)


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
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      ) -> Delayed[Drop]:
            future = Postable[Drop]()
            pad = self.pad
            def make_drop(_) -> None:
                # We want it to happen immediately, so we use our own journal.
                journal = ChangeJournal()
                journal.note_delivery(pad, self.liquid)
                journal.process_changes()
                if post_result:
                    # We're assuming that nobody is going to have turned off the pad, allowing
                    # the liquid to slip somewhere else.
                    future.post(pad.checked_drop)
            pad.schedule(Pad.TurnOn, after=after) \
                .then_call(make_drop)
            return future

    class TeleportInTo(StaticOperation['Drop']):
        extraction_point: Final[ExtractionPoint]
        liquid: Final[Liquid]
        mix_result: Final[Optional[Union[Reagent,str]]]
        def __init__(self, extraction_point: ExtractionPoint, *,
                     liquid: Optional[Liquid] = None,
                     reagent: Optional[Reagent] = None,
                     after: Optional[DelayType] = None,
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
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      ) -> Delayed[Drop]:
            liquid = self.liquid
            op = ExtractionPoint.TransferIn(
                liquid.reagent, liquid.volume, mix_result=self.mix_result)
            return self.extraction_point.schedule(
                op, after=after, post_result=post_result)

    class TeleportOut(Operation['Drop', None]):
        volume: Final[Optional[Volume]]
        product_loc: Final[Optional[Postable[ProductLocation]]]

        def __init__(self, *,
                     volume: Optional[Volume],
                     product_loc: Optional[Postable[ProductLocation]] = None
                     ) -> None:
            self.volume = volume
            self.product_loc = product_loc

        def _schedule_for(self, drop: Drop, *,
                      after: Optional[DelayType] = None,
                      post_result: bool = True,  # @UnusedVariable
                      ) -> Delayed[None]:
            op = ExtractionPoint.TransferOut(volume=self.volume, product_loc=self.product_loc)
            future = Postable[None]()

            def do_it() -> None:
                ep = cast(Pad, drop.pad).extraction_point
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
            assert isinstance(drop.pad, Pad)
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
            assert isinstance(drop.pad, Pad)
            pad = drop.pad
            direction = pad.board.orientation.pos_y
            current = pad.row
            steps = self.row-current
            return (direction, steps) if steps >=0 else (direction.opposite, -steps)


    class DispenseFrom(StaticOperation['Drop']):
        well: Final[Well]
        reagent: Final[Optional[Reagent]]
        empty_wrong_reagent: Final[bool]

        def _schedule(self, *,
                      after: Optional[DelayType] = None,
                      post_result: bool = True,
                      ) -> Delayed[Drop]:
            future = Postable[Drop]()
            well = self.well
            pad = well.exit_pad
            volume = well.dispensed_volume
            def make_drop(_) -> None:
                # Now that motion is infered, all we have to do is unreserve the pads and post the result
                # liquid = well.transfer_out(volume)
                board = pad.board
                # drop = Drop(pad=pad, liquid=liquid)
                # board.journal_delivery(pad, liquid)

                # If the caller gave us a before_release action, we invoke it
                # here, before any other dispense on this well can happen.
                if self.before_release is not None:
                    (self.before_release)()

                well.gate_reserved = False
                pad.unreserve()
                if post_result:
                    board.after_tick(lambda: future.post(pad.checked_drop))

            # The guard will be iterated when the motion is started, after any delay, but before the created
            # WellMotion tries to either get adopted by an in-progress motion or make changes on the well pads.
            def guard() -> Iterator[bool]:
                # First, we reserve the gate.  If there's a dispense in progress for this well, it will already have
                # the gate reserved, and we will spin until it's done.
                while not well.reserve_gate():
                    yield True
                # Next, if the caller gave us an after_reservation action, we call it.
                if self.after_reservation is not None:
                    (self.after_reservation)()
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
                well.schedule(Well.TransitionTo(WellState.DISPENSED, guard=guard()),
                               after=after) \
                    .then_call(make_drop) \
                    .then_schedule(Well.TransitionTo(WellState.READY))
            # well.ensure_content().then_call(run_group)
            run_group(None)
            return future


        def __init__(self, well: Well, *,
                     reagent: Optional[Reagent] = None,
                     empty_wrong_reagent: bool = False,
                     after_reservation: Optional[Callback] = None,
                     before_release: Optional[Callback] = None) -> None:
            self.well = well
            self.reagent = reagent
            self.empty_wrong_reagent = empty_wrong_reagent
            self.after_reservation = after_reservation
            self.before_release = before_release

    class EnterWell(Operation['Drop',None]):
        well: Final[Optional[Well]]
        empty_wrong_reagent: Final[bool]

        def __repr__(self) -> str:
            return f"<Drop.EnterWell: {self.well}>"

        def _schedule_for(self, drop: Drop, *,
                          after: Optional[DelayType] = None,
                          post_result: bool = True,
                          ) -> Delayed[None]:
            future = Postable[None]()
            if self.well is None:
                if not isinstance(drop.pad, Pad) or drop.pad.well is None:
                    raise NotAtWell(f"{drop} not at a well")
                well = drop.pad.well
            else:
                well = self.well

            # With inferred motion, we shouldn't have to do anything anymore
            # except possibly post to the future.

            def consume_drop(_) -> None:
                # blob = drop.blob
                # well.transfer_in(blob.contents)
                # pad = cast(Pad, drop.pad)
                # board = pad.board
                # board.journal_removal(pad, drop.blob_volume)
                # # drop.status = DropStatus.IN_WELL
                # # drop.pad.drop = None
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

                while True:
                    would_give = drop.blob_volume
                    f = well.ensure_space(volume=drop.blob_volume, reagent=drop.reagent,
                                          on_reagent_mismatch=mismatch_behavior)
                    while not f.has_value:
                        yield True
                    # The drop could've gotten bigger since we started.  If it hasn't, there's
                    # room.
                    if drop.blob_volume <= would_give:
                        yield False

            # Note, we post the drop as soon as we get to the DISPENSED state, even theough
            # we continue on to READY
            well.schedule(Well.TransitionTo(WellState.ABSORBED, guard=guard()), after=after) \
                .then_call(consume_drop) \
                .then_schedule(Well.TransitionTo(WellState.READY))
            return future


        def __init__(self, well: Optional[Well] = None, *,
                     empty_wrong_reagent: bool = False) -> None:
            self.well = well
            self.empty_wrong_reagent = empty_wrong_reagent
