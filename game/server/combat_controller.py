import sys
import math

from game.common.enums import *
from game.common.name_helpers import *
from game.common.asteroid_field import AsteroidField
from game.common.ship import Ship
from game.config import *

from game.server.notoriety_controller import NotorietyController

class CombatController:

    def __init__(self):

        self.debug = False
        self.events = []
        self.stats = []

        self.notoriety_controller = NotorietyController.get_instance()

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
                "damage": ship.weapon_damage,
                "attacker_position": ship.position,
                "target_position": target.position,
            })

            if target.current_hull == 0:
                self.print("Target destroyed, hiding ship.")

                self.events.append({
                    "type": LogEvent.ship_destroyed,
                    "ship": target.id,
                })

                target.respawn_counter = RESPAWN_TIME + 1 #+1 to account for this turn

                self.notoriety_controller.update_standing(ship)
                self.notoriety_controller.update_standing(target)

                # TODO when police and enforcers are implemented,
                #   add checks here to see if the target is one of the abovee
                #   and attrobute appropriately
                if target.legal_standing == LegalStanding.citizen:
                    self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.destroy_civilian)

                elif target.legal_standing == LegalStanding.pirate:

                    if ship.legal_standing in [LegalStanding.citizen, LegalStanding.bounty_hunter]:
                        self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.destroy_pirate)

                elif target.legal_standing == LegalStanding.bounty_hunter:
                    self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.destroy_bounty_hunter)




    def get_ship(self, id, universe):
        for obj in universe:
            if obj.object_type in [ObjectType.ship, ObjectType.police, ObjectType.enforcer] and obj.id == id:
                return obj
        return None

