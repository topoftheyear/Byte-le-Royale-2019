from game.common.material import *
from game.common.enums import *


class Iron(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.iron)       #material_type

class Steel(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.steel)       #material_type

class Copper(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.copper)       #material_type

class Circuitry(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.circuitry)       #material_type

class Pylons(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.pylons)       #material_type

class Weaponry(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.weaponry)       #material_type

class Machinery(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.machinery)       #material_type

class Computers(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.computers)       #material_type

class Drones(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.drones)       #material_type

class Gold(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.gold)       #material_type

class Cuperite(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.cuprite)       #material_type

class Geothite(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.goethite)       #material_type

class Wire(Material):
    def init(self, value=100):
        Material.init(self,
            value,                      #value
            MaterialType.wire)       #material_type



def load_material(material_type, data):
    if material_type == MaterialType.iron:
        new_material = Iron()
    elif material_type == MaterialType.steel:
        new_material = Steel()
    elif material_type == MaterialType.copper:
        new_material = Copper()
    elif material_type == MaterialType.circuitry:
        new_material = Circuitry()
    elif material_type == MaterialType.pylons:
        new_material = Pylons()
    elif material_type == MaterialType.weaponry:
        new_material = Weaponry()
    elif material_type == MaterialType.machinery:
        new_material = Machinery()
    elif material_type == MaterialType.computers:
        new_material = Computers()
    elif material_type == MaterialType.drones:
        new_material = Drones()
    elif material_type == MaterialType.gold:
        new_material = Gold()
    elif material_type == MaterialType.cuprite:
        new_material = Cuperite()
    elif material_type == MaterialType.goethite:
        new_material = Geothite()
    elif material_type == MaterialType.wire:
        new_material = Wire()

    else:
        raise Exception("Invalid material type: {0}".format(material_type))

        new_material.from_dict(data)
        return new_material
