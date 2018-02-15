import random

from game.client.user_client import UserClient
from game.common.enums import *



class CustomClient(UserClient):

    def __init__(self):
        """ Use the constructor to initialize any variables you would like to track between turns. """

    def team_name(self):
        print("Sending Team Name")

        return "Herp Derp (AKA Jordan Test)"

    def unit_choice(self):
        print("Sending Unit Choices")

        return [
                {
                    "name": "Dood",
                    "class": UnitClass.brawler
                },
                {
                    "name": "Surge",
                    "class": UnitClass.sorcerer
                },
                {
                    "name": "Kafka",
                    "class": UnitClass.pikeman
                },
                {
                    "name": "Donatello",
                    "class": UnitClass.magus
                }
            ]


    def town(self, units, gold, store):
        print()
        print("*"*50)
        print("Town")
        print("*"*50)

        print("Gold: {}".format(gold))

        #raise Exception("adfasdfA")

        #unit3 = self.get_unit("Dood", units)
        #if unit3 is not None:
        #    store.purchase(unit3, ItemType.spear_of_light, 1, item_slot=2)

        if store.get_town_number() is 0:
            unit1 = self.get_unit("ed", units)
            unit3 = self.get_unit("dood", units)
            if unit3 is not None:
                store.purchase(unit3, ItemType.shock_bomb, 1, item_slot=1)

        #elif store.get_town_number() is 1:
        #    unit1 = self.get_unit("ed", units)
        #    unit2 = self.get_unit("edd", units)
        #    unit3 = self.get_unit("carlos", units)
        #    if unit1 is not None:
        #        store.purchase(unit1, ItemType.sword, 2)
        #    if unit2 is not None:
        #        store.purchase(unit2, ItemType.mace, 2)
        #    if unit3 is not None:


        #elif store.get_town_number() is 2:
        #    unit1 = self.get_unit("ed", units)
        #    unit2 = self.get_unit("edd", units)
        #    unit3 = self.get_unit("carlos", units)
        #    if unit1 is not None:
        #        store.purchase(unit1, ItemType.sword, 3)
        #    if unit2 is not None:
        #        store.purchase(unit2, ItemType.mace, 3)
        #    if unit3 is not None:
        #        store.purchase(unit3, ItemType.fire_bomb, 3, item_slot=2)

        #elif store.get_town_number() is 3:
        #    unit1 = self.get_unit("ed", units)
        #    unit2 = self.get_unit("edd", units)
        #    unit3 = self.get_unit("carlos", units)
        #    if unit1 is not None:
        #        store.purchase(unit1, ItemType.sword, 4)
        #    if unit2 is not None:
        #        store.purchase(unit2, ItemType.mace, 4)
        #    if unit3 is not None:
        #        store.purchase(unit3, ItemType.frost_bomb, 4, item_slot=2)


    def room_choice(self, units, options):

        if len(options) == 1:
            return Direction.forward

        elif len(options) == 2:
            return random.choice([Direction.right, Direction.left])
        else:
            return MessageType.null

    def combat_round(self, monster, units):
        print()
        print("*"*50)
        print("Combat")
        print("*"*50)
        print(monster.summary())
        for u in units:
            print(u.summary())

        for u in units:
            if u.unit_class == UnitClass.alchemist:
                if u.bomb_1_quantity > 0:
                    u.use_bomb_1()
                else:
                    u.resupply(1)

            if u.unit_class == UnitClass.brawler:
                u.fit_of_rage()

            else:
                u.attack()

    def trap_round(self, trap, units):
        print()
        print("*"*50)
        print("Trap!")
        print("*"*50)
        print(trap.summary())
        for u in units:
            print(u.summary())

        if trap.trap_type == TrapType.puzzle_box:
            print()

        if trap.trap_type == TrapType.riddles_of_the_sphinx:
            print()


        for u in units:
            u.trap_action = random.choice([TrapAction.little_effort, TrapAction.large_effort, TrapAction.evade])


    ##################
    # Helper Methods #
    ##################

    def get_unit(self, name, units):
        for unit in units:
            if unit.name.lower() == name.lower():
                return unit
        return None


