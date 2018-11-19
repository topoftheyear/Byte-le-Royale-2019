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

    def unlock_module(self):
        self.reset_player_action()

        self._action = PlayerAction.unlock_module

    def drop_cargo(self, material_type, amount):
        self.reset_player_action()

        # Make sure material actually exists
        if material_type not in [
            MaterialType.iron,
            MaterialType.steel,
            MaterialType.copper,
            MaterialType.circuitry,
            MaterialType.pylons,
            MaterialType.weaponry,
            MaterialType.machinery,
            MaterialType.computers,
            MaterialType.drones,
            MaterialType.gold,
            MaterialType.goethite,
            MaterialType.cuprite,
            MaterialType.wire,
            MaterialType.salvage ]:
            return

        # Minimum cargo drop requirement
        if amount < 10:
            return

        self._action = PlayerAction.drop_cargo
        self._action_param_1 = material_type
        self._action_param_2 = amount

    def get_ships(self, universe, callback=None):
        return get_ships(universe, callback)

    def get_stations(self, universe):
        return get_stations(universe)

    def get_asteroid_fields(self, universe):
        return get_asteroid_fields(universe)


    def ships_in_attack_range(self, universe):
        return ships_in_attack_range(universe, self.ship)
