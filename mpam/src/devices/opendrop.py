from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser
from typing import Optional, Final, Sequence

from serial import Serial

from erk.config import ConfigParam
from erk.grid import XYCoord, Dir, Orientation
from mpam import device
from mpam.device import Well, WellOpSeqDict, WellState, PadBounds, \
    WellShape, Pad, WellGate, WellPad, StateDefs
from mpam.exerciser import PlatformChoiceTask, PlatformChoiceExerciser, \
    Exerciser
from mpam.types import OnOff, State
from quantities.SI import uL, ms


class Config:
    device = ConfigParam[Optional[str]](None)


class Electrode(State[OnOff]):
    index: Final[int]
    array: Final[bytearray]
    
    def realize_state(self, val: OnOff) -> None:
        self.array[self.index] = 1 if val else 0
    
    def __init__(self, x: int, y: int, a: bytearray) -> None:
        super().__init__(initial_state=OnOff.OFF)
        self.index = x*8+y
        self.array = a
        

class Board(device.Board):
    _dev: Optional[str]
    _states: bytearray
    _port: Optional[Serial]
    
    def _long_pad_bounds(self, ep_loc: XYCoord) -> PadBounds:
        epx = ep_loc.x
        epy = ep_loc.y
        outdir = -1 if epx == 1 else 1
        if outdir == 1:
            epx += 1
        return ((epx+outdir, epy),
                (epx+2.5*outdir, epy),
                (epx+2.5*outdir, epy-1),
                (epx+outdir, epy-1))
        
    def _side_pad_bounds(self, ep_loc: XYCoord) -> Sequence[PadBounds]:
        epx = ep_loc.x
        epy = ep_loc.y
        outdir = -1 if epx == 1 else 1
        if outdir == 1:
            epx += 1
        return (((epx+0.5*outdir, epy-1),
                 (epx+1.5*outdir, epy-1),
                 (epx+1.5*outdir, epy-2),
                 (epx+0.5*outdir, epy-2)),
                ((epx+0.5*outdir, epy),
                 (epx+1.5*outdir, epy),
                 (epx+1.5*outdir, epy+1),
                 (epx+0.5*outdir, epy+1))
                 )
    
    def _big_pad_bounds(self, ep_loc: XYCoord) -> PadBounds:
        epx = ep_loc.x
        epy = ep_loc.y
        outdir = -1 if epx == 1 else 1
        if outdir == 1:
            epx += 1
        return ((epx+1.5*outdir, epy+1),
                (epx+3.5*outdir, epy+1),
                (epx+3.5*outdir, epy-2),
                (epx+1.5*outdir, epy-2),
                (epx+1.5*outdir, epy-1),
                (epx+2.5*outdir, epy-1),
                (epx+2.5*outdir, epy),
                (epx+1.5*outdir, epy)
                )
        

    def _gate_bounds(self, ep_loc: XYCoord) -> PadBounds:
        epx = ep_loc.x
        epy = ep_loc.y
        outdir = -1 if epx == 1 else 1
        if outdir == 1:
            epx += 1
        return ((epx,epy), 
                (epx+outdir,epy), 
                (epx+outdir,epy-1),
                (epx, epy-1))
        
    def _reagent_circle_center(self, ep_loc: XYCoord) -> tuple[float,float]:
        epx = ep_loc.x
        epy = ep_loc.y
        outdir = -1 if epx == 1 else 1
        if outdir == 1:
            epx += 1
        return (epx+5*outdir, epy-0.5)
    
    def _well(self, states: StateDefs, exit_dir: Dir, gate_loc: XYCoord, exit_pad: Pad,
              inner_locs: Sequence[tuple[int,int]], shape: WellShape) -> Well:
        gate_electrode = Electrode(gate_loc.x, gate_loc.y, self._states)
        gate = WellGate(self, exit_pad, exit_dir, gate_electrode, neighbors=(0,1))
        pad_neighbors = [[-1,1,2], [0,2], [0, 1]]
        inner_electrodes = tuple(Electrode(x, y, self._states) for x,y in inner_locs)
        shared = tuple(WellPad(self, state=s, neighbors=ns) for s,ns in zip(inner_electrodes, pad_neighbors))
        return Well(board=self,
                    group=states,
                    exit_dir=exit_dir,
                    exit_pad=exit_pad,
                    gate=gate,
                    shared_pads = shared,
                    capacity=12*uL,
                    dispensed_volume=2*uL,
                    shape=shape
                    )
        
    def _add_pads(self)->None:
        super()._add_pads()
        for x in range(1,15):
            for y in range(0,8):
                loc = XYCoord(x, y)
                e = Electrode(x, y, self._states)
                p = Pad(loc, self, e)
                self.pads[loc] = p
    
    def __init__(self) -> None:
        super().__init__(orientation=Orientation.NORTH_NEG_EAST_POS,
                         drop_motion_time=500*ms)
        self._dev = Config.device()
        self._states = bytearray(128)
        self._port= None
                
        states = {
            WellState.READY: (1,2),
            WellState.EXTRACTABLE: (),
            WellState.INJECTABLE: (),
            }
        
        sequences: WellOpSeqDict = {
            (WellState.EXTRACTABLE, WellState.READY): ((2,),(1,2)),
            (WellState.READY, WellState.EXTRACTABLE): ((2,), ()),
            (WellState.READY, WellState.DISPENSED): ((-1,0,1),(-1,),(1,2)),
            (WellState.READY, WellState.ABSORBED): ((-1,2),(1,2)),
            }
        
        state_defs = StateDefs(states, sequences)
        
        def inner_locs(col: int, rows: Sequence[int]) -> Sequence[tuple[int,int]]:
            return [(col, r) for r in rows]
        
        shape = WellShape( 
                    side = Dir.EAST,
                    shared_pad_bounds = (
                        [(1,0.5), (1,1.5), (3,1.5),
                         (3,-1.5), (1,-1.5), (1,-0.5),
                         (2,-0.5), (2, 0.5)],
                        [WellShape.square((0.5,-1)), 
                         WellShape.square((0.5, 1))],
                        WellShape.rectangle((1.25,0),width=1.5)),
                    reagent_id_circle_radius = 1,
                    reagent_id_circle_center = (4.5, 0)
            )
        upper_left = self._well(state_defs, Dir.RIGHT, XYCoord(0,0), self.pad_at(1,1), inner_locs(0, (1,2,3)), shape)
        upper_right = self._well(state_defs, Dir.LEFT, XYCoord(15,0), self.pad_at(14,1), inner_locs(15, (1,2,3)), shape)
        lower_left = self._well(state_defs, Dir.RIGHT, XYCoord(0,7), self.pad_at(1,6), inner_locs(0, (6,5,4)), shape)
        lower_right = self._well(state_defs, Dir.LEFT, XYCoord(15,7), self.pad_at(14,6), inner_locs(15, (6,5,4)), shape)
        self._add_wells((upper_left, upper_right, lower_left, lower_right))
        
    def update_state(self) -> None:
        if self._port is None:
            if self._dev is not None:
                self._port = Serial(self._dev)
                # self._stream = open(self._dev, "wb")
        if self._port is not None:
            self._port.write(self._states)
            # I'm not sure why, but it seems that nothing happens until the 
            # first byte of the next round gets sent. (Sending 129 bytes works, 
            # but then the next round will use that extra byte.  Sending everything
            # twice seems to do the job.  I'll look into this further.
            self._port.write(self._states)
        super().update_state()
        
    def stop(self)->None:
        if self._port is not None:
            self._port.close()
            self._port = None
        super().stop()
        
    # def electrode(self, i: int) -> Electrode:
    #     return Electrode(i, self._states)
    
class PlatformTask(PlatformChoiceTask):
    def __init__(self, name: str = "Opendrop",
                 description: Optional[str] = None,
                 *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
    
    
    def make_board(self, args: Namespace, *,            # @UnusedVariable
                   exerciser: PlatformChoiceExerciser,  # @UnusedVariable
                   ) -> Board: # @UnusedVariable
        return Board()
    
    def _check_and_add_args_to(self, group:_ArgumentGroup, 
                               parser:ArgumentParser, 
                               *, processed:set[type[PlatformChoiceTask]], 
                               exerciser:Exerciser)-> None:
        if not self._args_needed(PlatformTask, processed):
            return
        super().add_args_to(group, parser, exerciser=exerciser)
        Config.device.add_arg_to(group,'-p', '--port',
                                 default_desc="to only run the display",
                                 help="The communication port (e.g., COM5) to use to talk to the board.")
        
        
    def available_wells(self, exerciser:Exerciser) -> Sequence[int]: # @UnusedVariable
        return [0,1,2,3]