import random
import sys

from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *
from game.utils.helpers import *

class TestTraderNPC(NPC):
    # NPC will choose a random trade material, buy as much of it as possible, then go to sell it
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
        sellPrices = get_material_sell_prices(universe)
        buyPrices = get_material_buy_prices(universe)
        trade_materials = [MaterialType.iron, MaterialType.steel, MaterialType.circuitry, MaterialType.computers, MaterialType.weaponry,
                           MaterialType.copper, MaterialType.drones, MaterialType.pylons, MaterialType.wire, MaterialType.machinery]

        firstHighest = 0
        firstMaterial = ""

        secondHighest = 0
        secondMaterial = ""

        thirdHighest = 0
        thirdMaterial = ""

        chosenMaterial = None
        chosenSellStation = None
        chosenBuyStation = None

        if self.doing is 0:
            self.heading = self.ship.position
            for key, sellPrice in sellPrices.items():
                if key not in trade_materials:
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
                elif difference > secondHighest:
                    thirdHighest = secondHighest
                    secondHighest = difference

                    thirdMaterial = secondMaterial
                    secondMaterial = key
                elif difference > thirdHighest:
                    thirdHighest = difference

                    thirdMaterial = key

            if firstMaterial == "":
                chosenMaterial = 9
                rand = 0
                print("No ideal material")
            elif secondMaterial == "":
                rand = 1
            elif thirdMaterial == "":
                rand = random.choice([1, 2])
            else:
                rand = random.choice([1, 2, 3])

            if rand == 1:
                chosenMaterial = firstMaterial
            elif rand == 2:
                chosenMaterial = secondMaterial
            elif rand == 3:
                chosenMaterial = thirdMaterial

            done = False
            while not done:
                chosenMaterial = random.choice(trade_materials)
                sell = False
                for tempStation in stations:
                    if (tempStation.primary_import == chosenMaterial or tempStation.secondary_import == chosenMaterial) and not sell:
                        chosenSellStation = tempStation
                        sell = True
                        break
                if sell is True:
                    for tempStation in stations:
                        if tempStation.production_material == chosenMaterial:
                            chosenBuyStation = tempStation
                            done = True
                            break

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
            self.bStation = chosenBuyStation
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
                # self.print("Action 1: Ship Bought: " + str(self.ship.inventory[self.material]) + " " + str(self.material))

        elif self.doing == 2:  # selling
            if self.material not in self.ship.inventory:
                self.doing = 0
                self.heading = self.ship.position
            else:
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

