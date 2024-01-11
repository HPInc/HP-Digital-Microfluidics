from __future__ import annotations

from _collections import defaultdict, deque
from argparse import _ArgumentGroup
from enum import Enum, auto
import fileinput
import json
import logging
import random
import re
from tempfile import NamedTemporaryFile
from threading import Thread, Event, Condition, RLock
import traceback
from typing import Union, Final, Any, cast, Optional, Callable, NamedTuple, \
    Sequence

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_runner import GracefulExit
import requests

from erk.afs import AsyncFunctionSerializer
from erk.config import ConfigParam
from mpam import exerciser
from mpam.device import System, Board, PipettingTarget, ProductLocation
from mpam.pipettor import Pipettor, Transfer, XferTarget, EmptyTarget, \
    PipettingSource
from mpam.types import Reagent, XferDir
from erk.quant.SI import seconds, uL, ml, ul
from erk.quant.dimensions import Time, Volume
from erk.quant.timestamp import time_now


logger = logging.getLogger(__name__)

JSONObj = dict[str, Any]

class ReagentUse(Enum):
    INPUT = auto()
    OUTPUT = auto()
    BIDI = auto()

class ReagentSource(NamedTuple):
    plate: int
    well: str
    quantity: Volume
    use: ReagentUse = ReagentUse.INPUT
    
    def as_json(self) -> JSONObj:
        use = self.use
        u = "input" if use is ReagentUse.INPUT else "output" if use is ReagentUse.OUTPUT else "bidi"
        return { 
                "plate": self.plate, 
                "well": self.well,
                "quantity": self.quantity.as_number(uL),
                "use": u 
                }

class Config:
    robot_ip: Final = ConfigParam[str]()
    configuration = ConfigParam[Union[str, JSONObj]]()
    reagents = ConfigParam[Optional[Union[str, dict[Reagent, Sequence[ReagentSource]]]]](None)
    listener_port = ConfigParam[Union[str, int]](8087)
    robot_port = ConfigParam[Union[str, int]](31950)
    board_def = ConfigParam[Optional[str]](None)

class VolAccum:
    total: Volume = Volume.ZERO
    
    def __iadd__(self, rhs: Volume) -> VolAccum:
        self.total += rhs
        return self

