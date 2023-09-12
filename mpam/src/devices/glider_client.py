from __future__ import annotations

from pathlib import Path
import pyglider
from typing import Union, Optional, Final, Generic, TypeVar, Callable, List,\
    cast, Sequence, Mapping
from mpam.types import State, OnOff, MISSING, MissingOr
from os import PathLike
from quantities.temperature import TemperaturePoint, abs_C
from quantities.dimensions import Voltage, Time
from quantities.SI import volts, ms
import pathlib
from functools import cached_property
import logging
from pyglider import ErrorCode
from erk.basic import ValOrFn, ensure_val, map_unless_None

logger = logging.getLogger(__name__)



def _to_path(p: Optional[Union[str, PathLike]]) -> Optional[PathLike]:
    if isinstance(p, str):
        return Path(p)
    return p

T = TypeVar("T")

def check_error(val: Union[T, ErrorCode], *,
                desc: Optional[ValOrFn[str]] = None,
                default: MissingOr[T] = MISSING) -> T:
    if isinstance(val, ErrorCode):
        desc = "Call to Glider device" if desc is None else ensure_val(desc, str)
        msg =f"{desc} returned error code {val}"
        logger.warning(msg)
        if default is MISSING:
            raise ValueError(msg)
        val = default
    return val

def print_error(val: Optional[ErrorCode], *,
                desc: Optional[ValOrFn[str]] = None) -> None:
    check_error(val, desc=desc, default=None)


CT = TypeVar("CT")
ST = TypeVar("ST")

class BinState(Generic[CT, ST], State[OnOff]):
    kind: Final[str]
    name: Final[str]
    
    def __init__(self, *, kind: str, 
                 name: str, 
                 remote: CT,
                 on_val: ST,
                 off_val: ST,
                 realize: Callable[[CT, ST], Optional[pyglider.ErrorCode]],
                 initial_state: Union[OnOff, Callable[[CT], ST]] = OnOff.OFF) -> None:
        if not isinstance(initial_state, OnOff):
            initial_state = OnOff.from_bool(initial_state(remote) is on_val)
        super().__init__(initial_state=initial_state)
        self.kind = kind
        self.name = name
        self.remote = remote
        self.on_val = on_val
        self.off_val = off_val
        self.realize = realize
        
    def __repr__(self) -> str:
        return f"<{self.kind.title()} {self.name}>"
        
    def realize_state(self, new_state: OnOff)->None:
        s = self.on_val if new_state else self.off_val
        # print(f"Setting {self.name} to {new_state} ({s})")
        ec = self.realize(self.remote, s)
        if ec is not None:
            logger.error(f"Error {ec} returned trying to set electrode {self.name} to {new_state}.")

class Electrode(BinState[pyglider.Electrode, pyglider.Electrode.ElectrodeState]):
    def __init__(self, name: str, remote: pyglider.Electrode) -> None:
        super().__init__(kind = "electrode",
                         name = name,
                         remote = remote,
                         on_val = pyglider.Electrode.ElectrodeState.On,
                         off_val = pyglider.Electrode.ElectrodeState.Off,
                         realize = lambda r,s: r.SetTargetState(s),
                         initial_state = lambda r: r.GetCurrentState() )
        
    def heater_names(self) -> List[str]:
        # Bug: mypy 4/17/23 For some reason, mypy on the github server isn't
        # able to infer the type of `self.remote` and calls it `Any`, resulting
        # in it complaining on the return.  Amazingly, this persists even if you
        # assign it to a correctly-annotated variable or even if you do an
        # explicit cast.  GPT-4 was just as mystified as I was, but it was
        # taking too much time, so I'm just going to ignore that error in the
        # three places it currently occurs: here, in `Electrode.magnet_names()`
        # and in `Heater.read_temperature()`.
        return self.remote.GetHeaters() # type: ignore [no-any-return]
    
    def magnet_names(self) -> List[str]:
        # See comment in Electrode.heater_names()
        return self.remote.GetMagnets() # type: ignore [no-any-return]
    
