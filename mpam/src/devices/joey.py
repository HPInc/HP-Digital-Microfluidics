from __future__ import annotations

from enum import Enum, auto
import random
from typing import Optional, Sequence, Final, Union

from mpam.device import WellOpSeqDict, WellState, PadBounds, \
    HeatingMode, WellShape, System, WellPad, Pad, Magnet, DispenseGroup, \
    transitions_from, WellGate, Heater, PowerSupply, PowerMode, Fan
import mpam.device as device
from mpam.paths import Path
from mpam.pipettor import Pipettor
from mpam.thermocycle import Thermocycler, ChannelEndpoint, Channel
from mpam.types import XYCoord, Orientation, GridRegion, Delayed, Dir, State, \
    OnOff, DummyState
from quantities.SI import uL, ms, deg_C, sec, volts
from quantities.core import DerivedDim
from quantities.dimensions import Temperature, Time, Volume, Voltage
from quantities.temperature import TemperaturePoint, abs_C
from quantities.timestamp import Timestamp, time_now
from mpam.exerciser import PlatformChoiceTask, PlatformChoiceExerciser,\
    Exerciser
from argparse import Namespace, ArgumentParser, _ArgumentGroup
from erk.stringutils import conj_str

class HeaterType(Enum):
    TSRs = auto()
    Paddles = auto()

class HeatingRate(DerivedDim):
    derived = Temperature/Time


class Well(device.Well):
    _pipettor: Final[Pipettor]

    def __init__(self,
                 *, board:Board,
                 number:int,
                 group:DispenseGroup,
                 exit_pad:device.Pad,
                 shared_pads: Sequence[WellPad],
                 gate:WellGate,
                 capacity:Volume,
                 dispensed_volume:Volume,
                 exit_dir:Dir,
                 is_voidable:bool=False,
                 shape:Optional[WellShape]=None,
                 pipettor: Pipettor)-> None:
        super().__init__(board=board,
                         number=number,
                         group=group,
                         exit_pad=exit_pad,
                         gate=gate,
                         shared_pads=shared_pads,
                         capacity=capacity,
                         dispensed_volume=dispensed_volume,
                         exit_dir=exit_dir,
                         is_voidable=is_voidable,
                         shape=shape)
        self._pipettor = pipettor

    @property
    def pipettor(self)->Optional[Pipettor]:
        return self._pipettor


class EmulatedHeater(device.Heater):
    _last_read_time: Timestamp
    _heating_rate: HeatingRate
    _cooling_rate: HeatingRate

    def __init__(self, num: int, board: Board, *,
                 regions: Sequence[GridRegion],
                 wells: Sequence[Well],
                 max_heat: Optional[TemperaturePoint],
                 min_chill: Optional[TemperaturePoint],
                 polling_interval: Time = 200*ms) -> None:
        locs = list[Union[device.Pad,device.Well]]()
        for region in regions:
            locs += (board.pad_array[xy] for xy in region)
        locs += wells
            
        super().__init__(num, board,
                         polling_interval = polling_interval,
                         locations = locs,
                         max_heat = max_heat,
                         min_chill = min_chill,
                         initial_temperature = board.ambient_temperature)
        self._last_read_time = time_now()
        self._heating_rate = 100*(deg_C/sec).a(HeatingRate)
        self._cooling_rate = 10*(deg_C/sec).a(HeatingRate)
        # It really seems as though we should be able to just override the target setter, but I
        # can't get the compiler (and MyPy) to accept it
        key=(self, "target changed", random.random())

        def set_lrt() -> None:
            self._last_read_time = time_now()
        self.on_target_change(lambda _old,_new: set_lrt(), key=key)

    def new_temp(self, target: Optional[TemperaturePoint]) -> Optional[TemperaturePoint]:
        now = time_now()
        elapsed = now-self._last_read_time
        self._last_read_time = now
        mode = self.mode
        if mode is HeatingMode.MAINTAINING:
            return self.current_temperature
        assert self.current_temperature is not None
        if mode is HeatingMode.OFF and self.current_temperature <= self.board.ambient_temperature:
            return self.current_temperature
        delta: Temperature
        if mode is HeatingMode.HEATING:
            delta = (self._heating_rate*elapsed).a(Temperature)
            new_temp = self.current_temperature + delta
            if target is not None:
                new_temp = min(new_temp, target)
        else:
            delta = (self._cooling_rate*elapsed).a(Temperature)
            new_temp = self.current_temperature - delta
            if target is None:
                new_temp = max(new_temp, self.board.ambient_temperature)
            else:
                new_temp = max(new_temp, target)
        return new_temp

    def poll(self) -> Delayed[Optional[TemperaturePoint]]:
        return Delayed.complete(self.new_temp(self.target))


