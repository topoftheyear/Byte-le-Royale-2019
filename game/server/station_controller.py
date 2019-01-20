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

        self.stats = [] # reset stats

    def tick(self, stations):
        for station in stations:

            if self.debug and station.production_material != MaterialType.copper:
                continue

            station_id = station.id

            self.station_data[station_id]["primary_consumed"] = 0

            if station.secondary_import != -1:
                self.station_data[station_id]["secondary_consumed"] = 0
            else:
                self.station_data[station_id]["secondary_consumed"] = -1

            self.station_data[station_id]["production_produced"] = 0

            self.print(f"Update Station {station.name} ({station.id}), produces: {station.production_material}")
            self.print(f"station.cargo: {station.cargo}")
            self.print(f"production counter: {self.station_data[station_id]['production_counter']}")


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

            consume_inputs = self.station_data[station_id]["production_counter"] >= station.production_frequency
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

            if sufficient_primary_in_cargo and consume_inputs and not_at_max_production:
                station.cargo[station.primary_import] -= station.primary_consumption_qty
                self.station_data[station_id]["primary_consumed"] += station.primary_consumption_qty

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

                    self.station_data[station_id]["production_produced"] += qty

                    self.print(f"Created x{station.production_qty}*2 material {station.production_material}")
                    self.station_data[station_id]["secondary_consumed"] += station.secondary_consumption_qty

                else:
                    qty = station.production_qty
                    if station.production_material not in station.cargo:
                        station.cargo[station.production_material] = qty
                    else:
                        qty = min(station.cargo[station.production_material] + qty, station.production_max)
                        station.cargo[station.production_material] = qty

                    self.station_data[station_id]["production_produced"] += qty

                    self.print(f"Created x{station.production_qty} material {station.production_material}")

            elif sufficient_primary_in_cargo and not consume_inputs:
                # increment counter if we have enough in cargo to do work, but havn't reached the counter
                self.station_data[station_id]["production_counter"] += 1

        # update prices
        jitter = 1
        jitter_thresh = 1

        for station in stations:

            value_max_mult = 100
            increase_mult = 0.01
            decrease_mult = 0.01
            if station.production_material in station.cargo:
                percentage_production = station.cargo[station.production_material] / (station.production_max)
            else:
                percentage_production = 0.0

            max_price = station.base_sell_price * value_max_mult
            percentage_max = math.floor(max_price * percentage_production)
            min_price = math.floor(station.base_sell_price * 0.5)
            if min_price > percentage_max:
                percentage_max = min_price
            if station.sell_price < percentage_max:
                station.sell_price += int(min(station.base_sell_price * increase_mult, percentage_max - station.sell_price) + random.randint(0, jitter_thresh) * jitter)
            elif station.sell_price > percentage_max:
                station.sell_price -= int(min(station.base_sell_price * decrease_mult, station.sell_price - percentage_max) + random.randint(0, jitter_thresh) * jitter)

            primary_max_price = station.base_primary_buy_price * value_max_mult
            primary_percentage_max = math.floor(primary_max_price * percentage_production)
            primary_min_price = station.base_primary_buy_price * 0.5
            if primary_min_price > primary_max_price:
                primary_percentage_max = primary_min_price
            if station.primary_buy_price < primary_percentage_max:
                station.primary_buy_price += int(min(station.base_primary_buy_price * increase_mult, primary_percentage_max - station.primary_buy_price) + random.randint(0, jitter_thresh) * jitter)
            elif station.primary_buy_price > primary_percentage_max:
                station.primary_buy_price -= int(min(station.base_primary_buy_price * decrease_mult, station.primary_buy_price - primary_percentage_max) + random.randint(0, jitter_thresh) * jitter)

            secondary_max_price = station.base_secondary_buy_price * value_max_mult
            secondary_percentage_max = math.floor(secondary_max_price * percentage_production)
            secondary_min_price = station.base_secondary_buy_price * 0.5
            if secondary_min_price > secondary_max_price:
                secondary_percentage_max = secondary_min_price
            if station.secondary_buy_price < secondary_percentage_max:
                station.secondary_buy_price += int(min(station.base_primary_buy_price * increase_mult, secondary_percentage_max - station.secondary_buy_price) + random.randint(0, jitter_thresh) * jitter)
            elif station.secondary_buy_price > secondary_percentage_max:
                station.secondary_buy_price -= int(min(station.base_secondary_buy_price * decrease_mult, station.secondary_buy_price - secondary_percentage_max) + random.randint(0, jitter_thresh) * jitter)

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
