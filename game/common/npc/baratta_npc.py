import random

from game.common.enums import *
from game.common.npc.npc import NPC
from game.utils.helpers import *
from game.client.user_client import UserClient
from game.config import *
import game.utils.filters as F


class BarattaNPC(NPC):

    # Set up the system.
    def __init__(self, ship):
        UserClient.__init__(self)
        self.name = "BarattaNPC"
        self.ship = ship
        self.ship_id = ship.id

        self.action = None
        self.target = None
        self.material = None

        self.type = None

        self.fields = None
        self.stations = None

        self.previous_position = None
        self.inactive_counter = 0
        self.action_choices = ["mine", "pirate", "module", "trade"]
        self.module_choices = [ModuleType.hull, ModuleType.weapons]

        # Upgrade weapons, then hull
        self.other_ships = None
        self.mod1_next_level = 1
        self.mod0_next_level = 1

    def team_name(self):
        return f"{self.name} #{random.randint(1,1000)}"

    def combat(self, other_ships):
        if self.target is None:
            best_target = None
            hull = self.ship.current_hull
            if other_ships is not None:
                for ships in self.other_ships:
                    if ships.current_hull <= hull and ships is not ObjectType.police:
                        best_target = ships
                        hull = ships.current_hull
            if best_target is None and other_ships is None:
                self.target = None
        else:
            best_target = self.target
        return best_target

    def take_turn(self, universe):
        # initialize empty variables
        if self.fields is None:
            self.fields = universe.get("asteroid_fields")
        if self.stations is None:
            self.stations = universe.get(ObjectType.station)
        self.other_ships = ships_in_attack_range(universe, self.ship)

        # select new action if not currently in one
        if self.action is None:
            self.action = random.choice(self.action_choices)

        # Mining stuff
        if self.action is "mine":
            # Defend my plot
            # if no target, determine what to do
            if self.target is None:
                self.target = random.choice(self.fields)
                self.move(*self.target.position)

            # Trading to the station
            elif self.target in self.stations:
                self.move(*self.target.position)
                if self.material is None or self.material not in self.ship.inventory:
                    
                    self.action = None
                    self.target = None
                elif in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e:e.position):
                    self.sell_material(self.material, self.ship.inventory[self.material])
                    self.target = None
                    self.action = random.choice(self.action_choices)

            # Go mining
            elif self.target in self.fields:
                self.move(*self.target.position)
                if sum(self.ship.inventory.values()) >= self.ship.cargo_space * 0.85:
                    # if the target is a sellable station, go there
                    for item, quantity in self.ship.inventory.items():
                        if quantity > 0:
                            self.material = item
                            self.target = get_best_material_prices(universe)["best_import_prices"][self.material][
                                "station"]
                            break
                    self.move(*self.target.position)
                else:
                    self.mine()

            # In combat
            elif self.target is ObjectType.ship:
                self.attack(self.target)
                self.move(*self.target.position)

        # If a pirate, go after others
        elif self.action is "pirate":
            if self.target is None:
                self.combat(self.other_ships)
            if self.target is None:
                pass
            elif self.target in [ObjectType.police, ObjectType.enforcer, ObjectType.ship] and not in_secure_zone(self.ship, self.target):
                self.move(*self.target.position)
                self.attack(self.target)
                if self.target.current_hull <= 0:
                    self.target = None
                    self.action = None
            # Made our profit, now to earn it
            elif self.target.object_type is ObjectType.black_market_station:
                self.move(*self.target.position)
                if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e: e.position):
                    self.sell_salvage()
                    self.target = None
                    self.action = None
            else:
                self.move(*self.target.position)

        # If time to module, get one
        elif self.action is "module":
            
            if self.mod0_next_level == 4 or self.mod1_next_level == 4:
                self.target = random.choice(universe.get(ObjectType.black_market_station))
                self.move(*self.target.position)
            else:
                self.target = universe.get(ObjectType.secure_station)[0]
                self.move(*self.target.position)
            if self.ship.module_1 is ModuleType.locked and get_module_unlock_price(get_median_material_price(get_material_sell_prices(universe)), ShipSlot.one) < self.ship.credits:
                self.unlock_module()
                
                self.move(*self.target.position)
                self.action = random.choice(["mine", "pirate"])
            elif get_module_price(get_median_material_price(get_material_sell_prices(universe)), self.mod0_next_level) < self.ship.credits and self.mod0_next_level <= 4:
                self.buy_module(ModuleType.weapons, self.mod0_next_level, self.ship.module_0)
                self.mod0_next_level = self.ship.module_0_level + 1
                
                self.move(*self.target.position)
                self.action = random.choice(["mine", "pirate"])
            elif get_module_price(get_median_material_price(get_material_sell_prices(universe)), self.mod1_next_level) < self.ship.credits and self.mod1_next_level <= 4:
                self.buy_module(ModuleType.engine_speed, self.mod1_next_level, self.ship.module_1)
                self.mod1_next_level = self.ship.module_1_level + 1
                
                self.move(*self.target.position)
                self.action = random.choice(["mine", "pirate", "trade"])
                self.target = None
            else:
                
                self.action = random.choice(["mine", "pirate", "trade"])
                self.target = None

        elif self.action is "trade":
            if self.target is None:
                toSell = get_best_material_prices(universe)
                # picks one of top 3 spots
                toChoose = random.choice([1, 1, 1, 2, 2, 3])
                mat = None
                toSellIter = iter(toSell["best_export_prices"])
                for x in range(toChoose):
                    mat = next(toSellIter)
                self.target = toSell["best_export_prices"][mat]["station"]
            self.move(*self.target.position)
            if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e: e.position):
                self.buy_material(99999)
                self.action = "sell"
                self.target = None

        elif self.action is "sell":
            if self.target is None:
                for thing, amount in self.ship.inventory.items():
                    if amount > 10:
                        self.material = thing
                        values = get_best_material_prices(universe)
                        self.target = values["best_import_prices"][self.material]["station"]
                        break
            else:
                self.move(*self.target.position)
                if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e: e.position):
                    self.sell_material(self.material, self.ship.inventory[self.material])
                    if self.target is None:
                        for thing, amount in self.ship.inventory.items():
                            if amount > 10:
                                self.material = thing
                                values = get_best_material_prices(universe)
                                self.target = values["best_import_prices"][self.material]["station"]
                                break
                        else:
                            self.action = None
                            self.target = None

        # healing
        if self.ship.current_hull / self.ship.max_hull <= 0.45:
            self.move(*universe.get(ObjectType.secure_station)[0].position)
            self.repair(self.ship.max_hull - self.ship.current_hull)

        # inactive tracker
        if self.previous_position is not None and \
                self.ship.position[0] == self.previous_position[0] and \
                self.ship.position[1] == self.previous_position[1]:

            self.inactive_counter += 1

        self.previous_position = self.ship.position

        # Well, time to go back to the mines
        if self.inactive_counter >= 40:
            self.inactive_counter = 0

            self.action = "mine"
            self.target = None
            self.material = None

            self.type = None

            self.fields = None
            self.stations = None

        return self.action_digest()
