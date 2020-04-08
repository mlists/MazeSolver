from functools import partial
import threading
import tkinter as tk

from solver import Solver
from maze import Maze


class SampleApp(tk.Tk):
    """The overall GUI class"""

    GRID_SIZE = 1

    def select(self, x, y):
        if self.choose_entry:
            self.entry = [x, y]
            self.choose_entry = False
            self.wipe_path()
        elif self.choose_goal:
            self.goal = [x, y]
            self.choose_goal = False
            self.wipe_path()
        else:
            if self.map[y][x] == 1:
                self.tile_rows[y][x].configure(bg="black")
                self.map[y][x] = -1
                # TODO put display code here
            elif self.map[y][x] == -1:
                self.map[y][x] = 1
                self.tile_rows[y][x].configure(bg="white")


    def run(self):
        self.wipe_path()
        maze = Maze(self.map)
        maze.configure_dimensions(x_right=True, y_up=False)
        solver = Solver(maze, self.entry, self.goal)
        path = solver.execute()
        for tile in path[1:-1]:
            # colour the path excluding the start and finish
            x, y = tile
            self.tile_rows[y][x].configure(bg="red")
        self.colour_ends()
    
    def wipe_path(self):
        for y, row in enumerate(self.tile_rows):
            for x, tile in enumerate(row):
                if self.map[y][x] == 1:
                    tile.configure(bg="white")
                elif self.map[y][x] == -1:
                    tile.configure(bg="black")
        self.colour_ends()
    
    def colour_ends(self):
        # colour the goal and entry
        ex, ey = self.entry
        self.tile_rows[ey][ex].configure(bg="blue")
        gx, gy = self.goal
        self.tile_rows[gy][gx].configure(bg="yellow")
    
    def new_entry(self):
        self.choose_entry = True
    
    def new_goal(self):
        self.choose_goal =  True

    def __init__(self):
        tk.Tk.__init__(self)

        # Variable definitions
        self.console_var = tk.StringVar()

        # GUI frame creation
        self.frame = tk.Frame(self)

        # Other GUI creation
        self.console_label = tk.Label(self, textvariable=self.console_var)
        self.run_button = tk.Button(self, text="Run", command=self.run)
        self.entry_button = tk.Button(self, text="New Entry", command=self.new_entry)
        self.goal_button = tk.Button(self, text="New Goal", command=self.new_goal)

        self.tile_rows = []
        for row in range(self.GRID_SIZE):
            self.tile_rows.append([])
            for column in range(self.GRID_SIZE):
                self.tile_rows[-1].append(
                    tk.Button(
                        self.frame,
                        command=partial(self.select, column, row),
                        width=3,
                        anchor="w",
                    )
                )
                # circumvent issues with using parameters in command calls using partial function
                self.tile_rows[row][column].grid(column=column, row=self.GRID_SIZE - row)
        # self.tile_rows.reverse()

        self.map = []
        for _ in range(self.GRID_SIZE):
            self.map.append([1] * self.GRID_SIZE)

        self.entry = [0, 0]
        self.goal = [self.GRID_SIZE-1, self.GRID_SIZE-1]

        self.choose_entry = False
        self.choose_goal = False

        # GUI positioning
        self.frame.pack()
        self.run_button.pack()
        self.entry_button.pack()
        self.goal_button.pack()
        self.console_label.pack()


app = SampleApp()
app.mainloop()
