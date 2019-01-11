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

        self.combat_counters = {}

        self.notoriety_controller = NotorietyController.get_instance()

    def print(self, msg):
        if self.debug:
            print("Combat Controller: " + str(msg))
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

            #verify target is in weapon range
            result = (ship.position[0] - target.position[0])**2 + (ship.position[1] - target.position[1])**2
            if not (result < ship.weapon_range**2):
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

            # if target was a police or enforcer give notoriety
            if target.object_type is ObjectType.police:
                self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.attack_police)
            elif target.object_type is ObjectType.enforcer:
                self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.attack_police)

            # record the most recent time these ships was in combat
            self.record_combat(target)
            self.record_combat(ship)


            if target.current_hull == 0:
                self.print("Target destroyed, hiding ship.")

                self.events.append({
                    "type": LogEvent.ship_destroyed,
                    "ship": target.id,
                })

                target.respawn_counter = RESPAWN_TIME + 1 #+1 to account for this turn

                self.notoriety_controller.update_standing(ship)
                self.notoriety_controller.update_standing(target)

                if ship.object_type is ObjectType.ship:
                    # don't attribute notoriety to police or enforcers

                    if target.object_type is ObjectType.ship:
                        if target.legal_standing == LegalStanding.citizen:
                            self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.destroy_civilian)

                            # If attacker is a pirate apply a bounty
                            if ship.legal_standing >= LegalStanding.pirate:
                                ship.bounty_list.append({"bounty_type": BountyType.ship_destroyed, "value": 1500, "age": 0})
                                self.print(f"Bounty {BountyType.ship_destroyed} given to ship {ship.id}")

                        elif target.legal_standing == LegalStanding.pirate:

                            if ship.legal_standing in [LegalStanding.citizen, LegalStanding.bounty_hunter]:
                                self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.destroy_pirate)

                                # If current notoriety is lower than a value, awards the bounty
                                if ship.notoriety <= 0:
                                    ship.credits += target.bounty
                                    self.print(f"Bounty of {target.bounty} given to ship {ship.id}")

                        elif target.legal_standing == LegalStanding.bounty_hunter:
                            self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.destroy_bounty_hunter)

                    elif target.object_type is ObjectType.police:
                        self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.destroy_police)

                    elif target.object_type is ObjectType.enforcer:
                        self.notoriety_controller.attribute_notoriety(ship, NotorietyChangeReason.destroy_enforcer)

        # increment combat counters
        self.increment_combat_counters()

    def get_ship(self, id, universe):
        for obj in universe.get("ships"):
            if obj.id == id:
                return obj
        return None

    def record_combat(self, ship):
        # start at -1 so we can blindly increment everyone
        # and then this ship's count will be 1
        self.combat_counters[ship.id] = -1


    def increment_combat_counters(self):
        for ship_id in self.combat_counters.keys():
            self.combat_counters[ship_id] += 1

    def get_combat_counts(self):
        return self.combat_counters



