
from game.common.enums import *
from game.common.ship import Ship

from game.common.stats import GameStats


class PoliceShip(Ship):

    def __str__(self):
        x = '<{}: {}>'.format(self.__class__.__name__, self.id)
        return x

    def __repr__(self):
        x = '<{}: {}>'.format(self.__class__.__name__, self.id)
        return x

    def init(self, level=1, position=(0,0)):
        if level == 1:
            name = "Police"
        elif level == 2:
            name = "Police Elite"
        elif level == 3:
            name = "Enforcer"
        super().init(name, True, position)

        if level == 3:
            self.object_type = ObjectType.enforcer
        else:
            self.object_type = ObjectType.police

        # explicitly set ship stats
        if level >= 1:
            self.max_hull = GameStats.get_ship_stat(ShipStat.hull, ModuleLevel.base)
            self.current_hull = self.max_hull
            self.engine_speed = GameStats.get_ship_stat(ShipStat.engine_speed, ModuleLevel.base) * 0.75
            self.weapon_damage = GameStats.get_ship_stat(ShipStat.weapon_damage, ModuleLevel.base) * 0.9
            self.weapon_range = GameStats.get_ship_stat(ShipStat.weapon_range, ModuleLevel.base) * 1.0
            self.cargo_space = GameStats.get_ship_stat(ShipStat.cargo_space, ModuleLevel.base) * 0.9
            self.mining_yield = 0
            self.sensor_range = GameStats.get_ship_stat(ShipStat.sensor_range, ModuleLevel.base) * 0.8

        if level >= 2:
            self.max_hull = GameStats.get_ship_stat(ShipStat.hull, ModuleLevel.two)
            self.current_hull = self.max_hull
            self.engine_speed = GameStats.get_ship_stat(ShipStat.engine_speed, ModuleLevel.two)
            self.weapon_damage = GameStats.get_ship_stat(ShipStat.weapon_damage, ModuleLevel.two)
            self.weapon_range = GameStats.get_ship_stat(ShipStat.weapon_range, ModuleLevel.two)
            self.sensor_range = GameStats.get_ship_stat(ShipStat.sensor_range, ModuleLevel.two)

        if level >= 3:
            self.max_hull = GameStats.get_ship_stat(ShipStat.hull, ModuleLevel.two)
            self.current_hull = self.max_hull
            self.engine_speed = GameStats.get_ship_stat(ShipStat.engine_speed, ModuleLevel.two)
            self.weapon_damage = GameStats.get_ship_stat(ShipStat.weapon_damage, ModuleLevel.two)
            self.weapon_range = GameStats.get_ship_stat(ShipStat.weapon_range, ModuleLevel.two)
            self.sensor_range = GameStats.get_ship_stat(ShipStat.sensor_range, ModuleLevel.two)



