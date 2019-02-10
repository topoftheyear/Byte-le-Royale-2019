from game.common.enums import ObjectType
from game.utils.helpers import separate_universe

_filter = filter

class UniverseManager:

    def __init__(self, flat_universe):

        self.universe = separate_universe(flat_universe)
        self.groups = {}

        self.add_group("police", [ObjectType.police, ObjectType.enforcer])
        self.add_group("ships", [ObjectType.police, ObjectType.enforcer, ObjectType.ship])
        self.add_group("all_stations", [
            ObjectType.station,
            ObjectType.secure_station,
            ObjectType.black_market_station])
        self.add_group("asteroid_fields", [
            ObjectType.cuprite_field,
            ObjectType.goethite_field,
            ObjectType.gold_field
        ])

    def add_group(self, group_name, object_types):
        self.groups[group_name.lower()] = object_types

    def remove_group(self, group_name):
        del self.groups[group_name.lower()]

    def get_group(self, group_name):
        return [obj for t in self.groups.get(group_name, []) if t in self.universe for obj in self.universe[t]]

    def get_type(self, object_type):
        if object_type not in self.universe:
            return []
        return self.universe[object_type]

    def get(self, identifier):
        if isinstance(identifier, int):
            return self.get_type(identifier)
        elif isinstance(identifier, str):
            return self.get_group(identifier)
        else:
            raise Exception(f"Bad identifier type: {type(identifier)}")

    def get_filtered(self, identifier, filter):
        return list(_filter(filter, self.get(identifier)))

    def get_filtered_one(self, identifier, filter):
        for obj in self.get(identifier):
            if filter(obj):
                return obj
        return None

    def add_object(self, obj):
        if obj.object_type not in self.universe:
            self.universe[obj.object_type] = []
        self.universe[obj.object_type].append(obj)

    def remove_object(self, obj):
        if obj.object_type not in self.universe:
            return
        self.universe[obj.object_type].remove(obj)

    def flatten(self):
        return [obj for types in self.universe.values() for obj in types]

    def load(self, flat_universe):
        self.universe = separate_universe(flat_universe)


