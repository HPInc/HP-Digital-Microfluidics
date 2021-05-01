import time
from .SI import sec

def time_now():
    return time.time()*sec

def time_in(delta):
    return time_now()+delta

def time_since(ts):
    return ts-time_now()