import json

EMPTY_CELL = 0
WALL = 1
ENTRY_PORTAL = 2
EXIT_PORTAL = 3


class MazeGenerator(object):
    def __init__(self, maze_file):
        self._mazes = []

        with open(maze_file) as data_file:
            self._mazes = json.load(data_file)

        self._maze_index = 0

    def get_next_maze(self):
        if self._maze_index < len(self._mazes):
            maze = self._mazes[self._maze_index]
            self._maze_index = self._maze_index + 1  # Increment maze index
        else:
            self._maze_index = 0  # Reset maze index
            maze = self._mazes[self._maze_index]

        return maze


class Maze(object):
    def __init__(self, maze):
        self._maze = maze
        self.reset()

    def reset(self):
        self._current_coords = self.get_entry_position()
        self._history = [self._current_coords]

    def get_entry_position(self):
        return Maze.get_portal_position(self._maze, ENTRY_PORTAL)

    def get_exit_position(self):
        return Maze.get_portal_position(self._maze, EXIT_PORTAL)

    @staticmethod
    def get_portal_position(maze, portal_type):
        coords = {'x': -1, 'y': -1}

        for x in range(0, len(maze)):
            for y in range(0, len(maze[x])):
                if maze[y][x] == portal_type:
                    coords = {'x': x, 'y': y}
                    break
            else:
                continue
            break

        return coords

    def get_current_position(self):
        return self._current_coords

    def _set_current_position(self, x, y):
        if self._check_free(x, y):
            self._current_coords = {'x': x, 'y': y}

        self._history.append(self._current_coords)

    def _check_in_maze(self, x, y):
        return x >= 0 and y >= 0 and y < len(self._maze) and x < len(self._maze[y])

    def _check_free(self, x, y):
        return self._check_in_maze(x, y) and self._maze[y][x] != WALL

    def get_neighbours(self):
        neighbours = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]

        for y in range(-1, 2):
            for x in range(-1, 2):
                if self._check_free(self._current_coords['x'] + x, self._current_coords['y'] + y):
                    neighbours[y + 1][x + 1] = self._maze[self._current_coords['y'] + y][self._current_coords['x'] + x]

        return neighbours

    def up(self):
        self._move(0, -1)
        return self._current_coords

    def down(self):
        self._move(0, 1)
        return self._current_coords

    def left(self):
        self._move(-1, 0)
        return self._current_coords

    def right(self):
        self._move(1, 0)
        return self._current_coords

    def _move(self, dx, dy):
        new_coords = {
            'x': self._current_coords['x'] + dx,
            'y': self._current_coords['y'] + dy
        }

        if self._check_in_maze(new_coords['x'], new_coords['y']):
            self._set_current_position(new_coords['x'], new_coords['y'])

    def is_maze_solved(self):
        exit_coords = self.get_exit_position()
        return self._current_coords['x'] == exit_coords['x'] and self._current_coords['y'] == exit_coords['y']

    def get_history(self):
        return self._history
