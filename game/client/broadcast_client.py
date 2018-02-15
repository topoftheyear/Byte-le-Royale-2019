from autobahn.asyncio.websocket import WebSocketClientProtocol
from autobahn.asyncio.websocket import WebSocketClientFactory

import sys
import os
import json
import random
import string


class BroadcastClientProtocol(WebSocketClientProtocol):

    def __init__(self, *args, **kwargs):
        super(WebSocketClientProtocol, self).__init__(*args, **kwargs)

        self.clients = []
        self.trigger_tick_cb = None
        self.id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
        self.verbose = False

    def onOpen(self):
        self.factory._registerClient(self)
        self.factory.trigger_initialize_cb()
        self.verbose = self.factory.verbose
        if self.verbose:
            print("Client connection open")

    def onConnect(self, client):
        if self.verbose:
            print("Client connecting: {}".format(client.peer))
        self.clients.append(client)


    def onMessage(self, payload, isBinary):

        # deserialize json
        obj = json.loads(payload.decode("utf8"))

        #if obj["type"] != "pong":
        #    print("Incoming Message: ", obj["type"])

        if(obj["type"] == "pong"):
            if self.verbose:
                print("Pong!");

        elif obj["type"] == "error":
            if self.verbose:
                print("Communication Error: {}".format(obj["msg"]))

        elif obj["type"] == "game_starting":
            self.factory.notify_game_started_cb()

        elif obj["type"] == "server_turn_prompt":
            data = obj["payload"][self.id]
            self.trigger_tick_cb(data)

        elif obj["type"] == "game_over":
            self.factory.notify_game_over_cb()


    def connectionLost(self, reason):
        WebSocketClientProtocol.connectionLost(self, reason)
        self.factory._unregisterClient(self)
        if self.verbose:
            print("Connection lost. Reason: {}".format(reason))

    def onClose(self, wasClean, code, reason):
        if self.verbose:
            print("Connection closed. Reason: {}".format(reason))
            print("Server Connection Closed. Exiting.")
        sys.exit(0)

    def register(self, id):
        self.clients.append(id)

    def broadcast(self, payload):
        self.send(payload, type="broadcast")


    def prepairSend(self, payload, broadcast=False):
        payload["id"] = self.id

        payload["broadcast"] = broadcast

        return payload


    def sendBulk(self, payloads, broadcast=False):
        prepared_payloads = []

        for load in payloads:
            prepared_payloads.append(
                    self.prepairSend(load) )

        payload = {
            "type": "command",
            "key" : "bulk",
            "frames": prepared_payloads
        }
        self.send(payload, broadcast)

    def send(self, payload,broadcast=False):
        payload = self.prepairSend(payload, broadcast)
        payload = json.dumps(payload, ensure_ascii=False).encode("utf8")
        self.sendMessage(payload)


    def ping(self):
        if self.verbose:
            print("Ping!")
        self.send({"type": "ping"})


class BroadcastClientFactory(WebSocketClientFactory):

    protocol = BroadcastClientProtocol

    def __init__(self, verbose):
        WebSocketClientFactory.__init__(self)
        self.client = None
        self.verbose = verbose
        self.trigger_tick_cb = None

    def _registerClient(self, client):
        self.client = client
        self.client.trigger_tick_cb = self.trigger_tick_cb

    def _unregisterClient(self, client):
        self.client = None

    def send(self, payload, broadcast=False):
        if self.client:
            self.client.send(payload, broadcast)
        else:
            if self.verbose:
                print("Attempted to send when no client connection has been established.")

    def sendBulk(self, payload, broadcast=False):
        if self.client:
            self.client.sendBulk(payload, broadcast)
        else:
            if self.verbose:
                print("Attempted to send when no client connection has been established.")

    def ping(self):
        if self.client:
            self.client.ping()
        else:
            if self.verbose:
                print("Attempted to send ping when no client connection has been established.")

    def subscribe(self, channel, callback):
        if channel not in self.subscriptions:
            if self.verbose:
                print("Invalid channel name \"{}\". Subscription failed.".format(channel))
        else:
            self.subscriptions[channel].append(callback)

    def unsubscribe(self, channel, callback):
        if channel not in self.subscriptions:
            if self.verbose:
                print("Invalid channel name \"{}\". Unsubscribe failed.".format(channel))
        else:
            for cb in self.subscriptions[channel]:
                if cb == callback:
                    self.subscriptions[channel].remove(cb)


    def _get_subscribers(self, channel):
        if channel not in self.subscriptions:
            if self.verbose:
                print("Attempted to handle undefined subscription type: {}".format(channel))
            return None
        return self.subscriptions[channel]


def start_client(host, port, client_logic, verbose=False):

    try:
       import asyncio
    except ImportError:
       ## Trollius >= 0.3 was renamed
       import trollius as asyncio

    if verbose:
        print("Client attempting to connect to {}:{}".format(host, port))

    factory = BroadcastClientFactory(verbose)

    factory.trigger_tick_cb = client_logic.tick
    factory.trigger_initialize_cb = client_logic.initialize
    factory.notify_game_started_cb = client_logic.notify_game_started
    factory.notify_game_over_cb = client_logic.notify_game_over

    loop = asyncio.get_event_loop()

    client_logic.set_loop(loop)
    client_logic.set_socket_client(factory)
    #loop.call_soon(client_logic.tick)

    coro = loop.create_connection(factory, host, port)
    client = loop.run_until_complete(coro)

    loop.run_forever()
