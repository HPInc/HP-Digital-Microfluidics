from __future__ import annotations

from abc import ABC, abstractmethod
import math
from numbers import Number
import random
from re import Pattern, Match
import re
from threading import RLock, Event, Lock
from typing import Final, Mapping, Optional, Union, Sequence, cast, Callable, \
    ClassVar, MutableMapping, Any
import logging

import clipboard
from matplotlib import pyplot
from matplotlib.artist import Artist
from matplotlib.axes._axes import Axes
from matplotlib.backend_bases import PickEvent, KeyEvent
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec, SubplotSpec
from matplotlib.legend import Legend
from matplotlib.legend_handler import HandlerPatch
from matplotlib.patches import Rectangle, Circle, PathPatch, Patch, Wedge
from matplotlib.path import Path
from matplotlib.text import Annotation
from matplotlib.widgets import Button, TextBox

from erk.basic import Count
from mpam import paths
from mpam.device import Board, Pad, Well, WellPad, PadBounds, \
    TemperatureMode, BinaryComponent, ChangeJournal, DropLoc, WellGate,\
    TempControllable, TemperatureControl, WellShape
from mpam.drop import Drop, DropStatus
from mpam.types import Orientation, XYCoord, OnOff, Reagent, Callback, Color, \
    ColorAllocator, Liquid, unknown_reagent, waste_reagent
from quantities.SI import ms, sec
from quantities.core import Unit, UEorSeq
from quantities.dimensions import Volume, Time
from quantities.temperature import abs_C, TemperaturePoint
from quantities.timestamp import time_now, Timestamp
from weakref import WeakKeyDictionary
from erk.stringutils import match_width, conj_str
import traceback
from argparse import _ArgumentGroup, ArgumentParser,\
    BooleanOptionalAction
from erk.config import ConfigParam
from mpam.cmd_line import time_arg
import tkinter

logger = logging.getLogger(__name__)

class Config:
    highlight_reservations: Final = ConfigParam(False)
    trace_clicks: Final = ConfigParam(False)
    initial_delay: Final = ConfigParam(0*ms)
    hold_display: Final = ConfigParam[Optional[Time]](0*ms)
    min_time: Final = ConfigParam[Optional[Time]](0*ms)
    max_time: Final = ConfigParam[Optional[Time]](None)
    update_interval: Final = ConfigParam(20*ms)
    use_display: Final = ConfigParam(True)
    

class ClickableMonitor(ABC):
    component: Final[BinaryComponent]
    patches: Final[list[Patch]]
    _neighbors: Optional[Sequence[ClickableMonitor]] = None

    @property
    def current_state(self) -> OnOff:
        return self.component.current_state

    @property
    def live(self) -> bool:
        return self.component.live

    @property
    def neighbors(self) -> Sequence[ClickableMonitor]:
        val = self._neighbors
        if val is None:
            val = self._neighbors = self.list_neighbors()
        return val

    def __init__(self, component: BinaryComponent) -> None:
        self.component = component
        self.patches = []

    def __repr__(self) -> str:
        return f"#<Monitor for {self.component}>"

    @abstractmethod
    def list_neighbors(self) -> Sequence[ClickableMonitor]: ...

    @abstractmethod
    def current_drop(self) -> Optional[Drop]: ...

    # @abstractmethod
    # def fix_drop(self, drop: Optional[Drop], liquid: Liquid) -> None: ... # @UnusedVariable

    @abstractmethod
    def holds_drop(self) -> bool: ...

    def draw(self, width: int, color: str) -> None:
        for patch in self.patches:
            patch.set_linewidth(width)
            patch.set_edgecolor(color)



    def note_state(self, state: OnOff) -> None:
        self.draw(3 if state else 1, "green" if state else "black")

    def preview_state(self, state: OnOff) -> None:
        self.draw(5, "green" if state else "black")


class TCMonitor:
    annotation: Final[Annotation]
    tc: Final[TemperatureControl]
    
    heating_mode_colors: Final[Mapping[TemperatureMode, str]] = {
            TemperatureMode.AMBIENT: 'darkred',
            TemperatureMode.HOT: 'red',
            TemperatureMode.HEATING: 'darkorange',
            TemperatureMode.WARMING: 'darkorange',
            TemperatureMode.CHILLING: 'cornflowerblue',
            TemperatureMode.COOLING: 'cornflowerblue',
            TemperatureMode.COLD: 'blue'
            }
    
    
    def __init__(self, tc: TemperatureControl, 
                 *, where: TempControllable,
                 patch: Patch,
                 board_monitor: BoardMonitor) -> None:
        plot = board_monitor.plot
        self.tc = tc
        self.annotation = plot.annotate(text='Off', xy=(0,0),
                                        xytext=(0.05, 0.05),
                                        xycoords=patch,
                                        horizontalalignment='left',
                                        color='darkred',
                                        fontsize='xx-small')
        key = (tc, f"monitor({where})", random.random())
        def cb(old: Optional[TemperaturePoint], new: Optional[TemperaturePoint]) -> None:  # @UnusedVariable
            board_monitor.in_display_thread(lambda : self.note_new_temperature())
        tc.on_temperature_change(cb, key=key)
        tc.on_target_change(cb, key=key)
        self.note_new_temperature()
        
    @classmethod
    def for_loc(cls, where: TempControllable, *,
                patch: Patch,
                board_monitor: BoardMonitor) -> Optional[TCMonitor]:
        tc = where.temperature_control
        if tc is None:
            return None
        return TCMonitor(tc, where=where, patch=patch, board_monitor=board_monitor)

    def note_new_temperature(self) -> None:
        tc = self.tc
        temp = tc.current_temperature

        mode = tc.mode
        weight = 'normal' if mode is TemperatureMode.AMBIENT else 'bold'
        if temp is None:
            text = 'Off' if mode.is_passive else 'On'
        else:
            text = f"{temp.as_number(abs_C):.0f}C"
        color = self.heating_mode_colors[mode]

        annotation = self.annotation
        annotation.set_weight(weight)
        annotation.set_text(text)
        annotation.set_color(color)



PadOrGate = Union[Pad, WellGate]


