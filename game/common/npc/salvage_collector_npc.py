import random
import math

from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *
from game.utils.helpers import *

class SalvageNPC(NPC):

    def take_turn(self, universe):

        if not (MaterialType.salvage in self.ship.inventory and self.ship.inventory[MaterialType.salvage] >= 500):
            closest_scrap = None

            scrap_piles = universe.get(ObjectType.illegal_salvage)
            if len(scrap_piles) > 0:
                closest_scrap = sorted(scrap_piles, key=lambda e: distance_to(self.ship, e, lambda s: s.position))[0]

            if closest_scrap is not None:
                self.move(closest_scrap.position[0], closest_scrap.position[1])
                self.collect_illegal_salvage()
        else:
            station = None
            for thing in universe.get(ObjectType.black_market_station):
                if thing.object_type is ObjectType.black_market_station:
                    station = thing

            self.move(station.position[0], station.position[1])
            self.sell_salvage()

        return self.action_digest()
