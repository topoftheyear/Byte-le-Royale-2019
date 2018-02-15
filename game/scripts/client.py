import importlib
import click

from game.client import start
from game.client.client_logic import ClientLogic
#from custom_client import CustomClient


@click.command()
@click.option("--client-verbose", is_flag=True)
@click.option("--client", default="custom_client")
@click.option("--port", default=8080)
def main(client_verbose, client, port):

    if client_verbose:
        print("Client Verbosity: ON")

    mod = importlib.import_module(client)

    start(ClientLogic(client_verbose, mod.CustomClient()), client_verbose, port)

if __name__ == "__main__":
    main()
