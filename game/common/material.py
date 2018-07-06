from game.common.game_serializable import Serializable
from game.common.enums import *

class Material(Serializable):

    def __init__(self):
        self.initialized = False
        
    def init(self, name, value, material_type):
        self.name = name
        self.value = value
        self.material_type = material_type
        
        self.initialized = True
        
    def from_dict(self, d, safe=False):
        if not safe:
            pass
            # info hidden from user here
            
        self.name = d["name"]
        self.value = d["value"]
        self.material_type = d["material_type"]
        
    def to_dict(self, safe=False):
        data = {}
        
        if not safe:
            pass
            # info hidden from user here
            
        data["name"] = self.name
        data["value"] = self.value
        data["material_type"] = self.material_type
        
        return data