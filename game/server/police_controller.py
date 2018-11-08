import random
import sys
import functools

from game.config import NUM_POLICE, WORLD_BOUNDS
from game.common.enums import *
from game.common.name_helpers import *
from game.common.police_ship import PoliceShip
from game.utils.helpers import *
from game.utils.projection import *

class PoliceVariant:
    free_roaming = 0
    flitting = 1
    patroling = 3
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

        if "variation" not in state:
            state["variation"] = random.choices([
                #PoliceVariant.free_roaming,
                #PoliceVariant.flitting,
                PoliceVariant.patroling,
                #PoliceVariant.guarding,
                ],
                #[
                #    0.15, # free roam
                #    0.10, # flitting
                #    0.25, # patroling
                #    0.50, # guarding
                #])
                )[0]


        if state["variation"] is PoliceVariant.free_roaming:
            return self.free_roaming_police(ship, state, universe)
        elif state["variation"] is PoliceVariant.flitting:
            return self.flitting_police(ship, state, universe)
        elif state["variation"] is PoliceVariant.patroling:
            return self.patroling_police(ship, state, universe)
        elif state["variation"] is PoliceVariant.guarding:
            return self.guarding_police(ship,state, universe)


    def free_roaming_police(self, ship, state, universe):
        action = None
        action_param_1 = None
        action_param_2 = None
        action_param_3 = None


        # pick target
        pick_target = lambda universe: random.choice(
                list(filter(lambda e:e.object_type == ObjectType.ship, universe)))

        if "target" not in state:
            target = pick_target(universe)
            state["target"] = target.id
            state["heading"] = target.position
        else:

            if state["target"] is None:
                target = pick_target(universe)
                state["target"] = target.id

            target = next(
                    filter(
                        lambda e:e.object_type == ObjectType.ship
                        and e.id == state["target"], universe), None)

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
        ships = filter(
                lambda e: e.object_type == ObjectType.ship
                and e.legal_standing == LegalStanding.pirate, ships)
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

    def flitting_police(self, ship, state, universe):
        action = None
        action_param_1 = None
        action_param_2 = None
        action_param_3 = None


        # pick target
        pick_target = lambda universe: random.choice(
                list(filter(lambda e:e.object_type == ObjectType.ship, universe)))

        if "target" not in state:
            target = pick_target(universe)
            state["target"] = target.id
            state["heading"] = target.position
        else:

            if state["target"] is None:
                target = pick_target(universe)
                state["target"] = target.id

            target = next(
                    filter(
                        lambda e:e.object_type == ObjectType.ship
                        and e.id == state["target"], universe), None)

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
        ships = filter(
                lambda e: e.object_type == ObjectType.ship
                and e.legal_standing == LegalStanding.pirate, ships)
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

    def patroling_police(self, ship, state, universe):
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


        # check ships nearby to verify no pirates
        if "target" not in state:
            ships = get_ships(universe, lambda s: s.legal_standing >= LegalStanding.pirate)

            num_ships = len(ships)

            if num_ships > 1:
                ships = sorted(ships, key=lambda e: distance_to(ship, e, lambda x:x.position))
                target_ship = next(filter(lambda s:s != ship, ships))
            elif num_ships == 1:
                target_ship = ships[0]
            else:
                target_ship = None

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
                # forget them and resume patroling
                if not in_radius(ship, state["target"], ship.sensor_range, lambda s:s.position) or not state["target"].is_alive():
                    state["patroling"] = True
                    state.pop("target")
                else:
                    state["patroling"] = False

                    # if the target is still in range, then attack and pursue.
                    action = PlayerAction.attack
                    action_param_1 = state["target"].id

                    state["heading"] = state["target"].position
            else:
                state["patroling"] = False
        else:
            state["patroling"] = True

        if state.get("patroling"):
            # if we get here, continue moving to waypoint

            distance = distance_to(
                    ship,
                    state["waypoint"],
                    lambda s: s.position)

            if not (distance[0] is 0 and distance[1] is 0):
                # we are not at waypoint, continue moving towards
                state["heading"] = state["waypoint"].position

            else:
                # on to the next station
                idx = state["patrol_route"].index(state["waypoint"])
                idx = 0 if idx+1 >= len(state["patrol_route"]) else idx+1
                state["waypoint"] = state["patrol_route"][idx]

                state["heading"] = state["waypoint"].position

        return {
            "move_action": state.get("heading") or ship.position,
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