# import matplotlib
# matplotlib.use('TkAgg')
class PadMonitor(ClickableMonitor):
    pad: Final[PadOrGate]
    board_monitor: Final[BoardMonitor]
    square: Final[Rectangle]
    magnet: Final[Optional[Annotation]]
    tc_monitor: Final[Optional[TCMonitor]]
    port: Final[Optional[Patch]]
    origin: Final[tuple[float, float]]
    width: Final[float]
    center: Final[tuple[float, float]]
    capacity: Final[Volume]


    def __init__(self, pad: PadOrGate, board_monitor: BoardMonitor):
        super().__init__(pad)
        self.pad = pad
        self.board_monitor = board_monitor
        plot = board_monitor.plot

        ox, oy = board_monitor.map_coord(pad.location)
        self.origin = (ox, oy)
        self.width = w = 1

        board_monitor._on_board(ox, oy)
        board_monitor._on_board(ox+1, oy+1)

        self.center = (ox+0.5*w, oy+0.5*w)

        pad_exists = isinstance(pad, WellGate) or pad.exists

        square = Rectangle(xy=(ox,oy), width=1, height=1,
                           facecolor='white' if pad_exists else 'black',
                           edgecolor='black',
                           picker=pad_exists)
        self.patches.append(square)
        board_monitor.click_id[square] = self
        self.square = square
        self.note_state(pad.current_state)
        board_monitor.plot.add_patch(square)
        self.capacity = board_monitor.board.drop_size

        if isinstance(pad, Pad) and pad.exists:
            if pad.magnet is None:
                m = None
            else:
                m = plot.annotate(text='M', xy=(0,0),
                                            xytext=(0.95, 0.05),
                                            xycoords=square,
                                            horizontalalignment='right')
                pad.magnet.on_state_change(lambda _,new: board_monitor.in_display_thread(lambda: self.note_magnet_state(new)))
            self.magnet = m
            if pad.magnet is not None:
                self.note_magnet_state(OnOff.OFF)

            self.tc_monitor = TCMonitor.for_loc(pad, patch=square, board_monitor=board_monitor)

            if pad.extraction_point is not None:
                ep = Circle((ox+0.5*w, oy+0.7*w), radius=0.1*w,
                            facecolor='white',
                            edgecolor='black')
                self.port = ep
                board_monitor.plot.add_patch(ep)

        pad.on_state_change(lambda _,new: board_monitor.in_display_thread(lambda : self.note_state(new)))
        pad.on_drop_change(lambda old,new: board_monitor.in_display_thread(lambda : self.note_drop_change(old, new)))
        if isinstance(pad, Pad) and Config.highlight_reservations(): # pad can be Pad or Gate
            pad.on_reserved_change(lambda _,new: board_monitor.in_display_thread(lambda : self.note_reserved(new)))


    def list_neighbors(self)->Sequence[ClickableMonitor]:
        m = self.board_monitor
        pad = self.pad
        def find_monitor(dl: DropLoc) -> ClickableMonitor:
            if isinstance(dl, Pad) or isinstance(dl, WellGate):
                return m.pads[dl]
            assert isinstance(dl, WellPad)
            return m.wells[dl.well].shared_pad_monitors[dl.index]
        neighbors: list[ClickableMonitor] = [find_monitor(p) for p in pad.neighbors_for_blob]
        return neighbors

    def current_drop(self) -> Optional[Drop]:
        if self.current_state is OnOff.OFF:
            return None
        drop = self.pad.drop
        assert drop is not None, f"{self.pad} on but has no drop"
        return drop

    def holds_drop(self)->bool:
        return True

    # def fix_drop(self, drop:Optional[Drop], liquid:Liquid)->None:
    #     if drop is None:
    #         Drop(self.pad, liquid)
    #         self.pad.board.change_journal.note_delivery(self.pad, liquid)
    #     else:
    #         drop.liquid.volume = liquid.volume
    #         drop.liquid.reagent = liquid.reagent
    #         drop.status = DropStatus.ON_BOARD
    #         drop.pad = self.pad

    def note_state(self, state: OnOff) -> None:
        # logger.debug(f"{self.pad} now {state}")
        if state:
            self.square.set_linewidth(3)
            self.square.set_edgecolor('green')
        else:
            self.square.set_linewidth(1)
            self.square.set_edgecolor('black')

    def note_reserved(self, reserved: bool) -> None:
        # logger.debug("{} is {}reserved".format(self.pad, "" if reserved else "not "))
        if reserved:
            self.square.set_facecolor('lightgray')
        else:
            self.square.set_facecolor('white')

    def preview_state(self, state: OnOff) -> None:
        # logger.debug(f"{self.pad} will be {state}")
        if state:
            self.square.set_linewidth(5)
            self.square.set_edgecolor('green')
        else:
            self.square.set_linewidth(5)
            self.square.set_edgecolor('black')

    def note_magnet_state(self, state: OnOff) -> None:
        magnet = self.magnet
        assert magnet is not None
        if state:
            magnet.set_fontsize('x-small')
            magnet.set_color('white')
            magnet.set_weight('heavy')
            magnet.set_bbox({'facecolor': 'dodgerblue', 'pad': 0})
        else:
            magnet.set_fontsize('xx-small')
            magnet.set_color('darkslateblue')
            magnet.set_weight('normal')
            magnet.set_bbox(None)


    def drop_radius(self, drop: Drop) -> float:
        square_width: int = self.square.get_width()
        return 0.45*square_width*math.sqrt(drop.display_volume.ratio(self.capacity))

    def note_drop_change(self, old: Optional[Drop], new: Optional[Drop]) -> None:
        # print(f"{self.pad}'s drop changed from {old} to {new}")
        if new is not None:
            square = self.square
            w = square.get_width()
            x = square.get_x()
            y = square.get_y()
            dm = self.board_monitor.drop_monitor(new)
            dm.circle.center = (x+0.5*w, y+0.5*w)
            dm.circle.visible = True
        if old is not None and old.status is not DropStatus.ON_BOARD:
            dm = self.board_monitor.drop_monitor(old)
            dm.circle.visible = False
            if old.status is not DropStatus.IN_MIX:
                del self.board_monitor.drop_map[old]


