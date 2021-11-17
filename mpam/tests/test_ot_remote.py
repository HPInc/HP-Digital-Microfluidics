from __future__ import annotations

from enum import Enum, auto
import json
from time import sleep
from typing import Any, Sequence, Optional, Final

import requests

from mpam.types import Reagent
from quantities.SI import seconds, uL, ml
from quantities.dimensions import Time, Volume
import random


ROBOT_IP_ADDRESS = "192.168.86.30"
ROBOT_PORT = "31950"

delay = 0.5*seconds

OT_DIR = "../opentrons"

HEADERS = {"Opentrons-Version": "2"}

def ot_file(path: str) -> str:
    return f"{OT_DIR}/{path}"



def make_url(cmd: str) -> str:
    return f"http://{ROBOT_IP_ADDRESS}:{ROBOT_PORT}/{cmd}"

def post_request(cmd: str, **kwd_args): 
    url = make_url(cmd)
    return requests.post(url=url, headers=HEADERS,
                         **kwd_args).json()

def get_request(cmd: str, **kwd_args): 
    url = make_url(cmd)
    return requests.get(url=url, headers=HEADERS,
                         **kwd_args).json()

def delete_request(cmd: str): 
    url = make_url(cmd)
    return requests.delete(url=url, headers=HEADERS)
    
def sleep_for(time: Time) -> None:
    sleep(time.as_number(seconds))
    
JSONObj = dict[str, Any]

class Size(Enum):
    SMALL = auto(),
    LARGE = auto()
    
    
class Side(Enum):
    LEFT = auto(),
    RIGHT = auto()
    
class Config:
    extras: Final[JSONObj]
    large_pipette: Optional[JSONObj] = None
    small_pipette: Optional[JSONObj] = None
    large_tipracks: Final[list[JSONObj]]
    small_tipracks: Final[list[JSONObj]]
    input_wellplates: Final[list[JSONObj]]
    output_wellplates: Final[list[JSONObj]]
    reagents: Final[list[JSONObj]]
    joey: Optional[JSONObj] = None
    
    
    
    def __init__(self) -> None:
        self.extras = {}
        self.large_tipracks = []
        self.small_tipracks = []
        self.input_wellplates = []
        self.output_wellplates = []
        self.reagents = []

        
    def as_dict(self) -> JSONObj:
        return {
            **self.extras,
            "pipettes": { "large": self.large_pipette, "small": self.small_pipette },
            "tipracks": { "large": self.large_tipracks, "small": self.small_tipracks },
            "input-wellplates": self.input_wellplates,
            "output-wellplates": self.output_wellplates,
            "joey": self.joey,
            "reagents": self.reagents
        }

        
    def json(self)->str:
        return json.dumps(self.as_dict())
    
    def add_extra(self, key: str, val: Any) -> None:
        self.extras[key] = val
        
    def add_reagent(self, reagent: Reagent, 
                    wells: Sequence[tuple[int, str, Volume]]) -> None:
        r = {"name": reagent.name,
             "wells": [{"plate": p, 
                        "well": w,
                        "quantity": q.as_number(uL)} for p,w,q in wells]
             }
        self.reagents.append(r)
        
    def set_pipette(self,
                    size: Size,
                    name: str,
                    side: Side,
                    vol_range: tuple[Volume, Volume]) -> None:
        min_vol, max_vol = vol_range
        p = {"name": name, 
             "side": "left" if side is Side.LEFT else "right",
             "max": max_vol.as_number(uL),
             "min": min_vol.as_number(uL) 
             }
        if size is Size.LARGE:
            self.large_pipette = p
        else:
            self.small_pipette = p
            
    def labware(self, name: str, slot: int) -> JSONObj:
        return { "name": name, "slot": slot}
    
    def add_tiprack(self, size: Size, name: str, slot: int) -> None:
        lw = self.labware(name, slot)
        tipracks = self.large_tipracks if size is Size.LARGE else self.small_tipracks
        tipracks.append(lw)
        
    def add_input_wellplate(self, name: str, slot: int) -> None:
        self.input_wellplates.append(self.labware(name, slot))
    def add_output_wellplate(self, name: str, slot: int) -> None:
        self.output_wellplates.append(self.labware(name, slot))
        
    def set_joey(self, name: str, slot: int, *,
                 drop_size: Volume,
                 wells: Sequence[str],
                 extraction_ports: Sequence[str] = []
                 ) -> None:
        joey = { 
                    "labware": self.labware(name, slot),
                    "drop-size": drop_size.as_number(uL),
                    "wells": wells,
                    "extraction-ports": extraction_ports
                }
        self.joey = joey
        
        
    
