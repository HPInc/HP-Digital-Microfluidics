import tkinter as tk
# from tkinter import ttk 


class TkCanvas(tk.Canvas):
    RECT_WIDTH = 30

    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def __init__(self, parent):
        super().__init__(parent, width=600, height=600)
        self.create_circle = self._create_circle

    def create_board(self, x1=0, x2=0,y1=RECT_WIDTH,y2=RECT_WIDTH, offset_x=0,offset_y=0):
        for i in range(0,19):
            for j in range(0,19):
                rect_id = i*19 + j
                self.create_rectangle(x1+offset_x, x2+offset_x, y1+offset_y, y2+offset_y, fill="white",tags=f"pad_on_board {rect_id}", outline="black")
                x1 += self.RECT_WIDTH
                y1 += self.RECT_WIDTH
            x1 = 0
            y1 = self.RECT_WIDTH
            x2 += self.RECT_WIDTH
            y2 += self.RECT_WIDTH
        
        self.tag_bind("pad_on_board","<Button-1>",self.clicked)

    def get_coord_from_center(self, x,y):
        dx = self.RECT_WIDTH 

        x0 = dx * x
        y0 = dx * y
        x1 = dx * x + dx
        y1 = dx * y + dx

        return {
            "x0": x0,
            "x1": x1,
            "y0": y0,
            "y1": y1
        }

    def conv_coord(self, x, y):
        dx = self.RECT_WIDTH

        xcells = [i for i in range(1,20)]
        for jx, xcell in enumerate(xcells):
            if x > jx*dx and x <= (jx+1)*dx:
                converted_x = xcell
                break
        if x == 0:
            converted_x = xcells[0]

        ycells = [i for i in range(1,20)]
        for jy, ycell in enumerate(ycells):
            if y > jy*dx and y <= (jy+1)*dx:
                converted_y = ycell
                break
        if y == 0:
            converted_y = ycells[0]
        return (converted_x, converted_y)

    def clear(self, object_id):
        self.delete(object_id)

    def clicked(self, *args):
        x = args[0].x
        y = args[0].y
        print("You clicked:",x, y)

    def _from_rgb(self, rgb_tuples):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        r = rgb_tuples[0]
        g = rgb_tuples[1]
        b = rgb_tuples[2]
        return "#%02x%02x%02x" % (int(r*255), int(g*255), int(b*255))


class Root(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.resizable(False, False)
        self.title("Widget Examples")
