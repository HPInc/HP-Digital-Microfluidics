from matplotlib import pyplot
from matplotlib.patches import Rectangle, Circle
from matplotlib.font_manager import FontProperties
from quantities.SI import uL
import math
from quantities.core import Scalar

# class MonitorThread(Thread):
#     def run(self) -> None:
#         figure = pyplot.figure()
#         plot = figure.add_subplot(111, aspect='equal')
#         plot.set_xlim(0,14)
#         plot.set_ylim(0,7)
#
#         pad = Rectangle((2,2), 1,1, 
#                         facecolor='beige',
#                         edgecolor='black',
#                         )
#         plot.add_patch(pad)
#
#         figure.canvas.draw()
#
#         pyplot.pause(100)        
#
#
# MonitorThread().start()

figure = pyplot.figure()
plot = figure.add_subplot(111, aspect='equal')
plot.set_xlim(0,14)
plot.set_ylim(0,7)
plot.axis('off')

x = 2
y = 2
pad = Rectangle(xy=(x,y), width=1,height=1, 
                facecolor='beige',
                edgecolor='black',
                )


plot.add_patch(pad)
font_size = 'xx-small'
pad_font = FontProperties(size=font_size, weight='normal')
temp = plot.annotate(text="Off", xy=(1,1), 
                     xytext=(0.05,0.05),
                     xycoords=pad,
                     horizontalalignment='left',
                     color='darkred',
                     fontsize=font_size,
                     )
magnet = plot.annotate(text="M", xy=(1,1), 
                     xytext=(0.95,0.05),
                     xycoords=pad,
                     horizontalalignment='right',
                     color='darkslateblue',
                     fontsize=font_size,
                     )

beads = plot.annotate(text="B", xy=(1,1), 
                      xytext=(0.3,0.47),
                      xycoords=pad,
                      horizontalalignment='center',
                      verticalalignment='center',
                      color='darkslateblue',
                      fontsize='x-small',
                      fontweight='bold',
                      visible=False
                      )

w = pad.get_width()
dried = Circle((x+w*.7, y+w*.5), radius=w*.1, color='magenta') 
plot.add_patch(dried)

hole = Circle((x+w*.5, y+w*.8), radius=w*0.05, edgecolor='black')
plot.add_patch(hole)

drop = drops = 0.5*uL.as_unit('drp')
capacity = 1*drop

vol = 1*drop

base_radius = w*0.45
radius = base_radius*math.sqrt(vol.ratio(capacity))

d = Circle((x+w*.5, y+w*.5), radius=radius, 
           facecolor='green',
           edgecolor = 'black',
           alpha=0.5)
plot.add_patch(d)
drop_beads = plot.annotate(text="B", xy=(1,1), 
                           xytext=(0.5,0.47),
                           xycoords=d,
                           horizontalalignment='center',
                           verticalalignment='center',
                           color='darkslateblue',
                           fontsize='x-small',
                           fontweight='bold',
                           visible=True
                           )

figure.canvas.draw()

pyplot.pause(5)

temp.set_text('50C')
temp.set_weight('bold')
temp.set_color('darkorange')

magnet.set_weight('heavy')
magnet.set_color('white')
magnet.set_size('x-small')
magnet.set_bbox({'facecolor': 'dodgerblue', 'pad': 0})

pad.set_linewidth(2)
pad.set_edgecolor('green')

beads.set_visible(True)
drop_beads.set_visible(False)

pyplot.pause(5)

temp.set_text('80C')
temp.set_color('red')

d.set_center((d.get_center()[0]+1, d.get_center()[1]))

# temp.set_fontsize('small')
# pad.set_x(5)
# figure.canvas.draw()

pyplot.pause(100)

# while True: pass

