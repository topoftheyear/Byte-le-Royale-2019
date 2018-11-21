
import math
import random

import pygame

from game.visualizer.spritesheet_functions import SpriteSheet
from game.common.enums import *
from game.utils.projection import *


class IllegalSalvageSprite(pygame.sprite.DirtySprite):
    def __init__(self, x, y, id):
        super().__init__()

        self.id = id

        self.image = pygame.Surface((2, 2))

        self.image.fill(pygame.Color(255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.center = world_to_display(x, y)


    def update(self, universe, group):

        obj = self.find_self(universe)
        if not obj:
            group.remove(self)


    def find_self(self, universe):
        for obj in universe:
            if obj.object_type == ObjectType.illegal_salvage and obj.id == self.id:
                return obj
        return None

