import json
from pathlib import Path
from snacky_dash.engine.grid import Grid
from snacky_dash.engine.game_state import GameState
from snacky_dash.engine.snake import Snake
from snacky_dash.engine.cart import Cart
from snacky_dash.engine.cart_stack import CartStack
from snacky_dash.engine.color import Color


def parse_color(color_name):
    return Color[color_name.upper()]


def load_level_from_dict(data):
    grid = Grid(data["grid"])

    snake_pos = tuple(data["snake"])
    snake = Snake((snake_pos,), ())

    fruits = {}
    for entry in data.get("fruits", []):
        pos = tuple(entry["position"])
        color = parse_color(entry["color"])
        fruits[pos] = color

    stacks_tuple = ()
    for s_data in data["stacks"]:
        top_left = tuple(s_data["top_left"])
        delivery = tuple(s_data["delivery"])
        cart_colors = s_data["colors"]
        carts = [
            Cart(parse_color(c), top_left, delivery, loaded_count=0)
            for c in cart_colors
        ]
        stacks_tuple += (CartStack(tuple(carts)),)

    return grid, GameState(snake, fruits, stacks_tuple)


def load_level_from_file(file_path):
    path = Path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return load_level_from_dict(data)