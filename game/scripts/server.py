import click

from game.server import start


@click.command()
@click.option("--server-verbose", is_flag=True)
@click.option("--port", default=8080)
@click.option("--no-wait", is_flag=True, help="Prevents server from waiting on client response for longer than configured turn time.")
def main(server_verbose, port, no_wait):

    if server_verbose:
        print("Server Verbosity: ON")

    start(server_verbose, port, no_wait)

if __name__ == "__main__":
    main()
