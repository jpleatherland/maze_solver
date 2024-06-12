from time import sleep
import random

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

class Cell():
    def __init__(self, tl_point, br_point, window, has_left_wall = True, has_bottom_wall = True, has_right_wall = True, has_top_wall = True, visited = False):
        self.tl_point = tl_point
        self.br_point = br_point
        self.has_left_wall = has_left_wall
        self.has_bottom_wall = has_bottom_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.window = window
        self.visited = visited

    def draw(self, fill_colour):
        bl_point = Point(self.tl_point.x, self.br_point.y)
        tr_point = Point(self.br_point.x, self.tl_point.y)
        if self.has_left_wall:
            left_line = Line(self.tl_point, bl_point)
            left_line.draw(self.window.canvas, fill_colour)
        if self.has_bottom_wall:
            bottom_line = Line(bl_point, self.br_point)
            bottom_line.draw(self.window.canvas, fill_colour)
        if self.has_right_wall:
            right_line = Line(self.br_point, tr_point)
            right_line.draw(self.window.canvas, fill_colour)
        if self.has_top_wall:
            top_line = Line(self.tl_point, tr_point)
            top_line.draw(self.window.canvas, fill_colour)

    def draw_move(self, to_cell, undo=False):
        start_point = Point(((self.tl_point.x + self.br_point.x) / 2), ((self.tl_point.y + self.br_point.y) / 2))
        end_point = Point(((to_cell.tl_point.x + to_cell.br_point.x) / 2), ((to_cell.tl_point.y + to_cell.br_point.y) / 2))
        fill_colour = "gray" if undo else "red"
        route = Line(start_point, end_point)
        route.draw(self.window.canvas, fill_colour)

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.cell_matrix = self.create_cells()
        self.seed = seed

    def create_cells(self):
        # loop through each column 
        # for each row in the column, create a cell
        # each columns collection of rows will have a static x and an increasing y
        # y increases per cell based on maze y1 + (cell_size_y * row index)
        # each row collection will have a static y and an increasing x
         
        cell_matrix = [[] for _ in range(self.num_cols)]
        for col_i in range(0, len(cell_matrix)):
            tl_x = self.x1 + (self.cell_size_x * col_i)
            br_x = tl_x + self.cell_size_x
            for row_i in range(0, self.num_rows): 
                tl_y = self.y1 + (self.cell_size_y * row_i)
                br_y = tl_y + self.cell_size_y
                cell = Cell(Point(tl_x, tl_y), Point(br_x, br_y), self.window)
                cell_matrix[col_i].append(cell)
                cell.draw("black")
                self.animate()
        return cell_matrix

    def animate(self, time = 0.01):
        self.window.redraw()
        sleep(time)

    def break_entrance_and_exit(self):
        entrance = self.cell_matrix[0][0]
        exit = self.cell_matrix[-1][-1]
        entrance.draw("white")
        entrance.has_left_wall = False
        entrance.draw("black")
        exit.draw("white")
        exit.has_right_wall = False
        exit.draw("black")

    def break_walls_r(self, col, row):
        cm = self.cell_matrix
        random.seed(self.seed)
        cm[col][row].visited = True
        while True:
            to_visit = []
            # right
            if col < self.num_cols-1 and not cm[col+1][row].visited:
                to_visit.append(("right", "left", col+1, row)) 
            # left
            if col > 0 and not cm[col-1][row].visited:
                to_visit.append(("left", "right", col-1, row)) 
            #down
            if row < self.num_rows-1 and not cm[col][row+1].visited:
                to_visit.append(("bottom", "top", col, row+1))
            #up
            if row > 0 and not cm[col][row-1].visited:
                to_visit.append(("top", "bottom", col, row-1))
            if not len(to_visit):
                cm[col][row].draw("black")
                break
            next_visit = to_visit[random.randrange(0, len(to_visit))]

            cm[col][row].draw("white")
            setattr(cm[col][row], f"has_{next_visit[0]}_wall", False)
            cm[col][row].draw("black")

            cm[next_visit[2]][next_visit[3]].draw("white")
            setattr(cm[next_visit[2]][next_visit[3]], f"has_{next_visit[1]}_wall", False)
            cm[next_visit[2]][next_visit[3]].draw("black")

            self.animate()
            self.break_walls_r(next_visit[2], next_visit[3])

    def reset_visited(self):
        for col in self.cell_matrix:
            for cell in col:
                cell.visited = False
    
    def solve(self, col, row):
        return self._solve_r(col, row)

    def _solve_r(self, col, row):
        cm = self.cell_matrix
        self.animate(0.05)
        cm[col][row].visited = True
        if col == self.num_cols-1 and row == self.num_rows-1:
            return True

        if not cm[col][row].has_bottom_wall and not cm[col][row+1].visited and not cm[col][row+1].has_top_wall:
            cm[col][row].draw_move(cm[col][row+1])
            if self._solve_r(col, row+1):
                return True
            else:
                cm[col][row].draw_move(cm[col][row+1], undo = True)

        if not cm[col][row].has_left_wall and not cm[col-1][row].visited and not cm[col-1][row].has_right_wall:
            cm[col][row].draw_move(cm[col-1][row])
            if self._solve_r(col-1, row):
                return True
            else:
                cm[col][row].draw_move(cm[col-1][row], undo = True)

        if not cm[col][row].has_top_wall and not cm[col][row-1].visited and not cm[col][row-1].has_bottom_wall:
            cm[col][row].draw_move(cm[col][row-1])
            if self._solve_r(col, row-1):
                return True
            else:
                cm[col][row].draw_move(cm[col][row-1], undo = True)

        if not cm[col][row].has_right_wall and not cm[col+1][row].visited and not cm[col+1][row].has_left_wall:
            cm[col][row].draw_move(cm[col+1][row])
            if self._solve_r(col+1, row):
                return True
            else:
                cm[col][row].draw_move(cm[col+1][row], undo = True)

        return False


