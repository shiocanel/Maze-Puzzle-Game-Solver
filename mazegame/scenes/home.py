from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame

import config
from level import Cell, Level, parse_level
from scenes.base import Scene
from ui import Button

if TYPE_CHECKING:
    from mazegame.app import App

HERO_LEVEL = """
#########
#S..#..F#
#.#.#.#.#
#.#...#.#
#.#####.#
#F....#.#
###.#.#.#
#T..#..T#
#########
"""

CELL = 36
HERO_TOP = 165

class HomeScene(Scene):
    def __init__(self, app: App) -> None:
        super().__init__(app)
        self.time = 0.0
        self.level: Level = parse_level(HERO_LEVEL)

        self.title_font = pygame.font.Font(None, 84)
        self.subtitle_font = pygame.font.Font(None, 28)
        self.button_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 22)

        width, _ = app.screen.get_size()
        button_w, button_h, gap = 340, 56, 14
        x = (width - button_w) // 2
        y = HERO_TOP + CELL * self.level.height + 40

        def rect(row: int) -> pygame.Rect:
            return pygame.Rect(x, y + row * (button_h + gap), button_w, button_h)

        self.buttons = [
            Button("Play", rect(0), enabled=False, hint="soon"),
            Button("Level Editor", rect(1), enabled=False, hint="soon"),
            Button("Quit", rect(2), on_click=app.quit),
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.quit()
            return
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt: float) -> None:
        self.time += dt

    def draw(self, screen: pygame.Surface) -> None:
        width, height = screen.get_size()
        screen.fill(config.BG)

        self._draw_centered(screen, self.title_font, config.GAME_TITLE, 70, shadow=True)
        self._draw_centered(screen, self.subtitle_font, config.TAGLINE, 120, color=config.TEXT_DIM)

        self._draw_hero(screen)

        for button in self.buttons:
            button.draw(screen, self.button_font, self.small_font)

        footer = "ESC to quit"
        self._draw_centered(screen, self.small_font, footer, height - 22, color=config.TEXT_DIM)

    def _draw_centered(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        y: int,
        color: tuple[int, int, int] = config.TEXT,
        shadow: bool = False,
    ) -> None:
        center_x = screen.get_width() // 2
        if shadow:
            surf = font.render(text, True, config.SHADOW)
            screen.blit(surf, surf.get_rect(center=(center_x + 3, y + 4)))
        surf = font.render(text, True, color)
        screen.blit(surf, surf.get_rect(center=(center_x, y)))

    def _cell_rect(self, origin: tuple[int, int], cell: Cell) -> pygame.Rect:
        return pygame.Rect(origin[0] + cell[0] * CELL, origin[1] + cell[1] * CELL, CELL, CELL)

    def _draw_hero(self, screen: pygame.Surface) -> None:
        level = self.level
        pad = 10
        panel_w, panel_h = CELL * level.width, CELL * level.height
        origin = ((screen.get_width() - panel_w) // 2, HERO_TOP)

        panel = pygame.Rect(origin, (panel_w, panel_h)).inflate(pad * 2, pad * 2)
        pygame.draw.rect(screen, config.PANEL, panel, border_radius=18)

        for y in range(level.height):
            for x in range(level.width):
                if (x, y) not in level.walls:
                    r = self._cell_rect(origin, (x, y)).inflate(-4, -4)
                    pygame.draw.rect(screen, config.FLOOR, r, border_radius=8)

        for index, cell in enumerate(sorted(level.fruits)):
            self._draw_fruit(screen, self._cell_rect(origin, cell), index)
        for cell in sorted(level.trucks):
            self._draw_truck(screen, self._cell_rect(origin, cell))

        sx, sy = level.start
        body = [(sx + i, sy) for i in range(3)]
        self._draw_snake(screen, [self._cell_rect(origin, c) for c in body])

    def _draw_fruit(self, screen: pygame.Surface, cell: pygame.Rect, index: int) -> None:
        bob = math.sin(self.time * 3 + index * 1.7) * 2
        cx, cy = cell.centerx, cell.centery + bob
        color = config.FRUIT_COLORS[index % len(config.FRUIT_COLORS)]
        radius = int(CELL * 0.26)
        pygame.draw.circle(screen, color, (cx, cy), radius)
        pygame.draw.rect(
            screen, config.FRUIT_STEM, (cx - 1, cy - radius - 4, 3, 6), border_radius=1
        )

    def _draw_truck(self, screen: pygame.Surface, cell: pygame.Rect) -> None:
        body = pygame.Rect(0, 0, int(CELL * 0.74), int(CELL * 0.46))
        body.center = (cell.centerx, cell.centery - 1)
        pygame.draw.rect(screen, config.TRUCK, body, border_radius=5)
        cab = pygame.Rect(
            body.right - int(CELL * 0.24), body.top + 3, int(CELL * 0.2), body.height - 6
        )
        pygame.draw.rect(screen, config.TRUCK_CAB, cab, border_radius=3)
        for wheel_x in (body.left + 7, body.right - 8):
            pygame.draw.circle(screen, config.TRUCK_WHEEL, (wheel_x, body.bottom), 4)

    def _draw_snake(self, screen: pygame.Surface, cells: list[pygame.Rect]) -> None:
        radius = int(CELL * 0.36)
        for a, b in zip(cells, cells[1:], strict=False):
            link = pygame.Rect(
                min(a.centerx, b.centerx),
                a.centery - radius,
                abs(a.centerx - b.centerx),
                radius * 2,
            )
            pygame.draw.rect(screen, config.SNAKE, link)
        for cell in cells:
            pygame.draw.circle(screen, config.SNAKE, cell.center, radius)

        head = cells[-1]
        for dy in (-6, 6):
            eye = (head.centerx + 5, head.centery + dy)
            pygame.draw.circle(screen, config.SNAKE_EYE, eye, 4)
            pygame.draw.circle(screen, config.SNAKE_PUPIL, (eye[0] + 1, eye[1]), 2)
