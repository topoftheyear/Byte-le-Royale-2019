import sys, math, random, time

import pygame
from pygame.locals import *

from game.visualizer.game_log_parser import GameLogParser
from game.visualizer.ship_sprites import *
from game.visualizer.station_sprites import *
from game.visualizer.asteroid_field_sprites import get_asteroid_field_sprite
from game.common.enums import *
from game.config import *
from game.visualizer.stats_display import *
import game.utils.stat_utils as stat_utils
import game.utils.click_utils as click_utils

import game.utils.ptext

pause = False
log_parser = None
global_surf = None
fpsClock = None
universe = None
events = None


# Create Sprite groups
ship_group = pygame.sprite.Group()
station_group = pygame.sprite.Group()
asteroid_field_group = pygame.sprite.Group()



def start(verbose, log_path, gamma, dont_wait, fullscreen):
    global fpsClock
    global log_parser
    global universe
    global events

    log_parser = GameLogParser(log_path)
    universe, events = log_parser.get_turn()

    # initialize pygame
    pygame.init()
    fpsClock = pygame.time.Clock()

    # get global surface object and set window caption
    global global_surf
    if fullscreen:
        global_surf = pygame.display.set_mode(DISPLAY_SIZE, flags=pygame.FULLSCREEN)
    else:
        global_surf = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption('Byte-le Royale')

    # set gamma (i.e. sort of like brightness)
    pygame.display.set_gamma(gamma)


    for obj in universe:
        if obj.object_type == ObjectType.ship:
            ship_sprite = NeutralShipSprite(*obj.position, obj.id)
            ship_group.add(ship_sprite)

        elif obj.object_type == ObjectType.station:
            station_sprite = NeutralStationSprite(*obj.position, obj.id)
            station_group.add(station_sprite)

        elif obj.object_type == ObjectType.black_market_station:
            station_sprite = BlackMarketStationSprite(*obj.position, obj.id)
            station_group.add(station_sprite)

        elif obj.object_type == ObjectType.secure_station:
            station_sprite = SecureStationSprite(*obj.position, obj.id)
            station_group.add(station_sprite)

        elif obj.object_type in [ObjectType.goethite_field, ObjectType.cuprite_field, ObjectType.gold_field]:
            asteroid_field_sprite = get_asteroid_field_sprite(obj.object_type, *obj.position)
            asteroid_field_group.add(asteroid_field_sprite)



    # prepare for game loop
    first_loop = True
    turn_wait_counter = 1

    while True:

        # Has the user paused the game?
        # if so don't try to update the screen
        if not pause:

            if log_parser.check_finished():
                sys.exit()

            # should we get the next turn event list
            # or should we wait for some animation to
            # finish
            if turn_wait_counter == 0:
                universe, events = log_parser.get_turn()

                if universe == None and events == None:
                    # game is over, go to end screen
                    pygame.quit()
                    sys.exit()
            else:
                turn_wait_counter -= 1


            # read through the events and handle
            for event in events:
                if not event["handled"]:
                    pass
                    #if event["type"] == LogEvent.demo:
                    #    # there should be data stored
                    #    # on the event object pertaining to
                    #    # the type of event
                    #    print(event)

                    #    # Marks that we have handled this event
                    #    # prevents us from attempting to handle this event again
                    #    event["handled"] = True



            #####
            # Rendering Stuff
            #####

            # render team name
            if first_loop:
                first_loop = False
                # render things here that should only be
                # rendered when we start and then are just redrawn
                # after this


            # intermediate loop
            # -- allows for pretty lerping of ship movement

            if VIS_INTERMEDIATE_FRAMES <= 0:
                update_groups(-1)
                draw_screen()
                handle_events()

                # update the display
                pygame.display.update()
                fpsClock.tick(FPS)
            else:
                for i in range(0,VIS_INTERMEDIATE_FRAMES):
                    if VIS_INTERMEDIATE_FRAMES >= 0:
                        intermediate = i/float(VIS_INTERMEDIATE_FRAMES)
                    else:
                        intermediate = -1

                    update_groups(intermediate)

                    draw_screen()

                    handle_events()

                    # update the display
                    pygame.display.update()
                    fpsClock.tick(FPS)
        else:
            handle_events()


def update_groups(intermediate):

    # call update on groups
    ship_group.update(universe, events, intermediate)

def draw_screen():

    # clear screen, fill with black
    global_surf.fill(pygame.Color(0,0,0))

    # draw groups to screan
    station_group.draw(global_surf)
    asteroid_field_group.draw(global_surf)
    ship_group.draw(global_surf)



def handle_events():
    for event in pygame.event.get():

        # if the application has been exited by the user
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # handle key up events
        elif event.type == KEYUP:
            if event.key == K_p:
                # if p is pressed, toggle pause
                global pause
                pause = not pause
            if event.key == K_f:
                # if f is pressed, toggle fullscreen
                # No guarentee it works for windows.
                pygame.display.toggle_fullscreen()
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_s:
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
        elif event.type == MOUSEBUTTONUP:
            pos = event.pos

            station = click_utils.get_static_obj_near_pos(pos, first=True, obj_type=ObjectType.station)
            if station is None:
                continue

            station_name = station["name"]

            stats = log_parser.get_stats()
            compiled = stat_utils.compile_stats("market", stats, ["station_id", "station_name"])

            show_station_stats_display( compiled[station_name], global_surf, fpsClock)
