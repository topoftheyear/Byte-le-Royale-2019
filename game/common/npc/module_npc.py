import random

from game.common.enums import *
from game.common.npc.npc import NPC
from game.config import *

class ModuleNPC(NPC):

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

        # buy random module if we don't have one and in range of station
        if self.ship.module_0 == UpgradeType.empty:
            for thing in universe:

                # Check for all stations in the universe
                if thing.object_type in [ObjectType.secure_station, ObjectType.black_market_station]:
                    current_station = thing
                    # Check if ship is within range of a / the station
                    st_x = current_station.position[0]
                    st_y = current_station.position[1]
                    radius = current_station.accessibility_radius

                    sh_x = self.ship.position[0]
                    sh_y = self.ship.position[1]

                    # Check if ship is within the asteroid field
                    left_result = (sh_x - st_x) ** 2 + (sh_y - st_y) ** 2
                    right_result = radius ** 2
                    if left_result >= right_result:
                        continue
                    self.buy_module(random.choice([UpgradeType.engine_speed, UpgradeType.weapon_damage, UpgradeType.weapon_range]),
                                    random.choice([UpgradeLevel.one, UpgradeLevel.two, UpgradeLevel.three]),
                                    0)

                    print(self.ship.module_0)

        return self.action_digest()


