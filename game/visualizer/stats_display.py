import sys
import math
import random

import pygame
from pygame.locals import *

from game.config import *

def test():

    pygame.init()
    fpsClock = pygame.time.Clock()

    global_surf = pygame.display.set_mode(DISPLAY_SIZE)
    #global_surf.fill(pygame.Color(255,255,255))
    global_surf.fill(pygame.Color(0,0,0))

    show_stats_display(None, global_surf, fpsClock)

    sys.exit()


def show_stats_display(stats, window_surf, clock):

    initial_screen = window_surf.copy()

    n = 3000

    hist = Histogram(500, 802, 50, 50, [
        [math.sin(i/100)+1 for i in range(n)],
        [math.cos(i/100)+1 for i in range(n)],
        [math.cos(i/100 + math.pi)+1 for i in range(n)],
        [math.sin(i/100 + math.pi)+1 for i in range(n)],
        [math.pow(i/1000, 1/2)+1 for i in range(n)],
        [math.pow(1/2, i/100)+1 for i in range(n)],
        [(i/n)*2 for i in range(n)],
        [(1-(i/n))*2 for i in range(n)],
    ] )

    graphs = pygame.sprite.Group()
    graphs.add(hist)

    graphs.update()

    close = False
    while not close:

        graphs.draw(window_surf)


        #
        # Handle Events
        #
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    close = True
                    break

        pygame.display.update()
        clock.tick(30)


    # show initial screen to transition back to game
    window_surf.blit(initial_screen, (0,0))
    pygame.display.update()
    clock.tick(30)



class Histogram(pygame.sprite.Sprite):

    def __init__(self, height, width, x, y, points):
        super().__init__()

        self.points = points

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.colors = [
            pygame.Color(0,255,0),
            pygame.Color(255,0,0),
            pygame.Color(155,155,0),
            pygame.Color(155,0,155),
            pygame.Color("#D4A190"),
            pygame.Color("#C390D4"),
            pygame.Color("#FFAE00"),
            pygame.Color("#A34400"),
        ]

    def update(self):

        # draw boundaries of graph
        self.image.fill(pygame.Color(0,0,0))

        horiz_margin = 0.05
        vert_margin = 0.05

        self.canvas_rect = pygame.Rect(
            self.rect.w * horiz_margin + 2,
            2,
            self.rect.w - math.ceil(self.rect.w * horiz_margin) - 3,
            self.rect.h - math.ceil(self.rect.h * vert_margin) - 3,
        )

        self.image.fill(pygame.Color(0,100,100), (self.canvas_rect.x-2, self.canvas_rect.y-2, self.canvas_rect.w+4, self.canvas_rect.h+4))
        self.image.fill(pygame.Color(0,0,0), (self.canvas_rect.x, self.canvas_rect.y, self.canvas_rect.w, self.canvas_rect.h))

        # draw points
        max_y = float(max( max(point_set) for point_set in self.points ))
        max_x = float(max( len(point_set) for point_set in self.points ))

        print(max_y)

        for color_id, point_set in enumerate(self.points):
            for idx, pt in enumerate(point_set):
                ## project point to graph coordinates
                percent_x = (idx+1) / (max_x+1)
                percent_y = pt / (max_y)

                x = math.floor(self.canvas_rect.w * percent_x) + (self.rect.w * horiz_margin)
                y = self.canvas_rect.h - math.floor((self.canvas_rect.h) * percent_y)

                self.image.fill(self.colors[color_id], (x+1, y+1, 1, 1) )






