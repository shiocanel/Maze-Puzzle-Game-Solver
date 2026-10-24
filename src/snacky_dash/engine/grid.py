from .tile import Tile


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0])

    def is_inside(self, position):
        return (
            position[0] >= 0
            and position[1] >= 0
            and position[0] < self.rows
            and position[1] < self.columns
        )

    def is_wall(self, position):
        if not self.is_inside(position):
            return True

        x, y = position
        return self.grid[x][y] == Tile.WALL.value
