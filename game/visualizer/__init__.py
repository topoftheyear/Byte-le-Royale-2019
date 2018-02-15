import sys, math, random, time

import pygame
from pygame.locals import *

from game.visualizer.game_log_parser import GameLogParser
from game.common.enums import *

import ptext

def start(verbose, log_path, gamma, dont_wait, fullscreen):

    log_parser = GameLogParser(log_path)
    events = log_parser.get_turn()

    # initialize pygame
    pygame.init()
    fpsClock = pygame.time.Clock()

    # get global surface object and set window caption
    if fullscreen:
        global_surf = pygame.display.set_mode((1280,720), flags=pygame.FULLSCREEN)
    else:
        global_surf = pygame.display.set_mode((1280,720))
    pygame.display.set_caption('Byte-le Royale')

    # set gamma (i.e. sort of like brightness)
    pygame.display.set_gamma(gamma)

    # Create Sprite groups
    example_group = pygame.sprite.Group()


    # prepare for game loop
    first_loop = True
    pause = False
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
                events = log_parser.get_turn()
            else:
                turn_wait_counter -= 1


            # read through the events and handle
            for event in events:
                if not event["handled"]:
                    if event["type"] == LogEvent.demo:
                        # there should be data stored
                        # on the event object pertaining to
                        # the type of event
                        print(event)

                        # Marks that we have handled this event
                        # prevents us from attempting to handle this event again
                        event["handled"] = True



            #####
            # Rendering Stuff
            #####

            # render team name
            if first_loop:
                first_loop = False
                # render things here that should only be
                # rendered when we start and then are just redrawn
                # after this


            # call update on groups
            example_group.update()


            #####
            # Begin Drawing to screen
            #####

            # clear screen, fill with black
            global_surf.fill(pygame.Color(0,0,0))

            # draw groups to screan
            example_group.draw(global_surf)


        #
        # Handle Events
        #
        for event in pygame.event.get():

            # if the application has been exited by the user
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # get mouse position
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            # Handle clicks
            elif event.type == MOUSEBUTTONUP:
               if event.button == 1:
                   pass # left mouse button clicked

            # handle key up events
            elif event.type == KEYUP:
                if event.key == K_p:
                    # if p is pressed, toggle pause
                    pause = not pause
                if event.key == K_f:
                    # if f is pressed, toggle fullscreen
                    # No guarentee it works for windows.
                    pygame.display.toggle_fullscreen()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        # update the display
        pygame.display.update()
        fpsClock.tick(30)


