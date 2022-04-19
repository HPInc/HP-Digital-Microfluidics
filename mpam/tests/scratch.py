from __future__ import annotations
COMBINED_FILES_KLUDGE = True

from typing import TypeVar, Generic, Sequence, Mapping


T = TypeVar('T')

class XferOp(Generic[T]):
    target: T
    volume: float
    is_last: bool = False
    
    def __init__(self, target: T, volume: float) -> None:
        self.target = target
        self.volume = volume
    
class AspirateOp(XferOp[T]):
    def __repr__(self):
        return f"Aspirate {self.volume} from {self.target}"
    
class DispenseOp(XferOp[T]):
    def __repr__(self):
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
    
class TransferScheduler(Generic[T]):
    max_volume: float
    min_volume: float
    
    def __init__(self, *, min_volume: float, max_volume: float) -> None:
        self.min_volume = min_volume
        self.max_volume = max_volume
        
        
        
    def partition(self, targets: Sequence[tuple[T, float]], *,
                  prefer_partial: bool) -> Sequence[Sequence[tuple[T, float]]]:
        max_v = self.max_volume
        min_v = self.min_volume

        amount = { i: t[1] for i,t in enumerate(targets)}
        
        need = sum(amount.values())
        transfers: list[Sequence[tuple[T, float]]] = []
        
        def to_transfer(by_index: Mapping[int, float]) -> Sequence[tuple[T, float]]:
            seq = [(targets[i][0], v) for i,v in by_index.items()]
            return seq
        
        while need > max_v:
            this_transfer: dict[int, float] = {}
            room = max_v
            for w,v in amount.items():
                if v > 0:
                    if prefer_partial and v >= 2*min_v:
                        v = min_v
                    this_transfer[w] = v
                    room -= v
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
            # But we may have room to expand them.
            if room > 0:
                available = {w: v-min_v for w,v in amount.items() if v > min_v and w in this_transfer}
                total_available = sum(available.values())
                if total_available > 0:
                    ratio = min(1, room/total_available)
                    for w,v in available.items():
                        v *= ratio
                        this_transfer[w] += v
                        amount[w] -= v
            transfers.append(to_transfer(this_transfer))
        if need > 0:
            transfers.append(to_transfer(amount))
        return transfers
    
    def fill_tip(self, volume: float, *,
                 sources: Sequence[RWell[T]]) -> tuple[float, Sequence[XferOp[T]]]:
        max_v = self.max_volume
        min_v = self.min_volume
        assert volume <= max_v
        assert volume >= min_v
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
        assert volume >= min_v
        
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
        have = sum(t[1] for t in on_board)
        gets = [AspirateOp(w, v) for w,v in on_board]
        extra, puts = self.empty_tip(have, sinks=off_board)
        ops: list[XferOp[T]] = list(gets)
        for op in puts:
            ops.append(op)
        if extra > 0:
            ops.append(DispenseOp(trash, extra))
        return (extra, ops)
    
#
#
# if __name__ == "__main__":
#     class RW(RWell[str]):
#         def __init__(self, well: str, vol: float) -> None:
#             super().__init__(well, vol, capacity=50) 
#
#     ts = TransferScheduler[str](min_volume=20, max_volume=100)
#     # targets = {"A": 25.0, "B": 54, "D": 80, "E": 20}
#     # targets = [("A", 25.0), ("B", 54), ("D", 80), ("E", 20)]
#
#     targets = [("A", 20.0), ("A", 20.0), ("B", 20.0)]
#
#     trips = ts.partition(targets, prefer_partial=True)
#     sources = [RW("S0", 7), RW("S1", 50), RW("S2", 50), RW("S3", 50), RW("S4", 50)]
#
#     print(sources)
#     for trip in trips:
#         print(ts.fill_ops(trip, sources))
#         print(sources)
#
#
#     # print(ts.partition(targets, prefer_partial=False))
#     # print(ts.partition({"X": 510}, prefer_partial=False))   
#
#
#     # print(sources)
#     # print(ts.fill_tip(40, sources=sources))
#     # print(sources)
#     # print(ts.fill_tip(40, sources=sources))
#     # print(sources)
#     # print(ts.fill_tip(22, sources=sources))
#     # print(sources)
#     # print(ts.fill_tip(22, sources=sources))
#     # print(sources)
#     # print(ts.fill_tip(22, sources=sources))
#     # print(sources)
#     # sinks = [RW("X0", 45), RW("X1", 0), RW("X2", 0), RW("X3", 0)]
#     # print(sinks)
#     # print(ts.empty_tip(60, sinks=sinks))
#     # print(sinks)
#     # print(ts.empty_tip(60, sinks=sinks))
#     # print(sinks)
#     # print(ts.empty_tip(60, sinks=sinks))
#     # print(sinks)
#     ...


