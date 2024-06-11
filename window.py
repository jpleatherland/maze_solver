from tkinter import Tk, BOTH, Canvas

class Window(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()    
        self.root.title("Title")
        self.canvas = Canvas()
        self.canvas.pack()
        self.running = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_colour):
        line.draw(self.canvas, fill_colour)
