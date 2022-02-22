from __future__ import annotations
from devices import opentrons

listener = opentrons.Listener(port=8087, name="OT-2 Listener")
listener.start()
# listener.join()