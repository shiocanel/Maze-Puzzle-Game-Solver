from snacky_dash.engine.snake import Snake


def test_snake():
    snake = Snake(((2, 4), (2, 3), (2, 2)))

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
    snake = Snake(((2, 2),))

    assert not snake.is_position_part_of_body((2, 2))

    assert snake.is_position_part_of_snake((2, 2))
    assert not snake.is_position_part_of_snake((5, 5))

    assert not snake.head_hit_body()

    assert snake.get_length() == 1
    assert snake.get_head_position() == (2, 2)
    assert snake.get_tail_position() == (2, 2)


def test_snake_colliding():
    snake = Snake(((2, 4), (2, 3), (2, 4)))

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
    snake = Snake(((2, 4), (2, 3), (2, 2)))

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


def test_grow_snake():
    snake = Snake(((2, 4), (2, 3), (2, 2)))

    new_snake = snake.grow_snake((2, 5))

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
