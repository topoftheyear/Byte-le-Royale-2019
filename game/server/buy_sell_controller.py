import sys
import math

from game.common.enums import *
from game.common.name_helpers import *
from game.common.station import *
from game.common.ship import Ship
from game.utils.helpers import *
from game.common.stats import *

class BuySellController:
    #arrays to track buy changes
    s0 = [] # wire
    s1 = [] # computers
    s2 = [] # circuits
    s3 = [] # drones
    s4 = [] # pylon
    s5 = [] # machinery
    s6 = [] # copper
    s7 = [] # steel
    s8 = [] # iron
    s9 = [] # weaponry


    def __init__(self):

        self.debug = False
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

    def add_to_buy_arrays(self, amount, material, ship, station):
        name = station.name
        if name == "Wire Station":
            self.s0.append([amount, material, ship, station])
        elif name == "Computers Station":
            self.s1.append([amount, material, ship, station])
        elif name == "Circuitry Station":
            self.s2.append([amount, material, ship, station])
        elif name == "Drones Station":
            self.s3.append([amount, material, ship, station])
        elif name == "Pylon Station":
            self.s4.append([amount, material, ship, station])
        elif name == "Machinery Station":
            self.s5.append([amount, material, ship, station])
        elif name == "Copper Station":
            self.s6.append([amount, material, ship, station])
        elif name == "Steel Station":
            self.s7.append([amount, material, ship, station])
        elif name == "Iron Station":
            self.s8.append([amount, material, ship, station])
        elif name == "Weaponry Station":
            self.s9.append([amount, material, ship, station])

    def do_changes(self):
        self.calculate(self.s0)
        self.s0 = []
        self.calculate(self.s1)
        self.s1 = []
        self.calculate(self.s2)
        self.s2 = []
        self.calculate(self.s3)
        self.s3 = []
        self.calculate(self.s4)
        self.s4 = []
        self.calculate(self.s5)
        self.s5 = []
        self.calculate(self.s6)
        self.s6 = []
        self.calculate(self.s7)
        self.s7 = []
        self.calculate(self.s8)
        self.s8 = []
        self.calculate(self.s9)
        self.s9 = []

    def calculate(self, array):
        if len(array) == 0:
            return

        totalbuy = 0
        ships = []
        amounts = []
        station = array[0][3]
        material = array[0][1]
        buyprice = station.base_sell_price


        for entry in array:
            amount = entry[0]
            totalbuy += amount
            ships.append(entry[2])
            amounts.append(amount)

        self.print(str(station.cargo[material]) + "   " + str(totalbuy))
        if station.cargo[material] >= totalbuy:
            for ship, amount in zip(ships, amounts):
                ship.inventory[material] += amount
                ship.credits += (amount * buyprice)
                station.cargo[material] -= amount
        else:
            while len(ships) != 0 and not station.cargo[material] == 0:
                remove = []
                for idx in range(len(ships)):
                    if amounts[idx] == 0:
                        remove.append(idx)
                        continue

                    if station.cargo[material] == 0:
                        self.print("broke out of buying")
                        break
                    ships[idx].inventory[material] += 1
                    ships[idx].credits += (buyprice)
                    amounts[idx] -= 1
                    station.cargo[material] -= 1

                    self.print("bought stuff")
                for idx in remove:
                    del ships[idx]
                    del amounts[idx]



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
                    if not (current_station.primary_import == material or current_station.secondary_import == material):
                        self.print('Improper material type for station')
                        continue

                    # add to ships funds and subtract from inventory amount
                    ship.inventory[material] -= amount
                    if material == current_station.primary_import:
                        ship.credits += amount * current_station.primary_buy_price
                    elif material == current_station.secondary_import:
                        ship.credits += amount * current_station.secondary_buy_price
                    self.print('Ship has received payment of ' + str(amount * current_station.primary_buy_price))


                    #station stuff
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
                        self.add_to_buy_arrays(amount, material, ship, current_station)
                    else:
                        ship.inventory[material] = 0
                        self.add_to_buy_arrays(amount, material, ship, current_station)


                    # Logging
                    # self.print('Logging purchase')
                    self.events.append({
                        "type": LogEvent.material_purchased,
                        "station_id": current_station.id,
                        "ship_id": ship.id,
                        "material": material,
                        "amount": amount
                    })
        self.do_changes()