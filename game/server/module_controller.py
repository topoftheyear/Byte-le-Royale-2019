import sys
import math

from game.common.enums import *
from game.common.name_helpers import *
from game.common.station import *
from game.common.ship import Ship

class ModuleController:

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

    def handle_actions(self, living_ships, universe, teams, npc_teams):
        for team, data in { **teams, **npc_teams}.items():
            ship = data["ship"]

            # Check for ships that are performing the buy module action
            if ship.action is PlayerAction.buy_module:
                for thing in universe:

                    # Check for all stations in the universe
                    if thing.object_type in [ObjectType.secure_station, ObjectType.black_market_station]:
                        current_station = thing

                        # Check if ship is within range of a / the station
                        st_x = current_station.position[0]
                        st_y = current_station.position[1]
                        radius = current_station.accessibility_radius

                        sh_x = ship.position[0]
                        sh_y = ship.position[1]

                        # Check if ship is within the asteroid field
                        left_result = (sh_x - st_x) ** 2 + (sh_y - st_y) ** 2
                        right_result = radius ** 2
                        if left_result >= right_result:
                            break

                        module = ship.action_param_1
                        upgrade_level = ship.action_param_2
                        ship_slot = ship.action_param_3

                        # Check is the slot is available
                        if ship_slot == UpgradeLevel.locked:
