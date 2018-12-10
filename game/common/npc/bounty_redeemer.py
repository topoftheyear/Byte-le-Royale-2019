import random

from game.common.enums import *
from game.common.npc.npc import NPC
from game.config import *
import game.utils.filters as F


class BountyRedeemerNPC(NPC):

    def take_turn(self, universe):

        # if at heading, clear heading
        if self.heading is None:
            hunting_list = []
            for ship in universe.get(ObjectType.ship):
                if ship.bounty_total > 0:
                    hunting_list.append(ship)
            if len(hunting_list) > 0:
                self.heading = random.choice(hunting_list)


        # move towards heading
        if self.heading is not None:
            self.move(*self.heading.position)
            self.attack(self.heading)

            if self.heading.current_hull <= 0:
                self.heading = None
        else:
            self.move(1000,1000)

        return self.action_digest()

