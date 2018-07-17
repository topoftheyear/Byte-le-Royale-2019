from uuid import uuid4

from game.common.game_object import GameObject
from game.common.enums import *
from game.common.material_types import *

class Station(GameObject):

    def init(self, name, station_type=ObjectType.station, position=(0,0), consumption_material=None, consumption_rate=1, production_material=None, production_rate=1, current_cargo=0, accessibility_radius=5):
        GameObject.init(self, station_type)

        self.id = str(uuid4())
        self.name = name

        self.position = position

        self.consumption_material = consumption_material
        self.consumption_rate = consumption_rate
        self.production_material = production_material
        self.production_rate = production_rate

        self.current_cargo = current_cargo

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

                "consumption_material": self.consumption_material,
                "consumption_rate": self.consumption_rate,
                "production_material": self.production_material,
                "production_rate": self.production_rate ,

                "current_cargo": self.current_cargo,

                "accessibility_radius": self.accessibility_radius
            }


            data = { **data, **other_player }

        return data


    def from_dict(self, data, security_level=SecurityLevel.other_player):
        GameObject.from_dict(self, data)

        if security_level is SecurityLevel.engine:
            # properties that will only be populated by the engine,
            #   prevents user tampering with variables

            self.id = data["id"]
            self.name = data["name"]

            self.position = data["position"]

            self.consumption_material = data["consumption_material"]
            self.consumption_rate = data["consumption_rate"]
            self.production_material = data["production_material"]
            self.production_rate = data["production_rate"]

            self.current_cargo = data["current_cargo"]

            self.accessibility_radius = data["accessibility_radius"]

        if security_level <= SecurityLevel.player_owned:
            pass

        if security_level <= SecurityLevel.other_player:
            pass

class BlackMarketStation(Station):
    def init(self, name, position=(0,0), consumption_material=None, consumption_rate=1, production_material=None, production_rate=1, current_cargo=0, accessibility_radius=5, object_type=ObjectType.station):
        Station.init(self, name, position=position, consumption_material=consumption_material, consumption_rate=consumption_rate, production_material=production_material, production_rate=production_rate, current_cargo=0, accessibility_radius=5, station_type=ObjectType.black_market_station)


class SecureStation(Station):
    def init(self, name, position=(0,0), consumption_material=None, consumption_rate=1, production_material=None, production_rate=1, current_cargo=0, accessibility_radius=5, object_type=ObjectType.station):
        Station.init(self, name, position=position, consumption_material=consumption_material, consumption_rate=consumption_rate, production_material=production_material, production_rate=production_rate, current_cargo=0, accessibility_radius=5, station_type=ObjectType.secure_station)
