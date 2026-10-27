import pytest
from snacky_dash.engine.game_state import GameState
from snacky_dash.engine.snake import Snake
from snacky_dash.engine.cart import Cart
from snacky_dash.engine.cart_stack import CartStack
from snacky_dash.engine.color import Color
from snacky_dash.engine.direction import Direction
from snacky_dash.engine.grid import Grid
from snacky_dash.engine.movement import (
    is_position_blocked,
    one_step,
    has_open_side,
    open_directions,
    slide,
)

@pytest.fixture
def sample_movement_setup():
    grid_lines = [
        "#########",
        "#CCC....#",
        "#CCC....#",
        "#CCC....#",
        "#.D.....#",
        "#.....H.#",
        "#########",
    ]
    grid = Grid(grid_lines)

    snake = Snake(((5, 6),), ())
    fruits = {
        (5, 4): Color.RED,
        (3, 6): Color.BLUE,
    }

    cart = Cart(
        color=Color.RED,
        top_left_position=(1, 1),
        delivery_position=(4, 2),
        loaded_count=0,
    )
    stacks = (CartStack((cart,)),)
    game_state = GameState(snake, fruits, stacks)

    return game_state, grid


def test_is_position_blocked(sample_movement_setup):
    game_state, grid = sample_movement_setup

    assert is_position_blocked(game_state, grid, (0, 0)) is True
    assert is_position_blocked(game_state, grid, (-1, 3)) is True
    assert is_position_blocked(game_state, grid, (2, 2)) is True

    assert is_position_blocked(game_state, grid, (4, 2)) is False
    assert is_position_blocked(game_state, grid, (5, 5)) is False


def test_one_step_from_5_6(sample_movement_setup):
    game_state, grid = sample_movement_setup

    state_left = one_step(game_state, grid, Direction.LEFT)
    assert state_left is not None
    assert state_left.snake.get_head_position() == (5, 5)

    state_up = one_step(game_state, grid, Direction.UP)
    assert state_up is not None
    assert state_up.snake.get_head_position() == (4, 6)

    state_down = one_step(game_state, grid, Direction.DOWN)
    assert state_down is None


def test_one_step_near_cart():
    grid_lines = [
        "#########",
        "#CCC....#",
        "#CCC....#",
        "#CCC....#",
        "#.D.....#",
        "#.....H.#",
        "#########",
    ]
    grid = Grid(grid_lines)

    snake = Snake(((4, 3),), ())
    cart = Cart(
        color=Color.RED,
        top_left_position=(1, 1),
        delivery_position=(4, 2),
        loaded_count=0,
    )
    game_state = GameState(snake, {}, (CartStack((cart,)),))

    state_up = one_step(game_state, grid, Direction.UP)
    assert state_up is None

    state_left = one_step(game_state, grid, Direction.LEFT)
    assert state_left is not None
    assert state_left.snake.get_head_position() == (4, 2)


def test_multi_segment_snake_movement():
    grid_lines = [
        "#########",
        "#CCC....#",
        "#CCC....#",
        "#CCC....#",
        "#.D.....#",
        "#.....H.#",
        "#########",
    ]

    grid = Grid(grid_lines)

    snake = Snake(((5, 6), (5, 7)), (Color.RED,))
    game_state = GameState(snake, {}, ())

    new_state = one_step(game_state, grid, Direction.LEFT)
    assert new_state is not None
    assert new_state.snake.snake_positions == ((5, 5), (5, 6))


def test_movement_immutability(sample_movement_setup):
    game_state, grid = sample_movement_setup
    original_head = game_state.snake.get_head_position()

    _ = one_step(game_state, grid, Direction.LEFT)

    assert game_state.snake.get_head_position() == original_head
    assert game_state.get_fruit_at((5, 4)) == Color.RED


def test_has_open_side_map_b():
    grid_lines = ["#########", "#.......#", "####.####", "####.####", "#########"]
    grid = Grid(grid_lines)
    game_state = GameState(Snake(((1, 4),), ()), {}, ())

    assert has_open_side(game_state, grid, Direction.RIGHT, (1, 4)) is True
    assert has_open_side(game_state, grid, Direction.RIGHT, (1, 3)) is False


