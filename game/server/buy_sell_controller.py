import sys
import math

from game.common.enums import *
from game.common.name_helpers import *
from game.common.station import *
from game.common.ship import Ship
from game.utils.helpers import *
from game.common.stats import *

class BuySellController:

    def __init__(self):

        self.debug = True
        self.events = []
        self.stats = []

    def print(self, msg):
        if self.debug:
            print("Buy Sell Controller: " + str(msg))
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

            # Check for ships that are performing the sell material action
            if ship.action is PlayerAction.sell_material:

                if not ship.is_alive():
                    continue

                for thing in universe:
                    # Check for all applicable stations in the universe
                    if thing.object_type not in [ObjectType.station]:
                        continue

                    current_station = thing
                    self.print('Found a ship trying to purchase material')

                    if thing.object_type is ObjectType.station:
                        self.print('Station found')

                    # Check if ship is within range of a / the station
                    ship_in_radius = in_radius(
                            current_station,
                            ship,
                            lambda s,t:s.accessibility_radius,
                            lambda e:e.position)

                    if not ship_in_radius:
                        continue

                    self.print('Ship in range of a station')
                    material = ship.action_param_1
                    amount = ship.action_param_2

                    # Check if material and the amount is in ships inventory
                    next = false
                    for item,total in ship.inventory.items():
                        if item is material:
                            if total < amount:
                                next = true
                    if next:
                        continue
                    # add to ships funds and subtract from inventory amount
                    # TODO Implement payment
                    self.print('Ship has received payment')
                    # TODO implement inventory subtraction


                    # Logging
                    self.print('Logging sale')
                    self.events.append({
                        "type": LogEvent.material_sold,
                        "ship_id": ship.id,
                        "material": material,
                        "amount": amount
                    })
            # Check for ships that are performing the buy material action
            if ship.action is PlayerAction.buy_material:
                # TODO buy resource
                continue



