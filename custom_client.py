import random

from game.client.user_client import UserClient
from game.common.enums import *



class CustomClient(UserClient):

    def __init__(self):
        """ Use the constructor to initialize any variables you would like to track between turns. """

    def team_name(self):
        print("Sending Team Name")

        return "End my life :)"

    def team_color(self):
        print("Sending Team Color")

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [154, 50, 205]

    def take_turn(self, ship, universe):
        ships_in_universe = 0
        for thing in universe:
            if thing.object_type is ObjectType.ship:
                ships_in_universe += 1
        print(ships_in_universe)

        self.move(random.randint(100,500), random.randint(100, 500))
        self.mine()



