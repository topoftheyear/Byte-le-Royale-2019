import math
import random

import pygame

import ptext

class FloatingNumber(pygame.sprite.Sprite):
    def __init__(self, x, y, value, color, size=18):
        super().__init__()
        self.size = size
        self.value = value
        self.color = color
        self.image = pygame.Surface((1,1))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.counter = 20
        self.delay = 0
        self.y = y

        self.direction = random.choice([-1, 1])

    def update(self, group):

        if self.delay > 0:
            self.delay -= 1
            return

        if self.counter > 0:
            c = self.counter * self.direction
            y = ((((self.counter * 0.75)-10) ** 2) + 2 * (self.counter * 0.75) + 0)
            self.rect.topleft = (self.rect.x+(4 * self.direction), y+self.y)
        else:
            if self in group.sprites():
                group.remove(self)


        alpha = math.floor( (self.counter/20) * 255 )


        self.image = ptext.draw(self.value, (0,0), color=self.color, owidth=1.0, ocolor=(0, 0, 0), alpha=alpha/255, fontsize=self.size, fontname='game/visualizer/assets/joystix/joystix monospace.ttf')[0]

        self.counter -= 1
