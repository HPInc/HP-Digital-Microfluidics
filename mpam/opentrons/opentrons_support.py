from __future__ import annotations

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

    from schedule_xfers import TransferScheduler, XferOp, RWell, AspirateOp, map_str
    import schedule_xfers
    
    
    # If I don't explicitly reload opentrons_support, changes between runs don't get reflected.
    schedule_xfers = importlib.reload(schedule_xfers)




def load_config(name: str) -> Any:
    with open(name, 'rb') as f:
        return json.load(f)
        
def labware_from_config(spec: Any, protocol: protocol_api.ProtocolContext) -> Labware:
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
                 spec: Any, 
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
        
    def __str__(self) -> str:
        return f"ReagentSource[{self.reagent}, in: {map_str(self.input_wells)}, out: {map_str(self.output_wells)}]"
        
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
                 spec: Any, 
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
        
    def __str__(self) -> str:
        return str(self.pipette)
        
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
        # self.message(f"make_empty({map_str(on_board)}, {map_str(off_board)})")
        extra, ops = self.empty_ops(on_board, off_board, trash=trash)
        return (extra, Transfer(self, ops))
        
        
        
    def make_transfer(self, direction: Direction,
                      on_board: Sequence[tuple[Well, float]],
                      reagent_source: ReagentSource, *,
                      trash: Well) -> tuple[float, Optional[Transfer]]:
        # self.message(f"dir: {direction}, source: {reagent_source}, on_board: {map_str(on_board)}, trash: {trash}")
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
        
    def __str__(self) -> str:
        return f"Transfer[{self.pipettor}: {map_str(self.ops)}]"
        
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
    large_pipettor: Optional[Pipettor] = None
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
    
    def __init__(self, config: Any, protocol: protocol_api.ProtocolContext)-> None:
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
        
        if "large" in config["pipettes"]:
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
        # self.message("Planning")
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
        if self.large_pipettor is not None:
            large_trips = self.large_pipettor.partition(large, prefer_partial=prefer_partial)
        else:
            large_trips = ()
            small = list(on_board)
            # self.message(f"Small transfers: {small}")
        small_trips = self.small_pipettor.partition(small, prefer_partial=prefer_partial)
        # self.message(f"Small trips: {small_trips}")
        # self.message(f"Partitioned: {len(large_trips)} large, {len(small_trips)} small")
        
        if direction is Direction.EMPTY and reagent == "product":
            r = ReagentSource(reagent)
            # self.message(f"Getting product well from {map_str(self.output_wells)}")
            w = self.output_wells.pop(0)
            # self.message(f"Output well is {w}")
            # self.message(f"  Output wells now {map_str(self.output_wells)}")
            r.add_well(w, 0, ReagentWellUse.OUTPUT)
            self.last_product_well = w
        else:
            self.last_product_well = None
            r = self.reagent_source[reagent]
        xfers: list[Transfer] = []
        trash = self.trash_well
        if self.large_pipettor is not None:
            for trip in large_trips:
                error, xfer = self.large_pipettor.make_transfer(direction, trip, r, trash=trash)
                if xfer is not None:
                    xfers.append(xfer)
                if error > 0:
                    # TODO: Do something with error (e.g., send a message back)
                    ...
        for trip in small_trips:
            # self.message(f"Making transfer: {trip}")
            error, xfer = self.small_pipettor.make_transfer(direction, trip, r, trash=trash)
            # self.message(f"error: {error}, xfer: {xfer}")
            if xfer is not None:
                xfers.append(xfer)
            if error > 0:
                # TODO: Do something with error
                ...
        xfers[-1].is_last()
        return xfers
        


        
    def pipette_and_tip(self, reagent: str, volume: float) -> tuple[InstrumentContext, Well]:
        if self.large_pipettor is not None and volume > self.threshold:
            p = self.large_pipettor
        else:
            p = self.small_pipettor
        return (p.pipette, p.tip[reagent])
    
            
    def fill(self, reagent: str, target: Well, volume: float) -> None:
        # self.message(f"Moving {volume}uL of {reagent} to {target}")
        
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
            # self.message(f"Calling ready: {call_params}")
            resp = self.http_post("ready", json = call_params)
            # self.message(f"Back from ready: {resp}")
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
            # self.message(f"Transfer plan: {map_str(transfers)}")
            on_board = {ws[0] for ws in wells}
            self.do_transfers(transfers, r, on_board=on_board)
            
        self.message("Exiting main loop")
        
