import random

from game.client.user_client import UserClient
from game.common.enums import *


class CustomClient(UserClient):

    def __init__(self):
        """ Use the constructor to initialize any variables you would like to track between turns. """
        self.purchase_station = None
        self.sell_station = None
        self.destination = None
        self.material = None
        self.asteroid_stations = []
        self.secure_station = []
        self.number = 0

        self.debug = False

    def team_name(self):
        self.print("Hooligans")

        return "Hooligans"

    def team_color(self):
        self.print("White")

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [255, 255, 255]

    def take_turn(self, ship, universe):
        self.update_cached_data(universe)
        stations = []
        ships_in_scanner = []

        cuprite = self.asteroid_fields[0]
        gold = self.asteroid_fields[2]
        goethite = self.asteroid_fields[1]

        # Stations for mined materials
        for obj in universe.get("all_stations"):
            if obj is not ObjectType.black_market_station or ObjectType.secure_station:
                if MaterialType.cuprite == obj.primary_import:
                    self.asteroid_stations.append(obj)
                if MaterialType.gold == obj.primary_import:
                    self.asteroid_stations.append(obj)
                if MaterialType.goethite == obj.primary_import:
                    self.asteroid_stations.append(obj)

        # Compile universe list into stations and scan-range ships
        for obj in universe.get("all_stations"):
            if obj.object_type not in [ObjectType.secure_station, ObjectType.black_market_station]:
                stations.append(obj)
            elif obj.object_type is ObjectType.ship:
                ships_in_scanner.append(obj)

        for obj in universe.get(ObjectType.secure_station):
            self.secure_station.append(obj)

        if self.in_radius_of_station(ship, self.secure_station[0]) and sum(ship.inventory.values()) == 0:
            self.destination = self.asteroid_fields[0]

        # If we are close to an asteroid field we set it as our destination
        if sum(ship.inventory.values()) < 200:
            if self.destination == cuprite:
                self.destination = cuprite
                if self.in_radius_of_asteroid_field(ship, cuprite):
                    self.mine()
            elif self.destination == gold:
                self.destination = gold
                if self.in_radius_of_asteroid_field(ship, gold):
                    self.mine()
            elif self.destination == goethite:
                self.destination = goethite
                if self.in_radius_of_asteroid_field(ship, goethite):
                    self.mine()

        # Sell mined materials from an asteroid field
        if sum(ship.inventory.values()) >= 200:
            if ship.inventory.get(MaterialType.cuprite, 0) > 0:
                self.destination = self.asteroid_stations[0]
                if self.in_radius_of_station(ship, self.asteroid_stations[0]):
                    self.number = 1
                    self.sell_material(MaterialType.cuprite, 1000)
            if ship.inventory.get(MaterialType.gold, 0) > 0:
                self.destination = self.asteroid_stations[2]
                if self.in_radius_of_station(ship, self.asteroid_stations[2]):
                    self.number = 2
                    self.sell_material(MaterialType.gold, 1000)
            if ship.inventory.get(MaterialType.goethite, 0) > 0:
                self.destination = self.asteroid_stations[1]
                if self.in_radius_of_station(ship, self.asteroid_stations[1]):
                    self.number = 3
                    self.sell_material(MaterialType.goethite, 1000)

        if ship.inventory.get(MaterialType.cuprite, 0) == 0 and self.number == 1:
            self.destination = self.asteroid_fields[2]
            self.number = 0
        elif ship.inventory.get(MaterialType.gold, 0) == 0 and self.number == 2:
            self.destination = self.asteroid_fields[0]
            self.number = 0
        elif ship.inventory.get(MaterialType.goethite, 0) == 0 and self.number == 3:
            self.destination = self.asteroid_fields[1]
            self.number = 0

        # If we aren't doing anything, determine a station to purchase from
        # if self.destination is None:
        #     self.print("new interaction generated")
        #     self.purchase_station = random.choice(stations)
        #     self.destination = self.purchase_station
        #     self.material = self.purchase_station.production_material
        #     self.print("new interaction generated: ", self.material)
        #     self.print("buying", self.material)

        # If we have a purchase place to go to, buy a material
        # if self.destination is self.purchase_station:
        #     # Buy its material
        #     self.buy_material(1)
        #
        #     # If we got it, go and sell it
        #     if self.material in ship.inventory and ship.inventory[self.material] > 0:
        #
        #         # Then we find a station that will buy it
        #         for station in stations:
        #             if self.material in [station.primary_import, station.secondary_import]:
        #                 self.print("switching to selling selling at ", station)
        #                 self.sell_station = station
        #                 self.destination = station
        #                 break
        #
        # # If we have a sell place to go to, go and sell it
        # elif self.destination is self.sell_station:
        #     # Sell the material when possible
        #     self.sell_material(self.material, ship.inventory[self.material])
        #
        # # If we sold it, then we completed our task
        #     if self.material in ship.inventory and ship.inventory[self.material] <= 0:
        #         self.destination = None

        # Always move towards our destination unless it doesn't exist
        if self.destination is not None:
            self.move(*self.destination.position)
        else:
            self.move(0, 0)

    def print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)