from _collections import defaultdict
from abc import ABC, abstractmethod
from enum import Enum, auto
import importlib
import json
from typing import Sequence, Optional, NamedTuple, Any, Dict, List

from opentrons import protocol_api
from opentrons.protocol_api.instrument_context import InstrumentContext
from opentrons.protocol_api.labware import Well, Labware
import requests

if "COMBINED_FILES_KLUDGE" not in globals():

    from schedule_xfers import TransferScheduler, XferOp, RWell, AspirateOp
    import schedule_xfers
    
    
    # If I don't explicitly reload opentrons_support, changes between runs don't get reflected.
    schedule_xfers = importlib.reload(schedule_xfers)




def load_config(name: str):
    with open(name, 'rb') as f:
        return json.load(f)
        
def labware_from_config(spec, protocol: protocol_api.ProtocolContext) -> Labware:
    defn_json = spec.get("definition", None)
    if defn_json is not None:
        labware: Labware = protocol.load_labware_from_definition(defn_json, spec["slot"])
    else:
        labware = protocol.load_labware(spec["name"], spec["slot"],
                                        namespace=spec.get('namespace', None),
                                        version=spec.get('version', None))
    return labware

class Board:
    plate: Labware
    wells: Sequence[Well]
    extraction_ports: Sequence[Well]
    oil_reservoir: Well
    drop_size: float
    well_map: dict[str, Well]
    well_names: dict[Well, str]
    
    def __init__(self,
                 spec, 
                 protocol: protocol_api.ProtocolContext,
                 *,
                 robot: Robot) -> None:
        robot.message(f"Board labware spec is {spec['labware']}")
        try:
            self.plate = labware_from_config(spec["labware"], protocol)
            robot.message(f"Board plate is {self.plate}")
            
            self.drop_size = spec["drop-size"]
            robot.message(f"Board drop size is {self.drop_size}")
            self.well_map = {}
            self.well_names = {}
            self.wells = [self.plate[w] for w in spec["wells"]]
            robot.message(f"Board wells is {self.wells}")
            self.name_wells("W", self.wells)
            self.extraction_ports = [self.plate[w] for w in spec["extraction-ports"]]
            robot.message(f"Board extraction_ports is {self.extraction_ports}")
            self.name_wells("E", self.extraction_ports)
            self.oil_reservoir = self.plate[spec["oil-reservoir"]]
            robot.message(f"Board oil_reservoir is {self.oil_reservoir}")
            self.name_wells("O", (self.oil_reservoir,))
            robot.message("Done creating board")
        except BaseException as ex:
            robot.message(f"Exception while creating board: {ex}")
        
    def name_wells(self, prefix: str, wells: Sequence[Well]) -> None:
        for i,w in enumerate(wells):
            name = f"{prefix}{i+1}"
            self.well_map[name] = w
            self.well_names[w] = name
        
class Direction(Enum):
    FILL = auto()
    EMPTY = auto()
    
class Target(ABC):
    @abstractmethod
    def well(self, robot: Robot, board: Board) -> Well: ... # @UnusedVariable

class BoardWell(Target):
    n: int
    def __init__(self, n: int) -> None:
        self.n = n
    def well(self, robot:Robot, board:Board)->Well: # @UnusedVariable
        return board.wells[self.n]

class BoardEP(Target):
    n: int
    def __init__(self, n: int) -> None:
        self.n = n
    def well(self, robot:Robot, board:Board)->Well: # @UnusedVariable
        return board.extraction_ports[self.n]

