from __future__ import annotations

from abc import abstractmethod, ABC
from threading import Lock
from typing import Final, Callable, Optional, Sequence, Any
import logging

from erk.errors import ErrorHandler, PRINT
from mpam.device import SystemComponent, UserOperation, PipettingTarget, System, \
    ProductLocation
from mpam.types import Reagent, OpScheduler, Callback, DelayType, \
    Liquid, Operation, Delayed, AsyncFunctionSerializer, T, XferDir, \
    unknown_reagent, MixResult, Postable, MonitoredProperty, ChangeCallbackList
from quantities.SI import uL
from quantities.dimensions import Volume
from mpam.engine import Worker
from erk.stringutils import map_str
import math

logger = logging.getLogger(__name__)


class XferTarget(ABC):
    target: Final[PipettingTarget]
    volume: Volume
    allow_merge: Final[bool]
    on_unknown: Final[ErrorHandler]
    on_insufficient: Final[ErrorHandler]
    got: Volume

    future: Final[Postable[Liquid]]

    def __init__(self, target: PipettingTarget, volume: Volume,
                 *,
                 future: Postable[Liquid],
                 allow_merge: bool,
                 on_unknown: ErrorHandler,
                 on_insufficient: ErrorHandler,
                 ) -> None:
        self.target = target
        self.volume = volume
        self.got = Volume.ZERO
        self.allow_merge = allow_merge
        self.future = future
        self.on_insufficient = on_insufficient
        self.on_unknown = on_unknown

    @property
    @abstractmethod
    def insufficient_msg(self) -> str: ...
    
    def __str__(self) -> str:
        return f"{type(self).__name__}[{self.volume} ({self.got}) @ {self.target}]"

    @abstractmethod
    def in_position(self, reagent: Reagent, volume: Volume) -> None: # @UnusedVariable
        ...

    def finished(self, reagent: Reagent, volume: Volume) -> None:
        self.got += volume
        last = self.got >= self.volume
        self.signal_done(reagent, volume, last=last)
        if last:
            liquid = Liquid(reagent, self.got)
            self.future.post(liquid)

    @abstractmethod
    def signal_done(self, reagent: Reagent, volume: Volume, *, last: bool) -> None: # @UnusedVariable
        ...
    def finished_overall_transfer(self, reagent: Reagent) -> None:
        future = self.future
        if not future.has_value:
            self.signal_done(reagent, Volume.ZERO, last=True)
            self.on_insufficient(self.insufficient_msg)
            future.post(Liquid(reagent, self.got))

class FillTarget(XferTarget):
    mix_result: Final[Optional[MixResult]]

    @property
    def insufficient_msg(self) -> str:
        expected = self.volume.in_units(uL)
        got = self.got.in_units(uL)
        return f"Expected {expected} transfered to {self.target}, only got {got}."

    def __init__(self, target: PipettingTarget, volume: Volume,
                 *,
                 future: Postable[Liquid],
                 allow_merge: bool,
                 mix_result: Optional[MixResult],
                 on_unknown: ErrorHandler,
                 on_insufficient: ErrorHandler) -> None:
        super().__init__(target, volume, future=future, allow_merge=allow_merge,
                         on_unknown=on_unknown, on_insufficient=on_insufficient)
        self.mix_result = mix_result

    def in_position(self, reagent: Reagent, volume: Volume) -> None: # @UnusedVariable
        self.target.prepare_for_add()

    def signal_done(self, reagent: Reagent, volume: Volume, *, last: bool) -> None:
        mix_result = self.mix_result if self.got >= self.volume else None
        self.target.pipettor_added(reagent, volume, mix_result=mix_result, last=last)