class ReagentLegend:
    board_monitor: Final[BoardMonitor]
    contents: Final[dict[Reagent, Patch]]
    contents_count: Final[Count[Reagent]]
    mixtures_count: Final[Count[Reagent]]
    pending_redraw: bool
    legend: Optional[Legend] = None

    def __init__(self, board_monitor: BoardMonitor) -> None:
        self.board_monitor = board_monitor
        self.contents = {}
        self.contents_count = Count[Reagent]()
        self.mixtures_count = Count[Reagent]()
        self.pending_redraw = False
        self.redraw()

    def redraw(self) -> None:
        self.pending_redraw = False
        on_board = [(r.name,p) for r,p in self.contents.items()]
        on_board.sort(key=lambda t:t[0])
        handles = [t[1] for t in on_board]
        old = self.legend
        if old is not None:
            old.remove()
        if len(handles) > 0:
            ncols = math.ceil(math.sqrt(len(handles)))
            self.legend = self.board_monitor.figure.legend(handles=handles,
                                                           title="Reagents",
                                                           ncol=ncols
                                                           # handler_map={Circle: self.HandlerCircle}
                                                           )
        else:
            self.legend = None

    class HandlerCircle(HandlerPatch):
        def create_artists(self, legend: Any, orig_handle: Any,
                           xdescent: float, ydescent: float,
                           width: float, height: float,
                           fontsize: float, trans: Any) -> Sequence[Circle]:  # @UnusedVariable
            center = 0.5*width-0.5*xdescent, 0.5*height-0.5*ydescent
            p = Circle(xy=center, radius=min(width+xdescent, height+ydescent))
            self.update_prop(p, orig_handle, legend)
            p.set_transform(trans)
            return [p]

    def changed_reagent(self, old: Optional[Reagent], new: Optional[Reagent]) -> None:
        need_redraw: bool = False
        mc = self.mixtures_count
        cc = self.contents_count
        if new is not None:
            if mc.inc(new) == 1:
                for r,_ in new.mixture:
                    if cc.inc(r) == 1:
                        color = self.board_monitor.reagent_color(r)
                        key = Circle((0,0),
                                     facecolor=color.rgba,
                                     edgecolor="black",
                                     alpha=0.5,
                                     label=r.name)
                        self.contents[r] = key
                        need_redraw = True
        if old is not None:
            if mc.dec(old) == 0:
                for r,_ in old.mixture:
                    if cc.dec(r) == 0:
                        del self.contents[r]
                        need_redraw = True
        if need_redraw and not self.pending_redraw:
            self.pending_redraw = True
            self.board_monitor.in_display_thread(lambda: self.redraw())



class ReagentCircle:
    board_monitor: Final[BoardMonitor]
    _center: tuple[float,float]
    _radius: float
    _reagent: Optional[Reagent]
    _visible: bool
    slices: Final[list[Wedge]]
    alpha: Final[float]

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, val: bool) -> None:
        if val != self.visible:
            self._visible = val
            for s in self.slices:
                s.set_visible(val)
            if val:
                self.board_monitor.legend.changed_reagent(None, self._reagent)
            else:
                self.board_monitor.legend.changed_reagent(self._reagent, None)

    @property
    def center(self) -> tuple[float,float]:
        return self._center

    @center.setter
    def center(self, val: tuple[float,float]) -> None:
        self._center = val
        for s in self.slices:
            s.set_center(val)

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, val: float) -> None:
        self._radius = val
        for s in self.slices:
            s.set_radius(val)

    @property
    def reagent(self) -> Optional[Reagent]:
        return self._reagent

    @reagent.setter
    def reagent(self, val: Optional[Reagent]) -> None:
        if val is self._reagent:
            return
        if self.visible:
            self.board_monitor.legend.changed_reagent(self.reagent, val)
        self._reagent = val
        slices = self.slices
        if len(slices) == 1 and val is not None and val.is_pure:
            # If we've got a whole circle and we want a whole circle, we can just change the color
            color = self.board_monitor.reagent_color(val)
            slices[0].set_facecolor(color.rgba)
            return
        for s in slices:
            s.set_visible(False)
            s.remove()
        slices.clear()
        bm = self.board_monitor
        plot = bm.plot
        center = self.center
        radius = self.radius
        alpha = self.alpha
        visible = self.visible
        if val is None:
            s = Wedge(center, radius, 0, 360,
                      facecolor = "white",
                      edgecolor = 'black',
                      alpha = alpha,
                      visible = visible)
        else:
            start = 0.0
            for r,f in val.mixture:
                portion = f*360.0
                end = start+portion
                color = bm.reagent_color(r)
                s = Wedge(center, radius, start, end,
                          facecolor = color.rgba,
                          edgecolor = 'black',
                          alpha = alpha,
                          visible = visible)
                slices.append(s)
                plot.add_patch(s)
                start = end


    def __init__(self, reagent: Optional[Reagent], *,
                 center: tuple[float,float],
                 radius: float,
                 board_monitor: BoardMonitor,
                 alpha: float = 0.5,
                 visible: bool = False):
        self.board_monitor = board_monitor
        self.slices = []
        self._visible = visible
        self._center = center
        self._radius = radius
        self.alpha = alpha
        self._reagent = None
        self.reagent = reagent



class DropMonitor:
    drop: Final[Drop]
    board_monitor: Final[BoardMonitor]
    circle: Final[ReagentCircle]

    def __init__(self, drop: Drop, board_monitor: BoardMonitor):
        self.drop = drop
        self.board_monitor = board_monitor

        drop = self.drop
        pm = board_monitor.pads[drop.pad]
        self.circle = ReagentCircle(drop.reagent,
                                    center=pm.center,
                                    radius=pm.drop_radius(drop),
                                    board_monitor=board_monitor)
        liquid = drop._display_liquid
        liquid.on_volume_change(lambda _, new: board_monitor.in_display_thread(lambda: self.note_volume(new)))
        liquid.on_reagent_change(lambda _, new: board_monitor.in_display_thread(lambda: self.note_reagent(new)))

    def note_volume(self, _: Volume) -> None:
        pm = self.board_monitor.pads[self.drop.pad]
        radius = pm.drop_radius(self.drop)
        self.circle.radius = radius

    def note_reagent(self, reagent: Reagent) -> None:
        self.circle.reagent = reagent