class OilReservoir(Target):
    def well(self, robot: Robot, board: Board)->Well: # @UnusedVariable
        return board.oil_reservoir

class ReagentWellUse(Enum):
    INPUT = auto()
    OUTPUT = auto()
    BIDI = auto()
    
class ReagentSource:
    reagent: str
    input_wells: list[RWell[Well]]
    output_wells: list[RWell[Well]]
    # has: dict[Well, float]
    # space: dict[Well, float]
        
    def __init__(self, reagent: str) -> None:
        self.reagent = reagent
        self.input_wells = []
        self.output_wells = []
        # self.has = {}
        # self.space = {}
        
    def add_well(self, well: Well, volume: float, use: ReagentWellUse) -> None:
        w = RWell(well, volume, capacity = well.max_volume)
        if use is ReagentWellUse.INPUT or use is ReagentWellUse.BIDI:
            self.input_wells.append(w)
        if use is ReagentWellUse.OUTPUT or use is ReagentWellUse.BIDI:
            self.output_wells.append(w)
        # self.has[well] = volume
        # self.space[well] = well.max_volume-volume
        
class Pipettor(TransferScheduler[Well]) :
    pipette: InstrumentContext
    protocol: protocol_api.ProtocolContext
    robot: Robot
    board: Board
    _tips: list[Well]
    tip: dict[str, Well]
    _current_tip: Optional[Well]
    _trash_tip: bool
    
    def __init__(self, 
                 spec, 
                 protocol: protocol_api.ProtocolContext,
                 tipracks: List[Labware],
                 *,
                 robot: Robot) -> None:
        self.protocol = protocol
        self.robot = robot
        self.board = robot.board
        p = protocol.load_instrument(spec["name"], spec["side"], tip_racks = tipracks)
        self.pipette = p
        min_v = p.min_volume
        max_v = min(p.max_volume, *(tr.wells()[0].max_volume for tr in tipracks))
        super().__init__(max_volume=max_v, min_volume=min_v)
        self._tips = []
        for tr in tipracks:
            self._tips += tr.wells()
        self.tip = defaultdict(lambda: self._tips.pop(0))
        self._current_tip = None
        
    def message(self, msg: str) -> None:
        self.robot.message(msg)
        
    def well_name(self, well: Well) -> str:
        return self.board.well_names[well]
        
    def wait_for_clearance(self, well: Well, volume: float) -> None:
        self.pipette.move_to(well.top(1))
        well_name = self.well_name(well)
        self.message(f"Waiting above {well_name}")
        self.robot.call_waiting(well, volume)
        # self.protocol.delay(seconds=0.5)
        
    def signal_clear(self, well: Well, volume: float) -> None:
        self.pipette.move_to(well.top(1))
        well_name = self.well_name(well)
        self.message(f"Resuming from {well_name}")
        self.robot.call_finished(well, volume)
    
        
    def process(self, op: XferOp[Well], *, on_board: set[Well]) -> None: 
        w = op.target
        v = op.volume
        p = self.pipette
        pause_around = w in on_board
        if pause_around:
            self.wait_for_clearance(w, v)
        if isinstance(op, AspirateOp):
            p.aspirate(v, w)
        else:
            p.dispense(v, w)
        if pause_around:
            self.signal_clear(w, v)

            
        
    def get_tip_for(self, reagent: str) -> None:
        assert self._current_tip is None
        if reagent == "product":
            tip = self._current_tip = self._tips.pop(0)
            self._trash_tip = True
        else:
            tip = self._current_tip = self.tip[reagent]
            self._trash_tip = False
        self.pipette.pick_up_tip(tip)
        
    def release_tip(self) -> None:
        assert self._current_tip is not None
        if self._trash_tip:
            self.pipette.drop_tip()
        else:
            self.pipette.drop_tip(self._current_tip)
        self._current_tip = None
        
    def make_fill(self, on_board: Sequence[tuple[Well, float]],
                  off_board: Sequence[RWell[Well]]) -> tuple[float, Optional[Transfer]]:
        (shortfall, ops) = self.fill_ops(on_board, off_board)
        
        if shortfall > 0 and shortfall == sum(t[1] for t in on_board):
            return (shortfall, None)
        return (shortfall, Transfer(self, ops))

    def make_empty(self, on_board: Sequence[tuple[Well, float]],
                  off_board: Sequence[RWell[Well]],
                  *, trash: Well) -> tuple[float, Transfer]:
        extra, ops = self.empty_ops(on_board, off_board, trash=trash)
        return (extra, Transfer(self, ops))
        
        
        
    def make_transfer(self, direction: Direction,
                      on_board: Sequence[tuple[Well, float]],
                      reagent_source: ReagentSource, *,
                      trash: Well) -> tuple[float, Optional[Transfer]]:
        if direction is Direction.FILL:
            return self.make_fill(on_board, reagent_source.input_wells)
        else:
            return self.make_empty(on_board, reagent_source.output_wells, trash=trash)
                
