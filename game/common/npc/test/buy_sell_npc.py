import random

from game.common.enums import *
from game.common.npc.npc import NPC
from game.config import *
from game.utils.helpers import *

class BuySellNPC(NPC):

    def take_turn(self, universe):

        # if at heading, clear heading
        if(self.heading is not None
                and self.heading[0] == self.ship.position[0]
                and self.heading[1] == self.ship.position[1]):
            self.heading = None

        # choose a new heading if we don't have one
        if self.heading is None:
            #self.heading = ( random.randint(0, WORLD_BOUNDS[0]), random.randint(0, WORLD_BOUNDS[1]))
            self.heading = random.choice(universe.get(ObjectType.station)).position

        # move towards heading
        self.move(*self.heading)

        for station in universe.get(ObjectType.station):

            # Check if ship is within range of a / the station
            ship_in_radius = in_radius(
                    station,
                    self.ship,
                    lambda s,t:s.accessibility_radius,
                    lambda e:e.position)
            if not ship_in_radius:
                continue

            if(station.primary_import in self.ship.inventory
                    and self.ship.inventory[station.primary_import] > 0):
                self.sell_material(station.primary_import, self.ship.inventory[station.primary_import])
            elif(station.secondary_import in self.ship.inventory
                    and self.ship.inventory[station.secondary_import] > 0):
                self.sell_material(station.secondary_import, self.ship.inventory[station.secondary_import])
            else:
                self.buy_material(1000)

        return self.action_digest()


