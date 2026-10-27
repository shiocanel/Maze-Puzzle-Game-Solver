class GameState:
    def __init__(self, snake, fruits, stacks) -> None:
        self.snake = snake
        self.fruits = dict(fruits)
        self.stacks = tuple(stacks)

    def get_fruit_at(self, position):
        return self.fruits.get(position)

    def remove_fruit_at(self, position):
        new_fruits = dict(self.fruits)
        new_fruits.pop(position, None)

        return GameState(self.snake, new_fruits, self.stacks)

    def get_stack_at(self, position):
        for stack in self.stacks:
            if stack.is_position_part_of_stack(position):
                return stack

        return None

    def is_won(self):
        return all(stack.is_stack_complete() for stack in self.stacks)

    def is_position_delivery(self, position):
        for stack in self.stacks:
            if stack.is_position_delivery(position):
                return True

        return False