class ArmPos(Enum):
    BOARD = auto()
    TIPS = auto()
    BLOCK = auto()


class ExtractionPoint(device.ExtractionPoint):
    _pipettor: Final[Pipettor]

    def __init__(self, pad: device.Pad, pipettor: Pipettor, *, splash_radius: Optional[int] = None) -> None:
        super().__init__(pad, splash_radius=splash_radius)
        self._pipettor = pipettor

    @property
    def pipettor(self) -> Optional[Pipettor]:
        return self._pipettor


class Board(device.Board):
    thermocycler: Final[Thermocycler]
    pipettor: Final[Pipettor]

    def _pad_state(self, x: int, y: int) -> Optional[State[OnOff]]: # @UnusedVariable
        return DummyState(initial_state=OnOff.OFF)
        # return None

    def _well_gate_state(self, well: int) -> State[OnOff]: # @UnusedVariable
        return DummyState(initial_state=OnOff.OFF)

    def _well_pad_state(self, group_name: str, num: int) -> State[OnOff]: # @UnusedVariable
        return DummyState(initial_state=OnOff.OFF)

    def _magnets(self, *, first_num: int = 0) -> Sequence[Magnet]: # @UnusedVariable
        def make_magnet(num: int, *, pads: Sequence[Pad]) -> Magnet:
            state = DummyState(initial_state=OnOff.OFF)
            return Magnet(num, self, state=state, pads=pads)
        pads = (self.pad_at(13, 6), self.pad_at(13, 12))
        return (make_magnet(0, pads=pads),)

    def _rectangle(self, x: float, y: float, outdir: int, width: float, height: float) -> PadBounds:
        return ((x,y), (x+width*outdir,y), (x+width*outdir, y+height), (x, y+height))

    def _big_well_pad(self, x: float, y: float, outdir) -> PadBounds:
        x2 = x+0.8*outdir
        x3 = x+2*outdir
        y2 = y+1.75
        y3 = y+2.25
        y4 = y+4
        return ((x,y), (x2,y), (x3,y2), (x3,y3), (x2,y4), (x,y4))

    def _well(self, num: int, group: DispenseGroup, exit_dir: Dir, exit_pad: device.Pad, pipettor: Pipettor,
              shared_states: Sequence[State[OnOff]]):
        epx = exit_pad.location.x
        epy = exit_pad.location.y
        outdir = -1 if epx == 0 else 1
        if outdir == 1:
            epx += 1
        # gate_electrode = Electrode(gate_loc.x, gate_loc.y, self._states)

        pre_gate = 1
        pad_neighbors = [[1,4],[-1,0,2,4], [1,4],
                         [4,6], [0,1,2,3,5,6],[4,6],
                         [3,4,5,7],[6,8],[7]]

        shape = WellShape(
                    gate_pad_bounds= self._rectangle(epx, epy, outdir, 1, 1),
                    shared_pad_bounds = [self._rectangle(epx+1*outdir,epy+1,outdir,1,0.5),
                                         self._rectangle(epx+1*outdir,epy,outdir,1,1),
                                         self._rectangle(epx+1*outdir,epy-0.5,outdir,1,0.5),
                                         self._rectangle(epx+2*outdir,epy+1.5,outdir,1,1),
                                         self._rectangle(epx+2*outdir,epy-0.5,outdir,1,2),
                                         self._rectangle(epx+2*outdir,epy-1.5,outdir,1,1),
                                         self._rectangle(epx+3*outdir,epy-1.5,outdir,1,4),
                                         self._rectangle(epx+4*outdir,epy-1.5,outdir,1,4),
                                         self._big_well_pad(epx+5*outdir, epy-1.5, outdir)],
                    reagent_id_circle_radius = 1,
                    reagent_id_circle_center = (epx+8.5*outdir, epy+0.5)
                    )
        return Well(number=num,
                    board=self,
                    group=group,
                    exit_pad=exit_pad,
                    gate=WellGate(self,
                                  exit_pad=exit_pad,
                                  exit_dir=exit_dir,
                                  state=self._well_gate_state(num),
                                  neighbors=(pre_gate,)),
                    shared_pads=tuple(WellPad(self, state=s, neighbors=ns) for s,ns in zip(shared_states,
                                                                                           pad_neighbors)),
                    capacity=54.25*uL,
                    # dispensed_volume=0.5*uL,
                    dispensed_volume=1*uL,
                    exit_dir=exit_dir,
                    shape = shape,
                    pipettor = pipettor
                                         # self._rectangle(epx+5*outdir,epy-1.5,outdir,1,4),
                    # shared_pad_bounds = (self._long_pad_bounds(exit_pad.location),
                    #                      self._side_pad_bounds(exit_pad.location),
                    #                      self._big_pad_bounds(exit_pad.location))
                    )
        
    def _heaters(self, heater_type: HeaterType, *,
                 first_num: int = 0,
                 polling_interval: Time = 200*ms) -> Sequence[Heater]:
        def make_heater(num: int, *,
                        regions: Sequence[GridRegion]) -> Heater:
            return EmulatedHeater(num, board=self, regions=regions, wells=[],
                                  max_heat = 120*abs_C,
                                  min_chill = None, 
                                  polling_interval=polling_interval)
        regions: Sequence[Sequence[GridRegion]]
        if heater_type is HeaterType.TSRs:
    
            regions = ([GridRegion(XYCoord(0,12),3,7)],
                       [GridRegion(XYCoord(0,0),3,7)],
                       [GridRegion(XYCoord(8,12),3,7)],
                       [GridRegion(XYCoord(8,0),3,7)],
                       [GridRegion(XYCoord(16,12),3,7)],
                       [GridRegion(XYCoord(16,0),3,7)])
        else:
            assert heater_type is HeaterType.Paddles
            regions = ([GridRegion(XYCoord(0,0),3,19)],
                       [GridRegion(XYCoord(8,0),3,19)],
                       [GridRegion(XYCoord(16,0),3,19)])
        return [make_heater(i+first_num, regions=r) for i,r in enumerate(regions)]
            
    
    def _power_supply(self, *,
                      min_voltage: Voltage,
                      max_voltage: Voltage,
                      initial_voltage: Voltage,
                      initial_mode: PowerMode,
                      can_toggle: bool,
                      can_change_mode: bool,
                      ) -> PowerSupply:
        return PowerSupply(self,
                           min_voltage=min_voltage,
                           max_voltage=max_voltage,
                           initial_voltage=initial_voltage,
                           mode=initial_mode,
                           can_toggle=can_toggle,
                           can_change_mode=can_change_mode)

    def _fan(self, *,
             initial_state: OnOff) -> Fan:
        return Fan(self, state=initial_state)

    def __init__(self, *,
                 heater_type: HeaterType,
                 pipettor: Optional[Pipettor] = None,
                 off_on_delay: Time = Time.ZERO,
                 extraction_point_splash_radius: int = 0,
                 ps_min_voltage: Voltage = 60*volts,
                 ps_max_voltage: Voltage = 298*volts,
                 ps_initial_voltage: Voltage = 0*volts,
                 ps_initial_mode: PowerMode = PowerMode.DC,
                 ps_can_toggle: bool = True,
                 ps_can_change_mode: bool = True,
                 fan_initial_state: OnOff = OnOff.OFF,
                 ) -> None:
        pad_dict = dict[XYCoord, Pad]()
        wells: list[Well] = []
        magnets: list[Magnet] = []
        heaters: list[Heater] = []
        extraction_points: list[ExtractionPoint] = []
        power_supply = self._power_supply(min_voltage=ps_min_voltage,
                                          max_voltage=ps_max_voltage,
                                          initial_voltage=ps_initial_voltage,
                                          initial_mode=ps_initial_mode,
                                          can_toggle=ps_can_toggle,
                                          can_change_mode=ps_can_change_mode)
        fan = self._fan(initial_state=fan_initial_state)
        super().__init__(pads=pad_dict,
                         wells=wells,
                         magnets=magnets,
                         heaters=heaters,
                         extraction_points=extraction_points,
                         extraction_point_splash_radius=extraction_point_splash_radius,
                         power_supply=power_supply,
                         fan=fan,
                         orientation=Orientation.NORTH_POS_EAST_POS,
                         drop_motion_time=500*ms,
                         off_on_delay=off_on_delay)

        dead_region = GridRegion(XYCoord(7,8), width=5, height=3)

        for x in range(0,19):
            for y in range(0,19):
                loc = XYCoord(x, y)
                state = self._pad_state(x, y)
                exists = state is not None and loc not in dead_region
                if state is None:
                    state = DummyState(initial_state=OnOff.OFF)
                pad_dict[loc] = Pad(loc, self, exists=exists, state=state)

        sequences: WellOpSeqDict = {
            (WellState.EXTRACTABLE, WellState.READY): ((7,), (7,6,3,4,5), (6,3,4,5)),
            (WellState.READY, WellState.EXTRACTABLE): ((7,6,3,4,5,), (7,)),
            (WellState.READY, WellState.DISPENSED): ((3,4,5,0,1,2,-1),
                                                     (4,0,1,2,-1),
                                                     (1,-1),
                                                     (4,-1),
                                                     (3,4,5,6,-1),
                                                     (3,4,5,6)
                                                     ),
            (WellState.DISPENSED, WellState.READY): (),
            (WellState.READY, WellState.ABSORBED): ((3,4,5,6,0,1,2,-1),),
            (WellState.ABSORBED, WellState.READY): ((3,4,5,6),)
            }

        transition = transitions_from(sequences)

        left_group = DispenseGroup("left", transition)
        right_group = DispenseGroup("right", transition)

        left_states = tuple(self._well_pad_state('left', n) for n in range(9))
        right_states = tuple(self._well_pad_state('right', n) for n in range(9))

        if pipettor is None:
            from devices.dummy_pipettor import DummyPipettor
            pipettor = DummyPipettor()
        self.pipettor = pipettor

        wells.extend((
            self._well(0, left_group, Dir.RIGHT, self.pad_at(0,18), pipettor, left_states),
            self._well(1, left_group, Dir.RIGHT, self.pad_at(0,12), pipettor, left_states),
            self._well(2, left_group, Dir.RIGHT, self.pad_at(0,6), pipettor, left_states),
            self._well(3, left_group, Dir.RIGHT, self.pad_at(0,0), pipettor, left_states),
            self._well(4, right_group, Dir.LEFT, self.pad_at(18,18), pipettor, right_states),
            self._well(5, right_group, Dir.LEFT, self.pad_at(18,12), pipettor, right_states),
            self._well(6, right_group, Dir.LEFT, self.pad_at(18,6), pipettor, right_states),
            self._well(7, right_group, Dir.LEFT, self.pad_at(18,0), pipettor, right_states),
            ))

        magnets.extend(self._magnets())
        heaters.extend(self._heaters(heater_type))
        

        for pos in ((13, 15), (13, 9), (13, 3)):
            extraction_points.append(
                ExtractionPoint(self.pad_at(*pos), pipettor, splash_radius=extraction_point_splash_radius))

        def tc_channel(row: int,
                       # heaters: tuple[int,int],
                       thresholds: tuple[int,int],
                       in_dir: Dir,
                       adjacent_step: Dir,
                       ) -> Channel:
            def heater(thresh: Pad, in_dir: Dir) -> Heater:
                pad = thresh.neighbor(in_dir)
                assert pad is not None, f"No pad at {thresh}+{in_dir}"
                heater = pad.heater
                assert heater is not None, f"No heater at {pad}"
                return heater 
            
            left_thresh = self.pad_at(thresholds[0], row)

            right_thresh = self.pad_at(thresholds[1], row)
            return (ChannelEndpoint(heater(left_thresh, in_dir).number,
                                    left_thresh,
                                    in_dir,
                                    adjacent_step,
                                    Path.to_col(thresholds[1])),
                    ChannelEndpoint(heater(right_thresh, in_dir.opposite).number,
                                    right_thresh,
                                    in_dir.opposite,
                                    adjacent_step,
                                    Path.to_col(thresholds[0])))
        # left_heaters = (1, 0)
        # right_heaters = (1, 2)
        left_thresholds = (7, 3)
        right_thresholds = (11, 15)

        def left_tc_channel(row: int, step_dir: Dir) -> Channel:
            return tc_channel(row, left_thresholds,
                              Dir.RIGHT, step_dir)
        def right_tc_channel(row: int, step_dir: Dir) -> Channel:
            return tc_channel(row, right_thresholds,
                              Dir.LEFT, step_dir)


        tc_channels = (
                left_tc_channel(18, Dir.DOWN), left_tc_channel(16, Dir.UP),
                left_tc_channel(14, Dir.DOWN), left_tc_channel(12, Dir.UP),
                left_tc_channel(6, Dir.DOWN), left_tc_channel(4, Dir.UP),
                left_tc_channel(2, Dir.DOWN), left_tc_channel(0, Dir.UP),
                right_tc_channel(18, Dir.DOWN), right_tc_channel(16, Dir.UP),
                right_tc_channel(14, Dir.DOWN), right_tc_channel(12, Dir.UP),
                right_tc_channel(6, Dir.DOWN), right_tc_channel(4, Dir.UP),
                right_tc_channel(2, Dir.DOWN), right_tc_channel(0, Dir.UP),
            )
        self.thermocycler = Thermocycler(
            heaters = heaters,
            channels = tc_channels)

    def join_system(self, system: System) -> None:
        super().join_system(system)
        self.pipettor.join_system(system)

    def update_state(self):
        super().update_state()

    def stop(self)->None:
        # if self._port is not None:
        #     self._port.close()
        #     self._port = None
        super().stop()
    

