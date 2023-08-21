from __future__ import annotations

import pyglider
from typing import Final, Optional, Sequence, Callable, Union, Mapping

from devices import joey, glider_client, bilby_task, eselog
from devices.glider_client import GliderClient
from mpam.types import OnOff, State, DummyState, Delayed, \
    AsyncFunctionSerializer, Postable, Dir, MISSING
from mpam import device
from mpam.device import Pad, Magnet, Well
from quantities.dimensions import Voltage, Frequency, Time, Temperature
from quantities.temperature import TemperaturePoint, abs_C
import logging
from erk.errors import ErrorHandler, PRINT
from devices.joey import HeaterType, JoeyLayout
from erk.basic import assert_never, not_None, map_unless_None
from devices.eselog import ESELog, ESELogChannel, EmulatedESELog
from quantities.SI import mV, deg_C
from quantities.timestamp import Timestamp, time_now, time_in, sleep_until
from functools import cached_property
from erk.stringutils import conj_str


logger = logging.getLogger(__name__)

class Config:
    dll_dir = bilby_task.Config.dll_dir
    config_dir = bilby_task.Config.config_dir
    voltage = bilby_task.Config.voltage
    thermal_state_tolerance = bilby_task.Config.thermal_state_tolerance
    remember_thermal_state_decisions = bilby_task.Config.remember_thermal_state_decisions
    
    setup_defaults = bilby_task.Config.setup_defaults

    

class Heater(device.Heater):
    remote: Final[glider_client.Heater]
    from_remote: Final = dict[glider_client.Heater, 'Heater']()

    
    def __init__(self, remote: glider_client.Heater, board: Board, *,
                 pads: Sequence[Pad],
                 wells: Sequence[Well]):
        super().__init__(board, locations=(*pads, *wells),
                         limit = 120*abs_C)
        self.remote = remote
        self.from_remote[remote] = self 
        def update_target(old: Optional[TemperaturePoint], new: Optional[TemperaturePoint]) -> None: # @UnusedVariable
            # We indirect through the board so that MakeItSo will be called.
            # This puts heater target changes synchronous with the clock.  I'm
            # not sure that's right, but it does allow the clock to be paused.
            # Note that this means that thermocycling needs to be not completely
            # asynchronous.
            current_ts = board.current_thermal_state
            if current_ts is None:
                board.communicate(lambda: self.remote.set_heating_target(new))
            elif self in current_ts.target and current_ts.target[self] == new:
                # We're already there.  Nothing to do.
                pass
            else:
                # We let the board take care of it
                board.set_thermal_state(self, new)
            
        update_target_key = f"Update Target for {self}"
        self.on_target_change(update_target, key = update_target_key)
        
    def __repr__(self) -> str:
        return f"<Heater {self.number} using {self.remote}>"

    
    def poll(self) -> Delayed[Optional[TemperaturePoint]]:
        temp = self.remote.read_temperature()
        return Delayed.complete(temp)
    
class Chiller(device.Chiller):
    remote: Final[glider_client.Heater]
    def __init__(self, remote: glider_client.Heater, board: Board, *,
                 pads: Sequence[Pad],
                 wells: Sequence[Well]):
        super().__init__(board, locations=(*pads, *wells),
                         limit = 5*abs_C)
        self.remote = remote 
        def update_target(old: Optional[TemperaturePoint], new: Optional[TemperaturePoint]) -> None: # @UnusedVariable
            # We indirect through the board so that MakeItSo will be called.
            # This puts heater target changes synchronous with the clock.  I'm
            # not sure that's right, but it does allow the clock to be paused.
            # Note that this means that thermocycling needs to be not completely
            # asynchronous.
            self.board.communicate(lambda: self.remote.set_chilling_target(new)) 
        update_target_key = f"Update Target for {self}"
        self.on_target_change(update_target, key = update_target_key)
        
    def __repr__(self) -> str:
        return f"<Chiller {self.number} using {self.remote}>"

    
    def poll(self) -> Delayed[Optional[TemperaturePoint]]:
        temp = self.remote.read_temperature()
        return Delayed.complete(temp)
    
