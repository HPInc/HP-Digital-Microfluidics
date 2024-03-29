from __future__ import annotations

from _collections import deque, defaultdict
from enum import Enum, auto
from functools import cached_property
from threading import Lock
from typing import (Final, NamedTuple, Sequence, Literal, Union, Optional,
                    Iterator, Any, Callable, Mapping)

from sifu.basic import not_None
from sifu.grid import Dir
from sifu.sched import Delayed, Postable
from sifu.quant.dimensions import Time
from sifu.quant.temperature import TemperaturePoint, absolute_zero
from sifu.quant.timestamp import time_now, Timestamp

from .device import TemperatureControl, Pad
from .drop import Drop
from .paths import Path
from .processes import MultiDropProcessType, PairwiseMix, MultiDropProcessRun


class ChannelEndpoint(NamedTuple):
    heater: TemperatureControl
    threshold: Pad
    in_dir: Dir
    adjacent_step_dir: Dir
    switch_path: Path.Middle
    
    @property
    def in_path(self) -> Path.Middle:
        return Path.walk(self.in_dir)
    @property
    def out_path(self) -> Path.Middle:
        return Path.walk(self.in_dir.opposite)

    def step_target(self, drop: Drop, i: int, shuttle_dir: ShuttleDir) -> Pad:
        if shuttle_dir is ShuttleDir.FULL:
            d = self.adjacent_step_dir if i%2==0 else self.in_dir
        elif shuttle_dir is ShuttleDir.ROW_ONLY:
            d = self.in_dir
        else:
            d = self.adjacent_step_dir
        return not_None(drop.on_board_pad.neighbor(d))
    

Channel = tuple[ChannelEndpoint, ChannelEndpoint]

ChannelEnd = Union[Literal[0], Literal[1]]

class ShuttleDir(Enum):
    FULL = auto()
    ROW_ONLY = auto()
    COL_ONLY = auto()

class Thermocycler:
    # heaters: Final[Sequence[TemperatureControl]]
    channels: Final[Sequence[Channel]]
        
    def __init__(self, *,
                 # heaters: Sequence[TemperatureControl],
                 channels: Sequence[Optional[Channel]]):
        # self.heaters = heaters
        self.channels = tuple(c for c in channels if c is not None)
        
    def as_process(self, *,
                   phases: Sequence[ThermocyclePhase],
                   channels: Sequence[int],
                   n_iterations: int,
                   shuttle_dir: ShuttleDir = ShuttleDir.FULL
                   ) -> ThermocycleProcessType:
        return ThermocycleProcessType(self, phases=phases, channels=channels, n_iterations=n_iterations,
                                      shuttle_dir=shuttle_dir)

class ThermocyclePhase(NamedTuple):
    name: str
    temperature: TemperaturePoint
    duration: Time
    
    def __repr__(self) -> str:
        return f"ThermocyclePhase({self.name}, {self.temperature}, {self.duration})"
    
class HeaterState:
    heaters: Final[Sequence[TemperatureControl]]
    target: Optional[TemperaturePoint] = None
    ready: bool
    ready_time: Timestamp
    lock: Final[Lock]
    
    def __init__(self, heater: Sequence[TemperatureControl]) -> None:
        self.heaters = heater
        self.lock = Lock()
        
    def change_to(self, target: Optional[TemperaturePoint]) -> Delayed[Timestamp]:
        if self.target is not None and self.target == target:
            return Delayed.complete(self.ready_time)
        val_future = Postable[Timestamp]()
        self.target = target
        self.ready = False
        needed = len(self.heaters)
        def update(_: Any) -> None:
            nonlocal needed
            with self.lock:
                if needed == 1:
                    now = self.ready_time = time_now()
                    val_future.post(now)
                    self.ready = True
                else:
                    needed -= 1
        for heater in self.heaters:
            future = heater.schedule(TemperatureControl.SetTemperature(target))
            future.then_call(update)
        return val_future
     
class BoundChannel:
    drop: Drop
    channel: Final[Channel]
    
    def __init__(self, drop: Drop, channel: Channel) -> None:
        self.drop = drop
        self.channel = channel
        
    def done_fn(self, rendezvous: Rendezvous) -> Callable[[Drop], None]:
        def fn(drop: Drop) -> None:
            self.drop = drop
            rendezvous.reached()
        return fn
    
    def step_in(self, end: ChannelEnd, rendezvous: Rendezvous) -> None:
        ep = self.channel[end]
        (ep.in_path
            .then_process(self.done_fn(rendezvous))
            .schedule_for(self.drop))
    def step_out(self, end: ChannelEnd, rendezvous: Rendezvous) -> None:
        ep = self.channel[end]
        (ep.out_path
           .then_process(self.done_fn(rendezvous))
           .schedule_for(self.drop))
    def switch_ends(self, end: ChannelEnd, rendezvous: Rendezvous) -> None:
        ep = self.channel[end]
        (ep.switch_path
           .then_process(self.done_fn(rendezvous))
           .schedule_for(self.drop))
            
    def step_target(self, end: ChannelEnd, i: int, shuttle_dir: ShuttleDir) -> Pad:
        ep = self.channel[end]
        return ep.step_target(self.drop, i, shuttle_dir)
    
