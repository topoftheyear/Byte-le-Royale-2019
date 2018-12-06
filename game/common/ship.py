from uuid import uuid4

from game.common.game_serializable import Serializable
from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import GameStats

focus_team = None


class Ship(GameObject):

    def __init__(self):
        global focus_team

    def init(self, team_name, is_npc=False, position=(0,0)):
        global focus_team
        if focus_team is not None and team_name == focus_team:
            GameObject.init(self, ObjectType.player_ship)
            print("PLAYER FOUND")
        else:
            GameObject.init(self, ObjectType.ship)
            # print(team_name)

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

        self.max_hull = GameStats.get_ship_stat(ShipStat.hull, ModuleLevel.base)
        self.current_hull = self.max_hull

        self.engine_speed = GameStats.get_ship_stat(ShipStat.engine_speed, ModuleLevel.base)

        self.weapon_damage = GameStats.get_ship_stat(ShipStat.weapon_damage, ModuleLevel.base)
        self.weapon_range = GameStats.get_ship_stat(ShipStat.weapon_range, ModuleLevel.base)

        self.cargo_space = GameStats.get_ship_stat(ShipStat.cargo_space, ModuleLevel.base)

        self.mining_yield = GameStats.get_ship_stat(ShipStat.mining_yield, ModuleLevel.base)

        self.sensor_range = GameStats.get_ship_stat(ShipStat.sensor_range, ModuleLevel.base)

        self.module_0 = ModuleType.empty
        self.module_1 = ModuleType.locked
        self.module_2 = ModuleType.locked
        self.module_3 = ModuleType.locked

        self.module_0_level = ModuleLevel.base
        self.module_1_level = ModuleLevel.base
        self.module_2_level = ModuleLevel.base
        self.module_3_level = ModuleLevel.base

        self.action = PlayerAction.none
        self.action_param_1 = None
        self.action_param_2 = None
        self.action_param_3 = None
        self.move_action = None

        # ideally a dictionary of ItemType enums mapped to a count of the number of that item
        self.inventory = {}

        self.position = position

        self.notoriety = 0
        self.legal_standing = LegalStanding.citizen

        self.respawn_counter = -1

        self.credits = 200

    def to_dict(self, security_level=SecurityLevel.other_player):
        data = GameObject.to_dict(self)

        if security_level is SecurityLevel.engine:
            # fields that only the engine (server, visualizer, logs) should
            #   be able to access
            engine = {
                "id": self.id,
                "team_name": self.team_name,
                "is_npc": self.is_npc,
            }


            data = { **data, **engine }

        if security_level <= SecurityLevel.player_owned:
            # fields that the player who owns the object can view
            player_owned = {
                "engine_speed": self.engine_speed,
                "weapon_damage": self.weapon_damage,
                "weapon_range": self.weapon_range,
                "cargo_space": self.cargo_space,
                "mining_yield": self.mining_yield,
                "sensor_range": self.sensor_range,

                "module_0": self.module_0,
                "module_1": self.module_1,
                "module_2": self.module_2,
                "module_3": self.module_3,

                "module_0_level": self.module_0_level,
                "module_1_level": self.module_1_level,
                "module_2_level": self.module_2_level,
                "module_3_level": self.module_3_level,

                "action": self.action,
                "action_param_1": self.action_param_1,
                "action_param_2": self.action_param_2,
                "action_param_3": self.action_param_3,
                "move_action": self.move_action,

                "respawn_counter": self.respawn_counter,

                "credits": self.credits,
            }

            data = { **data, **player_owned }

        if security_level <= SecurityLevel.other_player:
            # fields that other players can view on this object

            other_player = {
                "public_id": self.public_id,
                "max_hull": self.max_hull,
                "current_hull": self.current_hull,
                "cargo_space": self.cargo_space,
                "position": self.position,
                "inventory": self.inventory,

                "notoriety": self.notoriety,
                "legal_standing": self.legal_standing,
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
            self.weapon_range = data["weapon_range"]
            self.cargo_space = data["cargo_space"]
            self.mining_yield = data["mining_yield"]
            self.sensor_range = data["sensor_range"]

            self.module_0 = data["module_0"]
            self.module_1 = data["module_1"]
            self.module_2 = data["module_2"]
            self.module_3 = data["module_3"]

            self.module_0_level = data["module_0_level"]
            self.module_1_level = data["module_1_level"]
            self.module_2_level = data["module_2_level"]
            self.module_3_level = data["module_3_level"]

            self.position = data["position"]

            self.inventory = data["inventory"]

            self.is_npc = data["is_npc"]

            self.notoriety = data["notoriety"]
            self.legal_standing = data["legal_standing"]

            self.respawn_counter = data["respawn_counter"]

            self.credits = data["credits"]

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

    @staticmethod
    def set_focus_team(self, team_name=None):
        global focus_team
        focus_team = team_name

    def is_alive(self):
        return self.current_hull > 0

