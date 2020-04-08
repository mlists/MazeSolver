from functools import partial
import threading
import tkinter as tk

from solver import Solver
from maze import Maze


class SampleApp(tk.Tk):
    """The overall GUI class"""

    GRID_SIZE = 8

    def select(self, x, y, index):
        if self.map[y][x] == 1:
            self.tiles_1d[index].configure(bg="black")
            self.map[y][x] = -1
            # TODO put display code here
        elif self.map[y][x] == -1:
            self.map[y][x] = 1
            self.tiles_1d[index].configure(bg="white")


    def run(self):
        maze = Maze(self.map)
        maze.configure_dimensions(x_right=True, y_up=False)
        entry = [0, 0]
        goal = [self.GRID_SIZE-1, self.GRID_SIZE-1]
        solver = Solver(maze, entry, goal)
        path = solver.execute()
        for tile in path:
            x, y = tile
            # convert to 1d
            index = x * self.GRID_SIZE + y
            self.tiles_1d[index].configure(bg="red")


    def __init__(self):
        tk.Tk.__init__(self)

        # Variable definitions
        self.console_var = tk.StringVar()

        # GUI frame creation
        self.frame = tk.Frame(self)

        # Other GUI creation
        self.console_label = tk.Label(self, textvariable=self.console_var)
        self.run_button = tk.Button(self, text="Run", command=self.run)

        # product selection creation
        self.tiles_1d = []  # create the empty array
        self.tile_text = []
        self.first_selection_index = None
        """
        Unfortunately, tkinter hates 2d arrays, within a new object, button instances duplicate
        this way you can have more than one row of buttons, note that the y-axis is flipped to ensure
        correct display
        """
        for column in range(self.GRID_SIZE):
            for row in range(self.GRID_SIZE):
                index = column * self.GRID_SIZE + row
                self.tile_text.append(tk.StringVar())
                self.tiles_1d.append(
                    tk.Button(
                        self.frame,
                        textvariable=self.tile_text[index],
                        command=partial(self.select, column, row, index),
                        width=3,
                        anchor="w",
                    )
                )
                # circumvent issues with using parameters in command calls using partial function
                self.tiles_1d[index].grid(column=column, row=self.GRID_SIZE - row)
        self.map = []
        for _ in range(self.GRID_SIZE):
            self.map.append([1] * self.GRID_SIZE)

        # GUI positioning
        self.run_button.pack()
        self.frame.pack()
        self.console_label.pack()


app = SampleApp()
app.mainloop()