class Magnet(BinState[pyglider.Magnet, pyglider.Magnet.MagnetState]):
    def __init__(self, name: str, remote: pyglider.Magnet) -> None:
        super().__init__(kind = "magnet",
                         name = name,
                         remote = remote,
                         on_val = pyglider.Magnet.MagnetState.On,
                         off_val = pyglider.Magnet.MagnetState.Off,
                         realize = lambda r,s: r.SetTargetState(s))

    
class Heater:
    name: Final[str]
    remote: Final[pyglider.Heater]
    from_remote: Final = dict[pyglider.Heater, 'Heater']()
    
    @cached_property
    def is_heater(self) -> bool:
        t = self.remote.GetType()
        return t is pyglider.Heater.HeaterType.Paddle or t is pyglider.Heater.HeaterType.TSR

    @cached_property
    def is_chiller(self) -> bool:
        t = self.remote.GetType()
        return t is pyglider.Heater.HeaterType.Peltier
    
    def __init__(self, name: str, remote: pyglider.Heater) -> None:
        self.name = name
        self.remote = remote
        self.from_remote[remote] = self
        # htype = self.remote.GetType()
        # print(f"{self}'s type is {htype} ({id(htype)})")
        
    def __repr__(self) -> str:
        return f"<Heater {self.name}>"
        
    def read_temperature(self) -> TemperaturePoint:
        # s = self.remote.GetStatus()
        # print(f"{self.name}: Current: {s.GetCurrentTemperature()}, Target: {s.GetTargetTemperature()}, ETA: {s.GetEtaInMilliseconds()}")
        temp = self.remote.GetCurrentTemperature()
        tp = temp*abs_C
        # print(f"  {tp}")
        
        # See comment in Electrode.heater_names()
        return tp   # type: ignore [no-any-return]
    
    def set_heating_target(self, target: Optional[TemperaturePoint]) -> None:
        temp = 0.0 if target is None else target.as_number(abs_C)
        # print(f"Setting target for {self.name} to {target}")
        self.remote.SetTargetTemperatureHeating(temp)
        
    def set_chilling_target(self, target: Optional[TemperaturePoint]) -> None:
        temp = 0.0 if target is None else target.as_number(abs_C)
        # print(f"Setting target for {self.name} to {target}")
        self.remote.SetTargetTemperatureChilling(temp)
        
        
class ThermalState:
    remote: Final[pyglider.ThermalState]
    target: Final[Mapping[Heater, Optional[TemperaturePoint]]]
    from_remote: Final = dict[pyglider.ThermalState, 'ThermalState']()
    
    @cached_property
    def name(self) -> str:
        return self.remote.GetName()
    
    @cached_property
    def number(self) -> int:
        return self.remote.GetNumber()
    
    @property
    def is_default(self) -> bool:
        return self.number == 0
    
    @property
    def status(self) -> pyglider.ThermalState.ThermalStateStatus:
        return self.remote.GetStatus()
    
    @property
    def expected_transition_time(self) -> Time:
        return self.remote.GetExpectedTransitionTimeInMS()*ms
    
    @property
    def is_transitioning(self) -> bool:
        return self.status is pyglider.ThermalState.ThermalStateStatus.Transitioning
    
    @property
    def is_ready(self) -> bool:
        return self.status is pyglider.ThermalState.ThermalStateStatus.Ready

    @property
    def is_available(self) -> bool:
        return self.status is pyglider.ThermalState.ThermalStateStatus.Available
    
    @property
    def is_unavailable(self) -> bool:
        return self.status is pyglider.ThermalState.ThermalStateStatus.Unavailable
    
    def __init__(self, remote: pyglider.ThermalState) -> None:
        self.remote = remote
        self.from_remote[remote] = self
        targets = dict[Heater, Optional[TemperaturePoint]]()
        self.target = targets
        
        for target in remote.GetTargets():
            heater = Heater.from_remote[target.heater]
            target_temp = target.target
            targets[heater] = None if target_temp == 0 else target_temp*abs_C 
        
    def __repr__(self) -> str:
        return f"<ThermalState {self.name}>"
    
    
    
    
        
