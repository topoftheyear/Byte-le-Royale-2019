import math

from game.common.enums import *
from game.common.asteroid_field import AsteroidField
from game.common.ship import Ship

class MiningController:

    def handle_actions(self, living_ships, universe, teams, npc_teams):
        for team, data in { **teams, **npc_teams}.items():
            ship = data["ship"]
            # Check for ships that are performing the mining action
            if "action_type" in data and PlayerAction.mine in data["action_type"] and data["action_type"] is not None:
                for thing in universe:
                    # Check for all asteroid fields in the universe
                    if thing.object_type in [ObjectType.cuprite_field, ObjectType.goethite_field, ObjectType.gold_field]:
                        current_field = thing

                        as_x = current_field.position[0]
                        as_y = current_field.position[1]
                        radius = current_field.radius

                        sh_x = ship.position[0]
                        sh_y = ship.position[1]

                        # Check if ship is within the asteroid field
                        if (sh_x - as_x)**2 + (sh_y - as_y)**2 < radius**2:
                            # Get material, multiply rate at which the field can be mined by the rate the ship can mine
                            material = current_field.material_type
                            amount = math.floor(current_field.mining_rate * ship.mining_yield)

                            # Add the gathered materials to the inventory
                            if material not in ship.inventory:
                                ship.inventory.append({material: 0})
                            ship.inventory[material] += amount
