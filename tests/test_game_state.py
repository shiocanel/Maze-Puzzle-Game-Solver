import pytest
from snacky_dash.engine.game_state import GameState
from snacky_dash.engine.snake import Snake
from snacky_dash.engine.cart import Cart
from snacky_dash.engine.cart_stack import CartStack
from snacky_dash.engine.color import Color


@pytest.fixture
def sample_game_state():
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
    return GameState(snake, fruits, stacks)


def test_fruit_lookups(sample_game_state):
    assert sample_game_state.get_fruit_at((5, 4)) == Color.RED
    assert sample_game_state.get_fruit_at((3, 6)) == Color.BLUE
    assert sample_game_state.get_fruit_at((1, 1)) is None


def test_remove_fruit_immutability(sample_game_state):
    new_state = sample_game_state.remove_fruit_at((5, 4))
    
    assert new_state.get_fruit_at((5, 4)) is None
    assert sample_game_state.get_fruit_at((5, 4)) == Color.RED


def test_remove_nonexistent_fruit(sample_game_state):
    new_state = sample_game_state.remove_fruit_at((9, 9))
    assert new_state.get_fruit_at((5, 4)) == Color.RED
    assert new_state.get_fruit_at((3, 6)) == Color.BLUE


def test_stack_lookups(sample_game_state):
    assert sample_game_state.get_stack_at((2, 2)) is not None
    assert sample_game_state.get_stack_at((5, 5)) is None

    assert sample_game_state.is_position_delivery((4, 2)) == True
    assert sample_game_state.is_position_delivery((2, 2)) == False


def test_is_won_states():
    snake = Snake(((5, 6),), ())

    cart_unfilled = Cart(Color.RED, (1, 1), (4, 2), loaded_count=0)
    state_unfilled = GameState(snake, {}, (CartStack((cart_unfilled,)),))
    assert state_unfilled.is_won() is False

    cart_filled = Cart(Color.RED, (1, 1), (4, 2), loaded_count=9)
    state_filled = GameState(snake, {}, (CartStack((cart_filled,)),))
    assert state_filled.is_won() is True
