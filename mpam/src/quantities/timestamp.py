import time
from .SI import sec
from . import dimensions

def time_now() -> dimensions.Time:
    return time.time()*sec

def time_in(delta: dimensions.Time) -> dimensions.Time:
    return time_now()+delta

def time_since(ts: dimensions.Time) -> dimensions.Time:
    return ts-time_now()