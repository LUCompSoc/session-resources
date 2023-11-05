from __future__ import annotations

import math
from collections import deque
from enum import Enum, auto

import pygame as pg

from .wall import Wall


MAX_HISTORY_LENGTH = 10


class Action(Enum):
    MOVE_FORWARD = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()


class Entity:
    def __init__(self, pos: tuple[int, int], ai, is_enemy: bool = True) -> None:
        self.ai = ai
        self.__pos = pos
        self.__heading = 0
        self.__health = 10
        self.radius = 5
        self.is_enemy = is_enemy
        self.action_history = deque()

    def render(self, surface: pg.Surface):
        pg.draw.circle(
            surface, "red" if self.is_enemy else "blue", self.__pos, self.radius
        )
        move_amount = int(self.radius * 0.5)
        x, y = self.pos
        pg.draw.line(
            surface,
            "white",
            self.pos,
            (
                x + move_amount * math.cos(self.heading) * 4,
                y + move_amount * math.sin(self.heading) * 4,
            ),
        )

    def update(self, walls: list[Wall], opponents: list[Entity], allies: list[Entity]):
        x, y = old_x, old_y = self.__pos
        move_amount = int(self.radius * 0.5)
        action = self.ai(self, walls, opponents)
        match action:
            case Action.MOVE_FORWARD:
                x += move_amount * math.cos(self.__heading)
                y += move_amount * math.sin(self.__heading)
            case Action.MOVE_LEFT:
                x += move_amount * math.cos(self.__heading + math.pi / 2)
                y += move_amount * math.sin(self.__heading + math.pi / 2)
            case Action.MOVE_RIGHT:
                x += move_amount * math.cos(self.__heading - math.pi / 2)
                y += move_amount * math.sin(self.__heading - math.pi / 2)
            case Action.TURN_LEFT:
                self.__heading += 0.1
            case Action.TURN_RIGHT:
                self.__heading -= 0.1
        for e in opponents:
            if self.collides_with_entity(e):
                self.__health -= 0.5
                e.__health -= 0.5
        for e in allies:
            if e is not self and self.collides_with_entity(e):
                self.__health -= 0.5
                e.__health -= 0.5
        self.action_history.append(action)
        if len(self.action_history) > MAX_HISTORY_LENGTH:
            self.action_history.popleft()
        self.__pos = x, y
        if not any(self.collides_with_wall(w) for w in walls):
            return
        self.__pos = old_x, y
        if not any(self.collides_with_wall(w) for w in walls):
            return
        self.__pos = x, old_y
        if not any(self.collides_with_wall(w) for w in walls):
            return
        self.__pos = old_x, old_y

    def collides_with_wall(self, wall: Wall) -> bool:
        if wall.a[0] == wall.b[0]:
            # vertical
            aligned_axis = abs(self.__pos[0] - wall.a[0]) < self.radius
            min_off_axis = self.__pos[1] + self.radius > min(wall.a[1], wall.b[1])
            max_off_axis = self.__pos[1] - self.radius < max(wall.a[1], wall.b[1])
        elif wall.a[1] == wall.b[1]:
            # y collision
            aligned_axis = abs(self.__pos[1] - wall.a[1]) < self.radius
            min_off_axis = self.__pos[0] + self.radius > min(wall.a[0], wall.b[0])
            max_off_axis = self.__pos[0] - self.radius < max(wall.a[0], wall.b[0])
        else:
            raise NotImplementedError("diagonal line")
        return aligned_axis and min_off_axis and max_off_axis

    def collides_with_entity(self, entity: Entity) -> bool:
        sx, sy = self.pos
        ox, oy = entity.pos
        return (sx - ox) ** 2 + (sy - oy) ** 2 <= (self.radius + entity.radius) ** 2

    @property
    def pos(self):
        return self.__pos

    @property
    def heading(self):
        return self.__heading

    @property
    def health(self):
        return self.__health
