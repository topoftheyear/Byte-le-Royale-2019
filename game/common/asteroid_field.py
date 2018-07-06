from uuid import uuid4

from game.common.game_serializable import Serializable
from game.common.enums import *
from game.common.material_types import *

class Asteroid_Field(Serializable):

    def __init__(self):
        self.initialized = False
        
    def init(self, name, position=(0,0), material_type, mining_rate, accessibility_radius):
        
        self.id = str(uuid4())
        self.name = name
        
        self.position = position
        
        self.material_type = material_type
        self.mining_rate = mining_rate
        
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
                "name": self.name
                
                "position": self.position
                
                "material_type": self.material_type
                "mining_rate": self.mining_rate
                
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
            
            self.material_type = data["material_type"]
            self.mining_rate = data["mining_rate"]
            
            self.accessibility_radius = accessibility_radius
            
        if security_level <= SecurityLevel.player_owned:
            pass
            
        if security_level <= SecurityLevel.other_player:
            pass
            