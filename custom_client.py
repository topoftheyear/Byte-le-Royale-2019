import random

from game.client.user_client import UserClient
from game.common.enums import *



class CustomClient(UserClient):

    def __init__(self):
        """ Use the constructor to initialize any variables you would like to track between turns. """

    def team_name(self):
        print("Sending Team Name")

        return "Herp Derp"

    def team_color(self):
        print("Sending Team Color")

        return [154,50,205]

    def take_turn(self):

        pass



