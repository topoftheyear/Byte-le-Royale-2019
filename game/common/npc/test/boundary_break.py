import random
from game.common.enums import *
from game.common.npc.npc import NPC
from game.utils.helpers import *
from game.client.user_client import UserClient
from game.config import *
import game.utils.filters as F


class BoundaryBreak(NPC):

    def __init__(self, ship):
        UserClient.__init__(self)
        self.ship = ship
        self.ship_id = ship.id
        
        self.edition = random.randint(0, 1)
        self.subedition = random.randint(0, 1)

    def team_name(self):
        return f"Boundary Breaker# {random.randint(1,1000)}"

    def take_turn(self, universe):
        if self.ship.is_alive():
            if self.edition:
                if self.subedition:
                    # print("Checking edge of zeroes")
                    self.move(0, 0)
                else:
                    # print("Checking edge of max")
                    self.move(WORLD_BOUNDS[0], WORLD_BOUNDS[1])
            else:
                if self.subedition:
                    # print("I'm leaving max!")
                    self.move(WORLD_BOUNDS[0]+1, WORLD_BOUNDS[1]+1)
                else:
                    # print("I'm leaving min!")
                    self.move(-1, -1)
        else:
            print("D'oh, I'm dead!")

        return self.action_digest()
