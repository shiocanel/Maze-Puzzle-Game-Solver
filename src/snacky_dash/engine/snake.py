class Snake:

    def __init__(self, positions, colors):
        self.snake_positions = tuple(positions)
        self.colors = tuple(colors)

        if len(self.snake_positions) - 1 != len(self.colors):
            raise ValueError("Error length positions should equal length colors + 1")

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
        return Snake(new_positions, self.colors)

    def grow_snake(self, new_head, color):
        new_body = self.snake_positions
        new_positions = (tuple(new_head),) + new_body

        new_colors = self.colors + ((color),)
        return Snake(new_positions, new_colors)

    def count_color(self, color):
        return self.colors.count(color)
