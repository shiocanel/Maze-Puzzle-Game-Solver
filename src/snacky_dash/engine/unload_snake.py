def unload_snake_to_stack(snake, stack):
    current_snake = snake
    current_stack = stack

    while True:
        active_cart = current_stack.get_active_cart()
        if active_cart is None:
            return current_snake, current_stack

        fruit_count = current_snake.count_color(active_cart.color)
        if fruit_count == 0:
            return current_snake, current_stack

        count_to_load = min(fruit_count, active_cart.free_spaces())
        if count_to_load == 0:
            return current_snake, current_stack

        current_stack = current_stack.load(count_to_load)
        current_snake = current_snake.remove_colors(active_cart.color, count_to_load)