class Listener(Thread):
    app: web.Application
    port: Final[int]
    running: bool = True
    system_running: bool = True
    pending_transfer: Optional[Transfer]
    lock: Final[RLock]
    have_transfer: Final[Condition]
    ready_for_transfer: Final[Condition]
    target_wells: Final[dict[PipettingTarget, str]]
    call_number: int
    finish_queue: Final[AsyncFunctionSerializer]
    
    current_xfers: Final[dict[str, deque[XferTarget]]]
    current_reagent: Reagent
    
    def __init__(self, *, port: int, name: str) -> None:
        super().__init__(name=name)
        self.port = port
        self.pending_transfer = None
        self.lock = RLock()
        self.have_transfer = Condition(lock = self.lock)
        self.ready_for_transfer = Condition(lock = self.lock)
        self.target_wells = {}
        self.call_number = 0
        self.current_xfers = defaultdict(deque)
        self.finish_queue = AsyncFunctionSerializer(thread_name="OT-2 Finisher thread")
        
    def shutdown(self) -> None:
        with self.lock:
            self.system_running = False
            self.have_transfer.notify()
            
    def attach_to(self, board: Board) -> None:
        for i,w in enumerate(board.wells):
            self.target_wells[w] = f"W{i+1}"
        for i,ep in enumerate(board.extraction_points):
            self.target_wells[ep] = f"E{i+1}"
    
    async def message(self, request: Request) -> Response:
        try:
            body = await request.json()
        except json.JSONDecodeError:
            text = await body.text()
            logger.warning(f"Request was not json: {text}")
            return web.json_response(status=400, data = {"error": "bad-request"})
        
        msg = body["message"]
        stamp = time_now().strftime(fmt="%H:%M:%S")
        print(f"OT-2 [{stamp}]: {msg}")
        return web.json_response()
    
    async def exit(self, request: Request) -> Response: # @UnusedVariable
        # try:
        #     body = await request.json()
        # except json.JSONDecodeError:
        #     text = await body.text()
        #     print(f"Request was not json: {text}")
        #     return web.json_response(status=400, data = {"error": "bad-request"})
        logger.info("Shutting down OT2 listener")
        self.running = False
        raise GracefulExit()
    
    def well_volume_params(self, body: JSONObj) -> Optional[tuple[deque[XferTarget], Volume]]:
        w: Optional[str] = body.get("well", None)
        if w is None:
            return None
        v: float = body["volume"]
        return (self.current_xfers[w], v*uL)

    def handle_returned_params(self, body: JSONObj) -> None:
        wv = self.well_volume_params(body)
        if wv is not None:
            xfers,v = wv
            v = body["volume"]
            r = self.current_reagent 
            while v >= 0:
                assert xfers, f"Finished transfer with {v} unaccounted for."
                first = xfers[0]
                if v < first.volume:
                    first.finished(r, v)
                    break
                else:
                    first.finished(r, first.volume)
                    xfers.popleft()
                    v -= first.volume
    
    
    def package_transfer(self, transfer: Transfer) -> Response:
        body: JSONObj = {}
        body["reagent"] = "product" if transfer.is_product else transfer.reagent.name
        body["command"] = "fill" if transfer.xfer_dir is XferDir.FILL else "empty"
        
        merged: dict[PipettingTarget, VolAccum] = defaultdict(VolAccum)
        for t in transfer.targets:
            if t.allow_merge:
                merged[t.target] += t.volume
        merged_used = set[PipettingTarget]()
        target_descs: list[JSONObj] = []
        
        def target_desc(well: str, v: Volume) -> JSONObj:
            return {"well": well, "volume": v.as_number(uL)} 
        current_xfers = self.current_xfers
        current_xfers.clear()
        self.current_reagent = transfer.reagent
        for t in transfer.targets:
            pt = t.target
            well = self.target_wells[pt]
            current_xfers[well].append(t)
            if pt in merged:
                if pt not in merged_used:
                    target_descs.append(target_desc(well, merged[pt].total))
                    merged_used.add(pt)
            else:
                target_descs.append(target_desc(well, t.volume))
        body["targets"] = target_descs
        return web.json_response(data=body)
    
    
    def enqueue_finished(self, target: XferTarget, reagent: Reagent, volume: Volume) -> None:
        # print(f"/finished: {volume} of {reagent} @ {target.target}")
        self.finish_queue.enqueue(lambda: target.finished(reagent, volume))
        
    def enqueue_completely_finished(self, transfer: Transfer) -> None:
        def do_it() -> None:
            for t in transfer.targets:
                t.finished_overall_transfer(self.current_reagent)
        self.finish_queue.enqueue(do_it)
    
    
    async def waiting(self, request: Request) -> Response:
        logger.debug("Received waiting()")
        try:
            body = await request.json()
        except json.JSONDecodeError:
            text = await body.text()
            logger.warning(f"Request was not json: {text}")
            return web.json_response(status=400, data = {"error": "bad-request"})
        wv = self.well_volume_params(body)
        assert wv is not None, "/waiting called with no well/volume spec"
        xfers,v = wv
        r = self.current_reagent
        logger.debug(f"Waiting above {xfers[0].target}")
        xfers[0].in_position(r, v)
        return web.json_response()

    async def finished(self, request: Request) -> Response:
        logger.debug("Received finished()")
        try:
            body = await request.json()
        except json.JSONDecodeError:
            text = await body.text()
            logger.warning(f"Request was not json: {text}")
            return web.json_response(status=400, data = {"error": "bad-request"})
        wv = self.well_volume_params(body)
        assert wv is not None, "/finished called with no well/volume spec"
        xfers,v = wv
        r = self.current_reagent 
        # logger.debug(f"-- v: {v}, xfers: {map_str(xfers)}")
        while v > 0:
            assert xfers, f"Finished transfer at {body['well']} with {v} unaccounted for."
            first = xfers[0]
            # logger.debug(f"-- v: {v}, first: {first}")
            want = first.volume
            if want.is_close_to(v, abs_tol=0.01*uL):
                xfers.popleft()
                self.enqueue_finished(first, r, want)
                break
            elif v > want:
                xfers.popleft()
                self.enqueue_finished(first, r, want)
                v -= want
            else:
                self.enqueue_finished(first, r, v)
                break
        return web.json_response()
    
    async def ready(self, request: Request) -> Response:
        logger.debug("Received ready()")
        try:
            body = await request.json()
        except json.JSONDecodeError:
            text = await body.text()
            logger.warning(f"Request was not json: {text}")
            return web.json_response(status=400, data = {"error": "bad-request"})
        # The only way pending_transfer can be None is if this is the first time.  Otherwise
        # it's the last one we started.  Note that it might be non-None even on the first time
        # if the transfer request got there before the ready call.
        assert self.call_number == 0 or self.pending_transfer is not None
        if self.call_number > 0:
            assert self.pending_transfer is not None
            # First we enqueu calling finished_overall_transfer() for all of our targets
            self.enqueue_completely_finished(self.pending_transfer)
            
            product_well = body.get("product_well", None)
            if product_well is not None:
                xfer = self.pending_transfer.targets[0]
                assert isinstance(xfer, EmptyTarget), f"Received a product well for a non-empty transfer ({xfer})"
                product_loc = ProductLocation(self.pending_transfer.reagent, product_well)
                xfer.note_product_loc(product_loc)

            # Now we clear the pending transfer and signal that it's okay to add a new one.  
            # This will allow the pipettor's perform() to know that it is done.
            with self.lock:
                self.pending_transfer = None
                # print(f"Signalling ready_for_transfer: {self.pending_transfer}")
                self.ready_for_transfer.notify()
        # Now we wait until we have one
        with self.lock:
            while self.system_running and self.pending_transfer is None:
                self.have_transfer.wait()
            if self.system_running:
                self.call_number += 1
                assert self.pending_transfer is not None
                response = self.package_transfer(self.pending_transfer)
            else:
                response = web.json_response({"command": "exit"})
        # logger.debug(f"ready() response: {response}")
        return response
    
    def run(self) -> None:
        app = self.app = web.Application()
        app.router.add_post("/message", self.message)
        app.router.add_post("/exit", self.exit)
        app.router.add_post("/ready", self.ready)
        app.router.add_post("/finished", self.finished)
        app.router.add_post("/waiting", self.waiting)
        logger.info("Launching listener")
        self.running = True
        web.run_app(app,
                    host="0.0.0.0",
                    port=self.port)
        self.running = False
        logger.info("Shut down listener")
        
