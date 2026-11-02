from snacky_dash.engine.level_loader import load_level_from_dict
from snacky_dash.engine.color import Color


def test_load_level_from_dict():
    sample_dict = {
        "grid": [
            "#########",
            "#.......#",
            "#.......#",
            "#.......#",
            "#.......#",
            "#.......#",
            "#########"
        ],
        "snake": [5, 6],
        "fruits": [
            {"position": [5, 4], "color": "RED"},
            {"position": [3, 6], "color": "BLUE"}
        ],
        "stacks": [
            {
                "top_left": [1, 1],
                "delivery": [4, 2],
                "colors": ["RED", "BLUE"]
            }
        ]
    }

    grid, game_state = load_level_from_dict(sample_dict)

    assert grid.rows == 7
    assert grid.columns == 9
    assert game_state.snake.get_head_position() == (5, 6)
    assert game_state.get_fruit_at((5, 4)) == Color.RED
    assert game_state.get_fruit_at((3, 6)) == Color.BLUE
    assert game_state.get_stack_at((2, 2)) is not None
    assert game_state.is_won() is False