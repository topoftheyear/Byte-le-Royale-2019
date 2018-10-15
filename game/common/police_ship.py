
from game.common.enums import *
from game.common.ship import Ship

from game.common.stats import GameStats


class PoliceShip(Ship):

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
        #if level == 1:
        #    self.max_hull = GameStats.get_ship_stat(UpgradeType.hull, UpgradeLevel.base)
        #    self.current_hull = self.max_hull
        #    self.engine_speed = GameStats.get_ship_stat(UpgradeType.engine_speed, UpgradeLevel.base)
        #    self.weapon_damage = GameStats.get_ship_stat(UpgradeType.weapon_damage, UpgradeLevel.base)
        #    self.weapon_range = GameStats.get_ship_stat(UpgradeType.weapon_range, UpgradeLevel.base)
        #    self.cargo_space = GameStats.get_ship_stat(UpgradeType.cargo_space, UpgradeLevel.base)
        #    self.mining_yield = GameStats.get_ship_stat(UpgradeType.mining_yield, UpgradeLevel.base)
        #    self.sensor_range = GameStats.get_ship_stat(UpgradeType.sensor_range, UpgradeLevel.base)

        #elif level == 2:
        #    self.max_hull = GameStats.get_ship_stat(UpgradeType.hull, UpgradeLevel.two)
        #    self.current_hull = self.max_hull
        #    self.engine_speed = GameStats.get_ship_stat(UpgradeType.engine_speed, UpgradeLevel.two)
        #    self.weapon_damage = GameStats.get_ship_stat(UpgradeType.weapon_damage, UpgradeLevel.two)
        #    self.weapon_range = GameStats.get_ship_stat(UpgradeType.weapon_range, UpgradeLevel.two)
        #    self.sensor_range = GameStats.get_ship_stat(UpgradeType.sensor_range, UpgradeLevel.two)

        #elif level == 2:
        #    self.max_hull = GameStats.get_ship_stat(UpgradeType.hull, UpgradeLevel.two)
        #    self.current_hull = self.max_hull
        #    self.engine_speed = GameStats.get_ship_stat(UpgradeType.engine_speed, UpgradeLevel.two)
        #    self.weapon_damage = GameStats.get_ship_stat(UpgradeType.weapon_damage, UpgradeLevel.two)
        #    self.weapon_range = GameStats.get_ship_stat(UpgradeType.weapon_range, UpgradeLevel.two)
        #    self.sensor_range = GameStats.get_ship_stat(UpgradeType.sensor_range, UpgradeLevel.two)



