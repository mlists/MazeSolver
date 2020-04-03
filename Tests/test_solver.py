import timeit
from ..solver import Solver
from ..maze import Maze

values = [
    [1, 1, 1, 1, 1],
    [1, -1, -1, -1, 1],
    [1, 1, 1, -1, 1],
    [-1, -1, 1, -1, 1],
    [1, 1, 1, -1, 1],
]
maze = Maze(values)
entry = [0, 0]
goal = [4, 4]
solver = Solver(maze, entry, goal)

path = solver.execute()

def test_walls():
    """
    Test that the solver has not crossed any walls
    """
    for cell in path:
        assert maze[cell].pathable

def test_path_len():
    """
    Test that the shortest path has been found
    """
    assert len(path) == 13

def test_path():
    """
    Test that the path begins and ends in the correct places
    Test that the path order is correct
    """
    assert path[0] == entry
    assert path[-1] == goal

def test_speed():
    """
    Test that solving a 400 square grid takes < 1s
    """
    values2 = [[1] * 20] * 20
    maze2 = Maze(values2)
    entry2 = [0, 0]
    goal2 = [19, 19]
    solver2 = Solver(maze2, entry2, goal2)
    assert timeit.timeit(solver2.execute, number=10) <= 10

def test_no_path():
    values3 = [
    [1, -1, 1],
    [1, 1, -1],
    [1, 1, 1],
    ]
    maze3 = Maze(values3)
    entry3 = [0, 0]
    goal3 = [2, 2]
    solver3 = Solver(maze3, entry3, goal3)
    assert solver3.execute() == []