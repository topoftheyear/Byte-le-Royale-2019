import math
import random
import sys

from game.common.enums import *
from game.common.station import Station

class StationController:

    def __init__(self, stations):
        """Initialize StationController properties (if any)"""

        self.init_ticks = 10

        self.station_data = {}
        for station in stations:
            self.station_data[station.id] = {
                "production_counter": 0
            }

        self.stats = []
        self.initialized = False

        self.debug = False

    def init(self, stations):
        """Initialize Stations"""

        for i in range(self.init_ticks):
            self.tick(stations)

        self.initialized = True

    def tick(self, stations):
        for station in stations:

            if self.debug and station.production_material != MaterialType.copper:
                continue

            data = self.station_data[station.id]
            data["primary_consumed"] = 0
            data["secondary_consumed"] = 0
            data["production_produced"] = 0

            self.print(f"Update Station {station.name} ({station.id}), produces: {station.production_material}")
            self.print(f"station.cargo: {station.cargo}")
            self.print(f"production counter: {data['production_counter']}")


            sufficient_primary_in_cargo = (
                station.primary_import in station.cargo and
                station.cargo[station.primary_import] > station.primary_consumption_qty
            )
            self.print(f"Sufficient primary in cargo: {sufficient_primary_in_cargo}")

            has_secondary = station.secondary_import != None
            self.print(f"Has secondary: {has_secondary}")
            sufficient_secondary_in_cargo = (
                station.secondary_import in station.cargo and
                station.cargo[station.secondary_import] > station.secondary_consumption_qty
            )
            self.print(f"Sufficient secondary in cargo: {sufficient_secondary_in_cargo}")

            consume_inputs = data["production_counter"] >= station.production_frequency
            self.print(f"Consume inputs: {consume_inputs}")

            not_at_max_production = (
                station.production_material not in station.cargo or
                station.cargo[station.production_material] < station.production_max
            )
            self.print(f"Not at max production: {not_at_max_production}")

            sufficient_primary_for_boost = (
                sufficient_primary_in_cargo and
                station.cargo[station.primary_import] >= math.floor(station.primary_max * 0.85)
            )
            self.print(f"Sufficient primary for boost: {sufficient_primary_for_boost}")


            if(sufficient_primary_in_cargo and consume_inputs and not_at_max_production):
                station.cargo[station.primary_import] -= station.primary_consumption_qty
                data["primary_consumed"] = station.primary_consumption_qty

                if(has_secondary and
                    sufficient_secondary_in_cargo and
                    sufficient_primary_for_boost):

                    station.cargo[station.secondary_import] -= station.secondary_consumption_qty

                    qty = station.production_qty * 2
                    if station.production_material not in station.cargo:
                        station.cargo[station.production_material] = qty
                    else:
                        qty = min(station.cargo[station.production_material] + qty, station.production_max)
                        station.cargo[station.production_material] = qty

                    data["production_produced"] = qty

                    self.print(f"Created x{station.production_qty}*2 material {station.production_material}")
                    data["secondary_consumed"] = station.secondary_consumption_qty

                else:
                    if not has_secondary:
                        data["secondary_consumed"] = -1
                    else:
                        data["secondary_consumed"] = 0


                    qty = station.production_qty
                    if station.production_material not in station.cargo:
                        station.cargo[station.production_material] = qty
                    else:
                        qty = min(station.cargo[station.production_material] + qty, station.production_max)
                        station.cargo[station.production_material] = qty

                    data["production_produced"] = qty

                    self.print(f"Created x{station.production_qty} material {station.production_material}")


                data["production_counter"] = 0

            elif sufficient_primary_in_cargo and not consume_inputs:
                # increment counter if we have enough in cargo to do work, but havn't reached the counter
                data["production_counter"] += 1

        # update prices
        jitter = 1
        jitter_thresh = 1

        for station in stations:
            if self.debug and  station.primary_import is not MaterialType.cuprite:
                continue

            if station.primary_import in station.cargo:
                percentage_primary = station.cargo[station.primary_import] / (station.primary_max)
            else:
                percentage_primary = 0.0
            station.primary_buy_price = math.floor(max(0,
                    (1.0-percentage_primary) * station.base_primary_buy_price
                    + random.randint(0, jitter_thresh) * jitter
                ))

            if station.secondary_import in station.cargo:
                percentage_secondary = station.cargo[station.secondary_import] / (station.secondary_max)
            else:
                percentage_secondary = 0.0
            station.secondary_buy_price = math.floor(max(0,
                    (1.0-percentage_secondary) * station.base_secondary_buy_price
                    + random.randint(0, jitter_thresh) * jitter
                ))

            if station.production_material in station.cargo:
                percentage_production = station.cargo[station.production_material] / (station.production_max)
            else:
                percentage_production = 0.0
            station.sell_price = math.floor((2.0-percentage_production) * station.base_sell_price) \
                    + random.randint(0, jitter_thresh) * jitter

            # for debugging
            self.print(f"Primary Buy: {station.primary_buy_price} Secondary Buy: {station.secondary_buy_price} Production Sell: {station.sell_price}")

            self.stats.append({
                "station_id": station.id,
                "station_name": station.name,
                "primary_import": station.primary_import,
                "primary_buy_price": station.primary_buy_price,
                "secondary_import": station.secondary_import,
                "secondary_buy_price": station.secondary_buy_price,
                "production_material": station.production_material,
                "sell_price": station.sell_price,
                "primary_consumed": self.station_data[station.id]["primary_consumed"],
                "secondary_consumed": self.station_data[station.id]["secondary_consumed"],
                "production_produced": self.station_data[station.id]["production_produced"],
            })


    def get_stats(self):
        """Return and purge stats"""
        stats = self.stats

        self.stats = []

        return stats

    def print(self, msg):
        if self.debug:
            print(msg)
            sys.stdout.flush()
