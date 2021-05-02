import time
from .SI import sec
from . import dimensions, core

def time_now() -> core.Quantity[dimensions.Time]:
    return time.time()*sec

def time_in(delta: core.Quantity[dimensions.Time]) -> core.Quantity[dimensions.Time]:
    return time_now()+delta

def time_since(ts: core.Quantity[dimensions.Time]) -> core.Quantity[dimensions.Time]:
    return ts-time_now()