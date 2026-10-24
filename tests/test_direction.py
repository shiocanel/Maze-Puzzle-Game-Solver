from snacky_dash.engine.direction import Direction


def test_direction():
    assert Direction.UP.value == (-1, 0)
    assert Direction.DOWN.value == (1, 0)
    assert Direction.LEFT.value == (0, -1)
    assert Direction.RIGHT.value == (0, 1)


def test_UP():
    assert Direction.UP.move((1, 1)) == (0, 1)


def test_DOWN():
    assert Direction.DOWN.move((1, 1)) == (2, 1)


def test_LEFT():
    assert Direction.LEFT.move((1, 1)) == (1, 0)


def test_RIGHT():   
    assert Direction.RIGHT.move((1, 1)) == (1, 2)


def test_off_the_map():
    assert Direction.UP.move((0, 0)) == (-1, 0)
    assert Direction.LEFT.move((0, 0)) == (0, -1)