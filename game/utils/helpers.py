from game.common.enums import *

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
    return [ obj for obj in universe if obj.object_type == ObjectType.stations ]

def get_asteroid_fields(universe):
    return [ obj
            for obj in universe
            if obj.object_type in [
                ObjectType.cuprite_field,
                ObjectType.goethite_field,
                ObjectType.gold_field] ]
