from __future__ import annotations

from typing import Final

from .device import (BoardComponent, BinaryComponent, ExternalComponent,
                     PipettingTarget, DropLoc, LocatedPad, TempControllable, Pad, WellPad,
                     WellGate, WellState, GateStatus, WellMotion, WellShape, WellVolumeSpec,
                     WellOpStep, WellOpSeqDict,
                     TransitionStep, StateDefs, DispenseGroup, Well, Magnet, TemperatureMode,
                     TemperatureControl, Heater, Chiller, ProductLocation, ExtractionPoint,
                     SystemComponent, PowerMode, PowerSupply, FixedPowerSupply, Fan, ChangeJournal,
                     TempOrTP, AmbientThreshold, Laser, Sensor, ComponentFactory, Board,
                     UserOperation, Clock, Batch, System)
from .drop import Blob, DropStatus, MotionOp, Drop, DropComputeOp
from .engine import TimerFunc, ClockCallback, Worker, DevCommRequest
from .exceptions import MPAMError, PadBrokenError, WellEmptyError, WellFullError, NoSuchPad, UnsafeMotion, NotAtWell
from .exerciser import (Task, Exerciser, BadPlatformDescError, PlatformChoiceTask, ComponentConfig, PipettorConfig, 
                        PlatformChoiceExerciser, BoardKwdArgs)
from .interpreter import DMLInterpreter
from .monitor import BoardMonitor
from .paths import Schedulable, Path
from .pipettor import XferTarget, FillTarget, EmptyTarget, Transfer, PipettingSource, Pipettor
from .processes import (MultiDropProcessRun, MultiDropProcessType, StartProcess, JoinProcess,
                        PairwiseMix, MixSequence, Transform, DropCombinationRun, DropCombinationProcessType,
                        PlacedMixSequence)
from .thermocycle import (ChannelEndpoint as ThermocycleChannelEndpoint, 
                          Channel as ThermocycleChannel, ShuttleDir, Thermocycler, ThermocycleProcessType,
                          ThermocyclePhase)
from .types import (OnOff, deg_C_per_sec, UnknownConcentration, unknown_concentration,
                    Concentration, Chemical, ChemicalComposition, ProcessStep, MixtureSpec, Reagent,
                    waste_reagent, unknown_reagent, MixResult, Mixture, ProcessedReagent, Liquid,
                    XferDir, State, DummyState)


class Config:
    from . import device as _device

    local_ip_addr: Final = _device.Config.local_ip_addr
    subnet: Final = _device.Config.subnet
    subnet_mask: Final = _device.Config.subnet_mask
    off_on_delay: Final = _device.Config.off_on_delay
    extraction_point_splash_radius: Final = _device.Config.extraction_point_splash_radius
    polling_interval: Final = _device.Config.polling_interval
    ps_min_voltage: Final = _device.Config.ps_min_voltage
    ps_max_voltage: Final = _device.Config.ps_max_voltage
    ps_initial_voltage: Final = _device.Config.ps_initial_voltage
    ps_initial_mode: Final = _device.Config.ps_initial_mode
    ps_can_toggle: Final = _device.Config.ps_can_toggle
    ps_can_change_mode: Final = _device.Config.ps_can_change_mode
    fan_initial_state: Final = _device.Config.fan_initial_state
    fan_can_toggle: Final = _device.Config.fan_can_toggle
    component_factories: Final = _device.Config.component_factories
    owns_externals: Final = _device.Config.owns_externals
    
    from . import exerciser as _exerciser
    
    clock_interval: Final = _exerciser.Config.clock_interval
    start_clock: Final = _exerciser.Config.start_clock
    units: Final = _exerciser.Config.units
    log_config: Final = _exerciser.Config.log_config
    log_levels: Final = _exerciser.Config.log_levels
    trace_blobs: Final = _exerciser.Config.trace_blobs
    
    from . import interpreter as _interpreter
    
    dml_dirs: Final = _interpreter.Config.dml_dirs
    dml_file_names: Final = _interpreter.Config.dml_file_names
    dml_encoding: Final = _interpreter.Config.dml_encoding
    
    from . import monitor as _monitor
    
    highlight_reservations: Final = _monitor.Config.highlight_reservations
    trace_clicks: Final = _monitor.Config.trace_clicks
    initial_delay: Final = _monitor.Config.initial_delay
    hold_display: Final = _monitor.Config.hold_display
    min_time: Final = _monitor.Config.min_time
    max_time: Final = _monitor.Config.max_time
    update_interval: Final = _monitor.Config.update_interval
    use_display: Final = _monitor.Config.use_display
    
    from . import pipettor as _pipettor
    
    pipettor: Final = _pipettor.Config.pipettor
    value_formatter: Final = _pipettor.Config.value_formatter
    
