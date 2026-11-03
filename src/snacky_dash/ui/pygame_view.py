import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from snacky_dash.engine.level_loader import load_level_from_file
from pathlib import Path

CELL_SIZE = 48
WALL_COLOR = (153, 255, 51)
FLOOR_COLOR = (64, 64, 64)

CART_COLOR = (255, 179, 179)
FULL_CART_COLOR = (255, 119, 0)
DELIVERY_COLOR = (255, 128, 0)
INACTIVE_DELIVERY_COLOR = (120, 120, 120)

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


def draw_centered_rounded_square(screen, color, position, size=30, border_radius=6):
    r, c = position

    x = c * CELL_SIZE + (CELL_SIZE - size) // 2
    y = r * CELL_SIZE + (CELL_SIZE - size) // 2

    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)


def draw_delivery_cell(screen, deliv_pos, active=True):
    r, c = deliv_pos
    x = c * CELL_SIZE
    y = r * CELL_SIZE
    color = DELIVERY_COLOR if active else INACTIVE_DELIVERY_COLOR

    pygame.draw.polygon(
        screen,
        color,
        (
            (x, y),
            (x + 10, y),
            (x, y + 10),
        ),
    )

    pygame.draw.polygon(
        screen,
        color,
        (
            (x + CELL_SIZE, y),
            (x + CELL_SIZE - 10, y),
            (x + CELL_SIZE, y + 10),
        ),
    )

    pygame.draw.polygon(
        screen,
        color,
        (
            (x, y + CELL_SIZE - 1),
            (x + 10, y + CELL_SIZE - 1),
            (x, y + CELL_SIZE - 11),
        ),
    )

    pygame.draw.polygon(
        screen,
        color,
        (
            (x + CELL_SIZE - 1, y + CELL_SIZE),
            (x + CELL_SIZE - 11, y + CELL_SIZE - 1),
            (x + CELL_SIZE - 1, y + CELL_SIZE - 10),
        ),
    )
    draw_centered_rounded_square(
        screen,
        ORANGE_COLOR if active else INACTIVE_DELIVERY_COLOR,
        deliv_pos,
        size=20,
        border_radius=6,
    )


def draw_state(screen, state):
    for cart_stack in state.stacks:
        if cart_stack.is_stack_complete():
            for pos in cart_stack.carts[0].cart_positions:
                rect = pygame.Rect(
                    (pos[1]) * CELL_SIZE,
                    (pos[0]) * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                pygame.draw.rect(screen, FULL_CART_COLOR, rect)
            draw_delivery_cell(
                screen, cart_stack.carts[0].delivery_position, active=False
            )
            continue

        active_cart = cart_stack.get_active_cart()

        for pos in active_cart.cart_positions:
            rect = pygame.Rect(
                (pos[1]) * CELL_SIZE,
                (pos[0]) * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )

            pygame.draw.rect(screen, CART_COLOR, rect)

        draw_delivery_cell(screen, active_cart.delivery_position, active=True)


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
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        screen.fill(WALL_COLOR)
        draw_grid(screen, grid)
        draw_state(screen, state)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
