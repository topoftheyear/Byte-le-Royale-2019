from game.common.enums import  *
from game.common.game_object import GameObject
from game.utils.helpers import *

class UserClient:

    def __init__(self):
        self.reset_actions()


    def reset_actions(self):

        self._action = PlayerAction.none
        self._action_param_1 = None
        self._action_param_2 = None
        self._action_param_3 = None

        self._move_action = None

    def reset_player_action(self):
        self._action = PlayerAction.none
        self._action_param_1 = None
        self._action_param_2 = None
        self._action_param_3 = None


    def team_name(self):
        return "ForgotToSetAName"

    def move(self, x, y):

        self._move_action = (x, y)

    def mine(self):
        self.reset_player_action()

        self._action = PlayerAction.mine


    def attack(self, target):
        self.reset_player_action()

        if not isinstance(target, GameObject) and target.object_type is not ObjectType.ship:
            return

        self._action = PlayerAction.attack
        self._action_param_1 = target.id

    def buy_module(self, module, upgrade_level, ship_slot):
        # add functionality here
        pass

    def get_ships(self, universe, callback=None):
        return get_ships(universe, callback)

    def get_stations(self, universe):
        return get_stations(universe)

    def get_asteroid_fields(self, universe):
        return get_asteroid_fields(universe)


    def ships_in_attack_range(self, universe):
        return ships_in_attack_range(universe, self.ship)