class EmptyTarget(XferTarget):
    product_loc: Final[Optional[Postable[ProductLocation]]]

    def __init__(self, target: PipettingTarget, volume: Volume,
                 *,
                 future: Postable[Liquid],
                 allow_merge: bool,
                 product_loc: Optional[Postable[ProductLocation]],
                 on_unknown: ErrorHandler,
                 on_insufficient: ErrorHandler) -> None:
        super().__init__(target, volume, future=future, allow_merge=allow_merge,
                         on_unknown=on_unknown, on_insufficient=on_insufficient)
        self.product_loc = product_loc

    @property
    def insufficient_msg(self) -> str:
        expected = self.volume.in_units(uL)
        got = self.got.in_units(uL)
        return f"Expected {expected} transfered from {self.target}, only took {got}."

    def in_position(self, reagent: Reagent, volume: Volume) -> None: # @UnusedVariable
        self.target.prepare_for_remove()

    def signal_done(self, reagent: Reagent, volume: Volume, *, last: bool) -> None:
        self.target.pipettor_removed(reagent, volume, last=last)

    def note_product_loc(self, loc: ProductLocation) -> None:
        if self.product_loc is not None:
            self.product_loc.post(loc)


class Transfer:
    reagent: Final[Reagent]
    xfer_dir: Final[XferDir]
    targets: list[XferTarget]
    is_product: Final[bool]
    pending: bool

    def __init__(self, reagent: Reagent, xfer_dir: XferDir, *, is_product: bool = False) -> None:
        self.reagent = reagent
        self.xfer_dir = xfer_dir
        self.is_product = is_product
        self.targets = []
        self.pending = True
        
    def __repr__(self) -> str:
        targets = [f"{t.target}: {t.volume}" for t in self.targets]
        return f"Transfer({self.xfer_dir}, {self.reagent}, {map_str(targets)}"
        
    @property
    def total_volume(self) -> Volume:
        return sum((x.volume for x in self.targets), start = Volume.ZERO)

class TransferSchedule:
    pipettor: Final[Pipettor]
    fills: Final[dict[Reagent, Transfer]]
    empties: Final[dict[Reagent, Transfer]]
    _lock: Final[Lock]
    serializer: Final[AsyncFunctionSerializer]


    def __init__(self, pipettor: Pipettor) -> None:
        self.pipettor = pipettor
        self.fills = {}
        self.empties = {}
        self._lock = Lock()
        self.serializer = AsyncFunctionSerializer(thread_name=f"{pipettor} Thread",
                                                  on_empty_queue = lambda: self.pipettor.idle(),
                                                  on_nonempty_queue = lambda: self.pipettor.not_idle())

    def _schedule(self,
                  reagent_map: Optional[dict[Reagent, Transfer]],
                  target: XferTarget,
                  reagent: Reagent) -> None:
        with self._lock:
            xfer = None if reagent_map is None else reagent_map.get(reagent, None)
            if xfer is None or not xfer.pending:
                xd = XferDir.FILL if reagent_map is self.fills else XferDir.EMPTY
                is_product = reagent_map is None
                xfer = Transfer(reagent, xd, is_product=is_product)
                if reagent_map is not None:
                    reagent_map[reagent] = xfer
                real_xfer = xfer
                def run_it() -> None:
                    with self._lock:
                        real_xfer.pending = False
                    self.pipettor.perform(real_xfer)
                self.serializer.enqueue(run_it)
            xfer.targets.append(target)

    def add(self,
            target: PipettingTarget,
            reagent: Reagent,
            volume: Volume,
            *,
            future: Postable[Liquid],
            allow_merge: bool = False,
            mix_result: Optional[MixResult] = None,
            on_insufficient: ErrorHandler = PRINT,
            on_unknown: ErrorHandler = PRINT) -> None:
        xt = FillTarget(target, volume,
                        future=future, allow_merge=allow_merge,
                        mix_result=mix_result,
                        on_insufficient=on_insufficient,  on_unknown=on_unknown)
        self._schedule(self.fills, xt, reagent)

    def remove(self,
               target: PipettingTarget,
               reagent: Reagent,
               volume: Volume,
               *,
               future: Postable[Liquid],
               allow_merge: bool = False,
               on_insufficient: ErrorHandler = PRINT,
               on_unknown: ErrorHandler = PRINT,
               is_product: bool,
               product_loc: Optional[Postable[ProductLocation]]) -> None:
        transfer_dict = None if is_product else self.empties
        xt = EmptyTarget(target, volume,
                        future=future, allow_merge=allow_merge,
                        product_loc=product_loc,
                        on_insufficient=on_insufficient,  on_unknown=on_unknown)
        self._schedule(transfer_dict, xt, reagent)


