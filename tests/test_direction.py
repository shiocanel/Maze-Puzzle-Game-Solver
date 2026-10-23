from snacky_dash.engine.direction import Direction 


def test_direction():
    assert(Direction.UP.value == (-1, 0))
    assert(Direction.DOWN.value == (1, 0))
    assert(Direction.LEFT.value == (0, -1))
    assert(Direction.RIGHT.value == (0, 1))