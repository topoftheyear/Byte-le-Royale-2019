import random
import os
import json
import platform
import shutil
import sys
from datetime import datetime, timedelta



class ServerControl:

    def __init__(self, wait_on_client, verbose):

        self._loop = None
        self._socket_client = None
        self.verbose = verbose
        self.wait_on_client = wait_on_client

        self._clients_connected = 0
        self.connection_wait_timer = 3

        self._client_ids = []
        self._quit = False


        # Game Configuration options
        system = platform.system()
        if system == "Windows":
            self.turn_time = 0.025
        else:
            self.turn_time = 0.01

        self.game_tick_no = 0
        self.max_game_tick = 1000
        self.turn_data = []

    def initialize(self):
        if self.verbose:
            print("Initializing Server Logic")

        # clear game log
        if os.path.exists("game_log"):
            shutil.rmtree("game_log")
        self.send({ "type": "game_starting"})
        self.schedule(self.pre_tick, delay=0.1)

    def wait_for_clients(self):
        if self.verbose:
            print("Waiting for clients...")

        if self._clients_connected == 0:
            self.schedule(self.wait_for_clients, 2)
        elif  self.connection_wait_timer > 0:
            # this will slowly count down every  second and then start the game
            self.connection_wait_timer -= 1
            print(f"Starting in {self.connection_wait_timer}")
            self.schedule(self.wait_for_clients, 1)
        else:
            self.schedule(self.initialize, delay=0.1)

    def notify_client_connect(self, client_id):
        self._clients_connected += 1
        self._client_ids.append(client_id)
        self.turn_data = []

    def notify_client_turn(self, data, client_id):
        data["client_id"] = client_id
        self.turn_data.append(data)

    def pre_tick(self):
        if self.verbose: print("SERVER TICK: {}".format(self.game_tick_no))
        self.game_tick_no += 1

        self.turn_data = []

        self.pre_turn()

        self.send_turn_data()

        self.schedule(self.post_tick)


    def post_tick(self):

        # wait for turn data before handling post tick
        # TODO refactor to check to see if we have the same number of responses as clients, and wait only so long before continuing
        if self.turn_data is None and self.wait_on_client:
            self.schedule(self.post_tick)
            return

        self.post_turn()

        log_data = self.log()
        self.dump_log(log_data)

        if self.game_tick_no < self.max_game_tick:
            if not self._quit:
                self.schedule(self.pre_tick)
            else:
                # Exit Cleanly

                # Dump Game log manifest
                with open("game_log/manifest.json", "w") as f:
                    json.dump({"ticks": self.game_tick_no}, f)

                self._socket_client.close()
                self.schedule(lambda : sys.exit(0), 3)

        else:
            print("Exiting - MAX Tickes: {0} exceeded".format(self.max_game_tick))

            # Dump Game log manifest
            with open("game_log/manifest.json", "w") as f:
                json.dump({"ticks": self.game_tick_no}, f)

            self._socket_client.close()
            self.schedule(lambda : sys.exit(1), 3)

    def send_turn_data(self):
        pass

    def set_loop(self, loop):
        self._loop = loop

    def set_socket_client(self, socket_client):
        self._socket_client = socket_client

    def send(self, data):
        self._socket_client.sendAll( data )


    def schedule(self, callback, delay=None):
        self._loop.call_later(
                delay if delay != None else self.turn_time,
                callback)


    def pre_turn(self):
        """ Override. Logic to be executed before the players are allowed to take a turn """
        pass


    def post_turn(self):
        """Override. Logic to be executed after the players have sent turn actions"""
        pass

    def log(self):
        """Override. Dumps state to a file """
        return {}


    def dump_log(self, data):
        if not os.path.exists("game_log"):
            os.makedirs("game_log")

        with open("game_log/{0:05d}.json".format(self.game_tick_no), "w") as f:
            json.dump(data, f)

    def notify_game_over(self):
        self.send({
            "type": "game_over"
        })





