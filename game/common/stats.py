
from game.common.enums import *

class GameStats:

    hull_0 = 1000
    hull_1 = 2000
    hull_2 = 3000
    hull_3 = 4000
    hull_4 = 5000

    engine_speed_0 = 5
    engine_speed_1 = 7
    engine_speed_2 = 9
    engine_speed_3 = 11
    engine_speed_4 = 666  # Hail satan

    weapon_damage_0 = 10
    weapon_damage_1 = 20
    weapon_damage_2 = 30
    weapon_damage_3 = 40
    weapon_damage_4 = 50

    weapon_range_0 = 50
    weapon_range_1 = 75
    weapon_range_2 = 100
    weapon_range_3 = 125
    weapon_range_4 = 150

    cargo_space_0 = 500
    cargo_space_1 = 600
    cargo_space_2 = 700
    cargo_space_3 = 800
    cargo_space_4 = 1000

    mining_yield_0 = 5
    mining_yield_1 = 6
    mining_yield_2 = 7
    mining_yield_3 = 8
    mining_yield_4 = 10

    sensor_range_0 = 75
    sensor_range_1 = 100
    sensor_range_2 = 125
    sensor_range_3 = 150
    sensor_range_4 = 175

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
            elif module_level == ModuleLevel.illegal:
                return GameStats.hull_4

        if stat_type == ShipStat.engine_speed:
            if module_level == ModuleLevel.base:
                return GameStats.engine_speed_0
            elif module_level == ModuleLevel.one:
                return GameStats.engine_speed_1
            elif module_level == ModuleLevel.two:
                return GameStats.engine_speed_2
            elif module_level == ModuleLevel.three:
                return GameStats.engine_speed_3
            elif module_level == ModuleLevel.illegal:
                return GameStats.engine_speed_4

        if stat_type == ShipStat.weapon_damage:
            if module_level == ModuleLevel.base:
                return GameStats.weapon_damage_0
            elif module_level == ModuleLevel.one:
                return GameStats.weapon_damage_1
            elif module_level == ModuleLevel.two:
                return GameStats.weapon_damage_2
            elif module_level == ModuleLevel.three:
                return GameStats.weapon_damage_3
            elif module_level == ModuleLevel.illegal:
                return GameStats.weapon_damage_4

        if stat_type == ShipStat.cargo_space:
            if module_level == ModuleLevel.base:
                return GameStats.cargo_space_0
            elif module_level == ModuleLevel.one:
                return GameStats.cargo_space_1
            elif module_level == ModuleLevel.two:
                return GameStats.cargo_space_2
            elif module_level == ModuleLevel.three:
                return GameStats.cargo_space_3
            elif module_level == ModuleLevel.illegal:
                return GameStats.cargo_space_4

        if stat_type == ShipStat.mining_yield:
            if module_level == ModuleLevel.base:
                return GameStats.mining_yield_0
            elif module_level == ModuleLevel.one:
                return GameStats.mining_yield_1
            elif module_level == ModuleLevel.two:
                return GameStats.mining_yield_2
            elif module_level == ModuleLevel.three:
                return GameStats.mining_yield_3
            elif module_level == ModuleLevel.illegal:
                return GameStats.mining_yield_4

        if stat_type == ShipStat.sensor_range:
            if module_level == ModuleLevel.base:
                return GameStats.sensor_range_0
            elif module_level == ModuleLevel.one:
                return GameStats.sensor_range_1
            elif module_level == ModuleLevel.two:
                return GameStats.sensor_range_2
            elif module_level == ModuleLevel.three:
                return GameStats.sensor_range_3
            elif module_level == ModuleLevel.illegal:
                return GameStats.sensor_range_4

        if stat_type == ShipStat.weapon_range:
            if module_level == ModuleLevel.base:
                return GameStats.weapon_range_0
            elif module_level == ModuleLevel.one:
                return GameStats.weapon_range_1
            elif module_level == ModuleLevel.two:
                return GameStats.weapon_range_2
            elif module_level == ModuleLevel.three:
                return GameStats.weapon_range_3
            elif module_level == ModuleLevel.illegal:
                return GameStats.weapon_range_4

    # notoriety stats
    destroy_civilian = 2
    destroy_bounty_hunter = 3
    attack_police = 1
    destroy_police = 4
    destroy_enforcer = 5
    carrying_illegal_module = 1

    destroy_pirate = -2
    pay_off_bounty = -1

    # module prices ( figured in helper method )
    module_level_1_materials_cost = 100
    module_level_1_adjustment = 1.0

    module_level_2_materials_cost = 400
    module_level_2_adjustment = 1.0

    module_level_3_materials_cost = 900
    module_level_3_adjustment = 1.0

    module_level_4_materials_cost = 1600
    module_level_4_adjustment = 1.0

    # module unlock prices ( figured in helper method )
    unlock_slot_0_materials_cost = 100
    unlock_slot_0_adjustment = 0.75

    unlock_slot_1_materials_cost = 200
    unlock_slot_1_adjustment = 0.75

    unlock_slot_2_materials_cost = 300
    unlock_slot_2_adjustment = 0.75

    unlock_slot_3_materials_cost = 400
    unlock_slot_3_adjustment = 0.75

    # repair stats
    passive_repair_counter = 10
    passive_repair_amount = 500

    # stats to determine repair price ( figured in helper method )
    repair_adjustment = 0.75
    repair_materials_cost = 50

    repair_discount = 0.5
    repair_markup = 2

    healing_combat_cooldown = 20