VolumeRange = tuple[Volume,Volume]

class PipettingSource:
    name: Final[str]
    capacity: Final[Volume]
    pipettor: Final[Pipettor]
    
    _desc: Optional[str] = None
    
    _reagent: Optional[Reagent] = None
    assigned_reagent: Final[Delayed[Reagent]]

    bounds: MonitoredProperty[VolumeRange] = MonitoredProperty()
    on_bounds_change: ChangeCallbackList[VolumeRange] = bounds.callback_list
    
    @bounds.transform
    def _clip_bounds(self, volume_range: VolumeRange) -> VolumeRange:
        low,high = volume_range
        assert low <= high, f"Setting {self} to out-of-order bounds: {volume_range}"
        low = self._clip(low)
        high = self._clip(high)
        return low,high
    
    @property
    def min_volume(self) -> Volume:
        return self.bounds[0]
         
    @property
    def max_volume(self) -> Volume:
        return self.bounds[1]
    
    def _clip(self, v: Volume) -> Volume:
        return min(max(v, Volume.ZERO), self.capacity)
    
    
    @property
    def exact_volume(self) -> Optional[Volume]:
        low,high = self.bounds
        return low if low == high else None
    
    @exact_volume.setter
    def exact_volume(self, volume: Volume) -> None:
        self.bounds = (volume,volume)
    
    @property
    def reagent(self) -> Optional[Reagent]:
        return self._reagent
    
    @reagent.setter
    def reagent(self, reagent: Reagent) -> None:
        my_reagent = self.reagent
        if my_reagent is not None and my_reagent is not reagent:
            raise ValueError(f"Can't assign {reagent} to {self}.  Already assigned {self.reagent}")
        self._reagent = reagent
        postable = self.assigned_reagent
        assert isinstance(postable, Postable)
        postable.post(reagent)
    
    @property
    def is_assigned(self) -> bool:
        return self.reagent is not None
    
    def __init__(self, name: str, *,
                 pipettor: Pipettor,
                 capacity: Optional[Volume] = None,
                 reagent: Optional[Reagent] = None,
                 volume: Optional[Volume] = None) -> None:
        self.name = name
        if capacity is None:
            capacity = math.inf*uL
        self.capacity = capacity
        self.pipettor = pipettor
        self._reagent = reagent
        
        future: Delayed[Reagent]
        if reagent is None:
            future = Postable()
        else:
            future = Delayed.complete(reagent)
        self.assigned_reagent = future
        
        if volume is None:
            self.bounds = (Volume.ZERO, capacity)
        else:
            self.bounds = (volume, volume)
            
            
    def __repr__(self) -> str:
        desc = self._desc
        if desc is None:
            desc = self.pipettor.describe_source(self)
            self._desc = desc
        contents = self.content_desc()
        if contents != "":
            contents = ", "+contents
        return f'{type(self).__name__}("{desc}"{contents})'
    
    def content_desc(self) -> str:
        reagent = self.reagent
        low,high = self.bounds
        if reagent is None:
            return ""
        elif low == high:
            return f"{Liquid(reagent, low)}"
        else:
            contents = f"{reagent}"
            if low > 0:
                contents += f", min={low:,g}"
            if high.is_finite:
                contents += f", max={high:,g}"
            return contents
            
    def __iadd__(self, v: Volume) -> PipettingSource:
        low, high = self.bounds
        self.bounds = (low+v, high+v)
        return self
        
    def __isub__(self, v: Volume) -> PipettingSource:
        low, high = self.bounds
        self.bounds = (low-v, high-v)
        return self
        
        

