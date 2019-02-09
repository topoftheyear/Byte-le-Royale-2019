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

        self.max_price_multiplier = 20
        self.min_price = 5
        self.rate_of_change_multiplier = 0.03

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
                    prev_cargo = None
                    if station.production_material not in station.cargo:
                        station.cargo[station.production_material] = qty
                    else:
                        prev_cargo = station.cargo[station.production_material]
                        qty = min(qty, station.production_max - prev_cargo)
                        station.cargo[station.production_material] += qty

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
<<<<<<< HEAD
        for station in stations:

            # selling material price modification
            # maximum price is a dynamic multiplier by the base price
            max_price = math.ceil(station.base_sell_price * self.max_price_multiplier)

            # percent of how full the cargo is
            cargo_ratio = station.cargo[station.production_material] / station.production_max

            # percent of where the price stands between the highest and lowest it can be
            price_ratio = (station.sell_price - self.min_price) / (max_price - self.min_price)

            # what the price should be given supply / demand laws
            destination = (1 - cargo_ratio) * (max_price - self.min_price) + self.min_price

            # rate at which the price shall change, determined by distance to destination and current price
            rate_of_change = math.ceil(abs(destination - station.sell_price) * self.rate_of_change_multiplier)

            # prevent the rate from being too high
            rate_of_change = min(rate_of_change, 5)

            # if the cargo ratio is larger than the price ratio, reduce the price
            if cargo_ratio > 1 - price_ratio:
                station.sell_price -= rate_of_change

                if station.sell_price <= self.min_price:
                    station.sell_price = self.min_price

                    # dynamically changing the price frame down with a poor economy
                    self.max_price_multiplier -= 0.05
                    if self.max_price_multiplier < 1:
                        self.max_price_multiplier = 1

            # if the cargo ratio is smaller than the price ratio, increase the price
            elif cargo_ratio < 1 - price_ratio:
                station.sell_price += rate_of_change

                if station.sell_price >= max_price:
                    station.sell_price = max_price

                    # dynamically changing the price frame up with a good economy
                    self.max_price_multiplier += 0.04

            # ceiling function so price is always an integer
            station.sell_price = math.ceil(station.sell_price)


            # primary material price modification
            max_price = math.ceil(station.base_primary_buy_price * self.max_price_multiplier)

            cargo_ratio = station.cargo[station.primary_import] / station.primary_max
            price_ratio = (station.primary_buy_price - self.min_price) / (max_price - self.min_price)

            destination = (1 - cargo_ratio) * (max_price - self.min_price)
            rate_of_change = math.ceil(abs(destination - station.primary_buy_price) * self.rate_of_change_multiplier)
            rate_of_change = min(rate_of_change, 5)

            if cargo_ratio > 1 - price_ratio:
                station.primary_buy_price -= rate_of_change
            elif cargo_ratio < 1 - price_ratio:
                station.primary_buy_price += rate_of_change

            station.primary_buy_price = math.ceil(sorted([self.min_price, station.primary_buy_price, max_price])[1])


            # secondary material price modification if need be
            if station.secondary_import is not None and station.secondary_import is not MaterialType.null:
                max_price = math.ceil(station.base_secondary_buy_price * self.max_price_multiplier)

                cargo_ratio = station.cargo[station.secondary_import] / station.secondary_max
                price_ratio = (station.secondary_buy_price - self.min_price) / (max_price - self.min_price)

                destination = (1 - cargo_ratio) * (max_price - self.min_price)
                rate_of_change = math.ceil(abs(destination - station.secondary_buy_price) * self.rate_of_change_multiplier)
                rate_of_change = min(rate_of_change, 5)

                if cargo_ratio > 1 - price_ratio:
                    station.secondary_buy_price -= rate_of_change
                elif cargo_ratio < 1 - price_ratio:
                    station.secondary_buy_price += rate_of_change

                station.secondary_buy_price = math.ceil(sorted([self.min_price, station.secondary_buy_price, max_price])[1])

