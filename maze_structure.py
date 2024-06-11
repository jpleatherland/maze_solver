class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, point1, point2):
        self.start = (point1.x, point1.y)
        self.end = (point2.x, point2.y)

    def draw(self, canvas, fill_colour):
        canvas.create_line(
            self.start[0], self.start[1], self.end[0], self.end[1], fill=fill_colour, width = 2
        )
