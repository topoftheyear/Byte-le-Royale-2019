import sys
import random
import math

from game.utils.helpers import *
from game.common.stats import *
from game.common.illegal_salvage import IllegalSalvage

class IllegalSalvageController:

    def __init__(self):

        self.debug = False
        self.events = []
        self.stats = []

        self.material_prices = None

    def print(self, msg):
        if self.debug:
            print('IllegalSalvageController: ' + str(msg))
            sys.stdout.flush()

    def get_events(self):
        e = self.events
        self.events = []
        return e

    def get_stats(self):
        s = self.stats
        self.stats = []
        return s

    def handle_actions(self, living_ships, universe, teams, npc_teams):
        self.material_prices = None

        for team, data in { **teams, **npc_teams}.items():
            ship = data["ship"]

            # Check for ships that are performing the drop cargo action
            if ship.action is PlayerAction.drop_cargo:
                self.print('dropping illegal salvage...')

                if not ship.is_alive():
                    continue

                material_type = ship.action_param_1
                amount = ship.action_param_2

                if material_type not in ship.inventory:
                    continue

                inventory = ship.inventory[material_type]
                amount_left = max(0, inventory-amount)
                amount_dropped = inventory - amount_left

                ship.inventory[material_type] = amount_left

                self.material_prices = get_material_prices(universe)
                material_amount = self.material_prices[material_type]

                random_position = (
                    ship.position[0] + random.randint(-5, 5),
                    ship.position[1] + random.randint(-5, 5)
                )
                new_illegal_salvage = IllegalSalvage()
                new_illegal_salvage.init(position=random_position, amount=material_amount)

                universe.add_object(new_illegal_salvage)
                self.print('Created new illegal salvage at {} with amount {}CR'.format(random_position, material_amount))

                self.events.append({
                    "type": LogEvent.illegal_salvage_spawned,
                    "id": new_illegal_salvage.id,
                    "position": new_illegal_salvage.position
                })

                # Logging
                self.events.append({
                    "type": LogEvent.cargo_dropped,
                    "ship_id": ship.id,
                    "amount": amount
                })

            # Check for ships performing the salvage action
            elif ship.action is PlayerAction.collect_illegal_salvage:

                if not ship.is_alive():
                    continue

                salvage = None
                salvage_list = universe.get(ObjectType.illegal_salvage)
                for scrap in salvage_list:
                    ship_in_radius = in_radius(
                        scrap,
                        ship,
                        ship.weapon_range,
                        lambda e: e.position)

                    if ship_in_radius:
                        salvage = scrap
                        break
                else:
                    self.print('No illegal salvage found nearby')
                    continue

                # Check if salvage pile is already empty just in case
                if salvage.amount == 0:
                    self.print('Found illegal salvage has no amount')
                    continue

                # TODO determine balanced pickup rate
                pickup_rate = random.randint(1, 11) // 1

                pickup_amount = 0
                if salvage.amount >= pickup_rate:
                    pickup_amount = pickup_rate
                elif salvage.amount < pickup_rate:
                    pickup_amount = salvage.amount

                # Ensure cargo is not exceeded
                current_capacity = sum(ship.inventory.values())
                new_capacity = min(current_capacity + pickup_amount, ship.cargo_space)
                pickup_amount = new_capacity - current_capacity

                salvage.amount -= pickup_amount
                if MaterialType.salvage not in ship.inventory:
                    ship.inventory[MaterialType.salvage] = 0
                ship.inventory[MaterialType.salvage] += pickup_amount

                self.print('Illegal salvage collected')

                # Logging
                self.events.append({
                    "type": LogEvent.illegal_salvage_picked_up,
                    "ship_id": ship.id,
                })

                self.stats.append({
                    "ship_id": ship.id,
                    "material": MaterialType.salvage,
                    "yield": pickup_amount
                })





        # for now we will decay salvage until garbage collectior is finished.
        for salvage in universe.get(ObjectType.illegal_salvage):
            salvage.turns_till_recycling -= 1

            if salvage.turns_till_recycling <= 0 or salvage.amount <= 0:
                universe.remove_object(salvage)
                del salvage

