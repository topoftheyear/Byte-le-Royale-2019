import json
import os

from game.common.enums import *
from game.common.ship import Ship
from game.common.station import *
from game.common.asteroid_field_types import load_asteroid_field

class GameLogParser:
    def __init__(self, log_dir):

        if not os.path.exists(log_dir):
            raise Exception("Invalid log directory: {}".format(log_dir))

        self.log_dir = log_dir

        # parse manifest
        with open("{}/manifest.json".format(log_dir), "r") as f:
            manifest = json.load(f)
            self.max_ticks = manifest["ticks"]

        self.turns = []

        self.tick = 1

        self.load_turns()

    def load_turns(self):
        for tick in range(1,self.max_ticks):
            with open("{0}/{1:05d}.json".format(self.log_dir, tick), "r") as f:
                turn = json.load(f)

            events = self._parse_turn(turn)
            self.turns.append(events)

    def get_turn(self):
        if self.tick < self.max_ticks:
            turn = self.turns[self.tick]
            self.tick += 1
            return turn
        else:
            return None, None

    def check_finished(self):
        return self.tick > self.max_ticks


    def _parse_turn(self, turn):

        events = turn["turn_result"]["events"]
        universe = self.deserialize_universe(turn["turn_result"]["universe"])

        for event in events:
            # mark that the event hasn't been handled
            event["handled"] = False

            #if event["type"] == LogEvent.demo:
            #    pass # Deserialize game objects as needed


        return universe, events


    def deserialize_universe(self, data):
        objs = []

        for serialized_obj in data:
            obj_type = serialized_obj["object_type"]
            if obj_type == ObjectType.ship:
                obj = Ship()
                obj.from_dict(serialized_obj, security_level=SecurityLevel.engine)
                objs.append(obj)

            elif obj_type == ObjectType.station:
                obj = Station()
                obj.from_dict(serialized_obj, security_level=SecurityLevel.engine)
                objs.append(obj)

            elif obj_type == ObjectType.black_market_station:
                obj = BlackMarketStation()
                obj.from_dict(serialized_obj, security_level=SecurityLevel.engine)
                objs.append(obj)

            elif obj_type == ObjectType.secure_station:
                obj = SecureStation()
                obj.from_dict(serialized_obj, security_level=SecurityLevel.engine)
                objs.append(obj)

            elif obj_type in [ObjectType.cuprite_field]:
                obj = load_asteroid_field(obj_type, serialized_obj, security_level=SecurityLevel.engine)
                objs.append(obj)

            elif obj_type in [ObjectType.gold_field]:
                obj = load_asteroid_field(obj_type, serialized_obj, security_level=SecurityLevel.engine)
                objs.append(obj)

            elif obj_type in [ObjectType.goethite_field]:
                obj = load_asteroid_field(obj_type, serialized_obj, security_level=SecurityLevel.engine)
                objs.append(obj)

        return objs
