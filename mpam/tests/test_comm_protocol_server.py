from __future__ import annotations
from devices import opentrons

listener = opentrons.Listener()
listener.start()
# listener.join()