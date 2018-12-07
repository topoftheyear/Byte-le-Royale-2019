import sys
import math
import random

from game.common.enums import *
from game.common.name_helpers import *
from game.common.asteroid_field import AsteroidField
from game.common.ship import Ship
from game.common.illegal_salvage import IllegalSalvage
from game.utils.projection import percent_world
from game.config import *

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


    def handle_actions(self, dead_ships, universe):

        for ship in dead_ships:
            if ship.respawn_counter == RESPAWN_TIME + 1: #the respawn time that is set for when a ship just died
                self.on_death(ship, universe)
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

    def on_death(self, ship, universe):
        ship_salvage_constant = SHIP_SALVAGE_CONSTANT
        value_to_drop = 0
        if ship.object_type is ObjectType.ship:
            for key in ship.inventory:
                # TODO replace vvvvvvvvv with value method when added
                material_value = 100
                # TODO replace ^^^^^^^^^ with value method when added
                value_to_drop += ship.inventory[key] * material_value * 0.25  # update value of material
                ship.inventory[key] = 0
        value_to_drop += ship_salvage_constant

        random_position = (
            ship.position[0] + random.randint(-5, 5),
            ship.position[1] + random.randint(-5, 5)
        )
        new_illegal_salvage = IllegalSalvage()
        new_illegal_salvage.init(position=random_position, value=value_to_drop)

        universe.append(new_illegal_salvage)

        print('Created new illegal salvage at {} with value {}CR'.format(random_position, value_to_drop))

        self.events.append({
            "type": LogEvent.illegal_salvage_spawned,
            "id": new_illegal_salvage.id,
            "position": new_illegal_salvage.position,
            "value": value_to_drop
        })
