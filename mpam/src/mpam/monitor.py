from __future__ import annotations
# import matplotlib
# matplotlib.use('Agg')
from typing import Final, Mapping, Optional, Union, Sequence, cast, Callable,\
    ClassVar, MutableMapping
from mpam.device import Board, Pad, Well, WellPad, PadBounds, Heater,\
    HeatingMode, BinaryComponent, WellState
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
from matplotlib import pyplot, gridspec
from matplotlib.patches import Rectangle, Circle, PathPatch, Patch, Wedge
from mpam.types import Orientation, XYCoord, OnOff, Reagent, Callback, Color,\
    ColorAllocator, Liquid, unknown_reagent, waste_reagent
from matplotlib.text import Annotation
from mpam.drop import Drop, DropStatus
import math
from quantities.dimensions import Volume, Time
from threading import RLock, Event
from matplotlib.path import Path
from numbers import Number
from quantities.temperature import abs_C
from quantities.SI import ms, sec
import random
from quantities.timestamp import time_now
from quantities.core import Unit
from matplotlib.artist import Artist
from matplotlib.backend_bases import PickEvent
from matplotlib.legend_handler import HandlerPatch
from matplotlib.legend import Legend
from erk.basic import Count
from erk.stringutils import map_str
from matplotlib.widgets import Button
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec


class PadMonitor(object):
    pad: Final[Pad]
    board_monitor: Final[BoardMonitor]
    square: Final[Rectangle]
    magnet: Final[Optional[Annotation]]
    heater: Final[Optional[Annotation]]
    port: Final[Optional[Patch]]
    origin: Final[tuple[float, float]]
    width: Final[float]
    center: Final[tuple[float, float]]
    capacity: Final[Volume]
    
    
    def __init__(self, pad: Pad, board_monitor: BoardMonitor):
        self.pad = pad
        self.board_monitor = board_monitor
        plot = board_monitor.plot
        
        ox, oy = board_monitor.map_coord(pad.location)
        self.origin = (ox, oy)
        self.width = w = 1
        
        board_monitor._on_board(ox, oy)
        board_monitor._on_board(ox+1, oy+1)
        
        self.center = (ox+0.5*w, oy+0.5*w)
        
        square = Rectangle(xy=(ox,oy), width=1, height=1,
                           facecolor='white' if pad.exists else 'black',
                           edgecolor='black',
                           picker=pad.exists)
        board_monitor.click_id[square] = pad
        self.square = square
        self.note_state(pad.current_state)
        board_monitor.plot.add_patch(square)
        self.capacity = board_monitor.board.drop_size
        
        if pad.exists:
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
                
            if pad.heater is None:
                h = None
            else:
                h = plot.annotate(text='Off', xy=(0,0),
                                  xytext=(0.05, 0.05),
                                  xycoords=square,
                                  horizontalalignment='left',
                                  color='darkred',
                                  fontsize='xx-small')
                key = (pad.heater, f"monitor({pad.location.x},{pad.location.y})", random.random())
                def cb(old,new) -> None:  # @UnusedVariable
                    board_monitor.in_display_thread(lambda : self.note_new_temperature())
                pad.heater.on_temperature_change(cb, key=key) 
                pad.heater.on_target_change(cb, key=key)
            self.heater = h
            if pad.heater is not None:
                self.note_new_temperature()
                
            if pad.extraction_point is not None:
                ep = Circle((ox+0.5*w, oy+0.7*w), radius=0.1*w,
                            facecolor='white',
                            edgecolor='black')
                self.port = ep
                board_monitor.plot.add_patch(ep)
                
            
            pad.on_state_change(lambda _,new: board_monitor.in_display_thread(lambda : self.note_state(new)))
            pad.on_drop_change(lambda old,new: board_monitor.in_display_thread(lambda : self.note_drop_change(old, new)))
            
        
    def note_state(self, state: OnOff) -> None:
        # print(f"{self.pad} now {state}")
        if state:
            self.square.set_linewidth(3)
            self.square.set_edgecolor('green')
        else:
            self.square.set_linewidth(1)
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
            
    heating_mode_colors: Final[ClassVar[Mapping[HeatingMode, str]]] = {
            HeatingMode.OFF: 'darkred',
            HeatingMode.MAINTAINING: 'red',
            HeatingMode.HEATING: 'darkorange',
            HeatingMode.COOLING: 'blue'
            }
            
    def note_new_temperature(self) -> None:
        heater = self.pad.heater
        assert heater is not None
        annotation = self.heater
        assert annotation is not None
        
        temp = heater.current_temperature
        
        mode = heater.mode
        weight = 'normal' if mode is HeatingMode.OFF else 'bold'
        if temp is None:
            text = 'Off' if mode is HeatingMode.OFF or mode is HeatingMode.COOLING else 'On'
        else:
            text = f"{temp.as_number(abs_C):.0f}C"
        color = self.heating_mode_colors[mode]
        
        annotation.set_weight(weight)
        annotation.set_text(text)
        annotation.set_color(color)
            
    def drop_radius(self, drop: Drop) -> float:
        square_width: int = self.square.get_width()
        return 0.45*square_width*math.sqrt(drop.volume.ratio(self.capacity))
            
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
        ncols = math.ceil(math.sqrt(len(handles)))
        self.legend = self.board_monitor.figure.legend(handles=handles,
                                                       title="Reagents",
                                                       ncol=ncols
                                                       # handler_map={Circle: self.HandlerCircle}
                                                       )
        
    class HandlerCircle(HandlerPatch):
        def create_artists(self, legend, orig_handle, 
                           xdescent: float, ydescent: float, 
                           width: float, height: float, 
                           fontsize, trans):  # @UnusedVariable
            center = 0.5*width-0.5*xdescent, 0.5*height-0.5*ydescent
            p = Circle(xy=center, radius=min(width+xdescent, height+ydescent))
            self.update_prop(p, orig_handle, legend)
            p.set_transform(trans)
            return [p]
        
    def changed_reagent(self, old: Optional[Reagent], new: Optional[Reagent]):
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
        liquid = drop.liquid
        liquid.on_volume_change(lambda _, new: board_monitor.in_display_thread(lambda: self.note_volume(new)))
        liquid.on_reagent_change(lambda _, new: board_monitor.in_display_thread(lambda: self.note_reagent(new)))
        
    def note_volume(self, _: Volume) -> None:
        pm = self.board_monitor.pads[self.drop.pad]
        radius = pm.drop_radius(self.drop)
        self.circle.radius = radius

    def note_reagent(self, reagent: Reagent) -> None:
        self.circle.reagent = reagent
        
        
