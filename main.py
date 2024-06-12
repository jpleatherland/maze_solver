from window import Window
from maze_structure import (
    Maze
)
    
win = Window(1920, 1080) 
maze = Maze(100, 100, 15, 30, 50, 50, win)
maze.break_entrance_and_exit()
maze.break_walls_r(0,0)
maze.reset_visited()
maze.solve(0,0)
win.wait_for_close()