class Rendezvous:
    n_required: Final[int]
    lock: Final[Lock]
    n_reached: int
    ready: bool
    
    
    def __init__(self, required: int) -> None:
        self.n_required = required
        self.lock = Lock()
        self.reset()
        
    def reset(self) -> None:
        self.n_reached = 0
        self.ready = False
        
    def reached(self, n: int=1) -> int:
        with self.lock:
            val = self.n_reached
            self.n_reached += n
            # print(f"# {self.n_reached} reached")
            if val == self.n_required-1:
                # print(f"-- rendezvous finished")
                self.ready = True
            return val
        

class ThermocycleRun(MultiDropProcessRun['ThermocycleProcessType']):
    @cached_property
    def thermocycler(self) -> Thermocycler:
        return self.process_type.thermocycler
    
    @cached_property
    def phases(self) -> Sequence[ThermocyclePhase]:
        return self.process_type.phases

    @cached_property
    def n_iterations(self) -> int:
        return self.process_type.n_iterations

    @cached_property
    def channels(self) -> Sequence[int]:
        return self.process_type.channels

    @cached_property
    def shuttle_dir(self) -> ShuttleDir:
        return self.process_type.shuttle_dir
    
    
    def iterator(self) -> Iterator[bool]:
        tc = self.thermocycler
        shuttle_dir = self.shuttle_dir
        channels_used = set(self.channels)
        
        channels = tuple(tc.channels[i] for i in channels_used)
        # maybe_drops = tuple(drops[i] if i in channels_used else None for )

        pads = self.pads
        lead_pad = pads[0]
        board = lead_pad.board
        system = board.system
        flr = self.process_type.find_lead(lead_pad)
        this_end: ChannelEnd = flr.end
        other_end: ChannelEnd = 1 if this_end == 0 else 0
        
        these_heaters = HeaterState(tuple(set(c[this_end].heater for c in channels)))
        those_heaters = HeaterState(tuple(set(c[other_end].heater for c in channels)))

        mapping = { c[this_end].threshold: i for i,c in enumerate(channels) }
        bound = tuple(BoundChannel(p.checked_drop, c) 
                      for c,p in zip(channels, sorted(pads, key=lambda p: mapping[p])))
        
        phases = tuple(self.phases) * self.n_iterations
        
        downs = deque(p.temperature for i,p in enumerate(phases[1:]) if p.temperature < phases[i].temperature)
        
        pmix = PairwiseMix(0,1)
        
        def all_channels(fn: Callable[[BoundChannel], Any]) -> None:
            with system.batched():
                for bc in bound:
                    fn(bc)

        rendezvous = Rendezvous(len(pads))
        
        reached_rendezvous = lambda _: rendezvous.reached()
        
        in_zone = False
        if len(downs) > 0:
            those_heaters.change_to(downs.popleft())
        current_temp: TemperaturePoint = absolute_zero
        for phase in phases:
            # print(f"Starting {phase}")
            target = phase.temperature
            walk_until: Timestamp
            def start_clock(ts: Timestamp) -> None:
                # Not sure why MyPy is complaining that walk_until is unused.
                nonlocal walk_until
                walk_until = ts+phase.duration  # @UnusedVariable
            if target >= current_temp:
                these_heaters.change_to(target).then_call(start_clock)
            else:
                rendezvous.reset()
                all_channels(lambda bc: bc.step_out(this_end, rendezvous))
                while not rendezvous.ready:
                    yield True
                in_zone = False
                if len(downs) > 0:
                    these_heaters.change_to(downs.popleft())
                else:
                    these_heaters.change_to(None)
                rendezvous.reset()
                all_channels(lambda bc: bc.switch_ends(this_end, rendezvous))
                while not rendezvous.ready:
                    # BUG: MyPy 0.931 (9457).  MyPy incorrectly thinks that
                    # rendezvous.ready says Literal[True], even after the
                    # reset() call. https://github.com/python/mypy/issues/9457
                    yield True# type: ignore[unreachable]
                (this_end, other_end) = (other_end, this_end)
                (these_heaters, those_heaters) = (those_heaters, these_heaters)

            current_temp = target
            if not in_zone:
                while not these_heaters.ready:
                    yield True
                rendezvous.reset()
                all_channels(lambda bc: bc.step_in(this_end, rendezvous))
                while not rendezvous.ready:
                    yield True
                in_zone = True
                start_clock(time_now())
                step_no = -1
            while not these_heaters.ready or time_now() < walk_until:
                step_no += 1
                # print(f"step number {step_no}, end={this_end}")
                targets = defaultdict[Pad, list[Drop]](list)
                for bc in bound:
                    t = bc.step_target(this_end, step_no, shuttle_dir)
                    targets[t].append(bc.drop)
                # print(f"Targets = {targets}")
                rendezvous.reset()
                with system.batched():
                    for pad,drops in targets.items():
                        if len(drops) == 2:
                            # pads = (drops[0].pad, drops[1].pad)
                            # local_drops = drops
                            # We reach the rendezvous once for each drop
                            def mix_and_split(d1: Drop, d2: Drop) -> None:
                                my_pads = (d1.on_board_pad, d2.on_board_pad)
                                # print(f"m&s: {my_pads}, {my_drops}")
                                (pmix.merge(my_pads)
                                     .then_call(lambda _: (pmix.split(my_pads)
                                                               .then_call(reached_rendezvous)
                                                               .then_call(reached_rendezvous))))
                            mix_and_split(drops[0], drops[1])
                            
                        else:
                            assert len(drops) == 1
                            current = drops[0].pad
                            if current.row == pad.row:
                                (Path.to_col(pad.column)
                                     .to_col(current.column)
                                     .then_process(reached_rendezvous)
                                     .schedule_for(drops[0]))
                            else:
                                assert current.column == pad.column
                                (Path.to_row(pad.row)
                                     .to_row(current.row)
                                     .then_process(reached_rendezvous)
                                     .schedule_for(drops[0]))
                while not rendezvous.ready:
                    yield True
                # assert False
        rendezvous.reset()
        all_channels(lambda bc: bc.step_out(this_end, rendezvous))
        # print("Done with thermocycle")
        while not rendezvous.ready:
            yield True
        print("Rendezvous ready")
        these_heaters.change_to(None)
        while not these_heaters.ready or not those_heaters.ready:
            yield True
        yield False
    


