import sys
import math

from game.utils.helpers import *
from game.common.stats import *
from game.common.scrap import Scrap

class ScrapController:

    def __init__(self):

        self.debug = True
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

                if not ship.is_alive():
                    continue

                amount = ship.action_param_1

                #TODO: Determine if ship has enough cargo

                # Create scrap object
                Scrap.init(ship.position, math.floor(amount/100))

                # Logging
                self.events.append({
                    "type": LogEvent.cargo_dropped,
                    "ship_id": ship.id,
                    "amount": amount
                })
