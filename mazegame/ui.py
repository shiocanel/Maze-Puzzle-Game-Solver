from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pygame

import config

@dataclass
class Button:
    label: str
    rect: pygame.Rect
    on_click: Callable[[], None] | None = None
    enabled: bool = True
    hint: str = ""
    hovered: bool = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.enabled and self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.enabled and self.on_click and self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        hint_font: pygame.font.Font,
    ) -> None:
        if not self.enabled:
            fill, text_color = config.BUTTON_DISABLED, config.TEXT_DIM
        elif self.hovered:
            fill, text_color = config.BUTTON_HOVER, config.TEXT
        else:
            fill, text_color = config.BUTTON, config.TEXT

        shadow = self.rect.move(0, 4)
        pygame.draw.rect(surface, config.SHADOW, shadow, border_radius=16)
        pygame.draw.rect(surface, fill, self.rect, border_radius=16)

        label = font.render(self.label, True, text_color)
        surface.blit(label, label.get_rect(midleft=(self.rect.left + 28, self.rect.centery)))

        if self.hint:
            hint = hint_font.render(self.hint, True, config.TEXT_DIM)
            surface.blit(hint, hint.get_rect(midright=(self.rect.right - 20, self.rect.centery)))
