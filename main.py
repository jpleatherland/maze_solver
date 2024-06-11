from window import Window
from maze_structure import (
    Point, 
    Line
)
    
win = Window(800, 600) 
point1 = Point(0, 0)
point2 = Point(400, 300)
new_line = Line(point1, point2)
win.draw_line(new_line, "black")
win.redraw()
win.wait_for_close()
