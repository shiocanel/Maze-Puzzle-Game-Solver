from snacky_dash.engine.game_state import GameState


def is_position_blocked(game_state, grid, position):
    return grid.is_wall(position) or (game_state.get_stack_at(position) is not None)


def one_step(game_state, grid, direction):
    head_position = game_state.snake.get_head_position()
    new_head_position = direction.move(head_position)

    if is_position_blocked(game_state, grid, new_head_position):
        return None

    new_snake = game_state.snake.move_snake(new_head_position)
    return GameState(new_snake, game_state.fruits, game_state.stacks)