def test_has_open_side_map_c_with_cart():
    grid_lines = [
        "#########",
        "#...#####",
        "#...#####",
        "#...#####",
        "#.......#",
        "#########",
    ]
    grid = Grid(grid_lines)

    cart = Cart(
        color=Color.RED,
        top_left_position=(1, 1),
        delivery_position=(4, 2),
        loaded_count=0,
    )
    game_state = GameState(Snake(((4, 3),), ()), {}, (CartStack((cart,)),))

    assert has_open_side(game_state, grid, Direction.LEFT, (4, 3)) is False


def test_has_open_side_map_c_no_carts():
    grid_lines = [
        "#########",
        "#...#####",
        "#...#####",
        "#...#####",
        "#.......#",
        "#########",
    ]
    grid = Grid(grid_lines)
    game_state = GameState(Snake(((4, 3),), ()), {}, ())
    assert has_open_side(game_state, grid, Direction.LEFT, (4, 3)) is True


def test_open_directions_map_b():
    grid_lines = ["#########", "#.......#", "####.####", "####.####", "#########"]
    grid = Grid(grid_lines)
    game_state = GameState(Snake(((1, 4),), ()), {}, ())

    result_b1 = open_directions(game_state, grid, Direction.RIGHT, (1, 4))
    assert result_b1 == (Direction.RIGHT, Direction.DOWN)

    result_b2 = open_directions(game_state, grid, Direction.RIGHT, (1, 3))
    assert result_b2 == (Direction.RIGHT,)

    result_b3 = open_directions(game_state, grid, Direction.RIGHT, (1, 7))
    assert result_b3 == ()


def test_open_directions_map_d():
    grid_lines = ["#######", "#.....#", "#####.#", "#####.#", "#######"]
    grid = Grid(grid_lines)
    game_state = GameState(Snake(((1, 5),), ()), {}, ())

    result_d1 = open_directions(game_state, grid, Direction.RIGHT, (1, 5))
    assert result_d1 == (Direction.DOWN,)


def test_slide_map_b_basic():
    grid = Grid(["#########", "#.......#", "####.####", "####.####", "#########"])
    state = GameState(Snake(((1, 1),), ()), {}, ())
    final_state = slide(state, grid, Direction.RIGHT)
    assert final_state is not None
    assert final_state.snake.get_head_position() == (1, 4)


def test_slide_map_b_second():
    grid = Grid(["#########", "#.......#", "####.####", "####.####", "#########"])
    state = GameState(Snake(((1, 4),), ()), {}, ())
    final_state = slide(state, grid, Direction.RIGHT)
    assert final_state is not None
    assert final_state.snake.get_head_position() == (1, 7)


def test_slide_map_b_blocked_first():
    grid = Grid(["#########", "#.......#", "####.####", "####.####", "#########"])
    state = GameState(Snake(((1, 2),), ()), {}, ())
    final_state = slide(state, grid, Direction.DOWN)
    assert final_state is None


def test_slide_map_d_turning():
    grid = Grid(["#######", "#.....#", "#####.#", "#####.#", "#######"])
    state = GameState(Snake(((1, 1),), ()), {}, ())
    final_state = slide(state, grid, Direction.RIGHT)
    assert final_state is not None
    assert final_state.snake.get_head_position() == (3, 5)


def test_slide_map_c_delivery():
    grid = Grid(
        ["#########", "#...#####", "#...#####", "#...#####", "#.......#", "#########"]
    )
    cart = Cart(
        color=Color.RED,
        top_left_position=(1, 1),
        delivery_position=(4, 2),
        loaded_count=0,
    )
    state = GameState(Snake(((4, 7),), ()), {}, (CartStack((cart,)),))
    final_state = slide(state, grid, Direction.LEFT)
    assert final_state is not None
    assert final_state.snake.get_head_position() == (4, 2)
    assert final_state.is_position_delivery((4, 2)) is True


