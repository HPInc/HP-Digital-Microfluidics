from __future__ import annotations

from argparse import Namespace, ArgumentParser, _ArgumentGroup,\
    BooleanOptionalAction
from enum import Enum, auto
from typing import Optional, Sequence, Final, Union

from devices.emulated_heater import EmulatedHeater, EmulatedChiller
from erk.basic import assert_never
from erk.stringutils import conj_str
from mpam.device import WellOpSeqDict, WellState, \
    WellShape, System, WellPad, Pad, Magnet, DispenseGroup, \
    WellGate, TemperatureControl, PowerSupply, PowerMode, Fan,\
    Heater, Chiller, StateDefs
import mpam.device as device
from mpam.exerciser import PlatformChoiceTask, PlatformChoiceExerciser, \
    Exerciser, BoardKwdArgs
from mpam.paths import Path
from mpam.pipettor import Pipettor
from mpam.thermocycle import Thermocycler, ChannelEndpoint, Channel
from mpam.types import XYCoord, Orientation, GridRegion, Dir, State, \
    OnOff, DummyState, RCOrder, deg_C_per_sec
from quantities.SI import uL, ms, volts, deg_C, mm


from quantities.dimensions import Time, Volume, Voltage, Distance, Area
from quantities.temperature import abs_C
from mpam.cmd_line import coord_arg
from quantities.US import mil
import logging
from erk.config import ConfigParam

logger = logging.getLogger(__name__)

class HeaterType(Enum):
    TSRs = auto()
    Paddles = auto()
    
    @classmethod
    def from_name(cls, name: str) -> HeaterType:
        return heater_type_arg_names[name]
    
class JoeyLayout(Enum):
    V1 = auto()
    V1_5 = auto()
    
    @classmethod
    def from_name(cls, name: str) -> JoeyLayout:
        return joey_layout_arg_names[name]
    
    @property
    def gap(self) -> Distance:
        if self is JoeyLayout.V1:
            return 3*mil
        elif self is JoeyLayout.V1_5:
            return 2*mil
        else:
            assert_never(self)
            
    @property
    def pad_area(self) -> Area:
        pitch = 1.5*mm
        return (pitch-self.gap)**2
    
    def well_capacity(self, exit_dir: Dir) -> Volume:
        assert exit_dir is Dir.EAST or exit_dir is Dir.WEST
        if self is JoeyLayout.V1:
            return 30*uL if exit_dir is Dir.EAST else 15*uL
        if self is JoeyLayout.V1_5:
            return 15*uL
        else:
            assert_never(self)
            
joey_layout_arg_names = {
    "1": JoeyLayout.V1,
    "1.0": JoeyLayout.V1,
    "1.5": JoeyLayout.V1_5,
    }

class LidType(Enum):
    GLASS = auto()
    PLASTIC = auto()

    @property
    def height(self) -> Distance:
        if self is LidType.PLASTIC:
            return 0.3*mm
        elif self is LidType.GLASS:
            return 0.2*mm
        else:
            assert_never(self)

lid_type_arg_names = {
    "glass": LidType.GLASS,
    "GLASS": LidType.GLASS,
    "plastic": LidType.PLASTIC,
    "PLASTIC": LidType.PLASTIC
    }

class Config:
    heater_type: Final = ConfigParam(HeaterType.TSRs)
    layout: Final = ConfigParam(JoeyLayout.V1)
    ps_min_voltage: Final = ConfigParam(60*volts)
    ps_max_voltage: Final = ConfigParam(298*volts)
    ps_initial_voltage: Final = ConfigParam(0*volts)
    ps_initial_mode: Final = ConfigParam(PowerMode.DC)
    ps_can_toggle: Final = ConfigParam(True)
    ps_can_change_mode: Final = ConfigParam(True)
    fan_initial_state: Final = ConfigParam(OnOff.OFF)
    holes: Final = ConfigParam[Sequence[XYCoord]]([])
    default_holes: Final = ConfigParam(True)
    lid_type: Final = ConfigParam(LidType.PLASTIC)

    
