from game.common.asteroid_field import *
from game.common.material_types import *
from game.common.enums import *

def load_asteroid_field(asteroid_field_type, data, security_level=SecurityLevel.player_owned):
    if asteroid_field_type == ObjectType.ironium_field:
        new_asteroid_field = IroniumField()
    else:
        raise Exception("Invalid asteroid field type: {0}".format(asteroid_field_type))

    new_asteroid_field.from_dict(data, security_level=security_level)
    return new_asteroid_field

def create_asteroid_field(field_type, position):
    if field_type == ObjectType.ironium_field:
        obj = IroniumField()
    else:
        raise Exception("Invalid asteroid field type: {0}".format(field_type))

    obj.init(position)
    return obj


class IroniumField(AsteroidField):
    def init(self, position):
        AsteroidField.init(self,
                field_type=ObjectType.ironium_field,
                name="Ironium Field",
                position=position,
                material_type=MaterialType.ironium)

