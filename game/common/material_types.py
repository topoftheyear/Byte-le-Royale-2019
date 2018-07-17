from game.common.material import *
from game.common.enums import *


class Ironium(Material):
    def init(self, value=100):
        Material.init(self,
                value,                      #value
                MaterialType.ironium)       #material_type
                
class Food(Material):
    def init(self, value=100):
        Material.init(self,
                value,                      #value
                MaterialType.food)          #material_type
                
class Electrum(Material):
    def init(self, value=100):
        Material.init(self,
                value,                      #value
                MaterialType.electrum)      #material_type
               
class Circuitry(Material):
    def init(self, value=100):
        Material.init(self,
                value,                      #value
                MaterialType.circuitry)     #material_type
                
class Weaponry(Material):
    def init(self, value=100):
        Material.init(self,
                value,                      #value
                MaterialType.weaponry)      #material_type


def load_material(material_type, data):
    if material_type == MaterialType.ironium:
        new_material = Ironium()
    elif material_type == MaterialType.food:
        new_material = Food()
    elif material_type == MaterialType.electrum:
        new_material = Electrum()
    elif material_type == MaterialType.circuitry:
        new_material = Circuitry()
    elif material_type == MaterialType.weaponry:
        new_material = Weaponry()

    else:
        raise Exception("Invalid material type: {0}".format(material_type))

        new_material.from_dict(data)
        return new_material
