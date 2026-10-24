class Snake:
    def __init__(self, positions):
        self.snake_positions = tuple(positions)

    def is_position_part_of_snake(self, position):
        return position in self.snake_positions

    def is_position_part_of_body(self, position):
        body = self.snake_positions[1:]
        return position in body

    def head_hit_body(self):
        head_position = self.get_head_position()
        return self.is_position_part_of_body(head_position)

    def get_length(self):
        return len(self.snake_positions)

    def get_head_position(self):
        return self.snake_positions[0]

    def get_tail_position(self):
        return self.snake_positions[-1]

    def move_snake(self, new_head):
        new_body = self.snake_positions[:-1]
        new_positions = (tuple(new_head),) + new_body
        return Snake(new_positions)

    def grow_snake(self, new_head):
        new_body = self.snake_positions
        new_positions = (tuple(new_head),) + new_body
        return Snake(new_positions)
