from __future__ import annotations

from argparse import Namespace, ArgumentParser, _ArgumentGroup, \
    BooleanOptionalAction
from enum import Enum, auto
from functools import cached_property
import logging
from typing import Optional, Sequence, Final, Union, Mapping

from devices.emulated_heater import EmulatedHeater, EmulatedChiller
from sifu.basic import assert_never
from sifu.cmd_line import coord_arg
from sifu.config import ConfigParam
from sifu.grid import Dir, XYCoord, GridRegion, Orientation, RCOrder
from sifu.stringutils import conj_str
from mpam import WellOpSeqDict, WellState, \
    WellShape, WellPad, Pad, Magnet, DispenseGroup, \
    WellGate, TemperatureControl, PowerSupply, PowerMode, Fan, \
    Heater, Chiller, StateDefs
import mpam
from mpam.exerciser import PlatformChoiceTask, PlatformChoiceExerciser, \
    Exerciser, BoardKwdArgs
from mpam.paths import Path
from mpam.pipettor import Pipettor
from mpam.thermocycle import Thermocycler, ChannelEndpoint, Channel
from mpam.types import State, \
    OnOff, DummyState, deg_C_per_sec
from sifu.quant.SI import uL, ms, volts, deg_C, mm
from sifu.quant.US import mil
from sifu.quant.dimensions import Volume, Distance, Area
from sifu.quant.temperature import abs_C


logger = logging.getLogger(__name__)

class HeaterType(Enum):
    TSRs = auto()
    Paddles = auto()
    RTDs = auto()
    
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
    heater_type: Final = ConfigParam[HeaterType](HeaterType.TSRs)
    layout: Final = ConfigParam(JoeyLayout.V1)
    holes: Final = ConfigParam[Sequence[XYCoord]]([])
    default_holes: Final = ConfigParam(True)
    lid_type: Final = ConfigParam(LidType.PLASTIC)
    
    _defaults_set_up = False
    @classmethod
    def setup_defaults(cls) -> None:
        if not cls._defaults_set_up:
            from mpam import Config as mpamConfig
            
            mpamConfig.polling_interval.default = 200*ms
            mpamConfig.ps_min_voltage.default = 60*volts
            mpamConfig.ps_max_voltage.default = 298*volts
            mpamConfig.ps_initial_voltage.default = 0*volts
            mpamConfig.ps_initial_mode.default = PowerMode.DC
            mpamConfig.ps_can_toggle.default = True
            mpamConfig.ps_can_change_mode.default = True
            mpamConfig.fan_initial_state.default = OnOff.OFF
            mpamConfig.fan_can_toggle.default = True
            cls._defaults_set_up = True

    
class Well(mpam.Well):
    @property
    def pipettor(self)->Pipettor:
        return self.board.pipettor



class ArmPos(Enum):
    BOARD = auto()
    TIPS = auto()
    BLOCK = auto()


class ExtractionPoint(mpam.ExtractionPoint):

    def __init__(self, pad: mpam.Pad, *, splash_radius: Optional[int] = None) -> None:
        super().__init__(pad, splash_radius=splash_radius)

    @property
    def pipettor(self) -> Pipettor  :
        return self.board.pipettor
    
    
v1_shared_pad_cells: Mapping[tuple[str,int], str] = {
    ('left', 1): 'BC27', ('left', 2): 'B27', ('left', 3): 'AB27', 
    ('left', 4): 'C28', ('left', 5): 'B28', ('left', 6): 'A28',
    ('left', 7): 'B29', ('left', 8): 'B30', ('left', 9): 'B31',
    ('right', 1): 'BC05', ('right', 2): 'B05', ('right', 3): 'AB05', 
    ('right', 4): 'C04', ('right', 5): 'B04', ('right', 6): 'A04',
    ('right', 7): 'B03', ('right', 8): 'B02', ('right', 9): 'B01',
    }
v1_5_shared_pad_cells: Mapping[tuple[str,int], str] = {
    ('left', 1): 'B27', ('left', 2): 'B28', ('left', 3): 'B29', 
    ('left', 4): 'B30', ('left', 5): 'B31', ('left', 6): 'B32',
    ('right', 1): 'B05', ('right', 2): 'B04', ('right', 3): 'B03', 
    ('right', 4): 'B02', ('right', 5): 'B01', ('right', 6): 'B00',
    }

    
    