JSONObj = Dict[str, Any]

class Transfer(NamedTuple):
    pipettor: Pipettor
    ops: Sequence[XferOp[Well]]
    
    def is_last(self) -> None:
        self.ops[-1].is_last = True
        
class Robot:
    protocol: protocol_api.ProtocolContext
    board: Board
    large_tipracks: Sequence[Labware]
    small_tipracks: Sequence[Labware]
    # large_tips: list[Well]
    # small_tips: list[Well]
    input_plates: Sequence[Labware] 
    output_plates: Sequence[Labware]
    output_wells: list[Well]
    large_pipettor: Pipettor
    small_pipettor: Pipettor
    threshold: float
    # reagent_small_tip: dict[str, Well]
    # reagent_large_tip: dict[str, Well]
    reagent_source: dict[str, ReagentSource]
    trash_well: Well
    _next_product: int
    endpoint: Optional[str] = None
    last_product_well: Optional[Well] = None
    
    def message(self, msg: str) -> None:
        try_remote = self.http_post("message", json = { "message": msg})
        if try_remote is None:
            self.protocol.comment(msg)
        # if self.endpoint is not None:
        #     requests.post(f"{self.endpoint}/message",
        #                   json = { "message": msg })
        #     return
        # self.protocol.comment(msg)
    
    def __init__(self, config, protocol: protocol_api.ProtocolContext):
        self.protocol = protocol
        ep_config = config.get("endpoint", None)   
        if ep_config:
            ip = ep_config["ip"]
            port = ep_config["port"]
            self.endpoint = f"http://{ip}:{port}"
        self.message(f"Creating the robot. Callback endpoint is {self.endpoint}")
        self.board = Board(config["board"], protocol, robot=self)
        self.large_tipracks = [labware_from_config(s,protocol) for s in config["tipracks"]["large"]]
        self.large_tips = []
        for tr in self.large_tipracks:
            self.large_tips += tr.wells()
        self.small_tipracks = [labware_from_config(s,protocol) for s in config["tipracks"]["small"]]
        self.small_tips = []
        for tr in self.small_tipracks:
            self.small_tips += tr.wells()
        self.input_plates = [labware_from_config(s,protocol) for s in config["input-wellplates"]]
        self.output_plates = [labware_from_config(s,protocol) for s in config["output-wellplates"]]
        self.output_wells = []
        for p in self.output_plates:
            self.output_wells += p.wells()
        
        self.large_pipettor = Pipettor(config["pipettes"]["large"], protocol, self.large_tipracks, robot=self)
        self.small_pipettor = Pipettor(config["pipettes"]["small"], protocol, self.small_tipracks, robot=self)
        self.threshold: float = self.small_pipettor.max_volume
        # self.reagent_small_tip = defaultdict(lambda: self.small_tips.pop(0))
        # self.reagent_large_tip = defaultdict(lambda: self.large_tips.pop(0))
        self.reagent_source = {}
        for spec in config["reagents"]:
            rn = spec["name"]
            rs = ReagentSource(rn)
            self.reagent_source[rn] = rs
            # rw: list[tuple[Well, float]] = []
            for ws in spec["wells"]:
                rp = self.input_plates[ws["plate"]]
                use_spec = ws["use"]
                if use_spec == "input":
                    use = ReagentWellUse.INPUT
                elif use_spec == "output":
                    use = ReagentWellUse.OUTPUT
                else:
                    use = ReagentWellUse.BIDI
                rs.add_well(rp[ws["well"]], ws["quantity"], use)
        
        
        trash = protocol.load_labware("opentrons_1_trash_1100ml_fixed", 12)
        trash_source = ReagentSource("waste")
        self.reagent_source["waste"] = trash_source
        self.trash_well = trash["A1"]
        trash_source.add_well(trash["A1"], 0, ReagentWellUse.OUTPUT)
        
        self._next_product = 0
        
    def http_post(self, path: str, *, json: JSONObj = {}) -> Optional[requests.Response]:
        if self.endpoint is None:
            return None
        return requests.post(f"{self.endpoint}/{path}", json=json)
        
    def exit(self) -> None:
        self.http_post("exit")
        # if self.endpoint is not None:
            # requests.post(f"{self.endpoint}/exit")

    def do_transfers(self, transfers: Sequence[Transfer], reagent: str, *, 
                     on_board: set[Well]) -> None:
        p: Optional[Pipettor] = None
        for t in transfers:
            if p is not t.pipettor:
                if p is not None :
                    p.release_tip()
                p = t.pipettor
                p.get_tip_for(reagent)
            for op in t.ops:
                p.process(op, on_board=on_board)
        if p is not None:
            p.release_tip()
            
    def plan(self, direction: Direction, reagent: str, on_board: Sequence[tuple[Well, float]]) -> Sequence[Transfer]:
        threshold = self.threshold
        large = [ (w,v) for w,v in on_board if v > threshold ]
        small = [ (w,v) for w,v in on_board if v < threshold ]
        either = [ (w,v) for w,v in on_board if v == threshold ]
        if either:
            if large:
                large += either
            else:
                small += either
        prefer_partial = direction is Direction.FILL

        large_trips = self.large_pipettor.partition(large, prefer_partial=prefer_partial)
        small_trips = self.small_pipettor.partition(small, prefer_partial=prefer_partial)
        
        if direction is Direction.EMPTY and reagent == "product":
            r = ReagentSource(reagent)
            w = self.output_wells.pop(0)
            r.add_well(w, 0, ReagentWellUse.OUTPUT)
            self.last_product_well = w
        else:
            self.last_product_well = None
            r = self.reagent_source[reagent]
        xfers: list[Transfer] = []
        trash = self.trash_well
        for trip in large_trips:
            error, xfer = self.large_pipettor.make_transfer(direction, trip, r, trash=trash)
            if xfer is not None:
                xfers.append(xfer)
            if error > 0:
                # TODO: Do something with error (e.g., send a message back)
                ...
        for trip in small_trips:
            error, xfer = self.small_pipettor.make_transfer(direction, trip, r, trash=trash)
            if xfer is not None:
                xfers.append(xfer)
            if error > 0:
                # TODO: Do something with error
                ...
        xfers[-1].is_last()
        return xfers
        


        
    def pipette_and_tip(self, reagent: str, volume: float) -> tuple[InstrumentContext, Well]:
        if volume > self.threshold:
            p = self.large_pipettor
        else:
            p = self.small_pipettor
        return (p.pipette, p.tip[reagent])
    
            
    def fill(self, reagent: str, target: Well, volume: float) -> None:
        self.message(f"Moving {volume}uL of {reagent} to {target}")
        
        transfers  = self.plan(Direction.FILL, reagent, [(target,volume)])
        self.do_transfers(transfers, reagent, on_board={target})
        
    def deliver(self, reagent: str, targets: Sequence[Well], drop_size: float) -> None:
        self.message(f"Delivering {len(targets)} drop(s) of {reagent}")
        transfers = self.plan(Direction.FILL, reagent, [(w, drop_size) for w in targets])
        self.do_transfers(transfers, reagent, on_board = set(targets))

    def remove_product(self, source: Well, volume: float) -> None:
        # reagent = f"**product {self._next_product}**"
        self.message(f"Removing {volume}uL of product {self._next_product} from {source} ")
        self._next_product += 1
        reagent = "product"
        transfers = self.plan(Direction.EMPTY, reagent, [(source, volume)])
        self.do_transfers(transfers, reagent, on_board = {source})
        
    def empty_waste(self, sources: Sequence[tuple[Well, float]]) -> None:
        reagent = "waste"
        self.message(f"Emptying waste from {[w for w in sources]}")
        transfers = self.plan(Direction.EMPTY, reagent, sources)
        self.do_transfers(transfers, reagent, on_board={t[0] for t in sources})
        
    def prepare_call(self, *, json: Optional[JSONObj] = None) -> JSONObj:
        if json is None:
            json = {}
        # TODO: Add return info from prior transfers
        ...
        return json
    
    def call_finished(self, well: Well, volume: float) -> None:
        call_params = self.prepare_call()
        call_params["well"] = self.board.well_names[well]
        call_params["volume"] = volume
        resp = self.http_post("finished", json = call_params)
        assert resp is not None, f"No endpoint to call"
        assert resp.status_code == 200, f"/finished status code was {resp.status_code}"
        
    def call_waiting(self, well: Well, volume: float) -> None:
        call_params = self.prepare_call()
        call_params["well"] = self.board.well_names[well]
        call_params["volume"] = volume
        resp = self.http_post("waiting", json = call_params)
        assert resp is not None, f"No endpoint to call"
        assert resp.status_code == 200, f"/waiting status code was {resp.status_code}"
        
    def loop(self) -> None:
        self.message("Entering main loop")
        dirs = {"fill": Direction.FILL, "empty": Direction.EMPTY}
        well_map = self.board.well_map
        while True:
            # self.message("Making ready call")
            call_params = self.prepare_call()
            if self.last_product_well is not None:
                call_params["product_well"] = str(self.last_product_well)

            resp = self.http_post("ready", json = call_params)
            assert resp is not None, f"No endpoint to call"
            body = resp.json()
            # self.message(f"Body is {body}")
            cmd = body["command"]
            # self.message(f"Command is {cmd}")
            if cmd == "exit":
                self.message("Exit requested")
                break
            d = dirs[cmd]
            r = body["reagent"]
            well_specs = body["targets"]
            action = "supplying" if d is Direction.FILL else "removing" 
            tdescs = ", ".join([f"{ws['volume']} µL @ {ws['well']}" for ws in well_specs])
            self.message("-------------------")
            self.message(f"{action} {r}: {tdescs}")
            
            wells = [(well_map[ws["well"]], ws["volume"]) for ws in well_specs]
            transfers = self.plan(d, r, wells)
            on_board = {ws[0] for ws in wells}
            self.do_transfers(transfers, r, on_board=on_board)
            
        self.message("Exiting main loop")
        


