import random
import sys

from game.config import NUM_POLICE, WORLD_BOUNDS
from game.common.enums import *
from game.common.name_helpers import *
from game.common.police_ship import PoliceShip
from game.utils.helpers import *

class PoliceController:

    def __init__(self):

        self.debug = True
        self.events = []
        self.stats = []

        self.states = {}


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
        pass


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

        # if at heading, clear heading
        if(state.get("heading", None) is not None
                and state["heading"] == ship.position[0]
                and state["heading"] == ship.position[1]):
            self.heading = None

        # pick new location if at location
        if state.get("heading", None) is None:
            state["heading"] = random.choice(list(filter(lambda e:e.object_type != ObjectType.ship, universe))).position

        # attack ships in range
        ships = ships_in_attack_range(universe, ship)
        ships = filter(lambda e: e.object_type == ObjectType.ship, ships)
        ship_to_attack = next(ships, None)
        if ship_to_attack:
            action = PlayerAction.attack
            action_param_1 = ship_to_attack.id

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

        # if at heading, clear heading
        if("heading" in state and state["heading"] is not None
                and state["heading"] == ship.position[0]
                and state["heading"] == ship.position[1]):
            self.heading = None

        # pick new location if at location
        if state.get("heading", None) is None:
            state["heading"] = random.choice(list(filter(lambda e:e.object_type != ObjectType.ship, universe))).position

        # attack ships in range
        ships = ships_in_attack_range(universe, ship)
        ships = filter(lambda e: e.object_type == ObjectType.ship, ships)
        ship_to_attack = next(ships, None)
        if ship_to_attack:
            action = PlayerAction.attack
            action_param_1 = ship_to_attack.id

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


