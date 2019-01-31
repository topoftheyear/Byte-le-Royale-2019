import random

from game.common.enums import *
from game.common.npc.npc import NPC
from game.utils.helpers import *
from game.client.user_client import *
from game.config import *
import game.utils.filters as F


class AdvancedPirateNPC(NPC):

    def __init__(self, ship):
        UserClient.__init__(self)
        self.ship = ship
        self.ship_id = ship.id

        self.target_ship = None
        self.is_hunting = True
        self.is_gathering = False
        self.is_selling = False
        self.heading = None

    def take_turn(self, universe):
        # if at heading, clear heading
        if(self.heading is not None
                and self.heading[0] == self.ship.position[0]
                and self.heading[1] == self.ship.position[1]):
            self.heading = None

        ships = self.get_ships(universe)

        salvage_list = universe.get(ObjectType.illegal_salvage)
        scrap_nearby = False

        for scrap in salvage_list:
            if self.in_radius_of_illegal_salvage(self.ship, scrap):
                scrap_nearby = True

        if self.is_hunting and (self.target_ship is None or not self.target_ship.is_alive):
            self.is_hunting = False
            self.is_gathering = True

        elif self.is_gathering and not scrap_nearby:
            self.is_gathering = False
            self.is_selling = True

        elif self.is_selling and not (MaterialType.salvage in self.ship.inventory and self.ship.inventory[MaterialType.salvage] >= 50):
            self.is_selling = False
            self.is_hunting = True

        while self.is_hunting and (self.target_ship is None or not self.target_ship.is_alive):
            self.target_ship = random.choice(ships)

        if self.is_gathering:
            self.heading = self.ship.position
            self.collect_illegal_salvage()

        elif self.is_selling:
            for thing in universe.get(ObjectType.black_market_station):
                if thing.object_type is ObjectType.black_market_station:
                    station = thing

            self.heading = station.position

            self.sell_salvage()
        else:
            self.is_hunting = True
            self.heading = self.target_ship.position
            self.attack(self.target_ship)

        # move towards heading
        self.move(*self.heading)

        if self.ship.module_0 == ModuleType.empty:
            self.buy_module(ModuleType.weapons, 1, 0)

        return self.action_digest()