class Well(device.Well):
    _pipettor: Final[Pipettor]

    def __init__(self,
                 *, board:Board,
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
    _layout: Final[JoeyLayout]
    _lid: Final[LidType]

    def _pad_state(self, x: int, y: int) -> Optional[State[OnOff]]: # @UnusedVariable
        return DummyState(initial_state=OnOff.OFF)
        # return None

    def _well_gate_state(self, exit_pad: Pad) -> State[OnOff]: # @UnusedVariable
        return DummyState(initial_state=OnOff.OFF)

    def _well_pad_state(self, group_name: str, num: int) -> State[OnOff]: # @UnusedVariable
        return DummyState(initial_state=OnOff.OFF)

    def _magnets(self) -> Sequence[Magnet]: # @UnusedVariable
        def make_magnet(*, pads: Sequence[Pad]) -> Magnet:
            state = DummyState(initial_state=OnOff.OFF)
            return Magnet(self, state=state, pads=pads)
        pads = (self.pad_at(14, 7), self.pad_at(14, 13))
        return (make_magnet(pads=pads),)

    
    def _well_capacity(self, exit_dir: Dir) -> Volume:
        # TODO: Should this be based on the lid height?
        return self._layout.well_capacity(exit_dir)
        # return 54.25*uL
    
    def _dispensed_volume(self) -> Volume:
        return self._layout.pad_area*self._lid.height

    def _well(self, group: DispenseGroup, exit_dir: Dir, exit_pad: device.Pad, pipettor: Pipettor,
              shared_states: Sequence[State[OnOff]], shape: WellShape) -> Well:

        if self._layout is JoeyLayout.V1:
            pre_gate = 1
            pad_neighbors = [[1,4],[-1,0,2,4], [1,4],
                             [4,6], [0,1,2,3,5,6],[4,6],
                             [3,4,5,7],[6,8],[7]]
        elif self._layout is JoeyLayout.V1_5:
            pre_gate = 0
            pad_neighbors = [[-1,1], [0,2], [1,3], [2,4],
                             [3,5],[4]]
        else:
            assert_never(self._layout)

        return Well(board=self,
                    group=group,
                    exit_pad=exit_pad,
                    gate=WellGate(self,
                                  exit_pad=exit_pad,
                                  exit_dir=exit_dir,
                                  state=self._well_gate_state(exit_pad),
                                  neighbors=(pre_gate,)),
                    shared_pads=tuple(WellPad(self, state=s, neighbors=ns) for s,ns in zip(shared_states,
                                                                                           pad_neighbors)),
                    capacity=self._well_capacity(exit_dir),
                    dispensed_volume=self._dispensed_volume(),
                    # dispensed_volume=1*uL,
                    exit_dir=exit_dir,
                    shape = shape,
                    pipettor = pipettor
                    )
        
    def _heaters(self, heater_type: HeaterType, *,
                 polling_interval: Time = 200*ms) -> Sequence[Heater]:
        def make_heater(*, regions: Sequence[GridRegion]) -> Heater:
            return EmulatedHeater(board=self, regions=regions, wells=[],
                                  limit = 120*abs_C,
                                  polling_interval=polling_interval,
                                  driving_rate = 100*deg_C_per_sec,
                                  return_rate = 10*deg_C_per_sec,
                                  noise_sd = 0.05*deg_C)
        regions: Sequence[Sequence[GridRegion]]
        if heater_type is HeaterType.TSRs:
            regions = ([GridRegion(XYCoord(1,13),3,7)],
                       [GridRegion(XYCoord(1,1),3,7)],
                       [GridRegion(XYCoord(9,13),3,7)],
                       [GridRegion(XYCoord(9,1),3,7)],
                       [GridRegion(XYCoord(17,13),3,7)],
                       [GridRegion(XYCoord(17,1),3,7)])
        elif heater_type is HeaterType.Paddles:
            regions = ([GridRegion(XYCoord(1,1),3,19)],
                       [GridRegion(XYCoord(9,1),3,19)],
                       [GridRegion(XYCoord(17,1),3,19)])
        else:
            assert_never(heater_type)
        return [make_heater(regions=r) for r in regions]
            
    def _chillers(self, *, polling_interval: Time = 200*ms) -> Sequence[Chiller]:
        def make_chiller(*, wells: Sequence[device.Well]) -> Chiller:
            return EmulatedChiller(board=self, regions=[], wells=wells,
                                   limit = 5*abs_C,
                                   polling_interval=polling_interval,
                                   driving_rate = 100*deg_C_per_sec,
                                   return_rate = 10*deg_C_per_sec,
                                   noise_sd = 0.1*deg_C)
        well_sets = ([w for w in self.wells if w.exit_dir is Dir.EAST],
                     [w for w in self.wells if w.exit_dir is Dir.WEST])
        return [make_chiller(wells=w) for w in well_sets]
            
    
    
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
    
    def _extraction_point_locs(self) -> Sequence[Union[XYCoord,Pad,tuple[int,int]]]:
        return ()
        # return ((14, 16), (14, 10), (14, 4))
                                                 
        
    

    def __init__(self, *,
                 pipettor: Optional[Pipettor] = None,
                 ) -> None:
        joey_layout = Config.layout()
        logger.info(f"Joey layout version is {Config.layout()}")
        logger.info(f"Lid type is {Config.lid_type()}")
        logger.info(f"Heater type is {Config.heater_type()}")
        self._lid = Config.lid_type()
        self._layout = Config.layout()
        pad_dict = dict[XYCoord, Pad]()
        wells: list[Well] = []
        magnets: list[Magnet] = []
        extraction_points: list[ExtractionPoint] = []
        power_supply = self._power_supply(min_voltage=Config.ps_min_voltage(),
                                          max_voltage=Config.ps_max_voltage(),
                                          initial_voltage=Config.ps_initial_voltage(),
                                          initial_mode=Config.ps_initial_mode(),
                                          can_toggle=Config.ps_can_toggle(),
                                          can_change_mode=Config.ps_can_change_mode())
        fan = self._fan(initial_state=Config.fan_initial_state())
        super().__init__(pads=pad_dict,
                         wells=wells,
                         magnets=magnets,
                         extraction_points=extraction_points,
                         power_supply=power_supply,
                         fan=fan,
                         orientation=Orientation.NORTH_POS_EAST_POS,
                         drop_motion_time=500*ms,
                         cpt_layout=RCOrder.DOWN_RIGHT)
        
        dead_regions: Sequence[GridRegion]
        if joey_layout is JoeyLayout.V1:
            dead_regions = [GridRegion(XYCoord(8,9), width=5, height=3)]
        elif joey_layout is JoeyLayout.V1_5:
            dead_regions = [GridRegion(XYCoord(8,9), width=4, height=1),
                            GridRegion(XYCoord(8,11), width=4, height=1),
                            GridRegion(XYCoord(19,10), width=1, height=1),
                            GridRegion(XYCoord(2,4), width=1, height=2),
                            GridRegion(XYCoord(2,15), width=1, height=2),
                            GridRegion(XYCoord(10,4), width=1, height=2),
                            GridRegion(XYCoord(10,15), width=1, height=2),
                            GridRegion(XYCoord(18,4), width=1, height=2),
                            GridRegion(XYCoord(18,15), width=1, height=2),
                            ]
        else:
            assert_never(joey_layout)

        for x in range(1,20):
            for y in range(1,20):
                loc = XYCoord(x, y)
                state = self._pad_state(x, y)
                exists = (state is not None and 
                          all(loc not in r for r in dead_regions))
                if state is None:
                    state = DummyState(initial_state=OnOff.OFF)
                pad_dict[loc] = Pad(loc, self, exists=exists, state=state)
                
        sequences: WellOpSeqDict
        if self._layout is JoeyLayout.V1:
            sequences = {
                (WellState.EXTRACTABLE, WellState.READY): ((8,), (4,5,6,7,8), (4,5,6,7)),
                (WellState.READY, WellState.EXTRACTABLE): ((4,5,6,7,8), (8,), ()),
                (WellState.READY, WellState.DISPENSED): ((6,3,4,5,1,2,-1),
                                                         (5,1,2,3,-1),
                                                         (2,-1),
                                                         (5,-1),
                                                         (4,5,6,7,-1),
                                                         (4,5,6,7)
                                                         ),
                (WellState.READY, WellState.ABSORBED): ((4,5,6,7,1,2,3,-1),),
                (WellState.ABSORBED, WellState.READY): ((4,5,6,7),)
                }
            states = {
                WellState.READY: (4,5,6,7),
                WellState.EXTRACTABLE: (),
                WellState.INJECTABLE: (4,5,6,7,8), 
                }
            n_shared_pads = 9   
            well_shape = WellShape(
                    side = Dir.EAST,
                    shared_pad_bounds = [WellShape.rectangle((1, 0.75), height=0.5),
                                         WellShape.square((1,0)),
                                         WellShape.rectangle((1, -0.75), height=0.5),
                                         WellShape.square((2, 1.5)),
                                         WellShape.rectangle((2, 0), height=2),
                                         WellShape.square((2, -1.5)),
                                         WellShape.rectangle((3,0), height=4),
                                         WellShape.rectangle((4,0), height=4),
                                         [(4.5,-2), (5.3,-2), (6.5, -0.25),
                                          (6.5, 0.25), (5.3, 2), (4.5, 2)]],
                    reagent_id_circle_radius = 1,
                    reagent_id_circle_center = (8, 0)
                    )
        elif self._layout is JoeyLayout.V1_5:
            sequences = {
                (WellState.EXTRACTABLE, WellState.READY): ((4,), (2,3,4), (2,3)),
                (WellState.READY, WellState.EXTRACTABLE): ((2,3,4), (4,), ()),
                (WellState.READY, WellState.DISPENSED): ((1,2,-1),
                                                         (1,2,-1),
                                                         (1,-1),
                                                         (2,-1),
                                                         (2,3,-1),
                                                         (2,3)
                                                         ),
                (WellState.READY, WellState.ABSORBED): ((1,2,3,-1),),
                (WellState.ABSORBED, WellState.READY): ((2,3),)
                }
            states = {
                WellState.READY: (2,3),
                WellState.EXTRACTABLE: (),
                WellState.INJECTABLE: (2,3,4), 
                }   
            n_shared_pads = 6
            well_shape = WellShape(
                    side = Dir.EAST,
                    shared_pad_bounds = [WellShape.square((1,0)),
                                         [(1, -0.5), (1, -0.75), (2.5, -2),
                                          (2.5, 2), (1, 0.75), (1, 0.5),
                                          (1.5, 0.5), (1.5, -0.5)],
                                         WellShape.rectangle((3,0), height=4),
                                         WellShape.rectangle((4,0), height=4),
                                         WellShape.rectangle((5,0), height=4),
                                         [(5.5, -2), (5.75, -2), (6.5, -0.75),
                                          (6.5, 0.75), (5.75, 2), (5.5, 2),
                                          ]
                                         ],
                    reagent_id_circle_radius = 1,
                    reagent_id_circle_center = (8, 0)
                    )
        else:
            assert_never(self._layout)


        
        state_defs = StateDefs(states, sequences)

        left_group = DispenseGroup("left", states=state_defs)
        right_group = DispenseGroup("right", states=state_defs)

        left_states = tuple(self._well_pad_state('left', n+1) for n in range(n_shared_pads))
        right_states = tuple(self._well_pad_state('right', n+1) for n in range(n_shared_pads))

        if pipettor is None:
            from devices.dummy_pipettor import DummyPipettor
            pipettor = DummyPipettor()
        self.pipettor = pipettor
        
        

        self._add_wells((
            self._well(left_group, Dir.RIGHT, self.pad_at(1,19), pipettor, left_states, well_shape),
            self._well(left_group, Dir.RIGHT, self.pad_at(1,13), pipettor, left_states, well_shape),
            self._well(left_group, Dir.RIGHT, self.pad_at(1,7), pipettor, left_states, well_shape),
            self._well(left_group, Dir.RIGHT, self.pad_at(1,1), pipettor, left_states, well_shape),
            self._well(right_group, Dir.LEFT, self.pad_at(19,19), pipettor, right_states, well_shape),
            self._well(right_group, Dir.LEFT, self.pad_at(19,13), pipettor, right_states, well_shape),
            self._well(right_group, Dir.LEFT, self.pad_at(19,7), pipettor, right_states, well_shape),
            self._well(right_group, Dir.LEFT, self.pad_at(19,1), pipettor, right_states, well_shape),
            ))

        self._add_magnets(self._magnets())
        self._add_heaters(self._heaters(Config.heater_type()))
        self._add_chillers(self._chillers())
        # self._add_heaters(self._heaters(HeaterType.Peltier))
        

        def to_ep(xy: Union[XYCoord,Pad,tuple[int,int]], pipettor: Pipettor) -> ExtractionPoint:
            if isinstance(xy, tuple):
                xy = self.pad_at(*xy)
            elif isinstance(xy, XYCoord):
                xy = self.pad_array[xy]
            return ExtractionPoint(xy, pipettor)
        
        ep_locs = list[Union[XYCoord,Pad,tuple[int,int]]](Config.holes())
        if Config.default_holes():
            ep_locs.extend(self._extraction_point_locs())
        
        self._add_extraction_points([to_ep(xy, pipettor) for xy in ep_locs])

        def tc_channel(row: int,
                       # heaters: tuple[int,int],
                       thresholds: tuple[int,int],
                       in_dir: Dir,
                       adjacent_step: Dir,
                       ) -> Optional[Channel]:
            def heater(thresh: Pad, in_dir: Dir) -> Optional[TemperatureControl]:
                # We allow that this pad might not actually exist in order to handle Wombat
                pad = thresh.neighbor(in_dir, only_existing=False)
                assert pad is not None, f"No pad at {thresh}+{in_dir}"
                if not pad.exists:
                    return None
                heater = pad.temperature_control
                assert heater is not None, f"No heater at {pad}"
                return heater 
            
            left_thresh = self.pad_at(thresholds[0], row)
            left_heater = heater(left_thresh, in_dir)
            if left_heater is None:
                return None

            right_thresh = self.pad_at(thresholds[1], row)
            right_heater = heater(right_thresh, in_dir.opposite)
            if right_heater is None: 
                return None
            
            return (ChannelEndpoint(left_heater,
                                    left_thresh,
                                    in_dir,
                                    adjacent_step,
                                    Path.to_col(thresholds[1])),
                    ChannelEndpoint(right_heater,
                                    right_thresh,
                                    in_dir.opposite,
                                    adjacent_step,
                                    Path.to_col(thresholds[0])))
        # left_heaters = (1, 0)
        # right_heaters = (1, 2)
        left_thresholds = (8, 4)
        right_thresholds = (12, 16)

        def left_tc_channel(row: int, step_dir: Dir) -> Optional[Channel]:
            return tc_channel(row, left_thresholds,
                              Dir.RIGHT, step_dir)
        def right_tc_channel(row: int, step_dir: Dir) -> Optional[Channel]:
            return tc_channel(row, right_thresholds,
                              Dir.LEFT, step_dir)


        tc_channels = (
                left_tc_channel(19, Dir.DOWN), left_tc_channel(17, Dir.UP),
                left_tc_channel(15, Dir.DOWN), left_tc_channel(13, Dir.UP),
                left_tc_channel(7, Dir.DOWN), left_tc_channel(5, Dir.UP),
                left_tc_channel(3, Dir.DOWN), left_tc_channel(1, Dir.UP),
                right_tc_channel(19, Dir.DOWN), right_tc_channel(17, Dir.UP),
                right_tc_channel(15, Dir.DOWN), right_tc_channel(13, Dir.UP),
                right_tc_channel(7, Dir.DOWN), right_tc_channel(5, Dir.UP),
                right_tc_channel(3, Dir.DOWN), right_tc_channel(1, Dir.UP),
            )
        self.thermocycler = Thermocycler(
            # heaters = self.temperature_controls,
            channels = tc_channels)

    def join_system(self, system: System) -> None:
        super().join_system(system)
        self.pipettor.join_system(system)

    def update_state(self) -> None:
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
    
# def heater_type_arg(arg: str) -> HeaterType:
#     try:
#         return heater_type_arg_names[arg]
#     except KeyError:
#         choices = conj_str([f'"{s}"' for s in sorted(heater_type_arg_names.keys())])
#         raise ValueError(f"{arg} is not a valid heater type.  Choices are {choices}")
#
# def heater_type_arg_name_for(t: HeaterType) -> str:
#     for k,v in heater_type_arg_names.items():
#         if v is t:
#             return k
#     assert False, f"TemperatureControl type {t} doesn't have an argument representation"

        
class PlatformTask(PlatformChoiceTask):
    default_heater_type: Final[HeaterType]
    default_joey_layout: Final[JoeyLayout]
    def __init__(self, name: str = "Joey",
                 description: Optional[str] = None,
                 *,
                 default_heater_type: HeaterType = HeaterType.TSRs,
                 default_joey_layout: JoeyLayout = JoeyLayout.V1,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
        self.default_heater_type = default_heater_type
        self.default_joey_layout = default_joey_layout
    
    
    def make_board(self, args: Namespace, *, 
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                   pipettor: Pipettor) -> Board: 
        kwds = self.board_kwd_args(args, announce=True)
        # off_on_delay: Time = args.off_on_delay
        return Board(pipettor=pipettor, **kwds)
                    # heater_type = HeaterType.from_name(args.heaters),
                    # off_on_delay=off_on_delay,
                    # extraction_point_splash_radius=args.extraction_point_splash_radius,
                    # holes=args.holes,
                    # default_holes=args.default_holes
                    # )
        
    def add_args_to(self, 
                     group: _ArgumentGroup, 
                     parser: ArgumentParser,
                     *,
                     exerciser: Exerciser) -> None:
        super().add_args_to(group, parser, exerciser=exerciser)
        Config.heater_type.add_choice_arg_to(group, heater_type_arg_names, 
                                             '--heaters', metavar="TYPE",
                                             help = "The type of heater to use.")
        Config.layout.add_choice_arg_to(group, joey_layout_arg_names,
                                        '--joey-version', 
                                        metavar="VERSION", 
                                        help="The version of the Joey layout.")
        Config.lid_type.add_choice_arg_to(group, lid_type_arg_names,
                                        '--lid_type', 
                                        metavar="TYPE", 
                                        help="The type of lid used.")
        Config.lid_type.add_arg_to(group, '--glass', action='store_const', 
                                   dest='lid_type',
                                   # const=LidType.GLASS,
                                   const="glass", 
                                   deprecated=ConfigParam.use_instead("--lid-type glass"),
                                   help="Glass lid.")
        Config.lid_type.add_arg_to(group, '--plastic', action='store_const', 
                                   dest='lid_type',
                                   # const=LidType.PLASTIC,
                                   const="plastic", 
                                   deprecated=ConfigParam.use_instead("--lid-type plastic"),
                                   help="Plastic lid.")
        
        def default_holes_desc(holes: Sequence[XYCoord]) -> str:
            def fmt(xy: XYCoord) -> str:
                return f"({xy.col}, {xy.row})"
            if len(holes) == 0:
                return "to have no holes"
            if len(holes) == 1:
                return f"to have a hole at  {fmt(holes[0])}"
            return f"to have holes at {conj_str([fmt(xy) for xy in holes])}"
        Config.holes.add_arg_to(group,
                                '--hole', action='append', dest="holes", 
                                default_desc=default_holes_desc,
                                type=coord_arg, metavar="X,Y",
                                help='''The x,y coordinates of a hole in the lid.  
                                This may be specified multiple times.'''
                                )
        Config.default_holes.add_arg_to(group, '--default-holes', action=BooleanOptionalAction,
                           help="Whether or not to include default holes in addition to those specified by --hole."
                           )
        
    def board_kwd_args(self, args: Namespace, *,
                       announce: bool = False) -> BoardKwdArgs:
        kwds = super().board_kwd_args(args, announce=announce)
        return kwds

        
    def available_wells(self, exerciser:Exerciser) -> Sequence[int]: # @UnusedVariable
        return [1,2,3,4,5,6,7,8]
