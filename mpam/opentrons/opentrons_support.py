from __future__ import annotations

from _collections import defaultdict
from enum import Enum, auto
import json
from typing import Sequence, Optional, NamedTuple, Any

from opentrons import protocol_api
from opentrons.protocol_api.instrument_context import InstrumentContext
from opentrons.protocol_api.labware import Well, Labware
from abc import ABC, abstractmethod

import schedule_xfers
import importlib
import requests
# If I don't explicitly reload opentrons_support, changes between runs don't get reflected.
schedule_xfers = importlib.reload(schedule_xfers)


from schedule_xfers import TransferScheduler, XferOp, RWell, AspirateOp


def load_config(name: str):
    with open(name, 'rb') as f:
        return json.load(f)
        
def labware_from_config(spec, protocol: protocol_api.ProtocolContext) -> Labware:
    labware: Labware = protocol.load_labware(spec["name"], spec["slot"])
    return labware

class Board:
    plate: Labware
    wells: Sequence[Well]
    extraction_ports: Sequence[Well]
    oil_reservoir: Well
    drop_size: float
    well_map: dict[str, Well]
    
    def __init__(self,
                 spec, 
                 protocol: protocol_api.ProtocolContext) -> None:
        self.plate = labware_from_config(spec["labware"], protocol)
        self.drop_size = spec["drop-size"]
        self.well_map = {}
        self.wells = [self.plate[w] for w in spec["wells"]]
        self.name_wells("W", self.wells)
        self.extraction_ports = [self.plate[w] for w in spec["extraction-ports"]]
        self.name_wells("E", self.extraction_ports)
        self.oil_reservoir = self.plate[spec["oil-reservoir"]]
        self.name_wells("O", (self.oil_reservoir,))
        
    def name_wells(self, prefix: str, wells: Sequence[Well]) -> None:
        for i,w in enumerate(wells):
            name = f"{prefix}{i+1}"
            self.well_map[name] = w
        
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
    def well(self, robot:Robot, board:Board)->Well:
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
    _tips: list[Well]
    tip: dict[str, Well]
    _current_tip: Optional[Well]
    _trash_tip: bool
    
    def __init__(self, 
                 spec, 
                 protocol: protocol_api.ProtocolContext,
                 tipracks: Sequence[Labware],
                 *,
                 robot: Robot) -> None:
        self.protocol = protocol
        self.robot = robot
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
        
    def wait_for_clearance(self, well: Well) -> None:
        self.pipette.move_to(well.top(1))
        self.message(f"Waiting above {well}")
        self.protocol.delay(seconds=0.5)
        
    def signal_clear(self, well: Well) -> None:
        self.pipette.move_to(well.top(1))
        self.message(f"Resuming")
    
        
    def process(self, op: XferOp[Well], *, on_board: set[Well]) -> None: 
        w = op.target
        p = self.pipette
        pause_around = w in on_board
        if pause_around:
            self.wait_for_clearance(w)
        if isinstance(op, AspirateOp):
            p.aspirate(op.volume, w)
        else:
            p.dispense(op.volume, w)
        if pause_around:
            self.signal_clear(w)

            
        
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
                
        

class Transfer(NamedTuple):
    pipettor: Pipettor
    ops: Sequence[XferOp[Well]]
    
        
class Robot:
    protocol: protocol_api.ProtocolContext
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
        self.message("Creating the robot")
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
        
    def http_post(self, path: str, *, json: Any = {}) -> Optional[requests.Response]:
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
        else:
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
        
    def loop(self) -> None:
        ...
        
