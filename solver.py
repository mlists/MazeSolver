from typing import List, Tuple

class Maze():
    """
    Wrapper class for 2d arrays to convert them to cartesian form and allow easy 2d
    iteration, reusable for many applications outside of this project since it solves
    the machine land array problem due to the unconventional behaviour of ordinary arrays 
    """
    def __init__(self, array_2d: List[List[int]]):
        self.rows = array_2d

        # Defines the iteration orders, defaults to conventional cartesian
        self.x_right: bool = True
        self.y_up: bool = True

        # in machine coordinates
        self.current_x: int = None
        self.current_y: int = None

        self.y_max = len(self.rows) - 1
        self.x_max = len(self.rows[0]) - 1

        self._init_x()
        self._init_y()
    
    def _init_x(self):
        # initilise so first next returns the correct first item from the array
        self.current_x = 0 if self.x_right else self.x_max

    def _init_y(self):
        # initilise so first next returns the correct first item from the array
        self.current_y = self.y_max if self.y_up else 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        """
        Iterates through the 2d array in the currently specified order
        """
        x, y = self.current_x, self.current_y
        self.current_x += 1 if self.x_right else -1

        if not (-1 < x < self.x_max + 1):
            # Finished row, move to next one
            self._init_x()
            self.current_y -= 1 if self.y_up else -1
            x, y = self.current_x, self.current_y
            self.current_x += 1 if self.x_right else -1

            if not (-1 < y < self.y_max + 1):
                # Finished cycling, escape calling loop
                # reinitialise for next cycle
                self._init_x()
                self._init_y()
                raise StopIteration
        
        return self.rows[y][x]


    def __getitem__(self, indices: Tuple[int, int]) -> int:
        """
        Returns the value at the specified x, y coordinate, uses the current dimesion set.
        This object supports negative indicies with the direction of the index
        being reversed. This method can also be accessed with normal index notation
        thanks to python magic methods.

        @param
        indicies: Tuple[x: int, y: int]
            x: int - The x coordinate to fetch
            y: int - The y coordinate to fetch

        @returns
        The value at the specified coordinates

        @raises
        Will raise an index error if the coordinate is not avaliable
        """
        x, y = indices
        # Reverse axis as required
        x = x if self.x_right else self.x_max - x
        y = self.y_max - y if self.y_up else y
        if abs(x) <= self.x_max:
            if abs(y) <= self.y_max:
                return self.rows[y][x]
        raise IndexError
    
    def configure_dimensions(self, x_right: bool, y_up: bool) -> None:
        """
        Setup the iteration order of the class, this sticks untill reset. With both
        booleans True the array will loop right and upon completion of a row will move
        up. Calling this will reset iteration if it is currently running. This also
        affects the origin of the object for the purposes of indexing.

        @param
        x_right: bool - If True, the x-axis iterates right
        y_up: bool - If True, the y-axis iterates upwards
        """
        self.x_right = x_right
        self.y_up = y_up
        self._init_x()
        self._init_y()

class Solver():
    def __init__(self):
        self.maze = None

    def take_input(self, maze):
        self.maze = maze

test_grid = [
[12, 13, 14, 15],
[8, 9, 10, 11],
[4, 5, 6, 7],
[0, 1, 2, 3],
]

maze = Maze(test_grid)
maze.configure_dimensions(x_right=True, y_up=False)

# for num in maze:
#     print(num)
print(maze[0, 0])