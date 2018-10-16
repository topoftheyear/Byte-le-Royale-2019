from game.common.enums import *

class GameStats:

    hull_0 = 1000
    hull_1 = 2000
    hull_2 = 2000
    hull_3 = 2000

    import random
    engine_speed_0 = 6
    engine_speed_1 = 101
    engine_speed_2 = 201
    engine_speed_3 = 301

    weapon_damage_0 = 10
    weapon_damage_1 = 20
    weapon_damage_2 = 20
    weapon_damage_3 = 20

    weapon_range_0 = 50
    weapon_range_1 = 75
    weapon_range_2 = 100
    weapon_range_3 = 125

    cargo_space_0 = 500000
    cargo_space_1 = 650000
    cargo_space_2 = 800000
    cargo_space_3 = 1000000

    mining_yield_0 = 50000
    mining_yield_1 = 65000
    mining_yield_2 = 80000
    mining_yield_3 = 100000

    sensor_range_0 = 75
    sensor_range_1 = 100
    sensor_range_2 = 125
    sensor_range_3 = 150

    def get_ship_stat(stat_type, module_level):

        if stat_type == ShipStat.hull:
            if module_level == ModuleLevel.base:
                return GameStats.hull_0
            elif module_level == ModuleLevel.one:
                return GameStats.hull_1
            elif module_level == ModuleLevel.two:
                return GameStats.hull_2
            elif module_level == ModuleLevel.three:
                return GameStats.hull_3

        if stat_type == ShipStat.engine_speed:
            if module_level == ModuleLevel.base:
                return GameStats.engine_speed_0
            elif module_level == ModuleLevel.one:
                return GameStats.engine_speed_1
            elif module_level == ModuleLevel.two:
                return GameStats.engine_speed_2
            elif module_level == ModuleLevel.three:
                return GameStats.engine_speed_3

        if stat_type == ShipStat.weapon_damage:
            if module_level == ModuleLevel.base:
                return GameStats.weapon_damage_0
            elif module_level == ModuleLevel.one:
                return GameStats.weapon_damage_1
            elif module_level == ModuleLevel.two:
                return GameStats.weapon_damage_2
            elif module_level == ModuleLevel.three:
                return GameStats.weapon_damage_3

        if stat_type == ShipStat.cargo_space:
            if module_level == ModuleLevel.base:
                return GameStats.cargo_space_0
            elif module_level == ModuleLevel.one:
                return GameStats.cargo_space_1
            elif module_level == ModuleLevel.two:
                return GameStats.cargo_space_2
            elif module_level == ModuleLevel.three:
                return GameStats.cargo_space_3

        if stat_type == ShipStat.mining_yield:
            if module_level == ModuleLevel.base:
                return GameStats.mining_yield_0
            elif module_level == ModuleLevel.one:
                return GameStats.mining_yield_1
            elif module_level == ModuleLevel.two:
                return GameStats.mining_yield_2
            elif module_level == ModuleLevel.three:
                return GameStats.mining_yield_3

        if stat_type == ShipStat.sensor_range:
            if module_level == ModuleLevel.base:
                return GameStats.sensor_range_0
            elif module_level == ModuleLevel.one:
                return GameStats.sensor_range_1
            elif module_level == ModuleLevel.two:
                return GameStats.sensor_range_2
            elif module_level == ModuleLevel.three:
                return GameStats.sensor_range_3

        if stat_type == ShipStat.weapon_range:
            if module_level == ModuleLevel.base:
                return GameStats.weapon_range_0
            elif module_level == ModuleLevel.one:
                return GameStats.weapon_range_1
            elif module_level == ModuleLevel.two:
                return GameStats.weapon_range_2
            elif module_level == ModuleLevel.three:
                return GameStats.weapon_range_3

    # notoriety stats
    destroy_civilian = 2
    destroy_bounty_hunter = 3
    attack_police = 1
    destroy_police = 4
    destroy_enforcer = 5
    carrying_illegal_module = 1

    destroy_pirate = -2
    pay_off_bounty = -1