class ThermocycleProcessType(MultiDropProcessType):
    thermocycler: Final[Thermocycler]
    phases: Final[Sequence[ThermocyclePhase]]
    n_iterations: Final[int]
    channels: Final[Sequence[int]]
    shuttle_dir: Final[ShuttleDir]
    
    class FindLeadResult(NamedTuple):
        index_in_seq: int
        end: ChannelEnd
        channel: Channel
    
    
    def __init__(self,
                 thermocycler: Thermocycler, 
                 *,
                 channels: Sequence[int],
                 phases: Sequence[ThermocyclePhase],
                 n_iterations: int,
                 shuttle_dir: ShuttleDir = ShuttleDir.FULL) -> None:
        super().__init__(len(channels))
        self.thermocycler = thermocycler
        self.channels = channels
        self.phases = phases
        self.n_iterations = n_iterations
        self.shuttle_dir = shuttle_dir
        # print(f"Thermocycling over {channels}")
        
    def create_run(self, *, 
                   futures: Mapping[Pad, Postable[Drop]], 
                   pads: tuple[Pad, ...]) -> ThermocycleRun:
        return ThermocycleRun(self, futures, pads)
        
    def find_lead(self, lead_drop_pad: Pad) -> FindLeadResult:
        for index,c in enumerate(self.thermocycler.channels[i] for i in self.channels):
            if c[0].threshold is lead_drop_pad:
                return self.FindLeadResult(index, 0, c)
            if c[1].threshold is lead_drop_pad:
                return self.FindLeadResult(index, 1, c)
        raise ValueError(f"{lead_drop_pad} is not a threshold pad for any of channels {self.channels}")
        
    def secondary_pads(self, lead_drop_pad: Pad) -> Sequence[Pad]:
        end = self.find_lead(lead_drop_pad).end
        channels = (self.thermocycler.channels[i] for i in self.channels)
        
        return tuple(c[end].threshold for c in channels if c[end].threshold is not lead_drop_pad)
    
    def pads(self, end: ChannelEnd) -> Sequence[Pad]:
        tc = self.thermocycler
        return tuple(tc.channels[i][end].threshold for i in self.channels)
    
