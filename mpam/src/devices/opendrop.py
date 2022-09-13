from __future__ import annotations

from argparse import Namespace, _ArgumentGroup, ArgumentParser,\
    BooleanOptionalAction
from typing import Optional, Final, Sequence, Callable

from serial import Serial

from mpam import device
from mpam.device import Well, WellOpSeqDict, WellState, PadBounds, \
    WellShape, Pad, WellGate, WellPad, transitions_from, \
    TransitionFunc
from mpam.exerciser import PlatformChoiceTask, PlatformChoiceExerciser, \
    Exerciser
from mpam.pipettor import Pipettor
from mpam.types import OnOff, XYCoord, Orientation, Dir, State
from quantities.SI import uL, ms
from quantities.dimensions import Time
from abc import abstractmethod
import logging

logger = logging.getLogger(__name__)

class Electrode(State[OnOff]):
    byte_index: Final[int]
    bit_index: Final[int]

    array: Final[bytearray]
    
    def realize_state(self, val: OnOff) -> None:
        # assert self.index < len(self.array), f"{self.index} not in {len(self.array)}-byte array"
        
        bit = 1 << self.bit_index

        if val is OnOff.ON:
            self.array[self.byte_index] |= bit
        else:
            self.array[self.byte_index] &= ~bit
        
        # self.array[self.index] = 1 if val else 0
    
    def __init__(self, byte_index: int, bit_index: int, a: bytearray) -> None:
        super().__init__(initial_state=OnOff.OFF)
        self.byte_index = byte_index
        self.bit_index = bit_index
        self.array = a


class OpenDropFirmware:
    _states: Final[bytearray]
    _last_states: bytearray
    _device: Final[Optional[str]]
    _port: Optional[Serial] = None
    _double_write: Final[bool]
    
    def __init__(self, args: Namespace) -> None:
        self._states = bytearray(self.n_state_bytes)
        self._last_states = bytearray(self.n_state_bytes)
        self._device = args.port
        self._double_write = args.double_write
    
    @abstractmethod
    def indices(self, x: int, y: int) -> tuple[int, int]: # @UnusedVariable
        """
        Returns the byte and bit indices
        """
        ...
    @property
    @abstractmethod
    def n_state_bytes(self) -> int: ...
    
    def make_electrode(self, x: int, y: int) -> Electrode:
        (byte_index, bit_index) = self.indices(x,y)
        return Electrode(byte_index, bit_index, self._states)

    @classmethod    
    def add_args_to(cls, 
                    group: _ArgumentGroup, 
                    parser: ArgumentParser) -> None:
        group.add_argument('-p', '--port',
                           help='''
                           The communication port (e.g., COM5) to use to talk to the board.
                           By default, only the display is run
                           ''')
        vg = group.add_mutually_exclusive_group()
        vg.add_argument('-4.0', action='store_const', const=OpenDropV40, dest='od_version',
                        help="The OpenDrop board uses firmware version 4.0")
        vg.add_argument('-4.1', action='store_const', const=OpenDropV41, dest='od_version',
                        help="The OpenDrop board uses firmware version 4.1")
        # group.add_argument('--yaminon', action='store_true',
        #                    help="Mirror pads on top and bottom of the board.")
        double_write_default = True
        group.add_argument('--double-write', action=BooleanOptionalAction, default=double_write_default,
                           help=f'''
                           Send state array to OpenDrop twice.  
                           Default is {double_write_default}
                           ''')
        parser.set_defaults(od_version=OpenDropV40)
        
    @classmethod
    def make_firmware(cls, args: Namespace) -> OpenDropFirmware:
        t: Callable[[Namespace], OpenDropFirmware] = args.od_version
        return t(args)
    
    def send_states(self, states: bytearray) -> None:
        logger.debug("sending %s", states.hex())
        if self._port is not None:
            self._port.write(states)
            if self._double_write:
                # I'm not sure why, but it seems that nothing happens until the 
                # first byte of the next round gets sent. (Sending 129 bytes works, 
                # but then the next round will use that extra byte.  Sending everything
                # twice seems to do the job.  I'll look into this further.
                self._port.write(states)
    
    def update_state(self, delay: Time) -> None:
        if self._port is None and self._device is not None:
            self._port = Serial(self._device)
        new_states = bytearray(self._states)
        send_first: Optional[bytearray] = None
        if delay > 0:
            # First we send 
            send_first = bytearray(x&y for x,y in zip(self._last_states, new_states))
        elif delay < 0:
            send_first = bytearray(x|y for x,y in zip(self._last_states, new_states))
            delay = -delay
        if send_first is not None:
            self.send_states(send_first)
            logger.debug("Delaying for %s", delay)
            delay.sleep()
        self.send_states(new_states)
        self._last_states = new_states
    
    def stop(self)->None:
        if self._port is not None:
            self._port.close()
            self._port = None

    
class OpenDropV40(OpenDropFirmware):
    @property
    def n_state_bytes(self) -> int:
        return 128
    def indices(self, x:int, y:int)->tuple[int, int]:
        byte_index = x*8+y
        bit_index = 0
        assert byte_index < 128
        return (byte_index, bit_index)