class ShutdownDetected(RuntimeError): ...
        
        
class ProtocolManager(Thread):
    ot_dir: Final[str]
    config: Final[JSONObj]
    ip: Final[str]
    port: Final[int]
    headers = {"Opentrons-Version": "2"}
    protocol_id: str
    session_id: str
    delay: Final[Time]
    last_msg: int = 0
    print_actions: Final[bool]
    no_ip: bool = False

    def __init__(self, config: JSONObj, *, 
                 name: str,
                 ot_dir: str = "../opentrons",
                 ip: str,
                 port: Union[str, int],
                 run_check: Optional[Union[Event, Callable[[], bool]]] = None,
                 delay: Time = 0.5*seconds,
                 print_actions: bool = True,
                 ) -> None:
        super().__init__(name=name)
        self.config = config
        self.ot_dir = ot_dir
        self.ip = ip
        if isinstance(port, str):
            port = int(port)
        self.port = port
        self.run_check: Callable[[], bool]
        if run_check is None:
            self.run_check = lambda: True
        elif isinstance(run_check, Event):
            rc = run_check
            self.run_check = lambda: rc.is_set()
        else:
            self.run_check = run_check 
        self.delay = delay
        self.print_actions = print_actions
        
    def ensure_config_endpoint(self, system: System, listener_port: Union[str, int]) -> None:
        config = self.config
        if not "endpoint" in config:
            ip = system.local_ip_addr
            if ip is None:
                self.no_ip = True
                return
            config["endpoint"] = {
                    "ip": ip,
                    "port": listener_port
                }
        logger.info(f"Listening for OT-2 on {config['endpoint']['ip']}:{config['endpoint']['port']}")
        
    def ot_file(self, path: str) -> str:
        return f"{self.ot_dir}/{path}"

    def make_url(self, cmd: str) -> str:
        return f"http://{self.ip}:{self.port}/{cmd}"
    
    def post_request(self, cmd: str, **kwd_args: Any) -> Any: 
        url = self.make_url(cmd)
        return requests.post(url=url, headers=self.headers,
                             **kwd_args).json()
                             
    def get_request(self, cmd: str, **kwd_args: Any) -> Any: 
        url = self.make_url(cmd)
        return requests.get(url=url, headers=self.headers,
                             **kwd_args).json()
                             
    def delete_request(self, cmd: str) -> requests.Response: 
        url = self.make_url(cmd)
        return requests.delete(url=url, headers=self.headers)
                             
    def trace_response(self, msg: str, response: Any) -> bool:
        if hasattr(response, "status_code"):
            status_code: int = response.status_code
            tag = f": status code = {status_code}"
        else:
            status_code = 200
            tag = "."
        result = status_code == 200
        json = response.json() if hasattr(response, "json") else response
        if data := json.get("data"):
            if errors := data.get("errors", None):
                result = False
                tag = f": ERRORS: {errors}"
        # status_code: int = response.status_code
        # print(f"{msg}: Response code = {status_code}")
        logger.info(f"{msg}{tag}")
        return result
        # return status_code == 200
        
    def concatenate_files(self, config: JSONObj, files: Sequence[str]) ->str:
        
        
        
        return "\n".join(["COMBINED_FILES_KLUDGE = True",
                         "".join([*fileinput.input(files=files)]),
                         f"config = {json.dumps(config)}\n"])

    def run(self) -> None:
        if self.no_ip:
            logger.error("There are no IP addresses for local machine.  Not uploading protocol to OT-2")
            return
        pname = f"protocol-{random.randint(0,1000000)}"
        
        use_multiple_files = False
        
        if use_multiple_files:
            config = json.dumps(self.config)
            response = self.post_request("protocols",
                                         files=[("protocolFile", (pname, open(self.ot_file("looping_protocol.py"), "rb"))),
                                                ("supportFiles", ("opentrons_support.py", open(self.ot_file("opentrons_support.py"), "rb"))),
                                                ("supportFiles", ("schedule_xfers.py", open(self.ot_file("schedule_xfers.py"), "rb"))),
                                                ("supportFiles", ("config.json", config)),
                                                ]
                                         )
        else:
            # combined = self.concatenate_files(self.config, [self.ot_file("schedule_xfers.py"),
            #                                                 self.ot_file("opentrons_support.py"),
            #                                                 self.ot_file("looping_protocol.py")]) 
            tmp = NamedTemporaryFile(prefix="protocol_", suffix=".py", delete=False, mode="w")
            logger.info(f"Temp protocol file is {tmp.name}")
            with tmp:
                tmp.write("from __future__ import annotations\n")
                tmp.write("__name__ = '__main__'\n")
                tmp.write("COMBINED_FILES_KLUDGE = True\n")
                lines: list[str] = []
                imports: list[str] = []
                for file in (self.ot_file("schedule_xfers.py"),
                              self.ot_file("opentrons_support.py"),
                              self.ot_file("looping_protocol.py")):
                    with open(file) as f:
                        for line in f.readlines():
                            if not line.startswith("from __future"):
                                if line.startswith("from ") or line.startswith("import"):
                                    imports.append(line)
                                else:
                                    lines.append(line)
                        lines.append("\n")
                for line in imports:
                    tmp.write(line)
                tmp.write("\n")
                for line in lines:
                    tmp.write(line)
                tmp.write(f"config = {json.dumps(self.config)}\n")
            payload = open(tmp.name, "rb")
            response = self.post_request("protocols", files={"files": payload})
            payload.close()
            # os.remove(tmp.name)
        
        logger.info(f"Create Protocol result: {response}")
        
        self.protocol_id = response['data']['id']
        self.trace_response(f"Created protocol \"{self.protocol_id}\"", response)
        try:
            if errors := response['data'].get("errors"):
                raise RuntimeError(f"Errors in protocol: {errors}")
            self.run_protocol()
        finally:
            response = self.delete_request(f"protocols/{self.protocol_id}")
            self.trace_response("Deleted protocol", response)
        
    def print_event(self, e: Any, prefix: str) -> None:
        global last_msg
        num = int(e["commandId"])
        if num > self.last_msg:
            text = e["params"]["text"]
            print(f"{prefix} {num}: {text}")
            self.last_msg = num
             
        
    def extract_messages(self, response: Any) -> None:
        pass
        # # events = response["data"]["details"]["events"]
        # events = response["data"]["actions"]
        # # printed_something = False
        # for e in events:
        #     # print(e)
        #     continue
        #     if e["source"] != "protocol":
        #         continue
        #
        #     if e["event"] == "command.COMMENT.start":
        #         self.print_event(e, "Msg")
        #     elif self.print_actions:
        #         self.print_event(e, "cmd")
        #

            
    def wait_until(self, looking_for: str) -> Any:
        global last_msg
        # last_state = ""
        while True:
            self.delay.sleep()
            if not self.run_check():
                raise ShutdownDetected()
            response = self.get_request(f"runs/{self.session_id}")
            # print(f"Get status result: {response}")
            current_state = response["data"]["status"]
            # print(f"Current state is {current_state}")
            self.extract_messages(response)
            if current_state == looking_for:
                return response
            elif current_state == "error":
                raise RuntimeError(f"Error encountered: {response}")
            # else:
            #     print(f"state = {current_state}")
                
            # if current_state != last_state or printed_something:
            #     print(f"Get status result: {current_state} {response}")
            #     last_state = current_state
            
    
    def run_protocol(self) -> None:
        response = self.post_request("runs",
                                    json = {
                                        "data": {"protocolId": self.protocol_id}
                                        }
                                     )
        if "data" not in response:
            logger.error(f"Couldn't create session: {response}")
        self.session_id = response["data"]["id"]
        self.trace_response(f'Created session "{self.session_id}"', response)
        
        try:
            # self.wait_until("loaded")
            response = self.post_request(f"runs/{self.session_id}/actions",
                                         data=json.dumps({"data":{"actionType": "play"}})
                                         # json={"data": {
                                         #     "data": {
                                         #         "actionType": "play",
                                         #         }
                                         #     }}
                                         )
            self.trace_response("Started run", response)
            response = self.wait_until("finished")
            logger.info("Run is complete")
            # print(response)
        except ShutdownDetected:
            ...
        except RuntimeError:
            traceback.print_exc()
        finally:
            response = self.delete_request(f"runs/{self.session_id}")
            self.trace_response("Deleted session", response)
            
    
        
