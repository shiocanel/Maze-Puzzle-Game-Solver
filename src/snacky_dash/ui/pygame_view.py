import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from snacky_dash.engine.level_loader import load_level_from_file
from snacky_dash.engine.color import Color
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

STEM_COLOR = (120, 70, 40)
LEAF_COLOR = (46, 204, 113)
HIGHLIGHT_COLOR = (255, 255, 255)

COLOR_TO_RGB = {
    Color.RED: RED_COLOR,
    Color.YELLOW: YELLOW_COLOR,
    Color.BLUE: BLUE_COLOR,
    Color.GREEN: GREEN_COLOR,
    Color.ORANGE: ORANGE_COLOR,
    Color.PURPLE: PURPLE_COLOR,
}


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

        cart_color_rgb = COLOR_TO_RGB.get(active_cart.color, RED_COLOR)
        draw_cart_border(screen, active_cart, cart_color_rgb, border_width=4)
        draw_delivery_cell(screen, active_cart.delivery_position, active=True)


def draw_cart_border(screen, active_cart, color_rgb, border_width=4):
    r, c = active_cart.top_left_position
    rect = pygame.Rect(
        c * CELL_SIZE,
        r * CELL_SIZE,
        CELL_SIZE * 3,
        CELL_SIZE * 3,
    )
    pygame.draw.rect(screen, color_rgb, rect, width=border_width)


def draw_fruits(screen, state):
    for pos, fruit_color in state.fruits.items():
        center_x = pos[1] * CELL_SIZE + CELL_SIZE // 2
        center_y = pos[0] * CELL_SIZE + CELL_SIZE // 2

        radius = CELL_SIZE // 3
        color_rgb = COLOR_TO_RGB.get(fruit_color, (255, 255, 255))

        pygame.draw.circle(screen, color_rgb, (center_x, center_y), radius)

        highlight_radius = max(2, radius // 4)
        pygame.draw.circle(
            screen,
            HIGHLIGHT_COLOR,
            (center_x - radius // 3, center_y - radius // 3),
            highlight_radius,
        )

        stem_start = (center_x, center_y - radius)
        stem_end = (center_x + 2, center_y - radius - 6)
        pygame.draw.line(screen, STEM_COLOR, stem_start, stem_end, width=3)

        leaf_center = (center_x + 6, center_y - radius - 4)
        pygame.draw.circle(screen, LEAF_COLOR, leaf_center, 4)


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

        draw_grid(screen, grid)
        draw_state(screen, state)
        draw_fruits(screen, state)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
