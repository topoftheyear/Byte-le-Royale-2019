import math

import pygame

import ptext



class TrapText(pygame.sprite.Sprite):

    def __init__(self, y, text):
        super().__init__()


        self.image = ptext.draw(
            text,
            (0,0),
            color=(255, 255, 255),
            owidth=2.0,
            ocolor=(0, 0, 0),
            fontsize=24,
            fontname='game/visualizer/assets/joystix/joystix monospace.ttf')[0]

        self.rect = self.image.get_rect()

        x = math.floor( (1280/2.0) - (self.rect.w/2.0) )

        self.rect.topleft = (x, y)


