import random

from game.common.enums import *
from game.common.npc.npc import NPC
from game.utils.helpers import *
from game.client.user_client import UserClient
from game.config import *
import game.utils.filters as F


class FrankieNPC(NPC):

    def __init__(self, ship):
        UserClient.__init__(self)
        self.ship = ship
        self.ship_id = ship.id

        self.action = None
        self.target = None
        self.material = None

        self.type = None
        self.level = None

        self.bought = False

        self.fields = None
        self.stations = None

        self.previous_position = None
        self.inactive_counter = 0

    def team_name(self):
        return f"FrankieNPC# {random.randint(1,1000)}"

    def take_turn(self, universe):
        # initialize empty variables
        if self.fields is None:
            self.fields = universe.get("asteroid_fields")
        if self.stations is None:
            self.stations = universe.get(ObjectType.station)

        # select new action if not currently in one
        if self.action is None:
            self.action = random.choice(["mine", "mine", "trade", "trade", "trade", "pirate", "module"])

        # mining action ------------------------------------------------------------------------------------------------
        if self.action is "mine":
            # if we don't have a field to mine from, pick one
            if self.target is None:
                self.target = random.choice(self.fields)
                self.material = self.target.material_type

            # if we have a field to mine from, go to it and mine until inventory is full
            elif self.target in self.fields:
                self.mine()
                self.move(*self.target.position)

                if sum(self.ship.inventory.values()) >= self.ship.cargo_space * 7 / 8:
                    self.target = universe.get(ObjectType.secure_station)[0]

            # if we have things in our inventory, sell them all
            elif sum(self.ship.inventory.values()) > 0:
                if self.target.object_type is not ObjectType.station:
                    for thing, amount in self.ship.inventory.items():
                        if amount <= 0:
                            continue
                        self.material = thing
                        prices = get_best_material_prices(universe)
                        self.target = prices["best_import_prices"][self.material]["station"]
                        break
                if self.target is not None:
                    self.move(*self.target.position)

                    if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e:e.position):
                        self.sell_material(self.material, self.ship.inventory[self.material])
                        self.target = self.ship

            elif sum(self.ship.inventory.values()) <= 0:
                # mining action has been fulfilled
                self.action = None
                self.target = None
                self.material = None

                if self.ship.credits <= 100:
                    self.action = "mine"

        # trade action -------------------------------------------------------------------------------------------------
        elif self.action is "trade":
            # if we don't have a station to buy from, pick one
            if self.target is None:
                while True:
                    self.target = random.choice(self.stations)
                    if self.target.object_type not in [ObjectType.black_market_station, ObjectType.secure_station]:
                        break
                self.material = self.target.production_material

            # if we have a station to buy from, go to it and purchase some
            elif not self.bought:
                self.move(*self.target.position)
                if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e:e.position):
                    self.buy_material(min(self.ship.cargo_space - sum(self.ship.inventory.values()),
                                          math.floor(self.ship.credits / self.target.sell_price)))
                    self.bought = True
                    self.target = universe.get(ObjectType.secure_station)[0]

            # once done, sell all materials in the inventory (just in case)
            elif sum(self.ship.inventory.values()) > 0:
                if self.target.object_type is not ObjectType.station:
                    for thing, amount in self.ship.inventory.items():
                        if amount <= 0:
                            continue
                        self.material = thing
                        prices = get_best_material_prices(universe)
                        self.target = prices["best_import_prices"][self.material]["station"]
                        break
                elif self.target.object_type is ObjectType.station:
                    self.move(*self.target.position)

                    if self.material in self.ship.inventory.keys():
                        if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e:e.position):
                            self.sell_material(self.material, self.ship.inventory[self.material])
                            self.target = self.ship
                    else:
                        self.target = self.ship

            elif sum(self.ship.inventory.values()) <= 0:
                # trade action has been fulfilled
                self.action = None
                self.target = None
                self.material = None

                self.bought = False

                if self.ship.credits <= 100:
                    self.action = "mine"

        # pirate action ------------------------------------------------------------------------------------------------
        elif self.action is "pirate":
            # if we don't have a target, pick a new sucker
            if self.target is None:
                self.target = random.choice(universe.get("ships"))

            # if we have a target, pursue and kill until dead
            elif self.target.object_type is ObjectType.ship:
                if self.target.current_hull > 0 or self.target.respawn_counter == -1:
                    self.move(*self.target.position)
                    self.attack(self.target)
                else:
                    # target is dead
                    scrap_list = universe.get(ObjectType.illegal_salvage)
                    distance_list = [distance_to(self.ship, x, lambda e:e.position) for x in scrap_list]

                    self.target = scrap_list[distance_list.index(min(distance_list))]

            # once the target has died, go and take their trash
            elif self.target.object_type is ObjectType.illegal_salvage:
                self.move(*self.target.position)
                self.collect_illegal_salvage()

                if self.target.amount <= 10 or sum(self.ship.inventory.values()) >= self.ship.cargo_space:
                    # collected enough
                    market_list = universe.get(ObjectType.black_market_station)
                    distance_list = [distance_to(self.ship, x, lambda e: e.position) for x in market_list]

                    self.target = market_list[distance_list.index(min(distance_list))]

            # once we have scrap, go and sell it at a black market
            elif self.target.object_type is ObjectType.black_market_station:
                self.move(*self.target.position)
                if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e:e.position):
                    self.sell_salvage()

                    # pirate action has been fulfilled
                    self.action = None
                    self.target = None
                    self.material = None

                    if self.ship.credits <= 100:
                        self.action = "mine"

        # module action ------------------------------------------------------------------------------------------------
        elif self.action is "module":
            # determine if a relevant module can be purchased
            if self.target is None:
                # decide on what module to get
                self.type = None
                if self.ship.module_0 is not ModuleType.empty:
                    self.type = self.ship.module_0
                else:
                    self.type = random.choice([ModuleType.cargo_and_mining, ModuleType.engine_speed,
                                               ModuleType.hull, ModuleType.weapons])

                # decide on upgrade level
                    self.level = None
                if self.ship.module_0_level is not ModuleLevel.illegal:
                    self.level = self.ship.module_0_level + 1
                else:
                    # maximum level reached, cannot buy a module
                    pass

                if self.type is not None or self.level is not None:
                    # check if it is within budget
                    price = get_module_price(get_median_material_price(get_material_sell_prices(universe)), self.level)
                    if self.ship.credits > price:
                        self.target = universe.get(ObjectType.secure_station)[0]
                    else:
                        self.action = None
                else:
                    self.action = None

            # go out and buy the module
            else:
                self.move(*self.target.position)
                if self.ship.module_0 is not self.type and self.ship.module_0_level is not self.level:
                    self.buy_module(self.type, self.level, ShipSlot.zero)
                else:
                    # module action has been fulfilled
                    self.action = None
                    self.target = None

                    if self.ship.credits <= 100:
                        self.action = "mine"

        # override actions----------------------------------------------------------------------------------------------
        # healing
        if self.ship.current_hull / self.ship.max_hull <= 0.25:
            self.move(*universe.get(ObjectType.secure_station)[0].position)
            self.repair(self.ship.max_hull - self.ship.current_hull)

        # if piracy has gotten out of hand
        if self.action != "pirate" and self.ship.notoriety > 5:
            self.move(*universe.get(ObjectType.secure_station)[0].position)
            self.pay_off_bounty()

        # inactive tracker
        if self.previous_position is not None and \
                self.ship.position[0] == self.previous_position[0] and \
                self.ship.position[1] == self.previous_position[1]:

            self.inactive_counter += 1

        self.previous_position = self.ship.position

        # if standing still too long, turn off and on again
        if self.inactive_counter >= 150:
            self.inactive_counter = 0

            self.action = None
            self.target = None
            self.material = None

            self.type = None
            self.level = None

            self.bought = False

            self.fields = None
            self.stations = None

        return self.action_digest()
