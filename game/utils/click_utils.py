import pygame

from game.universe_config import *
from game.utils.projection import *
from game.common.enums import *

STATIC_OBJS = [
 *STATION_DEFINITIONS,
 *ASTEROID_FIELD_DEFINITIONS
]

def get_static_obj_near_pos(pos, radius = 40, first=False, obj_type=None):

    hits = []

    for obj in STATIC_OBJS:
        if obj_type is None or (obj_type is not None and obj_type == obj["type"]):
            obj_pos = world_to_display(*obj["position"])
            rect = pygame.Rect(obj_pos[0]-(radius/2), obj_pos[1]-(radius/2), radius, radius)

            if rect.collidepoint(pos):
                if first: return obj
                hits.append(obj)

    if first: return None
    return hits


def get_ship_near_pos(pos, universe, radius=40, first=False):

    hits = []

    for obj in filter(lambda e: e.object_type == ObjectType.ship, universe):
        obj_pos = world_to_display(*obj.position)
        rect = pygame.Rect(obj_pos[0]-(radius/2), obj_pos[1]-(radius/2), radius, radius)

        if rect.collidepoint(pos):
            if first:
                return obj
            hits.append(obj)

    if first: return None
    return hits








