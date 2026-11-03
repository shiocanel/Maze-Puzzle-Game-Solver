import pygame
from pygame.locals import K_ESCAPE, KEYDOWN
from snacky_dash.engine.level_loader import load_level_from_file
from pathlib import Path

CELL_SIZE = 48
WALL_COLOR = (153, 255, 51)
FLOOR_COLOR = (64, 64, 64)

CART_COLOR = (255, 179, 179)
DELIVERY_COLOR = (255, 128, 0)

RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)
BLUE_COLOR = (102, 102, 255)
GREEN_COLOR = (0, 204, 0)
ORANGE_COLOR = (255, 128, 0)
PURPLE_COLOR = (153, 0, 153)


def draw_grid(screen, grid):
    for r in range(grid.rows):
        for c in range(grid.columns):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid.is_wall((r, c)):
                pygame.draw.rect(screen, WALL_COLOR, rect)
            else:
                pygame.draw.rect(screen, FLOOR_COLOR, rect)


def draw_state(scree, state):
    pass


def main():
    pygame.init()

    level_path = Path("levels/level_02.json")
    try:
        grid, state = load_level_from_file(level_path)
    except FileNotFoundError:
        print(f"Level file not found")
        return

    screen_width = grid.columns * CELL_SIZE
    screen_height = grid.rows * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snacky Dash")

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        draw_grid(screen, grid)

        pygame.display.flip()


if __name__ == "__main__":
    main()
