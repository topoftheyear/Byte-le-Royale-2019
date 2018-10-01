from game.common.enums import *

class GameStats:

    hull_0 = 1000
    hull_1 = 2000
    hull_2 = 2000
    hull_3 = 2000

    import random
    engine_speed_0 = 3
    engine_speed_1 = 4
    engine_speed_2 = 6
    engine_speed_3 = 8

    weapon_damage_0 = 1000
    weapon_damage_1 = 2000
    weapon_damage_2 = 2000
    weapon_damage_3 = 2000

    cargo_space_0 = 10000
    cargo_space_1 = 20000
    cargo_space_2 = 20000
    cargo_space_3 = 20000

    mining_yield_0 = 1000
    mining_yield_1 = 1350
    mining_yield_2 = 1700
    mining_yield_3 = 2000

    sensor_range_0 = 1000
    sensor_range_1 = 2000
    sensor_range_2 = 2000
    sensor_range_3 = 2000

    def get_ship_stat(upgrade_type, upgrade_level):

        if upgrade_type == UpgradeType.hull:
            if upgrade_level == UpgradeLevel.base:
                return GameStats.hull_0
            elif upgrade_level == UpgradeLevel.one:
                return GameStats.hull_1
            elif upgrade_level == UpgradeLevel.two:
                return GameStats.hull_2
            elif upgrade_level == UpgradeLevel.three:
                return GameStats.hull_3

        if upgrade_type == UpgradeType.engine_speed:
            if upgrade_level == UpgradeLevel.base:
                return GameStats.engine_speed_0
            elif upgrade_level == UpgradeLevel.one:
                return GameStats.engine_speed_1
            elif upgrade_level == UpgradeLevel.two:
                return GameStats.engine_speed_2
            elif upgrade_level == UpgradeLevel.three:
                return GameStats.engine_speed_3

        if upgrade_type == UpgradeType.weapon_damage:
            if upgrade_level == UpgradeLevel.base:
                return GameStats.weapon_damage_0
            elif upgrade_level == UpgradeLevel.one:
                return GameStats.weapon_damage_1
            elif upgrade_level == UpgradeLevel.two:
                return GameStats.weapon_damage_2
            elif upgrade_level == UpgradeLevel.three:
                return GameStats.weapon_damage_3

        if upgrade_type == UpgradeType.cargo_space:
            if upgrade_level == UpgradeLevel.base:
                return GameStats.cargo_space_0
            elif upgrade_level == UpgradeLevel.one:
                return GameStats.cargo_space_1
            elif upgrade_level == UpgradeLevel.two:
                return GameStats.cargo_space_2
            elif upgrade_level == UpgradeLevel.three:
                return GameStats.cargo_space_3

        if upgrade_type == UpgradeType.mining_yield:
            if upgrade_level == UpgradeLevel.base:
                return GameStats.mining_yield_0
            elif upgrade_level == UpgradeLevel.one:
                return GameStats.mining_yield_1
            elif upgrade_level == UpgradeLevel.two:
                return GameStats.mining_yield_2
            elif upgrade_level == UpgradeLevel.three:
                return GameStats.mining_yield_3

        if upgrade_type == UpgradeType.sensor_range:
            if upgrade_level == UpgradeLevel.base:
                return GameStats.sensor_range_0
            elif upgrade_level == UpgradeLevel.one:
                return GameStats.sensor_range_1
            elif upgrade_level == UpgradeLevel.two:
                return GameStats.sensor_range_2
            elif upgrade_level == UpgradeLevel.three:
                return GameStats.sensor_range_3


