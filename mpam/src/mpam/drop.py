from __future__ import annotations
from mpam.types import Liquid, Dir, Delayed, OnOff
from mpam.device import Pad
from mpam.exceptions import NoSuchPad, UnsafeMotion
from mpam.engine import Callback

class Drop:
    liquid: Liquid
    pad: Pad
    
    def __init__(self, pad: Pad, liquid: Liquid) -> None:
        assert pad.drop is None, f"Trying to create a second drop at {pad}"
        self.liquid = liquid
        self.pad = pad
        pad._drop = self
        
    def __repr__(self) -> str:
        return f"Drop[{self.pad}, {self.liquid}]"
        
    def _move_fn(self, drop: Drop, from_pad: Pad, to_pad: Pad):
        def step() -> Callback:
            print(f"Moving from {from_pad} to {to_pad}")
            (from_pad.set_device_state)(OnOff.OFF)
            (to_pad.set_device_state)(OnOff.ON)
            def update() -> None:
                assert from_pad._drop is self, f"Moved {self}, but thought it was at {from_pad}"
                assert to_pad._drop is None, f"Moving {self} to non-empty {to_pad}"
                from_pad._drop = None
                drop.pad = to_pad
                to_pad._drop = drop
                print(f"Drop now at {to_pad}")
            return update
        return step
        
    def gated_move(self, direction: Dir, *, steps: int=1, allow_unsafe_motion: bool = False) -> Delayed[Drop]:
        board = self.pad._board
        system = board.in_system()
        future = Delayed[Drop]()
        with system.batched():
            last_pad: Pad = self.pad
            for delta in range(steps):
                next_pad = last_pad.neighbor(direction)
                if next_pad is None or next_pad.broken:
                    raise NoSuchPad(last_pad.location+direction)
                if not allow_unsafe_motion and not next_pad.safe():
                    raise UnsafeMotion(next_pad)
                step = self._move_fn(self, last_pad, next_pad)
                print(f"Scheduling {last_pad} to {next_pad} @ {delta}")
                board.on_tick(step, delta=delta)
                last_pad = next_pad
            def post() -> None:
                future.post(self)
            board.on_tick(post, delta=steps)
        return future
