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

    # def attribute_accolade(self, ship, change_reason):
    #     change = 0
    #
    #     if ship.object_type == ObjectType.police or ship.object_type == ObjectType.enforcer:
    #         return
    #
    #     # evil deeds
    #     if change_reason is NotorietyChangeReason.destroy_civilian:
    #         ship.notoriety += GameStats.destroy_civilian
    #     elif change_reason is NotorietyChangeReason.destroy_bounty_hunter:
    #         ship.notoriety += GameStats.destroy_bounty_hunter
    #     elif change_reason is NotorietyChangeReason.destroy_police:
    #         ship.notoriety += GameStats.destroy_police
    #     elif change_reason is NotorietyChangeReason.destroy_enforcer:
    #         ship.notoriety += GameStats.destroy_enforcer
    #     elif change_reason is NotorietyChangeReason.carrying_illegal_module:
    #         ship.notoriety += GameStats.carrying_illegal_module
    #     elif change_reason is NotorietyChangeReason.attack_police:
    #         ship.notoriety += GameStats.attack_police
    #
    #     # good deeds
    #     elif change_reason is NotorietyChangeReason.destroy_pirate:
    #         ship.notoriety += GameStats.destroy_pirate
    #
    #     # pay off your own bounty
    #     elif change_reason is NotorietyChangeReason.pay_off_bounty:
    #         ship.notoriety = LegalStanding.pirate - 1
    #
    #     self.events.append({
    #         "type": LogEvent.notoriety_change,
    #         "reason": change_reason,
    #         "ship_id": ship.id,
    #     })
    #
    #
    # def update_standing_universe(self, ships):
    #     for obj in ships:
    #         if obj.object_type is not ObjectType.ship: continue
    #         self.update_standing(obj)
    #
    #
    # def update_standing(self, ship):
    #     if ship.notoriety >= LegalStanding.pirate:
    #         # If ship previously was not a pirate add a bounty
    #         if ship.legal_standing < LegalStanding.pirate:
    #             ship.bounty_list.append({"bounty_type": BountyType.became_pirate, "value": 500, "age": 0})
    #             self.print(f"Bounty {BountyType.became_pirate} given to ship {ship.id}")
    #
    #         ship.legal_standing = LegalStanding.pirate
    #
    #     elif ship.notoriety <= LegalStanding.bounty_hunter:
    #         ship.legal_standing = LegalStanding.bounty_hunter
    #
    #     else:
    #         # If ship previously was a pirate remove possible bounties
    #         if ship.legal_standing >= LegalStanding.pirate:
    #             BountyController.clear_bounty(ship)
    #
    #         ship.legal_standing = LegalStanding.citizen

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
    #PROPERLY IMPLEMENT THIS


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

    def ship_moved(self, ship, distance):
        if ship in self.ore:
            self.ore[ship] += distance
        else:
            self.ore[ship] = distance

    # Final turn, add the credits to this controller
    def efficient_moved(self):
        most = -1
        ship = ""
        for x in self.ore:
            if self.ore[x] > most:
                most = self.ore[x]
                ship = x

        return [ship, most]