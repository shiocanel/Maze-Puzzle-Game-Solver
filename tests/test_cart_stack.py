import pytest

from snacky_dash.engine.cart_stack import CartStack
from snacky_dash.engine.cart import Cart
from snacky_dash.engine.color import Color


@pytest.fixture
def base_stack():
    return CartStack(
        (
            Cart(
                color=Color.RED,
                top_left_position=(1, 1),
                delivery_position=(4, 2),
                loaded_count=7,
            ),
            Cart(
                color=Color.RED,
                top_left_position=(1, 1),
                delivery_position=(4, 2),
                loaded_count=0,
            ),
            Cart(
                color=Color.BLUE,
                top_left_position=(1, 1),
                delivery_position=(4, 2),
                loaded_count=0,
            ),
        )
    )


def test_initial_stack_state(base_stack):
    assert base_stack.total_loaded() == 7
    assert base_stack.carts[0].loaded_count == 7
    assert base_stack.carts[1].loaded_count == 0
    assert base_stack.carts[2].loaded_count == 0


def test_load_two(base_stack):
    new_stack = base_stack.load(2)
    assert new_stack.total_loaded() == 9
    assert new_stack.carts[0].loaded_count == 9
    assert new_stack.carts[1].loaded_count == 0
    assert new_stack.carts[2].loaded_count == 0


def test_load_five(base_stack):
    new_stack = base_stack.load(5)
    assert new_stack.total_loaded() == 9
    assert new_stack.carts[0].loaded_count == 9
    assert new_stack.carts[1].loaded_count == 0


def test_sequential_loads(base_stack):
    stack_after_2 = base_stack.load(2)
    final_stack = stack_after_2.load(4)

    assert final_stack.total_loaded() == 13
    assert final_stack.carts[0].loaded_count == 9
    assert final_stack.carts[1].loaded_count == 4
    assert final_stack.carts[2].loaded_count == 0


def test_immutability(base_stack):
    _ = base_stack.load(5)
    assert base_stack.total_loaded() == 7
    assert base_stack.carts[0].loaded_count == 7
    assert base_stack.carts[1].loaded_count == 0
    assert base_stack.carts[2].loaded_count == 0


def test_active_cart_transitions(base_stack):
    active_1 = base_stack.get_active_cart()
    assert active_1.color == Color.RED
    assert active_1.loaded_count == 7

    stack_loaded = base_stack.load(2)
    active_2 = stack_loaded.get_active_cart()
    assert active_2.color == Color.RED
    assert active_2.loaded_count == 0


def test_all_full_stack():
    full_stack = CartStack(
        (
            Cart(
                color=Color.RED,
                top_left_position=(1, 1),
                delivery_position=(4, 2),
                loaded_count=9,
            ),
            Cart(
                color=Color.RED,
                top_left_position=(1, 1),
                delivery_position=(4, 2),
                loaded_count=9,
            ),
            Cart(
                color=Color.BLUE,
                top_left_position=(1, 1),
                delivery_position=(4, 2),
                loaded_count=9,
            ),
        )
    )

    assert full_stack.is_stack_complete() is True
    assert full_stack.get_active_cart() is None
    assert full_stack.total_loaded() == 27

    unchanged_stack = full_stack.load(5)
    assert unchanged_stack.total_loaded() == 27


def test_stack_positions(base_stack):
    assert base_stack.is_position_part_of_stack((1, 1)) is True
    assert base_stack.is_position_part_of_stack((5, 5)) is False
    assert base_stack.is_position_delivery((4, 2)) is True
    assert base_stack.is_position_delivery((1, 1)) is False
