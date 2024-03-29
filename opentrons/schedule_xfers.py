from __future__ import annotations

from typing import TypeVar, Generic, Sequence, Mapping
from abc import abstractmethod, ABC
from math import isclose

def map_str(d: Sequence) -> str:
    return f"[{', '.join(f'{v}' for v in d)}]"

T = TypeVar('T')

class XferOp(Generic[T]):
    target: T
    volume: float
    is_last: bool = False
    
    def __init__(self, target: T, volume: float) -> None:
        self.target = target
        self.volume = volume
    
class AspirateOp(XferOp[T]):
    def __repr__(self) -> str:
        return f"Aspirate {self.volume} from {self.target}"
    
class DispenseOp(XferOp[T]):
    def __repr__(self) -> str:
        return f"Dispense {self.volume} to {self.target}"
    
class RWell(Generic[T]):
    well: T
    has: float
    capacity: float
    
    @property
    def space(self) -> float:
        return self.capacity-self.has
    
    def __init__(self, well: T, volume: float, *, capacity: float):
        self.well = well
        self.has = volume
        self.capacity = capacity
        
    def __repr__(self) -> str:
        return f"RWell({self.well}, {self.has}/{self.capacity})"
    
class TransferScheduler(Generic[T], ABC):
    max_volume: float
    min_volume: float
    
    def __init__(self, *, min_volume: float, max_volume: float) -> None:
        self.min_volume = min_volume
        self.max_volume = max_volume
        
    @abstractmethod
    def message(self, msg: str) -> None: ... # @UnusedVariable
        
    def partition(self, targets: Sequence[tuple[T, float]], *,
                  prefer_partial: bool) -> Sequence[Sequence[tuple[T, float]]]:
        max_v = self.max_volume
        min_v = self.min_volume
        
        # self.message(f"targets: {targets}")
        # self.message(f"min/max: {min_v}/{max_v}")

        amount = { i: t[1] for i,t in enumerate(targets)}
        # self.message(f"amount: {amount}")
        
        need = sum(amount.values())
        transfers: list[Sequence[tuple[T, float]]] = []
        
        def to_transfer(by_index: Mapping[int, float]) -> Sequence[tuple[T, float]]:
            seq = [(targets[i][0], v) for i,v in by_index.items()]
            return seq
        
        while need > max_v:
            # self.message(f"{need} > {max_v}")
            this_transfer: dict[int, float] = {}
            room = max_v
            for w,v in amount.items():
                if v > 0:
                    if prefer_partial and v >= 2*min_v:
                        v = min_v
                    this_transfer[w] = v
                    room -= v
            # self.message(f"this_transfer: {this_transfer}")
            # self.message(f"room: {room}")

            # if we can't fit all of them even minimally, we take out the largest
            if room < 0:
                in_transfer = [(w,v) for w,v in this_transfer.items()]
                in_transfer.sort(key = lambda pair: pair[1], reverse=True)
                for w,v in in_transfer:
                    if room >= 0:
                        break
                    del this_transfer[w]
                    room += v
                    if (not prefer_partial) and room >= min_v:
                        # even if we'd rather not split, we'd rather split one to 
                        # make it fit
                        want = amount[w]
                        if want > 2*min_v:
                            v = min(room, want-min_v)
                            this_transfer[w] = v
                            room -= v
            # We've now committed to the wells we're going to transfer
            for w,v in this_transfer.items():
                amount[w] -= v
                if amount[w] == 0:
                    del amount[w]
                need -= v
            # self.message(f"amount: {amount}")
            # self.message(f"need: {need}")
            # But we may have room to expand them.
            if room > 0:
                available = {w: v for w,v in amount.items() if v > 0 and w in this_transfer}
                # self.message(f"available: {available}")
                total_available = sum(available.values())
                # self.message(f"total_available: {total_available}")
                if total_available > 0:
                    ratio = min(1, room/total_available)
                    # self.message(f"ratio: {ratio}")
                    for w,v in available.items():
                        # self.message(f"w,v: {w}, {v}")
                        v *= ratio
                        # self.message(f"v: {v}")
                        this_transfer[w] += v
                        # self.message(f"this_transfer[{w}]: {this_transfer[w]}")
                        amount[w] -= v
                        # self.message(f"amount[{w}]: {amount[w]}")
                        if amount[w] == 0:
                            del amount[w]
                        need -= v
                        # self.message(f"need: {need}")
                # self.message(f"amount: {amount}")
            transfers.append(to_transfer(this_transfer))
            # self.message(f"transfers: {transfers}")
        if need > 0:
            # self.message(f"remaining amount: {amount}")
            transfers.append(to_transfer(amount))
            # self.message(f"transfers: {transfers}")
        return transfers
    
    def fill_tip(self, volume: float, *,
                 sources: Sequence[RWell[T]]) -> tuple[float, Sequence[XferOp[T]]]:
        max_v = self.max_volume
        min_v = self.min_volume
        assert volume <= max_v
        if volume < min_v and not isclose(volume, min_v, rel_tol=0.01):
            self.message(f"WARNING: Requested volume ({volume}) is less than (and not close to) minimumum transfer volume ({min_v}).  Trying anyway with minimum.")
            volume = min_v
        # assert volume >= min_v
        decreasing = [w for w in sources if w.has > 0]
        # if there's nothing, there's nothing we can do.
        if len(decreasing) == 0:
            return (volume, ())
        # if there's only one, we have to use it.
        if len(decreasing) == 1:
            w = decreasing[0]
            v = min(volume, w.has)
            if v < min_v:
                return (volume, ())
            w.has -= v
            return (volume-v, (AspirateOp(w.well, v),))
        order = {w: i for i,w in enumerate(sources)}
        decreasing.sort(key=lambda w: (w.has, order[w]), reverse=True)
        ops: list[XferOp[T]] = []
        in_tip: float = 0
        # By construction, in_tip will either be zero or >= min_v, except when transferring the whole of one
        # well to another.
        need = volume
        while need > 0 and decreasing:
            smallest = decreasing[-1]
            in_smallest = smallest.has
            if in_smallest == 0:
                decreasing.pop()
                continue
            # if we can draw from the smallest, we do
            want = min(need, in_smallest)
            if want > min_v:
                ops.append(AspirateOp(smallest.well, want))
                need -= want
                smallest.has -= want
                in_tip += want
                if want == in_smallest:
                    decreasing.pop()
                continue
            # Either we need less than the minimum or have less than the minimum (or both).  
            # Maybe we can put back enough to allow it to happen if we go around again
            if in_tip == 0:
                putback: float = 0
            elif in_tip >= 2*min_v:
                putback = min_v
            else:
                putback = in_tip
            if putback > smallest.space:
                putback = 0
            if putback > 0 and in_smallest+putback >= min_v and need+putback > min_v:
                ops.append(DispenseOp(smallest.well, min_v))  # This will actually put in putback
                smallest.has += putback
                in_tip -= putback
                need += putback
                # we go around again, but now in_smallest will be >= min_v
                continue
            # if we can aspirate extra and put some back, we do so
            if need < min_v and need+min_v < max_v-in_tip and in_smallest >= need+min_v:
                ops.append(AspirateOp(smallest.well, need+min_v))
                ops.append(DispenseOp(smallest.well, min_v))
                need = 0
                in_tip += need
                smallest.has -= need
                continue
            # if we get here, we can't make progress just with what's in the pipette or the smallest well.
            if len(decreasing) == 1:
                break
            next_well = decreasing[-2]
            in_next = next_well.has
            # if there's nothing in our pipette and we can merge the smallest with the next, we do so
            if in_tip == 0 < min_v and in_next <= smallest.space:
                v = min(max_v, max(min_v, in_smallest))
                v = max(min_v, in_smallest)
                ops.append(AspirateOp(smallest.well, v))
                ops.append(DispenseOp(next_well.well, v))
                smallest.has = 0
                next_well.has += in_smallest
                decreasing.pop()
                continue
            # If we can pull a minimum transfer from the next, we do so and try again.
            if in_next >= min_v and in_tip+min_v <= max_v:
                ops.append(AspirateOp(next_well.well, min_v))
                ops.append(DispenseOp(smallest.well, min_v))
                smallest.has += min_v
                next_well.has -= min_v
                continue
            print(f"need = {need}")
            print(f"in_tip = {in_tip}")
            print(f"sources = {sources}")
            assert False
        return (need, ops)
    
    def empty_tip(self, volume: float, *,
                  sinks: Sequence[RWell[T]]) -> tuple[float, Sequence[XferOp[T]]]:
        max_v = self.max_volume
        min_v = self.min_volume
        assert volume <= max_v
        if volume < min_v and not isclose(volume, min_v, rel_tol=0.01):
            self.message(f"WARNING: Requested volume ({volume}) is less than (and not close to) minimumum transfer volume ({min_v}).  Trying anyway with minimum.")
            volume = min_v
        # assert volume >= min_v
        
        decreasing = [w for w in sinks if w.space > 0]
        # if there's nothing, there's nothing we can do.
        if len(decreasing) == 0:
            return (volume, ())
        # if there's only one, we have to use it.
        if len(decreasing) == 1:
            w = decreasing[0]
            v = min(volume, w.space)
            if v < min_v:
                return (volume, ())
            w.has += v
            return (volume-v, (DispenseOp(w.well, v),))

        order = {w: i for i,w in enumerate(sinks)}
        decreasing.sort(key=lambda w: (w.space, order[w]), reverse=True)
        ops: list[XferOp[T]] = []
        in_tip: float = volume
        
        while in_tip > 0 and decreasing:
            smallest = decreasing[-1]
            in_smallest = smallest.space
            
            if in_smallest == 0:
                decreasing.pop()
                continue
            # if we can put into the smallest, we do
            if in_tip <= in_smallest:
                ops.append(DispenseOp(smallest.well, in_tip))
                smallest.has += in_tip
                in_tip = 0
                break
            if in_smallest >= min_v:
                ops.append(DispenseOp(smallest.well, in_smallest))
                in_tip -= in_smallest
                smallest.has += in_smallest
                decreasing.pop()
                continue
            # At this point, we know that the room in the smallest is less than will
            # hold the volume in the tip and less than will hold a minimum transfer.
            
            # Can we pull up a minimum transfer and then fill the well?
            if in_tip+min_v <= max_v:
                ops.append(AspirateOp(smallest.well, min_v))
                in_tip += min_v
                smallest.has -= min_v
                continue
            
            # I'm sure there's more I can do, but for now, this will be good enough.
            decreasing.pop()
            
        ...
        return (in_tip, ops)
    
    def adjust_dispense(self, sinks: Sequence[tuple[T,float]], *,
                        shortfall: float) -> Sequence[tuple[T, float]]:
        if shortfall == 0:
            return sinks
        min_v = self.min_volume
        total_room = sum(v-min_v for w,v in sinks) # @UnusedVariable
        wells = [(v,w) for w,v in sinks]
        if total_room < shortfall:
            # we're going to have to do it by losing some targets entirely.
            wells.sort(reverse=True)
            v,w = wells.pop()
            total_room += (v-min_v)

        ratio = shortfall/total_room
        val = [(w, min_v + ratio*(v-min_v)) for v,w in wells]
        return val
    
    def fill_ops(self, on_board: Sequence[tuple[T, float]],
                  off_board: Sequence[RWell[T]]) -> tuple[float, Sequence[XferOp[T]]]:
        need = sum(t[1] for t in on_board)
        shortfall, gets = self.fill_tip(need, sources=off_board)
        if shortfall == need:
            return (shortfall, [])
        if shortfall > 0:
            on_board = self.adjust_dispense(on_board, shortfall=shortfall)
        ops = list(gets)
        for w,v in on_board:
            ops.append(DispenseOp(w,v))
        return (shortfall, ops)

    def empty_ops(self, on_board: Sequence[tuple[T, float]],
                  off_board: Sequence[RWell[T]],
                  *, trash: T) -> tuple[float, Sequence[XferOp[T]]]:
        # self.message(f"empty_ops({map_str(on_board)}, {map_str(off_board)})")
        have = sum(t[1] for t in on_board)
        # self.message(f"have: {have}")
        gets = [AspirateOp(w, v) for w,v in on_board]
        # self.message(f"gets: {map_str(gets)}")
        extra, puts = self.empty_tip(have, sinks=off_board)
        # self.message(f"extra: {extra}, puts: {puts}")
        ops: list[XferOp[T]] = list(gets)
        for op in puts:
            ops.append(op)
        if extra > 0:
            ops.append(DispenseOp(trash, extra))
        return (extra, ops)