class OpenDropV41(OpenDropFirmware):
    @property
    def n_state_bytes(self) -> int:
        return 32
    def indices(self, x:int, y:int)->tuple[int, int]:
        byte_index = x
        bit_index = y
        return (byte_index, bit_index)



class Board(device.Board):
    _firmware: Final[OpenDropFirmware]
    
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
    
    def _well(self, num: int, transition: TransitionFunc, exit_dir: Dir, gate_loc: XYCoord, exit_pad: Pad,
              inner_locs: Sequence[tuple[int,int]]):
        shape = WellShape(
                    gate_pad_bounds= self._gate_bounds(exit_pad.location),
                    shared_pad_bounds = (self._long_pad_bounds(exit_pad.location),
                                         self._side_pad_bounds(exit_pad.location),
                                         self._big_pad_bounds(exit_pad.location)),
                    reagent_id_circle_radius = 1,
                    reagent_id_circle_center = self._reagent_circle_center(exit_pad.location) 
            )
        gate_electrode = self._firmware.make_electrode(gate_loc.x, gate_loc.y)
        gate = WellGate(self, exit_pad, exit_dir, gate_electrode, neighbors=(0,1))
        pad_neighbors = [[-1,1,2], [-1,0,2], [0, 1]]
        inner_electrodes = tuple(self._firmware.make_electrode(x, y) for x,y in inner_locs)
        shared = tuple(WellPad(self, state=s, neighbors=ns) for s,ns in zip(inner_electrodes, pad_neighbors))
        return Well(number=num,
                    board=self,
                    group=transition,
                    exit_dir=exit_dir,
                    exit_pad=exit_pad,
                    gate=gate,
                    shared_pads = shared,
                    capacity=12*uL,
                    dispensed_volume=2*uL,
                    shape=shape
                    )
    
    def __init__(self, od_firmware : OpenDropFirmware, *,
                 off_on_delay: Time = Time.ZERO) -> None:
        pad_dict = dict[XYCoord, Pad]()
        wells: list[Well] = []
        super().__init__(pads=pad_dict, 
                         wells=wells,
                         orientation=Orientation.NORTH_NEG_EAST_POS,
                         drop_motion_time=500*ms,
                         off_on_delay=off_on_delay)
        self._firmware = od_firmware
        for x in range(1,15):
            for y in range(0,8):
                loc = XYCoord(x, y)
                e = od_firmware.make_electrode(x, y)
                p = Pad(loc, self, e)
                pad_dict[loc] = p
                
        sequences: WellOpSeqDict = {
            (WellState.EXTRACTABLE, WellState.READY): ((2,),(1,2)),
            (WellState.READY, WellState.EXTRACTABLE): ((2,), ()),
            (WellState.READY, WellState.DISPENSED): ((-1,0,1),(-1,),(1,2)),
            (WellState.DISPENSED, WellState.READY): (),
            (WellState.READY, WellState.ABSORBED): ((-1,2),(1,2)),
            (WellState.ABSORBED, WellState.READY): ()
            }
        
        transition = transitions_from(sequences)
        
        def inner_locs(col: int, rows: Sequence[int]) -> Sequence[tuple[int,int]]:
            return [(col, r) for r in rows]
        
        upper_left = self._well(0, transition, Dir.RIGHT, XYCoord(0,0), self.pad_at(1,1), inner_locs(0, (2,1,3)))
        upper_right = self._well(1, transition, Dir.LEFT, XYCoord(15,0), self.pad_at(14,1), inner_locs(15, (2,1,3)))
        lower_left = self._well(2, transition, Dir.RIGHT, XYCoord(0,7), self.pad_at(1,6), inner_locs(0, (5,6,4)))
        lower_right = self._well(3, transition, Dir.LEFT, XYCoord(15,7), self.pad_at(14,6), inner_locs(15, (5,6,4)))
        wells.extend((upper_left, upper_right, lower_left, lower_right))
        
    def update_state(self) -> None:
        self._firmware.update_state(self.off_on_delay)
        super().update_state()
        
    def stop(self)->None:
        self._firmware.stop()
        super().stop()
    
class PlatformTask(PlatformChoiceTask):
    def __init__(self, name: str = "Opendrop",
                 description: Optional[str] = None,
                 *,
                 aliases: Optional[Sequence[str]] = None) -> None:
        super().__init__(name, description, aliases=aliases)
    
    
    def make_board(self, args: Namespace, *, 
                   exerciser: PlatformChoiceExerciser, # @UnusedVariable
                   pipettor: Pipettor) -> Board: # @UnusedVariable
        off_on_delay: Time = args.off_on_delay
        firmware = OpenDropFirmware.make_firmware(args)
        return Board(od_firmware=firmware, off_on_delay=off_on_delay)
        
    def add_args_to(self, 
                     group: _ArgumentGroup, 
                     parser: ArgumentParser,
                     *,
                     exerciser: Exerciser) -> None:
        super().add_args_to(group, parser, exerciser=exerciser)
        OpenDropFirmware.add_args_to(group, parser)
        
        
    def available_wells(self, exerciser:Exerciser) -> Sequence[int]: # @UnusedVariable
        return [0,1,2,3]