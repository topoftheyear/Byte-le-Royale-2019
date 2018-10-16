import sys
import math

from game.common.enums import *
from game.common.name_helpers import *
from game.common.asteroid_field import AsteroidField
from game.common.ship import Ship
from game.utils.helpers import *

class MiningController:

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

            # Check for ships that are performing the mining action
            if ship.action is PlayerAction.mine:
                for thing in universe:

                    # Check for all asteroid fields in the universe
                    if thing.object_type in [ObjectType.cuprite_field, ObjectType.goethite_field, ObjectType.gold_field]:
                        current_field = thing

                        ship_in_radius = in_radius(
                            current_field,
                            ship,
                            lambda s, t: s.accessibility_radius,
                            lambda e: e.position)

                        if ship_in_radius:
                            # Get material, multiply rate at which the field can be mined by the rate the ship can mine
                            material = current_field.material_type
                            amount = math.floor(current_field.mining_rate * ship.mining_yield)

                            self.print("Logging events")
                            self.events.append({
                                "type": LogEvent.ship_mine,
                                "ship_id": ship.id,
                            })

                            self.stats.append({
                                "ship_id": ship.id,
                                "material": material,
                                "yield": amount
                            })

                            self.print(f"Adding {amount} of material {get_material_name(material)} to ship {ship.team_name}'s cargo")
                            # Add the gathered materials to the inventory
                            if material not in ship.inventory:
                                ship.inventory[material] = 0
                            ship.inventory[material] += amount
