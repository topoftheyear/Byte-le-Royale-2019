from uuid import uuid4

from game.common.game_serializable import Serializable
from game.common.enums import *
from game.common.stats import GameStates


class Ship(Serializable):

    def __init__(self):
        self.initialized = False


    def init(self, player_name, ):

        # used by engine to track ships
        self.id = str(uuid4())

        # allows players to track ships by random id
        #   could be changed to be more readable.
        self.public_id = str(uuid4())

        self.player_name = player_name

        self.max_hull = GameStats.get_ship_stat(UpgradeType.hull, UpgradeLevel.base)
        self.current_hull = self.max_hull


        self.engine_speed = GameStats.get_ship_stat(UpgradeType.engine_speed, UpgradeLevel.base)

        self.weapon_damage = GameStats.get_ship_stat(UpgradeType.weapon_damage, UpgradeLevel.base)

        self.cargo_space = GameStats.get_ship_stat(UpgradeType.cargo_space, UpgradeLevel.base)

        self.mining_yield = GameStats.get_ship_stat(UpgradeType.mining_yield, UpgradeLevel.base)

        self.sensor_range = GameStats.get_ship_stat(UpgradeType.sensor_range, UpgradeLevel.base)

        self.module_0 = UpgradeType.empty
        self.module_1 = UpgradeType.locked
        self.module_2 = UpgradeType.locked
        self.module_3 = UpgradeType.locked

        # ideally a dictionary of ItemType enums mapped to a count of the number of that item
        self.inventory = {}

        self.position = (0,0)

        self.player_move_action = (0,0)
        self.player_action = PlayerAction.none


    def to_dict(self, security_level=SecurityLevel.other_player):
        data = {}

        if security_level is SecurityLevel.engine:
            # fields that only the engine (server, visualizer, logs) should
            #   be able to access
            engine = {
                "id": self.id,
                "player_name": self.player_name
            }


            data = { *data, *engine }

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

                "player_move_action": self.player_move_action,
                "player_action": self.player_action
            }

            data = { *data, *player_owned }

        if security_level <= SecurityLevel.other_player:
            # fields that other players can view on this object

            other_player = {
                "public_id": self.public_id,
                "max_hull": self.max_hull,
                "current_hull": self.current_hull,
                "cargo_space": self.cargo_space,
                "position": self.position,
                "inventory": self.inventory
            }


            data = { *data, *other_player }


        return data


    def from_dict(self, data, security_level=SecurityLevel.other_player):

        if security_level is SecurityLevel.engine:
            # properties that will only be populated by the engine,
            #   prevents user tampering with variables

            self.id = data["id"]
            self.public_id = data["public_id"]
            self.player_name = data["player_name"]

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


        if security_level <= SecurityLevel.player_owned:
            # properties that the owner of a ship can update
            #   prevents other players from tampering with our ship

            self.player_move_action = data["player_move_action"]
            self.player_action = data["player_action"]


        if security_level <= SecurityLevel.other_player:
            pass

