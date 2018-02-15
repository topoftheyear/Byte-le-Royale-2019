import math

import pygame


class ProgressBar(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, initial_value, key):
        super().__init__()

        self.maximum = initial_value
        self.current = initial_value

        self.key = key

        self.font_obj = pygame.font.Font('game/visualizer/assets/joystix/joystix monospace.ttf', 12)

        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)

    def update(self, objects):

        current = self.key(objects)

        if current is None:
            return

        # Update health
        if current != self.current:
            self.current = current

            self.image.fill(pygame.Color("#DEDEDE"), (0, 0, self.rect.w, self.rect.h))

            #Draw progress bars
            self.image.fill(pygame.Color("#E0A3FF"),(2, 2, self.rect.w-4, self.rect.h-4))
            self.image.fill(pygame.Color("#AA00FF"),(2, 2, math.floor((self.current/float(self.maximum))*(self.rect.w-4)), self.rect.h-4))

