import math
from itertools import groupby
from game.utils.filters import in_radius as pred_in_radius
from game.utils.filters import AND, EQ, NOT
from game.common.stats import GameStats

import types
import statistics

from game.config import *
from game.common.enums import *



def ships_in_attack_range(universe, ship):
    def is_visible_wrapper(t):
        return in_radius(ship, t, ship.weapon_range, lambda e: e.position, verify_instance=True)

    return list(filter(is_visible_wrapper, universe.get("ships")))


def distance_to(source, target, accessor, target_accessor=None):
    """
    Params:
    - source: the source object that you wish to start from
    - target: the target you wish to determine the distance to
    - accessor: an accessor method used to get the position of the source. if target_accessor == None, this will be applied to the target.
    - target_accessor: an accessor method used to get the position of the target. Default: None.
    """

    source_pos = accessor(source)
    if target_accessor:
        target_pos = target_accessor(target)
    else:
        target_pos = accessor(target)

    return (
                   (source_pos[0] - target_pos[0]) ** 2 +
                   (source_pos[1] - target_pos[1]) ** 2
           ) ** (1 / 2)


def in_radius(source, target, radius, accessor, target_accessor=None, verify_instance=True):
    """
    Params:
    - source: the source object that you want to search a radius around
    - target: the target object you wish to see if it lies in a radius around the source
    - radius: either an integer, float or accessor function that takes the source and the target and returns an integer or float.
    - accessor: an accessor method used to get the position of the source. If target_accessor == None, this will also be applied to the target.
    - target_accessor: an accessor method used to get the position of the target. Default: None.
    - verify_instance: Verify that source and target do not have the same id.
    """
    source_pos = accessor(source)
    if target_accessor:
        target_pos = target_accessor(target)
    else:
        target_pos = accessor(target)

    result = (source_pos[0] - target_pos[0]) ** 2 + (source_pos[1] - target_pos[1]) ** 2

    if isinstance(radius, types.FunctionType):
        radius = radius(source, target)

    in_range = result < radius ** 2

    if verify_instance:
        return in_range and source.id != target.id
    else:
        return in_range


def convert_material_to_scrap(material_qty, material_value):
    """
    Params:
    :param universe: the universe
    :param material: MaterialType enum of material to convert
    :param amount: number amount of the material given
    :return: integer amount of how many scrap should be created
    """
    return math.ceil(material_qty * material_value * 0.25)


def in_secure_zone(source, accessor):
    """
    Params:
    - The object you wish to check if it's position == within the save zone

    """

    center_of_world = (
        WORLD_BOUNDS[0] / 2.0,
        WORLD_BOUNDS[1] / 2.0
    )

    return in_radius(source, center_of_world, SECURE_ZONE_RADIUS, accessor, target_accessor=lambda e: e)


def get_material_name(material_type):
    material_type = int(material_type)
    if material_type == MaterialType.circuitry:
        return "Circuitry"
    elif material_type == MaterialType.computers:
        return "Computers"
    elif material_type == MaterialType.copper:
        return "Copper"
    elif material_type == MaterialType.cuprite:
        return "Cuprite"
    elif material_type == MaterialType.drones:
        return "Drones"
    elif material_type == MaterialType.goethite:
        return "Goethite"
    elif material_type == MaterialType.gold:
        return "Gold"
    elif material_type == MaterialType.iron:
        return "Iron"
    elif material_type == MaterialType.machinery:
        return "Machinery"
    elif material_type == MaterialType.pylons:
        return "Pylons"
    elif material_type == MaterialType.steel:
        return "Steel"
    elif material_type == MaterialType.weaponry:
        return "Weaponry"
    elif material_type == MaterialType.wire:
        return "Wire"
    elif material_type == MaterialType.salvage:
        return "Salvage"
    return "N/A"


def separate_universe(flat_universe):
    universe = {}

    for key, group in groupby(flat_universe, lambda e: e.object_type):
        if key not in universe:
            universe[key] = []
        universe[key].extend(list(group))

    return universe


#  Finds median price of all materials in the universe
def get_median_material_price(material_prices):
    return statistics.median(material_prices)


