import random

from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *
from game.utils.helpers import *

class TestTraderNPC(NPC):
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
        chosenSellStation = ""
        chosenBuyStation = ""

        if self.action is None:
            for key,sellPrice in sellPrices.items():
                if key not in buyPrices:
                    continue
                buyPrice = buyPrices[key]
                difference = buyPrice - sellPrice

                if difference > firstHighest:
                    thirdHighest = secondHighest
                    secondHighest = firstHighest
                    firstHighest = difference

                    thirdMaterial = secondHighest
                    secondMaterial = firstHighest
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

                    thirdMaterial = secondHighest
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
                chosenbuy = firstBuy
            elif rand == 2:
                chosenPrice = secondHighest
                chosenMaterial = secondMaterial
                chosenSell = secondSell
                chosenbuy = secondBuy
            if rand == 3:
                chosenPrice = thirdHighest
                chosenMaterial = thirdMaterial
                chosenSell = thirdSell
                chosenbuy = thirdBuy

            for tempStation in stations:
                if tempStation.primary_buy_price == chosenSell and tempStation.primary_import == chosenMaterial:
                    chosenSellStation = tempStation
                elif tempStation.secondary_buy_price == chosenSell and tempStation.secondary_import == chosenMaterial:
                    chosenSellStation = tempStation

                if tempStation.sell_price == chosenBuy and tempStation.production_material == chosenMaterial:
                    chosenSellStation = tempStation
            self.sellStation = chosenSellStation
            self.buyStation = chosenBuyStation

            self.action = 1
            self.heading = self.buyStation

        elif self.action == 1:  # buying
            self.heading = self.buyStation
            # Gather as much of the material determined as possible
            self.buy_material(chosenMaterial, self.ship.cargo_space)

            if self.ship.inventory[chosenMaterial] > 0:
                self.action = 2

        elif self.action == 2:  # selling
            self.heading = self.sellStation
            # Sell material when possible
            self.sell_material(chosenMaterial, self.ship.inventory[chosenMaterial])

            if self.ship.inventory[chosenMaterial] == 0:
                self.action == 0
        # choose a new heading if we don't have one
            self.heading = random.choice(universe.get("asteroid_fields")).position

        # move towards heading
        self.move(*self.heading)

        # if at heading, clear heading
        if self.heading[0] == self.ship.position[0] and self.heading[1] == self.ship.position[1]:
            self.heading = None



        return self.action_digest()


    # Compile top 3 most profitable materials
    # Pick 1 randomly
    # Move to station and purchase as much as possible
    # Move to selling station and sell it
    # Repeat

