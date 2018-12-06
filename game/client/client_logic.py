import os
import sys

from game.common.enums import *



class ClientLogic:

    def __init__(self, verbose, player_client):
        self._loop = None
        self._socket_client = None
        self.verbose = verbose
        self.player_client = player_client

        # check to see if the client defiens the quit_in_game_over variable
        self.quit_on_game_over = getattr(self.player_client, "quit_on_game_over", True)

        # Public properties availiable to users

        self.started_game = False
        self.tick_no = 0

    def set_loop(self, loop):
        self._loop = loop

    def set_socket_client(self, socket_client):
        self._socket_client = socket_client

    def initialize(self):

        self.send({
            "type": "register"
        })

    def tick(self, turn_data):
        self.tick_no += 1

        turn_data = self.deserialize(turn_data)

        try:
            turn_result = self.turn(turn_data)
        except Exception as e:
            print()
            print("Exception:")
            print(e)
            raise e
            sys.exit(1)

        serialized_turn_result = self.serialize(turn_result)

        self.send({
            "type": "client_turn",
            "payload": serialized_turn_result
        })

    def turn(self, turn_data):

        if turn_data["message_type"] == MessageType.team_name:
            team_name = self.player_client.team_name()
            return {
                "message_type": MessageType.team_name,
                "team_name": team_name
            }
        elif turn_data["message_type"] == MessageType.team_color:
            team_color = self.player_client.team_color()
            return {
                "message_type": MessageType.team_color,
                "team_color": team_color
            }
        elif turn_data["message_type"] == MessageType.ping:
            print("Pong")
            return {
                "message_type": MessageType.pong
            }
        else:
            return{
                "message_type": MessageType.null
            }

    def send(self, data):
        self._socket_client.send(data)

    def notify_game_started(self):
        if self.verbose:
            print("Game Started")
        self.started_game = True

    def deserialize(self, turn_data):

        # deserialize any objects the client is going to need to work with and replace serialized copy with object

        return turn_data

    def serialize(self, turn_result):

        # serialize any objects the being sent to the server

        return turn_result

    def notify_game_over(self):
        if callable(getattr(self.player_client, "game_over", None)):
            self.player_client.game_over()

        if self.quit_on_game_over:
            exit()



