import random

from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *
from game.utils.helpers import *

class TestMinerNPC(NPC):

    def take_turn(self, universe):
        # Pick random best of 2 minerals to mine
        # Go to station and sell minerals
        # Repeat

        # Compile profit of each mineral
        if self.heading is None:
            max_price = 0
            max_mineral = None
            minerals = [MaterialType.cuprite, MaterialType.goethite, MaterialType.gold]
            prices = get_material_prices(universe)
            for key, item in prices:
                if key not in minerals:
                    continue
                if max_price > item:
                    max_price = item
                    max_mineral = key

            for field in universe.get(ObjectType.asteroid_field):
                if field.material_type is not max_mineral:
                    continue
                self.heading = field
                break
        elif self.heading is ObjectType.asteroid_field:
            #mine, set heading to station when full
            pass
        elif self.heading is ObjectType.station:
            #go and sell the stuff, set heading to None
            pass





        # choose a new heading if we don't have one
        if self.heading is None:
            self.heading = random.choice(universe.get("asteroid_fields")).position

        # move towards heading
        self.move(*self.heading)

        # if at heading, clear heading
        if self.heading[0] == self.ship.position[0] and self.heading[1] == self.ship.position[1]:
            self.heading = None

        self.mine()

        return self.action_digest()
