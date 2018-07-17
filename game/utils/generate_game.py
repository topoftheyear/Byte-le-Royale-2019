import json
import math

from game.config import *
from game.common.ship import Ship
from game.common.station import *
from game.common.enums import *


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

        if obj is not None:
            deserialized_univerze.append(obj)

    return deserialized_univerze


def generate():
    universe = []

    # Generate stations
    # ey add those non-existent stations in main man right in here append it to that map
    station_data = [
        {
            "type": ObjectType.station,
            "coords": [100, 100]
        },
        {
            "type": ObjectType.black_market_station,
            "coords": [200, 100]
        },
        {
            "type": ObjectType.secure_station,
            "coords": [ math.floor(WORLD_BOUNDS[0]/2.0), math.floor(WORLD_BOUNDS[1]/2.0)]
        }
    ]

    for i, data in enumerate(station_data):
        if data["type"] == ObjectType.station:
            station = Station()
        elif data["type"] == ObjectType.black_market_station:
            station = BlackMarketStation()
        elif data["type"] == ObjectType.secure_station:
            station = SecureStation()

        station.init(
                name="Station {0}".format(i),
                position=data["coords"])
        universe.append(station)


    # Generate mining fields
    # same deal append them to the map

    # Generate miscellaneous (spawn, black market, police station(?)...)
    # etc

    for i in range(NPCS_TO_GENERATE):
        new_npc_ship = Ship()
        new_npc_ship.init("~AI", is_npc=True)

        universe.append(new_npc_ship)


    save(universe)


