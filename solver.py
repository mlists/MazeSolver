from typing import List

class Maze():
    """
    Wrapper class for 2d arrays to convert them to cartesian form and allow easy 2d
    iteration, reusable for many applications outside of this project since it solves
    the machine land array problem due to the unconventional behaviour of ordinary arrays 
    """
    def __init__(self, array_2d: List[List[int]]):
        self.rows = array_2d
        # These are in machine coordinates
        self.current_y = len(self.rows)
        self.current_x = 0
        self.current_item = None

        # Defines the iteration orders, defaults to conventional cartesian
        self.x_right: bool = True
        self.y_up: bool = True

    def __iter__(self):
        return self

    def __next__(self) -> int:
        """
        Iterates through the 2d array in the currently specified order
        """
        pass

    def __getitem__(self, x: int, y: int) -> int:
        """
        Returns the value at the specified x, y coordinate, this will be in conventional
        cartesian form. i.e. with the x coordinate first, right positive and the y
        coordinate second being up positive. The first item in each dimension is at
        index 0, this object supports negative indicies with the direction of the index
        being reversed. This method can also be accessed with normal index notation
        thanks to python magic methods.

        @param
        x: int - The x coordinate to fetch
        y: int - The y coordinate to fetch

        @returns
        The value at the specified coordinates

        @raises
        Will raise an index error if the coordinate is not avaliable
        """
        return
    
    def configure_iteration(self, x_right: bool, y_up: bool) -> None:
        """
        Setup the iteration order of the class, this sticks untill reset. With both
        booleans True the array will loop right and upon completion of a row will move
        up.

        @param
        x_right: bool - If True, the x-axis iterates right
        y_up: bool - If True, the y-axis iterates upwards
        """
        pass

class Solver():
    def __init__(self):
        self.maze = None

    def take_input(self, maze):
        self.maze = maze