class GliderClient:
    remote: Final[pyglider.Board]
    electrodes: Final[dict[str, Electrode]]
    heaters: Final[dict[str, Heater]]
    magnets: Final[dict[str, Magnet]]
    thermal_states: Final[Optional[Sequence[ThermalState]]]
    # remote_electrodes: Final[dict[str, pyglider.Electrode]]
    
    _voltage_level: Optional[Voltage] = None 
    
    @property
    def voltage_level(self) -> Optional[Voltage]:
        return self._voltage_level
    
    @voltage_level.setter
    def voltage_level(self, opt_volts: Optional[Voltage]) -> None:
        self._voltage_level = opt_volts
        if opt_volts is None:
            self.remote.DisableHighVoltage()
        else:
            self.remote.SetHighVoltage(opt_volts.as_number(volts))
            self.remote.EnableHighVoltage()
            
    @property
    def fan_state(self) -> OnOff:
        return OnOff.from_bool(self.remote.IsFanEnabled())
    
    @fan_state.setter
    def fan_state(self, val: OnOff) -> None:
        if val:
            self.remote.EnableFan()
        else:
            self.remote.DisableFan()
            
    @cached_property
    def _remote_sensors(self) -> List[pyglider.Sensor]:
        return self.remote.GetSensors()
            
    @cached_property
    def eselog(self) -> Optional[ESELog]:
        for s in self._remote_sensors:
            if isinstance(s, pyglider.ESElog):
                return ESELog(s)
        return None
    
    @property
    def current_thermal_state(self) -> Optional[ThermalState]:
        return map_unless_None(self.remote.GetCurrentThermalState(),
                               ThermalState.from_remote)
            
    def __init__(self, board_type: pyglider.BoardId, *,
                 revision: float,
                 use_thermal_states: bool = True,
                 dll_dir: Optional[Union[str, PathLike]] = None,
                 config_dir: Optional[Union[str, PathLike]] = None) -> None:
        if config_dir is None:
            config_dir = pathlib.Path.cwd()
        dll_dir = _to_path(dll_dir)
        config_dir = _to_path(config_dir)
        self.remote = pyglider.Board.Find(board_type,
                                          board_rev=revision,
                                          use_thermal_states=use_thermal_states, 
                                          dll_dir=dll_dir,
                                          config_dir=config_dir)
        # self.remote_electrodes = { e.GetName(): e for e in b.GetElectrodes()}
        # print(f"Remote: {self.remote_electrodes}")
        # self.electrodes = { k: Electrode(k, v) for k,v in self.remote_electrodes.items()}
        assert self.remote is not None, f"""
        Couldn't instantiate Glider client.  
        Board type is {board_type} revision {revision}
        DLL dir is {"<search>" if dll_dir is None else dll_dir}
        config_dir is {config_dir}
        """
        self.electrodes = {}
        self.heaters = {n: Heater(n, h) for h,n in ((ph, ph.GetName()) for ph in self.remote.GetHeaters()) }
        self.magnets = {n: Magnet(n, h) for h,n in ((pm, pm.GetName()) for pm in self.remote.GetMagnets()) }
        thermal_states = tuple(ThermalState(ts) for ts in self.remote.GetThermalStates())
        self.thermal_states = None if len(thermal_states) == 0 else thermal_states
        n = self.remote.GetHighVoltage()
        if isinstance(n, pyglider.ErrorCode):
            logger.error(f"Error {n} returned trying to read voltage level.")
            self._voltage_level = None
        else:
            logger.info(f"The voltage level is {n}")
            self._voltage_level = n*volts
        
        # print(f"Local: {self.electrodes}")

    def on_electrodes(self) -> list[Electrode]:
        return [e for e in self.electrodes.values() 
                if e.remote.GetCurrentState() == pyglider.Electrode.ElectrodeState.On]
        
    def update_state(self) -> None:
        ec = self.remote.MakeItSo()
        if ec is not None:
            logger.error(f"Error {ec} returned trying to update board.")
            
            
    def electrode(self, name: Optional[str]) -> Optional[Electrode]:
        # print(f"Asking for electrode {name}")
        if name is None:
            # print("  not there")
            return None
        # print(f"  is {self.electrodes[name]}")
        e = self.electrodes.get(name)
        if e is None:
            re = self.remote.ElectrodeNamed(name)
            if re is None:
                logger.error(f"No electrode named {name}!")
            else:
                e = Electrode(name, re)
                self.electrodes[name] = e
        return e
    
    def heater(self, name: Optional[str]) -> Optional[Heater]:
        if name is None:
            return None
        h = self.heaters.get(name)
        if h is None:
            re = self.remote.HeaterNamed(name)
            if re is None:
                logger.error(f"No heater named {name}!")
            else:
                h = Heater(name, re)
                self.heaters[name] = h
        return h
    
    def magnet(self, name: Optional[str]) -> Optional[Magnet]:
        if name is None:
            return None
        m = self.magnets.get(name)
        if m is None:
            re = self.remote.MagnetNamed(name)
            if re is None:
                logger.error(f"No magnet named {name}")
            else:
                m = Magnet(name, re)
                self.magnets[name] = m
        return m
    
    def set_thermal_state(self, thermal_state: ThermalState) -> None:
        self.remote.SetThermalState(thermal_state.remote)
    
    
