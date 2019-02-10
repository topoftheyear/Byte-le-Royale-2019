from uuid import uuid4

from game.common.game_serializable import Serializable
from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import GameStats

focus_team = None


class Ship(GameObject):

    def __init__(self):
        pass

    def init(self, team_name, color=[255, 255, 255], is_npc=False, position=None):
        GameObject.init(self, ObjectType.ship)

        # used by engine to track ships
        self.id = str(uuid4())

        # used to match NPC client instances to npc ships
        self.is_npc = is_npc

        # allows players to track ships by random id
        #   could be changed to be more readable.
        self.public_id = str(uuid4())
        self.team_name = team_name

        if self.is_npc:
            self.color = None
        else:
            self.color = color

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

        self.bounty = 0
        self.bounty_list = []

        self.respawn_counter = -1

        self.credits = 2000

        self.passive_repair_counter = GameStats.passive_repair_counter

    def to_dict(self, security_level=SecurityLevel.other_player):
        data = GameObject.to_dict(self)

        if security_level is SecurityLevel.engine:
            # fields that only the engine (server, visualizer, logs) should
            #   be able to access
            engine = {
                "is_npc": self.is_npc,

                "bounty_list": self.bounty_list
            }


            data = { **data, **engine }

        if security_level <= SecurityLevel.player_owned:
            # fields that the player who owns the object can view
            player_owned = {
                "id": self.id,

                "team_name": self.team_name,
                "color": self.color,

                "respawn_counter": self.respawn_counter,

                "credits": self.credits,

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
                "max_hull": self.max_hull,
                "current_hull": self.current_hull,
                "cargo_space": self.cargo_space,
                "position": self.position,
                "inventory": self.inventory,

                "notoriety": self.notoriety,
                "legal_standing": self.legal_standing,

                "bounty": self.bounty,

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

                "bounty_list": self.bounty_list,

                "passive_repair_counter": self.passive_repair_counter,
            }


            data = { **data, **other_player }


        return data

    def from_dict(self, data, security_level=SecurityLevel.other_player):
        GameObject.from_dict(self, data)

        if security_level is SecurityLevel.engine:
            # properties that will only be populated by the engine,
            #   prevents user tampering with variables
            self.is_npc = data["is_npc"]

            self.bounty_list = data["bounty_list"]

        if security_level <= SecurityLevel.player_owned:
            # properties that the owner of a ship can update
            #   prevents other players from tampering with our ship
            self.id = data["id"]

            self.team_name = data["team_name"]
            self.color = data["color"]

            self.respawn_counter = data["respawn_counter"]

            self.credits = data["credits"]

            self.action = data["action"]
            self.move_action = data["move_action"]
            self.action_param_1 = data["action_param_1"]
            self.action_param_2 = data["action_param_2"]
            self.action_param_3 = data["action_param_3"]

            if((self.action_param_1 is not None and self.action_param_1 > 2147483647)
                    or (self.action_param_2 is not None and self.action_param_2 > 2147483647)
                    or (self.action_param_3 is not None and self.action_param_3 > 2147483647)):
                print("Action parameters cannot be larter than 2147483647")
                exit(1)


        if security_level <= SecurityLevel.other_player:
            self.public_id = data["public_id"]

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

            self.notoriety = data["notoriety"]
            self.legal_standing = data["legal_standing"]
            self.bounty = data["bounty"]

            self.passive_repair_counter = data["passive_repair_counter"]

    def is_alive(self):
        return self.current_hull > 0

