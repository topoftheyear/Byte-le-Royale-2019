from uuid import uuid4

from game.common.game_object import GameObject
from game.common.enums import *
from game.common.material_types import *

class AsteroidField(GameObject):

    def init(self, field_type, name, material_type, position=(0,0), mining_rate=1, accessibility_radius=200):
        GameObject.init(self, field_type)

        self.name = name

        self.position = position

        self.material_type = material_type
        self.mining_rate = mining_rate

        self.accessibility_radius = accessibility_radius


    def to_dict(self, security_level=SecurityLevel.other_player):
        data = GameObject.to_dict(self)

        if security_level is SecurityLevel.engine:
            # fields only accessible to the engine
            engine = {
                "id": self.id
            }

            data = { **data, **engine }

        if security_level <= SecurityLevel.player_owned:
            # fields only accessible to the player owner of this object

            # technically a feasible and interesting direction to go but not discussed yet
            pass


        if security_level <= SecurityLevel.other_player:
            # fields other players can view
            other_player = {
                "name": self.name,

                "position": self.position,

                "material_type": self.material_type,
                "mining_rate": self.mining_rate,

                "accessibility_radius": self.accessibility_radius
            }

            data = { **data, **other_player }

            return data


    def from_dict(self, data, security_level=SecurityLevel.other_player):
        GameObject.from_dict(self, data)

        if security_level is SecurityLevel.engine:
            # properties that will only be populated by the engine,
            #   prevents user tampering with variables

            self.name = data["name"]
            self.position = data["position"]
            self.material_type = data["material_type"]
            self.mining_rate = data["mining_rate"]

            self.accessibility_radius = data["accessibility_radius"]

        if security_level <= SecurityLevel.player_owned:
            pass

        if security_level <= SecurityLevel.other_player:
            pass