class PowerSupply(device.PowerSupply):
    
    def __init__(self, board: Board, *,
                 on_high_voltage: ErrorHandler = PRINT,
                 on_low_voltage: ErrorHandler = PRINT,
                 on_illegal_toggle: ErrorHandler = PRINT, 
                 on_illegal_mode_change: ErrorHandler = PRINT, 
                 ) -> None:
        
        super().__init__(board,
                         on_high_voltage=on_high_voltage,
                         on_low_voltage=on_low_voltage,
                         on_illegal_toggle=on_illegal_toggle,
                         on_illegal_mode_change=on_illegal_mode_change
                         )
        glider = board._device
        def voltage_changed(_old: Voltage, new: Voltage) -> None:
            if new > 0:
                logger.info(f"Voltage level is {new}")
            glider.voltage_level = None if new == 0 else new
        self.on_voltage_change(voltage_changed)
        
        def state_changed(_old: OnOff, new: OnOff) -> None:
            which = "on" if new else "off"
            logger.info(f"High voltage is {which}")
        self.on_state_change(state_changed)
        
class Fan(device.Fan):
        def __init__(self, board: Board, *,
                     live: bool = True) -> None:
            glider = board._device
            super().__init__(board, live=live)
            def state_changed(_old: OnOff, new: OnOff) -> None:
                which= "on" if new else "off"
                logger.info(f"Fan is {which}")
                glider.fan_state = new
            self.on_state_change(state_changed)

class ESELogProxy(ESELog.Proxy):
    remote: Final[glider_client.ESELog]
    serializer: Final[AsyncFunctionSerializer]
    
    
    def __init__(self, eselog: ESELog, remote: glider_client.ESELog) -> None:
        super().__init__(eselog)
        self.remote = remote
        laser = not_None(eselog.aiming_laser, desc=lambda: f"{eselog} has no laser")
        def handle_laser(_old: OnOff, new: OnOff) -> None:
            remote.aim(new)
        laser.on_state_change(handle_laser)
        self.serializer = AsyncFunctionSerializer(thread_name="{self.eselog.name} Thread")
        
    @property
    def available(self)->bool:
        return self.remote.is_available
        
    def read(self, *, n_samples:Optional[int]=None, 
             speed:Optional[Union[Time, Frequency]]=None)-> Delayed[Sequence[ESELog.Sample]]:
        
        future = Postable[Sequence[ESELog.Sample]]()
        
        def to_result(r: pyglider.ESElog.ESElogResult) -> ESELog.Sample:
            values = {
                (ESELogChannel.E1D1, OnOff.ON): r.e1d1_valueOn*mV,
                (ESELogChannel.E1D1, OnOff.OFF): r.e1d1_valueOff*mV,
                (ESELogChannel.E1D2, OnOff.ON): r.e1d2_valueOn*mV,
                (ESELogChannel.E1D2, OnOff.OFF): r.e1d2_valueOff*mV,
                (ESELogChannel.E2D2, OnOff.ON): r.e2d2_valueOn*mV,
                (ESELogChannel.E2D2, OnOff.OFF): r.e2d2_valueOff*mV,
                }
            return ESELog.Sample(ticket = r.ticket,
                                 time = Timestamp.from_time_t(r.time),
                                 temperature = r.temperature*abs_C,
                                 values = values)
        
        def take_readings() -> None:
            nonlocal n_samples
            remote = self.remote
            if speed is None:
                remote.request_samples(n_samples)
                vals = remote.read_results()
            else:
                n = self.eseLog.n_samples if n_samples is None else n_samples
                interval = Time.rate_from(speed)
                vals = list[pyglider.ESElog.ESElogResult]()
                next_reading = time_now()
                for _i in range(n):
                    sleep_until(next_reading)
                    next_reading = time_in(interval)
                    remote.request_samples(1)
                    vals.extend(remote.read_results())
            future.post([to_result(r) for r in vals])
                    
        
        self.serializer.enqueue(take_readings)
        return future
        
    def reset(self) -> None:
        ...

