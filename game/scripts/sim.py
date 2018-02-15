from game.common.node_types import *
from game.common.unit_classes import *
from game.common.item_types import *
from game.common.items import *
from game.server.combat import CombatManager
from game.utils.network_visualizer import visualize
from game.utils.generate_game import load


def main():

    turns = load()

    num_turns = len(turns)

    current_turn = turns.pop(0)
    current_node = current_turn[0]

    monsters_faced = 0
    traps_faced = 0


    num_units = 3
    units = []
    names = [ "a", "b", "c", "d" , "e" ]
    class_types = [ Knight, Brawler, Pikeman, Rogue ]

    print("Unit Line-up")
    for i in range(num_units):
        u = class_types[i]()
        u.init( names[i] )

        # give unit a sword
        s = get_item(ItemClass.melee, ItemType.sword, 1)
        s.init(1)
        u.items.append(s)

        units.append(u)
        print(u)

    turn_no = 1

    while turn_no < num_turns:
        print()
        print("#"*10)
        print("Turn: {}".format(turn_no))
        print("#"*10)

        # handle current room

        if isinstance(current_node, Town):

            print("Town")

            for u in units:
                u.reset_health()

            print("Press Enter to continue...")
            input()

        elif isinstance(current_node, MonsterRoom):
            monsters_faced += 1
            print("Combat against {}".format(current_node.monster.get_description()))
            print("Press enter to continue")
            input()

            combat_manager = CombatManager()

            combat_manager.print_summary(current_node.monster, units)

            while not combat_manager.done:

                input()
                combat_manager.play_round(current_node.monster, units)
                combat_manager.print_summary(current_node.monster, units)

            print()
            print(combat_manager.done_reason)

            if combat_manager.success is not None:
                if combat_manager.success is True:
                    input()
                elif combat_manager.success is False:
                    exit()


        elif isinstance(current_node, TrapRoom):
            traps_faced += 1
            print("Navgating trap {}".format(current_node.trap.get_description()))
            print("Press enter to continue")
            input()


        # Decision time

        if len(current_node.nodes) == 1:
            s = None
            while s != "f":
                print()
                print("You see a door.")
                print("f: {}".format(current_node.nodes[0].get_description()))
                s = input("Direction: ")
            current_node = current_node.nodes[0]

        elif len(current_node.nodes) == 2:
            sides = ["l", "r"]

            s = None
            while s not in sides:
                print()
                print("You see two doors.")
                for side, node in zip(sides, current_node.nodes):
                    print("{}: {}".format(side, node.get_description()))
                s = input("Direction: ")

            current_node = current_node.nodes[sides.index(s)]

        turn_no += 1

    print()
    print("#"*20)
    print("End of Run")
    print("#"*20)
    print("{} Monsters Killed".format(monsters_faced))
    print("{} Traps Evaded".format(traps_faced))


if __name__ == "__main__":
    main()
