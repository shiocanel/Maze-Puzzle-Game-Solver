from snacky_dash.engine.color import Color


def test_color():
    assert Color.RED.value == "R"
    assert Color.YELLOW.value == "Y"
    assert Color.BLUE.value == "B"
    assert Color.GREEN.value == "G"
    assert Color.ORANGE.value == "O"
    assert Color.PURPLE.value == "P"
