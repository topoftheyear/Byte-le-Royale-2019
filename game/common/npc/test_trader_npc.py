import random
import sys

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

        self.heading = ship.position
        self.doing = 0
        self.material = None
        self.debug = False

    def print(self, msg):
        if self.debug:
            print("Buy Sell Controller: " + str(msg))
            sys.stdout.flush()

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

        if self.doing is 0:
            self.heading = self.ship.position
            for key,sellPrice in sellPrices.items():
                if key is MaterialType.salvage:
                    continue
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

            # for tempStation in stations:
            #     if tempStation.primary_buy_price == chosenSell and tempStation.primary_import == chosenMaterial:
            #         chosenSellStation = tempStation
            #     elif tempStation.secondary_buy_price == chosenSell and tempStation.secondary_import == chosenMaterial:
            #         chosenSellStation = tempStation
            #
            #     if tempStation.sell_price == chosenBuy and tempStation.production_material == chosenMaterial:
            #         chosenBuyStation = tempStation
            done = False
            trade_materials = [MaterialType.iron, MaterialType.steel, MaterialType.circuitry, MaterialType.computers, MaterialType.weaponry, MaterialType.copper]
            while not done:
                chosenMaterial = random.choice(trade_materials)
                sell = False
                for tempStation in stations:
                    if tempStation.primary_import == chosenMaterial and not sell:
                        chosenSellStation = tempStation
                        sell = True
                        break
                if sell == True:
                    for tempStation in stations:
                        if tempStation.production_material == chosenMaterial:
                            chosenBuyStation = tempStation
                            done = True
                            break
                else:
                    continue

            # done = False
            # trade_materials = [MaterialType.iron, MaterialType.steel, MaterialType.circuitry, MaterialType.computers, MaterialType.weaponry, MaterialType.copper]
            # while not done:
            #     chosenMaterial = random.choice(trade_materials)
            #     buy_found = False
            #     for tempStation in stations:
            #         if tempStation.cargo[tempStation.production_material] == 0:
            #             if tempStation.production_material in trade_materials:
            #                 trade_materials.remove(tempStation.production_material)
            #                 chosenBuyStation = tempStation
            #             break
            #         if tempStation.production_material == chosenMaterial:
            #             chosenBuyStation = tempStation
            #             buy_found = True
            #             break
            #     for tempStation in stations:
            #         if tempStation.primary_import == chosenMaterial:
            #             chosenSellStation = tempStation
            #         if buy_found == True:
            #             done = True
            #             break
            #     if buy_found == False:
            #         if chosenMaterial in trade_materials:
            #             trade_materials.remove(chosenMaterial)
            #         if len(trade_materials) == 0:
            #             done = True
            #             print("EEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRR")

            self.sellStation = chosenSellStation.position
            self.buyStation = chosenBuyStation.position
            self.material = chosenMaterial
            self.print("Action 0:" + str(self.material) + ":" + str(self.sellStation) + ":" + str(self.buyStation))
            self.doing = 1
            self.heading = self.buyStation

        elif self.doing == 1:  # buying
            self.heading = self.buyStation
            self.buy_material(self.ship.cargo_space)
            # Gather as much of the material determined as possible
            if self.heading[0] == self.ship.position[0] and self.heading[1] == self.ship.position[1]:
                self.doing = 2
                self.heading = self.sellStation
                #self.print("Action 1: Ship Bought: " + str(self.ship.inventory[self.material]) + " " + str(self.material))


        elif self.doing == 2:  # selling
            self.heading = self.sellStation
            # Sell material when possible
            self.sell_material(self.material, self.ship.inventory[self.material])
            self.print("Action 2: ship has " + str(self.ship.inventory[self.material]) + " " + str(self.material))
            if self.ship.inventory[self.material] == 0 or (self.heading[0] == self.ship.position[0] and self.heading[1] == self.ship.position[1]):
                self.print("successfully sold")
                self.doing = 0
                self.heading = self.ship.position

        self.move(self.heading[0], self.heading[1])
        # move towards heading
        return self.action_digest()


    # Compile top 3 most profitable materials
    # Pick 1 randomly
    # Move to station and purchase as much as possible
    # Move to selling station and sell it
    # Repeat

