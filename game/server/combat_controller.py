import sys
import math

from game.common.enums import *
from game.common.name_helpers import *
from game.common.asteroid_field import AsteroidField
from game.common.ship import Ship
from game.config import *

class CombatController:

    def __init__(self):

        self.debug = True
        self.events = []
        self.stats = []

    def print(self, msg):
        if self.debug:
            print(str(msg))
            sys.stdout.flush()

    def get_events(self):
        e = self.events
        self.events = []
        return e

    def get_stats(self):
        s = self.stats
        self.stats = []
        return s


    def handle_actions(self, living_ships, universe, teams, npc_teams):
        for team, data in { **teams, **npc_teams}.items():
            ship = data["ship"]

            # Check for ships that are attempting to attack
            if not ship.action is PlayerAction.attack: continue

            # get attack target
            target = self.get_ship(ship.action_param_1, universe)
            self.print(f"Ship {ship.team_name} attempting to attack ship {ship.team_name}")

            #verify target is in sensor range
            result = (ship.position[0] - target.position[0])**2 + (ship.position[1] - target.position[1])**2
            if not (result < ship.sensor_range**2):
                self.print("Target not in range.")
                # the target is not in range
                continue

            self.print(f"Target is in range. Dealing {ship.weapon_damage} to target.")
            target.current_hull = max(target.current_hull-ship.weapon_damage, 0)
            self.print(f"Target hull now at {target.current_hull}")


            self.events.append({
                "type": LogEvent.ship_attack,
                "attacker": ship.id,
                "target": target.id,
                "damage": ship.weapon_damage
            })

            if target.current_hull == 0:
                self.print("Target destroyed, hiding ship.")
                exit()
                self.events.append({
                    "type": LogEvent.ship_destroyed,
                    "ship": target.id,
                })

                # move them off the map
                target.position = (-100, -100)
                target.respawn_counter = RESPAWN_TIME + 1 #+1 to account for this turn




    def get_ship(self, id, universe):
        for obj in universe:
            if obj.object_type is ObjectType.ship and obj.id == id:
                return obj
        return None

