from pathlib import Path
from snacky_dash.engine.level_loader import load_level_from_file
from snacky_dash.engine.direction import Direction
from snacky_dash.engine.movement import slide
from snacky_dash.engine.color import Color


def test_level_02_solve_right():
    test_dir = Path(__file__).parent
    level_path = test_dir.parent / "levels" / "level_02.json"

    grid, state = load_level_from_file(level_path)
    final_state = slide(state, grid, Direction.RIGHT)

    assert final_state is not None
    assert final_state.snake.get_head_position() == (6, 2)
    assert final_state.snake.get_length() == 2
    assert final_state.snake.colors == (Color.BLUE,)
    assert final_state.stacks[0].total_loaded() == 1
    assert final_state.get_fruit_at((1, 4)) is None
    assert final_state.get_fruit_at((4, 7)) is None