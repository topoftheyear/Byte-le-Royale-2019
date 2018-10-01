import sys
import math
import random

import pygame
from pygame.locals import *

from game.config import *

def test():

    pygame.init()
    pygame.font.init()
    fpsClock = pygame.time.Clock()

    global_surf = pygame.display.set_mode(DISPLAY_SIZE)
    #global_surf.fill(pygame.Color(255,255,255))
    global_surf.fill(pygame.Color(0,0,0))

    n = 3000
    show_station_stats_display({
        "a": [math.sin(i/100)+1 for i in range(n)],
        "b": [math.cos(i/100)+1 for i in range(n)],
        "c": [math.cos(i/100 + math.pi)+1 for i in range(n)],
        "d": [math.sin(i/100 + math.pi)+1 for i in range(n)],
        "e": [math.pow(i/1000, 1/2)+1 for i in range(n)],
        "f": [math.pow(1/2, i/100)+1 for i in range(n)],
        "g": [(i/n)*2 for i in range(n)],
        "h": [(1-(i/n))*2 for i in range(n)],
    }, global_surf, fpsClock)

    sys.exit()


def show_station_stats_display(plot_name, stats, window_surf, clock):
    initial_screen = window_surf.copy()
    window_surf.fill(pygame.Color(0,0,0))

    hist = Histogram(1000, 500, 50, 50, stats)
    graphs = pygame.sprite.Group()
    graphs.add(hist)

    font_name = pygame.font.get_default_font()
    font = pygame.font.Font(font_name, 16)

    plot_name_surf = font.render(plot_name, True, pygame.Color(0, 155, 0))
    window_surf.blit(plot_name_surf, (20,20))

    go_back_surf = font.render(f"Esc to go back", True, pygame.Color(0, 155, 0))
    window_surf.blit(go_back_surf, (550, 700))

    close = False
    while not close:
        graphs.update()
        graphs.draw(window_surf)

        # Handle Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    close = True
                    break

                hist.keydown_listener(event)

        pygame.display.update()
        clock.tick(30)


    # show initial screen to transition back to game
    window_surf.blit(initial_screen, (0,0))
    pygame.display.update()
    clock.tick(30)


def show_material_stats_display(plot_name, stats, window_surf, clock):
    initial_screen = window_surf.copy()
    window_surf.fill(pygame.Color(0,0,0))

    hist = Histogram(1000, 500, 50, 50, stats)
    graphs = pygame.sprite.Group()
    graphs.add(hist)

    font_name = pygame.font.get_default_font()
    font = pygame.font.Font(font_name, 16)

    plot_name_surf = font.render(plot_name, True, pygame.Color(0, 155, 0))
    window_surf.blit(plot_name_surf, (20,20))

    font_name = pygame.font.get_default_font()
    font = pygame.font.Font(font_name, 20)
    go_back_surf = font.render(f"Esc to go back", True, pygame.Color(0, 155, 0))
    window_surf.blit(go_back_surf, (550, 700))

    close = False
    while not close:
        graphs.update()
        graphs.draw(window_surf)


        # Handle Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    close = True
                    break

                hist.keydown_listener(event)

        pygame.display.update()
        clock.tick(30)


    # show initial screen to transition back to game
    window_surf.blit(initial_screen, (0,0))
    pygame.display.update()
    clock.tick(30)


def material_stats_selection_screen(stats, window_surf, clock):
    initial_screen = window_surf.copy()
    window_surf.fill(pygame.Color(0,0,0))

    font_name = pygame.font.get_default_font()
    font = pygame.font.Font(font_name, 20)

    y_offset = 25
    y_margin = 150
    x_margin = 525
    char_lut = {}


    text_surf = font.render(f"Select a material to view statistics on.", True, pygame.Color(0, 155, 0))
    window_surf.blit(text_surf, (x_margin-100, y_margin+(-2*y_offset)))

    for i, material in enumerate(stats.keys()):

        char = chr(97+i)
        char_lut[char] = material

        text_surf = font.render(f"{char}) {material}", True, pygame.Color(0, 155, 0))
        window_surf.blit(text_surf, (x_margin, y_margin+(i*y_offset)))

    text_surf = font.render(f"Esc to go back", True, pygame.Color(0, 155, 0))
    window_surf.blit(text_surf, (550, 700))

    close = False
    while not close:
        # draw here

        # Handle Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    close = True
                    break

                for k in char_lut.keys():
                    if event.key == eval(f"K_{k}"):
                        material = char_lut[k]
                        show_material_stats_display(f"{material} Buy vs Sell", stats[material], window_surf, clock)

        pygame.display.update()
        clock.tick(30)

    # show initial screen to transition back to game
    window_surf.blit(initial_screen, (0,0))
    pygame.display.update()
    clock.tick(30)