from opentrons import protocol_api

if "COMBINED_FILES_KLUDGE" not in globals():
    import importlib
    import opentrons_support
    # If I don't explicitly reload opentrons_support, changes between runs don't get reflected.
    opentrons_suport = importlib.reload(opentrons_support)



metadata = {
    'protocolName': 'Joey Peripheral Protocol',
    'author': 'Evan Kirshenbaum < evan.kirshenbaum@hp.com>',
    'description': 'A generic looping client to use the OT-2 as a peripheral for Joey',
    'apiLevel': '2.11'
}

        
            
config: Any = None            
            

def run(protocol: protocol_api.ProtocolContext) -> None:
    if "COMBINED_FILES_KLUDGE" not in globals():
        from opentrons_support import Robot, load_config
    global config
    
    if config is None:
        config = load_config("config.json")


    # turn_off_lights_at_end = not protocol.rail_lights_on
    turn_off_lights_at_end = False
    if turn_off_lights_at_end:
        protocol.set_rail_lights(True)
        

        
    if not protocol.is_simulating():
        # board = Board(config["board"], protocol)
        robot = Robot(config, protocol)
        board = robot.board
        
        robot.message("Created robot and board")
        
        for n,w in board.well_map.items():
            robot.message(f"{n}: {w}")
    
        robot.message("Starting run")
        
        if robot.endpoint:
            robot.message(robot.endpoint)
        
        
        robot.loop()
                
        if turn_off_lights_at_end:
            protocol.set_rail_lights(False)
        robot.message("Done")
        robot.exit()

