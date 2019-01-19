
from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *

class LazyNPC(NPC):

    def take_turn(self, universe):

        #  I am lazy
        #  I move nowhere, I do nothing
        #  That is my purpose
        #  I'm also a great example of how the passive healing works but
        #  I am lazy


        return self.action_digest()