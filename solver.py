from typing import List
from maze import Maze, Node

def find_insterion_index(sorted_array: List, target: object, getter: str) -> int:
    """
    A binary search used to find the index of the lowest number greater than the
    target, i.e. the index at which the object should be inserted

    @param
    sorted_array: the list that you want to search, must be sorted and items should
        be unique
    target: the item you want to find the index for
    getter: the string name of the function that converts the objects of the array
        into numbers that can be compared
    
    @returns
    The index of at which to insert the object
    """
    low = 0
    high = len(sorted_array)
    found = False
    while low < high and found is False:
        mid = (low + high) // 2
        # fetch and then call the get functions
        value = getattr(sorted_array[mid], getter)
        target_value = getattr(target, getter) + 1
        if value < target_value:
            low = mid
        elif value > target_value:
            high = mid
        else:
            found = True
    while found:
        # there should not duplicate data but this handles it anyway
        # varient of a linear search
        mid += 1
        value = getattr(sorted_array[mid], getter)()
        target_value = getattr(target, getter)() + 1
        if value != target_value:
            found = False
    return mid


class Solver:
    def __init__(self):
        self.maze = None

        # Open is the list (used as a queue) of all cells that need to be
        # checked, initialised to the maze entry in take input.
        # Cells are added to open if they are adjacent to the currently
        # inspected cell and not in either open or closed.
        self.open: List[Node] = None
        # A list containing all of the cells we have already checked
        self.closed: List[Node] = None

        self.entry = None
        self.goal = None

    def take_input(self, maze):
        self.maze = maze

    def find_distance(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        """
        Return the Manhattan distance between two points in the maze. This is
        the difference between the two points in both axis and is used in the
        pathfinding algorithm

        @param
        p1: Tuple[int, int] the first point you want distance between
        p2: Tuple[int, int] the second point you want distance between
        """
        x1, y1 = p1
        x2, y2 = p2
        return abs(x2 - x1) + abs(y2 - y1)

    def execute(self) -> None:
        """
        The main solver loop, runs constantly until a solution is found or all
        options are exhausted i.e. the maze is unsolveable
        """
        while self.open[0] is not self.goal:
            current = self.open.pop(0)
            self.closed.append(current)
            for neighbour in current.get_neighbours():
                cost = (
                    neighbour.best_pathing_score
                    + current.movement_cost
                    + neighbour.movement_cost
                )
                if neighbour in self.open and cost < neighbour.best_pathing_score:
                    self.open.remove(neighbour)
                if neighbour in self.closed and cost < neighbour.best_pathing_score:
                    self.closed.remove(neighbour)
                if neighbour not in self.open and neighbour not in self.closed:
                    neighbour.best_pathing_score = cost
                    find_insterion_index(self.open, neighbour, "best_pathing_score")
                    self.open.insert()
                    neighbour.parent = current
