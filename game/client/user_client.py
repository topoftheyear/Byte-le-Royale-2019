from game.common.enums import  *
from game.common.game_object import GameObject
from game.utils.helpers import *

class UserClient:

    def __init__(self):
        self.reset_actions()

        self._fetch_asteroid_fields = False

        self.asteroid_fields = None
        self.stations = None
        self.ships = None

        self.sell_prices = None
        self.buy_prices = None
        self.best_sell_prices = None
        self.best_buy_prices = None
        self.median_price = None


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

    def get_turn_result(self):
        return {
            "message_type": MessageType.take_turn,

            "action_type": self._action,
            "action_param_1": self._action_param_1,
            "action_param_2": self._action_param_2,
            "action_param_3": self._action_param_3,
            "move_action": self._move_action

        }



    def team_name(self):
        return "ForgotToSetAName"

    ################
    # Game Actions #
    ################

    def move(self, x, y):

        self._move_action = (x, y)

    def mine(self):
        self.reset_player_action()

        self._action = PlayerAction.mine


    def attack(self, target):
        self.reset_player_action()

        if not isinstance(target, GameObject) or target.object_type is not ObjectType.ship or target is None:
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

    def collect_illegal_salvage(self):
        self.reset_player_action()

        self._action = PlayerAction.collect_illegal_salvage

    def ships_in_attack_range(self, universe):
        return ships_in_attack_range(universe, self.ship)

    def sell_salvage(self):
        self.reset_player_action()

        self._action = PlayerAction.sell_salvage

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

    def repair(self, hull_to_repair):
        self.reset_player_action()

        # returns if not a valid payment
        if hull_to_repair <= 0:
            return

        self._action = PlayerAction.repair
        self._action_param_1 = hull_to_repair

    def pay_off_bounty(self):
        self.reset_player_action()

        self._action = PlayerAction.pay_off_bounty

    ##################
    # Helper Methods #
    ##################

    def update_cached_data(self, universe):
        if not hasattr(self, "_fetch_asteroid_fields"):
            self._fetch_asteroid_fields = True
            self.asteroid_fields = universe.get("asteroid_fields")

        self.stations = universe.get("all_stations")
        self.police = universe.get("police")
        self.ships = universe.get(ObjectType.ship)

        price_data = self._get_material_price_info(universe)
        self.sell_prices = price_data["sell_prices"]
        self.buy_prices = price_data["buy_prices"]
        self.best_export_prices = price_data["best_export_prices"]
        self.best_import_prices = price_data["best_import_prices"]

        self.median_price = self._get_median_material_price(self.sell_prices)


    # Helper class wrappers start here
    def distance_to_object(self, your_ship, target):
        """Returns the distance between `your_ship` an an object in the game"""
        return distance_to(your_ship, target, lambda e:e.position)

    def distance_to_coordinate(self, your_ship, xy_coords):
        """Returns the distance between `your_ship` an xy coordinate."""
        return distance_to(your_ship, xy_coords, lambda e:e.position, lambda e:e)

    def in_radius_of_station(self, your_ship, station):
        """Determins if you are within range of a station. If `True` you may perform any interactions
        with the station such as:
        - buying materials
        - selling materials
        - repairing (at select stations)
        - unlocking module slots (at select stations)
        - buying modules (at select stations)
        """
        return in_radius(your_ship, station, station.accessibility_radius, lambda e:e.position)

    def in_radius_of_asteroid_field(self, your_ship, field):
        """Determines if you are within range of an asteroid field. If `True`, mining will
        yeild results."""
        return in_radius(your_ship, field, field.accessibility_radius, lambda e:e.position)

    def in_radius_of_illegal_salvage(self, your_ship, salvage):
        """Returns `True` if your ship is in range to gather from a pile of illegal salvage."""
        return in_radius(your_ship, salvage, your_ship.weapon_range, lambda e:e.position)

    def in_weapons_range(self, your_ship, target_ship):
        """Note: prefer in_weapons_range() over distance_to() for checking if another ship
        is in range."""
        return in_radius(your_ship, target_ship, your_ship.weapon_range, lambda e:e.position)

    def get_material_to_scrap_conversion(self, quantity, value):
        """Given a quantity and a material value, returns the amount of illegal scrap
        that would be created by destroying a  ship carrying this quantity of material."""
        return convert_material_to_scrap(quantity, value)

    def in_secure_zone(self, check):
        return in_secure_zone(check, lambda e:e.position)

    def get_material_name(self, material_type):
        return get_material_name(material_type)

    def get_repair_price(self):
        return get_repair_price(self.median_price)

    def get_module_price(self, level):
        return get_module_price(self.median_price, level)

    def get_module_unlock_price(self, median_price, ship_slot):
        return get_module_unlock_price(self, median_price, ship_slot)


    ## Hidden

    def _get_median_material_price(self, material_prices):
        return get_median_material_price(material_prices)

    def _get_material_price_info(self, universe):
        """Cache this result at most once per turn, otherwise your client will be very slow.

        Returns a dictionary containing:
        - "sell_prices": The sell prices of each material
        - "buy_prices": The buy prices of each material
        - "best_import_prices": The best import price by material, and the corresponding station
        - "best_export_prices": The best export price by material, and the corresponding station

        :param universe:
        :return:
        """
        return {
            "sell_prices": get_material_sell_prices(universe),
            "buy_prices": get_material_buy_prices(universe),
            **get_best_material_prices(universe)
        }



