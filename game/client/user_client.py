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
        self.reset_player_action()

        # module checking, ModuleType type
        if module in [ModuleType.locked, ModuleType.empty]:
            return

        # upgrade_level checking, ModuleLevel type
        if upgrade_level in [ModuleLevel.base]:
            return

        # ship_slot checking
        if ship_slot not in [
                ShipSlot.zero,
                ShipSlot.one,
                ShipSlot.two,
                ShipSlot.three]:
            return

        self._action = PlayerAction.buy_module
        self._action_param_1 = module
        self._action_param_2 = upgrade_level
        self._action_param_3 = ship_slot


    def get_ships(self, universe, callback=None):
        return get_ships(universe, callback)

    def get_stations(self, universe):
        return get_stations(universe)

    def get_asteroid_fields(self, universe):
        return get_asteroid_fields(universe)


    def ships_in_attack_range(self, universe):
        return ships_in_attack_range(universe, self.ship)

    def sell_material(self, material, amount):
        self.reset_player_action()

        # returns if trying to sell <= to 0
        if amount <= 0:
            return

        self._action = PlayerAction.sell_material
        self._action_param_1 = material
        self._action_param_2 = amount

    def buy_material(self, amount):
        self.reset_player_action()

        # returns if trying to sell <= to 0
        if amount <= 0:
            return

        self._action = PlayerAction.buy_material
        self._action_param_1 = amount