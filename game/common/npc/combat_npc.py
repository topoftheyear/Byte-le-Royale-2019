import random

from game.common.enums import *
from game.common.npc.npc import NPC
from game.config import *


class CombatNPC(NPC):

    def take_turn(self, universe):

        # if at heading, clear heading
        if(self.heading is not None
                and self.heading[0] == self.ship.position[0]
                and self.heading[1] == self.ship.position[1]):
            self.heading = None

        # choose a new heading if we don't have one
        if self.heading is None:
            #self.heading = ( random.randint(0, WORLD_BOUNDS[0]), random.randint(0, WORLD_BOUNDS[1]))
            self.heading = random.choice(list(filter(lambda e:e.object_type != ObjectType.ship, universe))).position

        # move towards heading
        self.move(*self.heading)


        # attack ships in range
        ships = self.ships_in_attack_range(universe)
        ship_to_attack = next(iter(ships), None)
        if ship_to_attack:
            self.attack(ship_to_attack)

        return self.action_digest()


