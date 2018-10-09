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

        # module checking, UpgradeType type
        if module in [UpgradeType.locked, UpgradeType.empty]:
            return

        # upgrade_level checking, UpgradeLevel type
        if upgrade_level in [UpgradeLevel.base]:
            return

        # ship_slot checking
        if ship_slot not in [0, 1, 2, 3]:
            return

        self._action = PlayerAction.buy_module
        self._action_param_1 = module
        self._action_param_2 = upgrade_level
        self._action_param_3 = ship_slot


    def get_ships(self, universe, callback=None):
        if callback != None:
            return [ obj
                    for obj in universe
                    if obj.object_type == ObjectType.ship
                    and obj.is_alive()
                    and callback(obj)]

        return [ obj
                for obj in universe
                if obj.object_type == ObjectType.ship
                and obj.is_alive()]

    def get_stations(self, universe):
        return [ obj for obj in universe if obj.object_type == ObjectType.stations ]

    def get_asteroid_fields(self, universe):
        return [ obj
                for obj in universe
                if obj.object_type in [
                    ObjectType.cuprite_field,
                    ObjectType.goethite_field,
                    ObjectType.gold_field] ]


    def ships_in_attack_range(self, universe):
        def is_ship_visible_wrapper(ship):
            def is_ship_visible(target):
                result = (ship.position[0] - target.position[0])**2 + (ship.position[1] - target.position[1])**2
                in_range = result < ship.weapon_range**2
                return in_range  and ship.id != target.id
            return is_ship_visible

        return self.get_ships(universe, is_ship_visible_wrapper(self.ship))
