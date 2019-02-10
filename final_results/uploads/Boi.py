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

        self.debug = False

    def team_name(self):
        #self.print("Sending Team Name")

        return "-Boi"

    def team_color(self):
        #self.print("Sending Team Color")

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [255, 255, 255]

    def take_turn(self, ship, universe):
        self.update_cached_data(universe)
        stations = self.stations
        gold_station = list(filter(lambda x: x.primary_import==10, stations))[0]
        computer_station = list(filter(lambda x: x.primary_import==4, stations))[1]
        weaponry_station = list(filter(lambda x: x.primary_import==8, stations))[0]
        drones_station = list(filter(lambda x: x.primary_import==6, stations))[0]
        copper_station = list(filter(lambda x: x.secondary_import==9, stations))[0]
        gmine = universe.get(ObjectType.gold_field)[0]
        self.sell_station = gold_station

        if self.destination is not None:
            self.move(*self.destination)
        else:
           self.move(*ship.position)

        if len(ship.inventory) == 0:
            self.destination = gmine.position


        try:
            if self.in_radius_of_asteroid_field(ship, gmine):
                self.mine()

            elif self.in_radius_of_station(ship, gold_station):
                if ship.inventory[MaterialType.gold] > 0:
                    self.sell_material(MaterialType.gold, ship.inventory[MaterialType.gold])
                    #self.print("\nselling")
                else:
                    self.buy_material(10000)
                    #self.print("INVENTORY: " + str(ship.inventory))
                    self.destination = computer_station.position

            elif self.in_radius_of_station(ship, computer_station):
                if ship.inventory[MaterialType.circuitry] > 0:
                    self.sell_material(MaterialType.circuitry, ship.inventory[MaterialType.circuitry])
                    #self.print("\nselling")
                else:
                    self.buy_material(10000)
                    #self.print("INVENTORY: " + str(ship.inventory))
                    self.destination = weaponry_station.position

            elif self.in_radius_of_station(ship, weaponry_station):
                if ship.inventory[MaterialType.computers] > 0:
                    self.sell_material(MaterialType.computers, ship.inventory[MaterialType.computers])
                    #self.print("\nselling")
                else:
                    self.buy_material(10000)
                    #self.print("INVENTORY: " + str(ship.inventory))
                    self.destination = drones_station.position

            elif self.in_radius_of_station(ship, drones_station):
                if ship.inventory[MaterialType.weaponry] > 0:
                    self.sell_material(MaterialType.weaponry, ship.inventory[MaterialType.weaponry])
                    #self.print("\nselling")
                else:
                    self.buy_material(10000)
                    #self.print("INVENTORY: " + str(ship.inventory))
                    self.destination = copper_station.position
                    
            elif self.in_radius_of_station(ship, copper_station):
                self.sell_material(MaterialType.drones, ship.inventory[MaterialType.drones])

        except:
            pass

        try:
            if sum(ship.inventory.values()) == ship.cargo_space and self.destination != gold_station.position:
                self.destination = gold_station.position
                #self.print("\nGOLD FULL")
        except:
            pass

        try:
            if ship.inventory[MaterialType.circuitry] > 0:
                self.destination = computer_station.position
        except:
            pass

        self.print("\nINVENTORY" + str(ship.inventory))
        self.print("    CREDITS" + str(ship.credits))

    def take_turn3(self, ship, universe):
        self.update_cached_data(universe)
        #self.print("MOD0: " + str(ship.module_1))
        # self.print("\nMODUNLOCK1: " + str(self.get_module_unlock_price(ShipSlot.one)))
        # self.print("\nMODUNLOCK2: " + str(self.get_module_unlock_price(ShipSlot.two)))
        # self.print("\nMODUNLOCK3: " + str(self.get_module_unlock_price(ShipSlot.three)))
        #self.print("MODLVLPRICE: " + str(self.get_module_price(2)))
        # if ship.position == [500, 350] and ship.module_0 == ModuleType.empty:
        #     self.buy_module(ModuleType.cargo_and_mining, 1, ShipSlot.zero)
        #     self.print("creds" + str(ship.credits))

        stations = self.stations
        gold_station = list(filter(lambda x: x.primary_import==10, stations))[0]
        computer_station = list(filter(lambda x: x.primary_import==4, stations))[0]
        self.sell_station = gold_station
        #self.print("\nGOLD STATIONS" + str(gold_station))
        # Gold is #10
        # gold first then sell then kill
        gmine = universe.get(ObjectType.gold_field)[0]
        #self.print(str(gmine[0]))
        if len(ship.inventory) == 0:
            self.destination = gmine.position
        #self.print("\nPOS" + str(gmine[0].position) + "\n")
        if self.destination is not None:
            self.move(*self.destination)
        else:
           self.move(*ship.position)

        try:
            if sum(ship.inventory.values()) == ship.cargo_space and self.destination != gold_station.position:
                self.destination = gold_station.position
                #self.print("\nGOLD FULL")
        except:
            pass

        if self.in_radius_of_asteroid_field(ship, gmine):
            self.mine()
            #self.print("\nINVENTORY: " + str(ship.inventory))

        elif self.in_radius_of_station(ship, gold_station):
            #self.print("\nCredits: " + str(ship.credits))
            if ship.inventory[MaterialType.gold] > 0:
                self.sell_material(MaterialType.gold, ship.inventory[MaterialType.gold])
                #self.print("\nselling")
            else:
                self.buy_material(10000)
                #self.print("INVENTORY: " + str(ship.inventory))
                self.destination = gmine.position
            #self.print("\nCredits: " + str(ship.credits))
        elif self.in_radius_of_station(ship, computer_station):
            if ship.inventory[MaterialType.circuitry] > 0:
                self.sell_material(MaterialType.circuitry, ship.inventory[MaterialType.circuitry])
            else:
                self.buy_material(10000)
                self.destination = gmine.position

        try:
            if ship.inventory[MaterialType.circuitry] >= 300:
                self.destination = computer_station.position
        except:
            pass

        self.print("\nINVENTORY" + str(ship.inventory))
        self.print("    CREDITS" + str(ship.credits))



    def take_turn2(self, ship, universe):
        stations = []
        ships_in_scanner = []

        # Compile universe list into stations and scan-range ships
        for obj in universe:
            if obj.object_type is ObjectType.station and obj.object_type not in [ObjectType.secure_station, ObjectType.black_market_station]:
                stations.append(obj)
            elif obj.object_type is ObjectType.ship:
                ships_in_scanner.append(obj)

        # If we aren't doing anything, determine a station to purchase from
        if self.destination is None:
            self.print("new interaction generated")
            self.purchase_station = random.choice(stations)
            self.destination = self.purchase_station
            self.material = self.purchase_station.production_material
            self.print("new interaction generated: ", str(self.material))
            self.print("buying", self.material)

        # If we have a purchase place to go to, buy a material
        if self.destination is self.purchase_station:
            # Buy its material
            self.buy_material(1)

            # If we got it, go and sell it
            if str(self.material) in ship.inventory and ship.inventory[str(self.material)] > 0:

                # Then we find a station that will buy it
                for station in stations:
                    if self.material in [station.primary_import, station.secondary_import]:
                        self.print("switching to selling selling at ", station)
                        self.sell_station = station
                        self.destination = station
                        break

        # If we have a sell place to go to, go and sell it
        elif self.destination is self.sell_station:
            # Sell the material when possible
            self.sell_material(self.material, ship.inventory[str(self.material)])

            # If we sold it, then we completed our task
            if str(self.material) in ship.inventory and ship.inventory[str(self.material)] <= 0:
                self.destination = None

        # Always move towards our destination unless it doesn't exist
        if self.destination is not None:
            self.move(*self.destination.position)
        else:
            self.move(0,0)

    def print(self, string):
        f = open("mylog.txt", "a")
        f.write(string)
