from __future__ import annotations

from abc import abstractmethod, ABC
from threading import Lock
from typing import Final, Union, Callable, Optional, Sequence, TypeVar

from erk.basic import not_None
from erk.errors import ErrorHandler, PRINT
from mpam.device import SystemComponent, Well, ExtractionPoint, UserOperation, \
    Pad
from mpam.drop import Drop, DropStatus
from mpam.types import Reagent, OpScheduler, Callback, RunMode, DelayType, \
    Liquid, Operation, Delayed, AsyncFunctionSerializer, T
from quantities.dimensions import Volume


class PipettorComponent:
    pipettor: Final[Pipettor]
    
    def __init__(self, pipettor: Pipettor) -> None:
        self.pipettor = pipettor
    def schedule_communication(self, cb: Callable[[], Optional[Callback]], mode: RunMode, *,  
                               after: Optional[DelayType] = None) -> None:  
        return self.pipettor.schedule(cb, mode=mode, after=after)
    
    def delayed(self, function: Callable[[], T], *,
                after: Optional[DelayType]) -> Delayed[T]:
        return self.pipettor.delayed(function, after=after)
 
    def user_operation(self) -> UserOperation:
        return UserOperation(self.pipettor.in_system().engine.idle_barrier)


class WellBlock(PipettorComponent, ABC):
    class Reservoir:
        well_block: Final[WellBlock]
        
        def __init__(self, well_block: WellBlock) -> None:
            self.well_block = well_block
            
    @abstractmethod
    def reservoir_for(self, reagent: Reagent) -> Optional[WellBlock.Reservoir]:  # @UnusedVariable
        ...


Target = Union[Well, ExtractionPoint, WellBlock.Reservoir]

_Target = TypeVar("_Target", bound=Union[Well, ExtractionPoint])

DeliveryCallback = Callable[[_Target, Liquid], Delayed[None]]
TransferSpec = tuple[_Target, Volume, Delayed[Liquid]]

class FillRequest:
    well: Final[Well]
    liquid: Final[Liquid]
    when_done: Final[Delayed[Liquid]]
    mix_result: Final[Optional[Union[Reagent, str]]]
    on_insufficient: Final[ErrorHandler]
    on_no_source: Final[ErrorHandler]
    
    @property
    def volume(self) -> Volume:
        return self.liquid.volume
    def reagent(self) -> Reagent:
        return self.liquid.reagent
    
    def __init__(self, liquid: Liquid, well: Well, *,
                 when_done: Delayed[Liquid],
                 mix_result: Optional[Union[Reagent, str]]=None,
                 on_insufficient: ErrorHandler=PRINT,
                 on_no_source: ErrorHandler=PRINT

                 ) -> None:
        self.well = well
        self.liquid = liquid
        self.when_done = when_done
        self.mix_result = mix_result
        self.on_insufficient = on_insufficient
        self.on_no_source = on_no_source
    
    

