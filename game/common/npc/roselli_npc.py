import random
import bisect

from game.common.enums import *
from game.common.npc.npc import NPC
from game.utils.helpers import *
from game.client.user_client import UserClient
from game.config import *
import game.utils.filters as F

class RoselliNPC(NPC):

    def __init__(self, ship):
        UserClient.__init__(self)
        self.ship = ship
        self.ship_id = ship.id

        self.debug = False

        self.action = None
        self.target = None

        self.previous_hull = 1000

        self.counter = 0

        self.material = None

        self.purchased = None

        self.fields = None
        self.stations = None

    def team_name(self):
        return f"RoselliNPC# {random.randint(1,1000)}"

    def print(self, string):
        if self.debug:
            print(string)

    def take_turn(self, universe):
        # initialize empty variables
        if self.fields is None:
            self.fields = universe.get("asteroid_fields")
        if self.stations is None:
            self.stations = universe.get(ObjectType.station)


        # trade action: if good on money, make a profitable trade ------------------------------------------------------
        if (self.ship.credits > 6000 and self.action is None) or self.action == "trade":
            self.action = "trade"
            # determine a profitable trade
            if self.target is None:
                best_profit = []
                prices = get_best_material_prices(universe)

                for station in self.stations:
                    # if not a trading station, forget about it
                    if station.object_type in [ObjectType.black_market_station, ObjectType.secure_station]:
                        continue

                    material = station.production_material

                    profit = prices["best_import_prices"][material]["import_price"] - prices["best_export_prices"][material]["export_price"]

                    if profit > 0:
                        best_profit.append(material)

                # if nothing is profitable, let's mine instead
                if len(best_profit) == 0:
                    self.clear_variables()
                    self.action = "mine"
                # else pick any of the profitable materials
                else:
                    self.material = random.choice(best_profit)
                    self.target = prices["best_export_prices"][self.material]["station"]
                    self.purchased = False

            # go to the station and buy it
            if self.purchased is not None and not self.purchased:
                self.move(*self.target.position)
                if self.in_radius_of_station(self.ship, self.target):
                    self.buy_material(self.ship.cargo_space - sum(self.ship.inventory.values()))
                    self.target = get_best_material_prices(universe)["best_import_prices"][self.material]["station"]

                    self.purchased = True

            # go to the station that will buy it for the highest price
            elif self.purchased is not None and self.purchased:
                self.move(*self.target.position)
                if self.in_radius_of_station(self.ship, self.target):
                    if self.material in self.ship.inventory.keys():
                        self.sell_material(self.material, self.ship.inventory[self.material])

                    # trade action fulfilled
                    self.clear_variables()

        # mine action: if dirt broke or nothing else is profitable -----------------------------------------------------
        elif (self.ship.credits < 6000 and self.action is None) or self.action == "mine":
            self.action = "mine"
            # determine a field
            if self.target is None:
                best_material = random.choice(self.fields).material_type

                for field in self.fields:
                    if field.material_type is best_material:
                        self.target = field
                        self.material = best_material
                        break

            # move to selected field and mine until over 90% capacity is full
            if self.target.object_type in [ObjectType.goethite_field, ObjectType.gold_field, ObjectType.cuprite_field]:
                self.move(*self.target.position)
                if self.in_radius_of_asteroid_field(self.ship, self.target):
                    self.mine()

                    if sum(self.ship.inventory.values()) >= self.ship.cargo_space * 0.9:
                        prices = get_best_material_prices(universe)
                        self.target = get_best_material_prices(universe)["best_import_prices"][self.material]["station"]

            # move to station and sell the gathered resources
            if self.target.object_type is ObjectType.station:
                self.move(*self.target.position)
                if self.in_radius_of_station(self.ship, self.target):
                    self.sell_material(self.material, self.ship.inventory[self.material])
                    # mine action satisfied
                    self.clear_variables()

        # if attacked in the prior turn --------------------------------------------------------------------------------
        if self.ship.current_hull < self.previous_hull:
            count = 0
            attacker = None
            for other in universe.get(ObjectType.ship):
                if self.in_weapons_range(self.ship, other):
                    count += 1
                    attacker = other

            # attacker could only have been one person
            if count == 1:
                self.print('only one person')
                self.target = attacker
                self.action = "bounty"
            # attacker could be anyone
            else:
                self.action = "defense"
                self.print('couldnt find attacker')

        # if nearby a pirate, be a good bounty hunter maybe ------------------------------------------------------------
        if self.target is not None and self.target.object_type is not ObjectType.ship and random.randint(1,25) == 5:
            for other in universe.get(ObjectType.ship):
                if self.in_weapons_range(self.ship, other) and other.legal_standing is LegalStanding.pirate:
                    self.action = "bounty"
                    self.target = other
                    self.print('found attacker')

        # hunt down the nearby pirate or attacker ----------------------------------------------------------------------
        if self.action == "bounty":
            self.move(*self.target.position)
            if self.target.is_alive():
                self.attack(self.target)
            else:
                self.clear_variables()
                self.action = "clear inventory"
                self.print('other is dead')

        # run away from the stranger attacking you ---------------------------------------------------------------------
        if self.action == "defense":
            if self.counter < 150:
                self.move(*universe.get(ObjectType.secure_station)[0].position)
                self.counter += 1
            else:
                self.clear_variables()
                self.action = "clear inventory"

        # clear leftover garbage in inventory for money ----------------------------------------------------------------
        if self.action == "clear inventory":
            if self.target is None:
                if sum(self.ship.inventory.values()) > 0:
                    for material, amount in self.ship.inventory.items():
                        if amount > 0:
                            self.material = material
                            break

                    self.target = get_best_material_prices(universe)["best_import_prices"][self.material]["station"]

                else:
                    self.clear_variables()

            if self.target is not None and self.target.object_type is ObjectType.station:
                self.move(*self.target.position)
                if self.in_radius_of_station(self.ship, self.target):
                    if self.material in self.ship.inventory:
                        self.sell_material(self.material, self.ship.inventory[self.material])

                    self.target = None

        # housekeeping -------------------------------------------------------------------------------------------------
        self.previous_hull = self.ship.current_hull

        # purchase module at center station
        if self.in_radius_of_station(self.ship, universe.get(ObjectType.secure_station)[0]):
            if self.ship.module_0_level is not ModuleLevel.two and self.ship.module_1_level is not ModuleLevel.two:
                buy = False
                module = ModuleType.empty
                level = ModuleLevel.base
                slot = ShipSlot.zero
                if self.ship.module_0 is ModuleType.empty:
                    module = random.choice([ModuleType.hull, ModuleType.engine_speed])
                    slot = ShipSlot.zero
                    buy = True
                elif self.ship.module_1 is ModuleType.locked:
                    buy = False
                elif self.ship.module_1 is ModuleType.empty:
                    module = random.choice([ModuleType.cargo_and_mining, ModuleType.weapons])
                    slot = ShipSlot.one
                    buy = True
                else:
                    buy = True

                if self.ship.module_0_level is ModuleLevel.base:
                    level = ModuleLevel.one
                elif self.ship.module_1_level is ModuleLevel.base:
                    level = ModuleLevel.one
                elif self.ship.module_0_level is ModuleLevel.one:
                    module = self.ship.module_0
                    level = ModuleLevel.two
                    slot = ShipSlot.zero
                elif self.ship.module_1_level is ModuleLevel.one:
                    module = self.ship.module_1
                    level = ModuleLevel.two
                    slot = ShipSlot.one

                if buy:
                    self.buy_module(module, level, slot)
                else:
                    self.unlock_module()

        # health purchasing
        if self.ship.current_hull < 0.3 * self.ship.max_hull:
            self.move(*universe.get(ObjectType.secure_station)[0].position)
            self.repair(self.ship.max_hull - self.ship.current_hull)

        return self.action_digest()

    def clear_variables(self):
        self.action = None
        self.target = None

        self.counter = 0

        self.material = None

        self.purchased = None
