from game.common.game_object import GameObject
from game.common.enums import *

class Material(GameObject):

    def __str__(self):
        x = '<{}: {}>'.format(self.__class__.__name__, self.id)
        return x

    def __repr__(self):
        x = '<{}: {}>'.format(self.__class__.__name__, self.id)
        return x

    def __init__(self):
        pass

    def init(self, name, value, material_type):
        GameObject.init(self, ObjectType.material)
        self.name = name
        self.value = value
        self.material_type = material_type

        self.initialized = True

    def from_dict(self, d, safe=False):
        GameObject.from_dict(self, d)

        if not safe:
            pass
            # info hidden from user here

        self.name = d["name"]
        self.value = d["value"]
        self.material_type = d["material_type"]

    def to_dict(self, safe=False):
        data = GameObject.to_dict(self)

        if not safe:
            pass
            # info hidden from user here

        data["name"] = self.name
        data["value"] = self.value
        data["material_type"] = self.material_type

        return data
