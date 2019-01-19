import sys

from game.client.broadcast_client import start_client
from game.client.custom_client import CustomClient

def start(client, verbose=False, port=9000, host="127.0.0.1"):
    start_client(host, str(port), client, verbose)

