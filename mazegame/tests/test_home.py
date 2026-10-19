import pygame
import pytest

from mazegame.app import App
from mazegame.scenes.home import HomeScene


@pytest.fixture
def app():
    instance = App()
    yield instance
    pygame.quit()


def click(app, pos):
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)
    app.scene.handle_event(event)


def button(app, label):
    return next(b for b in app.scene.buttons if b.label == label)


def test_home_is_the_first_scene(app):
    assert isinstance(app.scene, HomeScene)


def test_home_draws_without_errors(app):
    app.scene.update(0.016)
    app.scene.draw(app.screen)


def test_buttons_fit_inside_the_window(app):
    window = app.screen.get_rect()
    for b in app.scene.buttons:
        assert window.contains(b.rect)


def test_quit_button_stops_the_app(app):
    click(app, button(app, "Quit").rect.center)
    assert not app.running


def test_escape_stops_the_app(app):
    app.scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    assert not app.running


def test_disabled_buttons_do_nothing(app):
    for label in ("Play", "Level Editor"):
        click(app, button(app, label).rect.center)
    assert app.running