class WellPlate:
    pipettor: Final[OT2]
    slot: Final[int]
    well_capacity: Final[Volume]
    wells: Final[Sequence[WPWell]]
    
    def __init__(self, pipettor: OT2, slot: int, *,
                 rows: int,
                 columns: int, 
                 well_capacity: Volume,
                 n_plates: int) -> None:
        self.pipettor = pipettor
        self.slot = slot
        self.well_capacity = well_capacity

        well_names = pipettor._generate_source_names(rows=rows, columns=columns, 
                                                     plates=1, start_plate=slot,
                                                     total_plates = n_plates)
        self.wells = [WPWell(n, plate=self, capacity=well_capacity) for n in well_names] 
        
    @classmethod
    def from_spec(cls, spec: dict, *,
                  pipettor: OT2, 
                  n_plates: int) -> WellPlate:
        name: str = spec["name"]
        slot: int = int(spec["slot"])
        m = re.search("_(\\d+)_.*_(\\d+)([um]l)", name, re.IGNORECASE)
        assert m is not None, f"Couldn't parse labware name {name}"
        n_wells = int(m[1])
        if n_wells == 1:
            rows,cols = 1,1
        elif n_wells == 6:
            rows,cols = 2,3
        elif n_wells == 24:
            rows,cols = 4,6
        elif n_wells == 96:
            rows,cols = 8,12
        elif n_wells == 384:
            rows,cols = 16,24
        elif n_wells == 1536:
            rows,cols = 32,48
        else:
            assert False, f"Don't know the configuration for a {n_wells}-well plate"
        u_spec: str = m[3].lower()
        if u_spec == "ml":
            unit = ml
        elif u_spec == "ul":
            unit = ul
        else:
            assert False, f"{u_spec} isn't a known unit for a wall plate capacity"
        capacity = int(m[2])*unit
        return WellPlate(pipettor, slot, rows=rows, columns=cols, 
                         well_capacity=capacity, n_plates=n_plates)
            
