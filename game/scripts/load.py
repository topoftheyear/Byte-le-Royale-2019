from game.common.node_types import *
from game.utils.network_visualizer import visualize
from game.utils.generate_game import load

def main():
    nodes = load()

    visualize(nodes)

if __name__ == "__main__":
    main()