heater_type_arg_names = {
    "tsr": HeaterType.TSRs,
    "tsrs": HeaterType.TSRs,
    "TSR": HeaterType.TSRs,
    "TSRs": HeaterType.TSRs,
    "paddles": HeaterType.Paddles,
    "paddle": HeaterType.Paddles,
    }
    
def heater_type_arg(arg: str) -> HeaterType:
    try:
        return heater_type_arg_names[arg]
    except KeyError:
        choices = conj_str([f'"{s}"' for s in sorted(heater_type_arg_names.keys())])
        raise ValueError(f"{arg} is not a valid heater type.  Choices are {choices}")
    
def heater_type_arg_name_for(t: HeaterType) -> str:
    for k,v in heater_type_arg_names.items():
        if v is t:
            return k
    assert False, f"Heater type {t} doesn't have an argument representation"

        
class PlatformTask(PlatformChoiceTask):
    default_heater_type: Final[HeaterType]
    def __init__(self, name: str = "Joey",
                 description: Optional[str] = None,
                 *,
                 default_heater_type: HeaterType = HeaterType.TSRs,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
        self.default_heater_type = default_heater_type
    
    
    def make_board(self, args: Namespace, *, 
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                   pipettor: Pipettor) -> Board: 
        off_on_delay: Time = args.off_on_delay
        return Board(pipettor=pipettor,
                     heater_type = heater_type_arg_names[args.heaters],
                     off_on_delay=off_on_delay,
                     extraction_point_splash_radius=args.extraction_point_splash_radius)
        
    def add_args_to(self, 
                     group: _ArgumentGroup, 
                     parser: ArgumentParser,
                     *,
                     exerciser: Exerciser) -> None:
        super().add_args_to(group, parser, exerciser=exerciser)
        group.add_argument('--heaters', 
                           # type=heater_type_arg, 
                           default=heater_type_arg_name_for(self.default_heater_type),
                           metavar="TYPE", 
                           choices=sorted(heater_type_arg_names),
                           help=f'''
                           The type of heater to use.  The default is {self.default_heater_type}.
                           ''')
        

        
    def available_wells(self, exerciser:Exerciser) -> Sequence[int]: # @UnusedVariable
        return [0,1,2,3,4,5,6,7]
