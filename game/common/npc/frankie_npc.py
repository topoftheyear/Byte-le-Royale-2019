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
        self.name = "FrankieNPC"
        self.ship = ship
        self.ship_id = ship.id

        self.transaction = None
        self.target = None

        self.fields = None
        self.stations = None

    def team_name(self):
        return f"FrankieNPC"

    def take_turn(self, universe):
        # initialize empty variables
        if self.fields is None:
            self.fields = universe.get("asteroid_fields")
        if self.stations is None:
            self.stations = universe.get("stations")

        # select new action if not currently in one
        if self.transaction is None:
            self.transaction = random.choice(["mine", "mine", "trade", "trade", "trade", "pirate", "module"])

        prices = get_best_material_prices(universe)
        # mining action
        if self.transaction is "mine":
            if self.target is None:
                self.target = random.choice(self.fields)

            if self.target in self.fields:
                self.mine()
                self.move(*self.target.position)

                if sum(self.ship.inventory.values()) >= self.ship.cargo_space:
                    prices = get_best_material_prices(universe)

                    self.target = prices["best_import_prices"][self.target.material_type]["station"]


            elif self.target.object_type is ObjectType.station:
                pass

        # trade action
        elif self.transaction is "trade":
            pass
        # pirate action
        elif self.transaction is "pirate":
            pass
        # module action
        elif self.transaction is "module":
            pass


        return self.action_digest()
