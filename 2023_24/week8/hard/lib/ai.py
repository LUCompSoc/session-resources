import math
import random

from .entity import Action, Entity
from .wall import Wall


def any():
    ais = [random_walk, target_player, target_player, target_player]
    random.shuffle(ais)
    return ais[0]


def random_walk(self, walls: list[Wall], opponents: list[Entity]):
    r = random.randrange(3)
    match r:
        case 0:
            return Action.MOVE_FORWARD
        case 1:
            return Action.TURN_LEFT
        case 2:
            return Action.TURN_RIGHT


def target_player(self: Entity, walls: list[Wall], opponents: list[Entity]):
    # TODO: boids
    px, py = opponents[0].pos
    sx, sy = self.pos
    dx = px - sx
    dy = py - sy
    offset_heading = math.atan2(dy, dx)
    d_heading = (offset_heading - self.heading) % math.tau
    if abs(d_heading) < math.pi / 8:
        return Action.MOVE_FORWARD
    if 0 < d_heading < math.pi:
        return Action.TURN_LEFT
    return Action.TURN_RIGHT
