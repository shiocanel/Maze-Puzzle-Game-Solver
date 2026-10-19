from __future__ import annotations

import pygame

import config
from scenes.base import Scene
from scenes.home import HomeScene

class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(config.GAME_TITLE)
        self.screen = pygame.display.set_mode(config.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene: Scene = HomeScene(self)

    def change_scene(self, scene: Scene) -> None:
        self.scene = scene

    def quit(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.scene.handle_event(event)
            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

def main() -> None:
    App().run()
