import math

from game.config import *

def percent_display(x, y):
    return [
        round(DISPLAY_SIZE[0]*x),
        round(DISPLAY_SIZE[1]*y)
    ]

def percent_world(x, y):
    return [
        round(WORLD_BOUNDS[0]*x),
        round(WORLD_BOUNDS[1]*y)
    ]

def world_to_display(x, y):
    percent_of_world = [
        x/float(WORLD_BOUNDS[0]),
        y/float(WORLD_BOUNDS[1])
    ]

    return [
        round(percent_of_world[0] * DISPLAY_SIZE[0]),
        round(percent_of_world[1] * DISPLAY_SIZE[1])
    ]

def display_to_world(x, y):
    percent_of_display = [
        x/float(DISPLAY_SIZE[0]),
        y/float(DISPLAY_SIZE[1])
    ]

    return [
        round(percent_of_display[0] * WORLD_BOUNDS[0]),
        round(percent_of_display[1] * WORLD_BOUNDS[1])
    ]
