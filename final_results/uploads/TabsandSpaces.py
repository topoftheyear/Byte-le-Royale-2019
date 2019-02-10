import random

from game.client.user_client import UserClient
from game.common.enums import *

class CustomClient(UserClient):


    def __init__(self):
        """ Use the constructor to initialize any variables you would like to track between turns. """
        self.purchase_station = None
        self.sell_station = None
        self.destination = None
        self.material = None
        #self.prevHull = current_hull
        self.isInBuySellCycle = False
        self.currentCycle = None
        self.goingToFirstLocation = False
        self.atFirstLocation = False
        self.goingToSecondLocation = False
        self.atSecondLocation = False
        self.tickNumber = 0
        self.mineTime = 120
        self.isStartOfRound = True
        self.currentIteration = 0
        self.varThatFixesBuyProblem = False
        
        self.debug = False

    def team_name(self):
        print("Sending Team Name")
        return "Tabs vs Spaces" #Our ship name should be "The Noether"

    def team_color(self):
        print("Sending Team Color")

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [127, 161, 216]
        
    """def defend():
        #if the ship is being attacked, fire back unless on a shop, in which case sell
        if(prevHull > currentHull) and self.position()!=:
            ship_to_attack = self.in_attack_range(universe)
            self.attack(ship_to_attack) #TODO: Actually attack the bad guy
            self.move(universe.get(ObjectType.secure_station))
        #if the ship's hull falls to less than 10%, repair hull
        elif(currentHull < (max_hull/10)):
            self.move(universe.get(ObjectType.secure_station))
            self.repair(max_hull/2)
        #if the attacker is more powerful, run to secure station
    
    def updatePrevHull():
        prevHull = current_hull"""
        

    def take_turn(self, ship, universe):
        self.update_cached_data(universe)
        self.tickNumber = self.tickNumber + 1
        if self.currentIteration == 6:
            correctLocation = None
            distance1 = 0
            distance2 = 0
            blackMarkets = universe.get(ObjectType.black_market_station)
            distance1 = self.distance_to_object(ship, blackMarkets[0])
            distance2 = self.distance_to_object(ship, blackMarkets[1])   
            if distance1 > distance2:
                correctLocation = blackMarkets[1]
            else:
                correctLocation = blackMarkets[0]
            self.move(correctLocation.position[0],correctLocation.position[1])
            if self.in_radius_of_station(ship, correctLocation) is True:
                self.currentIteration = 7
                print(self.get_module_price(ModuleLevel.one))
                self.buy_module(ModuleType.engine_speed, 1, ShipSlot.zero)
        elif self.currentIteration == 30:
            correctLocation = None
            distance1 = 0
            distance2 = 0
            blackMarkets = universe.get(ObjectType.black_market_station)
            distance1 = self.distance_to_object(ship, blackMarkets[0])
            distance2 = self.distance_to_object(ship, blackMarkets[1])   
            if distance1 > distance2:
                correctLocation = blackMarkets[1]
            else:
                correctLocation = blackMarkets[0]
            self.move(correctLocation.position[0],correctLocation.position[1])
            if self.in_radius_of_station(ship, correctLocation) is True:
                self.currentIteration = 31
                self.buy_module(ModuleType.engine_speed, 2, ShipSlot.zero)
        elif not self.isInBuySellCycle:
            optionsTree = self.makePriorityTree(ship, universe)
            options = self.traversePriorityTree(ship, universe, optionsTree)
            currentBest = pathOption(None, None, 0)
            for option in options:
                if option.quality > currentBest.quality:
                    currentBest = option
            self.currentCycle = currentBest
            print(" ----------------- BEST OPTION -------------- Buy/Mine: " + currentBest.firstLocation.name + " Sell: " + currentBest.secondLocation.name + " Quality: " + str(currentBest.quality) + " REVENUE: " + str(currentBest.totalRev) + " TURNS: " + str(currentBest.totalTurns) + " CURRENT WEALTH: " + str(ship.credits))
            self.isInBuySellCycle = True
            self.goingToFirstLocation = True
            if self.currentCycle.firstLocation.object_type is ObjectType.station:
                self.material = self.currentCycle.firstLocation.production_material
            elif self.currentCycle.firstLocation.object_type is ObjectType.goethite_field or self.currentCycle.firstLocation.object_type is ObjectType.cuprite_field or self.currentCycle.firstLocation.object_type is ObjectType.gold_field:
                self.material = self.currentCycle.firstLocation.material_type
        self.followBuySellCycle(ship, universe)
        if self.isStartOfRound is True:
            self.isStartOfRound = False
            self.buy_module(ModuleType.engine_speed, 1, ShipSlot.zero)


    def followBuySellCycle(self, ship, universe):
        if self.goingToFirstLocation is True:
            self.move(self.currentCycle.firstLocation.position[0],self.currentCycle.firstLocation.position[1])
            if self.currentCycle.firstLocation.object_type is ObjectType.station:
                if self.in_radius_of_station(ship, self.currentCycle.firstLocation) is True:
                    self.buy_material(min(self.currentCycle.firstLocation.cargo[self.currentCycle.firstLocation.production_material] - 1, (ship.credits/self.currentCycle.firstLocation.sell_price) - 1))
                    for key in ship.inventory:
                        if int(self.material) == int(key):
                            self.goingToFirstLocation = False
                            self.atFirstLocation = True
            else:
                self.mine()
                if self.material in ship.inventory and ship.inventory[self.material] > 0:
                    self.goingToFirstLocation = False
                    self.atFirstLocation = True
        if self.atFirstLocation is True:
            self.move(self.currentCycle.firstLocation.position[0],self.currentCycle.firstLocation.position[1])
            if self.currentCycle.firstLocation.object_type is ObjectType.station:
                self.buy_material(ship.cargo_space)
                d = " "
                for i in ship.inventory:
                    a=i
                    b=ship.inventory[i]
                    c=str(i)+":"+ str(ship.inventory[i])
                    d=d+c+'\n'
                print(".Buying: " + d + " Current Wealth: " + str(ship.credits))
                self.goingToSecondLocation = True
                self.atFirstLocation = False
            else:
                d = " "
                for i in ship.inventory:
                    a=i
                    b=ship.inventory[i]
                    c=str(i)+":"+ str(ship.inventory[i])
                    d=d+c+'\n'
                print(".Mining: " + d + " Current Wealth: " + str(ship.credits))
                self.mine()
                if self.material in ship.inventory and (ship.inventory[self.material] >= (self.mineTime)) or (ship.inventory[self.material] >= self.currentCycle.secondLocation.production_max):
                    self.goingToSecondLocation = True
                    self.atFirstLocation = False
        if self.goingToSecondLocation is True:
            self.move(self.currentCycle.secondLocation.position[0],self.currentCycle.secondLocation.position[1])
            if self.in_radius_of_station(ship, self.currentCycle.secondLocation) is True:
                print(ship.inventory)
                print(self.material)
                self.sell_material(self.material, 500)
                self.goingToSecondLocation = False
                self.atSecondLocation = True
        if self.atSecondLocation is True:
            self.sell_material(self.material, 500)
            d = " "
            for i in ship.inventory:
                a=i
                b=ship.inventory[i]
                c=str(i)+":"+ str(ship.inventory[i])
                d=d+c+'\n'
                print(".Selling: " + d + " Current Wealth: " + str(ship.credits))
                self.atSecondLocation = False
                self.isInBuySellCycle = False
                self.varThatFixesBuyProblem = False
                self.currentIteration = self.currentIteration + 1


            # If we sold it, then we completed our task

                
                        

    def makePriorityTree(self, ship, universe):
        stations = []
        mines = []
        #Step one: Declare ship root
        root = Node(ship)
        #Step two: Declare all mines and selling stores children of root, set path length to distance between ship and mine/shop, set price to 0 for mine, unit price for store
        for obj in universe.get(ObjectType.station):
            if obj.object_type is ObjectType.station and obj.object_type not in [ObjectType.secure_station, ObjectType.black_market_station]:
                stations.append(obj)
        for obj in universe.get(ObjectType.goethite_field):
            mines.append(obj)
        for obj in universe.get(ObjectType.cuprite_field):
            mines.append(obj)
        for obj in universe.get(ObjectType.gold_field):
            mines.append(obj)
        placesToBuy = stations + mines
        for location in placesToBuy:
                root.insert(location)
        #Step three: Declare all shops buying from corresponding store/mine children of mine, set path length to distance between mine/shop and shop, set profit to unit price for store
        for buyNode in root.children:
            for obj in universe.get(ObjectType.station):
                if obj.object_type is ObjectType.station and obj.object_type not in [ObjectType.secure_station, ObjectType.black_market_station]:
                    buyNode.insert(obj)
        #Step four: Return this tree, another method will traverse it
        return root
        #Note: Use different method if storage capacity is full

    #TODO: Include secondary buying products
    def traversePriorityTree(self, ship, universe, priorityTree):
        #Step one: Find the path in which (revenue - cost) / ((travel time / speed) +1) is greatest
        pathOptions = []
        for buyLocation in priorityTree.children:
            for sellLocation in buyLocation.children:
                totalTurns = (self.distance_to_object(ship, buyLocation.data) / ship.engine_speed) + 2 + (self.distance_to_object(buyLocation.data, sellLocation.data) / ship.engine_speed)
                totalRev = 0
                if buyLocation.data.object_type is ObjectType.station:
                    howManyWeCanBuy = ship.credits / buyLocation.data.sell_price
                    totalRev = sellLocation.data.primary_buy_price * min(buyLocation.data.cargo[buyLocation.data.production_material] - 1, sellLocation.data.primary_max, howManyWeCanBuy)
                    totalRev = totalRev - (buyLocation.data.sell_price * min(buyLocation.data.cargo[buyLocation.data.production_material], sellLocation.data.primary_max, howManyWeCanBuy))
                    if (totalTurns > 250) or totalTurns > (19500 - self.tickNumber):
                        totalRev = 0
                    if buyLocation.data.production_material is sellLocation.data.primary_import:
                        pathOptions.append(pathOption(buyLocation.data, sellLocation.data, totalRev / totalTurns, totalRev, totalTurns))
                if buyLocation.data.object_type is ObjectType.goethite_field or buyLocation.data.object_type is ObjectType.cuprite_field or buyLocation.data.object_type is ObjectType.gold_field:
                    totalTurns = totalTurns + (self.mineTime / (buyLocation.data.mining_rate * ship.mining_yield))
                    totalRev = (self.mineTime / (buyLocation.data.mining_rate * ship.mining_yield)) * sellLocation.data.primary_buy_price
                    if buyLocation.data.material_type is sellLocation.data.primary_import:
                        pathOptions.append(pathOption(buyLocation.data, sellLocation.data, totalRev / totalTurns, totalRev, totalTurns))
        #Step two: Return the object to immediately travel to / use 
        for path in pathOptions:
            print("Buy/Mine: " + path.firstLocation.name + " Sell: " + path.secondLocation.name + " Quality: " + str(path.quality))
        return pathOptions
    
class pathOption:

    def __init__(self, firstLocation, secondLocation, quality, totalRev = None, totalTurns = None):
        self.firstLocation = firstLocation
        self.secondLocation = secondLocation
        self.quality = quality
        self.totalRev = totalRev
        self.totalTurns = totalTurns

class Node:

  def __init__(self, data):
    self.children = []
    self.data = data

  def PrintTree(self):
    print(self.data)

  def insert(self, data):
    self.children.append(Node(data))