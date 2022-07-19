from __future__ import annotations

from os import PathLike
import pyglider
from typing import Mapping, Final, Optional, Union, Sequence, Callable

from devices import joey, glider_client
from devices.glider_client import GliderClient
from mpam.pipettor import Pipettor
from mpam.types import OnOff, State, DummyState, Delayed
from mpam import device
from mpam.device import Pad, PowerMode, Magnet
from quantities.dimensions import Time, Voltage
from quantities.SI import ms, volts
from quantities.temperature import TemperaturePoint, abs_C
import logging
from erk.errors import ErrorHandler, PRINT
from argparse import Namespace, _ArgumentGroup, ArgumentParser
from mpam.exerciser import PlatformChoiceExerciser, voltage_arg, Exerciser
from devices.joey import HeaterType, heater_type_arg_names


logger = logging.getLogger(__name__)


_shared_pad_cells: Mapping[tuple[str,int], str] = {
    ('left', 0): 'BC27', ('left', 1): 'B27', ('left', 2): 'AB27', 
    ('left', 3): 'C28', ('left', 4): 'B28', ('left', 5): 'A28',
    ('left', 6): 'B29', ('left', 7): 'B30', ('left', 8): 'B31',
    ('right', 0): 'BC05', ('right', 1): 'B05', ('right', 2): 'AB05', 
    ('right', 3): 'C04', ('right', 4): 'B04', ('right', 5): 'A04',
    ('right', 6): 'B03', ('right', 7): 'B02', ('right', 8): 'B01',
    }

_well_gate_cells: Mapping[int, str] = {
    0: 'T26', 1: 'N26', 2: 'H26', 3: 'B26',
    4: 'T06', 5: 'N06', 6: 'H06', 7: 'B06'
    }

    

class Heater(device.Heater):
    remote: Final[glider_client.Heater]
    def __init__(self, num: int, remote: glider_client.Heater, board: Board, *,
                 polling_interval: Time,
                 pads: Sequence[Pad]):
        super().__init__(num, board, polling_interval=polling_interval, locations=pads,
                         max_heat = 120*abs_C, min_chill = None)
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
        def voltage_changed(_old, new: Voltage) -> None:
            if new > 0:
                logger.info(f"Voltage level is {new}")
            glider.voltage_level = None if new == 0 else new
        self.on_voltage_change(voltage_changed)
        
        def state_changed(_old, new: OnOff) -> None:
            which = "on" if new else "off"
            logger.info(f"High voltage is {which}")
        self.on_state_change(state_changed)
        
class Fan(device.Fan):
        def __init__(self, board: Board, *,
                     state: OnOff,
                     live: bool = True) -> None:
            glider = board._device
            super().__init__(board, state=state, live=live)
            def state_changed(_old, new: OnOff) -> None:
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

    def _well_gate_state(self, well: int) -> State[OnOff]:
        cell = _well_gate_cells.get(well, None)
        # print(f"-- gate: {well} -- {cell}")
        return self._device.electrode(cell) or DummyState(initial_state=OnOff.OFF)
    
    def _pad_state(self, x: int, y: int) -> Optional[glider_client.Electrode]:
        cell = f"{ord('B')+y:c}{25-x:02d}"
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

    def _magnets(self, *, first_num: int = 0) -> Sequence[Magnet]:
        num = first_num
        def make_magnet(gm: glider_client.Magnet) -> Magnet:
            nonlocal num
            pads = self._pads_matching(gm.name, glider_client.Electrode.magnet_names)
            m = Magnet(num, self, state=gm, pads=pads)
            num += 1
            return m
        return [make_magnet(gm) for gm in self._device.magnets.values()]
    
    def _fan(self, *, initial_state: OnOff) -> Fan:
        return Fan(self, state=initial_state)
    
    def _heaters(self, heater_type: HeaterType, *,
                 first_num: int = 0,
                 polling_interval: Time = 200*ms) -> Sequence[Heater]:
        if heater_type is HeaterType.TSRs:
            gt = pyglider.Heater.HeaterType.TSR
        else:
            assert heater_type is HeaterType.Paddles, f"Unknown HeaterType {heater_type}"
            gt = pyglider.Heater.HeaterType.Paddle
            
        # print(f"Looking for heaters of type {gt} ({id(gt)})")
            
        num = first_num
        def make_heater(gh: glider_client.Heater) -> Heater:
            nonlocal num
            pads = self._pads_matching(gh.name, glider_client.Electrode.heater_names)
            h =  Heater(num, gh, self, pads=pads, polling_interval=polling_interval)
            num += 1
            return h
        
        ghs = list(self._device.heaters.values())
        usable = [h for h in ghs if h.remote.GetType() == gt]
        heaters = [make_heater(h) for h in usable]
        # heaters = [make_heater(h) for h in self._device.heaters.values() if h.remote.GetType() is gt]
        return heaters
    
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

class PlatformTask(joey.PlatformTask):
    def __init__(self, name: str = "Bilby",
                 description: Optional[str] = None,
                 *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
    
    
    def make_board(self, args: Namespace, *, 
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                   pipettor: Pipettor) -> Board: # @UnusedVariable
        voltage: Optional[Voltage] = args.voltage
        assert voltage is not None
        if voltage == 0:
            voltage = None
        return Board(heater_type = heater_type_arg_names[args.heaters],
                     pipettor=pipettor,
                     dll_dir=args.dll_dir, config_dir=args.config_dir,
                     off_on_delay=args.off_on_delay,
                     voltage=voltage,
                     extraction_point_splash_radius=args.extraction_point_splash_radius)
        
    def add_args_to(self, 
                    group: _ArgumentGroup, 
                    parser: ArgumentParser,
                    *,
                    exerciser: Exerciser) -> None:
        super().add_args_to(group, parser, exerciser=exerciser)
        group.add_argument("--dll-dir",
                           help='''
                           The directory that Wallaby.dll is found in.  Defaults to searching.
                           ''')
        group.add_argument("--config-dir",
                           help='''
                           The directory that WallabyElectrodes.csv and WallabyHeaters.csv
                           are found in.  Defaults to the current directory.
                           ''')
        default_voltage = 60*volts
        group.add_argument("--voltage", type=voltage_arg, metavar="VOLTAGE", default=default_voltage,
                           help=f'''
                           The voltage to set.  A value of 0V disables
                           the high voltage.  Any other value enables it.
                           The defaults is {default_voltage}.
                           ''')
        

