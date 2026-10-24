from snacky_dash.engine.tile import Tile


def test_FLOOR():
    assert Tile.FLOOR.value == "."

def test_WALL():
    assert Tile.WALL.value == "#"