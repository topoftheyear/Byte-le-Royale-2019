from uuid import uuid4

from game.common.game_serializable import Serializable
from game.common.enums import *
from game.common.material_types import *

class Station(Serializable):

    def __init__(self):
        self.initialized = False
        
    def init(self, name, position=(0,0), consumption_material=None, consumption_rate=1, production_material=None, production_rate=1, current_cargo=0, accessibility_radius=5, ):
    
        self.id = str(uuid4())
        self.name = name
        
        self.position = position
        
        self.consumption_material = consumption_material
        self.consumption_rate = consumption_rate
        self.production_material = production_material
        self.production_rate = production_rate
        
        self.current_cargo = current_cargo
        
        self.accessibility_radius = accessibility_radius
        
    def to_dict(self, security_level=SecurityLevel.other_player):
        data = {}
        
        if security_level is SecurityLevel.engine:
            # fields only accessible to the engine
            engine = {
                "id": self.id
            }
            
            data = { *data, *engine }
            
        if security_level <= SecurityLevel.player_owned:
            # fields only accessible to the player owner of this object
            
            # technically a feasible and interesting direction to go but not discussed yet
            pass

            
        if security_level <= SecurityLevel.other_player:
            # fields other players can view
            other_player = {
                "name": self.name,
                "position": self.position,
                
                "consumption_material": self.consumption_material,
                "consumption_rate": self.consumption_rate,
                "production_material": self.production_material,
                "production_rate": self.production_rate ,
                
                "current_cargo": self.current_cargo,
                
                "accessibility_radius": self.accessibility_radius
            }
            
            
            data = { *data, *other_player }
            
            
    def from_dict(self, data, security_level=SecurityLevel.other_player):
    
        if security_level is SecurityLevel.engine:
            # properties that will only be populated by the engine,
            #   prevents user tampering with variables
            
            self.id = data["id"]
            self.name = data["name"]
            
            self.position = data["position"]
            
            self.consumption_material = data["consumption_material"]
            self.consumption_rate = data["consumption_rate"]
            self.production_material = data["production_material"]
            self.production_rate = data["production_rate"]
            
            self.current_cargo = data["current_cargo"]
            
            self.accessibility_radius = data["accessibility_radius"]
            
        if security_level <= SecurityLevel.player_owned:
            pass
            
        if security_level <= SecurityLevel.other_player:
            pass