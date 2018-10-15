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

        self.debug = False
        self.events = []
        self.stats = []

    def print(self, msg):
        if self.debug:
            print(str(msg))
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
                    # Check for all stations in the universe
                    if thing.object_type not in [ObjectType.secure_station, ObjectType.black_market_station]:
                        continue

                    current_station = thing
                    self.print('ModuleController: found a ship trying to purchase module')

                    # Check if ship is within range of a / the station
                    ship_in_radius = in_radius(
                            current_station,
                            ship,
                            lambda s,t:s.accessibility_radius,
                            lambda e:e.position)

                    if not ship_in_radius:
                        continue

                    self.print('ModuleController: Ship in range of a station')
                    module = ship.action_param_1
                    upgrade_level = ship.action_param_2
                    ship_slot = ship.action_param_3

                    # Check is the slot is available
                    if ship_slot == UpgradeType.locked:
                        continue
                    self.print('ModuleController: Ship module slot is unlocked')


                    # Check if the module requested is illegal
                    if upgrade_level == UpgradeLevel.illegal and current_station not in [ObjectType.black_market_station]:
                        continue

                    # Check if ship has the funds and reduce them
                    # TODO Implement fund checking
                    if not True:
                        continue
                    self.print('ModuleController: Ship has fund for module')

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
                    for module, level in zip(ship_mod, ship_mod_lvl):
                        if ship_mod == UpgradeType.engine_speed:
                            self.engine_speed = GameStats.get_ship_stat(
                                    UpgradeType.engine_speed,
                                    level)
                        elif ship_mod == UpgradeType.weapon_damage or ship_mod == UpgradeType.weapon_range:
                            # NOTE: fix this oddity - separate module types and ship stat types
                            self.weapon_damage = GameStats.get_ship_stat(
                                    UpgradeType.weapon_damage,
                                    level)
                            self.weapon_range = GameStats.get_ship_stat(
                                    UpgradeType.weapon_range,
                                    level)

                        elif ship_mod == UpgradeType.cargo_space:
                            self.cargo_space = GameStats.get_ship_stat(
                                    UpgradeType.cargo_space,
                                    level)

                            self.mining_yield = GameStats.get_ship_stat(
                                    UpgradeType.mining_yield,
                                    level)

                        elif ship_mod == UpgradeType.hull:
                            original_hull = self.max_hull
                            self.max_hull = GameStats.get_ship_stat(
                                    UpgradeType.hull,
                                    level)
                            # TODO: Verify this does not cause problems when downgrading and low on health
                            # add the differenct between the two to current hull.
                            self.current_hull += self.max_hull - original_hull

                        elif ship_mod == UpgradeType.sensor_range:
                            self.sensor_range = GameStats.get_ship_stat(
                                    UpgradeType.sensor_range,
                                    level)


                    # Logging
                    self.print('ModuleController: Logging purchase')
                    self.events.append({
                        "type": LogEvent.module_purchased,
                        "ship_id": ship.id,
                        "module": module,
                        "level": upgrade_level,
                        "slot": ship_slot
                    })