class WellPadMonitor(ClickableMonitor):
    board_monitor: Final[BoardMonitor]
    shapes: Final[Sequence[PathPatch]]
    pad: Final[WellPad]

    def __init__(self, pad: WellPad, board_monitor: BoardMonitor,
                 bounds: Union[PadBounds, Sequence[PadBounds]],
                 *,
                 well: Well,
                 is_gate: bool,
                 well_shape: WellShape) -> None:
        super().__init__(pad)
        self.board_monitor = board_monitor
        self.pad = pad
        # This is ugly, but I don't see any easier way to do it.
        just_one = isinstance(bounds[0][0], Number)
        if just_one:
            bounds = (cast(PadBounds, bounds),)
        else:
            bounds = cast(Sequence[PadBounds], bounds)
        self.shapes = [ self._make_shape(b, pad, well=well, is_gate=is_gate, well_shape=well_shape) for b in bounds ]
        self.patches.extend(self.shapes)


    def _make_shape(self, bounds: PadBounds, pad: WellPad, *, 
                    well: Well, is_gate:bool, well_shape: WellShape) -> PathPatch:  # @UnusedVariable

        bm = self.board_monitor
        verts = [bm.map_coord(well_shape.for_well(well, xy)) for xy in bounds]
        verts.append(verts[0])
        for v in verts:
            bm._on_board(v[0], v[1])
        path = Path(verts)
        shape = PathPatch(path,
                          facecolor='white',
                          edgecolor='black',
                          # alpha = 0.5,
                          picker=True
                          )
        bm.click_id[shape] = self
        bm.plot.add_patch(shape)
        pad.on_state_change(lambda _,new: bm.in_display_thread(lambda: self.note_state(new)))
        # if not is_gate:
            # well.on_liquid_change(lambda _,new: bm.in_display_thread(lambda: self.note_liquid(new)))
        return shape

    def list_neighbors(self)->Sequence[ClickableMonitor]:
        if self.pad.is_gate:
            return [self.board_monitor.pads[self.pad.well.exit_pad]]
        else:
            return []

    def current_drop(self)->Optional[Drop]:
        if not self.pad.is_gate:
            return None
        if self.current_state is OnOff.OFF:
            return None
        well = self.pad.well
        drop = Drop(well.exit_pad, Liquid(well.reagent, well.dispensed_volume), status=DropStatus.IN_WELL)
        return drop

    def holds_drop(self)->bool:
        return self.pad.is_gate

    # def fix_drop(self, drop:Optional[Drop], liquid:Liquid)->None:
    #     assert isinstance(self, WellPadMonitor)
    #     well = self.pad.loc
    #     assert isinstance(well, Well)
    #     if drop is not None:
    #         drop.status = DropStatus.IN_WELL
    #         drop.pad.drop = None
    #         well.transfer_in(liquid)

    def note_state(self, state: OnOff) -> None:
        # print(f"{self.pad} now {state}")
        for shape in self.shapes:
            shape.set_linewidth(3 if state else 1)
            shape.set_edgecolor('green' if state else 'black')

    def note_liquid(self, liquid: Optional[Liquid]) -> None:
        for shape in self.shapes:
            if liquid is None:
                shape.set_facecolor('white')
            else:
                shape.set_facecolor(self.board_monitor.reagent_color(liquid.reagent).rgba)


class WellMonitor:
    well: Final[Well]
    board_monitor: Final[BoardMonitor]
    gate_monitor: Final[PadMonitor]
    shared_pad_monitors: Final[Sequence[WellPadMonitor]]
    reagent_circle: Final[ReagentCircle]
    # reagent_volume_circle: Final[Circle]
    # volume_rectangle: Final[Rectangle]
    volume_description: Final[Annotation]
    reagent_description: Final[Annotation]
    _tc_monitor_box: Final[Rectangle]
    tc_monitor: Final[Optional[TCMonitor]]
    
    



    def __init__(self, well: Well, board_monitor: BoardMonitor) -> None:
        self.well = well
        self.board_monitor = board_monitor

        shape = well._shape
        assert shape is not None
        self.gate_monitor = PadMonitor(well.gate, board_monitor)

        shared_pads = well.shared_pads

        self.shared_pad_monitors = [WellPadMonitor(wp, board_monitor, bounds, well=well, is_gate = False, well_shape=shape)
                                    for bounds, wp in zip(shape.shared_pad_bounds, shared_pads)]
        rc_center = board_monitor.map_coord(shape.for_well(well, shape.reagent_id_circle_center))
        rc_radius = shape.reagent_id_circle_radius
        board_monitor._on_board(rc_center[0]-rc_radius, rc_center[1]-rc_radius)
        board_monitor._on_board(rc_center[0]+rc_radius, rc_center[1]+rc_radius)
        board_monitor._on_board(rc_center[0]+rc_radius, rc_center[1]-rc_radius)
        board_monitor._on_board(rc_center[0]-rc_radius, rc_center[1]+rc_radius)
        rc = Circle(rc_center, radius = shape.reagent_id_circle_radius,
                    edgecolor='black',
                    facecolor='white',
                    alpha=0.5)
        board_monitor.plot.add_patch(rc)
        self.reagent_circle = ReagentCircle(None,
                                            center = rc_center,
                                            radius = rc_radius,
                                            board_monitor = board_monitor,
                                            visible = True)
        well.on_liquid_change(lambda _,new:
                              board_monitor.in_display_thread(lambda: self.note_liquid(new)))
        rd = board_monitor.plot.annotate(text='Reagent goes here', xy=(0,0),
                                         xytext=(0.5, -0.1),
                                         xycoords=rc,
                                         horizontalalignment='center',
                                         verticalalignment='top',
                                         fontsize='x-small',
                                         visible=False)
        vd = board_monitor.plot.annotate(text='volume goes here', xy=(0,0),
                                         xytext=(0.5, 1.1),
                                         xycoords=rc,
                                         horizontalalignment='center',
                                         verticalalignment='bottom',
                                         fontsize='x-small',
                                         visible=False)
        self.reagent_description = rd
        self.volume_description = vd
        tc_monitor_side = 1.4*shape.reagent_id_circle_radius
        self._tc_monitor_box = Rectangle(xy=(rc_center[0]-tc_monitor_side/2, rc_center[1]-tc_monitor_side/2),
                                         width=tc_monitor_side,
                                         height=tc_monitor_side,
                                         facecolor="white",
                                         edgecolor=None,
                                         visible=True)
        board_monitor.plot.add_patch(self._tc_monitor_box)
        self.tc_monitor = TCMonitor.for_loc(well, patch=self._tc_monitor_box, board_monitor=board_monitor)
        


    def note_liquid(self, liquid: Optional[Liquid]) -> None:
        if liquid is None:
            self.reagent_circle.reagent = None
            self.reagent_description.set_visible(False)
            self.volume_description.set_visible(False)
        else:
            self.reagent_circle.reagent = liquid.reagent
            # self.reagent_volume_circle.set_facecolor(self.board_monitor.reagent_color(liquid.reagent).rgba)
            # fraction: float = liquid.volume.ratio(self.well.capacity)
            # height = 2*fraction*self.reagent_circle.get_radius()
            # self.volume_rectangle.set_height(height)
            # self.reagent_volume_circle.set_clip_path(self.volume_rectangle)
            # self.content_description.set_text(str(liquid))
            units=self.board_monitor.drop_unit
            self.reagent_description.set_text(f"{liquid.reagent}")
            self.reagent_description.set_visible(True)
            self.volume_description.set_text(f"{liquid.volume.in_units(units):tf}")
            self.volume_description.set_visible(True)

