from ..maze import Maze

test_grid1 = [
    [12, 13, 14, 15],
    [8, 9, 10, 11],
    [4, 5, 6, 7],
    [0, 1, 2, 3],
]

test_grid2 = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11],
    [12, 13, 14, 15],
]

maze1 = Maze(test_grid1, value_type=int)

maze2 = Maze(test_grid2, value_type=int)


def test_iteration(maze1: Maze = maze1, maze2: Maze = maze2):
    """
    Test iteration in all directions
    """
    maze1.configure_dimensions(x_right=True, y_up=True)
    prev_num = -1
    for num in maze1:
        assert num == prev_num + 1
        prev_num = num

    maze1.configure_dimensions(x_right=False, y_up=False)
    prev_num = 16
    for num in maze1:
        assert num == prev_num - 1
        prev_num = num

    maze2.configure_dimensions(x_right=True, y_up=False)
    prev_num = -1
    for num in maze2:
        assert num == prev_num + 1
        prev_num = num

    maze2.configure_dimensions(x_right=False, y_up=True)
    prev_num = 16
    for num in maze2:
        assert num == prev_num - 1
        prev_num = num

def test_indexing(maze1: Maze = maze1, maze2: Maze = maze2):
    """
    Confirm that getting items works as expected
    """
    maze1.configure_dimensions(x_right=True, y_up=True)
    assert maze1[0, 0] == 0
    maze1.configure_dimensions(x_right=False, y_up=False)
    assert maze1[0, 0] == 15
    maze1.configure_dimensions(x_right=True, y_up=False)
    assert maze1[0, 0] == 12
    maze1.configure_dimensions(x_right=False, y_up=True)
    assert maze1[0, 0] == 3

test_grid3 = [
[1, 1, 1, 1],
[-1, -1, 1, 1],
[-1, -1, 1, 1],
[1, 1, 1, 1],
]

maze3 = Maze(test_grid3)

def test_node(maze = maze3):
    assert maze[0, 0].pathable
    assert maze[0, 0].move_cost == 1
    assert not maze[0, 1].pathable
    assert maze[0, 1].move_cost == None
