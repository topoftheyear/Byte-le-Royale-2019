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
import game.utils.filters as F

class PoliceVariant:
    waiting = 1
    patrolling = 3
    guarding = 4

class PoliceController:

    def __init__(self):

        self.debug = False
        self.events = []
        self.stats = []

        self.states = {}

        self.police_spawn_counter = 0
        self.police_spawn_timeout = 5

        self.profiles = {}



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

            universe.add_object(new_police)
            p.append(new_police)

            self.events.append({
                "type": LogEvent.police_spawned,
                "ship_id": new_police.id,
            })

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
        new_enforcers = []
        to_remove = []

        living_police = 0

        for police in universe.get(ObjectType.police):

            #  remove dead police
            if police.is_alive():
                living_police += 1
            else:
                universe.remove_object(police)
                self.events.append({
                    "type": LogEvent.police_removed,
                    "ship_id": police.id
                })

        for ship in universe.get_filtered(
                ObjectType.ship,
                filter=F.GT(ENFORCER_THRESHOLD, lambda e: e.legal_standing)):
            # track new pirates
            if ship.team_name not in self.profiles:
                self.profiles[ship.team_name] = {
                    "ship": ship.id,
                    "wave_counter": 0,
                    "wave_timer": 0,
                    "assigned_enforcers": []
                }

        teams_to_remove = []
        for team_name in self.profiles.keys():
            # stop tracking ships that are no longer within enforcer thresh
            ship = universe.get_filtered_one(
                ObjectType.ship,
                AND(
                    F.EQ(team_name),
                    F.less_than(ENFORCER_THRESHOLD, lambda e: e.legal_standing)
                ))

            if ship is not None:
                teams_to_remove.append(team_name)

            # stop tracking ships that are destroyed
            ship = universe.get_filtered_one(
                ObjectType.ship,
                AND(
                    F.EQ(team_name),
                    F.alive()
                ))
            if ship is not None:
                teams_to_remove.append(team_name)

        for team_name in teams_to_remove:
            if team_name in self.profiles:
                del self.profiles[team_name]

        # spawn enforcers if needed
        for team_name, profile in self.profiles.items():
            if profile["wave_timer"] <= 0:
                profile["wave_counter"] += 1
                self.print("Spawning {} enforcers".format(profile["wave_counter"]))
                for _ in range(profile["wave_counter"]):
                    # spawn new enforcer

                    new_enforcer = PoliceShip()
                    pos = percent_world(0.5, 0.5)
                    pos[0] += random.randint(-5, 5)
                    pos[1] += random.randint(-5, 5)
                    new_enforcer.init(level=3, position=pos)

                    profile["assigned_enforcers"].append(new_enforcer)

                    self.create_state(new_enforcer)

                    universe.add_object(new_enforcer)

                    self.events.append({
                        "type": LogEvent.enforcer_spawned,
                        "ship_id": new_enforcer.id
                    })

                profile["wave_timer"] = ENFORCER_WAVE_TIMER + 1  # +1 to compensate for -1 this turn

            profile["wave_timer"] -= 1

        # despawn enforcers without a profile if at center
        assigned_enforcers = [ e for _,p in self.profiles.items() for e in p["assigned_enforcers"]]
        for enforcer in universe.get(ObjectType.enforcer):
            # if at center of world
            there = in_radius(enforcer, percent_world(0.5, 0.5), 15, lambda e: e.position, lambda t: t)
            if there and enforcer not in assigned_enforcers:
                # if has no profile and should be removed
                self.print("Despawning enforcer {}".format(enforcer.id))
                to_remove.append(enforcer)
                self.events.append({
                    "type": LogEvent.despawn_enforcer,
                    "ship_id": enforcer.id
                })

        # Spawn more police if needed
        living_police = sum([e.is_alive() for e in universe.get(ObjectType.police)])

        if living_police < NUM_POLICE:
            self.police_spawn_counter += 1

            if self.police_spawn_counter >= self.police_spawn_timeout:
                new_ship = PoliceShip()
                new_ship.init(level=1, position=percent_world(0.5, 0.5))
                self.create_state(new_ship)

                new_police.append(new_ship)
                self.police_spawn_counter = 0

                universe.add_object(new_ship)
                self.events.append({
                    "type": LogEvent.police_spawned,
                    "ship_id": new_ship.id,
                })

        return new_police, new_enforcers, to_remove


    def take_turn(self, police_ship, universe):
        ship_state = self.states[police_ship.id]

        self.reset_actions(police_ship)

        if police_ship.object_type == ObjectType.police:
            return self.police_take_turn(police_ship, ship_state, universe)
        elif police_ship.object_type == ObjectType.enforcer:
            self.print("enforcer taking turn")
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
            id = state["target"].id
            target_ships = [ ship for ship in universe.get("ships") if ship.id == id]
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
            stations = universe.get("all_stations")

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
            id = state["target"].id
            target_ships = [ ship for ship in universe.get("ships") if ship.id == id]
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

            if not ( -5 < distance < 5 ):
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
            id = state["target"].id
            target_ships = [ ship for ship in universe.get("ships") if ship.id == id]
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

        if not state.get("heading"):
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
        action = None
        action_param_1 = None
        action_param_2 = None
        action_param_3 = None

        # find profile
        self.print("Finding profile")
        profile_name = None
        profile = None
        for p_name, p in self.profiles.items():
            if ship in p["assigned_enforcers"]:
                profile_name = p_name
                profile = p
                break

        if profile is None:
            self.print("Could not find profile, moving to center")
            # then the ship we were tracking is no longer within enforcer thresh
            # set heading to the center of the map

            center = percent_world(0.5, 0.5)
            state["heading"] = center
        else:
            self.print("Profile found, locating target")

            # get target
            target = None
            for ship in universe.get(ObjectType.ship):
                if ship.id == profile["ship"]:
                    target = ship
                    break

            if target is None or not target.is_alive():
                self.print("target not found or dead, moving to center.")
                # target is dead, head towards center
                state["heading"] = percent_world(0.5, 0.5)
            else:
                self.print("target found, following")
                # target is alive follow and try to attack
                state["heading"] = target.position

                # attack target if in range
                if in_radius(ship, target, ship.weapon_range, lambda e:e.position):
                    self.print("target in attack range attacking")
                    action = PlayerAction.attack
                    action_param_1 = ship.id

        return {
            "move_action": state["heading"],
            "action": action,
            "action_param_1": action_param_1,
            "action_param_2": action_param_2,
            "action_param_3": action_param_3,
        }



    def reset_actions(self, ship):
        ship.action = None
        ship.action_param_1 = None
        ship.action_param_2 = None
        ship.action_param_3 = None
        ship.move_action = None



    def closest_pirate(self, police_ship, universe):

        range_pred = F.in_radius(police_ship, police_ship.sensor_range, lambda s: s.position)
        ships = universe.get_filtered(ObjectType.ship, filter=F.AND(F.alive(), F.pirate(), range_pred))

        num_ships = len(ships)

        if num_ships > 1:
            ship = min(ships, key=lambda e: distance_to(police_ship, e, lambda x:x.position))
            return ship
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
