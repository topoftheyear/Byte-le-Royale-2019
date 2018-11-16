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

        self.debug = False
        self.events = []
        self.stats = []
        self.station_bids = {}

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

    def add_to_bids(self, amount, material, ship, station):
        if not station in self.station_bids:
            self.station_bids[station] = []
        self.station_bids[station].append([amount, material, ship])

    def do_changes(self):
        for station, bids in self.station_bids.items():
            self.calculate(station, bids)
        self.station_bids = {}

    def calculate(self, station, bids):
        if len(bids) == 0:
            return

        totalbuy = 0
        ships = []
        amounts = []
        end_amounts = [] #used to keep track of values for logging
        material = bids[0][1]
        buyprice = station.base_sell_price


        for entry in bids:
            amount = entry[0]
            totalbuy += amount
            ships.append(entry[2])
            amounts.append(amount)

        end_amounts = amounts.copy()

        self.print(str(station.cargo[material]) + " <--amount in station : Total wanted -->  " + str(totalbuy))
        if station.cargo[material] >= totalbuy:
            for ship, amount in zip(ships, amounts):
                ship.inventory[material] += amount
                ship.credits += (amount * buyprice)
                station.cargo[material] -= amount
        else:
            #case of a more demand than amount left in station, will evenly split resources among people
            while len(ships) != 0 and not station.cargo[material] == 0:
                for idx in range(len(ships)):
                    if amounts[idx] == 0:
                        continue

                    # check if station is out of material and if so modify end_amounts to be correct
                    if station.cargo[material] == 0:
                        self.print("station out of material")
                        for idx2 in range(len(amounts)):
                            end_amounts[idx2] -= amounts[idx2]
                        break
                    ships[idx].inventory[material] += 1
                    ships[idx].credits += (buyprice)
                    amounts[idx] -= 1
                    station.cargo[material] -= 1

                    self.print("bought stuff")
        for idx in range(len(ships)):
            ship = ships[idx]
            amount_bought = end_amounts[idx]
            price = amount_bought * buyprice

            #logging purchasees
            self.print('Logging purchase ' + str(price) + '     ' + str(amount_bought) + str(ship.id))
            self.events.append({
                "type": LogEvent.material_purchased,
                "station_id": station.id,
                "ship_id": ship.id,
                "material": material,
                "amount": amount_bought,
                "total_price": price
            })



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

                    # Check if ship is within range of a / the station
                    ship_in_radius = in_radius(
                            current_station,
                            ship,
                            lambda s,t:s.accessibility_radius,
                            lambda e:e.position)

                    if not ship_in_radius:
                        continue

                    #self.print('Ship in range of a station to sell')
                    material = ship.action_param_1
                    amount = ship.action_param_2

                    # Check if material and the amount is in ships inventory, if not set amount to max held in inventory
                    if material not in ship.inventory:
                        ship.inventory[material] = 0
                    if amount > ship.inventory[material]:
                        amount = ship.inventory[material]

                    # Check if station accepts material
                    if not (current_station.primary_import == material or current_station.secondary_import == material):
                        self.print('Improper material type for station')
                        continue

                    # check if it is primary or secondary import and modify inventory and credits
                    if material == current_station.primary_import:
                        ship.inventory[material] -= amount
                        ship.credits += (amount * current_station.primary_buy_price)
                        self.print('Ship has received primary payment of ' + str(amount * current_station.primary_buy_price))

                        station_max = current_station.primary_max
                        current_amount = current_station.cargo[material]
                        if station_max + current_amount > station_max:
                            current_station.cargo[material] = station_max
                        else:
                            current_station.cargo[material] += amount
                    elif material == current_station.secondary_import:
                        ship.inventory[material] -= amount
                        ship.credits += amount * current_station.secondary_buy_price
                        self.print('Ship has received secondary payment of ' + str(amount * current_station.secondary_buy_price))

                        station_max = current_station.secondary_max
                        current_amount = current_station.cargo[material]
                        if station_max + current_amount > station_max:
                            current_station.cargo[material] = station_max
                        else:
                            current_station.cargo[material] += amount


                    # Logging
                    self.print('Logging sale')
                    self.events.append({
                        "type": LogEvent.material_sold,
                        "station_id": current_station.id,
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

                    # self.print('Ship in range of a station to buy')
                    amount = ship.action_param_1
                    material = current_station.production_material

                    # Do checks and change values
                    total_cost = amount * current_station.sell_price

                    #not enough money
                    if ship.credits < total_cost:
                        self.print("not enough credits needs " + str(total_cost) + " but has " + str(ship.credits))
                        continue

                    #making sure material entry is in inventory
                    if material in ship.inventory:
                        self.add_to_bids(amount, material, ship, current_station)
                    else:
                        ship.inventory[material] = 0
                        self.add_to_bids(amount, material, ship, current_station)



        self.do_changes()