class Sensor:
    _remote: Final[pyglider.Sensor]
    @property
    def remote(self) -> pyglider.Sensor:
        return self._remote
    
    @property
    def is_available(self) -> bool:
        val = check_error(self._remote.IsAvailable(),
                          desc = lambda: f"Call to {self._remote}.IsAvailable()",
                          default=True)
        return val

    
    def __init__(self, remote: pyglider.Sensor) -> None:
        self._remote = remote
        
    def aim(self, state: OnOff) -> None:
        logger.info(f"*** calling Aim({state is OnOff.ON})")
        self._remote.Aim(state is OnOff.ON)
        
    def request_samples(self, num_samples: Optional[int] = None) -> Time:
        i = check_error(self._remote.RequestSamples() if num_samples is None 
                        else self._remote.RequestSamples(num_samples),
                        desc = lambda: f"Call to {self._remote}.RequestSamples({num_samples})",
                        default=0)
        return i*ms
    
    def read_results(self, *, units: pyglider.Sensor.ResultType = pyglider.Sensor.ResultType.Millivolts,
                     asynchronous: bool = False) -> Sequence[pyglider.Sensor.SensorResult]:
        method = self._remote.ReadResultsAsync if asynchronous else self._remote.ReadResultsSync
        r = check_error(method(units),
                        desc = lambda: f"Call to {self._remote}.ReadResults{'Async' if asynchronous else 'Sync'}()")
        return r.results
        
        
class ESELog(Sensor):
    @property
    def remote(self) -> pyglider.ESElog:
        return cast(pyglider.ESElog, self._remote)
    
    def __init__(self, remote: pyglider.ESElog) -> None:
        super().__init__(remote)
    
    def read_results(self, *, units: pyglider.Sensor.ResultType = pyglider.Sensor.ResultType.Millivolts,
                     asynchronous: bool = False) -> Sequence[pyglider.ESElog.ESElogResult]:
        results = super().read_results(units=units, asynchronous=asynchronous)
        assert(all(isinstance(r, pyglider.ESElog.ESElogResult) for r in results))
        return cast(Sequence[pyglider.ESElog.ESElogResult], results)
