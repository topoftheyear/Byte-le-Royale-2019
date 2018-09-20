import json
import math

from game.config import *
from game.common.ship import Ship
from game.common.station import *
from game.common.asteroid_field_types import create_asteroid_field, load_asteroid_field
from game.common.enums import *
from game.utils.projection import *

from game.universe_config import *



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
            print(serialized_obj["name"])
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
    for i, data in enumerate(STATION_DEFINITIONS):
        if data["type"] == ObjectType.station:
            station = Station()
            del data["type"]
            station.init(
                name="Station {0}".format(i),
                **data
            )

        elif data["type"] == ObjectType.black_market_station:
            del data["type"]
            station = BlackMarketStation()
            station.init(
                    name="Station {0}".format(i),
                    **data
                )

        elif data["type"] == ObjectType.secure_station:
            del data["type"]
            station = SecureStation()
            station.init(
                    name="Station {0}".format(i),
                    **data
                )

        universe.append(station)


    # Generate mining fields
    for i, data in enumerate(ASTEROID_FIELD_DEFINITIONS):
        obj = create_asteroid_field(data["type"], data["position"])
        universe.append(obj)


    # Generate miscellaneous (spawn, black market, police station(?)...)
    # etc

    for i in range(NPCS_TO_GENERATE):
        new_npc_ship = Ship()
        new_npc_ship.init("~AI", is_npc=True, position=percent_world(0.5, 0.5))

        universe.append(new_npc_ship)


    save(universe)