class WellPadMonitor:
    board_monitor: Final[BoardMonitor]
    shapes: Final[Sequence[PathPatch]]

    
    
    def __init__(self, pad: WellPad, board_monitor: BoardMonitor, 
                 bounds: Union[PadBounds, Sequence[PadBounds]],
                 *,
                 well: Well,
                 is_gate: bool) -> None:
        self.board_monitor = board_monitor
        # This is ugly, but I don't see any easier way to do it.
        just_one = isinstance(bounds[0][0], Number)
        if just_one:
            bounds = (cast(PadBounds, bounds),)
        else:
            bounds = cast(Sequence[PadBounds], bounds)
        self.shapes = [ self._make_shape(b, pad, well=well, is_gate=is_gate) for b in bounds ]
        
    
    def _make_shape(self, bounds: PadBounds, pad: WellPad, *, well: Well, is_gate:bool) -> PathPatch:  # @UnusedVariable

        bm = self.board_monitor
        verts = [bm.map_coord(xy) for xy in bounds]
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
        bm.click_id[shape] = pad
        bm.plot.add_patch(shape)
        pad.on_state_change(lambda _,new: bm.in_display_thread(lambda: self.note_state(new)))
        # if not is_gate:
            # well.on_liquid_change(lambda _,new: bm.in_display_thread(lambda: self.note_liquid(new)))
        return shape

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
    gate_monitor: Final[WellPadMonitor]
    shared_pad_monitors: Final[Sequence[WellPadMonitor]]
    reagent_circle: Final[ReagentCircle]
    # reagent_volume_circle: Final[Circle]
    # volume_rectangle: Final[Rectangle]
    volume_description: Final[Annotation]
    reagent_description: Final[Annotation]
    

    
    def __init__(self, well: Well, board_monitor: BoardMonitor) -> None:
        self.well = well
        self.board_monitor = board_monitor
        
        shape = well._shape
        assert shape is not None
        self.gate_monitor = WellPadMonitor(well.gate, board_monitor, shape.gate_pad_bounds, well = well, is_gate = True)
        
        self.shared_pad_monitors = [WellPadMonitor(wp, board_monitor, bounds, well=well, is_gate = False)
                                    for bounds, wp in zip(shape.shared_pad_bounds, well.group.shared_pads)]
        rc_center = board_monitor.map_coord(shape.reagent_id_circle_center)
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
            self.volume_description.set_text(f"{liquid.volume.in_units(units):g}")
            self.volume_description.set_visible(True)
        

            

