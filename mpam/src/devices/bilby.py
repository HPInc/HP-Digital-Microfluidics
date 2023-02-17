from __future__ import annotations

from os import PathLike
import pyglider
from typing import Mapping, Final, Optional, Union, Sequence, Callable

from devices import joey, glider_client
from devices.glider_client import GliderClient
from mpam.pipettor import Pipettor
from mpam.types import OnOff, State, DummyState, Delayed, XYCoord
from mpam import device
from mpam.device import Pad, PowerMode, Magnet, Well
from quantities.dimensions import Time, Voltage
from quantities.SI import ms, volts
from quantities.temperature import TemperaturePoint, abs_C
import logging
from erk.errors import ErrorHandler, PRINT
from devices.joey import HeaterType
from erk.basic import assert_never


logger = logging.getLogger(__name__)


_shared_pad_cells: Mapping[tuple[str,int], str] = {
    ('left', 1): 'BC27', ('left', 2): 'B27', ('left', 3): 'AB27', 
    ('left', 4): 'C28', ('left', 5): 'B28', ('left', 6): 'A28',
    ('left', 7): 'B29', ('left', 9): 'B30', ('left', 9): 'B31',
    ('right', 1): 'BC05', ('right', 2): 'B05', ('right', 3): 'AB05', 
    ('right', 4): 'C04', ('right', 5): 'B04', ('right', 6): 'A04',
    ('right', 7): 'B03', ('right', 8): 'B02', ('right', 9): 'B01',
    }

_well_gate_cells: Mapping[XYCoord, str] = {
    XYCoord(1,19): 'T26', XYCoord(1,13): 'N26', XYCoord(1,7): 'H26', XYCoord(1,1): 'B26',
    XYCoord(19,19): 'T06', XYCoord(19,13): 'N06', XYCoord(19,7): 'H06', XYCoord(19,1): 'B06'
    }
    

class Heater(device.Heater):
    remote: Final[glider_client.Heater]
    def __init__(self, remote: glider_client.Heater, board: Board, *,
                 polling_interval: Time,
                 pads: Sequence[Pad],
                 wells: Sequence[Well]):
        super().__init__(board, polling_interval=polling_interval, locations=(*pads, *wells),
                         limit = 120*abs_C)
        self.remote = remote 
        def update_target(old: Optional[TemperaturePoint], new: Optional[TemperaturePoint]) -> None: # @UnusedVariable
            # We indirect through the board so that MakeItSo will be called.
            # This puts heater target changes synchronous with the clock.  I'm
            # not sure that's right, but it does allow the clock to be paused.
            # Note that this means that thermocycling needs to be not completely
            # asynchronous.
            self.board.communicate(lambda: self.remote.set_heating_target(new)) 
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
                 polling_interval: Time,
                 pads: Sequence[Pad],
                 wells: Sequence[Well]):
        super().__init__(board, polling_interval=polling_interval, locations=(*pads, *wells),
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
                 min_voltage: Voltage,
                 max_voltage: Voltage,
                 initial_voltage: Voltage, 
                 mode: PowerMode,
                 can_toggle: bool = True,
                 can_change_mode: bool = True,
                 on_high_voltage: ErrorHandler = PRINT,
                 on_low_voltage: ErrorHandler = PRINT,
                 on_illegal_toggle: ErrorHandler = PRINT, 
                 on_illegal_mode_change: ErrorHandler = PRINT, 
                 ) -> None:
        
        super().__init__(board,
                         min_voltage=min_voltage,
                         max_voltage=max_voltage,
                         initial_voltage=initial_voltage,
                         mode=mode,
                         can_toggle=can_toggle,
                         can_change_mode=can_change_mode,
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
                     state: OnOff,
                     live: bool = True) -> None:
            glider = board._device
            super().__init__(board, state=state, live=live)
            def state_changed(_old: OnOff, new: OnOff) -> None:
                which= "on" if new else "off"
                logger.info(f"Fan is {which}")
                glider.fan_state = new
            self.on_state_change(state_changed)
