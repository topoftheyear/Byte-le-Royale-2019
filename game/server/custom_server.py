import json

from game.server.server_control import ServerControl
from game.common.enums import *


class CustomServer(ServerControl):

    def __init__(self, verbose=False, wait_on_client=False):
        super().__init__(wait_on_client, verbose)

        self.verbose = verbose

        self.started = False
        self.turn_log = None


    def pre_turn(self):
        self.print("#"*70)
        self.print("SERVER PRE TURN")

        # reset turn result
        self.turn_log = { "events":[
                {
                    "type": Event.demo
                }
            ],
        }

        if not self.started:
            # first turn, ask for client config, e.g. team name
            return # purposefully short circuit to get to send data

    def send_turn_data(self):
        # send turn data to clients
        self.print("SERVER SEND DATA")
        payload = {}

        for i in self._client_ids:
            payload[i] = { "message_type": MessageType.null }

            if not self.started:
                # request team registration info
                payload[i] = {
                        "message_type":  MessageType.demo
                }

            else:
                # send game specific data in payload
                pass

        # actually send the data to the client
        self.send({
            "type": "server_turn_prompt",
            "payload": payload
        })



    def post_turn(self):
        self.print("SERVER POST TURN")

        self.deserialize_turn_data()

        # handle response if we got one
        for data in self.turn_data:
            if "message_type" not in data:
                return # bad turn

            if not self.started:
                if data["message_type"] == g.demo:
                    # handle network message
                    # this code block is reserved for registering team info
                    # the game will not start until the client send a message
                    # that gets to this code block
                    self.started = True

            else:

                # queue action a player wants to take
                #   deal damage if a player would be damaged

                # check if player still alive

                # queue movement action player wants to take

                pass

        # check if player still alive

        # apply the results of any actions a player took if player still alive

        # apply movement action player wanted to take

        # update station market

        self.turn_data = []




    def log(self):
        # saves the turn log to this turn's log file.
        # This is what the visualizer reads
        return {
            "turn_result": self.turn_log
        }


    def deserialize_turn_data(self):
        # Deserialize a message from a client

        # if we have recieved a message, then turn data will not be none
        for idx, data in enumerate(self.turn_data):
            if data["message_type"] != MessageType.demo:
                # Deserialize message data, i.e. load ship data
                pass

    def check_end(self):
        # Detect if we have reached a stopping state
        # set self._quit to true to safely shutdown at end of turn
        #self._quit = True
        pass

    def print(self, msg):
        # Handles toggling print messages via verbose
        if self.verbose:
            print(msg)


    def game_over(self):

        # print game exit info

        self.turn_log["events"].append({
            "type": LogEvent.demo,
        })

        self._quit = True # die safely
        return


