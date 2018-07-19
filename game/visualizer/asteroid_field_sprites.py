import math

import pygame

from game.visualizer.spritesheet_functions import SpriteSheet
from game.common.enums import *
from game.utils.projection import *

class AsteroidFieldSpriteSheet(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_data, x, y, color):
        super().__init__()

        sprite_sheet = SpriteSheet("game/visualizer/assets/simple_asteroid_field.png")

        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.image_cache = self.image

        # Colorizing asteroid field
        self.color = pygame.Color(
            color.r,
            color.g,
            color.b,
            255
        )

        d = 60
        self.color_2 = pygame.Color(
            self.color.r if self.color.r-d < 0 else self.color.r-d,
            self.color.g if self.color.g-d < 0 else self.color.g-d,
            self.color.b if self.color.b-d < 0 else self.color.b-d,
            255
        )

        d = 100
        self.color_3 = pygame.Color(
            self.color.r if self.color.r-d < 0 else self.color.r-d,
            self.color.g if self.color.g-d < 0 else self.color.g-d,
            self.color.b if self.color.b-d < 0 else self.color.b-d,
            255
        )

        pa = pygame.PixelArray(self.image)
        pa.replace(pygame.Color("#ffffff"), self.color)
        pa.replace(pygame.Color("#a5a5a5"), self.color_2)
        pa.replace(pygame.Color("#3c3c3c"), self.color_3)
        del pa


        self.rect = self.image.get_rect()
        self.rect.center = world_to_display(x,y)




class IroniumFieldSprite(AsteroidFieldSpriteSheet):
    def __init__(self, x, y):
        AsteroidFieldSpriteSheet.__init__(self, [
            0, 0,
            128,128
        ], x, y, pygame.Color(117, 111, 100))


def get_asteroid_field_sprite(object_type, x, y):
    if object_type == ObjectType.ironium_field:
        return IroniumFieldSprite(x, y)
