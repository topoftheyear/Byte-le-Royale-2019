import sys

from game.visualizer import start

import click

@click.command()
@click.option("--verbose", is_flag=True)
@click.option("--log-path", default="./game_log")
@click.option("--gamma", default=1.0)
@click.option("--dont-wait", is_flag=True)
@click.option("--fullscreen", is_flag=True)
def main(verbose, log_path, gamma, dont_wait, fullscreen):

    start(verbose, log_path, gamma, dont_wait, fullscreen)

if __name__ == "__main__":

    main()