class ClickHandler:
    monitor: Final[BoardMonitor]
    lock: Final[Lock]
    scheduled: bool

    changes: Final[set[ClickableMonitor]]


    def __init__(self, monitor: BoardMonitor) -> None:
        self.monitor = monitor
        self.lock = Lock()
        self.scheduled = False

        self.changes = set()

    # called while locked
    def prepare(self, target: ClickableMonitor) -> bool:
        changes = self.changes

        state = target.current_state

        if target in changes:
            changes.remove(target)
            target.note_state(state)
            return False
        else:
            changes.add(target)
            target.preview_state(~state)
            return True

    def run(self) -> None:
        with self.lock:
            with self.monitor.board.system.batched():
                for p in self.changes:
                    new_state = ~p.current_state
                    p.component.schedule(BinaryComponent.SetState(new_state))
            self.changes.clear()
            self.scheduled = False

    def process_shift_click(self, target: ClickableMonitor, *, with_control: bool) -> None:
        assert isinstance(target, PadMonitor) or isinstance(target, WellPadMonitor)
        pad = target.pad
        change_journal = ChangeJournal()
        monitor = self.monitor
        volume: Volume
        reagent: Reagent
        if with_control:
            max_volume: Volume
            if (blob := pad.blob) is not None:
                max_volume = blob.total_volume
                if (well := blob.well) is not None:
                    max_volume += well.volume
            elif isinstance(pad, WellPad) and not pad.is_gate:
                max_volume = pad.well.volume
            else:
                max_volume = Volume.ZERO
            volume = min(pad.board.drop_size, max_volume)
            if volume > Volume.ZERO:
                change_journal.note_removal(pad, volume)
        else:
            reagent = monitor.interactive_reagent
            volume = monitor.interactive_volume
            change_journal.note_delivery(pad, Liquid(reagent, volume))
        change_journal.process_changes()
        pad.board.print_blobs()


    def process_click(self, target: ClickableMonitor, *, with_control: bool, with_shift: bool) -> None:
        with self.lock:
            if with_shift:
                self.process_shift_click(target, with_control=with_control)
                return

            selecting = self.prepare(target)

            # For some reason, when debugging, it often misses the control.
            # with_control = True

            if not with_control and target.current_state is OnOff.OFF:
                changes = self.changes
                for p in target.neighbors:
                    if p.current_state is OnOff.ON:
                        if selecting:
                            changes.add(p)
                            p.preview_state(OnOff.OFF)
                        elif p in changes and not any(n in changes for n in p.neighbors):
                            changes.remove(p)
                            p.note_state(OnOff.ON)
            if not self.scheduled:
                self.scheduled = True
                self.monitor.board.before_tick(lambda: self.run())


class InputBox(TextBox):
    history: Final[list[str]]
    history_pos: int

    def __init__(self, ax: Axes, label: str, initial: str='',
                 color: Any ='.95', hovercolor: Any ='1', label_pad: float =.01) -> None:
        super().__init__(ax, label, initial=initial, color=color, hovercolor=hovercolor, label_pad=label_pad)
        self.history = []
        self.history_pos = 0

    def add_to_history(self, text: str) -> None:
        self.history.append(text)
        self.history_pos = len(self.history)

    def _reset_val(self, text: str) -> None:
        e: bool = super().eventson
        self.eventson = False
        self.set_val(text)
        self.cursor_index = len(text)
        self.eventson = e

    def _keypress(self, event: KeyEvent) -> None:
        if self.ignore(event):
            return
        key: str = event.key
        # if len(key) > 1:
        #     print(f"Pressed '{key}'")
        if key == "up" and self.history_pos > 0:
            if len(self.text) > 0:
                if self.history_pos == len(self.history):
                    self.history.append(self.text)
                elif self.text != self.history[self.history_pos]:
                    self.history[self.history_pos] = self.text
            self.history_pos -= 1
            t = self.history[self.history_pos]
            self._reset_val(t)
            # print(f"Up pressed: '{t}'")
            return
        if key == "down" and self.history_pos < len(self.history)-1:
            if self.text != self.history[self.history_pos]:
                self.history[self.history_pos] = self.text
            self.history_pos += 1
            t = self.history[self.history_pos]
            self._reset_val(t)
            # print(f"Down pressed: '{t}'")
            return
        if key == "ctrl+c":
            t = self.text
            if len(t) > 0:
                # print(f"Copy pressed: {t}")
                clipboard.copy(t)
            return
        if key == "ctrl+x":
            t = self.text
            if len(t) > 0:
                # print(f"Copy pressed: {t}")
                clipboard.copy(t)
                self._reset_val("")
                self.history_pos = len(self.history)
            return
        if key == "ctrl+v":
            t = clipboard.paste()
            if len(t) > 0:
                # print(f"Paste pressed: {t}")
                ct = self.text
                ci = self.cursor_index
                new = ct[:ci]+t+ct[ci:]
                self._reset_val(new)
                self.cursor_index += len(t)
            return
        TextBox._keypress(self, event)
        
class NonBlockingDialog:
    root: Final[tkinter.Tk]
    window: Final[tkinter.Toplevel]
    def __init__(self, root: tkinter.Tk, *, 
                 message: Optional[str],
                 buttons: Sequence[str],
                 on_click: Callable[[str], Any],
                 title: str = "User Action Required") -> None:
        self.root = root
        self.on_click: Final = on_click
        self.window = tkinter.Toplevel(root)
        self.window.title(title)  # this line sets the window's title
        self.window.attributes('-topmost', 1)

        title_font = tkinter.font.Font(size=14, weight="bold")
        title_label = tkinter.Label(self.window, text=title, font=title_font)
        title_label.pack()
        
        tkinter.Frame(self.window, height=2, bg="black").pack(fill='x')

        if message is not None:        
            label = tkinter.Label(self.window, text=message, wraplength=200)
            label.pack()

        for button_text in buttons:
            button = tkinter.Button(self.window, text=button_text, command=lambda: self.button_clicked(button_text))
            button.pack(pady=5)
            
        self.window.update_idletasks()  # update window size
        width = max(self.window.winfo_width(), len(title) * 8)  # adjust width to title        
        x = root.winfo_rootx() + (root.winfo_width() - self.window.winfo_width()) // 2
        y = root.winfo_rooty() + (root.winfo_height() - self.window.winfo_height()) // 2
        self.window.geometry(f"{width}x{self.window.winfo_height()}+{x}+{y}")  # adjust width and position

    def button_clicked(self, text: str) -> None:
        (self.on_click)(text)
        self.window.destroy()
        

