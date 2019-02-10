import random

from game.client.user_client import UserClient
from game.common.enums import *



class CustomClient(UserClient):

    def __init__(self):
        """ Use the constructor to initialize any variables you would like to track between turns. """
        self.mining_location = None
        self.sell_station = None
        self.illegal_station = None
        self.center_station = ObjectType.secure_station
        self.destination = None
        self.material = None
        self.incrementor = 0
        self.moduleBought = False
        self.moduleBoughtHull = False
        self.tradeCircle = False
        self.nUnlocked = False
        self.repairedHull = False
        self.timeAtMine = 100;

        self.debug = True

    def team_name(self):
        self.print("Sending Team Name")

        return "Chaotic Neutral Lambs"

    def team_color(self):
        self.print("Sending Team Color")

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [168, 119, 90]

    def take_turn(self, ship, universe):
        stations = []
        ships_in_scanner = []
        self.incrementor += 1
        self.update_cached_data(universe)

        # Compile universe list into stations and scan-range ships
        # for obj in universe.dump():
        #     if obj.object_type is ObjectType.station and obj.object_type not in [ObjectType.secure_station, ObjectType.black_market_station]:
        #         stations.append(obj)
        #     elif obj.object_type is ObjectType.ship:
        #         ships_in_scanner.append(obj)
        #self.print(str(ship.credits))
        #self.print(self.get_module_price(1))
        for object in self.stations:
            if object.object_type is ObjectType.secure_station:
                if self.in_radius_of_station(ship, object):

                    self.buy_module(ModuleType.engine_speed, 1, 0)
                    self.print("I BOUGHT IT")



        # If we aren't doing anything, determine a station to purchase from
        #Brings us to gold field
        if self.destination is None:

            for object in self.stations:
                if object.object_type is ObjectType.secure_station:
                    if self.in_radius_of_station(ship, object):
                        self.buy_module(ModuleType.engine_speed, 1, 0)
                        self.print("I BOUGHT IT")
                        self.tradeCircle is True
            if self.tradeCircle is False:
                for object in self.asteroid_fields:
                    if object.object_type is ObjectType.gold_field:
                        self.destination = object
                        self.mining_location = object

        #If credits is more than 40000, the go to market
        #else if the have bought the module and credits is over 10000, then go buy cir
        if self.moduleBought is False and ship.credits > self.get_module_price(1) + 4000:
            for object in self.stations:
                if object.object_type is ObjectType.black_market_station:
                    self.destination = object
                    self.illegal_station = object
                    self.print("AT BLACKMARKET STATION")
        if self.moduleBought is True and self.moduleBoughtHull is False and ship.credits > self.get_module_price(1) + 4000:
            for object in self.stations:
                if object.object_type is ObjectType.black_market_station:
                    self.destination = object
                    self.illegal_station = object
                    self.print("AT BLACKMARKET STATION")
        elif self.moduleBought is True and ship.credits > 5000 and self.tradeCircle is True and self.in_radius_of_station(ship, self.sell_station):
            self.buy_material(100)
            self.material = self.sell_station.production_material

            if self.material in ship.inventory and ship.inventory[self.material] >= 90:
                # Then we find a station that will buy it
                for station in self.stations:
                    if self.material in [station.primary_import, station.secondary_import]:
                        self.print("switching to selling at ", station)
                        self.sell_station = station
                        self.destination = station
                        self.print("AT COMPUTER STATION")
                        self.print("Credits", str(ship.credits))
                        break

        #This buys the Module
        #Repairs the ship
        #Buy speed snd leave
        if self.destination is self.illegal_station and self.in_radius_of_station(ship,self.illegal_station):
            # if self.moduleBought is False:
            #     self.buy_module(ModuleType.engine_speed, 1, 0)
            #     self.print("I BOUGHT SPEED!")
            # # if self.moduleBought is True and self.nUnlocked is False:
            # #
            # # if self.moduleBought is True and self.moduleBoughtHull is False and self.nUnlocked is True:
            # #     self.buy_module(ModuleType.hull, 1, 0)
            # #     self.print("I BOUGHT HULL!")
            # if self.moduleBought is True and self.moduleBoughtHull is False:
            #     if ship.current_hull is not ship.max_hull:
            #         self.repair(ship.max_hull - ship.current_hull)
            #         self.print("I AM REPAIRED")
            #     self.destination = self.mining_location
            #     self.timeAtMine = 496
            # self.moduleBought = True

            if self.moduleBought is False:
                self.buy_module(ModuleType.engine_speed, 1, 0)
                self.print("I BOUGHT SPEED!")
                self.destination = self.mining_location
                self.moduleBought = True
            elif self.nUnlocked is False:
                #self.unlock_module()
                self.nUnlocked = True
                self.print("I BOUGHT THE MODULE")
            elif self.moduleBoughtHull is False:
                self.buy_module(ModuleType.hull, 1, 1)
                self.moduleBoughtHull = True
                self.print("I BOUGHT HULL!")
                self.destination = self.mining_location
            self.timeAtMine = 496
        # If we have a purchase place to go to, buy a material
        if self.destination is self.mining_location and self.in_radius_of_asteroid_field(ship, self.mining_location):
            # Buy its material
            #self.buy_material(1)
            self.mine()
            #self.print("AT MINE")
            self.material = self.destination.material_type

            # If we got it, go and sell it
            if self.material in ship.inventory and ship.inventory[self.material] > self.timeAtMine:

                # Then we find a station that will buy it
                for station in self.stations:
                    if self.material in [station.primary_import, station.secondary_import]:
                        self.print("switching to selling selling at ", station)
                        self.sell_station = station
                        self.destination = station
                        self.print("AT SELL STATION")
                        self.print("Credits", str(ship.credits))
                        break

        # If we have a sell place to go to, go and sell it
        elif self.destination is self.sell_station:
            # Sell the material when possible
            if self.repairedHull is False:
                if ship.current_hull is not ship.max_hull:
                    self.repair(ship.max_hull - ship.current_hull)
                    self.print("I AM REPAIRED")
                self.repairedHull = True
            else:
                self.sell_material(self.material, ship.inventory[self.material])
                # If we sold it, then we completed our task
                if self.material in ship.inventory and ship.inventory[self.material] <= 0:
                    self.destination = None

        # Always move towards our destination unless it doesn't exist
        if self.destination is not None:
            self.move(*self.destination.position)
        else:
            self.move(0,0)

    def print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)
