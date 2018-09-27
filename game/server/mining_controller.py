from game.common.enums import *
from game.common.asteroid_field import AsteroidField
from game.common.ship import Ship

class MiningController:

    def handle_actions(self, living_ships, universe):
        for team, data in { **self.teams, **self.npc_teams}.items():
            ship = data["ship"]
            # Check for ships that are performing the mining action
            if PlayerAction.mine in data["action_type"] and data["action_type"] is not None:
                for thing in universe:
                    # Check for all asteroid fields in the universe
                    if type(thing) is AsteroidField:
                        as_x = thing.position[0]
                        as_y = thing.position[1]
                        radius = thing.radius

                        sh_x = ship.position[0]
                        sh_y = ship.position[1]

                        # Check if ship is within the asteroid field
                        if 2**(sh_x - as_x) + 2**(sh_y - as_y) < 2**radius:
                            pass
