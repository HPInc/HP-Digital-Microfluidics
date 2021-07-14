from __future__ import annotations

from _collections import deque, defaultdict
from threading import Lock
from typing import Final, NamedTuple, Sequence, Literal, Union, Optional, \
    Iterator, Any, Callable

from mpam.device import Heater, Pad
from mpam.drop import Drop
from mpam.paths import Path
from mpam.processes import MultiDropProcessType, FinishFunction, PairwiseMix
from mpam.types import Delayed, Dir
from quantities.dimensions import Time
from quantities.temperature import TemperaturePoint, absolute_zero
from quantities.timestamp import time_now, Timestamp
from erk.basic import not_None


class ChannelEndpoint(NamedTuple):
    heater_no: int
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

    def step_target(self, drop: Drop, i: int) -> Pad:
        d = self.adjacent_step_dir if i%2==0 else self.in_dir
        return not_None(drop.pad.neighbor(d))
    

Channel = tuple[ChannelEndpoint, ChannelEndpoint]

ChannelEnd = Union[Literal[0], Literal[1]]

class Thermocycler:
    heaters: Final[Sequence[Heater]]
    channels: Final[Sequence[Channel]]
        
    def __init__(self, *,
                 heaters: Sequence[Heater],
                 channels: Sequence[Channel]):
        self.heaters = heaters
        self.channels = channels

class ThermocyclePhase(NamedTuple):
    name: str
    temperature: TemperaturePoint
    duration: Time
    
    def __repr__(self) -> str:
        return f"ThermocyclePhase({self.name}, {self.temperature}, {self.duration})"
    
class HeaterState:
    heaters: Final[Sequence[Heater]]
    target: Optional[TemperaturePoint] = None
    ready: bool
    ready_time: Timestamp
    lock: Final[Lock]
    
    def __init__(self, heater: Sequence[Heater]) -> None:
        self.heaters = heater
        self.lock = Lock()
        
    def change_to(self, target: Optional[TemperaturePoint]) -> Delayed[Timestamp]:
        val_future = Delayed[Timestamp]()
        if self.target is not None and self.target == target:
            val_future.post(self.ready_time)
        else:
            self.target = target
            self.ready = False
            needed = len(self.heaters)
            def update(_) -> None:
                nonlocal needed
                with self.lock:
                    if needed == 1:
                        now = self.ready_time = time_now()
                        val_future.post(now)
                        self.ready = True
                    else:
                        needed -= 1
            for heater in self.heaters:
                future = heater.schedule(Heater.SetTemperature(target))
                future.then_call(update)
        return val_future
     
class BoundChannel(NamedTuple):
    drop: Drop
    channel: Channel
    
    def step_in(self, end: ChannelEnd, rendezvous: Rendezvous) -> None:
        ep = self.channel[end]
        ep.in_path \
            .then_process(lambda _: rendezvous.reached()) \
            .schedule_for(self.drop)
    def step_out(self, end: ChannelEnd, rendezvous: Rendezvous) -> None:
        ep = self.channel[end]
        ep.out_path \
            .then_process(lambda _: rendezvous.reached()) \
            .schedule_for(self.drop)
    def switch_ends(self, end: ChannelEnd, rendezvous: Rendezvous) -> None:
        ep = self.channel[end]
        ep.switch_path \
            .then_process(lambda _: rendezvous.reached()) \
            .schedule_for(self.drop)
            
    def step_target(self, end: ChannelEnd, i: int) -> Pad:
        ep = self.channel[end]
        return ep.step_target(self.drop, i)
    
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
        