def labware(name: str, slot: int) -> dict[str,Any]:
    return { "name": name, "slot": slot}    
    

def config_reagent(config: dict, name: str, 
                   wells: Sequence[tuple[int, str, Volume]]) -> None:
    reagents: list[dict[str, Any]] = config.setdefault("reagents", [])
    r = {"name": name,
         "wells": [{"plate": p, 
                    "well": w,
                    "quantity": q.as_number(uL)} for p,w,q in wells]
         }
    reagents.append(r)

def run() -> None:
    config = Config()
    config.set_pipette(Size.LARGE, "p300_single_gen2", Side.RIGHT, (20*uL, 300*uL))
    config.set_pipette(Size.SMALL, "p20_single_gen2", Side.LEFT, (1*uL, 20*uL))
    config.add_tiprack(Size.LARGE, "opentrons_96_filtertiprack_200ul", 3)
    config.add_tiprack(Size.SMALL, "opentrons_96_filtertiprack_20ul", 6)
    config.add_input_wellplate("nest_96_wellplate_2ml_deep", 1)
    config.add_output_wellplate("nest_96_wellplate_2ml_deep", 10)
    config.set_joey("biorad_96_wellplate_200ul_pcr", 8, drop_size=0.5*uL,
                    wells=["A1", "B1", "C1", "D1", "A2", "B2", "C2", "D2"],
                    extraction_ports=["A3", "B3", "C3"])
    
    config.add_reagent(Reagent.find("r1"), [(0, "A1", 2*ml)])
    config.add_reagent(Reagent.find("r2"), [(0, "B1", 2*ml)])
    config.add_reagent(Reagent.find("r3"), [(0, "C1", 2*ml)])
    config.add_reagent(Reagent.find("r4"), [(0, "D1", 2*ml)])
    
    print(config.json())

    pname = f"protocol-{random.randint(0,1000000)}"
    response = post_request("protocols",
                            files=[("protocolFile", (pname,open(ot_file("remote_protocol.py"), "rb"))),
                                   ("supportFiles", ("opentrons_support.py", open(ot_file("opentrons_support.py"), "rb"))),
                                   ("supportFiles", ("config.json", config.json())),
                                   ]
                            )
    print(f"Create Protocol result: {response}")
    protocol_id = response['data']['id']
    print(f"Protocol id is {protocol_id}")
    
    try:
        if errors := response['data'].get("errors"):
            raise RuntimeError(f"Errors in protocol: {errors}")
        run_protocol(protocol_id)
    finally:
        response = delete_request(f"protocols/{protocol_id}")
        print(f"Delete protocol_response: {response.status_code}")
        
last_msg = 0
print_all = True

def print_event(e, prefix: str) -> None:
    global last_msg
    num = int(e["commandId"])
    if num > last_msg:
        text = e["params"]["text"]
        print(f"{prefix} {num}: {text}")
        last_msg = num
    
def extract_messages(response) -> None:
    events = response["data"]["details"]["events"]
    # printed_something = False
    for e in events:
        if e["source"] != "protocol":
            continue
        
        if e["event"] == "command.COMMENT.start":
            print_event(e, "Msg")
        elif print_all:
            print_event(e, "cmd")
            
            

def wait_until(looking_for: str, *, session_id: str):
    global last_msg
    # last_state = ""
    while True:
        sleep_for(delay)
        response = get_request(f"sessions/{session_id}")
        # print(f"Get status result: {response}")
        current_state = response["data"]["details"]["currentState"]
        extract_messages(response)
        if current_state == looking_for:
            return response
        elif current_state == "error":
            raise RuntimeError(f"Error encountered: {response}")
        # if current_state != last_state or printed_something:
        #     print(f"Get status result: {current_state} {response}")
        #     last_state = current_state
    
def run_protocol(protocol_id: str):
    response = post_request("sessions",
                            json = {
                                "data": {
                                    "sessionType": "protocol",
                                    "createParams": {
                                        "protocolId": protocol_id
                                        }
                                    }
                                }
                            )
    print(f"Create session result: {response}")
    
    session_id = response["data"]["id"]
    print(f"Session ID: {session_id}")
    
    try:
        wait_until("loaded", session_id=session_id)
        response = post_request(f"sessions/{session_id}/commands/execute",
                                json={
                                    "data": {
                                        "command": "protocol.startRun",
                                        "data": {} 
                                        }
                                    })
        print(f"startRun result: {response}")
        response = wait_until("finished", session_id=session_id)
        print("Run is complete")
        print(response)
    finally:
        response = delete_request(f"sessions/{session_id}")
        print(f"Delete session response: {response.status_code}")
        
if __name__ == "__main__":
    run()