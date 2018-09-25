import math

from game.universe_config import STATION_DEFINITIONS
from game.common.enums import *

def get_material_name(material_type):
    if material_type is MaterialType.circuitry:
        return "Circuitry"
    elif material_type is MaterialType.computers:
        return "Computers"
    elif material_type is MaterialType.copper:
        return "Copper"
    elif material_type is MaterialType.cuprite:
        return "Cuprite"
    elif material_type is MaterialType.drones:
        return "Drones"
    elif material_type is MaterialType.goethite:
        return "Goethite"
    elif material_type is MaterialType.gold:
        return "Gold"
    elif material_type is MaterialType.iron:
        return "Iron"
    elif material_type is MaterialType.machinery:
        return "Machinery"
    elif material_type is MaterialType.pylons:
        return "Pylons"
    elif material_type is MaterialType.steel:
        return "Steel"
    elif material_type is MaterialType.weaponry:
        return "Weaponry"
    elif material_type is MaterialType.wire:
        return "Wire"
    return "N/A"


class StatsTypes:
    primary_material_buy_by_station = 0
    secondary_material_buy_by_station = 1
    material_sell_by_station = 2
    material_buy_vs_sell = 3
    station_stats = 4

def generic_compile_stats(domain, stats, ignore_fields=[]):
    stat_names = list(stats[0][domain][1].keys())


    for r in ignore_fields:
        if r in stat_names:
            stat_names.remove(r)

    compiled = {  }
    for t in stats:
        for station in t[domain]:
            if station["station_name"] not in compiled:
                compiled[station["station_name"]] = {}

            for stat_name in stat_names:
                if stat_name not in compiled[station["station_name"]]:
                    compiled[station["station_name"]][stat_name] = []

                compiled[station["station_name"]][stat_name].append(station[stat_name])

    return compiled

def compile_station_stats( stats):
    return generic_compile_stats("market", stats, ["station_id", "station_name"])


def compile_primary_material_buy_by_station(stats):

    compiled = { }

    for t in stats:
        for station in t["market"]:
            if station["station_name"] not in compiled:
                compiled[station["station_name"]] = []

            compiled[station["station_name"]].append(station["primary_buy_price"])

    return compiled



def compile_secondary_material_buy_by_station(stats):
    compiled = { }

    for t in stats:
        for station in t["market"]:
            if station["station_name"] not in compiled:
                compiled[station["station_name"]] = []

            compiled[station["station_name"]].append( station["secondary_buy_price"])

    return compiled

def compile_material_sell_by_station(stats):
    compiled = { }

    for t in stats:
        for station in t["market"]:
            if station["station_name"] not in compiled:
                compiled[station["station_name"]] = []

            compiled[station["station_name"]].append(station["sell_price"])

    return compiled

def compile_material_buy_vs_sell(stats):

    compiled = { }

    for t in stats:
        for station in t["market"]:
            name = get_material_name(station["production_material"])
            if not name in compiled:
                compiled[name] = {
                    "primary_buy_price": [],
                    "secondary_buy_price": [],
                    "sell_price": [],
                }

            compiled[name]["sell_price"].append(
                station["sell_price"]
            )

            name = get_material_name(station["primary_import"])
            if not name in compiled:
                compiled[name] = {
                    "primary_buy_price": [],
                    "secondary_buy_price": [],
                    "sell_price": [],
                }

            compiled[name]["primary_buy_price"].append(
                station["primary_buy_price"]
            )

            name = get_material_name(station["secondary_import"])
            if not name in compiled:
                compiled[name] = {
                    "primary_buy_price": [],
                    "secondary_buy_price": [],
                    "sell_price": [],
                }

            compiled[name]["secondary_buy_price"].append(
                station["secondary_buy_price"]
            )


    del compiled["N/A"]

    # Fix for drones since they arent a primary but 2 secondaries
    drones_avg = []
    for i in range(0, math.floor(len(compiled["Drones"]["secondary_buy_price"])), 2):
        drones_avg.append( sum(compiled["Drones"]["secondary_buy_price"][i:i+1])/2 )
    compiled["Drones"]["secondary_buy_price"] = drones_avg


    return compiled



def format_stats(stats, format_type):
    if format_type is StatsTypes.primary_material_buy_by_station:
        return compile_primary_material_buy_by_station(stats)
    elif format_type is StatsTypes.secondary_material_buy_by_station:
        return compile_secondary_material_buy_by_station(stats)
    elif format_type is StatsTypes.material_sell_by_station:
        return compile_material_sell_by_station(stats)
    elif format_type is StatsTypes.material_buy_vs_sell:
        return compile_material_buy_vs_sell(stats)
    elif format_type is StatsTypes.station_stats:
        return compile_station_stats(stats)
    return None