class ThermocycleProcessType(MultiDropProcessType):
    thermocycler: Final[Thermocycler]
    phases: Final[Sequence[ThermocyclePhase]]
    n_iterations: Final[int]
    channels: Final[Sequence[int]]
    
    class FindLeadResult(NamedTuple):
        index_in_seq: int
        end: ChannelEnd
        channel: Channel
    
    
    def __init__(self,
                 thermocycler: Thermocycler, 
                 *,
                 channels: Sequence[int],
                 phases: Sequence[ThermocyclePhase],
                 n_iterations: int) -> None:
        super().__init__(len(channels))
        self.thermocycler = thermocycler
        self.channels = channels
        self.phases = phases
        self.n_iterations = n_iterations
        
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
    
    # returns None if the iterator still has work to do.  Otherwise, returns a function that will 
    # be called after the last tick.  This function returns True if the passed-in futures should 
    # be posted.
   
    def iterator(self, drops: tuple[Drop, ...])->Iterator[Optional[FinishFunction]]:
        tc = self.thermocycler
        channels_used = set(self.channels)
        
        channels = tuple(tc.channels[i] for i in channels_used)
        # maybe_drops = tuple(drops[i] if i in channels_used else None for )

        lead_drop = drops[0]
        board = lead_drop.pad.board
        system = board.in_system()
        flr = self.find_lead(lead_drop.pad)
        this_end: ChannelEnd = flr.end
        other_end: ChannelEnd = 1 if this_end == 0 else 0
        
        these_heaters = HeaterState(tuple(tc.heaters[i] 
                                          for i in set(c[this_end].heater_no for c in channels)))
        those_heaters = HeaterState(tuple(tc.heaters[i] 
                                          for i in set(c[other_end].heater_no for c in channels)))

        mapping = { c[this_end].threshold: i for i,c in enumerate(channels) }
        bound = tuple(BoundChannel(d,c) for c,d in zip(channels,
                                                       sorted(drops, key=lambda d: mapping[d.pad])))
        
        phases = tuple(self.phases) * self.n_iterations
        
        downs = deque(p.temperature for i,p in enumerate(phases[1:]) if p.temperature < phases[i].temperature)
        
        pmix = PairwiseMix(0,1)
        
        def all_channels(fn: Callable[[BoundChannel], Any]) -> None:
            with system.batched():
                for bc in bound:
                    fn(bc)

        rendezvous = Rendezvous(len(drops))
        
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
                    yield None
                in_zone = False
                if len(downs) > 0:
                    these_heaters.change_to(downs.popleft())
                else:
                    these_heaters.change_to(None)
                rendezvous.reset()
                all_channels(lambda bc: bc.switch_ends(this_end, rendezvous))
                while not rendezvous.ready:
                    yield None
                (this_end, other_end) = (other_end, this_end)
                (these_heaters, those_heaters) = (those_heaters, these_heaters)

            current_temp = target
            if not in_zone:
                while not these_heaters.ready:
                    yield None
                rendezvous.reset()
                all_channels(lambda bc: bc.step_in(this_end, rendezvous))
                while not rendezvous.ready:
                    yield None
                in_zone = True
                start_clock(time_now())
                step_no = -1
            while not these_heaters.ready or time_now() < walk_until:
                step_no += 1
                # print(f"step number {step_no}, end={this_end}")
                targets = defaultdict[Pad, list[Drop]](list)
                for bc in bound:
                    t = bc.step_target(this_end, step_no)
                    targets[t].append(bc.drop)
                # print(f"Targets = {targets}")
                rendezvous.reset()
                with system.batched():
                    for pad,drops in targets.items():
                        if len(drops) == 2:
                            # pads = (drops[0].pad, drops[1].pad)
                            # local_drops = drops
                            # We reach the rendezvous once for each drop
                            def mix_and_split(d1: Drop, d2: Drop):
                                my_drops = (d1, d2)
                                my_pads = (d1.pad, d2.pad)
                                # print(f"m&s: {my_pads}, {my_drops}")
                                pmix.merge(my_drops) \
                                    .then_call(lambda _: pmix.split(my_drops, my_pads) \
                                                            .then_call(reached_rendezvous) \
                                                            .then_call(reached_rendezvous))
                            mix_and_split(drops[0], drops[1])
                            # d1,d2 = drops
                            # p1,p2 = d1.pad,d2.pad
                            # pmix.merge((d1,d2)) \
                                # .then_call(lambda _: pmix.split((d1,d2), (p1,p2))) \
                                # .then_call(reached_rendezvous) \
                                # .then_call(reached_rendezvous)
                            
                        else:
                            assert len(drops) == 1
                            current = drops[0].pad
                            if current.row == pad.row:
                                Path.to_col(pad.column) \
                                    .to_col(current.column) \
                                    .then_process(reached_rendezvous) \
                                    .schedule_for(drops[0])
                            else:
                                assert current.column == pad.column
                                Path.to_row(pad.row) \
                                    .to_row(current.row) \
                                    .then_process(reached_rendezvous) \
                                    .schedule_for(drops[0])
                while not rendezvous.ready:
                    yield None
                # assert False
        rendezvous.reset()
        all_channels(lambda bc: bc.step_out(this_end, rendezvous))
        while not rendezvous.ready:
            yield None
        these_heaters.change_to(None)
        while not these_heaters.ready or not those_heaters.ready:
            yield None
        yield lambda _: True
                    

