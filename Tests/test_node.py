from ..maze import Maze, Node

values = [
    [6,7,8],
    [3,4,5],
    [0,1,2],
]

maze = Maze(values)

def test_get_pos(maze=maze):
    """
    Ensures that the nodes localise properly
    """
    maze.configure_dimensions(x_right=True, y_up=True)
    for y in range(len(values) - 1):
        for x in range(len(values[0])):
            assert maze[x, y].get_pos() == [x, y]

    maze.configure_dimensions(x_right=False, y_up=True)
    for y in range(len(values) - 1):
        for x in range(len(values[0])):
            assert maze[x, y].get_pos() == [x, y]

    maze.configure_dimensions(x_right=True, y_up=False)
    for y in range(len(values) - 1):
        for x in range(len(values[0])):
            assert maze[x, y].get_pos() == [x, y]
    
    maze.configure_dimensions(x_right=False, y_up=False)
    for y in range(len(values) - 1):
        for x in range(len(values[0])):
            assert maze[x, y].get_pos() == [x, y]


maze1 = Maze(values)

def test_get_neighbours(maze = maze1):
    # Main case
    maze.configure_dimensions(x_right=True, y_up=True)
    nodes = maze[1, 1].get_neighbours()
    assert nodes[0].move_cost == 1
    assert nodes[1].move_cost == 3
    assert nodes[2].move_cost == 5
    assert nodes[3].move_cost == 7
    # Literal edge case
    maze.configure_dimensions(x_right=False, y_up=False)
    nodes = maze[0, 0].get_neighbours()
    assert nodes[0] is None
    assert nodes[1] is None
    assert nodes[2].move_cost == 7
    assert nodes[3].move_cost == 5