class Board(joey.Board):
    _device: Final[GliderClient]
    
    def _well_pad_state(self, group_name: str, num: int) -> State[OnOff]:
        cell = _shared_pad_cells.get((group_name, num))  
        # print(f"-- shared: {group_name} {num} -- {cell}")
        return self._device.electrode(cell) or DummyState(initial_state=OnOff.OFF)

    def _well_gate_state(self, exit_pad: Pad) -> State[OnOff]:
        cell = _well_gate_cells.get(exit_pad.location, None)
        # print(f"-- gate: {well} -- {cell}")
        return self._device.electrode(cell) or DummyState(initial_state=OnOff.OFF)
    
    def _pad_state(self, x: int, y: int) -> Optional[glider_client.Electrode]:
        cell = f"{ord('B')+y-1:c}{26-x:02d}"
        # print(f"({x}, {y}): {cell}")
        return self._device.electrode(cell)
    
    def _pads_matching(self, name: str, fn: Callable[[glider_client.Electrode], Sequence[str]]) -> list[Pad]:
        pads: list[Pad] = []
        for pad in self.pads.values():
            state = pad.state
            if state is not None:
                assert isinstance(state, glider_client.Electrode), f"{state} is not an Electrode"
                if name in fn(state):
                    pads.append(pad)
        return pads

    def _wells_matching(self, name: str, fn: Callable[[glider_client.Electrode], Sequence[str]]) -> list[Well]:
        wells: list[Well] = []
        for well in self.wells:
            for pad in well.shared_pads:
                state = pad.state
                if state is not None:
                    assert isinstance(state, glider_client.Electrode), f"{state} is not an Electrode"
                    heater_names = fn(state)
                    if name in heater_names:
                        wells.append(well)
                        break
        return wells

    def _magnets(self) -> Sequence[Magnet]:
        def make_magnet(gm: glider_client.Magnet) -> Magnet:
            pads = self._pads_matching(gm.name, glider_client.Electrode.magnet_names)
            m = Magnet(self, state=gm, pads=pads)
            return m
        return [make_magnet(gm) for gm in self._device.magnets.values()]
    
    def _fan(self, *, initial_state: OnOff) -> Fan:
        return Fan(self, state=initial_state)
    
    def _heaters(self, heater_type: HeaterType, *,
                 polling_interval: Time = 200*ms) -> Sequence[Heater]:
        if heater_type is HeaterType.TSRs:
            gt = pyglider.Heater.HeaterType.TSR
        elif heater_type is HeaterType.Paddles:
            gt = pyglider.Heater.HeaterType.Paddle
        else:
            assert_never(heater_type)
            
        # print(f"Looking for heaters of type {gt} ({id(gt)})")
            
        def make_heater(gh: glider_client.Heater) -> Heater:
            pads = self._pads_matching(gh.name, glider_client.Electrode.heater_names)
            wells = self._wells_matching(gh.name, glider_client.Electrode.heater_names)
            h =  Heater(gh, self, pads=pads, wells=wells, polling_interval=polling_interval)
            return h
        
        ghs = list(self._device.heaters.values())
        usable = [h for h in ghs if h.remote.GetType() == gt]
        heaters = [make_heater(h) for h in usable]
        # heaters = [make_heater(h) for h in self._device.heaters.values() if h.remote.GetType() is gt]
        return heaters
    
    def _chillers(self, *, polling_interval: Time = 200*ms) -> Sequence[Chiller]:
        gt = pyglider.Heater.HeaterType.Peltier
            
        def make_chiller(gh: glider_client.Heater) -> Chiller:
            pads = self._pads_matching(gh.name, glider_client.Electrode.heater_names)
            wells = self._wells_matching(gh.name, glider_client.Electrode.heater_names)
            c =  Chiller(gh, self, pads=pads, wells=wells, polling_interval=polling_interval)
            return c
        
        ghs = list(self._device.heaters.values())
        usable = [h for h in ghs if h.remote.GetType() == gt]
        chillers = [make_chiller(h) for h in usable]
        # heaters = [make_heater(h) for h in self._device.heaters.values() if h.remote.GetType() is gt]
        return chillers
    
    def _power_supply(self, *, 
                      min_voltage: Voltage, 
                      max_voltage: Voltage, 
                      initial_voltage: Voltage, 
                      initial_mode: PowerMode, 
                      can_toggle: bool,
                      can_change_mode: bool) -> PowerSupply:
        return PowerSupply(self, 
                           min_voltage=min_voltage,
                           max_voltage=max_voltage,
                           initial_voltage=initial_voltage,
                           mode=initial_mode,
                           can_toggle=can_toggle,
                           can_change_mode=can_change_mode)
    
    # def _fan(self, *, initial_state: OnOff) -> Fan:
    #     return joey.Board._fan(self)
    
    def __init__(self, *,
                 heater_type: HeaterType,
                 holes: Sequence[XYCoord] = (),
                 default_holes: bool = True,
                 dll_dir: Optional[Union[str, PathLike]] = None,
                 config_dir: Optional[Union[str, PathLike]] = None,
                 pipettor: Optional[Pipettor] = None,
                 off_on_delay: Time = Time.ZERO,
                 extraction_point_splash_radius: int = 0,
                 ps_min_voltage: Voltage = 60*volts,
                 ps_max_voltage: Voltage = 298*volts,
                 voltage: Optional[Voltage]) -> None:
        self._device = GliderClient(pyglider.BoardId.Wallaby, dll_dir=dll_dir, config_dir=config_dir)
        
        current_mode = PowerMode.DC
        current_voltage = self._device.voltage_level
        if current_voltage is None:
            logger.info("Couldn't read Bilby voltage level.  Assuming off.")
            current_voltage = Voltage.ZERO
        if current_voltage.is_close_to(0):
            logger.info(f"Near-zero voltage ({current_voltage}) read from device.  Assuming zero.")
            current_voltage = Voltage.ZERO
            
        fan_state = self._device.fan_state
        
        super().__init__(heater_type=heater_type,
                         holes=holes,
                         default_holes=default_holes, 
                         pipettor=pipettor, off_on_delay=off_on_delay,
                         ps_min_voltage=ps_min_voltage,
                         ps_max_voltage=ps_max_voltage,
                         ps_initial_voltage=current_voltage,
                         ps_initial_mode=current_mode,
                         ps_can_toggle=True,
                         fan_initial_state=fan_state,
                         extraction_point_splash_radius=extraction_point_splash_radius,
                         )
        on_electrodes = self._device.on_electrodes()
        if on_electrodes:
            for e in on_electrodes:
                e.current_state = OnOff.ON
            self.infer_drop_motion()
        
        # self._device.voltage_level = voltage
        self.power_supply.voltage = 0*volts if voltage is None else voltage
        
    def update_state(self) -> None:
        self._device.update_state()
        super().update_state()

