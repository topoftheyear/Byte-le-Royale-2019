from uuid import uuid4

from game.common.game_serializable import Serializable
from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import GameStats


class Ship(GameObject):

    def __init__(self):
        pass


    def init(self, team_name, is_npc=False, position=(0,0)):
        GameObject.init(self, ObjectType.ship)

        # used by engine to track ships
        self.id = str(uuid4())

        # used to match NPC client instances to npc ships
        self.is_npc = is_npc

        # allows players to track ships by random id
        #   could be changed to be more readable.
        self.public_id = str(uuid4())

        if self.is_npc:
            self.team_name = team_name + f" ({self.id})"
        else:
            self.team_name = team_name

        self.max_hull = GameStats.get_ship_stat(UpgradeType.hull, UpgradeLevel.base)
        self.current_hull = self.max_hull


        import random
        self.engine_speed = random.randint(3,10)#GameStats.get_ship_stat(UpgradeType.engine_speed, UpgradeLevel.base)

        self.weapon_damage = GameStats.get_ship_stat(UpgradeType.weapon_damage, UpgradeLevel.base)

        self.cargo_space = GameStats.get_ship_stat(UpgradeType.cargo_space, UpgradeLevel.base)

        self.mining_yield = GameStats.get_ship_stat(UpgradeType.mining_yield, UpgradeLevel.base)

        self.sensor_range = GameStats.get_ship_stat(UpgradeType.sensor_range, UpgradeLevel.base)

        self.module_0 = UpgradeType.empty
        self.module_1 = UpgradeType.locked
        self.module_2 = UpgradeType.locked
        self.module_3 = UpgradeType.locked

        self.action = PlayerAction.none
        self.action_param_1 = None
        self.action_param_2 = None
        self.action_param_3 = None
        self.move_action = None

        # ideally a dictionary of ItemType enums mapped to a count of the number of that item
        self.inventory = {}

        self.position = position


    def to_dict(self, security_level=SecurityLevel.other_player):
        data = GameObject.to_dict(self)

        if security_level is SecurityLevel.engine:
            # fields that only the engine (server, visualizer, logs) should
            #   be able to access
            engine = {
                "id": self.id,
                "team_name": self.team_name
            }


            data = { **data, **engine }

        if security_level <= SecurityLevel.player_owned:
            # fields that the player who owns the object can view
            player_owned = {
                "engine_speed": self.engine_speed,
                "weapon_damage": self.weapon_damage,
                "cargo_space": self.cargo_space,
                "mining_yield": self.mining_yield,

                "module_0": self.module_0,
                "module_1": self.module_1,
                "module_2": self.module_2,
                "module_3": self.module_3,

                "action": self.action,
                "action_param_1": self.action_param_1,
                "action_param_2": self.action_param_2,
                "action_param_3": self.action_param_3,
                "move_action": self.move_action,
            }

            data = { **data, **player_owned }

        if security_level <= SecurityLevel.other_player:
            # fields that other players can view on this object

            other_player = {
                "public_id": self.public_id,
                "is_npc": self.is_npc,
                "max_hull": self.max_hull,
                "current_hull": self.current_hull,
                "cargo_space": self.cargo_space,
                "position": self.position,
                "inventory": self.inventory
            }


            data = { **data, **other_player }


        return data


    def from_dict(self, data, security_level=SecurityLevel.other_player):
        GameObject.from_dict(self, data)

        if security_level is SecurityLevel.engine:
            # properties that will only be populated by the engine,
            #   prevents user tampering with variables

            self.id = data["id"]
            self.public_id = data["public_id"]
            self.team_name = data["team_name"]

            self.max_hull = data["max_hull"]
            self.current_hull = data["current_hull"]

            self.engine_speed = data["engine_speed"]
            self.weapon_damage = data["weapon_damage"]
            self.cargo_space = data["cargo_space"]
            self.mining_yield = data["mining_yield"]

            self.module_0 = data["module_0"]
            self.module_1 = data["module_1"]
            self.module_2 = data["module_2"]
            self.module_3 = data["module_3"]

            self.position = data["position"]

            self.inventory = data["inventory"]

            self.is_npc = data["is_npc"]


        if security_level <= SecurityLevel.player_owned:
            # properties that the owner of a ship can update
            #   prevents other players from tampering with our ship

            self.action = data["action"]
            self.move_action = data["move_action"]
            self.action_param_1 = data["action_param_1"]
            self.action_param_2 = data["action_param_2"]
            self.action_param_3 = data["action_param_3"]


        if security_level <= SecurityLevel.other_player:
            pass



    def is_alive(self):
        return self.current_hull > 0
