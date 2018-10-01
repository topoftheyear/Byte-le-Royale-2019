from game.common.asteroid_field import *
from game.common.material_types import *
from game.common.enums import *

def load_asteroid_field(asteroid_field_type, data, security_level=SecurityLevel.player_owned):
    if asteroid_field_type == ObjectType.gold_field:
        new_asteroid_field = GoldField()
    elif asteroid_field_type == ObjectType.goethite_field:
        new_asteroid_field = GeothiteField()
    elif asteroid_field_type == ObjectType.cuprite_field:
        new_asteroid_field = CuperiteField()
    else:
        raise Exception("Invalid asteroid field type: {0}".format(asteroid_field_type))

    new_asteroid_field.from_dict(data, security_level=security_level)
    return new_asteroid_field

def create_asteroid_field(field_type, position):
    if field_type == ObjectType.gold_field:
        obj = GoldField()
    elif field_type == ObjectType.goethite_field:
        obj = GeothiteField()
    elif field_type == ObjectType.cuprite_field:
        obj = CuperiteField()
    else:
        raise Exception("Invalid asteroid field type: {0}".format(field_type))

    obj.init(position)
    return obj


class GoldField(AsteroidField):
    def init(self, position):
        AsteroidField.init(self,
                field_type=ObjectType.gold_field,
                name="Gold Field",
                position=position,
                material_type=MaterialType.gold,
                mining_rate=0.8)

class GeothiteField(AsteroidField):
    def init(self, position):
        AsteroidField.init(self,
                field_type=ObjectType.goethite_field,
                name="Geothite Field",
                position=position,
                material_type=MaterialType.goethite,
                mining_rate=1.0)

class CuperiteField(AsteroidField):
    def init(self, position):
        AsteroidField.init(self,
                field_type=ObjectType.cuprite_field,
                name="Cuperite Field",
                position=position,
                material_type=MaterialType.cuprite,
                mining_rate=1.2)
