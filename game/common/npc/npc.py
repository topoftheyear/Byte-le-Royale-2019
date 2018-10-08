import random

from game.common.enums import *
from game.client.user_client import UserClient
from game.config import *


class NPC(UserClient):

    def __init__(self, ship):
        UserClient.__init__(self)
        self.ship = ship
        self.ship_id = ship.id

        self.heading = None

    def team_name(self):
        return f"~AI ({self.ship_id})"

    def take_turn(self, universe):
        raise Exception("NPC.take_turn must be overriden")


    def action_digest(self):
        """ DO NOT OVERRIDE """
        return {
            "action_type": self._action,
            "action_param_1": self._action_param_1,
            "action_param_2": self._action_param_2,
            "action_param_3": self._action_param_3,
            "move_action": self._move_action
        }