class Board(mpam.Board):
    thermocycler: Thermocycler
    _layout: Final[JoeyLayout]
    _lid: Final[LidType]
    
    _shared_pad_cells: Final[Mapping[JoeyLayout, Mapping[tuple[str,int], str]]] = {
        JoeyLayout.V1: v1_shared_pad_cells,
        JoeyLayout.V1_5: v1_5_shared_pad_cells
        } 
    _well_gate_cells: Final[Mapping[XYCoord, str]] = {
        XYCoord(1,19): 'T26', XYCoord(1,13): 'N26', XYCoord(1,7): 'H26', XYCoord(1,1): 'B26',
        XYCoord(19,19): 'T06', XYCoord(19,13): 'N06', XYCoord(19,7): 'H06', XYCoord(19,1): 'B06'
        }
    
    def pad_cell(self, x: int, y: int) -> Optional[str]:
        if x > 19 or x < 1 or y > 19 or y < 1:
            return None
        return f"{ord('B')+y-1:c}{26-x:02d}"
    def shared_pad_cell(self, side: str, n: int) -> Optional[str]:
        return self._shared_pad_cells[self._layout].get((side, n))
    def well_gate_cell(self, exit_pad: Pad) -> Optional[str]:
        return self._well_gate_cells.get(exit_pad.location)

    @cached_property
    def power_supply(self) -> PowerSupply:
        return self.find_one(PowerSupply,
                             if_missing="Joey board doesn't have a registered power supply.")

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

    def _well(self, group: DispenseGroup, exit_dir: Dir, exit_pad: mpam.Pad,
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
                    shape = shape)
        
    def _heaters(self) -> Sequence[Heater]:
        heater_type = Config.heater_type()
        def make_heater(*, regions: Sequence[GridRegion]) -> Heater:
            return EmulatedHeater(board=self, regions=regions, wells=[],
                                  limit = 120*abs_C,
                                  driving_rate = 100*deg_C_per_sec,
                                  return_rate = 10*deg_C_per_sec,
                                  noise_sd = 0.05*deg_C)
        regions: Sequence[Sequence[GridRegion]]
        if (heater_type is HeaterType.TSRs
            or heater_type is HeaterType.RTDs):
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
            
    def _chillers(self) -> Sequence[Chiller]:
        def make_chiller(*, wells: Sequence[mpam.Well]) -> Chiller:
            return EmulatedChiller(board=self, regions=[], wells=wells,
                                   limit = 5*abs_C,
                                   driving_rate = 100*deg_C_per_sec,
                                   return_rate = 10*deg_C_per_sec,
                                   noise_sd = 0.1*deg_C)
        well_sets = ([w for w in self.wells if w.exit_dir is Dir.EAST],
                     [w for w in self.wells if w.exit_dir is Dir.WEST])
        return [make_chiller(wells=w) for w in well_sets]
            
    
    
    def _power_supply(self) -> PowerSupply:
        return PowerSupply(self)

    def _fan(self) -> Fan:
        return Fan(self)
    
    def _extraction_point_locs(self) -> Sequence[Union[XYCoord,Pad,tuple[int,int]]]:
        return ()
        # return ((14, 16), (14, 10), (14, 4))
                                                 
        
    def _add_pads(self)->None:
        super()._add_pads()
        joey_layout = self._layout
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
                self.pads[loc] = Pad(loc, self, exists=exists, state=state)
                
    def _add_all_wells(self) -> None:
                
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

        self._add_wells((
            self._well(left_group, Dir.RIGHT, self.pad_at(1,19), left_states, well_shape),
            self._well(left_group, Dir.RIGHT, self.pad_at(1,13), left_states, well_shape),
            self._well(left_group, Dir.RIGHT, self.pad_at(1,7), left_states, well_shape),
            self._well(left_group, Dir.RIGHT, self.pad_at(1,1), left_states, well_shape),
            self._well(right_group, Dir.LEFT, self.pad_at(19,19), right_states, well_shape),
            self._well(right_group, Dir.LEFT, self.pad_at(19,13), right_states, well_shape),
            self._well(right_group, Dir.LEFT, self.pad_at(19,7), right_states, well_shape),
            self._well(right_group, Dir.LEFT, self.pad_at(19,1), right_states, well_shape),
            ))
        
    def _add_all_externals(self)->None:
        super()._add_all_externals()
        self._add_externals(Magnet, self._magnets())
        self._add_externals(Heater, self._heaters())
        self._add_externals(Chiller, self._chillers())
        self._add_external(PowerSupply, self._power_supply())
        self._add_external(Fan, self._fan())


    def __init__(self) -> None:
        logger.info(f"Joey layout version is {Config.layout()}")
        logger.info(f"Lid type is {Config.lid_type()}")
        logger.info(f"Heater type is {Config.heater_type()}")

        self._layout = Config.layout()

        super().__init__(orientation=Orientation.NORTH_POS_EAST_POS,
                         drop_motion_time=500*ms,
                         cpt_layout=RCOrder.DOWN_RIGHT)
        
        self._lid = Config.lid_type()
        self._add_all_wells()
        
        def to_ep(xy: Union[XYCoord,Pad,tuple[int,int]]) -> ExtractionPoint:
            if isinstance(xy, tuple):
                xy = self.pad_at(*xy)
            elif isinstance(xy, XYCoord):
                xy = self.pad_array[xy]
            return ExtractionPoint(xy)
        
        ep_locs = list[Union[XYCoord,Pad,tuple[int,int]]](Config.holes())
        if Config.default_holes():
            ep_locs.extend(self._extraction_point_locs())
        
        self._add_extraction_points([to_ep(xy) for xy in ep_locs])
        
    def _finish_init(self) -> None:
        super()._finish_init()
        if not self._owns_externals:
            return
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
                # assert heater is not None, f"No heater at {pad}"
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

        # This isn't quite right.  At the moment (6/26/23), Joey 1.5 on Bilby
        # doesn't have any heaters.  I should actually figure out where there
        # are reasonable channels dynamically.
        if self.find_all(Heater):
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
                  ) -> Board: 
        kwds = self.board_kwd_args(args, announce=True)
        return Board(**kwds)
                    
    def setup_config_defaults(self) -> None:
        Config.setup_defaults()
        
        
    def _check_and_add_args_to(self, group:_ArgumentGroup, 
                               parser: ArgumentParser,
                               *, processed:set[type[PlatformChoiceTask]],
                               exerciser: Exerciser) -> None:
        if not self._args_needed(PlatformTask, processed):
            return
        Config.layout.add_choice_arg_to(group, joey_layout_arg_names,
                                        '--joey-version', 
                                        metavar="VERSION", 
                                        help="The version of the Joey layout.")
        Config.lid_type.add_choice_arg_to(group, LidType,
                                        '--lid-type', 
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
        super()._check_and_add_args_to(group, parser, processed=processed, exerciser=exerciser)
        self.add_heater_args_to(parser, exerciser=exerciser)
        self.add_power_supply_args_to(parser, exerciser=exerciser)
        self.add_fan_args_to(parser, exerciser=exerciser)
        
    def add_heater_args_to(self, parser:ArgumentParser, 
                           *, exerciser:Exerciser)->None:
        group = self.heater_group(parser)
        Config.heater_type.add_choice_arg_to(group, (HeaterType,
                                                     { 
                                                       "tsr": HeaterType.TSRs,
                                                       "TSR": HeaterType.TSRs,
                                                       "tsrs": HeaterType.TSRs,
                                                       "TSRs": HeaterType.TSRs,
                                                       "paddle": HeaterType.Paddles,
                                                       "paddles": HeaterType.Paddles,
                                                       "PADDLE": HeaterType.Paddles,
                                                       "rtd": HeaterType.RTDs,
                                                       "RTD": HeaterType.RTDs,
                                                       "rtds": HeaterType.RTDs,
                                                       "RTDs": HeaterType.RTDs,
                                                      }), 
                                             '--heaters', metavar="TYPE",
                                             
                                             help = "The type of heater to use.")
        super().add_heater_args_to(parser, exerciser=exerciser)

    def board_kwd_args(self, args: Namespace, *,
                       announce: bool = False) -> BoardKwdArgs:
        kwds = super().board_kwd_args(args, announce=announce)
        return kwds

        
    def available_wells(self, exerciser:Exerciser) -> Sequence[int]: # @UnusedVariable
        return [1,2,3,4,5,6,7,8]
