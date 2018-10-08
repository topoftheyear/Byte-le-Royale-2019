import random

from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *

class MiningNPC(NPC):

    def take_turn(self, universe):

        # choose a new heading if we don't have one
        if self.heading is None:
            locations = []
            for thing in universe:
                # Check for all asteroid fields in the universe
                if thing.object_type in [ObjectType.cuprite_field, ObjectType.goethite_field, ObjectType.gold_field]:
                    locations.append(thing)

            self.heading = random.choice(locations).position

        # move towards heading
        self.move(*self.heading)

        # if at heading, clear heading
        if self.heading[0] == self.ship.position[0] and self.heading[1] == self.ship.position[1]:
            self.heading = None

        self.mine()

        return self.action_digest()






