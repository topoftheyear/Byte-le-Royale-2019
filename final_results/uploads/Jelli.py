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
        self.ticker = 0
        self.turns = 0
        self.hugeAmount = 1000
        self.counter = 0
    
        self.debug = False

    def team_name(self):
        self.print("Sending Team Name")

        return "Jelli-"

    def team_color(self):
        self.print("Sending Team Color")

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [154, 50, 205]

    def take_turn(self, ship, universe):
        self.update_cached_data(universe)
        
        self.turns += 1 
        shipsInRange = []
        for obj in self.ships:
            shipsInRange.append(obj)
        
        if ship.current_hull <= 0:
            self.ticker = 0

        #This makes the ship mine while it is at the gold asteroid field
        if ship.position[0] == 850 and ship.position[1] == 595:
            self.mine()
            self.counter += 1

        #This method checks to see if there is gold in the ship before leaving to go sell the cargo
        if ship.position[0] == 850 and ship.position[1] == 595 and self.counter == 100:
            # if shipsInRange.count is not 0:
            #     self.attack(shipsInRange[0]) 
            self.ticker = 1
            self.counter = 0

        elif ship.position[0] == 900 and ship.position[1] == 266 and self.counter == 0:
            self.sell_material(MaterialType.gold, self.hugeAmount)
            
            self.counter = 1

        elif ship.position[0] == 900 and ship.position[1] == 266 and self.counter == 1:
            if self.turns >= 19500:
                self.sell_material(MaterialType.gold, self.hugeAmount)
                self.ticker = 2
            else:
                self.buy_material(self.hugeAmount)
            self.counter = 0
            self.ticker = 2

        elif ship.position[0] == 630 and ship.position[1] == 56 and self.counter == 0:
            self.sell_material(MaterialType.circuitry, self.hugeAmount)
            
            self.counter = 1

        elif ship.position[0] == 630 and ship.position[1] == 56 and self.counter == 1:
            if self.turns >= 19500:
                self.sell_material(MaterialType.circuitry, self.hugeAmount)
                self.ticker = 3
            else:
                self.buy_material(self.hugeAmount)
            self.counter = 0
            self.ticker = 3

        # elif ship.position[0] == 500 and ship.position[1] == 350 and self.ticker == 3:
        #     self.ticker = 4

        elif ship.position[0] == 150 and ship.position[1] == 406 and self.counter == 0:
            self.sell_material(MaterialType.computers, self.hugeAmount)
            self.counter = 1
        
        elif ship.position[0] == 150 and ship.position[1] == 406 and self.counter == 1:
            if self.turns >= 19500:
                self.sell_material(MaterialType.computers, self.hugeAmount)
                self.ticker = 4
            else:
                self.buy_material(self.hugeAmount)
            self.counter = 0
            self.ticker = 4

        elif ship.position[0] == 960 and ship.position[1] == 665 and self.counter == 0:
            self.sell_material(MaterialType.weaponry, self.hugeAmount)
            if self.turns >= 19500:
                self.sell_material(MaterialType.weaponry, self.hugeAmount)
                self.ticker = 1
            else:
                self.ticker = 0

        if self.ticker == 0:
            self.move(850,595)
        elif self.ticker == 1:
            self.move(900,266)
        elif self.ticker == 2:
            self.move(630,56)
        # elif self.ticker == 3:
        #     self.move(500,350)               
        elif self.ticker == 3:
            self.move(150,406)                    
        elif self.ticker == 4:
            self.move(960,665)

    def print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)