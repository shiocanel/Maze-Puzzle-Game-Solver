from snacky_dash.engine.snake import Snake
from snacky_dash.engine.color import Color

def test_snake():
    snake = Snake(((2, 4), (2, 3), (2, 2)), (Color.RED, Color.BLUE))

    assert snake.count_color(Color.RED) == 1
    assert snake.count_color(Color.BLUE) == 1

    assert not snake.is_position_part_of_body((2, 4))
    assert snake.is_position_part_of_body((2, 3))
    assert snake.is_position_part_of_body((2, 2))

    assert snake.is_position_part_of_snake((2, 4))
    assert snake.is_position_part_of_snake((2, 3))
    assert snake.is_position_part_of_snake((2, 2))
    assert not snake.is_position_part_of_snake((5, 5))

    assert not snake.head_hit_body()

    assert snake.get_length() == 3
    assert snake.get_head_position() == (2, 4)
    assert snake.get_tail_position() == (2, 2)


def test_small_snake():
    snake = Snake(((2, 2),), ())

    assert not snake.is_position_part_of_body((2, 2))

    assert snake.is_position_part_of_snake((2, 2))
    assert not snake.is_position_part_of_snake((5, 5))

    assert not snake.head_hit_body()

    assert snake.get_length() == 1
    assert snake.get_head_position() == (2, 2)
    assert snake.get_tail_position() == (2, 2)


def test_snake_colliding():
    snake = Snake(((2, 4), (2, 3), (2, 4)), (Color.RED, Color.BLUE))

    assert snake.is_position_part_of_body((2, 4))
    assert snake.is_position_part_of_body((2, 3))

    assert snake.is_position_part_of_snake((2, 4))
    assert snake.is_position_part_of_snake((2, 3))
    assert not snake.is_position_part_of_snake((5, 5))

    assert snake.head_hit_body()

    assert snake.get_length() == 3
    assert snake.get_head_position() == (2, 4)
    assert snake.get_tail_position() == (2, 4)


def test_move_snake():
    snake = Snake(((2, 4), (2, 3), (2, 2)), (Color.RED, Color.BLUE))

    new_snake = snake.move_snake((2, 5))

    assert not new_snake.is_position_part_of_body((2, 5))
    assert new_snake.is_position_part_of_body((2, 4))
    assert new_snake.is_position_part_of_body((2, 3))

    assert new_snake.is_position_part_of_snake((2, 5))
    assert new_snake.is_position_part_of_snake((2, 4))
    assert new_snake.is_position_part_of_snake((2, 3))
    assert not new_snake.is_position_part_of_snake((5, 5))

    assert not new_snake.head_hit_body()

    assert new_snake.get_length() == 3
    assert new_snake.get_head_position() == (2, 5)
    assert new_snake.get_tail_position() == (2, 3)

    assert snake.is_position_part_of_snake((2, 4))
    assert snake.is_position_part_of_snake((2, 3))
    assert snake.is_position_part_of_snake((2, 2))
    assert not snake.is_position_part_of_snake((5, 5))

    assert snake.colors == new_snake.colors


def test_grow_snake():
    snake = Snake(((2, 4), (2, 3), (2, 2)), (Color.RED, Color.BLUE))

    new_snake = snake.grow_snake((2, 5), Color.RED)

    assert new_snake.colors == (Color.RED, Color.BLUE, Color.RED)

    assert new_snake.count_color(Color.RED) == 2
    assert new_snake.count_color(Color.GREEN) == 0

    assert not new_snake.is_position_part_of_body((2, 5))
    assert new_snake.is_position_part_of_body((2, 4))
    assert new_snake.is_position_part_of_body((2, 3))
    assert new_snake.is_position_part_of_body((2, 2))

    assert new_snake.is_position_part_of_snake((2, 5))
    assert new_snake.is_position_part_of_snake((2, 4))
    assert new_snake.is_position_part_of_snake((2, 3))
    assert new_snake.is_position_part_of_snake((2, 2))
    assert not new_snake.is_position_part_of_snake((5, 5))

    assert not new_snake.head_hit_body()

    assert new_snake.get_length() == 4
    assert new_snake.get_head_position() == (2, 5)
    assert new_snake.get_tail_position() == (2, 2)

    assert snake.is_position_part_of_snake((2, 4))
    assert snake.is_position_part_of_snake((2, 3))
    assert snake.is_position_part_of_snake((2, 2))
    assert not snake.is_position_part_of_snake((5, 5))


def test_snake_remove_colors_partial():
    snake = Snake(
        ((5, 5), (5, 4), (5, 3), (5, 2), (5, 1)),
        (Color.RED, Color.RED, Color.RED, Color.BLUE),
    )

    new_snake = snake.remove_colors(Color.RED, 2)

    assert new_snake.colors == (Color.RED, Color.BLUE)
    assert new_snake.get_length() == 3
    assert new_snake.snake_positions == ((5, 5), (5, 4), (5, 3))


def test_snake_remove_colors_exceeds_available():
    snake = Snake(
        ((5, 5), (5, 4), (5, 3), (5, 2), (5, 1)),
        (Color.RED, Color.RED, Color.RED, Color.BLUE),
    )

    new_snake = snake.remove_colors(Color.RED, 5)

    assert new_snake.colors == (Color.BLUE,)
    assert new_snake.get_length() == 2
    assert new_snake.snake_positions == ((5, 5), (5, 4))

    assert snake.get_length() == 5
    assert snake.colors == (Color.RED, Color.RED, Color.RED, Color.BLUE)
