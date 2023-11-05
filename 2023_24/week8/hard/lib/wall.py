import pygame as pg


class Wall:
    def __init__(self, a: tuple[int, int], b: tuple[int, int]) -> None:
        self.a = a
        self.b = b

    def render(self, surface: pg.Surface):
        pg.draw.line(surface, "green", self.a, self.b)