class BoardMonitor:
    board: Final[Board]
    pads: Final[Mapping[Pad, PadMonitor]]
    wells: Final[Mapping[Well, WellMonitor]]
    figure: Final[Figure]
    plot: Final[Axes]
    # controls: Final[Axes]
    drop_map: Final[dict[Drop, DropMonitor]]
    lock: Final[RLock]
    update_callbacks: Optional[list[Callback]]
    color_allocator: Final[ColorAllocator[Reagent]]
    drop_unit: Final[Unit[Volume]]
    click_id: Final[MutableMapping[Artist, BinaryComponent]]
    close_event: Final[Event]
    legend: Final[ReagentLegend]
    
    left_buttons: Final[tuple[Button, ...]]
    right_buttons: Final[tuple[Button, ...]]
    
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    no_bounds: bool
    
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
    
    def __init__(self, board: Board) -> None:
        self.board = board
        self.drop_map = dict[Drop, DropMonitor]()
        self.lock = RLock()
        self.update_callbacks = None
        self.click_id = {}
        self.close_event = Event()
        
        self.no_bounds = True
        
        self.drop_unit = board.drop_size.as_unit("drops", singular="drop")

        self.figure = pyplot.figure(figsize=(10,8))
        main_grid = GridSpec(2,1, height_ratios = [5,1])
        self.plot = pyplot.subplot(main_grid[0, :])
        # self.controls = pyplot.subplot(main_grid[1, :])
        

        # self.figure,(self.plot,
        #              self.controls) = pyplot.subplots(2,1, figsize=(10,8), 
        #                           gridspec_kw={'height_ratios': [5,1]})
        self.figure.tight_layout
        
        self.plot.axis('off')
        # self.controls.axis('off')
        self.pads = { pad: PadMonitor(pad, self) for pad in board.pad_array.values()}
        self.wells = { well: WellMonitor(well, self) for well in board.wells if well._shape is not None}
        padding = 0.2
        self.plot.set_xlim(self.min_x-padding, self.max_x+padding)
        self.plot.set_ylim(self.min_y-padding, self.max_y+padding)
        reserved_colors = {
                unknown_reagent: Color.find("xkcd:violet"),
                waste_reagent: Color.find("xkcd:black"),
            }
        self.color_allocator = ColorAllocator[Reagent](reserved_colors)
        self.legend = ReagentLegend(self)

        for heater in board.heaters:       
            self.setup_heater_poll(heater) 

        def on_pick(event: PickEvent):
            artist = event.artist
            cpt = self.click_id[artist]
            if cpt.live:
                key = event.mouseevent.key
                print(f"Clicked on {cpt} (modifiers: {key})")
                if key == "control":
                    cpt.schedule(BinaryComponent.Toggle)
                elif key == "shift":
                    if isinstance(cpt, Pad):
                        on_neighbors = [p for p in cpt.all_neighbors if p.current_state]
                        def print_time(_) -> None:
                            # print(f"    Time is {Timestamp.now()}")
                            pass                            
                        def back_on(val: OnOff) -> None:  # @UnusedVariable
                            with board.in_system().batched():
                                print(f"  Turning off {cpt}.  Turning on {map_str(on_neighbors)}.")
                                cpt.schedule(Pad.SetState(OnOff.OFF)) \
                                    .then_call(print_time)
                                for p in on_neighbors:
                                    p.schedule(Pad.SetState(OnOff.ON))
                        with board.in_system().batched():
                            print(f"  Turning on {cpt}.  Turning off {map_str(on_neighbors)}.")
                            cpt.schedule(Pad.SetState(OnOff.ON)) \
                                .then_call(print_time) \
                                .then_call(back_on) 
                            for p in on_neighbors:
                                p.schedule(Pad.SetState(OnOff.OFF))
                else:
                    with board.in_system().batched():
                        for p in board.pad_array.values():
                            if p.live:
                                p.schedule(Pad.SetState(OnOff.ON if cpt is p else OnOff.OFF))
                        for wg in board.well_groups.values():
                            for wp in wg.shared_pads:
                                wp.schedule(Pad.SetState(OnOff.ON if cpt is wp else OnOff.OFF))
                            wg.state = WellState.EXTRACTABLE
                        for w in board.wells:
                            g = w.gate
                            if g.live:
                                g.schedule(Pad.SetState(OnOff.ON if cpt is g else OnOff.OFF))
            else:
                print(f"{cpt} is not live")
            
        self.figure.canvas.mpl_connect('pick_event', on_pick)
        self.figure.canvas.mpl_connect('close_event', lambda _: self.close_event.set())
        
        control_cols_grid = GridSpecFromSubplotSpec(1,3,main_grid[1,:],width_ratios=[1,5,1])
        n_buttons = 4
        left_button_stack = GridSpecFromSubplotSpec(n_buttons, 1, control_cols_grid[0])
        right_button_stack = GridSpecFromSubplotSpec(n_buttons, 1, control_cols_grid[2])

        def make_button(i: int, label: str, stack: GridSpecFromSubplotSpec) -> Button:
            ax = pyplot.subplot(stack[i, 0])
            label = ""
            b = Button(ax, label)
            b.on_clicked(lambda event: print(f"Clicked {label}"))
            b.set_active(False)
            return b
            
        self.left_buttons = tuple(make_button(i, f"Left {i}", left_button_stack)
                                                for i in range(n_buttons))
        self.right_buttons = tuple(make_button(i, f"Right {i}", right_button_stack)
                                                for i in range(n_buttons))

        # for i in range(n_buttons):
        #     ax = pyplot.subplot(left_button_stack[i, 0])
        #     b = Button(ax, f"Left {i}")
        #     ax = pyplot.subplot(right_button_stack[i, 0])
        #     b = Button(ax, f"Right {i}")
        # b = Button(self.controls, "Test")
        
        self.figure.canvas.draw()
        
    def setup_heater_poll(self, heater: Heater) -> None:
        interval = heater.polling_interval
        def do_poll() -> Optional[Time]:
            heater.poll()
            # print(f"Polling {heater}")
            return interval
        self.board.call_after(interval, do_poll, daemon=True)
        
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
                   min_time: Time = 0*sec, 
                   max_time: Optional[Time] = None, 
                   sentinel: Optional[Callable[[], bool]] = None,
                   update_interval: Time = 20*ms):
        now = time_now()
        kill_at = None if max_time is None else now+max_time
        live_through = now+min_time
        pause = update_interval.as_number(sec)
        saw_sentinel: bool = False
        def done() -> bool:
            nonlocal saw_sentinel
            if not saw_sentinel and sentinel is not None:
                saw_sentinel = sentinel()
            now = time_now()
            if now < live_through and not self.close_event.is_set():
                return False
            if kill_at is not None and now > kill_at:
                return True
            return saw_sentinel
            
        while not done():
            self.process_display_updates()
            self.figure.canvas.draw_idle()
            pyplot.pause(pause)
        
            