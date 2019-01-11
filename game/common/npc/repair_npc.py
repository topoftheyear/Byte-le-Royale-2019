import random
from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *

class RepairNPC(NPC):

    def take_turn(self, universe):

        # choose a new heading if we don't have one
        if self.heading is None:
            # self.heading = ( random.randint(0, WORLD_BOUNDS[0]), random.randint(0, WORLD_BOUNDS[1]))
            self.heading = random.choice(
                universe.get(ObjectType.station) +
                universe.get(ObjectType.secure_station) +
                universe.get(ObjectType.black_market_station)
            ).position

        # move towards heading
        self.move(*self.heading)

        self.repair( random.randint(0, self.ship.max_hull))


        return self.action_digest()