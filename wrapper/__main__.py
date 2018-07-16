import click



@click.group()
def cli():
    pass


@cli.command()
@click.option("--server-verbose", is_flag=True)
@click.option("--port", default=8080)
@click.option("--no-wait", is_flag=True, help="Prevents server from waiting on client response for longer than configured turn time.")
def server(server_verbose, port, no_wait):
    from game.server import start

    if server_verbose:
        print("Server Verbosity: ON")

    start(server_verbose, port, no_wait)




@cli.command()
@click.option("--client-verbose", is_flag=True)
@click.option("--script", default="custom_client")
@click.option("--port", default=8080)
def client(client_verbose, client, port):
    from game.client import start
    from game.client.client_logic import ClientLogic

    if client_verbose:
        print("Client Verbosity: ON")

    mod = importlib.import_module(client)

    start(ClientLogic(client_verbose, mod.CustomClient()), client_verbose, port)


@cli.command()
def generate():
    from game.utils.generate_game import generate as gen_data
    gen_data()


@click.command()
@click.option("--verbose", is_flag=True)
@click.option("--log-path", default="./game_log")
@click.option("--gamma", default=1.0)
@click.option("--dont-wait", is_flag=True)
@click.option("--fullscreen", is_flag=True)
def visualizer(verbose, log_path, gamma, dont_wait, fullscreen):
    from game.visualizer import start

    start(verbose, log_path, gamma, dont_wait, fullscreen)


if __name__ == "__main__":
    cli()
