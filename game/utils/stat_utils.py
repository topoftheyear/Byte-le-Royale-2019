import math

from game.universe_config import STATION_DEFINITIONS
from game.common.enums import *
from game.utils.helpers import get_material_name

class StatsTypes:
    primary_material_buy_by_station = 0
    secondary_material_buy_by_station = 1
    material_sell_by_station = 2
    material_buy_vs_sell = 3
    station_stats = 4
    material_production_vs_consumption = 5

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


    if "N/A" in compiled:

        del compiled["N/A"]

    # Fix for drones since they arent a primary but 2 secondaries
    drones_avg = []
    for i in range(0, math.floor(len(compiled["Drones"]["secondary_buy_price"])), 2):
        drones_avg.append( sum(compiled["Drones"]["secondary_buy_price"][i:i+1])/2 )
    compiled["Drones"]["secondary_buy_price"] = drones_avg

    # Fix for circuitry since they arent a secondary but 2 primaries
    circ_avg = []
    for i in range(0, math.floor(len(compiled["Circuitry"]["primary_buy_price"])), 2):
        circ_avg.append( sum(compiled["Circuitry"]["primary_buy_price"][i:i+1])/2 )
    compiled["Circuitry"]["primary_buy_price"] = circ_avg

    return compiled


def compile_consumption_vs_production(stats):
    compiled = {}

    for t in stats:
        compiled_tick = {}
        for station in t["market"]:
            prod_material = station["production_material"]
            pri_material = station["primary_import"]
            sec_material = station["secondary_import"]

            prod_name = get_material_name(prod_material)
            pri_name = get_material_name(pri_material)
            sec_name = get_material_name(sec_material)

            if prod_name not in compiled_tick:
                compiled_tick[prod_name] = {}
            if "Produced" not in compiled_tick[prod_name]:
                compiled_tick[prod_name]["Produced"] = 0
            compiled_tick[prod_name]["Produced"] += station["production_produced"]

            if pri_name not in compiled_tick:
                compiled_tick[pri_name] = {}
            pri_consumed = "Primary Consumed"
            if pri_consumed not in compiled_tick[pri_name]:
                compiled_tick[pri_name][pri_consumed] = 0
            compiled_tick[pri_name][pri_consumed] += station["primary_consumed"]

            if sec_material != -1:
                sec_consumed = "Secondary Consumed"
                if sec_name not in compiled_tick:
                    compiled_tick[sec_name] = {}
                if sec_consumed not in compiled_tick[sec_name]:
                    compiled_tick[sec_name][sec_consumed] = 0
                compiled_tick[sec_name][sec_consumed] += station["secondary_consumed"]

        for mat, counts in compiled_tick.items():
            if mat not in compiled:
                compiled[mat] = {}

            for type, count in counts.items():
                if type not in compiled[mat]:
                    compiled[mat][type] = []
                compiled[mat][type].append(count)

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
    elif format_type is StatsTypes.material_production_vs_consumption:
        return compile_consumption_vs_production(stats)
    return None


