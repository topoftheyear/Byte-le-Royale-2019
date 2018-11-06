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
                    if thing.object_type in [ObjectType.secure_station, ObjectType.black_market_station]:
                        continue

                    current_station = thing
                    # self.print('Found a ship trying to sell material')
                    #
                    # if thing.object_type is ObjectType.station:
                    #     self.print('Station found')

                    # Check if ship is within range of a / the station
                    ship_in_radius = in_radius(
                            current_station,
                            ship,
                            lambda s,t:s.accessibility_radius,
                            lambda e:e.position)

                    if not ship_in_radius:
                        continue

                    self.print('Ship in range of a station to sell')
                    material = ship.action_param_1
                    amount = ship.action_param_2

                    # Check if material and the amount is in ships inventory, if not set amount to max held in inventory
                    if material not in ship.inventory:
                        ship.inventory[material] = 0
                    if amount > ship.inventory[material]:
                        amount = ship.inventory[material]

                    # Check if station accepts material
                    if not current_station.primary_import == material:
                        self.print('Improper material type for station')
                        continue

                    # add to ships funds and subtract from inventory amount
                    ship.inventory[material] -= amount
                    ship.credits += amount * current_station.primary_buy_price
                    self.print('Ship has received payment')


                    #station stuff
                    current_station.cargo[material] += amount


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

                if not ship.is_alive():
                    continue

                for thing in universe:
                    # Check for all applicable stations in the universe
                    if thing.object_type not in [ObjectType.station]:
                        continue
                    if thing.object_type in [ObjectType.secure_station, ObjectType.black_market_station]:
                        continue

                    current_station = thing
                    # self.print('Found a ship trying to purchase material')
                    #
                    # if thing.object_type is ObjectType.station:
                    #     self.print('Station found')

                    # Check if ship is within range of a / the station
                    ship_in_radius = in_radius(
                            current_station,
                            ship,
                            lambda s,t:s.accessibility_radius,
                            lambda e:e.position)

                    if not ship_in_radius:
                        continue

                    self.print('Ship in range of a station to buy')
                    amount = ship.action_param_1
                    material = current_station.production_material

                    # Do checks and change values
                    if current_station.cargo[material] < amount:
                        amount = current_station.cargo[material]
                    total_cost = amount * current_station.sell_price
                    current_station.cargo[material] -= amount
                    ship.credits -= total_cost
                    if material in ship.inventory:
                        ship.inventory[material] += amount
                    else:
                        ship.inventory[material] = 0
                        ship.inventory[material] += amount
                    self.print('Ship has received materials')


                    # Logging
                    self.print('Logging purchase')
                    self.events.append({
                        "type": LogEvent.material_purchased,
                        "ship_id": ship.id,
                        "material": material,
                        "amount": amount
                    })