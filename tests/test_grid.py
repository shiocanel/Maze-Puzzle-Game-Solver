from snacky_dash.engine.grid import Grid


def test_grid():
    grid = [
        "#######",
        "#.#...#",
        "#.#.#.#",
        "#.....#",
        "#.###.#",
        "#.....#",
        "#######"
           ]

    gr = Grid(grid)
    assert gr.grid == grid
    assert gr.width == 7
    assert gr.height == 7
