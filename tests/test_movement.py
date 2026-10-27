import pytest
from snacky_dash.engine.game_state import GameState
from snacky_dash.engine.snake import Snake
from snacky_dash.engine.cart import Cart
from snacky_dash.engine.cart_stack import CartStack
from snacky_dash.engine.color import Color
from snacky_dash.engine.direction import Direction
from snacky_dash.engine.grid import Grid
from snacky_dash.engine.movement import is_position_blocked, one_step


@pytest.fixture
def sample_movement_setup():
    grid_lines = [
        "#########",
        "#CCC....#",
        "#CCC....#",
        "#CCC..B.#",
        "#.D.....#",
        "#...R.H.#",
        "#########"
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
        loaded_count=0
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
        "#CCC..B.#",
        "#.D.....#",
        "#...R.H.#",
        "#########"
    ]
    grid = Grid(grid_lines)
    
    snake = Snake(((4, 3),), ())
    cart = Cart(
        color=Color.RED,
        top_left_position=(1, 1),
        delivery_position=(4, 2),
        loaded_count=0
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
        "#CCC..B.#",
        "#.D.....#",
        "#...R.H.#",
        "#########"
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