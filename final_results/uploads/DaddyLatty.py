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

        self.debug = True

    def team_name(self):
        self.print("Sending Team Name")
        return "daddy latty"

    def team_color(self):
        self.print("Sending Team Color")

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [255, 0, 0]

    def take_turn(self, ship, universe):
        self.update_cached_data(universe)
        ships_in_scanner = []

        # If we aren't doing anything, determine a station to purchase from
        if self.destination is None:
            self.print("new interaction generated")
            self.purchase_station = random.choice(self.stations)
            self.destination = self.purchase_station
            self.material = self.purchase_station.production_material
            self.print("new interaction generated: ", str(self.material))
            self.print("buying", self.material)

        # If we have a purchase place to go to, buy a material
        if self.destination is self.purchase_station:
            # Buy its material
            self.buy_material(1)

            # If we got it, go and sell it
            if str(self.material) in ship.inventory and ship.inventory[str(self.material)] > 0:

                # Then we find a station that will buy it
                for station in self.stations:
                    if self.material in [station.primary_import, station.secondary_import]:
                        self.print("switching to selling selling at ", station)
                        self.sell_station = station
                        self.destination = station
                        break

        # If we have a sell place to go to, go and sell it
        elif self.destination is self.sell_station:
            # Sell the material when possible
            self.sell_material(self.material, ship.inventory[str(self.material)])

            # If we sold it, then we completed our task
            if str(self.material) in ship.inventory and ship.inventory[str(self.material)] <= 0:
                self.destination = None

        # Always move towards our destination unless it doesn't exist
        if self.destination is not None:
            self.move(*self.destination.position)
        else:
            self.move(0,0)

    def print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)
