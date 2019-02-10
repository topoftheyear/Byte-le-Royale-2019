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
        self.turn_count = 0
        self.debug = False
        self.task = "mine"
        self.upgrade_loop = 3
        self.backup = []
        self.first_time = True

    def team_name(self):
        self.print("Sending Team Name")

        return "W_T_OVERLOAD"

    def team_color(self):
        self.print("Sending Team Color")

        # list of [ red, green, blue ] values or
        # hex color "#333aaa"
        return [154, 50, 205]

    def take_turn(self, ship, universe):
        stations = []
        ships_in_scanner = []
        self.turn_count += 1  
        self.update_cached_data(universe)
        #print(self.task)
        def get_inventory_size(ship):
            total = 0
            for type in [MaterialType.iron,MaterialType.steel,MaterialType.copper,MaterialType.circuitry,MaterialType.pylons,MaterialType.weaponry,MaterialType.machinery,MaterialType.computers,MaterialType.drones,MaterialType.gold,MaterialType.goethite,MaterialType.cuprite,MaterialType.wire,MaterialType.salvage]:
                if type in ship.inventory:
                    total+= ship.inventory[type]
            return total
        def determine_threats(self, ship, universe) :
            #get list of surrounding ships
            listOfOthers = self.ships
            #Determine the disparities between my ships hull/noteriety and the enemies.
            #Partly based on the assumption that the higher their noteriety, the more aggressive they are.
            list_of_hull_diffs = [len(listOfOthers)]
            list_of_notoriety_diffs = [len(listOfOthers)]
            index = 0
            for enemy_ship in listOfOthers :
                hull_diff = ship.current_hull - enemy_ship.current_hull
                not_diff = ship.notoriety - enemy_ship.notoriety
                list_of_hull_diffs[index] = hull_diff
                list_of_notoriety_diffs[index] = not_diff
            evadeFlag =False
            flag = False
            flagged_ship_index = None
            index = 0
            for indv_hull_diff in list_of_hull_diffs :
                if indv_hull_diff < 0 and list_of_notoriety_diffs[index] < 0 :
                    flag = False
                    evadeFlag = True
                    flagged_ship_index = index
                    break
                elif indv_hull_diff > 0 and listOfOthers[index].notoriety >= 5 :
                    flagged_ship_index = index
                    flag = True
                    break
                else: 
                    index += 1
            if flag == True :
                return (True, list_of_others[index])
            elif evadeFlag == True:
                return (False, list_of_others[index])
            else :
                return None
        #The following function will attempt to pick up illegal salvage. Will return true if salvage has been picked up. 
        def determine_salvage(self, ship, universe) :
            notoriety = ship.notoriety
            if notoriety < 4 :
                if self.collect_illegal_salvage() :
                    return True
                else :
                    return False
            else:
                return False
        #Following function checks whether there exists any threats in the vicinity of the ship. Performs evasive/opportunistic manoevers depending on situation.
        def intermediate_in_transit(self):
            #Checks to see whether there are threats. 
            possible_threats = determine_threats(self, ship, universe)
            possible_salvage_spots = determine_salvage(self, ship, universe)
            if possible_threats is not None :
                if possible_threats[0] == True :
                    if possible_threats[0] :
                        #self.intermediate_destination = possible_threats[1].position
                        self.attack(possible_threat[2])
                    else:
                        #self.intermediate_destination = (possible_threats[1].position[0] , possible_threats[1].position[1])
                        enemy_x = possible_threats[1].position[0]
                        enemy_y = possible_threats[1].position[1]
                        diff_x = abs(self.position[0] - enemy_x)
                        diff_y = abs(self.position[1] - enemy_y)
                        evade_to_x = 0
                        evade_to_y = 0
                        if enemy_x < self.position[0]:
                            evade_to_x = self.position[0] + diff_x
                        else :
                            evade_to_x = self.position[0] - diff_x
                        if enemy_y < self.position[1]:
                            evade_to_y = self.position[1] + diff_y
                        else:
                            evade_to_y = self.position[1] - diff_y
                        self.move(evade_to_x, evade_to_y)
        
        def determine_station_to_sell(item):
            #Loop through stations and figure out which buys this item
            for station in universe.get("all_stations"):
                if station.primary_import == item:
                    return station
        
        def determine_highest_quantity_item(ship):
            vals = list(ship.inventory.values())
            keys = list(ship.inventory.keys())
            return keys[vals.index(max(vals))]

                
        def determine_module_to_upgrade(ship):
            module_levels = [[ship.module_0,ship.module_0_level], [ship.module_1,ship.module_2_level], [ship.module_2,ship.module_2_level], [ship.module_3,ship.module_3_level]]
            print(module_levels)
            level = 10000
            module_to_return = []
            for pair in module_levels:
                #if we have module unlocked and its the lowest level so far
                if pair[0] != -2 & pair[1] < level:
                    module_to_return = pair
                    level = pair[1]   
            
            #print(f"Determined to upgrade module{module_to_return[0]} to level {module_to_return[1]+1}")        
            return module_levels.index(module_to_return), module_to_return[1]
        def determine_if_fully_upgraded(ship):
            num_of_upgrades = ship.module_0_level + ship.module_1_level + ship.module_2_level + ship.module_3_level
            if num_of_upgrades == 9:
                return True
            else:
                return False
        def determine_if_all_modules_unlocked(ship):
            num_of_modules = 0
            for mod in [ship.module_0,ship.module_1,ship.module_2,ship.module_3]:
                if mod != -2:
                    num_of_modules += 1
            if num_of_modules == 4:
                return True
            else:
                return False
        intermediate_in_transit(self)
        if ship.respawn_counter > 1 :
            self.task = "mine"
            self.destination = universe.get(ObjectType.goethite_field)[0]
        #Start turn 1 buying mod and heading to mine
        if self.turn_count == 1:
            self.buy_module(ModuleType.engine_speed, ModuleLevel.one, ShipSlot.zero)
            self.destination = universe.get(ObjectType.cuprite_field)[0]        
       
        for a_ship in self.ships:
            if self.in_weapons_range(ship, a_ship) & a_ship.max_hull >1000 & False:
                print(f"Found pricey target to hunt! Take em down")
                if self.destination is None :
                    self.task = mine
                    self.destination = universe.get(ObjectType.goethite_field)[0]
                self.backup = [self.task, self.destination]
                self.task = "hunt"
                self.destination = a_ship
                
        if self.task == "mine":
            if self.destination is None:
                #Mine until cargo hold is full
                if self.first_time:
                    if get_inventory_size(ship)< ship.cargo_space/3:
                        self.mine()
                    else:
                        self.task = "sell"
                        self.destination = determine_station_to_sell(determine_highest_quantity_item(ship))
                        print(f"Time to sell, heading to {self.destination.name}")
                        self.first_time = False
                elif get_inventory_size(ship) < ship.cargo_space:
                    self.mine()
                #When its full its time to sell
                else:
                    
                    self.task = "sell"
                    self.destination = determine_station_to_sell(determine_highest_quantity_item(ship))
                    print(f"Time to sell, heading to {self.destination.name}")
            #Check if we've arrived. If so remove destination
            else:
                if self.in_radius_of_asteroid_field(ship, self.destination) == True:
                    self.destination = None
        
        elif self.task == "sell":
            if self.destination is None:
                self.sell_material(determine_highest_quantity_item(ship), 9999)
                
                self.task = "unlock"
                self.destination = universe.get(ObjectType.secure_station)[0]
                print(f"Time to unlock, heading to {self.destination.name} at {self.destination.position}")
            #Check if we've arrived. If so remove destination
            else:  
                if self.in_radius_of_station(ship, self.destination) == True:
                    self.destination = None
                    
        elif self.task == "unlock":
            if determine_if_all_modules_unlocked(ship) == False:
                if self.destination is None:
                    self.unlock_module()
                    print(f"Attempted to unlock,, time to upgrade")
                    self.task = "upgrade"
                else:
                    if self.in_radius_of_station(ship, self.destination) == True:
                        self.destination = None
            else:
                print("Fully unlocked, passing off to upgrade")
                self.task = "upgrade"       
        elif self.task == "upgrade":
            if determine_if_fully_upgraded(ship) == False:
                module_to_upgrade, level = determine_module_to_upgrade(ship)
                #Slot 0 - cargo_and_mining
                if module_to_upgrade == 2:
                    if level == 0:
                        print(f"Purchasing upgrade level {level+1} for cargo_and_mining")
                        self.buy_module(ModuleType.cargo_and_mining, ModuleLevel.one, ShipSlot.zero)
                    if level == 1:
                        print(f"Purchasing upgrade level {level+1} for cargo_and_mining")                    
                        self.buy_module(ModuleType.cargo_and_mining, ModuleLevel.two, ShipSlot.zero)
                    if level == 2:
                        print(f"Purchasing upgrade level {level+1} for cargo_and_mining")                    
                        self.buy_module(ModuleType.cargo_and_mining, ModuleLevel.three, ShipSlot.zero)                    
                elif module_to_upgrade == 1:
                    if level == 0:
                        print(f"Purchasing upgrade level {level+1} for hull")
                        self.buy_module(ModuleType.hull, ModuleLevel.one, ShipSlot.one)
                    if level == 1:
                        print(f"Purchasing upgrade level {level+1} for hull")                    
                        self.buy_module(ModuleType.hull, ModuleLevel.two, ShipSlot.one)
                    if level == 2:
                        print(f"Purchasing upgrade level {level+1} for hull")                    
                        self.buy_module(ModuleType.hull, ModuleLevel.three, ShipSlot.one) 
                elif module_to_upgrade == 0:
                    if level == 0:
                        print(f"Purchasing upgrade level {level+1} for engine_speed")
                        self.buy_module(ModuleType.engine_speed, ModuleLevel.one, ShipSlot.two)
                    if level == 1:
                        print(f"Purchasing upgrade level {level+1} for engine_speed")                    
                        self.buy_module(ModuleType.engine_speed, ModuleLevel.two, ShipSlot.two)
                    if level == 2:
                        print(f"Purchasing upgrade level {level+1} for engine_speed")                    
                        self.buy_module(ModuleType.engine_speed, ModuleLevel.three, ShipSlot.two)   
                elif module_to_upgrade == 3:
                    if level == 0:
                        print(f"Purchasing upgrade level {level+1} for weapons")
                        self.buy_module(ModuleType.weapons, ModuleLevel.one, ShipSlot.three)
                    if level == 1:
                        print(f"Purchasing upgrade level {level+1} for weapons")                    
                        self.buy_module(ModuleType.weapons, ModuleLevel.two, ShipSlot.three)
                    if level == 2:
                        print(f"Purchasing upgrade level {level+1} for weapons")                    
                        self.buy_module(ModuleType.weapons, ModuleLevel.three, ShipSlot.three)   
                if ship.credits <10000 | self.turn_count > 1200:
                    print("Low on funds or near end of game, don't waste money!!!")
                    self.task = "mine"
                    self.destination = universe.get(ObjectType.gold_field)[0]
                else:
                    print("Upgrade successful, let's try unlocking more")
                    self.task = "unlock"
            else:
                print("Fully upgraded, it's time to mine!")
                self.task = "mine"
                self.destination = random(universe.get("all_fields"))
        elif self.task == "hunt":
            if self.destination is not None:
                print("Attacking")
                self.attack(self.destination)
            else:
                print("he ded")
                self.task, self.destination = self.backup
        #Always be moving
        if self.destination is not None:
            self.move(*self.destination.position)
            
        
        

    def print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)




