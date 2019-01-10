import random

from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *
from game.utils.helpers import *

class TestTraderNPC(NPC):

    def __init__(self, ship):
        UserClient.__init__(self)
        self.ship = ship
        self.ship_id = ship.id

        self.heading = None
        self.action = 0
        self.material = None

    def take_turn(self, universe):

        stations = universe.get(ObjectType.station)
        sellPrices = get_material_prices(universe)
        buyPrices = get_material_buy_prices(universe)

        firstBuy = 0
        firstSell = 0
        firstHighest = 0
        firstMaterial = ""

        secondBuy = 0
        secondSell = 0
        secondHighest = 0
        secondMaterial = ""

        thirdBuy = 0
        thirdSell = 0
        thirdHighest = 0
        thirdMaterial = ""

        chosenSell = 0
        chosenBuy = 0
        chosenPrice = 0
        chosenMaterial = ""
        chosenSellStation = None
        chosenBuyStation = None

        if self.action is 0:
            for key,sellPrice in sellPrices.items():
                if key not in buyPrices:
                    continue
                buyPrice = buyPrices[key]
                difference = buyPrice - sellPrice

                if difference > firstHighest:
                    thirdHighest = secondHighest
                    secondHighest = firstHighest
                    firstHighest = difference

                    thirdMaterial = secondMaterial
                    secondMaterial = firstMaterial
                    firstMaterial = key

                    thirdBuy = secondBuy
                    secondBuy = firstBuy
                    firstBuy = buyPrice

                    thirdSell = secondSell
                    secondSell = firstSell
                    firstSell = sellPrice
                elif difference > secondHighest:
                    thirdHighest = secondHighest
                    secondHighest = difference

                    thirdMaterial = secondMaterial
                    secondMaterial = key

                    thirdBuy = secondBuy
                    secondBuy = buyPrice

                    thirdSell = secondSell
                    secondSell = sellPrice
                elif difference > thirdHighest:
                    thirdHighest = difference

                    thirdMaterial = key

                    thirdBuy = buyPrice

                    thirdSell = sellPrice

            rand = random.choice([1,2,3])
            if rand == 1:
                chosenPrice = firstHighest
                chosenMaterial = firstMaterial
                chosenSell = firstSell
                chosenBuy = firstBuy
            elif rand == 2:
                chosenPrice = secondHighest
                chosenMaterial = secondMaterial
                chosenSell = secondSell
                chosenBuy = secondBuy
            if rand == 3:
                chosenPrice = thirdHighest
                chosenMaterial = thirdMaterial
                chosenSell = thirdSell
                chosenBuy = thirdBuy

            for tempStation in stations:
                if tempStation.primary_buy_price == chosenSell and tempStation.primary_import == chosenMaterial:
                    chosenSellStation = tempStation
                elif tempStation.secondary_buy_price == chosenSell and tempStation.secondary_import == chosenMaterial:
                    chosenSellStation = tempStation

                if tempStation.sell_price == chosenBuy and tempStation.production_material == chosenMaterial:
                    chosenBuyStation = tempStation
            self.sellStation = chosenSellStation.position
            self.buyStation = chosenBuyStation.position
            self.material = chosenMaterial

            self.action = 1
            self.heading = self.buyStation

        elif self.action == 1:  # buying
            self.heading = self.buyStation
            # Gather as much of the material determined as possible
            if self.heading[0] == self.ship.position[0] and self.heading[1] == self.ship.position[1]:
                self.buy_material(self.ship.cargo_space)

            if self.material in self.ship.inventory and self.ship.inventory[self.material] > 0:
                self.action = 2
                self.heading = self.sellStation

        elif self.action == 2:  # selling
            self.heading = self.sellStation
            # Sell material when possible
            self.sell_material(self.material, self.ship.inventory[self.material])

            if self.ship.inventory[self.material] == 0:
                self.action == 0

        # move towards heading
        self.move(*self.heading)

        # if at heading, clear heading
        if self.heading[0] == self.ship.position[0] and self.heading[1] == self.ship.position[1]:
            if self.action == 1:
                self.action = 2
                self.heading = self.sellStation
            if self.action == 2:
                self.action = None
                self.heading = None



        return self.action_digest()


    # Compile top 3 most profitable materials
    # Pick 1 randomly
    # Move to station and purchase as much as possible
    # Move to selling station and sell it
    # Repeat