class WPWell(PipettingSource):
    plate: Final[WellPlate]
    
    def __init__(self, name: str, *,
                 plate: WellPlate,
                 capacity: Volume)->None:
        pipettor = plate.pipettor
        super().__init__(name, pipettor=pipettor, capacity=capacity)
        self.plate = plate
        pipettor._wells_by_name[name] = self
        def stash_on_reagent(r: Reagent) -> None:
            pipettor._wells_by_reagent[r].append(self)
            pipettor.dirty(self)
        self.assigned_reagent.when_value(stash_on_reagent)
        self.on_bounds_change(lambda _old,_new: pipettor.dirty(self))


class OT2(Pipettor):
    listener: Final[Listener]
    manager: Final[ProtocolManager]
    plates: Final[Sequence[WellPlate]]
    
    _wells_by_name: Final[dict[str, WPWell]]
    _wells_by_reagent: Final[dict[Reagent, list[WPWell]]]

    _lock: Final[RLock]
    _receiving_update: bool
    _dirty_wells: Optional[set[WPWell]] = None
    
    _listener_port: Final[int]
    
    def __init__(self, *,
                 name: str = "OT-2") -> None:
        super().__init__(name=name)
        self._lock = RLock()
        self._receiving_update = False
        
        robot_ip_addr = Config.robot_ip()
        robot_port = Config.robot_port()
        listener_port = Config.listener_port()
        config = Config.configuration()
        reagents = Config.reagents() 
        board_def = Config.board_def()
        
        if isinstance(listener_port, str):
            listener_port = int(listener_port)
        self._listener_port = listener_port
        
        self.listener = Listener(port=listener_port,
                                 name = f"{name} listener")
        
        if isinstance(robot_port, str):
            robot_port = int(robot_port)
        if isinstance(config, str):
            config = self.load_config(config)

        self._wells_by_name = {}
        self._wells_by_reagent = defaultdict(list)
            
        plate_specs: Sequence = config["input-wellplates"]
        n_plates = len(plate_specs)
        self.plates = [WellPlate.from_spec(s, pipettor=self, n_plates=n_plates) for s in plate_specs]
        
        rdesc: Sequence[dict]
        if reagents is None:
            rdesc = []
        elif isinstance(reagents, str):
            reagents_json = self.load_config(reagents)
            rdesc = reagents_json["reagents"]
        else:
            rdesc = [ { "name": r.name, "wells": [ w.as_json() for w in ws]} for r,ws in reagents.items()]
            
        config["reagents"] = rdesc
        
        for rd in rdesc:
            reagent = Reagent.find(rd["name"])
            rwells: Sequence[dict] = rd["wells"]
            for wd in rwells:
                well_name: str = wd["well"]
                quant: float = float(wd["quantity"])
                volume = quant*uL
                if len(self.plates) > 1:
                    plate: int = int(wd["plate"])
                    well_name += f"/{self.plates[plate].slot}"
                well = self.source_named(well_name)
                assert well is not None, f"Reagent spec says {reagent} in non-existent well {well_name}"
                well.reagent = reagent
                well.exact_volume = volume
        
        # if not "endpoint" in config:
        #     host_name = socket.gethostname()
        #     ip = socket.gethostbyname(host_name)
        #     config["endpoint"] = {
        #             "ip": ip,
        #             "port": listener_port
        #         }

        if board_def is not None:
            board_json = self.load_config(board_def)
            config["board"]["labware"]["definition"] = board_json
        self.manager = ProtocolManager(config, name = f"{name} protocol manager",
                                       ip = robot_ip_addr, port = robot_port,
                                       run_check = lambda: self.listener.running)
        
    def source_named(self, name: str) -> Optional[PipettingSource]:
        return self._wells_by_name.get(name, None)
    
    def sources_for(self, reagent: Reagent) -> Sequence[PipettingSource]:
        return self._wells_by_reagent[reagent]
    
    def describe_source(self, source: PipettingSource) -> str:
        assert isinstance(source, WPWell)
        return f"{source.name} (slot {source.plate.slot})"
    
    def dirty(self, well: WPWell) -> None:
        # _dirty_wells contains the wells that need to receive updates. The
        # logic here is that when we receive, we will lock and set
        # _receiving_update to True before changing any quantities.quant, so we don't
        # think we need to tell the robot about changes it already knows about.
        with self._lock:
            if not self._receiving_update:
                dirty_wells = self._dirty_wells
                if dirty_wells is None:
                    self._dirty_wells = {well}
                else:
                    dirty_wells.add(well)
        
    def load_config(self, file_name: str) -> JSONObj:
        with open(file_name, 'rb') as f:
            return cast(JSONObj, json.load(f))
        
    def join_system(self, system: System) -> None:
        super().join_system(system)
        self.listener.attach_to(system.board)
        self.listener.start()
        self.manager.ensure_config_endpoint(system, self._listener_port)
        self.manager.start()
        

    def system_shutdown(self) -> None:
        logger.info("Pipettor shutdown requested")
        self.listener.shutdown()
        
        
    def perform(self, transfer:Transfer) -> None:
        listener = self.listener
        with listener.lock:
            while listener.pending_transfer is not None:
                listener.ready_for_transfer.wait()
            listener.pending_transfer = transfer
            listener.have_transfer.notify()
        # Now we wait until it's done
        with listener.lock:
            while listener.pending_transfer is not None:
                # print(f"Waiting on ready_for_transfer: {listener.pending_transfer}")
                listener.ready_for_transfer.wait()

