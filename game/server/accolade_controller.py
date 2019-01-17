import sys
import math

from game.common.enums import *
from game.common.stats import *
from game.common.name_helpers import *
from game.common.asteroid_field import AsteroidField
from game.common.ship import Ship
from game.server.bounty_controller import *

class AccoladeController:

    __instance = None

    def __init__(self):

        if AccoladeController.__instance != None:
            print("AccoladeController is a singleton and has already been instanciated. Use AccoladeController.get_instance() to get instance of class")
        else:
            AccoladeController.__instance = self

        self.debug = False
        self.events = []
        self.stats = []
        self.ore = dict()
        self.bounties = dict()
        self.scrap = dict()
        self.salvage = dict()
        self.credits = dict() #credits earned NOT salvage
        self.moved = dict()
        self.upgrades = dict()



    @staticmethod
    def get_instance():
        if AccoladeController.__instance == None:
            AccoladeController()
        return AccoladeController.__instance

    def get_events(self):
        e = self.events
        self.events = []
        return e

    def get_stats(self):
        s = self.stats
        self.stats = []
        return s

    def print(self, msg):
        if self.debug:
            print("Accolade Controller:" + str(msg))
            sys.stdout.flush()

    # Ore Mined
    def ore_mined(self, ship, oreAdd):
        if ship in self.ore:
            self.ore[ship] += oreAdd
        else:
            self.ore[ship] = oreAdd

    def most_ore_mined(self):
        most = -1
        ship = ""
        for x in self.ore:
            if self.ore[x] > most:
                most = self.ore[x]
                ship = x

        return [ship, most]

    # Bounties claimed
    def bounty_claim(self, ship):
        if ship in self.bounties:
            self.bounties[ship] += 1
        else:
            self.bounties[ship] = 1
            
    def most_bounties_claimed(self):
        most = -1
        ship = ""
        for x in self.bounties:
            if self.bounties[x] > most:
                most = self.bounties[x]
                ship = x

        return [ship, most]

    # How much salavge redeemed
    def redeem_salvage(self, ship, salvageAdd):
        if ship in self.salvage:
            self.salvage[ship] += salvageAdd
        else:
            self.salvage[ship] = salvageAdd

    def most_salvage_redeemed(self):
        most = -1
        ship = ""
        for x in self.salvage:
            if self.salvage[x] > most:
                most = self.salvage[x]
                ship = x

        return [ship, most]

    # credits not from salvage
    def credits_earned(self, ship, creditAdd):
        if ship in self.credits:
            self.credits[ship] += creditAdd
        else:
            self.credits[ship] = creditAdd

    def most_credits_earned(self):
        most = -1
        ship = ""
        for x in self.credits:
            if self.credits[x] > most:
                most = self.credits[x]
                ship = x

        return [ship, most]

    # Fuel Efficient
    def ship_moved(self, ship, distance):
        if ship in self.ore:
            self.ore[ship] += distance
        else:
            self.ore[ship] = distance

    def ships_credits(self, ship):
        max_efficient = -1
        ship_efficient = {}
        for x in ship:
            if ship.credits / self.moved[x] > max_efficient:
                ship_efficient = x

        return [ship_efficient, max_efficient]

    # Ship Upgrades
    def ship_upgraded(self, ship, cost):
        if ship in self.upgrades:
            self.upgrades[ship] += cost
        else:
            self.upgrades[ship] = cost

    def most_upgrades(self):
        most = -1
        ship = {}
        for x in self.upgrades:
            if self.upgrades[x] > most:
                ship = x
                most = self.upgrades[x]
        return [ship, most]