def test_slide_map_t():
    grid = Grid(["#####", "##.##", "#...#", "#####"])
    state = GameState(Snake(((1, 2),), ()), {}, ())
    final_state = slide(state, grid, Direction.DOWN)
    assert final_state is not None
    assert final_state.snake.get_head_position() == (2, 2)


def test_slide_head_hit_body():
    grid = Grid(["#########", "#.......#", "####.####", "####.####", "#########"])
    snake = Snake(((1, 5), (1, 6), (1, 7)), (Color.RED, Color.BLUE))
    state = GameState(snake, {}, ())
    final_state = slide(state, grid, Direction.RIGHT)
    assert final_state is not None
    assert final_state.snake.head_hit_body() is True


def test_slide_immutability():
    grid = Grid(["#########", "#.......#", "####.####", "####.####", "#########"])
    state = GameState(Snake(((1, 1),), ()), {}, ())
    original_head = state.snake.get_head_position()
    _ = slide(state, grid, Direction.RIGHT)
    assert state.snake.get_head_position() == original_head


def test_slide_ring_no_hang():
    grid = Grid(["#####", "#...#", "#.#.#", "#...#", "#####"])
    state = GameState(Snake(((1, 1),), ()), {}, ())
    final_state = slide(state, grid, Direction.RIGHT)
    assert final_state is not None


def test_one_step_eating_fruit():
    grid_lines = [
        "#########",
        "#CCC....#",
        "#CCC....#",
        "#CCC..B.#",
        "#.D.....#",
        "#...R.H.#",
        "#########",
    ]
    grid = Grid(grid_lines)
    snake = Snake(((5, 5),), ())
    fruits = {
        (5, 4): Color.RED,
        (3, 6): Color.BLUE,
    }
    game_state = GameState(snake, fruits, ())

    new_state = one_step(game_state, grid, Direction.LEFT)
    assert new_state is not None
    assert new_state.snake.snake_positions == ((5, 4), (5, 5))
    assert new_state.snake.colors == (Color.RED,)
    assert new_state.get_fruit_at((5, 4)) is None
    assert new_state.get_fruit_at((3, 6)) == Color.BLUE

    assert game_state.snake.get_length() == 1
    assert game_state.get_fruit_at((5, 4)) == Color.RED


def test_one_step_eating_with_multi_segment_snake():
    grid_lines = [
        "#########",
        "#CCC....#",
        "#CCC....#",
        "#CCC..B.#",
        "#.D.....#",
        "#...R.H.#",
        "#########",
    ]
    grid = Grid(grid_lines)
    snake = Snake(((5, 5), (5, 6)), (Color.BLUE,))
    fruits = {(5, 4): Color.RED}
    game_state = GameState(snake, fruits, ())

    new_state = one_step(game_state, grid, Direction.LEFT)
    assert new_state is not None
    assert new_state.snake.snake_positions == ((5, 4), (5, 5), (5, 6))
    assert new_state.snake.colors == (Color.BLUE, Color.RED)


def test_one_step_empty_cell_preserves_fruits():
    grid_lines = [
        "#########",
        "#CCC....#",
        "#CCC....#",
        "#CCC..B.#",
        "#.D.....#",
        "#...R.H.#",
        "#########",
    ]
    grid = Grid(grid_lines)
    snake = Snake(((5, 5),), ())
    fruits = {(5, 4): Color.RED}
    game_state = GameState(snake, fruits, ())

    new_state = one_step(game_state, grid, Direction.UP)
    assert new_state is not None
    assert new_state.get_fruit_at((5, 4)) == Color.RED


def test_slide_eating_fruit():
    grid = Grid(["#######", "#.....#", "#######"])
    fruits = {(1, 3): Color.RED}
    state = GameState(Snake(((1, 1),), ()), fruits, ())

    final_state = slide(state, grid, Direction.RIGHT)

    assert final_state is not None
    assert final_state.snake.get_head_position() == (1, 5)
    assert final_state.snake.snake_positions == ((1, 5), (1, 4))
    assert final_state.snake.colors == (Color.RED,)
    assert final_state.get_fruit_at((1, 3)) is None
