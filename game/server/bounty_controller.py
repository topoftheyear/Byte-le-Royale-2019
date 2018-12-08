import sys
import math

from game.utils.helpers import *

class BountyController:

    def __init__(self):

        self.debug = True
        self.events = []
        self.stats = []

        self.material_prices = None

    def print(self, msg):
        if self.debug:
            print('BountyController: ' + str(msg))
            sys.stdout.flush()

    def get_events(self):
        e = self.events
        self.events = []
        return e

    def get_stats(self):
        s = self.stats
        self.stats = []
        return s

    def clear_bounty(self, ship):
        for bounty in ship.bounty_list:
            if bounty["bounty_type"] is not BountyType.became_pirate:
                ship.bounty_list.remove(bounty)
        self.print(f"Bounties removed from ship {ship.id}")

    def handle_actions(self, living_ships, universe, teams, npc_teams):
        for team, data in { **teams, **npc_teams}.items():
            ship = data["ship"]

            if ship.is_alive():
                # Determine new bounty if ship is not a pirate
                if ship.legal_standing < LegalStanding.pirate:
                    ship.bounty = 0
                    continue

                # Determine new bounty total
                new_bounty = 0

                # Sum the value of all bounties currently held
                for bounty in ship.bounty_list:
                    if bounty["bounty_type"] is BountyType.scrap_sold:
                        # Scrap sold has its bounty value reduced by 0.2% multiplied by number of ticks since it occurred
                        # TODO determine balanced rate to diminish scrap value by
                        ratio = 1 - (0.002 * bounty["age"])
                        if ratio <= 0:
                            ship.bounty_list.remove(bounty)
                            continue
                        new_bounty += ratio * bounty["value"]

                        bounty["age"] += 1
                    else:
                        new_bounty += bounty["value"]

                # Only performing the ceiling one time to maintain accuracy
                ship.bounty = math.ceil(new_bounty)
                self.print(f"New bounty of {new_bounty} determined for ship: {ship.id}")

            else:
                self.clear_bounty(ship)
