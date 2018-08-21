import json
import math

from game.config import *
from game.common.ship import Ship
from game.common.station import *
from game.common.asteroid_field_types import create_asteroid_field, load_asteroid_field
from game.common.enums import *
from game.utils.projection import *



def save(universe):


    serialized_universe = []

    for obj in universe:
        d = obj.to_dict(security_level=SecurityLevel.engine)
        serialized_universe.append(d)


    with open("game_data.json", "w") as f:
        json.dump({"universe": serialized_universe}, f, sort_keys=True, indent=4)


def load():
    with open("game_data.json", "r") as f:
        data = json.load(f)["universe"]

    deserialized_univerze = []
    for serialized_obj in data:
        obj_type = serialized_obj["object_type"]

        obj = None

        if obj_type == ObjectType.ship:
            obj = Ship()
            obj.from_dict(serialized_obj, security_level=SecurityLevel.engine)

        elif obj_type == ObjectType.station:
            obj = Station()
            obj.from_dict(serialized_obj, security_level=SecurityLevel.engine)

        elif obj_type == ObjectType.black_market_station:
            obj = BlackMarketStation()
            obj.from_dict(serialized_obj, security_level=SecurityLevel.engine)

        elif obj_type == ObjectType.secure_station:
            obj = SecureStation()
            obj.from_dict(serialized_obj, security_level=SecurityLevel.engine)

        elif obj_type in [ObjectType.goethite_field, ObjectType.gold_field, ObjectType.cuprite_field]:
            obj = load_asteroid_field(obj_type, serialized_obj, security_level=SecurityLevel.engine)


        if obj is not None:
            deserialized_univerze.append(obj)

    return deserialized_univerze


def generate():
    universe = []

    # Generate stations
    station_data = [
        {
            #s6 Copper
            "type": ObjectType.station,
            "coords": percent_world(0.05, 0.9),

            "primary_import": MaterialType.cuprite,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.drones,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.copper,
            "production_rate": 1
        },
        {
            #s4 Pylons
            "type": ObjectType.station,
            "coords": percent_world(0.025, 0.6),

            "primary_import": MaterialType.circuitry,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.null,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.pylons,
            "production_rate": 1
        },
        {
            #s9 Weaponry
            "type": ObjectType.station,
            "coords": percent_world(0.15, 0.58),

            "primary_import": MaterialType.computers,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.null,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.weaponry,
            "production_rate": 1
        },
        {
            #s5 Machinery
            "type": ObjectType.station,
            "coords": percent_world(0.085, 0.40),

            "primary_import": MaterialType.steel,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.pylons,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.machinery,
            "production_rate": 1
        },
        {
            #s0 Wire
            "type": ObjectType.station,
            "coords": percent_world(0.4, 0.10),

            "primary_import": MaterialType.copper,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.null,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.wire,
            "production_rate": 1
        },
        {
            #s8 Iron
            "type": ObjectType.station,
            "coords": percent_world(0.6, 0.80),

            "primary_import": MaterialType.goethite,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.machinery,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.iron,
            "production_rate": 1
        },
        {
            #s1 Computers
            "type": ObjectType.station,
            "coords": percent_world(0.63, 0.08),

            "primary_import": MaterialType.circuitry,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.null,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.computers,
            "production_rate": 1
        },
        {
            #s2 Circuitry
            "type": ObjectType.station,
            "coords": percent_world(0.90, 0.38),

            "primary_import": MaterialType.gold,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.wire,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.circuitry,
            "production_rate": 1
        },
        {
            #s3 Drones
            "type": ObjectType.station,
            "coords": percent_world(0.96, 0.95),

            "primary_import": MaterialType.weaponry,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.null,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.drones,
            "production_rate": 1
        },
        {
            #s7 Steel
            "type": ObjectType.station,
            "coords": percent_world(0.92, 0.03),

            "primary_import": MaterialType.iron,
            "primary_consumption_rate": 1,

            "secondary_import": MaterialType.drones,
            "secondary_consumption_rate": 1,

            "production_material": MaterialType.steel,
            "production_rate": 1
        },
        {
            # black market 2
            "type": ObjectType.black_market_station,
            "coords": percent_world(0.1, 0.8)
        },
        {
            # black market 1
            "type": ObjectType.black_market_station,
            "coords": percent_world(0.88, 0.25)
        },
        {
            "type": ObjectType.secure_station,
            "coords": percent_world(0.5, 0.5)
        }
    ]

    for i, data in enumerate(station_data):
        if data["type"] == ObjectType.station:
            station = Station()
            station.init(
                name="Station {0}".format(i),
                position=data["coords"],
                primary_import = data["primary_import"],
                primary_consumption_rate= data["primary_consumption_rate"],

                secondary_import = data["secondary_import"],
                secondary_consumption_rate= data["secondary_consumption_rate"],

                production_material = data["production_material"],
                production_rate = data["production_rate"]
            )

        elif data["type"] == ObjectType.black_market_station:
            station = BlackMarketStation()
            station.init(
                    name="Station {0}".format(i),
                    position=data["coords"])

        elif data["type"] == ObjectType.secure_station:
            station = SecureStation()
            station.init(
                    name="Station {0}".format(i),
                    position=data["coords"])

        universe.append(station)


    # Generate mining fields
    asteroid_field_data = [
        {
            "type": ObjectType.goethite_field,
            "coords": percent_world(0.05, 0.05)
        },
        {
            "type": ObjectType.gold_field,
            "coords": percent_world(0.85, 0.85)
        },
        {
            "type": ObjectType.cuprite_field,
            "coords": percent_world(0.5, 0.85)
        }
    ]

    for i, data in enumerate(asteroid_field_data):
        obj = create_asteroid_field(data["type"], data["coords"])
        universe.append(obj)


    # Generate miscellaneous (spawn, black market, police station(?)...)
    # etc

    for i in range(NPCS_TO_GENERATE):
        new_npc_ship = Ship()
        new_npc_ship.init("~AI", is_npc=True, position=percent_world(0.5, 0.5))

        universe.append(new_npc_ship)


    save(universe)


