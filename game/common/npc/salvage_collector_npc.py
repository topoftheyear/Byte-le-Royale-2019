import random
import math

from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *

class SalvageNPC(NPC):

    def take_turn(self, universe):

        if not (MaterialType.salvage in self.ship.inventory and self.ship.inventory[MaterialType.salvage] >= 500):
            closest_scrap = None
            distance = -1

            for thing in universe:
                if thing.object_type is ObjectType.illegal_salvage:
                    scrap = thing

                    if closest_scrap is None:
                        closest_scrap = scrap
                        distance = math.sqrt((scrap.position[0] - self.ship.position[0]) ** 2 + (scrap.position[1] - self.ship.position[1]) ** 2)
                    else:
                        new_distance = math.sqrt((scrap.position[0] - self.ship.position[0]) ** 2 + (scrap.position[1] - self.ship.position[1]) ** 2)
                        if new_distance < distance:
                            distance = new_distance
                            closest_scrap = scrap

            if closest_scrap is not None:
                self.move(closest_scrap.position[0], closest_scrap.position[1])
                self.collect_illegal_salvage()
        else:
            station = None
            for thing in universe:
                if thing.object_type is ObjectType.black_market_station:
                    station = thing

            self.move(station.position[0], station.position[1])
            self.sell_material(MaterialType.salvage, self.ship.inventory[MaterialType.salvage])




        return self.action_digest()