config = {"pipettes": {"large": {"name": "p300_single_gen2", "side": "right"}, "small": {"name": "p20_single_gen2", "side": "left"}}, "tipracks": {"large": [{"name": "opentrons_96_filtertiprack_200uL", "slot": 3}], "small": [{"name": "opentrons_96_filtertiprack_20uL", "slot": 6}]}, "input-wellplates": [{"name": "nest_96_wellplate_2ml_deep", "slot": 1}], "output-wellplates": [{"name": "nest_96_wellplate_2ml_deep", "slot": 10}], "board": {"labware": {"name": "biorad_96_wellplate_200ul_pcr", "slot": 8}, "drop-size": 1.0, "wells": ["E1", "F1", "G1", "H1", "E5", "F5", "G5", "H5"], "extraction-ports": ["E3", "F3", "G3"], "oil-reservoir": "A3"}, "endpoint": {"ip": "192.168.86.237", "port": 8087}, "reagents": [{"name": "Fragment-1", "wells": [{"plate": 0, "well": "A1", "quantity": 200, "use": "input"}]}, {"name": "Fragment-2", "wells": [{"plate": 0, "well": "A2", "quantity": 200, "use": "input"}]}, {"name": "Fragment-3", "wells": [{"plate": 0, "well": "A3", "quantity": 200, "use": "input"}]}, {"name": "Fragment-4", "wells": [{"plate": 0, "well": "A4", "quantity": 200, "use": "input"}]}, {"name": "Fragment-5", "wells": [{"plate": 0, "well": "A5", "quantity": 200, "use": "input"}]}, {"name": "Fragment-6", "wells": [{"plate": 0, "well": "A6", "quantity": 200, "use": "input"}]}, {"name": "Fragment-7", "wells": [{"plate": 0, "well": "A7", "quantity": 200, "use": "input"}]}, {"name": "Fragment-8", "wells": [{"plate": 0, "well": "A8", "quantity": 200, "use": "input"}]}, {"name": "Fragment-9", "wells": [{"plate": 0, "well": "A9", "quantity": 200, "use": "input"}]}, {"name": "Fragment-10", "wells": [{"plate": 0, "well": "A10", "quantity": 200, "use": "input"}]}, {"name": "Fragment-11", "wells": [{"plate": 0, "well": "A11", "quantity": 200, "use": "input"}]}, {"name": "Fragment-12", "wells": [{"plate": 0, "well": "A12", "quantity": 200, "use": "input"}]}, {"name": "Fragment-13", "wells": [{"plate": 0, "well": "B1", "quantity": 200, "use": "input"}]}, {"name": "Fragment-14", "wells": [{"plate": 0, "well": "B2", "quantity": 200, "use": "input"}]}, {"name": "Fragment-15", "wells": [{"plate": 0, "well": "B3", "quantity": 200, "use": "input"}]}, {"name": "Fragment-16", "wells": [{"plate": 0, "well": "B4", "quantity": 200, "use": "input"}]}, {"name": "Fragment-17", "wells": [{"plate": 0, "well": "B5", "quantity": 200, "use": "input"}]}, {"name": "Fragment-18", "wells": [{"plate": 0, "well": "B6", "quantity": 200, "use": "input"}]}, {"name": "Fragment-19", "wells": [{"plate": 0, "well": "B7", "quantity": 200, "use": "input"}]}, {"name": "Fragment-20", "wells": [{"plate": 0, "well": "B8", "quantity": 200, "use": "input"}]}, {"name": "PM Primers", "wells": [{"plate": 0, "well": "C1", "quantity": 1000, "use": "input"}]}, {"name": "Dilution Buffer", "wells": [{"plate": 0, "well": "D1", "quantity": 1000, "use": "input"}]}, {"name": "Master Mix", "wells": [{"plate": 0, "well": "E1", "quantity": 1000, "use": "input"}]}, {"name": "Prep Mixture", "wells": [{"plate": 0, "well": "F1", "quantity": 1000, "use": "input"}]}, {"name": "PF Primers", "wells": [{"plate": 0, "well": "G1", "quantity": 1000, "use": "input"}]}]}

run(None)
