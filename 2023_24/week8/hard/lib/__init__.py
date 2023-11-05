import random

import pygame as pg

from . import ai
from .entity import Entity
from .map import SIZE, MAP, WIDTH, HEIGHT

MAX_ENTITIES = 50


class Application:
    def __init__(self, ai_handler):
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption("CompSoc Doom")
        self.clock = pg.time.Clock()
        self.handle_ai = ai_handler
        self.entities = []

    def run(self):
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            self.render()
            self.update()
            self.clock.tick(60)

    def render(self):
        self.screen.fill("black")

        for wall in MAP:
            wall.render(self.screen)
        for entity in self.entities:
            entity.render(self.screen)

        pg.display.flip()

    def update(self):
        if len(self.entities) < MAX_ENTITIES and random.random() < 0.1:
            self.entities.append(Entity((WIDTH // 2, HEIGHT // 2 - 10), ai.any()))
        for entity in self.entities:
            entity.update(
                MAP,
                [e for e in self.entities if e.is_enemy != entity.is_enemy]
                + [Entity(pg.mouse.get_pos(), None)],
            )

    def teardown(self):
        pg.quit()


def main(ai_handler):
    app = Application(ai_handler)
    try:
        app.run()
    finally:
        app.teardown()
