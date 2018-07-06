# Enumeration Values used for serialization/deserialization of objects
# As well as indicating different thins
#
# e.g.
# class UnitType:
#   knight = 0
#   brawler = 1
#   pikeman = 2
#

class UpgradeType:
    locked = -2
    empty = -1
    hull = 0
    engine_speed = 1
    weapon_damage = 2
    cargo_space = 3
    mining_yield = 4
    sensor_range = 5

class UpgradeLevel:
    base = 0
    one = 1
    two = 2
    three = 3

class LogEvent:
    demo = 0


class MessageType:
    null = 0
    demo = 0
    ping = 1
    pong = 2
    team_name = 3
    take_turn = 4


class PlayerAction:
    none = 0

class SecurityLevel:
    engine = 0 # visible by server and visualizer
    player_owned = 1 # visible if a player owns the object
    other_player = 2 # visible if a player does not own the object

class ObjectType:
    ship = 0
