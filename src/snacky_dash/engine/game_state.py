# class GameState:
#     def __init__(self, snake, fruits, carts) -> None:
#         self.snake = snake
#         self.fruits = dict(fruits)
#         self.carts = tuple(carts)

#     def get_fruit_at(self, position):
#         return self.fruits.get(position)

#     def remove_fruit_at(self, position):
#         new_fruits = self.fruits.pop(position)

#         return GameState(self.snake, new_fruits, self.carts)

    