from autobahn.asyncio.websocket import WebSocketServerProtocol
from autobahn.asyncio.websocket import WebSocketServerFactory

import os
import json

class BroadcastServerProtocol(WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        super(WebSocketServerProtocol, self).__init__(*args, **kwargs)

        self.clients = []
        self.verbose = False

    def onOpen(self):
        self.factory.register(self)

        # copy verbosity
        self.verbose = self.factory.verbose
        if self.verbose:
            print("Client Connected")

    def onConnect(self, client):
        if self.verbose:
            print("Client connecting: {}".format(client.peer))
        self.clients.append(client)

    def onClose(self, wasClean, code, reason):
        if self.verbose:
            print("Client connection closed: {}".format(reason))
        self.factory.unregister(self)


    def onMessage(self, payload, isBinary):

        # deserialize json
        obj = json.loads(payload.decode("utf8"))

        if(obj["type"] == "ping"):
            self.send({"type": "pong"})

        elif(obj["type"] == "register"):
            self.register(obj["id"])
            self.factory.notify_client_connect_cb(obj["id"])

        elif obj["type"] == "client_turn":
            self.factory.notify_client_turn_cb(obj["payload"])


    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def register(self, id):
        self.clients.append(id)

    def broadcast(self, payload):
        self.send(payload, broadcast=True)


    def send(self, payload, broadcast=False):

        _payload = json.dumps(payload, ensure_ascii=False).encode("utf8")

        if broadcast:
            self.factory.broadcast(_payload)
        else:
            self.sendMessage(_payload)

    def getState(self, key):
        return self.factory.state[key]

    def setState(self, key, value):
        self.factory.state[key] = value



class BroadcastServerFactory(WebSocketServerFactory):

    protocol = BroadcastServerProtocol


    def __init__(self, verbose=False):
        WebSocketServerFactory.__init__(self)

        self.verbose = verbose
        self.clients = []


    def register(self, client):
        if client not in self.clients:
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def sendAll(self, payload):
        if len(self.clients) > 0:
            self.clients[0].broadcast(payload)

    def broadcast(self, payload):
        for c in self.clients:
            c.sendMessage(payload)

    def close(self):
        for c in self.clients:
            c.sendClose()




def start_server(host, port, server_logic, verbose=False):

   try:
      import asyncio
   except ImportError:
      ## Trollius >= 0.3 was renamed
      import trollius as asyncio


   factory = BroadcastServerFactory(verbose)

   factory.notify_client_connect_cb = server_logic.notify_client_connect
   factory.notify_client_turn_cb = server_logic.notify_client_turn

   loop = asyncio.get_event_loop()
   coro = loop.create_server(factory, host, port)
   server = loop.run_until_complete(coro)

   server_logic.set_loop(loop)
   server_logic.set_socket_client(factory)

   loop.call_soon(server_logic.wait_for_clients)

   try:
      loop.run_forever()
   except KeyboardInterrupt:
      pass
   finally:
      server.close()
      loop.close()
