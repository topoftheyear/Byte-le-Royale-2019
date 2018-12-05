import types
import math

from game.common.enums import *
from game.utils.material_price_finder import *

def get_ships(universe, callback=None):
    if callback != None:
        return [ obj
                for obj in universe
                if obj.object_type in [ ObjectType.ship, ObjectType.police, ObjectType.enforcer ]
                and obj.is_alive()
                and callback(obj)]

    return [ obj
            for obj in universe
            if obj.object_type == ObjectType.ship
            and obj.is_alive()]

def ships_in_attack_range(universe, ship):
    def is_ship_visible_wrapper(ship):
        def is_ship_visible(target):
            result = (ship.position[0] - target.position[0])**2 + (ship.position[1] - target.position[1])**2
            in_range = result < ship.weapon_range**2
            return in_range  and ship.id != target.id
        return is_ship_visible

    return get_ships(universe, is_ship_visible_wrapper(ship))

def get_stations(universe):
    return [ obj for obj in universe if obj.object_type == ObjectType.station ]

def get_asteroid_fields(universe):
    return [ obj
            for obj in universe
            if obj.object_type in [
                ObjectType.cuprite_field,
                ObjectType.goethite_field,
                ObjectType.gold_field] ]

def distance_to(source, target, accessor, target_accessor=None):
    """
    Params:
    - source: the source object that you wish to start from
    - target: the target you wish to determine the distance to
    - accessor: an accessor method used to get the position of the source. if target_accessor is None, this will be applied to the target.
    - target_accessor: an accessor method used to get the position of the target. Default: None.
    """

    source_pos = accessor(source)
    if target_accessor:
        target_pos = target_accessor(target)
    else:
        target_pos = accessor(target)

    return (
        source_pos[0] - target_pos[0],
        source_pos[1] - target_pos[1]
    )


def in_radius(source, target, radius, accessor, target_accessor=None, verify_instance=True):
    """
    Params:
    - source: the source object that you want to search a radius around
    - target: the target object you wish to see if it lies in a radius around the source
    - radius: either an integer, float or accessor function that takes the source and the target and returns an integer or float.
    - accessor: an accessor method used to get the position of the source. If target_accessor is None, this will also be applied to the target.
    - target_accessor: an accessor method used to get the position of the target. Default: None.
    - verify_instance: Verify that source and target do not have the same id.
    """
    source_pos = accessor(source)
    if target_accessor:
        target_pos = target_accessor(target)
    else:
        target_pos = accessor(target)

    result = (source_pos[0] - target_pos[0])**2 + (source_pos[1] - target_pos[1])**2

    if isinstance(radius, types.FunctionType):
        radius = radius(source, target)

    in_range = result < radius**2

    if verify_instance:
        return in_range
    else:
        return in_range

def convert_material_to_scrap(material, amount):
    """
    Params:
    :param material: MaterialType enum of material to convert
    :param amount: number amount of the material given
    :return: integer amount of how many scrap should be created
    """

    value = get_material_price(material)
    return math.ceil(amount * value * 0.25)

def get_material_price(material):
    """
    Get the current highest available market price for the given material
    :param material: MaterialType material to get the price of
    :return: number value of the material
    """
    value = ascertain_material_price(material)
    return value

def in_secure_zone(target, target_accessor):
    """
    Params:
    - The object you wish to check if it's position is within the save zone

    """

    center_of_world = (
        WORLD_BOUNDS[0]/2.0,
        WORLD_BOUNDS[1]/2.0
    )

    return in_radius(source, center_of_world, SECURE_ZONE_RADIUS, accessor, lambda e: e)
