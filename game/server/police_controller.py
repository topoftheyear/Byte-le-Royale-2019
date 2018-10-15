import random
import sys

from game.config import NUM_POLICE, WORLD_BOUNDS
from game.common.enums import *
from game.common.name_helpers import *
from game.common.police_ship import PoliceShip
from game.utils.helpers import *
from game.utils.projection import *

class PoliceController:

    def __init__(self):

        self.debug = True
        self.events = []
        self.stats = []

        self.states = {}

        self.police_spawn_counter = 0
        self.police_spawn_timeout = 5


    def print(self, *args):
        if self.debug:
            print(' '.join(str(msg) for msg in args) )
            sys.stdout.flush()

    def get_events(self):
        e = self.events
        self.events = []
        return e

    def get_stats(self):
        s = self.stats
        self.stats = []
        return s

    def setup_police(self, universe):
        p = []
        for _ in range(NUM_POLICE):
            pos = [
                random.randint(0, WORLD_BOUNDS[0]),
                random.randint(0, WORLD_BOUNDS[1])
            ]
            new_police = PoliceShip()
            new_police.init(level=1, position=pos)

            universe.append(new_police)
            p.append(new_police)

        return p


    def assess_universe(self, universe):
        # decide if to spawn new ships, etc.
        new_police = []
        to_remove = []

        living_police = 0

        for obj in universe:
            if obj.object_type is ObjectType.police:
                if obj.is_alive():
                    living_police += 1
                else:
                    to_remove.append(obj)

                    self.events.append({
                        "type": LogEvent.police_removed,
                        "ship_id": obj.id
                    })


        living_police = len(list(filter(
            lambda e: e.object_type is ObjectType.police and e.is_alive(),
            universe
            )))

        if living_police < NUM_POLICE:
            self.police_spawn_counter += 1

            if self.police_spawn_counter >= self.police_spawn_timeout:
                new_ship = PoliceShip()
                new_ship.init(level=1, position=percent_world(0.5, 0.5))

                new_police.append(new_ship)
                self.police_spawn_counter = 0

                self.events.append({
                    "type": LogEvent.police_spawned,
                    "ship_id": new_ship.id
                })

        return new_police, to_remove


    def take_turn(self, police_ship, universe):

        if police_ship.id not in self.states:
            self.states[police_ship.id] = {}
        ship_state = self.states[police_ship.id]

        self.reset_actions(police_ship)

        if police_ship.object_type == ObjectType.police:
            return self.police_take_turn(police_ship, ship_state, universe)
        elif police_ship.object_type == ObjectType.enforcer:
            return self.enforcer_take_turn(police_ship, ship_state, universe)

    def police_take_turn(self, ship, state, universe):
        action = None
        action_param_1 = None
        action_param_2 = None
        action_param_3 = None


        # pick target
        pick_target = lambda universe: random.choice(list(filter(lambda e:e.object_type == ObjectType.ship, universe)))
        if "target" not in state:
            target = pick_target(universe)
            state["target"] = target.id
            state["heading"] = target.position
        else:

            if state["target"] is None:
                target = pick_target(universe)
                state["target"] = target.id

            target = next(filter(lambda e:e.object_type == ObjectType.ship and e.id == state["target"], universe), None)

            if target is not None:

                if in_radius(ship, target, 10, lambda e:e.position):
                    # we are within a certain radius of a ship, choose a new target
                    target = pick_target(universe)
                    state["target"] = target.id

                # update heading
                state["heading"] = target.position
            else:
                state["heading"] = None

        # attack ships in range
        ships = ships_in_attack_range(universe, ship)
        ships = filter(lambda e: e.object_type == ObjectType.ship and e.legal_standing == LegalStanding.pirate, ships)
        ship_to_attack = next(ships, None)
        if ship_to_attack:
            action = PlayerAction.attack
            action_param_1 = ship_to_attack.id

            # also overwrite target and begin persuing
            state["target"] = ship_to_attack.id
            state["heading"] = ship_to_attack.position

        return {
            "move_action": state["heading"],
            "action": action,
            "action_param_1": action_param_1,
            "action_param_2": action_param_2,
            "action_param_3": action_param_3,
        }


    def enforcer_take_turn(self, ship, state, universe):
        # TODO: update later
        return self.police_take_turn(ship, state, universe)


    def reset_actions(self, ship):
        ship.action = None
        ship.action_param_1 = None
        ship.action_param_2 = None
        ship.action_param_3 = None
        ship.move_action = None


