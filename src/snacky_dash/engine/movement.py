from snacky_dash.engine.game_state import GameState


def is_position_blocked(game_state, grid, position):
    return grid.is_wall(position) or (game_state.get_stack_at(position) is not None)


def one_step(game_state, grid, direction):
    head_position = game_state.snake.get_head_position()
    new_head_position = direction.move(head_position)

    if is_position_blocked(game_state, grid, new_head_position):
        return None

    fruit_color = game_state.get_fruit_at(new_head_position)
    if fruit_color is not None:
        state_without_fruit = game_state.remove_fruit_at(new_head_position)
        new_snake = game_state.snake.grow_snake(new_head_position, fruit_color)

        return GameState(new_snake, state_without_fruit.fruits, game_state.stacks)

    new_snake = game_state.snake.move_snake(new_head_position)
    return GameState(new_snake, game_state.fruits, game_state.stacks)


def has_open_side(game_state, grid, direction, position):
    sideways = direction.sideways()

    for side in sideways:
        neighbour_cell = side.move(position)

        if not is_position_blocked(game_state, grid, neighbour_cell):
            return True

    return False


def open_directions(game_state, grid, direction, position):
    result = ()
    forward_position = direction.move(position)

    if not is_position_blocked(game_state, grid, forward_position):
        result = result + (direction,)

    sideways = direction.sideways()
    for side in sideways:
        neighbour_cell = side.move(position)

        if not is_position_blocked(game_state, grid, neighbour_cell):
            result = result + (side,)

    return result


def slide(game_state, grid, direction):
    current_state = one_step(game_state, grid, direction)
    if current_state is None:
        return None

    current_direction = direction
    seen = set()

    while True:
        head_position = current_state.snake.get_head_position()

        if current_state.snake.head_hit_body():
            return current_state

        if current_state.is_position_delivery(head_position):
            return current_state

        opens = open_directions(current_state, grid, current_direction, head_position)
        if len(opens) != 1:
            return current_state

        pair = (head_position, current_direction)
        if pair in seen:
            return current_state
        seen.add(pair)

        current_direction = opens[0]
        next_state = one_step(current_state, grid, current_direction)
        if next_state is None:
            return current_state
        current_state = next_state