class PipettorConfig(exerciser.PipettorConfig):
    def __init__(self) -> None:
        super().__init__("opentrons", OT2, aliases=("ot", "ot2"))

    def create(self) -> Pipettor:

        pipettor = OT2()
        return pipettor
    
    def add_args_to(self, group:_ArgumentGroup)->None:
        super().add_args_to(group)
        
        Config.robot_ip.add_arg_to(group, "-otip", "--ot-ip", metavar="IP",
                                   help="The IP address of the Opentrons robot")
        Config.robot_port.add_arg_to(group, "-otrp", "--ot-port", metavar="PORT",
                                    type=int, 
                                    help=f"The port to call on the Opentrons robot")
        Config.robot_ip.raise_on_no_default(lambda _cp: ValueError(f"--ot-ip must be specified to use the Opentrons pipettor"))

        Config.configuration.add_arg_to(group, "-otc", "--ot-config", metavar="FILE",
                                        help="The config file for the the Opentrons robot")
        Config.configuration.raise_on_no_default(lambda _cp: ValueError(f"--ot-config must be specified to use the Opentrons pipettor"))
        Config.reagents.add_arg_to(group, "-otr", "--ot-reagents", metavar="FILE",
                                   help=f"The reagents JSON file for the the Opentrons robot")
        Config.listener_port.add_arg_to(group, "-otlp", "--ot-listener-port", metavar="PORT",
                                        type=int, 
                                        help=f"The port for the local listener for the Opentrons robot")
