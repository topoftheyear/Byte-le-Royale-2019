import sys
import math

from game.common.enums import *
from game.common.name_helpers import *
from game.common.station import *
from game.common.ship import Ship
from game.utils.helpers import *
from game.common.stats import *

class ModuleController:

    def __init__(self):

        self.debug = True
        self.events = []
        self.stats = []

    def print(self, msg):
        if self.debug:
            print("Module Controller: " + str(msg))
            sys.stdout.flush()

    def get_events(self):
        e = self.events
        self.events = []
        return e

    def get_stats(self):
        s = self.stats
        self.stats = []
        return s

    def handle_actions(self, living_ships, universe, teams, npc_teams):

        for team, data in { **teams, **npc_teams}.items():
            ship = data["ship"]

            # Check for ships that are performing the buy module action
            if ship.action is PlayerAction.buy_module:

                if not ship.is_alive():
                    continue

                for thing in universe:
                    # Check for all applicable stations in the universe
                    if thing.object_type not in [ObjectType.black_market_station, ObjectType.secure_station]:
                        continue

                    current_station = thing
                    self.print('Found a ship trying to purchase module')

                    if thing.object_type is ObjectType.secure_station:
                        self.print('Secure Station found')
                    if thing.object_type is ObjectType.black_market_station:
                        self.print('Black Market found')

                    # Check if ship is within range of a / the station
                    ship_in_radius = in_radius(
                            current_station,
                            ship,
                            lambda s,t:s.accessibility_radius,
                            lambda e:e.position)

                    if not ship_in_radius:
                        continue

                    self.print('Ship in range of a station')
                    module = ship.action_param_1
                    upgrade_level = ship.action_param_2
                    ship_slot = ship.action_param_3

                    # Check is the slot is available
                    if ship_slot == ModuleType.locked:
                        continue
                    self.print('Ship module slot is unlocked')


                    # Check if the module requested is illegal
                    if upgrade_level == ModuleLevel.illegal and current_station is ObjectType.black_market_station:
                        continue

                    # TODO verify that ship doesn't already have module

                    # Check if ship has the funds and reduce them
                    # TODO Implement fund checking
                    if not True:
                        continue
                    self.print('Ship has fund for module')

                    # Apply purchase to ship
                    if ship_slot == ShipSlot.zero:
                        ship.module_0 = module
                        ship.module_0_level = upgrade_level

                    if ship_slot == ShipSlot.one:
                        ship.module_1 = module
                        ship.module_1_level = upgrade_level

                    if ship_slot == ShipSlot.two:
                        ship.module_2 = module
                        ship.module_2_level = upgrade_level

                    if ship_slot == ShipSlot.three:
                        ship.module_3 = module
                        ship.module_3_level = upgrade_level


                    #update ship stats
                    self.apply_modules(ship)

                    # Logging
                    self.print('Logging purchase')
                    self.events.append({
                        "type": LogEvent.module_purchased,
                        "ship_id": ship.id,
                        "module": module,
                        "level": upgrade_level,
                        "slot": ship_slot
                    })

    def apply_modules(self, ship):
        ship_mod = [
                ship.module_0,
                ship.module_1,
                ship.module_2,
                ship.module_3
                ]

        ship_mod_lvl = [
                ship.module_0_level,
                ship.module_1_level,
                ship.module_2_level,
                ship.module_3_level
                ]


        # reset all stats
        ship.max_hull = GameStats.get_ship_stat(ModuleType.hull, ModuleLevel.base)
        ship.current_hull = ship.max_hull

        ship.engine_speed = GameStats.get_ship_stat(ShipStat.engine_speed, ModuleLevel.base)

        ship.weapon_damage = GameStats.get_ship_stat(ShipStat.weapon_damage, ModuleLevel.base)
        ship.weapon_range = GameStats.get_ship_stat(ShipStat.weapon_range, ModuleLevel.base)

        ship.cargo_space = GameStats.get_ship_stat(ShipStat.cargo_space, ModuleLevel.base)

        ship.mining_yield = GameStats.get_ship_stat(ShipStat.mining_yield, ModuleLevel.base)

        ship.sensor_range = GameStats.get_ship_stat(ShipStat.sensor_range, ModuleLevel.base)


        # apply modules
        for module, level in zip(ship_mod, ship_mod_lvl):
            if module is ModuleType.engine_speed:
                ship.engine_speed = GameStats.get_ship_stat(
                        ShipStat.engine_speed,
                        level)

            elif module is ModuleType.weapons:
                ship.weapon_damage = GameStats.get_ship_stat(
                        ShipStat.weapon_damage,
                        level)
                ship.weapon_range = GameStats.get_ship_stat(
                        ShipStat.weapon_range,
                        level)

            elif module is ModuleType.cargo_and_mining:
                ship.cargo_space = GameStats.get_ship_stat(
                        ModuleLevel.cargo_space,
                        level)

                ship.mining_yield = GameStats.get_ship_stat(
                        ModuleLevel.mining_yield,
                        level)

            elif module is ModuleType.hull:
                ship.max_hull = GameStats.get_ship_stat(
                        ModuleLevel.hull,
                        level)
                ship.current_hull = ship.max_hull

            elif module is ModuleType.sensors:
                ship.sensor_range = GameStats.get_ship_stat(
                        ModuleLevel.sensor_range,
                        level)


