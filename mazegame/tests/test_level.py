from pathlib import Path

import pytest

from mazegame.level import LevelError, load_level, parse_level

SIMPLE = """
#####
#S.F#
#.#T#
#####
"""


def test_parse_simple_level():
    level = parse_level(SIMPLE)
    assert (level.width, level.height) == (5, 4)
    assert level.start == (1, 1)
    assert level.fruits == {(3, 1)}
    assert level.trucks == {(3, 2)}
    assert (0, 0) in level.walls


def test_cells_outside_grid_are_walls():
    level = parse_level(SIMPLE)
    assert level.is_wall((-1, 0))
    assert level.is_wall((5, 1))
    assert not level.is_wall((2, 1))


def test_ragged_rows_rejected():
    with pytest.raises(LevelError, match="row 1"):
        parse_level("###\n##\n###")


def test_unknown_character_rejected():
    with pytest.raises(LevelError, match="unknown character"):
        parse_level("#S#\n#X#")


@pytest.mark.parametrize("text", ["#.#\n#.#", "#S#\n#S#"])
def test_exactly_one_start_required(text):
    with pytest.raises(LevelError, match="exactly one start"):
        parse_level(text)


def test_empty_level_rejected():
    with pytest.raises(LevelError, match="empty"):
        parse_level("  \n ")


def test_example_level_file_loads():
    path = Path(__file__).parent.parent / "levels" / "001.txt"
    level = load_level(path)
    assert level.fruits and level.trucks
