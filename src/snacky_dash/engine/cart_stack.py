class CartStack:
    def __init__(self, carts) -> None:
        self.carts = tuple(carts)

    def get_active_cart(self):
        for cart in self.carts:
            if not cart.is_full():
                return cart

        return None

    def is_stack_complete(self):
        complete = True
        for cart in self.carts:
            complete = complete and cart.is_full()

        return complete

    def is_position_part_of_stack(self, position):
        return self.carts[0].is_position_part_of_cart(position)

    def is_position_delivery(self, position):
        return self.carts[0].is_position_delivery(position)

    def load(self, count):
        if self.is_stack_complete():
            return self

        active_idx = 0

        for i, cart in enumerate(self.carts):
            if not cart.is_full():
                active_idx = i
                break

        carts_before = self.carts[:active_idx]
        active_cart = self.carts[active_idx].load(count)
        carts_after = self.carts[active_idx + 1 :]

        new_carts = carts_before + (active_cart,) + carts_after

        return CartStack(new_carts)

    def total_loaded(self):
        return sum(cart.loaded_count for cart in self.carts)
