import json
import os

from game.common.enums import *

class GameLogParser:
    def __init__(self, log_dir):

        if not os.path.exists(log_dir):
            raise Exception("Invalid log directory: {}".format(log_dir))

        self.log_dir = log_dir

        # parse manifest
        with open("{}/manifest.json".format(log_dir), "r") as f:
            manifest = json.load(f)
            self.max_ticks = manifest["ticks"]

        self.tick = 1


    def get_turn(self):
        with open("{0}/{1:05d}.json".format(self.log_dir, self.tick), "r") as f:
            turn = json.load(f)

        events = self._parse_turn(turn)

        self.tick += 1

        return events

    def check_finished(self):
        return self.tick > self.max_ticks


    def _parse_turn(self, turn):

        events = turn["turn_result"]["events"]

        for event in events:
            # mark that the event hasn't been handled
            event["handled"] = False

            if event["type"] == LogEvent.demo:
                pass # Deserialize game objects as needed

        return events


