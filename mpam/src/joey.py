from __future__ import annotations
import mpam.device as device
from typing import Optional, Final, Sequence, ClassVar
from mpam.types import OnOff, XYCoord, Orientation, GridRegion, Delayed
from mpam.device import WellGroup, Well, WellOpSeqDict, WellState, PadBounds,\
    HeatingMode, ExtractionPoint, WellShape
from quantities.SI import uL, ms, deg_C, sec
from quantities.temperature import TemperaturePoint, abs_F
from quantities.timestamp import Timestamp, time_now
from quantities.dimensions import Temperature, Time
from quantities.core import DerivedDim
import random

class Electrode:
    index: Final[int]
    array: Final[bytearray]
    
    def set_state(self, val: OnOff) -> None:
        self.array[self.index] = 1 if val else 0
    
    def __init__(self, index: int, a: bytearray) -> None:
        self.index = index
        self.array = a
        
class Pad(device.Pad):
    electrode: Final[Optional[Electrode]]
    def __init__(self, e: Optional[Electrode], loc: XYCoord, board: Board, *, exists: bool):
        super().__init__(loc, board, exists=exists)
        self.electrode = e
        
        if e is None:
            self.set_device_state = lambda _: None
        else:
            real_e = e
            self.set_device_state = lambda v: real_e.set_state(v)
            
class Magnet(device.Magnet):
    def __init__(self, board: Board, *, pads: Sequence[device.Pad]):
        super().__init__(board, pads=pads)
        self.set_device_state = lambda _: None
            
class HeatingRate(DerivedDim['HeatingRate']):
    derived = Temperature.dim()/Time.dim()
    
class WellPad(device.WellPad):
    electrode: Optional[Electrode]
    def __init__(self, e: Optional[Electrode], board: Board):
        super().__init__(board)
        self.electrode = e
        
        if e is None:
            self.set_device_state = lambda _: None
        else:
            real_e = e
            self.set_device_state = lambda v: real_e.set_state(v)

class Heater(device.Heater):
    _last_read_time: Timestamp
    _heating_rate: HeatingRate
    _cooling_rate: HeatingRate
    
    ambient_temperature: ClassVar[TemperaturePoint] = 72*abs_F

    def __init__(self, num: int, board: Board, *, 
                 region: GridRegion) -> None:
        super().__init__(num, board,
                         polling_interval = 200*ms,
                         pads = [board.pad_array[xy] for xy in region])
        self._last_read_time = time_now()
        self._heating_rate = 100*(deg_C/sec).a(HeatingRate)
        self._cooling_rate = 10*(deg_C/sec).a(HeatingRate)
        self._last_reading = self.ambient_temperature
        # It really seems as though we should be able to just override the target setter, but I
        # can't get the compiler (and MyPy) to accept it
        key=(self, "target changed", random.random())
        self.on_target_change(lambda old,new: self._update_temp(old), key=key)  # @UnusedVariable
        
    def _update_temp(self, target: Optional[TemperaturePoint]) -> None:
        now = time_now()
        elapsed = now-self._last_read_time
        mode = self.mode
        if mode is HeatingMode.MAINTAINING:
            return
        assert self._last_reading is not None
        if mode is HeatingMode.OFF and self._last_reading == self.ambient_temperature:
            return
        target = self.target
        delta: Temperature
        if mode is HeatingMode.HEATING:
            delta = (self._heating_rate*elapsed).a(Temperature)
            new_temp = self._last_reading + delta
            if target is not None:
                new_temp = min(new_temp, target)
            self.current_temperature = new_temp
        else:
            delta = (self._cooling_rate*elapsed).a(Temperature)
            new_temp = self._last_reading - delta
            if target is None:
                new_temp = max(new_temp, self.ambient_temperature)
            else:
                new_temp = max(new_temp, target)
            self.current_temperature = new_temp
        self._last_read_time = now
            
    def poll(self) -> Delayed[Optional[TemperaturePoint]]:
        future = Delayed[Optional[TemperaturePoint]]()
        self._update_temp(self.target)
        future.post(self._last_reading)
        return future
    
    
        

