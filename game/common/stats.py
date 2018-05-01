from game.common.enums import *

class GameStats:

    hull_0 = 1000
    hull_1 = 2000
    hull_2 = 2000
    hull_3 = 2000

    engine_speed_0 = 1000
    engine_speed_1 = 2000
    engine_speed_2 = 2000
    engine_speed_3 = 2000

    weapon_damage_0 = 1000
    weapon_damage_1 = 2000
    weapon_damage_2 = 2000
    weapon_damage_3 = 2000

    cargo_space_0 = 1000
    cargo_space_1 = 2000
    cargo_space_2 = 2000
    cargo_space_3 = 2000

    mining_yield_0 = 1000
    mining_yield_1 = 2000
    mining_yield_2 = 2000
    mining_yield_3 = 2000

    sensor_range_0 = 1000
    sensor_range_1 = 2000
    sensor_range_2 = 2000
    sensor_range_3 = 2000

    def get_ship_stat(upgrade_type, upgrade_level):

        if(upgrade_type == UpgradeType.hull):
            if(upgrade_level == UpgradeLevel.base):
                return hull_0
            elif(upgrade_level == UpgradeLevel.one):
                return hull_1
            elif(upgrade_level == UpgradeLevel.two):
                return hull_2
            elif(upgrade_level == UpgradeLevel.three):
                return hull_3

        if(upgrade_type == UpgradeType.engine_speed):
            if(upgrade_level == UpgradeLevel.base):
                return engine_speed_0
            elif(upgrade_level == UpgradeLevel.one):
                return engine_speed_1
            elif(upgrade_level == UpgradeLevel.two):
                return engine_speed_2
            elif(upgrade_level == UpgradeLevel.three):
                return engine_speed_3

        if(upgrade_type == UpgradeType.weapon_damage):
            if(upgrade_level == UpgradeLevel.base):
                return weapon_damage_0
            elif(upgrade_level == UpgradeLevel.one):
                return weapon_damage_1
            elif(upgrade_level == UpgradeLevel.two):
                return weapon_damage_2
            elif(upgrade_level == UpgradeLevel.three):
                return weapon_damage_3

        if(upgrade_type == UpgradeType.cargo_space):
            if(upgrade_level == UpgradeLevel.base):
                return cargo_space_0
            elif(upgrade_level == UpgradeLevel.one):
                return cargo_space_1
            elif(upgrade_level == UpgradeLevel.two):
                return cargo_space_2
            elif(upgrade_level == UpgradeLevel.three):
                return cargo_space_3

        if(upgrade_type == UpgradeType.mining_yield):
            if(upgrade_level == UpgradeLevel.base):
                return mining_yield_0
            elif(upgrade_level == UpgradeLevel.one):
                return mining_yield_1
            elif(upgrade_level == UpgradeLevel.two):
                return mining_yield_2
            elif(upgrade_level == UpgradeLevel.three):
                return mining_yield_3

        if(upgrade_type == UpgradeType.sensor_range):
            if(upgrade_level == UpgradeLevel.base):
                return sensor_range_0
            elif(upgrade_level == UpgradeLevel.one):
                return sensor_range_1
            elif(upgrade_level == UpgradeLevel.two):
                return sensor_range_2
            elif(upgrade_level == UpgradeLevel.three):
                return sensor_range_3