class PipettorSysCpt(SystemComponent):
    pipettor: Final[Pipettor]

    def __init__(self, pipettor: Pipettor) -> None:
        self.pipettor = pipettor

    def update_state(self)->None:
        pass

    def user_operation(self, *, desc: Optional[Any] = None) -> UserOperation:
        if desc is None:
            desc = self.pipettor
        return UserOperation(self.system.engine.idle_barrier, desc=desc)

    def system_shutdown(self) -> None:
        self.pipettor.system_shutdown()

class Pipettor(OpScheduler['Pipettor'], ABC):
    sys_cpt: Final[PipettorSysCpt]
    OpFunc = Callable[[], None]
    name: Final[str]
    worker: Worker

    xfer_sched: Final[TransferSchedule]

    def __init__(self, *, name: str="Pipettor") -> None:
        self.sys_cpt = PipettorSysCpt(self)
        self.name = name
        self.xfer_sched = TransferSchedule(self)

    def __str__(self) -> str:
        return f'Pipettor("{self.name}")'

    def idle(self) -> None:
        logging.info(f'{self} is idle')
        self.worker.idle()

    def not_idle(self) -> None:
        logging.info(f'{self} is not idle')
        self.worker.not_idle()

    @abstractmethod
    def perform(self, transfer: Transfer) -> None: ... # @UnusedVariable
    
    @abstractmethod
    def sources_for(self, reagent: Reagent) -> Sequence[PipettingSource]: # @UnusedVariable
        ...
        
    def source_for(self, reagent: Reagent) -> Optional[PipettingSource]:
        sources = self.sources_for(reagent)
        if len(sources) == 0:
            return None
        if len(sources) > 1:
            # Return the first one that might have content
            for source in sources:
                if source.max_volume > 0:
                    return source
        # If everybody is empty, just return the first
        return sources[0]
        
    @abstractmethod
    def source_named(self, name: str) -> Optional[PipettingSource]: # @UnusedVariable
        ...
        
    def describe_source(self, source: PipettingSource) -> str:
        return source.name
    
    @classmethod
    def _generate_source_names(cls, *, rows: int = 8, columns: int = 12,
                               plates: int = 1,
                               start_plate: int = 1,
                               total_plates: int = 0) -> list[str]:
        a = ord("A")
        if total_plates == 0:
            total_plates = start_plate+plates-1
        def name(r: int, c: int, p: int) -> str:
            pd = "" if total_plates == 1 else f"/{p}"
            return f"{chr(a+r)}{c+1}{pd}"
        return [name(r,c,p) 
                for p in range(start_plate, start_plate+plates)
                for r in range(rows)
                for c in range(columns)]

    def _generate_sources_named(self, names: Sequence[str], *,
                                factory: Optional[Callable[[str, Pipettor, Volume], PipettingSource]] = None,
                                capacity: Volume = math.inf*uL,
                                ) -> list[PipettingSource]:
        if factory is None:
            factory = lambda n,p,c: PipettingSource(n, pipettor=p, capacity=c)
        return [factory(n,self,capacity) for n in names]
    
        
    def join_system(self, system: System) -> None:
        self.sys_cpt.join_system(system)
        self.worker = Worker(system.engine.idle_barrier, desc = self)

    def system_shutdown(self) -> None:
        pass

    def schedule_communication(self, cb: Callable[[], Optional[Callback]], *,
                               after: Optional[DelayType] = None) -> None:
        return self.sys_cpt.schedule(cb, after=after)

    def delayed(self, function: Callable[[], T], *,
                after: Optional[DelayType]) -> Delayed[T]:
        return self.sys_cpt.delayed(function, after=after)


    class Supply(Operation['Pipettor', Liquid]):
        reagent: Final[Reagent]
        volume: Final[Volume]
        target: Final[PipettingTarget]
        allow_merge: Final[bool]
        mix_result: Final[Optional[MixResult]]
        on_insufficient: Final[ErrorHandler]
        on_no_source: Final[ErrorHandler]

        def __init__(self, reagent: Reagent, volume: Volume, 
                     target: PipettingTarget, *,
                     allow_merge: bool = False,
                     mix_result: Optional[MixResult] = None,
                     on_insufficient: ErrorHandler=PRINT,
                     on_no_source: ErrorHandler=PRINT

                     ) -> None:
            self.reagent = reagent
            self.volume = volume
            self.target = target
            self.allow_merge = allow_merge
            self.mix_result = mix_result
            self.on_insufficient = on_insufficient
            self.on_no_source = on_no_source

        def _schedule_for(self, pipettor: Pipettor, *,
                          after: Optional[DelayType]=None,
                          post_result: bool=True, # @UnusedVariable
                          ) -> Delayed[Liquid]:

            future = Postable[Liquid]()
            def schedule_it() -> None:
                pipettor.xfer_sched.add(self.target, self.reagent, self.volume,
                                        future=future, allow_merge=self.allow_merge,
                                        mix_result=self.mix_result,
                                        on_unknown=self.on_no_source, on_insufficient=self.on_insufficient)

            pipettor.delayed(schedule_it, after=after)
            return future

    class Extract(Operation['Pipettor', Liquid]):
        volume: Final[Optional[Volume]]
        reagent: Final[Optional[Reagent]]
        target: Final[PipettingTarget]
        allow_merge: Final[bool]
        on_no_sink: Final[ErrorHandler]
        on_insufficient_space: Final[ErrorHandler]
        on_no_liquid: Final[ErrorHandler]
        is_product: Final[bool]
        product_loc: Final[Optional[Postable[ProductLocation]]]

        def __init__(self, volume: Optional[Volume], target: PipettingTarget, *,
                     on_no_sink: ErrorHandler=PRINT,
                     on_insufficient_space: ErrorHandler=PRINT,
                     on_no_liquid: ErrorHandler=PRINT,
                     allow_merge: bool = False,
                     is_product: bool = False,
                     product_loc: Optional[Postable[ProductLocation]] = None,
                     reagent: Optional[Reagent] = None
                     ) -> None:
            self.volume = volume
            self.target = target
            self.allow_merge = allow_merge
            self.on_no_sink = on_no_sink
            self.on_insufficient_space = on_insufficient_space
            self.is_product = is_product
            self.on_no_liquid = on_no_liquid
            self.reagent = reagent
            self.product_loc = product_loc

        def _schedule_for(self, pipettor: Pipettor, *,
                          after: Optional[DelayType]=None,
                          post_result: bool=True, # @UnusedVariable
                          ) -> Delayed[Liquid]:

            future = Postable[Liquid]()
            def schedule_it() -> None:
                target = self.target
                contents = target.removable_liquid
                volume = self.volume
                if volume is None:
                    if contents is None:
                        self.on_no_liquid(f"No volume specified on extraction from {target}, which is empty")
                        future.post(Liquid(unknown_reagent, Volume.ZERO))
                        return
                    else:
                        volume = contents.volume
                reagent = self.reagent
                if reagent is None:
                    reagent = unknown_reagent if contents is None else contents.reagent
                pipettor.xfer_sched.remove(target, reagent, volume,
                                           future=future, allow_merge=self.allow_merge,
                                           on_unknown=self.on_no_sink, on_insufficient=self.on_insufficient_space,
                                           is_product = self.is_product, product_loc=self.product_loc)
            pipettor.delayed(schedule_it, after=after)
            return future