class Board(device.Board):
    _states: bytearray
    
    def _rectangle(self, x: float, y: float, outdir: int, width: float, height: float) -> PadBounds:
        return ((x,y), (x+width*outdir,y), (x+width*outdir, y+height), (x, y+height))
    
    def _big_well_pad(self, x: float, y: float, outdir) -> PadBounds:
        x2 = x+0.8*outdir
        x3 = x+2*outdir
        y2 = y+1.75
        y3 = y+2.25
        y4 = y+4
        return ((x,y), (x2,y), (x3,y2), (x3,y3), (x2,y4), (x,y4)) 
    
    
    
    def _well(self, num: int, group: WellGroup, exit_pad: device.Pad):
        epx = exit_pad.location.x
        epy = exit_pad.location.y
        outdir = -1 if epx == 0 else 1
        if outdir == 1:
            epx += 1
        # gate_electrode = Electrode(gate_loc.x, gate_loc.y, self._states)
        
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
                    gate=WellPad(e=None, board=self),
                    capacity=20*uL,
                    dispensed_volume=0.5*uL,
                    shape = shape
                                         # self._rectangle(epx+5*outdir,epy-1.5,outdir,1,4),
                    # shared_pad_bounds = (self._long_pad_bounds(exit_pad.location),
                    #                      self._side_pad_bounds(exit_pad.location),
                    #                      self._big_pad_bounds(exit_pad.location))
                    )
    
    def __init__(self) -> None:
        pad_dict = dict[XYCoord, Pad]()
        wells: list[Well] = []
        magnets: list[Magnet] = []
        heaters: list[Heater] = []
        extraction_points: list[ExtractionPoint] = []
        super().__init__(pads=pad_dict,
                         wells=wells,
                         magnets=magnets,
                         heaters=heaters,
                         extraction_points=extraction_points,
                         orientation=Orientation.NORTH_POS_EAST_POS,
                         drop_motion_time=500*ms)
        self._states = bytearray(128)
        
        dead_region = GridRegion(XYCoord(7,8), width=5, height=3)
        
        for x in range(0,19):
            for y in range(0,19):
                loc = XYCoord(x, y)
                # e = Electrode(x, y, self._states)
                e = None
                exists = loc not in dead_region 
                p = Pad(e, loc, self, exists=exists)
                pad_dict[loc] = p
                
        sequences: WellOpSeqDict = {
            (WellState.EXTRACTABLE, WellState.READY): ((7,6), (7,3,4,5), (7,4,0,1,2)),
            (WellState.READY, WellState.EXTRACTABLE): ((7,3,4,5), (7,6), (8,), ()),
            (WellState.READY, WellState.DISPENSED): ((4,1,-1), (4,1)),
            (WellState.DISPENSED, WellState.READY): ((6,4), (7,4,0,1,2),),
            (WellState.READY, WellState.ABSORBED): ((-1,6,4,1,2,3),),
            (WellState.ABSORBED, WellState.READY): ((7,4,0,1,2),)
            }
        
        left_group = WellGroup("left", self, 
                               tuple(WellPad(None, self) for _ in range(9)),
                               sequences)
        right_group = WellGroup("right", self,
                                tuple(WellPad(None, self) for _ in range(9)),
                                sequences)
        
        
        wells.extend((
            self._well(0, left_group, self.pad_at(0,18)),
            self._well(1, left_group, self.pad_at(0,12)),
            self._well(2, left_group, self.pad_at(0,6)),
            self._well(3, left_group, self.pad_at(0,0)),
            self._well(4, right_group, self.pad_at(18,18)),
            self._well(5, right_group, self.pad_at(18,12)),
            self._well(6, right_group, self.pad_at(18,6)),
            self._well(7, right_group, self.pad_at(18,0)),
            ))
        
        magnets.append(Magnet(self, pads = (self.pad_at(13, 3), self.pad_at(13, 15),)))
        
        heaters.append(Heater(0, self, region=GridRegion(XYCoord(0,12),3,7)))
        heaters.append(Heater(1, self, region=GridRegion(XYCoord(0,0),3,7)))
        heaters.append(Heater(2, self, region=GridRegion(XYCoord(8,12),3,7)))
        heaters.append(Heater(3, self, region=GridRegion(XYCoord(8,0),3,7)))
        heaters.append(Heater(4, self, region=GridRegion(XYCoord(16,12),3,7)))
        heaters.append(Heater(5, self, region=GridRegion(XYCoord(16,0),3,7)))
        
        extraction_points.append(ExtractionPoint(self.pad_at(4,3)))
        extraction_points.append(ExtractionPoint(self.pad_at(4,9)))
        extraction_points.append(ExtractionPoint(self.pad_at(4,15)))
                       
    def update_state(self) -> None:
        pass
        
    def stop(self)->None:
        # if self._port is not None:
        #     self._port.close()
        #     self._port = None
        super().stop()
        
    # def electrode(self, i: int) -> Electrode:
    #     return Electrode(i, self._states)
    