#  Applies adjustments based on median material prices to find repair cost
def get_repair_price(median_price):
    return math.floor(GameStats.repair_adjustment * GameStats.repair_materials_cost * median_price)


#  Determine module price
def get_module_price(level, universe):
    median_price = get_median_material_price(get_material_sell_prices(universe))
    if level == ModuleLevel.one:
        return math.floor(GameStats.module_level_1_adjustment * median_price * GameStats.module_level_1_materials_cost)
    elif level == ModuleLevel.two:
        return math.floor(GameStats.module_level_2_adjustment * median_price * GameStats.module_level_2_materials_cost)
    elif level == ModuleLevel.three:
        return math.floor(GameStats.module_level_3_adjustment * median_price * GameStats.module_level_3_materials_cost)
    elif level == ModuleLevel.illegal:
        return math.floor(GameStats.module_level_4_adjustment * median_price * GameStats.module_level_4_materials_cost)
    else:
        return



#  Determine module unlock price given ship_slot
def get_module_unlock_price(median_price, ship_slot):
    if ship_slot == ShipSlot.zero:
        return math.floor(GameStats.unlock_slot_0_adjustment * median_price * GameStats.unlock_slot_0_materials_cost)
    elif ship_slot == ShipSlot.one:
        return math.floor(GameStats.unlock_slot_1_adjustment * median_price * GameStats.unlock_slot_1_materials_cost)
    elif ship_slot == ShipSlot.two:
        return math.floor(GameStats.unlock_slot_2_adjustment * median_price * GameStats.unlock_slot_2_materials_cost)
    elif ship_slot == ShipSlot.three:
        return math.floor(GameStats.unlock_slot_3_adjustment * median_price * GameStats.unlock_slot_3_materials_cost)
    else:
        return

def get_material_buy_prices(universe):
    all_prices = {}
    for station in universe.get(ObjectType.station):
        if station.production_material is not None:
            all_prices[station.production_material] = station.sell_price
    return all_prices

def get_material_sell_prices(universe):
    price_list = {}
    all_prices = {}
    for station in universe.get(ObjectType.station):
        if station.primary_import is not None:
            if station.primary_import not in all_prices:
                all_prices[station.primary_import] = []
            all_prices[station.primary_import].append(station.primary_buy_price)

        if station.secondary_import is not None:
            if station.secondary_import not in all_prices:
                all_prices[station.secondary_import] = []
            all_prices[station.secondary_import].append(station.secondary_buy_price)

    for material, prices in all_prices.items():
        if material not in price_list:
            price_list[material] = 0
        price_list[material] = max(prices)

    price_list[MaterialType.salvage] = ILLEGAL_SCRAP_VALUE

    return price_list

def get_best_material_prices(universe):
    """Cache result and only call once per turn"""
    best_import_prices = {}
    best_export_prices = {}
    for station in universe.get(ObjectType.station):
        # get best import prices
        if station.primary_import is not None:
            if station.primary_import not in best_import_prices:
                best_import_prices[station.primary_import] = {"import_price": -1, "station": None}

            if station.primary_buy_price > best_import_prices[station.primary_import]["import_price"]:
                best_import_prices[station.primary_import]["import_price"] = station.primary_buy_price
                best_import_prices[station.primary_import]["station"] = station

        if station.secondary_import is not None:
            if station.secondary_import not in best_import_prices:
                best_import_prices[station.secondary_import] = {"import_price": -1, "station": None}

            if station.secondary_buy_price > best_import_prices[station.secondary_import]["import_price"]:
                best_import_prices[station.secondary_import]["import_price"] = station.secondary_buy_price
                best_import_prices[station.secondary_import]["station"] = station

        # get best export prices
        if station.production_material not in best_export_prices:
            best_export_prices[station.production_material] = { "export_price": 9999999, "station": None }

        if station.sell_price < best_export_prices[station.production_material]["export_price"]:
            best_export_prices[station.production_material] = { "export_price": station.sell_price, "station": station}

    # Add salvage to import prices
    best_import_prices[MaterialType.salvage] = {"import_price": ILLEGAL_SCRAP_VALUE,
                                                "station":      universe.get(ObjectType.black_market_station)[0]}

    return {
        "best_import_prices": best_import_prices,
        "best_export_prices": best_export_prices
    }


