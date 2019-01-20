import random
import operator

from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *
from game.utils.helpers import *

class TestMinerNPC(NPC):

    def init(self):
        self.chosen_mineral = None

    def take_turn(self, universe):
        # Pick random best of 2 minerals to mine
        # Go to station and sell minerals
        # Repeat

        # Pick random of best 2 minerals
        if self.heading is None:
            mineral_prices = {}
            minerals = [MaterialType.cuprite, MaterialType.goethite, MaterialType.gold]
            fields = universe.get("asteroid_fields")
            prices = get_material_prices(universe)

            for key, item in prices.items():
                if key not in minerals:
                    continue
                mineral_prices[key] = item

            sorted_minerals = sorted(mineral_prices.items(), key=operator.itemgetter(1))
            sorted_minerals.reverse()
            # self.chosen_mineral = sorted_minerals[random.randint(0, 1)][0]
            self.chosen_mineral = random.choice(minerals)

            for field in fields:
                if field.material_type is not self.chosen_mineral:
                    continue
                self.heading = field
                break

        # Mine until full
        elif self.heading in universe.get("asteroid_fields"):
            total_items = sum(self.ship.inventory.values())
            if self.chosen_mineral not in self.ship.inventory or total_items < self.ship.cargo_space:
                self.mine()
                self.move(*self.heading.position)
            else:
                for station in universe.get(ObjectType.station):
                    if self.chosen_mineral not in [station.primary_import, station.secondary_import]:
                        continue
                    self.heading = station
                    break

        # Sell until empty
        elif self.heading in universe.get(ObjectType.station):
            if self.chosen_mineral in self.ship.inventory and self.ship.inventory[self.chosen_mineral] > 0:
                self.move(*self.heading.position)
                self.sell_material(self.chosen_mineral, self.ship.inventory[self.chosen_mineral])
            else:
                self.heading = None
        else:
            self.move(0,0)

        return self.action_digest()
