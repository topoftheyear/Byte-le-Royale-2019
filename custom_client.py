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

    def team_name(self):
        print("Sending Team Name")

        return "I want to die :)"

    def team_color(self):
        print("Sending Team Color")

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [154, 50, 205]

    def take_turn(self, ship, universe):
        stations = []
        ships_in_scanner = []

        # Compile universe list into stations and scan-range ships
        for obj in universe:
            if obj.object_type is ObjectType.station and obj.object_type not in [ObjectType.secure_station, ObjectType.black_market_station]:
                stations.append(obj)
            elif obj.object_type is ObjectType.ship:
                ships_in_scanner.append(obj)

        # If we aren't doing anything, determine a station to purchase from
        if self.destination is None:
            print("new interaction generated")
            self.purchase_station = random.choice(stations)
            self.destination = self.purchase_station
            self.material = self.purchase_station.production_material

        # If we have a purchase place to go to, buy a material
        if self.destination is self.purchase_station:
            print("buying",self.material)
            # Buy its material
            self.buy_material(1)

            # If we got it, go and sell it
            if self.material in ship.inventory and ship.inventory[self.material] > 0:

                # Then we find a station that will buy it
                for station in stations:
                    if self.material in [station.primary_import, station.secondary_import]:
                        self.sell_station = station
                        self.destination = station
                        break

        # If we have a sell place to go to, go and sell it
        elif self.destination is self.sell_station:
            print("selling")
            # Sell the material when possible
            self.sell_material(self.material, ship.inventory[self.material])

            # If we sold it, then we completed our task
            self.destination = None

        # Always move towards our destination
        self.move(*self.destination.position)
