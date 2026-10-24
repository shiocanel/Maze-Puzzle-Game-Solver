from snacky_dash.engine.grid import Grid


def test_grid():
    grid = ["#######", "#.#...#", "#.#.#.#", "#.....#", "#.###.#", "#.....#", "#######"]

    gr = Grid(grid)
    assert gr.grid == grid
    assert gr.rows == 7
    assert gr.columns == 7


def test_grid02():
    grid = ["#######", "#.#...#", "#.#.#.#", "#.....#", "#######"]

    gr = Grid(grid)
    assert gr.grid == grid
    assert gr.rows == 5
    assert gr.columns == 7


def test_is_inside():
    grid = ["#######", "#.#...#", "#.#.#.#", "#.....#", "#.###.#", "#.....#", "#######"]

    gr = Grid(grid)
    assert gr.is_inside((0, 0))
    assert gr.is_inside((0, 1))
    assert gr.is_inside((1, 1))
    assert gr.is_inside((6, 6))
    assert gr.is_inside((0, 6))
    assert gr.is_inside((6, 0))

    assert not gr.is_inside((-1, -1))
    assert not gr.is_inside((-1, 0))
    assert not gr.is_inside((0, -5))
    assert not gr.is_inside((1, 7))
    assert not gr.is_inside((6, -5))
    assert not gr.is_inside((7, 0))


def test_is_wall():
    grid = ["#######", "#.#...#", "#.#.#.#", "#.....#", "#.###.#", "#.....#", "#######"]
    gr = Grid(grid)

    assert gr.is_wall((0, 0))
    assert gr.is_wall((0, 1))
    assert gr.is_wall((0, 2))
    assert gr.is_wall((-1, 0))
    assert gr.is_wall((7, 3))
    assert gr.is_wall((1, 2))

    assert not gr.is_wall((1, 1))
    assert not gr.is_wall((2, 1))
    assert not gr.is_wall((3, 1))