=======
        jitter = 1
        jitter_thresh = 4

        for station in stations:
            # variables to change for balance

            value_max_mult = 25 #a multiplier for the max value prices will approach
            min_value_ratio = 0.3 #a ratio used on the base_price to determine the minimum a price will go to
            increase_mult = 0.0000001 #a multiplier multiplied to the base price to determine number to add to price when scaling
            decrease_mult = 0.0000001 #ditto to line above

            # the ratios of the three different materials in a station compared to the max they can hold of it

            percentage_production = None
            percentage_primary = None
            percentage_secondary = None
            no_sec = False
            percentage_production = station.cargo[station.production_material] / station.production_max
            percentage_primary = station.cargo[station.primary_import] / station.primary_max
            if station.secondary_import is MaterialType.null:
                no_sec = True
            else:
                percentage_secondary = station.cargo[station.secondary_import] / station.secondary_max

            # the logic for changing sell price
            max_price = station.base_sell_price * value_max_mult # the max price the value will approach
            sell_percentage_max = math.floor(max_price * (1-percentage_production)) # used for a dynamic max price, the less of the production material it has the higher the price can go at that time
            min_sell = math.ceil(station.base_sell_price * min_value_ratio) # the minimum sell price
            if station.sell_price > sell_percentage_max: # the price will decrease to approach the min_sell value
                station.sell_price -= math.ceil(station.base_sell_price * decrease_mult + random.randint(0, jitter_thresh) * jitter)
                if station.sell_price < min_sell:
                    station.sell_price = min_sell
            elif station.sell_price < sell_percentage_max: # the price will increase to approach the percentage_max value
                station.sell_price += math.ceil(station.base_sell_price * increase_mult + random.randint(0, jitter_thresh) * jitter)

            # the logic for changing primary price
            primary_max_price = station.base_primary_buy_price * value_max_mult # the max price the value will approach
            primary_percentage_max = math.floor(primary_max_price * (1 - percentage_primary)) # used for a dynamic max price, the less of the primary material it has the higher the price can go at that time
            primary_min_price = math.ceil(station.base_primary_buy_price * min_value_ratio) # the minimum sell price
            if station.primary_buy_price < primary_percentage_max: # the price will increase to approach the percentage_max value
                station.primary_buy_price += math.ceil(station.base_primary_buy_price * increase_mult + random.randint(0, jitter_thresh) * jitter)
            elif station.primary_buy_price > primary_percentage_max: # the price will decrease to approach the primary_min_price value

                station.primary_buy_price -= math.ceil(station.base_primary_buy_price * decrease_mult + random.randint(0, jitter_thresh) * jitter)
                if station.primary_buy_price < primary_min_price:
                    station.primary_buy_price = primary_min_price


            # the logic for changing secondary price
            if not no_sec:
                secondary_max_price = station.base_secondary_buy_price * value_max_mult # the max price the value will approach
                secondary_percentage_max = math.floor(secondary_max_price * (1 - percentage_secondary)) # used for a dynamic max price, the less of the secondary material it has the higher the price can go at that time
                secondary_min_price = math.ceil(station.base_secondary_buy_price * min_value_ratio) # the minimum sell price
                if station.secondary_buy_price < secondary_percentage_max: # the price will increase to approach the percentage_max value
                    station.secondary_buy_price += math.ceil(station.base_secondary_buy_price * increase_mult + random.randint(0, jitter_thresh) * jitter)
                elif station.secondary_buy_price > secondary_percentage_max: # the price will decrease to approach the secondary_min_price value
                    station.secondary_buy_price -= math.ceil(station.base_secondary_buy_price * decrease_mult + random.randint(0, jitter_thresh) * jitter)
                    if station.secondary_buy_price < secondary_min_price:
                        station.secondary_buy_price = secondary_min_price
>>>>>>> master

            # for debugging
            self.print(f"Station {station.name} Primary Buy: {station.primary_buy_price} Secondary Buy: {station.secondary_buy_price} Production Sell: {station.sell_price}")

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
