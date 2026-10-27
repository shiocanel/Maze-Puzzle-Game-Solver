from enum import Enum


class Direction(Enum):
    UP = -1, 0
    DOWN = 1, 0
    LEFT = 0, -1
    RIGHT = 0, 1

    def move(self, position):
        return (position[0] + self.value[0], position[1] + self.value[1])

    def sideways(self):
        if self == Direction.LEFT or self == Direction.RIGHT:
            return Direction.UP, Direction.DOWN

        return Direction.LEFT, Direction.RIGHT
