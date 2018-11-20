from uuid import uuid4

from game.common.game_serializable import Serializable
from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import GameStats


class IllegalSalvage(GameObject):

    def init(self, position=(0,0), value=0):
        GameObject.init(self, ObjectType.illegal_salvage)

        self.position = position
        self.material_type = MaterialType.salvage
        self.turns_till_recycling = 20
        self.value = value

    def to_dict(self, security_level=SecurityLevel.other_player):
        data = GameObject.to_dict(self)

        if security_level is SecurityLevel.engine:
            # fields only accessible to the engine
            engine = {

            }

            data = { ** data, **engine }

        if security_level <= SecurityLevel.player_owned:
            # fields only accessible to the player owner of this object
            # Could be used to determine who gets priority of the salvage
            pass

        if security_level <= SecurityLevel.other_player:
            # fields other players can view
            other_player = {
                "position": self.position,
                "material_type": self.material_type,

                "turns_till_recycling": self.turns_till_recycling,
                "value": self.value
            }

            data = { **data, **other_player }

            return data

    def from_dict(self, data, security_level=SecurityLevel.other_player):
        GameObject.from_dict(self, data)

        if security_level is SecurityLevel.engine:
            # properties that will only be populated by the engine,
            #   prevents user tampering with variables

            self.position = data["position"]
            self.material_type = data["material_type"]

            self.turns_till_recycling = data["turns_till_recycling"]
            self.value = data["value"]

        if security_level <= SecurityLevel.player_owned:
            pass

        if security_level <= SecurityLevel.other_player:
            pass