class Histogram(pygame.sprite.Sprite):

    def __init__(self, height, width, x, y, stats):
        super().__init__()

        self.image = pygame.Surface((height, width))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.stats = stats

        self.enabled_plots = [ True for k in stats.keys() ]

        self.names = sorted(self.stats.keys())


        self.colors = [
            pygame.Color(0,255,0),
            pygame.Color(255,0,0),
            pygame.Color(155,155,0),
            pygame.Color(155,0,155),
            pygame.Color("#D4A190"),
            pygame.Color("#C390D4"),
            pygame.Color("#FFAE00"),
            pygame.Color("#A34400"),
            pygame.Color("#FF00C3"),
            pygame.Color("#C3FF00"),
            pygame.Color("#00FFBC"),
        ]

        self.dirty = True

    def update(self):

        if not self.dirty: return
        else:
            self.dirty = False

        self.enabled_plots = [ (enabled and len(self.stats[name]) > 0)  for name, enabled in zip(self.names, self.enabled_plots) ]

        points = [ self.stats[name] for name, enabled in zip(self.names, self.enabled_plots) if enabled ]
        colors = [ color for color, enabled in zip(self.colors, self.enabled_plots) if enabled ]

        # disable plots without points


        # draw boundaries of graph
        self.image.fill(pygame.Color(0,0,0))

        left_margin = 0.05
        right_margin = 0.3
        vert_margin = 0.05

        self.canvas_rect = pygame.Rect(
            (self.rect.w * left_margin) + 2,
            2,
            self.rect.w - math.ceil(self.rect.w * right_margin) - 3,
            self.rect.h - math.ceil(self.rect.h * vert_margin) - 3,
        )

        self.image.fill(pygame.Color(0,100,100), (self.canvas_rect.x-2, self.canvas_rect.y-2, self.canvas_rect.w+4, self.canvas_rect.h+4))
        self.image.fill(pygame.Color(0,0,0), (self.canvas_rect.x, self.canvas_rect.y, self.canvas_rect.w, self.canvas_rect.h))

        font_name = pygame.font.get_default_font()
        font = pygame.font.Font(font_name, 14)

        if len(points) == 0:
            return
        if len(points[0]) == 0:
            return

        if len(points) == 0:
            max_y = 10
            max_x = 10
        else:
            max_y = float(max( max(point_set) for point_set in points ))
            max_x = float(max( len(point_set) for point_set in points ))

        # draw ticks
        ## horizontal ticks
        offset = self.rect.w * left_margin
        for y_pos in [(self.canvas_rect.h/10)*i for i in  range(0, 11)]:

            # Draw label
            percent_y = 1.0 - y_pos / self.canvas_rect.h
            text_surf = font.render("{0:02d}".format(math.floor(percent_y*max_y)), True, pygame.Color(0, 100, 100))
            self.image.blit(text_surf, (0, y_pos))

            # Draw tick
            pygame.draw.line(self.image, pygame.Color(0, 50, 50), (offset, y_pos), (self.canvas_rect.x+self.canvas_rect.w, y_pos), 1)


        ## vertical ticks
        for x_pos in [(self.canvas_rect.w/10)*i for i in  range(0, 10)]:
            # Draw label
            percent_x =  x_pos / self.canvas_rect.h
            text_surf = font.render("{0:02d}".format(math.floor(percent_x*max_x)), True, pygame.Color(0, 100, 100))
            self.image.blit(text_surf, (x_pos+offset-6, self.canvas_rect.h+15))

            x_pos += self.rect.w * left_margin
            pygame.draw.line(self.image, pygame.Color(0, 50, 50), (x_pos, 0), (x_pos, self.canvas_rect.y+self.canvas_rect.h), 1)


        # draw points
        for color_id, point_set in enumerate(points):
            for idx, pt in enumerate(point_set):
                ## project point to graph coordinates
                percent_x = (idx+1) / (max_x+1)
                percent_y = pt / max(max_y, 1)

                x = math.floor(self.canvas_rect.w * percent_x) + (self.rect.w * left_margin)
                y = self.canvas_rect.h - math.floor((self.canvas_rect.h) * percent_y)

                self.image.fill(colors[color_id], (x+1, y+1, 2, 2) )

        # draw lables
        y_offset = 20


        for i, name, color, enabled in zip(range(0, len(self.names)), self.names, self.colors, self.enabled_plots):
            if len(self.names) >= 10:
                text = f"{chr(i+97)}) {name.replace('_', ' ')}"
            else:
                text = f"{i+1}) {name.replace('_', ' ')}"

            text_surf = font.render(text, True, color)

            if not enabled:
                middle = text_surf.get_rect().h/2
                text_w = text_surf.get_rect().w
                pygame.draw.line(text_surf, color, (0, middle), (text_w, middle))

            text_pos = ( (self.rect.w * left_margin) + self.canvas_rect.w + 20, y_offset * i)

            self.image.blit(text_surf, text_pos)


    def keydown_listener(self, event):
        num_plots = len(list(self.stats.keys()))

        for i in range(num_plots):
            enable = False
            if num_plots >= 10:
                if event.key == eval(f"pygame.K_{chr(i+97)}"):
                    enable = True
            else:
                if event.key == eval(f"pygame.K_{i+1}"):
                    enable = True
            if enable:
                self.enabled_plots[i] = not self.enabled_plots[i]
                self.dirty = True



