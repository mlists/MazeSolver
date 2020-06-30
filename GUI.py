from functools import partial
import threading
import tkinter as tk

from solver import Solver
from maze import Maze


class SampleApp(tk.Tk):
    """The overall GUI class"""

    def select(self, x, y):
        if self.choose_entry:
            # set the entry to the selected square, remove any walls
            self.entry = [x, y]
            self.choose_entry = False
            self.map[y][x] = 1
            self.wipe_path()
        elif self.choose_goal:
            # set the goal to the selected square, remove any walls
            self.goal = [x, y]
            self.choose_goal = False
            self.map[y][x] = 1
            self.wipe_path()
        else:
            selected = [x, y]
            if not(selected == self.entry or selected == self.goal):
                # check that the wall is not being placed on an endpoint
                if self.map[y][x] == 1:
                    self.tile_rows[y][x].configure(bg="black")
                    self.map[y][x] = -1
                elif self.map[y][x] == -1:
                    self.map[y][x] = 1
                    self.tile_rows[y][x].configure(bg="white")

    def run(self):
        self.wipe_path()
        # erase any exising paths
        maze = Maze(self.map)
        maze.configure_dimensions(x_right=True, y_up=False)
        solver = Solver(maze, self.entry, self.goal)
        path = solver.execute()
        # setup the solver for the current maze
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
        self.console_var.set("")
    
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
        """
        Run on startup, creates the GUI elements
        """
        tk.Tk.__init__(self)
        self.title("MazeSolver")

        # Variable definitions
        self.console_var = tk.StringVar()
        self.grid_size = tk.IntVar(master=None, value=10)
        # initialise the gridsize with a default value

        self.define_widgets()

        self.setup_GUI(from_init=True)
    
    def define_widgets(self):
        # GUI frame creation
        self.frame = tk.Frame(self)
        self.button_frame = tk.Frame(self)

        # Other GUI creation
        self.console_label = tk.Label(self, textvariable=self.console_var)
        self.run_button = tk.Button(self.button_frame, text="Solve Maze", command=self.run, width=12, background="red", fg="white")
        self.entry_button = tk.Button(self.button_frame, text="Place Entry", command=self.new_entry, width=12, bg="blue", fg="white")
        self.goal_button = tk.Button(self.button_frame, text="Place Goal", command=self.new_goal, width=12, bg="yellow", fg="black")
        self.help_button = tk.Button(self.button_frame, text="?", command=self.open_help, width=12, fg="black")
        self.new_gridsize = tk.Entry(self.button_frame, textvariable=self.grid_size, width=15)
        self.change_size_button = tk.Button(self.button_frame, text="Change Size", command=self.setup_GUI, width=12)
    
    def destroy_widgets(self):
        self.frame.destroy()
        self.console_label.destroy()
        self.button_frame.destroy()
    
    def open_help(self):
        self.help_window = tk.Toplevel()
        self.help_window.title("Help")
        self.help_window.focus_force()

        self.help_intro = tk.Label(self.help_window, text=
        """
        Welcome to MazeSolver! This program will find the fastest path through your maze.
        Click on the grid to place impassable walls and click on walls to remove them again.
        Below is a key explaining the different types of squares:
        """)
        self.blank_help = tk.Button(self.help_window, width=3, anchor="w", bg="white")
        self.blank_label = tk.Label(self.help_window, text="A pathable square of the maze")

        self.wall_help = tk.Button(self.help_window, width=3, anchor="w", bg="black")
        self.wall_label = tk.Label(self.help_window, text="A wall that cannot be crossed")

        self.path_help = tk.Button(self.help_window, width=3, anchor="w", bg="red")
        self.path_label = tk.Label(self.help_window, text="The shortest path through the maze")

        self.entry_help = tk.Button(self.help_window, width=3, anchor="w", bg="blue")
        self.entry_label = tk.Label(self.help_window, text="The entry to the maze")

        self.exit_help = tk.Button(self.help_window, width=3, anchor="w", bg="yellow")
        self.exit_label = tk.Label(self.help_window, text="The exit from the maze")

        self.help_outro = tk.Label(self.help_window, text=
        """
        In this maze, only horizontal or vertical paths are possible. If no path can be
        found then no red will appear on the maze. The size of the maze can be adjusted by
        entering the desired size (an positive integer) into the textbox and clicking change
        size. Changing the size of the maze will reset it.
        """)

        # position the buttons and labels using a grid
        self.help_intro.grid(column=0, row=0, columnspan=3)
        self.blank_help.grid(column=0, row=1)
        self.blank_label.grid(column=1, row=1)
        self.wall_help.grid(column=0, row=2)
        self.wall_label.grid(column=1, row=2)
        self.path_help.grid(column=0, row=3)
        self.path_label.grid(column=1, row=3)
        self.entry_help.grid(column=0, row=4)
        self.entry_label.grid(column=1, row=4)
        self.exit_help.grid(column=0, row=5)
        self.exit_label.grid(column=1, row=5)
        self.help_outro.grid(column=0, row=6, columnspan=3)


    def setup_GUI(self, from_init=False):
        if int(self.grid_size.get()) > 0:

            if not from_init:
                # possibly not the cleanest way to do this
                # destroys and recreats all widgets so they appear in the correct order
                self.destroy_widgets()
                self.define_widgets()

            self.tile_rows = []
            for row in range(self.grid_size.get()):
                self.tile_rows.append([])
                for column in range(self.grid_size.get()):
                    self.tile_rows[-1].append(
                        tk.Button(
                            self.frame,
                            command=partial(self.select, column, row),
                            width=3,
                            anchor="w",
                        )
                    )
                    # circumvent issues with using parameters in command calls using partial function
                    self.tile_rows[row][column].grid(column=column, row=self.grid_size.get() - row)
            # self.tile_rows.reverse()

            self.map = []
            for _ in range(self.grid_size.get()):
                self.map.append([1] * self.grid_size.get())

            self.entry = [0, 0]
            self.goal = [self.grid_size.get()-1, self.grid_size.get()-1]

            self.choose_entry = False
            self.choose_goal = False

            # Outer frame positioning
            self.frame.pack()
            self.button_frame.pack()
            self.console_label.pack()

            # Positioning of the buttons using columns and rows
            self.run_button.grid(column=0, row=0)
            self.entry_button.grid(column=1, row=0)
            self.goal_button.grid(column=2, row=0)
            self.new_gridsize.grid(column=1, row=1)
            self.help_button.grid(column=2, row=1)
            self.change_size_button.grid(column=0, row=1)
            

            self.colour_ends()
        else:
            self.console_var.set("Grid size must ba a positive integer")


app = SampleApp()
app.mainloop()
