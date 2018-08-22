from uuid import uuid4

from game.common.game_object import GameObject
from game.common.enums import *
from game.common.material_types import *

class Station(GameObject):

    def init(self,
            name,
            station_type=ObjectType.station,
            position=(0,0),

            primary_import=None,
            primary_consumption_qty=1,
            primary_max = 200,

            secondary_import=None,
            secondary_consumption_qty=1,
            secondary_max = 50,

            production_frequency=5,
            production_material=None,
            production_qty=1,
            production_max = 200,

            cargo=None,
            accessibility_radius=5):
        GameObject.init(self, station_type)

        self.id = str(uuid4())
        self.name = name

        self.position = position

        self.primary_import = primary_import # primary import material
        self.primary_consumption_qty = primary_consumption_qty # qty to consume in one shot
        self.primary_max = primary_max

        self.secondary_import = secondary_import
        self.secondary_consumption_qty = secondary_consumption_qty
        self.secondary_max = secondary_max

        self.production_frequency = production_frequency # how often to consume inputs to create output
        self.production_material = production_material
        self.production_qty = production_qty
        self.production_max = production_max

        self.sell_price = 0
        self.primary_buy_price = 0
        self.secondary_buy_price = 0

        if cargo is None:
            self.cargo = {}
        else:
            self.cargo = cargo

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

                "primary_import": self.primary_import,
                "primary_consumption_qty": self.primary_consumption_qty,
                "primary_max": self.primary_max,

                "secondary_import": self.secondary_import,
                "secondary_consumption_qty": self.secondary_consumption_qty,
                "secondary_max": self.secondary_max,

                "production_frequency": self.production_frequency,
                "production_material": self.production_material,
                "production_qty": self.production_qty,
                "production_max": self.production_max,

                "cargo": self.cargo,

                "accessibility_radius": self.accessibility_radius,

                "sell_price": self.sell_price,
                "primary_buy_price": self.primary_buy_price,
                "secondary_buy_price": self.secondary_buy_price
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

            self.primary_import = data["primary_import"]
            self.primary_consumption_qty = data["primary_consumption_qty"]
            self.primary_max = data["primary_max"]

            self.secondary_import = data["secondary_import"]
            self.secondary_consumption_qty = data["secondary_consumption_qty"]
            self.secondary_max = data["secondary_max"]

            self.production_frequency = data["production_frequency"]
            self.production_material = data["production_material"]
            self.production_qty = data["production_qty"]
            self.production_max = data["production_max"]

            self.cargo = { int(k): v for k, v in data["cargo"].items() }

            self.accessibility_radius = data["accessibility_radius"]

            self.sell_price = data["sell_price"]
            self.primary_buy_price = data["primary_buy_price"]
            self.secondary_buy_price = data["primary_buy_price"]

        if security_level <= SecurityLevel.player_owned:
            pass

        if security_level <= SecurityLevel.other_player:
            pass


class BlackMarketStation(Station):
    def init(self,
            name,
            position=(0,0),

            primary_import=None,
            primary_consumption_qty=1,

            production_frequency=1,
            production_material=None,
            production_qty=1,

            cargo=None,
            accessibility_radius=5,
            object_type=ObjectType.station):

        Station.init(self,
                name,
                position=position,
                primary_import=primary_import,
                primary_consumption_qty=primary_consumption_qty,
                production_frequency=production_frequency,
                production_material=production_material,
                production_qty=production_qty,
                cargo=None,
                accessibility_radius=5,
                station_type=ObjectType.black_market_station)


class SecureStation(Station):
    def init(self,
            name,
            position=(0,0),

            primary_import=None,
            primary_consumption_qty=1,

            production_frequency=1,
            production_material=None,
            production_qty=1,

            cargo=None,
            accessibility_radius=5,
            object_type=ObjectType.station):

        Station.init(self,
                name,
                position=position,
                primary_import=primary_import,
                primary_consumption_qty=primary_consumption_qty,
                production_frequency=production_frequency,
                production_material=production_material,
                production_qty=production_qty,
                cargo=None,
                accessibility_radius=5,
                station_type=ObjectType.secure_station)


