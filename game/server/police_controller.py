import random
import math
import sys
import functools

from game.config import NUM_POLICE, WORLD_BOUNDS
from game.common.enums import *
from game.common.name_helpers import *
from game.common.police_ship import PoliceShip
from game.utils.helpers import *
from game.utils.projection import *

class PoliceVariant:
    waiting = 1
    patrolling = 3
    guarding = 4

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

            self.create_state(new_police)

            universe.append(new_police)
            p.append(new_police)

        return p


    def create_state(self, ship):
        self.states[ship.id] = {
            "variation":  random.choices([
                PoliceVariant.waiting,
                PoliceVariant.patrolling,
                PoliceVariant.guarding,
            ],
                [
                    0.50, # waiting
                    0.25, # patrolling
                    0.25 # guarding
                ]
            )[0]

        }

        if self.states[ship.id]["variation"] == PoliceVariant.guarding:
            # make sure they spawn in the center
            ship.position = percent_world(0.5, 0.5)


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
                self.create_state(new_ship)

                new_police.append(new_ship)
                self.police_spawn_counter = 0


                self.events.append({
                    "type": LogEvent.police_spawned,
                    "ship_id": new_ship.id
                })

        return new_police, to_remove


    def take_turn(self, police_ship, universe):

        ship_state = self.states[police_ship.id]

        self.reset_actions(police_ship)

        if police_ship.object_type == ObjectType.police:
            return self.police_take_turn(police_ship, ship_state, universe)
        elif police_ship.object_type == ObjectType.enforcer:
            return self.enforcer_take_turn(police_ship, ship_state, universe)

    def police_take_turn(self, ship, state, universe):



        if state["variation"] is PoliceVariant.waiting:
            return self.waiting_police(ship, state, universe)
        elif state["variation"] is PoliceVariant.patrolling:
            return self.patrolling_police(ship, state, universe)
        elif state["variation"] is PoliceVariant.guarding:
            return self.guarding_police(ship,state, universe)


    def waiting_police(self, ship, state, universe):
        action = None
        action_param_1 = None
        action_param_2 = None
        action_param_3 = None


        if not state.get("target"):
            target = self.closest_pirate(ship, universe)

            if target is not None:
                state["target"] = target
                state["heading"] = target.position

            else:
                state["heading"] = None
        else:
            # update target location
            target_ships = get_ships(universe, lambda s:s.id==state["target"].id)
            if len(target_ships) > 0:
                state["target"] = target_ships[0]
            else:

                # target is out of range, pick a new one
                if not (in_radius(ship, state["target"], ship.sensor_range, lambda s:s.position)
                        and state["target"].is_alive() ):
                    target = self.closest_pirate(ship, universe)

                if target is not None:
                    state["target"] = target
                    state["heading"] = target.position

                else:
                    state["heading"] = None


        # move toward target and attack
        if state.get("target"):
            if not state["target"].is_alive():
                state["target"] = None
                state["heading"] = None

            else:
                action = PlayerAction.attack
                action_param_1 = state["target"].id

                # also overwrite target and begin persuing
                state["heading"] = state["target"].position
        else:
            # otherwise wait here
            state["heading"] = ship.position

        return {
            "move_action": state["heading"],
            "action": action,
            "action_param_1": action_param_1,
            "action_param_2": action_param_2,
            "action_param_3": action_param_3,
        }

    def patrolling_police(self, ship, state, universe):
        action = None
        action_param_1 = None
        action_param_2 = None
        action_param_3 = None

        # first time pick 3 to 4 stations to patrol between

        if "patrol_route" not in state:
            # get stations to choose between
            stations = get_stations(universe)

            state["patrol_route"] = random.choices(stations, k=3)

            random.shuffle(state["patrol_route"])


            state["waypoint"] = state["patrol_route"][0]
            state["patrolling"] = True


        # check ships nearby to verify no pirates
        if "target" not in state:
            target_ship = self.closest_pirate(ship, universe)

            if target_ship is not None:
                # set target
                state["target"] = target_ship

        if "target" in state:
            # get updated copy of target
            target_ships = get_ships(universe, lambda s:s.id==state["target"].id)
            if len(target_ships) > 0:
                state["target"] = target_ships[0]

                # verify target is still in scanner range, just in
                # case they moved out of range last turn, if they moved out of range,
                # forget them and resume patrolling
                if not in_radius(ship, state["target"], ship.sensor_range, lambda s:s.position) or not state["target"].is_alive():
                    state["patrolling"] = True
                    state.pop("target")
                else:
                    state["patrolling"] = False

                    # if the target is still in range, then attack and pursue.
                    action = PlayerAction.attack
                    action_param_1 = state["target"].id

                    state["heading"] = state["target"].position
            else:
                state["patrolling"] = False
        else:
            state["patrolling"] = True

        if state.get("patrolling"):
            # if we get here, continue moving to waypoint
            distance = distance_to(
                    ship,
                    state["waypoint"],
                    lambda s: s.position)

            if not ( -5 < distance[0] < 5 and -5 < distance[1] < 5):
                # we are not at waypoint, continue moving towards
                state["heading"] = state["waypoint"].position

            else:
                # on to the next station
                idx = state["patrol_route"].index(state["waypoint"])
                idx = 0 if idx+1 >= len(state["patrol_route"]) else idx+1
                state["waypoint"] = state["patrol_route"][idx]

                state["heading"] = state["waypoint"].position


            # work around to fix bug where some police would reach their waypoint
            # but not move on to the next
            if "last_pos" in state:
                if(ship.position[0] == state["last_pos"][0] and
                    ship.position[1] == state["last_pos"][1] and
                    state["waypoint"].position[0] == ship.position[0] and
                    state["waypoint"].position[1] == ship.position[1]):

                    state["waypoint"] = random.choice(state["patrol_route"])
                    state["heading"] = state["waypoint"].position
        state["last_pos"] = ship.position

        return {
            "move_action": state.get("heading"),
            "action": action,
            "action_param_1": action_param_1,
            "action_param_2": action_param_2,
            "action_param_3": action_param_3,
        }

    def guarding_police(self, ship, state, universe):
        action = None
        action_param_1 = None
        action_param_2 = None
        action_param_3 = None


        if not state.get("target"):
            # if we need a target...
            target = self.closest_pirate(ship, universe)

            if target is not None:
                state["target"] = target
                state["heading"] = target.position

            else:
                state["heading"] = None
                state["target"] = None
        else:
            # if we have a target...

            # update target location
            target_ships = get_ships(universe, lambda s:s.id==state["target"].id)
            if len(target_ships) > 0:
                state["target"] = target_ships[0]

            else:
                # target is out of range, pick a new one
                if not (in_radius(ship, state["target"], ship.sensor_range, lambda s:s.position)
                        and state["target"].is_alive(),
                        not self.in_safe_zone(state["target"])  # target not in sz
                        ):
                    target = self.closest_pirate(ship, universe)
                else:
                    target = None

                state["target"] = target



        if state.get("target"):
            # if we have a target move toward it and attack

            if not state["target"].is_alive():
                # don't go toward dead target
                state["target"] = None
                state["heading"] = None

            else:
                # advance and attack living target
                action = PlayerAction.attack
                action_param_1 = state["target"].id

                # also overwrite target and begin persuing if in safe zone
                if self.in_safe_zone(state["target"]):
                    state["heading"] = state["target"].position
                else:
                    state["target"] = None
                    state["heaing"] = None


        # verify current heading does not place us out of the safe zone
        if not (state.get("heading") and self.in_safe_zone(state["heading"], lambda e:e)):
            state["heading"] = None

        if  not state.get("heading"):
            if not state.get("waypoint"):
                state["waypoint"] = self.get_point_in_safe_zone()
            elif state["waypoint"] == ship.position:  # we are at waypoint
                state["waypoint"] = self.get_point_in_safe_zone()

            state["heading"] = state["waypoint"]

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


    def closest_pirate(self, police_ship, universe):
        ships = get_ships(universe, lambda s: (
                s.legal_standing >= LegalStanding.pirate
                and in_radius(police_ship, s, police_ship.sensor_range, lambda s:s.position)
                and s.is_alive())
        )

        num_ships = len(ships)

        if num_ships > 1:
            ships = sorted(ships, key=lambda e: distance_to(police_ship, e, lambda x:x.position))
            return ships[0]
        elif num_ships == 1:
            return ships[0]
        else:
            return None

    def random_point_in_circle(self, radius):
        r = radius * (random.random()**2)
        theta = random.random() * 2 * math.pi
        return (
            r * math.cos(theta),
            r * math.sin(theta)
        )

    def in_safe_zone(self, ship, accessor=None):
        sz = percent_world(0.5, 0.5)

        if not accessor: accessor = lambda e:e.position
        return in_radius(sz, ship, SECURE_ZONE_RADIUS, lambda e:e, accessor, verify_instance=False)


    def get_point_in_safe_zone(self):
        center = percent_world(0.5, 0.5)
        pt = self.random_point_in_circle(SECURE_ZONE_RADIUS)
        pt = (
            center[0]+pt[0],
            center[1]+pt[1]
        )
        return pt
