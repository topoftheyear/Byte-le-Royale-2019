import json


def save(universe):


    serialized_universe = []

    for obj in universe:
        #TODO refactor later to serialize all objects
        #serialized_universe.append()
        pass


    with open("game_data.json", "w") as f:
        json.dump({"universe": serialized_universe}, f, sort_keys=True, indent=4)


def load():
    with open("game_data.json", "r") as f:
        data = json.load(f)["universe"]

    for serialized_obj in data:
        # TODO refactor later to deserialize all objects according to their object_type property
        pass


def generate():
    universe = []

    # Generate stations
    # ey add those non-existent stations in main man right in here append it to that map

    # Generate mining fields
    # same deal append them to the map

    # Generate miscellaneous (spawn, black market, police station(?)...)
    # etc


    save(universe)


