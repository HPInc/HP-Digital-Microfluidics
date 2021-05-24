from __future__ import annotations
# import matplotlib
# matplotlib.use('Agg')
from typing import Final, Mapping, Optional
from mpam.device import Board, Pad
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.patches import Rectangle, Circle
from mpam.types import Orientation, XYCoord, OnOff, Reagent, Callback
from matplotlib.text import Annotation
from mpam.drop import Drop
import math
from quantities.dimensions import Volume
from threading import Lock


class PadMonitor(object):
    pad: Final[Pad]
    board_monitor: Final[BoardMonitor]
    square: Final[Rectangle]
    magnet: Final[Optional[Annotation]]
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
        self.center = (ox+0.5*w, oy+0.5*w)
        square = Rectangle(xy=(ox,oy), width=1, height=1,
                           facecolor='white',
                           edgecolor='black')
        self.square = square
        self.note_state(pad.current_state)
        board_monitor.plot.add_patch(square)
        self.capacity = board_monitor.board.drop_size
        
        if pad.magnet is None:
            m = None
        else:
            m = plot.annotate(text='M', xy=(0,0),
                                        xytext=(0.95, 0.05),
                                        xycoords=square,
                                        horizontalalignment='right')
            self.note_magnet_state(OnOff.OFF)
            pad.magnet.on_state_change(lambda _,new: board_monitor.in_display_thread(lambda: self.note_magnet_state(new)))
        self.magnet = m
        
        pad.on_state_change(lambda _,new: board_monitor.in_display_thread(lambda : self.note_state(new)))
        pad.on_drop_change(lambda old,new: board_monitor.in_display_thread(lambda : self.note_drop_change(old, new)))
        
    def note_state(self, state: OnOff) -> None:
        # print(f"{self.pad} now {state}")
        if state:
            self.square.set_linewidth(5)
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
            
    def drop_radius(self, drop: Drop) -> float:
        return 0.45*self.square.get_width()*math.sqrt(drop.volume.ratio(self.capacity))
            
    def note_drop_change(self, old: Optional[Drop], new: Optional[Drop]) -> None:
        print(f"{self.pad}'s drop changed from {old} to {new}")
        if new is not None:
            dm = self.board_monitor.drop_monitor(new)
            circle = dm.shape
            square = self.square
            w = square.get_width()
            x = square.get_x()
            y = square.get_y()
            circle.set_visible(True)
            circle.set_center((x+0.5*w, y+0.5*w))
        if old is not None and not old.exists:
            dm = self.board_monitor.drop_monitor(old)
            dm.shape.set_visible(False)
            del self.board_monitor.drop_map[old]
    
class DropMonitor:
    drop: Final[Drop]
    board_monitor: Final[BoardMonitor]
    shape: Final[Circle]
    
    def __init__(self, drop: Drop, board_monitor: BoardMonitor):
        self.drop = drop
        self.board_monitor = board_monitor
        pad = drop.pad
        pm = board_monitor.pads[pad]
        reagent_color = 'green'
        self.shape= Circle(pm.center, radius=pm.drop_radius(drop),
                           facecolor = reagent_color,
                           edgecolor = 'black',
                           alpha = 0.5,
                           visible=False)
        board_monitor.plot.add_patch(self.shape)
        liquid = drop.liquid
        liquid.on_volume_change(lambda _, new: board_monitor.in_display_thread(lambda: self.note_volume(new)))
        liquid.on_reagent_change(lambda _, new: board_monitor.in_display_thread(lambda: self.note_reagent(new)))
        
    def note_volume(self, _: Volume) -> None:
        pm = self.board_monitor.pads[self.drop.pad]
        self.shape.set_radius(pm.drop_radius(self.drop))

    def note_reagent(self, reagent: Reagent) -> None:
        color = self.board_monitor.reagent_color(reagent)
        self.shape.set_facecolor(color)

        
        
            

class BoardMonitor:
    board: Final[Board]
    pads: Final[Mapping[Pad, PadMonitor]]
    figure: Final[Figure]
    plot: Final[Axes]
    drop_map: Final[dict[Drop, DropMonitor]]
    lock: Final[Lock]
    update_callbacks: Final[list[Callback]]
    
    def __init__(self, board: Board) -> None:
        self.board = board
        self.drop_map = dict[Drop, DropMonitor]()
        self.lock = Lock()
        self.update_callbacks = []
        
        self.figure = pyplot.figure()
        self.plot = self.figure.add_subplot(111, aspect='equal')
        # self.plot.axis('off')
        self.plot.set_xlim(board.min_column, board.max_column+1)
        self.plot.set_ylim(board.min_row, board.max_row+1)
        self.pads = { pad: PadMonitor(pad, self) for pad in board.pad_array.values()}
        self.figure.canvas.draw()
        
    def map_coord(self, xy: XYCoord) -> tuple[float, float]:
        board = self.board
        orientation = board.orientation
        if orientation is Orientation.NORTH_POS_EAST_POS:
            return (xy.x, xy.y)
        elif orientation is Orientation.NORTH_NEG_EAST_POS:
            return (xy.x, board.max_row-xy.y+board.min_row)
        elif orientation is Orientation.NORTH_POS_EAST_NEG:
            return (board.max_column-xy.x+board.min_column, xy.y)
        else:
            return (board.max_column-xy.x+board.min_column,
                    board.max_row-xy.y+board.min_row)
            
    def drop_monitor(self, drop: Drop) -> DropMonitor:
        dm: Optional[DropMonitor] = self.drop_map.get(drop, None)
        if dm is None:
            dm = DropMonitor(drop, self)
            self.drop_map[drop] = dm
        return dm
        
        
    def reagent_color(self, reagent: Reagent):
        return 'green'
    
    def in_display_thread(self, cb: Callback) -> None:
        with self.lock:
            self.update_callbacks.append(cb)
            
    def process_display_updates(self) -> None:
        with self.lock:
            for cb in self.update_callbacks:
                cb()
            