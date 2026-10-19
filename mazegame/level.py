"""Level format: a plain-text grid.

    #  wall
    .  empty floor
    S  snake start
    F  fruit
    T  delivery truck

Coordinates are (x, y) = (column, row), with (0, 0) in the top-left corner.
See levels/001.txt for an example.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

WALL, FLOOR, START, FRUIT, TRUCK = "#", ".", "S", "F", "T"
VALID_CHARS = frozenset({WALL, FLOOR, START, FRUIT, TRUCK})

Cell = tuple[int, int]


class LevelError(ValueError):
    ...

@dataclass(frozen=True)
class Level:
    width: int
    height: int
    walls: frozenset[Cell]
    start: Cell
    fruits: frozenset[Cell]
    trucks: frozenset[Cell]

    def is_wall(self, cell: Cell) -> bool:
        x, y = cell
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        return cell in self.walls


def parse_level(text: str) -> Level:
    rows = [line.strip() for line in text.strip().splitlines()]
    if not rows or not rows[0]:
        raise LevelError("level is empty")

    width = len(rows[0])
    walls: set[Cell] = set()
    fruits: set[Cell] = set()
    trucks: set[Cell] = set()
    starts: list[Cell] = []

    for y, row in enumerate(rows):
        if len(row) != width:
            raise LevelError(f"row {y} has length {len(row)}, expected {width}")
        for x, ch in enumerate(row):
            if ch not in VALID_CHARS:
                raise LevelError(f"unknown character {ch!r} at x={x}, y={y}")
            if ch == WALL:
                walls.add((x, y))
            elif ch == FRUIT:
                fruits.add((x, y))
            elif ch == TRUCK:
                trucks.add((x, y))
            elif ch == START:
                starts.append((x, y))

    if len(starts) != 1:
        raise LevelError(f"expected exactly one start 'S', found {len(starts)}")

    return Level(
        width=width,
        height=len(rows),
        walls=frozenset(walls),
        start=starts[0],
        fruits=frozenset(fruits),
        trucks=frozenset(trucks),
    )


def load_level(path: str | Path) -> Level:
    return parse_level(Path(path).read_text(encoding="utf-8"))
