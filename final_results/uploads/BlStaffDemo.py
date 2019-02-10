import random

from game.client.user_client import UserClient
from game.common.enums import *



class CustomClient(UserClient):

    def __init__(self):
        self.debug = False

        self.action = None
        self.target = None

        self.previous_hull = 1000

        self.counter = 0

        self.material = None

        self.purchased = None

        self.previous_position = [0,0]

        self.fields = None
        self.stations = None

        self.bored_counter = 0

    def team_name(self):
        return "Oh no its murder"

    def team_color(self):

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [189, 159, 153]

    def take_turn(self, ship, universe):
        self.update_cached_data(universe)
        #self.move(-1,-1)

        # initialize empty variables
        if self.target is None:
            ships_in_range = self.ships
            if len(ships_in_range) > 0 and random.randint(1,3) == 2:
                self.target = random.choice(ships_in_range)
            else:
                self.move(100,100)

        if self.target is not None:
            self.move(*self.target.position)
            if self.distance_to_object(ship, self.target) < ship.weapon_range:
                self.attack(self.target)

            if self.target.current_hull <= 0:
                self.target = None

        if ship.module_0 is ModuleType.empty and self.in_radius_of_station(ship, universe.get(ObjectType.secure_station)[0]):
            self.buy_module(ModuleType.weapons, ModuleLevel.one, ShipSlot.zero)

        if self.previous_position[0] == ship.position[0] and self.previous_position[1] == ship.position[1]:
            self.bored_counter += 1

        if self.bored_counter > 10:
            self.target = None
            self.bored_counter = 0

        self.previous_position = ship.position

    def clear_variables(self):
        self.action = None
        self.target = None

        self.counter = 0

        self.material = None

        self.purchased = None
