import random

from game.common.enums import *
from game.common.npc.npc import NPC
from game.utils.helpers import *
from game.client.user_client import UserClient
from game.config import *
import game.utils.filters as F


class ArnaldoNPC(NPC):

    # Set up the system.
    def __init__(self, ship):
        UserClient.__init__(self)
        self.name = "ArnaldoNPC"
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
        self.action_choices = ["mine", "module", "pirate", "trade"]
        self.module_choices = [ModuleType.cargo_and_mining, ModuleType.engine_speed,
                                               ModuleType.hull, ModuleType.weapons]
        self.other_ships = None
        # These will expand as time goes on
        self.next_locked_slot = ShipSlot.one
        self.next_module_level = 1
        self.next_module_price = 0
        self.get_module = False
        self.get_trade = False
    def team_name(self):
        return f"{self.name}#{random.randint(1,1000)}"

    def take_turn(self, universe):
        # initialize empty variables
        if self.fields is None:
            self.fields = universe.get("asteroid_fields")
        if self.stations is None:
            self.stations = universe.get(ObjectType.station)
        self.other_ships = ships_in_attack_range(universe, self.ship)
        self.next_module_price = int(get_module_price(get_median_material_price(get_material_sell_prices(universe)), self.next_module_level))

        # select new action if not currently in one
        if self.action is None:
            if self.get_module:
                self.action = "module"
            elif self.get_trade:
                self.action = "trade"
            else:
                self.action = "mine"

        # mining action ------------------------------------------------------------------------------------------------
        if self.action is "mine":
            # Start off by mining. This is the base state we will have.

            # If we can afford a module, get an upgrade
            if self.next_module_price < self.ship.credits:
                self.action = "module"
            # if not, attempt to take prey on nearby weakened ships
            else:
                # Sets a ship as the target if less health
                for otherShip in self.other_ships:
                    if otherShip.current_hull < self.ship.current_hull:
                        self.action = "pirate"
                # if there is no suitable ships to pirate, then mine enough to begin trading
                if self.action is not "pirate":
                    if self.target is None:
                        self.target = random.choice(self.fields)
                        self.material = self.target.material_type
                    # if we have a field to mine from, go to it and mine until inventory is full
                    if self.target in self.fields:
                        self.mine()
                        self.move(*self.target.position)
                    # When inventory is full, sell it at the best place
                    if sum(self.ship.inventory.values()) >= self.ship.cargo_space * 0.9:
                        if self.target.object_type is not ObjectType.station:
                            for thing, amount in self.ship.inventory.items():
                                if amount <= 0:
                                    continue
                                self.material = thing
                                prices = get_best_material_prices(universe)
                                self.target = prices["best_import_prices"][self.material]["station"]
                                break
                # If a target exists, move there and attempt to sell
                if self.target is not None and self.material is not None:
                    self.move(*self.target.position)

                    if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e:e.position):
                        self.sell_material(self.material, self.ship.inventory[self.material])
                        self.target = self.ship
                # if still broke, keep mining
                if self.ship.credits <= 100:
                    self.action = "mine"

        # Yarr harr, pirate here
        if self.action is "pirate":

            # Who's next on the chopping block?
            if self.target is None:
                self.target = random.choice(self.other_ships)

            # if we have a target, pursue only while we are healthier and they are alive.
            elif self.target.object_type is ObjectType.ship:
                if self.ship.current_hull >= self.target.current_hull > 0:
                    self.move(*self.target.position)
                    self.attack(self.target)
                elif self.target.current_hull <= 0:  # Target dead

                    # the more ships nearby, the less likely to gather scrap
                    self.next_list = ["gather", "gather"]
                    for other_ship in self.other_ships:
                        if other_ship.current_hull > 0:
                            self.next_list.append("no gather")
                    # if chooses to gather, get scrap, otherwise go back to pirating
                    if random.choice(self.next_list) is "gather":
                        scrap_list = universe.get(ObjectType.illegal_salvage)
                        distance_list = [distance_to(self.ship, x, lambda e:e.position) for x in scrap_list]
                        self.target = scrap_list[distance_list.index(min(distance_list))]
                        self.move(*self.target.position)
                        self.collect_illegal_salvage()
            # Raid their salvage, they didn't want it anyways
            elif self.target.object_type is ObjectType.illegal_salvage:
                if self.target.amount <= 1 or sum(self.ship.inventory.values()) >= self.ship.cargo_space:
                    # collected enough
                    market_list = universe.get(ObjectType.black_market_station)
                    distance_list = [distance_to(self.ship, x, lambda e: e.position) for x in market_list]

                    self.target = market_list[distance_list.index(random.choice(distance_list))]
            # Made our profit, now to earn it
            elif self.target.object_type is ObjectType.black_market_station:
                self.move(*self.target.position)
                if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e: e.position):
                    self.sell_salvage()

                    # If successful: try to get an upgrade next turn; if not, try to trade, else, mine
                    if self.next_module_price < self.ship.credits:
                        self.get_module = True
                    elif self.ship.credits > 100:
                        self.get_trade = True
                    else:
                        self.action = None

        # module action ------------------------------------------------------------------------------------------------
        if self.action is "module":
            # determine if a relevant module can be purchased
            if self.target is None:
                # decide on what module to get
                self.type = None
                # if we can afford to upgrade, upgrade. Otherwise, unlock a slot
                self.module_unlock_price = get_module_unlock_price(get_median_material_price(get_material_sell_prices(universe)), self.next_locked_slot)
                if self.ship.module_0 is not ModuleType.empty:
                    # if we can afford to get a new slot AND no slots are empty, we will get the new slot
                    if self.ship.module_1 == ModuleType.locked:
                        if self.ship.credits - self.module_unlock_price > 100:
                            self.unlock_module()
                            self.next_locked_slot = ShipSlot.one
                    elif self.ship.module_1 is not ModuleType.empty and self.ship.module_2 == ModuleType.locked:
                        if self.ship.credits - self.module_unlock_price > 200:
                            self.unlock_module()
                            self.next_locked_slot = ShipSlot.two
                    elif self.ship.module_2 is not ModuleType.empty and self.ship.module_3 == ModuleType.locked:
                        if self.ship.credits - self.module_unlock_price > 400:
                            self.unlock_module()
                            self.next_locked_slot = ShipSlot.zero # Done unlocking
                else:
                    self.type = random.choice(self.module_choices)
                # if we have a type of module to get, get it
                if self.type is not None:
                    # check if it is within budget
                    if self.ship.credits - 100 > self.next_module_price:
                        self.target = universe.get(ObjectType.secure_station)[0]
                    else:
                        self.action = None
                # otherwise, fall through to try and buy
                else:
                    self.action = None

            # go out and buy the module
            else:
                self.move(*self.target.position)
                if self.ship.module_0 is ModuleType.empty and self.ship.module_0_level <= 0:
                    self.buy_module(self.type, self.next_module_level, ShipSlot.zero)
                if self.ship.module_1 is ModuleType.empty and self.ship.module_0_level <= 0:
                    self.buy_module(self.type, self.next_module_level, ShipSlot.one)
                if self.ship.module_2 is ModuleType.empty and self.ship.module_0_level <= 0:
                    self.buy_module(self.type, self.next_module_level, ShipSlot.two)
                if self.ship.module_3 is ModuleType.empty and self.ship.module_0_level <= 0:
                    self.buy_module(self.type, self.next_module_level, ShipSlot.three)
                else:
                    # module action has been fulfilled
                    self.action = None
                    self.target = None

        # trade action -------------------------------------------------------------------------------------------------
        elif self.action is "trade":
            # if we don't have a station to buy from, pick one
            if self.target is None:
                while True:
                    self.target = random.choice(self.stations)
                    if self.target.object_type not in [ObjectType.black_market_station,
                                                       ObjectType.secure_station]:
                        break
                self.material = self.target.production_material

            # Buy as much as we can.
            elif sum(self.ship.inventory.values()) <= 0:
                self.move(*self.target.position)
                if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e: e.position):
                    self.buy_material(math.floor(self.ship.credits / self.target.sell_price))

                    # Find who will buy it
                    prices = get_best_material_prices(universe)
                    self.target = prices["best_import_prices"][self.material]["station"]

            # otherwise, sell all materials in the inventory
            elif self.target in self.stations:
                self.move(*self.target.position)
                if in_radius(self.ship, self.target, self.target.accessibility_radius, lambda e: e.position):
                    if self.material in self.ship.inventory:
                        self.sell_material(self.material, self.ship.inventory[self.material])

                if self.material not in self.ship.inventory or self.ship.inventory[self.material] <= 0:
                    # trade action has been fulfilled
                    self.action = None
                    self.target = None
                    self.material = None

        # override actions----------------------------------------------------------------------------------------------
        # healing
        if self.ship.current_hull / self.ship.max_hull <= 0.3:
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
