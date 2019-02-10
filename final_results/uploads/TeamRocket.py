import random

from game.client.user_client import UserClient
from game.common.enums import *

class CustomClient(UserClient):

    def __init__(self):
        """ Use the constructor to initialize any variables you would like to track between turns. """
        self.purchase_station = None
        self.sell_station = None
        self.destination = None
        self.material_type = None
        self.material = None
        self.done_mining = False
        self.first_sale = False
        self.second_sale = False
        self.second_sale = False
        self.engine = 1
        self.hull = 1
        self.turn = 0
        self.debug = False
    
    def team_name(self):
        self.print("Sending Team Name")
        return "Team Rocket"
    
    def team_color(self):
        self.print("Sending Team Color")
        return [0, 125, 125]    
    
    def take_turn(self, ship, universe):
        self.turn += 1
        self.update_cached_data(universe)
        
        asteroids = self.asteroid_fields
        stations = self.stations     
        
        legal_stations = []
        illegal_stations = []
        secure_station = universe.get(ObjectType.secure_station)
        ships_in_scanner = []
        filled_cargo = 0
        free_cargo_space = 500
                
        # Calculate filled and free cargo space
        for item in ship.inventory:
            filled_cargo += ship.inventory[item]
            free_cargo_space -= ship.inventory[item]
            
        # Divide stations list into legal and illegal stations and store ships in scanner
        for obj in stations:
            if obj.object_type is ObjectType.station and obj.object_type not in [ObjectType.secure_station, ObjectType.black_market_station]:
                legal_stations.append(obj)
            elif obj.object_type is ObjectType.station and obj.object_type in [ObjectType.black_market_station]:
                illegal_stations.append(obj)
            elif obj.object_type is ObjectType.ship:
                ships_in_scanner.append(obj)
                
            
        # Start by minning gold
        if self.destination is None and self.done_mining is False:
            for field in asteroids:
                if field.material_type == MaterialType.gold:
                    self.mine_field = field
                    break                    
            self.destination = self.mine_field
            self.material_type = self.mine_field.material_type
        
        # If we are at the destination mine, mine its material
        if self.in_radius_of_asteroid_field(ship, self.mine_field):
            if filled_cargo >= 250:
                self.done_mining = True
            else:    
                self.mine()
                
        # If mined mineral in inventory, go and sell it
        if self.material_type in ship.inventory and self.done_mining is True and self.first_sale is False:
            self.first_sale = True
            # Find a station that will buy it
            for station in legal_stations:
                if self.material_type in [station.primary_import]:
                    self.sell_station = station
                    self.destination = self.sell_station
                    break
                    
                    
        # If we are in radius of station we can sell to, sell material
        if self.sell_station is not None and self.in_radius_of_station(ship, self.sell_station):
            # Sell the material when possible
            self.sell_material(self.material_type, ship.inventory[self.material_type])

            # If we sold it, then we completed our task
            if self.material_type in ship.inventory and ship.inventory[self.material_type] <= 0:
                self.destination = None
               
            
            
        # If we have a mine place to go to, mine a material
        if self.destination is self.mine_field:
            # mine its material
            self.mine()

        # If we got it, go and sell it
            if str(self.material_type) in ship.inventory and ship.inventory[str(self.material_type)] >= ship.cargo_space:
                # Then we find a station that will buy it
                for station in stations:
                    if self.material_type in [station.primary_import, station.secondary_import]:
                        self.print("switching to selling at ", station.name)
                        self.print("Credits: ", ship.credits)
                        self.sell_station = station
                        self.destination = station
                        break
       

        # If we have a purchase place to go to, buy a material
        if self.destination is self.purchase_station:
            # Buy its material
            self.buy_material(1)        
             
        """ If we are in radius of station we can buy from and cargo isn't full, buy material       
        if self.in_radius_of_station(ship, self.sell_station):
            if filled_cargo <= 500:
                self.done_buying = True
            else:
                self.buy_material(self.material_type, ship.inventory[self.material_type])"""
            # Buy the material 
            
        
        """ If we aren't doing anything and have money, go to secure station
        if self.destination is None and self.done_mining is True and ship.credits >= 10000:
            self.destination = secure_station[0]
            self.print("Credits ", ship.credits)
            
        if self.in_radius_of_station(ship, secure_station[0]) and self.engine < 4:
            self.buy_module(ModuleType.engine_speed, self.engine, ShipSlot.zero)
            self.engine += 1    
            self.print("Credits ", ship.credits)
        
        if self.in_radius_of_station(ship, secure_station[0]) and self.engine > 3 and self.hull < 4:
            self.unlock_module()
            self.buy_module(ModuleType.hull, self.hull, ShipSlot.one)
            self.hull += 1      
            self.print("Credits ", ship.credits)"""
          
        
        
        # If mined mineral in inventory, go and sell it
        if self.material_type in ship.inventory and self.done_mining is True and self.second_sale is False:
            self.second_sale = True
            # Find a station that will buy it
            for station in legal_stations:
                if self.material_type in [station.primary_import]:
                    self.sell_station = station
                    self.destination = self.sell_station
                    break
                    
                    
        # If we are in radius of station we can sell to, sell material
        if self.sell_station is not None and self.in_radius_of_station(ship, self.sell_station):
            # Sell the material when possible
            self.sell_material(self.material_type, ship.inventory[self.material_type])

            # If we sold it, then we completed our task
            if self.material_type in ship.inventory and ship.inventory[self.material_type] <= 0:
                self.destination = None
                
                
                
        
        
        """ If we aren't doing anything, determine a second station to sell to
        if self.destination is None and self.done_mining is True:
            for station in legal_stations:
                if self.material_type in [station.primary_import]:
                    self.sell_station = legal_stations[1]
                    self.destination = self.sell_station
                    break
            
        # If we have a second selling place to go to, sell a material
        if self.sell_station is not None and self.in_radius_of_station(ship, self.sell_station):
            # Sell the material when possible
            self.sell_material(self.material_type, ship.inventory[self.material_type])
            self.print("Credits ", ship.credits)"""    
        
            
            
       
           

        # Always move towards our destination unless it doesn't exist
        if self.destination is not None and self.turn >= 2:
            self.move(*self.destination.position)
        else:
            self.move(0,0)

    def print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)