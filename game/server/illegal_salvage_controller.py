import sys
import math

from game.utils.helpers import *
from game.common.stats import *
from game.common.illegal_salvage import IllegalSalvage

class IllegalSalvageController:

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

            # Check for ships that are performing the drop cargo action
            if ship.action is PlayerAction.drop_cargo:
                self.print('dropping illegal salvage...')

                if not ship.is_alive():
                    continue

                material_type = ship.action_param_1
                amount = ship.action_param_2

                if material_type not in ship.inventory:
                    continue

                if ship.inventory[material_type] < amount:
                    continue

                ship.inventory[material_type] -= amount

                # Create salvage object
                #TODO: Create illegal salvage object on ground

                self.print('illegal salvage dropped')

                # Logging
                self.events.append({
                    "type": LogEvent.cargo_dropped,
                    "ship_id": ship.id,
                    "amount": amount
                })
