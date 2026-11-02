from snacky_dash.engine.direction import Direction
from snacky_dash.engine.level_loader import load_level_from_file
from snacky_dash.engine.movement import slide


def render_board(grid, game_state):
    board = [list(row) for row in grid.grid]

    for stack in game_state.stacks:
        for cart in stack.carts:
            for pos in cart.cart_positions:
                r, c = pos
                if grid.is_inside(pos) and not grid.is_wall(pos):
                    board[r][c] = "C"
            dr, dc = cart.delivery_position
            if grid.is_inside((dr, dc)):
                board[dr][dc] = "D"

    for pos, color in game_state.fruits.items():
        r, c = pos
        if grid.is_inside(pos):
            board[r][c] = color.value

    for i, pos in enumerate(game_state.snake.snake_positions):
        r, c = pos
        if grid.is_inside(pos):
            if i == 0:
                board[r][c] = "H"
            else:
                board[r][c] = "o"

    return "\n".join("".join(row) for row in board)


def main():
    level_path = "levels/level_02.json"
    try:
        grid, state = load_level_from_file(level_path)
    except FileNotFoundError:
        print(f"Level file not found at {level_path}")
        return

    print("===Snacky Dash Terminal Play===")
    print("Controls: w (UP), s (DOWN), a (LEFT), d (RIGHT), q (QUIT)")

    key_map = {
        "w": Direction.UP,
        "s": Direction.DOWN,
        "a": Direction.LEFT,
        "d": Direction.RIGHT,
    }

    while True:
        print("\n" + render_board(grid, state))
        print(f"Snake head: {state.snake.get_head_position()}")
        print(f"Snake colors: {[color.value for color in state.snake.colors]}")

        for i, stack in enumerate(state.stacks):
            print(f"Stack {i} loaded total: {stack.total_loaded()} (Complete: {stack.is_stack_complete()})")

        if state.is_won():
            print("\nYou won!")
            break

        if state.snake.head_hit_body():
            print("\nGame Over!")
            break

        choice = input("\nEnter move (w/a/s/d/q): ").strip().lower()
        if choice == "q":
            print("Exiting game.")
            break

        if choice not in key_map:
            print("Invalid input. Use w, a, s, d, or q.")
            continue

        direction = key_map[choice]
        new_state = slide(state, grid, direction)

        if new_state is None:
            print("You can't move there!")
        else:
            state = new_state


if __name__ == "__main__":
    main()