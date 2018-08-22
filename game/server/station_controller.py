import math
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

        self.log = []
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


                if(has_secondary and
                    sufficient_secondary_in_cargo and
                    sufficient_primary_for_boost):

                    station.cargo[station.secondary_import] -= station.secondary_consumption_qty

                    if station.production_material not in station.cargo:
                        station.cargo[station.production_material] = station.production_qty * 2
                    else:
                        station.cargo[station.production_material] += station.production_qty * 2

                    print(f"Created x{station.production_qty}*2 material {station.production_material}")

                else:

                    if station.production_material not in station.cargo:
                        station.cargo[station.production_material] = station.production_qty
                    else:
                        station.cargo[station.production_material] += station.production_qty

                    print(f"Created x{station.production_qty} material {station.production_material}")

                data["production_counter"] = 0

            elif sufficient_primary_in_cargo and not consume_inputs:
                # increment counter if we have enough in cargo to do work, but havn't reached the counter
                data["production_counter"] += 1




    def get_log(self):
        """Return and purge log"""
        log = self.log

        self.log = []

        return log

    def print(self, msg):
        if self.debug:
            print(msg)
            sys.stdout.flush()
