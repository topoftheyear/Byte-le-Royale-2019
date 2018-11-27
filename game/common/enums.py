# Enumeration Values used for serialization/deserialization of objects
# As well as indicating different things
#

class ModuleType:
    locked = -2
    empty = -1
    hull = 0
    engine_speed = 1
    weapons = 2
    cargo_and_mining = 3
    sensors = 4

class ShipStat:
    hull = 0
    engine_speed = 1
    weapon_damage = 2
    cargo_space = 3
    mining_yield = 4
    sensor_range = 5
    weapon_range = 6

class ModuleLevel:
    base = 0
    one = 1
    two = 2
    three = 3
    illegal = 4

class LogEvent:
    null = 0
    ship_move = 1
    market_update = 2
    ship_mine = 3
    notoriety_change = 4
    ship_attack = 5
    ship_destroyed = 6
    ship_respawned = 7
    police_removed = 8
    police_spawned = 9
    enforcer_spawned = 10
    module_purchased = 11
    module_unlocked = 12
    cargo_dropped = 13
    illegal_salvage_spawned = 14

class MessageType:
    null = 0
    demo = 0
    ping = 1
    pong = 2
    team_name = 3
    take_turn = 4


class PlayerAction:
    none = 0
    mine = 1
    attack = 2
    buy_module = 3
    unlock_module = 4
    drop_cargo = 5
    salvage = 6

class SecurityLevel:
    engine = 0 # visible by server and visualizer
    player_owned = 1 # visible if a player owns the object
    other_player = 2 # visible if a player does not own the object

class ObjectType:
    ship = 0
    station = 1
    black_market_station = 2
    secure_station = 3
    goethite_field = 4
    cuprite_field = 5
    gold_field = 6

    material = 7

    police = 8
    enforcer = 9

    illegal_salvage = 10

class MaterialType:
    null = -1
    iron = 1
    steel = 2
    copper = 3
    circuitry = 4
    pylons = 5
    weaponry = 6
    machinery = 7
    computers = 8
    drones = 9
    gold = 10
    goethite = 11
    cuprite = 12
    wire = 13
    salvage = 14

class LegalStanding:
    citizen = 0
    pirate = 5
    bounty_hunter = -5


class NotorietyChangeReason:
    # increase notoriety
    destroy_civilian = 0
    destroy_bounty_hunter = 1
    destroy_police = 2
    destroy_enforcer = 3
    carrying_illegal_module = 4
    attack_police = 7

    # decrease notoriety
    destroy_pirate = 5
    pay_off_bounty = 6 # possibly

class ShipSlot:
    zero = 0
    one = 1
    two = 2
    three = 3


