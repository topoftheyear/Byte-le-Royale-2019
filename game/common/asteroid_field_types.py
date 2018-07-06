from game.common.asteroid_field import *
from game.common.material_types import *
from game.common.enums import *

def load_asteroid_field(asteroid_field_type, data):
    if asteroid_field_type == AsteroidFieldType.ironium_field:
        new_asteroid_field = Ironium_Field()
    
    else:
        raise Exception("Invalid asteroid field type: "{0}.format(asteroid_field_type))
        
    new_asteroid_field.from_dict(data)
    return new_asteroid_field
    
class Ironium_Field(Asteroid_Field):
    def init(self, material_type=MaterialType.ironium):
        Asteroid_Field.init(self,
                material_type,          #material_type
                1)                      #mining rate