class BoardMonitor:
    board: Final[Board]
    pads: Final[Mapping[DropLoc, PadMonitor]]
    wells: Final[Mapping[Well, WellMonitor]]
    figure: Final[Figure]
    plot: Final[Axes]
    # controls: Final[Axes]
    drop_map: Final[WeakKeyDictionary[Drop, DropMonitor]]
    lock: Final[RLock]
    update_callbacks: Optional[list[Callback]]
    color_allocator: Final[ColorAllocator[Reagent]]
    drop_unit: Final[Unit[Volume]]
    click_id: Final[MutableMapping[Artist, ClickableMonitor]]
    close_event: Final[Event]
    legend: Final[ReagentLegend]
    click_handler: Final[ClickHandler]
    interactive_reagent: Reagent = unknown_reagent
    interactive_volume: Volume
    # config_params: Final[ConfigParams]
    last_clicked: Optional[BinaryComponent] = None

    _control_widgets: Final[Any]

    # left_buttons: Final[tuple[Button, ...]]
    # right_buttons: Final[tuple[Button, ...]]

    min_x: float
    max_x: float
    min_y: float
    max_y: float
    no_bounds: bool

    modifiers: ClassVar[Mapping[Optional[str], tuple[bool,bool]]] = {
            None: (False, False),
            "control": (True, False),
            "shift": (False, True),
            "shift+control": (True, True),
            "shift+ctrl": (True, True),
            "ctrl+shift": (True, True)
        }


    def _on_board(self, x: float, y: float) -> None:
        if self.no_bounds:
            self.min_x = self.max_x = x
            self.min_y = self.max_y = y
            self.no_bounds = False
        else:
            self.min_x = min(x, self.min_x)
            self.max_x = max(x, self.max_x)
            self.min_y = min(y, self.min_y)
            self.max_y = max(y, self.max_y)

    def __init__(self, board: Board, *,
                 # cmd_line_args: Optional[Namespace] = None,
                 # from_code: Optional[Mapping[str, Any]] = None,
                 control_setup: Optional[Callable[[BoardMonitor, SubplotSpec], Any]] = None,
                 control_fraction: Optional[float] = None) -> None:
        # print(f"Creating {self}.")
        self.board = board
        # self.config_params = ConfigParams(defaults = self.default_cmd_line_args,
        #                                   cmd_line = cmd_line_args,
        #                                   from_code = from_code)
        self.interactive_volume = board.drop_size
        self.drop_map = WeakKeyDictionary[Drop, DropMonitor]()
        self.lock = RLock()
        self.update_callbacks = None
        self.click_id = {}
        self.close_event = Event()
        self.click_handler = ClickHandler(self)

        self.no_bounds = True

        self.drop_unit = board.drop_size.as_unit("drops", singular="drop")
        if control_fraction is None:
            control_fraction = 0.15

        # self.figure = pyplot.figure(figsize=(10,8), constrained_layout=True)
        self.figure = pyplot.figure(figsize=(10,8))
        self.figure.canvas.mpl_disconnect(self.figure.canvas.manager.key_press_handler_id)
        main_grid = GridSpec(2,1, height_ratios = [1-control_fraction, control_fraction])
        self.plot = pyplot.subplot(main_grid[0, :])
        # self.controls = pyplot.subplot(main_grid[1, :])


        # self.figure,(self.plot,
        #              self.controls) = pyplot.subplots(2,1, figsize=(10,8),
        #                           gridspec_kw={'height_ratios': [5,1]})
        # self.figure.tight_layout()

        self.plot.axis('off')
        # self.controls.axis('off')
        self.pads = { pad: PadMonitor(pad, self) for pad in board.pad_array.values()}
        self.wells = { well: WellMonitor(well, self) for well in board.wells if well._shape is not None}
        for w in board.wells:
            self.pads[w.gate] = self.wells[w].gate_monitor
        padding = 0.2
        self.plot.set_xlim(self.min_x-padding, self.max_x+padding)
        self.plot.set_ylim(self.min_y-padding, self.max_y+padding)
        reserved_colors = {
                unknown_reagent: Color.find("xkcd:violet"),
                waste_reagent: Color.find("xkcd:black"),
            }
        self.color_allocator = ColorAllocator[Reagent](initial_reservations=reserved_colors)
        self.legend = ReagentLegend(self)

        # for heater in board.temperature_controls:
        #     self.setup_heater_poll(heater)

        def on_pick(event: PickEvent) -> None:
            artist = event.artist
            target = self.click_id[artist]
            if target.live:
                key = event.mouseevent.key
                with_control, with_shift = self.modifiers[key]
                # with_control = key == "control" or key == "ctrl+shift"
                # with_shift = key == "shift" or key == "ctrl+shift"
                if Config.trace_clicks():
                    print(f"Clicked on {target} (modifiers: {key})")
                # print(f"  Monitor is {self}")
                self.last_clicked = target.component
                self.click_handler.process_click(target,
                                                 with_control=with_control,
                                                 with_shift=with_shift)
            else:
                print(f"{target} is not live")

        self.figure.canvas.mpl_connect('pick_event', on_pick)
        self.figure.canvas.mpl_connect('close_event', lambda _: self.close_event.set())


        control_subplot: SubplotSpec = main_grid[1,:]

        control_widgets = None if control_setup is None else control_setup(self, control_subplot)
        if control_widgets is None:
            control_widgets = self.default_control_widgets(control_subplot)

        self._control_widgets = control_widgets



        self.figure.canvas.draw()
        
    @classmethod
    def fmt_time(self, t: Optional[Time], *,
                 units: Optional[UEorSeq[Time]] = None,
                 on_None: str = "unspecified") -> str:
        from mpam.exerciser import Exerciser
        return Exerciser.fmt_time(t, units=units, on_None=on_None)

    @classmethod
    def add_args_to(cls, group: _ArgumentGroup,
                         parser: ArgumentParser) -> None: # @UnusedVariable
        Config.initial_delay.add_arg_to(group, '--initial-delay', type=time_arg, metavar='TIME',
                                        default_desc = lambda t: cls.fmt_time(t),
                           help=f'''
                           The amount of time to wait before running the task.
                           ''')
        Config.hold_display.add_arg_to(group, '--hold-display-for', type=time_arg, metavar='TIME',
                                       default_desc = lambda t: cls.fmt_time(t, on_None="to wait forever"),
                           help="The minimum amount of time to leave the display up after the task has finished")
        Config.min_time.add_arg_to(group, '--min-time', type=time_arg, metavar='TIME',
                                   default_desc = lambda t: cls.fmt_time(t, on_None="to wait forever"),
                           help="The minimum amount of time to leave the display up, even if the task has finished")
        Config.max_time.add_arg_to(group, '--max-time', type=time_arg, metavar='TIME',
                                   default_desc = lambda t: cls.fmt_time(t, on_None="no limit"),
                           help="The maximum amount of time to leave the display up, even if the task hasn't finished")
        Config.use_display.add_arg_to(group, '-nd', '--no-display', action='store_false', dest='use_display',
                                      default_desc = lambda b: f"to {'' if b else 'not '} use the on-screen display",
                            help='Run the task without the on-screen display')
        Config.update_interval.add_arg_to(group, '--update-interval', type=time_arg, metavar='TIME', 
                                          default_desc = lambda t: cls.fmt_time(t, units=ms),
                           help="The maximum amount of time between display updates.")
        Config.highlight_reservations.add_arg_to(group, '--highlight-reservations', action=BooleanOptionalAction,
                                                 help="Highlight reserved pads on the display.")
        Config.trace_clicks.add_arg_to(group, '--trace-clicks', action=BooleanOptionalAction,
                                       help="Trace clicks to console.")


    def label(self, text: str, spec: SubplotSpec,
              *,
              fontsize: Optional[Any] = None,
              xy: tuple[float, float] = (0,0.5),
              frameon: bool = False,
              xycoords: str = "axes fraction",
              va: str ="center",
              **kwds: Mapping[str, Any]) -> Annotation:

        ax = self.figure.add_subplot(spec, frameon=frameon, **kwds)
        ax.axis('off')
        a = ax.annotate(text, xy=xy, xycoords=xycoords, va=va, **kwds)
        if fontsize is not None:
            a.set_fontsize(fontsize)
        return a

    def group(self, spec: SubplotSpec, *,
              title: Optional[str] = None,
              fontsize: Any = "x-small",
              facecolor: Optional[Any] = "white",
              edgecolor: Optional[Any] = "black") -> tuple[SubplotSpec, Any]:
        ax = self.figure.add_subplot(spec, frameon=False)
        ax.axis('off')
        border = Rectangle(xy=(0,00.01), width=0.99, height=0.99,
                           facecolor=facecolor, edgecolor=edgecolor)
        ax.add_patch(border)
        if title is None:
            grid = GridSpecFromSubplotSpec(3,3,spec, height_ratios=[1,100,1], width_ratios=[1,100,1])
            return (grid[1,1], (border,))
        else:
            grid = GridSpecFromSubplotSpec(4,3,spec, height_ratios=[1,2,100,1], width_ratios=[1,100,1])
            # self.figure.add_subplot(grid[2,1]).add_patch(Rectangle(xy=(0,0), width=1, height=1))
            tlabel = self.label(title, grid[1,0:], fontsize=fontsize)
            return (grid[2,1], (border, tlabel))



    def clock_widgets(self, spec: SubplotSpec) -> Any:
        clock = self.board.system.clock

        whole, group = self.group(spec, title="Clock:")
        grid = GridSpecFromSubplotSpec(1,5, whole, width_ratios=[1,1,1,1,0.5])
        fig = self.figure



        # label = self.label("Clock:", grid[0,0:], fontsize="x-small")

        def pr_label() -> str:
            return "Pause" if clock.running else "Run"
        pause_run = Button(fig.add_subplot(grid[0,0]), pr_label())
        pause_run.label.set_fontsize("small")
        def toggle_running(event: Any) -> None: # @UnusedVariable
            if clock.running:
                clock.pause()
            else:
                clock.start()
        pause_run.on_clicked(toggle_running)
        def update_pr_label() -> None:
            pause_run.label.set_text(pr_label())
        def pr_cb(old: bool, new: bool) -> None: # @UnusedVariable
            self.in_display_thread(lambda: update_pr_label())
        clock.on_state_change(pr_cb)

        step = Button(fig.add_subplot(grid[0,1]), "Step")
        if clock.running:
            step.set_active(False)
        step.label.set_fontsize("small")
        def update_step_active() -> None:
            step.set_active(not clock.running)
        def step_cb(old: bool, new: bool) -> None: # @UnusedVariable
            self.in_display_thread(lambda: update_step_active())
        clock.on_state_change(step_cb)
        def do_step(event: Any) -> None: # @UnusedVariable
            assert not clock.running
            self.board.after_tick(lambda: clock.pause())
            clock.start()
        step.on_clicked(do_step)

        speed = TextBox(fig.add_subplot(grid[0,3]),
                        "Tick:",
                        initial=f"{clock.update_interval.as_number(ms):g}",
                        label_pad = 0.2)
        speed.label.set_fontsize("small")
        def update_speed(new: Time) -> None:
            speed.set_val(f"{new.as_number(ms):g}")
        def interval_cb(old: Time, new: Time) -> None:   # @UnusedVariable
            self.in_display_thread(lambda: update_speed(new))
        def new_speed(s: str) -> None:
            ns = int(s)*ms
            logger.info(f"Setting tick to {ns}")
            clock.update_interval=int(s)*ms
        clock.on_interval_change(interval_cb)
        speed.on_submit(new_speed)
        units = self.label("ms", grid[0,4], fontsize="small")


        return (group, pause_run, step, speed, units)

    def path_widgets(self, spec: SubplotSpec) -> Any:
        grid = GridSpecFromSubplotSpec(1, 2, spec, width_ratios = [5,1])
        fig = self.figure
        text = TextBox(fig.add_subplot(grid[0,0]), "Path:",
                       # label_pad = 0.2
                       )
        text.label.set_fontsize("small")

        apply = Button(fig.add_subplot(grid[0,1]), "Do it")

        cmd_re: Pattern = re.compile(" *(\\d+) *, *(\\d+) *: *")
        def on_press(event: Event) -> None: # @UnusedVariable
            spec = text.text
            m: Optional[Match[str]] = cmd_re.match(spec)
            if m is None:
                raise ValueError(f"Path specification must begin with 'x,y:'.  Was '{spec}'.")
            x,y = int(m.group(1)), int(m.group(2))
            spec = spec[m.end():]
            board = self.board
            start_pad = board.pad_at(x, y)
            (path, end_pad, path_len) = paths.Path.from_spec(spec, start=start_pad) # @UnusedVariable
            text.set_val(f"{end_pad.column}, {end_pad.row}: ")
            print(f"Executing '{text.text}'")
            drop = start_pad.drop
            if drop is None:
                (paths.Path.appear_at(start_pad, board=board)+path).schedule()
            else:
                path.schedule_for(drop)
        apply.on_clicked(on_press)

        return (text, apply)

    def dmf_lang_widgets(self, spec: SubplotSpec) -> Any:
        grid = GridSpecFromSubplotSpec(1, 2, spec, width_ratios = [5,1])
        fig = self.figure
        text = InputBox(fig.add_subplot(grid[0,0]), "Expr:",
                       # label_pad = 0.2
                       )
        text.label.set_fontsize("small")

        apply = Button(fig.add_subplot(grid[0,1]), "Do it")

        from mpam.interpreter import DMLInterpreter
        interp = DMLInterpreter(board=self.board, cache_val_as="last")
        def on_press(event: KeyEvent) -> None: # @UnusedVariable
            expr = text.text.strip()
            if len(expr) > 0:
                text.add_to_history(expr)
                try:
                    interp.eval_and_print(expr)
                    text.set_val("")
                except RuntimeError as ex:
                    header = f"Exception caught evaluating '{expr}':"
                    print(header)
                    print(match_width(header, repeating="-"))
                    traceback.print_exception(type(ex), ex, ex.__traceback__)

        apply.on_clicked(on_press)
        text.on_submit(on_press)

        return (text, apply)


    def default_control_widgets(self, spec: SubplotSpec) -> Any:
        grid = GridSpecFromSubplotSpec(1,2, spec, width_ratios=[1,1])
        clock = self.clock_widgets(grid[0,0])
        # path = self.path_widgets(grid[0,1])
        cmd = self.dmf_lang_widgets(grid[0,1])
        return (clock, cmd)

    # def setup_heater_poll(self, heater: Heater) -> None:
    #     interval = heater.polling_interval
    #     def do_poll() -> Optional[Time]:
    #         heater.poll()
    #         # print(f"Polling {heater}")
    #         return interval
    #     self.board.call_after(interval, do_poll, daemon=True)

    def map_coord(self, xy: Union[XYCoord, tuple[float,float]]) -> tuple[float, float]:
        board = self.board
        orientation = board.orientation
        if isinstance(xy, XYCoord):
            x: float = xy.x
            y: float = xy.y
        else:
            x,y = xy

        if orientation is Orientation.NORTH_POS_EAST_POS:
            return (x, y)
        elif orientation is Orientation.NORTH_NEG_EAST_POS:
            return (x, board.max_row-y+board.min_row)
        elif orientation is Orientation.NORTH_POS_EAST_NEG:
            return (board.max_column-x+board.min_column, y)
        else:
            return (board.max_column-x+board.min_column,
                    board.max_row-y+board.min_row)

    def drop_monitor(self, drop: Drop) -> DropMonitor:
        dm: Optional[DropMonitor] = self.drop_map.get(drop, None)
        if dm is None:
            dm = DropMonitor(drop, self)
            self.drop_map[drop] = dm
        return dm

    def reserve_color(self, reagent: Reagent, color: Color) -> None:
        with self.lock:
            self.color_allocator.reserve_color(reagent, color)

    def reagent_color(self, reagent: Reagent) -> Color:
        with self.lock:
            return self.color_allocator.get_color(reagent)
        
    def prompt_user(self, *,
                    message: str,
                    on_click: Callable[[str], None],
                    buttons: Sequence[str]) -> None:
        def open_dialog_box() -> None:
            root = self.figure.canvas._tkcanvas.master
            NonBlockingDialog(root, message=message, on_click=on_click, buttons=buttons)
        self.in_display_thread(open_dialog_box)

    def in_display_thread(self, cb: Callback) -> None:
        with self.lock:
            cbs = self.update_callbacks
            if cbs is None:
                self.update_callbacks = [cb]
            else:
                cbs.append(cb)

    def process_display_updates(self) -> None:
        cbs = self.update_callbacks
        if cbs is not None:
            with self.lock:
                self.update_callbacks = None
            for cb in cbs:
                cb()

    def keep_alive(self, *,
                   sentinel: Optional[Callable[[], bool]] = None,
                   ) -> None:
        min_time = Config.min_time()
        max_time = Config.max_time()
        update_interval = Config.update_interval()
        hold_display_for = Config.hold_display()
        now = time_now()
        kill_at = None if max_time is None else now+max_time
        live_through = None if min_time is None else now+min_time
        pause = update_interval.as_number(sec)
        saw_sentinel: bool = False
        time_desc = ""
        def fmt_timestamp(ts: Timestamp) -> str:
            return ts.strftime(fmt="%Y-%m-%d_%H:%M:%S")
        if min_time is None or hold_display_for is None:
            time_desc = "until the user closes the window"
        else:
            options = list[str]()
            time_desc = "until the task ends"
            if min_time > 0 and live_through is not None:
                options.append(f"for at least {min_time.in_HMS():.0} (until {fmt_timestamp(live_through)}), even if the task has completed")
            if hold_display_for > 0:
                options.append(f"for at least {hold_display_for.in_HMS():.0} after the task completes")
            if options:
                time_desc = f"{conj_str(options)}"
        if max_time is not None and kill_at is not None:
            time_desc += f", but no longer than {max_time.in_HMS():.0} (until {fmt_timestamp(kill_at)}), even if the task hasn't completed"
        if time_desc:
            logger.info(f"The display will stay up {time_desc}")
        def done() -> bool:
            nonlocal saw_sentinel, live_through
            just_ended = False
            if not saw_sentinel and sentinel is not None:
                saw_sentinel = sentinel()
                if saw_sentinel and hold_display_for is not None:
                    just_ended = True
            now = time_now()
            if just_ended and hold_display_for is not None:
                logger.info("Task completed")
                hold_end = now+hold_display_for
                if hold_display_for > 0 and live_through is not None and live_through < hold_end:
                    live_through = hold_end
                    logger.info(f"The display will stay up at least until {fmt_timestamp(live_through)}")
            if (live_through is None or now < live_through) and not self.close_event.is_set():
                return False
            if kill_at is not None and now > kill_at:
                return True
            return saw_sentinel

        while not done():
            self.process_display_updates()
            self.figure.canvas.draw_idle()
            pyplot.pause(pause)
        logger.info("Closing display")
            
