import random
import sys

from game.common.enums import *
from game.client.user_client import UserClient
from game.common.npc.npc import NPC
from game.config import *
from game.utils.helpers import *

class TestPriorityTraderNPC(NPC):
    # NPC that will take the top 3 current most profitable materials, select one, then go buy as much of it as possible and go to sell it
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
            for key,sellPrice in sellPrices.items():
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
                rand = random.choice([1,2])
            else:
                rand = random.choice([1,2,3])

            if rand == 1:
                chosenMaterial = firstMaterial
            elif rand == 2:
                chosenMaterial = secondMaterial
            elif rand == 3:
                chosenMaterial = thirdMaterial


            for tempStation in stations:
                if tempStation.primary_import == chosenMaterial:
                    if chosenSellStation is None:
                        chosenSellStation = tempStation
                    elif chosenSellStation.primary_import == chosenMaterial and chosenSellStation.primary_buy_price < tempStation.primary_buy_price:
                        chosenSellStation = tempStation
                    elif chosenSellStation.secondary_import == chosenMaterial and chosenSellStation.secondary_buy_price < tempStation.primary_buy_price:
                        chosenSellStation = tempStation
                elif tempStation.secondary_import == chosenMaterial:
                    if chosenSellStation is None:
                        chosenSellStation = tempStation
                    elif chosenSellStation.primary_import == chosenMaterial and chosenSellStation.primary_buy_price < tempStation.secondary_buy_price:
                        chosenSellStation = tempStation
                    elif chosenSellStation.secondary_import == chosenMaterial and chosenSellStation.secondary_buy_price < tempStation.secondary_buy_price:
                        chosenSellStation = tempStation

                if tempStation.production_material == chosenMaterial:
                    chosenBuyStation = tempStation

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

