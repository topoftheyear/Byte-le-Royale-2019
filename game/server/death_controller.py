import sys
import math

from game.common.enums import *
from game.common.name_helpers import *
from game.common.asteroid_field import AsteroidField
from game.common.ship import Ship
from game.utils.projection import percent_world

class DeathController:

    def __init__(self):

        self.debug = False
        self.events = []
        self.stats = []

    def print(self, msg):
        if self.debug:
            print(str(msg))
            sys.stdout.flush()

    def get_events(self):
        e = self.events
        self.events = []
        return e

    def get_stats(self):
        s = self.stats
        self.stats = []
        return s


    def handle_actions(self, dead_ships):

        for ship in dead_ships:
            ship.position = [-100, -100]
            ship.respawn_counter -= 1

            if ship.respawn_counter == 0:
                ship.respawn_counter = -1
                ship.position = percent_world(0.5, 0.5)
                ship.current_hull = ship.max_hull

                self.events.append({
                    "type": LogEvent.ship_respawned,
                    "ship_id": ship.id
                })


