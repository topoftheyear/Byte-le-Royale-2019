import random
from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *

class RepairNPC(NPC):

    def take_turn(self, universe):

        self.repair(self, random.randint(self.max_hull))


        return self.action_digest()