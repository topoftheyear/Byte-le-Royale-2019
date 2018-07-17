import random

from game.client.user_client import UserClient


class NPC(UserClient):

    def __init__(self, ship):
        UserClient.__init__(self)
        self.ship = ship
        self.ship_id = ship.id

        self.heading = None

    def team_name(self):
        return f"~AI ({self.ship_id})"

    def take_turn(self, universe):

        # wander between random waypoints
        if self.heading is None:
            self.heading = ( random.randint(0, 1280), random.randint(0, 720))

        self.move(*self.heading)

        if self.heading[0] == self.ship.position[0] and self.heading[1] == self.ship.position[1]:
            self.heading = None

        return self.action_digest()

    def action_digest(self):
        """ DO NOT OVERRIDE """
        return {
            "action_type": self._action,
            "action_param_1": self._action_param_1,
            "action_param_2": self._action_param_2,
            "action_param_3": self._action_param_3,
            "move_action": self._move_action
        }





