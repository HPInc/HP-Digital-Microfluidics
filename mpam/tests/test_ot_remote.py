from __future__ import annotations

import requests
from quantities.dimensions import Time
from quantities.SI import seconds
from time import sleep

ROBOT_IP_ADDRESS = "192.168.86.30"
ROBOT_PORT = "31950"

delay = 2*seconds

OT_DIR = "../src/opentrons"

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
    


def run():
    response = post_request("protocols",
                            files=[("protocolFile", open(ot_file("remote_protocol.py"), "rb")),
                                   ]
                            )
    print(f"Create Protocol result: {response}")
    protocol_id = response['data']['id']
    
    try:
        if errors := response['data'].get("errors"):
            raise RuntimeError("Errors in protocol: {errors}")
        run_protocol(protocol_id)
    finally:
        delete_request(f"protocols/{protocol_id}")
        
def wait_until(looking_for: str, *, session_id: str):
    while True:
        sleep_for(delay)
        response = get_request(f"sessions/{session_id}")
        print(f"Get status result: {response}")
        current_state = response["data"]["details"]["currentState"]
        if current_state == looking_for:
            return response
        elif current_state == "error":
            raise RuntimeError(f"Error encountered: {response}")
    
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
        delete_request(f"sessions/{session_id}")
        
if __name__ == "__main__":
    run()