from snacky_dash.engine.unload_snake import unload_snake_to_stack
from snacky_dash.engine.snake import Snake
from snacky_dash.engine.cart import Cart
from snacky_dash.engine.cart_stack import CartStack
from snacky_dash.engine.color import Color


def test_delivery_worked_example():
    cart1 = Cart(
        color=Color.RED,
        top_left_position=(1, 1),
        delivery_position=(4, 2),
        loaded_count=7,
    )
    cart2 = Cart(
        color=Color.RED,
        top_left_position=(1, 1),
        delivery_position=(4, 2),
        loaded_count=0,
    )
    cart3 = Cart(
        color=Color.GREEN,
        top_left_position=(1, 1),
        delivery_position=(4, 2),
        loaded_count=0,
    )
    stack = CartStack((cart1, cart2, cart3))

    positions = ((5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0))
    colors = (Color.RED, Color.RED, Color.RED, Color.BLUE, Color.BLUE, Color.BLUE)
    snake = Snake(positions, colors)

    new_snake, new_stack = unload_snake_to_stack(snake, stack)

    assert new_stack.carts[0].loaded_count == 9
    assert new_stack.carts[1].loaded_count == 1
    assert new_stack.carts[2].loaded_count == 0

    assert new_snake.colors == (Color.BLUE, Color.BLUE, Color.BLUE)
    assert new_snake.get_length() == 4


def test_delivery_no_matching_color():
    cart = Cart(
        color=Color.RED,
        top_left_position=(1, 1),
        delivery_position=(4, 2),
        loaded_count=0,
    )
    stack = CartStack((cart,))

    snake = Snake(((2, 2), (2, 1)), (Color.BLUE,))

    new_snake, new_stack = unload_snake_to_stack(snake, stack)

    assert new_snake.colors == snake.colors
    assert new_snake.snake_positions == snake.snake_positions
    assert new_stack.carts[0].loaded_count == 0
