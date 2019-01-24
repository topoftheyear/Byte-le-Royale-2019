
import sys

from game.server.broadcast_server import start_server
from game.server.custom_server import CustomServer


def start(
        verbose=False,
        port=9000,
        no_wait=False,
        connection_wait_timer=3,
        wait_timeout=600,
        game_length=1000):

    server_logic = CustomServer(
            verbose=verbose,
            wait_on_client=not no_wait,
            connection_wait_timer=connection_wait_timer,
            wait_timer=wait_timeout,
            max_game_tick=game_length)

    start_server("0.0.0.0", str(port), server_logic, verbose=verbose)