class PipettingArm(PipettorComponent, OpScheduler['PipettingArm']):
    OpFunc = Callable[[], None]
    
    serializer: Final[AsyncFunctionSerializer]
    lock: Final[Lock]
    waste_requests: Optional[list[TransferSpec[Well]]] = None
    product_requests: Optional[list[ExtractionPoint]] = None
    delivery_requests: Final[dict[Reagent, list[ExtractionPoint]]]
    fill_requests: Final[dict[Reagent, list[FillRequest]]]
    
                                  
    def __init__(self, pipettor: Pipettor, *, name: str="Pipetting Arm") -> None:
        super().__init__(pipettor)
        self.serializer = AsyncFunctionSerializer(thread_name=f"{name} Thread")
        # ,
        # after_task=lambda: self.to_ready_state())
        self.lock = Lock()
        self.delivery_requests = {}
        self.fill_requests = {}
        
    @abstractmethod
    def add_to_wells(self, reagent: Reagent, targets: Sequence[TransferSpec[Well]], *,  # @UnusedVariable
                     when_in_pos: DeliveryCallback[Well],                               # @UnusedVariable
                     when_done: DeliveryCallback[Well]                                  # @UnusedVariable
                     ) -> None: ...
        
    @abstractmethod
    def remove_waste(self, wells: Sequence[TransferSpec[Well]], *,  # @UnusedVariable
                     when_in_pos: DeliveryCallback[Well],           # @UnusedVariable
                     when_done: DeliveryCallback[Well]              # @UnusedVariable
                     ) -> None: ...

    @abstractmethod
    def deliver_drops(self, wells: Sequence[ExtractionPoint], *,        # @UnusedVariable
                     when_in_pos: DeliveryCallback[ExtractionPoint],    # @UnusedVariable
                     when_done: DeliveryCallback[ExtractionPoint],      # @UnusedVariable
                     drop_size: Optional[Volume] = None                 # @UnusedVariable
                     ) -> None: ...

    @abstractmethod
    def remove_product_drops(self, wells: Sequence[ExtractionPoint], *,         # @UnusedVariable
                             when_in_pos: DeliveryCallback[ExtractionPoint],    # @UnusedVariable
                             when_done: DeliveryCallback[ExtractionPoint],      # @UnusedVariable
                             drop_size: Optional[Volume] = None                 # @UnusedVariable
                     ) -> None: ...

    # @abstractmethod
    # def acquire_liquid(self, liquid: Liquid) -> Liquid: ...  # @UnusedVariable
    # @abstractmethod
    # def deposit_liquid(self) -> None: ...
    # @abstractmethod
    # def move_to(self, target: Target) -> None: ...  # @UnusedVariable
    # @abstractmethod 
    # def to_ready_state(self) -> None: ...
    
    def run_serialized(self, op_fn: OpFunc) -> None:
        self.serializer.enqueue(op_fn)
        
    class AddToWell(Operation['PipettingArm', Liquid]):
        liquid: Final[Liquid]
        target: Final[Well]
        mix_result: Final[Optional[Union[Reagent, str]]]
        on_insufficient: Final[ErrorHandler]
        on_no_source: Final[ErrorHandler]

        def __init__(self, liquid: Liquid, target: Well, *,
                     mix_result: Optional[Union[Reagent, str]]=None,
                     on_insufficient: ErrorHandler=PRINT,
                     on_no_source: ErrorHandler=PRINT

                     ) -> None:
            self.liquid = liquid
            self.target = target
            self.mix_result = mix_result
            self.on_insufficient = on_insufficient
            self.on_no_source = on_no_source

        def _schedule_for(self, arm: PipettingArm, *,
                          mode: RunMode=RunMode.GATED,
                          after: Optional[DelayType]=None,
                          post_result: bool=True,
                          ) -> Delayed[Liquid]:

            future = Delayed[Liquid]()
            target = self.target
            liquid = self.liquid
            reagent = liquid.reagent
            volume = liquid.volume
            request = FillRequest(liquid, target, 
                                  when_done=future,
                                  mix_result=self.mix_result,
                                  on_insufficient=self.on_insufficient,
                                  on_no_source=self.on_no_source)
            with arm.lock:
                requests = arm.fill_requests.get(reagent, None)
                if requests is not None:
                    requests.append(request)
                    return future
                requests = [request]
                def do_it() -> None:
                    ...
                ...
            # maybe_reservoir = arm.pipettor.reservoir_for(liquid.reagent)
            # if maybe_reservoir is None:
            #     self.on_no_source(f"No reservoir for {liquid.reagent}")
            #     return Delayed.complete(Liquid(liquid.reagent, Volume.ZERO()))
            # reservoir = maybe_reservoir
            def do_it() -> None:
                arm.move_to(reservoir)
                got = arm.acquire_liquid(liquid)
                self.on_insufficient.expect_true(got.volume >= liquid.volume,
                                                 lambda: f"""Asked for {liquid.volume} of {liquid.reagent},
                                                             only got {got.volume}""")
                arm.move_to(target)
                if isinstance(target, ExtractionPoint):
                    target.reserve_pad(expect_drop=self.expect_drop).wait()
                arm.deposit_liquid()
                if isinstance(target, ExtractionPoint):
                    drop = target.pad.drop
                    if drop is None:
                        drop = Drop(target.pad, got)
                        drop.pad.schedule(Pad.TurnOn)
                    else:
                        drop.liquid.mix_in(got, result=self.mix_result)
                    target.pad.reserved = False
                else:
                    target.transfer_in(liquid)
                if post_result:
                    future.post(got)

            arm.pipettor.delayed(lambda: arm.run_serialized(do_it), after=after)
            return future

    
    class Supply(Operation['PipettingArm', Liquid]):
        liquid: Final[Liquid]
        target: Final[Union[Well, ExtractionPoint]]
        mix_result: Final[Optional[Union[Reagent, str]]]
        expect_drop: Final[bool]
        on_insufficient: Final[ErrorHandler]
        on_no_source: Final[ErrorHandler]

        def __init__(self, liquid: Liquid, target: Union[Well, ExtractionPoint], *,
                     mix_result: Optional[Union[Reagent, str]]=None,
                     expect_drop: bool = False,
                     on_insufficient: ErrorHandler=PRINT,
                     on_no_source: ErrorHandler=PRINT

                     ) -> None:
            self.liquid = liquid
            self.target = target
            self.mix_result = mix_result
            self.expect_drop = expect_drop
            self.on_insufficient = on_insufficient
            self.on_no_source = on_no_source

        def _schedule_for(self, arm: PipettingArm, *,
                          mode: RunMode=RunMode.GATED,
                          after: Optional[DelayType]=None,
                          post_result: bool=True,
                          ) -> Delayed[Liquid]:

            future = Delayed[Liquid]()
            target = self.target
            liquid = self.liquid
            maybe_reservoir = arm.pipettor.reservoir_for(liquid.reagent)
            if maybe_reservoir is None:
                self.on_no_source(f"No reservoir for {liquid.reagent}")
                return Delayed.complete(Liquid(liquid.reagent, Volume.ZERO()))
            reservoir = maybe_reservoir
            def do_it() -> None:
                arm.move_to(reservoir)
                got = arm.acquire_liquid(liquid)
                self.on_insufficient.expect_true(got.volume >= liquid.volume,
                                                 lambda: f"""Asked for {liquid.volume} of {liquid.reagent},
                                                             only got {got.volume}""")
                arm.move_to(target)
                if isinstance(target, ExtractionPoint):
                    target.reserve_pad(expect_drop=self.expect_drop).wait()
                arm.deposit_liquid()
                if isinstance(target, ExtractionPoint):
                    drop = target.pad.drop
                    if drop is None:
                        drop = Drop(target.pad, got)
                        drop.pad.schedule(Pad.TurnOn)
                    else:
                        drop.liquid.mix_in(got, result=self.mix_result)
                    target.pad.reserved = False
                else:
                    target.transfer_in(liquid)
                if post_result:
                    future.post(got)

            arm.pipettor.delayed(lambda: arm.run_serialized(do_it), after=after)
            return future

    class Extract(Operation['PipettingArm', Liquid]):
        volume: Final[Optional[Volume]]
        target: Final[Union[Well, ExtractionPoint]]
        on_no_sink: Final[ErrorHandler]

        def __init__(self, volume: Optional[Volume], target: Union[Well, ExtractionPoint], *,
                     on_no_sink: ErrorHandler=PRINT
                     ) -> None:
            self.volume = volume
            self.target = target
            self.on_no_sink = on_no_sink

        def _schedule_for(self, arm: PipettingArm, *,
                          mode: RunMode=RunMode.GATED,
                          after: Optional[DelayType]=None,
                          post_result: bool=True,
                          ) -> Delayed[Liquid]:

            future = Delayed[Liquid]()
            target = self.target

            def do_it() -> None:
                arm.move_to(target)
                if isinstance(target, ExtractionPoint):
                    target.ensure_drop().wait()
                if isinstance(target, ExtractionPoint):
                    drop = not_None(target.pad.drop)
                    # if self.volume is None:
                    #     volume = drop.volume
                    # else:
                    #     volume = min(drop.volume, self.volume)
                    volume = drop.volume if self.volume is None else min(drop.volume, self.volume)
                    liquid = Liquid(drop.reagent, volume)
                else:
                    contents = target.contents
                    assert contents is not None, f"Trying to extract from empty {target}"
                    volume = target.volume if self.volume is None else min(target.volume, self.volume)
                    liquid = Liquid(contents.reagent, volume)
                reservoir = arm.pipettor.reservoir_for(liquid.reagent)
                if reservoir is None:
                    self.on_no_sink(f"No reservoir for {liquid.reagent}")
                else:
                    got = arm.acquire_liquid(liquid)
                    if isinstance(target, ExtractionPoint):
                        # I'm pretty sure that drop should still be defined here.
                        if drop.volume == got.volume:
                            drop.pad.schedule(Pad.TurnOff)
                            drop.status = DropStatus.OFF_BOARD
                            drop.pad.drop = None
                        else:
                            drop.liquid.volume = drop.volume-got.volume
                    else:
                        target.transfer_out(got.volume)
                    if post_result:
                        future.post(got)
                    arm.move_to(reservoir)
                    arm.deposit_liquid()

            arm.pipettor.delayed(lambda: arm.run_serialized(do_it), after=after)
            return future


class Pipettor(SystemComponent):

    well_blocks: Final[Sequence[WellBlock]]
    arms: Final[Sequence[PipettingArm]]
    
    def __init__(self, 
                 well_blocks: Sequence[WellBlock], 
                 arms: Sequence[PipettingArm]) -> None:
        self.well_blocks = well_blocks
        self.arms = arms

    def reservoir_for(self, reagent: Reagent) -> Optional[WellBlock.Reservoir]:
        for wb in self.well_blocks:
            r = wb.reservoir_for(reagent)
            if r is not None:
                return r
        return None

