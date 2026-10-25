CAPACITY = 9


class Cart:
    def __init__(
        self, color, top_left_position, delivery_position, loaded_count=0
    ) -> None:
        self.color = color
        self.top_left_position = top_left_position
        self.delivery_position = delivery_position
        self.loaded_count = loaded_count

        self.cart_positions = ()
        for i in range(top_left_position[0], top_left_position[0] + 3):
            for j in range(top_left_position[1], top_left_position[1] + 3):
                self.cart_positions = self.cart_positions + ((i, j),)

    def free_spaces(self):
        return CAPACITY - self.loaded_count

    def is_full(self):
        return CAPACITY == self.loaded_count

    def load(self, count):
        new_loaded_count = min(count + self.loaded_count, CAPACITY)

        return Cart(
            self.color, self.top_left_position, self.delivery_position, new_loaded_count
        )

    def is_position_part_of_cart(self, position):
        return position in self.cart_positions

    def is_position_delivery(self, position):
        return position == self.delivery_position
