from game.common.material import *
from game.common.enums import *

def load_ore(material_type, data):
    if material_type == MaterialType.ironium:
        new_ore = Ironium()
    elif material_type == MaterialType.food:
        new_ore = Food()
    elif material_type == MaterialType.electrum:
        new_ore = Electrum()
    elif material_type == MaterialType.circuitry:
        new_ore = Circuitry()
    elif material_type == MaterialType.weaponry:
        new_ore = Weaponry()
        
    else:
        raise Exception("Invalid ore type: "{0}.format(material_type))
    
    new_ore.from_dict(data)
    return new_ore

class Ironium(Ore):
    def init(self):
        Ore.init(self,
                100,                        #value
                MaterialType.ironium)       #material_type
                
class Food(Ore):
    def init(self):
        Ore.init(self,
                100,                        #value
                MaterialType.food)          #material_type
                
class Electrum(Ore):
    def init(self):
        Ore.init(self,
                100,                        #value
                MaterialType.electrum)      #material_type
               
class Circuitry(Ore):
    def init(self):
        Ore.init(self,
                100,                        #value
                MaterialType.circuitry)     #material_type
                
class Weaponry(Ore):
    def init(self):
        Ore.init(self,
                100,                        #value
                MaterialType.weaponry)      #material_type