class ThermalState:
    board: Final[Board]
    remote: Final[glider_client.ThermalState]
    target: Final[Mapping[Heater, Optional[TemperaturePoint]]]
    from_remote: Final[dict[glider_client.ThermalState, ThermalState]] = {}
    
    @cached_property
    def name(self) -> str:
        return self.remote.name
    
    @cached_property
    def number(self) -> int:
        return self.remote.number
    
    def __init__(self, remote: glider_client.ThermalState, *,
                 board: Board) -> None:
        self.board = board
        self.remote = remote
        self.target = {Heater.from_remote[h]: t for h,t in remote.target.items()}
        self.from_remote[remote] = self
        
    def __repr__(self) -> str:
        return f"<ThermalState {self.number} using {self.remote}>"
        
class Board(joey.Board):
    _device: Final[GliderClient]
    thermal_states: Final[Optional[Sequence[ThermalState]]]
    current_thermal_state: Optional[ThermalState] = None
    
    def _well_pad_state(self, group_name: str, num: int) -> State[OnOff]:
        cell = self.shared_pad_cell(group_name, num)  
        # print(f"-- shared: {group_name} {num} -- {cell}")
        # state = self._device.electrode(cell) or DummyState(initial_state=OnOff.OFF)
        state = self._device.electrode(cell)
        assert state is not None
        return state

    def _well_gate_state(self, exit_pad: Pad) -> State[OnOff]:
        cell = self.well_gate_cell(exit_pad)
        # print(f"-- gate: {well} -- {cell}")
        return self._device.electrode(cell) or DummyState(initial_state=OnOff.OFF)
    
    def _pad_state(self, x: int, y: int) -> Optional[State[OnOff]]:
        cell = self.pad_cell(x, y)
        # print(f"({x}, {y}): {cell}")
        return self._device.electrode(cell)
    
    def _pads_matching(self, name: str, fn: Callable[[glider_client.Electrode], Sequence[str]]) -> list[Pad]:
        pads: list[Pad] = []
        for pad in self.pads.values():
            state = self._pad_state(pad.column, pad.row)
            if state is not None:
                assert isinstance(state, glider_client.Electrode), f"{state} is not an Electrode"
                if name in fn(state):
                    pads.append(pad)
        return pads

    def _wells_matching(self, name: str, fn: Callable[[glider_client.Electrode], Sequence[str]]) -> list[Well]:
        wells: list[Well] = []
        for well in self.wells:
            side = "left" if well.exit_dir is Dir.EAST else "right"
            for i in range(len(well.shared_pads)):
                state = self._well_pad_state(side, i+1)
                assert isinstance(state, glider_client.Electrode), f"{state} is not an Electrode"
                names = fn(state)
                if name in names:
                    wells.append(well)
                    break
        return wells

    def _magnets(self) -> Sequence[Magnet]:
        def make_magnet(gm: glider_client.Magnet) -> Magnet:
            pads = self._pads_matching(gm.name, glider_client.Electrode.magnet_names)
            m = Magnet(self, state=gm, pads=pads)
            return m
        return [make_magnet(gm) for gm in self._device.magnets.values()]
    
    def _fan(self) -> Fan:
        return Fan(self)
    
    def _heaters(self) -> Sequence[Heater]:
        heater_type = joey.Config.heater_type()
        if self._layout is JoeyLayout.V1_5:
            # For the moment, at least, v1.5 only has RTDs in bilby
            gt = pyglider.Heater.HeaterType.RTD
        elif heater_type is HeaterType.TSRs:
            gt = pyglider.Heater.HeaterType.TSR
        elif heater_type is HeaterType.Paddles:
            gt = pyglider.Heater.HeaterType.Paddle
        elif heater_type is HeaterType.RTDs:
            gt = pyglider.Heater.HeaterType.RTD
        else:
            assert_never(heater_type)
            
        # print(f"Looking for heaters of type {gt} ({id(gt)})")
            
        def make_heater(gh: glider_client.Heater) -> Heater:
            pads = self._pads_matching(gh.name, glider_client.Electrode.heater_names)
            wells = self._wells_matching(gh.name, glider_client.Electrode.heater_names)
            h =  Heater(gh, self, pads=pads, wells=wells)
            return h
        
        ghs = list(self._device.heaters.values())
        usable = [h for h in ghs if h.remote.GetType() == gt]
        heaters = [make_heater(h) for h in usable]
        # heaters = [make_heater(h) for h in self._device.heaters.values() if h.remote.GetType() is gt]
        return heaters
    
    def _chillers(self) -> Sequence[Chiller]:
        gt = pyglider.Heater.HeaterType.Peltier
             
        def make_chiller(gh: glider_client.Heater) -> Chiller:
            pads = self._pads_matching(gh.name, glider_client.Electrode.heater_names)
            wells = self._wells_matching(gh.name, glider_client.Electrode.heater_names)
            c =  Chiller(gh, self, pads=pads, wells=wells)
            return c
        
        ghs = list(self._device.heaters.values())
        usable = [h for h in ghs if h.remote.GetType() == gt]
        chillers = [make_chiller(h) for h in usable]
        # heaters = [make_heater(h) for h in self._device.heaters.values() if h.remote.GetType() is gt]
        return chillers
    
    def _power_supply(self) -> PowerSupply:
        return PowerSupply(self)
    
    # def _fan(self, *, initial_state: OnOff) -> Fan:
    #     return joey.Board._fan(self)
    
    def __init__(self) -> None:
        
        dll_dir = Config.dll_dir()
        config_dir = Config.config_dir()
        
        revision: float
        layout = joey.Config.layout()
        if layout is JoeyLayout.V1:
            revision = 1.0
        elif layout is JoeyLayout.V1_5:
            revision = 1.5
        else:
            assert_never(layout)
            
        self._device = GliderClient(pyglider.BoardId.Wallaby, revision=revision, 
                                    dll_dir=dll_dir, config_dir=config_dir)
        
        current_voltage = self._device.voltage_level
        if current_voltage is None:
            logger.info("Couldn't read Bilby voltage level.  Assuming off.")
            current_voltage = Voltage.ZERO
        if current_voltage.is_close_to(0):
            logger.info(f"Near-zero voltage ({current_voltage}) read from device.  Assuming zero.")
            current_voltage = Voltage.ZERO
        
        def eselog_proxy_factory(eselog: ESELog) -> ESELog.Proxy:
            remote = self._device.eselog
            if remote is None:
                logger.warning(f"Using emulated ESELog, because Bilby device doesn't have one.")
                return EmulatedESELog(eselog)
            return ESELogProxy(eselog, remote)

        with eselog.Config.proxy_factory >> eselog_proxy_factory:
            super().__init__()
        on_electrodes = self._device.on_electrodes()
        if on_electrodes:
            for e in on_electrodes:
                e.current_state = OnOff.ON
            self.infer_drop_motion()
            
        self.power_supply.voltage = Config.voltage()
        thermal_states: Optional[Sequence[ThermalState]] = None
        tstates = self._device.thermal_states
        if tstates is not None:
            thermal_states = [ThermalState(ts, board=self) for ts in tstates]
            self.current_thermal_state = map_unless_None(self._device.current_thermal_state,
                                                         ThermalState.from_remote)
        self.thermal_states = thermal_states
        
    def update_state(self) -> None:
        self._device.update_state()
        super().update_state()
        
    @cached_property
    def _ts_tolerance(self) -> Temperature:
        return Config.thermal_state_tolerance()
    
    @cached_property
    def _remember_ts_choice(self) -> bool:
        return Config.remember_thermal_state_decisions()
    
    @cached_property
    def _ts_options(self) -> dict[tuple[Heater, Optional[TemperaturePoint]],
                                  Union[ThermalState, Sequence[ThermalState], None]]:
        return {}
    
    def thermal_state_for(self, heater: Heater, 
                          target: Optional[TemperaturePoint]) -> Delayed[Optional[ThermalState]]:
        options = self._ts_options
        key = (heater, target)
        states = options.get(key, None)
        if isinstance(states, ThermalState):
            return Delayed.complete(states)
        if states is None:
            my_tstates = not_None(self.thermal_states, desc=lambda: f"{self}.thermal_states")
            best: list[ThermalState]
            
            if target is None:
                best = [ts for ts in my_tstates if ts.target.get(heater, MISSING) is None]
            else:
                best_delta = 1000*deg_C
                best = []
                for ts in my_tstates:
                    t = ts.target.get(heater, None)
                    if t is not None:
                        if t >= self.ambient_temperature:
                            delta = abs(t-target)
                            if delta < best_delta:
                                best = [ts]
                                best_delta = delta
                            elif delta == best_delta:
                                if len(ts.target) == 1:
                                    # If this state only affects this one target 
                                    # and it's the closest, there's no choice.
                                    best = [ts]
                                else:
                                    best.append(ts) 
            options[key] = best
            states = best
        if len(states) == 0:
            return Delayed.complete(None)
        if len(states) == 1:
            only_ts = states[0]
            delta = (0*deg_C if target is None 
                     else abs(not_None(only_ts.target[heater])-not_None(target)))
            if delta <= self._ts_tolerance:
                options[key] = only_ts
                return Delayed.complete(only_ts)
            msg = f'''
            Heater #{heater.number} was requested to set its target to {target}.  The closest
            thermal state to this is #{only_ts.number}, whose target for heater #{heater.number}
            is {only_ts.target[heater]}, which is not within {self._ts_tolerance}.  Do you want
            to apply it anyway?
            
            (You can change the tolerance by specifying --thermal-state-tolerance).
            '''
            # msg = textwrap.fill(msg, 40)
            def on_answer(s: str) -> Optional[ThermalState]:
                # logger.info(f"Got back '{s}'")
                if s == "Yes":
                    if self._remember_ts_choice:
                        options[key] = only_ts
                    return only_ts
                else:
                    return None
            return (self
                    .system.prompt_and_wait(msg,
                                            title="Thermal state confirmation", 
                                            options=("Yes", "No"))
                    .transformed(on_answer))
        
        def to_state_desc(ts: ThermalState) -> str:
            def htdesc(h: Heater, t: Optional[TemperaturePoint]) -> str:
                if t is None: 
                    return f"turns heater #{h.number} off"
                else:
                    return f"sets heater #{h.number} to {t}"
            return f'''
            thermal state #{ts} (which also
            {conj_str([htdesc(h,t) for h,t in ts.target.items() if h is not heater])})
            '''
        states = sorted(states, key = lambda ts: ts.number)

        msg = f'''
            Heater #{heater.number} was requested to set its target to {target}.  
            There are {len(states)} that are closest to that target:
            {conj_str([to_state_desc(ts) for ts in states])}.  Which, if any,
            would you like to use.
        '''
        # msg = textwrap.fill(msg, 40)
        from_string = { f"#{ts.number}": ts for ts in states }
        def on_choice(s: str) -> Optional[ThermalState]:
            ts = from_string.get(s, None)
            if ts is not None and self._remember_ts_choice:
                options[key] = ts
            return ts
        buttons = ["None", *("f{ts.number} for ts in states")]
        return (self.system
                .prompt_and_wait(msg,
                                 title = "Thermal state selection", 
                                 options = buttons)
                .transformed(on_choice)
                )
            
    def set_thermal_state(self, heater: Heater, target: Optional[TemperaturePoint]) -> None:
        def with_thermal_state(thermal_state: Optional[ThermalState]) -> None:
            # At this point, we either have the one to set or we have None, indicating
            # that we will never get there.  I'm not sure what to do in that case,
            # but I'm leaning toward not doing anything. 
            if thermal_state is None:
                return
            # There are three things to do here.  (1) Note the ThermalState
            # we're going to, (2) tell the device to go there, and (3) reset the
            # targets for all of the heaters in the state.  Since we're setting
            # to the exact temperature of our current state's target for each
            # heater, we won't get any further calls.
            self.current_thermal_state = thermal_state
            ts_remote = thermal_state.remote
            self.communicate(lambda: self._device.set_thermal_state(ts_remote))
            for h,t in thermal_state.target.items():
                h.target = t
        (self.thermal_state_for(heater, target)
         .then_call(with_thermal_state))
        ...
