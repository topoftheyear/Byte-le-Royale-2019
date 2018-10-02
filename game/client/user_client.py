from game.common.enums import  *
from game.common.game_object import GameObject

class UserClient:

    def __init__(self):
        self.reset_actions()


    def reset_actions(self):

        self._action = PlayerAction.none
        self._action_param_1 = None
        self._action_param_2 = None
        self._action_param_3 = None

        self._move_action = None

    def team_name(self):
        return "ForgotToSetAName"

    def move(self, x, y):

        self._move_action = (x, y)

    def mine(self):
        self.reset_actions()

        self._action = PlayerAction.mine


    def attack(self, target):
        self.reset_actions()

        if not isinstance(target, GameObject) and target.object_type is not ObjectType.ship:
            return

        self._action = PlayerAction.attack
        self._action_param_1 = target.id

    def get_ships(self, universe):
        return [ obj for obj in universe if obj.object_type == ObjectType.ship ]

    def get_stations(self, universe):
        return [ obj for obj in universe if obj.object_type == ObjectType.stations ]

    def get_asteroid_fields(self, universe):
        return [ obj
                for obj in universe
                if obj.object_type in [
                    ObjectType.cuprite_field,
                    ObjectType.goethite_field,
                    ObjectType.gold_field] ]
