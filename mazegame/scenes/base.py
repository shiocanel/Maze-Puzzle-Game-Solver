from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from mazegame.app import App


class Scene:
    def __init__(self, app: App) -> None:
        self.app = app

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        ...
        
    def draw(self, screen: pygame.Surface) -> None:
        pass
